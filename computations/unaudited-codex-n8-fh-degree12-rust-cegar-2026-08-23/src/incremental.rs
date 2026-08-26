//! Persistent sparse modular elimination for the full-Fh D12 CEGAR.

use std::collections::BTreeMap;
use std::env;
use std::fs::{self, File};
use std::io::{self, BufRead, BufReader, BufWriter, Read, Write};
use std::path::Path;
use std::time::{Duration, Instant};

type Sparse = BTreeMap<usize, u64>;
const MAGIC: &[u8; 16] = b"FH_D12_BASIS_V1\0";
const BATCH_MAGIC: &[u8; 16] = b"FH_D12_BATCH_V1\0";

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("fh-d12-incremental: {}", message.as_ref());
    std::process::exit(2);
}

fn read_u32<R: Read>(input: &mut R) -> u32 {
    let mut bytes = [0_u8; 4];
    input.read_exact(&mut bytes).unwrap_or_else(|error| fail(error.to_string()));
    u32::from_le_bytes(bytes)
}

fn read_u64<R: Read>(input: &mut R) -> u64 {
    let mut bytes = [0_u8; 8];
    input.read_exact(&mut bytes).unwrap_or_else(|error| fail(error.to_string()));
    u64::from_le_bytes(bytes)
}

fn write_u32<W: Write>(output: &mut W, value: u32) {
    output.write_all(&value.to_le_bytes()).unwrap_or_else(|error| fail(error.to_string()));
}

