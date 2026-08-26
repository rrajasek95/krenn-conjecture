//! Whole degree<=12 Macaulay component after normalizing the twelve orbit0
//! anchor variables to one.  Rows retain only nonanchor factors.

use std::collections::{BTreeMap, HashMap, HashSet};
use std::env;
use std::fs::{self, File};
use std::io::{self, BufRead, BufReader, BufWriter, Read, Write};
use std::path::Path;
use std::time::Instant;

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Mono {
    len: u8,
    cells: [u8; 12],
}
#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Column {
    word: u16,
    multiplier: Mono,
}
#[derive(Clone, Copy)]
struct Action {
    sites: [u8; 8],
    colours: [u8; 3],
}
struct Seed {
    anchors: [bool; 252],
    actions: Vec<Action>,
}
struct Engine {
    anchors: [bool; 252],
    cell_u: [u8; 252],
    cell_v: [u8; 252],
    cell_a: [u8; 252],
    cell_b: [u8; 252],
    edge_id: [[u8; 8]; 8],
    transforms: Vec<[u8; 252]>,
    word_transforms: Vec<Vec<u16>>,
    minimum_actions: Vec<Vec<u16>>,
    terms: Vec<Vec<Mono>>,
    word_minimum: [u8; 6561],
    pair_constant_only: bool,
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("normalized-anchor: {}", message.as_ref());
    std::process::exit(2)
}
fn nibble(b: u8) -> u8 {
    match b {
        b'0'..=b'9' => b - b'0',
        b'a'..=b'f' => b - b'a' + 10,
        b'A'..=b'F' => b - b'A' + 10,
        _ => fail("bad hex"),
    }
}
fn parse_hex<const N: usize>(s: &str) -> [u8; N] {
    if s.len() != 2 * N {
        fail("bad hex length")
    }
    let b = s.as_bytes();
    let mut out = [0; N];
    for i in 0..N {
        out[i] = 16 * nibble(b[2 * i]) + nibble(b[2 * i + 1]);
    }
    out
}
fn encode_word(s: &[u8; 8]) -> u16 {
    s.iter().fold(0, |code, d| 3 * code + *d as u16)
}
fn decode_word(mut code: u16) -> [u8; 8] {
    let mut w = [0; 8];
    for i in (0..8).rev() {
        w[i] = (code % 3) as u8;
        code /= 3;
    }
    w
}
fn hex(m: Mono) -> String {
    const H: &[u8; 16] = b"0123456789abcdef";
    let mut s = String::with_capacity(2 * m.len as usize);
    for &b in &m.cells[..m.len as usize] {
        s.push(H[(b >> 4) as usize] as char);
        s.push(H[(b & 15) as usize] as char)
    }
    s
}
fn mono(cells: &[u8]) -> Mono {
    if cells.len() > 12 {
        fail("monomial degree exceeds12")
    }
    let mut data = [255; 12];
    let mut sorted = cells.to_vec();
    sorted.sort_unstable();
    data[..sorted.len()].copy_from_slice(&sorted);
    Mono {
        len: sorted.len() as u8,
        cells: data,
    }
}
fn product(left: Mono, right: Mono) -> Mono {
    let mut cells = Vec::with_capacity(left.len as usize + right.len as usize);
    cells.extend_from_slice(&left.cells[..left.len as usize]);
    cells.extend_from_slice(&right.cells[..right.len as usize]);
    mono(&cells)
}

fn parse_seed(path: &Path) -> io::Result<Seed> {
    let mut anchors = [false; 252];
    let mut actions = Vec::new();
    for (number, line) in BufReader::new(File::open(path)?).lines().enumerate() {
        let line = line?;
        let f: Vec<_> = line.split_whitespace().collect();
        if f.is_empty() {
            continue;
        }
        match f[0] {
            "KRENN_ORBIT0_R8_SEED_V1" => {
                if number != 0 {
                    fail("magic not first")
                }
            }
            "ANCHORS" => {
                for c in parse_hex::<12>(f[1]) {
                    anchors[c as usize] = true
                }
            }
            "ACTION" => {
                let mut sites = [0; 8];
                let mut colours = [0; 3];
                for (i, b) in f[1].bytes().enumerate() {
                    sites[i] = b - b'0'
                }
                for (i, b) in f[2].bytes().enumerate() {
                    colours[i] = b - b'0'
                }
                actions.push(Action { sites, colours })
            }
            "SCALE" | "R8" => {}
            _ => fail("unknown seed record"),
        }
    }
    if actions.len() != 2304 {
        fail("action count")
    };
    Ok(Seed { anchors, actions })
}

fn parse_support(path: &Path) -> io::Result<Vec<Mono>> {
    let mut rows = Vec::new();
    for line in BufReader::new(File::open(path)?).lines() {
        let line = line?;
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.is_empty() {
            continue;
        }
        if fields[0] != "ROW" {
            fail("unknown support record");
        }
        if fields[1] == "-" {
            rows.push(mono(&[]));
        } else {
            if fields[1].len() % 2 != 0 || fields[1].len() > 24 {
                fail("bad support row");
            }
            let mut cells = Vec::new();
            for pair in fields[1].as_bytes().chunks_exact(2) {
                cells.push(16 * nibble(pair[0]) + nibble(pair[1]));
            }
            rows.push(mono(&cells));
        }
    }
    Ok(rows)
}

fn parse_columns(path: &Path) -> io::Result<Vec<Column>> {
    let mut columns = Vec::new();
    for (number, line) in BufReader::new(File::open(path)?).lines().enumerate() {
        let line = line?;
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.is_empty() { continue; }
        if number == 0 {
            if fields != ["KRENN_NORMALIZED_ANCHOR_PRUNE_COLUMNS_V1"] {
                fail("bad prune-column ledger magic");
            }
            continue;
        }
        if fields.len() != 4 || fields[0] != "COLUMN" {
            fail("bad prune-column record");
        }
        let index = fields[1].parse::<usize>().unwrap_or_else(|_| fail("bad column index"));
        if index != columns.len() || fields[2].len() != 8 {
            fail("nonsequential column ledger");
        }
        let mut word = [0u8; 8];
        for (i, digit) in fields[2].bytes().enumerate() {
            if !(b'0'..=b'2').contains(&digit) { fail("bad word digit"); }
            word[i] = digit - b'0';
        }
        let multiplier = if fields[3] == "-" {
            mono(&[])
        } else {
            if fields[3].len() % 2 != 0 || fields[3].len() > 16 {
                fail("bad column multiplier");
            }
            let mut cells = Vec::new();
            for pair in fields[3].as_bytes().chunks_exact(2) {
                cells.push(16 * nibble(pair[0]) + nibble(pair[1]));
            }
            mono(&cells)
        };
        columns.push(Column { word: encode_word(&word), multiplier });
    }
    Ok(columns)
}
fn matchings() -> Vec<[(u8, u8); 4]> {
    fn rec(v: &[u8], p: &mut Vec<(u8, u8)>, o: &mut Vec<[(u8, u8); 4]>) {
        if v.is_empty() {
            o.push([p[0], p[1], p[2], p[3]]);
            return;
        }
        for i in 1..v.len() {
            let mut r = Vec::new();
            r.extend_from_slice(&v[1..i]);
            r.extend_from_slice(&v[i + 1..]);
            p.push((v[0], v[i]));
            rec(&r, p, o);
            p.pop();
        }
    }
    let mut o = Vec::new();
    rec(&[0, 1, 2, 3, 4, 5, 6, 7], &mut Vec::new(), &mut o);
    o
}

