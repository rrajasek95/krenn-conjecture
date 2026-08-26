//! Streaming structural census for a peeled anchor-K sparse interface.
//!
//! This deliberately performs no field arithmetic.  It records exact
//! bipartite connected components, target-bearing components, and row/column
//! degree histograms before a modular or rational solve is attempted.

use std::collections::{BTreeMap, BTreeSet};
use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;
use std::time::Instant;

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("core-structure: {}", message.as_ref());
    std::process::exit(2);
}

fn key_start(line: &str, key: &str) -> usize {
    let needle = format!("\"{key}\"");
    let key_pos = line.find(&needle).unwrap_or_else(|| fail(format!("missing JSON key {key}")));
    let tail = &line[key_pos + needle.len()..];
    let colon = tail.find(':').unwrap_or_else(|| fail(format!("missing colon after {key}")));
    key_pos + needle.len() + colon + 1
}

fn integer_value(line: &str, key: &str) -> usize {
    let start = key_start(line, key);
    let tail = line[start..].trim_start();
    let end = tail.find(|c: char| !c.is_ascii_digit()).unwrap_or(tail.len());
    tail[..end].parse().unwrap_or_else(|_| fail(format!("bad integer at {key}")))
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
            if escaped { escaped = false; }
            else if *byte == b'\\' { escaped = true; }
            else if *byte == b'"' { quoted = false; }
            continue;
        }
        match *byte {
            b'"' => quoted = true,
            b'[' => depth += 1,
            b']' => {
                depth -= 1;
                if depth == 0 { return &line[begin..=begin + offset]; }
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
            while index < bytes.len() && bytes[index].is_ascii_digit() { index += 1; }
            answer.push(text[begin..index].parse().unwrap_or_else(|_| fail("bad array integer")));
        } else { index += 1; }
    }
    answer
}

#[derive(Clone, Copy)]
struct UnionFindEntry {
    parent: u32,
    size: u32,
}

struct UnionFind(Vec<UnionFindEntry>);

impl UnionFind {
    fn new(count: usize) -> Self {
        if count > u32::MAX as usize { fail("too many rows for packed union-find"); }
        Self((0..count).map(|index| UnionFindEntry { parent: index as u32, size: 1 }).collect())
    }

    fn find(&mut self, mut index: u32) -> u32 {
        let mut root = index;
        while self.0[root as usize].parent != root { root = self.0[root as usize].parent; }
        while index != root {
            let next = self.0[index as usize].parent;
            self.0[index as usize].parent = root;
            index = next;
        }
        root
    }

    fn union(&mut self, left: u32, right: u32) {
        let mut a = self.find(left);
        let mut b = self.find(right);
        if a == b { return; }
        if self.0[a as usize].size < self.0[b as usize].size { std::mem::swap(&mut a, &mut b); }
        self.0[b as usize].parent = a;
        self.0[a as usize].size += self.0[b as usize].size;
    }
}

#[derive(Default)]
struct Component {
    rows: usize,
    columns: usize,
    target_rows: usize,
    min_row: usize,
    min_column: usize,
}

fn increment(histogram: &mut BTreeMap<usize, usize>, key: usize) {
    *histogram.entry(key).or_default() += 1;
}

fn write_histogram<W: Write>(out: &mut W, histogram: &BTreeMap<usize, usize>) -> io::Result<()> {
    write!(out, "{{")?;
    for (number, (key, count)) in histogram.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "\"{key}\":{count}")?;
    }
    write!(out, "}}")
}

