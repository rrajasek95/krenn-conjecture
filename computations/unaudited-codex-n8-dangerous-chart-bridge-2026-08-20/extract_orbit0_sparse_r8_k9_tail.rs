//! Expand the exact 9,607-column sparse cutoff-nine solution at K-degree 9.
//!
//! No external crates are used.  Input is the deterministic plain interface
//! written by `export_orbit0_sparse_r8_k9_tail_input.py`.

use std::collections::{BTreeMap, HashMap};
use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::sync::Arc;
use std::thread;
use std::time::Instant;

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Row([u8; 12]);

#[derive(Clone)]
struct Source {
    coefficient: i64,
    word: [u8; 8],
    multiplier: [u8; 8],
}

fn fail(message: &str) -> ! {
    eprintln!("k9-tail: {message}");
    std::process::exit(2);
}

fn nibble(value: u8) -> u8 {
    match value {
        b'0'..=b'9' => value - b'0',
        b'a'..=b'f' => value - b'a' + 10,
        _ => fail("bad hex digit"),
    }
}

fn parse_hex<const N: usize>(text: &str) -> [u8; N] {
    if text.len() != 2 * N { fail("wrong hex length"); }
    let raw = text.as_bytes();
    let mut answer = [0; N];
    for i in 0..N { answer[i] = 16 * nibble(raw[2 * i]) + nibble(raw[2 * i + 1]); }
    answer
}

fn write_hex<W: Write>(out: &mut W, row: &Row) {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    for value in row.0 {
        out.write_all(&[HEX[(value >> 4) as usize], HEX[(value & 15) as usize]]).unwrap();
    }
}

fn generate_matchings() -> Vec<[(u8, u8); 4]> {
    fn go(vertices: &[u8], pairs: &mut Vec<(u8, u8)>, out: &mut Vec<[(u8, u8); 4]>) {
        if vertices.is_empty() {
            out.push([pairs[0], pairs[1], pairs[2], pairs[3]]);
            return;
        }
        let u = vertices[0];
        for i in 1..vertices.len() {
            let mut rest = Vec::new();
            rest.extend_from_slice(&vertices[1..i]);
            rest.extend_from_slice(&vertices[i + 1..]);
            pairs.push((u, vertices[i]));
            go(&rest, pairs, out);
            pairs.pop();
        }
    }
    let mut answer = Vec::new();
    go(&[0, 1, 2, 3, 4, 5, 6, 7], &mut Vec::new(), &mut answer);
    if answer.len() != 105 { fail("matching census changed"); }
    answer
}

fn cell_tables() -> ([u8; 252], [u8; 252], [u8; 252], [u8; 252], [[u8; 8]; 8]) {
    let mut cu = [0; 252];
    let mut cv = [0; 252];
    let mut ca = [0; 252];
    let mut cb = [0; 252];
    let mut edge_id = [[0; 8]; 8];
    let mut edge = 0_u8;
    for u in 0..8_u8 {
        for v in u + 1..8_u8 {
            edge_id[u as usize][v as usize] = edge;
            edge_id[v as usize][u as usize] = edge;
            for a in 0..3_u8 {
                for b in 0..3_u8 {
                    let id = edge as usize * 9 + a as usize * 3 + b as usize;
                    cu[id] = u; cv[id] = v; ca[id] = a; cb[id] = b;
                }
            }
            edge += 1;
        }
    }
    (cu, cv, ca, cb, edge_id)
}

fn cell_id(edge_id: &[[u8; 8]; 8], u: u8, v: u8, a: u8, b: u8) -> u8 {
    (edge_id[u as usize][v as usize] as usize * 9
     + a as usize * 3 + b as usize) as u8
}

