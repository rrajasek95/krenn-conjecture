//! Incremental sparse column-echelon CEGAR for the chart-26 degree-nine dual.
//!
//! Unlike the earlier row solver, adding a crossing never rebuilds the old
//! matrix.  Each source column is reduced once in the degree-nine top-row
//! space, carrying its lower lambda8 boundary as one augmented scalar.

use std::collections::{BTreeMap, BTreeSet, HashMap};
use std::env;
use std::fs::{self, File};
use std::hash::{Hash, Hasher};
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::path::Path;
use std::thread;
use std::time::{Duration, Instant};

const N: usize = 8;
const Q: usize = 3;
const N_EDGES: usize = 28;
const N_COORDS: usize = 252;
const N_WORDS: usize = 6561;
const DEGREE: usize = 9;
const GENERATOR_DEGREE: usize = 4;
const MULTIPLIER_DEGREE: usize = DEGREE - GENERATOR_DEGREE;
const PRIME: u64 = 1_073_741_827;
const SUPPORT_IDS: [u8; 12] = [0, 22, 62, 89, 103, 125, 130, 135, 162, 233, 238, 243];

const SITE_ACTIONS: [[u8; N]; 4] = [
    [0, 1, 2, 3, 4, 5, 6, 7],
    [0, 1, 5, 7, 6, 2, 4, 3],
    [1, 0, 2, 4, 3, 5, 7, 6],
    [1, 0, 5, 6, 7, 2, 3, 4],
];
const COLOUR_ACTIONS: [[u8; Q]; 4] = [
    [0, 1, 2], [0, 2, 1], [0, 2, 1], [0, 1, 2],
];

#[derive(Clone, Copy, Eq, Ord, PartialEq, PartialOrd)]
struct Mono { len: u8, ids: [u8; DEGREE] }

impl Hash for Mono {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.len.hash(state);
        self.slice().hash(state);
    }
}

impl Mono {
    #[inline]
    fn new(mut ids: Vec<u8>) -> Self {
        if ids.len() > DEGREE { fail("monomial exceeds homogeneous degree nine"); }
        ids.sort_unstable();
        let mut packed = [0; DEGREE];
        packed[..ids.len()].copy_from_slice(&ids);
        Self { len: ids.len() as u8, ids: packed }
    }
    #[inline]
    fn slice(&self) -> &[u8] { &self.ids[..self.len as usize] }
    #[inline]
    fn concat(self, other: Mono) -> Self {
        let total = self.len as usize + other.len as usize;
        if total > DEGREE { fail("monomial exceeds homogeneous degree nine"); }
        let mut ids = [0u8; DEGREE];
        let (mut left,mut right,mut out) = (0usize,0usize,0usize);
        while left < self.len as usize && right < other.len as usize {
            if self.ids[left] <= other.ids[right] {
                ids[out]=self.ids[left]; left+=1;
            } else {
                ids[out]=other.ids[right]; right+=1;
            }
            out+=1;
        }
        while left < self.len as usize { ids[out]=self.ids[left]; left+=1; out+=1; }
        while right < other.len as usize { ids[out]=other.ids[right]; right+=1; out+=1; }
        Self {len: total as u8, ids}
    }
    #[inline]
    fn quotient(self, divisor: Mono) -> Option<Self> {
        let mut ids = [0u8; DEGREE];
        let (mut source,mut divide,mut out)=(0usize,0usize,0usize);
        while source < self.len as usize {
            if divide < divisor.len as usize && self.ids[source] == divisor.ids[divide] {
                source+=1; divide+=1;
            } else {
                if divide < divisor.len as usize && divisor.ids[divide] < self.ids[source] { return None; }
                ids[out]=self.ids[source]; source+=1; out+=1;
            }
        }
        if divide != divisor.len as usize { return None; }
        Some(Self {len: out as u8, ids})
    }
}

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Column { word: u16, multiplier: Mono }

#[derive(Clone)]
struct Action { var_map: [u8; N_COORDS], word_map: [u16; N_WORDS] }

struct Engine {
    actions: Vec<Action>,
    polynomials: Vec<Vec<(Mono, i32)>>,
    term_index: HashMap<Mono, Vec<u16>>,
    row_cache: HashMap<Mono, Mono>,
    column_cache: HashMap<Column, Column>,
    incident_cache: HashMap<Mono, Vec<Column>>,
    output_cache: HashMap<Column, Vec<(Mono, i32)>>,
}

struct BasisRecord { vector: Vec<(Mono, u64)>, rhs: u64 }

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("degree9-incremental: {}", message.as_ref());
    std::process::exit(2)
}

