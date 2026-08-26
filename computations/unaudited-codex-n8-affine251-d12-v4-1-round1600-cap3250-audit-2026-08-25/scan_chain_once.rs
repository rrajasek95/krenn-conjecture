use std::collections::HashMap;
use std::convert::TryInto;
use std::env;
use std::fs::{self, File};
use std::io::{BufReader, BufWriter, Read, Write};
use std::path::{Path, PathBuf};
use std::time::Instant;

const PRIME: u64 = 1_073_741_827;
const CP_MAGIC: &[u8; 12] = b"AFF12CEG1\0\0\0";
const VEC_MAGIC: &[u8; 12] = b"AFF12VEC1\0\0\0";
const FNV_OFFSET: u64 = 14_695_981_039_346_656_037;
const FNV_PRIME: u64 = 1_099_511_628_211;
const TARGET: [u8; 12] = [251; 12];

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("REJECT: {}", message.as_ref());
    std::process::exit(2);
}

fn read_exact<R: Read>(reader: &mut R, count: usize, label: &str) -> Vec<u8> {
    let mut answer = vec![0u8; count];
    reader.read_exact(&mut answer).unwrap_or_else(|_| fail(format!("truncated {label}")));
    answer
}

fn read_u64<R: Read>(reader: &mut R, label: &str) -> u64 {
    u64::from_le_bytes(read_exact(reader, 8, label).try_into().unwrap())
}

fn canonical(ids: &[u8]) -> bool {
    ids.windows(2).all(|pair| pair[0] <= pair[1])
}

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Column {
    word: u16,
    multiplier: [u8; 8],
}

struct Checkpoint {
    round: u64,
    support: u64,
    columns: Vec<Column>,
    candidate: HashMap<[u8; 12], u64>,
}

fn read_checkpoint(path: &Path, retain_candidate: bool) -> Checkpoint {
    let mut input = BufReader::with_capacity(1 << 20, File::open(path).unwrap());
    if read_exact(&mut input, 12, "checkpoint magic").as_slice() != CP_MAGIC {
        fail("checkpoint magic");
    }
    if read_u64(&mut input, "checkpoint prime") != PRIME {
        fail("checkpoint prime");
    }
    let round = read_u64(&mut input, "checkpoint round");
    let count = read_u64(&mut input, "checkpoint count") as usize;
    let support = read_u64(&mut input, "checkpoint support");
    let mut columns = Vec::with_capacity(count);
    for _ in 0..count {
        let word = u16::from_le_bytes(read_exact(&mut input, 2, "column word").try_into().unwrap());
        let mono = read_exact(&mut input, 13, "column mono");
        if word >= 6561 || mono[0] != 8 || !canonical(&mono[1..9]) || mono[9..] != [0; 4] {
            fail("checkpoint column encoding");
        }
        let column = Column { word, multiplier: mono[1..9].try_into().unwrap() };
        if columns.last().is_some_and(|old| old >= &column) {
            fail("checkpoint column order");
        }
        columns.push(column);
    }
    let mut candidate = HashMap::with_capacity(if retain_candidate { support as usize } else { 0 });
    let mut previous: Option<[u8; 12]> = None;
    let mut target = None;
    for _ in 0..support {
        let mono = read_exact(&mut input, 13, "candidate mono");
        let value = read_u64(&mut input, "candidate value");
        let row: [u8; 12] = mono[1..].try_into().unwrap();
        if mono[0] != 12 || !canonical(&row) || previous.is_some_and(|old| old >= row)
            || value == 0 || value >= PRIME {
            fail("checkpoint candidate encoding");
        }
        if row == TARGET { target = Some(value); }
        if retain_candidate && candidate.insert(row, value).is_some() {
            fail("duplicate candidate row");
        }
        previous = Some(row);
    }
    let mut trailing = [0u8; 1];
    if input.read(&mut trailing).unwrap() != 0 || target != Some(1) {
        fail("checkpoint trailing bytes or target normalization");
    }
    Checkpoint { round, support, columns, candidate }
}

fn descendant(parent: &[Column], child: &[Column]) -> bool {
    let (mut left, mut right) = (0usize, 0usize);
    while left < parent.len() {
        if right == child.len() { return false; }
        if child[right] < parent[left] { right += 1; }
        else if child[right] == parent[left] { left += 1; right += 1; }
        else { return false; }
    }
    true
}

struct VectorReader {
    input: BufReader<File>,
    provider: u64,
    expected_fingerprint: u64,
    count: usize,
    index: usize,
    columns: Vec<Column>,
    head: Option<(Column, usize)>,
}

