//! Dependency-free sparse modular common-echelon solver for anchor-K JSONL.
//!
//! This is a discovery accelerator.  Its solution is an index/coefficient
//! ledger which must be replayed against labelled source columns over Q.

use std::collections::BTreeMap;
use std::collections::BTreeSet;
use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;
use std::sync::atomic::{AtomicI64, Ordering};
use std::time::Instant;

static MODULUS: AtomicI64 = AtomicI64::new(1009);
type Sparse = BTreeMap<usize, i64>;

fn prime() -> i64 { MODULUS.load(Ordering::Relaxed) }

#[derive(Debug)]
struct Header {
    format: String,
    row_count: usize,
    column_count: usize,
    target: Sparse,
}

#[derive(Debug)]
struct Pivot {
    vector: Sparse,
    source_column: usize,
    raw_pivot_coefficient: i64,
    normalization_inverse: i64,
    reductions: Vec<(usize, i64)>,
    insertion_ordinal: usize,
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("anchor-k-echelon: {}", message.as_ref());
    std::process::exit(2);
}

fn modp(value: i64) -> i64 {
    value.rem_euclid(prime())
}

fn inverse(value: i64) -> i64 {
    let (mut old_r, mut r) = (prime(), modp(value));
    let (mut old_s, mut s) = (0_i64, 1_i64);
    while r != 0 {
        let q = old_r / r;
        (old_r, r) = (r, old_r - q * r);
        (old_s, s) = (s, old_s - q * s);
    }
    if old_r != 1 {
        fail(format!("non-unit coefficient {value} modulo {}", prime()));
    }
    modp(old_s)
}

fn add_scaled(left: &mut Sparse, right: &Sparse, scale: i64) {
    if modp(scale) == 0 {
        return;
    }
    for (&index, &value) in right {
        let updated = modp(left.get(&index).copied().unwrap_or(0) + scale * value);
        if updated == 0 {
            left.remove(&index);
        } else {
            left.insert(index, updated);
        }
    }
}

fn scale(vector: &mut Sparse, factor: i64) {
    for value in vector.values_mut() {
        *value = modp(*value * factor);
    }
    vector.retain(|_, value| *value != 0);
}

fn key_start(line: &str, key: &str) -> usize {
    let needle = format!("\"{key}\"");
    let key_pos = line.find(&needle).unwrap_or_else(|| fail(format!("missing JSON key {key}")));
    let tail = &line[key_pos + needle.len()..];
    let colon = tail.find(':').unwrap_or_else(|| fail(format!("missing colon after {key}")));
    key_pos + needle.len() + colon + 1
}

fn integer_value(line: &str, key: &str) -> i64 {
    let start = key_start(line, key);
    let tail = line[start..].trim_start();
    let end = tail.find(|c: char| !(c == '-' || c.is_ascii_digit())).unwrap_or(tail.len());
    tail[..end].parse().unwrap_or_else(|_| fail(format!("bad integer at {key}")))
}

fn string_value(line: &str, key: &str) -> String {
    let start = key_start(line, key);
    let tail = line[start..].trim_start();
    if !tail.starts_with('"') {
        fail(format!("bad string at {key}"));
    }
    let end = tail[1..].find('"').unwrap_or_else(|| fail(format!("unterminated string at {key}")));
    tail[1..1 + end].to_string()
}

fn array_text<'a>(line: &'a str, key: &str) -> &'a str {
    let start = key_start(line, key);
    let relative = line[start..].find('[').unwrap_or_else(|| fail(format!("missing array at {key}")));
    let begin = start + relative;
    let mut depth = 0_i32;
    let mut quoted = false;
    let mut escaped = false;
    for (offset, byte) in line.as_bytes()[begin..].iter().enumerate() {
        if quoted {
            if escaped {
                escaped = false;
            } else if *byte == b'\\' {
                escaped = true;
            } else if *byte == b'"' {
                quoted = false;
            }
            continue;
        }
        match *byte {
            b'"' => quoted = true,
            b'[' => depth += 1,
            b']' => {
                depth -= 1;
                if depth == 0 {
                    return &line[begin..=begin + offset];
                }
            }
            _ => {}
        }
    }
    fail(format!("unterminated array at {key}"));
}

