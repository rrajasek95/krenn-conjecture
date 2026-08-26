//! Deterministic bounded randomized falsifier for diagonal packet signatures
//! over F5/F7.  Discovery only: neither hits nor misses are characteristic-zero
//! certificates.

use std::collections::HashMap;
use std::env;
use std::fs::File;
use std::io::{self, BufWriter, Write};
use std::time::Instant;

const EDGES: [(usize, usize); 6] = [
    (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
];

#[derive(Clone, Copy)]
struct Sig {
    x: u32,
    c: u32,
    q: u16,
    blocks: [u16; 6],
    count: u64,
}

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        let mut x = self.0;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        self.0 = x;
        x
    }
}

fn permanent(matrix: &[u8; 4], prime: u8) -> u8 {
    (matrix[0] * matrix[3] + matrix[1] * matrix[2]) % prime
}

fn triangle(a: &[u8; 4], b: &[u8; 4], c: &[u8; 4], prime: u8) -> u8 {
    let mut total = 0u8;
    for x in 0..2 {
        for y in 0..2 {
            for z in 0..2 {
                total = (total + a[2 * x + y]
                    * b[2 * (1 - x) + z]
                    * c[2 * (1 - y) + (1 - z)]) % prime;
            }
        }
    }
    total
}

fn perfect_matchings(vertices: &[usize]) -> Vec<Vec<(usize, usize)>> {
    if vertices.is_empty() { return vec![Vec::new()]; }
    let first = vertices[0];
    let mut answer = Vec::new();
    for index in 1..vertices.len() {
        let second = vertices[index];
        let mut remainder = vertices[1..index].to_vec();
        remainder.extend_from_slice(&vertices[index + 1..]);
        for mut tail in perfect_matchings(&remainder) {
            let mut row = vec![(first, second)];
            row.append(&mut tail);
            answer.push(row);
        }
    }
    answer
}

fn edge_index(i: usize, j: usize) -> usize {
    EDGES.iter().position(|edge| *edge == (i, j)).unwrap()
}

fn matching_variables() -> Vec<Vec<usize>> {
    perfect_matchings(&(0usize..8).collect::<Vec<_>>())
        .into_iter()
        .map(|matching| matching.into_iter().filter_map(|(u, v)| {
            let (i, x) = (u / 2, u % 2);
            let (j, y) = (v / 2, v % 2);
            if i == j { None } else { Some(4 * edge_index(i, j) + 2 * x + y) }
        }).collect())
        .collect()
}

fn h_and_gradient(values: &[u8; 24], matchings: &[Vec<usize>], prime: u8) -> (u8, u32) {
    let mut h = 0u8;
    let mut gradient = [0u8; 24];
    for variables in matchings {
        let mut product = 1u8;
        for &variable in variables { product = product * values[variable] % prime; }
        h = (h + product) % prime;
        for (position, &variable) in variables.iter().enumerate() {
            let mut derivative = 1u8;
            for (other_position, &other) in variables.iter().enumerate() {
                if other_position != position { derivative = derivative * values[other] % prime; }
            }
            gradient[variable] = (gradient[variable] + derivative) % prime;
        }
    }
    let mut mask = 0u32;
    for (index, &value) in gradient.iter().enumerate() {
        if value != 0 { mask |= 1u32 << index; }
    }
    (h, mask)
}

fn q_mask(values: &[u8; 24], prime: u8) -> u16 {
    let mut mask = 0u16;
    for index in 0..16usize {
        let bit = |site: usize| (index >> (3 - site)) & 1;
        let q = (values[4 * 0 + 2 * bit(0) + bit(1)] * values[4 * 5 + 2 * bit(2) + bit(3)]
            + values[4 * 1 + 2 * bit(0) + bit(2)] * values[4 * 4 + 2 * bit(1) + bit(3)]
            + values[4 * 2 + 2 * bit(0) + bit(3)] * values[4 * 3 + 2 * bit(1) + bit(2)]) % prime;
        if q != 0 { mask |= 1u16 << index; }
    }
    mask
}

fn reverse_q(mask: u16) -> u16 { mask.reverse_bits() }

fn compatible(left: Sig, right: Sig) -> bool {
    right.x & left.c == 0 && left.x & right.c == 0
        && left.q & reverse_q(right.q) == 0
        && right.q & reverse_q(left.q) == 0
}

fn support(signature: Sig) -> u64 {
    signature.x as u64 | (signature.c as u64) << 24 | (signature.q as u64) << 48
}
fn forbidden(signature: Sig) -> u64 {
    signature.c as u64 | (signature.x as u64) << 24 | (reverse_q(signature.q) as u64) << 48
}

struct ResultRow {
    prime: u8,
    trials: u64,
    block_types: usize,
    packet_valid: u64,
    live: u64,
    distinct: usize,
    compatible_unordered: u64,
    first_pair: Option<(Sig, Sig)>,
    elapsed: f64,
}