fn encode_word(word: &[u8; N]) -> u16 {
    word.iter().fold(0, |code, digit| code * 3 + *digit as u16)
}

fn decode_word(mut code: u16) -> [u8; N] {
    let mut word = [0; N];
    for index in (0..N).rev() { word[index] = (code % 3) as u8; code /= 3; }
    word
}

fn generate_matchings() -> Vec<[(u8, u8); 4]> {
    fn visit(vertices: &[u8], pairs: &mut Vec<(u8,u8)>, out: &mut Vec<[(u8,u8);4]>) {
        if vertices.is_empty() {
            out.push([pairs[0], pairs[1], pairs[2], pairs[3]]);
            return;
        }
        for position in 1..vertices.len() {
            let mut rest = Vec::new();
            rest.extend_from_slice(&vertices[1..position]);
            rest.extend_from_slice(&vertices[position+1..]);
            pairs.push((vertices[0], vertices[position]));
            visit(&rest, pairs, out);
            pairs.pop();
        }
    }
    let mut answer = Vec::new();
    visit(&[0,1,2,3,4,5,6,7], &mut Vec::new(), &mut answer);
    if answer.len() != 105 { fail("matching census changed"); }
    answer
}

fn parse_hex(value: &str) -> Mono {
    if value == "-" { return Mono::new(Vec::new()); }
    if value.len() % 2 != 0 { fail("odd monomial hex"); }
    Mono::new((0..value.len()).step_by(2).map(|index|
        u8::from_str_radix(&value[index..index+2], 16)
            .unwrap_or_else(|_| fail("bad monomial hex"))).collect())
}

fn mono_hex(value: Mono) -> String {
    if value.len == 0 { return "-".into(); }
    value.slice().iter().map(|item| format!("{item:02x}")).collect()
}

fn inverse_mod(mut base: u64) -> u64 {
    let mut exponent = PRIME - 2;
    let mut answer = 1;
    while exponent != 0 {
        if exponent & 1 != 0 { answer = answer * base % PRIME; }
        base = base * base % PRIME;
        exponent >>= 1;
    }
    answer
}

fn sub_mod(left: u64, right: u64) -> u64 {
    if left >= right { left - right } else { left + PRIME - right }
}

impl Engine {
    fn new() -> Self {
        let mut edges = [(0,0); N_EDGES];
        let mut edge_id = [[0; N]; N];
        let mut next = 0;
        for left in 0..N as u8 { for right in left+1..N as u8 {
            edges[next] = (left,right);
            edge_id[left as usize][right as usize] = next as u8;
            edge_id[right as usize][left as usize] = next as u8;
            next += 1;
        }}
        let mut support = [false; N_COORDS];
        for &value in &SUPPORT_IDS { support[value as usize] = true; }
        let mut actions = Vec::new();
        for action_index in 0..4 {
            let sites = SITE_ACTIONS[action_index];
            let colours = COLOUR_ACTIONS[action_index];
            let mut var_map = [0; N_COORDS];
            for coordinate in 0..N_COORDS {
                let edge = coordinate / 9;
                let a = (coordinate % 9) / 3;
                let b = coordinate % 3;
                let (left,right) = edges[edge];
                let (mut moved_left, mut moved_right) = (sites[left as usize], sites[right as usize]);
                let (mut moved_a, mut moved_b) = (colours[a], colours[b]);
                if moved_left > moved_right {
                    std::mem::swap(&mut moved_left, &mut moved_right);
                    std::mem::swap(&mut moved_a, &mut moved_b);
                }
                let moved_edge = edge_id[moved_left as usize][moved_right as usize] as usize;
                var_map[coordinate] = (moved_edge*9 + moved_a as usize*3 + moved_b as usize) as u8;
            }
            let mut word_map = [0; N_WORDS];
            for code in 0..N_WORDS {
                let word = decode_word(code as u16);
                let mut moved = [0; N];
                for site in 0..N { moved[sites[site] as usize] = colours[word[site] as usize]; }
                word_map[code] = encode_word(&moved);
            }
            actions.push(Action { var_map, word_map });
        }
        let matchings = generate_matchings();
        let mut polynomials = vec![Vec::new(); N_WORDS];
        let mut term_index: HashMap<Mono, Vec<u16>> = HashMap::new();
        for code in 0..N_WORDS {
            let word = decode_word(code as u16);
            if word.iter().all(|value| *value == word[0]) { continue; }
            let mut terms = BTreeMap::<Mono,i32>::new();
            for matching in &matchings {
                let mut ids = Vec::new();
                for &(left,right) in matching {
                    let edge = edge_id[left as usize][right as usize] as usize;
                    let coordinate = edge*9 + word[left as usize] as usize*3 + word[right as usize] as usize;
                    if !support[coordinate] { ids.push(coordinate as u8); }
                }
                *terms.entry(Mono::new(ids)).or_default() += 1;
            }
            polynomials[code] = terms.into_iter().collect();
            for &(term,_) in &polynomials[code] { term_index.entry(term).or_default().push(code as u16); }
        }
        Self {
            actions, polynomials, term_index,
            row_cache: HashMap::new(), column_cache: HashMap::new(),
            incident_cache: HashMap::new(), output_cache: HashMap::new(),
        }
    }

