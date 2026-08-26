//! Generic no-crate anchor-K orbit closure and cascading singleton peel.

use std::collections::{BTreeMap, HashMap, HashSet, VecDeque};
use std::cell::RefCell;
use std::env;
use std::fs::File;
use std::hash::Hash;
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;
use std::time::Instant;

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Row([u8; 12]);

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Column {
    word: u16,
    multiplier: [u8; 8],
}

#[derive(Clone)]
struct Action {
    sites: [u8; 8],
    colours: [u8; 3],
}

struct Seed {
    degree: u8,
    cutoff: u8,
    anchors: [bool; 252],
    actions: Vec<Action>,
    rows: BTreeMap<Row, (i64, i64)>,
    expected: [usize; 5],
}

struct Engine {
    degree: u8,
    cutoff: u8,
    anchors: [bool; 252],
    actions: Vec<Action>,
    cell_u: [u8; 252],
    cell_v: [u8; 252],
    cell_a: [u8; 252],
    cell_b: [u8; 252],
    edge_id: [[u8; 8]; 8],
    cell_transforms: Vec<[u8; 252]>,
    word_transforms: Vec<Vec<u16>>,
    matchings: Vec<[(u8, u8); 4]>,
    word_minimum: [u8; 6561],
    row_canonical_cache: RefCell<HashMap<Row, Row>>,
    column_canonical_cache: RefCell<HashMap<Column, Column>>,
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("orbit-closure: {}", message.as_ref());
    std::process::exit(2);
}

fn hex_nibble(byte: u8) -> u8 {
    match byte {
        b'0'..=b'9' => byte - b'0',
        b'a'..=b'f' => byte - b'a' + 10,
        b'A'..=b'F' => byte - b'A' + 10,
        _ => fail("bad hex digit"),
    }
}

fn parse_hex<const N: usize>(text: &str) -> [u8; N] {
    if text.len() != 2 * N { fail(format!("expected {} hex digits", 2 * N)); }
    let bytes = text.as_bytes();
    let mut answer = [0_u8; N];
    for index in 0..N {
        answer[index] = 16 * hex_nibble(bytes[2 * index]) + hex_nibble(bytes[2 * index + 1]);
    }
    answer
}

fn write_hex<W: Write, const N: usize>(out: &mut W, bytes: &[u8; N]) -> io::Result<()> {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    for byte in bytes {
        out.write_all(&[HEX[(byte >> 4) as usize], HEX[(byte & 15) as usize]])?;
    }
    Ok(())
}

fn parse_seed(path: &Path) -> io::Result<Seed> {
    let mut degree = None;
    let mut cutoff = None;
    let mut anchors = [false; 252];
    let mut actions = Vec::new();
    let mut rows = BTreeMap::new();
    let mut expected = None;
    let file = BufReader::new(File::open(path)?);
    for (line_number, line_result) in file.lines().enumerate() {
        let line = line_result?;
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.is_empty() { continue; }
        match fields[0] {
            "KRENN_ANCHOR_K_SEED_V1" | "KRENN_ANCHOR_K_CUTOFF_SEED_V1" => {
                if line_number != 0 { fail("seed magic is not first"); }
            }
            "DEGREE" => degree = Some(fields[1].parse().unwrap_or_else(|_| fail("bad degree"))),
            "CUTOFF" => cutoff = Some(fields[1].parse().unwrap_or_else(|_| fail("bad cutoff"))),
            "ANCHORS" => {
                let ids = parse_hex::<12>(fields[1]);
                for id in ids { anchors[id as usize] = true; }
            }
            "EXPECTED" => expected = Some([
                fields[1].parse().unwrap(), fields[2].parse().unwrap(),
                fields[3].parse().unwrap(), fields[4].parse().unwrap(),
                fields[5].parse().unwrap(),
            ]),
            "ACTION" => {
                if fields[1].len() != 8 || fields[2].len() != 3 { fail("bad action"); }
                let mut sites = [0; 8];
                let mut colours = [0; 3];
                for (index, byte) in fields[1].bytes().enumerate() { sites[index] = byte - b'0'; }
                for (index, byte) in fields[2].bytes().enumerate() { colours[index] = byte - b'0'; }
                actions.push(Action { sites, colours });
            }
            "ROW" | "TARGET" => {
                let row = Row(parse_hex::<12>(fields[1]));
                let numerator = fields[2].parse().unwrap_or_else(|_| fail("bad numerator"));
                let denominator = fields[3].parse().unwrap_or_else(|_| fail("bad denominator"));
                if rows.insert(row, (numerator, denominator)).is_some() { fail("duplicate seed row"); }
            }
            _ => fail(format!("unknown seed record {}", fields[0])),
        }
    }
    if actions.is_empty() || rows.is_empty() { fail("incomplete seed"); }
    Ok(Seed {
        degree: degree.unwrap_or(0), cutoff: cutoff.unwrap_or(0), anchors,
        actions, rows, expected: expected.unwrap_or([0; 5]),
    })
}