fn canonical(row: Row, transforms: &[[u8; 252]], cache: &mut HashMap<Row, Row>) -> Row {
    if let Some(answer) = cache.get(&row) { return *answer; }
    let mut best = row;
    for transform in transforms {
        let mut image = row.0.map(|cell| transform[cell as usize]);
        image.sort_unstable();
        let candidate = Row(image);
        if candidate < best { best = candidate; }
    }
    if cache.len() < 300_000 { cache.insert(row, best); }
    best
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 { fail("usage: extract_k9_tail INPUT OUTPUT"); }
    let started = Instant::now();
    let (cu, cv, ca, cb, edge_id) = cell_tables();
    let mut anchors = [false; 252];
    let mut action_specs = Vec::new();
    let mut target = BTreeMap::<Row, i128>::new();
    let mut sources = Vec::new();
    let input = BufReader::new(File::open(&args[1]).unwrap());
    for line_result in input.lines() {
        let line = line_result.unwrap();
        let f: Vec<_> = line.split_whitespace().collect();
        if f.is_empty() || f[0] == "KRENN_ORBIT0_SPARSE_R8_K9_TAIL_V1" { continue; }
        match f[0] {
            "ANCHORS" => for id in parse_hex::<12>(f[1]) { anchors[id as usize] = true; },
            "ACTION" => {
                let sites: Vec<_> = f[1].bytes().map(|x| x - b'0').collect();
                let colours: Vec<_> = f[2].bytes().map(|x| x - b'0').collect();
                action_specs.push((sites, colours));
            }
            "TARGET" => { target.insert(Row(parse_hex::<12>(f[1])), f[2].parse().unwrap()); }
            "SOURCE" => {
                let digits: Vec<_> = f[2].bytes().map(|x| x - b'0').collect();
                let mut word = [0; 8]; word.copy_from_slice(&digits);
                sources.push(Source { coefficient: f[1].parse().unwrap(), word,
                                      multiplier: parse_hex::<8>(f[3]) });
            }
            _ => fail("unknown record"),
        }
    }
    if action_specs.len() != 2304 || target.len() != 103 || sources.len() != 9607 {
        fail("interface census changed");
    }
    let mut transforms = Vec::new();
    for (sites, colours) in action_specs {
        let mut transform = [0; 252];
        for id in 0..252 {
            let (mut u, mut v) = (sites[cu[id] as usize], sites[cv[id] as usize]);
            let (mut a, mut b) = (colours[ca[id] as usize], colours[cb[id] as usize]);
            if u > v { std::mem::swap(&mut u, &mut v); std::mem::swap(&mut a, &mut b); }
            transform[id] = cell_id(&edge_id, u, v, a, b);
        }
        transforms.push(transform);
    }
    let transforms = Arc::new(transforms);
    let matchings = Arc::new(generate_matchings());
    let sources = Arc::new(sources);
    let edge_id = Arc::new(edge_id);
    let threads = thread::available_parallelism().map_or(4, |n| n.get().min(8));
    let mut partials = Vec::new();
    thread::scope(|scope| {
        let mut handles = Vec::new();
        for thread_id in 0..threads {
            let transforms = Arc::clone(&transforms);
            let matchings = Arc::clone(&matchings);
            let sources = Arc::clone(&sources);
            let edge_id = Arc::clone(&edge_id);
            let anchors = anchors;
            handles.push(scope.spawn(move || {
                let mut answer = HashMap::<Row, i128>::new();
                let mut cache = HashMap::<Row, Row>::new();
                let mut raw_outputs = 0_usize;
                for source_index in (thread_id..sources.len()).step_by(threads) {
                    let source = &sources[source_index];
                    let multiplier_k: u8 = source.multiplier.iter()
                        .map(|id| (!anchors[*id as usize]) as u8).sum();
                    for matching in matchings.iter() {
                        let mut row = [0; 12];
                        row[..8].copy_from_slice(&source.multiplier);
                        let mut k = multiplier_k;
                        for (position, &(u, v)) in matching.iter().enumerate() {
                            let id = cell_id(&edge_id, u, v,
                                             source.word[u as usize], source.word[v as usize]);
                            row[8 + position] = id;
                            k += (!anchors[id as usize]) as u8;
                        }
                        if k != 9 { continue; }
                        raw_outputs += 1;
                        row.sort_unstable();
                        let representative = canonical(Row(row), &transforms, &mut cache);
                        *answer.entry(representative).or_insert(0) += source.coefficient as i128;
                    }
                }
                (answer, raw_outputs, cache.len())
            }));
        }
        for handle in handles { partials.push(handle.join().unwrap()); }
    });
    let mut raw_outputs = 0;
    let mut cached = 0;
    for (partial, raw, cache) in partials {
        raw_outputs += raw;
        cached += cache;
        for (row, value) in partial { *target.entry(row).or_insert(0) -= value; }
    }
    target.retain(|_, value| *value != 0);
    let residual_mass: i128 = target.values().sum();
    let maximum = target.values().map(|x| x.abs()).max().unwrap_or(0);
    let mut out = BufWriter::new(File::create(&args[2]).unwrap());
    writeln!(out, "KRENN_ORBIT0_SPARSE_R8_K9_TAIL_RESULT_V1").unwrap();
    writeln!(out, "TARGET_ORBITS 103").unwrap();
    writeln!(out, "SOURCES 9607").unwrap();
    writeln!(out, "RAW_K9_SOURCE_OUTPUTS {raw_outputs}").unwrap();
    writeln!(out, "RESIDUAL_ORBITS {}", target.len()).unwrap();
    writeln!(out, "RESIDUAL_MASS {residual_mass}").unwrap();
    writeln!(out, "MAX_ABS_COEFFICIENT {maximum}").unwrap();
    for (row, coefficient) in &target {
        write!(out, "ROW ").unwrap(); write_hex(&mut out, row);
        writeln!(out, " {coefficient}").unwrap();
    }
    out.flush().unwrap();
    eprintln!("threads/raw/cache/residual: {threads}/{raw_outputs}/{cached}/{}", target.len());
    eprintln!("residual mass/max: {residual_mass}/{maximum}");
    eprintln!("elapsed: {:.3}s", started.elapsed().as_secs_f64());
}
