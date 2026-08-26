//! Exact fixed-chart homogeneous ideal membership with stabilizer-orbit compression.
//!
//! The input is the 251-variable affine msolve system obtained by fixing
//! x67_01=1.  We homogenize with a new variable t and decide whether t^D is
//! in the degree-D part of the homogeneous ideal over a caller-selected
//! prime.  The stabilizer S6 x C2 (order 1440) fixes both the system and t,
//! so it is exact to work with orbit-sum rows and columns.

use std::collections::{BTreeMap, HashMap, HashSet, VecDeque};
use std::env;
use std::fs::{self, File};
use std::hash::{BuildHasherDefault, Hash, Hasher};
use std::io::{BufReader, BufWriter, Read, Write};
use std::path::{Path, PathBuf};
use std::process::Command;
use std::thread;
use std::time::{Duration, Instant};

const N: usize = 8;
const N_EDGES: usize = 28;
const ORIGINAL_COORDS: usize = 252;
const AFFINE_COORDS: usize = 251;
const T_ID: u8 = 251;
const TOTAL_COORDS: usize = 252;
const N_WORDS: usize = 6561;
const GROUP_ORDER: u16 = 1440;
const GENERATOR_DEGREE: usize = 4;
const MAX_DEGREE: usize = 12;
const FIXED_ORIGINAL: usize = 27 * 9 + 1; // edge 67, colours 0,1
const CHECKPOINT_MAGIC: &[u8; 12] = b"AFF251CL1\0\0\0";

#[derive(Clone, Copy, Eq, Ord, PartialEq, PartialOrd)]
struct Mono {
    len: u8,
    ids: [u8; MAX_DEGREE],
}

impl Hash for Mono {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.len.hash(state);
        self.slice().hash(state);
    }
}

impl Mono {
    fn new(mut ids: Vec<u8>) -> Self {
        if ids.len() > MAX_DEGREE { fail("monomial exceeds degree 12"); }
        ids.sort_unstable();
        let mut packed = [0; MAX_DEGREE];
        packed[..ids.len()].copy_from_slice(&ids);
        Self { len: ids.len() as u8, ids: packed }
    }

    fn slice(&self) -> &[u8] { &self.ids[..self.len as usize] }

    fn concat(self, other: Mono) -> Self {
        let total = self.len as usize + other.len as usize;
        if total > MAX_DEGREE { fail("monomial product exceeds degree 12"); }
        let mut ids = [0; MAX_DEGREE];
        let (mut left, mut right, mut out) = (0usize, 0usize, 0usize);
        while left < self.len as usize && right < other.len as usize {
            if self.ids[left] <= other.ids[right] {
                ids[out] = self.ids[left]; left += 1;
            } else {
                ids[out] = other.ids[right]; right += 1;
            }
            out += 1;
        }
        while left < self.len as usize { ids[out] = self.ids[left]; left += 1; out += 1; }
        while right < other.len as usize { ids[out] = other.ids[right]; right += 1; out += 1; }
        Self { len: total as u8, ids }
    }

    fn quotient(self, divisor: Mono) -> Option<Self> {
        let mut ids = [0; MAX_DEGREE];
        let (mut source, mut divide, mut out) = (0usize, 0usize, 0usize);
        while source < self.len as usize {
            if divide < divisor.len as usize && self.ids[source] == divisor.ids[divide] {
                source += 1; divide += 1;
            } else {
                if divide < divisor.len as usize && divisor.ids[divide] < self.ids[source] {
                    return None;
                }
                ids[out] = self.ids[source]; source += 1; out += 1;
            }
        }
        if divide != divisor.len as usize { return None; }
        Some(Self { len: out as u8, ids })
    }
}

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Column { word: u16, multiplier: Mono }

struct Action { var_map: [u8; TOTAL_COORDS], word_map: Vec<u16> }

struct Provider {
    actions: Vec<Action>,
    polynomials: Vec<Vec<(Mono, i32)>>,
    term_index: HashMap<Mono, Vec<u16>>,
    parsed_terms: usize,
    distinct_terms: usize,
}

#[derive(Clone, Copy)]
struct RowInfo { canonical: Mono, stabilizer: u16 }

struct OrbitEngine {
    provider: Provider,
    row_cache: HashMap<Mono, RowInfo>,
}

struct Gate {
    started: Instant,
    wall: Duration,
    rss_limit_kib: u64,
    peak_rss_kib: u64,
    last_rss_check: Instant,
}

#[derive(Default)]
struct Closure {
    rows: HashSet<Mono>,
    columns: HashSet<Column>,
    row_frontier: VecDeque<Mono>,
    column_frontier: VecDeque<Column>,
    rounds: Vec<(usize, usize, usize, usize)>,
    complete: bool,
}

struct Config {
    input: PathBuf,
    output: PathBuf,
    checkpoint: PathBuf,
    dual: PathBuf,
    degree: usize,
    prime: u64,
    wall_seconds: u64,
    rss_gib: u64,
    workers: usize,
    pivot_last: bool,
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("affine251-orbit-membership: {}", message.as_ref());
    std::process::exit(2)
}

fn json_escape(value: &str) -> String {
    value.replace('\\', "\\\\").replace('"', "\\\"")
}

fn mono_hex(value: Mono) -> String {
    if value.len == 0 { return "-".into(); }
    value.slice().iter().map(|item| format!("{item:02x}")).collect()
}

fn encode_word(word: &[u8; N]) -> u16 {
    word.iter().fold(0, |code, digit| code * 3 + *digit as u16)
}

fn decode_word(mut code: u16) -> [u8; N] {
    let mut word = [0; N];
    for index in (0..N).rev() { word[index] = (code % 3) as u8; code /= 3; }
    word
}

fn edge_tables() -> ([(u8, u8); N_EDGES], [[u8; N]; N]) {
    let mut edges = [(0, 0); N_EDGES];
    let mut edge_id = [[0; N]; N];
    let mut next = 0;
    for left in 0..N as u8 {
        for right in left + 1..N as u8 {
            edges[next] = (left, right);
            edge_id[left as usize][right as usize] = next as u8;
            edge_id[right as usize][left as usize] = next as u8;
            next += 1;
        }
    }
    (edges, edge_id)
}

fn coordinate_name(original: usize) -> String {
    let (edges, _) = edge_tables();
    let edge = original / 9;
    let a = (original % 9) / 3;
    let b = original % 3;
    format!("x{}{}_{}{}", edges[edge].0, edges[edge].1, a, b)
}

fn permutations_six() -> Vec<[u8; 6]> {
    fn visit(position: usize, used: &mut [bool; 6], current: &mut [u8; 6], out: &mut Vec<[u8; 6]>) {
        if position == 6 { out.push(*current); return; }
        for value in 0..6 {
            if used[value] { continue; }
            used[value] = true;
            current[position] = value as u8;
            visit(position + 1, used, current, out);
            used[value] = false;
        }
    }
    let mut out = Vec::with_capacity(720);
    visit(0, &mut [false; 6], &mut [0; 6], &mut out);
    if out.len() != 720 { fail("S6 generation failed"); }
    out
}

fn build_actions(header: &[String]) -> Vec<Action> {
    if header.len() != AFFINE_COORDS { fail("affine variable count is not 251"); }
    let mut original_to_affine = [T_ID; ORIGINAL_COORDS];
    let mut next = 0usize;
    for original in 0..ORIGINAL_COORDS {
        if original == FIXED_ORIGINAL { continue; }
        let expected = coordinate_name(original);
        if header[next] != expected {
            fail(format!("variable order changed at {next}: {} != {expected}", header[next]));
        }
        original_to_affine[original] = next as u8;
        next += 1;
    }
    if next != AFFINE_COORDS || coordinate_name(FIXED_ORIGINAL) != "x67_01" {
        fail("fixed-coordinate convention changed");
    }
    let (edges, edge_id) = edge_tables();
    let mut actions = Vec::with_capacity(GROUP_ORDER as usize);
    for permutation in permutations_six() {
        for flip in 0..2usize {
            let mut sites = [0u8; N];
            sites[..6].copy_from_slice(&permutation);
            sites[6] = if flip == 0 { 6 } else { 7 };
            sites[7] = if flip == 0 { 7 } else { 6 };
            let colours = if flip == 0 { [0u8, 1, 2] } else { [1u8, 0, 2] };
            let mut var_map = [0u8; TOTAL_COORDS];
            for affine in 0..AFFINE_COORDS {
                let original = if affine < FIXED_ORIGINAL { affine } else { affine + 1 };
                let edge = original / 9;
                let a = (original % 9) / 3;
                let b = original % 3;
                let (left, right) = edges[edge];
                let (mut ml, mut mr) = (sites[left as usize], sites[right as usize]);
                let (mut ma, mut mb) = (colours[a], colours[b]);
                if ml > mr {
                    std::mem::swap(&mut ml, &mut mr);
                    std::mem::swap(&mut ma, &mut mb);
                }
                let moved_original = edge_id[ml as usize][mr as usize] as usize * 9
                    + ma as usize * 3 + mb as usize;
                var_map[affine] = original_to_affine[moved_original];
            }
            var_map[T_ID as usize] = T_ID;
            let mut word_map = vec![0u16; N_WORDS];
            for code in 0..N_WORDS {
                let word = decode_word(code as u16);
                let mut moved = [0u8; N];
                for site in 0..N {
                    moved[sites[site] as usize] = colours[word[site] as usize];
                }
                word_map[code] = encode_word(&moved);
            }
            actions.push(Action { var_map, word_map });
        }
    }
    if actions.len() != GROUP_ORDER as usize { fail("stabilizer order changed"); }
    actions
}

fn parse_provider(path: &Path) -> Provider {
    let mut text = String::new();
    BufReader::new(File::open(path).unwrap_or_else(|e| fail(e.to_string())))
        .read_to_string(&mut text).unwrap_or_else(|e| fail(e.to_string()));
    let mut lines = text.lines();
    let header: Vec<String> = lines.next().unwrap_or_else(|| fail("missing msolve header"))
        .split(',').map(str::to_owned).collect();
    let file_prime = lines.next().unwrap_or_else(|| fail("missing msolve prime"));
    if file_prime != "32003" && file_prime != "1073741827" {
        fail("unexpected msolve input prime");
    }
    let actions = build_actions(&header);
    let variable_ids: HashMap<&str, u8> = header.iter().enumerate()
        .map(|(index, name)| (name.as_str(), index as u8)).collect();
    let mut polynomials = Vec::with_capacity(N_WORDS);
    let mut parsed_terms = 0usize;
    for (number, raw_line) in lines.enumerate() {
        let line = raw_line.trim_end_matches(',');
        let expanded = line.replace("-1", "+-1");
        let mut aggregated = BTreeMap::<Mono, i32>::new();
        for token in expanded.split('+').filter(|item| !item.is_empty()) {
            parsed_terms += 1;
            if token == "-1" {
                *aggregated.entry(Mono::new(vec![T_ID; 4])).or_default() -= 1;
                continue;
            }
            let mut ids = Vec::with_capacity(4);
            for factor in token.split('*') {
                if factor == "1" { continue; }
                ids.push(*variable_ids.get(factor)
                    .unwrap_or_else(|| fail(format!("unknown factor {factor} in equation {number}"))));
            }
            if ids.len() > 4 { fail("provider term exceeds degree four"); }
            while ids.len() < 4 { ids.push(T_ID); }
            *aggregated.entry(Mono::new(ids)).or_default() += 1;
        }
        let polynomial: Vec<_> = aggregated.into_iter().filter(|(_, value)| *value != 0).collect();
        if polynomial.is_empty() { fail(format!("provider equation {number} vanished")); }
        polynomials.push(polynomial);
    }
    if polynomials.len() != N_WORDS { fail("provider equation count is not 6561"); }
    let mut term_index: HashMap<Mono, Vec<u16>> = HashMap::new();
    for (word, polynomial) in polynomials.iter().enumerate() {
        for &(term, _) in polynomial {
            term_index.entry(term).or_default().push(word as u16);
        }
    }
    for words in term_index.values_mut() { words.sort_unstable(); words.dedup(); }
    let distinct_terms = term_index.len();
    Provider { actions, polynomials, term_index, parsed_terms, distinct_terms }
}

impl OrbitEngine {
    fn new(provider: Provider) -> Self {
        Self { provider, row_cache: HashMap::new() }
    }

    fn moved_mono(&self, value: Mono, action: usize) -> Mono {
        let mut ids = [0u8; MAX_DEGREE];
        for index in 0..value.len as usize {
            ids[index] = self.provider.actions[action].var_map[value.ids[index] as usize];
        }
        ids[..value.len as usize].sort_unstable();
        Mono { len: value.len, ids }
    }

    fn row_info(&mut self, row: Mono) -> RowInfo {
        if let Some(&answer) = self.row_cache.get(&row) { return answer; }
        let mut canonical = row;
        let mut stabilizer = 0u16;
        for action in 0..self.provider.actions.len() {
            let moved = self.moved_mono(row, action);
            if moved < canonical { canonical = moved; }
            if moved == row { stabilizer += 1; }
        }
        if stabilizer == 0 || GROUP_ORDER % stabilizer != 0 { fail("bad row stabilizer"); }
        let answer = RowInfo { canonical, stabilizer };
        if self.row_cache.len() >= 2_000_000 { self.row_cache.clear(); }
        self.row_cache.insert(row, answer);
        self.row_cache.entry(canonical).or_insert(RowInfo { canonical, stabilizer });
        answer
    }