fn census(input: &Path, output: &Path) -> io::Result<()> {
    let started = Instant::now();
    let mut reader = BufReader::new(File::open(input)?);
    let mut header = String::new();
    reader.read_line(&mut header)?;
    if header.is_empty() { fail("empty input"); }
    let row_count = integer_value(&header, "row_count");
    let column_count = integer_value(&header, "column_count");
    let target_flat = integers(array_text(&header, "target"));
    if target_flat.len() % 3 != 0 { fail("target is not index/numerator/denominator triples"); }
    let mut target_rows = BTreeSet::new();
    for triple in target_flat.chunks_exact(3) {
        if triple[0] < 0 || triple[0] as usize >= row_count { fail("target row out of range"); }
        if triple[1] != 0 { target_rows.insert(triple[0] as usize); }
    }

    let mut union_find = UnionFind::new(row_count);
    let mut row_degrees = vec![0_u32; row_count];
    let mut column_first_rows = Vec::with_capacity(column_count);
    let mut column_offsets = Vec::with_capacity(column_count + 1);
    let mut column_rows = Vec::<u32>::new();
    column_offsets.push(0);
    let mut column_support_histogram = BTreeMap::new();
    let mut column_mass_histogram = BTreeMap::new();
    let mut total_nonzeros = 0_usize;
    let mut line = String::new();
    let mut read_columns = 0_usize;
    loop {
        line.clear();
        if reader.read_line(&mut line)? == 0 { break; }
        if line.trim().is_empty() { continue; }
        let index = integer_value(&line, "index");
        if index != read_columns { fail(format!("expected column {read_columns}, read {index}")); }
        let entries = integers(array_text(&line, "entries"));
        if entries.len() % 2 != 0 { fail("entries is not index/value pairs"); }
        let mut first = None;
        let mut support = 0_usize;
        let mut mass = 0_usize;
        for pair in entries.chunks_exact(2) {
            if pair[0] < 0 || pair[0] as usize >= row_count { fail("column row out of range"); }
            if pair[1] == 0 { continue; }
            let row = pair[0] as usize;
            row_degrees[row] += 1;
            column_rows.push(row as u32);
            support += 1;
            mass += pair[1].unsigned_abs() as usize;
            if let Some(anchor) = first { union_find.union(anchor, row as u32); }
            else { first = Some(row as u32); }
        }
        let first = first.unwrap_or_else(|| fail(format!("zero column {index}")));
        column_first_rows.push(first);
        column_offsets.push(column_rows.len());
        increment(&mut column_support_histogram, support);
        increment(&mut column_mass_histogram, mass);
        total_nonzeros += support;
        read_columns += 1;
    }
    if read_columns != column_count { fail(format!("header columns {column_count}, read {read_columns}")); }

    // Complementary leaf peel: the producer already removed columns whose
    // current support is one.  Here a row occurring in one current column
    // pivots that column; removing it can expose further row leaves.  This is
    // a purely structural maximum-matching reduction, not a coefficient solve.
    let mut row_offsets = vec![0_usize; row_count + 1];
    for row in 0..row_count { row_offsets[row + 1] = row_offsets[row] + row_degrees[row] as usize; }
    let mut row_columns = vec![0_u32; total_nonzeros];
    let mut cursors = row_offsets[..row_count].to_vec();
    for column in 0..column_count {
        for &row in &column_rows[column_offsets[column]..column_offsets[column + 1]] {
            let cursor = &mut cursors[row as usize];
            row_columns[*cursor] = column as u32;
            *cursor += 1;
        }
    }
    let mut active_columns = vec![true; column_count];
    let mut leaf_degrees = row_degrees.clone();
    let mut queue = std::collections::VecDeque::new();
    for (row, &degree) in leaf_degrees.iter().enumerate() {
        if degree == 1 { queue.push_back(row as u32); }
    }
    let initial_row_leaves = queue.len();
    let mut row_leaf_pivots = 0_usize;
    while let Some(row) = queue.pop_front() {
        if leaf_degrees[row as usize] != 1 { continue; }
        let incident = row_columns[row_offsets[row as usize]..row_offsets[row as usize + 1]].iter()
            .find(|&&column| active_columns[column as usize]).copied()
            .unwrap_or_else(|| fail("degree-one row has no active incident column"));
        active_columns[incident as usize] = false;
        row_leaf_pivots += 1;
        for &touched in &column_rows[column_offsets[incident as usize]..column_offsets[incident as usize + 1]] {
            let degree = &mut leaf_degrees[touched as usize];
            if *degree == 0 { fail("active column touches degree-zero row"); }
            *degree -= 1;
            if *degree == 1 { queue.push_back(touched); }
        }
    }
    let mut post_leaf_row_degree_histogram = BTreeMap::new();
    for &degree in &leaf_degrees { increment(&mut post_leaf_row_degree_histogram, degree as usize); }
    let active_row_count = leaf_degrees.iter().filter(|&&degree| degree != 0).count();
    let active_column_count = active_columns.iter().filter(|&&active| active).count();
    let isolated_row_count = row_count - active_row_count;

    // Connected components of the smaller structural fixed point.
    let mut leaf_union = UnionFind::new(row_count);
    let mut leaf_first_rows = vec![u32::MAX; column_count];
    for column in 0..column_count {
        if !active_columns[column] { continue; }
        let mut first = None;
        for &row in &column_rows[column_offsets[column]..column_offsets[column + 1]] {
            if leaf_degrees[row as usize] == 0 { fail("active column retained an isolated row"); }
            if let Some(anchor) = first { leaf_union.union(anchor, row); }
            else { first = Some(row); }
        }
        leaf_first_rows[column] = first.unwrap_or_else(|| fail("active zero column"));
    }
    let mut leaf_components = BTreeMap::<u32, (usize, usize, usize)>::new();
    for row in 0..row_count {
        if leaf_degrees[row] == 0 { continue; }
        let root = leaf_union.find(row as u32);
        let entry = leaf_components.entry(root).or_default();
        entry.0 += 1;
        if target_rows.contains(&row) { entry.2 += 1; }
    }
    for column in 0..column_count {
        if !active_columns[column] { continue; }
        let root = leaf_union.find(leaf_first_rows[column]);
        leaf_components.get_mut(&root).unwrap().1 += 1;
    }

    let mut components: BTreeMap<u32, Component> = BTreeMap::new();
    let mut row_degree_histogram = BTreeMap::new();
    for (row, degree) in row_degrees.iter().copied().enumerate() {
        increment(&mut row_degree_histogram, degree as usize);
        let root = union_find.find(row as u32);
        let component = components.entry(root).or_insert_with(|| Component {
            min_row: usize::MAX, min_column: usize::MAX, ..Component::default()
        });
        component.rows += 1;
        component.min_row = component.min_row.min(row);
        if target_rows.contains(&row) { component.target_rows += 1; }
    }
    for (column, &first) in column_first_rows.iter().enumerate() {
        let root = union_find.find(first);
        let component = components.get_mut(&root).unwrap_or_else(|| fail("missing component root"));
        component.columns += 1;
        component.min_column = component.min_column.min(column);
    }

    let mut shapes = BTreeMap::<(usize, usize, usize), usize>::new();
    let mut target_components = Vec::new();
    let mut largest: Vec<_> = components.iter().map(|(&root, component)| (root, component)).collect();
    largest.sort_by_key(|(_, component)| std::cmp::Reverse(component.rows + component.columns));
    for (&root, component) in &components {
        *shapes.entry((component.rows, component.columns, component.target_rows)).or_default() += 1;
        if component.target_rows != 0 { target_components.push((root, component)); }
    }
    target_components.sort_by_key(|(_, component)| std::cmp::Reverse(component.rows + component.columns));

    let min_row_degree = row_degree_histogram.keys().next().copied().unwrap_or(0);
    let min_column_support = column_support_histogram.keys().next().copied().unwrap_or(0);
    let mut out = File::create(output)?;
    writeln!(out, "{{")?;
    writeln!(out, "  \"format\":\"anchor-k-core-structure-v1\",")?;
    writeln!(out, "  \"input\":{:?},", input.to_string_lossy())?;
    writeln!(out, "  \"row_count\":{row_count},")?;
    writeln!(out, "  \"column_count\":{column_count},")?;
    writeln!(out, "  \"nonzero_count\":{total_nonzeros},")?;
    writeln!(out, "  \"target_nonzeros\":{},", target_rows.len())?;
    write!(out, "  \"row_degree_histogram\":")?; write_histogram(&mut out, &row_degree_histogram)?; writeln!(out, ",")?;
    write!(out, "  \"column_support_histogram\":")?; write_histogram(&mut out, &column_support_histogram)?; writeln!(out, ",")?;
    write!(out, "  \"column_coefficient_mass_histogram\":")?; write_histogram(&mut out, &column_mass_histogram)?; writeln!(out, ",")?;
    writeln!(out, "  \"minimum_row_degree\":{min_row_degree},")?;
    writeln!(out, "  \"minimum_column_support\":{min_column_support},")?;
    writeln!(out, "  \"column_singleton_fixed_point\":{},", min_column_support >= 2)?;
    writeln!(out, "  \"initial_row_leaves\":{initial_row_leaves},")?;
    writeln!(out, "  \"row_leaf_pivots\":{row_leaf_pivots},")?;
    writeln!(out, "  \"post_row_leaf_rows\":{active_row_count},")?;
    writeln!(out, "  \"post_row_leaf_columns\":{active_column_count},")?;
    writeln!(out, "  \"post_row_leaf_isolated_rows\":{isolated_row_count},")?;
    write!(out, "  \"post_row_leaf_degree_histogram\":")?; write_histogram(&mut out, &post_leaf_row_degree_histogram)?; writeln!(out, ",")?;
    writeln!(out, "  \"post_row_leaf_component_count\":{},", leaf_components.len())?;
    write!(out, "  \"post_row_leaf_component_shapes\":[")?;
    let mut leaf_shapes = BTreeMap::new();
    for &(rows, columns, targets) in leaf_components.values() {
        *leaf_shapes.entry((rows, columns, targets)).or_insert(0_usize) += 1;
    }
    for (number, ((rows, columns, targets), count)) in leaf_shapes.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "[\"{rows}x{columns}\",{targets},{count}]")?;
    }
    writeln!(out, "],")?;
    writeln!(out, "  \"component_count\":{},", components.len())?;
    writeln!(out, "  \"target_component_count\":{},", target_components.len())?;
    write!(out, "  \"component_shape_histogram\":[")?;
    for (number, ((rows, columns, target), count)) in shapes.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "[\"{rows}x{columns}\",{target},{count}]")?;
    }
    writeln!(out, "],")?;
    write!(out, "  \"target_components\":[")?;
    for (number, (root, component)) in target_components.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "{{\"root\":{root},\"rows\":{},\"columns\":{},\"target_rows\":{},\"min_row\":{},\"min_column\":{}}}",
            component.rows, component.columns, component.target_rows, component.min_row, component.min_column)?;
    }
    writeln!(out, "],")?;
    write!(out, "  \"largest_components\":[")?;
    for (number, (root, component)) in largest.iter().take(32).enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "{{\"root\":{root},\"rows\":{},\"columns\":{},\"target_rows\":{},\"min_row\":{},\"min_column\":{}}}",
            component.rows, component.columns, component.target_rows, component.min_row, component.min_column)?;
    }
    writeln!(out, "],")?;
    writeln!(out, "  \"elapsed_seconds\":{:.6}", started.elapsed().as_secs_f64())?;
    writeln!(out, "}}")?;
    eprintln!("PASS rows={row_count} columns={column_count} nnz={total_nonzeros} components={} target_components={} min_degrees={min_row_degree}/{min_column_support} elapsed={:.3}s",
        components.len(), target_components.len(), started.elapsed().as_secs_f64());
    Ok(())
}

fn main() {
    let args: Vec<_> = env::args().collect();
    if args.len() != 3 {
        eprintln!("usage: core_structure INPUT.jsonl OUTPUT.json");
        std::process::exit(2);
    }
    if let Err(error) = census(Path::new(&args[1]), Path::new(&args[2])) { fail(error.to_string()); }
}
