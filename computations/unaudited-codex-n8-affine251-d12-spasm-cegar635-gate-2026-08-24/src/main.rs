//! Exact streaming bridge between the retained round-635 cache and SpaSM.

use std::collections::{BTreeMap, BTreeSet, HashMap};
use std::env;
use std::fs::{self, File};
use std::io::{BufRead, BufReader, BufWriter, Read, Write};
use std::path::{Path, PathBuf};
use std::time::Instant;

const PRIME: u64 = 1_073_741_827;
const COUNT: usize = 222_676;
const SUPPORT: usize = 315;
const ROUND: u64 = 635;
const T_ID: u8 = 251;
const CHECKPOINT_MAGIC: &[u8; 12] = b"AFF12CEG1\0\0\0";
const VECTOR_MAGIC: &[u8; 12] = b"AFF12VEC1\0\0\0";
const PROVIDER_FINGERPRINT: u64 = 9_218_588_987_274_412_661;
const VECTOR_FINGERPRINT: u64 = 6_593_799_974_443_584_084;
const FNV_OFFSET: u64 = 14_695_981_039_346_656_037;
const FNV_PRIME: u64 = 1_099_511_628_211;

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Mono {
    len: u8,
    ids: [u8; 12],
}

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct Column {
    word: u16,
    multiplier: Mono,
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("cegar635-spasm-bridge: {}", message.as_ref());
    std::process::exit(1)
}

fn read_u64<R: Read>(input: &mut R) -> u64 {
    let mut raw = [0u8; 8];
    input.read_exact(&mut raw).unwrap_or_else(|e| fail(e.to_string()));
    u64::from_le_bytes(raw)
}

fn read_mono<R: Read>(input: &mut R) -> Mono {
    let mut len = [0u8; 1];
    let mut ids = [0u8; 12];
    input.read_exact(&mut len).unwrap_or_else(|e| fail(e.to_string()));
    input.read_exact(&mut ids).unwrap_or_else(|e| fail(e.to_string()));
    if len[0] > 12 || !ids[..len[0] as usize].windows(2).all(|w| w[0] <= w[1]) {
        fail("bad monomial");
    }
    Mono { len: len[0], ids }
}

fn read_column<R: Read>(input: &mut R) -> Column {
    let mut word = [0u8; 2];
    input.read_exact(&mut word).unwrap_or_else(|e| fail(e.to_string()));
    let answer = Column { word: u16::from_le_bytes(word), multiplier: read_mono(input) };
    if answer.word >= 6561 || answer.multiplier.len != 8 {
        fail("bad column");
    }
    answer
}

fn no_trailing<R: Read>(input: &mut R) {
    let mut byte = [0u8; 1];
    if input.read(&mut byte).unwrap_or_else(|e| fail(e.to_string())) != 0 {
        fail("trailing bytes");
    }
}

fn fnv(mut hash: u64, bytes: &[u8]) -> u64 {
    for &byte in bytes {
        hash ^= byte as u64;
        hash = hash.wrapping_mul(FNV_PRIME);
    }
    hash
}

fn add_mod(sum: u64, product: u64) -> u64 {
    let value = sum + product;
    if value >= PRIME { value - PRIME } else { value }
}

fn mul_mod(a: u64, b: u64) -> u64 {
    (a as u128 * b as u128 % PRIME as u128) as u64
}

fn signed(value: u64) -> i64 {
    if value <= PRIME / 2 { value as i64 } else { value as i64 - PRIME as i64 }
}

fn read_checkpoint(path: &Path) -> (Vec<Column>, BTreeMap<Mono, u64>) {
    let mut input = BufReader::with_capacity(1 << 20, File::open(path).unwrap_or_else(|e| fail(e.to_string())));
    let mut magic = [0u8; 12];
    input.read_exact(&mut magic).unwrap_or_else(|e| fail(e.to_string()));
    if &magic != CHECKPOINT_MAGIC || read_u64(&mut input) != PRIME || read_u64(&mut input) != ROUND
        || read_u64(&mut input) != COUNT as u64 || read_u64(&mut input) != SUPPORT as u64 {
        fail("checkpoint header mismatch");
    }
    let mut columns = Vec::with_capacity(COUNT);
    for _ in 0..COUNT {
        let column = read_column(&mut input);
        if columns.last().is_some_and(|old| old >= &column) { fail("checkpoint columns not strict"); }
        columns.push(column);
    }
    let mut candidate = BTreeMap::new();
    for _ in 0..SUPPORT {
        let row = read_mono(&mut input);
        let value = read_u64(&mut input);
        if row.len != 12 || value == 0 || value >= PRIME || candidate.insert(row, value).is_some() {
            fail("bad checkpoint candidate");
        }
    }
    no_trailing(&mut input);
    let target = Mono { len: 12, ids: [T_ID; 12] };
    if candidate.get(&target).copied() != Some(1) { fail("checkpoint target not normalized"); }
    (columns, candidate)
}

