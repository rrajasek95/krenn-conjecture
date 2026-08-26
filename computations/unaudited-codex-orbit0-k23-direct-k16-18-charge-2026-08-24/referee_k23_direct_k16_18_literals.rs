//! Independent literal replay for the three grouped direct-K16 K23 sinks.
#![allow(dead_code)]
mod referee {
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");
    use std::fs::File;
    use std::io::{Read, Seek, SeekFrom};
    const INPUT: &str =
        "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin";
    const N: u64 = 24_097_095;
    const U: i128 = 400_591_699_200;
    const R43_RECORDS: [u64; 37] = [
        0, 94129, 188258, 282392, 376517, 470654, 564777, 658916, 753034, 847163, 941463, 1035422,
        1129556, 1223829, 1317816, 1411964, 1506072, 1600198, 1694326, 1788456, 1882585, 1976714,
        2070844, 2164973, 2259114, 2353234, 2447361, 2541490, 2635619, 2729754, 2823878, 2918017,
        3012136, 3106266, 3200395, 3294537, 3388653,
    ];
    fn rh(s: &str) -> Row {
        assert_eq!(s.len(), 48);
        let mut x = [0u8; 24];
        for i in 0..24 {
            x[i] = u8::from_str_radix(&s[2 * i..2 * i + 2], 16).unwrap()
        }
        assert!(x.windows(2).all(|w| w[0] <= w[1]));
        Row(x)
    }
    fn source(file: &mut File, index: u64) -> (Row, i128) {
        file.seek(SeekFrom::Start(16 + 32 * index)).unwrap();
        let mut b = [0u8; 32];
        file.read_exact(&mut b).unwrap();
        let mut x = [0u8; 24];
        x.copy_from_slice(&b[..24]);
        (
            Row(x),
            i64::from_le_bytes(b[24..].try_into().unwrap()) as i128,
        )
    }
    fn terminal(row: &Row, p: usize, d: usize, e: &E) -> i64 {
        let s = sig(row, e);
        let mut q = 0;
        for t in &e.tails[p][d - 2] {
            q += charge(&replace(row, &e.anchors[p], t), e);
            assert!(avail(child_sig(s, p, t, e), e).is_empty())
        }
        q
    }
    fn window(j: usize, index: u64) {
        assert!(index >= N * j as u64 / 257 && index < N * (j as u64 + 1) / 257)
    }
    fn two(
        path: &str,
        first: usize,
        finald: usize,
        expected_start: usize,
        expected_end: usize,
        e: &E,
        file: &mut File,
    ) -> usize {
        let text = std::fs::read_to_string(path).unwrap();
        let mut seen = [false; 257];
        let mut continuations = HashSet::new();
        let mut n = 0;
        for (ln, line) in text.lines().enumerate() {
            if ln == 0 {
                assert_eq!(line,"sample_ordinal\trecord_index\tcoefficient\tsource_row\tintermediate_row\tp1\tt1\tp2\tm1\tm2\tfirst_degree\tfinal_degree\tterminal_q\tunit_scaled_U\tnonzero_contribution_scaled_U");
                continue;
            }
            let f: Vec<_> = line.split('\t').collect();
            assert_eq!(f.len(), 15);
            let j = f[0].parse::<usize>().unwrap();
            let index = f[1].parse::<u64>().unwrap();
            assert!(!seen[j]);
            seen[j] = true;
            if first == 4 {
                assert!(R43_RECORDS.contains(&index));
                assert!(continuations.insert(f[1..].join("\t")))
            } else {
                window(j, index)
            }
            let v = f[2].parse::<i128>().unwrap();
            let r0 = rh(f[3]);
            let r1 = rh(f[4]);
            let p1 = f[5].parse::<usize>().unwrap();
            let ti = f[6].parse::<usize>().unwrap();
            let p2 = f[7].parse::<usize>().unwrap();
            let m1 = f[8].parse::<usize>().unwrap();
            let m2 = f[9].parse::<usize>().unwrap();
            assert_eq!(
                (
                    f[10].parse::<usize>().unwrap(),
                    f[11].parse::<usize>().unwrap()
                ),
                (first, finald)
            );
            let q = f[12].parse::<i64>().unwrap();
            let unit = f[13].parse::<i128>().unwrap();
            let contrib = f[14].parse::<i128>().unwrap();
            let (src, sv) = source(file, index);
            assert!(src == r0);
            assert_eq!(sv, v);
            let s0 = sig(&r0, e);
            let ps1 = avail(s0, e);
            assert_eq!(ps1.len(), m1);
            assert!(ps1.contains(&p1));
            let t = &e.tails[p1][first - 2][ti];
            assert!(replace(&r0, &e.anchors[p1], t) == r1);
            let s1 = sig(&r1, e);
            assert_eq!(s1, child_sig(s0, p1, t, e));
            let ps2 = avail(s1, e);
            assert_eq!(ps2.len(), m2);
            assert!(ps2.contains(&p2));
            assert_ne!(q, 0);
            assert_eq!(q, terminal(&r1, p2, finald, e));
            assert_eq!(unit, U / ((m1 * m2) as i128));
            assert_eq!(contrib, v * unit * (q as i128));
            n += 1
        }
        assert!(seen[..expected_start].iter().all(|x| !*x));
        assert!(seen[expected_start..expected_end].iter().all(|x| *x));
        assert!(seen[expected_end..].iter().all(|x| !*x));
        assert_eq!(n, expected_end - expected_start);
        n
    }
    fn triple(path: &str, e: &E, file: &mut File) -> usize {
        let text = std::fs::read_to_string(path).unwrap();
        let mut seen = [false; 257];
        let mut n = 0;
        for (ln, line) in text.lines().enumerate() {
            if ln == 0 {
                assert_eq!(line,"sample_ordinal\trecord_index\tcoefficient\tsource_row\tK18_row\tK20_row\tp1\tt1\tp2\tt2\tp3\tm1\tm2\tm3\tterminal_q\tunit_scaled_U\tnonzero_contribution_scaled_U\tfinal_degree");
                continue;
            }
            let f: Vec<_> = line.split('\t').collect();
            assert_eq!(f.len(), 18);
            let j = f[0].parse::<usize>().unwrap();
            let index = f[1].parse::<u64>().unwrap();
            assert!(!seen[j]);
            seen[j] = true;
            window(j, index);
            let v = f[2].parse::<i128>().unwrap();
            let r0 = rh(f[3]);
            let r1 = rh(f[4]);
            let r2 = rh(f[5]);
            let p1 = f[6].parse::<usize>().unwrap();
            let ti1 = f[7].parse::<usize>().unwrap();
            let p2 = f[8].parse::<usize>().unwrap();
            let ti2 = f[9].parse::<usize>().unwrap();
            let p3 = f[10].parse::<usize>().unwrap();
            let m1 = f[11].parse::<usize>().unwrap();
            let m2 = f[12].parse::<usize>().unwrap();
            let m3 = f[13].parse::<usize>().unwrap();
            let q = f[14].parse::<i64>().unwrap();
            let unit = f[15].parse::<i128>().unwrap();
            let contrib = f[16].parse::<i128>().unwrap();
            assert_eq!(f[17].parse::<usize>().unwrap(), 3);
            let (src, sv) = source(file, index);
            assert!(src == r0);
            assert_eq!(sv, v);
            let s0 = sig(&r0, e);
            let ps1 = avail(s0, e);
            assert_eq!(ps1.len(), m1);
            assert!(ps1.contains(&p1));
            let t1 = &e.tails[p1][0][ti1];
            assert!(replace(&r0, &e.anchors[p1], t1) == r1);
            let s1 = sig(&r1, e);
            assert_eq!(s1, child_sig(s0, p1, t1, e));
            let ps2 = avail(s1, e);
            assert_eq!(ps2.len(), m2);
            assert!(ps2.contains(&p2));
            let t2 = &e.tails[p2][0][ti2];
            assert!(replace(&r1, &e.anchors[p2], t2) == r2);
            let s2 = sig(&r2, e);
            assert_eq!(s2, child_sig(s1, p2, t2, e));
            let ps3 = avail(s2, e);
            assert_eq!(ps3.len(), m3);
            assert!(ps3.contains(&p3));
            assert_ne!(q, 0);
            assert_eq!(q, terminal(&r2, p3, 3, e));
            assert_eq!(unit, -U / ((m1 * m2 * m3) as i128));
            assert_eq!(contrib, v * unit * (q as i128));
            n += 1
        }
        assert!(seen.iter().all(|x| *x));
        assert_eq!(n, 257);
        n
    }
    pub fn run() {
        let a: Vec<_> = std::env::args().collect();
        if a.len() == 3 && a[1] == "--reconcile-34-shard0" {
            let e = parse();
            let mut f = File::open(INPUT).unwrap();
            let n = two(&a[2], 3, 4, 0, 129, &e, &mut f);
            println!("{{\"status\":\"PASS_INDEPENDENT_K23_DIRECT_K16_R3_4_SHARD0_LITERAL_REPLAY\",\"samples\":{},\"all_nonzero_terminal_irreducible_sign_U_exact\":true}}", n);
            return;
        }
        if a.len() == 3 && a[1] == "--reconcile-34-shard1" {
            let e = parse();
            let mut f = File::open(INPUT).unwrap();
            let n = two(&a[2], 3, 4, 128, 257, &e, &mut f);
            println!("{{\"status\":\"PASS_INDEPENDENT_K23_DIRECT_K16_R3_4_SHARD1_LITERAL_REPLAY\",\"samples\":{},\"all_nonzero_terminal_irreducible_sign_U_exact\":true}}", n);
            return;
        }
        if a.len() == 3 && a[1] == "--reconcile-34-full" {
            let e = parse();
            let mut f = File::open(INPUT).unwrap();
            let n = two(&a[2], 3, 4, 0, 257, &e, &mut f);
            println!("{{\"status\":\"PASS_INDEPENDENT_K23_DIRECT_K16_R3_4_MERGED_LITERAL_REPLAY\",\"samples\":{},\"all_nonzero_terminal_irreducible_sign_U_exact\":true}}", n);
            return;
        }
        if a.len() == 3 && a[1] == "--reconcile-223-full" {
            let e = parse();
            let mut f = File::open(INPUT).unwrap();
            let n = triple(&a[2], &e, &mut f);
            println!("{{\"status\":\"PASS_INDEPENDENT_K23_DIRECT_K16_R2_2_3_LITERAL_REPLAY\",\"samples\":{},\"all_nonzero_terminal_irreducible_sign_U_exact\":true}}", n);
            return;
        }
        assert!(
            a.len() == 4 || a.len() == 5,
            "referee R3-4.tsv R4-3.tsv R2-2-3.tsv [output.json]"
        );
        let e = parse();
        let mut f = File::open(INPUT).unwrap();
        let n1 = two(&a[1], 3, 4, 0, 257, &e, &mut f);
        let n2 = two(&a[2], 4, 3, 0, 257, &e, &mut f);
        let n3 = triple(&a[3], &e, &mut f);
        let text = format!("{{\"status\":\"PASS_INDEPENDENT_K23_DIRECT_K16_18_LITERAL_REPLAY\",\"R3_4_samples\":{},\"R4_3_samples\":{},\"R2_2_3_samples\":{},\"total_samples\":{},\"all_nonzero_terminal_irreducible_sign_U_exact\":true}}\n",n1,n2,n3,n1+n2+n3);
        if a.len() == 5 {
            let tmp = format!("{}.tmp", a[4]);
            std::fs::write(&tmp, &text).unwrap();
            std::fs::rename(tmp, &a[4]).unwrap();
        }
        print!("{}", text)
    }
}
fn main() {
    referee::run()
}