    fn degree_four_divisors(row: Mono) -> Vec<(Mono, Mono)> {
        if row.len < 4 { return Vec::new(); }
        let mut runs = Vec::<(u8, usize)>::new();
        for &value in row.slice() {
            if let Some(last) = runs.last_mut() {
                if last.0 == value { last.1 += 1; continue; }
            }
            runs.push((value, 1));
        }
        fn visit(row: Mono, runs: &[(u8, usize)], index: usize, remaining: usize,
                 selected: &mut Vec<u8>, answer: &mut Vec<(Mono, Mono)>) {
            if remaining == 0 {
                let divisor = Mono::new(selected.clone());
                let multiplier = row.quotient(divisor).unwrap_or_else(|| fail("internal quotient failure"));
                answer.push((divisor, multiplier));
                return;
            }
            if index == runs.len() { return; }
            let (value, count) = runs[index];
            for take in 0..=count.min(remaining) {
                for _ in 0..take { selected.push(value); }
                visit(row, runs, index + 1, remaining - take, selected, answer);
                selected.truncate(selected.len() - take);
            }
        }
        let mut answer = Vec::new();
        visit(row, &runs, 0, 4, &mut Vec::with_capacity(4), &mut answer);
        answer
    }

}

// Read-only worker kernels.  They deliberately keep canonicalization caches
// thread-local, so the large incidence frontier scales without locks while
// the 689k-term provider is shared immutably.
fn moved_mono_pure(provider: &Provider, value: Mono, action: usize) -> Mono {
    let mut ids = [0u8; MAX_DEGREE];
    for index in 0..value.len as usize {
        ids[index] = provider.actions[action].var_map[value.ids[index] as usize];
    }
    ids[..value.len as usize].sort_unstable();
    Mono { len: value.len, ids }
}

fn canonical_column_pure(provider: &Provider, column: Column,
                         cache: &mut HashMap<Column, Column>) -> Column {
    if let Some(&answer) = cache.get(&column) { return answer; }
    let mut answer = column;
    for action in 0..provider.actions.len() {
        let moved = Column {
            word: provider.actions[action].word_map[column.word as usize],
            multiplier: moved_mono_pure(provider, column.multiplier, action),
        };
        if moved < answer { answer = moved; }
    }
    cache.insert(column, answer);
    answer
}

fn row_info_pure(provider: &Provider, row: Mono, cache: &mut HashMap<Mono, RowInfo>) -> RowInfo {
    if let Some(&answer) = cache.get(&row) { return answer; }
    let mut canonical = row;
    let mut stabilizer = 0u16;
    for action in 0..provider.actions.len() {
        let moved = moved_mono_pure(provider, row, action);
        if moved < canonical { canonical = moved; }
        if moved == row { stabilizer += 1; }
    }
    if stabilizer == 0 || GROUP_ORDER % stabilizer != 0 { fail("bad worker row stabilizer"); }
    let answer = RowInfo { canonical, stabilizer };
    cache.insert(row, answer);
    answer
}

fn incident_columns_pure(provider: &Provider, row: Mono,
                         cache: &mut HashMap<Column, Column>, out: &mut HashSet<Column>) {
    for (term, multiplier) in OrbitEngine::degree_four_divisors(row) {
        let Some(words) = provider.term_index.get(&term) else { continue; };
        for &word in words {
            out.insert(canonical_column_pure(provider, Column { word, multiplier }, cache));
        }
    }
}

fn output_rows_pure(provider: &Provider, column: Column,
                    cache: &mut HashMap<Mono, RowInfo>, out: &mut HashSet<Mono>) {
    for &(term, coefficient) in &provider.polynomials[column.word as usize] {
        if coefficient != 0 {
            out.insert(row_info_pure(provider, column.multiplier.concat(term), cache).canonical);
        }
    }
}

fn invariant_column_pure(provider: &Provider, column: Column, prime: u64,
                         cache: &mut HashMap<Mono, RowInfo>) -> Vec<(Mono, u64)> {
    let mut aggregate = BTreeMap::<Mono, i64>::new();
    for &(term, coefficient) in &provider.polynomials[column.word as usize] {
        let info = row_info_pure(provider, column.multiplier.concat(term), cache);
        *aggregate.entry(info.canonical).or_default() += coefficient as i64;
    }
    aggregate.into_iter().filter_map(|(row, coefficient)| {
        if coefficient == 0 { return None; }
        let stabilizer = row_info_pure(provider, row, cache).stabilizer as i128;
        let value = ((coefficient as i128 * stabilizer).rem_euclid(prime as i128)) as u64;
        if value == 0 { None } else { Some((row, value)) }
    }).collect()
}

fn parallel_incident(provider: &Provider, rows: &[Mono], workers: usize) -> HashSet<Column> {
    if workers == 1 || rows.len() < 64 {
        let mut cache = HashMap::new();
        let mut out = HashSet::new();
        for &row in rows { incident_columns_pure(provider, row, &mut cache, &mut out); }
        return out;
    }
    let chunk_size = rows.len().div_ceil(workers).max(1);
    thread::scope(|scope| {
        let mut handles = Vec::new();
        for chunk in rows.chunks(chunk_size) {
            handles.push(scope.spawn(move || {
                let mut cache = HashMap::new();
                let mut out = HashSet::new();
                for &row in chunk { incident_columns_pure(provider, row, &mut cache, &mut out); }
                out
            }));
        }
        let mut answer = HashSet::new();
        for handle in handles { answer.extend(handle.join().unwrap_or_else(|_| fail("row worker panicked"))); }
        answer
    })
}

fn parallel_outputs(provider: &Provider, columns: &[Column], workers: usize) -> HashSet<Mono> {
    if workers == 1 || columns.len() < 16 {
        let mut cache = HashMap::new();
        let mut out = HashSet::new();
        for &column in columns { output_rows_pure(provider, column, &mut cache, &mut out); }
        return out;
    }
    let chunk_size = columns.len().div_ceil(workers).max(1);
    thread::scope(|scope| {
        let mut handles = Vec::new();
        for chunk in columns.chunks(chunk_size) {
            handles.push(scope.spawn(move || {
                let mut cache = HashMap::new();
                let mut out = HashSet::new();
                for &column in chunk { output_rows_pure(provider, column, &mut cache, &mut out); }
                out
            }));
        }
        let mut answer = HashSet::new();
        for handle in handles { answer.extend(handle.join().unwrap_or_else(|_| fail("column worker panicked"))); }
        answer
    })
}

fn parallel_invariant_columns(provider: &Provider, columns: &[Column], prime: u64,
                              workers: usize) -> Vec<Vec<(Mono, u64)>> {
    if workers == 1 || columns.len() < 16 {
        let mut cache = HashMap::new();
        return columns.iter().map(|&column| invariant_column_pure(provider, column, prime, &mut cache)).collect();
    }
    let chunk_size = columns.len().div_ceil(workers).max(1);
    thread::scope(|scope| {
        let mut handles = Vec::new();
        for chunk in columns.chunks(chunk_size) {
            handles.push(scope.spawn(move || {
                let mut cache = HashMap::new();
                chunk.iter().map(|&column| invariant_column_pure(provider, column, prime, &mut cache))
                    .collect::<Vec<_>>()
            }));
        }
        let mut answer = Vec::with_capacity(columns.len());
        for handle in handles { answer.extend(handle.join().unwrap_or_else(|_| fail("matrix worker panicked"))); }
        answer
    })
}

impl Gate {
    fn new(wall_seconds: u64, rss_gib: u64) -> Self {
        let now = Instant::now();
        Self {
            started: now,
            wall: Duration::from_secs(wall_seconds),
            rss_limit_kib: rss_gib * 1024 * 1024,
            peak_rss_kib: 0,
            last_rss_check: now - Duration::from_secs(60),
        }
    }

    fn elapsed(&self) -> f64 { self.started.elapsed().as_secs_f64() }

    fn check(&mut self) -> Result<(), &'static str> {
        if self.started.elapsed() >= self.wall { return Err("WALL_CAP"); }
        if self.last_rss_check.elapsed() >= Duration::from_secs(5) {
            self.last_rss_check = Instant::now();
            let pid = std::process::id().to_string();
            if let Ok(output) = Command::new("ps").args(["-o", "rss=", "-p", &pid]).output() {
                if let Ok(text) = String::from_utf8(output.stdout) {
                    if let Ok(rss) = text.trim().parse::<u64>() {
                        self.peak_rss_kib = self.peak_rss_kib.max(rss);
                        if rss >= self.rss_limit_kib { return Err("RSS_CAP"); }
                    }
                }
            }
        }
        Ok(())
    }
}

fn write_mono<W: Write>(out: &mut W, value: Mono) {
    out.write_all(&[value.len]).unwrap_or_else(|e| fail(e.to_string()));
    out.write_all(&value.ids).unwrap_or_else(|e| fail(e.to_string()));
}

fn read_mono<R: Read>(input: &mut R) -> Mono {
    let mut len = [0u8; 1];
    let mut ids = [0u8; MAX_DEGREE];
    input.read_exact(&mut len).unwrap_or_else(|e| fail(e.to_string()));
    input.read_exact(&mut ids).unwrap_or_else(|e| fail(e.to_string()));
    if len[0] as usize > MAX_DEGREE || !ids[..len[0] as usize].windows(2).all(|w| w[0] <= w[1]) {
        fail("bad checkpoint monomial");
    }
    Mono { len: len[0], ids }
}

fn write_u64<W: Write>(out: &mut W, value: u64) {
    out.write_all(&value.to_le_bytes()).unwrap_or_else(|e| fail(e.to_string()));
}

fn read_u64<R: Read>(input: &mut R) -> u64 {
    let mut bytes = [0u8; 8];
    input.read_exact(&mut bytes).unwrap_or_else(|e| fail(e.to_string()));
    u64::from_le_bytes(bytes)
}

fn write_checkpoint(path: &Path, degree: usize, closure: &Closure) {
    let tmp = path.with_extension("bin.tmp");
    let mut out = BufWriter::new(File::create(&tmp).unwrap_or_else(|e| fail(e.to_string())));
    out.write_all(CHECKPOINT_MAGIC).unwrap();
    out.write_all(&[degree as u8, closure.complete as u8]).unwrap();
    write_u64(&mut out, closure.rows.len() as u64);
    write_u64(&mut out, closure.columns.len() as u64);
    write_u64(&mut out, closure.row_frontier.len() as u64);
    write_u64(&mut out, closure.column_frontier.len() as u64);
    let mut rows: Vec<_> = closure.rows.iter().copied().collect(); rows.sort_unstable();
    let mut columns: Vec<_> = closure.columns.iter().copied().collect(); columns.sort_unstable();
    for row in rows { write_mono(&mut out, row); }
    for column in columns {
        out.write_all(&column.word.to_le_bytes()).unwrap(); write_mono(&mut out, column.multiplier);
    }
    for &row in &closure.row_frontier { write_mono(&mut out, row); }
    for &column in &closure.column_frontier {
        out.write_all(&column.word.to_le_bytes()).unwrap(); write_mono(&mut out, column.multiplier);
    }
    out.flush().unwrap(); drop(out);
    fs::rename(tmp, path).unwrap_or_else(|e| fail(e.to_string()));
}

fn read_checkpoint(path: &Path, degree: usize) -> Option<Closure> {
    if !path.exists() { return None; }
    let mut input = BufReader::new(File::open(path).unwrap_or_else(|e| fail(e.to_string())));
    let mut magic = [0u8; 12]; input.read_exact(&mut magic).unwrap_or_else(|e| fail(e.to_string()));
    if &magic != CHECKPOINT_MAGIC { fail("bad closure checkpoint magic"); }
    let mut header = [0u8; 2]; input.read_exact(&mut header).unwrap();
    if header[0] as usize != degree || header[1] > 1 { fail("checkpoint degree/status mismatch"); }
    let nr = read_u64(&mut input) as usize;
    let nc = read_u64(&mut input) as usize;
    let nrf = read_u64(&mut input) as usize;
    let ncf = read_u64(&mut input) as usize;
    let mut closure = Closure { complete: header[1] == 1, ..Closure::default() };
    for _ in 0..nr { if !closure.rows.insert(read_mono(&mut input)) { fail("duplicate checkpoint row"); } }
    for _ in 0..nc {
        let mut bytes = [0u8; 2]; input.read_exact(&mut bytes).unwrap();
        let column = Column { word: u16::from_le_bytes(bytes), multiplier: read_mono(&mut input) };
        if column.word as usize >= N_WORDS || !closure.columns.insert(column) { fail("bad checkpoint column"); }
    }
    for _ in 0..nrf { closure.row_frontier.push_back(read_mono(&mut input)); }
    for _ in 0..ncf {
        let mut bytes = [0u8; 2]; input.read_exact(&mut bytes).unwrap();
        closure.column_frontier.push_back(Column { word: u16::from_le_bytes(bytes), multiplier: read_mono(&mut input) });
    }
    let mut trailing = [0u8; 1];
    if input.read(&mut trailing).unwrap_or_else(|e| fail(e.to_string())) != 0 { fail("trailing checkpoint bytes"); }
    Some(closure)
}

fn compute_closure(engine: &mut OrbitEngine, degree: usize, checkpoint: &Path, gate: &mut Gate,
                   workers: usize)
    -> Result<Closure, &'static str>
{
    let target = Mono::new(vec![T_ID; degree]);
    let mut closure = read_checkpoint(checkpoint, degree).unwrap_or_else(|| {
        let target = engine.row_info(target).canonical;
        let mut value = Closure::default();
        value.rows.insert(target); value.row_frontier.push_back(target); value
    });
    if closure.complete { return Ok(closure); }
    let mut last_checkpoint = Instant::now();
    while !closure.row_frontier.is_empty() || !closure.column_frontier.is_empty() {
        let before_rows = closure.rows.len();
        let before_columns = closure.columns.len();
        let mut processed_rows = 0usize;
        let mut processed_columns = 0usize;
        while !closure.row_frontier.is_empty() {
            if let Err(reason) = gate.check() { write_checkpoint(checkpoint, degree, &closure); return Err(reason); }
            let take = closure.row_frontier.len().min(32768);
            let batch: Vec<_> = closure.row_frontier.drain(..take).collect();
            for column in parallel_incident(&engine.provider, &batch, workers) {
                if column.multiplier.len as usize != degree - GENERATOR_DEGREE {
                    fail("incident multiplier has wrong degree");
                }
                if closure.columns.insert(column) { closure.column_frontier.push_back(column); }
            }
            processed_rows += batch.len();
            if last_checkpoint.elapsed() >= Duration::from_secs(60) {
                write_checkpoint(checkpoint, degree, &closure); last_checkpoint = Instant::now();
            }
        }
        while !closure.column_frontier.is_empty() {
            if let Err(reason) = gate.check() { write_checkpoint(checkpoint, degree, &closure); return Err(reason); }
            let take = closure.column_frontier.len().min(8192);
            let batch: Vec<_> = closure.column_frontier.drain(..take).collect();
            for row in parallel_outputs(&engine.provider, &batch, workers) {
                if row.len as usize != degree { fail("output row has wrong degree"); }
                if closure.rows.insert(row) { closure.row_frontier.push_back(row); }
            }
            processed_columns += batch.len();
            if last_checkpoint.elapsed() >= Duration::from_secs(60) {
                write_checkpoint(checkpoint, degree, &closure); last_checkpoint = Instant::now();
            }
        }
        closure.rounds.push((processed_rows, processed_columns,
            closure.rows.len() - before_rows, closure.columns.len() - before_columns));
        write_checkpoint(checkpoint, degree, &closure);
        eprintln!("closure degree={degree} round={} rows={} columns={} frontier={} elapsed={:.3}s rss_peak_kib={}",
            closure.rounds.len(), closure.rows.len(), closure.columns.len(), closure.row_frontier.len(),
            gate.elapsed(), gate.peak_rss_kib);
    }
    closure.complete = true;
    write_checkpoint(checkpoint, degree, &closure);
    Ok(closure)
}

