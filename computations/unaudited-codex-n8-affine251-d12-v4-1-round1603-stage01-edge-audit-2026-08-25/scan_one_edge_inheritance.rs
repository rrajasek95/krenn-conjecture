use std::convert::TryInto;
use std::env;
use std::fs::File;
use std::io::{BufReader, BufWriter, Read, Seek, SeekFrom, Write};
use std::path::{Path, PathBuf};
use std::time::Instant;

const PRIME: u64 = 1_073_741_827;
const CP_MAGIC: &[u8; 12] = b"AFF12CEG1\0\0\0";
const VEC_MAGIC: &[u8; 12] = b"AFF12VEC1\0\0\0";
const TARGET: [u8; 12] = [251; 12];

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("REJECT: {}", message.as_ref());
    std::process::exit(2);
}
fn bytes<R: Read>(input: &mut R, size: usize, what: &str) -> Vec<u8> {
    let mut value = vec![0; size];
    input.read_exact(&mut value).unwrap_or_else(|_| fail(format!("truncated {what}")));
    value
}
fn u64le<R: Read>(input: &mut R, what: &str) -> u64 {
    u64::from_le_bytes(bytes(input, 8, what).try_into().unwrap())
}
fn canonical(value: &[u8]) -> bool { value.windows(2).all(|pair| pair[0] <= pair[1]) }

#[derive(Clone, Copy, Eq, Ord, PartialEq, PartialOrd)]
struct Column { word: u16, mono: [u8; 8] }

struct Checkpoint { round: u64, support: u64, columns: Vec<Column> }
fn checkpoint(path: &Path) -> Checkpoint {
    let mut input = BufReader::with_capacity(1 << 20, File::open(path).unwrap());
    if bytes(&mut input, 12, "checkpoint magic").as_slice() != CP_MAGIC { fail("checkpoint magic"); }
    if u64le(&mut input, "checkpoint prime") != PRIME { fail("checkpoint prime"); }
    let round = u64le(&mut input, "checkpoint round");
    let count = u64le(&mut input, "checkpoint count") as usize;
    let support = u64le(&mut input, "checkpoint support");
    let mut columns = Vec::with_capacity(count);
    for _ in 0..count {
        let word = u16::from_le_bytes(bytes(&mut input, 2, "column word").try_into().unwrap());
        let raw = bytes(&mut input, 13, "column mono");
        if word >= 6561 || raw[0] != 8 || !canonical(&raw[1..9]) || raw[9..] != [0; 4] { fail("column encoding"); }
        let column = Column { word, mono: raw[1..9].try_into().unwrap() };
        if columns.last().is_some_and(|old| old >= &column) { fail("checkpoint column order"); }
        columns.push(column);
    }
    let mut previous: Option<[u8; 12]> = None;
    let mut target = None;
    for _ in 0..support {
        let raw = bytes(&mut input, 13, "candidate mono");
        let coefficient = u64le(&mut input, "candidate coefficient");
        let row: [u8; 12] = raw[1..].try_into().unwrap();
        if raw[0] != 12 || !canonical(&row) || previous.is_some_and(|old| old >= row)
            || coefficient == 0 || coefficient >= PRIME { fail("candidate encoding"); }
        if row == TARGET { target = Some(coefficient); }
        previous = Some(row);
    }
    let mut trailing = [0; 1];
    if input.read(&mut trailing).unwrap() != 0 || target != Some(1) { fail("checkpoint tail/target"); }
    Checkpoint { round, support, columns }
}
fn descendant(parent: &[Column], child: &[Column]) -> bool {
    let (mut p, mut c) = (0, 0);
    while p < parent.len() {
        if c == child.len() { return false; }
        if child[c] < parent[p] { c += 1; }
        else if child[c] == parent[p] { p += 1; c += 1; }
        else { return false; }
    }
    true
}