impl VectorReader {
    fn open(path: &Path, columns: Vec<Column>) -> Self {
        let mut input = BufReader::with_capacity(1 << 20, File::open(path).unwrap());
        if read_exact(&mut input, 12, "vector magic").as_slice() != VEC_MAGIC
            || read_u64(&mut input, "vector prime") != PRIME {
            fail("vector header");
        }
        let provider = read_u64(&mut input, "provider fingerprint");
        let expected_fingerprint = read_u64(&mut input, "vector fingerprint");
        let count = read_u64(&mut input, "vector count") as usize;
        if count != columns.len() { fail("vector/checkpoint count"); }
        let mut answer = Self { input, provider, expected_fingerprint, count, index: 0, columns, head: None };
        answer.advance();
        answer
    }

    fn advance(&mut self) {
        if self.index == self.count { self.head = None; return; }
        let word_bytes = read_exact(&mut self.input, 2, "vector word");
        let word = u16::from_le_bytes(word_bytes.try_into().unwrap());
        let mono = read_exact(&mut self.input, 13, "vector multiplier");
        let size = read_u64(&mut self.input, "vector size") as usize;
        if mono[0] != 8 || !canonical(&mono[1..9]) || mono[9..] != [0; 4] || size == 0 || size > 700_000 {
            fail("vector record header");
        }
        let column = Column { word, multiplier: mono[1..9].try_into().unwrap() };
        if column != self.columns[self.index] { fail("vector/checkpoint column mismatch"); }
        self.head = Some((column, size));
    }
}

fn fnv(mut value: u64, bytes: &[u8]) -> u64 {
    for &byte in bytes { value = (value ^ byte as u64).wrapping_mul(FNV_PRIME); }
    value
}

fn head_bytes(column: Column, size: usize) -> Vec<u8> {
    let mut answer = Vec::with_capacity(23);
    answer.extend_from_slice(&column.word.to_le_bytes());
    answer.push(8);
    answer.extend_from_slice(&column.multiplier);
    answer.extend_from_slice(&[0; 4]);
    answer.extend_from_slice(&(size as u64).to_le_bytes());
    answer
}