fn add_scaled(target: &mut BTreeMap<usize, u64>, source: &[(usize, u64)], factor: u64, prime: u64) {
    if factor == 0 { return; }
    for &(row, coefficient) in source {
        let old = target.get(&row).copied().unwrap_or(0);
        let subtract = (factor as u128 * coefficient as u128 % prime as u128) as u64;
        let value = if old >= subtract { old - subtract } else { old + prime - subtract };
        if value == 0 { target.remove(&row); } else { target.insert(row, value); }
    }
}

fn inverse_mod(mut base: u64, prime: u64) -> u64 {
    let mut exponent = prime - 2;
    let mut answer = 1u64;
    while exponent != 0 {
        if exponent & 1 != 0 { answer = (answer as u128 * base as u128 % prime as u128) as u64; }
        base = (base as u128 * base as u128 % prime as u128) as u64;
        exponent >>= 1;
    }
    answer
}

fn reduce_vector(mut vector: BTreeMap<usize, u64>, basis: &[Option<Vec<(usize, u64)>>], prime: u64,
                 pivot_last: bool)
    -> BTreeMap<usize, u64>
{
    loop {
        let entry = if pivot_last { vector.last_key_value() } else { vector.first_key_value() };
        let Some((&pivot, &value)) = entry else { return vector; };
        let Some(record) = basis[pivot].as_ref() else { return vector; };
        add_scaled(&mut vector, record, value, prime);
    }
}

fn write_dual(path: &Path, prime: u64, rows: &[Mono], values: &HashMap<usize, u64>, pairing: u64) {
    let tmp = path.with_extension("tsv.tmp");
    let mut out = BufWriter::new(File::create(&tmp).unwrap_or_else(|e| fail(e.to_string())));
    let nonzero = values.values().filter(|value| **value != 0).count();
    writeln!(out, "KRENN_AFFINE251_ORBIT_DUAL_V1 {prime} {nonzero} {pairing}").unwrap();
    let mut entries: Vec<_> = values.iter().filter(|(_, value)| **value != 0).collect();
    entries.sort_by_key(|(row, _)| **row);
    for (&row, &value) in entries { writeln!(out, "ROW {} {} {}", row, mono_hex(rows[row]), value).unwrap(); }
    out.flush().unwrap(); drop(out);
    fs::rename(tmp, path).unwrap_or_else(|e| fail(e.to_string()));
}

struct LinearResult {
    rank: usize,
    nnz: usize,
    target_residual_nnz: usize,
    target_pairing: u64,
    member: bool,
}

fn linear_membership(engine: &mut OrbitEngine, closure: &Closure, degree: usize, prime: u64,
                     dual_path: &Path, gate: &mut Gate, workers: usize, pivot_last: bool)
    -> Result<LinearResult, &'static str>
{
    let mut rows: Vec<_> = closure.rows.iter().copied().collect(); rows.sort_unstable();
    let mut columns: Vec<_> = closure.columns.iter().copied().collect(); columns.sort_unstable();
    let row_id: HashMap<Mono, usize> = rows.iter().enumerate().map(|(i, row)| (*row, i)).collect();
    let mut basis: Vec<Option<Vec<(usize, u64)>>> = vec![None; rows.len()];
    let mut rank = 0usize;
    let mut nnz = 0usize;
    for (batch_index, batch) in columns.chunks(1024).enumerate() {
        gate.check()?;
        let invariants = parallel_invariant_columns(&engine.provider, batch, prime, workers);
        for invariant in invariants {
            nnz += invariant.len();
            let mut vector = BTreeMap::new();
            for (row, coefficient) in invariant {
                let id = *row_id.get(&row).unwrap_or_else(|| fail("matrix row absent from closure"));
                if coefficient != 0 { vector.insert(id, coefficient); }
            }
            vector = reduce_vector(vector, &basis, prime, pivot_last);
            let entry = if pivot_last { vector.last_key_value() } else { vector.first_key_value() };
            if let Some((&pivot, &value)) = entry {
                let inverse = inverse_mod(value, prime);
                let record: Vec<_> = vector.into_iter().map(|(row, coefficient)|
                    (row, (coefficient as u128 * inverse as u128 % prime as u128) as u64)).collect();
                basis[pivot] = Some(record); rank += 1;
            }
        }
        if (batch_index + 1) % 16 == 0 {
            eprintln!("matrix degree={degree} columns={}/{} rank={} nnz={} elapsed={:.3}s rss_peak_kib={}",
                ((batch_index + 1) * 1024).min(columns.len()), columns.len(), rank, nnz,
                gate.elapsed(), gate.peak_rss_kib);
        }
    }
    let target = Mono::new(vec![T_ID; degree]);
    let target_id = *row_id.get(&target).unwrap_or_else(|| fail("target row absent from closure"));
    let mut target_vector = BTreeMap::new(); target_vector.insert(target_id, 1);
    let residual = reduce_vector(target_vector, &basis, prime, pivot_last);
    if residual.is_empty() {
        if dual_path.exists() { fs::remove_file(dual_path).unwrap_or_else(|e| fail(e.to_string())); }
        return Ok(LinearResult { rank, nnz, target_residual_nnz: 0, target_pairing: 0, member: true });
    }
    // Turn one free residual coordinate into an exact left-nullspace witness.
    let (&free_row, _) = if pivot_last { residual.last_key_value().unwrap() }
                         else { residual.first_key_value().unwrap() };
    let mut dual = HashMap::<usize, u64>::new(); dual.insert(free_row, 1);
    let pivot_order: Box<dyn Iterator<Item=usize>> = if pivot_last {
        Box::new(0..basis.len())
    } else {
        Box::new((0..basis.len()).rev())
    };
    for pivot in pivot_order {
        let Some(record) = basis[pivot].as_ref() else { continue; };
        let mut sum = 0u64;
        for &(row, coefficient) in record {
            if row == pivot { continue; }
            let value = dual.get(&row).copied().unwrap_or(0);
            sum = (sum + (coefficient as u128 * value as u128 % prime as u128) as u64) % prime;
        }
        if sum != 0 { dual.insert(pivot, prime - sum); }
    }
    let target_pairing = dual.get(&target_id).copied().unwrap_or(0);
    if target_pairing == 0 { fail("constructed dual does not separate target"); }
    for record in basis.iter().flatten() {
        let pairing = record.iter().fold(0u64, |sum, (row, coefficient)|
            (sum + (*coefficient as u128 * dual.get(row).copied().unwrap_or(0) as u128 % prime as u128) as u64) % prime);
        if pairing != 0 { fail("constructed dual does not annihilate basis"); }
    }
    write_dual(dual_path, prime, &rows, &dual, target_pairing);
    Ok(LinearResult { rank, nnz, target_residual_nnz: residual.len(), target_pairing, member: false })
}

fn parse_args() -> Config {
    let args: Vec<String> = env::args().collect();
    let mut values = HashMap::<String, String>::new();
    let mut index = 1usize;
    while index < args.len() {
        if !args[index].starts_with("--") || index + 1 >= args.len() { fail("expected --key value arguments"); }
        if values.insert(args[index].clone(), args[index + 1].clone()).is_some() { fail("duplicate argument"); }
        index += 2;
    }
    let get = |name: &str| values.get(name).cloned().unwrap_or_else(|| fail(format!("missing {name}")));
    let degree: usize = get("--degree").parse().unwrap_or_else(|_| fail("bad degree"));
    let prime: u64 = get("--prime").parse().unwrap_or_else(|_| fail("bad prime"));
    let wall_seconds: u64 = values.get("--wall-seconds").map(|v| v.parse().unwrap_or_else(|_| fail("bad wall"))).unwrap_or(1800);
    let rss_gib: u64 = values.get("--rss-gib").map(|v| v.parse().unwrap_or_else(|_| fail("bad rss"))).unwrap_or(42);
    let workers: usize = values.get("--workers").map(|v| v.parse().unwrap_or_else(|_| fail("bad workers")))
        .unwrap_or_else(|| thread::available_parallelism().map(|x| x.get().min(16)).unwrap_or(1));
    let pivot_last = match values.get("--pivot").map(String::as_str).unwrap_or("first") {
        "first" => false, "last" => true, _ => fail("pivot must be first or last"),
    };
    if !(4..=MAX_DEGREE).contains(&degree) { fail("degree must be 4..12"); }
    if prime < 10_000 || prime % 2 == 0 || GROUP_ORDER as u64 % prime == 0 { fail("bad prime"); }
    if workers == 0 || workers > 18 { fail("workers must be 1..18"); }
    Config {
        input: PathBuf::from(get("--input")), output: PathBuf::from(get("--output")),
        checkpoint: PathBuf::from(get("--checkpoint")), dual: PathBuf::from(get("--dual")),
        degree, prime, wall_seconds, rss_gib, workers, pivot_last,
    }
}

fn write_result(config: &Config, provider: &Provider, closure: Option<&Closure>, linear: Option<&LinearResult>,
                gate: &Gate, status: &str, reason: Option<&str>) {
    let tmp = config.output.with_extension("json.tmp");
    let mut out = BufWriter::new(File::create(&tmp).unwrap_or_else(|e| fail(e.to_string())));
    let rows = closure.map(|x| x.rows.len()).unwrap_or(0);
    let columns = closure.map(|x| x.columns.len()).unwrap_or(0);
    let complete = closure.map(|x| x.complete).unwrap_or(false);
    let rank = linear.map(|x| x.rank as i64).unwrap_or(-1);
    let nnz = linear.map(|x| x.nnz as i64).unwrap_or(-1);
    let residual = linear.map(|x| x.target_residual_nnz as i64).unwrap_or(-1);
    let pairing = linear.map(|x| x.target_pairing as i128).unwrap_or(-1);
    let member = linear.map(|x| if x.member { "true" } else { "false" }).unwrap_or("null");
    let reason_json = reason.map(|x| format!("\"{}\"", json_escape(x))).unwrap_or("null".into());
    writeln!(out, "{{").unwrap();
    writeln!(out, "  \"schema\": \"KRENN_AFFINE251_ORBIT_MEMBERSHIP_V1\",").unwrap();
    writeln!(out, "  \"status\": \"{status}\",").unwrap();
    writeln!(out, "  \"incomplete_reason\": {reason_json},").unwrap();
    writeln!(out, "  \"input\": \"{}\",", json_escape(&config.input.display().to_string())).unwrap();
    writeln!(out, "  \"degree\": {},", config.degree).unwrap();
    writeln!(out, "  \"prime\": {},", config.prime).unwrap();
    writeln!(out, "  \"variables_affine\": 251,").unwrap();
    writeln!(out, "  \"homogenizing_variable\": 251,").unwrap();
    writeln!(out, "  \"provider_equations\": {},", provider.polynomials.len()).unwrap();
    writeln!(out, "  \"provider_terms_parsed\": {},", provider.parsed_terms).unwrap();
    writeln!(out, "  \"provider_distinct_terms\": {},", provider.distinct_terms).unwrap();
    writeln!(out, "  \"group_order\": {},", GROUP_ORDER).unwrap();
    writeln!(out, "  \"closure_complete\": {complete},").unwrap();
    writeln!(out, "  \"row_orbits\": {rows},").unwrap();
    writeln!(out, "  \"column_orbits\": {columns},").unwrap();
    writeln!(out, "  \"rank\": {rank},").unwrap();
    writeln!(out, "  \"matrix_nnz\": {nnz},").unwrap();
    writeln!(out, "  \"target_residual_nnz\": {residual},").unwrap();
    writeln!(out, "  \"target_pairing\": {pairing},").unwrap();
    writeln!(out, "  \"member_mod_prime\": {member},").unwrap();
    writeln!(out, "  \"wall_limit_seconds\": {},", config.wall_seconds).unwrap();
    writeln!(out, "  \"rss_limit_gib\": {},", config.rss_gib).unwrap();
    writeln!(out, "  \"workers\": {},", config.workers).unwrap();
    writeln!(out, "  \"pivot_order\": \"{}\",", if config.pivot_last { "last" } else { "first" }).unwrap();
    writeln!(out, "  \"elapsed_seconds\": {:.6},", gate.elapsed()).unwrap();
    writeln!(out, "  \"peak_rss_kib\": {},", gate.peak_rss_kib).unwrap();
    writeln!(out, "  \"checkpoint\": \"{}\",", json_escape(&config.checkpoint.display().to_string())).unwrap();
    writeln!(out, "  \"dual\": \"{}\"", json_escape(&config.dual.display().to_string())).unwrap();
    writeln!(out, "}}").unwrap();
    out.flush().unwrap(); drop(out);
    fs::rename(tmp, &config.output).unwrap_or_else(|e| fail(e.to_string()));
}

