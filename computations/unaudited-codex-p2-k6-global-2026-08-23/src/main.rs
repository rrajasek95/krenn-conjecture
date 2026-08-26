//! Exact S6 x S3 orbit closure for the global truncated n=6 P^2 Macaulay map.
//!
//! This performs no field arithmetic.  Starting from every target row, it
//! closes under every literal mixed-source column whose outputs meet
//! K-degree <= cutoff.  Hence lower-filtration kernels are retained.

use std::cell::RefCell;
use std::cmp::Reverse;
use std::collections::{BTreeMap, BinaryHeap, HashMap, HashSet, VecDeque};
use std::env;
use std::fs::File;
use std::hash::{Hash, Hasher};
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::path::Path;
use std::time::Instant;

const N_ACTIONS: usize = 4320;
const N_EDGES: usize = 15;
const N_OFF: usize = 90;
const MORSE_PRIME: i64 = 1_073_741_827;

#[derive(Clone, Copy, Eq, Ord, PartialEq, PartialOrd)]
struct Packed {
    len: u8,
    // A cutoff-six multiplier has at most six off variables; adding one
    // three-edge generator term can transiently reach nine before filtering.
    off: [u8; 9],
    gs: [u32; 3],
}

impl Hash for Packed {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.len.hash(state);
        self.off[..self.len as usize].hash(state);
        self.gs.hash(state);
    }
}

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Column {
    word: u16,
    multiplier: Packed,
}

#[derive(Clone)]
struct Action {
    sites: [u8; 6],
    colours: [u8; 3],
    off_map: [u8; N_OFF],
    edge_map: [u8; N_EDGES],
}

struct Engine {
    cutoff: u8,
    actions: Vec<Action>,
    edges: [(u8, u8); N_EDGES],
    edge_id: [[u8; 6]; 6],
    off_cells: [(u8, u8, u8, u8); N_OFF],
    off_index: [[[[u8; 3]; 3]; 6]; 6],
    matchings: Vec<[(u8, u8); 3]>,
    word_minimum: [u8; 729],
    word_actions: Vec<Vec<u16>>,
    word_canonical: [u16; 729],
    row_cache: RefCell<HashMap<Packed, Packed>>,
    column_cache: RefCell<HashMap<Column, Column>>,
}

struct DfsState {
    assigned: HashMap<Packed, Column>,
    used: HashSet<Column>,
    visiting: HashSet<Packed>,
    order: Vec<(Packed, Column, i32)>,
    calls: usize,
}

#[derive(Clone)]
struct Pivot {
    row: Packed,
    column: Column,
    diagonal: i32,
}

struct Morse<'a> {
    engine: &'a Engine,
    pivots: Vec<Pivot>,
    row_index: HashMap<Packed, u32>,
    pivot_index: HashMap<Column, u32>,
    lower_incident_cache: RefCell<HashMap<u32, Vec<(Column, i32)>>>,
    pivot_tail_cache: RefCell<HashMap<u32, Vec<(Packed, i32)>>>,
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("p2-k6-global: {}", message.as_ref());
    std::process::exit(2);
}

fn permutations<const N: usize>() -> Vec<[u8; N]> {
    fn recurse<const N: usize>(position: usize, current: &mut [u8; N], used: &mut [bool; N], out: &mut Vec<[u8; N]>) {
        if position == N { out.push(*current); return; }
        for value in 0..N {
            if used[value] { continue; }
            used[value] = true;
            current[position] = value as u8;
            recurse(position + 1, current, used, out);
            used[value] = false;
        }
    }
    let mut out = Vec::new();
    recurse(0, &mut [0; N], &mut [false; N], &mut out);
    out
}

fn generate_matchings() -> Vec<[(u8, u8); 3]> {
    fn rec(vertices: &[u8], pairs: &mut Vec<(u8, u8)>, out: &mut Vec<[(u8, u8); 3]>) {
        if vertices.is_empty() {
            out.push([pairs[0], pairs[1], pairs[2]]);
            return;
        }
        let first = vertices[0];
        for index in 1..vertices.len() {
            let second = vertices[index];
            let mut rest = Vec::new();
            rest.extend_from_slice(&vertices[1..index]);
            rest.extend_from_slice(&vertices[index + 1..]);
            pairs.push((first, second));
            rec(&rest, pairs, out);
            pairs.pop();
        }
    }
    let mut answer = Vec::new();
    rec(&[0, 1, 2, 3, 4, 5], &mut Vec::new(), &mut answer);
    if answer.len() != 15 { fail("perfect matching census changed"); }
    answer
}

fn encode_word(word: &[u8; 6]) -> u16 {
    word.iter().fold(0, |code, digit| code * 3 + *digit as u16)
}

fn decode_word(mut code: u16) -> [u8; 6] {
    let mut word = [0; 6];
    for index in (0..6).rev() { word[index] = (code % 3) as u8; code /= 3; }
    word
}

fn decode_graph(mut code: u32) -> [u8; N_EDGES] {
    let mut result = [0; N_EDGES];
    for digit in &mut result { *digit = (code % 3) as u8; code /= 3; }
    result
}

fn encode_graph(digits: &[u8; N_EDGES]) -> u32 {
    let mut code = 0_u32;
    let mut factor = 1_u32;
    for &digit in digits { code += digit as u32 * factor; factor *= 3; }
    code
}

impl Packed {
    fn new(mut off: Vec<u8>, gs: [u32; 3]) -> Self {
        if off.len() > 9 { fail("packed off-degree exceeds transient storage"); }
        off.sort_unstable();
        let mut array = [0; 9];
        array[..off.len()].copy_from_slice(&off);
        Self { len: off.len() as u8, off: array, gs }
    }

    fn off_slice(&self) -> &[u8] { &self.off[..self.len as usize] }
}

