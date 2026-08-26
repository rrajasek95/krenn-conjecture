//! Exact H-coinvariant row expansion of the omitted sparse-R8 tail in K9..K12.
//!
//! This generalizes the sealed K9-only expander without changing it.  It
//! collects the literal target and all 9,607 source-column outputs under the
//! frozen 2,304-element H action, then writes the nonzero target-source rows.

use std::collections::{BTreeMap, HashMap, HashSet};
use std::env;
use std::fs::{self, File};
use std::io::{self, BufRead, BufReader, BufWriter, Write};
use std::path::Path;
use std::time::Instant;

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Row12([u8; 12]);

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Row24([u8; 24]);

#[derive(Clone, Copy)]
struct Action {
    sites: [u8; 8],
    colours: [u8; 3],
}

#[derive(Clone)]
struct Term {
    index: usize,
    coefficient: i64,
    word: u16,
    multiplier: [u8; 8],
}

struct Seed {
    anchors: [bool; 252],
    actions: Vec<Action>,
    terms: Vec<Term>,
}

struct Engine {
    anchors: [bool; 252],
    actions: Vec<Action>,
    cell_u: [u8; 252],
    cell_v: [u8; 252],
    cell_a: [u8; 252],
    cell_b: [u8; 252],
    edge_id: [[u8; 8]; 8],
    transforms: Vec<[u8; 252]>,
    matchings: Vec<[(u8, u8); 4]>,
    word_minimum_degree: [u8; 6561],
}

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Column8 {
    word: u16,
    multiplier: [u8; 8],
}

#[derive(Default)]
struct Piece {
    rows: BTreeMap<(u8, Row12), i128>,
    emissions: [u64; 13],
    firing_terms: [u64; 13],
}

#[derive(Default)]
struct StagePiece {
    rows: BTreeMap<(u8, Row24), i128>,
    parents: u64,
    parent_mass: i128,
    parent_l1: i128,
    pivotable: u64,
    terminal: u64,
    raw_children: [u64; 25],
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("expand-k9-k12-tail: {}", message.as_ref());
    std::process::exit(2)
}

fn nibble(byte: u8) -> u8 {
    match byte {
        b'0'..=b'9' => byte - b'0',
        b'a'..=b'f' => byte - b'a' + 10,
        b'A'..=b'F' => byte - b'A' + 10,
        _ => fail("bad hex digit"),
    }
}

fn parse_hex<const N: usize>(text: &str) -> [u8; N] {
    if text.len() != 2 * N {
        fail("bad hex length")
    }
    let bytes = text.as_bytes();
    let mut out = [0; N];
    for i in 0..N {
        out[i] = 16 * nibble(bytes[2 * i]) + nibble(bytes[2 * i + 1]);
    }
    out
}

fn hex(row: &Row12) -> String {
    const DIGITS: &[u8; 16] = b"0123456789abcdef";
    let mut out = String::with_capacity(24);
    for byte in row.0 {
        out.push(DIGITS[(byte >> 4) as usize] as char);
        out.push(DIGITS[(byte & 15) as usize] as char);
    }
    out
}

fn hex24(row: &Row24) -> String {
    const DIGITS: &[u8; 16] = b"0123456789abcdef";
    let mut out = String::with_capacity(48);
    for byte in row.0 {
        out.push(DIGITS[(byte >> 4) as usize] as char);
        out.push(DIGITS[(byte & 15) as usize] as char);
    }
    out
}

fn hex8(row: &[u8; 8]) -> String {
    const DIGITS: &[u8; 16] = b"0123456789abcdef";
    let mut out = String::with_capacity(16);
    for byte in row {
        out.push(DIGITS[(byte >> 4) as usize] as char);
        out.push(DIGITS[(byte & 15) as usize] as char);
    }
    out
}

fn encode_word(text: &str) -> u16 {
    if text.len() != 8 {
        fail("bad word width")
    }
    text.bytes().fold(0, |code, digit| {
        if !(b'0'..=b'2').contains(&digit) {
            fail("bad word digit")
        }
        3 * code + (digit - b'0') as u16
    })
}

fn decode_word(mut code: u16) -> [u8; 8] {
    let mut word = [0; 8];
    for i in (0..8).rev() {
        word[i] = (code % 3) as u8;
        code /= 3;
    }
    word
}

fn parse_seed(path: &Path) -> io::Result<Seed> {
    let mut anchors = [false; 252];
    let mut anchor_count = 0;
    let mut actions = Vec::new();
    let mut terms = Vec::new();
    for (number, line) in BufReader::new(File::open(path)?).lines().enumerate() {
        let line = line?;
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.is_empty() {
            continue;
        }
        match fields[0] {
            "KRENN_SPARSE_R8_K9_TAIL_TERMS_V1" => {
                if number != 0 {
                    fail("magic is not first")
                }
            }
            "ANCHORS" => {
                if anchor_count != 0 {
                    fail("duplicate anchors")
                }
                for cell in parse_hex::<12>(fields[1]) {
                    if anchors[cell as usize] {
                        fail("duplicate anchor cell")
                    }
                    anchors[cell as usize] = true;
                    anchor_count += 1;
                }
            }
            "ACTION" => {
                let mut sites = [0; 8];
                let mut colours = [0; 3];
                if fields[1].len() != 8 || fields[2].len() != 3 {
                    fail("bad action width")
                }
                for (i, byte) in fields[1].bytes().enumerate() {
                    sites[i] = byte - b'0';
                }
                for (i, byte) in fields[2].bytes().enumerate() {
                    colours[i] = byte - b'0';
                }
                actions.push(Action { sites, colours });
            }
            "TERM" => {
                if fields.len() != 7 {
                    fail("bad term schema")
                }
                terms.push(Term {
                    index: fields[1].parse().unwrap_or_else(|_| fail("bad term index")),
                    coefficient: fields[2].parse().unwrap_or_else(|_| fail("bad coefficient")),
                    word: encode_word(fields[3]),
                    multiplier: parse_hex::<8>(fields[4]),
                });
            }
            _ => fail(format!("unknown seed record {}", fields[0])),
        }
    }
    if anchor_count != 12 || actions.len() != 2304 || terms.len() != 9607 {
        fail("seed census changed")
    }
    for (index, term) in terms.iter().enumerate() {
        if term.index != index {
            fail("term indices changed")
        }
    }
    Ok(Seed { anchors, actions, terms })
}

fn perfect_matchings() -> Vec<[(u8, u8); 4]> {
    fn recurse(vertices: &[u8], pairs: &mut Vec<(u8, u8)>, out: &mut Vec<[(u8, u8); 4]>) {
        if vertices.is_empty() {
            out.push([pairs[0], pairs[1], pairs[2], pairs[3]]);
            return;
        }
        for i in 1..vertices.len() {
            let mut rest = Vec::new();
            rest.extend_from_slice(&vertices[1..i]);
            rest.extend_from_slice(&vertices[i + 1..]);
            pairs.push((vertices[0], vertices[i]));
            recurse(&rest, pairs, out);
            pairs.pop();
        }
    }
    let mut out = Vec::new();
    recurse(&[0, 1, 2, 3, 4, 5, 6, 7], &mut Vec::new(), &mut out);
    if out.len() != 105 {
        fail("matching census changed")
    }
    out
}