// Sparse, dual-first D12 constraint generation.  This entry point lives here
// so the optimized provider and symmetry kernels above remain a single source
// of truth for both binaries.
const SPARSE_CHECKPOINT_MAGIC: &[u8; 12] = b"AFF12CEG1\0\0\0";
const SPARSE_VECTOR_MAGIC: &[u8; 12] = b"AFF12VEC1\0\0\0";

#[derive(Clone, Copy)]
enum SparsePivot { First, Last, Rare }

impl SparsePivot {
    fn name(self) -> &'static str {
        match self { Self::First => "first", Self::Last => "last", Self::Rare => "rare" }
    }
}

struct SparseConfig {
    input: PathBuf,
    output: PathBuf,
    checkpoint: PathBuf,
    dual: PathBuf,
    vector_cache: PathBuf,
    seed_dual: Option<PathBuf>,
    prime: u64,
    wall_seconds: u64,
    rss_gib: u64,
    workers: usize,
    pivot: String,
    strategy: String,
    elimination: String,
    incremental: bool,
    portfolio_period: usize,
    portfolio_parallel: bool,
    support_cap: usize,
    column_cap: usize,
    round_cap: usize,
}

#[derive(Clone)]
struct SparseRound {
    index: usize,
    columns: usize,
    new_columns: usize,
    support: usize,
    new_support_rows: usize,
    strategy: String,
    pivot: String,
    incident_seconds: f64,
    materialize_seconds: f64,
    solve_seconds: f64,
}

struct SparseRestoreStats {
    cached_vectors_loaded: usize,
    vectors_materialized_on_restore: usize,
    restore_seconds: f64,
}

fn sparse_parse_args() -> SparseConfig {
    let args: Vec<String> = env::args().collect();
    let mut values = HashMap::<String, String>::new();
    let mut index = 1usize;
    while index < args.len() {
        if !args[index].starts_with("--") || index + 1 >= args.len() { fail("expected --key value arguments"); }
        if values.insert(args[index].clone(), args[index + 1].clone()).is_some() { fail("duplicate argument"); }
        index += 2;
    }
    let get = |name: &str| values.get(name).cloned().unwrap_or_else(|| fail(format!("missing {name}")));
    let prime = get("--prime").parse().unwrap_or_else(|_| fail("bad prime"));
    let wall_seconds = values.get("--wall-seconds").map(|x| x.parse().unwrap_or_else(|_| fail("bad wall"))).unwrap_or(600);
    let rss_gib = values.get("--rss-gib").map(|x| x.parse().unwrap_or_else(|_| fail("bad rss"))).unwrap_or(8);
    let workers = values.get("--workers").map(|x| x.parse().unwrap_or_else(|_| fail("bad workers")))
        .unwrap_or_else(|| thread::available_parallelism().map(|x| x.get().min(16)).unwrap_or(1));
    let pivot = values.get("--pivot").cloned().unwrap_or_else(|| "auto".into());
    let strategy = values.get("--strategy").cloned().unwrap_or_else(|| "best".into());
    let elimination = values.get("--elimination").cloned().unwrap_or_else(|| "tree".into());
    let incremental = match values.get("--incremental").map(String::as_str).unwrap_or("no") {
        "yes" => true, "no" => false, _ => fail("incremental must be yes or no"),
    };
    let portfolio_period = values.get("--portfolio-period").map(|x|
        x.parse().unwrap_or_else(|_| fail("bad portfolio period"))).unwrap_or(32);
    let portfolio_parallel = match values.get("--portfolio-parallel").map(String::as_str).unwrap_or("yes") {
        "yes" => true, "no" => false, _ => fail("portfolio parallel must be yes or no"),
    };
    let support_cap = values.get("--support-cap").map(|x| x.parse().unwrap_or_else(|_| fail("bad support cap"))).unwrap_or(100_000);
    let column_cap = values.get("--column-cap").map(|x| x.parse().unwrap_or_else(|_| fail("bad column cap"))).unwrap_or(1_000_000);
    let round_cap = values.get("--round-cap").map(|x| x.parse().unwrap_or_else(|_| fail("bad round cap"))).unwrap_or(100);
    if prime < 10_000 || prime % 2 == 0 || GROUP_ORDER as u64 % prime == 0 { fail("bad prime"); }
    if workers == 0 || workers > 18 { fail("workers must be 1..18"); }
    if wall_seconds == 0 || wall_seconds > 1800 || rss_gib == 0 || rss_gib > 42 { fail("resource cap out of contract"); }
    if !matches!(pivot.as_str(), "first" | "last" | "rare" | "auto") { fail("bad sparse pivot"); }
    if !matches!(strategy.as_str(), "cold" | "repair" | "best") { fail("bad sparse strategy"); }
    if !matches!(elimination.as_str(), "tree" | "vec" | "hierarchical") {
        fail("bad sparse elimination kernel");
    }
    if incremental && elimination != "tree" { fail("incremental mode requires tree elimination"); }
    if elimination == "hierarchical"
        && (workers != 16 || pivot != "rare" || strategy != "cold" || incremental)
    {
        fail("hierarchical elimination requires explicit --workers 16 --pivot rare --strategy cold --incremental no");
    }
    if support_cap < 7 || column_cap < 17 || round_cap == 0 || round_cap > 1000
        || portfolio_period == 0 || portfolio_period > 256 { fail("bad sparse search cap"); }
    let checkpoint = PathBuf::from(get("--checkpoint"));
    let vector_cache = values.get("--vector-cache").map(PathBuf::from)
        .unwrap_or_else(|| checkpoint.with_extension("vectors.bin"));
    SparseConfig {
        input: PathBuf::from(get("--input")),
        output: PathBuf::from(get("--output")),
        checkpoint,
        dual: PathBuf::from(get("--dual")),
        vector_cache,
        seed_dual: values.get("--seed-dual").map(PathBuf::from),
        prime, wall_seconds, rss_gib, workers, pivot, strategy, elimination, incremental,
        portfolio_period, portfolio_parallel,
        support_cap, column_cap, round_cap,
    }
}

fn sparse_parallel_incident_lists(provider: &Provider, rows: &[Mono], workers: usize)
    -> Vec<(Mono, Vec<Column>)>
{
    if workers == 1 || rows.len() < 8 {
        let mut cache = HashMap::new();
        return rows.iter().map(|&row| {
            let mut set = HashSet::new();
            incident_columns_pure(provider, row, &mut cache, &mut set);
            let mut columns: Vec<_> = set.into_iter().collect(); columns.sort_unstable();
            (row, columns)
        }).collect();
    }
    let chunk_size = rows.len().div_ceil(workers).max(1);
    thread::scope(|scope| {
        let mut handles = Vec::new();
        for chunk in rows.chunks(chunk_size) {
            handles.push(scope.spawn(move || {
                let mut cache = HashMap::new();
                let mut answer = Vec::with_capacity(chunk.len());
                for &row in chunk {
                    let mut set = HashSet::new();
                    incident_columns_pure(provider, row, &mut cache, &mut set);
                    let mut columns: Vec<_> = set.into_iter().collect(); columns.sort_unstable();
                    answer.push((row, columns));
                }
                answer
            }));
        }
        let mut answer = Vec::with_capacity(rows.len());
        for handle in handles { answer.extend(handle.join().unwrap_or_else(|_| fail("sparse incident worker panicked"))); }
        answer.sort_unstable_by_key(|x| x.0);
        answer
    })
}

fn sparse_pairing(vector: &[(Mono, u64)], candidate: &HashMap<Mono, u64>, prime: u64) -> u64 {
    vector.iter().fold(0u64, |sum, (row, coefficient)| {
        let product = (*coefficient as u128 * candidate.get(row).copied().unwrap_or(0) as u128
            % prime as u128) as u64;
        let value = sum + product;
        if value >= prime { value - prime } else { value }
    })
}

fn sparse_sub_scaled(target: &mut BTreeMap<Mono, u64>, source: &BTreeMap<Mono, u64>,
                     factor: u64, prime: u64) {
    if factor == 0 { return; }
    for (&row, &coefficient) in source {
        let old = target.get(&row).copied().unwrap_or(0);
        let subtract = (factor as u128 * coefficient as u128 % prime as u128) as u64;
        let value = if old >= subtract { old - subtract } else { old + prime - subtract };
        if value == 0 { target.remove(&row); } else { target.insert(row, value); }
    }
}

fn sparse_compare_rows(left: &Mono, right: &Mono, pivot: SparsePivot,
                       frequency: &HashMap<Mono, usize>) -> std::cmp::Ordering {
    match pivot {
        SparsePivot::First => left.cmp(right),
        SparsePivot::Last => right.cmp(left),
        SparsePivot::Rare => (frequency.get(left).copied().unwrap_or(usize::MAX), left)
            .cmp(&(frequency.get(right).copied().unwrap_or(usize::MAX), right)),
    }
}

fn sparse_choose_pivot(vector: &BTreeMap<Mono, u64>, pivot: SparsePivot,
                       frequency: &HashMap<Mono, usize>) -> Mono {
    *vector.keys().min_by(|a, b| sparse_compare_rows(a, b, pivot, frequency)).unwrap()
}

// Exact fixed-order hierarchical echelon kernel.  This is deliberately only
// selectable for the cold/rare/16-worker path; all other solver modes retain
// their established implementations.
#[derive(Clone, Copy)]
struct HierarchicalTerm { rank: u32, value: u32 }

struct HierarchicalEquation { terms: Vec<HierarchicalTerm>, rhs: u32 }

struct HierarchicalRecord { terms: Vec<HierarchicalTerm>, rhs: u32 }

struct HierarchicalBasis {
    records: HashMap<u32, HierarchicalRecord>,
    inconsistent: bool,
}

struct HierarchicalRankMetrics {
    ordered_sort_seconds: f64,
    rank_map_build_seconds: f64,
    compact_materialize_seconds: f64,
    shard_min_rows: usize,
    shard_max_rows: usize,
}

#[derive(Default)]
struct HierarchicalFnvHasher(u64);

impl Hasher for HierarchicalFnvHasher {
    fn finish(&self) -> u64 { self.0 }

    fn write(&mut self, bytes: &[u8]) {
        let mut hash = if self.0 == 0 { 0xcbf29ce484222325 } else { self.0 };
        for byte in bytes {
            hash ^= *byte as u64;
            hash = hash.wrapping_mul(0x100000001b3);
        }
        self.0 = hash;
    }
}

type HierarchicalRankMap =
    HashMap<Mono, u32, BuildHasherDefault<HierarchicalFnvHasher>>;

fn hierarchical_row_hash(row: &Mono) -> u64 {
    let mut hasher = HierarchicalFnvHasher::default();
    hasher.write(&[row.len]);
    hasher.write(&row.ids);
    hasher.finish()
}

fn hierarchical_materialize_chunk(
    columns: &[Column], vectors: &HashMap<Column, Vec<(Mono, u64)>>,
    rank_maps: &[HierarchicalRankMap], rank_shards: usize,
    target: Mono, prime: u32,
) -> Vec<HierarchicalEquation> {
    let mut equations = Vec::with_capacity(columns.len());
    for column in columns {
        let raw = &vectors[column];
        let target_coefficient = raw.iter().find_map(|(row, coefficient)|
            if *row == target { Some(*coefficient) } else { None }).unwrap_or(0);
        let target32 = u32::try_from(target_coefficient)
            .unwrap_or_else(|_| fail("hierarchical target residue exceeds u32"));
        let rhs = if target32 == 0 { 0 } else { prime - target32 };
        let mut terms = Vec::with_capacity(raw.len());
        for &(row, value) in raw {
            if row != target && value != 0 {
                let shard = hierarchical_row_hash(&row) as usize & (rank_shards - 1);
                let dense = rank_maps[shard].get(&row).copied()
                    .unwrap_or_else(|| fail("hierarchical row absent from sharded rare census"));
                let value32 = u32::try_from(value)
                    .unwrap_or_else(|_| fail("hierarchical residue exceeds u32"));
                terms.push(HierarchicalTerm { rank: dense, value: value32 });
            }
        }
        terms.sort_unstable_by_key(|term| term.rank);
        if terms.windows(2).any(|pair| pair[0].rank >= pair[1].rank) {
            fail("hierarchical equation ranks are not strict");
        }
        equations.push(HierarchicalEquation { terms, rhs });
    }
    equations
}

