use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::convert::TryInto;
use std::fs::{File, metadata, read_dir, rename};
use std::io::{BufReader, BufWriter, Read, Seek, SeekFrom, Write};
use std::path::PathBuf;
use std::time::Instant;

const DIR: &str = "computations/unaudited-codex-orbit0-k18-k14-full-profiles-2026-08-23/";
const U: u64 = 400_591_699_200;
const IN_HEADER: usize = 96;
const OUT_HEADER: usize = 256;
const REC: usize = 104;

#[derive(Clone, Copy, Eq, Ord, PartialEq, PartialOrd)]
struct Key([u8; 42]);
#[derive(Clone, Copy)]
struct Val { weight: i128, uses: u64, witness: [u8; 38] }

fn i128le(x: &[u8]) -> i128 { i128::from_le_bytes(x.try_into().unwrap()) }
fn u64le(x: &[u8]) -> u64 { u64::from_le_bytes(x.try_into().unwrap()) }

fn read_record<R: Read>(r: &mut R) -> Option<(Key, Val)> {
    let mut b = [0u8; REC];
    match r.read_exact(&mut b) {
        Ok(()) => {},
        Err(e) if e.kind() == std::io::ErrorKind::UnexpectedEof => return None,
        Err(e) => panic!("record read: {e}"),
    }
    let mut k = [0u8; 42]; k.copy_from_slice(&b[..42]);
    let mut witness = [0u8; 38]; witness.copy_from_slice(&b[66..]);
    Some((Key(k), Val { weight: i128le(&b[42..58]), uses: u64le(&b[58..66]), witness }))
}

fn write_record<W: Write>(w: &mut W, k: Key, v: Val) {
    w.write_all(&k.0).unwrap();
    w.write_all(&v.weight.to_le_bytes()).unwrap();
    w.write_all(&v.uses.to_le_bytes()).unwrap();
    w.write_all(&v.witness).unwrap();
}

struct Run {
    reader: BufReader<File>, cur: Option<(Key, Val)>, prior: Option<Key>,
    read: u64, expected: u64,
}
impl Run {
    fn open(path: &PathBuf) -> (Self, u64, i128) {
        let mut reader = BufReader::with_capacity(1 << 16, File::open(path).unwrap());
        let mut h = [0u8; IN_HEADER]; reader.read_exact(&mut h).unwrap();
        assert_eq!(&h[..8], b"K18PRF2\0");
        assert_eq!(u32::from_le_bytes(h[8..12].try_into().unwrap()), 2);
        assert_eq!((h[12], h[13]), (1, 2));
        assert_eq!(u16::from_le_bytes(h[14..16].try_into().unwrap()) as usize, REC);
        assert_eq!(u64le(&h[16..24]), U);
        let n = u64le(&h[32..40]);
        let uses = u64le(&h[40..48]);
        let weight = i128le(&h[48..64]);
        assert_eq!(metadata(path).unwrap().len(), IN_HEADER as u64 + REC as u64 * n);
        let mut out = Run { reader, cur: None, prior: None, read: 0, expected: n };
        out.advance();
        (out, uses, weight)
    }
    fn advance(&mut self) {
        let x = read_record(&mut self.reader);
        if let Some((k, v)) = x {
            assert_ne!(v.weight, 0);
            assert!(v.uses > 0);
            if let Some(p) = self.prior { assert!(p < k); }
            self.prior = Some(k); self.read += 1;
        }
        self.cur = x;
    }
    fn finish(&self) { assert!(self.cur.is_none()); assert_eq!(self.read, self.expected); }
}