impl Engine {
    fn new(cutoff: u8) -> Self {
        if cutoff > 6 { fail("this bounded engine supports cutoff <= 6"); }
        let mut edges = [(0, 0); N_EDGES];
        let mut edge_id = [[0; 6]; 6];
        let mut edge = 0;
        for u in 0..6_u8 {
            for v in u + 1..6_u8 {
                edges[edge] = (u, v);
                edge_id[u as usize][v as usize] = edge as u8;
                edge_id[v as usize][u as usize] = edge as u8;
                edge += 1;
            }
        }
        let mut off_cells = [(0, 0, 0, 0); N_OFF];
        let mut off_index = [[[[255_u8; 3]; 3]; 6]; 6];
        let mut next = 0;
        for &(u, v) in &edges {
            for a in 0..3_u8 {
                for b in 0..3_u8 {
                    if a == b { continue; }
                    off_cells[next] = (u, v, a, b);
                    off_index[u as usize][v as usize][a as usize][b as usize] = next as u8;
                    off_index[v as usize][u as usize][b as usize][a as usize] = next as u8;
                    next += 1;
                }
            }
        }
        if next != N_OFF { fail("off-variable census changed"); }

        let site_perms = permutations::<6>();
        let colour_perms = permutations::<3>();
        let mut actions = Vec::with_capacity(N_ACTIONS);
        for sites in site_perms {
            let mut edge_map = [0; N_EDGES];
            for (index, &(u, v)) in edges.iter().enumerate() {
                edge_map[index] = edge_id[sites[u as usize] as usize][sites[v as usize] as usize];
            }
            for colours in &colour_perms {
                let mut off_map = [0; N_OFF];
                for (index, &(u, v, a, b)) in off_cells.iter().enumerate() {
                    let uu = sites[u as usize];
                    let vv = sites[v as usize];
                    let aa = colours[a as usize];
                    let bb = colours[b as usize];
                    off_map[index] = off_index[uu as usize][vv as usize][aa as usize][bb as usize];
                }
                actions.push(Action { sites, colours: *colours, off_map, edge_map });
            }
        }
        if actions.len() != N_ACTIONS { fail("group order changed"); }
        let matchings = generate_matchings();
        let mut word_minimum = [255; 729];
        let mut word_canonical = [u16::MAX; 729];
        let mut word_actions = vec![Vec::new(); 729];
        for code in 0..729_u16 {
            let word = decode_word(code);
            let mut minimum = 3;
            for matching in &matchings {
                let cross = matching.iter().filter(|&&(u, v)| word[u as usize] != word[v as usize]).count() as u8;
                minimum = minimum.min(cross);
            }
            word_minimum[code as usize] = minimum;
            for (action_index, action) in actions.iter().enumerate() {
                let mut image = [0; 6];
                for site in 0..6 { image[action.sites[site] as usize] = action.colours[word[site] as usize]; }
                let moved = encode_word(&image);
                if moved < word_canonical[code as usize] {
                    word_canonical[code as usize] = moved;
                    word_actions[code as usize].clear();
                    word_actions[code as usize].push(action_index as u16);
                } else if moved == word_canonical[code as usize] {
                    word_actions[code as usize].push(action_index as u16);
                }
            }
        }
        Self {
            cutoff, actions, edges, edge_id, off_cells, off_index, matchings,
            word_minimum, word_actions, word_canonical,
            row_cache: RefCell::new(HashMap::new()),
            column_cache: RefCell::new(HashMap::new()),
        }
    }

    fn transform_graph(&self, code: u32, action: usize) -> u32 {
        let source = decode_graph(code);
        let mut target = [0; N_EDGES];
        for index in 0..N_EDGES { target[self.actions[action].edge_map[index] as usize] = source[index]; }
        encode_graph(&target)
    }

    fn moved_packed(&self, row: Packed, action: usize) -> Packed {
        let map = &self.actions[action].off_map;
        let mut off = [0; 9];
        for (index, &value) in row.off_slice().iter().enumerate() { off[index] = map[value as usize]; }
        off[..row.len as usize].sort_unstable();
        let mut gs = [0; 3];
        for colour in 0..3 {
            gs[self.actions[action].colours[colour] as usize] = self.transform_graph(row.gs[colour], action);
        }
        Packed { len: row.len, off, gs }
    }

    fn canonical_row(&self, row: Packed) -> Packed {
        if let Some(&answer) = self.row_cache.borrow().get(&row) { return answer; }
        let mut best_off: Option<[u8; 9]> = None;
        let mut choices = Vec::new();
        for (index, action) in self.actions.iter().enumerate() {
            let mut moved = [0; 9];
            for (position, &value) in row.off_slice().iter().enumerate() { moved[position] = action.off_map[value as usize]; }
            moved[..row.len as usize].sort_unstable();
            match best_off {
                None => { best_off = Some(moved); choices.push(index); },
                Some(current) if moved < current => { best_off = Some(moved); choices.clear(); choices.push(index); },
                Some(current) if moved == current => choices.push(index),
                _ => {},
            }
        }
        let mut best = None;
        for action in choices {
            let candidate = self.moved_packed(row, action);
            if best.map_or(true, |current| candidate < current) { best = Some(candidate); }
        }
        let answer = best.unwrap();
        let mut cache = self.row_cache.borrow_mut();
        if cache.len() < 1_000_000 { cache.insert(row, answer); }
        answer
    }

    fn canonical_column(&self, column: Column) -> Column {
        if let Some(&answer) = self.column_cache.borrow().get(&column) { return answer; }
        let canonical_word = self.word_canonical[column.word as usize];
        let mut best = None;
        for &action in &self.word_actions[column.word as usize] {
            let candidate = Column { word: canonical_word, multiplier: self.moved_packed(column.multiplier, action as usize) };
            if best.map_or(true, |current| candidate < current) { best = Some(candidate); }
        }
        let answer = best.unwrap();
        let mut cache = self.column_cache.borrow_mut();
        if cache.len() < 1_000_000 { cache.insert(column, answer); }
        answer
    }

    fn add_term(&self, multiplier: Packed, word: &[u8; 6], matching: &[(u8, u8); 3]) -> Packed {
        let mut off = multiplier.off_slice().to_vec();
        let mut digits = multiplier.gs.map(decode_graph);
        for &(u, v) in matching {
            let a = word[u as usize];
            let b = word[v as usize];
            if a == b {
                let edge = self.edge_id[u as usize][v as usize] as usize;
                digits[a as usize][edge] += 1;
                if digits[a as usize][edge] > 2 { fail("diagonal exponent exceeded two"); }
            } else {
                off.push(self.off_index[u as usize][v as usize][a as usize][b as usize]);
            }
        }
        Packed::new(off, digits.map(|value| encode_graph(&value)))
    }

    fn remove_term(&self, row: Packed, word: &[u8; 6], matching: &[(u8, u8); 3]) -> Packed {
        let mut off = row.off_slice().to_vec();
        let mut digits = row.gs.map(decode_graph);
        for &(u, v) in matching {
            let a = word[u as usize];
            let b = word[v as usize];
            if a == b {
                let edge = self.edge_id[u as usize][v as usize] as usize;
                if digits[a as usize][edge] == 0 { fail("remove absent diagonal variable"); }
                digits[a as usize][edge] -= 1;
            } else {
                let variable = self.off_index[u as usize][v as usize][a as usize][b as usize];
                let position = off.iter().position(|&value| value == variable).unwrap_or_else(|| fail("remove absent off variable"));
                off.remove(position);
            }
        }
        Packed::new(off, digits.map(|value| encode_graph(&value)))
    }

