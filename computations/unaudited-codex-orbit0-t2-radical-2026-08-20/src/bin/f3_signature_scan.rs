//! Exact indexed compatibility scan for the 69,696 F3 diagonal signatures.
//! No external crates.  The bitset index answers the three subset/disjointness
//! conditions without a quadratic JSON-level comparison loop.

use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader, BufWriter, Write};
use std::path::Path;
use std::time::Instant;

#[derive(Clone, Copy)]
struct Signature {
    x: u32,
    c: u32,
    q: u16,
    count: u64,
    blocks: [u8; 6],
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("f3-signature-scan: {}", message.as_ref());
    std::process::exit(2)
}

fn integer(line: &str, key: &str) -> u64 {
    let pattern = format!("\"{key}\":");
    let start = line.find(&pattern).unwrap_or_else(|| fail(format!("missing {key}")))
        + pattern.len();
    let bytes = line.as_bytes();
    let mut end = start;
    while end < bytes.len() && bytes[end].is_ascii_digit() { end += 1; }
    line[start..end].parse().unwrap_or_else(|_| fail(format!("bad {key}")))
}

fn blocks(line: &str) -> [u8; 6] {
    let pattern = "\"representative_block_indices\":[";
    let start = line.find(pattern).unwrap_or_else(|| fail("missing representative"))
        + pattern.len();
    let end = start + line[start..].find(']').unwrap_or_else(|| fail("bad representative"));
    let values: Vec<_> = line[start..end]
        .split(',')
        .map(|raw| raw.trim().parse::<u8>().unwrap_or_else(|_| fail("bad block index")))
        .collect();
    if values.len() != 6 { fail("representative length"); }
    values.try_into().unwrap()
}

fn parse(path: &Path) -> io::Result<Vec<Signature>> {
    let mut signatures = Vec::new();
    for (line_number, line) in BufReader::new(File::open(path)?).lines().enumerate() {
        let line = line?;
        if line_number == 0 {
            if !line.contains("\"field\":3") || !line.contains("\"type\":\"header\"") {
                fail("bad signature header");
            }
            continue;
        }
        let index = integer(&line, "index") as usize;
        if index != signatures.len() { fail("nonsequential signature index"); }
        signatures.push(Signature {
            x: integer(&line, "x24") as u32,
            c: integer(&line, "cofactor24") as u32,
            q: integer(&line, "q16") as u16,
            count: integer(&line, "labelled_count"),
            blocks: blocks(&line),
        });
    }
    if signatures.len() != 69_696 { fail("signature count changed"); }
    Ok(signatures)
}

fn complement_q(mask: u16) -> u16 {
    mask.reverse_bits()
}

fn compatible(left: Signature, right: Signature) -> bool {
    (right.x & left.c) == 0
        && (left.x & right.c) == 0
        && (left.q & complement_q(right.q)) == 0
        && (right.q & complement_q(left.q)) == 0
}

fn support(signature: Signature) -> u64 {
    signature.x as u64 | ((signature.c as u64) << 24) | ((signature.q as u64) << 48)
}

fn forbidden(signature: Signature) -> u64 {
    signature.c as u64
        | ((signature.x as u64) << 24)
        | ((complement_q(signature.q) as u64) << 48)
}

#[derive(Default)]
struct Piece {
    unordered: u64,
    strict: u64,
    self_pairs: u64,
    weighted_ordered: u128,
    pairs: Vec<(u32, u32)>,
    overflow: bool,
    first: Option<(u32, u32)>,
}