struct Scan {
    rows: BTreeSet<Mono>,
    matrix_nnz: u64,
    rhs_nnz: u64,
    cache_bytes_read: u64,
}

fn scan_vectors(path: &Path, columns: &[Column], candidate: &BTreeMap<Mono, u64>) -> Scan {
    let target = Mono { len: 12, ids: [T_ID; 12] };
    let mut input = BufReader::with_capacity(8 << 20, File::open(path).unwrap_or_else(|e| fail(e.to_string())));
    let mut magic = [0u8; 12];
    input.read_exact(&mut magic).unwrap_or_else(|e| fail(e.to_string()));
    if &magic != VECTOR_MAGIC || read_u64(&mut input) != PRIME
        || read_u64(&mut input) != PROVIDER_FINGERPRINT {
        fail("vector header mismatch");
    }
    let expected_fingerprint = read_u64(&mut input);
    if expected_fingerprint != VECTOR_FINGERPRINT || read_u64(&mut input) != COUNT as u64 {
        fail("vector fingerprint/count mismatch");
    }
    let mut hash = FNV_OFFSET;
    let mut rows = BTreeSet::new();
    let mut matrix_nnz = 0u64;
    let mut rhs_nnz = 0u64;
    for (index, expected_column) in columns.iter().enumerate() {
        let column = read_column(&mut input);
        if &column != expected_column { fail(format!("checkpoint/vector column mismatch at {index}")); }
        let size = read_u64(&mut input);
        if size > 700_000 { fail("vector size out of contract"); }
        hash = fnv(hash, &column.word.to_le_bytes());
        hash = fnv(hash, &[column.multiplier.len]);
        hash = fnv(hash, &column.multiplier.ids);
        hash = fnv(hash, &size.to_le_bytes());
        let mut previous = None;
        let mut dot = 0u64;
        for _ in 0..size {
            let row = read_mono(&mut input);
            let value = read_u64(&mut input);
            if row.len != 12 || value == 0 || value >= PRIME || previous.is_some_and(|old| old >= row) {
                fail("bad cached vector record");
            }
            previous = Some(row);
            hash = fnv(hash, &[row.len]);
            hash = fnv(hash, &row.ids);
            hash = fnv(hash, &value.to_le_bytes());
            rows.insert(row);
            if row == target { rhs_nnz += 1; } else { matrix_nnz += 1; }
            if let Some(&weight) = candidate.get(&row) {
                dot = add_mod(dot, mul_mod(value, weight));
            }
        }
        if dot != 0 { fail(format!("retained tree solution violates cached column {index}")); }
    }
    no_trailing(&mut input);
    if hash != expected_fingerprint { fail("vector cache internal FNV mismatch"); }
    if !rows.contains(&target) { fail("target absent from cached rows"); }
    Scan { rows, matrix_nnz, rhs_nnz, cache_bytes_read: fs::metadata(path).unwrap().len() }
}

fn vector_header(input: &mut BufReader<File>) {
    let mut magic = [0u8; 12];
    input.read_exact(&mut magic).unwrap();
    if &magic != VECTOR_MAGIC || read_u64(input) != PRIME || read_u64(input) != PROVIDER_FINGERPRINT
        || read_u64(input) != VECTOR_FINGERPRINT || read_u64(input) != COUNT as u64 {
        fail("vector replay header mismatch");
    }
}

