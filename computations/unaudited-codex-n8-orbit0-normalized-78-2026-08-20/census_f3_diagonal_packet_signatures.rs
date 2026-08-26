// Exact F3 census of the diagonal pairconstant + 4+4 + 6+2 packet.
//
// No external crates.  Enumerates all six 2x2 blocks with permanent -1 and
// all four triangle contractions 2, filters pure H != 0, and deduplicates the
// support signature (X_nonanchor[24], cofactor[24], Q[16]).

use std::collections::HashMap;
use std::fs::File;
use std::io::{BufWriter, Write};
use std::time::Instant;

const EDGES: [(usize, usize); 6] = [
    (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
];
const TRIANGLES: [(usize, usize, usize); 4] = [
    (0, 1, 3), (0, 2, 4), (1, 2, 5), (3, 4, 5),
];

#[derive(Clone)]
struct SigRecord {
    count: u64,
    representative: [u8; 6],
}

fn permanent(m: &[u8; 4]) -> u8 {
    (m[0] * m[3] + m[1] * m[2]) % 3
}

fn triangle(a: &[u8; 4], b: &[u8; 4], c: &[u8; 4]) -> u8 {
    let mut total = 0u8;
    for x in 0..2 {
        for y in 0..2 {
            for z in 0..2 {
                total = (total
                    + a[2 * x + y] * b[2 * (1 - x) + z]
                        * c[2 * (1 - y) + (1 - z)]) % 3;
            }
        }
    }
    total
}

fn perfect_matchings(vertices: &[usize]) -> Vec<Vec<(usize, usize)>> {
    if vertices.is_empty() {
        return vec![Vec::new()];
    }
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
        .map(|matching| {
            matching.into_iter().filter_map(|(u, v)| {
                let (i, x) = (u / 2, u % 2);
                let (j, y) = (v / 2, v % 2);
                if i == j { None } else {
                    Some(4 * edge_index(i, j) + 2 * x + y)
                }
            }).collect()
        }).collect()
}

fn h_and_gradient(values: &[u8; 24], matchings: &[Vec<usize>]) -> (u8, u32) {
    let mut h = 0u8;
    let mut gradient = [0u8; 24];
    for variables in matchings {
        let mut zeros = 0usize;
        let mut zero_variable = 0usize;
        let mut product_nonzero = 1u8;
        for &variable in variables {
            let value = values[variable];
            if value == 0 {
                zeros += 1;
                zero_variable = variable;
            } else {
                product_nonzero = product_nonzero * value % 3;
            }
        }
        if zeros == 0 {
            h = (h + product_nonzero) % 3;
            for &variable in variables {
                // Every nonzero element of F3 is its own inverse.
                gradient[variable] = (gradient[variable]
                    + product_nonzero * values[variable]) % 3;
            }
        } else if zeros == 1 {
            gradient[zero_variable] = (gradient[zero_variable]
                + product_nonzero) % 3;
        }
    }
    let mut mask = 0u32;
    for (index, value) in gradient.iter().enumerate() {
        if *value != 0 { mask |= 1u32 << index; }
    }
    (h, mask)
}

fn q_mask(values: &[u8; 24]) -> u16 {
    let mut mask = 0u16;
    for index in 0..16usize {
        let bit = |site: usize| -> usize { (index >> (3 - site)) & 1 };
        let q = (
            values[4 * 0 + 2 * bit(0) + bit(1)]
                * values[4 * 5 + 2 * bit(2) + bit(3)]
            + values[4 * 1 + 2 * bit(0) + bit(2)]
                * values[4 * 4 + 2 * bit(1) + bit(3)]
            + values[4 * 2 + 2 * bit(0) + bit(3)]
                * values[4 * 3 + 2 * bit(1) + bit(2)]
        ) % 3;
        if q != 0 { mask |= 1u16 << index; }
    }
    mask
}

fn complement_q(mask: u16) -> u16 {
    let mut answer = 0u16;
    for index in 0..16usize {
        if mask & (1u16 << index) != 0 {
            answer |= 1u16 << (15 - index);
        }
    }
    answer
}

fn compatible(left: &(u32, u32, u16), right: &(u32, u32, u16)) -> bool {
    let (xl, cl, ql) = *left;
    let (xr, cr, qr) = *right;
    (xr & cl) == 0 && (xl & cr) == 0
        && (ql & complement_q(qr)) == 0
        && (qr & complement_q(ql)) == 0
}

fn main() {
    let started = Instant::now();
    let mut matrices = Vec::<[u8; 4]>::new();
    for code in 0..81usize {
        let mut value = code;
        let mut matrix = [0u8; 4];
        for entry in &mut matrix {
            *entry = (value % 3) as u8;
            value /= 3;
        }
        if permanent(&matrix) == 2 { matrices.push(matrix); }
    }
    assert_eq!(matrices.len(), 24);

    let mut allowed = vec![vec![Vec::<usize>::new(); 24]; 24];
    let mut triangle_count = 0usize;
    for a in 0..24 {
        for b in 0..24 {
            for c in 0..24 {
                if triangle(&matrices[a], &matrices[b], &matrices[c]) == 2 {
                    allowed[a][b].push(c);
                    triangle_count += 1;
                }
            }
        }
    }
    assert_eq!(triangle_count, 4200);
    let matchings = matching_variables();
    assert_eq!(matchings.len(), 105);

    let mut labelled = 0u64;
    let mut live_labelled = 0u64;
    let mut signatures: HashMap<(u32, u32, u16), SigRecord> = HashMap::new();
    let mut h_hist = [0u64; 3];
    for a in 0..24 {
        for b in 0..24 {
            for c in 0..24 {
                for &d in &allowed[a][b] {
                    for &e in &allowed[a][c] {
                        for &f in &allowed[b][c] {
                            if triangle(&matrices[d], &matrices[e], &matrices[f]) != 2 {
                                continue;
                            }
                            labelled += 1;
                            let chosen = [a as u8, b as u8, c as u8,
                                          d as u8, e as u8, f as u8];
                            let mut values = [0u8; 24];
                            for edge in 0..6 {
                                values[4 * edge..4 * edge + 4]
                                    .copy_from_slice(&matrices[chosen[edge] as usize]);
                            }
                            let (h, cofactors) = h_and_gradient(&values, &matchings);
                            h_hist[h as usize] += 1;
                            if h == 0 { continue; }
                            live_labelled += 1;
                            let mut xmask = 0u32;
                            for index in 0..24 {
                                if values[index] != 0 { xmask |= 1u32 << index; }
                            }
                            let signature = (xmask, cofactors, q_mask(&values));
                            signatures.entry(signature)
                                .and_modify(|record| record.count += 1)
                                .or_insert(SigRecord { count: 1,
                                                       representative: chosen });
                        }
                    }
                }
            }
        }
    }
    assert_eq!(labelled, 1_681_552);

    let mut ordered: Vec<((u32, u32, u16), SigRecord)> = signatures.into_iter().collect();
    ordered.sort_by_key(|row| row.0);

    let stream_path = "computations/unaudited-codex-n8-orbit0-normalized-78-2026-08-20/f3_diagonal_packet_signatures.jsonl";
    let stream_file = File::create(stream_path).unwrap();
    let mut stream = BufWriter::new(stream_file);
    write!(stream, "{{\"type\":\"header\",\"field\":3,\"edge_order\":[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],\"matrix_types\":[").unwrap();
    for (index, matrix) in matrices.iter().enumerate() {
        if index != 0 { write!(stream, ",").unwrap(); }
        write!(stream, "[{},{},{},{}]", matrix[0], matrix[1], matrix[2], matrix[3]).unwrap();
    }
    writeln!(stream, "]}}").unwrap();
    for (index, row) in ordered.iter().enumerate() {
        writeln!(stream,
                 "{{\"type\":\"signature\",\"index\":{},\"x24\":{},\"cofactor24\":{},\"q16\":{},\"labelled_count\":{},\"representative_block_indices\":{:?}}}",
                 index, (row.0).0, (row.0).1, (row.0).2,
                 row.1.count, row.1.representative).unwrap();
    }
    stream.flush().unwrap();
    let mut compatible_ordered = 0u64;
    let mut compatible_unordered = 0u64;
    let mut first_pair: Option<(usize, usize)> = None;
    if ordered.len() <= 50_000 {
        for i in 0..ordered.len() {
            for j in 0..ordered.len() {
                if compatible(&ordered[i].0, &ordered[j].0) {
                    compatible_ordered += 1;
                    if i <= j { compatible_unordered += 1; }
                    if first_pair.is_none() { first_pair = Some((i, j)); }
                }
            }
        }
    }

    let output_path = "computations/unaudited-codex-n8-orbit0-normalized-78-2026-08-20/results_f3_diagonal_packet_signatures.json";
    let file = File::create(output_path).unwrap();
    let mut out = BufWriter::new(file);
    writeln!(out, "{{").unwrap();
    writeln!(out, "  \"status\": \"UNAUDITED exact F3 diagonal packet signature census\",").unwrap();
    writeln!(out, "  \"permanent_minus_one_block_types\": {},", matrices.len()).unwrap();
    writeln!(out, "  \"valid_oriented_triangle_triples\": {},", triangle_count).unwrap();
    writeln!(out, "  \"labelled_one_colour_graphs\": {},", labelled).unwrap();
    writeln!(out, "  \"H_value_histogram\": [ {}, {}, {} ],", h_hist[0], h_hist[1], h_hist[2]).unwrap();
    writeln!(out, "  \"live_labelled_graphs\": {},", live_labelled).unwrap();
    writeln!(out, "  \"distinct_live_support_signatures\": {},", ordered.len()).unwrap();
    writeln!(out, "  \"pair_scan_performed\": {},", ordered.len() <= 50_000).unwrap();
    if ordered.len() <= 50_000 {
        writeln!(out, "  \"compatible_ordered_signature_pairs\": {},", compatible_ordered).unwrap();
        writeln!(out, "  \"compatible_unordered_signature_pairs\": {},", compatible_unordered).unwrap();
    } else {
        writeln!(out, "  \"compatible_ordered_signature_pairs\": null,").unwrap();
        writeln!(out, "  \"compatible_unordered_signature_pairs\": null,").unwrap();
    }
    if let Some((i, j)) = first_pair {
        let left = &ordered[i];
        let right = &ordered[j];
        writeln!(out, "  \"first_compatible_pair\": {{").unwrap();
        writeln!(out, "    \"left_signature\": [{},{},{}],", (left.0).0, (left.0).1, (left.0).2).unwrap();
        writeln!(out, "    \"right_signature\": [{},{},{}],", (right.0).0, (right.0).1, (right.0).2).unwrap();
        writeln!(out, "    \"left_block_indices\": {:?},", left.1.representative).unwrap();
        writeln!(out, "    \"right_block_indices\": {:?}", right.1.representative).unwrap();
        writeln!(out, "  }},").unwrap();
    } else {
        writeln!(out, "  \"first_compatible_pair\": null,").unwrap();
    }
    writeln!(out, "  \"elapsed_seconds\": {:.6},", started.elapsed().as_secs_f64()).unwrap();
    writeln!(out, "  \"scope\": \"Exact over F3 and only on the same-colour diagonal locus; support compatibility encodes the 01010101 and 00000101 cores.\"").unwrap();
    writeln!(out, "}}").unwrap();
    out.flush().unwrap();

    println!("F3 diagonal packet census: PASS");
    println!("labelled/live/signatures: {}/{}/{}", labelled, live_labelled, ordered.len());
    println!("H histogram: {:?}", h_hist);
    if ordered.len() <= 50_000 {
        println!("compatible ordered/unordered: {}/{}", compatible_ordered, compatible_unordered);
    } else {
        println!("compatible pair scan: SKIPPED (signature threshold)");
    }
    println!("elapsed seconds: {:.3}", started.elapsed().as_secs_f64());
}