    fn incident_columns(&self, row: Packed) -> HashSet<Column> {
        let mut by_edge: [Vec<(u8, u8)>; N_EDGES] = std::array::from_fn(|_| Vec::new());
        for colour in 0..3 {
            let digits = decode_graph(row.gs[colour]);
            for edge in 0..N_EDGES {
                if digits[edge] != 0 { by_edge[edge].push((colour as u8, colour as u8)); }
            }
        }
        for &variable in row.off_slice() {
            let (u, v, a, b) = self.off_cells[variable as usize];
            let edge = self.edge_id[u as usize][v as usize] as usize;
            if !by_edge[edge].contains(&(a, b)) { by_edge[edge].push((a, b)); }
        }
        let mut answer = HashSet::new();
        for matching in &self.matchings {
            let options = matching.map(|(u, v)| &by_edge[self.edge_id[u as usize][v as usize] as usize]);
            if options.iter().any(|items| items.is_empty()) { continue; }
            for &(a0, b0) in options[0] {
                for &(a1, b1) in options[1] {
                    for &(a2, b2) in options[2] {
                        let colours = [(a0, b0), (a1, b1), (a2, b2)];
                        let mut word = [255; 6];
                        for (index, &(u, v)) in matching.iter().enumerate() {
                            word[u as usize] = colours[index].0;
                            word[v as usize] = colours[index].1;
                        }
                        if word.iter().all(|value| *value == word[0]) { continue; }
                        let code = encode_word(&word);
                        let multiplier = self.remove_term(row, &word, matching);
                        let minimum = multiplier.len + self.word_minimum[code as usize];
                        if minimum <= self.cutoff {
                            answer.insert(self.canonical_column(Column { word: code, multiplier }));
                        }
                    }
                }
            }
        }
        answer
    }

    fn outputs_at_most(&self, column: Column, maximum: u8) -> BTreeMap<Packed, i32> {
        if maximum > self.cutoff { fail("requested output above engine cutoff"); }
        let word = decode_word(column.word);
        let mut answer = BTreeMap::new();
        for matching in &self.matchings {
            let row = self.add_term(column.multiplier, &word, matching);
            if row.len <= maximum {
                *answer.entry(self.canonical_row(row)).or_default() += 1;
            }
        }
        answer
    }

    fn truncated_outputs(&self, column: Column) -> BTreeMap<Packed, i32> {
        self.outputs_at_most(column, self.cutoff)
    }
}

fn read_seed(path: &Path) -> BTreeMap<Packed, i64> {
    let input = BufReader::new(File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    let mut rows = BTreeMap::new();
    for (line_number, line) in input.lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if line_number == 0 {
            if fields != ["KRENN_P2_TARGET_V1"] { fail("bad seed magic"); }
            continue;
        }
        if fields.len() != 5 || fields[0] != "ROW" { fail("bad seed row"); }
        let gs = [fields[1].parse().unwrap(), fields[2].parse().unwrap(), fields[3].parse().unwrap()];
        let coefficient = fields[4].parse().unwrap();
        rows.insert(Packed::new(Vec::new(), gs), coefficient);
    }
    if rows.len() != 663 { fail(format!("target seed has {} rows", rows.len())); }
    rows
}

fn prove_dfs(engine: &Engine, row: Packed, state: &mut DfsState) -> bool {
    state.calls += 1;
    if state.calls % 10_000 == 0 {
        eprintln!("dfs calls={} assigned={} visiting={} current_degree={}",
                  state.calls, state.assigned.len(), state.visiting.len(), row.len);
    }
    if state.assigned.contains_key(&row) { return true; }
    if !state.visiting.insert(row) { return false; }
    let mut options = Vec::new();
    for column in engine.incident_columns(row) {
        if state.used.contains(&column) { continue; }
        let outputs = engine.truncated_outputs(column);
        if !outputs.contains_key(&row) { fail("incident column lost its row"); }
        let dependencies: Vec<_> = outputs.keys().filter(|&&other| other != row).copied().collect();
        options.push((dependencies.len(), column, dependencies, outputs[&row]));
    }
    options.sort_by_key(|(count, column, _, _)| (*count, *column));
    for (_, column, dependencies, diagonal) in options {
        if state.used.contains(&column) { continue; }
        if dependencies.into_iter().all(|dependency| prove_dfs(engine, dependency, state)) {
            if state.used.contains(&column) { continue; }
            state.used.insert(column);
            state.assigned.insert(row, column);
            state.order.push((row, column, diagonal));
            state.visiting.remove(&row);
            return true;
        }
    }
    state.visiting.remove(&row);
    false
}

fn write_packed<W: Write>(output: &mut W, value: Packed) -> std::io::Result<()> {
    write!(output, "{}", value.len)?;
    for item in value.off_slice() { write!(output, " {}", item)?; }
    write!(output, " | {} {} {}", value.gs[0], value.gs[1], value.gs[2])
}

fn parse_packed(text: &str) -> Packed {
    let fields: Vec<_> = text.split_whitespace().collect();
    let len: usize = fields.first().unwrap_or_else(|| fail("empty packed value")).parse().unwrap_or_else(|_| fail("bad packed length"));
    if len > 9 || fields.len() != len + 5 || fields[len + 1] != "|" { fail("bad packed field count"); }
    let off = (0..len).map(|index| fields[index + 1].parse().unwrap_or_else(|_| fail("bad off variable"))).collect();
    let gs = [fields[len + 2].parse().unwrap(), fields[len + 3].parse().unwrap(), fields[len + 4].parse().unwrap()];
    Packed::new(off, gs)
}

fn modulo(value: i64) -> i64 {
    let answer = value % MORSE_PRIME;
    if answer < 0 { answer + MORSE_PRIME } else { answer }
}

fn inverse_mod(value: i64) -> i64 {
    let mut base = modulo(value);
    let mut exponent = MORSE_PRIME - 2;
    let mut answer = 1_i64;
    while exponent != 0 {
        if exponent & 1 != 0 { answer = answer * base % MORSE_PRIME; }
        base = base * base % MORSE_PRIME;
        exponent >>= 1;
    }
    answer
}