fn integers(text: &str) -> Vec<i64> {
    let bytes = text.as_bytes();
    let mut answer = Vec::new();
    let mut index = 0;
    while index < bytes.len() {
        if bytes[index].is_ascii_digit() || bytes[index] == b'-' {
            let begin = index;
            index += 1;
            while index < bytes.len() && bytes[index].is_ascii_digit() {
                index += 1;
            }
            answer.push(text[begin..index].parse().unwrap_or_else(|_| fail("bad array integer")));
        } else {
            index += 1;
        }
    }
    answer
}

fn parse_pairs(line: &str, key: &str) -> Sparse {
    let flat = integers(array_text(line, key));
    if flat.len() % 2 != 0 {
        fail(format!("{key} does not contain index/value pairs"));
    }
    let mut answer = Sparse::new();
    for pair in flat.chunks_exact(2) {
        if pair[0] < 0 {
            fail(format!("negative row index in {key}"));
        }
        let index = pair[0] as usize;
        let value = modp(pair[1]);
        if value != 0 {
            let updated = modp(answer.get(&index).copied().unwrap_or(0) + value);
            if updated == 0 {
                answer.remove(&index);
            } else {
                answer.insert(index, updated);
            }
        }
    }
    answer
}

fn parse_header(line: &str) -> Header {
    if string_value(line, "type") != "header" {
        fail("first JSONL record is not a header");
    }
    let flat = integers(array_text(line, "target"));
    if flat.len() % 3 != 0 {
        fail("target does not contain index/numerator/denominator triples");
    }
    let mut target = Sparse::new();
    for triple in flat.chunks_exact(3) {
        if triple[0] < 0 {
            fail("negative target row index");
        }
        let coefficient = modp(triple[1] * inverse(triple[2]));
        if coefficient != 0 {
            target.insert(triple[0] as usize, coefficient);
        }
    }
    Header {
        format: string_value(line, "format"),
        row_count: integer_value(line, "row_count") as usize,
        column_count: integer_value(line, "column_count") as usize,
        target,
    }
}

fn validate_rows(vector: &Sparse, row_count: usize, context: &str) {
    if let Some((&index, _)) = vector.last_key_value() {
        if index >= row_count {
            fail(format!("row {index} outside row_count {row_count} in {context}"));
        }
    }
}

fn insert_column(
    mut vector: Sparse,
    source_column: usize,
    basis: &mut BTreeMap<usize, Pivot>,
) -> bool {
    let mut reductions = Vec::new();
    loop {
        let Some((&pivot, &value)) = vector.first_key_value() else {
            return false;
        };
        if let Some(base) = basis.get(&pivot) {
            add_scaled(&mut vector, &base.vector, -value);
            reductions.push((pivot, value));
            continue;
        }
        let inv = inverse(value);
        scale(&mut vector, inv);
        let insertion_ordinal = basis.len();
        basis.insert(pivot, Pivot {
            vector,
            source_column,
            raw_pivot_coefficient: value,
            normalization_inverse: inv,
            reductions,
            insertion_ordinal,
        });
        return true;
    }
}

/// Reduce every coordinate for which the common echelon has a pivot.
/// Crucially, a smaller free coordinate does not stop higher reductions.
fn reduce_target_completely(mut residual: Sparse, basis: &BTreeMap<usize, Pivot>) -> (Sparse, Sparse) {
    let mut pivot_uses = Sparse::new();
    loop {
        let reducible = residual.keys().find(|row| basis.contains_key(row)).copied();
        let Some(pivot) = reducible else { break };
        let value = residual[&pivot];
        let base = &basis[&pivot];
        add_scaled(&mut residual, &base.vector, -value);
        let updated = modp(pivot_uses.get(&pivot).copied().unwrap_or(0) + value);
        if updated == 0 { pivot_uses.remove(&pivot); }
        else { pivot_uses.insert(pivot, updated); }
    }
    (residual, pivot_uses)
}