fn decode_word(mut code: u16) -> [u8; 8] {
    let mut word = [0; 8];
    for index in (0..8).rev() {
        word[index] = (code % 3) as u8;
        code /= 3;
    }
    word
}

fn encode_word(word: &[u8; 8]) -> u16 {
    word.iter().fold(0_u16, |code, digit| 3 * code + *digit as u16)
}

fn generate_matchings() -> Vec<[(u8, u8); 4]> {
    fn recurse(vertices: &[u8], pairs: &mut Vec<(u8, u8)>, out: &mut Vec<[(u8, u8); 4]>) {
        if vertices.is_empty() {
            out.push([pairs[0], pairs[1], pairs[2], pairs[3]]);
            return;
        }
        let u = vertices[0];
        for index in 1..vertices.len() {
            let v = vertices[index];
            let mut rest = Vec::with_capacity(vertices.len() - 2);
            rest.extend_from_slice(&vertices[1..index]);
            rest.extend_from_slice(&vertices[index + 1..]);
            pairs.push((u, v));
            recurse(&rest, pairs, out);
            pairs.pop();
        }
    }
    let mut out = Vec::new();
    recurse(&[0, 1, 2, 3, 4, 5, 6, 7], &mut Vec::new(), &mut out);
    if out.len() != 105 { fail("perfect matching count changed"); }
    out
}

impl Engine {
    fn new(seed: &Seed) -> Self {
        let mut cell_u = [0; 252];
        let mut cell_v = [0; 252];
        let mut cell_a = [0; 252];
        let mut cell_b = [0; 252];
        let mut edge_id = [[0; 8]; 8];
        let mut edge = 0_u8;
        for u in 0..8_u8 {
            for v in u + 1..8_u8 {
                edge_id[u as usize][v as usize] = edge;
                edge_id[v as usize][u as usize] = edge;
                for a in 0..3_u8 {
                    for b in 0..3_u8 {
                        let id = edge as usize * 9 + a as usize * 3 + b as usize;
                        cell_u[id] = u; cell_v[id] = v; cell_a[id] = a; cell_b[id] = b;
                    }
                }
                edge += 1;
            }
        }
        let cell_id = |u: u8, v: u8, a: u8, b: u8| -> u8 {
            let edge = edge_id[u as usize][v as usize] as usize;
            (edge * 9 + a as usize * 3 + b as usize) as u8
        };
        let mut cell_transforms = Vec::new();
        for action in &seed.actions {
            let mut transform = [0; 252];
            for id in 0..252 {
                let (mut u, mut v) = (
                    action.sites[cell_u[id] as usize], action.sites[cell_v[id] as usize]
                );
                let (mut a, mut b) = (
                    action.colours[cell_a[id] as usize], action.colours[cell_b[id] as usize]
                );
                if u > v { std::mem::swap(&mut u, &mut v); std::mem::swap(&mut a, &mut b); }
                transform[id] = cell_id(u, v, a, b);
            }
            cell_transforms.push(transform);
        }
        let mut word_transforms = Vec::new();
        for action in &seed.actions {
            let mut table = vec![0_u16; 6561];
            for code in 0..6561_u16 {
                let word = decode_word(code);
                let mut image = [0; 8];
                for site in 0..8 {
                    image[action.sites[site] as usize] = action.colours[word[site] as usize];
                }
                table[code as usize] = encode_word(&image);
            }
            word_transforms.push(table);
        }
        let matchings = generate_matchings();
        let mut engine = Self {
            degree: seed.degree, cutoff: seed.cutoff, anchors: seed.anchors, actions: seed.actions.clone(),
            cell_u, cell_v, cell_a, cell_b, edge_id, cell_transforms,
            word_transforms, matchings, word_minimum: [255; 6561],
            row_canonical_cache: RefCell::new(HashMap::new()),
            column_canonical_cache: RefCell::new(HashMap::new()),
        };
        for code in 0..6561_u16 {
            let word = decode_word(code);
            let mut minimum = 4;
            for matching in &engine.matchings {
                let mut off = 0;
                for &(u, v) in matching {
                    let id = engine.cell_id(u, v, word[u as usize], word[v as usize]);
                    off += (!engine.anchors[id as usize]) as u8;
                }
                minimum = minimum.min(off);
            }
            engine.word_minimum[code as usize] = minimum;
        }
        engine
    }

    fn cell_id(&self, u: u8, v: u8, a: u8, b: u8) -> u8 {
        (self.edge_id[u as usize][v as usize] as usize * 9
         + a as usize * 3 + b as usize) as u8
    }

