use std::collections::HashMap;
use std::env;
use std::fs;
use std::io::{BufWriter, Write};

fn hex_bytes(text: &str) -> Vec<u8> {
    assert!(text.len() % 2 == 0);
    (0..text.len()).step_by(2)
        .map(|i| u8::from_str_radix(&text[i..i+2], 16).unwrap()).collect()
}

fn bytes_hex(values: &[u8]) -> String {
    const DIGIT: &[u8; 16] = b"0123456789abcdef";
    let mut answer = String::with_capacity(values.len() * 2);
    for &value in values {
        answer.push(DIGIT[(value >> 4) as usize] as char);
        answer.push(DIGIT[(value & 15) as usize] as char);
    }
    answer
}

fn partition_code(parts: &[u8]) -> u128 {
    let mut code = 0u128;
    for &part in parts { code = (code << 5) | part as u128; }
    code
}

fn union_partition_code(left: &[u8; 24], right: &[u8; 24]) -> u128 {
    // left o right is two copies of the half-cycle permutation on every
    // alternating component.  Convert its cycle counts back to edge lengths.
    let mut seen = [false; 24];
    let mut half_counts = [0u8; 25];
    for start in 0..24 {
        if seen[start] { continue; }
        let mut cursor = start;
        let mut length = 0usize;
        while !seen[cursor] {
            seen[cursor] = true;
            cursor = left[right[cursor] as usize] as usize;
            length += 1;
        }
        half_counts[length] += 1;
    }
    let mut code = 0u128;
    for half in 1..=12 {
        assert!(half_counts[half] % 2 == 0);
        for _ in 0..half_counts[half] / 2 {
            code = (code << 5) | (2 * half) as u128;
        }
    }
    code
}

fn matching(text: &str) -> [u8; 24] {
    let values = hex_bytes(text);
    assert_eq!(values.len(), 24);
    let mut answer = [0u8; 24];
    answer.copy_from_slice(&values);
    for i in 0..24 { assert_eq!(answer[answer[i] as usize] as usize, i); }
    answer
}

fn row12(text: &str) -> [u8; 12] {
    let values = hex_bytes(text);
    assert_eq!(values.len(), 12);
    let mut answer = [0u8; 12];
    answer.copy_from_slice(&values);
    answer
}

fn singleton_pivotable(left: &[u8; 12], right: &[u8; 12], anchor: &[i8; 256]) -> bool {
    let mut masks = [0u8; 4];
    for &cell in left.iter().chain(right.iter()) {
        let code = anchor[cell as usize];
        if code >= 0 {
            let pair = (code as usize) / 3;
            let colour = (code as usize) % 3;
            masks[pair] |= 1 << colour;
        }
    }
    if masks.iter().any(|&mask| mask == 0) { return false; }
    let union = masks.iter().fold(0u8, |value, &mask| value | mask);
    union.count_ones() >= 2
}

fn merged(left: &[u8; 12], right: &[u8; 12]) -> [u8; 24] {
    let mut answer = [0u8; 24];
    let (mut i, mut j, mut k) = (0usize, 0usize, 0usize);
    while i < 12 || j < 12 {
        if j == 12 || (i < 12 && left[i] <= right[j]) {
            answer[k] = left[i]; i += 1;
        } else {
            answer[k] = right[j]; j += 1;
        }
        k += 1;
    }
    answer
}

fn canonical_row(row: &[u8; 24], transforms: &Vec<[u8; 252]>) -> [u8; 24] {
    let mut best = [255u8; 24];
    for transform in transforms {
        let mut image = [0u8; 24];
        for i in 0..24 { image[i] = transform[row[i] as usize]; }
        image.sort_unstable();
        if image < best { best = image; }
    }
    best
}

