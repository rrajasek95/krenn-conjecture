//! Exact grouped terminal K2 evaluator for
//! D16:{224,233,242,323,332,422}|R:3-2.
//!
//! `checkpoint_direct_k16.bin` retains canonical literal rows and their
//! collected signed direct-P coefficients, but not the six packet labels.
//! Consequently this evaluator reports only the source-faithful six-ID group.
//! Every row and first pivot remains literal until the K3 child and its second
//! pivot are known; profile compression begins only at the terminal K2 call.
#![allow(dead_code)]

mod run {
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

    use std::collections::BTreeMap;
    use std::fs::{File, metadata, rename};
    use std::io::{BufReader, Read, Seek, SeekFrom};
    use std::sync::Mutex;

    const INPUT: &str = "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin";
    const DEFAULT_OUT: &str = "computations/unaudited-codex-orbit0-k21-direct-k16-32-2026-08-24/results_k21_direct_k16_32.json";
    const HEADER: u64 = 16;
    const RECORD: u64 = 32;
    const EXPECTED_RECORDS: u64 = 24_097_095;
    const CHUNK: u64 = 100_000;
    const U21: i128 = 400_591_699_200;
    const IDS: [&str; 6] = [
        "D16:224|R:3-2", "D16:233|R:3-2", "D16:242|R:3-2",
        "D16:323|R:3-2", "D16:332|R:3-2", "D16:422|R:3-2",
    ];

    #[derive(Clone, Copy, Debug, Eq, PartialEq)]
    struct Outcome {
        pivotable_k19: u64,
        p2_uses: u64,
        k21_children: u64,
        charge_per_source_coefficient_scaled: i128,
        m2_hist: [u8; 79],
    }

    impl Default for Outcome {
        fn default() -> Self {
            Self {
                pivotable_k19: 0,
                p2_uses: 0,
                k21_children: 0,
                charge_per_source_coefficient_scaled: 0,
                m2_hist: [0; 79],
            }
        }
    }

    #[derive(Default)]
    struct Sum {
        source_rows: u64,
        signed_source_coefficient: i128,
        l1_source_coefficient: i128,
        pivotable_k16_rows: u64,
        p1_uses: u64,
        k19_children: u64,
        pivotable_k19_children: u64,
        p2_uses: u64,
        k21_children: u64,
        charge: i128,
        terminal_hits: u64,
        terminal_misses: u64,
        peak_terminal_keys_per_chunk: usize,
        denominator_hist: BTreeMap<(u8, u8), u64>,
    }

    impl Sum {
        fn add(&mut self, x: Sum) {
            self.source_rows += x.source_rows;
            self.signed_source_coefficient += x.signed_source_coefficient;
            self.l1_source_coefficient += x.l1_source_coefficient;
            self.pivotable_k16_rows += x.pivotable_k16_rows;
            self.p1_uses += x.p1_uses;
            self.k19_children += x.k19_children;
            self.pivotable_k19_children += x.pivotable_k19_children;
            self.p2_uses += x.p2_uses;
            self.k21_children += x.k21_children;
            self.charge += x.charge;
            self.terminal_hits += x.terminal_hits;
            self.terminal_misses += x.terminal_misses;
            self.peak_terminal_keys_per_chunk = self
                .peak_terminal_keys_per_chunk
                .max(x.peak_terminal_keys_per_chunk);
            for (key, value) in x.denominator_hist {
                *self.denominator_hist.entry(key).or_default() += value;
            }
        }
    }

