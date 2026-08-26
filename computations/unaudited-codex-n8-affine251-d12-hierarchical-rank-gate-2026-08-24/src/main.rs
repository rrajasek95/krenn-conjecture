use std::collections::HashMap;
use std::env;
use std::fs::{self, File};
use std::hash::{BuildHasherDefault, Hasher};
use std::io::{BufReader, BufWriter, Read, Write};
use std::path::{Path, PathBuf};
use std::process::Command;
use std::thread;
use std::time::Instant;

type Row = [u8; 12];

const VECTOR_MAGIC: &[u8; 12] = b"AFF12VEC1\0\0\0";
const CHECKPOINT_MAGIC: &[u8; 12] = b"AFF12CEG1\0\0\0";
const PRIME: u32 = 1_073_741_827;
const PROVIDER_FINGERPRINT: u64 = 9_218_588_987_274_412_661;
const ROUND: u64 = 660;
const EQUATIONS: usize = 246_321;
const EXPECTED_SUPPORT: usize = 352;
const TARGET: Row = [251; 12];
const VECTOR_SHA256: &str = "ecbcb26bcb8d2ecbb38cff4cce56457a960b2f11ba944536cd7bcf8d15b01275";
const CHECKPOINT_SHA256: &str = "92185737bc273f112f91240ee58eb8d0b4cd842739490838ebd30c870b8b6155";
const SEQUENTIAL_SOLVE_SECONDS: f64 = 8.726527;
const HARD_WALL_SECONDS: f64 = 120.0;
const STOP_SCHEDULING_SECONDS: f64 = 110.0;
const HARD_RSS_BYTES: i64 = 36 * 1024 * 1024 * 1024;

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct Column {
    word: u16,
    multiplier: Row,
}

#[derive(Clone, Copy)]
struct RawTerm {
    row: Row,
    value: u32,
}

struct RawEquation {
    terms: Vec<RawTerm>,
    rhs: u32,
}

#[derive(Clone, Copy)]
struct Term {
    rank: u32,
    value: u32,
}

struct Equation {
    terms: Vec<Term>,
    rhs: u32,
}

struct Record {
    terms: Vec<Term>,
    rhs: u32,
}

struct Basis {
    records: HashMap<u32, Record>,
    inconsistent: bool,
}

struct WorkerRecord {
    index: usize,
    begin: usize,
    end: usize,
    basis_records: usize,
    basis_terms: usize,
    inconsistent: bool,
    seconds: f64,
}

struct MergeRecord {
    level: usize,
    pair: usize,
    left_records: usize,
    right_records: usize,
    output_records: usize,
    output_terms: usize,
    inconsistent: bool,
    seconds: f64,
}

struct RankMetrics {
    ordered_sort_seconds: f64,
    rank_map_build_seconds: f64,
    compact_materialize_seconds: f64,
    shard_min_rows: usize,
    shard_max_rows: usize,
}

#[derive(Default)]
struct FnvHasher(u64);

impl Hasher for FnvHasher {
    fn finish(&self) -> u64 {
        self.0
    }

    fn write(&mut self, bytes: &[u8]) {
        let mut hash = if self.0 == 0 {
            0xcbf29ce484222325u64
        } else {
            self.0
        };
        for byte in bytes {
            hash ^= *byte as u64;
            hash = hash.wrapping_mul(0x100000001b3);
        }
        self.0 = hash;
    }
}

type FastRankMap = HashMap<Row, u32, BuildHasherDefault<FnvHasher>>;

#[repr(C)]
#[derive(Clone, Copy)]
struct Timeval {
    seconds: i64,
    micros: i32,
    padding: i32,
}

#[repr(C)]
struct Rusage {
    user: Timeval,
    system: Timeval,
    max_rss: i64,
    remainder: [i64; 13],
}

extern "C" {
    fn getrusage(who: i32, usage: *mut Rusage) -> i32;
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("FAIL: {}", message.as_ref());
    std::process::exit(2)
}

fn require(condition: bool, message: impl AsRef<str>) {
    if !condition {
        fail(message)
    }
}

fn argument(name: &str) -> PathBuf {
    let args: Vec<_> = env::args().collect();
    let position = args
        .iter()
        .position(|value| value == name)
        .unwrap_or_else(|| fail(format!("missing {name}")));
    require(
        position + 1 < args.len(),
        format!("missing value for {name}"),
    );
    PathBuf::from(&args[position + 1])
}

fn argument_usize(name: &str) -> usize {
    let value = argument(name);
    value
        .to_str()
        .unwrap_or_else(|| fail(format!("non-UTF8 value for {name}")))
        .parse()
        .unwrap_or_else(|_| fail(format!("invalid integer for {name}")))
}

fn argument_string(name: &str) -> String {
    argument(name)
        .to_str()
        .unwrap_or_else(|| fail(format!("non-UTF8 value for {name}")))
        .to_string()
}

