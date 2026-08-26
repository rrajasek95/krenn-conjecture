//! Sparse modular Markowitz elimination for the exact closed K0--K9 component.

use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap, HashSet};
use std::env;
use std::fs::{self, File};
use std::hash::{BuildHasherDefault, Hash, Hasher};
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::path::Path;
use std::time::Instant;

const ROWS: usize = 1_012_256;
const COLUMNS: usize = 837_883;
const EDGES: u64 = 8_342_855;

#[derive(Default)]
struct IdentityHasher(u64);
impl Hasher for IdentityHasher {
    fn finish(&self) -> u64 { self.0 }
    fn write(&mut self, bytes: &[u8]) {
        let mut value = 0u64;
        for (shift, byte) in bytes.iter().take(8).enumerate() { value |= (*byte as u64) << (8 * shift); }
        self.0 = value;
    }
    fn write_u32(&mut self, value: u32) { self.0 = value as u64; }
}
type U32Map<V> = HashMap<u32, V, BuildHasherDefault<IdentityHasher>>;
type U32Set = HashSet<u32, BuildHasherDefault<IdentityHasher>>;

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct RowKey { degree: u8, row: [u8; 12] }

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("closed-markowitz: {}", message.as_ref());
    std::process::exit(2)
}

fn nibble(byte: u8) -> u8 {
    match byte {
        b'0'..=b'9' => byte - b'0', b'a'..=b'f' => byte - b'a' + 10,
        b'A'..=b'F' => byte - b'A' + 10, _ => fail("bad hex digit"),
    }
}

fn row_key(degree: u8, text: &str) -> RowKey {
    if text.len() != 24 { fail("bad row hex length") }
    let mut row = [0u8; 12];
    for index in 0..12 {
        row[index] = 16 * nibble(text.as_bytes()[2 * index]) + nibble(text.as_bytes()[2 * index + 1]);
    }
    RowKey { degree, row }
}

fn modp(value: i64, prime: i64) -> i64 {
    let value = value % prime;
    if value < 0 { value + prime } else { value }
}

fn inverse(value: i64, prime: i64) -> i64 {
    let (mut base, mut exponent, mut answer) = (modp(value, prime), prime - 2, 1i64);
    if base == 0 { fail("zero pivot coefficient") }
    while exponent != 0 {
        if exponent & 1 != 0 { answer = answer * base % prime; }
        base = base * base % prime;
        exponent >>= 1;
    }
    answer
}

struct Matrix {
    row_keys: Vec<RowKey>,
    rows: Vec<U32Set>,
    columns: Vec<U32Map<i64>>,
    rhs: Vec<i64>,
    active_rows: Vec<bool>,
    active_columns: Vec<bool>,
    row_heap: BinaryHeap<Reverse<(usize, u32)>>,
    column_heap: BinaryHeap<Reverse<(usize, u32)>>,
    nnz: u64,
}

struct PivotRecord {
    row: u32,
    normalized_tail: Vec<(u32, i64)>,
}

fn load(edges_path: &Path, target_path: &Path, prime: i64) -> Matrix {
    let mut row_index = HashMap::<RowKey, u32>::new();
    let mut row_keys = Vec::with_capacity(ROWS);
    let mut rows: Vec<U32Set> = Vec::with_capacity(ROWS);
    let mut columns: Vec<U32Map<i64>> = (0..COLUMNS).map(|_| U32Map::default()).collect();
    let mut nnz = 0u64;
    for (number, line) in BufReader::new(File::open(edges_path).unwrap_or_else(|error| fail(error.to_string()))).lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        if number == 0 {
            if line != "column_index\tdegree\trow\tmultiplicity" { fail("edge header changed") }
            continue;
        }
        let fields: Vec<_> = line.split('\t').collect();
        if fields.len() != 4 { fail("edge schema changed") }
        let column: u32 = fields[0].parse().unwrap_or_else(|_| fail("bad edge column"));
        let degree: u8 = fields[1].parse().unwrap_or_else(|_| fail("bad edge degree"));
        let value: i64 = fields[3].parse().unwrap_or_else(|_| fail("bad edge value"));
        if column as usize >= COLUMNS || degree > 9 || value <= 0 || value >= prime { fail("bad edge record") }
        let key = row_key(degree, fields[2]);
        let row = *row_index.entry(key).or_insert_with(|| {
            let index = row_keys.len() as u32;
            row_keys.push(key);
            rows.push(U32Set::default());
            index
        });
        if columns[column as usize].insert(row, value).is_some() || !rows[row as usize].insert(column) {
            fail("duplicate matrix edge")
        }
        nnz += 1;
    }
    if row_keys.len() != ROWS || nnz != EDGES || columns.iter().any(U32Map::is_empty) {
        fail("matrix census changed")
    }
    let mut rhs = vec![0i64; ROWS];
    let mut targets = 0usize;
    for (number, line) in BufReader::new(File::open(target_path).unwrap_or_else(|error| fail(error.to_string()))).lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        if number == 0 {
            if line != "degree\trow\tcoefficient" { fail("target header changed") }
            continue;
        }
        let fields: Vec<_> = line.split('\t').collect();
        if fields.len() != 3 || fields[0] != "9" { continue; }
        let key = row_key(9, fields[1]);
        let row = *row_index.get(&key).unwrap_or_else(|| fail("target row outside closed component"));
        let value: i128 = fields[2].parse().unwrap_or_else(|_| fail("bad target coefficient"));
        rhs[row as usize] = ((value % prime as i128 + prime as i128) % prime as i128) as i64;
        targets += 1;
    }
    if targets != 49_988 { fail("target census changed") }
    let mut row_heap = BinaryHeap::new();
    for (row, entries) in rows.iter().enumerate() { row_heap.push(Reverse((entries.len(), row as u32))); }
    let mut column_heap = BinaryHeap::new();
    for (column, entries) in columns.iter().enumerate() { column_heap.push(Reverse((entries.len(), column as u32))); }
    Matrix {
        row_keys, rows, columns, rhs, active_rows: vec![true; ROWS], active_columns: vec![true; COLUMNS],
        row_heap, column_heap, nnz,
    }
}