/// Expand the compact elimination DAG only once, for the final target.
fn expand_solution(pivot_uses: &Sparse, basis: &BTreeMap<usize, Pivot>) -> Sparse {
    let mut coefficients = pivot_uses.clone();
    let mut insertion_order: Vec<_> = basis.iter().map(|(&row, pivot)| {
        (pivot.insertion_ordinal, row)
    }).collect();
    insertion_order.sort_unstable();
    let mut solution = Sparse::new();
    for &(_, pivot_row) in insertion_order.iter().rev() {
        let coefficient = coefficients.remove(&pivot_row).unwrap_or(0);
        if coefficient == 0 { continue; }
        let pivot = &basis[&pivot_row];
        let normalized_coefficient = modp(coefficient * pivot.normalization_inverse);
        let source_updated = modp(solution.get(&pivot.source_column).copied().unwrap_or(0)
                                  + normalized_coefficient);
        if source_updated == 0 { solution.remove(&pivot.source_column); }
        else { solution.insert(pivot.source_column, source_updated); }
        for &(prior_pivot, reduction_value) in &pivot.reductions {
            let updated = modp(coefficients.get(&prior_pivot).copied().unwrap_or(0)
                               - normalized_coefficient * reduction_value);
            if updated == 0 { coefficients.remove(&prior_pivot); }
            else { coefficients.insert(prior_pivot, updated); }
        }
    }
    if !coefficients.is_empty() {
        fail("provenance DAG retained unknown pivots");
    }
    solution
}

fn dot(left: &Sparse, right: &Sparse) -> i64 {
    let (small, large) = if left.len() <= right.len() { (left, right) } else { (right, left) };
    modp(small.iter().map(|(index, value)| {
        *value * large.get(index).copied().unwrap_or(0)
    }).sum())
}

/// Build a left-null functional by solving lambda(V_p)=0 backwards through
/// normalized echelon pivots, with lambda(free_row)=1 and all other free
/// coordinates initially zero.
fn left_dual(basis: &BTreeMap<usize, Pivot>, free_row: usize) -> Sparse {
    if basis.contains_key(&free_row) {
        fail("requested dual seed is a pivot row");
    }
    let mut dual = Sparse::from([(free_row, 1)]);
    for (&pivot_row, record) in basis.iter().rev() {
        let tail_pairing = dot(&record.vector, &dual);
        // record.vector[pivot_row] is normalized to one, while dual has no
        // pivot_row entry yet in this descending recursion.
        if tail_pairing != 0 {
            dual.insert(pivot_row, modp(-tail_pairing));
        }
    }
    for (&pivot_row, record) in basis {
        if dot(&dual, &record.vector) != 0 {
            fail(format!("left-dual recursion failed at pivot {pivot_row}"));
        }
    }
    dual
}

fn write_sparse<W: Write>(out: &mut W, vector: &Sparse) -> io::Result<()> {
    write!(out, "[")?;
    for (number, (&index, &value)) in vector.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "[{index},{value}]")?;
    }
    write!(out, "]")
}

fn build_basis(path: &Path) -> io::Result<(Header, BTreeMap<usize, Pivot>, usize)> {
    let file = File::open(path)?;
    let mut lines = BufReader::new(file).lines();
    let first = lines.next().unwrap_or_else(|| fail("empty basis input"))?;
    let header = parse_header(&first);
    validate_rows(&header.target, header.row_count, "basis target");
    let mut basis = BTreeMap::new();
    let mut read_columns = 0;
    for line_result in lines {
        let line = line_result?;
        if line.trim().is_empty() { continue; }
        if string_value(&line, "type") != "column" {
            fail("non-column record after basis header");
        }
        let source_column = integer_value(&line, "index") as usize;
        if source_column != read_columns {
            fail(format!("non-deterministic basis column order: expected {read_columns}, got {source_column}"));
        }
        let vector = parse_pairs(&line, "entries");
        validate_rows(&vector, header.row_count, "basis column");
        insert_column(vector, source_column, &mut basis);
        read_columns += 1;
    }
    if read_columns != header.column_count {
        fail(format!("basis header says {} columns but read {read_columns}", header.column_count));
    }
    Ok((header, basis, read_columns))
}

