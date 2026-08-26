//! Exact, read-only round849 -> round850 rare-order index gate.
//!
//! This is deliberately a sibling of the production affine251 source.  It
//! streams the two frozen vector caches, compares the existing full natural
//! `(frequency, Mono)` sort with an incremental frequency-bucket index, and
//! never writes a checkpoint or vector cache.

use std::collections::{HashMap, HashSet};
use std::convert::TryFrom;
use std::env;
use std::fs::{self, File};
use std::io::{BufReader, BufWriter, Read, Write};
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::time::Instant;

const MAX_DEGREE: usize = 12;
const N_WORDS: usize = 6561;
const SPARSE_VECTOR_MAGIC: &[u8; 12] = b"AFF12VEC1\0\0\0";
const NONE_FREQUENCY: u32 = u32::MAX;

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Mono {
    len: u8,
    ids: [u8; MAX_DEGREE],
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Column {
    word: u16,
    multiplier: Mono,
}

#[derive(Clone, Copy)]
struct Entry {
    current: u32,
    committed: u32,
}

struct RareOrderIndex {
    entries: HashMap<Mono, Entry>,
    buckets: Vec<Vec<Mono>>,
    touched: HashSet<Mono>,
}

impl RareOrderIndex {
    fn from_frequency(frequency: HashMap<Mono, u32>) -> Self {
        let max_frequency = frequency.values().copied().max().unwrap_or(0) as usize;
        let mut buckets = vec![Vec::new(); max_frequency + 1];
        let mut entries = HashMap::with_capacity(frequency.len());
        for (row, count) in frequency {
            assert!(
                count > 0 && count != NONE_FREQUENCY,
                "invalid initial frequency"
            );
            buckets[count as usize].push(row);
            assert!(entries
                .insert(
                    row,
                    Entry {
                        current: count,
                        committed: count
                    }
                )
                .is_none());
        }
        for bucket in &mut buckets {
            bucket.sort_unstable();
            assert_strict(bucket, "initial bucket");
        }
        let answer = Self {
            entries,
            buckets,
            touched: HashSet::new(),
        };
        assert_eq!(
            answer.bucket_count(),
            answer.entries.len(),
            "initial index census"
        );
        answer
    }

    fn bump(&mut self, row: Mono) {
        let entry = self.entries.entry(row).or_insert(Entry {
            current: 0,
            committed: NONE_FREQUENCY,
        });
        entry.current = entry.current.checked_add(1).expect("frequency overflow");
        assert!(
            entry.current != NONE_FREQUENCY,
            "frequency reserved-value collision"
        );
        self.touched.insert(row);
    }

    fn commit(&mut self) -> CommitStats {
        let touched = self.touched.len();
        let required = self
            .entries
            .values()
            .map(|entry| entry.current)
            .max()
            .unwrap_or(0) as usize
            + 1;
        if self.buckets.len() < required {
            self.buckets.resize_with(required, Vec::new);
        }
        let mut removals = vec![Vec::<Mono>::new(); self.buckets.len()];
        let mut additions = vec![Vec::<Mono>::new(); self.buckets.len()];
        for row in self.touched.drain() {
            let entry = self.entries.get_mut(&row).expect("touched row absent");
            if entry.committed != entry.current {
                if entry.committed != NONE_FREQUENCY {
                    removals[entry.committed as usize].push(row);
                }
                additions[entry.current as usize].push(row);
                entry.committed = entry.current;
            }
        }

        let mut dirty_buckets = 0usize;
        let mut merged_old_rows = 0usize;
        let mut removed_rows = 0usize;
        let mut added_rows = 0usize;
        for frequency in 0..self.buckets.len() {
            if removals[frequency].is_empty() && additions[frequency].is_empty() {
                continue;
            }
            dirty_buckets += 1;
            removals[frequency].sort_unstable();
            additions[frequency].sort_unstable();
            assert_strict(&removals[frequency], "removal delta");
            assert_strict(&additions[frequency], "addition delta");
            let old = std::mem::take(&mut self.buckets[frequency]);
            merged_old_rows += old.len();
            removed_rows += removals[frequency].len();
            added_rows += additions[frequency].len();

            let mut retained = Vec::with_capacity(old.len() - removals[frequency].len());
            let mut removal = 0usize;
            for row in old {
                if removal < removals[frequency].len() && removals[frequency][removal] == row {
                    removal += 1;
                } else {
                    assert!(
                        removal == removals[frequency].len() || removals[frequency][removal] > row,
                        "removal delta is not a subset of committed bucket"
                    );
                    retained.push(row);
                }
            }
            assert_eq!(
                removal,
                removals[frequency].len(),
                "removal delta is not exhausted by committed bucket"
            );

            let additions = &additions[frequency];
            let mut merged = Vec::with_capacity(retained.len() + additions.len());
            let (mut left, mut right) = (0usize, 0usize);
            while left < retained.len() || right < additions.len() {
                if right == additions.len()
                    || (left < retained.len() && retained[left] < additions[right])
                {
                    merged.push(retained[left]);
                    left += 1;
                } else {
                    assert!(
                        left == retained.len() || additions[right] < retained[left],
                        "addition collides with retained row"
                    );
                    merged.push(additions[right]);
                    right += 1;
                }
            }
            assert_strict(&merged, "committed bucket");
            self.buckets[frequency] = merged;
        }
        assert_eq!(
            self.bucket_count(),
            self.entries.len(),
            "post-commit index census"
        );
        CommitStats {
            touched,
            dirty_buckets,
            merged_old_rows,
            removed_rows,
            added_rows,
        }
    }

    fn bucket_count(&self) -> usize {
        self.buckets.iter().map(Vec::len).sum()
    }

    fn indexed_order(&self) -> Vec<(u32, Mono)> {
        let mut answer = Vec::with_capacity(self.entries.len());
        for (frequency, bucket) in self.buckets.iter().enumerate() {
            let frequency = u32::try_from(frequency).expect("bucket frequency overflow");
            for &row in bucket {
                answer.push((frequency, row));
            }
        }
        answer
    }

    fn baseline_order(&self) -> Vec<(u32, Mono)> {
        let mut answer: Vec<_> = self
            .entries
            .iter()
            .map(|(&row, entry)| (entry.current, row))
            .collect();
        answer.sort_unstable();
        assert_strict(&answer, "baseline order");
        answer
    }
}

#[derive(Clone, Copy)]
struct CommitStats {
    touched: usize,
    dirty_buckets: usize,
    merged_old_rows: usize,
    removed_rows: usize,
    added_rows: usize,
}

struct CacheStats {
    prime: u64,
    provider: u64,
    fingerprint: u64,
    records: usize,
    terms: u64,
}

struct Config {
    old_cache: PathBuf,
    new_cache: PathBuf,
    output: PathBuf,
    expected_old_records: usize,
    expected_new_records: usize,
    expected_new_columns: usize,
    wall_seconds: f64,
    rss_gib: u64,
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("FAIL: {}", message.as_ref());
    std::process::exit(1)
}

fn assert_strict<T: Ord>(values: &[T], label: &str) {
    if values.windows(2).any(|pair| pair[0] >= pair[1]) {
        fail(format!("{label} is not strict"));
    }
}

fn read_u64<R: Read>(input: &mut R) -> u64 {
    let mut bytes = [0u8; 8];
    input
        .read_exact(&mut bytes)
        .unwrap_or_else(|error| fail(error.to_string()));
    u64::from_le_bytes(bytes)
}

fn read_mono<R: Read>(input: &mut R) -> Mono {
    let mut len = [0u8; 1];
    let mut ids = [0u8; MAX_DEGREE];
    input
        .read_exact(&mut len)
        .unwrap_or_else(|error| fail(error.to_string()));
    input
        .read_exact(&mut ids)
        .unwrap_or_else(|error| fail(error.to_string()));
    if len[0] as usize > MAX_DEGREE
        || !ids[..len[0] as usize]
            .windows(2)
            .all(|pair| pair[0] <= pair[1])
        || ids[len[0] as usize..].iter().any(|&id| id != 0)
    {
        fail("bad cache monomial");
    }
    Mono { len: len[0], ids }
}

fn hash_bytes(mut hash: u64, bytes: &[u8]) -> u64 {
    for byte in bytes {
        hash ^= *byte as u64;
        hash = hash.wrapping_mul(1_099_511_628_211);
    }
    hash
}

fn scan_cache<F>(path: &Path, mut consume: F) -> CacheStats
where
    F: FnMut(Column, &[(Mono, u64)]),
{
    let mut input = BufReader::with_capacity(
        1 << 20,
        File::open(path).unwrap_or_else(|error| fail(error.to_string())),
    );
    let mut magic = [0u8; 12];
    input
        .read_exact(&mut magic)
        .unwrap_or_else(|error| fail(error.to_string()));
    if &magic != SPARSE_VECTOR_MAGIC {
        fail("sparse vector magic mismatch");
    }
    let prime = read_u64(&mut input);
    let provider = read_u64(&mut input);
    let expected_fingerprint = read_u64(&mut input);
    let records_u64 = read_u64(&mut input);
    let records = usize::try_from(records_u64).unwrap_or_else(|_| fail("record count overflow"));
    let mut fingerprint = 14_695_981_039_346_656_037u64;
    let mut previous_column = None;
    let mut terms = 0u64;
    for _ in 0..records {
        let mut bytes = [0u8; 2];
        input
            .read_exact(&mut bytes)
            .unwrap_or_else(|error| fail(error.to_string()));
        let column = Column {
            word: u16::from_le_bytes(bytes),
            multiplier: read_mono(&mut input),
        };
        let size_u64 = read_u64(&mut input);
        let size = usize::try_from(size_u64).unwrap_or_else(|_| fail("vector size overflow"));
        if column.word as usize >= N_WORDS || column.multiplier.len != 8 || size > 700_000 {
            fail("bad sparse vector cache record");
        }
        if previous_column.is_some_and(|old| old >= column) {
            fail("cache columns are not strict");
        }
        previous_column = Some(column);
        fingerprint = hash_bytes(fingerprint, &column.word.to_le_bytes());
        fingerprint = hash_bytes(fingerprint, &[column.multiplier.len]);
        fingerprint = hash_bytes(fingerprint, &column.multiplier.ids);
        fingerprint = hash_bytes(fingerprint, &size_u64.to_le_bytes());
        let mut vector = Vec::with_capacity(size);
        let mut previous_row = None;
        for _ in 0..size {
            let row = read_mono(&mut input);
            let value = read_u64(&mut input);
            if row.len != 12
                || value == 0
                || value >= prime
                || previous_row.is_some_and(|old| old >= row)
            {
                fail("bad sparse cached vector");
            }
            previous_row = Some(row);
            fingerprint = hash_bytes(fingerprint, &[row.len]);
            fingerprint = hash_bytes(fingerprint, &row.ids);
            fingerprint = hash_bytes(fingerprint, &value.to_le_bytes());
            vector.push((row, value));
        }
        terms = terms.checked_add(size_u64).expect("term count overflow");
        consume(column, &vector);
    }
    let mut trailing = [0u8; 1];
    if input
        .read(&mut trailing)
        .unwrap_or_else(|error| fail(error.to_string()))
        != 0
    {
        fail("trailing sparse vector bytes");
    }
    if fingerprint != expected_fingerprint {
        fail("sparse vector cache checksum mismatch");
    }
    CacheStats {
        prime,
        provider,
        fingerprint,
        records,
        terms,
    }
}

fn order_sha256(order: &[(u32, Mono)]) -> String {
    let mut child = Command::new("shasum")
        .args(["-a", "256"])
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .unwrap_or_else(|error| fail(format!("cannot launch shasum: {error}")));
    {
        let mut input =
            BufWriter::with_capacity(1 << 20, child.stdin.take().expect("shasum stdin"));
        for &(frequency, row) in order {
            input
                .write_all(&frequency.to_le_bytes())
                .unwrap_or_else(|error| fail(error.to_string()));
            input
                .write_all(&[row.len])
                .unwrap_or_else(|error| fail(error.to_string()));
            input
                .write_all(&row.ids)
                .unwrap_or_else(|error| fail(error.to_string()));
        }
        input
            .flush()
            .unwrap_or_else(|error| fail(error.to_string()));
    }
    let output = child
        .wait_with_output()
        .unwrap_or_else(|error| fail(error.to_string()));
    if !output.status.success() {
        fail("shasum failed");
    }
    let text = String::from_utf8(output.stdout).unwrap_or_else(|error| fail(error.to_string()));
    let hash = text
        .split_whitespace()
        .next()
        .unwrap_or_else(|| fail("empty shasum output"));
    if hash.len() != 64 || !hash.bytes().all(|byte| byte.is_ascii_hexdigit()) {
        fail("malformed shasum output");
    }
    hash.to_ascii_lowercase()
}

fn current_rss_kib() -> u64 {
    let pid = std::process::id().to_string();
    let output = match Command::new("ps").args(["-o", "rss=", "-p", &pid]).output() {
        Ok(output) => output,
        Err(_) => return 0,
    };
    String::from_utf8(output.stdout)
        .ok()
        .and_then(|text| text.trim().parse().ok())
        .unwrap_or(0)
}

fn gate(started: Instant, wall_seconds: f64, rss_limit_kib: u64, peak: &mut u64, phase: &str) {
    *peak = (*peak).max(current_rss_kib());
    if started.elapsed().as_secs_f64() >= wall_seconds {
        fail(format!("WALL_CAP after {phase}"));
    }
    if *peak >= rss_limit_kib {
        fail(format!("RSS_CAP after {phase}"));
    }
}

fn parse_config() -> Config {
    let mut args = env::args().skip(1);
    let mut values = HashMap::<String, String>::new();
    while let Some(key) = args.next() {
        if key == "--self-test" {
            return Config {
                old_cache: PathBuf::new(),
                new_cache: PathBuf::new(),
                output: PathBuf::new(),
                expected_old_records: 0,
                expected_new_records: 0,
                expected_new_columns: 0,
                wall_seconds: 0.0,
                rss_gib: 0,
            };
        }
        let value = args
            .next()
            .unwrap_or_else(|| fail(format!("missing value after {key}")));
        values.insert(key, value);
    }
    let take = |key: &str| {
        values
            .get(key)
            .cloned()
            .unwrap_or_else(|| fail(format!("missing {key}")))
    };
    Config {
        old_cache: take("--old-cache").into(),
        new_cache: take("--new-cache").into(),
        output: take("--output").into(),
        expected_old_records: take("--expected-old-records")
            .parse()
            .unwrap_or_else(|_| fail("bad old records")),
        expected_new_records: take("--expected-new-records")
            .parse()
            .unwrap_or_else(|_| fail("bad new records")),
        expected_new_columns: take("--expected-new-columns")
            .parse()
            .unwrap_or_else(|_| fail("bad new columns")),
        wall_seconds: take("--wall-seconds")
            .parse()
            .unwrap_or_else(|_| fail("bad wall seconds")),
        rss_gib: take("--rss-gib")
            .parse()
            .unwrap_or_else(|_| fail("bad rss GiB")),
    }
}

fn sample_mono(ids: &[u8]) -> Mono {
    let mut packed = [0u8; MAX_DEGREE];
    packed[..ids.len()].copy_from_slice(ids);
    Mono {
        len: ids.len() as u8,
        ids: packed,
    }
}

fn self_test() {
    let a = sample_mono(&[1, 2]);
    let b = sample_mono(&[1, 3]);
    let c = sample_mono(&[2]);
    let d = sample_mono(&[1, 2, 3]);
    let mut index = RareOrderIndex::from_frequency(HashMap::from([(b, 1), (a, 1), (c, 2)]));
    assert_eq!(index.baseline_order(), index.indexed_order());
    index.bump(a);
    index.bump(a);
    index.bump(b);
    index.bump(d);
    index.bump(d);
    let stats = index.commit();
    assert_eq!(stats.touched, 3);
    assert_eq!(index.baseline_order(), index.indexed_order());
    let before = index.indexed_order();
    let empty = index.commit();
    assert_eq!(empty.touched, 0);
    assert_eq!(before, index.indexed_order());
    println!(
        "PASS_SELF_TEST mono_size={} tuple_size={}",
        std::mem::size_of::<Mono>(),
        std::mem::size_of::<(u32, Mono)>()
    );
}

fn main() {
    let config = parse_config();
    if config.old_cache.as_os_str().is_empty() {
        self_test();
        return;
    }
    if config.wall_seconds <= 0.0 || config.rss_gib == 0 || config.rss_gib > 36 {
        fail("invalid hard gate");
    }
    let started = Instant::now();
    let rss_limit_kib = config.rss_gib * 1024 * 1024;
    let mut peak_rss_kib = current_rss_kib();
    let target = Mono {
        len: 12,
        ids: [251; 12],
    };

    let old_scan_started = Instant::now();
    let mut frequency = HashMap::<Mono, u32>::new();
    let mut old_columns = HashSet::<Column>::with_capacity(config.expected_old_records);
    let old_stats = scan_cache(&config.old_cache, |column, vector| {
        if !old_columns.insert(column) {
            fail("duplicate old column");
        }
        for &(row, coefficient) in vector {
            if row != target && coefficient != 0 {
                let count = frequency.entry(row).or_default();
                *count = count.checked_add(1).expect("initial frequency overflow");
            }
        }
    });
    let old_scan_seconds = old_scan_started.elapsed().as_secs_f64();
    if old_stats.records != config.expected_old_records {
        fail("old record count mismatch");
    }
    gate(
        started,
        config.wall_seconds,
        rss_limit_kib,
        &mut peak_rss_kib,
        "old cache scan",
    );

    let initial_build_started = Instant::now();
    let mut index = RareOrderIndex::from_frequency(frequency);
    let old_ranked_rows = index.entries.len();
    let initial_build_seconds = initial_build_started.elapsed().as_secs_f64();
    gate(
        started,
        config.wall_seconds,
        rss_limit_kib,
        &mut peak_rss_kib,
        "initial index build",
    );

    let old_compare_started = Instant::now();
    let old_baseline = index.baseline_order();
    gate(
        started,
        config.wall_seconds,
        rss_limit_kib,
        &mut peak_rss_kib,
        "old baseline sort",
    );
    let old_indexed = index.indexed_order();
    if old_baseline != old_indexed {
        fail("round849 indexed order differs from baseline");
    }
    let old_order_sha256 = order_sha256(&old_baseline);
    let old_compare_seconds = old_compare_started.elapsed().as_secs_f64();
    drop(old_baseline);
    drop(old_indexed);
    gate(
        started,
        config.wall_seconds,
        rss_limit_kib,
        &mut peak_rss_kib,
        "old order compare",
    );

    let new_scan_started = Instant::now();
    let mut seen_old = HashSet::<Column>::with_capacity(config.expected_old_records);
    let mut new_columns_seen = 0usize;
    let new_stats = scan_cache(&config.new_cache, |column, vector| {
        if old_columns.contains(&column) {
            if !seen_old.insert(column) {
                fail("duplicate inherited new-cache column");
            }
        } else {
            new_columns_seen += 1;
            for &(row, coefficient) in vector {
                if row != target && coefficient != 0 {
                    index.bump(row);
                }
            }
        }
    });
    let new_scan_seconds = new_scan_started.elapsed().as_secs_f64();
    if new_stats.records != config.expected_new_records
        || new_columns_seen != config.expected_new_columns
        || seen_old.len() != old_columns.len()
        || old_stats.prime != new_stats.prime
        || old_stats.provider != new_stats.provider
    {
        fail("round850 cache descendant/count/header mismatch");
    }
    drop(seen_old);
    drop(old_columns);
    gate(
        started,
        config.wall_seconds,
        rss_limit_kib,
        &mut peak_rss_kib,
        "new cache scan",
    );

    let incremental_started = Instant::now();
    let commit_stats = index.commit();
    let incremental_commit_seconds = incremental_started.elapsed().as_secs_f64();
    gate(
        started,
        config.wall_seconds,
        rss_limit_kib,
        &mut peak_rss_kib,
        "incremental commit",
    );

    let new_baseline_started = Instant::now();
    let new_baseline = index.baseline_order();
    let new_baseline_sort_seconds = new_baseline_started.elapsed().as_secs_f64();
    gate(
        started,
        config.wall_seconds,
        rss_limit_kib,
        &mut peak_rss_kib,
        "new baseline sort",
    );
    let new_indexed_started = Instant::now();
    let new_indexed = index.indexed_order();
    let new_indexed_flatten_seconds = new_indexed_started.elapsed().as_secs_f64();
    if new_baseline != new_indexed {
        fail("round850 indexed order differs from baseline");
    }
    let new_order_sha256 = order_sha256(&new_baseline);
    let ranked_rows = new_baseline.len();
    drop(new_baseline);
    drop(new_indexed);
    gate(
        started,
        config.wall_seconds,
        rss_limit_kib,
        &mut peak_rss_kib,
        "new order compare",
    );

    let elapsed_seconds = started.elapsed().as_secs_f64();
    let tmp = config.output.with_extension("json.tmp");
    let mut out =
        BufWriter::new(File::create(&tmp).unwrap_or_else(|error| fail(error.to_string())));
    writeln!(out, "{{").unwrap();
    writeln!(
        out,
        "  \"schema\": \"KRENN_AFF251_D12_RARE_ORDER_INDEX_GATE_V1\","
    )
    .unwrap();
    writeln!(
        out,
        "  \"status\": \"PASS_EXACT_ROUND849_850_ORDER_EQUIVALENCE\","
    )
    .unwrap();
    writeln!(out, "  \"scope\": \"read-only round849/850 cache order benchmark; no solve and no continuation\",").unwrap();
    writeln!(out, "  \"prime\": {},", old_stats.prime).unwrap();
    writeln!(out, "  \"provider_fingerprint\": {},", old_stats.provider).unwrap();
    writeln!(out, "  \"round849\": {{\"records\": {}, \"terms\": {}, \"ranked_rows\": {}, \"cache_fingerprint\": {}, \"order_sha256_baseline\": \"{}\", \"order_sha256_index\": \"{}\"}},",
        old_stats.records, old_stats.terms, old_ranked_rows,
        old_stats.fingerprint, old_order_sha256, old_order_sha256).unwrap();
    writeln!(out, "  \"round850\": {{\"records\": {}, \"terms\": {}, \"new_columns\": {}, \"ranked_rows\": {}, \"cache_fingerprint\": {}, \"order_sha256_baseline\": \"{}\", \"order_sha256_index\": \"{}\"}},",
        new_stats.records, new_stats.terms, new_columns_seen, ranked_rows,
        new_stats.fingerprint, new_order_sha256, new_order_sha256).unwrap();
    writeln!(out, "  \"incremental\": {{\"touched_rows\": {}, \"dirty_buckets\": {}, \"merged_old_rows\": {}, \"removed_rows\": {}, \"added_rows\": {}}},",
        commit_stats.touched, commit_stats.dirty_buckets, commit_stats.merged_old_rows,
        commit_stats.removed_rows, commit_stats.added_rows).unwrap();
    writeln!(out, "  \"timings_seconds\": {{\"old_scan\": {:.6}, \"initial_index_build\": {:.6}, \"old_compare_and_hash\": {:.6}, \"new_scan\": {:.6}, \"incremental_commit\": {:.6}, \"new_baseline_sort\": {:.6}, \"new_index_flatten\": {:.6}, \"total\": {:.6}}},",
        old_scan_seconds, initial_build_seconds, old_compare_seconds, new_scan_seconds,
        incremental_commit_seconds, new_baseline_sort_seconds, new_indexed_flatten_seconds,
        elapsed_seconds).unwrap();
    writeln!(out, "  \"peak_rss_kib_phase_sampled\": {},", peak_rss_kib).unwrap();
    writeln!(
        out,
        "  \"mono_size_bytes\": {},",
        std::mem::size_of::<Mono>()
    )
    .unwrap();
    writeln!(
        out,
        "  \"ordered_tuple_size_bytes\": {},",
        std::mem::size_of::<(u32, Mono)>()
    )
    .unwrap();
    writeln!(out, "  \"checkpoint_or_cache_written\": false").unwrap();
    writeln!(out, "}}").unwrap();
    out.flush().unwrap_or_else(|error| fail(error.to_string()));
    drop(out);
    fs::rename(tmp, &config.output).unwrap_or_else(|error| fail(error.to_string()));
    eprintln!("PASS rows={} touched={} baseline_sort={:.6}s index_commit_plus_flatten={:.6}s peak_rss_kib={}",
        ranked_rows, commit_stats.touched, new_baseline_sort_seconds,
        incremental_commit_seconds + new_indexed_flatten_seconds, peak_rss_kib);
}