fn valid_row_min(matrix: &mut Matrix) -> Option<(usize, u32)> {
    loop {
        let Reverse((degree, row)) = *matrix.row_heap.peek()?;
        if !matrix.active_rows[row as usize] || matrix.rows[row as usize].len() != degree {
            matrix.row_heap.pop();
        } else { return Some((degree, row)); }
    }
}

fn valid_column_min(matrix: &mut Matrix) -> Option<(usize, u32)> {
    loop {
        let Reverse((degree, column)) = *matrix.column_heap.peek()?;
        if !matrix.active_columns[column as usize] || matrix.columns[column as usize].len() != degree {
            matrix.column_heap.pop();
        } else { return Some((degree, column)); }
    }
}

fn choose_pivot(matrix: &mut Matrix) -> Option<(u32, u32, usize)> {
    loop {
        while let Some((0, row)) = valid_row_min(matrix) {
            matrix.row_heap.pop();
            if matrix.rhs[row as usize] != 0 { return Some((row, u32::MAX, usize::MAX)); }
            matrix.active_rows[row as usize] = false;
        }
        while let Some((0, column)) = valid_column_min(matrix) {
            matrix.column_heap.pop();
            matrix.active_columns[column as usize] = false;
        }
        let (row_degree, row) = valid_row_min(matrix)?;
        let (column_degree, column) = valid_column_min(matrix)?;
        let row_column = *matrix.rows[row as usize].iter()
            .min_by_key(|&&candidate| matrix.columns[candidate as usize].len()).unwrap();
        let column_row = *matrix.columns[column as usize].keys()
            .min_by_key(|&&candidate| matrix.rows[candidate as usize].len()).unwrap();
        let row_cost = (row_degree - 1) * (matrix.columns[row_column as usize].len() - 1);
        let column_cost = (column_degree - 1) * (matrix.rows[column_row as usize].len() - 1);
        return if row_cost <= column_cost { Some((row, row_column, row_cost)) }
            else { Some((column_row, column, column_cost)) };
    }
}