    fn canonical_row(&self, row: Row) -> Row {
        if let Some(&answer) = self.row_canonical_cache.borrow().get(&row) { return answer; }
        let mut best = None;
        for transform in &self.cell_transforms {
            let mut image = row.0.map(|cell| transform[cell as usize]);
            image.sort_unstable();
            let candidate = Row(image);
            if best.map_or(true, |current| candidate < current) { best = Some(candidate); }
        }
        let answer = best.unwrap();
        let mut cache = self.row_canonical_cache.borrow_mut();
        if cache.len() < 500_000 { cache.insert(row, answer); }
        answer
    }

    fn canonical_column(&self, column: Column) -> Column {
        if let Some(&answer) = self.column_canonical_cache.borrow().get(&column) { return answer; }
        let mut best = None;
        let mut best_word = u16::MAX;
        let mut best_key: Option<String> = None;
        for action in 0..self.actions.len() {
            let mut multiplier = column.multiplier.map(|cell| self.cell_transforms[action][cell as usize]);
            multiplier.sort_unstable();
            let candidate = Column {
                word: self.word_transforms[action][column.word as usize], multiplier,
            };
            // Python tuple repr order agrees with numeric lexicographic order
            // for fixed-length words in digits 0,1,2.  Compare that cheap part
            // before constructing the much more expensive bytes repr key.
            if candidate.word > best_word { continue; }
            let key = column_repr_key(&candidate);
            if candidate.word < best_word
                || best_key.as_ref().map_or(true, |current| key < *current)
            {
                best = Some(candidate);
                best_word = candidate.word;
                best_key = Some(key);
            }
        }
        let answer = best.unwrap();
        let mut cache = self.column_canonical_cache.borrow_mut();
        if cache.len() < 500_000 { cache.insert(column, answer); }
        answer
    }

    fn multiplier_degree(&self, multiplier: &[u8; 8]) -> u8 {
        multiplier.iter().map(|cell| (!self.anchors[*cell as usize]) as u8).sum()
    }

    fn minimum_degree(&self, column: &Column) -> u8 {
        self.multiplier_degree(&column.multiplier) + self.word_minimum[column.word as usize]
    }

    fn column_in_scope(&self, column: &Column) -> bool {
        let minimum = self.minimum_degree(column);
        if self.cutoff != 0 { minimum < self.cutoff } else { minimum == self.degree }
    }

    fn incident_columns(&self, row: Row) -> HashSet<Column> {
        let mut answer = HashSet::new();
        for i in 0..9 {
            for j in i + 1..10 {
                for k in j + 1..11 {
                    for l in k + 1..12 {
                        let selected = [i, j, k, l];
                        let mut mask = 0_u16;
                        let mut word = [255_u8; 8];
                        let mut valid = true;
                        for position in selected {
                            let id = row.0[position] as usize;
                            let u = self.cell_u[id] as usize;
                            let v = self.cell_v[id] as usize;
                            let bits = (1_u16 << u) | (1_u16 << v);
                            if mask & bits != 0 { valid = false; break; }
                            mask |= bits;
                            word[u] = self.cell_a[id]; word[v] = self.cell_b[id];
                        }
                        if !valid || mask != 255 || word.iter().all(|colour| *colour == word[0]) { continue; }
                        let mut multiplier = [0_u8; 8];
                        let mut next = 0;
                        for position in 0..12 {
                            if position != i && position != j && position != k && position != l {
                                multiplier[next] = row.0[position]; next += 1;
                            }
                        }
                        answer.insert(Column { word: encode_word(&word), multiplier });
                    }
                }
            }
        }
        answer
    }

    fn leading_outputs(&self, column: &Column) -> Vec<Row> {
        let word = decode_word(column.word);
        let multiplier_degree = self.multiplier_degree(&column.multiplier);
        let mut answer = Vec::new();
        for matching in &self.matchings {
            let mut term = [0_u8; 4];
            let mut off = multiplier_degree;
            for (index, &(u, v)) in matching.iter().enumerate() {
                let id = self.cell_id(u, v, word[u as usize], word[v as usize]);
                term[index] = id;
                off += (!self.anchors[id as usize]) as u8;
            }
            if if self.cutoff != 0 { off >= self.cutoff } else { off != self.degree } { continue; }
            let mut row = [0_u8; 12];
            row[..8].copy_from_slice(&column.multiplier);
            row[8..].copy_from_slice(&term);
            row.sort_unstable();
            answer.push(self.canonical_row(Row(row)));
        }
        answer
    }
}