fn hierarchical_rank_and_materialize(
    columns: &[Column], vectors: &HashMap<Column, Vec<(Mono, u64)>>,
    frequency: &HashMap<Mono, usize>, workers: usize, rank_shards: usize,
    target: Mono, prime: u32,
) -> (Vec<HierarchicalEquation>, Vec<Mono>, HierarchicalRankMetrics) {
    if !rank_shards.is_power_of_two() || rank_shards > 64 {
        fail("hierarchical rank shards must be a power of two at most 64");
    }
    let sort_started = Instant::now();
    let mut ordered: Vec<(u32, Mono)> = frequency.iter().map(|(&row, &count)| {
        let count32 = u32::try_from(count)
            .unwrap_or_else(|_| fail("hierarchical frequency exceeds u32"));
        (count32, row)
    }).collect();
    ordered.sort_unstable();
    if ordered.windows(2).any(|pair| pair[0] >= pair[1]) {
        fail("hierarchical owned frequency/row sort order");
    }
    let rows_by_rank: Vec<Mono> = ordered.into_iter().map(|item| item.1).collect();
    if rows_by_rank.len() >= u32::MAX as usize { fail("hierarchical rare rank overflow"); }
    let ordered_sort_seconds = sort_started.elapsed().as_secs_f64();

    let map_started = Instant::now();
    let mut buckets: Vec<Vec<(Mono, u32)>> = (0..rank_shards)
        .map(|_| Vec::with_capacity(rows_by_rank.len() / rank_shards + 1)).collect();
    for (rank, row) in rows_by_rank.iter().copied().enumerate() {
        if row == target { fail("target present in hierarchical rare census"); }
        let shard = hierarchical_row_hash(&row) as usize & (rank_shards - 1);
        buckets[shard].push((row, rank as u32));
    }
    let shard_min_rows = buckets.iter().map(Vec::len).min().unwrap_or(0);
    let shard_max_rows = buckets.iter().map(Vec::len).max().unwrap_or(0);
    let rank_maps: Vec<HierarchicalRankMap> = thread::scope(|scope| {
        let handles: Vec<_> = buckets.into_iter().map(|bucket| scope.spawn(move || {
            let mut map = HierarchicalRankMap::with_capacity_and_hasher(
                bucket.len(), BuildHasherDefault::default());
            for (row, rank) in bucket {
                if map.insert(row, rank).is_some() {
                    fail("duplicate hierarchical sharded rank row");
                }
            }
            map
        })).collect();
        handles.into_iter().map(|handle| handle.join()
            .unwrap_or_else(|_| fail("hierarchical rank map worker panicked"))).collect()
    });
    if rank_maps.iter().map(HashMap::len).sum::<usize>() != rows_by_rank.len() {
        fail("hierarchical rank shard census");
    }
    let rank_map_build_seconds = map_started.elapsed().as_secs_f64();

    let materialize_started = Instant::now();
    let base = columns.len() / workers;
    let remainder = columns.len() % workers;
    let chunk_results = thread::scope(|scope| {
        let mut handles = Vec::with_capacity(workers);
        let mut begin = 0usize;
        for worker in 0..workers {
            let count = base + usize::from(worker < remainder);
            let slice = &columns[begin..begin + count];
            let maps = &rank_maps;
            handles.push(scope.spawn(move || hierarchical_materialize_chunk(
                slice, vectors, maps, rank_shards, target, prime)));
            begin += count;
        }
        handles.into_iter().map(|handle| handle.join()
            .unwrap_or_else(|_| fail("hierarchical materialization worker panicked")))
            .collect::<Vec<_>>()
    });
    let mut equations = Vec::with_capacity(columns.len());
    for mut chunk in chunk_results { equations.append(&mut chunk); }
    if equations.len() != columns.len() { fail("hierarchical materialized equation census"); }
    drop(rank_maps);
    let compact_materialize_seconds = materialize_started.elapsed().as_secs_f64();
    (equations, rows_by_rank, HierarchicalRankMetrics {
        ordered_sort_seconds, rank_map_build_seconds, compact_materialize_seconds,
        shard_min_rows, shard_max_rows,
    })
}

fn hierarchical_subtract(left: u32, right: u32, prime: u32) -> u32 {
    if left >= right { left - right } else { left + prime - right }
}

fn hierarchical_multiply(left: u32, right: u32, prime: u32) -> u32 {
    (left as u64 * right as u64 % prime as u64) as u32
}

fn hierarchical_sub_scaled(target: &[HierarchicalTerm], source: &[HierarchicalTerm],
                           factor: u32, prime: u32) -> Vec<HierarchicalTerm> {
    let mut answer = Vec::with_capacity(target.len() + source.len());
    let (mut left, mut right) = (0usize, 0usize);
    while left < target.len() || right < source.len() {
        if right == source.len()
            || (left < target.len() && target[left].rank < source[right].rank)
        {
            answer.push(target[left]); left += 1;
        } else if left == target.len() || source[right].rank < target[left].rank {
            let subtract = hierarchical_multiply(factor, source[right].value, prime);
            if subtract != 0 {
                answer.push(HierarchicalTerm { rank: source[right].rank,
                                               value: prime - subtract });
            }
            right += 1;
        } else {
            let value = hierarchical_subtract(target[left].value,
                hierarchical_multiply(factor, source[right].value, prime), prime);
            if value != 0 { answer.push(HierarchicalTerm { rank: target[left].rank, value }); }
            left += 1; right += 1;
        }
    }
    answer
}

impl HierarchicalBasis {
    fn empty(capacity: usize) -> Self {
        Self { records: HashMap::with_capacity(capacity), inconsistent: false }
    }

    fn add(&mut self, mut terms: Vec<HierarchicalTerm>, mut rhs: u32, prime: u32) {
        if self.inconsistent { return; }
        loop {
            if terms.is_empty() {
                if rhs != 0 { self.inconsistent = true; }
                return;
            }
            let pivot = terms[0].rank;
            let factor = terms[0].value;
            if let Some(record) = self.records.get(&pivot) {
                terms = hierarchical_sub_scaled(&terms, &record.terms, factor, prime);
                rhs = hierarchical_subtract(rhs,
                    hierarchical_multiply(factor, record.rhs, prime), prime);
                continue;
            }
            let inverse = inverse_mod(factor as u64, prime as u64) as u32;
            for term in &mut terms {
                term.value = hierarchical_multiply(term.value, inverse, prime);
            }
            rhs = hierarchical_multiply(rhs, inverse, prime);
            if terms[0].value != 1 { fail("hierarchical pivot normalization failed"); }
            if self.records.insert(pivot, HierarchicalRecord { terms, rhs }).is_some() {
                fail("duplicate hierarchical pivot");
            }
            return;
        }
    }

    fn terms(&self) -> usize {
        self.records.values().map(|record| record.terms.len()).sum()
    }
}

fn hierarchical_local(equations: &[HierarchicalEquation], prime: u32)
    -> (HierarchicalBasis, f64)
{
    let local_started = Instant::now();
    let mut basis = HierarchicalBasis::empty(equations.len());
    for equation in equations {
        basis.add(equation.terms.clone(), equation.rhs, prime);
        if basis.inconsistent { break; }
    }
    (basis, local_started.elapsed().as_secs_f64())
}

fn hierarchical_merge(mut left: HierarchicalBasis, right: HierarchicalBasis,
                      prime: u32) -> HierarchicalBasis {
    if right.inconsistent { left.inconsistent = true; }
    let mut records: Vec<_> = right.records.into_iter().collect();
    records.sort_unstable_by_key(|item| item.0);
    for (_, record) in records {
        left.add(record.terms, record.rhs, prime);
        if left.inconsistent { break; }
    }
    left
}

fn sparse_solve_correction_hierarchical(
    columns: &[Column], vectors: &HashMap<Column, Vec<(Mono, u64)>>,
    base: &HashMap<Mono, u64>, target: Mono, prime: u64,
    frequency: &HashMap<Mono, usize>, workers: usize,
) -> Option<HashMap<Mono, u64>> {
    if workers != 16 || base.len() != 1 || base.get(&target).copied() != Some(1) {
        fail("hierarchical kernel requires cold target-only base and 16 workers");
    }
    let prime32 = u32::try_from(prime)
        .unwrap_or_else(|_| fail("hierarchical kernel requires a u32 prime"));
    // The rank order is still the exact natural (frequency,row) order.  FNV
    // only selects one of 16 lookup shards and therefore cannot affect pivots.
    let (equations, rows_by_rank, rank_metrics) = hierarchical_rank_and_materialize(
        columns, vectors, frequency, workers, 16, target, prime32);

    let base_count = equations.len() / workers;
    let remainder = equations.len() % workers;
    let local_started = Instant::now();
    let bases = thread::scope(|scope| {
        let mut handles = Vec::with_capacity(workers);
        let mut begin = 0usize;
        for worker in 0..workers {
            let count = base_count + usize::from(worker < remainder);
            let slice = &equations[begin..begin + count];
            handles.push(scope.spawn(move || hierarchical_local(slice, prime32)));
            begin += count;
        }
        handles.into_iter().map(|handle|
            handle.join().unwrap_or_else(|_| fail("hierarchical local worker panicked")))
            .collect::<Vec<_>>()
    });
    let local_eliminate_seconds = bases.iter().map(|item| item.1).fold(0.0f64, f64::max);
    let mut bases: Vec<HierarchicalBasis> = bases.into_iter().map(|item| item.0).collect();
    if bases.iter().any(|basis| basis.inconsistent) { return None; }
    let local_wall_seconds = local_started.elapsed().as_secs_f64();
    let merge_started = Instant::now();
    let mut levels = 0usize;
    while bases.len() > 1 {
        if bases.len() % 2 != 0 { fail("hierarchical merge tree is not pairable"); }
        let mut pairs = Vec::with_capacity(bases.len() / 2);
        let mut iterator = bases.into_iter();
        while let Some(left) = iterator.next() { pairs.push((left, iterator.next().unwrap())); }
        bases = thread::scope(|scope| {
            let handles: Vec<_> = pairs.into_iter().map(|(left, right)|
                scope.spawn(move || hierarchical_merge(left, right, prime32))).collect();
            handles.into_iter().map(|handle|
                handle.join().unwrap_or_else(|_| fail("hierarchical merge worker panicked")))
                .collect()
        });
        if bases.iter().any(|basis| basis.inconsistent) { return None; }
        levels += 1;
    }
    if levels != 4 { fail("hierarchical merge tree did not have four levels"); }
    let merge_seconds = merge_started.elapsed().as_secs_f64();
    let basis = bases.pop().unwrap();
    let basis_records = basis.records.len();
    let basis_terms = basis.terms();
    let mut pivots: Vec<_> = basis.records.keys().copied().collect();
    pivots.sort_unstable();
    let backsolve_started = Instant::now();
    let mut values = vec![0u32; rows_by_rank.len()];
    for pivot in pivots.into_iter().rev() {
        let record = &basis.records[&pivot];
        if !record.terms.first().is_some_and(|term| term.rank == pivot && term.value == 1) {
            fail("hierarchical backsolve pivot changed");
        }
        let mut value = record.rhs;
        for term in &record.terms[1..] {
            value = hierarchical_subtract(value,
                hierarchical_multiply(term.value, values[term.rank as usize], prime32), prime32);
        }
        values[pivot as usize] = value;
    }
    let backsolve_seconds = backsolve_started.elapsed().as_secs_f64();
    let mut answer = base.clone();
    for (index, value) in values.into_iter().enumerate() {
        if value != 0 { answer.insert(rows_by_rank[index], value as u64); }
    }
    let verify_started = Instant::now();
    if answer.get(&target).copied() != Some(1)
        || columns.iter().any(|column| sparse_pairing(&vectors[column], &answer, prime) != 0)
    {
        fail("hierarchical solver returned a violating candidate");
    }
    let verify_seconds = verify_started.elapsed().as_secs_f64();
    eprintln!("hierarchical cold/rare columns={} variables={} basis={} terms={} ordered_sort={:.6}s rank_map={:.6}s materialize={:.6}s rank_shard_min={} rank_shard_max={} local_eliminate_critical={:.6}s local_wall={:.6}s merge={:.6}s backsolve={:.6}s verify={:.6}s support={}",
        columns.len(), rows_by_rank.len(), basis_records, basis_terms,
        rank_metrics.ordered_sort_seconds, rank_metrics.rank_map_build_seconds,
        rank_metrics.compact_materialize_seconds, rank_metrics.shard_min_rows,
        rank_metrics.shard_max_rows, local_eliminate_seconds, local_wall_seconds,
        merge_seconds, backsolve_seconds, verify_seconds, answer.len());
    Some(answer)
}

fn sparse_solve_correction(columns: &[Column], vectors: &HashMap<Column, Vec<(Mono, u64)>>,
                           base: &HashMap<Mono, u64>, target: Mono, prime: u64,
                           pivot_mode: SparsePivot, frequency: &HashMap<Mono, usize>)
    -> Option<HashMap<Mono, u64>> {
    let mut basis = HashMap::<Mono, (BTreeMap<Mono, u64>, u64)>::new();
    for column in columns {
        let raw = &vectors[column];
        let pairing = sparse_pairing(raw, base, prime);
        let mut rhs = if pairing == 0 { 0 } else { prime - pairing };
        let mut vector = BTreeMap::<Mono, u64>::new();
        for &(row, coefficient) in raw {
            if row != target && coefficient != 0 { vector.insert(row, coefficient); }
        }
        let mut inserted = false;
        while !vector.is_empty() {
            let pivot = sparse_choose_pivot(&vector, pivot_mode, frequency);
            let value = vector[&pivot];
            if let Some((record, record_rhs)) = basis.get(&pivot) {
                sparse_sub_scaled(&mut vector, record, value, prime);
                let subtract = (value as u128 * *record_rhs as u128 % prime as u128) as u64;
                rhs = if rhs >= subtract { rhs - subtract } else { rhs + prime - subtract };
                continue;
            }
            let inverse = inverse_mod(value, prime);
            for coefficient in vector.values_mut() {
                *coefficient = (*coefficient as u128 * inverse as u128 % prime as u128) as u64;
            }
            rhs = (rhs as u128 * inverse as u128 % prime as u128) as u64;
            basis.insert(pivot, (std::mem::take(&mut vector), rhs));
            inserted = true;
            break;
        }
        if !inserted && rhs != 0 { return None; }
    }
    let mut pivots: Vec<_> = basis.keys().copied().collect();
    pivots.sort_by(|a, b| sparse_compare_rows(a, b, pivot_mode, frequency));
    let mut correction = HashMap::<Mono, u64>::new();
    for pivot in pivots.into_iter().rev() {
        let (record, record_rhs) = &basis[&pivot];
        let mut value = *record_rhs;
        for (&row, &coefficient) in record {
            if row == pivot { continue; }
            let subtract = (coefficient as u128 * correction.get(&row).copied().unwrap_or(0) as u128
                % prime as u128) as u64;
            value = if value >= subtract { value - subtract } else { value + prime - subtract };
        }
        if value != 0 { correction.insert(pivot, value); }
    }
    let mut answer = base.clone();
    for (row, value) in correction {
        let old = answer.get(&row).copied().unwrap_or(0);
        let sum = old + value;
        let sum = if sum >= prime { sum - prime } else { sum };
        if sum == 0 { answer.remove(&row); } else { answer.insert(row, sum); }
    }
    if answer.get(&target).copied() != Some(1) { fail("sparse solver changed target normalization"); }
    if columns.iter().any(|column| sparse_pairing(&vectors[column], &answer, prime) != 0) {
        fail("sparse solver returned a violating candidate");
    }
    Some(answer)
}

