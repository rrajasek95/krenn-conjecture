//! Exact target-rooted DFS for the normalized N8 degree-seven homogeneous map.
//!
//! The twelve frozen support variables are one.  A row stores only its sorted
//! nonsupport raw coordinate IDs; at homogeneous degree seven its t exponent
//! is implicit as 7-len(row).  A multiplier has total degree three and hence
//! implicit t exponent 3-len(multiplier).  No output is truncated.

use std::collections::{BTreeMap, BTreeSet, HashMap, HashSet};
use std::env;
use std::fs::File;
use std::hash::{Hash, Hasher};
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::path::Path;
use std::time::{Duration, Instant};

const N: usize = 8;
const Q: usize = 3;
const N_EDGES: usize = 28;
const N_COORDS: usize = 252;
const N_WORDS: usize = 6561;
const HOMOGENEOUS_DEGREE: usize = 7;
const GENERATOR_DEGREE: usize = 4;
const MULTIPLIER_DEGREE: usize = HOMOGENEOUS_DEGREE - GENERATOR_DEGREE;
const SUPPORT_IDS: [u8; 12] = [0, 22, 62, 89, 103, 125, 130, 135, 162, 233, 238, 243];

const SITE_ACTIONS: [[u8; N]; 4] = [
    [0, 1, 2, 3, 4, 5, 6, 7],
    [0, 1, 5, 7, 6, 2, 4, 3],
    [1, 0, 2, 4, 3, 5, 7, 6],
    [1, 0, 5, 6, 7, 2, 3, 4],
];
const COLOUR_ACTIONS: [[u8; Q]; 4] = [
    [0, 1, 2],
    [0, 2, 1],
    [0, 2, 1],
    [0, 1, 2],
];

#[derive(Clone, Copy, Eq, Ord, PartialEq, PartialOrd)]
struct Mono {
    len: u8,
    ids: [u8; HOMOGENEOUS_DEGREE],
}

impl Hash for Mono {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.len.hash(state);
        self.slice().hash(state);
    }
}

impl Mono {
    fn new(mut ids: Vec<u8>) -> Self {
        if ids.len() > HOMOGENEOUS_DEGREE {
            fail(format!("normalized degree {} exceeds {}", ids.len(), HOMOGENEOUS_DEGREE));
        }
        ids.sort_unstable();
        let mut packed = [0; HOMOGENEOUS_DEGREE];
        packed[..ids.len()].copy_from_slice(&ids);
        Self { len: ids.len() as u8, ids: packed }
    }

    fn slice(&self) -> &[u8] {
        &self.ids[..self.len as usize]
    }

    fn concat(self, other: Mono) -> Self {
        let mut ids = self.slice().to_vec();
        ids.extend_from_slice(other.slice());
        Self::new(ids)
    }

    fn quotient(self, divisor: Mono) -> Option<Self> {
        let mut ids = self.slice().to_vec();
        for &value in divisor.slice() {
            let position = ids.iter().position(|&candidate| candidate == value)?;
            ids.remove(position);
        }
        Some(Self::new(ids))
    }
}

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Column {
    word: u16,
    multiplier: Mono,
}

#[derive(Clone)]
struct Action {
    var_map: [u8; N_COORDS],
    word_map: [u16; N_WORDS],
}

struct Engine {
    actions: Vec<Action>,
    polynomials: Vec<Vec<(Mono, i32)>>,
    term_index: HashMap<Mono, Vec<u16>>,
    row_cache: HashMap<Mono, Mono>,
    column_cache: HashMap<Column, Column>,
    incident_cache: HashMap<Mono, Vec<Column>>,
    output_cache: HashMap<Column, BTreeMap<Mono, i32>>,
}

struct DfsState {
    assigned: HashMap<Mono, Column>,
    used: HashSet<Column>,
    visiting: HashSet<Mono>,
    order: Vec<(Mono, Column, i32)>,
    calls: usize,
    maximum_depth: usize,
    last_dead_end: Option<(Mono, usize)>,
}