fn export_sms(vector_path: &Path, columns: &[Column], scan: &Scan,
              matrix_path: &Path, rhs_path: &Path, metadata_path: &Path, started: Instant) {
    let target = Mono { len: 12, ids: [T_ID; 12] };
    let variables: Vec<_> = scan.rows.iter().copied().filter(|row| *row != target).collect();
    let ids: HashMap<_, _> = variables.iter().enumerate().map(|(i, row)| (*row, i)).collect();
    let matrix_tmp = matrix_path.with_extension("sms.tmp");
    let rhs_tmp = rhs_path.with_extension("sms.tmp");
    let metadata_tmp = metadata_path.with_extension("json.tmp");
    let mut matrix = BufWriter::with_capacity(8 << 20, File::create(&matrix_tmp).unwrap());
    let mut rhs = BufWriter::with_capacity(1 << 20, File::create(&rhs_tmp).unwrap());
    writeln!(matrix, "{} {} M", variables.len(), COUNT).unwrap();
    writeln!(rhs, "1 {} M", COUNT).unwrap();
    let mut input = BufReader::with_capacity(8 << 20, File::open(vector_path).unwrap());
    vector_header(&mut input);
    let mut matrix_nnz = 0u64;
    let mut rhs_nnz = 0u64;
    for (equation, expected_column) in columns.iter().enumerate() {
        if read_column(&mut input) != *expected_column { fail("vector replay column mismatch"); }
        let size = read_u64(&mut input);
        for _ in 0..size {
            let row = read_mono(&mut input);
            let value = read_u64(&mut input);
            if row == target {
                writeln!(rhs, "1 {} {}", equation + 1, -signed(value)).unwrap();
                rhs_nnz += 1;
            } else {
                writeln!(matrix, "{} {} {}", ids[&row] + 1, equation + 1, signed(value)).unwrap();
                matrix_nnz += 1;
            }
        }
    }
    no_trailing(&mut input);
    if matrix_nnz != scan.matrix_nnz || rhs_nnz != scan.rhs_nnz { fail("export nnz mismatch"); }
    writeln!(matrix, "0 0 0").unwrap();
    writeln!(rhs, "0 0 0").unwrap();
    matrix.flush().unwrap(); rhs.flush().unwrap();
    drop(matrix); drop(rhs);
    fs::rename(&matrix_tmp, matrix_path).unwrap();
    fs::rename(&rhs_tmp, rhs_path).unwrap();
    let mut metadata = BufWriter::new(File::create(&metadata_tmp).unwrap());
    writeln!(metadata, "{{").unwrap();
    writeln!(metadata, "  \"schema\": \"KRENN_AFFINE251_D12_CEGAR635_SPASM_EXPORT_V1\",").unwrap();
    writeln!(metadata, "  \"status\": \"PASS\",").unwrap();
    writeln!(metadata, "  \"prime\": {PRIME},").unwrap();
    writeln!(metadata, "  \"round\": {ROUND},").unwrap();
    writeln!(metadata, "  \"equations_cached_columns\": {COUNT},").unwrap();
    writeln!(metadata, "  \"variables_excluding_target\": {},", variables.len()).unwrap();
    writeln!(metadata, "  \"row_union_including_target\": {},", scan.rows.len()).unwrap();
    writeln!(metadata, "  \"matrix_nnz\": {},", scan.matrix_nnz).unwrap();
    writeln!(metadata, "  \"rhs_nnz\": {},", scan.rhs_nnz).unwrap();
    writeln!(metadata, "  \"cache_bytes_read_per_pass\": {},", scan.cache_bytes_read).unwrap();
    writeln!(metadata, "  \"orientation\": \"SpaSM XA=B: X is non-target y; A is transpose of mathematical A^T; B=-target coefficients\",").unwrap();
    writeln!(metadata, "  \"retained_tree_candidate_verified_all_columns\": true,").unwrap();
    writeln!(metadata, "  \"elapsed_seconds\": {:.6}", started.elapsed().as_secs_f64()).unwrap();
    writeln!(metadata, "}}").unwrap();
    metadata.flush().unwrap(); drop(metadata);
    fs::rename(&metadata_tmp, metadata_path).unwrap();
}

fn mod_i128(value: i128) -> u64 {
    let p = PRIME as i128;
    let answer = ((value % p) + p) % p;
    answer as u64
}

fn read_solution(path: &Path, variables: usize) -> Vec<u64> {
    let input = BufReader::new(File::open(path).unwrap_or_else(|e| fail(e.to_string())));
    let mut lines = input.lines();
    let header = lines.next().unwrap_or_else(|| fail("empty solution")).unwrap();
    if header != format!("1 {variables} M") { fail("solution header mismatch"); }
    let mut answer = vec![0u64; variables];
    let mut terminated = false;
    for line in lines {
        let line = line.unwrap();
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.len() != 3 { fail("bad solution line"); }
        let i: usize = fields[0].parse().unwrap_or_else(|_| fail("bad solution row"));
        let j: usize = fields[1].parse().unwrap_or_else(|_| fail("bad solution column"));
        let value: i128 = fields[2].parse().unwrap_or_else(|_| fail("bad solution value"));
        if (i, j, value) == (0, 0, 0) { terminated = true; break; }
        if i != 1 || j == 0 || j > variables || answer[j - 1] != 0 { fail("solution index/duplicate"); }
        let value = mod_i128(value);
        if value == 0 { fail("explicit zero solution entry"); }
        answer[j - 1] = value;
    }
    if !terminated { fail("solution terminator missing"); }
    Ok::<(), ()>(()).unwrap();
    answer
}