fn sparse_sub_scaled_vec(target: &mut Vec<(Mono, u64)>, source: &[(Mono, u64)],
                         factor: u64, prime: u64, scratch: &mut Vec<(Mono, u64)>) {
    if factor == 0 { return; }
    scratch.clear();
    scratch.reserve(target.len() + source.len());
    let (mut left, mut right) = (0usize, 0usize);
    while left < target.len() || right < source.len() {
        if right == source.len() || (left < target.len() && target[left].0 < source[right].0) {
            scratch.push(target[left]);
            left += 1;
        } else if left == target.len() || source[right].0 < target[left].0 {
            let subtract = (factor as u128 * source[right].1 as u128 % prime as u128) as u64;
            if subtract != 0 { scratch.push((source[right].0, prime - subtract)); }
            right += 1;
        } else {
            let subtract = (factor as u128 * source[right].1 as u128 % prime as u128) as u64;
            let old = target[left].1;
            let value = if old >= subtract { old - subtract } else { old + prime - subtract };
            if value != 0 { scratch.push((target[left].0, value)); }
            left += 1;
            right += 1;
        }
    }
    std::mem::swap(target, scratch);
}

fn sparse_solve_correction_vec(columns: &[Column], vectors: &HashMap<Column, Vec<(Mono, u64)>>,
                               base: &HashMap<Mono, u64>, target: Mono, prime: u64,
                               pivot_mode: SparsePivot, frequency: &HashMap<Mono, usize>)
    -> Option<HashMap<Mono, u64>>
{
    let mut basis = HashMap::<Mono, (Vec<(Mono, u64)>, u64)>::new();
    let mut scratch = Vec::<(Mono, u64)>::new();
    for column in columns {
        let raw = &vectors[column];
        let pairing = sparse_pairing(raw, base, prime);
        let mut rhs = if pairing == 0 { 0 } else { prime - pairing };
        let mut vector: Vec<_> = raw.iter().copied()
            .filter(|(row, coefficient)| *row != target && *coefficient != 0).collect();
        let mut inserted = false;
        while !vector.is_empty() {
            let pivot = vector.iter().map(|item| item.0)
                .min_by(|a, b| sparse_compare_rows(a, b, pivot_mode, frequency)).unwrap();
            let value = vector.iter().find(|item| item.0 == pivot).unwrap().1;
            if let Some((record, record_rhs)) = basis.get(&pivot) {
                sparse_sub_scaled_vec(&mut vector, record, value, prime, &mut scratch);
                let subtract = (value as u128 * *record_rhs as u128 % prime as u128) as u64;
                rhs = if rhs >= subtract { rhs - subtract } else { rhs + prime - subtract };
                continue;
            }
            let inverse = inverse_mod(value, prime);
            for (_, coefficient) in &mut vector {
                *coefficient = (*coefficient as u128 * inverse as u128 % prime as u128) as u64;
            }
            rhs = (rhs as u128 * inverse as u128 % prime as u128) as u64;
            basis.insert(pivot, (std::mem::take(&mut vector), rhs));
            inserted = true;
            break;
        }
        if !inserted && rhs != 0 { return None; }
    }
    let mut pivots: Vec<_> = basis.keys().copied().collect();
    pivots.sort_by(|a, b| sparse_compare_rows(a, b, pivot_mode, frequency));
    let mut correction = HashMap::<Mono, u64>::new();
    for pivot in pivots.into_iter().rev() {
        let (record, record_rhs) = &basis[&pivot];
        let mut value = *record_rhs;
        for &(row, coefficient) in record {
            if row == pivot { continue; }
            let subtract = (coefficient as u128 * correction.get(&row).copied().unwrap_or(0) as u128
                % prime as u128) as u64;
            value = if value >= subtract { value - subtract } else { value + prime - subtract };
        }
        if value != 0 { correction.insert(pivot, value); }
    }
    let mut answer = base.clone();
    for (row, value) in correction {
        let old = answer.get(&row).copied().unwrap_or(0);
        let sum = old + value;
        let sum = if sum >= prime { sum - prime } else { sum };
        if sum == 0 { answer.remove(&row); } else { answer.insert(row, sum); }
    }
    if answer.get(&target).copied() != Some(1) { fail("sparse vec solver changed target normalization"); }
    if columns.iter().any(|column| sparse_pairing(&vectors[column], &answer, prime) != 0) {
        fail("sparse vec solver returned a violating candidate");
    }
    Some(answer)
}

// Cold/rare is the stable winner after the exploratory prefix.  Preserve its
// echelon basis between CEGAR rounds, adding only the newly exposed equations.
// The rarity ordering is frozen for a 32-round epoch and rebuilt at the next
// portfolio audit, so triangularity is exact while priorities still adapt.
struct SparseIncremental {
    prime: u64,
    target: Mono,
    frequency: HashMap<Mono, usize>,
    basis: HashMap<Mono, (BTreeMap<Mono, u64>, u64)>,
    inconsistent: bool,
}

impl SparseIncremental {
    fn build(columns: &[Column], vectors: &HashMap<Column, Vec<(Mono, u64)>>, target: Mono, prime: u64) -> Self {
        let mut frequency = HashMap::<Mono, usize>::new();
        for column in columns {
            for &(row, coefficient) in &vectors[column] {
                if row != target && coefficient != 0 { *frequency.entry(row).or_default() += 1; }
            }
        }
        let mut answer = Self { prime, target, frequency, basis: HashMap::new(), inconsistent: false };
        answer.add(columns, vectors);
        answer
    }

    fn add(&mut self, columns: &[Column], vectors: &HashMap<Column, Vec<(Mono, u64)>>) {
        for column in columns {
            if self.inconsistent { return; }
            let raw = &vectors[column];
            let target_coefficient = raw.iter().find_map(|(row, coefficient)|
                if *row == self.target { Some(*coefficient) } else { None }).unwrap_or(0);
            let mut rhs = if target_coefficient == 0 { 0 } else { self.prime - target_coefficient };
            let mut vector = BTreeMap::<Mono, u64>::new();
            for &(row, coefficient) in raw {
                if row != self.target && coefficient != 0 { vector.insert(row, coefficient); }
            }
            let mut inserted = false;
            while !vector.is_empty() {
                let pivot = sparse_choose_pivot(&vector, SparsePivot::Rare, &self.frequency);
                let value = vector[&pivot];
                if let Some((record, record_rhs)) = self.basis.get(&pivot) {
                    sparse_sub_scaled(&mut vector, record, value, self.prime);
                    let subtract = (value as u128 * *record_rhs as u128 % self.prime as u128) as u64;
                    rhs = if rhs >= subtract { rhs - subtract } else { rhs + self.prime - subtract };
                    continue;
                }
                let inverse = inverse_mod(value, self.prime);
                for coefficient in vector.values_mut() {
                    *coefficient = (*coefficient as u128 * inverse as u128 % self.prime as u128) as u64;
                }
                rhs = (rhs as u128 * inverse as u128 % self.prime as u128) as u64;
                self.basis.insert(pivot, (std::mem::take(&mut vector), rhs));
                inserted = true;
                break;
            }
            if !inserted && rhs != 0 { self.inconsistent = true; }
        }
    }

    fn solution(&self) -> Option<HashMap<Mono, u64>> {
        if self.inconsistent { return None; }
        let mut pivots: Vec<_> = self.basis.keys().copied().collect();
        pivots.sort_by(|a, b| sparse_compare_rows(a, b, SparsePivot::Rare, &self.frequency));
        let mut answer = HashMap::<Mono, u64>::from([(self.target, 1)]);
        for pivot in pivots.into_iter().rev() {
            let (record, record_rhs) = &self.basis[&pivot];
            let mut value = *record_rhs;
            for (&row, &coefficient) in record {
                if row == pivot { continue; }
                let subtract = (coefficient as u128 * answer.get(&row).copied().unwrap_or(0) as u128
                    % self.prime as u128) as u64;
                value = if value >= subtract { value - subtract } else { value + self.prime - subtract };
            }
            if value != 0 { answer.insert(pivot, value); }
        }
        Some(answer)
    }
}

fn sparse_seed(path: Option<&Path>, prime: u64, provider: &Provider, target: Mono) -> HashMap<Mono, u64> {
    let Some(path) = path else { return HashMap::from([(target, 1)]); };
    let text = fs::read_to_string(path).unwrap_or_else(|e| fail(e.to_string()));
    let mut lines = text.lines();
    let header: Vec<_> = lines.next().unwrap_or_else(|| fail("empty seed dual")).split_whitespace().collect();
    if header.len() != 4 || header[0] != "KRENN_AFFINE251_ORBIT_DUAL_V1"
        || header[1].parse::<u64>().ok() != Some(prime) { fail("seed dual header mismatch"); }
    let expected: usize = header[2].parse().unwrap_or_else(|_| fail("bad seed support"));
    let pairing: u64 = header[3].parse().unwrap_or_else(|_| fail("bad seed pairing"));
    if pairing == 0 || pairing >= prime { fail("bad seed normalization"); }
    let normalize = inverse_mod(pairing, prime);
    let mut answer = HashMap::<Mono, u64>::new();
    for line in lines {
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.len() != 4 || fields[0] != "ROW" || fields[2].len() != 16 { fail("bad seed row"); }
        let mut ids = Vec::with_capacity(12);
        for pair in fields[2].as_bytes().chunks_exact(2) {
            let token = std::str::from_utf8(pair).unwrap_or_else(|_| fail("bad seed hex"));
            ids.push(u8::from_str_radix(token, 16).unwrap_or_else(|_| fail("bad seed hex")));
        }
        ids.extend([T_ID; 4]);
        let row = Mono::new(ids);
        let canonical = row_info_pure(provider, row, &mut HashMap::new()).canonical;
        let raw: u64 = fields[3].parse().unwrap_or_else(|_| fail("bad seed value"));
        let value = (raw as u128 * normalize as u128 % prime as u128) as u64;
        if value == 0 || answer.insert(canonical, value).is_some() { fail("duplicate/zero seed row"); }
    }
    if answer.len() != expected || answer.get(&target).copied() != Some(1) { fail("seed support/target mismatch"); }
    answer
}

fn sparse_write_checkpoint(path: &Path, prime: u64, round: usize,
                           columns: &HashSet<Column>, candidate: &HashMap<Mono, u64>) {
    let tmp = path.with_extension("bin.tmp");
    let mut out = BufWriter::new(File::create(&tmp).unwrap_or_else(|e| fail(e.to_string())));
    out.write_all(SPARSE_CHECKPOINT_MAGIC).unwrap();
    write_u64(&mut out, prime); write_u64(&mut out, round as u64);
    write_u64(&mut out, columns.len() as u64); write_u64(&mut out, candidate.len() as u64);
    let mut sorted_columns: Vec<_> = columns.iter().copied().collect(); sorted_columns.sort_unstable();
    let mut sorted_candidate: Vec<_> = candidate.iter().map(|(row, value)| (*row, *value)).collect();
    sorted_candidate.sort_unstable_by_key(|x| x.0);
    for column in sorted_columns {
        out.write_all(&column.word.to_le_bytes()).unwrap(); write_mono(&mut out, column.multiplier);
    }
    for (row, value) in sorted_candidate { write_mono(&mut out, row); write_u64(&mut out, value); }
    out.flush().unwrap(); drop(out);
    fs::rename(tmp, path).unwrap_or_else(|e| fail(e.to_string()));
}

fn sparse_read_checkpoint(path: &Path, prime: u64) -> Option<(usize, HashSet<Column>, HashMap<Mono, u64>)> {
    if !path.exists() { return None; }
    let mut input = BufReader::new(File::open(path).unwrap_or_else(|e| fail(e.to_string())));
    let mut magic = [0u8; 12]; input.read_exact(&mut magic).unwrap_or_else(|e| fail(e.to_string()));
    if &magic != SPARSE_CHECKPOINT_MAGIC || read_u64(&mut input) != prime { fail("sparse checkpoint mismatch"); }
    let round = read_u64(&mut input) as usize;
    let nc = read_u64(&mut input) as usize; let ns = read_u64(&mut input) as usize;
    let mut columns = HashSet::with_capacity(nc);
    let mut candidate = HashMap::with_capacity(ns);
    for _ in 0..nc {
        let mut bytes = [0u8; 2]; input.read_exact(&mut bytes).unwrap_or_else(|e| fail(e.to_string()));
        let column = Column { word: u16::from_le_bytes(bytes), multiplier: read_mono(&mut input) };
        if column.word as usize >= N_WORDS || column.multiplier.len != 8 || !columns.insert(column) {
            fail("bad sparse checkpoint column");
        }
    }
    for _ in 0..ns {
        let row = read_mono(&mut input); let value = read_u64(&mut input);
        if row.len != 12 || value == 0 || value >= prime || candidate.insert(row, value).is_some() {
            fail("bad sparse checkpoint candidate");
        }
    }
    let mut trailing = [0u8; 1];
    if input.read(&mut trailing).unwrap_or_else(|e| fail(e.to_string())) != 0 { fail("trailing sparse checkpoint bytes"); }
    Some((round, columns, candidate))
}

fn sparse_hash_bytes(mut hash: u64, bytes: &[u8]) -> u64 {
    // Stable FNV-1a is used only as an internal corruption/staleness guard;
    // the sealed artifacts are additionally pinned with SHA-256.
    for &byte in bytes {
        hash ^= byte as u64;
        hash = hash.wrapping_mul(1_099_511_628_211);
    }
    hash
}

fn sparse_provider_fingerprint(provider: &Provider) -> u64 {
    let mut hash = 14_695_981_039_346_656_037u64;
    for (word, polynomial) in provider.polynomials.iter().enumerate() {
        hash = sparse_hash_bytes(hash, &(word as u64).to_le_bytes());
        hash = sparse_hash_bytes(hash, &(polynomial.len() as u64).to_le_bytes());
        for &(term, coefficient) in polynomial {
            hash = sparse_hash_bytes(hash, &[term.len]);
            hash = sparse_hash_bytes(hash, &term.ids);
            hash = sparse_hash_bytes(hash, &coefficient.to_le_bytes());
        }
    }
    hash
}