fn remap_to_free(residual: &Sparse, free_index: &BTreeMap<usize, usize>) -> Sparse {
    residual.iter().map(|(&row, &value)| {
        let quotient_row = free_index.get(&row).copied()
            .unwrap_or_else(|| fail(format!("projected residual retained pivot row {row}")));
        (quotient_row, value)
    }).collect()
}

fn write_target<W: Write>(out: &mut W, target: &Sparse) -> io::Result<()> {
    write!(out, "[")?;
    for (number, (&index, &value)) in target.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "[{index},{value},1]")?;
    }
    write!(out, "]")
}

/// Project transfer/lower-tail columns through a frozen common echelon and
/// emit a solver-compatible quotient JSONL.  Failure in a restricted transfer
/// file is not a global obstruction unless that file contains all lower tails.
fn project(basis_path: &Path, vectors_path: &Path, output: &Path) -> io::Result<()> {
    let started = Instant::now();
    let (basis_header, basis, _) = build_basis(basis_path)?;
    let free_rows: Vec<_> = (0..basis_header.row_count)
        .filter(|row| !basis.contains_key(row)).collect();
    let free_index: BTreeMap<_, _> = free_rows.iter().enumerate()
        .map(|(index, &row)| (row, index)).collect();

    let file = File::open(vectors_path)?;
    let mut lines = BufReader::new(file).lines();
    let first = lines.next().unwrap_or_else(|| fail("empty vector input"))?;
    let vector_header = parse_header(&first);
    if vector_header.row_count != basis_header.row_count {
        fail("basis/vector row_count mismatch");
    }
    let (target_residual, _) = reduce_target_completely(vector_header.target, &basis);
    let quotient_target = remap_to_free(&target_residual, &free_index);
    let mut out = File::create(output)?;
    write!(out, "{{\"column_count\":{},\"format\":\"anchor-k-common-echelon-projection-v1\",\"prime\":{},\"quotient_row_count\":{},\"row_count\":{},\"source_basis_format\":{:?},\"source_free_rows\":[",
        vector_header.column_count, prime(), free_rows.len(), free_rows.len(), basis_header.format)?;
    for (number, row) in free_rows.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "{row}")?;
    }
    write!(out, "],\"source_vector_format\":{:?},\"target\":", vector_header.format)?;
    write_target(&mut out, &quotient_target)?;
    write!(out, ",\"type\":\"header\"}}\n")?;

    let mut read_columns = 0;
    let mut nonzero_columns = 0;
    for line_result in lines {
        let line = line_result?;
        if line.trim().is_empty() { continue; }
        let source_column = integer_value(&line, "index") as usize;
        if source_column != read_columns {
            fail(format!("non-deterministic transfer order: expected {read_columns}, got {source_column}"));
        }
        let vector = parse_pairs(&line, "entries");
        validate_rows(&vector, vector_header.row_count, "transfer column");
        let (residual, _) = reduce_target_completely(vector, &basis);
        let quotient = remap_to_free(&residual, &free_index);
        if !quotient.is_empty() { nonzero_columns += 1; }
        write!(out, "{{\"entries\":")?;
        write_sparse(&mut out, &quotient)?;
        write!(out, ",\"index\":{source_column},\"source_column\":{source_column},\"type\":\"column\"}}\n")?;
        read_columns += 1;
    }
    if read_columns != vector_header.column_count {
        fail(format!("vector header says {} columns but read {read_columns}", vector_header.column_count));
    }
    eprintln!("basis_rank={} quotient_rows={} transfer_columns={} nonzero_projected={} target_residual={} elapsed={:.3}s",
        basis.len(), free_rows.len(), read_columns, nonzero_columns,
        quotient_target.len(), started.elapsed().as_secs_f64());
    Ok(())
}

