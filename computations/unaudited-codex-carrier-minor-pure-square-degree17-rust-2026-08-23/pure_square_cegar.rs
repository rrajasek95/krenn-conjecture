use std::collections::{BTreeMap, BTreeSet, HashMap, HashSet};
use std::fs::File;
use std::io::Write;
use std::time::Instant;

const P: u32 = 32003;
const TARGET_BASE: u32 = 1_000_000_000;
const ROUND_CAP: usize = 10_000;
const RANK_CAP: usize = 100_000;
const COLUMN_CAP: usize = 5_000_000;
const FILL_CAP: usize = 600_000_000;
const DUAL_CAP: usize = 20_000;
const SECONDS_CAP: u64 = 1_150;

type Mon3 = [u16; 3];
type Mon4 = [u16; 4];
type Mon8 = [u16; 8];
type Mon9 = [u16; 9];
type Mon13 = [u16; 13];
type Mon17 = [u16; 17];
type Row = Vec<(u32, u32)>;

fn mod_add(a: u32, b: u32) -> u32 {
    let z = a + b;
    if z >= P { z - P } else { z }
}

fn mod_sub(a: u32, b: u32) -> u32 {
    if a >= b { a - b } else { a + P - b }
}

fn mod_mul(a: u32, b: u32) -> u32 {
    ((a as u64 * b as u64) % P as u64) as u32
}

fn mod_pow(mut a: u32, mut n: u32) -> u32 {
    let mut out = 1u32;
    while n != 0 {
        if n & 1 != 0 { out = mod_mul(out, a); }
        a = mod_mul(a, a);
        n >>= 1;
    }
    out
}

fn edge_index(u: usize, v: usize) -> u16 {
    assert!(u < v);
    let mut index = 0u16;
    for left in 0..8 {
        for right in left + 1..8 {
            if left == u && right == v { return index; }
            index += 1;
        }
    }
    unreachable!()
}

fn cell(u: usize, v: usize, a: u8, b: u8) -> u16 {
    if u < v {
        edge_index(u, v) * 9 + a as u16 * 3 + b as u16
    } else {
        edge_index(v, u) * 9 + b as u16 * 3 + a as u16
    }
}

fn matching_rec(vertices: &[usize], chosen: &mut Vec<(usize, usize)>, out: &mut Vec<Mon4>) {
    if vertices.is_empty() {
        let mut mon = [0u16; 4];
        for (index, &(u, v)) in chosen.iter().enumerate() {
            mon[index] = edge_index(u, v) * 9;
        }
        mon.sort();
        out.push(mon);
        return;
    }
    let u = vertices[0];
    for position in 1..vertices.len() {
        let v = vertices[position];
        let mut rest = Vec::with_capacity(vertices.len() - 2);
        rest.extend_from_slice(&vertices[1..position]);
        rest.extend_from_slice(&vertices[position + 1..]);
        chosen.push((u, v));
        matching_rec(&rest, chosen, out);
        chosen.pop();
    }
}

fn matchings_edges() -> Vec<Vec<(usize, usize)>> {
    fn rec(vertices: &[usize], chosen: &mut Vec<(usize, usize)>, out: &mut Vec<Vec<(usize, usize)>>) {
        if vertices.is_empty() { out.push(chosen.clone()); return; }
        let u = vertices[0];
        for position in 1..vertices.len() {
            let v = vertices[position];
            let mut rest = Vec::with_capacity(vertices.len() - 2);
            rest.extend_from_slice(&vertices[1..position]);
            rest.extend_from_slice(&vertices[position + 1..]);
            chosen.push((u, v));
            rec(&rest, chosen, out);
            chosen.pop();
        }
    }
    let mut out = Vec::new();
    rec(&(0usize..8).collect::<Vec<_>>(), &mut Vec::new(), &mut out);
    assert_eq!(out.len(), 105);
    out
}

fn matching_word(edges: &[(usize, usize)], word: &[u8; 8]) -> Mon4 {
    let mut mon = [0u16; 4];
    for (index, &(u, v)) in edges.iter().enumerate() {
        mon[index] = cell(u, v, word[u], word[v]);
    }
    mon.sort();
    mon
}

fn cofactor_terms(edges_all: &[Vec<(usize, usize)>], word: &[u8; 8], omitted: (usize, usize)) -> Vec<Mon3> {
    let mut out = Vec::new();
    for matching in edges_all {
        if !matching.contains(&omitted) { continue; }
        let mut term = Vec::new();
        for &(u, v) in matching {
            if (u, v) != omitted { term.push(cell(u, v, word[u], word[v])); }
        }
        term.sort();
        out.push([term[0], term[1], term[2]]);
    }
    assert_eq!(out.len(), 15);
    out
}

