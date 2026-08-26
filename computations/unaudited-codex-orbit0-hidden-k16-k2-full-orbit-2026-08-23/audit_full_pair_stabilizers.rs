use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufReader, Read};

fn main() {
    let path = "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin";
    let mut r = BufReader::with_capacity(8 << 20, File::open(path).unwrap());
    let mut h = [0u8; 80]; r.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8], b"H16ORM1\0");
    let n = u64::from_le_bytes(h[48..56].try_into().unwrap());
    let expected_sum = i128::from_le_bytes(h[64..80].try_into().unwrap());
    let mut hist = BTreeMap::<u16,u64>::new();
    let mut sum = 0i128;
    let mut prior: Option<[u8;25]> = None;
    for _ in 0..n {
        let mut b = [0u8;53]; r.read_exact(&mut b).unwrap();
        let key: [u8;25] = b[..25].try_into().unwrap();
        if let Some(p) = prior { assert!(p < key); } prior = Some(key);
        sum += i128::from_le_bytes(b[25..41].try_into().unwrap());
        let os = u16::from_le_bytes(b[49..51].try_into().unwrap());
        let ss = u16::from_le_bytes(b[51..53].try_into().unwrap());
        assert_eq!(u32::from(os) * u32::from(ss), 384);
        *hist.entry(ss).or_default() += 1;
    }
    assert_eq!(sum, expected_sum);
    let mut tail=[0u8;1]; assert_eq!(r.read(&mut tail).unwrap(),0);
    println!("count={} weight_sum={} stabilizer_hist={:?}", n, sum, hist);
}