fn add_mod<K: Eq + Hash + Copy>(map: &mut HashMap<K, i64>, key: K, value: i64) {
    if value == 0 { return; }
    let updated = modulo(map.get(&key).copied().unwrap_or(0) + value);
    if updated == 0 { map.remove(&key); } else { map.insert(key, updated); }
}

fn read_pivots(path: &Path, engine: &Engine) -> Vec<Pivot> {
    let input = BufReader::new(File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    let mut expected = None;
    let mut pivots = Vec::new();
    for (line_number, line) in input.lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        if line_number == 0 {
            let fields: Vec<_> = line.split_whitespace().collect();
            if fields.len() < 4 || fields[0] != "KRENN_P2_TRUNCATED_PEEL_V1" { fail("bad Morse ledger header"); }
            if fields[1] != "3" { fail("Morse transfer requires cutoff-three ledger"); }
            expected = Some(fields.last().unwrap().parse::<usize>().unwrap());
            continue;
        }
        let pieces: Vec<_> = line.split("||").collect();
        if pieces.len() != 3 || !pieces[0].trim_start().starts_with("PIVOT ") { fail("bad Morse pivot record"); }
        let row = parse_packed(pieces[0].trim_start().strip_prefix("PIVOT ").unwrap());
        let column_fields: Vec<_> = pieces[1].split_whitespace().collect();
        let word = column_fields[0].parse().unwrap_or_else(|_| fail("bad Morse column word"));
        let multiplier = parse_packed(&column_fields[1..].join(" "));
        let column = Column { word, multiplier };
        let diagonal = pieces[2].trim().parse().unwrap_or_else(|_| fail("bad Morse diagonal"));
        if engine.canonical_row(row) != row || engine.canonical_column(column) != column { fail("noncanonical Morse pivot"); }
        pivots.push(Pivot { row, column, diagonal });
    }
    if expected != Some(pivots.len()) { fail("Morse pivot count mismatch"); }
    pivots
}

impl<'a> Morse<'a> {
    fn new(engine: &'a Engine, pivots: Vec<Pivot>) -> Self {
        let row_index: HashMap<_, _> = pivots.iter().enumerate().map(|(index, pivot)| (pivot.row, index as u32)).collect();
        let pivot_index: HashMap<_, _> = pivots.iter().enumerate().map(|(index, pivot)| (pivot.column, index as u32)).collect();
        if row_index.len() != pivots.len() || pivot_index.len() != pivots.len() { fail("duplicate Morse row or column"); }
        Self {
            engine, pivots, row_index, pivot_index,
            lower_incident_cache: RefCell::new(HashMap::new()),
            pivot_tail_cache: RefCell::new(HashMap::new()),
        }
    }

    fn minimum_degree(&self, column: Column) -> u8 {
        column.multiplier.len + self.engine.word_minimum[column.word as usize]
    }

    fn lower_outputs(&self, column: Column) -> Vec<(u32, i32)> {
        self.engine.outputs_at_most(column, 3).into_iter().map(|(row, coefficient)| {
            let index = self.row_index.get(&row).copied().unwrap_or_else(|| fail("lower column escaped frozen component"));
            (index, coefficient)
        }).collect()
    }

    fn column_in_component(&self, column: Column) -> bool {
        if self.minimum_degree(column) > 3 { return false; }
        let outputs = self.engine.outputs_at_most(column, 3);
        outputs.keys().any(|row| self.row_index.contains_key(row))
    }

    fn lower_incident(&self, row: u32) -> Vec<(Column, i32)> {
        if let Some(answer) = self.lower_incident_cache.borrow().get(&row) { return answer.clone(); }
        let packed = self.pivots[row as usize].row;
        let mut answer = Vec::new();
        for column in self.engine.incident_columns(packed) {
            if self.minimum_degree(column) > 3 { continue; }
            let coefficient = self.engine.outputs_at_most(column, 3).get(&packed).copied()
                .unwrap_or_else(|| fail("lower incident column lost row"));
            answer.push((column, coefficient));
        }
        answer.sort_by_key(|(column, _)| *column);
        self.lower_incident_cache.borrow_mut().insert(row, answer.clone());
        answer
    }

    fn pivot_tail(&self, pivot: u32) -> Vec<(Packed, i32)> {
        if let Some(answer) = self.pivot_tail_cache.borrow().get(&pivot) { return answer.clone(); }
        let answer: Vec<_> = self.engine.outputs_at_most(self.pivots[pivot as usize].column, 4)
            .into_iter().filter(|(row, _)| row.len == 4).collect();
        self.pivot_tail_cache.borrow_mut().insert(pivot, answer.clone());
        answer
    }

    // Return the degree-four tail of a literal column after cancelling its
    // complete degree<=3 part through the frozen triangular right inverse.
    fn contract_column(&self, column: Column) -> Vec<(Packed, i64)> {
        let outputs = self.engine.outputs_at_most(column, 4);
        let mut residual = HashMap::new();
        let mut pending = BinaryHeap::new();
        let mut tail = HashMap::new();
        for (row, coefficient) in outputs {
            if row.len == 4 {
                add_mod(&mut tail, row, coefficient as i64);
            } else {
                let index = self.row_index.get(&row).copied().unwrap_or_else(|| fail("contracted column escaped lower component"));
                add_mod(&mut residual, index, coefficient as i64);
                pending.push(index);
            }
        }
        while let Some(index) = pending.pop() {
            let value = residual.get(&index).copied().unwrap_or(0);
            if value == 0 { continue; }
            let pivot = &self.pivots[index as usize];
            let scale = modulo(-value * inverse_mod(pivot.diagonal as i64));
            for (other, coefficient) in self.engine.outputs_at_most(pivot.column, 3) {
                let other_index = self.row_index[&other];
                if other_index > index { fail("Morse ledger lost triangularity"); }
                add_mod(&mut residual, other_index, scale * coefficient as i64);
                if other_index < index { pending.push(other_index); }
            }
            if residual.contains_key(&index) { fail("Morse column cancellation failed"); }
            for (row, coefficient) in self.pivot_tail(index) {
                add_mod(&mut tail, row, scale * coefficient as i64);
            }
        }
        if !residual.is_empty() { fail("Morse column has uncancelled lower rows"); }
        let mut answer: Vec<_> = tail.into_iter().collect();
        answer.sort_by_key(|(row, _)| *row);
        answer
    }

