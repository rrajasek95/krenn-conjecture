use std::collections::BTreeMap;
use std::env;
use std::fs::File;
use std::io::{BufReader, BufWriter, Read, Write};
use std::path::{Path, PathBuf};
use std::time::Instant;

const PRIME: u64 = 1_073_741_827;
const TARGET: [u8; 12] = [251; 12];
const CHECKPOINT_MAGIC: &[u8; 12] = b"AFF12CEG1\0\0\0";
const VECTOR_MAGIC: &[u8; 12] = b"AFF12VEC1\0\0\0";
const FNV_OFFSET: u64 = 14_695_981_039_346_656_037;
const FNV_PRIME: u64 = 1_099_511_628_211;

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("hierarchical-integration-audit: {}", message.as_ref());
    std::process::exit(2)
}

fn read_exact<const N: usize>(input: &mut impl Read, label: &str) -> [u8; N] {
    let mut bytes = [0u8; N];
    input.read_exact(&mut bytes).unwrap_or_else(|_| fail(format!("truncated {label}")));
    bytes
}

fn read_u64(input: &mut impl Read, label: &str) -> u64 {
    u64::from_le_bytes(read_exact(input, label))
}

fn read_mono(input: &mut impl Read, degree: usize, label: &str) -> [u8; 12] {
    let actual = read_exact::<1>(input, label)[0] as usize;
    let ids = read_exact::<12>(input, label);
    if actual != degree || ids[..degree].windows(2).any(|pair| pair[0] > pair[1])
        || ids[degree..].iter().any(|&value| value != 0)
    {
        fail(format!("bad {label}"));
    }
    ids
}

fn fnv(hash: &mut u64, bytes: &[u8]) {
    for &byte in bytes {
        *hash ^= byte as u64;
        *hash = hash.wrapping_mul(FNV_PRIME);
    }
}

type Column = (u16, [u8; 12]);

fn checkpoint(path: &Path, expected_round: u64, expected_columns: usize,
              expected_support: usize) -> (Vec<Column>, BTreeMap<[u8; 12], u64>) {
    let mut input = BufReader::new(File::open(path).unwrap_or_else(|e| fail(e.to_string())));
    if &read_exact::<12>(&mut input, "checkpoint magic") != CHECKPOINT_MAGIC
        || read_u64(&mut input, "checkpoint prime") != PRIME
        || read_u64(&mut input, "checkpoint round") != expected_round
    {
        fail("checkpoint header mismatch");
    }
    let count = read_u64(&mut input, "checkpoint columns") as usize;
    let support = read_u64(&mut input, "checkpoint support") as usize;
    if count != expected_columns || support != expected_support { fail("checkpoint census mismatch"); }
    let mut columns = Vec::with_capacity(count);
    for _ in 0..count {
        let word = u16::from_le_bytes(read_exact(&mut input, "checkpoint word"));
        let multiplier = read_mono(&mut input, 8, "checkpoint multiplier");
        let column = (word, multiplier);
        if word >= 6561 || columns.last().is_some_and(|old| old >= &column) {
            fail("checkpoint column order/range");
        }
        columns.push(column);
    }
    let mut candidate = BTreeMap::new();
    for _ in 0..support {
        let row = read_mono(&mut input, 12, "checkpoint row");
        let value = read_u64(&mut input, "checkpoint value");
        if value == 0 || value >= PRIME || candidate.insert(row, value).is_some() {
            fail("checkpoint candidate entry");
        }
    }
    let mut trailing = [0u8; 1];
    if input.read(&mut trailing).unwrap_or_else(|e| fail(e.to_string())) != 0 {
        fail("checkpoint trailing bytes");
    }
    if candidate.get(&TARGET) != Some(&1) { fail("target normalization"); }
    (columns, candidate)
}