fn read_array<const N: usize, R: Read>(input: &mut R) -> [u8; N] {
    let mut value = [0u8; N];
    input
        .read_exact(&mut value)
        .unwrap_or_else(|error| fail(error.to_string()));
    value
}

fn read_u16<R: Read>(input: &mut R) -> u16 {
    u16::from_le_bytes(read_array(input))
}
fn read_u64<R: Read>(input: &mut R) -> u64 {
    u64::from_le_bytes(read_array(input))
}

fn read_mono<R: Read>(input: &mut R, degree: u8) -> Row {
    require(
        read_array::<1, _>(input)[0] == degree,
        "monomial degree changed",
    );
    read_array(input)
}

fn write_mono<W: Write>(output: &mut W, degree: u8, row: Row) {
    output.write_all(&[degree]).unwrap();
    output.write_all(&row).unwrap();
}

fn trailing_eof<R: Read>(input: &mut R) {
    let mut byte = [0u8; 1];
    require(
        input
            .read(&mut byte)
            .unwrap_or_else(|error| fail(error.to_string()))
            == 0,
        "trailing bytes",
    );
}

fn sha256(path: &Path) -> String {
    let output = Command::new("/usr/bin/shasum")
        .arg("-a")
        .arg("256")
        .arg(path)
        .output()
        .unwrap_or_else(|error| fail(error.to_string()));
    require(output.status.success(), "shasum failed");
    String::from_utf8(output.stdout)
        .unwrap()
        .split_whitespace()
        .next()
        .unwrap()
        .to_string()
}

fn peak_rss_bytes() -> i64 {
    let mut usage = Rusage {
        user: Timeval {
            seconds: 0,
            micros: 0,
            padding: 0,
        },
        system: Timeval {
            seconds: 0,
            micros: 0,
            padding: 0,
        },
        max_rss: 0,
        remainder: [0; 13],
    };
    require(unsafe { getrusage(0, &mut usage) } == 0, "getrusage failed");
    usage.max_rss
}

fn gate(started: Instant, phase: &str) {
    require(
        started.elapsed().as_secs_f64() < STOP_SCHEDULING_SECONDS,
        format!("stop-scheduling wall gate at {phase}"),
    );
    require(
        peak_rss_bytes() < HARD_RSS_BYTES,
        format!("RSS gate at {phase}"),
    );
}

#[inline(always)]
fn subtract_mod(left: u32, right: u32) -> u32 {
    if left >= right {
        left - right
    } else {
        left + PRIME - right
    }
}

#[inline(always)]
fn multiply_mod(left: u32, right: u32) -> u32 {
    (left as u64 * right as u64 % PRIME as u64) as u32
}

fn inverse_mod(mut base: u32) -> u32 {
    let mut exponent = PRIME - 2;
    let mut answer = 1u32;
    while exponent != 0 {
        if exponent & 1 != 0 {
            answer = multiply_mod(answer, base);
        }
        base = multiply_mod(base, base);
        exponent >>= 1;
    }
    answer
}

fn sub_scaled(target: &[Term], source: &[Term], factor: u32) -> Vec<Term> {
    let mut answer = Vec::with_capacity(target.len() + source.len());
    let (mut left, mut right) = (0usize, 0usize);
    while left < target.len() || right < source.len() {
        if right == source.len() || (left < target.len() && target[left].rank < source[right].rank)
        {
            answer.push(target[left]);
            left += 1;
        } else if left == target.len() || source[right].rank < target[left].rank {
            let value = multiply_mod(factor, source[right].value);
            if value != 0 {
                answer.push(Term {
                    rank: source[right].rank,
                    value: PRIME - value,
                });
            }
            right += 1;
        } else {
            let value = subtract_mod(
                target[left].value,
                multiply_mod(factor, source[right].value),
            );
            if value != 0 {
                answer.push(Term {
                    rank: target[left].rank,
                    value,
                });
            }
            left += 1;
            right += 1;
        }
    }
    answer
}

impl Basis {
    fn empty(capacity: usize) -> Self {
        Self {
            records: HashMap::with_capacity(capacity),
            inconsistent: false,
        }
    }

    fn add(&mut self, mut terms: Vec<Term>, mut rhs: u32) {
        if self.inconsistent {
            return;
        }
        loop {
            if terms.is_empty() {
                if rhs != 0 {
                    self.inconsistent = true;
                }
                return;
            }
            let pivot = terms[0].rank;
            let factor = terms[0].value;
            if let Some(record) = self.records.get(&pivot) {
                terms = sub_scaled(&terms, &record.terms, factor);
                rhs = subtract_mod(rhs, multiply_mod(factor, record.rhs));
                continue;
            }
            let inverse = inverse_mod(factor);
            for term in &mut terms {
                term.value = multiply_mod(term.value, inverse);
            }
            rhs = multiply_mod(rhs, inverse);
            require(terms[0].value == 1, "basis normalization");
            require(
                self.records.insert(pivot, Record { terms, rhs }).is_none(),
                "duplicate basis pivot",
            );
            return;
        }
    }