    fn moved_mono(&self, value: Mono, action: usize) -> Mono {
        let mut ids=[0u8;DEGREE];
        for index in 0..value.len as usize {
            ids[index]=self.actions[action].var_map[value.ids[index] as usize];
        }
        ids[..value.len as usize].sort_unstable();
        Mono {len:value.len,ids}
    }
    fn canonical_row(&mut self, row: Mono) -> Mono {
        if let Some(&answer) = self.row_cache.get(&row) { return answer; }
        let answer = (0..4).map(|action| self.moved_mono(row, action)).min().unwrap();
        if self.row_cache.len() >= 1_000_000 { self.row_cache.clear(); }
        self.row_cache.insert(row, answer);
        answer
    }
    #[inline]
    fn canonical_row_uncached(&self, row: Mono) -> Mono {
        (0..4).map(|action| self.moved_mono(row, action)).min().unwrap()
    }
    fn moved_column(&self, column: Column, action: usize) -> Column {
        Column { word: self.actions[action].word_map[column.word as usize],
                 multiplier: self.moved_mono(column.multiplier, action) }
    }
    fn column_orbit(&self, column: Column) -> Vec<Column> {
        let mut answer: Vec<_>=(0..4).map(|action| self.moved_column(column, action)).collect();
        answer.sort_unstable(); answer.dedup(); answer
    }
    fn canonical_column(&mut self, column: Column) -> Column {
        if let Some(&answer) = self.column_cache.get(&column) { return answer; }
        let answer = self.canonical_column_uncached(column);
        self.column_cache.insert(column, answer);
        answer
    }
    fn canonical_column_uncached(&self, column: Column) -> Column {
        self.column_orbit(column).into_iter().min().unwrap()
    }
    fn divisors(&self, row: Mono) -> Vec<Mono> {
        let mut answer = Vec::new();
        for mask in 0..(1usize << row.len) {
            if mask.count_ones() as usize > GENERATOR_DEGREE { continue; }
            let mut ids=[0u8;DEGREE];
            let mut len=0usize;
            for (index,&value) in row.slice().iter().enumerate() {
                if (mask>>index)&1 == 1 { ids[len]=value; len+=1; }
            }
            answer.push(Mono {len:len as u8,ids});
        }
        answer.sort_unstable(); answer.dedup(); answer
    }
    fn incident_columns(&mut self, row: Mono) -> Vec<Column> {
        if let Some(answer) = self.incident_cache.get(&row) { return answer.clone(); }
        let answer = self.incident_columns_uncached(row);
        self.incident_cache.insert(row, answer.clone());
        answer
    }
    fn incident_columns_uncached(&self, row: Mono) -> Vec<Column> {
        let mut answer = Vec::new();
        for term in self.divisors(row) {
            if row.len as usize - term.len as usize > MULTIPLIER_DEGREE { continue; }
            let Some(codes) = self.term_index.get(&term).cloned() else { continue; };
            let multiplier = row.quotient(term).unwrap();
            for code in codes {
                answer.push(self.canonical_column_uncached(Column { word: code, multiplier }));
            }
        }
        answer.sort_unstable(); answer.dedup(); answer
    }
    fn invariant_outputs(&mut self, column: Column) -> Vec<(Mono,i32)> {
        if let Some(answer) = self.output_cache.get(&column) { return answer.clone(); }
        let answer = self.invariant_outputs_uncached(column);
        self.output_cache.insert(column, answer.clone());
        answer
    }
    fn invariant_outputs_uncached(&mut self, column: Column) -> Vec<(Mono,i32)> {
        if column.multiplier.len as usize > MULTIPLIER_DEGREE { fail("multiplier exceeds degree five"); }
        let mut raw = Vec::new();
        for actual in self.column_orbit(column) {
            for (term, coefficient) in self.polynomials[actual.word as usize].clone() {
                let row = actual.multiplier.concat(term);
                if self.canonical_row(row) == row { raw.push((row,coefficient)); }
            }
        }
        raw.sort_unstable_by_key(|item| item.0);
        let mut answer: Vec<(Mono,i32)> = Vec::new();
        for (row,coefficient) in raw {
            if let Some(last)=answer.last_mut() {
                if last.0==row { last.1+=coefficient; continue; }
            }
            answer.push((row,coefficient));
        }
        answer.retain(|(_,value)| *value!=0);
        if answer.is_empty() { fail("invariant output vanished"); }
        answer
    }
    // Read-only variant for candidate sweeps.  It deliberately avoids all
    // caches, so worker threads share the provider without cloning either the
    // provider or the (much larger) echelon basis.
    fn invariant_outputs_pure(&self, column: Column) -> Vec<(Mono,i32)> {
        if column.multiplier.len as usize > MULTIPLIER_DEGREE { fail("multiplier exceeds degree five"); }
        let mut raw = Vec::new();
        for actual in self.column_orbit(column) {
            for &(term, coefficient) in &self.polynomials[actual.word as usize] {
                let row = actual.multiplier.concat(term);
                if self.canonical_row_uncached(row) == row { raw.push((row,coefficient)); }
            }
        }
        raw.sort_unstable_by_key(|item| item.0);
        let mut answer: Vec<(Mono,i32)> = Vec::new();
        for (row,coefficient) in raw {
            if let Some(last)=answer.last_mut() {
                if last.0==row { last.1+=coefficient; continue; }
            }
            answer.push((row,coefficient));
        }
        answer.retain(|(_,value)| *value!=0);
        if answer.is_empty() { fail("invariant output vanished"); }
        answer
    }
}

