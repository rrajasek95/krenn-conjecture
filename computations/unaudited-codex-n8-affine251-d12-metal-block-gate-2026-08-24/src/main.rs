use std::collections::{HashMap, HashSet};
use std::env;
use std::fs::{self, File};
use std::io::{BufReader, BufWriter, Read, Write};
use std::path::{Path, PathBuf};
use std::process::Command;
use std::time::Instant;

const VECTOR_MAGIC: &[u8; 12] = b"AFF12VEC1\0\0\0";
const CHECKPOINT_MAGIC: &[u8; 12] = b"AFF12CEG1\0\0\0";
const OUTPUT_MAGIC: &[u8; 16] = b"D12CSRCSCV1\0\0\0\0\0";
const HEADER_BYTES: usize = 256;
const PRIME: u64 = 1_073_741_827;
const PROVIDER_FINGERPRINT: u64 = 9_218_588_987_274_412_661;
const RECORDS: usize = 222_676;
const ROUND: u64 = 635;
const CANDIDATE_SUPPORT: usize = 315;
const MAX_COEFFICIENT: i64 = 1_440;
const SOURCE_SHA256: &str = "dd74d7392a005fb9c7726d9a0cc5c86e5b16d987bcb707d1c3a0f90e6e4d9e40";
const CHECKPOINT_SHA256: &str = "761804372a3f7e12b1915dd2718f7f69ef00b799dc6f90cd083b2fa7d2fc3c88";

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Column {
    word: u16,
    multiplier: [u8; 12],
}

#[derive(Clone)]
struct Candidate {
    row: [u8; 12],
    value: u32,
    dense: Option<u32>,
}

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
    let args: Vec<String> = env::args().collect();
    let index = args.iter().position(|item| item == name)
        .unwrap_or_else(|| fail(format!("missing {name}")));
    require(index + 1 < args.len(), format!("missing value for {name}"));
    PathBuf::from(&args[index + 1])
}

fn read_array<const N: usize, R: Read>(input: &mut R) -> [u8; N] {
    let mut value = [0u8; N];
    input.read_exact(&mut value).unwrap_or_else(|error| fail(error.to_string()));
    value
}

fn read_u16<R: Read>(input: &mut R) -> u16 {
    u16::from_le_bytes(read_array(input))
}

fn read_u64<R: Read>(input: &mut R) -> u64 {
    u64::from_le_bytes(read_array(input))
}

fn read_mono<R: Read>(input: &mut R, expected_degree: u8) -> [u8; 12] {
    let degree = read_array::<1, _>(input)[0];
    let ids = read_array::<12, _>(input);
    require(degree == expected_degree, "unexpected monomial degree");
    ids
}

fn trailing_eof<R: Read>(input: &mut R) {
    let mut trailing = [0u8; 1];
    require(input.read(&mut trailing).unwrap_or_else(|error| fail(error.to_string())) == 0,
            "trailing bytes");
}

fn sha256(path: &Path) -> String {
    let output = Command::new("/usr/bin/shasum").arg("-a").arg("256").arg(path)
        .output().unwrap_or_else(|error| fail(error.to_string()));
    require(output.status.success(), "shasum failed");
    let text = String::from_utf8(output.stdout).unwrap_or_else(|error| fail(error.to_string()));
    let digest = text.split_whitespace().next().unwrap_or_else(|| fail("empty shasum"));
    require(digest.len() == 64 && digest.bytes().all(|byte| byte.is_ascii_hexdigit()),
            "invalid shasum output");
    digest.to_ascii_lowercase()
}

fn decode_sha256(value: &str) -> [u8; 32] {
    require(value.len() == 64, "bad SHA-256 length");
    let mut answer = [0u8; 32];
    for (index, slot) in answer.iter_mut().enumerate() {
        *slot = u8::from_str_radix(&value[2 * index..2 * index + 2], 16)
            .unwrap_or_else(|_| fail("bad SHA-256 hex"));
    }
    answer
}

fn check_time(started: Instant) {
    require(started.elapsed().as_secs_f64() < 170.0, "export stop-scheduling wall gate");
}

fn peak_rss_bytes() -> i64 {
    let mut usage = Rusage {
        user: Timeval { seconds: 0, micros: 0, padding: 0 },
        system: Timeval { seconds: 0, micros: 0, padding: 0 },
        max_rss: 0,
        remainder: [0; 13],
    };
    let status = unsafe { getrusage(0, &mut usage) };
    require(status == 0, "getrusage failed");
    usage.max_rss
}