struct Limits {
    call_cap: usize,
    row_cap: usize,
    deadline: Instant,
}

struct WordPacket {
    allowed: [bool; N_WORDS],
    literal_words: usize,
    stabilizer_orbits: usize,
}

#[derive(Clone, Copy)]
enum DfsLimit {
    Calls,
    Rows,
    Wall,
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("n8-normalized-dfs-degree7: {}", message.as_ref());
    std::process::exit(2);
}

fn encode_word(word: &[u8; N]) -> u16 {
    word.iter().fold(0, |code, digit| code * 3 + *digit as u16)
}

fn decode_word(mut code: u16) -> [u8; N] {
    let mut word = [0; N];
    for index in (0..N).rev() {
        word[index] = (code % 3) as u8;
        code /= 3;
    }
    word
}

fn generate_matchings() -> Vec<[(u8, u8); GENERATOR_DEGREE]> {
    fn visit(vertices: &[u8], pairs: &mut Vec<(u8, u8)>, out: &mut Vec<[(u8, u8); 4]>) {
        if vertices.is_empty() {
            out.push([pairs[0], pairs[1], pairs[2], pairs[3]]);
            return;
        }
        let first = vertices[0];
        for position in 1..vertices.len() {
            let second = vertices[position];
            let mut rest = Vec::new();
            rest.extend_from_slice(&vertices[1..position]);
            rest.extend_from_slice(&vertices[position + 1..]);
            pairs.push((first, second));
            visit(&rest, pairs, out);
            pairs.pop();
        }
    }
    let mut answer = Vec::new();
    visit(&[0, 1, 2, 3, 4, 5, 6, 7], &mut Vec::new(), &mut answer);
    if answer.len() != 105 {
        fail("eight-site perfect-matching census changed");
    }
    answer
}

fn parse_hex(value: &str) -> Mono {
    if value.len() % 2 != 0 {
        fail("odd-length monomial hex");
    }
    let ids = (0..value.len())
        .step_by(2)
        .map(|index| u8::from_str_radix(&value[index..index + 2], 16)
             .unwrap_or_else(|_| fail("bad monomial hex")))
        .collect();
    Mono::new(ids)
}

fn mono_hex(value: Mono) -> String {
    value.slice().iter().map(|item| format!("{item:02x}")).collect()
}

fn read_words(path: &Path) -> WordPacket {
    let input = BufReader::new(File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    let mut allowed = [false; N_WORDS];
    let mut rows = 0;
    let mut expected_rows = None;
    let mut expected_orbits = None;
    for (line_number, line) in input.lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if line_number == 0 {
            if fields.len() != 3 || fields[0] != "KRENN_N8_WORD_PACKET_V1" {
                fail("bad word-packet magic");
            }
            expected_rows = Some(fields[1].parse().unwrap_or_else(|_| fail("bad word census")));
            expected_orbits = Some(fields[2].parse().unwrap_or_else(|_| fail("bad word-orbit census")));
            continue;
        }
        if fields.len() != 3 || fields[0] != "WORD" {
            fail("bad word-packet row");
        }
        let code: usize = fields[1].parse().unwrap_or_else(|_| fail("bad word code"));
        if code >= N_WORDS || allowed[code] {
            fail("duplicate or out-of-range word code");
        }
        let decoded: String = decode_word(code as u16).iter().map(|item| char::from(b'0' + *item)).collect();
        if decoded != fields[2] {
            fail("word label/code mismatch");
        }
        allowed[code] = true;
        rows += 1;
    }
    if Some(rows) != expected_rows {
        fail(format!("word packet has {rows} rows, expected {:?}", expected_rows));
    }
    WordPacket {
        allowed,
        literal_words: rows,
        stabilizer_orbits: expected_orbits.unwrap_or_else(|| fail("missing word header")),
    }
}