fn read_selected(path: &Path) -> io::Result<BTreeSet<usize>> {
    let mut answer = BTreeSet::new();
    for line in BufReader::new(File::open(path)?).lines() {
        let text = line?;
        if text.trim().is_empty() { continue; }
        let index = text.trim().parse().unwrap_or_else(|_| fail("bad selected column index"));
        if !answer.insert(index) { fail("duplicate selected column index"); }
    }
    Ok(answer)
}

fn solve(path: &Path, output: &Path, selected_path: Option<&Path>, emit_pivots: bool) -> io::Result<()> {
    let started = Instant::now();
    let file = File::open(path)?;
    let mut lines = BufReader::new(file).lines();
    let first = lines.next().unwrap_or_else(|| fail("empty input"))?;
    let header = parse_header(&first);
    validate_rows(&header.target, header.row_count, "target");
    let mut basis: BTreeMap<usize, Pivot> = BTreeMap::new();
    let mut read_columns = 0_usize;
    let mut dependent_columns = 0_usize;
    let selected = match selected_path { Some(path) => Some(read_selected(path)?), None => None };
    for line_result in lines {
        let line = line_result?;
        if line.trim().is_empty() { continue; }
        if string_value(&line, "type") != "column" {
            fail("non-column record after header");
        }
        let source_column = integer_value(&line, "index") as usize;
        if source_column != read_columns {
            fail(format!("non-deterministic column order: expected {read_columns}, got {source_column}"));
        }
        let vector = parse_pairs(&line, "entries");
        validate_rows(&vector, header.row_count, "column");
        if selected.as_ref().map_or(true, |indices| indices.contains(&source_column)) {
            if !insert_column(vector, source_column, &mut basis) {
                dependent_columns += 1;
                if selected.is_some() { fail(format!("selected column {source_column} is dependent at prime {}", prime())); }
            }
        }
        read_columns += 1;
    }
    if read_columns != header.column_count {
        fail(format!("header says {} columns but read {read_columns}", header.column_count));
    }
    if let Some(indices) = &selected {
        if basis.len() != indices.len() { fail("not every selected column was present"); }
    }
    let target_for_pairing = header.target.clone();
    let (residual, pivot_uses) = reduce_target_completely(header.target, &basis);
    let solution = expand_solution(&pivot_uses, &basis);
    let dual_data = residual.first_key_value().map(|(&free_row, _)| {
        let dual = left_dual(&basis, free_row);
        let pairing = dot(&dual, &target_for_pairing);
        if pairing == 0 {
            fail("selected residual coordinate produced zero target pairing");
        }
        (free_row, pairing, dual)
    });
    let elapsed = started.elapsed().as_secs_f64();
    let mut out = File::create(output)?;
    write!(out, "{{\n  \"status\":\"UNAUDITED modular discovery; exact-Q replay required\",\n")?;
    write!(out, "  \"format\":\"anchor-k-modular-solution-v1\",\n")?;
    write!(out, "  \"input_format\":{:?},\n", header.format)?;
    write!(out, "  \"prime\":{},\n  \"row_count\":{},\n  \"column_count\":{},\n", prime(), header.row_count, header.column_count)?;
    write!(out, "  \"rank\":{},\n  \"dependent_columns\":{},\n", basis.len(), dependent_columns)?;
    write!(out, "  \"target_in_image\":{},\n  \"target_remainder_nonzeros\":{},\n", residual.is_empty(), residual.len())?;
    write!(out, "  \"remainder\":")?;
    write_sparse(&mut out, &residual)?;
    write!(out, ",\n  \"solution\":")?;
    write_sparse(&mut out, &solution)?;
    match &dual_data {
        Some((free_row, pairing, dual)) => {
            write!(out, ",\n  \"left_dual_free_row\":{free_row},\n  \"left_dual_target_pairing\":{pairing},\n  \"left_dual\":")?;
            write_sparse(&mut out, dual)?;
        }
        None => write!(out, ",\n  \"left_dual_free_row\":null,\n  \"left_dual_target_pairing\":0,\n  \"left_dual\":[]")?,
    }
    write!(out, ",\n  \"pivot_provenance\":[")?;
    if emit_pivots {
        for (number, (&pivot, record)) in basis.iter().enumerate() {
            if number != 0 { write!(out, ",")?; }
            write!(out, "\n    {{\"pivot_row\":{pivot},\"source_column\":{},\"raw_pivot_coefficient\":{},\"normalization_inverse\":{},\"reduced_support\":{},\"reductions\":[",
                record.source_column, record.raw_pivot_coefficient,
                record.normalization_inverse, record.vector.len())?;
            for (reduction_number, &(prior_pivot, factor)) in record.reductions.iter().enumerate() {
                if reduction_number != 0 { write!(out, ",")?; }
                write!(out, "[{prior_pivot},{factor}]")?;
            }
            write!(out, "]}}")?;
        }
    }
    write!(out, "\n  ]\n}}\n")?;
    eprintln!("rank={} residual={} solution_terms={} elapsed={elapsed:.3}s", basis.len(), residual.len(), solution.len());
    Ok(())
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let solve_mode = (args.len() == 4 || args.len() == 5) && args.get(1).map(String::as_str) == Some("solve");
    let selected_mode = args.len() == 6 && args.get(1).map(String::as_str) == Some("solve-selected");
    let project_mode = (args.len() == 5 || args.len() == 6) && args.get(1).map(String::as_str) == Some("project");
    if !solve_mode && !selected_mode && !project_mode {
        eprintln!("usage:\n  anchor-k-echelon solve INPUT.jsonl OUTPUT.json [PRIME]\n  anchor-k-echelon solve-selected INPUT.jsonl SELECTED.txt OUTPUT.json PRIME\n  anchor-k-echelon project BASIS.jsonl VECTORS.jsonl OUTPUT.jsonl [PRIME]");
        std::process::exit(2);
    }
    let prime_argument = if solve_mode && args.len() == 5 { Some(&args[4]) }
        else if selected_mode { Some(&args[5]) }
        else if project_mode && args.len() == 6 { Some(&args[5]) }
        else { None };
    if let Some(raw_prime) = prime_argument {
        let modulus: i64 = raw_prime.parse().unwrap_or_else(|_| fail("bad prime"));
        if modulus <= 2 { fail("prime must exceed two"); }
        MODULUS.store(modulus, Ordering::Relaxed);
    }
    let result = if solve_mode {
        solve(Path::new(&args[2]), Path::new(&args[3]), None, true)
    } else if selected_mode {
        solve(Path::new(&args[2]), Path::new(&args[4]), Some(Path::new(&args[3])), false)
    } else {
        project(Path::new(&args[2]), Path::new(&args[3]), Path::new(&args[4]))
    };
    if let Err(error) = result {
        fail(error.to_string());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn complete_reduction_passes_a_smaller_free_coordinate() {
        let mut basis = BTreeMap::new();
        assert!(insert_column(Sparse::from([(2, 1)]), 0, &mut basis));
        let (residual, pivot_uses) = reduce_target_completely(
            Sparse::from([(1, 1), (2, 1)]), &basis,
        );
        let solution = expand_solution(&pivot_uses, &basis);
        assert_eq!(residual, Sparse::from([(1, 1)]));
        assert_eq!(solution, Sparse::from([(0, 1)]));
    }

    #[test]
    fn repeated_entries_are_added_not_set() {
        let line = r#"{"entries":[[0,1],[0,1],[2,1]]}"#;
        assert_eq!(parse_pairs(line, "entries"), Sparse::from([(0, 2), (2, 1)]));
    }
}