impl Engine {
    fn new(seed: &Seed) -> Self {
        let mut cell_u = [0; 252];
        let mut cell_v = [0; 252];
        let mut cell_a = [0; 252];
        let mut cell_b = [0; 252];
        let mut edge_id = [[0; 8]; 8];
        let mut edge = 0u8;
        for u in 0..8u8 {
            for v in u + 1..8u8 {
                edge_id[u as usize][v as usize] = edge;
                edge_id[v as usize][u as usize] = edge;
                for a in 0..3u8 {
                    for b in 0..3u8 {
                        let id = edge as usize * 9 + a as usize * 3 + b as usize;
                        cell_u[id] = u;
                        cell_v[id] = v;
                        cell_a[id] = a;
                        cell_b[id] = b;
                    }
                }
                edge += 1;
            }
        }
        let cell = |u: u8, v: u8, a: u8, b: u8| -> u8 {
            (edge_id[u as usize][v as usize] as usize * 9 + a as usize * 3 + b as usize) as u8
        };
        let mut transforms = Vec::new();
        for action in &seed.actions {
            let mut transform = [0; 252];
            for id in 0..252 {
                let (mut u, mut v) = (action.sites[cell_u[id] as usize], action.sites[cell_v[id] as usize]);
                let (mut a, mut b) = (action.colours[cell_a[id] as usize], action.colours[cell_b[id] as usize]);
                if u > v {
                    std::mem::swap(&mut u, &mut v);
                    std::mem::swap(&mut a, &mut b);
                }
                transform[id] = cell(u, v, a, b);
            }
            transforms.push(transform);
        }
        let matchings = perfect_matchings();
        let mut word_minimum_degree = [4u8; 6561];
        for code in 0..6561u16 {
            let word = decode_word(code);
            word_minimum_degree[code as usize] = matchings.iter()
                .map(|matching| {
                    let mut row = [0u8; 4];
                    for (i, &(u, v)) in matching.iter().enumerate() {
                        row[i] = cell(u, v, word[u as usize], word[v as usize]);
                    }
                    row.iter().map(|entry| (!seed.anchors[*entry as usize]) as u8).sum()
                })
                .min().unwrap();
        }
        Self {
            anchors: seed.anchors,
            actions: seed.actions.clone(),
            cell_u,
            cell_v,
            cell_a,
            cell_b,
            edge_id,
            transforms,
            matchings,
            word_minimum_degree,
        }
    }

    fn cell(&self, u: u8, v: u8, a: u8, b: u8) -> u8 {
        (self.edge_id[u as usize][v as usize] as usize * 9 + a as usize * 3 + b as usize) as u8
    }

    fn degree(&self, cells: &[u8]) -> u8 {
        cells.iter().map(|cell| (!self.anchors[*cell as usize]) as u8).sum()
    }

    fn matching_row(&self, word: &[u8; 8], matching: &[(u8, u8); 4]) -> [u8; 4] {
        let mut row = [0; 4];
        for (i, &(u, v)) in matching.iter().enumerate() {
            row[i] = self.cell(u, v, word[u as usize], word[v as usize]);
        }
        row
    }

    fn canonical(&self, row: Row12, cache: &mut HashMap<Row12, Row12>) -> Row12 {
        if let Some(answer) = cache.get(&row) {
            return *answer;
        }
        let mut best = None;
        for transform in &self.transforms {
            let mut image = row.0.map(|cell| transform[cell as usize]);
            image.sort_unstable();
            let candidate = Row12(image);
            if best.map_or(true, |old| candidate < old) {
                best = Some(candidate);
            }
        }
        let answer = best.unwrap();
        if cache.len() < 400_000 {
            cache.insert(row, answer);
        }
        answer
    }

    fn canonical24(&self, row: Row24, cache: &mut HashMap<Row24, Row24>) -> Row24 {
        if let Some(answer) = cache.get(&row) {
            return *answer;
        }
        let mut best = None;
        for transform in &self.transforms {
            let mut image = row.0.map(|cell| transform[cell as usize]);
            image.sort_unstable();
            let candidate = Row24(image);
            if best.map_or(true, |old| candidate < old) {
                best = Some(candidate);
            }
        }
        let answer = best.unwrap();
        if cache.len() < 200_000 {
            cache.insert(row, answer);
        }
        answer
    }

    fn canonical_column8(&self, column: Column8, cache: &mut HashMap<Column8, Column8>) -> Column8 {
        if let Some(answer) = cache.get(&column) {
            return *answer;
        }
        let word = decode_word(column.word);
        let mut best = None;
        for (index, action) in self.actions.iter().enumerate() {
            let mut image_word = [0u8; 8];
            for site in 0..8 {
                image_word[action.sites[site] as usize] = action.colours[word[site] as usize];
            }
            let mut multiplier = column.multiplier.map(|cell| self.transforms[index][cell as usize]);
            multiplier.sort_unstable();
            let candidate = Column8 { word: image_word.iter().fold(0, |code, digit| 3 * code + *digit as u16), multiplier };
            if best.map_or(true, |old| candidate < old) {
                best = Some(candidate);
            }
        }
        let answer = best.unwrap();
        if cache.len() < 500_000 {
            cache.insert(column, answer);
        }
        answer
    }
}

fn expand_source(engine: &Engine, terms: &[Term], workers: usize) -> Piece {
    let chunk = terms.len().div_ceil(workers);
    let mut pieces = Vec::new();
    std::thread::scope(|scope| {
        let mut handles = Vec::new();
        for worker in 0..workers {
            let start = worker * chunk;
            let end = ((worker + 1) * chunk).min(terms.len());
            if start >= end {
                continue;
            }
            handles.push(scope.spawn(move || {
                let begun = Instant::now();
                let mut piece = Piece::default();
                let mut cache = HashMap::new();
                for term in &terms[start..end] {
                    let word = decode_word(term.word);
                    let multiplier_degree = engine.degree(&term.multiplier);
                    let mut fired = [false; 13];
                    for matching in &engine.matchings {
                        let selected = engine.matching_row(&word, matching);
                        let degree = multiplier_degree + engine.degree(&selected);
                        if !(9..=12).contains(&degree) {
                            continue;
                        }
                        let mut row = [0; 12];
                        row[..8].copy_from_slice(&term.multiplier);
                        row[8..].copy_from_slice(&selected);
                        row.sort_unstable();
                        let representative = engine.canonical(Row12(row), &mut cache);
                        *piece.rows.entry((degree, representative)).or_default() += term.coefficient as i128;
                        piece.emissions[degree as usize] += 1;
                        fired[degree as usize] = true;
                    }
                    for degree in 9..=12 {
                        piece.firing_terms[degree] += fired[degree] as u64;
                    }
                }
                eprintln!(
                    "source {start}..{end} rows={} cache={} elapsed={:.3}s",
                    piece.rows.len(), cache.len(), begun.elapsed().as_secs_f64()
                );
                piece
            }));
        }
        for handle in handles {
            pieces.push(handle.join().unwrap_or_else(|_| fail("source worker panic")));
        }
    });
    merge_pieces(pieces)
}