fn main() {
    let arguments: Vec<String> = env::args().collect();
    if arguments.len() < 5 || (arguments.len() - 2) % 2 != 0 {
        fail("usage: scan_chain_once OUTPUT CP0 VEC0 [CP1 VEC1 ...]");
    }
    let output = PathBuf::from(&arguments[1]);
    let pairs: Vec<(PathBuf, PathBuf)> = arguments[2..].chunks(2)
        .map(|pair| (PathBuf::from(&pair[0]), PathBuf::from(&pair[1]))).collect();
    if pairs.len() != 7 { fail("exactly seven states required"); }
    let started = Instant::now();

    let mut checkpoints = Vec::new();
    for (index, (path, _)) in pairs.iter().enumerate() {
        checkpoints.push(read_checkpoint(path, index + 1 == pairs.len()));
    }
    for edge in 0..6 {
        if !descendant(&checkpoints[edge].columns, &checkpoints[edge + 1].columns) {
            fail(format!("checkpoint descendant edge {edge}"));
        }
    }
    let candidate = checkpoints.last_mut().unwrap().candidate.clone();
    let mut readers: Vec<VectorReader> = pairs.iter().enumerate().map(|(index, (_, path))| {
        VectorReader::open(path, std::mem::take(&mut checkpoints[index].columns))
    }).collect();
    let provider = readers[0].provider;
    if readers.iter().any(|reader| reader.provider != provider) { fail("provider fingerprint drift"); }

    let mut origin = [0usize; 7];
    let mut buffers: Vec<Vec<u8>> = (0..7).map(|_| vec![0u8; 21 * 65_536]).collect();
    let mut final_fingerprint = FNV_OFFSET;
    let mut terms = 0u64;
    let mut hit_terms = 0u64;
    let mut target_terms = 0u64;
    let mut failures = 0u64;
    loop {
        let key = readers.iter().filter_map(|reader| reader.head.map(|head| head.0)).min();
        let Some(key) = key else { break; };
        let present: Vec<usize> = readers.iter().enumerate()
            .filter_map(|(index, reader)| (reader.head.map(|head| head.0) == Some(key)).then_some(index)).collect();
        let first = present[0];
        if present != (first..7).collect::<Vec<_>>() { fail("cache descendant suffix"); }
        origin[first] += 1;
        let size = readers[first].head.unwrap().1;
        if present.iter().any(|&index| readers[index].head.unwrap().1 != size) { fail("inherited vector size drift"); }
        final_fingerprint = fnv(final_fingerprint, &head_bytes(key, size));
        let mut remaining = size;
        let mut previous: Option<[u8; 12]> = None;
        let mut pairing = 0u64;
        while remaining > 0 {
            let rows = remaining.min(65_536);
            let bytes = rows * 21;
            for &index in &present {
                readers[index].input.read_exact(&mut buffers[index][..bytes]).unwrap_or_else(|_| fail("truncated vector payload"));
            }
            let reference = &buffers[*present.last().unwrap()][..bytes];
            for &index in &present[..present.len() - 1] {
                if buffers[index][..bytes] != *reference { fail("inherited vector payload changed"); }
            }
            final_fingerprint = fnv(final_fingerprint, reference);
            for row in reference.chunks_exact(21) {
                let ids: [u8; 12] = row[1..13].try_into().unwrap();
                let value = u64::from_le_bytes(row[13..21].try_into().unwrap());
                if row[0] != 12 || !canonical(&ids) || previous.is_some_and(|old| old >= ids)
                    || value == 0 || value >= PRIME { fail("final vector row encoding"); }
                if let Some(&coefficient) = candidate.get(&ids) {
                    pairing = (pairing + ((value as u128 * coefficient as u128) % PRIME as u128) as u64) % PRIME;
                    hit_terms += 1;
                }
                if ids == TARGET { target_terms += 1; }
                previous = Some(ids);
                terms += 1;
            }
            remaining -= rows;
        }
        if pairing != 0 { failures += 1; }
        for &index in &present {
            readers[index].index += 1;
            readers[index].advance();
        }
    }
    for reader in &mut readers {
        if reader.index != reader.count || reader.head.is_some() { fail("vector count exhaustion"); }
        let mut trailing = [0u8; 1];
        if reader.input.read(&mut trailing).unwrap() != 0 { fail("vector trailing bytes"); }
    }
    if final_fingerprint != readers[6].expected_fingerprint || failures != 0 || target_terms != 2 {
        fail("final replay fingerprint/pairing/target");
    }
    let counts: Vec<usize> = readers.iter().map(|reader| reader.count).collect();
    for state in 0..7 {
        let expected: usize = origin[..=state].iter().sum();
        if expected != counts[state] { fail("cache origin census"); }
    }
    let checkpoint_rounds: Vec<u64> = checkpoints.iter().map(|x| x.round).collect();
    let checkpoint_supports: Vec<u64> = checkpoints.iter().map(|x| x.support).collect();
    let seconds = started.elapsed().as_secs_f64();
    let tmp = output.with_extension("json.tmp");
    let mut out = BufWriter::new(File::create(&tmp).unwrap());
    writeln!(out, "{{").unwrap();
    writeln!(out, "  \"schema\": \"KRENN_AFFINE251_D12_CHAIN_SINGLE_PASS_REPLAY_V1\",").unwrap();
    writeln!(out, "  \"status\": \"PASS_SIX_DESCENDANT_EDGES_AND_ALL_COLUMNS\",").unwrap();
    writeln!(out, "  \"rounds\": {:?},", checkpoint_rounds).unwrap();
    writeln!(out, "  \"supports\": {:?},", checkpoint_supports).unwrap();
    writeln!(out, "  \"columns\": {:?},", counts).unwrap();
    writeln!(out, "  \"new_records_by_origin\": {:?},", origin).unwrap();
    writeln!(out, "  \"checkpoint_descendant_edges\": 6,").unwrap();
    writeln!(out, "  \"cache_descendant_edges\": 6,").unwrap();
    writeln!(out, "  \"inherited_vectors_byte_identical\": true,").unwrap();
    writeln!(out, "  \"provider_fingerprint\": {provider},").unwrap();
    writeln!(out, "  \"final_vector_fingerprint\": {final_fingerprint},").unwrap();
    writeln!(out, "  \"terms_replayed\": {terms},").unwrap();
    writeln!(out, "  \"candidate_hit_terms\": {hit_terms},").unwrap();
    writeln!(out, "  \"target_terms\": {target_terms},").unwrap();
    writeln!(out, "  \"verification_failures\": {failures},").unwrap();
    writeln!(out, "  \"seconds\": {:.6}", seconds).unwrap();
    writeln!(out, "}}").unwrap();
    out.flush().unwrap();
    drop(out);
    fs::rename(tmp, output).unwrap();
    println!("PASS six edges, {} columns, {} terms, {:.3}s", counts[6], terms, seconds);
}
