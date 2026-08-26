//! Exact disk-partitioned aggregation of the factored full y10 transfer.
//!
//! This realizes the circuit exported by audit_factored_y10_transfer.py:
//!
//! C10 = R10 - R8*h2 + R7*S3 + R6*S4 + L(R9).
//!
//! Records are hash-partitioned before reduction, keeping the peak memory
//! independent of the terminal support size.  The terminal support is then
//! screened against the 2,206 literal N4 three-term leading blocks.

use std::collections::{BTreeMap, HashMap, HashSet};
use std::env;
use std::fs::{create_dir_all, File};
use std::hash::{Hash, Hasher};
use std::io::{BufRead, BufReader, BufWriter, Read, Write};
use std::path::Path;
use std::time::Instant;

const BUCKETS: usize = 64;

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("aggregate-full-y10: {}", message.as_ref());
    std::process::exit(2);
}

#[derive(Clone, Copy, Eq, Ord, PartialEq, PartialOrd)]
struct Key10([u8; 10]);

impl Hash for Key10 {
    fn hash<H: Hasher>(&self, state: &mut H) { self.0.hash(state); }
}

fn hex(bytes: &[u8]) -> String {
    let mut answer = String::with_capacity(2 * bytes.len());
    for value in bytes { answer.push_str(&format!("{value:02x}")); }
    answer
}

fn decode_hex(text: &str) -> Vec<u8> {
    if text.len() % 2 != 0 { fail("odd monomial hex"); }
    let mut answer = Vec::with_capacity(text.len() / 2);
    for index in 0..text.len() / 2 {
        answer.push(u8::from_str_radix(&text[2 * index..2 * index + 2], 16)
            .unwrap_or_else(|_| fail("bad monomial hex")));
    }
    if !answer.windows(2).all(|window| window[0] <= window[1]) {
        fail("unsorted monomial");
    }
    answer
}

fn multiply(left: &[u8], right: &[u8]) -> Key10 {
    if left.len() + right.len() != 10 { fail("product is not y-degree ten"); }
    let mut data = [0_u8; 10];
    let (mut i, mut j, mut k) = (0, 0, 0);
    while i < left.len() || j < right.len() {
        if j == right.len() || (i < left.len() && left[i] <= right[j]) {
            data[k] = left[i]; i += 1;
        } else {
            data[k] = right[j]; j += 1;
        }
        k += 1;
    }
    Key10(data)
}