fn expand_target(engine: &Engine, workers: usize) -> Piece {
    let pure: Vec<Vec<[u8; 4]>> = (0..3u8)
        .map(|colour| {
            let word = [colour; 8];
            engine.matchings.iter().map(|matching| engine.matching_row(&word, matching)).collect()
        })
        .collect();
    let chunk = 105usize.div_ceil(workers);
    let mut pieces = Vec::new();
    std::thread::scope(|scope| {
        let mut handles = Vec::new();
        for worker in 0..workers {
            let start = worker * chunk;
            let end = ((worker + 1) * chunk).min(105);
            if start >= end {
                continue;
            }
            let pure = &pure;
            handles.push(scope.spawn(move || {
                let begun = Instant::now();
                let mut piece = Piece::default();
                let mut cache = HashMap::new();
                for first in start..end {
                    for second in 0..105 {
                        for third in 0..105 {
                            let mut row = [0; 12];
                            row[..4].copy_from_slice(&pure[0][first]);
                            row[4..8].copy_from_slice(&pure[1][second]);
                            row[8..].copy_from_slice(&pure[2][third]);
                            let degree = engine.degree(&row);
                            if !(9..=12).contains(&degree) {
                                continue;
                            }
                            row.sort_unstable();
                            let representative = engine.canonical(Row12(row), &mut cache);
                            *piece.rows.entry((degree, representative)).or_default() += 1;
                            piece.emissions[degree as usize] += 1;
                        }
                    }
                }
                eprintln!(
                    "target {start}..{end} rows={} cache={} elapsed={:.3}s",
                    piece.rows.len(), cache.len(), begun.elapsed().as_secs_f64()
                );
                piece
            }));
        }
        for handle in handles {
            pieces.push(handle.join().unwrap_or_else(|_| fail("target worker panic")));
        }
    });
    merge_pieces(pieces)
}

fn merge_pieces(pieces: Vec<Piece>) -> Piece {
    let mut out = Piece::default();
    for piece in pieces {
        for ((degree, row), coefficient) in piece.rows {
            *out.rows.entry((degree, row)).or_default() += coefficient;
        }
        for degree in 9..=12 {
            out.emissions[degree] += piece.emissions[degree];
            out.firing_terms[degree] += piece.firing_terms[degree];
        }
    }
    out
}

fn write_outputs(result_path: &Path, row_path: &Path, target: &Piece, source: &Piece, elapsed: f64) -> io::Result<()> {
    let mut tail = target.rows.clone();
    for (&key, &coefficient) in &source.rows {
        *tail.entry(key).or_default() -= coefficient;
    }
    tail.retain(|_, coefficient| *coefficient != 0);

    let row_tmp = row_path.with_extension("tsv.tmp");
    let mut rows = BufWriter::new(File::create(&row_tmp)?);
    writeln!(rows, "degree\trow\tcoefficient")?;
    for ((degree, row), coefficient) in &tail {
        writeln!(rows, "{degree}\t{}\t{coefficient}", hex(row))?;
    }
    rows.flush()?;
    drop(rows);
    fs::rename(&row_tmp, row_path)?;

    let mut target_orbits = [0u64; 13];
    let mut source_orbits = [0u64; 13];
    let mut tail_orbits = [0u64; 13];
    let mut tail_mass = [0i128; 13];
    let mut tail_l1 = [0i128; 13];
    for &(degree, _) in target.rows.keys() {
        target_orbits[degree as usize] += 1;
    }
    for &(degree, _) in source.rows.keys() {
        source_orbits[degree as usize] += 1;
    }
    for (&(degree, _), &coefficient) in &tail {
        tail_orbits[degree as usize] += 1;
        tail_mass[degree as usize] += coefficient;
        tail_l1[degree as usize] += coefficient.abs();
    }

    let array = |values: &[u64; 13]| format!("[{}, {}, {}, {}]", values[9], values[10], values[11], values[12]);
    let array_i = |values: &[i128; 13]| format!("[\"{}\", \"{}\", \"{}\", \"{}\"]", values[9], values[10], values[11], values[12]);
    let text = format!(
        "{{\n  \"status\": \"PASS_EXACT_H_COINVARIANT_K9_K12_TAIL_ROWS\",\n  \"degrees\": [9, 10, 11, 12],\n  \"source_terms\": 9607,\n  \"stabilizer_order\": 2304,\n  \"perfect_matchings\": 105,\n  \"target_literal_emissions\": {},\n  \"source_literal_emissions\": {},\n  \"source_firing_terms\": {},\n  \"target_row_orbits_before_subtraction\": {},\n  \"source_row_orbits_before_subtraction\": {},\n  \"tail_nonzero_row_orbits\": {},\n  \"tail_coefficient_mass\": {},\n  \"tail_coefficient_l1\": {},\n  \"row_ledger\": \"{}\",\n  \"representation\": \"natural H-coinvariant representatives with labelled multiplicities summed into integer orbit masses\",\n  \"elapsed_seconds\": {:.6},\n  \"scope\": \"exact K9--K12 row interface only; no filtered continuation, K24 residual, membership, or conjecture claim\"\n}}\n",
        array(&target.emissions), array(&source.emissions), array(&source.firing_terms),
        array(&target_orbits), array(&source_orbits), array(&tail_orbits),
        array_i(&tail_mass), array_i(&tail_l1), row_path.display(), elapsed
    );
    let result_tmp = result_path.with_extension("json.tmp");
    fs::write(&result_tmp, text)?;
    fs::rename(result_tmp, result_path)?;
    Ok(())
}

fn pivot_packets(engine: &Engine) -> Vec<([u8; 4], Vec<[u8; 4]>)> {
    let base = [(0u8, 1u8), (2, 3), (4, 5), (6, 7)];
    let mut packets = Vec::new();
    for code in 0..81u8 {
        let mut value = code;
        let mut pair_colours = [0u8; 4];
        for i in (0..4).rev() {
            pair_colours[i] = value % 3;
            value /= 3;
        }
        if pair_colours.iter().all(|colour| *colour == pair_colours[0]) {
            continue;
        }
        let mut word = [0u8; 8];
        for i in 0..4 {
            word[base[i].0 as usize] = pair_colours[i];
            word[base[i].1 as usize] = pair_colours[i];
        }
        let mut pivot = engine.matching_row(&word, &base);
        pivot.sort_unstable();
        if engine.degree(&pivot) != 0 {
            fail("pivot left K0")
        }
        let mut tails = Vec::new();
        let mut histogram = [0u64; 5];
        for matching in &engine.matchings {
            let mut tail = engine.matching_row(&word, matching);
            tail.sort_unstable();
            let degree = engine.degree(&tail) as usize;
            if degree == 0 {
                if tail != pivot {
                    fail("word has unexpected K0 matching")
                }
            } else {
                histogram[degree] += 1;
                tails.push(tail);
            }
        }
        if histogram != [0, 0, 12, 32, 60] || tails.len() != 104 {
            fail("pivot tail histogram changed")
        }
        packets.push((pivot, tails));
    }
    packets.sort_by_key(|packet| packet.0);
    if packets.len() != 78 {
        fail("pivot packet census changed")
    }
    packets
}

fn remove_pivot(row: &Row24, pivot: &[u8; 4]) -> Option<[u8; 20]> {
    let mut multiplier = [0u8; 20];
    let (mut selected, mut kept) = (0usize, 0usize);
    for &cell in &row.0 {
        if selected < 4 && cell == pivot[selected] {
            selected += 1;
        } else {
            if kept >= 20 {
                return None;
            }
            multiplier[kept] = cell;
            kept += 1;
        }
    }
    if selected == 4 && kept == 20 { Some(multiplier) } else { None }
}

fn merge_stage_pieces(pieces: Vec<StagePiece>) -> StagePiece {
    let mut out = StagePiece::default();
    for piece in pieces {
        out.parents += piece.parents;
        out.parent_mass += piece.parent_mass;
        out.parent_l1 += piece.parent_l1;
        out.pivotable += piece.pivotable;
        out.terminal += piece.terminal;
        for degree in 0..=24 {
            out.raw_children[degree] += piece.raw_children[degree];
        }
        for (key, coefficient) in piece.rows {
            *out.rows.entry(key).or_default() += coefficient;
        }
    }
    out.rows.retain(|_, coefficient| *coefficient != 0);
    out
}