fn row_partition_code(row: &[u8; 24], ports: &[[u8; 2]; 252]) -> u128 {
    let mut parent = [0u8; 24];
    let mut size = [1u8; 24];
    for i in 0..24 { parent[i] = i as u8; }
    fn root(parent: &mut [u8; 24], mut x: usize) -> usize {
        while parent[x] as usize != x {
            parent[x] = parent[parent[x] as usize];
            x = parent[x] as usize;
        }
        x
    }
    for &cell in row {
        let [x0, y0] = ports[cell as usize];
        let mut x = root(&mut parent, x0 as usize);
        let mut y = root(&mut parent, y0 as usize);
        if x != y {
            if size[x] < size[y] { std::mem::swap(&mut x, &mut y); }
            parent[y] = x as u8;
            size[x] += size[y];
        }
    }
    let mut parts = Vec::<u8>::new();
    for i in 0..24 {
        if root(&mut parent, i) == i { parts.push(size[i]); }
    }
    parts.sort_unstable();
    assert_eq!(parts.iter().map(|&x| x as usize).sum::<usize>(), 24);
    partition_code(&parts)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    assert_eq!(args.len(), 4);
    let dual_text = fs::read_to_string(&args[2]).unwrap();
    let mut dual = HashMap::<u128, i64>::new();
    for line in dual_text.lines().skip(1) {
        let fields: Vec<&str> = line.split('\t').collect();
        let parts: Vec<u8> = fields[0].split(',').map(|x| x.parse().unwrap()).collect();
        dual.insert(partition_code(&parts), fields[1].parse().unwrap());
    }
    assert_eq!(dual.len(), 77);

    let input = fs::read_to_string(&args[1]).unwrap();
    let headers: Vec<&str> = input.lines().take(3).collect();
    assert_eq!(headers[0], "KRENN_MISSING_K16_CYCLE_CHARGE_V1");
    let expected_reps: usize = headers[1].split_whitespace().nth(1).unwrap().parse().unwrap();
    let expected_packet: usize = headers[2].split_whitespace().nth(1).unwrap().parse().unwrap();
    let mut reps = Vec::<([u8; 12], [u8; 24], i64)>::new();
    let mut packet = Vec::<([u8; 12], [u8; 24], i64)>::new();
    let mut anchor = [-1i8; 256];
    let mut transforms = Vec::<[u8; 252]>::new();
    let mut ports = [[255u8; 2]; 252];
    for line in input.lines().skip(3) {
        let fields: Vec<&str> = line.split('\t').collect();
        match fields[0] {
            "A" => {
                let cell: usize = fields[1].parse().unwrap();
                let pair: i8 = fields[2].parse().unwrap();
                let colour: i8 = fields[3].parse().unwrap();
                anchor[cell] = 3 * pair + colour;
            },
            "H" => {
                let values = hex_bytes(fields[1]);
                assert_eq!(values.len(), 252);
                let mut transform = [0u8; 252];
                transform.copy_from_slice(&values);
                transforms.push(transform);
            },
            "C" => {
                let cell: usize = fields[1].parse().unwrap();
                ports[cell] = [fields[2].parse().unwrap(), fields[3].parse().unwrap()];
            },
            "R" => reps.push((row12(fields[1]), matching(fields[2]), fields[3].parse().unwrap())),
            "P" => packet.push((row12(fields[1]), matching(fields[2]), fields[3].parse().unwrap())),
            _ => panic!("bad input record"),
        }
    }
    assert_eq!(reps.len(), expected_reps);
    assert_eq!(packet.len(), expected_packet);
    assert_eq!(transforms.len(), 384);
    assert!(ports.iter().all(|pair| pair[0] < 24 && pair[1] < 24));
    let mut product_pairing = 0i128;
    let mut pivotable_pairing = 0i128;
    let mut irreducible_pairing = 0i128;
    let mut nonzero_pairs = 0u64;
    let mut pivotable_pairs = 0u64;
    let mut irreducible_pairs = 0u64;
    let mut irreducible_collected = HashMap::<[u8; 24], i128>::new();
    for (left_row, left, mass) in &reps {
        for (right_row, right, coefficient) in &packet {
            let value = *dual.get(&union_partition_code(left, right)).unwrap_or(&0);
            if value != 0 { nonzero_pairs += 1; }
            let contribution = *mass as i128 * *coefficient as i128 * value as i128;
            product_pairing += contribution;
            if singleton_pivotable(left_row, right_row, &anchor) {
                pivotable_pairs += 1;
                pivotable_pairing += contribution;
            } else {
                irreducible_pairs += 1;
                irreducible_pairing += contribution;
                let key = canonical_row(&merged(left_row, right_row), &transforms);
                *irreducible_collected.entry(key).or_insert(0) +=
                    *mass as i128 * *coefficient as i128;
            }
        }
    }
    assert_eq!(product_pairing, pivotable_pairing + irreducible_pairing);
    irreducible_collected.retain(|_, value| *value != 0);
    let mut collected_charge = 0i128;
    for (row, mass) in &irreducible_collected {
        let value = *dual.get(&row_partition_code(row, &ports)).unwrap_or(&0);
        collected_charge += *mass * value as i128;
    }
    assert_eq!(collected_charge, irreducible_pairing);
    let mut collected_rows: Vec<([u8; 24], i128)> = irreducible_collected
        .iter().map(|(row, mass)| (*row, -*mass)).collect();
    collected_rows.sort_unstable_by_key(|record| record.0);
    let mut writer = BufWriter::new(fs::File::create(&args[3]).unwrap());
    writeln!(writer, "row\tmissing_direct_orbit_mass").unwrap();
    for (row, mass) in &collected_rows {
        writeln!(writer, "{}\t{}", bytes_hex(row), mass).unwrap();
    }
    let component_pairing = -product_pairing;
    println!("{{\"component_sign\":-1,\"R8_packet_pairs\":{},\"pivotable_pairs\":{},\"irreducible_pairs\":{},\"irreducible_collected_H_orbits\":{},\"nonzero_dual_pairs\":{},\"unsigned_R8_packet_pairing\":{},\"unsigned_pivotable_pairing\":{},\"unsigned_irreducible_pairing\":{},\"missing_direct_component_pairing\":{},\"missing_direct_pivotable_pairing\":{},\"missing_direct_irreducible_pairing\":{},\"collected_missing_direct_irreducible_pairing\":{}}}",
             reps.len() as u64 * packet.len() as u64, pivotable_pairs, irreducible_pairs,
             irreducible_collected.len(), nonzero_pairs, product_pairing, pivotable_pairing,
             irreducible_pairing, component_pairing, -pivotable_pairing,
             -irreducible_pairing, -collected_charge);
}