fn add3x3(a: &Mon3, b: &Mon3, c: &Mon3) -> Mon9 {
    let mut out = [0u16; 9];
    out[..3].copy_from_slice(a);
    out[3..6].copy_from_slice(b);
    out[6..9].copy_from_slice(c);
    out.sort(); out
}

fn add4x4(a: &Mon4, b: &Mon4) -> Mon8 {
    let mut out = [0u16; 8];
    out[..4].copy_from_slice(a); out[4..].copy_from_slice(b);
    out.sort(); out
}

fn add9x8(a: &Mon9, b: &Mon8) -> Mon17 {
    let mut out = [0u16; 17];
    out[..9].copy_from_slice(a); out[9..].copy_from_slice(b);
    out.sort(); out
}

fn add13x4(a: &Mon13, b: &Mon4) -> Mon17 {
    let mut out = [0u16; 17];
    out[..13].copy_from_slice(a); out[13..].copy_from_slice(b);
    out.sort(); out
}

fn quotient_17_4(big: &Mon17, small: &Mon4) -> Option<Mon13> {
    let mut out = [0u16; 13];
    let (mut i, mut j, mut k) = (0usize, 0usize, 0usize);
    while i < 17 {
        if j < 4 && big[i] == small[j] { i += 1; j += 1; }
        else {
            if j < 4 && big[i] > small[j] { return None; }
            if k == 13 { return None; }
            out[k] = big[i]; k += 1; i += 1;
        }
    }
    if j == 4 && k == 13 { Some(out) } else { None }
}

fn quotient_17_8(big: &Mon17, small: &Mon8) -> Option<Mon9> {
    let mut out = [0u16; 9];
    let (mut i, mut j, mut k) = (0usize, 0usize, 0usize);
    while i < 17 {
        if j < 8 && big[i] == small[j] { i += 1; j += 1; }
        else {
            if j < 8 && big[i] > small[j] { return None; }
            if k == 9 { return None; }
            out[k] = big[i]; k += 1; i += 1;
        }
    }
    if j == 8 && k == 9 { Some(out) } else { None }
}

fn build_delta(edges_all: &[Vec<(usize, usize)>]) -> HashMap<Mon9, i32> {
    let cap_pairs = [(0u8, 1u8), (1, 1), (2, 1)];
    let triangle = [(0usize, 1usize), (0, 2), (1, 2)];
    let mut cofactors: Vec<Vec<Vec<Mon3>>> = Vec::new();
    for &(a, b) in &cap_pairs {
        let mut word = [0u8; 8]; word[6] = a; word[7] = b;
        cofactors.push(triangle.iter().map(|&e| cofactor_terms(edges_all, &word, e)).collect());
    }
    let permutations = [
        ([0usize, 1usize, 2usize], 1i32), ([0, 2, 1], -1),
        ([1, 0, 2], -1), ([1, 2, 0], 1),
        ([2, 0, 1], 1), ([2, 1, 0], -1),
    ];
    let mut delta = HashMap::new();
    for (permutation, sign) in permutations {
        for a in &cofactors[0][permutation[0]] {
            for b in &cofactors[1][permutation[1]] {
                for c in &cofactors[2][permutation[2]] {
                    *delta.entry(add3x3(a, b, c)).or_insert(0) += sign;
                }
            }
        }
    }
    delta.retain(|_, value| *value != 0);
    assert_eq!(delta.len(), 6900);
    delta
}

struct Oracle {
    delta: HashMap<Mon9, i32>,
    pure_square: HashMap<Mon8, i32>,
    cache: HashMap<Mon17, i32>,
}

impl Oracle {
    fn coefficient(&mut self, mon: &Mon17) -> i32 {
        if let Some(value) = self.cache.get(mon) { return *value; }
        let mut value = 0i32;
        for (factor, coefficient) in &self.pure_square {
            if let Some(q) = quotient_17_8(mon, factor) {
                value += coefficient * self.delta.get(&q).copied().unwrap_or(0);
            }
        }
        self.cache.insert(*mon, value);
        value
    }
}

struct Columns {
    map: HashMap<Mon17, u32>,
    outside: Vec<Mon17>,
    reserved: Vec<Mon17>,
}