fn reduce_initial_stage(seed_path: &Path, input_path: &Path, degree: u8, result_path: &Path, output_path: &Path) {
    let begun = Instant::now();
    let seed = parse_seed(seed_path).unwrap_or_else(|error| fail(error.to_string()));
    let engine = Engine::new(&seed);
    let packets = pivot_packets(&engine);
    let mut anchor_cells = [0u8; 12];
    let mut anchor_count = 0;
    for (cell, present) in seed.anchors.iter().enumerate() {
        if *present {
            anchor_cells[anchor_count] = cell as u8;
            anchor_count += 1;
        }
    }
    if anchor_count != 12 {
        fail("anchor census changed")
    }

    let mut parents = Vec::new();
    for (number, line) in BufReader::new(File::open(input_path).unwrap_or_else(|error| fail(error.to_string()))).lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        if number == 0 {
            if line != "degree\trow\tcoefficient" {
                fail("input row header changed")
            }
            continue;
        }
        let fields: Vec<_> = line.split('\t').collect();
        if fields.len() != 3 {
            fail("input row schema changed")
        }
        let row_degree: u8 = fields[0].parse().unwrap_or_else(|_| fail("bad input degree"));
        if row_degree != degree {
            continue;
        }
        let tail = parse_hex::<12>(fields[1]);
        let coefficient: i128 = fields[2].parse().unwrap_or_else(|_| fail("bad input coefficient"));
        if coefficient == 0 || engine.degree(&tail) != degree {
            fail("bad input row")
        }
        let mut row = [0u8; 24];
        row[..12].copy_from_slice(&anchor_cells);
        row[12..].copy_from_slice(&tail);
        row.sort_unstable();
        parents.push((Row24(row), coefficient));
    }
    if parents.is_empty() {
        fail("empty selected degree")
    }

    let workers = std::thread::available_parallelism().map_or(4, |count| count.get()).min(8);
    let chunk = parents.len().div_ceil(workers);
    let mut pieces = Vec::new();
    std::thread::scope(|scope| {
        let mut handles = Vec::new();
        for worker in 0..workers {
            let start = worker * chunk;
            let end = ((worker + 1) * chunk).min(parents.len());
            if start >= end {
                continue;
            }
            let parents = &parents;
            let packets = &packets;
            let engine = &engine;
            handles.push(scope.spawn(move || {
                let worker_begun = Instant::now();
                let mut piece = StagePiece::default();
                let mut cache = HashMap::new();
                for &(row, coefficient) in &parents[start..end] {
                    piece.parents += 1;
                    piece.parent_mass += coefficient;
                    piece.parent_l1 += coefficient.abs();
                    let selected = packets.iter().find_map(|(pivot, tails)| {
                        remove_pivot(&row, pivot).map(|multiplier| (multiplier, tails))
                    });
                    let Some((multiplier, tails)) = selected else {
                        piece.terminal += 1;
                        continue;
                    };
                    piece.pivotable += 1;
                    for tail in tails {
                        let child_degree = degree + engine.degree(tail);
                        if child_degree > 24 {
                            fail("child degree exceeded 24")
                        }
                        let mut child = [0u8; 24];
                        child[..20].copy_from_slice(&multiplier);
                        child[20..].copy_from_slice(tail);
                        child.sort_unstable();
                        let representative = engine.canonical24(Row24(child), &mut cache);
                        *piece.rows.entry((child_degree, representative)).or_default() -= coefficient;
                        piece.raw_children[child_degree as usize] += 1;
                    }
                }
                eprintln!(
                    "stage K{degree} {start}..{end} rows={} cache={} elapsed={:.3}s",
                    piece.rows.len(), cache.len(), worker_begun.elapsed().as_secs_f64()
                );
                piece
            }));
        }
        for handle in handles {
            pieces.push(handle.join().unwrap_or_else(|_| fail("stage worker panic")));
        }
    });
    let stage = merge_stage_pieces(pieces);
    if stage.parents != parents.len() as u64 || stage.terminal != 0 || stage.pivotable != stage.parents {
        fail("initial stage pivotability changed")
    }

    let output_tmp = output_path.with_extension("tsv.tmp");
    let mut output = BufWriter::new(File::create(&output_tmp).unwrap_or_else(|error| fail(error.to_string())));
    writeln!(output, "degree\trow\tcoefficient").unwrap();
    let mut output_counts = [0u64; 25];
    let mut output_mass = [0i128; 25];
    let mut output_l1 = [0i128; 25];
    for (&(child_degree, row), &coefficient) in &stage.rows {
        writeln!(output, "{child_degree}\t{}\t{coefficient}", hex24(&row)).unwrap();
        output_counts[child_degree as usize] += 1;
        output_mass[child_degree as usize] += coefficient;
        output_l1[child_degree as usize] += coefficient.abs();
    }
    output.flush().unwrap();
    drop(output);
    fs::rename(&output_tmp, output_path).unwrap_or_else(|error| fail(error.to_string()));

    let d2 = degree as usize + 2;
    let d3 = degree as usize + 3;
    let d4 = degree as usize + 4;
    let text = format!(
        "{{\n  \"status\": \"PASS_EXACT_SINGLE_PIVOT_INITIAL_STAGE\",\n  \"input_degree\": {degree},\n  \"input_rows\": {},\n  \"input_coefficient_mass\": \"{}\",\n  \"input_coefficient_l1\": \"{}\",\n  \"pivotable_rows\": {},\n  \"terminal_rows\": {},\n  \"pivot_policy\": \"lexicographically first available mixed pair-constant K0 word on each natural H-coinvariant row\",\n  \"raw_children_by_degree\": {{\"{d2}\": {}, \"{d3}\": {}, \"{d4}\": {}}},\n  \"nonzero_output_orbits_by_degree\": {{\"{d2}\": {}, \"{d3}\": {}, \"{d4}\": {}}},\n  \"output_mass_by_degree\": {{\"{d2}\": \"{}\", \"{d3}\": \"{}\", \"{d4}\": \"{}\"}},\n  \"output_l1_by_degree\": {{\"{d2}\": \"{}\", \"{d3}\": \"{}\", \"{d4}\": \"{}\"}},\n  \"output_ledger\": \"{}\",\n  \"stabilizer_order\": 2304,\n  \"source_relation\": \"q*m = -sum_(nonleading matchings t) t*m in the mixed ideal coinvariants; no pivot averaging or division\",\n  \"elapsed_seconds\": {:.6},\n  \"scope\": \"one exact initial reduction stage only; no complete tail reduction, K24 residual, membership, or conjecture claim\"\n}}\n",
        stage.parents, stage.parent_mass, stage.parent_l1, stage.pivotable, stage.terminal,
        stage.raw_children[d2], stage.raw_children[d3], stage.raw_children[d4],
        output_counts[d2], output_counts[d3], output_counts[d4],
        output_mass[d2], output_mass[d3], output_mass[d4],
        output_l1[d2], output_l1[d3], output_l1[d4],
        output_path.display(), begun.elapsed().as_secs_f64()
    );
    let result_tmp = result_path.with_extension("json.tmp");
    fs::write(&result_tmp, text).unwrap_or_else(|error| fail(error.to_string()));
    fs::rename(result_tmp, result_path).unwrap_or_else(|error| fail(error.to_string()));
    eprintln!("PASS exact initial K{degree} reduction stage elapsed={:.3}s", begun.elapsed().as_secs_f64());
}