fn scan(prime: u8, trials: u64, seed: u64, matchings: &[Vec<usize>]) -> ResultRow {
    let begun = Instant::now();
    let mut matrices = Vec::new();
    let total = (prime as usize).pow(4);
    for code in 0..total {
        let mut value = code;
        let mut matrix = [0u8; 4];
        for entry in &mut matrix { *entry = (value % prime as usize) as u8; value /= prime as usize; }
        if permanent(&matrix, prime) == prime - 1 { matrices.push(matrix); }
    }
    let mut rng = Rng(seed);
    let mut packet_valid = 0u64;
    let mut live = 0u64;
    let mut signatures: HashMap<(u32, u32, u16), Sig> = HashMap::new();
    for _ in 0..trials {
        let mut chosen = [0u16; 6];
        for block in &mut chosen { *block = (rng.next() % matrices.len() as u64) as u16; }
        let [a, b, c, d, e, f] = chosen.map(|index| &matrices[index as usize]);
        if triangle(a, b, d, prime) != 2 % prime
            || triangle(a, c, e, prime) != 2 % prime
            || triangle(b, c, f, prime) != 2 % prime
            || triangle(d, e, f, prime) != 2 % prime { continue; }
        packet_valid += 1;
        let mut values = [0u8; 24];
        for edge in 0..6 { values[4 * edge..4 * edge + 4].copy_from_slice(&matrices[chosen[edge] as usize]); }
        let (h, cofactor) = h_and_gradient(&values, matchings, prime);
        if h == 0 { continue; }
        live += 1;
        let mut x = 0u32;
        for (index, &value) in values.iter().enumerate() { if value != 0 { x |= 1u32 << index; } }
        let key = (x, cofactor, q_mask(&values, prime));
        signatures.entry(key).and_modify(|signature| signature.count += 1)
            .or_insert(Sig { x: key.0, c: key.1, q: key.2, blocks: chosen, count: 1 });
    }
    let sigs: Vec<_> = signatures.into_values().collect();
    let n = sigs.len();
    let words = n.div_ceil(64);
    let mut bitsets = vec![vec![0u64; words]; 64];
    for (index, &signature) in sigs.iter().enumerate() {
        let bits = support(signature);
        for bit in 0..64 { if bits & (1u64 << bit) != 0 { bitsets[bit][index / 64] |= 1u64 << (index % 64); } }
    }
    let mut candidate = vec![u64::MAX; words];
    let mut compatible_unordered = 0u64;
    let mut first_pair = None;
    for i in 0..n {
        candidate.fill(u64::MAX);
        if n % 64 != 0 { candidate[words - 1] &= (1u64 << (n % 64)) - 1; }
        let forbid = forbidden(sigs[i]);
        for bit in 0..64 { if forbid & (1u64 << bit) != 0 {
            for word in 0..words { candidate[word] &= !bitsets[bit][word]; }
        }}
        for word_index in i / 64..words {
            let mut bits = candidate[word_index];
            if word_index == i / 64 { bits &= u64::MAX << (i % 64); }
            while bits != 0 {
                let bit = bits.trailing_zeros() as usize;
                bits &= bits - 1;
                let j = 64 * word_index + bit;
                if j < n {
                    if !compatible(sigs[i], sigs[j]) { panic!("index false positive"); }
                    compatible_unordered += 1;
                    if first_pair.is_none() { first_pair = Some((sigs[i], sigs[j])); }
                }
            }
        }
    }
    ResultRow { prime, trials, block_types: matrices.len(), packet_valid, live,
        distinct: n, compatible_unordered, first_pair,
        elapsed: begun.elapsed().as_secs_f64() }
}

fn main() -> io::Result<()> {
    let args: Vec<_> = env::args().collect();
    if args.len() != 3 {
        eprintln!("usage: diagonal_packet_random TRIALS_PER_PRIME RESULTS.json");
        std::process::exit(2);
    }
    let trials = args[1].parse::<u64>().unwrap();
    let matchings = matching_variables();
    assert_eq!(matchings.len(), 105);
    let rows = [scan(5, trials, 0x5a17d1a6c35e9b21, &matchings),
                scan(7, trials, 0x7b29e3c8d461af05, &matchings)];
    let mut out = BufWriter::new(File::create(&args[2])?);
    writeln!(out, "{{\n  \"status\":\"UNAUDITED bounded deterministic randomized diagonal-packet falsifier\",\n  \"rows\":[")?;
    for (number, row) in rows.iter().enumerate() {
        if number != 0 { writeln!(out, ",")?; }
        write!(out, "    {{\"prime\":{},\"trials\":{},\"permanent_minus_one_block_types\":{},\"packet_valid_samples\":{},\"H_live_samples\":{},\"distinct_live_signatures\":{},\"compatible_unordered_signature_pairs\":{},", row.prime, row.trials, row.block_types, row.packet_valid, row.live, row.distinct, row.compatible_unordered)?;
        if let Some((left, right)) = row.first_pair {
            write!(out, "\"first_pair\":{{\"left_blocks\":{:?},\"right_blocks\":{:?},\"left_signature\":[{},{},{}],\"right_signature\":[{},{},{}]}},", left.blocks, right.blocks, left.x,left.c,left.q,right.x,right.c,right.q)?;
        } else { write!(out, "\"first_pair\":null,")?; }
        write!(out, "\"elapsed_seconds\":{:.6}}}", row.elapsed)?;
    }
    writeln!(out, "\n  ],\n  \"scope\":\"Discovery-only bounded samples over F5/F7. A compatible finite-field pair does not lift to characteristic zero; absence in a sample proves nothing.\"\n}}")?;
    out.flush()?;
    for row in &rows {
        println!("p{} trials/packet/live/sigs/pairs={}/{}/{}/{}/{} elapsed={:.3}s", row.prime,row.trials,row.packet_valid,row.live,row.distinct,row.compatible_unordered,row.elapsed);
    }
    Ok(())
}