struct Vectors {
    input: BufReader<File>, columns: Vec<Column>, index: usize, provider: u64,
    fingerprint: u64, head: Option<(Column, usize)>, records: usize,
}
impl Vectors {
    fn open(path: &Path, columns: Vec<Column>) -> Self {
        let mut input = BufReader::with_capacity(1 << 20, File::open(path).unwrap());
        if bytes(&mut input, 12, "cache magic").as_slice() != VEC_MAGIC
            || u64le(&mut input, "cache prime") != PRIME { fail("cache header"); }
        let provider = u64le(&mut input, "provider fingerprint");
        let fingerprint = u64le(&mut input, "cache fingerprint");
        let records = u64le(&mut input, "cache count") as usize;
        if records != columns.len() { fail("cache/checkpoint count"); }
        let mut answer = Self { input, columns, index: 0, provider, fingerprint, head: None, records };
        answer.advance(); answer
    }
    fn advance(&mut self) {
        if self.index == self.records { self.head = None; return; }
        let word = u16::from_le_bytes(bytes(&mut self.input, 2, "vector word").try_into().unwrap());
        let raw = bytes(&mut self.input, 13, "vector mono");
        let count = u64le(&mut self.input, "vector size") as usize;
        if raw[0] != 8 || !canonical(&raw[1..9]) || raw[9..] != [0; 4] || count == 0 || count > 700_000 { fail("vector header"); }
        let column = Column { word, mono: raw[1..9].try_into().unwrap() };
        if column != self.columns[self.index] { fail("vector/checkpoint order"); }
        self.head = Some((column, count));
    }
    fn skip_payload(&mut self, count: usize) {
        self.input.seek(SeekFrom::Current((count * 21) as i64)).unwrap_or_else(|_| fail("skip payload"));
        self.index += 1; self.advance();
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 6 { fail("usage: scan OUTPUT PARENT_CP PARENT_VEC CHILD_CP CHILD_VEC"); }
    let output = PathBuf::from(&args[1]); let started = Instant::now();
    let mut parent_cp = checkpoint(Path::new(&args[2]));
    let mut child_cp = checkpoint(Path::new(&args[4]));
    if !descendant(&parent_cp.columns, &child_cp.columns) { fail("checkpoint descendant"); }
    let parent_columns = parent_cp.columns.len(); let child_columns = child_cp.columns.len();
    let mut parent = Vectors::open(Path::new(&args[3]), std::mem::take(&mut parent_cp.columns));
    let mut child = Vectors::open(Path::new(&args[5]), std::mem::take(&mut child_cp.columns));
    if parent.provider != child.provider { fail("provider fingerprint drift"); }
    let mut inherited = 0usize; let mut new_records = 0usize; let mut compared_bytes = 0u64;
    let mut left = vec![0u8; 21 * 65_536]; let mut right = vec![0u8; 21 * 65_536];
    while let Some((pkey, pcount)) = parent.head {
        let Some((ckey, ccount)) = child.head else { fail("child exhausted"); };
        if ckey < pkey { child.skip_payload(ccount); new_records += 1; continue; }
        if ckey > pkey || ccount != pcount { fail("inherited record missing/size drift"); }
        let mut remaining = pcount;
        while remaining != 0 {
            let rows = remaining.min(65_536); let size = rows * 21;
            parent.input.read_exact(&mut left[..size]).unwrap_or_else(|_| fail("parent payload"));
            child.input.read_exact(&mut right[..size]).unwrap_or_else(|_| fail("child payload"));
            if left[..size] != right[..size] { fail("inherited payload changed"); }
            compared_bytes += size as u64; remaining -= rows;
        }
        inherited += 1; parent.index += 1; child.index += 1; parent.advance(); child.advance();
    }
    while let Some((_key, count)) = child.head { child.skip_payload(count); new_records += 1; }
    for reader in [&mut parent, &mut child] {
        let mut tail = [0; 1]; if reader.input.read(&mut tail).unwrap() != 0 { fail("cache trailing bytes"); }
    }
    if inherited != parent_columns || inherited + new_records != child_columns { fail("record census"); }
    let temporary = output.with_extension("json.tmp");
    let mut out = BufWriter::new(File::create(&temporary).unwrap());
    writeln!(out, "{{").unwrap();
    writeln!(out, "  \"schema\": \"KRENN_AFFINE251_D12_ONE_EDGE_INHERITANCE_V1\",").unwrap();
    writeln!(out, "  \"status\": \"PASS_EXACT_CHECKPOINT_AND_CACHE_DESCENDANT\",").unwrap();
    writeln!(out, "  \"parent_round\": {},", parent_cp.round).unwrap();
    writeln!(out, "  \"child_round\": {},", child_cp.round).unwrap();
    writeln!(out, "  \"parent_support\": {},", parent_cp.support).unwrap();
    writeln!(out, "  \"child_support\": {},", child_cp.support).unwrap();
    writeln!(out, "  \"parent_columns\": {parent_columns},").unwrap();
    writeln!(out, "  \"child_columns\": {child_columns},").unwrap();
    writeln!(out, "  \"inherited_records_byte_identical\": {inherited},").unwrap();
    writeln!(out, "  \"new_child_records\": {new_records},").unwrap();
    writeln!(out, "  \"inherited_payload_bytes_compared\": {compared_bytes},").unwrap();
    writeln!(out, "  \"provider_fingerprint\": {},", parent.provider).unwrap();
    writeln!(out, "  \"parent_vector_fingerprint\": {},", parent.fingerprint).unwrap();
    writeln!(out, "  \"child_vector_fingerprint\": {},", child.fingerprint).unwrap();
    writeln!(out, "  \"final_candidate_pairing_replayed\": false,").unwrap();
    writeln!(out, "  \"seconds\": {:.6}", started.elapsed().as_secs_f64()).unwrap();
    writeln!(out, "}}").unwrap(); out.flush().unwrap(); drop(out);
    std::fs::rename(temporary, output).unwrap();
    println!("PASS parent={parent_columns} child={child_columns} inherited={inherited} new={new_records}");
}