    fn term_count(&self) -> usize {
        self.records.values().map(|record| record.terms.len()).sum()
    }
}

fn parse_checkpoint(path: &Path) -> (Vec<Column>, Vec<(Row, u32)>) {
    let mut input = BufReader::with_capacity(
        4 << 20,
        File::open(path).unwrap_or_else(|error| fail(error.to_string())),
    );
    require(
        &read_array::<12, _>(&mut input) == CHECKPOINT_MAGIC,
        "checkpoint magic",
    );
    require(read_u64(&mut input) == PRIME as u64, "checkpoint prime");
    require(read_u64(&mut input) == ROUND, "checkpoint round");
    require(
        read_u64(&mut input) == EQUATIONS as u64,
        "checkpoint equations",
    );
    require(
        read_u64(&mut input) == EXPECTED_SUPPORT as u64,
        "checkpoint support",
    );
    let mut columns = Vec::with_capacity(EQUATIONS);
    let mut previous = None;
    for _ in 0..EQUATIONS {
        let column = Column {
            word: read_u16(&mut input),
            multiplier: read_mono(&mut input, 8),
        };
        require(
            previous.is_none_or(|old| old < column),
            "checkpoint column order",
        );
        previous = Some(column);
        columns.push(column);
    }
    let mut candidate = Vec::with_capacity(EXPECTED_SUPPORT);
    let mut previous_row = None;
    for _ in 0..EXPECTED_SUPPORT {
        let row = read_mono(&mut input, 12);
        let value = read_u64(&mut input);
        require(
            previous_row.is_none_or(|old| old < row),
            "checkpoint candidate order",
        );
        require(
            value > 0 && value < PRIME as u64,
            "checkpoint candidate value",
        );
        previous_row = Some(row);
        candidate.push((row, value as u32));
    }
    trailing_eof(&mut input);
    require(
        candidate
            .binary_search_by_key(&TARGET, |item| item.0)
            .ok()
            .is_some_and(|index| candidate[index].1 == 1),
        "target normalization changed",
    );
    (columns, candidate)
}

fn parse_vectors(path: &Path) -> (u64, Vec<Column>, Vec<RawEquation>, HashMap<Row, u32>) {
    let mut input = BufReader::with_capacity(
        16 << 20,
        File::open(path).unwrap_or_else(|error| fail(error.to_string())),
    );
    require(
        &read_array::<12, _>(&mut input) == VECTOR_MAGIC,
        "vector magic",
    );
    require(read_u64(&mut input) == PRIME as u64, "vector prime");
    require(
        read_u64(&mut input) == PROVIDER_FINGERPRINT,
        "provider fingerprint",
    );
    let vector_fingerprint = read_u64(&mut input);
    require(
        read_u64(&mut input) == EQUATIONS as u64,
        "vector equation count",
    );
    let mut columns = Vec::with_capacity(EQUATIONS);
    let mut equations = Vec::with_capacity(EQUATIONS);
    let mut frequency = HashMap::<Row, u32>::with_capacity(18_000_000);
    let mut previous_column = None;
    for _ in 0..EQUATIONS {
        let column = Column {
            word: read_u16(&mut input),
            multiplier: read_mono(&mut input, 8),
        };
        require(
            previous_column.is_none_or(|old| old < column),
            "vector column order",
        );
        previous_column = Some(column);
        columns.push(column);
        let size = read_u64(&mut input) as usize;
        require(size > 0 && size <= 700_000, "vector size");
        let mut terms = Vec::with_capacity(size);
        let mut rhs = 0u32;
        let mut previous_row = None;
        for _ in 0..size {
            let row = read_mono(&mut input, 12);
            require(previous_row.is_none_or(|old| old < row), "vector row order");
            previous_row = Some(row);
            let value = read_u64(&mut input);
            require(value > 0 && value < PRIME as u64, "vector residue");
            if row == TARGET {
                require(rhs == 0, "duplicate target term");
                rhs = PRIME - value as u32;
                if rhs == PRIME {
                    rhs = 0;
                }
            } else {
                let count = frequency.entry(row).or_default();
                *count = count
                    .checked_add(1)
                    .unwrap_or_else(|| fail("frequency overflow"));
                terms.push(RawTerm {
                    row,
                    value: value as u32,
                });
            }
        }
        equations.push(RawEquation { terms, rhs });
    }
    trailing_eof(&mut input);
    (vector_fingerprint, columns, equations, frequency)
}