impl Columns {
    fn new(reserved: Vec<Mon17>) -> Self {
        let mut map = HashMap::new();
        for (index, mon) in reserved.iter().enumerate() {
            map.insert(*mon, TARGET_BASE + index as u32);
        }
        Self { map, outside: Vec::new(), reserved }
    }
    fn identify(&mut self, mon: Mon17) -> u32 {
        if let Some(id) = self.map.get(&mon) { return *id; }
        let id = self.outside.len() as u32;
        self.outside.push(mon); self.map.insert(mon, id); id
    }
    fn monomial(&self, id: u32) -> Mon17 {
        if id >= TARGET_BASE { self.reserved[(id - TARGET_BASE) as usize] }
        else { self.outside[id as usize] }
    }
    fn len(&self) -> usize { self.outside.len() + self.reserved.len() }
}

fn normalize_raw(mut entries: Vec<u32>) -> Row {
    entries.sort_unstable();
    let mut row: Row = Vec::new();
    for id in entries {
        if let Some(last) = row.last_mut() {
            if last.0 == id { last.1 = mod_add(last.1, 1); continue; }
        }
        row.push((id, 1));
    }
    row.retain(|&(_, value)| value != 0);
    row
}

fn row_sub_scaled(left: &Row, right: &Row, scale: u32) -> Row {
    let (mut i, mut j) = (0usize, 0usize);
    let mut out = Vec::with_capacity(left.len() + right.len());
    while i < left.len() || j < right.len() {
        if j == right.len() || (i < left.len() && left[i].0 < right[j].0) {
            out.push(left[i]); i += 1;
        } else if i == left.len() || right[j].0 < left[i].0 {
            let value = mod_sub(0, mod_mul(scale, right[j].1));
            if value != 0 { out.push((right[j].0, value)); }
            j += 1;
        } else {
            let value = mod_sub(left[i].1, mod_mul(scale, right[j].1));
            if value != 0 { out.push((left[i].0, value)); }
            i += 1; j += 1;
        }
    }
    out
}

fn insert(mut row: Row, basis: &mut BTreeMap<u32, Row>, fill: &mut usize) -> bool {
    while !row.is_empty() {
        let pivot = row[0].0;
        if let Some(stored) = basis.get(&pivot) {
            row = row_sub_scaled(&row, stored, row[0].1);
        } else {
            let inverse = mod_pow(row[0].1, P - 2);
            for entry in &mut row { entry.1 = mod_mul(entry.1, inverse); }
            *fill += row.len();
            basis.insert(pivot, row);
            return true;
        }
    }
    false
}

fn encoded_row(label: &(u8, Mon13), generators: &[Vec<Mon4>], columns: &mut Columns) -> Row {
    let mut ids = Vec::with_capacity(105);
    for term in &generators[label.0 as usize] {
        ids.push(columns.identify(add13x4(&label.1, term)));
    }
    normalize_raw(ids)
}

fn functional_from_free(basis: &BTreeMap<u32, Row>, free: u32) -> HashMap<u32, u32> {
    let mut dual = HashMap::new(); dual.insert(free, 1);
    for (&pivot, row) in basis.iter().rev() {
        let mut value = 0u32;
        for &(column, coefficient) in row.iter().skip(1) {
            if let Some(d) = dual.get(&column) { value = mod_add(value, mod_mul(coefficient, *d)); }
        }
        if value != 0 { dual.insert(pivot, mod_sub(0, value)); }
    }
    dual
}

fn choose_separator(
    basis: &BTreeMap<u32, Row>, seed_columns: &[u32], columns: &Columns, oracle: &mut Oracle
) -> Option<(HashMap<u32, u32>, u32, usize)> {
    for (seed_index, &free) in seed_columns.iter().enumerate() {
        if basis.contains_key(&free) { continue; }
        let dual = functional_from_free(basis, free);
        let mut pairing = 0u32;
        for (&column, &coefficient) in &dual {
            let target = oracle.coefficient(&columns.monomial(column));
            let residue = ((target % P as i32) + P as i32) as u32 % P;
            pairing = mod_add(pairing, mod_mul(coefficient, residue));
        }
        if pairing != 0 { return Some((dual, pairing, seed_index)); }
    }
    None
}