impl Engine {
    fn new(seed: &Seed, pair_constant_only: bool) -> Self {
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
                        cell_b[id] = b
                    }
                }
                edge += 1
            }
        }
        let cid = |u: u8, v: u8, a: u8, b: u8| -> u8 {
            (edge_id[u as usize][v as usize] as usize * 9 + a as usize * 3 + b as usize) as u8
        };
        let mut transforms = Vec::new();
        let mut word_transforms = Vec::new();
        for action in &seed.actions {
            let mut t = [0; 252];
            for id in 0..252 {
                let (mut u, mut v) = (
                    action.sites[cell_u[id] as usize],
                    action.sites[cell_v[id] as usize],
                );
                let (mut a, mut b) = (
                    action.colours[cell_a[id] as usize],
                    action.colours[cell_b[id] as usize],
                );
                if u > v {
                    std::mem::swap(&mut u, &mut v);
                    std::mem::swap(&mut a, &mut b)
                }
                t[id] = cid(u, v, a, b)
            }
            transforms.push(t);
            let mut wt = vec![0u16; 6561];
            for code in 0..6561u16 {
                let word = decode_word(code);
                let mut image = [0; 8];
                for site in 0..8 {
                    image[action.sites[site] as usize] = action.colours[word[site] as usize]
                }
                wt[code as usize] = encode_word(&image)
            }
            word_transforms.push(wt)
        }
        let mut minimum_actions: Vec<Vec<u16>> = (0..6561).map(|_| Vec::new()).collect();
        for code in 0..6561usize {
            let min = word_transforms.iter().map(|t| t[code]).min().unwrap();
            for (a, t) in word_transforms.iter().enumerate() {
                if t[code] == min {
                    minimum_actions[code].push(a as u16)
                }
            }
        }
        let ms = matchings();
        let mut terms: Vec<Vec<Mono>> = Vec::with_capacity(6561);
        let mut word_minimum = [4; 6561];
        for code in 0..6561u16 {
            let word = decode_word(code);
            let mut list = Vec::with_capacity(105);
            for matching in &ms {
                let mut cells = Vec::new();
                for &(u, v) in matching {
                    let c = cid(u, v, word[u as usize], word[v as usize]);
                    if !seed.anchors[c as usize] {
                        cells.push(c)
                    }
                }
                list.push(mono(&cells))
            }
            word_minimum[code as usize] = list.iter().map(|m| m.len).min().unwrap();
            terms.push(list)
        }
        Self {
            anchors: seed.anchors,
            cell_u,
            cell_v,
            cell_a,
            cell_b,
            edge_id,
            transforms,
            word_transforms,
            minimum_actions,
            terms,
            word_minimum,
            pair_constant_only,
        }
    }
    fn canonical_mono(&self, m: Mono, cache: &mut HashMap<Mono, Mono>) -> Mono {
        if let Some(&x) = cache.get(&m) {
            return x;
        }
        let mut best = None;
        for t in &self.transforms {
            let mut cells = [255; 12];
            for i in 0..m.len as usize {
                cells[i] = t[m.cells[i] as usize]
            }
            cells[..m.len as usize].sort_unstable();
            let c = Mono { len: m.len, cells };
            if best.map_or(true, |old| c < old) {
                best = Some(c)
            }
        }
        let x = best.unwrap();
        if cache.len() < 500_000 {
            cache.insert(m, x);
        }
        x
    }
    fn canonical_column(&self, c: Column) -> Column {
        let mut best = None;
        let code = c.word as usize;
        let minword = self.word_transforms[self.minimum_actions[code][0] as usize][code];
        for &a in &self.minimum_actions[code] {
            let t = &self.transforms[a as usize];
            let mut cells = [255; 12];
            for i in 0..c.multiplier.len as usize {
                cells[i] = t[c.multiplier.cells[i] as usize]
            }
            cells[..c.multiplier.len as usize].sort_unstable();
            let x = Column {
                word: minword,
                multiplier: Mono {
                    len: c.multiplier.len,
                    cells,
                },
            };
            if best.map_or(true, |old| x < old) {
                best = Some(x)
            }
        }
        best.unwrap()
    }
    fn remove_selected(row: Mono, positions: &[usize]) -> Mono {
        let chosen: HashSet<_> = positions.iter().copied().collect();
        let cells: Vec<_> = (0..row.len as usize)
            .filter(|i| !chosen.contains(i))
            .map(|i| row.cells[i])
            .collect();
        mono(&cells)
    }
    fn incident(&self, row: Mono) -> HashSet<Column> {
        let mut answer = HashSet::new();
        let n = row.len as usize;
        for size in 0..=4.min(n) {
            let mut chosen = Vec::new();
            self.incident_rec(row, size, 0, &mut chosen, &mut answer)
        }
        answer
    }
    fn incident_rec(
        &self,
        row: Mono,
        want: usize,
        start: usize,
        chosen: &mut Vec<usize>,
        answer: &mut HashSet<Column>,
    ) {
        if chosen.len() != want {
            for i in start..row.len as usize {
                chosen.push(i);
                self.incident_rec(row, want, i + 1, chosen, answer);
                chosen.pop();
            }
            return;
        }
        let mut mask = 0u16;
        let mut word = [255u8; 8];
        for &position in chosen.iter() {
            let id = row.cells[position] as usize;
            let u = self.cell_u[id] as usize;
            let v = self.cell_v[id] as usize;
            let bits = (1 << u) | (1 << v);
            if mask & bits != 0 {
                return;
            }
            mask |= bits;
            word[u] = self.cell_a[id];
            word[v] = self.cell_b[id]
        }
        let mut uncovered = Vec::new();
        for pair in 0..4 {
            let left = 2 * pair;
            let a = mask & (1 << left) != 0;
            let b = mask & (1 << (left + 1)) != 0;
            if a != b {
                return;
            }
            if !a {
                uncovered.push(pair)
            }
        }
        let assignments = 3usize.pow(uncovered.len() as u32);
        for mut code in 0..assignments {
            let mut completed = word;
            for &pair in &uncovered {
                let colour = (code % 3) as u8;
                code /= 3;
                completed[2 * pair] = colour;
                completed[2 * pair + 1] = colour
            }
            if completed.iter().all(|c| *c == completed[0]) {
                continue;
            }
            if self.pair_constant_only
                && (0..4).any(|pair| completed[2 * pair] != completed[2 * pair + 1])
            {
                continue;
            }
            let word_code = encode_word(&completed);
            if self.word_minimum[word_code as usize] as usize > want {
                fail("incidence term below word minimum")
            };
            let raw = Column {
                word: word_code,
                multiplier: Self::remove_selected(row, chosen),
            };
            // Sound bounded Macaulay component: every specialized H_w has
            // maximum degree four, so multiplier degree at most eight keeps
            // every literal output at degree at most twelve. No tail is
            // truncated.
            if raw.multiplier.len > 8 {
                continue;
            }
            answer.insert(self.canonical_column(raw));
        }
    }
    fn outputs(&self, column: Column, cache: &mut HashMap<Mono, Mono>) -> Vec<(Mono, u8)> {
        let mut accumulated: BTreeMap<Mono, u8> = BTreeMap::new();
        for &term in &self.terms[column.word as usize] {
            if column.multiplier.len + term.len > 12 {
                fail("degree<=8 multiplier emitted a degree>12 tail");
            }
            let raw = product(column.multiplier, term);
            let row = self.canonical_mono(raw, cache);
            *accumulated.entry(row).or_default() += 1
        }
        accumulated.into_iter().collect()
    }

    fn outputs_top12(&self, column: Column, cache: &mut HashMap<Mono, Mono>) -> Vec<(Mono, u8)> {
        if column.multiplier.len != 8 {
            fail("top block column multiplier is not degree eight");
        }
        let mut accumulated: BTreeMap<Mono, u8> = BTreeMap::new();
        for &term in &self.terms[column.word as usize] {
            if term.len != 4 {
                continue;
            }
            let row = self.canonical_mono(product(column.multiplier, term), cache);
            *accumulated.entry(row).or_default() += 1;
        }
        accumulated.into_iter().collect()
    }
}