fn python_bytes_repr(bytes: &[u8; 8]) -> String {
    let contains_single = bytes.contains(&b'\'');
    let contains_double = bytes.contains(&b'"');
    let quote = if contains_single && !contains_double { b'"' } else { b'\'' };
    let mut out = String::from("b");
    out.push(quote as char);
    for &byte in bytes {
        match byte {
            b'\\' => out.push_str("\\\\"),
            b'\t' => out.push_str("\\t"),
            b'\n' => out.push_str("\\n"),
            b'\r' => out.push_str("\\r"),
            value if value == quote => { out.push('\\'); out.push(value as char); }
            0x20..=0x7e => out.push(byte as char),
            _ => out.push_str(&format!("\\x{byte:02x}")),
        }
    }
    out.push(quote as char);
    out
}

fn column_repr_key(column: &Column) -> String {
    let word = decode_word(column.word);
    format!("(({}, {}, {}, {}, {}, {}, {}, {}), {})",
        word[0], word[1], word[2], word[3], word[4], word[5], word[6], word[7],
        python_bytes_repr(&column.multiplier))
}

fn closure(engine: &Engine, seed_rows: &BTreeMap<Row, (i64, i64)>)
    -> (HashSet<Row>, HashSet<Column>, Vec<(usize, usize)>) {
    let mut rows: HashSet<Row> = seed_rows.keys().map(|row| engine.canonical_row(*row)).collect();
    let mut frontier: HashSet<Row> = rows.clone();
    let mut columns = HashSet::new();
    let mut layers = Vec::new();
    while !frontier.is_empty() {
        let before = columns.len();
        let mut new_rows = HashSet::new();
        for row in frontier {
            for raw_column in engine.incident_columns(row) {
                if !engine.column_in_scope(&raw_column) { continue; }
                let column = engine.canonical_column(raw_column);
                if !columns.insert(column) { continue; }
                for output in engine.leading_outputs(&column) {
                    if rows.insert(output) { new_rows.insert(output); }
                }
            }
        }
        let layer = (new_rows.len(), columns.len() - before);
        layers.push(layer);
        eprintln!("layer {}: +{} rows +{} cols totals {}/{}",
            layers.len(), layer.0, layer.1, rows.len(), columns.len());
        frontier = new_rows;
    }
    (rows, columns, layers)
}

struct Peel {
    ordered_columns: Vec<Column>,
    original_supports: Vec<Vec<(Row, u8)>>,
    supports: Vec<Vec<(Row, u8)>>,
    pivot_rows: HashSet<Row>,
    pivot_ledger: Vec<(Row, usize, u8)>,
    initial_singleton_rows: usize,
    leading_histogram: BTreeMap<usize, usize>,
    projected_histogram: BTreeMap<usize, usize>,
}

fn peel(engine: &Engine, rows: &HashSet<Row>, columns: &HashSet<Column>) -> Peel {
    let mut ordered_columns: Vec<_> = columns.iter().copied().collect();
    ordered_columns.sort_by_cached_key(column_repr_key);
    let mut supports = Vec::with_capacity(ordered_columns.len());
    let mut row_to_columns: HashMap<Row, Vec<usize>> = HashMap::new();
    let mut leading_histogram = BTreeMap::new();
    for (number, column) in ordered_columns.iter().enumerate() {
        let mut outputs = engine.leading_outputs(column);
        *leading_histogram.entry(outputs.len()).or_insert(0) += 1;
        outputs.sort_unstable();
        let mut support = Vec::new();
        for row in outputs {
            if let Some((last, count)) = support.last_mut() {
                if *last == row { *count += 1; continue; }
            }
            support.push((row, 1));
        }
        for &(row, _) in &support { row_to_columns.entry(row).or_default().push(number); }
        supports.push(support);
    }
    let original_supports = supports.clone();
    let initial_rows: HashSet<_> = supports.iter().filter(|support| support.len() == 1)
        .map(|support| support[0].0).collect();
    let mut queue: VecDeque<_> = supports.iter().enumerate()
        .filter(|(_, support)| support.len() == 1).map(|(number, _)| number).collect();
    let mut pivot_rows = HashSet::new();
    let mut pivot_ledger = Vec::new();
    while let Some(number) = queue.pop_front() {
        if supports[number].len() != 1 { continue; }
        let row = supports[number][0].0;
        if !pivot_rows.insert(row) { continue; }
        pivot_ledger.push((row, number, supports[number][0].1));
        if let Some(incident_columns) = row_to_columns.get(&row) {
            for &incident in incident_columns {
                if let Some(position) = supports[incident].iter().position(|(candidate, _)| *candidate == row) {
                    supports[incident].swap_remove(position);
                    if supports[incident].len() == 1 { queue.push_back(incident); }
                }
            }
        }
    }
    let mut projected_histogram = BTreeMap::new();
    for support in &supports {
        let mass: usize = support.iter().map(|(_, count)| *count as usize).sum();
        *projected_histogram.entry(mass).or_insert(0) += 1;
    }
    if pivot_rows.len() > rows.len() { fail("peel pivoted unknown rows"); }
    Peel { ordered_columns, original_supports, supports, pivot_rows, pivot_ledger,
        initial_singleton_rows: initial_rows.len(), leading_histogram, projected_histogram }
}