fn crossing_labels(
    dual: &HashMap<u32, u32>, generators: &[Vec<Mon4>], columns: &Columns
) -> (Vec<(u8, Mon13)>, usize) {
    let mut pairings: HashMap<(u8, Mon13), u32> = HashMap::new();
    let mut candidates = 0usize;
    for (&column, &coefficient) in dual {
        let mon = columns.monomial(column);
        for (word_index, generator) in generators.iter().enumerate() {
            for term in generator {
                if let Some(q) = quotient_17_4(&mon, term) {
                    let key = (word_index as u8, q);
                    let old = pairings.get(&key).copied().unwrap_or(0);
                    pairings.insert(key, mod_add(old, coefficient));
                    candidates += 1;
                }
            }
        }
    }
    let mut live: Vec<_> = pairings.into_iter().filter_map(|(key, value)| if value != 0 { Some(key) } else { None }).collect();
    live.sort();
    (live, candidates)
}

#[derive(Clone)]
struct Round {
    round: usize, rank: usize, columns: usize, fill: usize, dual: usize,
    crossing: usize, independent: usize, seed: usize, pairing: u32, candidates: usize,
}

fn validate_checkpoint(r: &Round) {
    let expected = match r.round {
        1 => Some((4, 471, 420, 1, 4, 0, 1)),
        15 => Some((188, 16159, 86537, 7, 17, 0, 31999)),
        28 => Some((549, 47985, 196313, 33, 137, 2, 8)),
        44 => Some((1770, 127489, 1192963, 44, 175, 1, 6)),
        69 => Some((3258, 244678, 1849651, 119, 468, 4, 31975)),
        90 => Some((3924, 287797, 2711856, 6, 5, 0, 1)),
        103 => Some((4752, 333327, 5882357, 252, 279, 6, 24018)),
        109 => Some((5711, 391585, 12135624, 214, 172, 6, 31961)),
        _ => None,
    };
    if let Some(tuple) = expected {
        assert_eq!((r.rank, r.columns, r.fill, r.dual, r.crossing, r.seed, r.pairing), tuple,
                   "Python-prefix checkpoint mismatch at round {}", r.round);
    }
}

fn write_result(
    status: &str, rounds: &[Round], basis: &BTreeMap<u32, Row>, fill: usize,
    columns: &Columns, dual: &HashMap<u32, u32>, elapsed: u64,
) {
    let mut file = File::create("results_pure_square_cegar_rust_p32003.json").unwrap();
    writeln!(file, "{{").unwrap();
    writeln!(file, "  \"status\": \"{}\",", status).unwrap();
    writeln!(file, "  \"prime\": {},", P).unwrap();
    writeln!(file, "  \"python_prefix_109_validated\": {},", rounds.len() >= 109).unwrap();
    writeln!(file, "  \"rounds_completed\": {},", rounds.len()).unwrap();
    writeln!(file, "  \"final_rank\": {},", basis.len()).unwrap();
    writeln!(file, "  \"final_columns\": {},", columns.len()).unwrap();
    writeln!(file, "  \"final_basis_fill\": {},", fill).unwrap();
    writeln!(file, "  \"final_dual_support\": {},", dual.len()).unwrap();
    writeln!(file, "  \"elapsed_seconds\": {},", elapsed).unwrap();
    writeln!(file, "  \"caps\": {{\"seconds\":{},\"rank\":{},\"columns\":{},\"fill\":{},\"dual\":{}}},",
             SECONDS_CAP, RANK_CAP, COLUMN_CAP, FILL_CAP, DUAL_CAP).unwrap();
    writeln!(file, "  \"rounds\": [").unwrap();
    for (index, r) in rounds.iter().enumerate() {
        writeln!(file, "    {{\"round\":{},\"rank_after\":{},\"columns_after\":{},\"basis_fill_after\":{},\"dual_support\":{},\"crossing_rows\":{},\"independent_rows_added\":{},\"seed_index\":{},\"target_pairing\":{},\"quotient_candidates\":{}}}{}",
                 r.round,r.rank,r.columns,r.fill,r.dual,r.crossing,r.independent,r.seed,r.pairing,r.candidates,
                 if index + 1 == rounds.len() {""} else {","}).unwrap();
    }
    writeln!(file, "  ],").unwrap();
    writeln!(file, "  \"terminal_dual\": [").unwrap();
    let mut dual_entries: Vec<_> = dual.iter().collect(); dual_entries.sort_by_key(|(id, _)| **id);
    for (index, (&id, &coefficient)) in dual_entries.iter().enumerate() {
        let mon = columns.monomial(id);
        write!(file, "    {{\"monomial\":[").unwrap();
        for (j, atom) in mon.iter().enumerate() {
            write!(file, "{}{}", if j==0 {""} else {","}, atom).unwrap();
        }
        writeln!(file, "],\"coefficient\":{}}}{}", coefficient,
                 if index + 1 == dual_entries.len() {""} else {","}).unwrap();
    }
    writeln!(file, "  ]").unwrap();
    writeln!(file, "}}").unwrap();
}