fn build_target(engine: &Engine, workers: usize) -> BTreeMap<Mono, i64> {
    let pure = [&engine.terms[0], &engine.terms[3280], &engine.terms[6560]];
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
            let p = pure;
            handles.push(scope.spawn(move || {
                let begun = Instant::now();
                let mut out: BTreeMap<Mono, i64> = BTreeMap::new();
                let mut cache = HashMap::new();
                for i in start..end {
                    for j in 0..105 {
                        for k in 0..105 {
                            let row = product(product(p[0][i], p[1][j]), p[2][k]);
                            let canonical = engine.canonical_mono(row, &mut cache);
                            *out.entry(canonical).or_default() += 1
                        }
                    }
                }
                eprintln!(
                    "target worker={start}..{end} rows={} elapsed={:.3}s",
                    out.len(),
                    begun.elapsed().as_secs_f64()
                );
                out
            }));
        }
        for h in handles {
            pieces.push(h.join().unwrap_or_else(|_| fail("target worker panic")))
        }
    });
    let mut out = BTreeMap::new();
    for piece in pieces {
        for (row, value) in piece {
            *out.entry(row).or_default() += value
        }
    }
    out
}

fn closure(
    engine: &Engine,
    target: &BTreeMap<Mono, i64>,
    max_layers: Option<usize>,
) -> (HashSet<Mono>, HashSet<Column>, Vec<(usize, usize)>) {
    let mut rows: HashSet<_> = target.keys().copied().collect();
    let mut frontier: HashSet<_> = rows.clone();
    let mut columns = HashSet::new();
    let mut layers = Vec::new();
    let mut cache = HashMap::new();
    while !frontier.is_empty() {
        let before = columns.len();
        let mut new_rows = HashSet::new();
        for row in frontier {
            for column in engine.incident(row) {
                if !columns.insert(column) {
                    continue;
                }
                for (output, _count) in engine.outputs(column, &mut cache) {
                    if rows.insert(output) {
                        new_rows.insert(output);
                    }
                }
            }
        }
        layers.push((new_rows.len(), columns.len() - before));
        eprintln!(
            "layer={} +rows={} +cols={} totals={}/{}",
            layers.len(),
            new_rows.len(),
            columns.len() - before,
            rows.len(),
            columns.len()
        );
        frontier = new_rows;
        if max_layers.map_or(false, |bound| layers.len() >= bound) {
            break;
        }
    }
    (rows, columns, layers)
}

fn write_matrix(
    path: &Path,
    engine: &Engine,
    target: &BTreeMap<Mono, i64>,
    rows: &HashSet<Mono>,
    columns: &HashSet<Column>,
) -> io::Result<()> {
    let mut ordered_rows: Vec<_> = rows.iter().copied().collect();
    ordered_rows.sort_unstable();
    let row_index: HashMap<_, _> = ordered_rows
        .iter()
        .enumerate()
        .map(|(index, row)| (*row, index))
        .collect();
    let mut ordered_columns: Vec<_> = columns.iter().copied().collect();
    ordered_columns.sort_unstable();
    let mut out = File::create(path)?;
    write!(out, "{{\"column_count\":{},\"format\":\"krenn-orbit0-normalized-anchor-degree12-pairconstant-first-layer-v1\",\"row_count\":{},\"rows_hex\":[", ordered_columns.len(), ordered_rows.len())?;
    for (number, row) in ordered_rows.iter().enumerate() {
        if number != 0 {
            write!(out, ",")?;
        }
        write!(out, "\"{}\"", hex(*row))?;
    }
    write!(out, "],\"target\":[")?;
    for (number, (row, coefficient)) in target.iter().enumerate() {
        if number != 0 {
            write!(out, ",")?;
        }
        write!(out, "[{},{},1]", row_index[row], coefficient)?;
    }
    writeln!(out, "],\"type\":\"header\"}}")?;
    let mut cache = HashMap::new();
    for (index, column) in ordered_columns.iter().enumerate() {
        let mut entries: Vec<_> = engine
            .outputs(*column, &mut cache)
            .into_iter()
            .map(|(row, coefficient)| (row_index[&row], coefficient))
            .collect();
        entries.sort_unstable();
        write!(out, "{{\"entries\":[")?;
        for (number, (row, coefficient)) in entries.iter().enumerate() {
            if number != 0 {
                write!(out, ",")?;
            }
            write!(out, "[{row},{coefficient}]")?;
        }
        write!(
            out,
            "],\"index\":{index},\"multiplier\":\"{}\",\"type\":\"column\",\"word\":\"",
            hex(column.multiplier)
        )?;
        for digit in decode_word(column.word) {
            write!(out, "{digit}")?;
        }
        writeln!(out, "\"}}")?;
    }
    Ok(())
}

fn top12_closure(
    engine: &Engine,
    target: &BTreeMap<Mono, i64>,
) -> (
    BTreeMap<Mono, i64>,
    HashSet<Mono>,
    HashSet<Column>,
    Vec<(usize, usize)>,
) {
    let top_target: BTreeMap<_, _> = target
        .iter()
        .filter(|(row, _)| row.len == 12)
        .map(|(row, value)| (*row, *value))
        .collect();
    let mut rows: HashSet<_> = top_target.keys().copied().collect();
    let mut frontier: HashSet<_> = rows.clone();
    let mut columns = HashSet::new();
    let mut layers = Vec::new();
    let mut cache = HashMap::new();
    while !frontier.is_empty() {
        let before = columns.len();
        let mut new_rows = HashSet::new();
        for row in frontier {
            for column in engine.incident(row) {
                if column.multiplier.len != 8 || !columns.insert(column) {
                    continue;
                }
                for (output, _coefficient) in engine.outputs_top12(column, &mut cache) {
                    if rows.insert(output) {
                        new_rows.insert(output);
                    }
                }
            }
        }
        layers.push((new_rows.len(), columns.len() - before));
        eprintln!(
            "top12 layer={} +rows={} +cols={} totals={}/{}",
            layers.len(),
            new_rows.len(),
            columns.len() - before,
            rows.len(),
            columns.len()
        );
        frontier = new_rows;
    }
    (top_target, rows, columns, layers)
}

