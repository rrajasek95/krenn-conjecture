//! Exact grouped direct-K16 K2,K2,K4 K24 charge-only fold: R:2-2-4.
#![allow(dead_code)]
mod fold {
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");
    use std::collections::BTreeMap;
    use std::fs::{metadata, rename, File};
    use std::io::{BufReader, Read, Seek, SeekFrom};
    use std::sync::Mutex;
    const INPUT: &str =
        "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin";
    const HEADER: u64 = 16;
    const RECORD: u64 = 32;
    const N: u64 = 24_097_095;
    const U: i128 = 400_591_699_200;
    const IDS: [&str; 6] = [
        "D16:224|R:2-2-4",
        "D16:233|R:2-2-4",
        "D16:242|R:2-2-4",
        "D16:323|R:2-2-4",
        "D16:332|R:2-2-4",
        "D16:422|R:2-2-4",
    ];
    type Plan = Vec<(u8, [u8; 12], Vec<usize>)>;
    #[derive(Default)]
    struct Q {
        rows: u64,
        source: i128,
        l1: i128,
        piv16: u64,
        p1: u64,
        k18: u64,
        piv18: u64,
        p2: u64,
        k20: u64,
        piv20: u64,
        p3: u64,
        k23: u64,
        charge: i128,
        hits: u64,
        misses: u64,
        peak: usize,
        hist: BTreeMap<(u8, u8, u8), u64>,
    }
    impl Q {
        fn add(&mut self, x: Q) {
            self.rows += x.rows;
            self.source += x.source;
            self.l1 += x.l1;
            self.piv16 += x.piv16;
            self.p1 += x.p1;
            self.k18 += x.k18;
            self.piv18 += x.piv18;
            self.p2 += x.p2;
            self.k20 += x.k20;
            self.piv20 += x.piv20;
            self.p3 += x.p3;
            self.k23 += x.k23;
            self.charge += x.charge;
            self.hits += x.hits;
            self.misses += x.misses;
            self.peak = self.peak.max(x.peak);
            for (k, v) in x.hist {
                *self.hist.entry(k).or_default() += v
            }
        }
    }
    fn hx(r: &Row) -> String {
        r.0.iter().map(|x| format!("{:02x}", x)).collect()
    }
    fn target(i: u64) -> Option<usize> {
        Some((i * 257 / N).min(256) as usize)
    }
    fn worker(
        e: Arc<E>,
        ranges: Vec<(u64, u64)>,
        samples: Arc<Mutex<Vec<Option<(u64, String)>>>>,
    ) -> Q {
        let file = File::open(INPUT).unwrap();
        let mut rd = BufReader::with_capacity(4 << 20, file);
        let mut q = Q::default();
        let mut ac: HashMap<[u8; 12], Vec<usize>> = HashMap::new();
        let mut pc: HashMap<([u8; 12], u8), Plan> = HashMap::new();
        for (start, end) in ranges {
            rd.seek(SeekFrom::Start(HEADER + RECORD * start)).unwrap();
            let mut terminal: HashMap<RKey, (i64, i64, u64, u64)> = HashMap::new();
            for index in start..end {
                let mut b = [0u8; 32];
                rd.read_exact(&mut b).unwrap();
                let mut rr = [0u8; 24];
                rr.copy_from_slice(&b[..24]);
                let row = Row(rr);
                assert!(row.0.windows(2).all(|w| w[0] <= w[1]));
                let v = i64::from_le_bytes(b[24..].try_into().unwrap()) as i128;
                assert_ne!(v, 0);
                q.rows += 1;
                q.source += v;
                q.l1 += v.abs();
                let s1 = sig(&row, &e);
                let ps1 = ac.entry(s1).or_insert_with(|| avail(s1, &e)).clone();
                if ps1.is_empty() {
                    continue;
                }
                q.piv16 += 1;
                let m1 = ps1.len();
                q.p1 += m1 as u64;
                q.k18 += 12 * m1 as u64;
                let sj = target(index);
                let mut sample = None;
                for p1 in ps1 {
                    for (ti1, t1) in e.tails[p1][0].iter().enumerate() {
                        let s2 = child_sig(s1, p1, t1, &e);
                        let ps2 = ac.entry(s2).or_insert_with(|| avail(s2, &e)).clone();
                        if ps2.is_empty() {
                            continue;
                        }
                        q.piv18 += 1;
                        let m2 = ps2.len();
                        q.p2 += m2 as u64;
                        q.k20 += 12 * m2 as u64;
                        let row2 = replace(&row, &e.anchors[p1], t1);
                        assert_eq!(sig(&row2, &e), s2);
                        for p2 in ps2 {
                            let plan = pc.entry((s2, p2 as u8)).or_insert_with(|| {
                                let mut z = Vec::new();
                                for (ti, t2) in e.tails[p2][0].iter().enumerate() {
                                    let s3 = child_sig(s2, p2, t2, &e);
                                    let ps3 = avail(s3, &e);
                                    if !ps3.is_empty() {
                                        z.push((ti as u8, s3, ps3))
                                    }
                                }
                                z
                            });
                            for (ti2, s3, ps3) in plan.iter() {
                                q.piv20 += 1;
                                let m3 = ps3.len();
                                q.p3 += m3 as u64;
                                *q.hist.entry((m1 as u8, m2 as u8, m3 as u8)).or_default() += 1;
                                assert_eq!(U % ((m1 * m2 * m3) as i128), 0);
                                let unit = -U / ((m1 * m2 * m3) as i128);
                                let row3 =
                                    replace(&row2, &e.anchors[p2], &e.tails[p2][0][*ti2 as usize]);
                                assert_eq!(sig(&row3, &e), *s3);
                                for &p3 in ps3 {
                                    let key = RKey {
                                        profile: profile(&row3, p3, &e),
                                        sig: *s3,
                                        pivot: p3 as u8,
                                        degree: 4,
                                    };
                                    let z = if let Some(&x) = terminal.get(&key) {
                                        q.hits += 1;
                                        x
                                    } else {
                                        q.misses += 1;
                                        resp(&row3, *s3, p3, 4, &e, &mut terminal)
                                    };
                                    assert_eq!((z.2, z.3), (60, 60));
                                    assert_eq!(z.0, z.1);
                                    q.k23 += 60;
                                    q.charge += v * unit * (z.0 as i128);
                                    if sj.is_some() && sample.is_none() && z.0 != 0 {
                                        sample=Some(format!("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",sj.unwrap(),index,v,hx(&row),hx(&row2),hx(&row3),p1,ti1,p2,ti2,p3,m1,m2,m3,z.0,unit,v*unit*(z.0 as i128),4))
                                    }
                                }
                            }
                        }
                    }
                }
                if let Some(x) = sample {
                    let j = sj.unwrap();
                    let mut z = samples.lock().unwrap();
                    if z[j].as_ref().map(|v| index < v.0).unwrap_or(true) {
                        z[j] = Some((index, x))
                    }
                }
            }
            q.peak = q.peak.max(terminal.len())
        }
        q
    }
    fn ranges(begin: u64, count: u64, distributed: bool, workers: usize) -> Vec<Vec<(u64, u64)>> {
        let pieces = workers * 256;
        let mut out = vec![Vec::new(); workers];
        for p in 0..pieces {
            let (a, b) = if distributed {
                let wa = count * p as u64 / pieces as u64;
                let wb = count * (p + 1) as u64 / pieces as u64;
                let base = N * p as u64 / pieces as u64;
                (base, base + wb - wa)
            } else {
                (
                    begin + count * p as u64 / pieces as u64,
                    begin + count * (p + 1) as u64 / pieces as u64,
                )
            };
            if a < b {
                out[p % workers].push((a, b))
            }
        }
        out
    }
    fn hist(h: &BTreeMap<(u8, u8, u8), u64>) -> String {
        h.iter()
            .map(|(&(a, b, c), n)| format!("\"{}_{}_{}\":{}", a, b, c, n))
            .collect::<Vec<_>>()
            .join(",")
    }
    pub fn run() {
        let begun = Instant::now();
        let a: Vec<_> = std::env::args().collect();
        let mut begin = 0u64;
        let mut count = N;
        let mut distributed = false;
        let mut workers = 8usize;
        let mut output = "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_k16_r224_prefix.json".to_string();
        let mut i = 1;
        while i < a.len() {
            match a[i].as_str() {
                "--start-record" => {
                    begin = a[i + 1].parse().unwrap();
                    i += 2
                }
                "--count-records" => {
                    count = a[i + 1].parse().unwrap();
                    i += 2
                }
                "--distributed-records" => {
                    count = a[i + 1].parse().unwrap();
                    distributed = true;
                    i += 2
                }
                "--workers" => {
                    workers = a[i + 1].parse().unwrap();
                    i += 2
                }
                "--output" => {
                    output = a[i + 1].clone();
                    i += 2
                }
                _ => panic!("bad arg"),
            }
        }
        assert!((1..=8).contains(&workers) && begin <= N && count <= N - begin);
        let mut header = [0u8; 16];
        File::open(INPUT).unwrap().read_exact(&mut header).unwrap();
        assert_eq!(&header[..8], b"K16DIR1\0");
        assert_eq!(u64::from_le_bytes(header[8..].try_into().unwrap()), N);
        assert_eq!(metadata(INPUT).unwrap().len(), HEADER + RECORD * N);
        let e = Arc::new(parse());
        let samples = Arc::new(Mutex::new(
            (0..257)
                .map(|_| None)
                .collect::<Vec<Option<(u64, String)>>>(),
        ));
        let mut rr = ranges(begin, count, distributed, workers);
        let mut jobs = Vec::new();
        for w in 0..workers {
            let ee = e.clone();
            let ss = samples.clone();
            let r = std::mem::take(&mut rr[w]);
            jobs.push(thread::spawn(move || worker(ee, r, ss)))
        }
        let mut q = Q::default();
        for j in jobs {
            q.add(j.join().unwrap())
        }
        let full = !distributed && begin == 0 && count == N;
        if full {
            assert_eq!(
                (q.rows, q.source, q.l1),
                (24_097_095, 1_464_625_152, 13_978_655_136)
            );
            assert_eq!((q.piv16, q.p1), (24_003_767, 129_939_187));
            assert_eq!(
                (q.k18, q.piv18, q.p2),
                (1_559_270_244, 807_499_618, 2_049_974_172)
            );
            assert_eq!(
                (q.k20, q.piv20, q.p3),
                (24_599_690_064, 2_745_607_644, 2_745_607_644)
            );
        }
        assert_eq!(q.k18, 12 * q.p1);
        assert_eq!(q.k20, 12 * q.p2);
        assert_eq!(q.k23, 60 * q.p3);
        assert_eq!(q.hits + q.misses, q.p3);
        assert_eq!(q.hist.values().sum::<u64>(), q.piv20);
        assert_eq!(
            q.hist
                .iter()
                .map(|((_, _, m), n)| *m as u64 * *n)
                .sum::<u64>(),
            q.p3
        );
        let elapsed = begun.elapsed().as_secs_f64();
        assert!(elapsed < 600.0);
        let projected = elapsed * N as f64 / count as f64;
        let ids = IDS
            .iter()
            .map(|x| format!("\"{}\"", x))
            .collect::<Vec<_>>()
            .join(",");
        let ss = samples
            .lock()
            .unwrap()
            .iter()
            .filter_map(|x| x.as_ref().map(|v| v.1.clone()))
            .collect::<Vec<_>>();
        if full {
            assert_eq!(ss.len(), 257)
        }
        let sp = format!("{}.samples.tsv", output);
        let mut lines=vec!["sample_ordinal\trecord_index\tcoefficient\tsource_row\tK18_row\tK20_row\tp1\tt1\tp2\tt2\tp3\tm1\tm2\tm3\tterminal_q\tunit_scaled_U\tnonzero_contribution_scaled_U\tfinal_degree".to_string()];
        lines.extend(ss);
        let st = format!("{}.tmp", sp);
        std::fs::write(&st, format!("{}\n", lines.join("\n"))).unwrap();
        rename(st, &sp).unwrap();
        let status = if full {
            "PASS_COMPLETE_GROUPED_SIX_D16_R_2_2_4_K24_CHARGE_ONLY"
        } else {
            "PASS_BOUNDED_GROUPED_SIX_D16_R_2_2_4_K24_CHARGE_ONLY_GATE"
        };
        let text=format!("{{\n  \"status\":\"{}\",\n  \"group_id\":\"source_D16_R2_2_4\",\n  \"degree\":24,\n  \"scale_U\":\"{}\",\n  \"ids\":[{}],\n  \"covered_ids\":6,\n  \"individual_id_charges\":null,\n  \"record_interval\":[{},{}],\n  \"records_declared\":{},\n  \"distributed_prefix\":{},\n  \"source_rows\":{},\n  \"signed_source_coefficient\":\"{}\",\n  \"l1_source_coefficient\":\"{}\",\n  \"pivotable_K16_rows\":{},\n  \"p1_uses\":{},\n  \"K18_children\":{},\n  \"pivotable_K18_children\":{},\n  \"p2_uses\":{},\n  \"K20_children\":{},\n  \"pivotable_K20_children\":{},\n  \"p3_uses\":{},\n  \"K24_terminal_occurrences\":{},\n  \"full_occurrences\":{},\n  \"irreducible_occurrences\":{},\n  \"full_charge_scaled_U\":\"{}\",\n  \"irreducible_charge_scaled_U\":\"{}\",\n  \"m1_m2_m3_hist\":{{{}}},\n  \"terminal_cache\":{{\"hits\":{},\"misses\":{},\"peak_keys_per_piece\":{}}},\n  \"literal_samples\":{},\n  \"sample_ledger\":\"{}\",\n  \"packet_grouping_guard\":\"checkpoint retains collected canonical rows and coefficients but not packet labels; only the grouped six-ID scalar is source-faithful\",\n  \"sign_rule\":\"stored v is the direct coefficient in P; three normalized response flips give -v/(m1*m2*m3)\",\n  \"terminality\":\"every K24 K4 child has active-anchor mass 0 and cannot pivot; full equals irreducible\",\n  \"elapsed_seconds\":{:.6},\n  \"projected_full_seconds\":{:.6},\n  \"scope\":\"strict grouped six-ID K24 R2-2-4 charge-only sink; no individual reconstruction, other sink, rows/columns, or membership claim\"\n}}\n",status,U,ids,begin,begin+count,N,distributed,q.rows,q.source,q.l1,q.piv16,q.p1,q.k18,q.piv18,q.p2,q.k20,q.piv20,q.p3,q.k23,q.k23,q.k23,q.charge,q.charge,hist(&q.hist),q.hits,q.misses,q.peak,lines.len()-1,sp,elapsed,projected);
        let tmp = format!("{}.tmp", output);
        std::fs::write(&tmp, &text).unwrap();
        rename(tmp, &output).unwrap();
        print!("{}", text)
    }
}
fn main() {
    fold::run()
}