fn main() {
    let started = Instant::now();
    let edges_all = matchings_edges();
    let pure_word = [0u8; 8];
    let pure: Vec<Mon4> = edges_all.iter().map(|m| matching_word(m, &pure_word)).collect();
    let delta = build_delta(&edges_all);
    let mut pure_square: HashMap<Mon8, i32> = HashMap::new();
    for a in &pure { for b in &pure { *pure_square.entry(add4x4(a,b)).or_insert(0) += 1; } }
    assert_eq!(pure_square.len(), 5250);
    let mut oracle = Oracle { delta, pure_square, cache: HashMap::new() };

    let mut delta_keys: Vec<_> = oracle.delta.keys().copied().collect(); delta_keys.sort();
    let mut square_keys: Vec<_> = oracle.pure_square.keys().copied().collect(); square_keys.sort();
    let mut seed_set = BTreeSet::new(); let mut seeds = Vec::new();
    'outer: for a in delta_keys.iter().take(16) {
        for b in square_keys.iter().take(16) {
            let mon = add9x8(a,b);
            if seed_set.insert(mon) && oracle.coefficient(&mon) != 0 {
                seeds.push(mon); if seeds.len() == 64 { break 'outer; }
            }
        }
    }
    assert_eq!(seeds.len(), 64);
    let mut columns = Columns::new(seeds);
    let seed_columns: Vec<u32> = (0..64).map(|i| TARGET_BASE + i).collect();
    let words = [
        [0,0,0,0,0,0,0,1], [0,0,0,0,0,0,1,0],
        [0,0,0,0,0,0,1,1], [0,0,0,0,0,0,2,0],
        [0,0,0,0,0,0,2,1],
    ];
    let generators: Vec<Vec<Mon4>> = words.iter().map(|w| edges_all.iter().map(|m| matching_word(m,w)).collect()).collect();
    let mut basis: BTreeMap<u32,Row> = BTreeMap::new();
    let mut fill = 0usize; let mut seen: HashSet<(u8,Mon13)> = HashSet::new();
    let mut rounds = Vec::new(); let mut terminal_dual = HashMap::new();
    let mut status = "ROUND_CAP".to_string();

    for round_index in 0..ROUND_CAP {
        if started.elapsed().as_secs() >= SECONDS_CAP { status="TIME_CAP".into(); break; }
        if basis.len() >= RANK_CAP || columns.len() >= COLUMN_CAP || fill >= FILL_CAP {
            status="SIZE_CAP".into(); break;
        }
        let chosen = choose_separator(&basis, &seed_columns, &columns, &mut oracle);
        if chosen.is_none() { status="NO_SEPARATOR_ON_64_SEEDS".into(); break; }
        let (dual, pairing, seed) = chosen.unwrap(); terminal_dual = dual.clone();
        if dual.len() >= DUAL_CAP { status="DUAL_CAP".into(); break; }
        let (live, candidates) = crossing_labels(&dual, &generators, &columns);
        let mut new_count = 0usize;
        for label in &live {
            assert!(!seen.contains(label), "crossing row was already in basis span");
            seen.insert(*label);
            let row = encoded_row(label, &generators, &mut columns);
            if insert(row, &mut basis, &mut fill) { new_count += 1; }
        }
        let record = Round { round:round_index+1, rank:basis.len(), columns:columns.len(), fill,
                             dual:dual.len(), crossing:live.len(), independent:new_count,
                             seed, pairing, candidates };
        validate_checkpoint(&record);
        println!("ROUND {} rank={} cols={} fill={} dual={} crossing={} independent={} seed={} pair={} sec={}",
                 record.round,record.rank,record.columns,record.fill,record.dual,record.crossing,
                 record.independent,record.seed,record.pairing,started.elapsed().as_secs());
        rounds.push(record);
        if live.is_empty() { status="SEPARATOR_MOD_P".into(); break; }
    }
    let elapsed = started.elapsed().as_secs();
    write_result(&status,&rounds,&basis,fill,&columns,&terminal_dual,elapsed);
    println!("TERMINAL {} rounds={} rank={} cols={} fill={} dual={} sec={}",
             status,rounds.len(),basis.len(),columns.len(),fill,terminal_dual.len(),elapsed);
}