fn write_top_matrix(
    path: &Path,
    engine: &Engine,
    target: &BTreeMap<Mono, i64>,
    rows: &HashSet<Mono>,
    columns: &HashSet<Column>,
) -> io::Result<()> {
    let mut ordered_rows: Vec<_> = rows.iter().copied().collect();
    ordered_rows.sort_unstable();
    let row_index: HashMap<_, _> = ordered_rows
        .iter()
        .enumerate()
        .map(|(i, r)| (*r, i))
        .collect();
    let mut ordered_columns: Vec<_> = columns.iter().copied().collect();
    ordered_columns.sort_unstable();
    let mut out = File::create(path)?;
    write!(out, "{{\"column_count\":{},\"format\":\"krenn-orbit0-normalized-anchor-top12-v1\",\"row_count\":{},\"rows_hex\":[", ordered_columns.len(), ordered_rows.len())?;
    for (number, row) in ordered_rows.iter().enumerate() {
        if number != 0 {
            write!(out, ",")?;
        }
        write!(out, "\"{}\"", hex(*row))?;
    }
    write!(out, "],\"target\":[")?;
    for (number, (row, coefficient)) in target.iter().enumerate() {
        if number != 0 {
            write!(out, ",")?;
        }
        write!(out, "[{},{},1]", row_index[row], coefficient)?;
    }
    writeln!(out, "],\"type\":\"header\"}}")?;
    let mut cache = HashMap::new();
    for (index, column) in ordered_columns.iter().enumerate() {
        let mut entries: Vec<_> = engine
            .outputs_top12(*column, &mut cache)
            .into_iter()
            .map(|(row, c)| (row_index[&row], c))
            .collect();
        entries.sort_unstable();
        write!(out, "{{\"entries\":[")?;
        for (number, (row, coefficient)) in entries.iter().enumerate() {
            if number != 0 {
                write!(out, ",")?;
            }
            write!(out, "[{row},{coefficient}]")?;
        }
        write!(
            out,
            "],\"index\":{index},\"multiplier\":\"{}\",\"type\":\"column\",\"word\":\"",
            hex(column.multiplier)
        )?;
        for digit in decode_word(column.word) {
            write!(out, "{digit}")?;
        }
        writeln!(out, "\"}}")?;
    }
    Ok(())
}

#[derive(Default)]
struct SamplePiece {
    columns: HashSet<Column>,
    incidence: usize,
    row_histogram: BTreeMap<usize, usize>,
}

fn sample_overlap(engine: &Engine, rows: &[Mono], workers: usize) -> SamplePiece {
    let chunk = rows.len().div_ceil(workers);
    let mut pieces = Vec::new();
    std::thread::scope(|scope| {
        let mut handles = Vec::new();
        for worker in 0..workers {
            let start = worker * chunk;
            let end = ((worker + 1) * chunk).min(rows.len());
            if start >= end {
                continue;
            }
            handles.push(scope.spawn(move || {
                let mut piece = SamplePiece::default();
                for &row in &rows[start..end] {
                    let columns = engine.incident(row);
                    piece.incidence += columns.len();
                    *piece.row_histogram.entry(columns.len()).or_default() += 1;
                    piece.columns.extend(columns);
                }
                piece
            }));
        }
        for handle in handles {
            pieces.push(
                handle
                    .join()
                    .unwrap_or_else(|_| fail("sample worker panic")),
            );
        }
    });
    let mut answer = SamplePiece::default();
    for piece in pieces {
        answer.incidence += piece.incidence;
        for (degree, count) in piece.row_histogram {
            *answer.row_histogram.entry(degree).or_default() += count;
        }
        answer.columns.extend(piece.columns);
    }
    answer
}

fn write_sample(
    path: &Path,
    total_rows: usize,
    sample: &[Mono],
    piece: &SamplePiece,
    output_rows: usize,
    elapsed: f64,
) -> io::Result<()> {
    let mut out = File::create(path)?;
    write!(out, "{{\n  \"status\":\"UNAUDITED deterministic all-generator residual-support overlap estimate\",\n  \"support_rows\":{total_rows},\n  \"sample_rows\":{},\n  \"sample_incidence\":{},\n  \"sample_distinct_columns\":{},\n  \"estimated_total_incidence\":{},\n  \"bounded_output_columns\":{},\n  \"bounded_canonical_output_rows\":{output_rows},\n  \"row_incidence_histogram\":{{", sample.len(), piece.incidence, piece.columns.len(), piece.incidence as u128 * total_rows as u128 / sample.len() as u128, piece.columns.len().min(128))?;
    for (number, (degree, count)) in piece.row_histogram.iter().enumerate() {
        if number != 0 {
            write!(out, ",")?;
        }
        write!(out, "\"{degree}\":{count}")?;
    }
    write!(out, "}},\n  \"elapsed_seconds\":{elapsed:.6}\n}}\n")?;
    Ok(())
}

fn write_prune_columns(
    result_path: &Path,
    column_path: &Path,
    total_rows: usize,
    piece: &SamplePiece,
    elapsed: f64,
) -> io::Result<()> {
    let mut columns: Vec<_> = piece.columns.iter().copied().collect();
    columns.sort_unstable();
    let mut degree_histogram: BTreeMap<u8, usize> = BTreeMap::new();
    let mut ledger = BufWriter::new(File::create(column_path)?);
    writeln!(ledger, "KRENN_NORMALIZED_ANCHOR_PRUNE_COLUMNS_V1")?;
    for (index, column) in columns.iter().enumerate() {
        *degree_histogram.entry(column.multiplier.len).or_default() += 1usize;
        write!(ledger, "COLUMN {index} ")?;
        for digit in decode_word(column.word) {
            write!(ledger, "{digit}")?;
        }
        let multiplier = hex(column.multiplier);
        writeln!(ledger, " {}", if multiplier.is_empty() { "-" } else { &multiplier })?;
    }
    ledger.flush()?;

    let mut out = BufWriter::new(File::create(result_path)?);
    write!(out, "{{\n  \"status\":\"UNAUDITED exact normalized-anchor all-generator residual-overlap column census\",\n  \"support_rows\":{total_rows},\n  \"target_column_incidence\":{},\n  \"distinct_columns\":{},\n  \"multiplier_degree_histogram\":{{", piece.incidence, columns.len())?;
    for (number, (degree, count)) in degree_histogram.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "\"{degree}\":{count}")?;
    }
    write!(out, "}},\n  \"target_row_incidence_histogram\":{{")?;
    for (number, (degree, count)) in piece.row_histogram.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "\"{degree}\":{count}")?;
    }
    write!(out, "}},\n  \"column_ledger\":{:?},\n  \"elapsed_seconds\":{elapsed:.6}\n}}\n", column_path.to_string_lossy())?;
    Ok(())
}

#[derive(Clone, Copy, Eq, Ord, PartialEq, PartialOrd)]
struct IncidenceRecord {
    row: Mono,
    column: u32,
    coefficient: u8,
}

const INCIDENCE_RECORD_BYTES: usize = 18;
const INCIDENCE_BUCKETS: usize = 16;