fn json_integer(line: &str, key: &str) -> i64 {
    let needle = format!("\"{key}\":");
    let start = line.find(&needle).unwrap_or_else(|| fail(format!("missing key {key}"))) + needle.len();
    let tail = &line[start..];
    let end = tail.find(|c: char| !(c == '-' || c.is_ascii_digit())).unwrap_or(tail.len());
    tail[..end].parse().unwrap_or_else(|_| fail(format!("bad integer {key}")))
}

fn parse_tail6(line: &str) -> Vec<(Row, i64)> {
    let needle = "\"tail6\":[";
    let start = line.find(needle).unwrap_or_else(|| fail("missing tail6")) + needle.len();
    let end = line[start..].find("],\"type\"").unwrap_or_else(|| fail("unterminated tail6")) + start + 1;
    let text = &line[start..end];
    let mut answer = Vec::new();
    let mut cursor = 0;
    while let Some(relative) = text[cursor..].find("[\"") {
        let row_start = cursor + relative + 2;
        let row_end = row_start + 24;
        let row = Row(parse_hex::<12>(&text[row_start..row_end]));
        let comma = text[row_end..].find(',').unwrap_or_else(|| fail("tail6 pair missing comma")) + row_end + 1;
        let value_end = text[comma..].find(']').unwrap_or_else(|| fail("tail6 pair missing close")) + comma;
        let value = text[comma..value_end].parse().unwrap_or_else(|_| fail("bad tail6 coefficient"));
        answer.push((row, value));
        cursor = value_end + 1;
    }
    answer
}

fn write_pivot_ledger(path: &Path, peel: &Peel) -> io::Result<()> {
    let mut out = File::create(path)?;
    writeln!(out, "{{\"format\":\"anchor-k-singleton-pivot-ledger-v1\",\"pivot_count\":{},\"type\":\"header\"}}", peel.pivot_ledger.len())?;
    for (order, &(row, column_number, coefficient)) in peel.pivot_ledger.iter().enumerate() {
        let column = peel.ordered_columns[column_number];
        write!(out, "{{\"coefficient\":{coefficient},\"multiplier_cell_ids\":[")?;
        for (number, cell) in column.multiplier.iter().enumerate() {
            if number != 0 { write!(out, ",")?; }
            write!(out, "{cell}")?;
        }
        write!(out, "],\"order\":{order},\"pivot_row_hex\":\"")?;
        write_hex(&mut out, &row.0)?;
        write!(out, "\",\"source_closure_column\":{column_number},\"type\":\"pivot\",\"word\":\"")?;
        for digit in decode_word(column.word) { write!(out, "{digit}")?; }
        writeln!(out, "\"}}")?;
    }
    Ok(())
}

fn write_source_ledger(path: &Path, peel: &Peel) -> io::Result<()> {
    let core_count = peel.supports.iter().filter(|support| support.len() >= 2).count();
    let mut out = File::create(path)?;
    writeln!(out, "{{\"core_count\":{core_count},\"format\":\"anchor-k-source-support-ledger-v1\",\"pivot_count\":{},\"type\":\"header\"}}", peel.pivot_ledger.len())?;
    let pivot_order: HashMap<_, _> = peel.pivot_ledger.iter().enumerate()
        .map(|(order, &(row, column, coefficient))| (column, (order, row, coefficient))).collect();
    let mut core_index = 0_usize;
    for (column_number, column) in peel.ordered_columns.iter().enumerate() {
        let role = if let Some(&(order, pivot_row, coefficient)) = pivot_order.get(&column_number) {
            format!("\"pivot_coefficient\":{coefficient},\"pivot_order\":{order},\"pivot_row_hex\":\"{}\",\"role\":\"pivot\"", hex_string(&pivot_row.0))
        } else if peel.supports[column_number].len() >= 2 {
            let text = format!("\"core_index\":{core_index},\"role\":\"core\"");
            core_index += 1;
            text
        } else { continue };
        write!(out, "{{\"multiplier_cell_ids\":[")?;
        for (number, cell) in column.multiplier.iter().enumerate() {
            if number != 0 { write!(out, ",")?; }
            write!(out, "{cell}")?;
        }
        write!(out, "],\"original_entries\":[")?;
        for (number, (row, count)) in peel.original_supports[column_number].iter().enumerate() {
            if number != 0 { write!(out, ",")?; }
            write!(out, "[\"{}\",{count}]", hex_string(&row.0))?;
        }
        write!(out, "],{role},\"source_closure_column\":{column_number},\"type\":\"source_column\",\"word\":\"")?;
        for digit in decode_word(column.word) { write!(out, "{digit}")?; }
        writeln!(out, "\"}}")?;
    }
    if core_index != core_count { fail("source ledger core numbering mismatch"); }
    Ok(())
}