    fn contract_target(&self, seed: &BTreeMap<Packed, i64>) -> Vec<(Packed, i64)> {
        // Contract the pseudo-column -target.  Its tail is B*B^{-1}target,
        // so membership of this tail in the critical image is equivalent to
        // lifting the target one filtration step.
        let mut residual = HashMap::new();
        let mut pending = BinaryHeap::new();
        let mut tail = HashMap::new();
        for (&row, &coefficient) in seed {
            let canonical = self.engine.canonical_row(row);
            let index = self.row_index.get(&canonical).copied().unwrap_or_else(|| fail("target row absent from Morse ledger"));
            add_mod(&mut residual, index, -coefficient);
            pending.push(index);
        }
        let mut used = 0_usize;
        while let Some(index) = pending.pop() {
            let value = residual.get(&index).copied().unwrap_or(0);
            if value == 0 { continue; }
            used += 1;
            let pivot = &self.pivots[index as usize];
            let scale = modulo(-value * inverse_mod(pivot.diagonal as i64));
            for (other, coefficient) in self.engine.outputs_at_most(pivot.column, 3) {
                let other_index = self.row_index[&other];
                if other_index > index { fail("target contraction lost triangularity"); }
                add_mod(&mut residual, other_index, scale * coefficient as i64);
                if other_index < index { pending.push(other_index); }
            }
            if residual.contains_key(&index) { fail("target contraction failed"); }
            for (row, coefficient) in self.pivot_tail(index) {
                add_mod(&mut tail, row, scale * coefficient as i64);
            }
        }
        if !residual.is_empty() { fail("target has uncancelled lower rows"); }
        eprintln!("morse target contraction pivots={} critical_support={}", used, tail.len());
        let mut answer: Vec<_> = tail.into_iter().collect();
        answer.sort_by_key(|(row, _)| *row);
        answer
    }

    // Compute one exact row of the Schur operator without materializing all
    // 3.88 million free lower columns.  The forward solve qB=A4(row,B)
    // enumerates precisely the lower columns whose transferred tails meet row.
    fn critical_incident(&self, row: Packed) -> Vec<(Column, i64)> {
        if row.len != 4 { fail("critical incidence requested outside degree four"); }
        let mut coefficients = HashMap::new();
        let mut numerators = HashMap::new();
        let mut pending = BinaryHeap::new();
        for column in self.engine.incident_columns(row) {
            let raw = self.engine.outputs_at_most(column, 4).get(&row).copied()
                .unwrap_or_else(|| fail("critical incident column lost row"));
            let minimum = self.minimum_degree(column);
            if minimum == 4 {
                add_mod(&mut coefficients, column, raw as i64);
            } else if minimum <= 3 && self.column_in_component(column) {
                if let Some(&index) = self.pivot_index.get(&column) {
                    add_mod(&mut numerators, index, raw as i64);
                    pending.push(Reverse(index));
                } else {
                    add_mod(&mut coefficients, column, raw as i64);
                }
            }
        }
        let mut quotient = HashMap::new();
        while let Some(Reverse(index)) = pending.pop() {
            if quotient.contains_key(&index) { continue; }
            let numerator = numerators.get(&index).copied().unwrap_or(0);
            let value = modulo(numerator * inverse_mod(self.pivots[index as usize].diagonal as i64));
            quotient.insert(index, value);
            if value == 0 { continue; }
            for (column, coefficient) in self.lower_incident(index) {
                if let Some(&other) = self.pivot_index.get(&column) {
                    if other == index { continue; }
                    if other < index { fail("transpose Morse solve lost triangularity"); }
                    add_mod(&mut numerators, other, -value * coefficient as i64);
                    pending.push(Reverse(other));
                } else {
                    add_mod(&mut coefficients, column, -value * coefficient as i64);
                }
            }
        }
        let mut answer: Vec<_> = coefficients.into_iter().filter(|(_, value)| *value != 0).collect();
        answer.sort_by_key(|(column, _)| *column);
        answer
    }
}

fn verify_certificate(engine: &Engine, seed: &BTreeMap<Packed, i64>, path: &Path, started: Instant) {
    let input = BufReader::new(File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    let mut seen = HashSet::new();
    let mut expected = None;
    let mut pivots = 0_usize;
    for (line_number, line) in input.lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        if line_number == 0 {
            let fields: Vec<_> = line.split_whitespace().collect();
            if fields.len() < 4 || !fields[0].starts_with("KRENN_P2_TRUNCATED_") { fail("bad certificate header"); }
            let certificate_cutoff: u8 = fields[1].parse().unwrap();
            if certificate_cutoff != engine.cutoff { fail("certificate cutoff mismatch"); }
            expected = Some(fields.last().unwrap().parse::<usize>().unwrap());
            continue;
        }
        let pieces: Vec<_> = line.split("||").collect();
        if pieces.len() != 3 || !pieces[0].trim_start().starts_with("PIVOT ") { fail("bad pivot record"); }
        let row = parse_packed(pieces[0].trim_start().strip_prefix("PIVOT ").unwrap());
        let column_fields: Vec<_> = pieces[1].split_whitespace().collect();
        if column_fields.is_empty() { fail("missing column word"); }
        let word = column_fields[0].parse().unwrap_or_else(|_| fail("bad column word"));
        let multiplier = parse_packed(&column_fields[1..].join(" "));
        let column = Column { word, multiplier };
        let diagonal: i32 = pieces[2].trim().parse().unwrap_or_else(|_| fail("bad diagonal"));
        if engine.canonical_row(row) != row || engine.canonical_column(column) != column { fail("noncanonical ledger entry"); }
        let outputs = engine.truncated_outputs(column);
        if outputs.get(&row).copied() != Some(diagonal) || diagonal == 0 { fail("pivot diagonal changed"); }
        if !outputs.keys().all(|other| *other == row || seen.contains(other)) { fail("certificate is not triangular"); }
        if !seen.insert(row) { fail("duplicate pivot row"); }
        pivots += 1;
        if pivots % 100_000 == 0 { eprintln!("verified pivots={pivots} elapsed={:.1}s", started.elapsed().as_secs_f64()); }
    }
    if expected != Some(pivots) { fail("certificate pivot count mismatch"); }
    for row in seed.keys().map(|row| engine.canonical_row(*row)) {
        if !seen.contains(&row) { fail("certificate omits a target row"); }
    }
    eprintln!("VERIFY_SUCCESS pivots={} target_rows={} elapsed={:.1}s", pivots, seed.len(), started.elapsed().as_secs_f64());
}