fn verify_solution(vector_path: &Path, columns: &[Column], scan: &Scan,
                   solution_path: &Path, output_path: &Path, started: Instant) {
    let target = Mono { len: 12, ids: [T_ID; 12] };
    let variables: Vec<_> = scan.rows.iter().copied().filter(|row| *row != target).collect();
    let values = read_solution(solution_path, variables.len());
    let weights: HashMap<_, _> = variables.iter().copied().zip(values.iter().copied())
        .filter(|(_, value)| *value != 0).collect();
    let mut input = BufReader::with_capacity(8 << 20, File::open(vector_path).unwrap());
    vector_header(&mut input);
    let mut checked_nnz = 0u64;
    for (index, expected_column) in columns.iter().enumerate() {
        if read_column(&mut input) != *expected_column { fail("verify column mismatch"); }
        let size = read_u64(&mut input);
        let mut dot = 0u64;
        for _ in 0..size {
            let row = read_mono(&mut input);
            let coefficient = read_u64(&mut input);
            let weight = if row == target { 1 } else { weights.get(&row).copied().unwrap_or(0) };
            dot = add_mod(dot, mul_mod(coefficient, weight));
            checked_nnz += 1;
        }
        if dot != 0 { fail(format!("SpaSM solution violates cached column {index}")); }
    }
    no_trailing(&mut input);
    let tmp = output_path.with_extension("json.tmp");
    let mut out = BufWriter::new(File::create(&tmp).unwrap());
    writeln!(out, "{{").unwrap();
    writeln!(out, "  \"schema\": \"KRENN_AFFINE251_D12_CEGAR635_SPASM_SOLUTION_AUDIT_V1\",").unwrap();
    writeln!(out, "  \"status\": \"PASS\",").unwrap();
    writeln!(out, "  \"prime\": {PRIME},").unwrap();
    writeln!(out, "  \"round\": {ROUND},").unwrap();
    writeln!(out, "  \"target_value\": 1,").unwrap();
    writeln!(out, "  \"cached_columns_annihilated\": {COUNT},").unwrap();
    writeln!(out, "  \"cached_nonzeros_checked\": {checked_nnz},").unwrap();
    writeln!(out, "  \"solution_support_excluding_target\": {},", weights.len()).unwrap();
    writeln!(out, "  \"elapsed_seconds\": {:.6}", started.elapsed().as_secs_f64()).unwrap();
    writeln!(out, "}}").unwrap();
    out.flush().unwrap(); drop(out); fs::rename(tmp, output_path).unwrap();
}

fn args() -> HashMap<String, String> {
    let raw: Vec<_> = env::args().collect();
    let mut answer = HashMap::new();
    let mut i = 1;
    while i < raw.len() {
        if !raw[i].starts_with("--") || i + 1 == raw.len() || answer.insert(raw[i].clone(), raw[i + 1].clone()).is_some() {
            fail("arguments must be unique --key value pairs");
        }
        i += 2;
    }
    answer
}

fn main() {
    let started = Instant::now();
    let args = args();
    let get = |key: &str| PathBuf::from(args.get(key).cloned().unwrap_or_else(|| fail(format!("missing {key}"))));
    let mode = args.get("--mode").cloned().unwrap_or_else(|| fail("missing --mode"));
    let checkpoint = get("--checkpoint");
    let vectors = get("--vectors");
    let (columns, candidate) = read_checkpoint(&checkpoint);
    let scan = scan_vectors(&vectors, &columns, &candidate);
    match mode.as_str() {
        "export" => export_sms(&vectors, &columns, &scan, &get("--matrix"), &get("--rhs"), &get("--metadata"), started),
        "verify" => verify_solution(&vectors, &columns, &scan, &get("--solution"), &get("--output"), started),
        _ => fail("mode must be export or verify"),
    }
}
