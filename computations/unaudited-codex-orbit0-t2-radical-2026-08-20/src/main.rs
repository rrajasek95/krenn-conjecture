//! Exact orbit product generator for the orbit0 R8 square.
//!
//! The first implementation deliberately uses the literal 2304-action
//! canonicalization as a correctness baseline.  `--candidate-limit` provides
//! a bounded cost probe before attempting the full 48.7M relative products.

use std::collections::{BTreeMap, BTreeSet, HashMap, HashSet};
use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;
use std::time::Instant;

const GROUP_ORDER: i64 = 2304;

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Row12([u8; 12]);

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Row24([u8; 24]);

#[derive(Clone, Copy, Eq, Hash, PartialEq)]
struct Action {
    sites: [u8; 8],
    colours: [u8; 3],
}

#[derive(Clone)]
struct ResidualOrbit {
    representative: Row12,
    mass_units: i64,
    stated_size: usize,
    orbit: Vec<(Row12, u16)>,
    action_images: Vec<Row12>,
    stabilizer: Vec<u16>,
}

struct Seed {
    anchors: [bool; 252],
    coefficient_scale: i64,
    anchor_pair: [i8; 252],
    unary_reducible: [bool; 4096],
    transforms: Vec<[u8; 252]>,
    multiplication: Vec<Vec<u16>>,
    residual: Vec<ResidualOrbit>,
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("r8-square-target: {}", message.as_ref());
    std::process::exit(2);
}

fn hex_nibble(byte: u8) -> u8 {
    match byte {
        b'0'..=b'9' => byte - b'0',
        b'a'..=b'f' => byte - b'a' + 10,
        b'A'..=b'F' => byte - b'A' + 10,
        _ => fail("bad hex digit"),
    }
}

fn parse_hex<const N: usize>(text: &str) -> [u8; N] {
    if text.len() != 2 * N { fail(format!("expected {} hex digits", 2 * N)); }
    let bytes = text.as_bytes();
    let mut answer = [0_u8; N];
    for index in 0..N {
        answer[index] = 16 * hex_nibble(bytes[2 * index]) + hex_nibble(bytes[2 * index + 1]);
    }
    answer
}

fn write_hex<W: Write, const N: usize>(out: &mut W, bytes: &[u8; N]) -> io::Result<()> {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    for byte in bytes {
        out.write_all(&[HEX[(byte >> 4) as usize], HEX[(byte & 15) as usize]])?;
    }
    Ok(())
}

fn build_cell_tables() -> ([u8; 252], [u8; 252], [u8; 252], [u8; 252], [[u8; 8]; 8]) {
    let mut cell_u = [0; 252];
    let mut cell_v = [0; 252];
    let mut cell_a = [0; 252];
    let mut cell_b = [0; 252];
    let mut edge_id = [[0; 8]; 8];
    let mut edge = 0_u8;
    for u in 0..8_u8 {
        for v in u + 1..8_u8 {
            edge_id[u as usize][v as usize] = edge;
            edge_id[v as usize][u as usize] = edge;
            for a in 0..3_u8 {
                for b in 0..3_u8 {
                    let id = edge as usize * 9 + a as usize * 3 + b as usize;
                    cell_u[id] = u; cell_v[id] = v; cell_a[id] = a; cell_b[id] = b;
                }
            }
            edge += 1;
        }
    }
    (cell_u, cell_v, cell_a, cell_b, edge_id)
}

