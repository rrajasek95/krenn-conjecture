//! Sparse modular column-span separator for the normalized Fh D12 CEGAR.

use std::collections::BTreeMap;
use std::io::{self, BufRead};
use std::time::{Duration, Instant};

type Sparse = BTreeMap<usize, u64>;

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("fh-d12-moddual: {}", message.as_ref());
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

fn subtract_scaled(target: &mut Sparse, source: &Sparse, scalar: u64, prime: u64) {
    if scalar == 0 { return; }
    for (&index, &coefficient) in source {
        let old = target.get(&index).copied().unwrap_or(0);
        let decrement = scalar * coefficient % prime;
        let value = if old >= decrement { old - decrement } else { old + prime - decrement };
        if value == 0 { target.remove(&index); } else { target.insert(index, value); }
    }
}

fn dot(left: &Sparse, right: &Sparse, prime: u64) -> u64 {
    let (small, large) = if left.len() <= right.len() { (left, right) } else { (right, left) };
    small.iter().fold(0_u64, |sum, (&index, &value)| {
        (sum + value * large.get(&index).copied().unwrap_or(0)) % prime
    })
}

fn main() {
    let input = io::stdin();
    let mut lines = input.lock().lines();
    let header = lines.next().unwrap_or_else(|| fail("missing header"))
        .unwrap_or_else(|error| fail(error.to_string()));
    let fields: Vec<_> = header.split_whitespace().collect();
    if fields.len() != 5 || fields[0] != "KRENN_FH_D12_MODDUAL_V1" {
        fail("bad header");
    }
    let prime: u64 = fields[1].parse().unwrap_or_else(|_| fail("bad prime"));
    let coordinates: usize = fields[2].parse().unwrap_or_else(|_| fail("bad coordinate count"));
    let vectors: usize = fields[3].parse().unwrap_or_else(|_| fail("bad vector count"));
    let wall_seconds: u64 = fields[4].parse().unwrap_or_else(|_| fail("bad wall cap"));
    let deadline = Instant::now() + Duration::from_secs(wall_seconds);

    let target_line = lines.next().unwrap_or_else(|| fail("missing target"))
        .unwrap_or_else(|error| fail(error.to_string()));
    let target_fields: Vec<_> = target_line.split_whitespace().collect();
    if target_fields.len() < 2 || target_fields[0] != "TARGET" { fail("bad target"); }
    let target_terms: usize = target_fields[1].parse().unwrap_or_else(|_| fail("bad target support"));
    if target_fields.len() != 2 + 2 * target_terms { fail("bad target fields"); }
    let mut target = Sparse::new();
    for position in 0..target_terms {
        let index: usize = target_fields[2 + 2 * position].parse().unwrap_or_else(|_| fail("bad target index"));
        let value: u64 = target_fields[3 + 2 * position].parse().unwrap_or_else(|_| fail("bad target value"));
        if index >= coordinates || value == 0 || value >= prime || target.insert(index, value).is_some() {
            fail("invalid target term");
        }
    }
    let original_target = target.clone();

    let mut basis: Vec<Option<Sparse>> = vec![None; coordinates];
    let mut rank = 0_usize;
    let started = Instant::now();
    for vector_index in 0..vectors {
        if vector_index % 64 == 0 && Instant::now() >= deadline {
            fail("WALL_CAP");
        }
        let line = lines.next().unwrap_or_else(|| fail("missing vector"))
            .unwrap_or_else(|error| fail(error.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.len() < 2 || fields[0] != "VECTOR" { fail("bad vector record"); }
        let terms: usize = fields[1].parse().unwrap_or_else(|_| fail("bad vector support"));
        if fields.len() != 2 + 2 * terms { fail("bad vector fields"); }
        let mut vector = Sparse::new();
        for position in 0..terms {
            let index: usize = fields[2 + 2 * position].parse().unwrap_or_else(|_| fail("bad vector index"));
            let value: u64 = fields[3 + 2 * position].parse().unwrap_or_else(|_| fail("bad vector value"));
            if index >= coordinates || value == 0 || value >= prime || vector.insert(index, value).is_some() {
                fail("invalid vector term");
            }
        }
        while let Some((&pivot, &value)) = vector.first_key_value() {
            if let Some(record) = &basis[pivot] {
                subtract_scaled(&mut vector, record, value, prime);
            } else {
                let inverse = inverse_mod(value, prime);
                for coefficient in vector.values_mut() {
                    *coefficient = *coefficient * inverse % prime;
                }
                basis[pivot] = Some(vector);
                rank += 1;
                break;
            }
        }
        if (vector_index + 1) % 256 == 0 || vector_index + 1 == vectors {
            eprintln!("MODCHECK vectors={}/{} rank={} elapsed={:.3}s",
                      vector_index + 1, vectors, rank, started.elapsed().as_secs_f64());
        }
    }
    if lines.next().is_some() { fail("trailing input"); }

    while let Some((&pivot, &value)) = target.first_key_value() {
        let Some(record) = &basis[pivot] else { break; };
        subtract_scaled(&mut target, record, value, prime);
    }
    if target.is_empty() {
        println!("KRENN_FH_D12_MODDUAL_RESULT_V1 {} {} 0 0 0", prime, rank);
        return;
    }

    let selected = *target.first_key_value().unwrap().0;
    let target_pairing = target[&selected];
    let mut dual = Sparse::from([(selected, 1_u64)]);
    for pivot in (0..coordinates).rev() {
        let Some(record) = &basis[pivot] else { continue; };
        let mut value = 0_u64;
        for (&index, &coefficient) in record {
            if index != pivot {
                value = (value + coefficient * dual.get(&index).copied().unwrap_or(0)) % prime;
            }
        }
        if value != 0 { dual.insert(pivot, prime - value); }
    }
    for record in basis.iter().flatten() {
        if dot(record, &dual, prime) != 0 { fail("constructed dual misses a basis vector"); }
    }
    if dot(&original_target, &dual, prime) != target_pairing {
        fail("constructed dual has wrong target pairing");
    }
    println!("KRENN_FH_D12_MODDUAL_RESULT_V1 {} {} {} {} {}",
             prime, rank, target.len(), dual.len(), target_pairing);
    for (index, coefficient) in dual {
        println!("DUAL {} {}", index, coefficient);
    }
}