fn rank_equations_baseline(
    raw: Vec<RawEquation>,
    frequency: HashMap<Row, u32>,
) -> (Vec<Equation>, Vec<Row>, RankMetrics) {
    let sort_started = Instant::now();
    let mut ordered: Vec<(Row, u32)> = frequency.into_iter().collect();
    ordered.sort_unstable_by(|left, right| (left.1, left.0).cmp(&(right.1, right.0)));
    let rows_by_rank: Vec<Row> = ordered.iter().map(|item| item.0).collect();
    let ordered_sort_seconds = sort_started.elapsed().as_secs_f64();
    let map_started = Instant::now();
    let mut rank = HashMap::<Row, u32>::with_capacity(rows_by_rank.len());
    for (index, row) in rows_by_rank.iter().copied().enumerate() {
        require(
            rank.insert(row, index as u32).is_none(),
            "duplicate ranked row",
        );
    }
    drop(ordered);
    let rank_map_build_seconds = map_started.elapsed().as_secs_f64();
    let materialize_started = Instant::now();
    let mut equations = Vec::with_capacity(raw.len());
    for equation in raw {
        let mut terms: Vec<Term> = equation
            .terms
            .into_iter()
            .map(|term| Term {
                rank: *rank.get(&term.row).unwrap_or_else(|| fail("unranked row")),
                value: term.value,
            })
            .collect();
        terms.sort_unstable_by_key(|term| term.rank);
        require(
            terms.windows(2).all(|pair| pair[0].rank < pair[1].rank),
            "ranked equation duplicate/order",
        );
        equations.push(Equation {
            terms,
            rhs: equation.rhs,
        });
    }
    drop(rank);
    let compact_materialize_seconds = materialize_started.elapsed().as_secs_f64();
    let count = rows_by_rank.len();
    (
        equations,
        rows_by_rank,
        RankMetrics {
            ordered_sort_seconds,
            rank_map_build_seconds,
            compact_materialize_seconds,
            shard_min_rows: count,
            shard_max_rows: count,
        },
    )
}

fn row_hash(row: &Row) -> u64 {
    let mut hasher = FnvHasher::default();
    hasher.write(row);
    hasher.finish()
}

fn materialize_chunk(
    raw: Vec<RawEquation>,
    rank_maps: &[FastRankMap],
    rank_shards: usize,
) -> Vec<Equation> {
    let mut equations = Vec::with_capacity(raw.len());
    for equation in raw {
        let mut terms: Vec<Term> = equation
            .terms
            .into_iter()
            .map(|term| {
                let shard = row_hash(&term.row) as usize & (rank_shards - 1);
                Term {
                    rank: *rank_maps[shard]
                        .get(&term.row)
                        .unwrap_or_else(|| fail("unranked sharded row")),
                    value: term.value,
                }
            })
            .collect();
        terms.sort_unstable_by_key(|term| term.rank);
        require(
            terms.windows(2).all(|pair| pair[0].rank < pair[1].rank),
            "sharded ranked equation duplicate/order",
        );
        equations.push(Equation {
            terms,
            rhs: equation.rhs,
        });
    }
    equations
}

fn rank_equations_sharded(
    raw: Vec<RawEquation>,
    frequency: HashMap<Row, u32>,
    workers: usize,
    rank_shards: usize,
) -> (Vec<Equation>, Vec<Row>, RankMetrics) {
    require(
        rank_shards.is_power_of_two() && rank_shards <= 64,
        "rank shards must be power of two at most 64",
    );
    let sort_started = Instant::now();
    let mut ordered: Vec<(u32, Row)> = frequency
        .into_iter()
        .map(|(row, frequency)| (frequency, row))
        .collect();
    ordered.sort_unstable();
    require(
        ordered
            .windows(2)
            .all(|pair| (pair[0].0, pair[0].1) < (pair[1].0, pair[1].1)),
        "owned frequency/row sort order",
    );
    let rows_by_rank: Vec<Row> = ordered.iter().map(|item| item.1).collect();
    drop(ordered);
    let ordered_sort_seconds = sort_started.elapsed().as_secs_f64();

    let map_started = Instant::now();
    let mut buckets: Vec<Vec<(Row, u32)>> = (0..rank_shards)
        .map(|_| Vec::with_capacity(rows_by_rank.len() / rank_shards + 1))
        .collect();
    for (rank, row) in rows_by_rank.iter().copied().enumerate() {
        let shard = row_hash(&row) as usize & (rank_shards - 1);
        buckets[shard].push((row, rank as u32));
    }
    let shard_min_rows = buckets.iter().map(Vec::len).min().unwrap();
    let shard_max_rows = buckets.iter().map(Vec::len).max().unwrap();
    let rank_maps: Vec<FastRankMap> = thread::scope(|scope| {
        let handles: Vec<_> = buckets
            .into_iter()
            .map(|bucket| {
                scope.spawn(move || {
                    let mut map = FastRankMap::with_capacity_and_hasher(
                        bucket.len(),
                        BuildHasherDefault::default(),
                    );
                    for (row, rank) in bucket {
                        require(
                            map.insert(row, rank).is_none(),
                            "duplicate sharded rank row",
                        );
                    }
                    map
                })
            })
            .collect();
        handles
            .into_iter()
            .map(|handle| {
                handle
                    .join()
                    .unwrap_or_else(|_| fail("rank map worker panic"))
            })
            .collect()
    });
    require(
        rank_maps.iter().map(HashMap::len).sum::<usize>() == rows_by_rank.len(),
        "rank shard census",
    );
    let rank_map_build_seconds = map_started.elapsed().as_secs_f64();

    let materialize_started = Instant::now();
    let base = raw.len() / workers;
    let remainder = raw.len() % workers;
    let mut iterator = raw.into_iter();
    let mut chunks = Vec::with_capacity(workers);
    for worker in 0..workers {
        let count = base + usize::from(worker < remainder);
        chunks.push(iterator.by_ref().take(count).collect::<Vec<_>>());
    }
    require(iterator.next().is_none(), "materialization chunk coverage");
    let chunk_results = thread::scope(|scope| {
        let handles: Vec<_> = chunks
            .into_iter()
            .map(|chunk| {
                let maps = &rank_maps;
                scope.spawn(move || materialize_chunk(chunk, maps, rank_shards))
            })
            .collect();
        handles
            .into_iter()
            .map(|handle| {
                handle
                    .join()
                    .unwrap_or_else(|_| fail("materialization worker panic"))
            })
            .collect::<Vec<_>>()
    });
    let mut equations = Vec::with_capacity(EQUATIONS);
    for mut chunk in chunk_results {
        equations.append(&mut chunk);
    }
    require(equations.len() == EQUATIONS, "materialized equation census");
    drop(rank_maps);
    let compact_materialize_seconds = materialize_started.elapsed().as_secs_f64();
    (
        equations,
        rows_by_rank,
        RankMetrics {
            ordered_sort_seconds,
            rank_map_build_seconds,
            compact_materialize_seconds,
            shard_min_rows,
            shard_max_rows,
        },
    )
}