fn eliminate(matrix: &mut Matrix, row: u32, column: u32, prime: i64) -> (u64, u64, PivotRecord) {
    let pivot_entries: Vec<_> = matrix.columns[column as usize].iter().map(|(&r, &v)| (r, v)).collect();
    let pivot_value = *matrix.columns[column as usize].get(&row).unwrap_or_else(|| fail("missing pivot edge"));
    let pivot_inverse = inverse(pivot_value, prime);
    let normalized_tail = pivot_entries.iter().filter_map(|&(affected, entry)| {
        (affected != row).then_some((affected, entry * pivot_inverse % prime))
    }).collect();
    let target_value = matrix.rhs[row as usize] * pivot_inverse % prime;
    if target_value != 0 {
        for &(affected, entry) in &pivot_entries {
            matrix.rhs[affected as usize] = modp(matrix.rhs[affected as usize] - target_value * entry, prime);
        }
    }
    let other_columns: Vec<_> = matrix.rows[row as usize].iter().copied().filter(|&candidate| candidate != column).collect();
    let mut inserted = 0u64;
    let mut removed = 0u64;
    for affected_column in other_columns {
        let entry = matrix.columns[affected_column as usize][&row];
        let factor = entry * pivot_inverse % prime;
        for &(affected_row, pivot_entry) in &pivot_entries {
            if affected_row == row { continue; }
            let old = matrix.columns[affected_column as usize].get(&affected_row).copied().unwrap_or(0);
            let new = modp(old - factor * pivot_entry, prime);
            if old == 0 && new != 0 {
                matrix.columns[affected_column as usize].insert(affected_row, new);
                matrix.rows[affected_row as usize].insert(affected_column);
                matrix.nnz += 1;
                inserted += 1;
                matrix.row_heap.push(Reverse((matrix.rows[affected_row as usize].len(), affected_row)));
            } else if old != 0 && new == 0 {
                matrix.columns[affected_column as usize].remove(&affected_row);
                matrix.rows[affected_row as usize].remove(&affected_column);
                matrix.nnz -= 1;
                removed += 1;
                matrix.row_heap.push(Reverse((matrix.rows[affected_row as usize].len(), affected_row)));
            } else if new != 0 {
                matrix.columns[affected_column as usize].insert(affected_row, new);
            }
        }
        if matrix.columns[affected_column as usize].remove(&row).is_none()
            || !matrix.rows[row as usize].remove(&affected_column) { fail("failed to remove pivot row edge") }
        matrix.nnz -= 1;
        removed += 1;
        matrix.column_heap.push(Reverse((matrix.columns[affected_column as usize].len(), affected_column)));
    }
    for &(affected_row, _) in &pivot_entries {
        if matrix.rows[affected_row as usize].remove(&column) {
            matrix.nnz -= 1;
            removed += 1;
            matrix.row_heap.push(Reverse((matrix.rows[affected_row as usize].len(), affected_row)));
        }
    }
    matrix.columns[column as usize].clear();
    matrix.rows[row as usize].clear();
    matrix.active_columns[column as usize] = false;
    matrix.active_rows[row as usize] = false;
    matrix.rhs[row as usize] = 0;
    (inserted, removed, PivotRecord { row, normalized_tail })
}

fn hex(row: &[u8; 12]) -> String {
    const DIGITS: &[u8; 16] = b"0123456789abcdef";
    let mut out = String::with_capacity(24);
    for byte in row {
        out.push(DIGITS[(byte >> 4) as usize] as char);
        out.push(DIGITS[(byte & 15) as usize] as char);
    }
    out
}

fn reconstruct_and_verify_dual(
    matrix: &Matrix,
    pivots: &[PivotRecord],
    contradiction_row: u32,
    edges_path: &Path,
    target_path: &Path,
    prime: i64,
    output_path: &Path,
) -> (usize, i64) {
    let mut dual = U32Map::<i64>::default();
    dual.insert(contradiction_row, 1);
    for record in pivots.iter().rev() {
        let pairing = record.normalized_tail.iter().map(|(row, value)| {
            *value * dual.get(row).copied().unwrap_or(0)
        }).sum::<i64>();
        let value = modp(-pairing, prime);
        if value != 0 { dual.insert(record.row, value); }
    }
    let mut key_dual = HashMap::with_capacity(dual.len());
    for (&row, &value) in &dual { key_dual.insert(matrix.row_keys[row as usize], value); }
    let mut column_pairing = vec![0i64; COLUMNS];
    for (number, line) in BufReader::new(File::open(edges_path).unwrap_or_else(|error| fail(error.to_string()))).lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        if number == 0 { continue; }
        let fields: Vec<_> = line.split('\t').collect();
        let column: usize = fields[0].parse().unwrap_or_else(|_| fail("bad verification column"));
        let degree: u8 = fields[1].parse().unwrap_or_else(|_| fail("bad verification degree"));
        let entry: i64 = fields[3].parse().unwrap_or_else(|_| fail("bad verification entry"));
        if let Some(&value) = key_dual.get(&row_key(degree, fields[2])) {
            column_pairing[column] = modp(column_pairing[column] + value * entry, prime);
        }
    }
    if column_pairing.iter().any(|value| *value != 0) { fail("reconstructed dual does not annihilate original matrix") }
    let mut target_pairing = 0i64;
    for (number, line) in BufReader::new(File::open(target_path).unwrap_or_else(|error| fail(error.to_string()))).lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        if number == 0 { continue; }
        let fields: Vec<_> = line.split('\t').collect();
        if fields[0] != "9" { continue; }
        let value: i128 = fields[2].parse().unwrap_or_else(|_| fail("bad verification target"));
        let coefficient = ((value % prime as i128 + prime as i128) % prime as i128) as i64;
        if let Some(&dual_value) = key_dual.get(&row_key(9, fields[1])) {
            target_pairing = modp(target_pairing + dual_value * coefficient, prime);
        }
    }
    if target_pairing == 0 { fail("reconstructed dual has zero target pairing") }
    let mut ordered: Vec<_> = dual.into_iter().collect();
    ordered.sort_by_key(|(row, _)| matrix.row_keys[*row as usize]);
    let tmp = output_path.with_extension("tsv.tmp");
    let mut out = BufWriter::new(File::create(&tmp).unwrap_or_else(|error| fail(error.to_string())));
    writeln!(out, "degree\trow\tvalue").unwrap();
    for (row, value) in &ordered {
        let key = matrix.row_keys[*row as usize];
        writeln!(out, "{}\t{}\t{value}", key.degree, hex(&key.row)).unwrap();
    }
    out.flush().unwrap();
    drop(out);
    fs::rename(tmp, output_path).unwrap_or_else(|error| fail(error.to_string()));
    (ordered.len(), target_pairing)
}