    fn outcome(
        row: &Row,
        p1: usize,
        m1: usize,
        e: &E,
        terminal: &mut HashMap<RKey, (i64, i64, u64, u64)>,
        hits: &mut u64,
        misses: &mut u64,
    ) -> Outcome {
        let mut out = Outcome::default();
        for t1 in &e.tails[p1][1] {
            let k19 = replace(row, &e.anchors[p1], t1);
            let s2 = sig(&k19, e);
            let ps2 = avail(s2, e);
            if ps2.is_empty() {
                continue;
            }
            out.pivotable_k19 += 1;
            let m2 = ps2.len();
            out.m2_hist[m2] += 1;
            assert_eq!(U21 % ((m1 * m2) as i128), 0);
            // The stored direct-K16 coefficient is in P.  Each normalized
            // response flips sign, hence two responses give +v/(m1*m2).
            let unit_weight = U21 / ((m1 * m2) as i128);
            for p2 in ps2 {
                out.p2_uses += 1;
                let key = RKey {
                    profile: profile(&k19, p2, e),
                    sig: s2,
                    pivot: p2 as u8,
                    degree: 2,
                };
                let z = if let Some(&z) = terminal.get(&key) {
                    *hits += 1;
                    z
                } else {
                    *misses += 1;
                    resp(&k19, s2, p2, 2, e, terminal)
                };
                let (full_q, irreducible_q, full_n, irreducible_n) = z;
                assert_eq!((full_n, irreducible_n), (12, 12));
                assert_eq!(full_q, irreducible_q);
                out.k21_children += full_n;
                out.charge_per_source_coefficient_scaled +=
                    unit_weight * (full_q as i128);
            }
        }
        assert_eq!(out.k21_children, 12 * out.p2_uses);
        out
    }

    fn hex(row: &Row) -> String {
        row.0.iter().map(|x| format!("{:02x}", x)).collect()
    }

    fn sample_ordinal(index: u64) -> Option<usize> {
        (0..257).find(|&j| j as u64 * (EXPECTED_RECORDS - 1) / 256 == index)
    }

    fn worker(
        e: Arc<E>,
        ranges: Vec<(u64, u64)>,
        samples: Arc<Mutex<Vec<String>>>,
    ) -> Sum {
        let file = File::open(INPUT).unwrap();
        let mut reader = BufReader::with_capacity(4 << 20, file);
        let mut sum = Sum::default();
        let mut terminal = HashMap::new();
        for (start, end) in ranges {
            reader.seek(SeekFrom::Start(HEADER + RECORD * start)).unwrap();
            if !terminal.is_empty() {
                sum.peak_terminal_keys_per_chunk =
                    sum.peak_terminal_keys_per_chunk.max(terminal.len());
                terminal.clear();
            }
            for index in start..end {
                if index != start && index % CHUNK == 0 {
                    sum.peak_terminal_keys_per_chunk =
                        sum.peak_terminal_keys_per_chunk.max(terminal.len());
                    terminal.clear();
                }
                let mut bytes = [0u8; 32];
                reader.read_exact(&mut bytes).unwrap();
                let mut rr = [0u8; 24];
                rr.copy_from_slice(&bytes[..24]);
                let row = Row(rr);
                assert!(row.0.windows(2).all(|w| w[0] <= w[1]));
                let coefficient = i64::from_le_bytes(bytes[24..32].try_into().unwrap()) as i128;
                assert_ne!(coefficient, 0);
                sum.source_rows += 1;
                sum.signed_source_coefficient += coefficient;
                sum.l1_source_coefficient += coefficient.abs();
                let ps1 = avail(sig(&row, &e), &e);
                if ps1.is_empty() {
                    continue;
                }
                sum.pivotable_k16_rows += 1;
                let m1 = ps1.len();
                sum.p1_uses += m1 as u64;
                sum.k19_children += 32 * (m1 as u64);
                let sample = sample_ordinal(index);
                for (p1_ordinal, p1) in ps1.into_iter().enumerate() {
                    let z = outcome(
                        &row, p1, m1, &e, &mut terminal,
                        &mut sum.terminal_hits, &mut sum.terminal_misses,
                    );
                    sum.pivotable_k19_children += z.pivotable_k19;
                    sum.p2_uses += z.p2_uses;
                    sum.k21_children += z.k21_children;
                    sum.charge += coefficient * z.charge_per_source_coefficient_scaled;
                    for (m2, &count) in z.m2_hist.iter().enumerate() {
                        if count != 0 {
                            *sum.denominator_hist.entry((m1 as u8, m2 as u8)).or_default() +=
                                count as u64;
                        }
                    }
                    if sample.is_some() && p1_ordinal == 0 {
                        samples.lock().unwrap().push(format!(
                            "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                            sample.unwrap(), index, hex(&row), coefficient, m1, p1,
                            z.pivotable_k19, z.p2_uses, z.k21_children,
                            z.charge_per_source_coefficient_scaled,
                        ));
                    }
                }
            }
        }
        sum.peak_terminal_keys_per_chunk =
            sum.peak_terminal_keys_per_chunk.max(terminal.len());
        sum
    }