fn write_morse_packet(
    path: &Path,
    status: &str,
    target: &[(Packed, i64)],
    rows: &HashSet<Packed>,
    columns: &HashMap<Column, Vec<(Packed, i64)>>,
    processed: usize,
    frontier: &VecDeque<Packed>,
    peel: Option<(usize, usize, usize, Vec<(Packed, Column, i64)>, HashSet<Packed>)>,
    elapsed: f64,
) {
    let mut output = BufWriter::new(File::create(path).unwrap_or_else(|error| fail(error.to_string())));
    writeln!(output, "KRENN_P2_MORSE4_V1").unwrap();
    writeln!(output, "PRIME {}", MORSE_PRIME).unwrap();
    writeln!(output, "STATUS {}", status).unwrap();
    writeln!(output, "COUNTS target_support={} rows={} columns={} processed={} frontier={} elapsed_seconds={:.3}",
             target.len(), rows.len(), columns.len(), processed, frontier.len(), elapsed).unwrap();
    for &(row, coefficient) in target {
        write!(output, "TARGET ").unwrap();
        write_packed(&mut output, row).unwrap();
        writeln!(output, " || {}", coefficient).unwrap();
    }
    if let Some((pivot_count, core_rows, core_columns, ledger, active)) = peel {
        writeln!(output, "PEEL pivots={} core_rows={} core_columns={}", pivot_count, core_rows, core_columns).unwrap();
        for &(row, column, diagonal) in &ledger {
            write!(output, "CPIVOT ").unwrap();
            write_packed(&mut output, row).unwrap();
            write!(output, " || {} ", column.word).unwrap();
            write_packed(&mut output, column.multiplier).unwrap();
            writeln!(output, " || {}", diagonal).unwrap();
        }
        let mut core_target: Vec<_> = target.iter().filter(|(row, coefficient)| *coefficient != 0 && active.contains(row)).copied().collect();
        core_target.sort_by_key(|(row, _)| *row);
        for (row, coefficient) in core_target {
            write!(output, "CORE_TARGET ").unwrap();
            write_packed(&mut output, row).unwrap();
            writeln!(output, " || {}", coefficient).unwrap();
        }
    } else {
        for row in frontier.iter().take(500) {
            write!(output, "FRONTIER ").unwrap();
            write_packed(&mut output, *row).unwrap();
            writeln!(output).unwrap();
        }
    }
    output.flush().unwrap();
}

fn morse4(engine: &Engine, seed: &BTreeMap<Packed, i64>, ledger_path: &Path, packet_path: &Path, started: Instant) {
    if engine.cutoff != 4 { fail("Morse transfer must run with cutoff four engine"); }
    let pivots = read_pivots(ledger_path, engine);
    if pivots.len() != 543_640 { fail("unexpected cutoff-three full pivot count"); }
    eprintln!("morse ledger loaded pivots={} elapsed={:.1}s", pivots.len(), started.elapsed().as_secs_f64());
    let morse = Morse::new(engine, pivots);
    let target = morse.contract_target(seed);
    let mut rows: HashSet<Packed> = target.iter().filter(|(_, coefficient)| *coefficient != 0).map(|(row, _)| *row).collect();
    let mut frontier: VecDeque<Packed> = rows.iter().copied().collect();
    let mut columns: HashMap<Column, Vec<(Packed, i64)>> = HashMap::new();
    let mut processed = 0_usize;
    let mut timed_out = false;
    let mut checked = 0_usize;
    while let Some(row) = frontier.pop_front() {
        if started.elapsed().as_secs_f64() >= 270.0 {
            frontier.push_front(row);
            timed_out = true;
            break;
        }
        let incident = morse.critical_incident(row);
        for (column, expected) in incident {
            if columns.contains_key(&column) { continue; }
            let outputs = morse.contract_column(column);
            if checked < 100 {
                let actual = outputs.iter().find(|(candidate, _)| *candidate == row).map(|(_, coefficient)| *coefficient).unwrap_or(0);
                if actual != expected { fail(format!("Schur row/column cross-check failed: expected {expected}, got {actual}")); }
                checked += 1;
            }
            for &(output, coefficient) in &outputs {
                if coefficient != 0 && rows.insert(output) { frontier.push_back(output); }
            }
            columns.insert(column, outputs);
        }
        processed += 1;
        if processed % 10 == 0 {
            eprintln!("morse closure processed={} rows={} columns={} frontier={} caches lower={} tails={} elapsed={:.1}s",
                      processed, rows.len(), columns.len(), frontier.len(),
                      morse.lower_incident_cache.borrow().len(), morse.pivot_tail_cache.borrow().len(),
                      started.elapsed().as_secs_f64());
        }
    }
    if timed_out {
        write_morse_packet(packet_path, "UNRESOLVED_TIMEOUT", &target, &rows, &columns, processed, &frontier, None, started.elapsed().as_secs_f64());
        eprintln!("MORSE4_UNRESOLVED rows={} columns={} processed={} frontier={} packet={} elapsed={:.1}s",
                  rows.len(), columns.len(), processed, frontier.len(), packet_path.display(), started.elapsed().as_secs_f64());
        return;
    }
    eprintln!("morse closure complete rows={} columns={} elapsed={:.1}s", rows.len(), columns.len(), started.elapsed().as_secs_f64());
    let mut ordered_rows: Vec<_> = rows.iter().copied().collect();
    ordered_rows.sort();
    let row_index: HashMap<_, _> = ordered_rows.iter().enumerate().map(|(index, row)| (*row, index as u32)).collect();
    let mut ordered_columns: Vec<_> = columns.keys().copied().collect();
    ordered_columns.sort();
    let mut column_rows = Vec::with_capacity(ordered_columns.len());
    let mut row_degree = vec![0_u32; ordered_rows.len()];
    for column in &ordered_columns {
        let entries: Vec<_> = columns[column].iter().filter(|(_, coefficient)| *coefficient != 0).map(|(row, _)| row_index[row]).collect();
        for &row in &entries { row_degree[row as usize] += 1; }
        column_rows.push(entries);
    }
    let mut offsets = vec![0_usize; ordered_rows.len() + 1];
    for index in 0..ordered_rows.len() { offsets[index + 1] = offsets[index] + row_degree[index] as usize; }
    let mut row_columns = vec![0_u32; offsets[ordered_rows.len()]];
    let mut cursor = offsets[..ordered_rows.len()].to_vec();
    for (column, entries) in column_rows.iter().enumerate() {
        for &row in entries {
            row_columns[cursor[row as usize]] = column as u32;
            cursor[row as usize] += 1;
        }
    }
    let mut active_rows = vec![true; ordered_rows.len()];
    let mut active_degree: Vec<u32> = column_rows.iter().map(|entries| entries.len() as u32).collect();
    let mut queue = VecDeque::new();
    for (column, &degree) in active_degree.iter().enumerate() { if degree == 1 { queue.push_back(column as u32); } }
    let mut critical_ledger = Vec::new();
    while let Some(column_index) = queue.pop_front() {
        if active_degree[column_index as usize] != 1 { continue; }
        let row_index_value = column_rows[column_index as usize].iter().find(|&&row| active_rows[row as usize]).copied()
            .unwrap_or_else(|| fail("critical singleton lost row"));
        active_rows[row_index_value as usize] = false;
        let row = ordered_rows[row_index_value as usize];
        let column = ordered_columns[column_index as usize];
        let diagonal = columns[&column].iter().find(|(candidate, _)| *candidate == row).unwrap().1;
        critical_ledger.push((row, column, diagonal));
        for &touched in &row_columns[offsets[row_index_value as usize]..offsets[row_index_value as usize + 1]] {
            active_degree[touched as usize] -= 1;
            if active_degree[touched as usize] == 1 { queue.push_back(touched); }
        }
    }
    let active: HashSet<_> = ordered_rows.iter().enumerate().filter(|(index, _)| active_rows[*index]).map(|(_, row)| *row).collect();
    let core_columns = active_degree.iter().filter(|&&degree| degree != 0).count();
    let core_target = target.iter().filter(|(row, coefficient)| *coefficient != 0 && active.contains(row)).count();
    let status = if core_target == 0 { "MEMBER_MOD_P" } else { "DEAD_CORE_MOD_P" };
    write_morse_packet(packet_path, status, &target, &rows, &columns, processed, &frontier,
                       Some((critical_ledger.len(), active.len(), core_columns, critical_ledger, active)),
                       started.elapsed().as_secs_f64());
    eprintln!("MORSE4_{} rows={} columns={} core_rows={} core_columns={} core_target={} packet={} elapsed={:.1}s",
              status, rows.len(), columns.len(), active_rows.iter().filter(|&&value| value).count(), core_columns,
              core_target, packet_path.display(), started.elapsed().as_secs_f64());
}