fn hex_string<const N: usize>(bytes: &[u8; N]) -> String {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    let mut answer = String::with_capacity(2 * N);
    for byte in bytes {
        answer.push(HEX[(byte >> 4) as usize] as char);
        answer.push(HEX[(byte & 15) as usize] as char);
    }
    answer
}

fn augment_with_transfers(direct_path: &Path, transfer_path: &Path, output_path: &Path,
                          pivot_path: &Path, rows: &HashSet<Row>, peel: &Peel) -> io::Result<(usize, usize, usize)> {
    let mut coupled_rows: Vec<_> = rows.iter().filter(|row| !peel.pivot_rows.contains(row)).copied().collect();
    coupled_rows.sort_unstable();
    let row_index: HashMap<_, _> = coupled_rows.iter().enumerate().map(|(i, row)| (*row, i)).collect();

    let transfer_file = BufReader::new(File::open(transfer_path)?);
    let mut transfer_lines = transfer_file.lines();
    let transfer_header = transfer_lines.next().unwrap_or_else(|| fail("empty transfer file"))?;
    let transfer_count = json_integer(&transfer_header, "kernel_dimension") as usize;
    let transfer_prime = json_integer(&transfer_header, "prime");
    let direct_count = peel.supports.iter().filter(|support| support.len() >= 2).count();

    let direct_file = BufReader::new(File::open(direct_path)?);
    let mut direct_lines = direct_file.lines();
    let mut header = direct_lines.next().unwrap_or_else(|| fail("empty direct interface"))?;
    header = header.replacen(
        &format!("\"column_count\":{direct_count}"),
        &format!("\"column_count\":{}", direct_count + transfer_count), 1,
    );
    header = header.replacen(
        "krenn-dangerous-chart26-degree6-coupled-v1",
        "krenn-anchor-k-degree6-augmented-lower-kernel-v1", 1,
    );
    let insertion = format!("\"lower_kernel_prime\":{transfer_prime},\"direct_column_count\":{direct_count},");
    header = header.replacen("\"format\":", &(insertion + "\"format\":"), 1);
    let mut out = File::create(output_path)?;
    writeln!(out, "{header}")?;
    for line in direct_lines { writeln!(out, "{}", line?)?; }

    let mut read_transfers = 0;
    let mut nonzero_transfers = 0;
    let mut projected_nnz = 0;
    for line_result in transfer_lines {
        let line = line_result?;
        let source_index = json_integer(&line, "index") as usize;
        if source_index != read_transfers { fail("non-deterministic transfer index"); }
        let mut projected: BTreeMap<usize, i64> = BTreeMap::new();
        for (row, value) in parse_tail6(&line) {
            if let Some(&index) = row_index.get(&row) {
                let updated = (projected.get(&index).copied().unwrap_or(0) + value)
                    .rem_euclid(transfer_prime);
                if updated == 0 { projected.remove(&index); }
                else { projected.insert(index, updated); }
            } else if !peel.pivot_rows.contains(&row) {
                fail("transfer row absent from closed component");
            }
        }
        if !projected.is_empty() { nonzero_transfers += 1; }
        projected_nnz += projected.len();
        let output_index = direct_count + source_index;
        write!(out, "{{\"entries\":[")?;
        for (number, (row, value)) in projected.iter().enumerate() {
            if number != 0 { write!(out, ",")?; }
            write!(out, "[{row},{value}]")?;
        }
        writeln!(out, "],\"index\":{output_index},\"source_transfer_index\":{source_index},\"type\":\"column\"}}")?;
        read_transfers += 1;
    }
    if read_transfers != transfer_count { fail("transfer count mismatch"); }
    write_pivot_ledger(pivot_path, peel)?;
    Ok((transfer_count, nonzero_transfers, projected_nnz))
}

