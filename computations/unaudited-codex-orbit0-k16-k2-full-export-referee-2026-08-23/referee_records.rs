mod referee {
    #![allow(dead_code)]
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

    const ROOT: &str = "computations/unaudited-codex-orbit0-k16-k2-full-export-referee-2026-08-23/";
    const U2: i128 = 400_591_699_200;
    const EXPECT_N: u64 = 63_918_401;
    const EXPECT_WEIGHT: i128 = 3_218_269_567_887_566_438_400;

    fn i128le(x: &[u8]) -> i128 { i128::from_le_bytes(x.try_into().unwrap()) }

    fn replay(x: &[u8; 104], start: usize, end: usize, e: &E, direct: &[u8]) {
        let mut rr = [0u8; 24]; rr.copy_from_slice(&x[66..90]); let row = Row(rr);
        let source = u64le(&x[90..98]) as usize;
        let (p1, t1, p2, m1, m2, packet) =
            (x[98] as usize, x[99] as usize, x[100] as usize, x[101] as usize,
             x[102] as usize, x[103]);
        assert!(source >= start && source < end);
        assert!(p1 < 78 && t1 < 12 && p2 < 78 && m1 > 0 && m2 > 0);
        assert_eq!(packet, 255); assert_eq!(p2, x[41] as usize);
        let s2 = sig(&row, e);
        assert_eq!(&s2[..], &x[29..41]);
        assert_eq!(&profile(&row, p2, e)[..], &x[..29]);
        let ps2 = avail(s2, e); assert_eq!(ps2.len(), m2); assert!(ps2.contains(&p2));
        assert_eq!(U2 % ((m1 * m2) as i128), 0);
        let (head, v) = rec(direct, source); assert_ne!(v, 0);
        let ps1 = avail(sig(&head, e), e); assert_eq!(ps1.len(), m1); assert!(ps1.contains(&p1));
        let child = replace(&head, &e.anchors[p1], &e.tails[p1][0][t1]);
        assert_eq!(child, row);
        let contribution = (v as i128) * U2 / ((m1 * m2) as i128);
        assert_ne!(contribution, 0);
    }

    pub fn run() {
        use std::fs::File;
        use std::io::{BufRead, BufReader, Read};
        use std::time::Instant;
        let begun = Instant::now();
        let e = parse();
        let direct = read(format!("{}checkpoint_direct_k16.bin", DIR)).unwrap();
        assert_eq!(nrec(&direct), 24_097_095);
        let tsv = File::open(format!("{}verified_parts.tsv", ROOT)).unwrap();
        let mut lines = BufReader::new(tsv).lines(); assert!(lines.next().unwrap().unwrap().starts_with("shard\t"));
        let (mut parts, mut records, mut uses, mut weight, mut samples) = (0u64, 0u64, 0u64, 0i128, 0u64);
        for line in lines {
            let line = line.unwrap(); if line.is_empty() { continue }
            let f: Vec<_> = line.split('\t').collect(); assert_eq!(f.len(), 7);
            let (shard, start, end, part): (usize, usize, usize, u64) =
                (f[0].parse().unwrap(), f[1].parse().unwrap(), f[2].parse().unwrap(), f[3].parse().unwrap());
            assert_eq!((start, end), (24_097_095usize * shard / 64, 24_097_095usize * (shard + 1) / 64));
            let expected_bytes: u64 = f[5].parse().unwrap();
            let mut r = BufReader::with_capacity(16 << 20, File::open(f[4]).unwrap());
            let mut h = [0u8; 96]; r.read_exact(&mut h).unwrap();
            assert_eq!(&h[..8], b"K18PRF2\0"); assert_eq!(u32le(&h[8..12]), 2);
            assert_eq!((h[12], h[13], u16::from_le_bytes(h[14..16].try_into().unwrap())), (3, 2, 104));
            assert_eq!(u64le(&h[16..24]), U2 as u64); assert_eq!(u64le(&h[24..32]), part);
            let n = u64le(&h[32..40]); let hu = u64le(&h[40..48]); let hw = i128le(&h[48..64]);
            assert!(h[64..].iter().all(|&b| b == 0));
            assert_eq!(expected_bytes, 96 + 104 * n);
            let (mut prior, mut pu, mut pw) = (None, 0u64, 0i128);
            let sample_idx = [0, n / 3, (2 * n) / 3, n.saturating_sub(1)];
            for i in 0..n {
                let mut x = [0u8; 104]; r.read_exact(&mut x).unwrap();
                let mut key = [0u8; 42]; key.copy_from_slice(&x[..42]);
                if let Some(p) = prior { assert!(p < key); } prior = Some(key);
                let w = i128le(&x[42..58]); let u = u64le(&x[58..66]);
                assert_ne!(w, 0); assert!(u > 0); pw += w; pu += u;
                let source = u64le(&x[90..98]) as usize;
                assert!(source >= start && source < end);
                assert!(x[98] < 78 && x[99] < 12 && x[100] < 78 && x[101] > 0 && x[102] > 0);
                assert_eq!(x[103], 255); assert_eq!(x[100], x[41]);
                assert_eq!(U2 % ((x[101] as i128) * (x[102] as i128)), 0);
                if sample_idx.contains(&i) { replay(&x, start, end, &e, &direct); samples += 1; }
            }
            let mut z = [0u8; 1]; assert_eq!(r.read(&mut z).unwrap(), 0);
            assert_eq!((pu, pw), (hu, hw));
            records += n; uses += pu; weight += pw; parts += 1;
        }
        assert_eq!(parts, 281); assert_eq!(records, EXPECT_N); assert_eq!(weight, EXPECT_WEIGHT);
        let text = format!(concat!(
            "{{\n  \"status\": \"PASS_INDEPENDENT_FULL_RECORD_SCAN_AND_DISTRIBUTED_LITERAL_REPLAY\",\n",
            "  \"parts\": {},\n  \"records\": {},\n  \"compact_record_uses\": {},\n",
            "  \"signed_weight_scaled\": \"{}\",\n  \"literal_witness_samples\": {},\n",
            "  \"checks\": [\"header_schema_and_size\", \"strict_part_key_order\", \"nonzero_weight_and_use\",",
            " \"header_record_sums\", \"source_range\", \"pivot_profile_signature\", \"source_child_replay\", \"denominator_divisibility\"],\n",
            "  \"elapsed_seconds\": {:.6}\n}}\n"), parts, records, uses, weight, samples, begun.elapsed().as_secs_f64());
        std::fs::write(format!("{}results_record_scan.json", ROOT), &text).unwrap();
        print!("{}", text);
    }
}

fn main() { referee::run(); }