fn build_local(index: usize, begin: usize, equations: &[Equation]) -> (Basis, WorkerRecord) {
    let started = Instant::now();
    let mut basis = Basis::empty(equations.len());
    for equation in equations {
        basis.add(equation.terms.clone(), equation.rhs);
        if basis.inconsistent {
            break;
        }
    }
    let record = WorkerRecord {
        index,
        begin,
        end: begin + equations.len(),
        basis_records: basis.records.len(),
        basis_terms: basis.term_count(),
        inconsistent: basis.inconsistent,
        seconds: started.elapsed().as_secs_f64(),
    };
    (basis, record)
}

fn merge_bases(level: usize, pair: usize, mut left: Basis, right: Basis) -> (Basis, MergeRecord) {
    let started = Instant::now();
    let left_records = left.records.len();
    let right_records = right.records.len();
    if right.inconsistent {
        left.inconsistent = true;
    }
    let mut incoming: Vec<(u32, Record)> = right.records.into_iter().collect();
    incoming.sort_unstable_by_key(|item| item.0);
    for (_, record) in incoming {
        left.add(record.terms, record.rhs);
        if left.inconsistent {
            break;
        }
    }
    let record = MergeRecord {
        level,
        pair,
        left_records,
        right_records,
        output_records: left.records.len(),
        output_terms: left.term_count(),
        inconsistent: left.inconsistent,
        seconds: started.elapsed().as_secs_f64(),
    };
    (left, record)
}

fn merge_group(
    level: usize,
    group_index: usize,
    arity: usize,
    group: Vec<Basis>,
) -> (Basis, Vec<MergeRecord>) {
    require(!group.is_empty(), "empty merge group");
    let mut iterator = group.into_iter();
    let mut left = iterator.next().unwrap();
    let mut records = Vec::new();
    for (child, right) in iterator.enumerate() {
        let pair = group_index * arity + child;
        let (merged, record) = merge_bases(level, pair, left, right);
        left = merged;
        records.push(record);
    }
    (left, records)
}

