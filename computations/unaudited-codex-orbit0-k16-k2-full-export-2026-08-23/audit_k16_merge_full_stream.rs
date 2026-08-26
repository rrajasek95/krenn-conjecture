use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::convert::TryInto;
use std::fs::{metadata, File};
use std::io::{BufReader, Read};
use std::time::Instant;

const DIR: &str = "computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23/";
const CAT: &str = "computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23/k16_merge_inputs.tsv";
const OUT: &str = "computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23/checkpoint_k16_k2_profiles_merged.bin";
const IH: usize = 96;
const OH: usize = 128;
const REC: usize = 104;
const U: i128 = 400_591_699_200;

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct Key([u8; 42]);

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct Record {
    key: Key,
    weight: i128,
    uses: u64,
    witness: [u8; 38],
}

fn u16le(x: &[u8]) -> u16 { u16::from_le_bytes(x.try_into().unwrap()) }
fn u32le(x: &[u8]) -> u32 { u32::from_le_bytes(x.try_into().unwrap()) }
fn u64le(x: &[u8]) -> u64 { u64::from_le_bytes(x.try_into().unwrap()) }
fn i128le(x: &[u8]) -> i128 { i128::from_le_bytes(x.try_into().unwrap()) }

fn decode(x: &[u8; REC]) -> Record {
    let mut key = [0u8; 42];
    key.copy_from_slice(&x[..42]);
    let mut witness = [0u8; 38];
    witness.copy_from_slice(&x[66..]);
    Record {
        key: Key(key),
        weight: i128le(&x[42..58]),
        uses: u64le(&x[58..66]),
        witness,
    }
}

fn catalog() -> Vec<(String, u64)> {
    let text = std::fs::read_to_string(CAT).unwrap();
    let mut lines = text.lines();
    assert_eq!(lines.next(), Some("path\tbytes\tsha256\tshard"));
    let mut out = Vec::new();
    for line in lines {
        let fields: Vec<_> = line.split('\t').collect();
        assert_eq!(fields.len(), 4);
        assert_eq!(fields[2].len(), 64);
        out.push((fields[0].to_string(), fields[1].parse().unwrap()));
    }
    assert_eq!(out.len(), 281);
    out
}

struct Input {
    r: BufReader<File>,
    n: u64,
    seen: u64,
    expect_uses: u64,
    expect_weight: i128,
    uses: u64,
    weight: i128,
    prior: Option<Key>,
}

impl Input {
    fn open(path: &str, bytes: u64) -> Self {
        assert_eq!(metadata(path).unwrap().len(), bytes);
        let mut r = BufReader::with_capacity(1 << 17, File::open(path).unwrap());
        let mut h = [0u8; IH];
        r.read_exact(&mut h).unwrap();
        assert_eq!(&h[..8], b"K18PRF2\0");
        assert_eq!(u32le(&h[8..12]), 2);
        assert_eq!((h[12], h[13], u16le(&h[14..16]) as usize), (3, 2, REC));
        assert_eq!(u64le(&h[16..24]), U as u64);
        let n = u64le(&h[32..40]);
        assert_eq!(bytes, IH as u64 + REC as u64 * n);
        Self {
            r,
            n,
            seen: 0,
            expect_uses: u64le(&h[40..48]),
            expect_weight: i128le(&h[48..64]),
            uses: 0,
            weight: 0,
            prior: None,
        }
    }

    fn next(&mut self) -> Option<Record> {
        if self.seen == self.n {
            assert_eq!((self.uses, self.weight), (self.expect_uses, self.expect_weight));
            return None;
        }
        let mut b = [0u8; REC];
        self.r.read_exact(&mut b).unwrap();
        let x = decode(&b);
        if let Some(p) = self.prior { assert!(p < x.key); }
        self.prior = Some(x.key);
        assert_ne!(x.weight, 0);
        assert!(x.uses > 0);
        let source = u64le(&x.witness[24..32]);
        let p1 = x.witness[32] as usize;
        let tail1 = x.witness[33] as usize;
        let p2 = x.witness[34] as usize;
        let m1 = x.witness[35] as i128;
        let m2 = x.witness[36] as i128;
        assert!(source < 24_097_095 && p1 < 78 && tail1 < 12 && p2 < 78);
        assert_eq!(p2, x.key.0[41] as usize);
        assert_eq!(x.witness[37], 255);
        assert!(m1 > 0 && m2 > 0 && U % (m1 * m2) == 0);
        self.seen += 1;
        self.uses += x.uses;
        self.weight += x.weight;
        Some(x)
    }
}

