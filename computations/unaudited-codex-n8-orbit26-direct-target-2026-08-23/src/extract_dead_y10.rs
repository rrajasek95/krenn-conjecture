//! Extract the exact zero-PM4-incidence projection of frozen C10 buckets.

use std::collections::{HashMap, HashSet};
use std::env;
use std::fs::File;
use std::hash::{Hash, Hasher};
use std::io::{BufRead, BufReader, BufWriter, Read, Write};
use std::path::Path;

const BUCKETS: usize = 64;

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("extract-dead-y10: {}", message.as_ref());
    std::process::exit(2);
}

#[derive(Clone, Copy, Eq, Ord, PartialEq, PartialOrd)]
struct Key10([u8; 10]);
impl Hash for Key10 { fn hash<H: Hasher>(&self, state: &mut H) { self.0.hash(state); } }

fn decode_hex(text: &str) -> Vec<u8> {
    if text.len() % 2 != 0 { fail("odd hex"); }
    (0..text.len()/2).map(|i| u8::from_str_radix(&text[2*i..2*i+2], 16)
        .unwrap_or_else(|_| fail("bad hex"))).collect()
}

fn hex(bytes: &[u8]) -> String {
    let mut answer = String::with_capacity(2 * bytes.len());
    for value in bytes { answer.push_str(&format!("{value:02x}")); }
    answer
}

fn read_terms(path: &Path) -> HashSet<[u8; 2]> {
    let input = BufReader::new(File::open(path).unwrap_or_else(|e| fail(e.to_string())));
    let mut answer = HashSet::new();
    for line in input.lines() {
        let line = line.unwrap_or_else(|e| fail(e.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.first() != Some(&"BLOCK") { continue; }
        let terms = fields.iter().find(|x| x.starts_with("TERMS=")).unwrap();
        for text in terms[6..].split(',') {
            let term = decode_hex(text);
            if term.len() != 2 { fail("nonquadratic term"); }
            answer.insert([term[0], term[1]]);
        }
    }
    if answer.len() != 6618 { fail(format!("term census {}", answer.len())); }
    answer
}

fn incident(row: Key10, terms: &HashSet<[u8; 2]>) -> bool {
    for i in 0..10 { for j in i+1..10 {
        if terms.contains(&[row.0[i], row.0[j]]) { return true; }
    }}
    false
}

fn main() {
    let args: Vec<_> = env::args().collect();
    if args.len() != 4 { fail("usage: extract-dead-y10 BLOCKS SCRATCH OUTPUT"); }
    let terms = read_terms(Path::new(&args[1]));
    let scratch = Path::new(&args[2]);
    let mut dead = Vec::new();
    let mut support = 0_u64;
    for index in 0..BUCKETS {
        let path = scratch.join(format!("bucket-{index:03}.bin"));
        let mut reader = BufReader::with_capacity(1 << 20,
            File::open(path).unwrap_or_else(|e| fail(e.to_string())));
        let mut map: HashMap<Key10, i64> = HashMap::new();
        let mut record = [0_u8; 18];
        loop {
            match reader.read_exact(&mut record) {
                Ok(()) => {},
                Err(e) if e.kind() == std::io::ErrorKind::UnexpectedEof => break,
                Err(e) => fail(e.to_string()),
            }
            let mut key = [0_u8; 10]; key.copy_from_slice(&record[..10]);
            let mut coefficient = [0_u8; 8]; coefficient.copy_from_slice(&record[10..]);
            *map.entry(Key10(key)).or_insert(0) += i64::from_le_bytes(coefficient);
        }
        for (row, coefficient) in map {
            if coefficient == 0 { continue; }
            support += 1;
            if !incident(row, &terms) { dead.push((row, coefficient)); }
        }
        eprintln!("bucket {}/64 support={} dead={}", index + 1, support, dead.len());
    }
    dead.sort_unstable_by_key(|x| x.0);
    let mut output = BufWriter::new(File::create(&args[3]).unwrap_or_else(|e| fail(e.to_string())));
    writeln!(output, "KRENN_C10_DEAD_PROJECTION_V1 COUNT {}", dead.len()).unwrap();
    for (row, coefficient) in dead { writeln!(output, "ROW {} {}", hex(&row.0), coefficient).unwrap(); }
    output.flush().unwrap();
}