fn main() {
    let args: Vec<_> = env::args().collect();
    if args.len() != 8 {
        fail("usage: solve_closed_component_markowitz EDGES.tsv TARGET.tsv PRIME MAX_PIVOTS MAX_NNZ RESULTS.json DUAL.tsv")
    }
    let prime: i64 = args[3].parse().unwrap_or_else(|_| fail("bad prime"));
    let max_pivots: usize = args[4].parse().unwrap_or_else(|_| fail("bad pivot cap"));
    let max_nnz: u64 = args[5].parse().unwrap_or_else(|_| fail("bad nnz cap"));
    let begun = Instant::now();
    let mut matrix = load(Path::new(&args[1]), Path::new(&args[2]), prime);
    let load_seconds = begun.elapsed().as_secs_f64();
    let mut pivots = 0usize;
    let mut zero_cost = 0usize;
    let mut total_inserted = 0u64;
    let mut total_removed = 0u64;
    let mut maximum_cost = 0usize;
    let mut status = "PIVOT_CAP_REACHED";
    let mut pivot_records = Vec::new();
    let mut contradiction_row = None;
    while pivots < max_pivots {
        let Some((row, column, cost)) = choose_pivot(&mut matrix) else {
            status = "PASS_MATRIX_EXHAUSTED";
            break;
        };
        if column == u32::MAX {
            status = "PROVED_NO_SOLUTION_MOD_PRIME";
            contradiction_row = Some(row);
            break;
        }
        let (inserted, removed, record) = eliminate(&mut matrix, row, column, prime);
        pivot_records.push(record);
        total_inserted += inserted;
        total_removed += removed;
        pivots += 1;
        if cost == 0 { zero_cost += 1; }
        maximum_cost = maximum_cost.max(cost);
        if matrix.nnz > max_nnz {
            status = "NNZ_CAP_REACHED";
            break;
        }
        if pivots % 10_000 == 0 {
            eprintln!("pivots={pivots} nnz={} cost={cost} inserted={total_inserted} removed={total_removed} elapsed={:.1}s",
                matrix.nnz, begun.elapsed().as_secs_f64());
        }
    }
    let active_rows = matrix.active_rows.iter().filter(|&&value| value).count();
    let active_columns = matrix.active_columns.iter().filter(|&&value| value).count();
    let residual_nonzero = matrix.rhs.iter().enumerate().filter(|(row, value)| matrix.active_rows[*row] && **value != 0).count();
    let (dual_support, dual_target_pairing) = if let Some(row) = contradiction_row {
        reconstruct_and_verify_dual(
            &matrix, &pivot_records, row, Path::new(&args[1]), Path::new(&args[2]), prime, Path::new(&args[7]),
        )
    } else { (0, 0) };
    let text = format!(
        "{{\n  \"status\":\"{status}\",\n  \"prime\":{prime},\n  \"rows\":{ROWS},\n  \"columns\":{COLUMNS},\n  \"initial_weighted_edges\":{EDGES},\n  \"pivots\":{pivots},\n  \"zero_cost_pivots\":{zero_cost},\n  \"maximum_markowitz_cost\":{maximum_cost},\n  \"inserted_edges\":{total_inserted},\n  \"removed_edges\":{total_removed},\n  \"active_rows\":{active_rows},\n  \"active_columns\":{active_columns},\n  \"active_weighted_edges\":{},\n  \"active_residual_nonzero_rows\":{residual_nonzero},\n  \"dual_support\":{dual_support},\n  \"dual_target_pairing\":{dual_target_pairing},\n  \"load_seconds\":{load_seconds:.6},\n  \"elapsed_seconds\":{:.6},\n  \"scope\":\"modular discovery on exact closed component; positive/negative requires independently replayable exact certificate\"\n}}\n",
        matrix.nnz, begun.elapsed().as_secs_f64());
    let output = Path::new(&args[6]);
    let tmp = output.with_extension("json.tmp");
    fs::write(&tmp, text).unwrap_or_else(|error| fail(error.to_string()));
    fs::rename(tmp, output).unwrap_or_else(|error| fail(error.to_string()));
    eprintln!("{status} pivots={pivots} nnz={} elapsed={:.1}s", matrix.nnz, begun.elapsed().as_secs_f64());
}