fn main() {
    let mut checkpoint_path = None::<PathBuf>;
    let mut vector_path = None::<PathBuf>;
    let mut output_path = None::<PathBuf>;
    let mut expected_round = None::<u64>;
    let mut expected_columns = None::<usize>;
    let mut expected_support = None::<usize>;
    let args: Vec<_> = env::args().collect();
    let mut index = 1;
    while index < args.len() {
        if index + 1 == args.len() { fail("expected --key value"); }
        match args[index].as_str() {
            "--checkpoint" => checkpoint_path = Some(PathBuf::from(&args[index + 1])),
            "--vectors" => vector_path = Some(PathBuf::from(&args[index + 1])),
            "--output" => output_path = Some(PathBuf::from(&args[index + 1])),
            "--round" => expected_round = Some(args[index + 1].parse().unwrap_or_else(|_| fail("bad round"))),
            "--columns" => expected_columns = Some(args[index + 1].parse().unwrap_or_else(|_| fail("bad columns"))),
            "--support" => expected_support = Some(args[index + 1].parse().unwrap_or_else(|_| fail("bad support"))),
            _ => fail("unknown argument"),
        }
        index += 2;
    }
    let checkpoint_path = checkpoint_path.unwrap_or_else(|| fail("missing checkpoint"));
    let vector_path = vector_path.unwrap_or_else(|| fail("missing vectors"));
    let output_path = output_path.unwrap_or_else(|| fail("missing output"));
    let expected_round = expected_round.unwrap_or_else(|| fail("missing round"));
    let expected_columns = expected_columns.unwrap_or_else(|| fail("missing columns"));
    let expected_support = expected_support.unwrap_or_else(|| fail("missing support"));
    let started = Instant::now();
    let (columns, candidate) = checkpoint(&checkpoint_path, expected_round,
                                          expected_columns, expected_support);
    let mut input = BufReader::with_capacity(1 << 20,
        File::open(&vector_path).unwrap_or_else(|e| fail(e.to_string())));
    if &read_exact::<12>(&mut input, "vector magic") != VECTOR_MAGIC
        || read_u64(&mut input, "vector prime") != PRIME
    {
        fail("vector header mismatch");
    }
    let provider_fingerprint = read_u64(&mut input, "provider fingerprint");
    let expected_fingerprint = read_u64(&mut input, "vector fingerprint");
    let count = read_u64(&mut input, "vector count") as usize;
    if count != columns.len() { fail("vector/checkpoint count mismatch"); }
    let mut vector_fingerprint = FNV_OFFSET;
    let mut terms = 0u64;
    let mut hits = 0u64;
    let mut target_terms = 0u64;
    let mut failures = 0usize;
    let mut previous_column = None::<Column>;
    for expected in &columns {
        let word_bytes = read_exact::<2>(&mut input, "vector word");
        let word = u16::from_le_bytes(word_bytes);
        let degree = read_exact::<1>(&mut input, "vector multiplier degree");
        let multiplier = read_exact::<12>(&mut input, "vector multiplier");
        let size_bytes = read_exact::<8>(&mut input, "vector size");
        let size = u64::from_le_bytes(size_bytes);
        let column = (word, multiplier);
        if degree[0] != 8 || multiplier[..8].windows(2).any(|p| p[0] > p[1])
            || multiplier[8..].iter().any(|&x| x != 0) || word >= 6561
            || &column != expected || previous_column.is_some_and(|old| old >= column)
            || size == 0 || size > 700_000
        {
            fail("bad vector column record");
        }
        previous_column = Some(column);
        fnv(&mut vector_fingerprint, &word_bytes);
        fnv(&mut vector_fingerprint, &degree);
        fnv(&mut vector_fingerprint, &multiplier);
        fnv(&mut vector_fingerprint, &size_bytes);
        let mut previous_row = None::<[u8; 12]>;
        let mut pairing = 0u64;
        for _ in 0..size {
            let row_degree = read_exact::<1>(&mut input, "vector row degree");
            let row = read_exact::<12>(&mut input, "vector row");
            let value_bytes = read_exact::<8>(&mut input, "vector value");
            let value = u64::from_le_bytes(value_bytes);
            if row_degree[0] != 12 || row.windows(2).any(|p| p[0] > p[1])
                || previous_row.is_some_and(|old| old >= row) || value == 0 || value >= PRIME
            {
                fail("bad vector term record");
            }
            previous_row = Some(row);
            fnv(&mut vector_fingerprint, &row_degree);
            fnv(&mut vector_fingerprint, &row);
            fnv(&mut vector_fingerprint, &value_bytes);
            if let Some(&coefficient) = candidate.get(&row) {
                pairing = ((pairing as u128 + value as u128 * coefficient as u128)
                    % PRIME as u128) as u64;
                hits += 1;
            }
            if row == TARGET { target_terms += 1; }
            terms += 1;
        }
        if pairing != 0 { failures += 1; }
    }
    let mut trailing = [0u8; 1];
    if input.read(&mut trailing).unwrap_or_else(|e| fail(e.to_string())) != 0 {
        fail("vector trailing bytes");
    }
    if vector_fingerprint != expected_fingerprint { fail("vector FNV mismatch"); }
    if failures != 0 { fail(format!("candidate violates {failures} cached columns")); }
    let temporary = output_path.with_extension("json.tmp");
    let mut output = BufWriter::new(File::create(&temporary).unwrap_or_else(|e| fail(e.to_string())));
    writeln!(output, "{{").unwrap();
    writeln!(output, "  \"schema\": \"KRENN_AFFINE251_D12_CACHE_REPLAY_V1\",").unwrap();
    writeln!(output, "  \"status\": \"PASS_ALL_COLUMNS\",").unwrap();
    writeln!(output, "  \"round\": {expected_round},").unwrap();
    writeln!(output, "  \"columns_replayed\": {count},").unwrap();
    writeln!(output, "  \"terms_replayed\": {terms},").unwrap();
    writeln!(output, "  \"candidate_hit_terms\": {hits},").unwrap();
    writeln!(output, "  \"target_terms\": {target_terms},").unwrap();
    writeln!(output, "  \"verification_failures\": {failures},").unwrap();
    writeln!(output, "  \"provider_fingerprint\": {provider_fingerprint},").unwrap();
    writeln!(output, "  \"vector_fingerprint\": {expected_fingerprint},").unwrap();
    writeln!(output, "  \"seconds\": {:.6}", started.elapsed().as_secs_f64()).unwrap();
    writeln!(output, "}}").unwrap();
    output.flush().unwrap(); drop(output);
    std::fs::rename(temporary, output_path).unwrap_or_else(|e| fail(e.to_string()));
}
