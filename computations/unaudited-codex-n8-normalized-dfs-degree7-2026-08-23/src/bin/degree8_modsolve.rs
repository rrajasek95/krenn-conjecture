//! Sparse modular row solver for the chart-26 degree-eight lazy CEGAR.
//!
//! The Python provider emits invariant top-row vectors in its frozen sorted
//! order.  This binary performs exactly the same least-column-pivot
//! elimination over the requested prime and returns the corresponding sparse
//! functional on the original top rows.

use std::collections::BTreeMap;
use std::io::{self, BufRead};

#[derive(Clone)]
struct Basis {
    vector: BTreeMap<usize, u64>,
    combination: BTreeMap<usize, u64>,
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("degree8-modsolve: {}", message.as_ref());
    std::process::exit(2);
}

fn inverse_mod(mut base: u64, prime: u64) -> u64 {
    let mut exponent = prime - 2;
    let mut answer = 1_u64;
    while exponent != 0 {
        if exponent & 1 != 0 { answer = answer * base % prime; }
        base = base * base % prime;
        exponent >>= 1;
    }
    answer
}

fn subtract_scaled(target: &mut BTreeMap<usize, u64>, source: &BTreeMap<usize, u64>, scalar: u64, prime: u64) {
    if scalar == 0 { return; }
    for (&index, &coefficient) in source {
        let old = target.get(&index).copied().unwrap_or(0);
        let decrement = scalar * coefficient % prime;
        let value = if old >= decrement { old - decrement } else { old + prime - decrement };
        if value == 0 { target.remove(&index); } else { target.insert(index, value); }
    }
}

fn add_scaled(target: &mut BTreeMap<usize, u64>, source: &BTreeMap<usize, u64>, scalar: u64, prime: u64) {
    if scalar == 0 { return; }
    for (&index, &coefficient) in source {
        let value = (target.get(&index).copied().unwrap_or(0) + scalar * coefficient) % prime;
        if value == 0 { target.remove(&index); } else { target.insert(index, value); }
    }
}

fn normalize(vector: &mut BTreeMap<usize, u64>, scalar: u64, prime: u64) {
    for value in vector.values_mut() { *value = *value * scalar % prime; }
}

fn main() {
    let input = io::stdin();
    let mut lines = input.lock().lines();
    let header = lines.next().unwrap_or_else(|| fail("missing header")).unwrap_or_else(|error| fail(error.to_string()));
    let fields: Vec<_> = header.split_whitespace().collect();
    if fields.len() != 4 || fields[0] != "KRENN_D8_MODSOLVE_V1" { fail("bad header"); }
    let prime: u64 = fields[1].parse().unwrap_or_else(|_| fail("bad prime"));
    let columns: usize = fields[2].parse().unwrap_or_else(|_| fail("bad column count"));
    let rows: usize = fields[3].parse().unwrap_or_else(|_| fail("bad row count"));
    let target_line = lines.next().unwrap_or_else(|| fail("missing target")).unwrap_or_else(|error| fail(error.to_string()));
    let target_fields: Vec<_> = target_line.split_whitespace().collect();
    if target_fields.len() < 2 || target_fields[0] != "TARGET" { fail("bad target"); }
    let target_terms: usize = target_fields[1].parse().unwrap_or_else(|_| fail("bad target support"));
    if target_fields.len() != 2 + 2 * target_terms { fail("bad target field count"); }
    let mut target = BTreeMap::new();
    for position in 0..target_terms {
        let index: usize = target_fields[2 + 2 * position].parse().unwrap_or_else(|_| fail("bad target index"));
        let value: u64 = target_fields[3 + 2 * position].parse().unwrap_or_else(|_| fail("bad target value"));
        if index >= columns || value >= prime || value == 0 || target.insert(index, value).is_some() { fail("bad target term"); }
    }

    let mut basis: Vec<Option<Basis>> = vec![None; columns];
    let mut labels = Vec::with_capacity(rows);
    let mut rank = 0_usize;
    for row_index in 0..rows {
        let line = lines.next().unwrap_or_else(|| fail("missing row")).unwrap_or_else(|error| fail(error.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.len() < 3 || fields[0] != "ROW" { fail("bad row record"); }
        labels.push(fields[1].to_string());
        let terms: usize = fields[2].parse().unwrap_or_else(|_| fail("bad row support"));
        if fields.len() != 3 + 2 * terms { fail("bad row field count"); }
        if rank == columns { continue; }
        let mut vector = BTreeMap::new();
        for position in 0..terms {
            let index: usize = fields[3 + 2 * position].parse().unwrap_or_else(|_| fail("bad row index"));
            let value: u64 = fields[4 + 2 * position].parse().unwrap_or_else(|_| fail("bad row value"));
            if index >= columns || value >= prime || value == 0 || vector.insert(index, value).is_some() { fail("bad row term"); }
        }
        let mut combination = BTreeMap::from([(row_index, 1_u64)]);
        loop {
            let Some((&pivot, &value)) = vector.first_key_value() else { break; };
            if let Some(record) = &basis[pivot] {
                subtract_scaled(&mut vector, &record.vector, value, prime);
                subtract_scaled(&mut combination, &record.combination, value, prime);
            } else {
                let inverse = inverse_mod(value, prime);
                normalize(&mut vector, inverse, prime);
                normalize(&mut combination, inverse, prime);
                basis[pivot] = Some(Basis { vector, combination });
                rank += 1;
                break;
            }
        }
    }
    if lines.next().is_some() { fail("trailing input rows"); }

    let mut solution = BTreeMap::new();
    while let Some((&pivot, &value)) = target.first_key_value() {
        let Some(record) = &basis[pivot] else { break; };
        subtract_scaled(&mut target, &record.vector, value, prime);
        add_scaled(&mut solution, &record.combination, value, prime);
    }
    println!("KRENN_D8_MODSOLUTION_V1 {} {} {} {}", prime, rank, target.len(), solution.len());
    for (row, coefficient) in solution {
        println!("SOLUTION {} {}", labels[row], coefficient);
    }
}