fn remove_selected12(row: &Row12, selected: &[u8; 4]) -> Option<[u8; 8]> {
    let mut selected = *selected;
    selected.sort_unstable();
    let mut multiplier = [0u8; 8];
    let (mut removed, mut kept) = (0usize, 0usize);
    for &cell in &row.0 {
        if removed < 4 && cell == selected[removed] {
            removed += 1;
        } else {
            if kept >= 8 {
                return None;
            }
            multiplier[kept] = cell;
            kept += 1;
        }
    }
    if removed == 4 && kept == 8 { Some(multiplier) } else { None }
}

fn incident_columns8(engine: &Engine, row: Row12, cache: &mut HashMap<Column8, Column8>) -> HashSet<Column8> {
    let mut by_edge: Vec<Vec<u8>> = (0..28).map(|_| Vec::new()).collect();
    for &cell in &row.0 {
        let edge = engine.edge_id[engine.cell_u[cell as usize] as usize][engine.cell_v[cell as usize] as usize] as usize;
        if !by_edge[edge].contains(&cell) {
            by_edge[edge].push(cell);
        }
    }
    let mut columns = HashSet::new();
    for matching in &engine.matchings {
        let lists: [&[u8]; 4] = matching.map(|(u, v)| {
            by_edge[engine.edge_id[u as usize][v as usize] as usize].as_slice()
        });
        if lists.iter().any(|list| list.is_empty()) {
            continue;
        }
        for &c0 in lists[0] {
            for &c1 in lists[1] {
                for &c2 in lists[2] {
                    for &c3 in lists[3] {
                        let selected = [c0, c1, c2, c3];
                        let mut word = [255u8; 8];
                        for &cell in &selected {
                            let id = cell as usize;
                            word[engine.cell_u[id] as usize] = engine.cell_a[id];
                            word[engine.cell_v[id] as usize] = engine.cell_b[id];
                        }
                        if !word.iter().all(|digit| *digit < 3) || word.iter().all(|digit| *digit == word[0]) {
                            continue;
                        }
                        let multiplier = remove_selected12(&row, &selected).unwrap_or_else(|| fail("bad row divisor"));
                        let raw = Column8 { word: word.iter().fold(0, |code, digit| 3 * code + *digit as u16), multiplier };
                        columns.insert(engine.canonical_column8(raw, cache));
                    }
                }
            }
        }
    }
    columns
}

fn column_minimum_degree(engine: &Engine, column: Column8) -> u8 {
    engine.degree(&column.multiplier) + engine.word_minimum_degree[column.word as usize]
}

fn column_k9_outputs(engine: &Engine, column: Column8, cache: &mut HashMap<Row12, Row12>) -> BTreeMap<Row12, u8> {
    let word = decode_word(column.word);
    let multiplier_degree = engine.degree(&column.multiplier);
    let mut rows = BTreeMap::new();
    for matching in &engine.matchings {
        let selected = engine.matching_row(&word, matching);
        if multiplier_degree + engine.degree(&selected) != 9 {
            continue;
        }
        let mut row = [0u8; 12];
        row[..8].copy_from_slice(&column.multiplier);
        row[8..].copy_from_slice(&selected);
        row.sort_unstable();
        let representative = engine.canonical(Row12(row), cache);
        *rows.entry(representative).or_default() += 1;
    }
    rows
}

fn column_outputs_through9(engine: &Engine, column: Column8, cache: &mut HashMap<Row12, Row12>) -> BTreeMap<(u8, Row12), u8> {
    let word = decode_word(column.word);
    let multiplier_degree = engine.degree(&column.multiplier);
    let mut rows = BTreeMap::new();
    for matching in &engine.matchings {
        let selected = engine.matching_row(&word, matching);
        let degree = multiplier_degree + engine.degree(&selected);
        if degree > 9 {
            continue;
        }
        let mut row = [0u8; 12];
        row[..8].copy_from_slice(&column.multiplier);
        row[8..].copy_from_slice(&selected);
        row.sort_unstable();
        let representative = engine.canonical(Row12(row), cache);
        *rows.entry((degree, representative)).or_default() += 1;
    }
    rows
}

fn parse_column_ledger(path: &Path) -> Vec<Column8> {
    let mut columns = Vec::new();
    for (number, line) in BufReader::new(File::open(path).unwrap_or_else(|error| fail(error.to_string()))).lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        if number == 0 {
            if line != "column_index\tminimum_degree\tword\tmultiplier" {
                fail("column ledger header changed")
            }
            continue;
        }
        let fields: Vec<_> = line.split('\t').collect();
        if fields.len() != 4 || fields[0].parse::<usize>().unwrap_or(usize::MAX) != columns.len() {
            fail("column ledger schema/index changed")
        }
        columns.push(Column8 { word: encode_word(fields[2]), multiplier: parse_hex::<8>(fields[3]) });
    }
    columns
}

fn column_output_gate(
    seed_path: &Path,
    columns_path: &Path,
    requested: usize,
    result_path: &Path,
    edge_output: Option<&Path>,
) {
    let begun = Instant::now();
    let seed = parse_seed(seed_path).unwrap_or_else(|error| fail(error.to_string()));
    let engine = Engine::new(&seed);
    let columns = parse_column_ledger(columns_path);
    if columns.len() != 128_875 || requested == 0 || requested > columns.len() {
        fail("column/sample census changed")
    }
    let sample: Vec<_> = (0..requested).map(|index| {
        let column_index = index * columns.len() / requested;
        (column_index, columns[column_index])
    }).collect();
    let mut cache = HashMap::new();
    let mut raw_hist = BTreeMap::new();
    let mut edge_hist = BTreeMap::new();
    let mut rows_by_degree: Vec<HashSet<Row12>> = (0..10).map(|_| HashSet::new()).collect();
    let mut edges = 0u64;
    let mut edge_writer = edge_output.map(|path| {
        let tmp = path.with_extension("tsv.tmp");
        let mut writer = BufWriter::new(File::create(&tmp).unwrap_or_else(|error| fail(error.to_string())));
        writeln!(writer, "column_index\tdegree\trow\tmultiplicity").unwrap();
        (path.to_path_buf(), tmp, writer)
    });
    for (column_index, column) in sample {
        let outputs = column_outputs_through9(&engine, column, &mut cache);
        for (&(degree, row), &multiplicity) in &outputs {
            if let Some((_, _, writer)) = edge_writer.as_mut() {
                writeln!(writer, "{column_index}\t{degree}\t{}\t{multiplicity}", hex(&row)).unwrap();
            }
            *edge_hist.entry(degree).or_insert(0u64) += 1;
            *raw_hist.entry(degree).or_insert(0u64) += multiplicity as u64;
            rows_by_degree[degree as usize].insert(row);
            edges += 1;
        }
    }
    if let Some((path, tmp, mut writer)) = edge_writer {
        writer.flush().unwrap();
        drop(writer);
        fs::rename(tmp, path).unwrap_or_else(|error| fail(error.to_string()));
    }
    let hist = |map: &BTreeMap<u8, u64>| {
        map.iter().map(|(key, value)| format!("\"{key}\":{value}")).collect::<Vec<_>>().join(",")
    };
    let rows_hist = (0..=9).filter(|degree| !rows_by_degree[*degree].is_empty())
        .map(|degree| format!("\"{degree}\":{}", rows_by_degree[degree].len())).collect::<Vec<_>>().join(",");
    let text = format!(
        "{{\n  \"status\": \"PASS_BOUNDED_K5_K9_JOINT_COLUMN_OUTPUT_GATE\",\n  \"total_columns\": {},\n  \"sample_columns\": {requested},\n  \"unique_weighted_edges\": {edges},\n  \"raw_outputs_by_degree\": {{{}}},\n  \"unique_edges_by_degree\": {{{}}},\n  \"unique_rows_by_degree\": {{{rows_hist}}},\n  \"row_canonical_cache\": {},\n  \"elapsed_seconds\": {:.6},\n  \"projected_full_seconds\": {:.6},\n  \"scope\": \"bounded joint lower/K9 output gate only; no complete closure, kernel, membership, or conjecture result\"\n}}\n",
        columns.len(), hist(&raw_hist), hist(&edge_hist), cache.len(), begun.elapsed().as_secs_f64(),
        begun.elapsed().as_secs_f64() * columns.len() as f64 / requested as f64
    );
    let tmp = result_path.with_extension("json.tmp");
    fs::write(&tmp, text).unwrap_or_else(|error| fail(error.to_string()));
    fs::rename(tmp, result_path).unwrap_or_else(|error| fail(error.to_string()));
    eprintln!("PASS bounded joint output sample={requested} edges={edges} elapsed={:.3}s", begun.elapsed().as_secs_f64());
}