fn main() -> io::Result<()> {
    let args: Vec<_> = env::args().collect();
    if args.len() != 3 {
        eprintln!("usage: f3_signature_scan SIGNATURES.jsonl RESULTS.json");
        std::process::exit(2);
    }
    let begun = Instant::now();
    let signatures = parse(Path::new(&args[1]))?;
    let n = signatures.len();
    let words = n.div_ceil(64);
    let mut bitsets = vec![vec![0u64; words]; 64];
    let mut q_subset_counts = vec![0u64; 1 << 16];
    for (index, &signature) in signatures.iter().enumerate() {
        q_subset_counts[signature.q as usize] += 1;
        let bits = support(signature);
        for bit in 0..64 {
            if bits & (1u64 << bit) != 0 {
                bitsets[bit][index / 64] |= 1u64 << (index % 64);
            }
        }
    }
    for bit in 0..16 {
        for mask in 0..(1usize << 16) {
            if mask & (1usize << bit) != 0 {
                q_subset_counts[mask] += q_subset_counts[mask ^ (1usize << bit)];
            }
        }
    }
    let q_compatible_ordered: u64 = signatures.iter().map(|signature| {
        let allowed = !complement_q(signature.q);
        q_subset_counts[allowed as usize]
    }).sum();
    let workers = std::thread::available_parallelism().map_or(4, |value| value.get()).min(8);
    let chunk = n.div_ceil(workers);
    const LOCAL_PAIR_CAP: usize = 4_000_000;
    let mut pieces = Vec::new();
    std::thread::scope(|scope| {
        let mut handles = Vec::new();
        for worker in 0..workers {
            let start = worker * chunk;
            let end = ((worker + 1) * chunk).min(n);
            if start >= end { continue; }
            let signatures = &signatures;
            let bitsets = &bitsets;
            handles.push(scope.spawn(move || {
                let mut piece = Piece::default();
                let mut candidate = vec![u64::MAX; words];
                for i in start..end {
                    candidate.fill(u64::MAX);
                    if n % 64 != 0 { candidate[words - 1] &= (1u64 << (n % 64)) - 1; }
                    let forbidden = forbidden(signatures[i]);
                    for bit in 0..64 {
                        if forbidden & (1u64 << bit) != 0 {
                            for word in 0..words {
                                candidate[word] &= !bitsets[bit][word];
                            }
                        }
                    }
                    for word_index in i / 64..words {
                        let mut bits = candidate[word_index];
                        if word_index == i / 64 { bits &= u64::MAX << (i % 64); }
                        while bits != 0 {
                            let bit = bits.trailing_zeros() as usize;
                            bits &= bits - 1;
                            let j = 64 * word_index + bit;
                            if j >= n { continue; }
                            if !compatible(signatures[i], signatures[j]) {
                                fail("bitset index admitted an incompatible pair");
                            }
                            piece.unordered += 1;
                            if i == j { piece.self_pairs += 1; } else { piece.strict += 1; }
                            let ordered_factor = if i == j { 1u128 } else { 2u128 };
                            piece.weighted_ordered += ordered_factor
                                * signatures[i].count as u128
                                * signatures[j].count as u128;
                            if piece.first.is_none() { piece.first = Some((i as u32, j as u32)); }
                            if piece.pairs.len() < LOCAL_PAIR_CAP {
                                piece.pairs.push((i as u32, j as u32));
                            } else {
                                piece.overflow = true;
                            }
                        }
                    }
                }
                eprintln!("worker={worker} range={start}..{end} unordered={} elapsed={:.3}s", piece.unordered, begun.elapsed().as_secs_f64());
                piece
            }));
        }
        for handle in handles {
            pieces.push(handle.join().unwrap_or_else(|_| fail("scan worker panic")));
        }
    });
    let unordered: u64 = pieces.iter().map(|piece| piece.unordered).sum();
    let strict: u64 = pieces.iter().map(|piece| piece.strict).sum();
    let self_pairs: u64 = pieces.iter().map(|piece| piece.self_pairs).sum();
    let ordered = 2 * strict + self_pairs;
    let weighted_ordered: u128 = pieces.iter().map(|piece| piece.weighted_ordered).sum();
    let overflow = pieces.iter().any(|piece| piece.overflow);
    let first = pieces.iter().filter_map(|piece| piece.first).min();
    let mut pairs = Vec::new();
    if !overflow {
        for piece in pieces { pairs.extend(piece.pairs); }
        pairs.sort_unstable();
        if pairs.len() as u64 != unordered { fail("stored pair count mismatch"); }
    }

    // If the graph is sparse enough to retain, detect/count compatible
    // triples with repetition by intersecting sorted closed neighborhoods.
    let mut triple_count = None;
    let mut first_triple = None;
    if !overflow {
        let mut neighbors = vec![Vec::<u32>::new(); n];
        for &(i, j) in &pairs {
            neighbors[i as usize].push(j);
            if i != j { neighbors[j as usize].push(i); }
        }
        for row in &mut neighbors { row.sort_unstable(); }
        let mut triples = 0u64;
        'pair_loop: for &(i, j) in &pairs {
            let left = &neighbors[i as usize];
            let right = &neighbors[j as usize];
            let (mut a, mut b) = (left.partition_point(|&k| k < j), right.partition_point(|&k| k < j));
            while a < left.len() && b < right.len() {
                if left[a] == right[b] {
                    triples += 1;
                    if first_triple.is_none() { first_triple = Some((i, j, left[a])); }
                    a += 1;
                    b += 1;
                } else if left[a] < right[b] { a += 1; } else { b += 1; }
            }
            if triples > 100_000_000 {
                triple_count = None;
                break 'pair_loop;
            }
        }
        if triple_count.is_none() && triples <= 100_000_000 { triple_count = Some(triples); }
    }

    let mut out = BufWriter::new(File::create(&args[2])?);
    writeln!(out, "{{")?;
    writeln!(out, "  \"status\":\"UNAUDITED exact indexed F3 diagonal signature compatibility scan\",")?;
    writeln!(out, "  \"signatures\":{n},")?;
    writeln!(out, "  \"q_compatible_ordered_candidates\":{q_compatible_ordered},")?;
    writeln!(out, "  \"compatible_unordered_signature_pairs\":{unordered},")?;
    writeln!(out, "  \"compatible_ordered_signature_pairs\":{ordered},")?;
    writeln!(out, "  \"compatible_self_signature_pairs\":{self_pairs},")?;
    writeln!(out, "  \"compatible_weighted_ordered_labelled_pairs\":\"{weighted_ordered}\",")?;
    writeln!(out, "  \"pair_list_retained\":{},", !overflow)?;
    if let Some((i, j)) = first {
        writeln!(out, "  \"first_pair\":{{\"indices\":[{i},{j}],\"left_blocks\":{:?},\"right_blocks\":{:?}}},", signatures[i as usize].blocks, signatures[j as usize].blocks)?;
    } else {
        writeln!(out, "  \"first_pair\":null,")?;
    }
    if let Some(count) = triple_count {
        writeln!(out, "  \"compatible_unordered_signature_triples_with_repetition\":{count},")?;
    } else {
        writeln!(out, "  \"compatible_unordered_signature_triples_with_repetition\":null,")?;
    }
    if let Some((i, j, k)) = first_triple {
        writeln!(out, "  \"first_triple\":{{\"indices\":[{i},{j},{k}],\"blocks\":[{:?},{:?},{:?}]}},", signatures[i as usize].blocks, signatures[j as usize].blocks, signatures[k as usize].blocks)?;
    } else {
        writeln!(out, "  \"first_triple\":null,")?;
    }
    writeln!(out, "  \"elapsed_seconds\":{:.6},", begun.elapsed().as_secs_f64())?;
    writeln!(out, "  \"scope\":\"Exact over F3 on the same-colour diagonal packet locus. A finite-field absence can refute that locus; existence does not lift to characteristic zero without an exact lift.\"")?;
    writeln!(out, "}}")?;
    out.flush()?;
    println!("F3 indexed compatibility scan: PASS");
    println!("unordered/ordered/self: {unordered}/{ordered}/{self_pairs}");
    println!("q-compatible ordered candidates: {q_compatible_ordered}");
    println!("first pair/triple: {:?}/{:?}", first, first_triple);
    println!("elapsed: {:.3}s", begun.elapsed().as_secs_f64());
    Ok(())
}