fn write_u64<W: Write>(output: &mut W, value: u64) {
    output.write_all(&value.to_le_bytes()).unwrap_or_else(|error| fail(error.to_string()));
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

fn load_map(path: &Path, old_coordinates: usize, new_coordinates: usize) -> Vec<usize> {
    let mut input = BufReader::new(File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    let count = read_u64(&mut input) as usize;
    if count != old_coordinates { fail("row-map count differs from old basis coordinates"); }
    let mut answer = Vec::with_capacity(count);
    let mut previous = None;
    for _ in 0..count {
        let value = read_u32(&mut input) as usize;
        if value >= new_coordinates || previous.is_some_and(|old| value <= old) {
            fail("row map is not a strictly increasing embedding");
        }
        previous = Some(value);
        answer.push(value);
    }
    let mut trailing = [0_u8; 1];
    if input.read(&mut trailing).unwrap_or_else(|error| fail(error.to_string())) != 0 {
        fail("trailing row-map bytes");
    }
    answer
}

fn load_basis(path: &Path, expected_prime: u64, new_coordinates: usize,
              map_path: &Path) -> (Vec<Option<Sparse>>, usize, usize) {
    let mut input = BufReader::new(File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    let mut magic = [0_u8; 16];
    input.read_exact(&mut magic).unwrap_or_else(|error| fail(error.to_string()));
    if &magic != MAGIC { fail("bad basis-state magic"); }
    let prime = read_u64(&mut input);
    let old_coordinates = read_u64(&mut input) as usize;
    let old_rank = read_u64(&mut input) as usize;
    if prime != expected_prime { fail("basis-state prime changed"); }
    let map = load_map(map_path, old_coordinates, new_coordinates);
    let mut basis: Vec<Option<Sparse>> = vec![None; new_coordinates];
    for _ in 0..old_rank {
        let old_pivot = read_u32(&mut input) as usize;
        let terms = read_u32(&mut input) as usize;
        if old_pivot >= old_coordinates { fail("old pivot out of range"); }
        let pivot = map[old_pivot];
        let mut vector = Sparse::new();
        for _ in 0..terms {
            let old_index = read_u32(&mut input) as usize;
            let coefficient = read_u32(&mut input) as u64;
            if old_index >= old_coordinates || coefficient == 0 || coefficient >= prime {
                fail("invalid old basis term");
            }
            if vector.insert(map[old_index], coefficient).is_some() {
                fail("duplicate remapped basis term");
            }
        }
        if vector.first_key_value().map(|item| *item.0) != Some(pivot)
            || vector.get(&pivot) != Some(&1) || basis[pivot].replace(vector).is_some() {
            fail("remapped basis lost echelon form");
        }
    }
    let mut trailing = [0_u8; 1];
    if input.read(&mut trailing).unwrap_or_else(|error| fail(error.to_string())) != 0 {
        fail("trailing basis-state bytes");
    }
    (basis, old_rank, old_coordinates)
}

fn save_basis(path: &Path, prime: u64, basis: &[Option<Sparse>], rank: usize) {
    let mut output = BufWriter::new(File::create(path).unwrap_or_else(|error| fail(error.to_string())));
    output.write_all(MAGIC).unwrap();
    write_u64(&mut output, prime);
    write_u64(&mut output, basis.len() as u64);
    write_u64(&mut output, rank as u64);
    let mut written = 0_usize;
    for (pivot, record) in basis.iter().enumerate() {
        let Some(vector) = record else { continue; };
        write_u32(&mut output, pivot as u32);
        write_u32(&mut output, vector.len() as u32);
        for (&index, &coefficient) in vector {
            write_u32(&mut output, index as u32);
            write_u32(&mut output, coefficient as u32);
        }
        written += 1;
    }
    if written != rank { fail("saved basis rank mismatch"); }
    output.flush().unwrap_or_else(|error| fail(error.to_string()));
}

fn batch_path(directory: &Path, start: usize, end: usize) -> std::path::PathBuf {
    directory.join(format!("batch_{start:08}_{end:08}.bin"))
}

fn save_batch(directory: &Path, prime: u64, coordinates: usize, base_rank: usize,
              start: usize, end: usize, records: &[(usize, Sparse)]) {
    fs::create_dir_all(directory).unwrap_or_else(|error| fail(error.to_string()));
    let final_path = batch_path(directory, start, end);
    if final_path.exists() { fail("refusing to overwrite an existing batch checkpoint"); }
    let temporary = directory.join(format!(".batch_{start:08}_{end:08}.tmp"));
    let mut output = BufWriter::new(File::create(&temporary)
        .unwrap_or_else(|error| fail(error.to_string())));
    output.write_all(BATCH_MAGIC).unwrap();
    write_u64(&mut output, prime);
    write_u64(&mut output, coordinates as u64);
    write_u64(&mut output, base_rank as u64);
    write_u64(&mut output, start as u64);
    write_u64(&mut output, end as u64);
    write_u64(&mut output, records.len() as u64);
    for (pivot, vector) in records {
        write_u32(&mut output, *pivot as u32);
        write_u32(&mut output, vector.len() as u32);
        for (&index, &coefficient) in vector {
            write_u32(&mut output, index as u32);
            write_u32(&mut output, coefficient as u32);
        }
    }
    output.flush().unwrap_or_else(|error| fail(error.to_string()));
    output.get_ref().sync_all().unwrap_or_else(|error| fail(error.to_string()));
    drop(output);
    fs::rename(&temporary, &final_path).unwrap_or_else(|error| fail(error.to_string()));
    File::open(directory).and_then(|file| file.sync_all())
        .unwrap_or_else(|error| fail(error.to_string()));
}

fn load_batches(directory: &Path, prime: u64, coordinates: usize, base_rank: usize,
                basis: &mut [Option<Sparse>]) -> (usize, usize) {
    if !directory.exists() { return (0, 0); }
    let mut paths: Vec<_> = fs::read_dir(directory)
        .unwrap_or_else(|error| fail(error.to_string()))
        .map(|entry| entry.unwrap_or_else(|error| fail(error.to_string())).path())
        .filter(|path| path.file_name().and_then(|name| name.to_str())
            .is_some_and(|name| name.starts_with("batch_") && name.ends_with(".bin")))
        .collect();
    paths.sort();
    let mut processed = 0_usize;
    let mut added_rank = 0_usize;
    for path in paths {
        let mut input = BufReader::new(File::open(&path)
            .unwrap_or_else(|error| fail(error.to_string())));
        let mut magic = [0_u8; 16];
        input.read_exact(&mut magic).unwrap_or_else(|error| fail(error.to_string()));
        if &magic != BATCH_MAGIC { fail("bad batch-state magic"); }
        let found_prime = read_u64(&mut input);
        let found_coordinates = read_u64(&mut input) as usize;
        let found_base_rank = read_u64(&mut input) as usize;
        let start = read_u64(&mut input) as usize;
        let end = read_u64(&mut input) as usize;
        let record_count = read_u64(&mut input) as usize;
        if (found_prime, found_coordinates, found_base_rank)
            != (prime, coordinates, base_rank) || start != processed || end <= start {
            fail("batch checkpoint header differs from current round");
        }
        for _ in 0..record_count {
            let pivot = read_u32(&mut input) as usize;
            let terms = read_u32(&mut input) as usize;
            if pivot >= coordinates { fail("batch pivot out of range"); }
            let mut vector = Sparse::new();
            for _ in 0..terms {
                let index = read_u32(&mut input) as usize;
                let coefficient = read_u32(&mut input) as u64;
                if index >= coordinates || coefficient == 0 || coefficient >= prime
                    || vector.insert(index, coefficient).is_some() {
                    fail("invalid batch basis term");
                }
            }
            if vector.first_key_value().map(|item| *item.0) != Some(pivot)
                || vector.get(&pivot) != Some(&1) || basis[pivot].replace(vector).is_some() {
                fail("batch checkpoint lost echelon form");
            }
            added_rank += 1;
        }
        let mut trailing = [0_u8; 1];
        if input.read(&mut trailing).unwrap_or_else(|error| fail(error.to_string())) != 0 {
            fail("trailing batch-state bytes");
        }
        processed = end;
    }
    (processed, added_rank)
}

fn main() {
    let arguments: Vec<_> = env::args().collect();
    if arguments.len() != 5 {
        fail("usage: fh-d12-incremental STATE_IN_OR_DASH ROW_MAP_OR_DASH STATE_OUT BATCH_DIR");
    }
    let input = io::stdin();
    let mut lines = input.lock().lines();
    let header = lines.next().unwrap_or_else(|| fail("missing header"))
        .unwrap_or_else(|error| fail(error.to_string()));
    let fields: Vec<_> = header.split_whitespace().collect();
    if fields.len() != 5 || fields[0] != "KRENN_FH_D12_INCREMENTAL_V1" {
        fail("bad header");
    }
    let prime: u64 = fields[1].parse().unwrap_or_else(|_| fail("bad prime"));
    let coordinates: usize = fields[2].parse().unwrap_or_else(|_| fail("bad coordinate count"));
    let new_vectors: usize = fields[3].parse().unwrap_or_else(|_| fail("bad vector count"));
    let wall_seconds: u64 = fields[4].parse().unwrap_or_else(|_| fail("bad wall cap"));
    let deadline = Instant::now() + Duration::from_secs(wall_seconds);

    let (mut basis, mut rank, old_coordinates) = if arguments[1] == "-" {
        if arguments[2] != "-" { fail("initial state cannot have a row map"); }
        (vec![None; coordinates], 0_usize, 0_usize)
    } else {
        if arguments[2] == "-" { fail("resumed state requires a row map"); }
        load_basis(Path::new(&arguments[1]), prime, coordinates, Path::new(&arguments[2]))
    };
    let base_rank = rank;
    let (resume_vectors, resumed_rank) = load_batches(
        Path::new(&arguments[4]), prime, coordinates, base_rank, &mut basis);
    if resume_vectors > new_vectors { fail("batch checkpoint passes input vector count"); }
    rank += resumed_rank;
    eprintln!("INCREMENTAL_RESUME vectors={} base_rank={} rank={}",
              resume_vectors, base_rank, rank);

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
    let started = Instant::now();
    let mut batch_start = resume_vectors;
    let mut batch_records: Vec<(usize, Sparse)> = Vec::new();
    for vector_index in 0..new_vectors {
        if vector_index % 64 == 0 && Instant::now() >= deadline { fail("WALL_CAP"); }
        let line = lines.next().unwrap_or_else(|| fail("missing vector"))
            .unwrap_or_else(|error| fail(error.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.len() < 2 || fields[0] != "VECTOR" { fail("bad vector record"); }
        let terms: usize = fields[1].parse().unwrap_or_else(|_| fail("bad vector support"));
        if fields.len() != 2 + 2 * terms { fail("bad vector fields"); }
        if vector_index < resume_vectors { continue; }
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
                for coefficient in vector.values_mut() { *coefficient = *coefficient * inverse % prime; }
                batch_records.push((pivot, vector.clone()));
                basis[pivot] = Some(vector);
                rank += 1;
                break;
            }
        }
        if (vector_index + 1) % 256 == 0 || vector_index + 1 == new_vectors {
            save_batch(Path::new(&arguments[4]), prime, coordinates, base_rank,
                       batch_start, vector_index + 1, &batch_records);
            batch_records.clear();
            batch_start = vector_index + 1;
            eprintln!("INCREMENTAL new={}/{} old_rank={} rank={} elapsed={:.3}s",
                      vector_index + 1, new_vectors, base_rank, rank,
                      started.elapsed().as_secs_f64());
        }
    }
    if lines.next().is_some() { fail("trailing input"); }

    while let Some((&pivot, &value)) = target.first_key_value() {
        let Some(record) = &basis[pivot] else { break; };
        subtract_scaled(&mut target, record, value, prime);
    }
    save_basis(Path::new(&arguments[3]), prime, &basis, rank);
    if target.is_empty() {
        println!("KRENN_FH_D12_INCREMENTAL_RESULT_V1 {} {} 0 0 0 {} {}",
                 prime, rank, old_coordinates, coordinates);
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
        if dot(record, &dual, prime) != 0 { fail("dual misses basis vector"); }
    }
    if dot(&original_target, &dual, prime) != target_pairing { fail("wrong target pairing"); }
    println!("KRENN_FH_D12_INCREMENTAL_RESULT_V1 {} {} {} {} {} {} {}",
             prime, rank, target.len(), dual.len(), target_pairing,
             old_coordinates, coordinates);
    for (index, coefficient) in dual { println!("DUAL {} {}", index, coefficient); }
}