fn read_seed(path: &Path) -> BTreeMap<Mono, i32> {
    let input = BufReader::new(File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    let mut rows = BTreeMap::new();
    for (line_number, line) in input.lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if line_number == 0 {
            if fields != ["KRENN_N8_NORMALIZED_TAIL_V1", "7", "564", "2"] {
                fail("bad target-seed magic or census");
            }
            continue;
        }
        if fields.len() != 3 || fields[0] != "ROW" {
            fail("bad target-seed row");
        }
        let row = parse_hex(fields[1]);
        let coefficient: i32 = fields[2].parse().unwrap_or_else(|_| fail("bad target coefficient"));
        if coefficient == 0 || rows.insert(row, coefficient).is_some() {
            fail("zero or duplicate target row");
        }
    }
    if rows.len() != 564 {
        fail(format!("target seed has {} rows", rows.len()));
    }
    rows
}

impl Engine {
    fn new(packet: WordPacket) -> Self {
        let allowed = packet.allowed;
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
        if next != N_EDGES { fail("edge census changed"); }

        let mut support = [false; N_COORDS];
        for &value in &SUPPORT_IDS { support[value as usize] = true; }

        let mut actions = Vec::new();
        for action_index in 0..4 {
            let sites = SITE_ACTIONS[action_index];
            let colours = COLOUR_ACTIONS[action_index];
            let mut var_map = [0; N_COORDS];
            for coordinate in 0..N_COORDS {
                let edge = coordinate / 9;
                let left_colour = (coordinate % 9) / 3;
                let right_colour = coordinate % 3;
                let (left, right) = edges[edge];
                let mut moved_left = sites[left as usize];
                let mut moved_right = sites[right as usize];
                let mut moved_left_colour = colours[left_colour];
                let mut moved_right_colour = colours[right_colour];
                if moved_left > moved_right {
                    std::mem::swap(&mut moved_left, &mut moved_right);
                    std::mem::swap(&mut moved_left_colour, &mut moved_right_colour);
                }
                let moved_edge = edge_id[moved_left as usize][moved_right as usize] as usize;
                var_map[coordinate] = (moved_edge * 9
                    + moved_left_colour as usize * 3 + moved_right_colour as usize) as u8;
            }
            if (0..N_COORDS).any(|coordinate| support[coordinate] != support[var_map[coordinate] as usize]) {
                fail("listed group action does not preserve support");
            }

            let mut word_map = [0; N_WORDS];
            for code in 0..N_WORDS {
                let word = decode_word(code as u16);
                let mut moved = [0; N];
                for site in 0..N {
                    moved[sites[site] as usize] = colours[word[site] as usize];
                }
                word_map[code] = encode_word(&moved);
            }
            actions.push(Action { var_map, word_map });
        }

        for code in 0..N_WORDS {
            for action in &actions {
                if allowed[code] != allowed[action.word_map[code] as usize] {
                    fail("word packet is not support-stabilizer closed");
                }
            }
        }
        let word_orbits: BTreeSet<_> = (0..N_WORDS)
            .filter(|&code| allowed[code])
            .map(|code| actions.iter().map(|action| action.word_map[code]).min().unwrap())
            .collect();
        if word_orbits.len() != packet.stabilizer_orbits {
            fail("word-packet orbit census changed");
        }
        if packet.literal_words != 78 && packet.literal_words != 6558 {
            fail("unsupported bounded word packet");
        }

        let matchings = generate_matchings();
        let mut polynomials = vec![Vec::new(); N_WORDS];
        let mut term_index: HashMap<Mono, Vec<u16>> = HashMap::new();
        for code in 0..N_WORDS {
            if !allowed[code] { continue; }
            let word = decode_word(code as u16);
            let mut terms = BTreeMap::<Mono, i32>::new();
            for matching in &matchings {
                let mut ids = Vec::new();
                for &(left, right) in matching {
                    let edge = edge_id[left as usize][right as usize] as usize;
                    let coordinate = edge * 9
                        + word[left as usize] as usize * 3
                        + word[right as usize] as usize;
                    if !support[coordinate] { ids.push(coordinate as u8); }
                }
                *terms.entry(Mono::new(ids)).or_default() += 1;
            }
            polynomials[code] = terms.into_iter().collect();
            for &(term, _) in &polynomials[code] {
                term_index.entry(term).or_default().push(code as u16);
            }
        }

        Self {
            actions, polynomials, term_index,
            row_cache: HashMap::new(), column_cache: HashMap::new(),
            incident_cache: HashMap::new(), output_cache: HashMap::new(),
        }
    }