fn sparse_vectors_fingerprint(vectors: &HashMap<Column, Vec<(Mono, u64)>>) -> u64 {
    let mut hash = 14_695_981_039_346_656_037u64;
    let mut columns: Vec<_> = vectors.keys().copied().collect();
    columns.sort_unstable();
    for column in columns {
        hash = sparse_hash_bytes(hash, &column.word.to_le_bytes());
        hash = sparse_hash_bytes(hash, &[column.multiplier.len]);
        hash = sparse_hash_bytes(hash, &column.multiplier.ids);
        hash = sparse_hash_bytes(hash, &(vectors[&column].len() as u64).to_le_bytes());
        for &(row, value) in &vectors[&column] {
            hash = sparse_hash_bytes(hash, &[row.len]);
            hash = sparse_hash_bytes(hash, &row.ids);
            hash = sparse_hash_bytes(hash, &value.to_le_bytes());
        }
    }
    hash
}

fn sparse_write_vectors(path: &Path, prime: u64, provider_fingerprint: u64,
                        vectors: &HashMap<Column, Vec<(Mono, u64)>>) {
    let tmp = path.with_extension("bin.tmp");
    let mut out = BufWriter::with_capacity(1 << 20,
        File::create(&tmp).unwrap_or_else(|e| fail(e.to_string())));
    out.write_all(SPARSE_VECTOR_MAGIC).unwrap(); write_u64(&mut out, prime);
    write_u64(&mut out, provider_fingerprint);
    write_u64(&mut out, sparse_vectors_fingerprint(vectors));
    write_u64(&mut out, vectors.len() as u64);
    let mut columns: Vec<_> = vectors.keys().copied().collect(); columns.sort_unstable();
    for column in columns {
        out.write_all(&column.word.to_le_bytes()).unwrap(); write_mono(&mut out, column.multiplier);
        write_u64(&mut out, vectors[&column].len() as u64);
        for &(row, value) in &vectors[&column] { write_mono(&mut out, row); write_u64(&mut out, value); }
    }
    out.flush().unwrap(); drop(out); fs::rename(tmp, path).unwrap_or_else(|e| fail(e.to_string()));
}

fn sparse_read_vectors(path: &Path, prime: u64, provider_fingerprint: u64)
    -> HashMap<Column, Vec<(Mono, u64)>>
{
    if !path.exists() { return HashMap::new(); }
    let mut input = BufReader::with_capacity(1 << 20,
        File::open(path).unwrap_or_else(|e| fail(e.to_string())));
    let mut magic = [0u8; 12]; input.read_exact(&mut magic).unwrap_or_else(|e| fail(e.to_string()));
    if &magic != SPARSE_VECTOR_MAGIC || read_u64(&mut input) != prime
        || read_u64(&mut input) != provider_fingerprint { fail("sparse vector cache mismatch"); }
    let expected_fingerprint = read_u64(&mut input);
    let count = read_u64(&mut input) as usize;
    let mut answer = HashMap::with_capacity(count);
    for _ in 0..count {
        let mut bytes = [0u8; 2]; input.read_exact(&mut bytes).unwrap_or_else(|e| fail(e.to_string()));
        let column = Column { word: u16::from_le_bytes(bytes), multiplier: read_mono(&mut input) };
        let size = read_u64(&mut input) as usize;
        if column.word as usize >= N_WORDS || column.multiplier.len != 8 || size > 700_000 {
            fail("bad sparse vector cache record");
        }
        let mut vector = Vec::with_capacity(size);
        let mut previous = None;
        for _ in 0..size {
            let row = read_mono(&mut input); let value = read_u64(&mut input);
            if row.len != 12 || value == 0 || value >= prime
                || previous.is_some_and(|old| old >= row) { fail("bad sparse cached vector"); }
            previous = Some(row);
            vector.push((row, value));
        }
        if answer.insert(column, vector).is_some() { fail("duplicate sparse cached column"); }
    }
    let mut trailing = [0u8; 1];
    if input.read(&mut trailing).unwrap_or_else(|e| fail(e.to_string())) != 0 { fail("trailing sparse vector bytes"); }
    if sparse_vectors_fingerprint(&answer) != expected_fingerprint { fail("sparse vector cache checksum mismatch"); }
    answer
}

fn sparse_maybe_write_vectors(config: &SparseConfig, provider_fingerprint: u64,
                              vectors: &HashMap<Column, Vec<(Mono, u64)>>,
                              dirty: &mut bool) -> f64 {
    if !*dirty { return 0.0; }
    let started = Instant::now();
    sparse_write_vectors(&config.vector_cache, config.prime, provider_fingerprint, vectors);
    *dirty = false;
    started.elapsed().as_secs_f64()
}

fn sparse_write_dual(path: &Path, prime: u64, candidate: &HashMap<Mono, u64>) {
    let tmp = path.with_extension("tsv.tmp");
    let mut out = BufWriter::new(File::create(&tmp).unwrap_or_else(|e| fail(e.to_string())));
    writeln!(out, "KRENN_AFFINE251_SPARSE_D12_DUAL_V1 {prime} {} 1", candidate.len()).unwrap();
    let mut rows: Vec<_> = candidate.iter().map(|(row, value)| (*row, *value)).collect(); rows.sort_unstable_by_key(|x| x.0);
    for (row, value) in rows { writeln!(out, "ROW {} {}", mono_hex(row), value).unwrap(); }
    out.flush().unwrap(); drop(out);
    fs::rename(tmp, path).unwrap_or_else(|e| fail(e.to_string()));
}

fn sparse_write_result(config: &SparseConfig, provider: &Provider, gate: &Gate, status: &str,
                       reason: Option<&str>, columns: usize, support: usize, round: usize,
                       rounds: &[SparseRound], seed_support: usize,
                       restore: &SparseRestoreStats, vector_cache_write_seconds: f64) {
    let tmp = config.output.with_extension("json.tmp");
    let mut out = BufWriter::new(File::create(&tmp).unwrap_or_else(|e| fail(e.to_string())));
    writeln!(out, "{{").unwrap();
    writeln!(out, "  \"schema\": \"KRENN_AFFINE251_D12_NATIVE_SPARSE_DUAL_V1\",").unwrap();
    writeln!(out, "  \"status\": \"{status}\",").unwrap();
    writeln!(out, "  \"incomplete_reason\": {},", reason.map(|x| format!("\"{}\"", json_escape(x))).unwrap_or_else(|| "null".into())).unwrap();
    writeln!(out, "  \"degree\": 12,").unwrap();
    writeln!(out, "  \"prime\": {},", config.prime).unwrap();
    writeln!(out, "  \"group_order\": 1440,").unwrap();
    writeln!(out, "  \"provider_equations\": {},", provider.polynomials.len()).unwrap();
    writeln!(out, "  \"provider_terms_parsed\": {},", provider.parsed_terms).unwrap();
    writeln!(out, "  \"provider_distinct_terms\": {},", provider.distinct_terms).unwrap();
    writeln!(out, "  \"seed_support\": {seed_support},").unwrap();
    writeln!(out, "  \"column_orbits_exposed\": {columns},").unwrap();
    writeln!(out, "  \"dual_support\": {support},").unwrap();
    writeln!(out, "  \"rounds_completed\": {round},").unwrap();
    writeln!(out, "  \"global_annihilation\": {},", if status == "COMPLETE_MODULAR_DUAL" { "true" } else { "null" }).unwrap();
    writeln!(out, "  \"target_pairing\": {},", if status == "COMPLETE_MODULAR_DUAL" { "1" } else { "null" }).unwrap();
    writeln!(out, "  \"workers\": {},", config.workers).unwrap();
    writeln!(out, "  \"pivot_mode\": \"{}\",", config.pivot).unwrap();
    writeln!(out, "  \"strategy\": \"{}\",", config.strategy).unwrap();
    writeln!(out, "  \"elimination_kernel\": \"{}\",", config.elimination).unwrap();
    writeln!(out, "  \"incremental_basis\": {},", config.incremental).unwrap();
    writeln!(out, "  \"portfolio_period\": {},", config.portfolio_period).unwrap();
    writeln!(out, "  \"portfolio_parallel\": {},", config.portfolio_parallel).unwrap();
    writeln!(out, "  \"support_cap\": {},", config.support_cap).unwrap();
    writeln!(out, "  \"column_cap\": {},", config.column_cap).unwrap();
    writeln!(out, "  \"wall_limit_seconds\": {},", config.wall_seconds).unwrap();
    writeln!(out, "  \"rss_limit_gib\": {},", config.rss_gib).unwrap();
    writeln!(out, "  \"elapsed_seconds\": {:.6},", gate.elapsed()).unwrap();
    writeln!(out, "  \"peak_rss_kib\": {},", gate.peak_rss_kib).unwrap();
    writeln!(out, "  \"cached_vectors_loaded\": {},", restore.cached_vectors_loaded).unwrap();
    writeln!(out, "  \"vectors_materialized_on_restore\": {},", restore.vectors_materialized_on_restore).unwrap();
    writeln!(out, "  \"restore_seconds\": {:.6},", restore.restore_seconds).unwrap();
    writeln!(out, "  \"vector_cache_write_seconds\": {:.6},", vector_cache_write_seconds).unwrap();
    writeln!(out, "  \"vector_cache_bytes\": {},",
        fs::metadata(&config.vector_cache).map(|item| item.len()).unwrap_or(0)).unwrap();
    writeln!(out, "  \"checkpoint\": \"{}\",", json_escape(&config.checkpoint.display().to_string())).unwrap();
    writeln!(out, "  \"vector_cache\": \"{}\",", json_escape(&config.vector_cache.display().to_string())).unwrap();
    writeln!(out, "  \"dual\": \"{}\",", json_escape(&config.dual.display().to_string())).unwrap();
    writeln!(out, "  \"rounds\": [").unwrap();
    for (index, record) in rounds.iter().enumerate() {
        writeln!(out, "    {{\"round\":{},\"columns\":{},\"new_columns\":{},\"dual_support\":{},\"new_support_rows\":{},\"selected_strategy\":\"{}\",\"selected_pivot\":\"{}\",\"incident_seconds\":{:.6},\"materialize_seconds\":{:.6},\"solve_seconds\":{:.6}}}{}",
            record.index, record.columns, record.new_columns, record.support, record.new_support_rows,
            record.strategy, record.pivot, record.incident_seconds, record.materialize_seconds,
            record.solve_seconds, if index + 1 == rounds.len() { "" } else { "," }).unwrap();
    }
    writeln!(out, "  ]").unwrap(); writeln!(out, "}}").unwrap();
    out.flush().unwrap(); drop(out); fs::rename(tmp, &config.output).unwrap_or_else(|e| fail(e.to_string()));
}