    pub fn run_main() {
        let begun = Instant::now();
        let args: Vec<String> = std::env::args().collect();
        let mut limit = None;
        let mut distributed = None;
        let mut workers = 8usize;
        let mut output = DEFAULT_OUT.to_string();
        let mut i = 1;
        while i < args.len() {
            match args[i].as_str() {
                "--limit-records" => {
                    limit = Some(args[i + 1].parse::<u64>().unwrap());
                    i += 2;
                }
                "--distributed-records" => {
                    distributed = Some(args[i + 1].parse::<u64>().unwrap());
                    i += 2;
                }
                "--workers" => {
                    workers = args[i + 1].parse().unwrap();
                    i += 2;
                }
                "--output" => {
                    output = args[i + 1].clone();
                    i += 2;
                }
                _ => panic!("usage: evaluator [--limit-records N | --distributed-records N] [--workers N] [--output PATH]"),
            }
        }
        assert!((1..=8).contains(&workers));
        assert!(limit.is_none() || distributed.is_none());
        let mut header = [0u8; 16];
        File::open(INPUT).unwrap().read_exact(&mut header).unwrap();
        assert_eq!(&header[..8], b"K16DIR1\0");
        let declared = u64::from_le_bytes(header[8..16].try_into().unwrap());
        assert_eq!(declared, EXPECTED_RECORDS);
        assert_eq!(metadata(INPUT).unwrap().len(), HEADER + RECORD * declared);
        let consumed = distributed.or(limit).unwrap_or(declared).min(declared);
        let e = Arc::new(parse());
        let samples = Arc::new(Mutex::new(Vec::new()));
        let pieces = workers * 32;
        let mut ranges = vec![Vec::new(); workers];
        for piece in 0..pieces {
            let (start, end) = if distributed.is_some() {
                let width_start = consumed * (piece as u64) / (pieces as u64);
                let width_end = consumed * ((piece + 1) as u64) / (pieces as u64);
                let base = declared * (piece as u64) / (pieces as u64);
                (base, base + width_end - width_start)
            } else {
                (consumed * (piece as u64) / (pieces as u64),
                 consumed * ((piece + 1) as u64) / (pieces as u64))
            };
            if start < end {
                ranges[piece % workers].push((start, end));
            }
        }
        let mut jobs = Vec::new();
        for w in 0..workers {
            let ee = e.clone();
            let ss = samples.clone();
            let rr = std::mem::take(&mut ranges[w]);
            jobs.push(thread::spawn(move || worker(ee, rr, ss)));
        }
        let mut total = Sum::default();
        for job in jobs {
            total.add(job.join().unwrap());
        }
        if consumed == declared && distributed.is_none() {
            assert_eq!(total.source_rows, 24_097_095);
            assert_eq!(total.signed_source_coefficient, 1_464_625_152);
            assert_eq!(total.l1_source_coefficient, 13_978_655_136);
            assert_eq!(total.pivotable_k16_rows, 24_003_767);
            assert_eq!(total.p1_uses, 129_939_187);
            assert_eq!(total.k19_children, 4_158_053_984);
        }
        let elapsed = begun.elapsed().as_secs_f64();
        assert!(elapsed < 600.0, "hard 600-second runtime gate exceeded");
        let projected = elapsed * (declared as f64) / (consumed as f64);
        let mut sample_rows = samples.lock().unwrap().clone();
        sample_rows.sort_by_key(|line| line.split('\t').next().unwrap().parse::<usize>().unwrap());
        if consumed == declared && distributed.is_none() {
            assert_eq!(sample_rows.len(), 257);
        }
        let sample_path = format!("{}.samples.tsv", output);
        let mut lines = vec![
            "sample_ordinal\trecord_index\tK16_row\tcoefficient\tm1\tp1\tpivotable_K19_children\tp2_uses\tK21_children\tcharge_per_source_coefficient_scaled_U".to_string()
        ];
        lines.extend(sample_rows);
        let sample_tmp = format!("{}.tmp", sample_path);
        std::fs::write(&sample_tmp, format!("{}\n", lines.join("\n"))).unwrap();
        rename(sample_tmp, &sample_path).unwrap();
        let hist = total.denominator_hist.iter().map(|(&(m1, m2), &count)|
            format!("\"{}_{}\":{}", m1, m2, count)
        ).collect::<Vec<_>>().join(",");
        let ids = IDS.iter().map(|id| format!("\"{}\"", id)).collect::<Vec<_>>().join(",");
        let status = if consumed == declared && distributed.is_none() {
            "PASS_COMPLETE_GROUPED_SIX_D16_R_3_2_K21_CHARGE"
        } else {
            "PASS_BOUNDED_PREFIX_GROUPED_SIX_D16_R_3_2_K21_EVALUATOR"
        };
        let text = format!(concat!(
            "{{\n  \"status\":\"{}\",\n  \"scale_U\":\"{}\",\n",
            "  \"ids\":[{}],\n  \"covered_ids\":6,\n  \"individual_id_charges\":null,\n",
            "  \"packet_grouping_guard\":\"checkpoint retains collected canonical rows and coefficients but not packet labels; only the grouped six-ID scalar is source-faithful\",\n",
            "  \"input\":\"{}\",\n  \"records_consumed\":{},\n  \"records_declared\":{},\n  \"workers\":{},\n",
            "  \"prefix_selection\":\"{}\",\n",
            "  \"source_rows\":{},\n  \"signed_source_coefficient\":\"{}\",\n  \"l1_source_coefficient\":\"{}\",\n",
            "  \"pivotable_K16_rows\":{},\n  \"selected_p1_uses\":{},\n  \"K19_child_occurrences\":{},\n",
            "  \"pivotable_K19_child_occurrences\":{},\n  \"selected_p2_uses\":{},\n",
            "  \"K21_terminal_occurrences\":{},\n  \"full_occurrences\":{},\n  \"irreducible_occurrences\":{},\n",
            "  \"full_charge_scaled_U\":\"{}\",\n  \"irreducible_charge_scaled_U\":\"{}\",\n",
            "  \"all_K21_children_irreducible\":true,\n",
            "  \"terminal_profile_cache\":{{\"hits\":{},\"misses\":{},\"peak_keys_per_100k_chunk\":{}}},\n",
            "  \"m1_m2_occurrence_hist\":{{{}}},\n  \"literal_provenance_ledger\":\"{}\",\n",
            "  \"compression_proof\":\"literal K16 row and p1 are expanded through every K3 tail before p2; only the terminal K2 response is cached by (profile,literal signature,p2,degree), after the last pivot decision\",\n",
            "  \"sign_rule\":\"stored v is the direct coefficient in P; two normalized response sign flips give +v/(m1*m2)\",\n",
            "  \"scope\":\"exactly the grouped six requested K21 IDs; no individual reconstruction, other K21 ID, row checkpoint, or membership inference\",\n",
            "  \"elapsed_seconds\":{:.6},\n  \"projected_full_seconds_from_prefix\":{:.6}\n}}\n"
        ), status, U21, ids, INPUT, consumed, declared, workers,
            if distributed.is_some() { "eight evenly spaced contiguous slices" } else { "leading contiguous prefix or full stream" },
            total.source_rows, total.signed_source_coefficient, total.l1_source_coefficient,
            total.pivotable_k16_rows, total.p1_uses, total.k19_children,
            total.pivotable_k19_children, total.p2_uses, total.k21_children,
            total.k21_children, total.k21_children, total.charge, total.charge,
            total.terminal_hits, total.terminal_misses,
            total.peak_terminal_keys_per_chunk, hist, sample_path, elapsed, projected);
        let tmp = format!("{}.tmp", output);
        std::fs::write(&tmp, &text).unwrap();
        rename(tmp, output).unwrap();
        print!("{}", text);
    }
}

fn main() {
    run::run_main();
}