    fn moved_mono(&self, value: Mono, action: usize) -> Mono {
        Mono::new(value.slice().iter()
                  .map(|&item| self.actions[action].var_map[item as usize])
                  .collect())
    }

    fn canonical_row(&mut self, row: Mono) -> Mono {
        if let Some(&answer) = self.row_cache.get(&row) { return answer; }
        let answer = (0..self.actions.len())
            .map(|action| self.moved_mono(row, action)).min().unwrap();
        self.row_cache.insert(row, answer);
        answer
    }

    fn moved_column(&self, column: Column, action: usize) -> Column {
        Column {
            word: self.actions[action].word_map[column.word as usize],
            multiplier: self.moved_mono(column.multiplier, action),
        }
    }

    fn column_orbit(&self, column: Column) -> BTreeSet<Column> {
        (0..self.actions.len())
            .map(|action| self.moved_column(column, action)).collect()
    }

    fn canonical_column(&mut self, column: Column) -> Column {
        if let Some(&answer) = self.column_cache.get(&column) { return answer; }
        let answer = self.column_orbit(column).into_iter().min().unwrap();
        self.column_cache.insert(column, answer);
        answer
    }

    fn divisors(&self, row: Mono) -> BTreeSet<Mono> {
        let mut answer = BTreeSet::new();
        for mask in 0..(1_usize << row.len) {
            if mask.count_ones() as usize > GENERATOR_DEGREE { continue; }
            let ids = row.slice().iter().enumerate()
                .filter_map(|(index, &value)| ((mask >> index) & 1 == 1).then_some(value))
                .collect();
            answer.insert(Mono::new(ids));
        }
        answer
    }

    fn incident_columns(&mut self, row: Mono) -> Vec<Column> {
        if let Some(answer) = self.incident_cache.get(&row) { return answer.clone(); }
        let mut answer = BTreeSet::new();
        for term in self.divisors(row) {
            let multiplier_len = row.len as usize - term.len as usize;
            if multiplier_len > MULTIPLIER_DEGREE { continue; }
            let Some(codes) = self.term_index.get(&term).cloned() else { continue; };
            let multiplier = row.quotient(term).unwrap();
            for code in codes {
                let column = self.canonical_column(Column { word: code, multiplier });
                answer.insert(column);
            }
        }
        let answer: Vec<_> = answer.into_iter().collect();
        self.incident_cache.insert(row, answer.clone());
        answer
    }

    fn invariant_outputs(&mut self, column: Column) -> BTreeMap<Mono, i32> {
        if let Some(answer) = self.output_cache.get(&column) { return answer.clone(); }
        if column.multiplier.len as usize > MULTIPLIER_DEGREE {
            fail("column multiplier escaped degree three");
        }
        let mut answer = BTreeMap::new();
        for actual in self.column_orbit(column) {
            let terms = self.polynomials[actual.word as usize].clone();
            for (term, coefficient) in terms {
                let row = actual.multiplier.concat(term);
                if self.canonical_row(row) == row {
                    *answer.entry(row).or_default() += coefficient;
                }
            }
        }
        if answer.is_empty() { fail("invariant column image vanished"); }
        self.output_cache.insert(column, answer.clone());
        answer
    }
}