fn dfs_certificate(engine: &Engine, seed: &BTreeMap<Packed, i64>, output_path: &Path, started: Instant) {
    let mut state = DfsState {
        assigned: HashMap::new(), used: HashSet::new(), visiting: HashSet::new(),
        order: Vec::new(), calls: 0,
    };
    let targets: Vec<_> = seed.keys().map(|row| engine.canonical_row(*row)).collect();
    for (index, row) in targets.into_iter().enumerate() {
        if !prove_dfs(engine, row, &mut state) {
            eprintln!("DFS_FAILURE target={}/{} row_len={} assigned={} calls={} elapsed={:.1}s",
                      index + 1, seed.len(), row.len, state.assigned.len(), state.calls,
                      started.elapsed().as_secs_f64());
            std::process::exit(3);
        }
        if (index + 1) % 25 == 0 {
            eprintln!("dfs targets={}/{} pivots={} calls={} elapsed={:.1}s",
                      index + 1, seed.len(), state.order.len(), state.calls,
                      started.elapsed().as_secs_f64());
        }
    }
    let mut seen = HashSet::new();
    for &(row, column, diagonal) in &state.order {
        if diagonal == 0 || !seen.insert(row) { fail("bad DFS pivot ledger"); }
        let outputs = engine.truncated_outputs(column);
        if outputs[&row] != diagonal { fail("DFS diagonal replay changed"); }
        if !outputs.keys().all(|other| *other == row || seen.contains(other)) {
            fail("DFS order is not triangular");
        }
    }
    let mut output = BufWriter::new(File::create(output_path).unwrap_or_else(|error| fail(error.to_string())));
    writeln!(output, "KRENN_P2_TRUNCATED_DFS_V1 {} {} {}", engine.cutoff, seed.len(), state.order.len()).unwrap();
    for (row, column, diagonal) in &state.order {
        write!(output, "PIVOT ").unwrap();
        write_packed(&mut output, *row).unwrap();
        write!(output, " || {} ", column.word).unwrap();
        write_packed(&mut output, column.multiplier).unwrap();
        writeln!(output, " || {}", diagonal).unwrap();
    }
    output.flush().unwrap();
    eprintln!("DFS_SUCCESS pivots={} calls={} certificate={} bytes={} elapsed={:.1}s",
              state.order.len(), state.calls, output_path.display(),
              output_path.metadata().unwrap().len(), started.elapsed().as_secs_f64());
}