fn row_bucket(row: Mono) -> usize {
    let mut hash = 0xcbf29ce484222325u64;
    hash ^= row.len as u64;
    hash = hash.wrapping_mul(0x100000001b3);
    for &cell in &row.cells[..row.len as usize] {
        hash ^= cell as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    (hash as usize) & (INCIDENCE_BUCKETS - 1)
}

fn write_record(out: &mut impl Write, record: IncidenceRecord) -> io::Result<()> {
    out.write_all(&[record.row.len])?;
    out.write_all(&record.row.cells)?;
    out.write_all(&record.column.to_le_bytes())?;
    out.write_all(&[record.coefficient])
}

fn read_records(path: &Path) -> io::Result<Vec<IncidenceRecord>> {
    let mut bytes = Vec::new();
    File::open(path)?.read_to_end(&mut bytes)?;
    if bytes.len() % INCIDENCE_RECORD_BYTES != 0 {
        fail("truncated incidence shard");
    }
    let mut records = Vec::with_capacity(bytes.len() / INCIDENCE_RECORD_BYTES);
    for raw in bytes.chunks_exact(INCIDENCE_RECORD_BYTES) {
        let mut cells = [255u8; 12];
        cells.copy_from_slice(&raw[1..13]);
        let row = Mono { len: raw[0], cells };
        let column = u32::from_le_bytes(raw[13..17].try_into().unwrap());
        records.push(IncidenceRecord { row, column, coefficient: raw[17] });
    }
    Ok(records)
}

#[derive(Default)]
struct IncidencePiece {
    records: usize,
    degree_histogram: BTreeMap<u8, usize>,
    cache_entries: usize,
    elapsed: f64,
}

fn write_incidence_buckets(
    engine: &Engine,
    columns: &[Column],
    output_dir: &Path,
    temporary_dir: &Path,
    workers: usize,
) -> io::Result<(Vec<usize>, Vec<IncidencePiece>)> {
    fs::create_dir_all(output_dir)?;
    fs::create_dir_all(temporary_dir)?;
    let chunk = columns.len().div_ceil(workers);
    let mut pieces = Vec::new();
    std::thread::scope(|scope| {
        let mut handles = Vec::new();
        for worker in 0..workers {
            let start = worker * chunk;
            let end = ((worker + 1) * chunk).min(columns.len());
            if start >= end { continue; }
            handles.push(scope.spawn(move || -> io::Result<(usize, IncidencePiece)> {
                let begun = Instant::now();
                let mut writers = Vec::new();
                for bucket in 0..INCIDENCE_BUCKETS {
                    let path = temporary_dir.join(format!("worker{worker:02}-bucket{bucket:02}.bin"));
                    writers.push(BufWriter::with_capacity(1 << 20, File::create(path)?));
                }
                let mut cache = HashMap::new();
                let mut piece = IncidencePiece::default();
                for (offset, &column) in columns[start..end].iter().enumerate() {
                    let column_index = (start + offset) as u32;
                    for (row, coefficient) in engine.outputs(column, &mut cache) {
                        let bucket = row_bucket(row);
                        write_record(&mut writers[bucket], IncidenceRecord {
                            row,
                            column: column_index,
                            coefficient,
                        })?;
                        piece.records += 1;
                        *piece.degree_histogram.entry(row.len).or_default() += 1;
                    }
                    if offset != 0 && offset % 25_000 == 0 {
                        eprintln!(
                            "incidence worker={worker} columns={offset}/{} records={} elapsed={:.1}s",
                            end - start,
                            piece.records,
                            begun.elapsed().as_secs_f64()
                        );
                    }
                }
                for writer in &mut writers { writer.flush()?; }
                piece.cache_entries = cache.len();
                piece.elapsed = begun.elapsed().as_secs_f64();
                Ok((worker, piece))
            }));
        }
        for handle in handles {
            pieces.push(handle.join().unwrap_or_else(|_| fail("incidence worker panic")));
        }
    });
    let mut ordered = Vec::new();
    for result in pieces { ordered.push(result?); }
    ordered.sort_by_key(|(worker, _)| *worker);
    let pieces: Vec<_> = ordered.into_iter().map(|(_, piece)| piece).collect();

    let mut bucket_counts = Vec::new();
    for bucket in 0..INCIDENCE_BUCKETS {
        let mut records = Vec::new();
        for worker in 0..pieces.len() {
            let path = temporary_dir.join(format!("worker{worker:02}-bucket{bucket:02}.bin"));
            records.extend(read_records(&path)?);
        }
        records.sort_unstable();
        let path = output_dir.join(format!("bucket{bucket:02}.bin"));
        let mut out = BufWriter::with_capacity(1 << 20, File::create(path)?);
        for record in &records { write_record(&mut out, *record)?; }
        out.flush()?;
        bucket_counts.push(records.len());
        eprintln!("merged bucket={bucket} records={}", records.len());
    }
    Ok((bucket_counts, pieces))
}

fn write_incidence_results(
    path: &Path,
    columns: usize,
    bucket_counts: &[usize],
    pieces: &[IncidencePiece],
    output_dir: &Path,
    elapsed: f64,
) -> io::Result<()> {
    let records: usize = bucket_counts.iter().sum();
    let mut degree_histogram: BTreeMap<u8, usize> = BTreeMap::new();
    for piece in pieces {
        for (&degree, &count) in &piece.degree_histogram {
            *degree_histogram.entry(degree).or_default() += count;
        }
    }
    let mut out = BufWriter::new(File::create(path)?);
    write!(out, "{{\n  \"status\":\"UNAUDITED exact normalized-anchor full-output incidence buckets\",\n  \"columns\":{columns},\n  \"incidence_records\":{records},\n  \"record_bytes\":{INCIDENCE_RECORD_BYTES},\n  \"bucket_count\":{INCIDENCE_BUCKETS},\n  \"bucket_record_counts\":[")?;
    for (number, count) in bucket_counts.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "{count}")?;
    }
    write!(out, "],\n  \"row_degree_incidence_histogram\":{{")?;
    for (number, (degree, count)) in degree_histogram.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "\"{degree}\":{count}")?;
    }
    write!(out, "}},\n  \"worker_cache_entries\":[")?;
    for (number, piece) in pieces.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "{}", piece.cache_entries)?;
    }
    write!(out, "],\n  \"worker_seconds\":[")?;
    for (number, piece) in pieces.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "{:.6}", piece.elapsed)?;
    }
    write!(out, "],\n  \"bucket_directory\":{:?},\n  \"elapsed_seconds\":{elapsed:.6}\n}}\n", output_dir.to_string_lossy())?;
    Ok(())
}

#[derive(Default)]
struct PrivateRound {
    relative_singleton_zero_rows: usize,
    previously_known_nonprivate: usize,
    newly_checked_nonprivate: usize,
    globally_private_rows: usize,
    newly_eliminated_columns: usize,
}

fn private_zero_cascade(
    engine: &Engine,
    columns: &[Column],
    target: &HashSet<Mono>,
    bucket_dir: &Path,
) -> io::Result<(Vec<bool>, Vec<PrivateRound>, HashSet<Mono>)> {
    let mut active = vec![true; columns.len()];
    let mut nonprivate = HashSet::new();
    let mut rounds = Vec::new();
    loop {
        let mut round = PrivateRound::default();
        let mut eliminate = HashSet::new();
        for bucket in 0..INCIDENCE_BUCKETS {
            let records = read_records(&bucket_dir.join(format!("bucket{bucket:02}.bin")))?;
            let mut begin = 0;
            while begin < records.len() {
                let row = records[begin].row;
                let mut end = begin + 1;
                while end < records.len() && records[end].row == row { end += 1; }
                if !target.contains(&row) {
                    let mut sole = None;
                    let mut count = 0usize;
                    for record in &records[begin..end] {
                        if active[record.column as usize] {
                            count += 1;
                            sole = Some(record.column as usize);
                            if count > 1 { break; }
                        }
                    }
                    if count == 1 {
                        round.relative_singleton_zero_rows += 1;
                        if nonprivate.contains(&row) {
                            round.previously_known_nonprivate += 1;
                        } else {
                            let incident = engine.incident(row);
                            if incident.len() == 1 {
                                let column = sole.unwrap();
                                if !incident.contains(&columns[column]) {
                                    fail("global private row does not contain its recorded column");
                                }
                                round.globally_private_rows += 1;
                                eliminate.insert(column);
                            } else {
                                nonprivate.insert(row);
                                round.newly_checked_nonprivate += 1;
                            }
                        }
                    }
                }
                begin = end;
            }
        }
        for &column in &eliminate {
            if active[column] {
                active[column] = false;
                round.newly_eliminated_columns += 1;
            }
        }
        eprintln!(
            "private round={} relative_singletons={} global_private={} eliminated={} nonprivate_new={} active={}",
            rounds.len() + 1,
            round.relative_singleton_zero_rows,
            round.globally_private_rows,
            round.newly_eliminated_columns,
            round.newly_checked_nonprivate,
            active.iter().filter(|&&value| value).count()
        );
        let done = round.newly_eliminated_columns == 0;
        rounds.push(round);
        if done { break; }
    }
    Ok((active, rounds, nonprivate))
}