fn census(engine: &mut Engine, seed: &BTreeMap<Mono, i32>, literal_words: usize) {
    let started = Instant::now();
    let mut columns = BTreeSet::new();
    let mut option_histogram = BTreeMap::<usize, usize>::new();
    for &row in seed.keys() {
        if engine.canonical_row(row) != row { fail("seed row is not canonical"); }
        let options = engine.incident_columns(row);
        *option_histogram.entry(options.len()).or_default() += 1;
        columns.extend(options);
    }
    let mut rows = BTreeSet::new();
    let mut support_histogram = BTreeMap::<usize, usize>::new();
    let mut coefficient_histogram = BTreeMap::<i32, usize>::new();
    for &column in &columns {
        let outputs = engine.invariant_outputs(column);
        *support_histogram.entry(outputs.len()).or_default() += 1;
        for (&row, &coefficient) in &outputs {
            rows.insert(row);
            *coefficient_histogram.entry(coefficient).or_default() += 1;
        }
    }
    let mut degree_histogram = BTreeMap::<usize, usize>::new();
    for row in &rows { *degree_histogram.entry(row.len as usize).or_default() += 1; }
    let expected = match literal_words {
        78 => (294, 25_153, BTreeMap::from([
            (0, 1), (2, 16), (3, 70), (4, 419),
            (5, 2330), (6, 7906), (7, 14_411),
        ])),
        6558 => (902, 78_081, BTreeMap::from([
            (0, 1), (2, 16), (3, 111), (4, 953),
            (5, 5837), (6, 23_922), (7, 47_241),
        ])),
        _ => fail("unsupported census packet"),
    };
    if columns.len() != expected.0 || rows.len() != expected.1
        || degree_histogram != expected.2 {
        fail("frozen 294-column/25153-row root census changed");
    }
    println!(
        "CENSUS_SUCCESS target_rows={} columns={} one_hop_rows={} option_histogram={:?} degree_histogram={:?} support_histogram={:?} coefficient_histogram={:?} elapsed={:.3}s",
        seed.len(), columns.len(), rows.len(), option_histogram, degree_histogram,
        support_histogram, coefficient_histogram, started.elapsed().as_secs_f64()
    );
}

fn prove_dfs(
    engine: &mut Engine,
    row: Mono,
    state: &mut DfsState,
    limits: &Limits,
    depth: usize,
) -> Result<bool, DfsLimit> {
    state.calls += 1;
    state.maximum_depth = state.maximum_depth.max(depth);
    if state.calls > limits.call_cap { return Err(DfsLimit::Calls); }
    if state.assigned.len() > limits.row_cap { return Err(DfsLimit::Rows); }
    if state.calls % 10_000 == 0 {
        if Instant::now() >= limits.deadline { return Err(DfsLimit::Wall); }
        eprintln!(
            "dfs calls={} assigned={} visiting={} depth={} row_degree={}",
            state.calls, state.assigned.len(), state.visiting.len(), depth, row.len
        );
    }
    if state.assigned.contains_key(&row) { return Ok(true); }
    if !state.visiting.insert(row) { return Ok(false); }

    let mut options = Vec::new();
    for column in engine.incident_columns(row) {
        if state.used.contains(&column) { continue; }
        let outputs = engine.invariant_outputs(column);
        let Some(&diagonal) = outputs.get(&row) else {
            fail("incident column lost its row");
        };
        let dependencies: Vec<_> = outputs.keys()
            .filter(|&&other| other != row).copied().collect();
        options.push((dependencies.len(), column, dependencies, diagonal));
    }
    options.sort_by_key(|(count, column, _, _)| (*count, *column));
    let option_count = options.len();
    for (_, column, dependencies, diagonal) in options {
        if state.used.contains(&column) { continue; }
        let mut complete = true;
        for dependency in dependencies {
            if !prove_dfs(engine, dependency, state, limits, depth + 1)? {
                complete = false;
                break;
            }
        }
        if complete {
            if state.used.contains(&column) { continue; }
            state.used.insert(column);
            state.assigned.insert(row, column);
            state.order.push((row, column, diagonal));
            state.visiting.remove(&row);
            return Ok(true);
        }
    }
    state.visiting.remove(&row);
    state.last_dead_end = Some((row, option_count));
    Ok(false)
}