fn column_output_interval(
    seed_path: &Path,
    columns_path: &Path,
    start: usize,
    count: usize,
    index_offset: usize,
    result_path: &Path,
    edge_path: &Path,
) {
    let begun = Instant::now();
    let seed = parse_seed(seed_path).unwrap_or_else(|error| fail(error.to_string()));
    let engine = Engine::new(&seed);
    let columns = parse_column_ledger(columns_path);
    let end = start.checked_add(count).unwrap_or_else(|| fail("column interval overflow"));
    if count == 0 || end > columns.len() {
        fail("bad column interval")
    }
    if result_path.exists() || edge_path.exists() {
        fail("refusing to overwrite column interval output")
    }

    let edge_tmp = edge_path.with_extension("tsv.tmp");
    let mut writer = BufWriter::new(File::create(&edge_tmp).unwrap_or_else(|error| fail(error.to_string())));
    writeln!(writer, "column_index\tdegree\trow\tmultiplicity").unwrap();
    let mut cache = HashMap::new();
    let mut raw_hist = BTreeMap::new();
    let mut edge_hist = BTreeMap::new();
    let mut rows_by_degree: Vec<HashSet<Row12>> = (0..10).map(|_| HashSet::new()).collect();
    let mut edges = 0u64;
    for (column_index, &column) in columns[start..end].iter().enumerate() {
        let global_index = index_offset + start + column_index;
        let outputs = column_outputs_through9(&engine, column, &mut cache);
        for (&(degree, row), &multiplicity) in &outputs {
            writeln!(writer, "{global_index}\t{degree}\t{}\t{multiplicity}", hex(&row)).unwrap();
            *edge_hist.entry(degree).or_insert(0u64) += 1;
            *raw_hist.entry(degree).or_insert(0u64) += multiplicity as u64;
            rows_by_degree[degree as usize].insert(row);
            edges += 1;
        }
    }
    writer.flush().unwrap();
    drop(writer);
    fs::rename(&edge_tmp, edge_path).unwrap_or_else(|error| fail(error.to_string()));

    let hist = |map: &BTreeMap<u8, u64>| {
        map.iter().map(|(key, value)| format!("\"{key}\":{value}")).collect::<Vec<_>>().join(",")
    };
    let rows_hist = (0..=9).filter(|degree| !rows_by_degree[*degree].is_empty())
        .map(|degree| format!("\"{degree}\":{}", rows_by_degree[degree].len())).collect::<Vec<_>>().join(",");
    let elapsed = begun.elapsed().as_secs_f64();
    let text = format!(
        "{{\n  \"status\": \"PASS_EXACT_K5_K9_COLUMN_OUTPUT_INTERVAL\",\n  \"total_columns\": {},\n  \"start\": {start},\n  \"end\": {end},\n  \"count\": {count},\n  \"index_offset\": {index_offset},\n  \"unique_weighted_edges\": {edges},\n  \"raw_outputs_by_degree\": {{{}}},\n  \"unique_edges_by_degree\": {{{}}},\n  \"unique_rows_by_degree_within_interval\": {{{rows_hist}}},\n  \"row_canonical_cache\": {},\n  \"elapsed_seconds\": {:.6},\n  \"scope\": \"exact bounded column interval only; global closure/kernel/membership require fail-closed merge\"\n}}\n",
        columns.len(), hist(&raw_hist), hist(&edge_hist), cache.len(), elapsed,
    );
    let result_tmp = result_path.with_extension("json.tmp");
    fs::write(&result_tmp, text).unwrap_or_else(|error| fail(error.to_string()));
    fs::rename(result_tmp, result_path).unwrap_or_else(|error| fail(error.to_string()));
    eprintln!("PASS column output interval {start}..{end} edges={edges} elapsed={elapsed:.3}s");
}