fn write_private_results(
    path: &Path,
    active_path: &Path,
    columns: &[Column],
    active: &[bool],
    rounds: &[PrivateRound],
    nonprivate: &HashSet<Mono>,
    elapsed: f64,
) -> io::Result<()> {
    let mut ledger = BufWriter::new(File::create(active_path)?);
    writeln!(ledger, "KRENN_NORMALIZED_ANCHOR_ACTIVE_COLUMNS_V1")?;
    for (index, &value) in active.iter().enumerate() {
        if value { writeln!(ledger, "ACTIVE {index}")?; }
    }
    ledger.flush()?;
    let active_count = active.iter().filter(|&&value| value).count();
    let mut degree_histogram = BTreeMap::new();
    for (column, &value) in columns.iter().zip(active) {
        if value { *degree_histogram.entry(column.multiplier.len).or_insert(0usize) += 1; }
    }
    let mut out = BufWriter::new(File::create(path)?);
    write!(out, "{{\n  \"status\":\"UNAUDITED sound global-private-row cascade on normalized target-overlap layer\",\n  \"input_columns\":{},\n  \"active_columns\":{active_count},\n  \"eliminated_columns\":{},\n  \"known_nonprivate_relative_singleton_rows\":{},\n  \"rounds\":[", columns.len(), columns.len() - active_count, nonprivate.len())?;
    for (number, round) in rounds.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "{{\"relative_singleton_zero_rows\":{},\"previously_known_nonprivate\":{},\"newly_checked_nonprivate\":{},\"globally_private_rows\":{},\"newly_eliminated_columns\":{}}}", round.relative_singleton_zero_rows, round.previously_known_nonprivate, round.newly_checked_nonprivate, round.globally_private_rows, round.newly_eliminated_columns)?;
    }
    write!(out, "],\n  \"active_multiplier_degree_histogram\":{{")?;
    for (number, (degree, count)) in degree_histogram.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "\"{degree}\":{count}")?;
    }
    write!(out, "}},\n  \"scope\":\"A column is removed only when an output row has exactly one globally incident bounded-Macaulay column. Relative-private rows with missing remote columns are retained. This is sound pruning but is not yet complete component closure.\",\n  \"active_ledger\":{:?},\n  \"elapsed_seconds\":{elapsed:.6}\n}}\n", active_path.to_string_lossy())?;
    Ok(())
}

fn parse_active(path: &Path, column_count: usize) -> io::Result<Vec<bool>> {
    let mut active = vec![false; column_count];
    for (number, line) in BufReader::new(File::open(path)?).lines().enumerate() {
        let line = line?;
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.is_empty() { continue; }
        if number == 0 {
            if fields != ["KRENN_NORMALIZED_ANCHOR_ACTIVE_COLUMNS_V1"] {
                fail("bad active-column ledger magic");
            }
            continue;
        }
        if fields.len() != 2 || fields[0] != "ACTIVE" {
            fail("bad active-column record");
        }
        let column = fields[1].parse::<usize>().unwrap_or_else(|_| fail("bad active index"));
        if column >= active.len() || active[column] { fail("bad/duplicate active index"); }
        active[column] = true;
    }
    Ok(active)
}

#[derive(Clone, Copy, Eq, Ord, PartialEq, PartialOrd)]
struct RemoteRecord {
    column: Column,
    parent: Mono,
}

const REMOTE_RECORD_BYTES: usize = 28;

fn column_bucket(column: Column) -> usize {
    let mut hash = 0xcbf29ce484222325u64;
    hash ^= column.word as u64;
    hash = hash.wrapping_mul(0x100000001b3);
    hash ^= column.multiplier.len as u64;
    hash = hash.wrapping_mul(0x100000001b3);
    for &cell in &column.multiplier.cells[..column.multiplier.len as usize] {
        hash ^= cell as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    (hash as usize) & (INCIDENCE_BUCKETS - 1)
}

fn write_remote_record(out: &mut impl Write, record: RemoteRecord) -> io::Result<()> {
    out.write_all(&record.column.word.to_le_bytes())?;
    out.write_all(&[record.column.multiplier.len])?;
    out.write_all(&record.column.multiplier.cells)?;
    out.write_all(&[record.parent.len])?;
    out.write_all(&record.parent.cells)
}

fn read_remote_records(path: &Path) -> io::Result<Vec<RemoteRecord>> {
    let mut bytes = Vec::new();
    File::open(path)?.read_to_end(&mut bytes)?;
    if bytes.len() % REMOTE_RECORD_BYTES != 0 { fail("truncated remote record shard"); }
    let mut records = Vec::with_capacity(bytes.len() / REMOTE_RECORD_BYTES);
    for raw in bytes.chunks_exact(REMOTE_RECORD_BYTES) {
        let word = u16::from_le_bytes(raw[0..2].try_into().unwrap());
        let mut multiplier_cells = [255u8; 12];
        multiplier_cells.copy_from_slice(&raw[3..15]);
        let mut parent_cells = [255u8; 12];
        parent_cells.copy_from_slice(&raw[16..28]);
        records.push(RemoteRecord {
            column: Column {
                word,
                multiplier: Mono { len: raw[2], cells: multiplier_cells },
            },
            parent: Mono { len: raw[15], cells: parent_cells },
        });
    }
    Ok(records)
}

#[derive(Default)]
struct RemotePiece {
    active_rows: usize,
    raw_missing_occurrences: usize,
    global_incidence_histogram: BTreeMap<usize, usize>,
    elapsed: f64,
}

fn discover_remote_degree(
    engine: &Engine,
    columns: &[Column],
    active: &[bool],
    bucket_dir: &Path,
    temporary_dir: &Path,
    row_degree: u8,
    workers: usize,
) -> io::Result<(Vec<RemoteRecord>, Vec<RemotePiece>)> {
    fs::create_dir_all(temporary_dir)?;
    let known: HashSet<_> = columns.iter().copied().collect();
    if known.len() != columns.len() { fail("input column ledger has duplicates"); }
    let mut pieces = Vec::new();
    std::thread::scope(|scope| {
        let mut handles = Vec::new();
        for worker in 0..workers {
            let known = &known;
            handles.push(scope.spawn(move || -> io::Result<(usize, RemotePiece)> {
                let begun = Instant::now();
                let mut writers = Vec::new();
                for bucket in 0..INCIDENCE_BUCKETS {
                    let path = temporary_dir.join(format!("remote-worker{worker:02}-bucket{bucket:02}.bin"));
                    writers.push(BufWriter::with_capacity(1 << 20, File::create(path)?));
                }
                let mut piece = RemotePiece::default();
                for input_bucket in (worker..INCIDENCE_BUCKETS).step_by(workers) {
                    let records = read_records(&bucket_dir.join(format!("bucket{input_bucket:02}.bin")))?;
                    let mut begin = 0;
                    while begin < records.len() {
                        let row = records[begin].row;
                        let mut end = begin + 1;
                        while end < records.len() && records[end].row == row { end += 1; }
                        if row.len == row_degree
                            && records[begin..end].iter().any(|record| active[record.column as usize])
                        {
                            piece.active_rows += 1;
                            let incident = engine.incident(row);
                            *piece.global_incidence_histogram.entry(incident.len()).or_default() += 1;
                            for column in incident {
                                if !known.contains(&column) {
                                    let bucket = column_bucket(column);
                                    write_remote_record(&mut writers[bucket], RemoteRecord { column, parent: row })?;
                                    piece.raw_missing_occurrences += 1;
                                }
                            }
                            if piece.active_rows % 500_000 == 0 {
                                eprintln!(
                                    "remote worker={worker} degree={row_degree} rows={} missing={} elapsed={:.1}s",
                                    piece.active_rows,
                                    piece.raw_missing_occurrences,
                                    begun.elapsed().as_secs_f64()
                                );
                            }
                        }
                        begin = end;
                    }
                    eprintln!(
                        "remote worker={worker} finished_input_bucket={input_bucket} rows={} missing={} elapsed={:.1}s",
                        piece.active_rows,
                        piece.raw_missing_occurrences,
                        begun.elapsed().as_secs_f64()
                    );
                }
                for writer in &mut writers { writer.flush()?; }
                piece.elapsed = begun.elapsed().as_secs_f64();
                Ok((worker, piece))
            }));
        }
        for handle in handles {
            pieces.push(handle.join().unwrap_or_else(|_| fail("remote worker panic")));
        }
    });
    let mut ordered = Vec::new();
    for result in pieces { ordered.push(result?); }
    ordered.sort_by_key(|(worker, _)| *worker);
    let pieces: Vec<_> = ordered.into_iter().map(|(_, piece)| piece).collect();

    let mut remote = Vec::new();
    for bucket in 0..INCIDENCE_BUCKETS {
        let mut records = Vec::new();
        for worker in 0..pieces.len() {
            records.extend(read_remote_records(
                &temporary_dir.join(format!("remote-worker{worker:02}-bucket{bucket:02}.bin"))
            )?);
        }
        records.sort_unstable();
        let mut previous = None;
        for record in records {
            if previous == Some(record.column) { continue; }
            previous = Some(record.column);
            remote.push(record);
        }
        eprintln!("remote merge bucket={bucket} cumulative_distinct={}", remote.len());
    }
    remote.sort_by_key(|record| record.column);
    Ok((remote, pieces))
}

fn write_remote_results(
    result_path: &Path,
    ledger_path: &Path,
    row_degree: u8,
    remote: &[RemoteRecord],
    pieces: &[RemotePiece],
    elapsed: f64,
) -> io::Result<()> {
    let mut ledger = BufWriter::new(File::create(ledger_path)?);
    writeln!(ledger, "KRENN_NORMALIZED_ANCHOR_REMOTE_COLUMNS_V1")?;
    for (index, record) in remote.iter().enumerate() {
        write!(ledger, "REMOTE {index} ")?;
        for digit in decode_word(record.column.word) { write!(ledger, "{digit}")?; }
        let multiplier = hex(record.column.multiplier);
        let parent = hex(record.parent);
        writeln!(ledger, " {} {}", if multiplier.is_empty() { "-" } else { &multiplier }, if parent.is_empty() { "-" } else { &parent })?;
    }
    ledger.flush()?;
    let active_rows: usize = pieces.iter().map(|piece| piece.active_rows).sum();
    let raw_missing: usize = pieces.iter().map(|piece| piece.raw_missing_occurrences).sum();
    let mut global_histogram = BTreeMap::new();
    for piece in pieces {
        for (&degree, &count) in &piece.global_incidence_histogram {
            *global_histogram.entry(degree).or_insert(0usize) += count;
        }
    }
    let mut out = BufWriter::new(File::create(result_path)?);
    write!(out, "{{\n  \"status\":\"UNAUDITED exact recursive remote-column discovery from active normalized component\",\n  \"row_degree\":{row_degree},\n  \"active_output_rows\":{active_rows},\n  \"raw_missing_column_occurrences\":{raw_missing},\n  \"distinct_new_columns\":{},\n  \"global_row_incidence_histogram\":{{", remote.len())?;
    for (number, (degree, count)) in global_histogram.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "\"{degree}\":{count}")?;
    }
    write!(out, "}},\n  \"worker_seconds\":[")?;
    for (number, piece) in pieces.iter().enumerate() {
        if number != 0 { write!(out, ",")?; }
        write!(out, "{:.6}", piece.elapsed)?;
    }
    write!(out, "],\n  \"remote_ledger\":{:?},\n  \"scope\":\"This is one exact row-degree expansion layer. Component closure requires emitting full outputs of these new columns and repeating until no missing incident columns remain.\",\n  \"elapsed_seconds\":{elapsed:.6}\n}}\n", ledger_path.to_string_lossy())?;
    Ok(())
}