fn write_certificate(
    engine: &mut Engine,
    seed: &BTreeMap<Mono, i32>,
    state: &DfsState,
    path: &Path,
) {
    let mut seen = HashSet::new();
    let mut used = HashSet::new();
    for &(row, column, diagonal) in &state.order {
        if diagonal == 0 || !seen.insert(row) || !used.insert(column) {
            fail("bad DFS pivot ledger");
        }
        let outputs = engine.invariant_outputs(column);
        if outputs.get(&row) != Some(&diagonal) {
            fail("DFS diagonal replay changed");
        }
        if !outputs.keys().all(|other| *other == row || seen.contains(other)) {
            fail("DFS order is not triangular");
        }
    }
    if !seed.keys().all(|row| seen.contains(row)) {
        fail("DFS certificate omitted a target row");
    }
    let mut output = BufWriter::new(File::create(path).unwrap_or_else(|error| fail(error.to_string())));
    writeln!(output, "KRENN_N8_HOMOGENEOUS_DFS_V1 7 {} {}", seed.len(), state.order.len()).unwrap();
    for &(row, column, diagonal) in &state.order {
        writeln!(output, "PIVOT {} || {} {} || {}",
                 mono_hex(row), column.word, mono_hex(column.multiplier), diagonal).unwrap();
    }
    output.flush().unwrap();
}

fn write_failure(
    seed: &BTreeMap<Mono, i32>,
    state: &DfsState,
    path: &Path,
    target_index: usize,
    target: Mono,
    reason: &str,
    engine: &Engine,
) {
    let mut output = BufWriter::new(File::create(path).unwrap_or_else(|error| fail(error.to_string())));
    writeln!(output,
             "KRENN_N8_HOMOGENEOUS_DFS_FAILURE_V1 7 {} {} {} {} {} {}",
             seed.len(), target_index, mono_hex(target), reason, state.calls, state.assigned.len()).unwrap();
    writeln!(output, "STATS used={} visiting={} order={} max_depth={} incident_cache={} output_cache={}",
             state.used.len(), state.visiting.len(), state.order.len(), state.maximum_depth,
             engine.incident_cache.len(), engine.output_cache.len()).unwrap();
    if let Some((row, options)) = state.last_dead_end {
        writeln!(output, "LAST_DEAD_END {} options={}", mono_hex(row), options).unwrap();
    }
    for row in state.visiting.iter().copied().take(256) {
        writeln!(output, "VISITING {}", mono_hex(row)).unwrap();
    }
    output.flush().unwrap();
}

fn dfs_gate(
    mut engine: Engine,
    seed: BTreeMap<Mono, i32>,
    certificate: &Path,
    failure: &Path,
    wall_seconds: u64,
    call_cap: usize,
    row_cap: usize,
) {
    let started = Instant::now();
    let limits = Limits {
        call_cap, row_cap,
        deadline: started + Duration::from_secs(wall_seconds),
    };
    let mut state = DfsState {
        assigned: HashMap::new(), used: HashSet::new(), visiting: HashSet::new(),
        order: Vec::new(), calls: 0, maximum_depth: 0, last_dead_end: None,
    };
    let targets: Vec<_> = seed.keys().copied().collect();
    for (index, row) in targets.into_iter().enumerate() {
        let outcome = prove_dfs(&mut engine, row, &mut state, &limits, 1);
        match outcome {
            Ok(true) => {},
            Ok(false) => {
                write_failure(&seed, &state, failure, index + 1, row, "DEAD_END", &engine);
                eprintln!("DFS_FAILURE target={}/{} row={} assigned={} calls={} elapsed={:.3}s packet={}",
                          index + 1, seed.len(), mono_hex(row), state.assigned.len(), state.calls,
                          started.elapsed().as_secs_f64(), failure.display());
                std::process::exit(3);
            },
            Err(limit) => {
                let reason = match limit {
                    DfsLimit::Calls => "CALL_CAP",
                    DfsLimit::Rows => "ROW_CAP",
                    DfsLimit::Wall => "WALL_CAP",
                };
                write_failure(&seed, &state, failure, index + 1, row, reason, &engine);
                eprintln!("DFS_LIMIT reason={} target={}/{} row={} assigned={} calls={} elapsed={:.3}s packet={}",
                          reason, index + 1, seed.len(), mono_hex(row), state.assigned.len(), state.calls,
                          started.elapsed().as_secs_f64(), failure.display());
                std::process::exit(4);
            },
        }
        if (index + 1) % 25 == 0 {
            eprintln!("dfs targets={}/{} pivots={} calls={} elapsed={:.3}s",
                      index + 1, seed.len(), state.order.len(), state.calls,
                      started.elapsed().as_secs_f64());
        }
    }
    write_certificate(&mut engine, &seed, &state, certificate);
    eprintln!("DFS_SUCCESS pivots={} calls={} max_depth={} certificate={} bytes={} elapsed={:.3}s",
              state.order.len(), state.calls, state.maximum_depth, certificate.display(),
              certificate.metadata().unwrap().len(), started.elapsed().as_secs_f64());
}

