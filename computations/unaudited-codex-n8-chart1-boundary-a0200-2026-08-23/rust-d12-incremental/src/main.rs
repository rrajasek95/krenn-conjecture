//! Persistent sparse modular column basis for the chart-1 boundary D12 CEGAR.
//!
//! Rows have stable integer identifiers assigned by the Python source provider.
//! `ADD` retains every pivot, so later rounds pay only for genuinely new columns.

use std::collections::BTreeMap;
use std::io::{self, BufRead, Write};
use std::time::{Duration, Instant};

type Sparse = BTreeMap<usize, u64>;

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("chart1-boundary-d12-incremental: {}", message.as_ref());
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

fn parse_sparse(fields: &[&str], tag: &str, coordinates: usize, prime: u64) -> Sparse {
    if fields.len() < 2 || fields[0] != tag { fail(format!("bad {tag} record")); }
    let terms: usize = fields[1].parse().unwrap_or_else(|_| fail("bad support count"));
    if fields.len() != 2 + 2 * terms { fail(format!("bad {tag} field count")); }
    let mut result = Sparse::new();
    for position in 0..terms {
        let index: usize = fields[2 + 2 * position].parse()
            .unwrap_or_else(|_| fail("bad row identifier"));
        let value: u64 = fields[3 + 2 * position].parse()
            .unwrap_or_else(|_| fail("bad coefficient"));
        if index >= coordinates || value == 0 || value >= prime || result.insert(index, value).is_some() {
            fail(format!("invalid {tag} term"));
        }
    }
    result
}

fn main() {
    let input = io::stdin();
    let mut lines = input.lock().lines();
    let header = lines.next().unwrap_or_else(|| fail("missing header"))
        .unwrap_or_else(|error| fail(error.to_string()));
    let fields: Vec<_> = header.split_whitespace().collect();
    if fields.len() != 3 || fields[0] != "KRENN_BOUNDARY_D12_INCREMENTAL_V1" {
        fail("bad header");
    }
    let prime: u64 = fields[1].parse().unwrap_or_else(|_| fail("bad prime"));
    let wall_seconds: u64 = fields[2].parse().unwrap_or_else(|_| fail("bad wall cap"));
    let deadline = Instant::now() + Duration::from_secs(wall_seconds);
    let started = Instant::now();
    let mut coordinates = 0_usize;
    let mut target = Sparse::new();
    let mut basis: Vec<Option<Sparse>> = Vec::new();
    let mut rank = 0_usize;
    let mut total_vectors = 0_usize;
    let stdout = io::stdout();
    let mut output = stdout.lock();

    while let Some(line) = lines.next() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.is_empty() { continue; }
        if Instant::now() >= deadline { fail("WALL_CAP"); }
        match fields[0] {
            "INIT" => {
                if coordinates != 0 || fields.len() < 3 { fail("bad or repeated INIT"); }
                coordinates = fields[1].parse().unwrap_or_else(|_| fail("bad coordinate count"));
                let terms: usize = fields[2].parse().unwrap_or_else(|_| fail("bad target support"));
                if fields.len() != 3 + 2 * terms { fail("bad INIT target fields"); }
                target.clear();
                for position in 0..terms {
                    let index: usize = fields[3 + 2 * position].parse().unwrap_or_else(|_| fail("bad target index"));
                    let value: u64 = fields[4 + 2 * position].parse().unwrap_or_else(|_| fail("bad target value"));
                    if index >= coordinates || value == 0 || value >= prime || target.insert(index, value).is_some() {
                        fail("invalid INIT target term");
                    }
                }
                basis.resize_with(coordinates, || None);
                writeln!(output, "INITIALIZED {} {}", coordinates, target.len()).unwrap();
                output.flush().unwrap();
            }
            "EXTEND" => {
                if fields.len() != 2 { fail("bad EXTEND"); }
                let new_count: usize = fields[1].parse().unwrap_or_else(|_| fail("bad EXTEND count"));
                if new_count < coordinates { fail("EXTEND shrinks coordinates"); }
                coordinates = new_count;
                basis.resize_with(coordinates, || None);
                writeln!(output, "EXTENDED {}", coordinates).unwrap();
                output.flush().unwrap();
            }
            "ADD" => {
                if fields.len() != 2 { fail("bad ADD"); }
                let count: usize = fields[1].parse().unwrap_or_else(|_| fail("bad ADD count"));
                let rank_before = rank;
                let mut zero = 0_usize;
                for offset in 0..count {
                    if offset % 32 == 0 && Instant::now() >= deadline { fail("WALL_CAP"); }
                    let record = lines.next().unwrap_or_else(|| fail("missing VECTOR"))
                        .unwrap_or_else(|error| fail(error.to_string()));
                    let values: Vec<_> = record.split_whitespace().collect();
                    let mut vector = parse_sparse(&values, "VECTOR", coordinates, prime);
                    let mut added_pivot = false;
                    while let Some((&pivot, &value)) = vector.first_key_value() {
                        if let Some(existing) = &basis[pivot] {
                            subtract_scaled(&mut vector, existing, value, prime);
                        } else {
                            let inverse = inverse_mod(value, prime);
                            for coefficient in vector.values_mut() {
                                *coefficient = *coefficient * inverse % prime;
                            }
                            basis[pivot] = Some(std::mem::take(&mut vector));
                            rank += 1;
                            added_pivot = true;
                            break;
                        }
                    }
                    if !added_pivot { zero += 1; }
                    total_vectors += 1;
                    if (offset + 1) % 128 == 0 {
                        eprintln!("INCADD batch={}/{} total={} rank={} elapsed={:.3}s",
                                  offset + 1, count, total_vectors, rank, started.elapsed().as_secs_f64());
                    }
                }
                writeln!(output, "ADDED {} {} {} {}", count, rank, rank - rank_before, zero).unwrap();
                output.flush().unwrap();
            }
            "SOLVE" => {
                if fields.len() != 1 { fail("bad SOLVE"); }
                let mut remainder = target.clone();
                while let Some((&pivot, &value)) = remainder.first_key_value() {
                    let Some(existing) = &basis[pivot] else { break; };
                    subtract_scaled(&mut remainder, existing, value, prime);
                }
                if remainder.is_empty() {
                    writeln!(output, "RESULT MEMBER {} 0 0 0", rank).unwrap();
                    writeln!(output, "END").unwrap();
                    output.flush().unwrap();
                    continue;
                }
                let selected = *remainder.first_key_value().unwrap().0;
                let target_pairing = remainder[&selected];
                let mut dual = Sparse::from([(selected, 1_u64)]);
                for pivot in (0..coordinates).rev() {
                    let Some(existing) = &basis[pivot] else { continue; };
                    let mut value = 0_u64;
                    for (&index, &coefficient) in existing {
                        if index != pivot {
                            value = (value + coefficient * dual.get(&index).copied().unwrap_or(0)) % prime;
                        }
                    }
                    if value != 0 { dual.insert(pivot, prime - value); }
                }
                for existing in basis.iter().flatten() {
                    if dot(existing, &dual, prime) != 0 { fail("dual misses retained basis"); }
                }
                if dot(&target, &dual, prime) != target_pairing { fail("wrong target pairing"); }
                writeln!(output, "RESULT NONMEMBER {} {} {} {}", rank, remainder.len(), dual.len(), target_pairing).unwrap();
                for (index, coefficient) in dual {
                    writeln!(output, "DUAL {} {}", index, coefficient).unwrap();
                }
                writeln!(output, "END").unwrap();
                output.flush().unwrap();
            }
            "QUIT" => break,
            other => fail(format!("unknown command {other}")),
        }
    }
}