fn read_dual(path: &Path) -> HashMap<Mono,u64> {
    let mut answer = HashMap::new();
    let input = BufReader::new(File::open(path).unwrap_or_else(|e| fail(e.to_string())));
    let mut expected = None;
    for (number,line) in input.lines().enumerate() {
        let line = line.unwrap_or_else(|e| fail(e.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if number == 0 {
            if fields.len()!=3 || fields[0]!="KRENN_N8_LAMBDA8_MOD_V1" || fields[1].parse::<u64>().ok()!=Some(PRIME) { fail("bad dual header"); }
            expected = fields[2].parse::<usize>().ok();
            continue;
        }
        if fields.len()!=5 || fields[0]!="ROW" { fail("bad dual row"); }
        let row = parse_hex(fields[1]);
        let value: u64 = fields[2].parse().unwrap_or_else(|_| fail("bad dual residue"));
        if row.len as usize > 8 || value==0 || value>=PRIME || answer.insert(row,value).is_some() { fail("bad dual entry"); }
    }
    if Some(answer.len()) != expected || answer.get(&Mono::new(Vec::new())) != Some(&1) { fail("dual census/target changed"); }
    answer
}

fn read_columns(path: &Path) -> BTreeSet<Column> {
    let input = BufReader::new(File::open(path).unwrap_or_else(|e| fail(e.to_string())));
    let mut answer = BTreeSet::new();
    let mut expected = None;
    for (number,line) in input.lines().enumerate() {
        let line = line.unwrap_or_else(|e| fail(e.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if number==0 {
            if fields.len()!=2 || (fields[0]!="KRENN_N8_D9_SELECTED_V1" && fields[0]!="KRENN_N8_D9_SELECTED_INCREMENTAL_V1") { fail("bad column header"); }
            expected = fields[1].parse::<usize>().ok();
            continue;
        }
        if fields.len()!=3 || fields[0]!="COLUMN" { fail("bad column row"); }
        let word: u16 = fields[1].parse().unwrap_or_else(|_| fail("bad word"));
        let multiplier = parse_hex(fields[2]);
        if word as usize >= N_WORDS || multiplier.len as usize != 5 || answer.insert(Column{word,multiplier}) == false { fail("bad/duplicate selected column"); }
    }
    if Some(answer.len()) != expected { fail("selected census changed"); }
    answer
}

fn pairing(outputs: &[(Mono,i32)], functional: &HashMap<Mono,u64>) -> u64 {
    outputs.iter().fold(0, |sum,(row,coefficient)| {
        let coefficient = (*coefficient as i64).rem_euclid(PRIME as i64) as u64;
        (sum + coefficient * functional.get(row).copied().unwrap_or(0)) % PRIME
    })
}

fn subtract_scaled(target: &mut BTreeMap<Mono,u64>, source: &[(Mono,u64)], scalar: u64) {
    if scalar==0 { return; }
    for &(row,coefficient) in source {
        let value = sub_mod(target.get(&row).copied().unwrap_or(0), scalar*coefficient%PRIME);
        if value==0 { target.remove(&row); } else { target.insert(row,value); }
    }
}

fn add_column(engine: &mut Engine, column: Column, lambda8: &HashMap<Mono,u64>, basis: &mut BTreeMap<Mono,BasisRecord>, pivot_last: bool) -> Result<Option<Mono>,()> {
    let outputs = engine.invariant_outputs(column);
    let lower = pairing(&outputs, lambda8);
    let mut rhs = if lower==0 {0} else {PRIME-lower};
    let mut vector = BTreeMap::new();
    for (row,coefficient) in outputs {
        if row.len as usize != DEGREE { continue; }
        let value = (coefficient as i64).rem_euclid(PRIME as i64) as u64;
        if value!=0 { vector.insert(row,value); }
    }
    loop {
        let pivot_value = if pivot_last { vector.last_key_value() } else { vector.first_key_value() };
        let Some((&pivot,&value)) = pivot_value else {
            return if rhs==0 {Ok(None)} else {Err(())};
        };
        if let Some(record) = basis.get(&pivot) {
            subtract_scaled(&mut vector, &record.vector, value);
            rhs = sub_mod(rhs, value*record.rhs%PRIME);
        } else {
            let inverse = inverse_mod(value);
            for coefficient in vector.values_mut() { *coefficient = *coefficient*inverse%PRIME; }
            rhs = rhs*inverse%PRIME;
            basis.insert(pivot, BasisRecord{vector: vector.into_iter().collect(),rhs});
            return Ok(Some(pivot));
        }
    }
}

fn solve_functional(lambda8: &HashMap<Mono,u64>, basis: &BTreeMap<Mono,BasisRecord>, pivot_last: bool) -> HashMap<Mono,u64> {
    let mut top = HashMap::new();
    if pivot_last {
        for (&pivot,record) in basis.iter() {
            let mut value = record.rhs;
            for &(row,coefficient) in &record.vector {
                if row==pivot { continue; }
                value = sub_mod(value, coefficient*top.get(&row).copied().unwrap_or(0)%PRIME);
            }
            if value!=0 { top.insert(pivot,value); }
        }
    } else {
        for (&pivot,record) in basis.iter().rev() {
            let mut value = record.rhs;
            for &(row,coefficient) in &record.vector {
                if row==pivot { continue; }
                value = sub_mod(value, coefficient*top.get(&row).copied().unwrap_or(0)%PRIME);
            }
            if value!=0 { top.insert(pivot,value); }
        }
    }
    let mut answer = lambda8.clone();
    answer.extend(top);
    answer
}

fn verify_basis(functional: &HashMap<Mono,u64>, basis: &BTreeMap<Mono,BasisRecord>) {
    for record in basis.values() {
        let value = record.vector.iter().fold(0u64, |sum,(row,coefficient)|
            (sum + *coefficient * functional.get(row).copied().unwrap_or(0)) % PRIME);
        if value != record.rhs { fail("back-substituted functional fails basis equation"); }
    }
}

fn verify_basis_records(functional: &HashMap<Mono,u64>, basis: &BTreeMap<Mono,BasisRecord>, pivots: &[Mono]) {
    for pivot in pivots {
        let record = basis.get(pivot).unwrap_or_else(|| fail("new basis pivot disappeared"));
        let value = record.vector.iter().fold(0u64, |sum,(row,coefficient)|
            (sum + *coefficient * functional.get(row).copied().unwrap_or(0)) % PRIME);
        if value != record.rhs { fail("back-substituted functional fails new basis equation"); }
    }
}

fn write_columns(path: &Path, selected: &BTreeSet<Column>) {
    let tmp = path.with_extension("tsv.tmp");
    let mut out = BufWriter::new(File::create(&tmp).unwrap_or_else(|e| fail(e.to_string())));
    writeln!(out,"KRENN_N8_D9_SELECTED_INCREMENTAL_V1 {}",selected.len()).unwrap();
    for column in selected { writeln!(out,"COLUMN {} {}",column.word,mono_hex(column.multiplier)).unwrap(); }
    out.flush().unwrap(); drop(out);
    fs::rename(tmp,path).unwrap_or_else(|e| fail(e.to_string()));
}

fn write_dual(path: &Path, functional: &HashMap<Mono,u64>) {
    let tmp = path.with_extension("tsv.tmp");
    let mut rows: Vec<_> = functional.iter().filter(|(_,value)| **value!=0).collect();
    rows.sort_by_key(|(row,_)| **row);
    let mut out = BufWriter::new(File::create(&tmp).unwrap_or_else(|e| fail(e.to_string())));
    writeln!(out,"KRENN_N8_D9_MODULAR_DUAL_V1 {} {}",PRIME,rows.len()).unwrap();
    for (&row,&value) in rows { writeln!(out,"ROW {} {}",mono_hex(row),value).unwrap(); }
    out.flush().unwrap(); drop(out);
    fs::rename(tmp,path).unwrap_or_else(|e| fail(e.to_string()));
}

fn read_processed_pivots(path: &Path) -> BTreeSet<Mono> {
    if !path.exists() { return BTreeSet::new(); }
    let input=BufReader::new(File::open(path).unwrap_or_else(|e| fail(e.to_string())));
    let mut answer=BTreeSet::new();
    let mut expected=None;
    for (number,line) in input.lines().enumerate() {
        let line=line.unwrap_or_else(|e| fail(e.to_string()));
        let fields: Vec<_>=line.split_whitespace().collect();
        if number==0 {
            if fields.len()!=2 || fields[0]!="KRENN_N8_D9_PROCESSED_PIVOTS_V1" { fail("bad processed-pivot header"); }
            expected=fields[1].parse::<usize>().ok();
            continue;
        }
        if fields.len()!=2 || fields[0]!="PIVOT" { fail("bad processed-pivot row"); }
        let pivot=parse_hex(fields[1]);
        if pivot.len as usize!=DEGREE || !answer.insert(pivot) { fail("bad/duplicate processed pivot"); }
    }
    if Some(answer.len())!=expected { fail("processed-pivot census changed"); }
    answer
}

fn write_processed_pivots(path: &Path, pivots: &BTreeSet<Mono>) {
    let tmp=path.with_extension("tsv.tmp");
    let mut out=BufWriter::new(File::create(&tmp).unwrap_or_else(|e| fail(e.to_string())));
    writeln!(out,"KRENN_N8_D9_PROCESSED_PIVOTS_V1 {}",pivots.len()).unwrap();
    for &pivot in pivots { writeln!(out,"PIVOT {}",mono_hex(pivot)).unwrap(); }
    out.flush().unwrap(); drop(out);
    fs::rename(tmp,path).unwrap_or_else(|e| fail(e.to_string()));
}

fn main() {
    let args: Vec<_> = env::args().collect();
    if args.len()<7 || args.len()>11 { fail("usage: degree9_incremental LAMBDA8.tsv SELECTED.tsv RESULT.json CHECKPOINT.tsv DUAL.tsv WALL_SECONDS [violations|frontier|pivots|closure] [first|last] [workers] [PROCESSED_PIVOTS.tsv]"); }
    let strategy = args.get(7).map(String::as_str).unwrap_or("violations");
    match strategy {
        "violations" | "frontier" | "pivots" | "closure" => (),
        _ => fail("strategy must be violations, frontier, pivots, or closure"),
    }
    let pivot_last = match args.get(8).map(String::as_str).unwrap_or("first") {
        "first" => false,
        "last" => true,
        _ => fail("pivot order must be first or last"),
    };
    let workers: usize = args.get(9).map(|value| value.parse().unwrap_or_else(|_| fail("bad worker count"))).unwrap_or(1);
    if workers==0 || workers>32 { fail("worker count must be 1..32"); }
    let wall: u64 = args[6].parse().unwrap_or_else(|_| fail("bad wall"));
    let started = Instant::now();
    let deadline = started + Duration::from_secs(wall);
    let lambda8 = read_dual(Path::new(&args[1]));
    let mut selected = read_columns(Path::new(&args[2]));
    let initial_selected = selected.len();
    let mut engine = Engine::new();
    for &column in &selected {
        if engine.canonical_column(column)!=column { fail("selected column is not canonical"); }
    }
    let mut basis = BTreeMap::new();
    for (index,&column) in selected.iter().enumerate() {
        let _independent = add_column(&mut engine,column,&lambda8,&mut basis,pivot_last)
            .unwrap_or_else(|_| fail("initial relative inconsistency"));
        if (index+1)%5000==0 {
            eprintln!("basis {}/{} rank={} outputs={} rows={} elapsed={:.1}",index+1,selected.len(),basis.len(),engine.output_cache.len(),engine.row_cache.len(),started.elapsed().as_secs_f64());
            engine.output_cache.clear();
        }
    }
    engine.output_cache.clear();
    engine.row_cache.clear();
    engine.column_cache.clear();
    let mut rounds = Vec::new();
    let mut status = "WALL_CAP_UNRESOLVED";
    let mut terminal_functional = None;
    let processed_path=args.get(10).map(Path::new);
    let mut processed_pivots = processed_path.map(read_processed_pivots).unwrap_or_default();
    if processed_pivots.iter().any(|pivot| !basis.contains_key(pivot)) { fail("processed pivot absent from rebuilt basis"); }
    let mut new_pivots = Vec::new();
    let mut closure_rounds: Vec<(usize,usize,usize,usize)> = Vec::new();
    for round in 0..1000usize {
        if Instant::now()>=deadline { break; }
        if strategy=="closure" {
            const CLOSURE_CHUNK: usize = 10_000;
            let closure_rows: Vec<Mono> = basis.keys()
                .filter(|row| !processed_pivots.contains(*row))
                .take(CLOSURE_CHUNK).copied().collect();
            if !closure_rows.is_empty() {
                let chunk_size = closure_rows.len().div_ceil(workers).max(1);
                let unseen: BTreeSet<Column> = if workers==1 {
                    let mut answer = BTreeSet::new();
                    for &row in &closure_rows {
                        for column in engine.incident_columns_uncached(row) {
                            if column.multiplier.len as usize==MULTIPLIER_DEGREE && !selected.contains(&column) {
                                answer.insert(column);
                            }
                        }
                    }
                    answer
                } else {
                    thread::scope(|scope| {
                        let mut handles = Vec::new();
                        for chunk in closure_rows.chunks(chunk_size) {
                            let engine_ref=&engine;
                            let selected_ref=&selected;
                            handles.push(scope.spawn(move || {
                                let mut local=BTreeSet::new();
                                for &row in chunk {
                                    for column in engine_ref.incident_columns_uncached(row) {
                                        if column.multiplier.len as usize==MULTIPLIER_DEGREE && !selected_ref.contains(&column) {
                                            local.insert(column);
                                        }
                                    }
                                }
                                local
                            }));
                        }
                        let mut answer=BTreeSet::new();
                        for handle in handles {
                            answer.extend(handle.join().unwrap_or_else(|_| fail("closure worker panicked")));
                        }
                        answer
                    })
                };
                processed_pivots.extend(closure_rows.iter().copied());
                let before=selected.len();
                for column in unseen {
                    if selected.insert(column) {
                        let independent=add_column(&mut engine,column,&lambda8,&mut basis,pivot_last)
                            .unwrap_or_else(|_| fail("closure proves relative inconsistency"));
                        if let Some(pivot)=independent { new_pivots.push(pivot); }
                    }
                }
                let additions=selected.len()-before;
                eprintln!("closure round={} processed={} total_processed={} additions={} selected={} rank={} elapsed={:.1}",
                          round,closure_rows.len(),processed_pivots.len(),additions,selected.len(),basis.len(),started.elapsed().as_secs_f64());
                closure_rounds.push((closure_rows.len(),processed_pivots.len(),additions,basis.len()));
                write_columns(Path::new(&args[4]),&selected);
                engine.output_cache.clear();
                engine.row_cache.clear();
                engine.column_cache.clear();
                engine.incident_cache.clear();
                continue;
            }
            eprintln!("closure incidence complete pivots={} selected={} rank={} elapsed={:.1}",processed_pivots.len(),selected.len(),basis.len(),started.elapsed().as_secs_f64());
        }
        let functional = solve_functional(&lambda8,&basis,pivot_last);
        // A complete scan is retained at round zero, periodically, and before
        // accepting a terminal dual.  Between those points only newly inserted
        // records need an independent check; solve_functional constructs the
        // old equations by triangular back-substitution.
        if round==0 || round%64==0 { verify_basis(&functional,&basis); }
        else { verify_basis_records(&functional,&basis,&new_pivots); }
        new_pivots.clear();
        let mut candidates = BTreeSet::new();
        let candidate_rows: Vec<Mono> = if strategy=="pivots" {
            basis.keys().filter(|row| !processed_pivots.contains(*row)).copied().collect()
        } else {
            functional.iter().filter_map(|(&row,&value)| (value!=0 && row.len as usize==DEGREE).then_some(row)).collect()
        };
        let candidate_row_count = candidate_rows.len();
        for &row in &candidate_rows {
            let incident = if strategy=="pivots" {
                engine.incident_columns_uncached(row)
            } else {
                engine.incident_columns(row)
            };
            for column in incident {
                if column.multiplier.len as usize==MULTIPLIER_DEGREE { candidates.insert(column); }
            }
        }
        if strategy=="pivots" { processed_pivots.extend(candidate_rows); }
        let mut violations: Vec<(Column,u64)> = if workers==1 {
            let mut answer = Vec::new();
            for &column in &candidates {
                let outputs = if strategy=="pivots" {
                    engine.invariant_outputs_uncached(column)
                } else {
                    engine.invariant_outputs(column)
                };
                let value = pairing(&outputs,&functional);
                if value!=0 { answer.push((column,value)); }
            }
            answer
        } else {
            let candidate_vec: Vec<Column> = candidates.iter().copied().collect();
            let chunk_size = candidate_vec.len().div_ceil(workers).max(1);
            thread::scope(|scope| {
                let mut handles = Vec::new();
                for chunk in candidate_vec.chunks(chunk_size) {
                    let engine_ref = &engine;
                    let functional_ref = &functional;
                    handles.push(scope.spawn(move || {
                        let mut local = Vec::new();
                        for &column in chunk {
                            let outputs = engine_ref.invariant_outputs_pure(column);
                            let value = pairing(&outputs,functional_ref);
                            if value!=0 { local.push((column,value)); }
                        }
                        local
                    }));
                }
                let mut answer = Vec::new();
                for handle in handles { answer.extend(handle.join().unwrap_or_else(|_| fail("candidate worker panicked"))); }
                answer
            })
        };
        violations.sort_unstable_by_key(|item| item.0);
        for &(column,_) in &violations {
            if selected.contains(&column) { fail("functional fails selected column"); }
        }
        eprintln!("round={} selected={} rank={} functional={} candidate_rows={} candidates={} violations={} elapsed={:.1}",round,selected.len(),basis.len(),functional.len(),
                  candidate_row_count,candidates.len(),violations.len(),started.elapsed().as_secs_f64());
        rounds.push((selected.len(),basis.len(),functional.len(),candidates.len(),violations.len()));
        if violations.is_empty() {
            verify_basis(&functional,&basis);
            status = "MODULAR_EXTENDED_DUAL";
            terminal_functional = Some(functional);
            break;
        }
        if strategy=="closure" { fail("complete pivot-incidence closure still has a violated column"); }
        let additions: Vec<Column> = if strategy!="violations" {
            candidates.iter().filter(|column| !selected.contains(column)).copied().collect()
        } else {
            violations.into_iter().map(|(column,_)| column).collect()
        };
        eprintln!("round={} strategy={} additions={}", round,strategy,additions.len());
        for column in additions {
            if selected.insert(column) {
                // Violations are discovered against the pre-round functional.
                // A later member of the same batch may therefore become a
                // consistent linear consequence after earlier members enter.
                // That is harmless; only an inconsistent augmented relation
                // rules out extension of lambda8.
                let independent = add_column(&mut engine,column,&lambda8,&mut basis,pivot_last)
                    .unwrap_or_else(|_| fail("new relative inconsistency"));
                if let Some(pivot)=independent { new_pivots.push(pivot); }
            }
        }
        write_columns(Path::new(&args[4]),&selected);
        engine.output_cache.clear();
        engine.row_cache.clear();
        engine.column_cache.clear();
        engine.incident_cache.clear();
    }
    if let Some(functional) = terminal_functional.as_ref() { write_dual(Path::new(&args[5]),functional); }
    if let Some(path)=processed_path { write_processed_pivots(path,&processed_pivots); }
    let rounds_json = rounds.iter().enumerate().map(|(index,(selected,rank,functional,candidates,violations))|
        format!("{{\"round\":{index},\"selected_columns\":{selected},\"rank\":{rank},\"functional_support\":{functional},\"incident_columns\":{candidates},\"violations\":{violations}}}"))
        .collect::<Vec<_>>().join(",");
    let closure_json = closure_rounds.iter().enumerate().map(|(index,(processed,total,additions,rank))|
        format!("{{\"round\":{index},\"processed_pivots\":{processed},\"total_processed_pivots\":{total},\"additions\":{additions},\"rank\":{rank}}}"))
        .collect::<Vec<_>>().join(",");
    let text = format!("{{\n  \"status\": \"{status}\",\n  \"prime\": {PRIME},\n  \"initial_selected_columns\": {initial_selected},\n  \"terminal_selected_columns\": {},\n  \"terminal_rank\": {},\n  \"processed_pivots\": {},\n  \"rounds\": [{rounds_json}],\n  \"closure_rounds\": [{closure_json}],\n  \"row_cache\": {},\n  \"column_cache\": {},\n  \"incident_cache\": {},\n  \"output_cache\": {},\n  \"elapsed_seconds\": {:.6},\n  \"scope_guard\": \"modular discovery only until independent exact-Q replay\"\n}}\n",selected.len(),basis.len(),processed_pivots.len(),engine.row_cache.len(),engine.column_cache.len(),engine.incident_cache.len(),engine.output_cache.len(),started.elapsed().as_secs_f64());
    let result_path = Path::new(&args[3]);
    let tmp = result_path.with_extension("json.tmp");
    fs::write(&tmp,text).unwrap_or_else(|e| fail(e.to_string()));
    fs::rename(tmp,result_path).unwrap_or_else(|e| fail(e.to_string()));
    eprintln!("terminal status={} selected={} rank={} elapsed={:.1}",status,selected.len(),basis.len(),started.elapsed().as_secs_f64());
}