fn main() {
    let arguments: Vec<_> = env::args().collect();
    if arguments.len() < 4 {
        fail("usage: n8-normalized-dfs-degree7 SEED WORDS --census | --dfs CERT FAILURE [WALL CALLS ROWS] | --dfs-root HEX CERT FAILURE [WALL CALLS ROWS]");
    }
    let seed = read_seed(Path::new(&arguments[1]));
    let packet = read_words(Path::new(&arguments[2]));
    let literal_words = packet.literal_words;
    let mut engine = Engine::new(packet);
    census(&mut engine, &seed, literal_words);
    match arguments[3].as_str() {
        "--census" => {
            if arguments.len() != 4 { fail("--census takes no more arguments"); }
        },
        "--dfs" => {
            if arguments.len() < 6 || arguments.len() > 9 {
                fail("--dfs requires CERT FAILURE [WALL_SECONDS CALL_CAP ROW_CAP]");
            }
            let wall_seconds = arguments.get(6).map(|value| value.parse().unwrap_or_else(|_| fail("bad wall cap"))).unwrap_or(110);
            let call_cap = arguments.get(7).map(|value| value.parse().unwrap_or_else(|_| fail("bad call cap"))).unwrap_or(2_000_000);
            let row_cap = arguments.get(8).map(|value| value.parse().unwrap_or_else(|_| fail("bad row cap"))).unwrap_or(200_000);
            std::thread::Builder::new().name("n8-d7-dfs".into())
                .stack_size(1024 * 1024 * 1024)
                .spawn(move || dfs_gate(
                    engine, seed, Path::new(&arguments[4]), Path::new(&arguments[5]),
                    wall_seconds, call_cap, row_cap,
                ))
                .unwrap_or_else(|error| fail(error.to_string())).join()
                .unwrap_or_else(|_| fail("DFS worker panicked"));
        },
        "--dfs-root" => {
            if arguments.len() < 7 || arguments.len() > 10 {
                fail("--dfs-root requires HEX CERT FAILURE [WALL_SECONDS CALL_CAP ROW_CAP]");
            }
            let root = parse_hex(&arguments[4]);
            let Some(&coefficient) = seed.get(&root) else {
                fail("requested root is not in the frozen tail seed");
            };
            let root_seed = BTreeMap::from([(root, coefficient)]);
            let wall_seconds = arguments.get(7).map(|value| value.parse().unwrap_or_else(|_| fail("bad wall cap"))).unwrap_or(290);
            let call_cap = arguments.get(8).map(|value| value.parse().unwrap_or_else(|_| fail("bad call cap"))).unwrap_or(10_000_000);
            let row_cap = arguments.get(9).map(|value| value.parse().unwrap_or_else(|_| fail("bad row cap"))).unwrap_or(500_000);
            std::thread::Builder::new().name("n8-d7-root-dfs".into())
                .stack_size(1024 * 1024 * 1024)
                .spawn(move || dfs_gate(
                    engine, root_seed, Path::new(&arguments[5]), Path::new(&arguments[6]),
                    wall_seconds, call_cap, row_cap,
                ))
                .unwrap_or_else(|error| fail(error.to_string())).join()
                .unwrap_or_else(|_| fail("DFS worker panicked"));
        },
        _ => fail("expected --census, --dfs, or --dfs-root"),
    }
}