fn parse_vectors_pass1(path: &Path) -> (u64, Vec<Column>, Vec<u32>, Vec<[u8; 12]>, u64) {
    let mut input = BufReader::with_capacity(8 << 20,
        File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    require(&read_array::<12, _>(&mut input) == VECTOR_MAGIC, "vector magic");
    require(read_u64(&mut input) == PRIME, "vector prime");
    require(read_u64(&mut input) == PROVIDER_FINGERPRINT, "provider fingerprint");
    let vector_fingerprint = read_u64(&mut input);
    require(read_u64(&mut input) == RECORDS as u64, "vector record count");

    let mut columns = Vec::with_capacity(RECORDS);
    let mut pointers = Vec::with_capacity(RECORDS + 1);
    let mut rows = Vec::<[u8; 12]>::with_capacity(24_000_000);
    pointers.push(0);
    let mut previous_column = None;
    for _ in 0..RECORDS {
        let column = Column { word: read_u16(&mut input), multiplier: read_mono(&mut input, 8) };
        require(column.word < 6561, "column word out of range");
        require(previous_column.is_none_or(|old| old < column), "columns not strict");
        previous_column = Some(column);
        columns.push(column);
        let size = read_u64(&mut input) as usize;
        require(size > 0 && size <= 700_000, "vector size out of range");
        let mut previous_row = None;
        for _ in 0..size {
            let row = read_mono(&mut input, 12);
            require(previous_row.is_none_or(|old| old < row), "vector rows not strict");
            previous_row = Some(row);
            let residue = read_u64(&mut input);
            require(residue > 0 && residue < PRIME, "source residue out of range");
            let centered = if residue <= PRIME / 2 { residue as i64 }
                           else { residue as i64 - PRIME as i64 };
            require(centered.abs() <= MAX_COEFFICIENT,
                    "source residue lacks bounded integral lift");
            rows.push(row);
        }
        require(rows.len() < u32::MAX as usize, "NNZ exceeds u32");
        pointers.push(rows.len() as u32);
    }
    trailing_eof(&mut input);
    (vector_fingerprint, columns, pointers, rows, fs::metadata(path).unwrap().len())
}

fn parse_checkpoint(path: &Path) -> (Vec<Column>, Vec<Candidate>, u64) {
    let mut input = BufReader::with_capacity(4 << 20,
        File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    require(&read_array::<12, _>(&mut input) == CHECKPOINT_MAGIC, "checkpoint magic");
    require(read_u64(&mut input) == PRIME, "checkpoint prime");
    require(read_u64(&mut input) == ROUND, "checkpoint round");
    require(read_u64(&mut input) == RECORDS as u64, "checkpoint column count");
    require(read_u64(&mut input) == CANDIDATE_SUPPORT as u64, "candidate support");
    let mut columns = Vec::with_capacity(RECORDS);
    let mut previous = None;
    for _ in 0..RECORDS {
        let column = Column { word: read_u16(&mut input), multiplier: read_mono(&mut input, 8) };
        require(previous.is_none_or(|old| old < column), "checkpoint columns not strict");
        previous = Some(column);
        columns.push(column);
    }
    let mut candidate = Vec::with_capacity(CANDIDATE_SUPPORT);
    let mut seen = HashSet::with_capacity(CANDIDATE_SUPPORT);
    let mut previous_row = None;
    for _ in 0..CANDIDATE_SUPPORT {
        let row = read_mono(&mut input, 12);
        require(previous_row.is_none_or(|old| old < row), "candidate rows not strict");
        previous_row = Some(row);
        require(seen.insert(row), "duplicate candidate row");
        let value = read_u64(&mut input);
        require(value > 0 && value < PRIME, "candidate value out of range");
        candidate.push(Candidate { row, value: value as u32, dense: None });
    }
    trailing_eof(&mut input);
    (columns, candidate, fs::metadata(path).unwrap().len())
}

fn parse_vectors_pass2(path: &Path, columns: &[Column], dense: &HashMap<[u8; 12], u32>,
                       expected_pointers: &[u32]) -> (Vec<u32>, Vec<i32>, Vec<u32>) {
    let mut input = BufReader::with_capacity(8 << 20,
        File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    require(&read_array::<12, _>(&mut input) == VECTOR_MAGIC, "vector magic pass2");
    require(read_u64(&mut input) == PRIME, "vector prime pass2");
    require(read_u64(&mut input) == PROVIDER_FINGERPRINT, "provider pass2");
    let _fingerprint = read_u64(&mut input);
    require(read_u64(&mut input) == RECORDS as u64, "records pass2");
    let nnz = *expected_pointers.last().unwrap() as usize;
    let mut row_indices = Vec::with_capacity(nnz);
    let mut values = Vec::with_capacity(nnz);
    let mut row_counts = vec![0u32; dense.len()];
    for (column_index, expected_column) in columns.iter().enumerate() {
        let column = Column { word: read_u16(&mut input), multiplier: read_mono(&mut input, 8) };
        require(&column == expected_column, "pass2 column changed");
        let size = read_u64(&mut input) as usize;
        require(expected_pointers[column_index + 1] as usize
                    - expected_pointers[column_index] as usize == size, "pass2 size changed");
        let mut previous_dense = None;
        for _ in 0..size {
            let row = read_mono(&mut input, 12);
            let row_index = *dense.get(&row).unwrap_or_else(|| fail("missing dense row"));
            require(previous_dense.is_none_or(|old| old < row_index), "CSC rows not strict");
            previous_dense = Some(row_index);
            let residue = read_u64(&mut input);
            require(residue > 0 && residue < PRIME, "pass2 residue");
            let centered = if residue <= PRIME / 2 { residue as i64 }
                           else { residue as i64 - PRIME as i64 };
            require(centered != 0 && centered.abs() <= MAX_COEFFICIENT, "pass2 lift");
            row_indices.push(row_index);
            values.push(centered as i32);
            row_counts[row_index as usize] = row_counts[row_index as usize]
                .checked_add(1).unwrap_or_else(|| fail("row count overflow"));
        }
    }
    trailing_eof(&mut input);
    require(row_indices.len() == nnz && values.len() == nnz, "pass2 NNZ");
    (row_indices, values, row_counts)
}

fn write_u32s<W: Write>(output: &mut W, values: &[u32]) {
    let bytes = unsafe {
        std::slice::from_raw_parts(values.as_ptr() as *const u8, values.len() * 4)
    };
    output.write_all(bytes).unwrap_or_else(|error| fail(error.to_string()));
}

fn write_i32s<W: Write>(output: &mut W, values: &[i32]) {
    let bytes = unsafe {
        std::slice::from_raw_parts(values.as_ptr() as *const u8, values.len() * 4)
    };
    output.write_all(bytes).unwrap_or_else(|error| fail(error.to_string()));
}

fn put_u32(header: &mut [u8], offset: usize, value: u32) {
    header[offset..offset + 4].copy_from_slice(&value.to_le_bytes());
}

fn put_u64(header: &mut [u8], offset: usize, value: u64) {
    header[offset..offset + 8].copy_from_slice(&value.to_le_bytes());
}

fn json_path(path: &Path) -> String {
    path.display().to_string().replace('\\', "\\\\").replace('"', "\\\"")
}

fn main() {
    require(cfg!(target_endian = "little"), "little-endian build required");
    let source = argument("--vectors");
    let checkpoint = argument("--checkpoint");
    let output_path = argument("--output");
    let ledger_path = argument("--ledger");
    let started = Instant::now();

    let hash_started = Instant::now();
    let source_sha = sha256(&source);
    let checkpoint_sha = sha256(&checkpoint);
    require(source_sha == SOURCE_SHA256, "unfrozen vector cache SHA-256");
    require(checkpoint_sha == CHECKPOINT_SHA256, "unfrozen checkpoint SHA-256");
    let hash_seconds = hash_started.elapsed().as_secs_f64();
    check_time(started);

    let pass1_started = Instant::now();
    let (vector_fingerprint, columns, csc_pointers, mut row_keys, source_bytes) =
        parse_vectors_pass1(&source);
    let (checkpoint_columns, mut candidate, checkpoint_bytes) = parse_checkpoint(&checkpoint);
    require(columns == checkpoint_columns, "checkpoint/vector column sets differ");
    let nnz = row_keys.len();
    row_keys.sort_unstable();
    row_keys.dedup();
    require(row_keys.len() < u32::MAX as usize, "coordinate count exceeds u32");
    let pass1_seconds = pass1_started.elapsed().as_secs_f64();
    check_time(started);

    let map_started = Instant::now();
    let mut dense = HashMap::with_capacity(row_keys.len());
    for (index, row) in row_keys.iter().copied().enumerate() {
        require(dense.insert(row, index as u32).is_none(), "duplicate dense row");
    }
    for record in &mut candidate {
        record.dense = dense.get(&record.row).copied();
    }
    let candidate_present = candidate.iter().filter(|item| item.dense.is_some()).count();
    let (csc_rows, csc_values, row_counts) =
        parse_vectors_pass2(&source, &columns, &dense, &csc_pointers);
    drop(dense);
    let map_pass2_seconds = map_started.elapsed().as_secs_f64();
    check_time(started);

    let csr_started = Instant::now();
    let mut csr_pointers = Vec::with_capacity(row_counts.len() + 1);
    csr_pointers.push(0u32);
    for count in row_counts {
        let next = csr_pointers.last().copied().unwrap().checked_add(count)
            .unwrap_or_else(|| fail("CSR pointer overflow"));
        csr_pointers.push(next);
    }
    require(csr_pointers.last().copied() == Some(nnz as u32), "CSR NNZ mismatch");
    let mut positions = csr_pointers[..row_keys.len()].to_vec();
    let mut csr_columns = vec![0u32; nnz];
    let mut csr_values = vec![0i32; nnz];
    for column in 0..columns.len() {
        for edge in csc_pointers[column] as usize..csc_pointers[column + 1] as usize {
            let row = csc_rows[edge] as usize;
            let position = positions[row] as usize;
            require(position < csr_pointers[row + 1] as usize, "CSR scatter overflow");
            csr_columns[position] = column as u32;
            csr_values[position] = csc_values[edge];
            positions[row] += 1;
        }
    }
    for row in 0..row_keys.len() {
        require(positions[row] == csr_pointers[row + 1], "CSR scatter incomplete");
        let range = csr_pointers[row] as usize..csr_pointers[row + 1] as usize;
        require(csr_columns[range].windows(2).all(|pair| pair[0] < pair[1]),
                "CSR columns not strict");
    }
    drop(positions);
    let csr_seconds = csr_started.elapsed().as_secs_f64();
    check_time(started);

    let write_started = Instant::now();
    let csc_pointer_offset = HEADER_BYTES as u64;
    let csc_rows_offset = csc_pointer_offset + (csc_pointers.len() * 4) as u64;
    let csc_values_offset = csc_rows_offset + (csc_rows.len() * 4) as u64;
    let csr_pointer_offset = csc_values_offset + (csc_values.len() * 4) as u64;
    let csr_columns_offset = csr_pointer_offset + (csr_pointers.len() * 4) as u64;
    let csr_values_offset = csr_columns_offset + (csr_columns.len() * 4) as u64;
    let candidate_offset = csr_values_offset + (csr_values.len() * 4) as u64;
    let file_bytes = candidate_offset + (candidate.len() * 24) as u64;
    let mut header = vec![0u8; HEADER_BYTES];
    header[..16].copy_from_slice(OUTPUT_MAGIC);
    put_u32(&mut header, 16, 1);
    put_u32(&mut header, 20, PRIME as u32);
    put_u64(&mut header, 24, row_keys.len() as u64);
    put_u64(&mut header, 32, columns.len() as u64);
    put_u64(&mut header, 40, nnz as u64);
    put_u64(&mut header, 48, candidate.len() as u64);
    put_u64(&mut header, 56, candidate_present as u64);
    put_u64(&mut header, 64, source_bytes);
    put_u64(&mut header, 72, checkpoint_bytes);
    put_u64(&mut header, 80, PROVIDER_FINGERPRINT);
    put_u64(&mut header, 88, vector_fingerprint);
    put_u64(&mut header, 96, ROUND);
    header[104..136].copy_from_slice(&decode_sha256(&source_sha));
    header[136..168].copy_from_slice(&decode_sha256(&checkpoint_sha));
    put_u64(&mut header, 168, HEADER_BYTES as u64);
    put_u64(&mut header, 176, csc_pointer_offset);
    put_u64(&mut header, 184, csc_rows_offset);
    put_u64(&mut header, 192, csc_values_offset);
    put_u64(&mut header, 200, csr_pointer_offset);
    put_u64(&mut header, 208, csr_columns_offset);
    put_u64(&mut header, 216, csr_values_offset);
    put_u64(&mut header, 224, candidate_offset);
    put_u64(&mut header, 232, file_bytes);

    let temporary = output_path.with_extension("bin.tmp");
    let mut output = BufWriter::with_capacity(16 << 20,
        File::create(&temporary).unwrap_or_else(|error| fail(error.to_string())));
    output.write_all(&header).unwrap();
    write_u32s(&mut output, &csc_pointers);
    write_u32s(&mut output, &csc_rows);
    write_i32s(&mut output, &csc_values);
    write_u32s(&mut output, &csr_pointers);
    write_u32s(&mut output, &csr_columns);
    write_i32s(&mut output, &csr_values);
    for record in &candidate {
        output.write_all(&record.dense.unwrap_or(u32::MAX).to_le_bytes()).unwrap();
        output.write_all(&record.value.to_le_bytes()).unwrap();
        output.write_all(&[12]).unwrap();
        output.write_all(&record.row).unwrap();
        output.write_all(&[0u8; 3]).unwrap();
    }
    output.flush().unwrap_or_else(|error| fail(error.to_string()));
    drop(output);
    require(fs::metadata(&temporary).unwrap().len() == file_bytes, "matrix byte length");
    fs::rename(&temporary, &output_path).unwrap_or_else(|error| fail(error.to_string()));
    let output_sha = sha256(&output_path);
    let write_hash_seconds = write_started.elapsed().as_secs_f64();
    let total_seconds = started.elapsed().as_secs_f64();
    let peak = peak_rss_bytes();
    require(total_seconds < 180.0, "export exceeded wall gate");
    require(peak < 6 * 1024 * 1024 * 1024i64, "export exceeded RSS gate");

    let ledger = format!(
        concat!(
        "{{\n  \"status\": \"PASS_EXACT_ROUND635_CSR_CSC_EXPORT\",\n",
        "  \"schema\": \"KRENN_AFFINE251_D12_ROUND635_CSR_CSC_V1\",\n",
        "  \"vectors\": {{\"path\":\"{}\",\"sha256\":\"{}\",\"bytes\":{}}},\n",
        "  \"checkpoint\": {{\"path\":\"{}\",\"sha256\":\"{}\",\"bytes\":{},\"round\":{}}},\n",
        "  \"matrix\": {{\"path\":\"{}\",\"sha256\":\"{}\",\"bytes\":{},\"rows\":{},\"columns\":{},\"nnz\":{}}},\n",
        "  \"candidate_support\": {},\n  \"candidate_dense_present\": {},\n",
        "  \"coefficient_type\": \"centered-i32-le exact lift bounded by 1440\",\n",
        "  \"index_type\": \"u32-le\",\n",
        "  \"layout\": \"A CSC followed by A CSR and exact checkpoint candidate provenance\",\n",
        "  \"timings_seconds\": {{\"source_hash\":{:.6},\"pass1_parse_sort\":{:.6},\"dense_map_pass2\":{:.6},\"csr_transpose\":{:.6},\"write_and_output_hash\":{:.6},\"total_export_build\":{:.6}}},\n",
        "  \"peak_rss_bytes\": {},\n",
        "  \"scope\": \"Exact round-635 resident operator interface only; no closure, rank, Krylov, or membership run.\"\n}}\n"),
        json_path(&source), source_sha, source_bytes,
        json_path(&checkpoint), checkpoint_sha, checkpoint_bytes, ROUND,
        json_path(&output_path), output_sha, file_bytes, row_keys.len(), columns.len(), nnz,
        candidate.len(), candidate_present,
        hash_seconds, pass1_seconds, map_pass2_seconds, csr_seconds, write_hash_seconds,
        total_seconds, peak);
    let ledger_temporary = ledger_path.with_extension("json.tmp");
    fs::write(&ledger_temporary, ledger).unwrap_or_else(|error| fail(error.to_string()));
    fs::rename(ledger_temporary, ledger_path).unwrap_or_else(|error| fail(error.to_string()));
    println!("PASS rows={} columns={} nnz={} candidate_present={} seconds={:.3} rss={}",
             row_keys.len(), columns.len(), nnz, candidate_present, total_seconds, peak);
}