fn solve_hierarchical(
    equations: &[Equation],
    rows_by_rank: &[Row],
    workers: usize,
    merge_arity: usize,
) -> (
    Vec<(Row, u32)>,
    Vec<WorkerRecord>,
    Vec<MergeRecord>,
    f64,
    usize,
) {
    let solve_started = Instant::now();
    require(workers >= 1 && workers <= 64, "workers outside [1,64]");
    require(
        merge_arity >= 2 && merge_arity <= 64,
        "merge arity outside [2,64]",
    );
    let base = equations.len() / workers;
    let remainder = equations.len() % workers;
    let local_results = thread::scope(|scope| {
        let mut handles = Vec::with_capacity(workers);
        let mut begin = 0usize;
        for worker in 0..workers {
            let count = base + usize::from(worker < remainder);
            let slice = &equations[begin..begin + count];
            let worker_begin = begin;
            handles.push(scope.spawn(move || build_local(worker, worker_begin, slice)));
            begin += count;
        }
        handles
            .into_iter()
            .map(|handle| handle.join().unwrap_or_else(|_| fail("local worker panic")))
            .collect::<Vec<_>>()
    });
    let mut bases = Vec::with_capacity(workers);
    let mut worker_records = Vec::with_capacity(workers);
    for (basis, record) in local_results {
        require(
            !basis.inconsistent,
            format!("local inconsistency worker {}", record.index),
        );
        bases.push(basis);
        worker_records.push(record);
    }
    let mut merge_records = Vec::new();
    let mut level = 0usize;
    while bases.len() > 1 {
        let mut groups = Vec::with_capacity((bases.len() + merge_arity - 1) / merge_arity);
        let mut iterator = bases.into_iter();
        loop {
            let mut group = Vec::with_capacity(merge_arity);
            for _ in 0..merge_arity {
                if let Some(basis) = iterator.next() {
                    group.push(basis);
                } else {
                    break;
                }
            }
            if group.is_empty() {
                break;
            }
            groups.push(group);
        }
        let merged = thread::scope(|scope| {
            let handles: Vec<_> = groups
                .into_iter()
                .enumerate()
                .map(|(group_index, group)| {
                    scope.spawn(move || merge_group(level, group_index, merge_arity, group))
                })
                .collect();
            handles
                .into_iter()
                .map(|handle| handle.join().unwrap_or_else(|_| fail("merge worker panic")))
                .collect::<Vec<_>>()
        });
        bases = Vec::with_capacity(merged.len());
        for (basis, records) in merged {
            require(
                !basis.inconsistent,
                format!("merge inconsistency level {level}"),
            );
            bases.push(basis);
            merge_records.extend(records);
        }
        level += 1;
    }
    let basis = bases.pop().unwrap();
    let basis_terms = basis.term_count();
    let mut pivots: Vec<u32> = basis.records.keys().copied().collect();
    pivots.sort_unstable();
    let mut values = vec![0u32; rows_by_rank.len()];
    for pivot in pivots.into_iter().rev() {
        let record = &basis.records[&pivot];
        require(
            record
                .terms
                .first()
                .is_some_and(|term| term.rank == pivot && term.value == 1),
            "backsolve pivot normalization",
        );
        let mut value = record.rhs;
        for term in &record.terms[1..] {
            value = subtract_mod(value, multiply_mod(term.value, values[term.rank as usize]));
        }
        values[pivot as usize] = value;
    }
    let verification_failures: usize = thread::scope(|scope| {
        let mut handles = Vec::with_capacity(workers);
        let base = equations.len() / workers;
        let remainder = equations.len() % workers;
        let mut begin = 0usize;
        for worker in 0..workers {
            let count = base + usize::from(worker < remainder);
            let slice = &equations[begin..begin + count];
            let values_ref = &values;
            handles.push(scope.spawn(move || {
                slice
                    .iter()
                    .filter(|equation| {
                        let mut sum = 0u32;
                        for term in &equation.terms {
                            let product = multiply_mod(term.value, values_ref[term.rank as usize]);
                            let next = sum + product;
                            sum = if next >= PRIME { next - PRIME } else { next };
                        }
                        sum != equation.rhs
                    })
                    .count()
            }));
            begin += count;
        }
        handles
            .into_iter()
            .map(|handle| {
                handle
                    .join()
                    .unwrap_or_else(|_| fail("verify worker panic"))
            })
            .sum()
    });
    require(
        verification_failures == 0,
        "merged solution violates exposed equation",
    );
    let mut candidate = Vec::with_capacity(basis.records.len() + 1);
    candidate.push((TARGET, 1));
    for (rank, value) in values.into_iter().enumerate() {
        if value != 0 {
            candidate.push((rows_by_rank[rank], value));
        }
    }
    candidate.sort_unstable_by_key(|item| item.0);
    require(
        candidate.windows(2).all(|pair| pair[0].0 < pair[1].0),
        "candidate row order",
    );
    let solve_seconds = solve_started.elapsed().as_secs_f64();
    (
        candidate,
        worker_records,
        merge_records,
        solve_seconds,
        basis_terms,
    )
}

fn write_checkpoint(path: &Path, columns: &[Column], candidate: &[(Row, u32)]) {
    let temporary = path.with_extension("bin.tmp");
    let mut output = BufWriter::with_capacity(
        4 << 20,
        File::create(&temporary).unwrap_or_else(|error| fail(error.to_string())),
    );
    output.write_all(CHECKPOINT_MAGIC).unwrap();
    output.write_all(&(PRIME as u64).to_le_bytes()).unwrap();
    output.write_all(&ROUND.to_le_bytes()).unwrap();
    output
        .write_all(&(columns.len() as u64).to_le_bytes())
        .unwrap();
    output
        .write_all(&(candidate.len() as u64).to_le_bytes())
        .unwrap();
    for column in columns {
        output.write_all(&column.word.to_le_bytes()).unwrap();
        write_mono(&mut output, 8, column.multiplier);
    }
    for &(row, value) in candidate {
        write_mono(&mut output, 12, row);
        output.write_all(&(value as u64).to_le_bytes()).unwrap();
    }
    output.flush().unwrap();
    drop(output);
    fs::rename(temporary, path).unwrap_or_else(|error| fail(error.to_string()));
}