fn parse_seed(path: &Path) -> io::Result<Seed> {
    let (cell_u, cell_v, cell_a, cell_b, edge_id) = build_cell_tables();
    let cell_id = |u: u8, v: u8, a: u8, b: u8| -> u8 {
        (edge_id[u as usize][v as usize] as usize * 9 + a as usize * 3 + b as usize) as u8
    };
    let mut anchors = [false; 252];
    let mut actions = Vec::<Action>::new();
    let mut residual_raw = Vec::new();
    let mut coefficient_scale = None;
    for (line_number, line_result) in BufReader::new(File::open(path)?).lines().enumerate() {
        let line = line_result?;
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.is_empty() { continue; }
        match fields[0] {
            "KRENN_ORBIT0_R8_SEED_V1" => {
                if line_number != 0 { fail("seed magic is not first"); }
            }
            "ANCHORS" => for id in parse_hex::<12>(fields[1]) { anchors[id as usize] = true; },
            "SCALE" => {
                let scale = fields[1].parse::<i64>().unwrap_or_else(|_| fail("bad coefficient scale"));
                if scale <= 0 || coefficient_scale.replace(scale).is_some() {
                    fail("coefficient scale must occur once and be positive");
                }
            }
            "ACTION" => {
                if fields[1].len() != 8 || fields[2].len() != 3 { fail("bad action"); }
                let mut sites = [0; 8];
                let mut colours = [0; 3];
                for (index, byte) in fields[1].bytes().enumerate() { sites[index] = byte - b'0'; }
                for (index, byte) in fields[2].bytes().enumerate() { colours[index] = byte - b'0'; }
                actions.push(Action { sites, colours });
            }
            "R8" => residual_raw.push((
                Row12(parse_hex::<12>(fields[1])),
                fields[2].parse::<i64>().unwrap_or_else(|_| fail("bad mass")),
                fields[3].parse::<usize>().unwrap_or_else(|_| fail("bad orbit size")),
            )),
            _ => fail(format!("unknown seed record {}", fields[0])),
        }
    }
    if actions.len() != GROUP_ORDER as usize || residual_raw.is_empty() {
        fail("seed action count changed or residual is empty");
    }
    let mut anchor_edges: Vec<u8> = (0..252).filter(|&id| anchors[id])
        .map(|id| edge_id[cell_u[id] as usize][cell_v[id] as usize]).collect();
    anchor_edges.sort_unstable();
    anchor_edges.dedup();
    if anchor_edges.len() != 4 { fail("expected four physical anchor pairs"); }
    let mut anchor_pair = [-1_i8; 252];
    for id in 0..252 {
        if anchors[id] {
            let edge = edge_id[cell_u[id] as usize][cell_v[id] as usize];
            anchor_pair[id] = anchor_edges.iter().position(|&item| item == edge).unwrap() as i8;
        }
    }
    let mut unary_reducible = [false; 4096];
    for packed in 0..4096_usize {
        let masks = [
            (packed & 7) as u8,
            ((packed >> 3) & 7) as u8,
            ((packed >> 6) & 7) as u8,
            ((packed >> 9) & 7) as u8,
        ];
        for word in 0..81_usize {
            let mut cursor = word;
            let mut colours = [0_u8; 4];
            let mut supported = true;
            for pair in 0..4 {
                colours[pair] = (cursor % 3) as u8;
                cursor /= 3;
                supported &= masks[pair] & (1 << colours[pair]) != 0;
            }
            let mixed = colours.iter().any(|&colour| colour != colours[0]);
            if supported && mixed { unary_reducible[packed] = true; break; }
        }
    }
    let mut transforms = Vec::with_capacity(actions.len());
    for action in &actions {
        let mut transform = [0_u8; 252];
        for id in 0..252 {
            let (mut u, mut v) = (action.sites[cell_u[id] as usize], action.sites[cell_v[id] as usize]);
            let (mut a, mut b) = (action.colours[cell_a[id] as usize], action.colours[cell_b[id] as usize]);
            if u > v { std::mem::swap(&mut u, &mut v); std::mem::swap(&mut a, &mut b); }
            transform[id] = cell_id(u, v, a, b);
        }
        transforms.push(transform);
    }
    let action_index: HashMap<_, _> = actions.iter().enumerate()
        .map(|(index, &action)| (action, index as u16)).collect();
    let mut multiplication = vec![vec![0_u16; actions.len()]; actions.len()];
    for (left_index, left) in actions.iter().enumerate() {
        for (right_index, right) in actions.iter().enumerate() {
            let mut sites = [0; 8];
            let mut colours = [0; 3];
            for index in 0..8 { sites[index] = left.sites[right.sites[index] as usize]; }
            for index in 0..3 { colours[index] = left.colours[right.colours[index] as usize]; }
            multiplication[left_index][right_index] = *action_index.get(&Action { sites, colours })
                .unwrap_or_else(|| fail("actions are not closed under composition"));
        }
    }
    let mut residual = Vec::with_capacity(residual_raw.len());
    for (representative, mass_units, stated_size) in residual_raw {
        let mut orbit_map = BTreeMap::new();
        let mut action_images = Vec::with_capacity(transforms.len());
        let mut stabilizer = Vec::new();
        for (action, transform) in transforms.iter().enumerate() {
            let mut row = representative.0.map(|cell| transform[cell as usize]);
            row.sort_unstable();
            let image = Row12(row);
            if image == representative { stabilizer.push(action as u16); }
            orbit_map.entry(image).or_insert(action as u16);
            action_images.push(image);
        }
        if orbit_map.len() != stated_size || stabilizer.len() * stated_size != GROUP_ORDER as usize {
            fail("R8 orbit/stabilizer size does not replay");
        }
        residual.push(ResidualOrbit {
            representative, mass_units, stated_size,
            orbit: orbit_map.into_iter().collect(), action_images, stabilizer,
        });
    }
    Ok(Seed { anchors, coefficient_scale: coefficient_scale.unwrap_or_else(|| fail("missing SCALE")),
              anchor_pair, unary_reducible, transforms, multiplication, residual })
}

