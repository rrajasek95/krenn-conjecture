//! Exact grouped direct-K16 K24 charge-only fold: R:4-4.
#![allow(dead_code)]
mod fold {
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");
    use std::collections::BTreeMap;
    use std::fs::{metadata, rename, File};
    use std::io::{BufRead, BufReader, Read, Seek, SeekFrom};
    use std::sync::Mutex;

    const INPUT: &str =
        "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin";
    const HEADER: u64 = 16;
    const RECORD: u64 = 32;
    const N: u64 = 24_097_095;
    const U: i128 = 400_591_699_200;
    const CANDIDATES: &str =
        "computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/k24_k16_r44_support_candidates.tsv";
    const CANDIDATES_SHA256: &str =
        "57b7f0cfa15b436b6b821922c426f19d15496eb7a1cd64e7e632acaa003d5fbf";
    const BASE: [&str; 6] = ["224", "233", "242", "323", "332", "422"];

    #[derive(Default)]
    struct Q {
        rows: u64,
        source: i128,
        l1: i128,
        pivotable: u64,
        p1: u64,
        first_children: u64,
        pivmid: u64,
        p2: u64,
        terminal: u64,
        charge: i128,
        hits: u64,
        misses: u64,
        peak: usize,
        hist: BTreeMap<(u8, u8), u64>,
        nonzero_support_records: BTreeMap<u16, u64>,
    }
    impl Q {
        fn add(&mut self, x: Q) {
            self.rows += x.rows;
            self.source += x.source;
            self.l1 += x.l1;
            self.pivotable += x.pivotable;
            self.p1 += x.p1;
            self.first_children += x.first_children;
            self.pivmid += x.pivmid;
            self.p2 += x.p2;
            self.terminal += x.terminal;
            self.charge += x.charge;
            self.hits += x.hits;
            self.misses += x.misses;
            self.peak = self.peak.max(x.peak);
            for (k, v) in x.hist {
                *self.hist.entry(k).or_default() += v
            }
            for (k, v) in x.nonzero_support_records {
                *self.nonzero_support_records.entry(k).or_default() += v
            }
        }
    }
    fn hx(r: &Row) -> String {
        r.0.iter().map(|x| format!("{:02x}", x)).collect()
    }
    fn target(i: u64) -> Option<usize> {
        Some((i * 257 / N).min(256) as usize)
    }
    #[derive(Clone, Copy)]
    struct Candidate { slot: usize, support_bin: u16, p1: usize, t1: usize, p2: usize }
    fn load_candidates() -> HashMap<u64, Candidate> {
        let mut out = HashMap::new();
        let mut lines = BufReader::new(File::open(CANDIDATES).unwrap()).lines();
        assert_eq!(lines.next().unwrap().unwrap(), "candidate_slot\tsupport_bin\trecord_index\tcoefficient\tsource_row\tintermediate_row\tp1\tt1\tp2\tm1\tm2\tterminal_q\tunit_scaled_U\tnonzero_contribution_scaled_U\tfinal_degree");
        for line in lines {
            let line = line.unwrap();
            let f: Vec<_> = line.split('\t').collect();
            assert_eq!(f.len(), 15);
            let c = Candidate { slot: f[0].parse().unwrap(), support_bin: f[1].parse().unwrap(), p1: f[6].parse().unwrap(), t1: f[7].parse().unwrap(), p2: f[8].parse().unwrap() };
            let index: u64 = f[2].parse().unwrap();
            assert_eq!(c.support_bin as usize, target(index).unwrap());
            assert!(c.slot < 257 && out.insert(index, c).is_none());
        }
        assert_eq!(out.len(), 257);
        let mut slots = out.values().map(|c| c.slot).collect::<Vec<_>>();
        slots.sort_unstable();
        assert_eq!(slots, (0..257).collect::<Vec<_>>());
        let mut quotas=BTreeMap::new();
        for c in out.values(){*quotas.entry(c.support_bin).or_insert(0usize)+=1}
        assert_eq!(quotas.keys().copied().collect::<Vec<_>>(),(0u16..37).collect::<Vec<_>>());
        for bin in 0u16..37{assert_eq!(quotas[&bin],if bin<35{7}else{6})}
        out
    }
    fn worker(
        e: Arc<E>,
        ranges: Vec<(u64, u64)>,
        first: usize,
        finald: usize,
        candidates: Arc<HashMap<u64, Candidate>>,
        samples: Arc<Mutex<Vec<Option<(u64, String)>>>>,
    ) -> Q {
        let file = File::open(INPUT).unwrap();
        let mut rd = BufReader::with_capacity(4 << 20, file);
        let mut q = Q::default();
        for (start, end) in ranges {
            rd.seek(SeekFrom::Start(HEADER + RECORD * start)).unwrap();
            let mut cache: HashMap<RKey, (i64, i64, u64, u64)> = HashMap::new();
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
                let ps1 = avail(s1, &e);
                if ps1.is_empty() {
                    continue;
                }
                q.pivotable += 1;
                let m1 = ps1.len();
                q.p1 += m1 as u64;
                q.first_children += e.tails[0][first - 2].len() as u64 * m1 as u64;
                let candidate = candidates.get(&index).copied();
                let sample_j = candidate.map(|c| c.slot);
                let mut sample = None;
                let mut record_has_nonzero = false;
                for p1 in ps1 {
                    for (ti, t1) in e.tails[p1][first - 2].iter().enumerate() {
                        let s2 = child_sig(s1, p1, t1, &e);
                        let ps2 = avail(s2, &e);
                        if ps2.is_empty() {
                            continue;
                        }
                        q.pivmid += 1;
                        let m2 = ps2.len();
                        *q.hist.entry((m1 as u8, m2 as u8)).or_default() += 1;
                        assert_eq!(U % ((m1 * m2) as i128), 0);
                        let unit = U / ((m1 * m2) as i128);
                        let row2 = replace(&row, &e.anchors[p1], t1);
                        assert_eq!(sig(&row2, &e), s2);
                        for p2 in ps2 {
                            q.p2 += 1;
                            let key = RKey {
                                profile: profile(&row2, p2, &e),
                                sig: s2,
                                pivot: p2 as u8,
                                degree: finald as u8,
                            };
                            let z = if let Some(&x) = cache.get(&key) {
                                q.hits += 1;
                                x
                            } else {
                                q.misses += 1;
                                resp(&row2, s2, p2, finald, &e, &mut cache)
                            };
                            let tailn = e.tails[p2][finald - 2].len() as u64;
                            assert_eq!((z.2, z.3), (tailn, tailn));
                            assert_eq!(z.0, z.1);
                            q.terminal += tailn;
                            q.charge += v * unit * (z.0 as i128);
                            record_has_nonzero |= z.0 != 0;
                            if candidate.map_or(false, |c| c.p1 == p1 && c.t1 == ti && c.p2 == p2) {
                                assert!(sample.is_none() && z.0 != 0);
                                sample = Some(format!(
                                    "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                                    sample_j.unwrap(),
                                    index,
                                    v,
                                    hx(&row),
                                    hx(&row2),
                                    p1,
                                    ti,
                                    p2,
                                    m1,
                                    m2,
                                    first,
                                    finald,
                                    z.0,
                                    unit,
                                    v * unit * (z.0 as i128)
                                ))
                            }
                        }
                    }
                }
                if record_has_nonzero {
                    *q.nonzero_support_records.entry(target(index).unwrap() as u16).or_default() += 1;
                }
                if candidate.is_some() { assert!(sample.is_some()) }
                if let Some(x) = sample {
                    let j = sample_j.unwrap();
                    let mut z = samples.lock().unwrap();
                    if z[j].as_ref().map(|v| index < v.0).unwrap_or(true) {
                        z[j] = Some((index, x))
                    }
                }
            }
            q.peak = q.peak.max(cache.len())
        }
        q
    }
    fn ranges(begin: u64, count: u64, distributed: bool, workers: usize) -> Vec<Vec<(u64, u64)>> {
        let pieces = workers * 32;
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
    fn hist(h: &BTreeMap<(u8, u8), u64>) -> String {
        h.iter()
            .map(|(&(a, b), n)| format!("\"{}_{}\":{}", a, b, n))
            .collect::<Vec<_>>()
            .join(",")
    }
    fn support_hist(h: &BTreeMap<u16, u64>) -> String {
        h.iter().map(|(b, n)| format!("\"{}\":{}", b, n)).collect::<Vec<_>>().join(",")
    }
    pub fn run() {
        let begun = Instant::now();
        let a: Vec<_> = std::env::args().collect();
        let mut mode = "44".to_string();
        let mut begin = 0u64;
        let mut count = N;
        let mut distributed = false;
        let mut workers = 8usize;
        let mut output = "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_k16_r44_prefix.json".to_string();
        let mut i = 1;
        while i < a.len() {
            match a[i].as_str() {
                "--mode" => {
                    mode = a[i + 1].clone();
                    i += 2
                }
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
        assert!(mode == "44");
        assert!((1..=8).contains(&workers) && begin <= N && count <= N - begin);
        let (first, finald, sink) = (4, 4, "4-4");
        let mut header = [0u8; 16];
        File::open(INPUT).unwrap().read_exact(&mut header).unwrap();
        assert_eq!(&header[..8], b"K16DIR1\0");
        assert_eq!(u64::from_le_bytes(header[8..].try_into().unwrap()), N);
        assert_eq!(metadata(INPUT).unwrap().len(), HEADER + RECORD * N);
        let e = Arc::new(parse());
        let candidates = Arc::new(load_candidates());
        let samples = Arc::new(Mutex::new(
            (0..257)
                .map(|_| None)
                .collect::<Vec<Option<(u64, String)>>>(),
        ));
        let mut rr = ranges(begin, count, distributed, workers);
        let mut jobs = Vec::new();
        for w in 0..workers {
            let ee = e.clone();
            let cc = candidates.clone();
            let ss = samples.clone();
            let r = std::mem::take(&mut rr[w]);
            jobs.push(thread::spawn(move || worker(ee, r, first, finald, cc, ss)))
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
            assert_eq!((q.pivotable, q.p1), (24_003_767, 129_939_187));
            assert_eq!(q.nonzero_support_records.keys().copied().collect::<Vec<_>>(), (0u16..37).collect::<Vec<_>>());
        }
        let nt = match finald {
            2 => 12,
            3 => 32,
            4 => 60,
            _ => unreachable!(),
        };
        assert_eq!(q.terminal, nt * q.p2);
        assert_eq!(q.hits + q.misses, q.p2);
        assert_eq!(q.hist.values().sum::<u64>(), q.pivmid);
        assert_eq!(
            q.hist.iter().map(|((_, m), n)| *m as u64 * *n).sum::<u64>(),
            q.p2
        );
        let elapsed = begun.elapsed().as_secs_f64();
        assert!(elapsed < 600.0);
        let projected = elapsed * N as f64 / count as f64;
        let ids = BASE
            .iter()
            .map(|x| format!("\"D16:{}|R:{}\"", x, sink))
            .collect::<Vec<_>>()
            .join(",");
        let ss = {
            samples
                .lock()
                .unwrap()
                .iter()
                .filter_map(|x| x.as_ref().map(|v| v.1.clone()))
                .collect::<Vec<_>>()
        };
        if full {
            assert_eq!(ss.len(), 257)
        }
        let sp = format!("{}.samples.tsv", output);
        let mut lines=vec!["sample_ordinal\trecord_index\tcoefficient\tsource_row\tintermediate_row\tp1\tt1\tp2\tm1\tm2\tfirst_degree\tfinal_degree\tterminal_q\tunit_scaled_U\tnonzero_contribution_scaled_U".to_string()];
        lines.extend(ss);
        let st = format!("{}.tmp", sp);
        std::fs::write(&st, format!("{}\n", lines.join("\n"))).unwrap();
        rename(st, &sp).unwrap();
        let status = if full {
            "PASS_COMPLETE_GROUPED_SIX_D16_K24_R44_CHARGE_ONLY"
        } else {
            "PASS_BOUNDED_GROUPED_SIX_D16_K24_R44_CHARGE_ONLY_GATE"
        };
        let support_bins=q.nonzero_support_records.keys().map(|x|x.to_string()).collect::<Vec<_>>().join(",");
        let support_outside=q.nonzero_support_records.iter().filter(|(b,_)|**b>=37).map(|(_,n)|*n).sum::<u64>();
        let text=format!("{{\n  \"status\":\"{}\",\n  \"group_id\":\"source_D16_R{}_{}\",\n  \"degree\":24,\n  \"scale_U\":\"{}\",\n  \"ids\":[{}],\n  \"covered_ids\":6,\n  \"individual_id_charges\":null,\n  \"record_interval\":[{},{}],\n  \"records_declared\":{},\n  \"distributed_prefix\":{},\n  \"source_rows\":{},\n  \"signed_source_coefficient\":\"{}\",\n  \"l1_source_coefficient\":\"{}\",\n  \"pivotable_K16_rows\":{},\n  \"p1_uses\":{},\n  \"first_children\":{},\n  \"pivotable_intermediate_children\":{},\n  \"p2_uses\":{},\n  \"K24_terminal_occurrences\":{},\n  \"full_occurrences\":{},\n  \"irreducible_occurrences\":{},\n  \"full_charge_scaled_U\":\"{}\",\n  \"irreducible_charge_scaled_U\":\"{}\",\n  \"m1_m2_hist\":{{{}}},\n  \"terminal_cache\":{{\"hits\":{},\"misses\":{},\"peak_keys_per_piece\":{}}},\n  \"nonzero_support_record_hist\":{{{}}},\n  \"nonzero_support_bins\":[{}],\n  \"nonzero_support_records_outside_bins_0_36\":{},\n  \"candidate_quota_by_support_bin\":{{\"0_through_34\":7,\"35_through_36\":6}},\n  \"literal_samples\":{},\n  \"sample_ledger\":\"{}\",\n  \"support_candidate_ledger\":\"{}\",\n  \"support_candidate_ledger_sha256\":\"{}\",\n  \"support_rule\":\"257 frozen distinct nonzero continuations balanced 7 each over bins 0..34 and 6 each over bins 35..36\",\n  \"packet_grouping_guard\":\"checkpoint retains collected canonical rows and coefficients but not packet labels; only the grouped six-ID scalar is source-faithful\",\n  \"sign_rule\":\"stored v is the direct coefficient in P; two normalized response flips give +v/(m1*m2)\",\n  \"terminality\":\"each K24 K4 child has active-anchor mass 0 and cannot pivot; full equals irreducible\",\n  \"elapsed_seconds\":{:.6},\n  \"projected_full_seconds\":{:.6},\n  \"scope\":\"strict grouped six-ID K24 R4-4 charge-only sink; no individual reconstruction, other sink, rows/columns, or membership claim\"\n}}\n",status,first,finald,U,ids,begin,begin+count,N,distributed,q.rows,q.source,q.l1,q.pivotable,q.p1,q.first_children,q.pivmid,q.p2,q.terminal,q.terminal,q.terminal,q.charge,q.charge,hist(&q.hist),q.hits,q.misses,q.peak,support_hist(&q.nonzero_support_records),support_bins,support_outside,lines.len()-1,sp,CANDIDATES,CANDIDATES_SHA256,elapsed,projected);
        let tmp = format!("{}.tmp", output);
        std::fs::write(&tmp, &text).unwrap();
        rename(tmp, &output).unwrap();
        print!("{}", text)
    }
}
fn main() {
    fold::run()
}
