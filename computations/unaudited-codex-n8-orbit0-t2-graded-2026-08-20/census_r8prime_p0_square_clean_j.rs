use std::collections::{BTreeMap, HashSet};
use std::env;
use std::fs::File;
use std::hash::{Hash, Hasher};
use std::io::{BufRead, BufReader};

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Row([u8; 16]);

#[derive(Clone, Copy, Eq, Ord, PartialEq, PartialOrd)]
struct Multiplier([u8; 12]);

impl Hash for Multiplier {
    fn hash<H: Hasher>(&self, state: &mut H) { self.0.hash(state); }
}

#[derive(Clone)]
struct Action {
    sites: [u8; 8],
    colours: [u8; 3],
    cells: [u8; 252],
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("clean-J-census: {}", message.as_ref());
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

fn cell_tables() -> ([u8; 252], [u8; 252], [u8; 252], [u8; 252], [[u8; 8]; 8]) {
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
    (cell_u, cell_v, cell_a, cell_b, edge_id)
}

fn actions() -> Vec<Action> {
    let (cell_u, cell_v, cell_a, cell_b, edge_id) = cell_tables();
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
                let mut cells = [0_u8; 252];
                for id in 0..252 {
                    let mut u = sites[cell_u[id] as usize];
                    let mut v = sites[cell_v[id] as usize];
                    let mut a = colours[cell_a[id] as usize];
                    let mut b = colours[cell_b[id] as usize];
                    if u > v {
                        std::mem::swap(&mut u, &mut v);
                        std::mem::swap(&mut a, &mut b);
                    }
                    cells[id] = cell_id(u, v, a, b);
                }
                answer.push(Action { sites, colours, cells });
            }
        }
    }
    if answer.len() != 768 { fail("action count is not 768"); }
    answer
}

fn word(mask: u8, site: u8) -> u8 {
    let choice = (mask >> (site / 2)) & 1;
    if site % 2 == 0 { 1 + choice } else { 2 - choice }
}

fn moved_word_mask(mask: u8, action: &Action) -> u8 {
    let mut moved = [0_u8; 8];
    for site in 0..8_u8 {
        moved[action.sites[site as usize] as usize] =
            action.colours[word(mask, site) as usize];
    }
    let mut result = 0_u8;
    for pair in 0..4_u8 {
        let even = moved[(2 * pair) as usize];
        let odd = moved[(2 * pair + 1) as usize];
        if !((even == 1 && odd == 2) || (even == 2 && odd == 1)) {
            fail("action did not preserve alternating words");
        }
        if even == 2 { result |= 1 << pair; }
    }
    result
}

fn perfect_matchings(edge_id: &[[u8; 8]; 8]) -> Vec<[u8; 4]> {
    fn recurse(remaining: u16, edge_id: &[[u8; 8]; 8], current: &mut Vec<u8>, out: &mut Vec<[u8; 4]>) {
        if remaining == 0 {
            let mut item = [0_u8; 4];
            item.copy_from_slice(current);
            item.sort_unstable();
            out.push(item);
            return;
        }
        let u = remaining.trailing_zeros() as u8;
        let without_u = remaining & !(1_u16 << u);
        for v in u + 1..8_u8 {
            if without_u & (1_u16 << v) == 0 { continue; }
            current.push(edge_id[u as usize][v as usize]);
            recurse(without_u & !(1_u16 << v), edge_id, current, out);
            current.pop();
        }
    }
    let mut answer = Vec::new();
    recurse(0xff, edge_id, &mut Vec::new(), &mut answer);
    answer.sort_unstable();
    answer.dedup();
    if answer.len() != 105 { fail("perfect matching count is not 105"); }
    answer
}

fn term_cells(mask: u8, matching: &[u8; 4], cell_u: &[u8; 252], cell_v: &[u8; 252]) -> [u8; 4] {
    let mut term = [0_u8; 4];
    for (index, edge) in matching.iter().enumerate() {
        let base = *edge as usize * 9;
        let u = cell_u[base];
        let v = cell_v[base];
        term[index] = *edge * 9 + 3 * word(mask, u) + word(mask, v);
    }
    term.sort_unstable();
    term
}