fn product(left: Row12, right: Row12) -> Row24 {
    let mut row = [0_u8; 24];
    row[..12].copy_from_slice(&left.0);
    row[12..].copy_from_slice(&right.0);
    row.sort_unstable();
    Row24(row)
}

fn unary_reducible(seed: &Seed, row: Row24) -> bool {
    let mut masks = [0_u8; 4];
    for &cell in &row.0 {
        let pair = seed.anchor_pair[cell as usize];
        if pair >= 0 {
            // Orbit-0 anchors are the three diagonal-colour cells on a pair.
            masks[pair as usize] |= 1 << (cell % 9) / 4;
        }
    }
    let packed = masks[0] as usize
        | ((masks[1] as usize) << 3)
        | ((masks[2] as usize) << 6)
        | ((masks[3] as usize) << 9);
    seed.unary_reducible[packed]
}

struct Canonicalizer<'a> {
    seed: &'a Seed,
    calls: usize,
    literal_controls: usize,
}

fn run_named_controls(seed: &Seed) {
    for &(left, right, expected) in &[(84_usize, 84_usize, 18_usize),
                                      (84, 12, 72), (0, 1, 1108)] {
        let mut canonicalizer = Canonicalizer { seed, calls: 0, literal_controls: 0 };
        let mut support = BTreeSet::new();
        for &(_row, action) in &seed.residual[right].orbit {
            support.insert(canonicalizer.canonical_pair(left, right, action));
        }
        if support.len() != expected {
            fail(format!("named product control ({left},{right}) gave {} orbits, expected {expected}",
                         support.len()));
        }
        eprintln!("control pair=({left},{right}) product_orbits={} literal_checks={}",
                  support.len(), canonicalizer.literal_controls);
    }
}

impl<'a> Canonicalizer<'a> {
    fn literal_canonical(&self, left: usize, right: usize, relative_action: u16) -> Row24 {
        let initial = product(
            self.seed.residual[left].representative,
            self.seed.residual[right].action_images[relative_action as usize],
        );
        let mut best = None;
        for transform in &self.seed.transforms {
            let mut row = initial.0.map(|cell| transform[cell as usize]);
            row.sort_unstable();
            let candidate = Row24(row);
            if best.map_or(true, |current| candidate < current) { best = Some(candidate); }
        }
        best.unwrap()
    }

    fn canonical_pair(&mut self, left: usize, right: usize, relative_action: u16) -> Row24 {
        self.calls += 1;
        let mut best = None;
        for action in 0..GROUP_ORDER as usize {
            let left_image = self.seed.residual[left].action_images[action];
            let right_action = self.seed.multiplication[action][relative_action as usize] as usize;
            let right_image = self.seed.residual[right].action_images[right_action];
            let candidate = product(left_image, right_image);
            if best.map_or(true, |current| candidate < current) { best = Some(candidate); }
        }
        let answer = best.unwrap();
        // A literal transform-and-sort replay guards the composition convention.
        // Keep this bounded: it is deliberately slower than the hot path.
        if self.literal_controls < 256 {
            let literal = self.literal_canonical(left, right, relative_action);
            if answer != literal { fail("precomputed pair canonicalizer disagrees with literal action replay"); }
            self.literal_controls += 1;
        }
        answer
    }
}

#[derive(Default)]
struct Accumulation {
    target: BTreeMap<Row24, i64>,
    relative_rows: usize,
    double_cosets: usize,
    survivor_rows: usize,
    survivor_blocks: usize,
    unary_rows: usize,
    unary_blocks: usize,
    colliding_blocks: usize,
    canonical_calls: usize,
    literal_controls: usize,
    complete: bool,
}