fn k9_incidence_sample(
    seed_path: &Path,
    rows_path: &Path,
    requested: usize,
    result_path: &Path,
    column_output: Option<&Path>,
    edge_output: Option<&Path>,
) {
    let begun = Instant::now();
    let seed = parse_seed(seed_path).unwrap_or_else(|error| fail(error.to_string()));
    let engine = Engine::new(&seed);
    let mut target = Vec::new();
    for (number, line) in BufReader::new(File::open(rows_path).unwrap_or_else(|error| fail(error.to_string()))).lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        if number == 0 {
            if line != "degree\trow\tcoefficient" {
                fail("row ledger header changed")
            }
            continue;
        }
        let fields: Vec<_> = line.split('\t').collect();
        if fields[0] == "9" {
            target.push(Row12(parse_hex::<12>(fields[1])));
        }
    }
    if target.len() != 49_988 || requested == 0 || requested > target.len() {
        fail("bad K9 target/sample census")
    }
    let target_set: HashSet<_> = target.iter().copied().collect();
    let sample: Vec<_> = (0..requested).map(|index| target[index * target.len() / requested]).collect();
    let mut column_cache = HashMap::new();
    let mut columns = HashSet::new();
    let mut row_incidence_hist = BTreeMap::new();
    let mut incidence_min_hist = BTreeMap::new();
    let mut incidence = 0u64;
    for row in sample {
        let local = incident_columns8(&engine, row, &mut column_cache);
        *row_incidence_hist.entry(local.len()).or_insert(0u64) += 1;
        incidence += local.len() as u64;
        for column in local {
            *incidence_min_hist.entry(column_minimum_degree(&engine, column)).or_insert(0u64) += 1;
            columns.insert(column);
        }
    }
    let mut unique_min_hist = BTreeMap::new();
    for &column in &columns {
        *unique_min_hist.entry(column_minimum_degree(&engine, column)).or_insert(0u64) += 1;
    }
    let mut sorted_columns: Vec<_> = columns.iter().copied().collect();
    sorted_columns.sort_unstable();
    if let Some(path) = column_output {
        let tmp = path.with_extension("tsv.tmp");
        let mut writer = BufWriter::new(File::create(&tmp).unwrap_or_else(|error| fail(error.to_string())));
        writeln!(writer, "column_index\tminimum_degree\tword\tmultiplier").unwrap();
        for (index, column) in sorted_columns.iter().enumerate() {
            let word: String = decode_word(column.word).iter().map(|digit| (b'0' + *digit) as char).collect();
            writeln!(writer, "{index}\t{}\t{word}\t{}", column_minimum_degree(&engine, *column), hex8(&column.multiplier)).unwrap();
        }
        writer.flush().unwrap();
        drop(writer);
        fs::rename(tmp, path).unwrap_or_else(|error| fail(error.to_string()));
    }
    let min9: Vec<_> = sorted_columns.iter().enumerate()
        .filter_map(|(index, column)| (column_minimum_degree(&engine, *column) == 9).then_some((index, *column)))
        .collect();
    let mut row_cache = HashMap::new();
    let mut leading_rows = HashSet::new();
    let mut leading_edges = 0u64;
    let mut edge_writer = edge_output.map(|path| {
        let tmp = path.with_extension("tsv.tmp");
        let mut writer = BufWriter::new(File::create(&tmp).unwrap_or_else(|error| fail(error.to_string())));
        writeln!(writer, "column_index\trow\tmultiplicity").unwrap();
        (path.to_path_buf(), tmp, writer)
    });
    for (column_index, column) in min9 {
        let outputs = column_k9_outputs(&engine, column, &mut row_cache);
        leading_edges += outputs.len() as u64;
        for (&row, &multiplicity) in &outputs {
            if let Some((_, _, writer)) = edge_writer.as_mut() {
                writeln!(writer, "{column_index}\t{}\t{multiplicity}", hex(&row)).unwrap();
            }
            leading_rows.insert(row);
        }
    }
    if let Some((path, tmp, mut writer)) = edge_writer {
        writer.flush().unwrap();
        drop(writer);
        fs::rename(tmp, path).unwrap_or_else(|error| fail(error.to_string()));
    }
    let outside = leading_rows.iter().filter(|row| !target_set.contains(row)).count();
    let hist = |map: &BTreeMap<usize, u64>| {
        map.iter().map(|(key, value)| format!("\"{key}\":{value}")).collect::<Vec<_>>().join(",")
    };
    let hist_u8 = |map: &BTreeMap<u8, u64>| {
        map.iter().map(|(key, value)| format!("\"{key}\":{value}")).collect::<Vec<_>>().join(",")
    };
    let text = format!(
        "{{\n  \"status\": \"PASS_BOUNDED_K9_TARGET_ROOTED_INCIDENCE_GATE\",\n  \"target_K9_rows\": 49988,\n  \"sample_rows\": {requested},\n  \"sample_incidence\": {incidence},\n  \"sample_unique_columns\": {},\n  \"sample_row_incidence_histogram\": {{{}}},\n  \"sample_incidence_by_column_minimum_degree\": {{{}}},\n  \"sample_unique_columns_by_minimum_degree\": {{{}}},\n  \"sample_min9_leading_edges\": {leading_edges},\n  \"sample_min9_leading_row_orbits\": {},\n  \"sample_min9_leading_rows_outside_current_target\": {outside},\n  \"column_canonical_cache\": {},\n  \"row_canonical_cache\": {},\n  \"elapsed_seconds\": {:.6},\n  \"scope\": \"distributed target-rooted incidence gate only; not complete closure, rank, membership, or conjecture result\"\n}}\n",
        columns.len(), hist(&row_incidence_hist), hist_u8(&incidence_min_hist), hist_u8(&unique_min_hist),
        leading_rows.len(), column_cache.len(), row_cache.len(), begun.elapsed().as_secs_f64()
    );
    let tmp = result_path.with_extension("json.tmp");
    fs::write(&tmp, text).unwrap_or_else(|error| fail(error.to_string()));
    fs::rename(tmp, result_path).unwrap_or_else(|error| fail(error.to_string()));
    eprintln!("PASS bounded K9 incidence sample={requested} columns={} elapsed={:.3}s", columns.len(), begun.elapsed().as_secs_f64());
}

fn joint_incidence_sample(
    seed_path: &Path,
    edges_path: &Path,
    existing_columns_path: &Path,
    requested_per_degree: usize,
    result_path: &Path,
    new_column_output: Option<&Path>,
) {
    let begun = Instant::now();
    if requested_per_degree == 0 {
        fail("joint incidence sample must be positive")
    }
    let seed = parse_seed(seed_path).unwrap_or_else(|error| fail(error.to_string()));
    let engine = Engine::new(&seed);
    let existing_columns: HashSet<_> = parse_column_ledger(existing_columns_path).into_iter().collect();
    if existing_columns.is_empty() {
        fail("empty existing column ledger")
    }

    let mut rows_by_degree: Vec<HashSet<Row12>> = (0..10).map(|_| HashSet::new()).collect();
    for (number, line) in BufReader::new(File::open(edges_path).unwrap_or_else(|error| fail(error.to_string()))).lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        if number == 0 {
            if line != "column_index\tdegree\trow\tmultiplicity" {
                fail("joint edge ledger header changed")
            }
            continue;
        }
        let fields: Vec<_> = line.split('\t').collect();
        if fields.len() != 4 {
            fail("joint edge ledger schema changed")
        }
        let degree: usize = fields[1].parse().unwrap_or_else(|_| fail("bad joint edge degree"));
        let multiplicity: u8 = fields[3].parse().unwrap_or_else(|_| fail("bad joint edge multiplicity"));
        if degree > 9 || multiplicity == 0 {
            fail("bad joint edge")
        }
        rows_by_degree[degree].insert(Row12(parse_hex::<12>(fields[2])));
    }

    let mut joint_hist = BTreeMap::new();
    for degree in 0..=9 {
        if !rows_by_degree[degree].is_empty() {
            joint_hist.insert(degree as u8, rows_by_degree[degree].len() as u64);
        }
    }

    let mut selected = Vec::new();
    let mut selected_hist = BTreeMap::new();
    for degree in 0..=9 {
        if rows_by_degree[degree].is_empty() {
            continue;
        }
        let mut rows: Vec<_> = rows_by_degree[degree].drain().collect();
        rows.sort_unstable();
        let count = requested_per_degree.min(rows.len());
        for index in 0..count {
            selected.push((degree as u8, rows[index * rows.len() / count]));
        }
        selected_hist.insert(degree as u8, count as u64);
    }

    let mut column_cache = HashMap::new();
    let mut all_incident = HashSet::new();
    let mut new_columns = HashSet::new();
    let mut incidence_by_row_degree = BTreeMap::new();
    let mut incidence_by_minimum_degree = BTreeMap::new();
    let mut new_by_minimum_degree = BTreeMap::new();
    let mut incidence = 0u64;
    for (row_degree, row) in selected {
        let local = incident_columns8(&engine, row, &mut column_cache);
        incidence += local.len() as u64;
        *incidence_by_row_degree.entry(row_degree).or_insert(0u64) += local.len() as u64;
        for column in local {
            let minimum_degree = column_minimum_degree(&engine, column);
            if minimum_degree > row_degree {
                fail("incident column minimum exceeds row degree")
            }
            *incidence_by_minimum_degree.entry(minimum_degree).or_insert(0u64) += 1;
            all_incident.insert(column);
            if !existing_columns.contains(&column) {
                new_columns.insert(column);
            }
        }
    }
    for &column in &new_columns {
        *new_by_minimum_degree.entry(column_minimum_degree(&engine, column)).or_insert(0u64) += 1;
    }

    let mut sorted_new: Vec<_> = new_columns.iter().copied().collect();
    sorted_new.sort_unstable();
    if let Some(path) = new_column_output {
        let tmp = path.with_extension("tsv.tmp");
        let mut writer = BufWriter::new(File::create(&tmp).unwrap_or_else(|error| fail(error.to_string())));
        writeln!(writer, "column_index\tminimum_degree\tword\tmultiplier").unwrap();
        for (index, column) in sorted_new.iter().enumerate() {
            let word: String = decode_word(column.word).iter().map(|digit| (b'0' + *digit) as char).collect();
            writeln!(writer, "{index}\t{}\t{word}\t{}", column_minimum_degree(&engine, *column), hex8(&column.multiplier)).unwrap();
        }
        writer.flush().unwrap();
        drop(writer);
        fs::rename(tmp, path).unwrap_or_else(|error| fail(error.to_string()));
    }

    let hist = |map: &BTreeMap<u8, u64>| {
        map.iter().map(|(key, value)| format!("\"{key}\":{value}")).collect::<Vec<_>>().join(",")
    };
    let elapsed = begun.elapsed().as_secs_f64();
    let text = format!(
        "{{\n  \"status\": \"PASS_BOUNDED_JOINT_ROW_ROOTED_INCIDENCE_GATE\",\n  \"existing_columns\": {},\n  \"joint_rows_by_degree\": {{{}}},\n  \"requested_per_degree\": {requested_per_degree},\n  \"sampled_rows_by_degree\": {{{}}},\n  \"sample_incidence\": {incidence},\n  \"sample_incidence_by_row_degree\": {{{}}},\n  \"sample_incidence_by_column_minimum_degree\": {{{}}},\n  \"sample_unique_incident_columns\": {},\n  \"sample_unique_new_columns\": {},\n  \"sample_unique_new_columns_by_minimum_degree\": {{{}}},\n  \"column_canonical_cache\": {},\n  \"elapsed_seconds\": {:.6},\n  \"scope\": \"bounded next-closure incidence gate only; no complete closure, kernel, membership, or conjecture result\"\n}}\n",
        existing_columns.len(), hist(&joint_hist), hist(&selected_hist), hist(&incidence_by_row_degree),
        hist(&incidence_by_minimum_degree), all_incident.len(), new_columns.len(),
        hist(&new_by_minimum_degree), column_cache.len(), elapsed,
    );
    let tmp = result_path.with_extension("json.tmp");
    fs::write(&tmp, text).unwrap_or_else(|error| fail(error.to_string()));
    fs::rename(tmp, result_path).unwrap_or_else(|error| fail(error.to_string()));
    eprintln!(
        "PASS bounded joint incidence rows={} new_columns={} elapsed={elapsed:.3}s",
        selected_hist.values().sum::<u64>(), new_columns.len()
    );
}