fn main() {
    let begun = Instant::now();
    let mut paths: Vec<_> = read_dir(DIR).unwrap().map(|x| x.unwrap().path())
        .filter(|p| p.file_name().unwrap().to_string_lossy().contains(".part") && p.extension().map_or(false, |x| x == "bin"))
        .collect();
    paths.sort(); assert_eq!(paths.len(), 490);

    let mut runs = Vec::with_capacity(paths.len());
    let mut heap = BinaryHeap::new();
    let (mut input_uses, mut input_weight) = (0u64, 0i128);
    for (i, p) in paths.iter().enumerate() {
        let (r, uses, weight) = Run::open(p);
        input_uses += uses; input_weight += weight;
        if let Some((k, _)) = r.cur { heap.push(Reverse((k, i))); }
        runs.push(r);
    }

    let out = format!("{}k14_k4_enriched_profiles.bin", DIR);
    let tmp = format!("{}.tmp", out);
    let mut writer = BufWriter::with_capacity(16 << 20, File::create(&tmp).unwrap());
    writer.write_all(&[0u8; OUT_HEADER]).unwrap();
    let (mut output_count, mut zero_count, mut output_uses, mut output_weight) = (0u64, 0u64, 0u64, 0i128);
    while let Some(Reverse((key, i))) = heap.pop() {
        let (_, mut val) = runs[i].cur.unwrap(); runs[i].advance();
        if let Some((next, _)) = runs[i].cur { heap.push(Reverse((next, i))); }
        while let Some(Reverse((other, j))) = heap.peek().copied() {
            if other != key { break; }
            heap.pop(); let (_, x) = runs[j].cur.unwrap();
            val.weight += x.weight; val.uses += x.uses;
            if x.witness < val.witness { val.witness = x.witness; }
            runs[j].advance();
            if let Some((next, _)) = runs[j].cur { heap.push(Reverse((next, j))); }
        }
        if val.weight == 0 { zero_count += 1; continue; }
        write_record(&mut writer, key, val);
        output_count += 1; output_uses += val.uses; output_weight += val.weight;
    }
    writer.flush().unwrap(); drop(writer);
    for r in &runs { r.finish(); }
    assert_eq!(output_weight, input_weight);

    let mut h = [0u8; OUT_HEADER];
    h[..8].copy_from_slice(b"K14MRG1\0");
    h[8..16].copy_from_slice(&U.to_le_bytes());
    h[16..24].copy_from_slice(&(paths.len() as u64).to_le_bytes());
    h[24..32].copy_from_slice(&runs.iter().map(|r| r.expected).sum::<u64>().to_le_bytes());
    h[32..40].copy_from_slice(&input_uses.to_le_bytes());
    h[40..56].copy_from_slice(&input_weight.to_le_bytes());
    h[56..64].copy_from_slice(&output_count.to_le_bytes());
    h[64..72].copy_from_slice(&zero_count.to_le_bytes());
    h[72..80].copy_from_slice(&output_uses.to_le_bytes());
    h[80..96].copy_from_slice(&output_weight.to_le_bytes());
    let mut f = std::fs::OpenOptions::new().write(true).open(&tmp).unwrap();
    f.seek(SeekFrom::Start(0)).unwrap(); f.write_all(&h).unwrap(); f.sync_all().unwrap(); drop(f);
    rename(&tmp, &out).unwrap();
    assert_eq!(metadata(&out).unwrap().len(), OUT_HEADER as u64 + REC as u64 * output_count);

    let result = format!(concat!("{{\n  \"status\":\"PASS_EXTERNAL_SIGNED_MERGE\",\n",
        "  \"scale_U\":{},\n  \"atomic_parts\":{},\n  \"atomic_nonzero_records\":{},\n",
        "  \"atomic_record_uses\":{},\n  \"signed_weight_sum_scaled\":\"{}\",\n",
        "  \"merged_nonzero_profiles\":{},\n  \"cross_part_exact_zero_profiles\":{},\n",
        "  \"merged_retained_uses\":{},\n  \"checkpoint\":\"{}\",\n  \"elapsed_seconds\":{:.6}\n}}\n"),
        U, paths.len(), runs.iter().map(|r| r.expected).sum::<u64>(), input_uses, input_weight,
        output_count, zero_count, output_uses, out, begun.elapsed().as_secs_f64());
    std::fs::write(format!("{}results_k14_k4_profile_merge.json", DIR), &result).unwrap();
    print!("{}", result);
}