fn accumulate_range(seed: &Seed, start: usize, end: usize,
                    limit: Option<usize>) -> Accumulation {
    let mut canonicalizer = Canonicalizer {
        seed, calls: 0, literal_controls: 0,
    };
    let mut answer = Accumulation { complete: true, ..Accumulation::default() };
    let mut complete = true;
    'outer: for left_index in start..end {
        for right_index in left_index..seed.residual.len() {
            let left = &seed.residual[left_index];
            let right = &seed.residual[right_index];
            let (fixed_index, enumerated_index) = if left.stated_size <= right.stated_size {
                (left_index, right_index)
            } else { (right_index, left_index) };
            let fixed = &seed.residual[fixed_index];
            let enumerated = &seed.residual[enumerated_index];
            let symmetry = if left_index == right_index { 1_i64 } else { 2_i64 };
            let coefficient = symmetry * fixed.mass_units * enumerated.mass_units
                * (GROUP_ORDER / enumerated.stated_size as i64);
            let mut seen = HashSet::<Row12>::with_capacity(enumerated.stated_size);
            for &(image, relative_action) in &enumerated.orbit {
                if seen.contains(&image) { continue; }
                if limit.map_or(false, |bound| answer.double_cosets >= bound) {
                    complete = false;
                    break 'outer;
                }
                let mut block = HashSet::<Row12>::with_capacity(fixed.stabilizer.len());
                for &stabilizer_action in &fixed.stabilizer {
                    let action = seed.multiplication[stabilizer_action as usize][relative_action as usize];
                    block.insert(enumerated.action_images[action as usize]);
                }
                let block_size = block.len();
                for item in block { seen.insert(item); }
                if block_size == 0 { fail("empty stabilizer block"); }
                answer.relative_rows += block_size;
                answer.double_cosets += 1;
                let initial = product(fixed.representative,
                                      enumerated.action_images[relative_action as usize]);
                if unary_reducible(seed, initial) {
                    answer.unary_rows += block_size;
                    answer.unary_blocks += 1;
                } else {
                    answer.survivor_rows += block_size;
                    answer.survivor_blocks += 1;
                }
                let representative = canonicalizer.canonical_pair(
                    fixed_index, enumerated_index, relative_action,
                );
                let contribution = coefficient * block_size as i64;
                if answer.target.contains_key(&representative) { answer.colliding_blocks += 1; }
                *answer.target.entry(representative).or_default() += contribution;
            }
            if seen.len() != enumerated.stated_size { fail("stabilizer blocks do not partition enumerated orbit"); }
        }
    }
    answer.complete = complete;
    answer.canonical_calls = canonicalizer.calls;
    answer.literal_controls = canonicalizer.literal_controls;
    answer
}