fn expansion_main(args: &[String]) {
    if args.len() != 4 {
        fail("usage: expand_k9_k12_tail_rows SEED RESULTS.json ROWS.tsv")
    }
    let begun = Instant::now();
    let seed = parse_seed(Path::new(&args[1])).unwrap_or_else(|error| fail(error.to_string()));
    let engine = Engine::new(&seed);
    let workers = std::thread::available_parallelism().map_or(4, |count| count.get()).min(8);
    let source = expand_source(&engine, &seed.terms, workers);
    let target = expand_target(&engine, workers);
    if target.emissions[9..=12] != [171008, 313920, 345600, 216000]
        || source.emissions[9..=12] != [92410, 272332, 350472, 249840]
        || source.firing_terms[9..=12] != [5308, 9238, 7522, 4164]
    {
        fail("literal degree census changed")
    }
    write_outputs(Path::new(&args[2]), Path::new(&args[3]), &target, &source, begun.elapsed().as_secs_f64())
        .unwrap_or_else(|error| fail(error.to_string()));
    eprintln!("PASS exact K9--K12 tail row interface elapsed={:.3}s", begun.elapsed().as_secs_f64());
}

fn main() {
    let args: Vec<_> = env::args().collect();
    if args.get(1).map(String::as_str) == Some("--reduce-initial") {
        if args.len() != 7 {
            fail("usage: expand_k9_k12_tail_rows --reduce-initial SEED ROWS.tsv DEGREE RESULTS.json OUTPUT.tsv")
        }
        let degree: u8 = args[4].parse().unwrap_or_else(|_| fail("bad selected degree"));
        reduce_initial_stage(Path::new(&args[2]), Path::new(&args[3]), degree, Path::new(&args[5]), Path::new(&args[6]));
    } else if args.get(1).map(String::as_str) == Some("--incidence-k9-sample") {
        if args.len() != 6 {
            fail("usage: expand_k9_k12_tail_rows --incidence-k9-sample SEED ROWS.tsv SAMPLE RESULTS.json")
        }
        let sample: usize = args[4].parse().unwrap_or_else(|_| fail("bad sample size"));
        k9_incidence_sample(Path::new(&args[2]), Path::new(&args[3]), sample, Path::new(&args[5]), None, None);
    } else if args.get(1).map(String::as_str) == Some("--incidence-k9-full") {
        if args.len() != 7 {
            fail("usage: expand_k9_k12_tail_rows --incidence-k9-full SEED ROWS.tsv RESULTS.json COLUMNS.tsv EDGES.tsv")
        }
        k9_incidence_sample(
            Path::new(&args[2]), Path::new(&args[3]), 49_988, Path::new(&args[4]),
            Some(Path::new(&args[5])), Some(Path::new(&args[6])),
        );
    } else if args.get(1).map(String::as_str) == Some("--column-output-gate") {
        if args.len() != 6 {
            fail("usage: expand_k9_k12_tail_rows --column-output-gate SEED COLUMNS.tsv SAMPLE RESULTS.json")
        }
        let sample: usize = args[4].parse().unwrap_or_else(|_| fail("bad sample size"));
        column_output_gate(Path::new(&args[2]), Path::new(&args[3]), sample, Path::new(&args[5]), None);
    } else if args.get(1).map(String::as_str) == Some("--column-output-full") {
        if args.len() != 6 {
            fail("usage: expand_k9_k12_tail_rows --column-output-full SEED COLUMNS.tsv RESULTS.json EDGES.tsv")
        }
        column_output_gate(
            Path::new(&args[2]), Path::new(&args[3]), 128_875, Path::new(&args[4]), Some(Path::new(&args[5])),
        );
    } else if args.get(1).map(String::as_str) == Some("--incidence-joint-sample") {
        if args.len() != 7 && args.len() != 8 {
            fail("usage: expand_k9_k12_tail_rows --incidence-joint-sample SEED EDGES.tsv EXISTING_COLUMNS.tsv SAMPLE_PER_DEGREE RESULTS.json [NEW_COLUMNS.tsv]")
        }
        let sample: usize = args[5].parse().unwrap_or_else(|_| fail("bad sample size"));
        joint_incidence_sample(
            Path::new(&args[2]), Path::new(&args[3]), Path::new(&args[4]), sample,
            Path::new(&args[6]), args.get(7).map(|path| Path::new(path)),
        );
    } else if args.get(1).map(String::as_str) == Some("--column-output-interval") {
        if args.len() != 9 {
            fail("usage: expand_k9_k12_tail_rows --column-output-interval SEED COLUMNS.tsv START COUNT INDEX_OFFSET RESULTS.json EDGES.tsv")
        }
        let start: usize = args[4].parse().unwrap_or_else(|_| fail("bad interval start"));
        let count: usize = args[5].parse().unwrap_or_else(|_| fail("bad interval count"));
        let index_offset: usize = args[6].parse().unwrap_or_else(|_| fail("bad interval index offset"));
        column_output_interval(
            Path::new(&args[2]), Path::new(&args[3]), start, count, index_offset,
            Path::new(&args[7]), Path::new(&args[8]),
        );
    } else {
        expansion_main(&args);
    }
}
