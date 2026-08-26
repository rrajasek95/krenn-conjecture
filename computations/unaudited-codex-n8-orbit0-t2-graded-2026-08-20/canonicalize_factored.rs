use std::collections::{BTreeMap, HashMap, HashSet};
use std::env;
use std::fs::File;
use std::hash::Hash;
use std::io::{BufRead, BufReader, BufWriter, Write};

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Row([u8; 16]);

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("factored-canonicalizer: {}", message.as_ref());
    std::process::exit(2);
}

fn nibble(byte: u8) -> u8 {
    match byte {
        b'0'..=b'9' => byte - b'0',
        b'a'..=b'f' => byte - b'a' + 10,
        _ => fail("bad hex digit"),
    }
}

fn parse_row(text: &str) -> Row {
    if text.len() != 32 { fail("row hex is not 32 digits"); }
    let raw = text.as_bytes();
    let mut row = [0_u8; 16];
    for index in 0..16 {
        row[index] = 16 * nibble(raw[2 * index]) + nibble(raw[2 * index + 1]);
    }
    Row(row)
}

fn hex(row: Row) -> String {
    const DIGITS: &[u8; 16] = b"0123456789abcdef";
    let mut answer = Vec::with_capacity(32);
    for byte in row.0 {
        answer.push(DIGITS[(byte >> 4) as usize]);
        answer.push(DIGITS[(byte & 15) as usize]);
    }
    String::from_utf8(answer).unwrap()
}

fn parse_record(line: &str) -> Option<(Row, i64)> {
    if !line.contains("\"type\":\"row\"") { return None; }
    let row_marker = "\"row\":\"";
    let row_start = line.find(row_marker).unwrap_or_else(|| fail("row missing"))
        + row_marker.len();
    let row_end = row_start + 32;
    let coefficient_marker = "\"coefficient\":[";
    let coefficient_start = line.find(coefficient_marker)
        .unwrap_or_else(|| fail("coefficient missing")) + coefficient_marker.len();
    let coefficient_tail = &line[coefficient_start..];
    let comma = coefficient_tail.find(',').unwrap_or_else(|| fail("bad coefficient"));
    let close = coefficient_tail.find(']').unwrap_or_else(|| fail("bad coefficient"));
    let numerator: i64 = coefficient_tail[..comma].parse()
        .unwrap_or_else(|_| fail("bad numerator"));
    let denominator: i64 = coefficient_tail[comma + 1..close].parse()
        .unwrap_or_else(|_| fail("bad denominator"));
    if denominator != 1 { fail("nonintegral coefficient unsupported"); }
    Some((parse_row(&line[row_start..row_end]), numerator))
}

fn permutations4() -> Vec<[u8; 4]> {
    let mut answer = Vec::new();
    for a in 0..4_u8 { for b in 0..4_u8 { if b == a { continue; }
    for c in 0..4_u8 { if c == a || c == b { continue; }
    for d in 0..4_u8 { if d == a || d == b || d == c { continue; }
        answer.push([a, b, c, d]);
    }}}}
    answer
}

fn transforms() -> Vec<[u8; 252]> {
    let mut edge_id = [[0_u8; 8]; 8];
    let mut cell_u = [0_u8; 252];
    let mut cell_v = [0_u8; 252];
    let mut cell_a = [0_u8; 252];
    let mut cell_b = [0_u8; 252];
    let mut edge = 0_u8;
    for u in 0..8_u8 { for v in u + 1..8_u8 {
        edge_id[u as usize][v as usize] = edge;
        edge_id[v as usize][u as usize] = edge;
        for a in 0..3_u8 { for b in 0..3_u8 {
            let id = edge as usize * 9 + a as usize * 3 + b as usize;
            cell_u[id] = u; cell_v[id] = v; cell_a[id] = a; cell_b[id] = b;
        }}
        edge += 1;
    }}
    let cell_id = |u: u8, v: u8, a: u8, b: u8| -> u8 {
        (edge_id[u as usize][v as usize] as usize * 9
         + a as usize * 3 + b as usize) as u8
    };
    let colour_actions = [[0_u8, 1, 2], [0_u8, 2, 1]];
    let mut answer = Vec::new();
    for pair_permutation in permutations4() {
        for flip_mask in 0..16_u8 {
            let mut sites = [0_u8; 8];
            for pair in 0..4 {
                let flip = (flip_mask >> pair) & 1;
                sites[2 * pair] = 2 * pair_permutation[pair] + flip;
                sites[2 * pair + 1] = 2 * pair_permutation[pair] + 1 - flip;
            }
            for colours in colour_actions {
                let mut transform = [0_u8; 252];
                for id in 0..252 {
                    let mut u = sites[cell_u[id] as usize];
                    let mut v = sites[cell_v[id] as usize];
                    let mut a = colours[cell_a[id] as usize];
                    let mut b = colours[cell_b[id] as usize];
                    if u > v {
                        std::mem::swap(&mut u, &mut v);
                        std::mem::swap(&mut a, &mut b);
                    }
                    transform[id] = cell_id(u, v, a, b);
                }
                answer.push(transform);
            }
        }
    }
    if answer.len() != 768 { fail("transform count is not 768"); }
    answer
}