pub fn sparse_d12_dual_entry() {
    let config = sparse_parse_args();
    let mut gate = Gate::new(config.wall_seconds, config.rss_gib);
    let provider = parse_provider(&config.input);
    if provider.parsed_terms != 688_908 || provider.distinct_terms != 688_906 { fail("provider census changed"); }
    let target = Mono::new(vec![T_ID; 12]);
    let seed = sparse_seed(config.seed_dual.as_deref(), config.prime, &provider, target);
    let seed_support = seed.len();
    let (mut completed_rounds, mut columns, mut candidate) = sparse_read_checkpoint(&config.checkpoint, config.prime)
        .unwrap_or_else(|| (0, HashSet::new(), seed));
    if candidate.get(&target).copied() != Some(1) { fail("checkpoint target not normalized"); }
    let mut incidence_cache = HashMap::<Mono, Vec<Column>>::new();
    let provider_fingerprint = sparse_provider_fingerprint(&provider);
    let restore_started = Instant::now();
    let mut vectors = sparse_read_vectors(&config.vector_cache, config.prime, provider_fingerprint);
    if vectors.keys().any(|column| !columns.contains(column)) {
        fail("sparse vector cache is not a checkpoint subset");
    }
    let cached_vectors_loaded = vectors.len();
    let mut vector_cache_dirty = false;
    let mut exposed_frequency = HashMap::<Mono, usize>::new();
    if !columns.is_empty() {
        let mut restored: Vec<_> = columns.iter().filter(|column| !vectors.contains_key(column)).copied().collect();
        restored.sort_unstable();
        let values = parallel_invariant_columns(&provider, &restored, config.prime, config.workers);
        for (column, vector) in restored.into_iter().zip(values) {
            vectors.insert(column, vector);
        }
        vector_cache_dirty = vectors.len() != cached_vectors_loaded;
    }
    if vectors.len() != columns.len() { fail("sparse vector restore incomplete"); }
    for vector in vectors.values() {
        for &(row, coefficient) in vector {
            if row != target && coefficient != 0 { *exposed_frequency.entry(row).or_default() += 1; }
        }
    }
    let restore = SparseRestoreStats {
        cached_vectors_loaded,
        vectors_materialized_on_restore: vectors.len() - cached_vectors_loaded,
        restore_seconds: restore_started.elapsed().as_secs_f64(),
    };
    let mut vector_cache_write_seconds = 0.0;
    let mut records = Vec::<SparseRound>::new();
    let mut incremental = None::<SparseIncremental>;
    let mut incremental_suspended_until = 0usize;
    loop {
        if let Err(reason) = gate.check() {
            sparse_write_checkpoint(&config.checkpoint, config.prime, completed_rounds, &columns, &candidate);
            vector_cache_write_seconds += sparse_maybe_write_vectors(&config, provider_fingerprint,
                &vectors, &mut vector_cache_dirty);
            sparse_write_result(&config, &provider, &gate, "INCOMPLETE_RESOURCE_GATE", Some(reason),
                columns.len(), candidate.len(), completed_rounds, &records, seed_support,
                &restore, vector_cache_write_seconds);
            return;
        }
        if completed_rounds >= config.round_cap {
            sparse_write_checkpoint(&config.checkpoint, config.prime, completed_rounds, &columns, &candidate);
            vector_cache_write_seconds += sparse_maybe_write_vectors(&config, provider_fingerprint,
                &vectors, &mut vector_cache_dirty);
            sparse_write_result(&config, &provider, &gate, "INCOMPLETE_SEARCH_CAP", Some("ROUND_CAP"),
                columns.len(), candidate.len(), completed_rounds, &records, seed_support,
                &restore, vector_cache_write_seconds);
            return;
        }
        let phase = Instant::now();
        let mut missing_rows: Vec<_> = candidate.keys().filter(|row| !incidence_cache.contains_key(row)).copied().collect();
        missing_rows.sort_unstable();
        for (row, incident) in sparse_parallel_incident_lists(&provider, &missing_rows, config.workers) {
            incidence_cache.insert(row, incident);
        }
        let mut incident = HashSet::<Column>::new();
        for row in candidate.keys() { incident.extend(incidence_cache[row].iter().copied()); }
        let incident_seconds = phase.elapsed().as_secs_f64();
        let mut new_columns: Vec<_> = incident.difference(&columns).copied().collect(); new_columns.sort_unstable();
        if new_columns.is_empty() {
            sparse_write_dual(&config.dual, config.prime, &candidate);
            sparse_write_checkpoint(&config.checkpoint, config.prime, completed_rounds, &columns, &candidate);
            vector_cache_write_seconds += sparse_maybe_write_vectors(&config, provider_fingerprint,
                &vectors, &mut vector_cache_dirty);
            sparse_write_result(&config, &provider, &gate, "COMPLETE_MODULAR_DUAL", None,
                columns.len(), candidate.len(), completed_rounds, &records, seed_support,
                &restore, vector_cache_write_seconds);
            eprintln!("terminal sparse dual support={} columns={} rounds={} elapsed={:.3}s peak_rss_kib={}",
                candidate.len(), columns.len(), completed_rounds, gate.elapsed(), gate.peak_rss_kib);
            return;
        }
        if columns.len() + new_columns.len() > config.column_cap {
            sparse_write_checkpoint(&config.checkpoint, config.prime, completed_rounds, &columns, &candidate);
            vector_cache_write_seconds += sparse_maybe_write_vectors(&config, provider_fingerprint,
                &vectors, &mut vector_cache_dirty);
            sparse_write_result(&config, &provider, &gate, "INCOMPLETE_SEARCH_CAP", Some("COLUMN_CAP"),
                columns.len(), candidate.len(), completed_rounds, &records, seed_support,
                &restore, vector_cache_write_seconds);
            return;
        }
        let phase = Instant::now();
        let values = parallel_invariant_columns(&provider, &new_columns, config.prime, config.workers);
        for (column, vector) in new_columns.iter().copied().zip(values) {
            for &(row, coefficient) in &vector {
                if row != target && coefficient != 0 { *exposed_frequency.entry(row).or_default() += 1; }
            }
            vectors.insert(column, vector);
        }
        columns.extend(new_columns.iter().copied());
        vector_cache_dirty = true;
        let materialize_seconds = phase.elapsed().as_secs_f64();
        let mut sorted_columns: Vec<_> = columns.iter().copied().collect(); sorted_columns.sort_unstable();
        // The broad portfolio is valuable while the component geometry is
        // unknown.  Once it is established, cold+rare has dominated every
        // accepted round; use that route between periodic 32-round portfolio
        // audits.  This removes five redundant full eliminations per round
        // without silently freezing the heuristic forever.
        let broad_portfolio = columns.len() <= 1024 || completed_rounds % config.portfolio_period == 0;
        let mut score_frontiers = broad_portfolio;
        let effective_pivot = if config.pivot == "auto" && !broad_portfolio { "rare" } else { config.pivot.as_str() };
        let effective_strategy = if config.strategy == "best" && !broad_portfolio { "cold" } else { config.strategy.as_str() };
        let use_incremental = config.incremental && config.pivot == "auto" && config.strategy == "best"
            && !broad_portfolio && completed_rounds >= incremental_suspended_until;
        let pivots: Vec<_> = match effective_pivot {
            "first" => vec![SparsePivot::First], "last" => vec![SparsePivot::Last],
            "rare" => vec![SparsePivot::Rare],
            "auto" => vec![SparsePivot::First, SparsePivot::Last, SparsePivot::Rare], _ => unreachable!(),
        };
        let bases: Vec<(&str, HashMap<Mono, u64>)> = match effective_strategy {
            "cold" => vec![("cold", HashMap::from([(target, 1)]))],
            "repair" => vec![("repair", candidate.clone())],
            "best" => vec![("repair", candidate.clone()), ("cold", HashMap::from([(target, 1)]))],
            _ => unreachable!(),
        };
        let phase = Instant::now();
        let mut choices = Vec::<(HashMap<Mono, u64>, String, SparsePivot)>::new();
        if use_incremental {
            if let Some(state) = incremental.as_mut() {
                state.add(&new_columns, &vectors);
            } else {
                incremental = Some(SparseIncremental::build(&sorted_columns, &vectors, target, config.prime));
            }
            if let Some(solution) = incremental.as_ref().and_then(SparseIncremental::solution) {
                if sorted_columns.iter().any(|column| sparse_pairing(&vectors[column], &solution, config.prime) != 0) {
                    fail("incremental sparse solver returned a violating candidate");
                }
                let mut missing: Vec<_> = solution.keys().filter(|row|
                    !incidence_cache.contains_key(row)).copied().collect();
                missing.sort_unstable();
                for (row, incident) in sparse_parallel_incident_lists(&provider, &missing, config.workers) {
                    incidence_cache.insert(row, incident);
                }
                let mut next_columns = HashSet::<Column>::new();
                for row in solution.keys() {
                    next_columns.extend(incidence_cache[row].iter()
                        .filter(|column| !columns.contains(column)).copied());
                }
                let frontier_limit = new_columns.len().saturating_mul(4).max(1024);
                choices.push((solution, "cold-incremental".into(), SparsePivot::Rare));
                if next_columns.len() > frontier_limit {
                    // Frozen epoch pivot priorities can eventually create a
                    // valid but geometrically disastrous dual.  Compare it
                    // with a fresh rare-pivot solve before accepting growth.
                    if let Some(solution) = sparse_solve_correction(&sorted_columns, &vectors,
                            &HashMap::from([(target, 1)]), target, config.prime,
                            SparsePivot::Rare, &exposed_frequency) {
                        choices.push((solution, "cold-fallback".into(), SparsePivot::Rare));
                        score_frontiers = true;
                        incremental_suspended_until = ((completed_rounds / config.portfolio_period) + 1)
                            * config.portfolio_period;
                    }
                }
            }
        } else {
            let tasks: Vec<_> = bases.iter().flat_map(|(strategy, base)|
                pivots.iter().map(move |&pivot| (*strategy, base, pivot))).collect();
            let use_vec = config.elimination == "vec";
            let use_hierarchical = config.elimination == "hierarchical";
            if config.portfolio_parallel && tasks.len() > 1 && config.workers >= tasks.len() {
                choices = thread::scope(|scope| {
                    let mut handles = Vec::new();
                    let sorted_columns_ref = &sorted_columns;
                    let vectors_ref = &vectors;
                    let frequency_ref = &exposed_frequency;
                    let prime = config.prime;
                    for (strategy, base, pivot) in tasks {
                        handles.push(scope.spawn(move || {
                            let solution = if use_hierarchical {
                                sparse_solve_correction_hierarchical(sorted_columns_ref, vectors_ref,
                                    base, target, prime, frequency_ref, 16)
                            } else if use_vec {
                                sparse_solve_correction_vec(sorted_columns_ref, vectors_ref, base, target,
                                    prime, pivot, frequency_ref)
                            } else {
                                sparse_solve_correction(sorted_columns_ref, vectors_ref, base, target,
                                    prime, pivot, frequency_ref)
                            };
                            solution.map(|answer| (answer, strategy.into(), pivot))
                        }));
                    }
                    handles.into_iter().filter_map(|handle|
                        handle.join().unwrap_or_else(|_| fail("portfolio solver worker panicked"))).collect()
                });
            } else {
                for (strategy, base, pivot) in tasks {
                    let solution = if use_hierarchical {
                        sparse_solve_correction_hierarchical(&sorted_columns, &vectors, base, target,
                            config.prime, &exposed_frequency, config.workers)
                    } else if use_vec {
                        sparse_solve_correction_vec(&sorted_columns, &vectors, base, target,
                            config.prime, pivot, &exposed_frequency)
                    } else {
                        sparse_solve_correction(&sorted_columns, &vectors, base, target,
                            config.prime, pivot, &exposed_frequency)
                    };
                    if let Some(solution) = solution { choices.push((solution, strategy.into(), pivot)); }
                }
            }
        }
        let solve_seconds = phase.elapsed().as_secs_f64();
        if score_frontiers && choices.len() > 1 {
            // A slightly larger dual can be substantially better if its rows
            // touch fewer unseen columns.  Canonicalize the small union of
            // portfolio support once and score the actual next frontier.
            let mut portfolio_rows = HashSet::<Mono>::new();
            for (solution, _, _) in &choices { portfolio_rows.extend(solution.keys().copied()); }
            let mut missing: Vec<_> = portfolio_rows.into_iter()
                .filter(|row| !incidence_cache.contains_key(row)).collect();
            missing.sort_unstable();
            for (row, incident) in sparse_parallel_incident_lists(&provider, &missing, config.workers) {
                incidence_cache.insert(row, incident);
            }
            choices.sort_by_key(|(solution, _, _)| {
                let mut next_columns = HashSet::<Column>::new();
                for row in solution.keys() {
                    next_columns.extend(incidence_cache[row].iter().filter(|column| !columns.contains(column)).copied());
                }
                (next_columns.len(), solution.len())
            });
        } else {
            choices.sort_by_key(|choice| choice.0.len());
        }
        let Some((next, selected_strategy, selected_pivot)) = choices.into_iter().next() else {
            sparse_write_checkpoint(&config.checkpoint, config.prime, completed_rounds, &columns, &candidate);
            vector_cache_write_seconds += sparse_maybe_write_vectors(&config, provider_fingerprint,
                &vectors, &mut vector_cache_dirty);
            sparse_write_result(&config, &provider, &gate, "TARGET_FORCED_BY_EXPOSED_COLUMNS", None,
                columns.len(), candidate.len(), completed_rounds, &records, seed_support,
                &restore, vector_cache_write_seconds);
            return;
        };
        if next.len() > config.support_cap {
            sparse_write_checkpoint(&config.checkpoint, config.prime, completed_rounds, &columns, &candidate);
            vector_cache_write_seconds += sparse_maybe_write_vectors(&config, provider_fingerprint,
                &vectors, &mut vector_cache_dirty);
            sparse_write_result(&config, &provider, &gate, "INCOMPLETE_SEARCH_CAP", Some("SUPPORT_CAP"),
                columns.len(), next.len(), completed_rounds, &records, seed_support,
                &restore, vector_cache_write_seconds);
            return;
        }
        let new_support_rows = next.keys().filter(|row| !candidate.contains_key(row)).count();
        candidate = next; completed_rounds += 1;
        if config.incremental && broad_portfolio && config.pivot == "auto" && config.strategy == "best" {
            incremental = Some(SparseIncremental::build(&sorted_columns, &vectors, target, config.prime));
        }
        let record = SparseRound {
            index: completed_rounds, columns: columns.len(), new_columns: new_columns.len(),
            support: candidate.len(), new_support_rows, strategy: selected_strategy,
            pivot: selected_pivot.name().into(), incident_seconds, materialize_seconds, solve_seconds,
        };
        eprintln!("sparse round={} columns={} new={} support={} new_rows={} strategy={} pivot={} incident={:.3}s materialize={:.3}s solve={:.3}s elapsed={:.3}s rss_peak_kib={}",
            record.index, record.columns, record.new_columns, record.support, record.new_support_rows,
            record.strategy, record.pivot, record.incident_seconds, record.materialize_seconds,
            record.solve_seconds, gate.elapsed(), gate.peak_rss_kib);
        records.push(record);
        sparse_write_checkpoint(&config.checkpoint, config.prime, completed_rounds, &columns, &candidate);
    }
}

fn main() {
    let config = parse_args();
    let mut gate = Gate::new(config.wall_seconds, config.rss_gib);
    let provider = parse_provider(&config.input);
    if provider.parsed_terms != 688_908 || provider.distinct_terms != 688_906 {
        fail(format!("provider census changed: terms={} distinct={}", provider.parsed_terms, provider.distinct_terms));
    }
    if let Err(reason) = gate.check() {
        write_result(&config, &provider, None, None, &gate, "INCOMPLETE_RESOURCE_GATE", Some(reason));
        return;
    }
    let mut engine = OrbitEngine::new(provider);
    let closure = match compute_closure(&mut engine, config.degree, &config.checkpoint, &mut gate, config.workers) {
        Ok(value) => value,
        Err(reason) => {
            let partial = read_checkpoint(&config.checkpoint, config.degree);
            write_result(&config, &engine.provider, partial.as_ref(), None, &gate,
                         "INCOMPLETE_RESOURCE_GATE", Some(reason));
            return;
        }
    };
    let linear = match linear_membership(&mut engine, &closure, config.degree, config.prime, &config.dual, &mut gate,
                                         config.workers, config.pivot_last) {
        Ok(value) => value,
        Err(reason) => {
            write_result(&config, &engine.provider, Some(&closure), None, &gate, "INCOMPLETE_RESOURCE_GATE", Some(reason));
            return;
        }
    };
    let status = if linear.member { "COMPLETE_MEMBER_MOD_PRIME" } else { "COMPLETE_NONMEMBER_MOD_PRIME" };
    write_result(&config, &engine.provider, Some(&closure), Some(&linear), &gate, status, None);
    eprintln!("terminal status={status} degree={} prime={} rows={} columns={} rank={} nnz={} elapsed={:.3}s peak_rss_kib={}",
        config.degree, config.prime, closure.rows.len(), closure.columns.len(), linear.rank, linear.nnz,
        gate.elapsed(), gate.peak_rss_kib);
}