fn generate(seed: &Seed, limit: Option<usize>, output: &Path) -> io::Result<()> {
    let started = Instant::now();
    let workers = if limit.is_some() { 1 } else {
        std::thread::available_parallelism().map_or(4, |value| value.get()).min(8)
    };
    let mut pieces = Vec::new();
    if workers == 1 {
        pieces.push(accumulate_range(seed, 0, seed.residual.len(), limit));
    } else {
        let chunk = seed.residual.len().div_ceil(workers);
        std::thread::scope(|scope| {
            let mut handles = Vec::new();
            for worker in 0..workers {
                let start = worker * chunk;
                let end = ((worker + 1) * chunk).min(seed.residual.len());
                if start < end {
                    handles.push((start, end, scope.spawn(move || {
                        let local_started = Instant::now();
                        let result = accumulate_range(seed, start, end, None);
                        eprintln!("worker={start}..{end} blocks={} target={} elapsed={:.3}s",
                                  result.double_cosets, result.target.len(),
                                  local_started.elapsed().as_secs_f64());
                        result
                    })));
                }
            }
            for (_start, _end, handle) in handles {
                pieces.push(handle.join().unwrap_or_else(|_| fail("target worker panicked")));
            }
        });
    }
    let mut combined = Accumulation { complete: true, ..Accumulation::default() };
    for piece in pieces {
        combined.relative_rows += piece.relative_rows;
        combined.double_cosets += piece.double_cosets;
        combined.survivor_rows += piece.survivor_rows;
        combined.survivor_blocks += piece.survivor_blocks;
        combined.unary_rows += piece.unary_rows;
        combined.unary_blocks += piece.unary_blocks;
        combined.colliding_blocks += piece.colliding_blocks;
        combined.canonical_calls += piece.canonical_calls;
        combined.literal_controls += piece.literal_controls;
        combined.complete &= piece.complete;
        for (row, coefficient) in piece.target {
            if combined.target.contains_key(&row) { combined.colliding_blocks += 1; }
            *combined.target.entry(row).or_default() += coefficient;
        }
    }
    let all_generated_target_orbits = combined.target.len();
    let zero_sum_target_orbits = combined.target.values().filter(|&&coefficient| coefficient == 0).count();
    combined.target.retain(|_row, coefficient| *coefficient != 0);
    let full_target = &combined.target;
    // Signed sparse R8' requires collecting coincident product monomials before
    // unary deletion.  Unary reducibility is row-orbit invariant, so this
    // partition is also an exact source reduction of the collected target.
    let mut target = BTreeMap::<Row24, i64>::new();
    let mut unary_target_orbits = 0_usize;
    let mut unary_target_l1 = 0_u128;
    for (&row, &coefficient) in full_target {
        if unary_reducible(seed, row) {
            unary_target_orbits += 1;
            unary_target_l1 += coefficient.unsigned_abs() as u128;
        } else {
            target.insert(row, coefficient);
        }
    }
    let mut out = File::create(output)?;
    writeln!(out, "{{")?;
    writeln!(out, "  \"status\":{:?},", if combined.complete { "complete exact target" } else { "bounded canonicalization cost probe" })?;
    writeln!(out, "  \"complete\":{},", combined.complete)?;
    writeln!(out, "  \"worker_count\":{workers},")?;
    writeln!(out, "  \"relative_product_rows\":{},", combined.relative_rows)?;
    writeln!(out, "  \"double_coset_blocks\":{},", combined.double_cosets)?;
    writeln!(out, "  \"unary_reduced_rows\":{},", combined.unary_rows)?;
    writeln!(out, "  \"unary_reduced_blocks\":{},", combined.unary_blocks)?;
    writeln!(out, "  \"survivor_rows\":{},", combined.survivor_rows)?;
    writeln!(out, "  \"survivor_blocks\":{},", combined.survivor_blocks)?;
    writeln!(out, "  \"colliding_blocks\":{},", combined.colliding_blocks)?;
    writeln!(out, "  \"all_generated_target_orbits_including_zero\":{all_generated_target_orbits},")?;
    writeln!(out, "  \"zero_sum_target_orbits\":{zero_sum_target_orbits},")?;
    writeln!(out, "  \"full_target_row_orbits_after_collection\":{},", full_target.len())?;
    writeln!(out, "  \"unary_target_row_orbits_after_collection\":{unary_target_orbits},")?;
    writeln!(out, "  \"unary_target_scaled_l1_after_collection\":{unary_target_l1},")?;
    writeln!(out, "  \"target_row_orbits\":{},", target.len())?;
    writeln!(out, "  \"canonical_calls\":{},", combined.canonical_calls)?;
    writeln!(out, "  \"literal_canonicalization_controls\":{},", combined.literal_controls)?;
    writeln!(out, "  \"elapsed_seconds\":{:.6},", started.elapsed().as_secs_f64())?;
    writeln!(out, "  \"target_scale\":\"{}^2/2304\",", seed.coefficient_scale)?;
    writeln!(out, "  \"target\":[")?;
    for (number, (row, coefficient)) in target.iter().enumerate() {
        if number != 0 { writeln!(out, ",")?; }
        write!(out, "    [\"")?; write_hex(&mut out, &row.0)?; write!(out, "\",{coefficient}]")?;
    }
    writeln!(out, "\n  ]\n}}")?;
    eprintln!("PASS complete={} rows={} blocks={} survivor_rows={} survivor_blocks={} literal_controls={} full_target={} unary_target={} target_orbits={} elapsed={:.3}s",
        combined.complete, combined.relative_rows, combined.double_cosets,
        combined.survivor_rows, combined.survivor_blocks, combined.literal_controls, full_target.len(), unary_target_orbits,
        target.len(), started.elapsed().as_secs_f64());
    Ok(())
}

fn main() {
    let args: Vec<_> = env::args().collect();
    if args.len() != 3 && args.len() != 5 {
        eprintln!("usage: r8-square-target SEED.txt OUTPUT.json [--candidate-limit N]");
        std::process::exit(2);
    }
    let limit = if args.len() == 5 {
        if args[3] != "--candidate-limit" { fail("unknown option"); }
        Some(args[4].parse().unwrap_or_else(|_| fail("bad candidate limit")))
    } else { None };
    let seed = parse_seed(Path::new(&args[1])).unwrap_or_else(|e| fail(e.to_string()));
    // Every R8 representative has exactly eight non-anchor factors.
    for residual in &seed.residual {
        let degree = residual.representative.0.iter()
            .filter(|cell| !seed.anchors[**cell as usize]).count();
        if degree != 8 { fail("R8 K-degree control failed"); }
    }
    if seed.residual.len() == 301 { run_named_controls(&seed); }
    generate(&seed, limit, Path::new(&args[2])).unwrap_or_else(|e| fail(e.to_string()));
}