fn bucket(key: Key10) -> usize {
    let mut hash = 0xcbf29ce484222325_u64;
    for byte in key.0 {
        hash ^= byte as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    (hash as usize) & (BUCKETS - 1)
}

fn read_residual(path: &Path, expected_degree: usize) -> Vec<(Vec<u8>, i64)> {
    let input = BufReader::new(File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    let mut expected = None;
    let mut answer = Vec::new();
    for (line_number, line) in input.lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if line_number == 0 {
            if fields.len() != 5 || fields[1..4] != ["SCALE", "4", "COUNT"] {
                fail(format!("bad residual header {}", path.display()));
            }
            expected = Some(fields[4].parse::<usize>().unwrap_or_else(|_| fail("bad row count")));
            continue;
        }
        if fields.len() != 3 || fields[0] != "ROW" { fail("bad residual row"); }
        let row = decode_hex(fields[1]);
        if row.len() != expected_degree { fail("residual degree changed"); }
        let coefficient = fields[2].parse::<i64>().unwrap_or_else(|_| fail("bad coefficient"));
        if coefficient == 0 { fail("zero residual coefficient"); }
        answer.push((row, coefficient));
    }
    if expected != Some(answer.len()) { fail("residual count changed"); }
    answer
}

fn read_kernels(path: &Path) -> HashMap<String, Vec<(Vec<u8>, i64)>> {
    let input = BufReader::new(File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    let mut answer: HashMap<String, Vec<(Vec<u8>, i64)>> = HashMap::new();
    let mut active: Option<String> = None;
    for line in input.lines() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.first() == Some(&"BEGIN") {
            active = Some(fields[1].to_string());
        } else if fields.first() == Some(&"END") {
            active = None;
        } else if fields.first() == Some(&"ROW") {
            let label = active.as_ref().unwrap_or_else(|| fail("kernel row outside section"));
            answer.entry(label.clone()).or_default().push((
                decode_hex(fields[1]),
                fields[2].parse().unwrap_or_else(|_| fail("bad kernel coefficient")),
            ));
        }
    }
    for (label, count) in [("H2", 12), ("S3", 66), ("S4", 244)] {
        if answer.get(label).map(Vec::len) != Some(count) { fail(format!("{label} profile changed")); }
    }
    answer
}

fn read_linear_quadratic(path: &Path) -> HashMap<u8, Vec<(Vec<u8>, i64)>> {
    let input = BufReader::new(File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    let mut answer: HashMap<u8, Vec<(Vec<u8>, i64)>> = HashMap::new();
    for line in input.lines() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.first() == Some(&"L2") {
            let cell: u8 = fields[1].parse().unwrap_or_else(|_| fail("bad L2 cell"));
            answer.entry(cell).or_default().push((
                decode_hex(fields[2]),
                fields[3].parse().unwrap_or_else(|_| fail("bad L2 coefficient")),
            ));
        }
    }
    if answer.len() != 240 || answer.values().any(|rows| rows.len() != 6) {
        fail("linear quadratic provider changed");
    }
    answer
}

#[derive(Clone)]
struct Block {
    terms: [[u8; 2]; 3],
}

fn read_blocks(path: &Path) -> (Vec<Block>, HashMap<[u8; 2], usize>) {
    let input = BufReader::new(File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    let mut blocks = Vec::new();
    let mut term_to_block = HashMap::new();
    for line in input.lines() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.first() != Some(&"BLOCK") { continue; }
        let terms_field = fields.iter().find(|field| field.starts_with("TERMS="))
            .unwrap_or_else(|| fail("block has no terms"));
        let terms_vec: Vec<_> = terms_field[6..].split(',').map(|text| {
            let decoded = decode_hex(text);
            if decoded.len() != 2 { fail("block term is not quadratic"); }
            [decoded[0], decoded[1]]
        }).collect();
        if terms_vec.len() != 3 { fail("block lost its three terms"); }
        let terms = [terms_vec[0], terms_vec[1], terms_vec[2]];
        let index = blocks.len();
        for term in terms {
            if term_to_block.insert(term, index).is_some() { fail("quadratic terms are not disjoint"); }
        }
        blocks.push(Block { terms });
    }
    if blocks.len() != 2206 || term_to_block.len() != 6618 { fail("PM4 census changed"); }
    (blocks, term_to_block)
}

fn emit(writers: &mut [BufWriter<File>], key: Key10, coefficient: i64) {
    if coefficient == 0 { return; }
    let writer = &mut writers[bucket(key)];
    writer.write_all(&key.0).unwrap_or_else(|error| fail(error.to_string()));
    writer.write_all(&coefficient.to_le_bytes()).unwrap_or_else(|error| fail(error.to_string()));
}

fn convolve_emit(writers: &mut [BufWriter<File>], rows: &[(Vec<u8>, i64)],
                 kernel: &[(Vec<u8>, i64)], sign: i64) -> u64 {
    let mut count = 0_u64;
    for (row, coefficient) in rows {
        for (term, term_coefficient) in kernel {
            emit(writers, multiply(row, term), coefficient * term_coefficient * sign);
            count += 1;
        }
    }
    count
}

fn remove_pair(row: Key10, pair: [u8; 2]) -> Vec<u8> {
    let mut remaining = row.0.to_vec();
    for cell in pair {
        let position = remaining.iter().position(|&value| value == cell)
            .unwrap_or_else(|| fail("pair does not divide row"));
        remaining.remove(position);
    }
    remaining
}

fn incident_blocks(row: Key10, term_to_block: &HashMap<[u8; 2], usize>) -> Vec<(usize, [u8; 2])> {
    let mut answer = Vec::new();
    let mut seen = HashSet::new();
    for i in 0..10 {
        for j in i + 1..10 {
            let pair = [row.0[i], row.0[j]];
            if let Some(&block) = term_to_block.get(&pair) {
                if seen.insert((block, pair)) { answer.push((block, pair)); }
            }
        }
    }
    answer.sort_unstable();
    answer
}

fn main() {
    let arguments: Vec<_> = env::args().collect();
    if arguments.len() != 3 { fail("usage: aggregate-full-y10 ARTIFACT_DIR SCRATCH_DIR"); }
    let artifact = Path::new(&arguments[1]);
    let scratch = Path::new(&arguments[2]);
    create_dir_all(scratch).unwrap_or_else(|error| fail(error.to_string()));
    let started = Instant::now();

    let residual = |degree: usize| read_residual(
        &artifact.join(format!("direct_fh_original_y{degree}_residual.txt")), degree);
    let r6 = residual(6);
    let r7 = residual(7);
    let r8 = residual(8);
    let r9 = residual(9);
    let r10 = residual(10);
    let kernels = read_kernels(&artifact.join("direct_fh_transfer_kernels.txt"));
    let linear = read_linear_quadratic(&artifact.join("direct_fh_unique_min_provider.txt"));
    let (blocks, term_to_block) = read_blocks(&artifact.join("quadratic_pm4_blocks.txt"));
    eprintln!("inputs R6={} R7={} R8={} R9={} R10={} elapsed={:.1}s",
        r6.len(), r7.len(), r8.len(), r9.len(), r10.len(), started.elapsed().as_secs_f64());

    let mut writers: Vec<_> = (0..BUCKETS).map(|index| {
        let path = scratch.join(format!("bucket-{index:03}.bin"));
        BufWriter::with_capacity(1 << 20, File::create(path).unwrap_or_else(|error| fail(error.to_string())))
    }).collect();
    let mut emitted = 0_u64;
    for (row, coefficient) in &r10 {
        emit(&mut writers, multiply(row, &[]), *coefficient);
        emitted += 1;
    }
    emitted += convolve_emit(&mut writers, &r8, kernels.get("H2").unwrap(), -1);
    eprintln!("emitted through R8*h2={} elapsed={:.1}s", emitted, started.elapsed().as_secs_f64());
    emitted += convolve_emit(&mut writers, &r7, kernels.get("S3").unwrap(), 1);
    eprintln!("emitted through R7*S3={} elapsed={:.1}s", emitted, started.elapsed().as_secs_f64());
    emitted += convolve_emit(&mut writers, &r6, kernels.get("S4").unwrap(), 1);
    eprintln!("emitted through R6*S4={} elapsed={:.1}s", emitted, started.elapsed().as_secs_f64());
    for (row, coefficient) in &r9 {
        let cell = row[0];
        let quotient = &row[1..];
        for (term, term_coefficient) in linear.get(&cell).unwrap_or_else(|| fail("R9 chose support cell")) {
            emit(&mut writers, multiply(quotient, term), -coefficient * term_coefficient);
            emitted += 1;
        }
    }
    drop(writers);
    eprintln!("emitted total={} elapsed={:.1}s", emitted, started.elapsed().as_secs_f64());

    let mut support = 0_u64;
    let mut coefficient_histogram: BTreeMap<i64, u64> = BTreeMap::new();
    let mut incidence_histogram: BTreeMap<usize, u64> = BTreeMap::new();
    let mut lex_dead: Option<(Key10, i64)> = None;
    let mut lex_live: Option<(Key10, i64, Vec<(usize, [u8; 2])>)> = None;
    for index in 0..BUCKETS {
        let path = scratch.join(format!("bucket-{index:03}.bin"));
        let mut reader = BufReader::with_capacity(1 << 20,
            File::open(&path).unwrap_or_else(|error| fail(error.to_string())));
        let mut map: HashMap<Key10, i64> = HashMap::new();
        let mut record = [0_u8; 18];
        loop {
            match reader.read_exact(&mut record) {
                Ok(()) => {},
                Err(error) if error.kind() == std::io::ErrorKind::UnexpectedEof => break,
                Err(error) => fail(error.to_string()),
            }
            let mut key = [0_u8; 10];
            key.copy_from_slice(&record[..10]);
            let mut coefficient = [0_u8; 8];
            coefficient.copy_from_slice(&record[10..]);
            let value = i64::from_le_bytes(coefficient);
            let entry = map.entry(Key10(key)).or_insert(0);
            *entry = entry.checked_add(value).unwrap_or_else(|| fail("coefficient overflow"));
        }
        for (row, coefficient) in map {
            if coefficient == 0 { continue; }
            support += 1;
            *coefficient_histogram.entry(coefficient).or_insert(0) += 1;
            let incidence = incident_blocks(row, &term_to_block);
            *incidence_histogram.entry(incidence.len()).or_insert(0) += 1;
            if incidence.is_empty() && lex_dead.map_or(true, |old| row < old.0) {
                lex_dead = Some((row, coefficient));
            }
            if !incidence.is_empty() && lex_live.as_ref().map_or(true, |old| row < old.0) {
                lex_live = Some((row, coefficient, incidence));
            }
        }
        if (index + 1) % 16 == 0 {
            eprintln!("reduced buckets={} support={} elapsed={:.1}s", index + 1, support, started.elapsed().as_secs_f64());
        }
    }

    // Re-reduce only the buckets needed for the lex-first live cell's one-hop
    // N4 outputs, so the local target-rooted packet records their coefficients.
    let live = lex_live.unwrap_or_else(|| fail("terminal support has no N4 incidence"));
    let mut query = HashSet::new();
    for &(block_index, pair) in &live.2 {
        let multiplier = remove_pair(live.0, pair);
        for term in blocks[block_index].terms {
            query.insert(multiply(&multiplier, &term));
        }
    }
    let query_buckets: HashSet<_> = query.iter().copied().map(bucket).collect();
    let mut query_values: HashMap<Key10, i64> = HashMap::new();
    for index in query_buckets {
        let path = scratch.join(format!("bucket-{index:03}.bin"));
        let mut reader = BufReader::new(File::open(path).unwrap_or_else(|error| fail(error.to_string())));
        let mut record = [0_u8; 18];
        loop {
            match reader.read_exact(&mut record) {
                Ok(()) => {},
                Err(error) if error.kind() == std::io::ErrorKind::UnexpectedEof => break,
                Err(error) => fail(error.to_string()),
            }
            let mut key_bytes = [0_u8; 10]; key_bytes.copy_from_slice(&record[..10]);
            let key = Key10(key_bytes);
            if !query.contains(&key) { continue; }
            let mut coefficient = [0_u8; 8]; coefficient.copy_from_slice(&record[10..]);
            *query_values.entry(key).or_insert(0) += i64::from_le_bytes(coefficient);
        }
    }

    let result_path = artifact.join("results_full_y10_aggregate.txt");
    let mut result = BufWriter::new(File::create(&result_path).unwrap_or_else(|error| fail(error.to_string())));
    writeln!(result, "KRENN_N8_DIRECT_FH_FULL_Y10_AGGREGATE_V1").unwrap();
    writeln!(result, "FORMULA C10=R10-R8*h2+R7*S3+R6*S4+L(R9) SCALE 4").unwrap();
    writeln!(result, "EMITTED {emitted}").unwrap();
    writeln!(result, "SUPPORT {support}").unwrap();
    write!(result, "COEFFICIENT_HIST").unwrap();
    for (coefficient, count) in coefficient_histogram { write!(result, " {coefficient}:{count}").unwrap(); }
    writeln!(result).unwrap();
    write!(result, "INCIDENCE_HIST").unwrap();
    for (incidence, count) in incidence_histogram { write!(result, " {incidence}:{count}").unwrap(); }
    writeln!(result).unwrap();
    if let Some((row, coefficient)) = lex_dead {
        writeln!(result, "LEX_DEAD {} {}", hex(&row.0), coefficient).unwrap();
    } else {
        writeln!(result, "LEX_DEAD NONE").unwrap();
    }
    writeln!(result, "LEX_LIVE {} {} INCIDENT {}", hex(&live.0.0), live.1, live.2.len()).unwrap();
    for (block_index, pair) in live.2 {
        let multiplier = remove_pair(live.0, pair);
        writeln!(result, "COLUMN block={} pivot={} multiplier={}", block_index, hex(&pair), hex(&multiplier)).unwrap();
        for term in blocks[block_index].terms {
            let output = multiply(&multiplier, &term);
            writeln!(result, "OUTPUT {} coefficient={}", hex(&output.0), query_values.get(&output).copied().unwrap_or(0)).unwrap();
        }
    }
    writeln!(result, "SCOPE exact chosen-right-inverse y10 support; dead rows obstruct this deterministic extension only, not all lower-kernel choices").unwrap();
    result.flush().unwrap();
    eprintln!("PASS support={} result={} elapsed={:.1}s", support, result_path.display(), started.elapsed().as_secs_f64());
}