fn write_interface(path: &Path, seed: &Seed, rows: &HashSet<Row>, peel: &Peel) -> io::Result<(usize, usize)> {
    let mut coupled_rows: Vec<_> = rows.iter().filter(|row| !peel.pivot_rows.contains(row)).copied().collect();
    coupled_rows.sort_unstable();
    let row_index: HashMap<_, _> = coupled_rows.iter().enumerate().map(|(i, row)| (*row, i)).collect();
    let coupled_columns: Vec<_> = peel.supports.iter().enumerate()
        .filter(|(_, support)| support.len() >= 2).map(|(i, _)| i).collect();
    let mut out = File::create(path)?;
    let interface_format = if seed.cutoff != 0 {
        format!("krenn-anchor-k-truncated-cutoff{}-coupled-v1", seed.cutoff)
    } else {
        "krenn-dangerous-chart26-degree6-coupled-v1".to_string()
    };
    write!(out, "{{\"column_count\":{},\"format\":{:?},\"row_count\":{},\"rows_hex\":[",
        coupled_columns.len(), interface_format, coupled_rows.len())?;
    for (number, row) in coupled_rows.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "\"")?; write_hex(&mut out, &row.0)?; write!(out, "\"")?;
    }
    write!(out, "],\"target\":[")?;
    let mut first = true;
    for (row, &(numerator, denominator)) in &seed.rows {
        if numerator == 0 { continue; }
        if let Some(&index) = row_index.get(row) {
            if !first { write!(out, ",")?; } first = false;
            write!(out, "[{index},{numerator},{denominator}]")?;
        }
    }
    write!(out, "],\"type\":\"header\"}}\n")?;
    for (output_number, &column_number) in coupled_columns.iter().enumerate() {
        let column = peel.ordered_columns[column_number];
        let mut entries: Vec<_> = peel.supports[column_number].iter()
            .map(|(row, count)| (row_index[row], *count)).collect();
        entries.sort_unstable();
        write!(out, "{{\"entries\":[")?;
        for (number, (row, count)) in entries.iter().enumerate() {
            if number != 0 { write!(out, ",")?; }
            write!(out, "[{row},{count}]")?;
        }
        write!(out, "],\"index\":{output_number},\"multiplier_cell_ids\":[")?;
        for (number, cell) in column.multiplier.iter().enumerate() {
            if number != 0 { write!(out, ",")?; }
            write!(out, "{cell}")?;
        }
        let word = decode_word(column.word);
        write!(out, "],\"type\":\"column\",\"word\":\"")?;
        for digit in word { write!(out, "{digit}")?; }
        write!(out, "\"}}\n")?;
    }
    Ok((coupled_rows.len(), coupled_columns.len()))
}

fn write_results(path: &Path, seed: &Seed, rows: usize, columns: usize,
                 layers: &[(usize, usize)], peel: &Peel,
                 coupled_rows: usize, coupled_columns: usize) -> io::Result<()> {
    let mut out = File::create(path)?;
    write!(out, "{{\n  \"status\":\"UNAUDITED Rust exact census; Python replay required\",\n  \"degree\":{},\n  \"cutoff\":{},\n  \"stabilizer_order\":{},\n  \"seed_rows\":{},\n  \"closure_rows\":{rows},\n  \"closure_columns\":{columns},\n  \"closure_layers\":[",
        seed.degree, seed.cutoff, seed.actions.len(), seed.rows.len())?;
    for (number, (new_rows, new_columns)) in layers.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "[{new_rows},{new_columns}]")?;
    }
    write!(out, "],\n  \"initial_singleton_rows\":{},\n  \"saturated_pivot_rows\":{},\n  \"coupled_rows\":{coupled_rows},\n  \"coupled_columns\":{coupled_columns},\n  \"leading_histogram\":{{",
        peel.initial_singleton_rows, peel.pivot_rows.len())?;
    for (number, (mass, count)) in peel.leading_histogram.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "\"{mass}\":{count}")?;
    }
    write!(out, "}},\n  \"projected_histogram\":{{")?;
    for (number, (mass, count)) in peel.projected_histogram.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "\"{mass}\":{count}")?;
    }
    write!(out, "}},\n  \"expected_control\":[{},{},{},{},{}],\n  \"controls_match\":{}\n}}\n",
        seed.expected[0], seed.expected[1], seed.expected[2], seed.expected[3], seed.expected[4],
        control_matches(seed.expected[0], rows) && control_matches(seed.expected[1], columns)
        && control_matches(seed.expected[2], layers.len())
        && control_matches(seed.expected[3], coupled_rows)
        && control_matches(seed.expected[4], coupled_columns))?;
    Ok(())
}

fn control_matches(expected: usize, actual: usize) -> bool {
    expected == 0 || expected == actual
}

fn gcd(mut left: i64, mut right: i64) -> i64 {
    left = left.abs(); right = right.abs();
    while right != 0 { let remainder = left % right; left = right; right = remainder; }
    left.max(1)
}