fn write_results(
    path: &Path,
    target: &BTreeMap<Mono, i64>,
    rows: &HashSet<Mono>,
    columns: &HashSet<Column>,
    layers: &[(usize, usize)],
    elapsed: f64,
) -> io::Result<()> {
    let mut degree_hist: BTreeMap<u8, usize> = BTreeMap::new();
    for row in rows {
        *degree_hist.entry(row.len).or_default() += 1
    }
    let mut out = File::create(path)?;
    write!(out,"{{\n  \"status\":\"UNAUDITED exact normalized-anchor target and closure census\",\n  \"target_row_orbits\":{},\n  \"target_total_mass\":{},\n  \"closure_rows\":{},\n  \"closure_columns\":{},\n  \"closure_layers\":[",target.len(),target.values().sum::<i64>(),rows.len(),columns.len())?;
    for (i, (r, c)) in layers.iter().enumerate() {
        if i != 0 {
            write!(out, ",")?
        }
        write!(out, "[{r},{c}]")?
    }
    write!(out, "],\n  \"closure_row_degree_histogram\":{{")?;
    for (i, (d, c)) in degree_hist.iter().enumerate() {
        if i != 0 {
            write!(out, ",")?
        }
        write!(out, "\"{d}\":{c}")?
    }
    write!(
        out,
        "}},\n  \"elapsed_seconds\":{elapsed:.6},\n  \"target\":["
    )?;
    for (i, (row, value)) in target.iter().enumerate() {
        if i != 0 {
            write!(out, ",")?
        }
        write!(out, "[\"{}\",{}]", hex(*row), value)?
    }
    write!(out, "]\n}}\n")?;
    Ok(())
}