fn main() {
    let begun = Instant::now();
    let paths = catalog();
    let mut out = BufReader::with_capacity(8 << 20, File::open(OUT).unwrap());
    let mut oh = [0u8; OH];
    out.read_exact(&mut oh).unwrap();
    assert_eq!(&oh[..8], b"K16MRG1\0");
    assert_eq!((u32le(&oh[8..12]), u16le(&oh[12..14]) as usize), (1, REC));
    assert_eq!(i128le(&oh[16..32]), U);
    assert_eq!(u64le(&oh[32..40]), 281);
    assert_eq!(u64le(&oh[40..48]), 63_918_401);
    assert_eq!(u64le(&oh[48..56]), 1_614_846_654);
    assert_eq!(u64le(&oh[56..64]), 6_876_260);
    assert_eq!(u64le(&oh[64..72]), 203_023);
    assert_eq!(u64le(&oh[72..80]), 1_604_299_948);
    assert_eq!(i128le(&oh[80..96]), 3_218_269_567_887_566_438_400);
    assert_eq!(i128le(&oh[96..112]), i128le(&oh[80..96]));
    assert_eq!(u64le(&oh[112..120]), 10_546_706);
    assert_eq!(u64le(&oh[120..128]), 2_049_974_172);

    let mut inputs: Vec<_> = paths.iter().map(|(p, b)| Input::open(p, *b)).collect();
    let mut current = Vec::new();
    let mut heap = BinaryHeap::new();
    for (i, input) in inputs.iter_mut().enumerate() {
        let value = input.next();
        if let Some(record) = value { heap.push(Reverse((record.key, i))); }
        current.push(value);
    }

    let (mut input_records, mut input_uses, mut input_weight) = (0u64, 0u64, 0i128);
    let (mut output_records, mut output_uses, mut output_weight) = (0u64, 0u64, 0i128);
    let (mut zero_groups, mut zero_uses) = (0u64, 0u64);
    let mut prior = None;
    while let Some(Reverse((key, i))) = heap.pop() {
        let mut aggregate = current[i].take().unwrap();
        input_records += 1;
        input_uses += aggregate.uses;
        input_weight += aggregate.weight;
        current[i] = inputs[i].next();
        if let Some(record) = current[i] { heap.push(Reverse((record.key, i))); }
        while let Some(Reverse((next_key, j))) = heap.peek().copied() {
            if next_key != key { break; }
            heap.pop();
            let record = current[j].take().unwrap();
            input_records += 1;
            input_uses += record.uses;
            input_weight += record.weight;
            aggregate.weight += record.weight;
            aggregate.uses += record.uses;
            if record.witness < aggregate.witness { aggregate.witness = record.witness; }
            current[j] = inputs[j].next();
            if let Some(value) = current[j] { heap.push(Reverse((value.key, j))); }
        }
        if aggregate.weight == 0 {
            zero_groups += 1;
            zero_uses += aggregate.uses;
        } else {
            let mut bytes = [0u8; REC];
            out.read_exact(&mut bytes).unwrap();
            let actual = decode(&bytes);
            assert_eq!(actual, aggregate);
            if let Some(p) = prior { assert!(p < aggregate.key); }
            prior = Some(aggregate.key);
            output_records += 1;
            output_uses += aggregate.uses;
            output_weight += aggregate.weight;
        }
    }
    let mut eof = [0u8; 1];
    assert_eq!(out.read(&mut eof).unwrap(), 0);
    for input in &inputs { assert_eq!(input.seen, input.n); }
    assert_eq!((input_records, input_uses, input_weight),
               (63_918_401, 1_614_846_654, 3_218_269_567_887_566_438_400));
    assert_eq!((output_records, output_uses, output_weight),
               (6_876_260, 1_604_299_948, input_weight));
    assert_eq!((zero_groups, zero_uses), (203_023, 10_546_706));
    assert_eq!(output_uses + zero_uses, input_uses);

    let result = format!(
        "{{\"status\":\"PASS_FULL_281_WAY_K16_STREAM_AND_BYTE_REPLAY\",\"input_parts\":281,\"input_records\":{},\"input_collected_uses\":{},\"input_weight_scaled\":\"{}\",\"output_records\":{},\"output_uses\":{},\"output_weight_scaled\":\"{}\",\"exact_zero_groups\":{},\"exact_zero_uses\":{},\"raw_outgoing_pivot_uses\":2049974172,\"elapsed_seconds\":{:.6}}}\n",
        input_records, input_uses, input_weight, output_records, output_uses,
        output_weight, zero_groups, zero_uses, begun.elapsed().as_secs_f64());
    std::fs::write(format!("{}results_k16_merge_full_stream_referee.json", DIR), &result).unwrap();
    print!("{}", result);
}