fn json_path(path: &Path) -> String {
    path.display()
        .to_string()
        .replace('\\', "\\\\")
        .replace('"', "\\\"")
}

fn main() {
    require(
        cfg!(target_endian = "little"),
        "little-endian host required",
    );
    let vectors_path = argument("--vectors");
    let checkpoint_path = argument("--checkpoint");
    let source_path = argument("--source");
    let output_checkpoint = argument("--output-checkpoint");
    let output_result = argument("--output-result");
    let workers_count = argument_usize("--workers");
    let merge_arity = argument_usize("--merge-arity");
    let rank_mode = argument_string("--rank-mode");
    let rank_shards = argument_usize("--rank-shards");
    let started = Instant::now();

    let hash_started = Instant::now();
    require(
        sha256(&vectors_path) == VECTOR_SHA256,
        "unfrozen vector SHA-256",
    );
    require(
        sha256(&checkpoint_path) == CHECKPOINT_SHA256,
        "unfrozen checkpoint SHA-256",
    );
    let source_sha = sha256(&source_path);
    let executable_sha =
        sha256(&env::current_exe().unwrap_or_else(|error| fail(error.to_string())));
    let hash_seconds = hash_started.elapsed().as_secs_f64();
    gate(started, "hash");

    let parse_started = Instant::now();
    let (expected_columns, expected_candidate) = parse_checkpoint(&checkpoint_path);
    let (vector_fingerprint, columns, raw_equations, frequency) = parse_vectors(&vectors_path);
    require(
        columns == expected_columns,
        "checkpoint/vector columns differ",
    );
    let source_terms: usize = raw_equations
        .iter()
        .map(|equation| equation.terms.len())
        .sum();
    let parse_seconds = parse_started.elapsed().as_secs_f64();
    gate(started, "parse");

    let rank_started = Instant::now();
    let distinct_variables = frequency.len();
    let (equations, rows_by_rank, rank_metrics) = match rank_mode.as_str() {
        "baseline" => rank_equations_baseline(raw_equations, frequency),
        "sharded" => rank_equations_sharded(raw_equations, frequency, workers_count, rank_shards),
        _ => fail("rank mode must be baseline or sharded"),
    };
    let rank_seconds = rank_started.elapsed().as_secs_f64();
    gate(started, "rank");

    let (candidate, workers, merges, elimination_seconds, final_basis_terms) =
        solve_hierarchical(&equations, &rows_by_rank, workers_count, merge_arity);
    gate(started, "solve");
    let candidate_identical = candidate == expected_candidate;
    require(
        candidate_identical,
        "hierarchical candidate differs; actual next-frontier scorer is required before acceptance",
    );
    require(
        candidate.len() == EXPECTED_SUPPORT,
        "candidate support differs",
    );
    // Count the representation-specific rare-rank/materialization pass as solve
    // work.  The sequential baseline constructs its BTreeMap equations inside
    // its sealed solve timer, so excluding our equivalent preparation would be
    // an unfair promotion comparison.
    let solve_seconds = rank_seconds + elimination_seconds;
    let speedup = SEQUENTIAL_SOLVE_SECONDS / solve_seconds;
    require(
        speedup >= 2.0,
        format!("solve speedup below 2x: {speedup:.6}"),
    );

    let write_started = Instant::now();
    write_checkpoint(&output_checkpoint, &columns, &candidate);
    let output_checkpoint_sha = sha256(&output_checkpoint);
    require(
        output_checkpoint_sha == CHECKPOINT_SHA256,
        "checkpoint bytes are not identical",
    );
    let write_seconds = write_started.elapsed().as_secs_f64();
    let total_seconds = started.elapsed().as_secs_f64();
    let peak = peak_rss_bytes();
    require(total_seconds < HARD_WALL_SECONDS, "hard wall gate");
    require(peak < HARD_RSS_BYTES, "hard RSS gate");

    let worker_json = workers.iter().map(|record| format!(
        "{{\"worker\":{},\"begin\":{},\"end\":{},\"equations\":{},\"basis_records\":{},\"basis_terms\":{},\"inconsistent\":{},\"seconds\":{:.6}}}",
        record.index, record.begin, record.end, record.end - record.begin,
        record.basis_records, record.basis_terms, record.inconsistent, record.seconds))
        .collect::<Vec<_>>().join(",\n    ");
    let merge_json = merges.iter().map(|record| format!(
        "{{\"level\":{},\"pair\":{},\"left_records\":{},\"right_records\":{},\"output_records\":{},\"output_terms\":{},\"inconsistent\":{},\"seconds\":{:.6}}}",
        record.level, record.pair, record.left_records, record.right_records,
        record.output_records, record.output_terms, record.inconsistent, record.seconds))
        .collect::<Vec<_>>().join(",\n    ");
    let result = format!(concat!(
        "{{\n  \"status\": \"PASS_EXACT_PARALLEL_HIERARCHICAL_ROUND660_PROMOTION_GATE\",\n",
        "  \"schema\": \"KRENN_AFFINE251_D12_HIERARCHICAL_ROUND660_V1\",\n",
        "  \"source_sha256\": \"{}\",\n  \"binary_sha256\": \"{}\",\n",
        "  \"vectors\": {{\"path\":\"{}\",\"sha256\":\"{}\",\"bytes\":{},\"fingerprint\":{}}},\n",
        "  \"sequential_checkpoint\": {{\"path\":\"{}\",\"sha256\":\"{}\"}},\n",
        "  \"output_checkpoint\": {{\"path\":\"{}\",\"sha256\":\"{}\",\"byte_identical\":true}},\n",
        "  \"round\": {},\n  \"prime\": {},\n  \"workers\": {},\n  \"merge_arity\": {},\n",
        "  \"rank_mode\": \"{}\",\n  \"rank_shards\": {},\n",
        "  \"equations\": {},\n  \"source_variable_terms\": {},\n  \"distinct_variables\": {},\n",
        "  \"candidate_support\": {},\n  \"candidate_identical\": true,\n",
        "  \"all_equations_verified\": true,\n  \"verification_failures\": 0,\n",
        "  \"frontier_comparison\": \"IDENTICAL_CANDIDATE_AND_COLUMNS_IMPLY_IDENTICAL_NEXT_FRONTIER\",\n",
        "  \"final_basis_terms\": {},\n",
        "  \"sequential_solve_seconds\": {:.6},\n  \"hierarchical_solve_seconds\": {:.6},\n",
        "  \"hierarchical_elimination_backsolve_verify_seconds\": {:.6},\n",
        "  \"solve_speedup\": {:.9},\n  \"promotion_threshold\": 2.0,\n",
        "  \"timings_seconds\": {{\"source_hash\":{:.6},\"parse_and_frequency\":{:.6},\"rare_rank_and_materialize\":{:.6},\"owned_frequency_row_sort\":{:.6},\"rank_map_build\":{:.6},\"compact_equation_materialize\":{:.6},\"hierarchical_elimination_backsolve_verify\":{:.6},\"checkpoint_write_hash\":{:.6},\"total\":{:.6}}},\n",
        "  \"rank_shard_rows\": {{\"min\":{},\"max\":{}}},\n",
        "  \"peak_rss_bytes\": {},\n  \"hard_wall_seconds\": 120,\n  \"hard_rss_bytes\": {},\n",
        "  \"worker_records\": [\n    {}\n  ],\n",
        "  \"merge_records\": [\n    {}\n  ],\n",
        "  \"scope\": \"One exact round-660 cold/rare solve only; no CEGAR continuation, closure, rank, Krylov, or higher-degree run.\"\n}}\n"),
        source_sha, executable_sha,
        json_path(&vectors_path), VECTOR_SHA256, fs::metadata(&vectors_path).unwrap().len(), vector_fingerprint,
        json_path(&checkpoint_path), CHECKPOINT_SHA256,
        json_path(&output_checkpoint), output_checkpoint_sha,
        ROUND, PRIME, workers_count, merge_arity, rank_mode, rank_shards,
        EQUATIONS, source_terms, distinct_variables,
        candidate.len(), final_basis_terms,
        SEQUENTIAL_SOLVE_SECONDS, solve_seconds, elimination_seconds, speedup,
        hash_seconds, parse_seconds, rank_seconds,
        rank_metrics.ordered_sort_seconds, rank_metrics.rank_map_build_seconds,
        rank_metrics.compact_materialize_seconds, elimination_seconds, write_seconds, total_seconds,
        rank_metrics.shard_min_rows, rank_metrics.shard_max_rows,
        peak, HARD_RSS_BYTES, worker_json, merge_json);
    let temporary = output_result.with_extension("json.tmp");
    fs::write(&temporary, result).unwrap_or_else(|error| fail(error.to_string()));
    fs::rename(temporary, &output_result).unwrap_or_else(|error| fail(error.to_string()));
    println!(
        "PASS mode={} shards={} rank={:.6}s solve={:.6}s speedup={:.3} support={} rss={} total={:.3}s",
        rank_mode,
        rank_shards,
        rank_seconds,
        solve_seconds,
        speedup,
        candidate.len(),
        peak,
        total_seconds
    );
}