fn main() {
    let arguments: Vec<_> = env::args().collect();
    if arguments.len() < 3 || arguments.len() > 6 {
        fail("usage: p2-k6-global SEED CUTOFF [--peel [CERTIFICATE] | --dfs CERTIFICATE | --verify CERTIFICATE | --morse4 LEDGER PACKET]");
    }
    let cutoff: u8 = arguments[2].parse().unwrap_or_else(|_| fail("bad cutoff"));
    let want_peel = arguments.get(3).map(String::as_str) == Some("--peel");
    let seed = read_seed(Path::new(&arguments[1]));
    let started = Instant::now();
    let engine = Engine::new(cutoff);
    if arguments.get(3).map(String::as_str) == Some("--morse4") {
        if arguments.len() != 6 { fail("--morse4 requires a cutoff-three ledger and output packet"); }
        morse4(&engine, &seed, Path::new(&arguments[4]), Path::new(&arguments[5]), started);
        return;
    }
    if arguments.get(3).map(String::as_str) == Some("--verify") {
        if arguments.len() != 5 { fail("--verify requires a certificate path"); }
        verify_certificate(&engine, &seed, Path::new(&arguments[4]), started);
        return;
    }
    if arguments.get(3).map(String::as_str) == Some("--dfs") {
        if arguments.len() != 5 { fail("--dfs requires a certificate path"); }
        let output = arguments[4].clone();
        std::thread::Builder::new().name("p2-dfs".into())
            .stack_size(1024 * 1024 * 1024)
            .spawn(move || dfs_certificate(&engine, &seed, Path::new(&output), started))
            .unwrap_or_else(|error| fail(error.to_string())).join()
            .unwrap_or_else(|_| fail("DFS worker panicked"));
        return;
    }
    let mut rows: HashSet<Packed> = seed.keys().map(|row| engine.canonical_row(*row)).collect();
    let mut frontier = rows.clone();
    let mut columns = HashSet::new();
    let mut stored_outputs: HashMap<Column, Vec<(Packed, i32)>> = HashMap::new();
    let mut layers = Vec::new();
    let mut total_nnz = 0_usize;
    while !frontier.is_empty() {
        let before = columns.len();
        let mut new_rows = HashSet::new();
        for (index, row) in frontier.into_iter().enumerate() {
            for column in engine.incident_columns(row) {
                if !columns.insert(column) { continue; }
                let outputs = engine.truncated_outputs(column);
                total_nnz += outputs.len();
                for output in outputs.keys() {
                    if rows.insert(*output) { new_rows.insert(*output); }
                }
                if want_peel { stored_outputs.insert(column, outputs.into_iter().collect()); }
            }
            if (index + 1) % 25_000 == 0 {
                eprintln!("frontier {}/? totals rows={} cols={} elapsed={:.1}s",
                          index + 1, rows.len(), columns.len(), started.elapsed().as_secs_f64());
            }
        }
        layers.push((new_rows.len(), columns.len() - before));
        eprintln!("layer {}: +{} rows +{} cols totals {}/{} nnz={} elapsed={:.1}s",
                  layers.len(), new_rows.len(), columns.len() - before,
                  rows.len(), columns.len(), total_nnz, started.elapsed().as_secs_f64());
        frontier = new_rows;
    }
    let mut row_degree = BTreeMap::new();
    for row in &rows { *row_degree.entry(row.len).or_insert(0_usize) += 1; }
    let mut column_degree = BTreeMap::new();
    for column in &columns {
        let degree = column.multiplier.len + engine.word_minimum[column.word as usize];
        *column_degree.entry(degree).or_insert(0_usize) += 1;
    }
    let mut peel = None;
    if want_peel {
        let ordered_rows: Vec<_> = rows.iter().copied().collect();
        let row_index: HashMap<_, _> = ordered_rows.iter().enumerate().map(|(index, row)| (*row, index as u32)).collect();
        let ordered_columns: Vec<_> = columns.iter().copied().collect();
        let mut column_rows: Vec<Vec<u32>> = Vec::with_capacity(columns.len());
        let mut row_degrees = vec![0_u32; rows.len()];
        for (index, column) in ordered_columns.iter().enumerate() {
            let entries: Vec<_> = stored_outputs[column].iter().map(|(row, _)| row_index[row]).collect();
            for &row in &entries { row_degrees[row as usize] += 1; }
            column_rows.push(entries);
            if (index + 1) % 500_000 == 0 { eprintln!("matrix replay columns={}/{}", index + 1, columns.len()); }
        }
        let mut offsets = vec![0_usize; rows.len() + 1];
        for index in 0..rows.len() { offsets[index + 1] = offsets[index] + row_degrees[index] as usize; }
        let mut row_columns = vec![0_u32; offsets[rows.len()]];
        let mut cursor = offsets[..rows.len()].to_vec();
        for (column, entries) in column_rows.iter().enumerate() {
            for &row in entries {
                row_columns[cursor[row as usize]] = column as u32;
                cursor[row as usize] += 1;
            }
        }
        let mut active_rows = vec![true; rows.len()];
        let mut active_degree: Vec<u8> = column_rows.iter().map(|entries| entries.len() as u8).collect();
        let mut queue = VecDeque::new();
        for (column, &degree) in active_degree.iter().enumerate() {
            if degree == 1 { queue.push_back(column as u32); }
        }
        let initial_singletons = queue.len();
        let mut pivots = 0_usize;
        let mut pivot_ledger = Vec::new();
        while let Some(column) = queue.pop_front() {
            if active_degree[column as usize] != 1 { continue; }
            let row = column_rows[column as usize].iter().find(|&&row| active_rows[row as usize]).copied().unwrap_or_else(|| fail("singleton lost active row"));
            active_rows[row as usize] = false;
            pivots += 1;
            let pivot_row = ordered_rows[row as usize];
            let pivot_column = ordered_columns[column as usize];
            let diagonal = stored_outputs[&pivot_column].iter()
                .find(|(candidate, _)| *candidate == pivot_row).unwrap().1;
            pivot_ledger.push((pivot_row, pivot_column, diagonal));
            for &touched in &row_columns[offsets[row as usize]..offsets[row as usize + 1]] {
                let degree = &mut active_degree[touched as usize];
                if *degree == 0 { fail("active row met empty column"); }
                *degree -= 1;
                if *degree == 1 { queue.push_back(touched); }
            }
        }
        let core_rows = active_rows.iter().filter(|&&active| active).count();
        let core_columns = active_degree.iter().filter(|&&degree| degree != 0).count();
        let core_nnz: usize = active_degree.iter().map(|&degree| degree as usize).sum();
        eprintln!("peel initial_singletons={} pivots={} core={}/{} nnz={} elapsed={:.1}s",
                  initial_singletons, pivots, core_rows, core_columns, core_nnz, started.elapsed().as_secs_f64());
        if let Some(path) = arguments.get(4) {
            let mut output = BufWriter::new(File::create(path).unwrap_or_else(|error| fail(error.to_string())));
            writeln!(output, "KRENN_P2_TRUNCATED_PEEL_V1 {} {} {} {}", cutoff, seed.len(), rows.len(), pivot_ledger.len()).unwrap();
            for (row, column, diagonal) in &pivot_ledger {
                write!(output, "PIVOT ").unwrap();
                write_packed(&mut output, *row).unwrap();
                write!(output, " || {} ", column.word).unwrap();
                write_packed(&mut output, column.multiplier).unwrap();
                writeln!(output, " || {}", diagonal).unwrap();
            }
            output.flush().unwrap();
            eprintln!("peel certificate={} bytes={}", path, Path::new(path).metadata().unwrap().len());
        }
        peel = Some((initial_singletons, pivots, core_rows, core_columns, core_nnz));
    }
    println!("{{\"cutoff\":{},\"target_rows\":{},\"rows\":{},\"columns\":{},\"nnz\":{},\"row_degree\":{:?},\"column_min_degree\":{:?},\"layers\":{:?},\"peel\":{:?},\"elapsed_seconds\":{:.3}}}",
             cutoff, seed.len(), rows.len(), columns.len(), total_nnz,
             row_degree, column_degree, layers, peel, started.elapsed().as_secs_f64());
}