fn orbit(row: Row, transforms: &[[u8; 252]]) -> HashSet<Row> {
    let mut answer = HashSet::new();
    for transform in transforms {
        let mut image = row.0.map(|cell| transform[cell as usize]);
        image.sort_unstable();
        answer.insert(Row(image));
    }
    answer
}

fn main() {
    let args: Vec<_> = env::args().collect();
    if args.len() != 3 { fail("usage: canonicalize_factored INPUT.jsonl OUTPUT.jsonl"); }
    let mut input = HashMap::<Row, i64>::new();
    let mut input_records = 0_usize;
    let mut input_mass = 0_i128;
    let reader = BufReader::new(File::open(&args[1]).unwrap_or_else(|e| fail(e.to_string())));
    for line_result in reader.lines() {
        let line = line_result.unwrap_or_else(|e| fail(e.to_string()));
        if let Some((row, coefficient)) = parse_record(&line) {
            if input.insert(row, coefficient).is_some() { fail("duplicate raw input row"); }
            input_records += 1;
            input_mass += coefficient as i128;
        }
    }
    let transforms = transforms();
    let mut output = BTreeMap::<Row, i64>::new();
    let mut removed_records = 0_usize;
    let mut generated_orbits = 0_usize;
    while let Some(seed) = input.keys().next().copied() {
        let members = orbit(seed, &transforms);
        let representative = *members.iter().min().unwrap();
        let mut coefficient = 0_i128;
        for member in members {
            if let Some(value) = input.remove(&member) {
                coefficient += value as i128;
                removed_records += 1;
            }
        }
        if coefficient < i64::MIN as i128 || coefficient > i64::MAX as i128 {
            fail("coefficient overflow");
        }
        if coefficient != 0 {
            if output.insert(representative, coefficient as i64).is_some() {
                fail("canonical representative repeated");
            }
        }
        generated_orbits += 1;
    }
    if removed_records != input_records { fail("not every input record removed"); }
    let output_mass: i128 = output.values().map(|value| *value as i128).sum();
    if output_mass != input_mass { fail("canonical collection changed mass"); }
    let mut writer = BufWriter::new(File::create(&args[2]).unwrap_or_else(|e| fail(e.to_string())));
    writeln!(writer,
        "{{\"type\":\"header\",\"format\":\"krenn-r8prime-square-pure-anchor-factored-canonical-v1\",\"stabilizer_order\":768,\"input_records\":{},\"generated_orbits\":{},\"nonzero_orbits\":{},\"input_mass\":{},\"output_mass\":{}}}",
        input_records, generated_orbits, output.len(), input_mass, output_mass).unwrap();
    for (index, (row, coefficient)) in output.iter().enumerate() {
        writeln!(writer,
            "{{\"type\":\"row\",\"index\":{},\"row\":\"{}\",\"coefficient\":[{},1]}}",
            index, hex(*row), coefficient).unwrap();
    }
    writer.flush().unwrap();
    eprintln!("PASS input={} orbit_classes={} nonzero={} zeros={} mass={}",
        input_records, generated_orbits, output.len(), generated_orbits - output.len(), output_mass);
}