fn main() {
    let args: Vec<_> = env::args().collect();
    if args.len() < 3 || args.len() > 10 {
        eprintln!("usage: normalized_anchor R8_SEED RESULTS.json [pairconstant|pairconstant-one|all-one|top12 [MATRIX.jsonl] | overlap-sample SUPPORT.txt N | prune-columns SUPPORT.txt COLUMNS.txt | prune-incidence COLUMNS.txt BUCKET_DIR TEMP_DIR | prune-private COLUMNS.txt SUPPORT.txt BUCKET_DIR ACTIVE.txt | prune-expand-degree COLUMNS.txt ACTIVE.txt BUCKET_DIR REMOTE.txt TEMP_DIR DEGREE]");
        std::process::exit(2)
    }
    let begun = Instant::now();
    let seed = parse_seed(Path::new(&args[1])).unwrap_or_else(|e| fail(e.to_string()));
    let stage = args.get(3).map(String::as_str);
    let pair_constant_only = matches!(stage, Some("pairconstant") | Some("pairconstant-one"));
    if stage.is_some()
        && !pair_constant_only
        && stage != Some("all-one")
        && stage != Some("overlap-sample")
        && stage != Some("prune-columns")
        && stage != Some("prune-incidence")
        && stage != Some("prune-private")
        && stage != Some("prune-expand-degree")
        && stage != Some("top12")
    {
        fail("unknown generator stage");
    }
    let one_layer = matches!(stage, Some("pairconstant-one") | Some("all-one"));
    if one_layer && args.len() != 5 {
        fail("one-layer stage requires a matrix output path");
    }
    if stage == Some("top12") && args.len() != 5 {
        fail("top12 requires a matrix output path");
    }
    let engine = Engine::new(&seed, pair_constant_only);
    let workers = std::thread::available_parallelism()
        .map_or(4, |v| v.get())
        .min(8);
    if stage == Some("overlap-sample") {
        if args.len() != 6 {
            fail("overlap-sample requires support and sample count");
        }
        let support = parse_support(Path::new(&args[4])).unwrap_or_else(|e| fail(e.to_string()));
        let count = args[5]
            .parse::<usize>()
            .unwrap_or_else(|_| fail("bad sample count"))
            .min(support.len());
        let sample: Vec<_> = (0..count)
            .map(|index| support[index * support.len() / count])
            .collect();
        let piece = sample_overlap(&engine, &sample, workers);
        let mut cache = HashMap::new();
        let mut outputs = HashSet::new();
        for &column in piece.columns.iter().take(128) {
            outputs.extend(
                engine
                    .outputs(column, &mut cache)
                    .into_iter()
                    .map(|(row, _)| row),
            );
        }
        write_sample(
            Path::new(&args[2]),
            support.len(),
            &sample,
            &piece,
            outputs.len(),
            begun.elapsed().as_secs_f64(),
        )
        .unwrap_or_else(|e| fail(e.to_string()));
        eprintln!(
            "PASS overlap sample={} incidence={} columns={} bounded_outputs={} elapsed={:.3}s",
            sample.len(),
            piece.incidence,
            piece.columns.len(),
            outputs.len(),
            begun.elapsed().as_secs_f64()
        );
        return;
    }
    if stage == Some("prune-columns") {
        if args.len() != 6 {
            fail("prune-columns requires support and column-ledger paths");
        }
        let support = parse_support(Path::new(&args[4]))
            .unwrap_or_else(|e| fail(e.to_string()));
        let piece = sample_overlap(&engine, &support, workers);
        write_prune_columns(
            Path::new(&args[2]),
            Path::new(&args[5]),
            support.len(),
            &piece,
            begun.elapsed().as_secs_f64(),
        )
        .unwrap_or_else(|e| fail(e.to_string()));
        eprintln!(
            "PASS prune-columns support={} incidence={} columns={} elapsed={:.3}s",
            support.len(),
            piece.incidence,
            piece.columns.len(),
            begun.elapsed().as_secs_f64()
        );
        return;
    }
    if stage == Some("prune-incidence") {
        if args.len() != 7 {
            fail("prune-incidence requires column-ledger, bucket-dir, and temp-dir paths");
        }
        let mut columns = parse_columns(Path::new(&args[4]))
            .unwrap_or_else(|e| fail(e.to_string()));
        if let Ok(raw_limit) = env::var("KRENN_PRUNE_COLUMN_LIMIT") {
            let limit = raw_limit.parse::<usize>().unwrap_or_else(|_| fail("bad KRENN_PRUNE_COLUMN_LIMIT"));
            columns.truncate(limit.min(columns.len()));
        }
        let (bucket_counts, pieces) = write_incidence_buckets(
            &engine,
            &columns,
            Path::new(&args[5]),
            Path::new(&args[6]),
            workers,
        )
        .unwrap_or_else(|e| fail(e.to_string()));
        write_incidence_results(
            Path::new(&args[2]),
            columns.len(),
            &bucket_counts,
            &pieces,
            Path::new(&args[5]),
            begun.elapsed().as_secs_f64(),
        )
        .unwrap_or_else(|e| fail(e.to_string()));
        eprintln!(
            "PASS prune-incidence columns={} records={} elapsed={:.3}s",
            columns.len(),
            bucket_counts.iter().sum::<usize>(),
            begun.elapsed().as_secs_f64()
        );
        return;
    }
    if stage == Some("prune-private") {
        if args.len() != 8 {
            fail("prune-private requires columns, support, bucket-dir, and active-ledger paths");
        }
        let columns = parse_columns(Path::new(&args[4]))
            .unwrap_or_else(|e| fail(e.to_string()));
        let target: HashSet<_> = parse_support(Path::new(&args[5]))
            .unwrap_or_else(|e| fail(e.to_string()))
            .into_iter()
            .collect();
        let (active, rounds, nonprivate) = private_zero_cascade(
            &engine,
            &columns,
            &target,
            Path::new(&args[6]),
        )
        .unwrap_or_else(|e| fail(e.to_string()));
        write_private_results(
            Path::new(&args[2]),
            Path::new(&args[7]),
            &columns,
            &active,
            &rounds,
            &nonprivate,
            begun.elapsed().as_secs_f64(),
        )
        .unwrap_or_else(|e| fail(e.to_string()));
        eprintln!(
            "PASS prune-private active={}/{} rounds={} elapsed={:.3}s",
            active.iter().filter(|&&value| value).count(),
            active.len(),
            rounds.len(),
            begun.elapsed().as_secs_f64()
        );
        return;
    }
    if stage == Some("prune-expand-degree") {
        if args.len() != 10 {
            fail("prune-expand-degree requires columns, active, bucket-dir, remote-ledger, temp-dir, degree");
        }
        let columns = parse_columns(Path::new(&args[4]))
            .unwrap_or_else(|e| fail(e.to_string()));
        let active = parse_active(Path::new(&args[5]), columns.len())
            .unwrap_or_else(|e| fail(e.to_string()));
        let row_degree = args[9].parse::<u8>().unwrap_or_else(|_| fail("bad row degree"));
        let (remote, pieces) = discover_remote_degree(
            &engine,
            &columns,
            &active,
            Path::new(&args[6]),
            Path::new(&args[8]),
            row_degree,
            workers,
        )
        .unwrap_or_else(|e| fail(e.to_string()));
        write_remote_results(
            Path::new(&args[2]),
            Path::new(&args[7]),
            row_degree,
            &remote,
            &pieces,
            begun.elapsed().as_secs_f64(),
        )
        .unwrap_or_else(|e| fail(e.to_string()));
        eprintln!(
            "PASS prune-expand-degree degree={} remote={} elapsed={:.3}s",
            row_degree,
            remote.len(),
            begun.elapsed().as_secs_f64()
        );
        return;
    }
    let target = build_target(&engine, workers);
    eprintln!(
        "target rows={} mass={}",
        target.len(),
        target.values().sum::<i64>()
    );
    if stage == Some("top12") {
        let (top_target, rows, columns, layers) = top12_closure(&engine, &target);
        write_top_matrix(Path::new(&args[4]), &engine, &top_target, &rows, &columns)
            .unwrap_or_else(|e| fail(e.to_string()));
        write_results(
            Path::new(&args[2]),
            &top_target,
            &rows,
            &columns,
            &layers,
            begun.elapsed().as_secs_f64(),
        )
        .unwrap_or_else(|e| fail(e.to_string()));
        eprintln!(
            "PASS top12 target={} rows={} cols={} elapsed={:.3}s",
            top_target.len(),
            rows.len(),
            columns.len(),
            begun.elapsed().as_secs_f64()
        );
        return;
    }
    let max_layers = if one_layer { Some(1) } else { None };
    let (rows, columns, layers) = closure(&engine, &target, max_layers);
    if one_layer {
        write_matrix(Path::new(&args[4]), &engine, &target, &rows, &columns)
            .unwrap_or_else(|e| fail(e.to_string()));
    }
    write_results(
        Path::new(&args[2]),
        &target,
        &rows,
        &columns,
        &layers,
        begun.elapsed().as_secs_f64(),
    )
    .unwrap_or_else(|e| fail(e.to_string()));
    eprintln!(
        "PASS target={} rows={} cols={} elapsed={:.3}s",
        target.len(),
        rows.len(),
        columns.len(),
        begun.elapsed().as_secs_f64()
    );
}