fn divides(row: Row, term: &[u8; 4]) -> bool {
    term.iter().all(|cell| row.0.binary_search(cell).is_ok())
}

fn quotient(row: Row, term: &[u8; 4]) -> Multiplier {
    let mut answer = [0_u8; 12];
    let mut used = [false; 16];
    for cell in term {
        let index = row.0.iter().enumerate().find(|(index, value)|
            !used[*index] && **value == *cell).map(|(index, _)| index)
            .unwrap_or_else(|| fail("term did not divide row"));
        used[index] = true;
    }
    let mut target = 0;
    for (index, cell) in row.0.iter().enumerate() {
        if !used[index] { answer[target] = *cell; target += 1; }
    }
    if target != 12 { fail("bad quotient degree"); }
    Multiplier(answer)
}

fn canonical_multiplier(multiplier: Multiplier, normalizers: &[usize], actions: &[Action]) -> Multiplier {
    let mut best = Multiplier([u8::MAX; 12]);
    for index in normalizers {
        let action = &actions[*index];
        let mut image = multiplier.0.map(|cell| action.cells[cell as usize]);
        image.sort_unstable();
        let item = Multiplier(image);
        if item < best { best = item; }
    }
    best
}

fn main() {
    let args: Vec<_> = env::args().collect();
    if args.len() != 2 { fail("usage: census_r8prime_p0_square_clean_j TARGET.jsonl"); }
    let actions = actions();
    let (cell_u, cell_v, _cell_a, _cell_b, edge_id) = cell_tables();
    let matchings = perfect_matchings(&edge_id);
    let mut normalizers = vec![Vec::<usize>::new(); 16];
    for mask in 0..16_u8 {
        for (index, action) in actions.iter().enumerate() {
            if moved_word_mask(mask, action) == 0 { normalizers[mask as usize].push(index); }
        }
        if normalizers[mask as usize].len() != 48 { fail("normalizer coset is not order 48"); }
    }
    let terms: Vec<Vec<[u8; 4]>> = (0..16_u8).map(|mask|
        matchings.iter().map(|matching| term_cells(mask, matching, &cell_u, &cell_v)).collect()
    ).collect();

    let reader = BufReader::new(File::open(&args[1]).unwrap_or_else(|e| fail(e.to_string())));
    let mut rows = 0_u64;
    let mut target_mass = 0_i128;
    let mut rows_with_incidence = 0_u64;
    let mut incidences = 0_u64;
    let mut incidence_histogram = BTreeMap::<u32, u64>::new();
    let mut column_orbits = HashSet::<Multiplier>::new();
    for line_result in reader.lines() {
        let line = line_result.unwrap_or_else(|e| fail(e.to_string()));
        let Some((row, coefficient)) = parse_record(&line) else { continue; };
        rows += 1;
        target_mass += coefficient as i128;
        let mut local = 0_u32;
        for mask in 0..16_u8 {
            for term in &terms[mask as usize] {
                if !divides(row, term) { continue; }
                local += 1;
                let q = quotient(row, term);
                column_orbits.insert(canonical_multiplier(q, &normalizers[mask as usize], &actions));
            }
        }
        if local > 0 { rows_with_incidence += 1; }
        incidences += local as u64;
        *incidence_histogram.entry(local).or_default() += 1;
        if rows % 100000 == 0 {
            eprintln!("rows={} incident={} incidences={} columns={}",
                      rows, rows_with_incidence, incidences, column_orbits.len());
        }
    }
    println!("PASS");
    println!("target_rows {}", rows);
    println!("target_mass {}", target_mass);
    println!("rows_with_incidence {}", rows_with_incidence);
    println!("incidences {}", incidences);
    println!("column_orbits {}", column_orbits.len());
    print!("incidence_histogram");
    for (degree, count) in incidence_histogram { print!(" {}:{}", degree, count); }
    println!();
}