/// Accept either already-quotiented seed rows or labelled/raw seed rows.  The
/// latter is important for very large stabilizers: Rust can canonicalize and
/// sum the orbit mass much faster than the seed exporter.  Recanonicalizing an
/// existing quotient seed is idempotent and is covered by the chart26 digest.
fn canonicalize_seed_rows(engine: &Engine, rows: &BTreeMap<Row, (i64, i64)>)
    -> BTreeMap<Row, (i64, i64)>
{
    let mut answer = BTreeMap::new();
    for (&row, &(numerator, denominator)) in rows {
        if denominator == 0 { fail("zero seed denominator"); }
        let representative = engine.canonical_row(row);
        let (old_numerator, old_denominator) = answer.get(&representative).copied().unwrap_or((0, 1));
        let new_numerator = old_numerator as i128 * denominator as i128
            + numerator as i128 * old_denominator as i128;
        let new_denominator = old_denominator as i128 * denominator as i128;
        if new_numerator < i64::MIN as i128 || new_numerator > i64::MAX as i128
            || new_denominator < 1 || new_denominator > i64::MAX as i128
        { fail("seed rational overflow"); }
        let divisor = gcd(new_numerator as i64, new_denominator as i64);
        answer.insert(representative,
            (new_numerator as i64 / divisor, new_denominator as i64 / divisor));
    }
    answer.retain(|_, (numerator, _)| *numerator != 0);
    answer
}

fn main() {
    let args: Vec<_> = env::args().collect();
    if !(args.len() == 4 || args.len() == 5 || args.len() == 6 || args.len() == 7) {
        eprintln!("usage: orbit_closure SEED.txt OUT_MATRIX.jsonl OUT_RESULTS.json [OUT_PIVOTS.jsonl [OUT_SOURCE_LEDGER.jsonl]]\n       orbit_closure SEED.txt OUT_MATRIX.jsonl OUT_RESULTS.json TRANSFERS.jsonl OUT_AUGMENTED.jsonl OUT_PIVOTS.jsonl");
        std::process::exit(2);
    }
    let total = Instant::now();
    let mut seed = parse_seed(Path::new(&args[1])).unwrap_or_else(|e| fail(e.to_string()));
    let engine = Engine::new(&seed);
    seed.rows = canonicalize_seed_rows(&engine, &seed.rows);
    let closure_start = Instant::now();
    let (rows, columns, layers) = closure(&engine, &seed.rows);
    let closure_seconds = closure_start.elapsed().as_secs_f64();
    let peel_start = Instant::now();
    let peel = peel(&engine, &rows, &columns);
    let peel_seconds = peel_start.elapsed().as_secs_f64();
    let (coupled_rows, coupled_columns) = write_interface(Path::new(&args[2]), &seed, &rows, &peel)
        .unwrap_or_else(|e| fail(e.to_string()));
    write_results(Path::new(&args[3]), &seed, rows.len(), columns.len(), &layers,
                  &peel, coupled_rows, coupled_columns)
        .unwrap_or_else(|e| fail(e.to_string()));
    if args.len() == 5 || args.len() == 6 {
        write_pivot_ledger(Path::new(&args[4]), &peel)
            .unwrap_or_else(|e| fail(e.to_string()));
        if args.len() == 6 {
            write_source_ledger(Path::new(&args[5]), &peel)
                .unwrap_or_else(|e| fail(e.to_string()));
        }
        eprintln!("pivot_ledger={}", peel.pivot_ledger.len());
    } else if args.len() == 7 {
        let transfer_stats = augment_with_transfers(
            Path::new(&args[2]), Path::new(&args[4]), Path::new(&args[5]),
            Path::new(&args[6]), &rows, &peel,
        ).unwrap_or_else(|e| fail(e.to_string()));
        eprintln!("projected transfers={} nonzero={} nnz={} pivot_ledger={}",
            transfer_stats.0, transfer_stats.1, transfer_stats.2, peel.pivot_ledger.len());
    }
    if !(control_matches(seed.expected[0], rows.len())
         && control_matches(seed.expected[1], columns.len())
         && control_matches(seed.expected[2], layers.len())
         && control_matches(seed.expected[3], coupled_rows)
         && control_matches(seed.expected[4], coupled_columns)) {
        fail("frozen census controls did not match");
    }
    eprintln!("PASS closure={closure_seconds:.3}s peel={peel_seconds:.3}s total={:.3}s",
        total.elapsed().as_secs_f64());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn producer_cutoff_header_and_target_alias_are_accepted() {
        let path = std::env::temp_dir().join(format!(
            "krenn-orbit-seed-parser-{}-{}.txt", std::process::id(), line!()
        ));
        std::fs::write(&path, concat!(
            "KRENN_ANCHOR_K_CUTOFF_SEED_V1\n",
            "CUTOFF 7\n",
            "ANCHORS 000102030405060708090a0b\n",
            "ACTION 01234567 012\n",
            "TARGET 000102030405060708090a0b 3 2\n",
        )).unwrap();
        let seed = parse_seed(&path).unwrap();
        std::fs::remove_file(&path).unwrap();
        assert_eq!(seed.cutoff, 7);
        assert_eq!(seed.actions.len(), 1);
        assert_eq!(seed.rows.values().copied().collect::<Vec<_>>(), vec![(3, 2)]);
        assert_eq!(seed.expected, [0; 5]);
    }
}
