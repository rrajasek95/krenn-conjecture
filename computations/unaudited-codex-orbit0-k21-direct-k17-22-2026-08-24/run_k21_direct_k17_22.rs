//! Exact occurrencewise terminal K2 evaluator for the seven direct-K17
//! lineages D17:{234,243,324,333,342,423,432}|R:2-2.
//!
//! The source is replayed from the frozen filtered-K16 structure.  Within
//! each signed R8prime orbit record, identical literal `(K17 row,p1)` pairs
//! are memoized.  This is an exact compression: the complete sorted row and
//! selected first pivot determine every literal K2 child, its second pivot
//! set, every terminal K2 child, and the 77-cycle value.  No profile-only K19
//! checkpoint is used and exact-zero source contributions are not discarded.
#![allow(dead_code)]

mod run {
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

    use std::collections::BTreeMap;
    use std::fs::rename;
    use std::sync::Mutex;

    const U21: i128 = 400_591_699_200;
    const IDS: [&str; 7] = [
        "D17:234|R:2-2",
        "D17:243|R:2-2",
        "D17:324|R:2-2",
        "D17:333|R:2-2",
        "D17:342|R:2-2",
        "D17:423|R:2-2",
        "D17:432|R:2-2",
    ];

    #[derive(Clone, Copy, Eq, Hash, PartialEq)]
    struct LiteralFirstKey {
        row: Row,
        p1: u8,
    }

    #[derive(Clone, Copy, Debug, Eq, PartialEq)]
    struct Outcome {
        pivotable_k19: u64,
        p2_uses: u64,
        k21_children: u64,
        charge_per_source_mass_scaled: i128,
        m2_hist: [u8; 79],
    }

    impl Default for Outcome {
        fn default() -> Self {
            Self {
                pivotable_k19: 0,
                p2_uses: 0,
                k21_children: 0,
                charge_per_source_mass_scaled: 0,
                m2_hist: [0; 79],
            }
        }
    }

    #[derive(Clone, Copy, Debug, Default)]
    struct SectorStat {
        raw_heads: u64,
        pivotable_k17: u64,
        p1_uses: u64,
        k19_children: u64,
        pivotable_k19: u64,
        p2_uses: u64,
        k21_children: u64,
        charge: i128,
    }

    impl SectorStat {
        fn add(&mut self, x: SectorStat) {
            self.raw_heads += x.raw_heads;
            self.pivotable_k17 += x.pivotable_k17;
            self.p1_uses += x.p1_uses;
            self.k19_children += x.k19_children;
            self.pivotable_k19 += x.pivotable_k19;
            self.p2_uses += x.p2_uses;
            self.k21_children += x.k21_children;
            self.charge += x.charge;
        }
    }

    #[derive(Default)]
    struct WorkerResult {
        sectors: [SectorStat; 7],
        denominator_hist: BTreeMap<(u8, u8), u64>,
        literal_first_lookups: u64,
        literal_first_misses: u64,
        peak_literal_first_keys_per_r8: usize,
        terminal_profile_hits: u64,
        terminal_profile_misses: u64,
    }

    fn outcome(
        row: &Row,
        p1: usize,
        m1: usize,
        e: &E,
        terminal: &mut HashMap<RKey, (i64, i64, u64, u64)>,
        terminal_hits: &mut u64,
        terminal_misses: &mut u64,
    ) -> Outcome {
        let mut out = Outcome::default();
        for t1 in &e.tails[p1][0] {
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
            let unit_weight = -U21 / ((m1 * m2) as i128);
            for p2 in ps2 {
                out.p2_uses += 1;
                let key = RKey {
                    profile: profile(&k19, p2, e),
                    sig: s2,
                    pivot: p2 as u8,
                    degree: 2,
                };
                let z = if let Some(&z) = terminal.get(&key) {
                    *terminal_hits += 1;
                    z
                } else {
                    *terminal_misses += 1;
                    let z = resp(&k19, s2, p2, 2, e, terminal);
                    z
                };
                let (full_q, irreducible_q, full_n, irreducible_n) = z;
                assert_eq!((full_n, irreducible_n), (12, 12));
                assert_eq!(full_q, irreducible_q);
                // `resp` literally checks pivotability of each K21 child when
                // forming its irreducible subtotal, so equality of counts is
                // the terminal-page assertion, not a DAG-only assignment.
                out.k21_children += full_n;
                out.charge_per_source_mass_scaled +=
                    unit_weight * (full_q as i128);
            }
        }
        assert_eq!(out.k21_children, 12 * out.p2_uses);
        out
    }

    fn hex(bytes: &[u8]) -> String {
        bytes.iter().map(|x| format!("{:02x}", x)).collect()
    }

    #[allow(clippy::too_many_arguments)]
    fn emit(
        row: Row,
        sector: usize,
        source_mass: i128,
        r8_index: usize,
        factors: [&[u8; 4]; 3],
        e: &E,
        first: &mut HashMap<LiteralFirstKey, Outcome>,
        terminal: &mut HashMap<RKey, (i64, i64, u64, u64)>,
        wr: &mut WorkerResult,
        samples: &Mutex<Vec<String>>,
        sample_this_r8: bool,
        sampled_this_r8: &mut bool,
    ) {
        let st = &mut wr.sectors[sector];
        st.raw_heads += 1;
        let s1 = sig(&row, e);
        let ps1 = avail(s1, e);
        if ps1.is_empty() {
            return;
        }
        st.pivotable_k17 += 1;
        let m1 = ps1.len();
        st.p1_uses += m1 as u64;
        st.k19_children += 12 * (m1 as u64);
        for p1 in ps1 {
            wr.literal_first_lookups += 1;
            let key = LiteralFirstKey { row, p1: p1 as u8 };
            let z = if let Some(&z) = first.get(&key) {
                z
            } else {
                wr.literal_first_misses += 1;
                let z = outcome(
                    &row,
                    p1,
                    m1,
                    e,
                    terminal,
                    &mut wr.terminal_profile_hits,
                    &mut wr.terminal_profile_misses,
                );
                first.insert(key, z);
                z
            };
            st.pivotable_k19 += z.pivotable_k19;
            st.p2_uses += z.p2_uses;
            st.k21_children += z.k21_children;
            st.charge += source_mass * z.charge_per_source_mass_scaled;
            for (m2, &n) in z.m2_hist.iter().enumerate() {
                if n != 0 {
                    *wr.denominator_hist.entry((m1 as u8, m2 as u8)).or_default() += n as u64;
                }
            }
            if sample_this_r8 && !*sampled_this_r8 {
                let mut ledger = samples.lock().unwrap();
                ledger.push(format!(
                    "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                    IDS[sector], r8_index, hex(&row.0), hex(factors[0]),
                    hex(factors[1]), hex(factors[2]), source_mass, m1, p1,
                    z.pivotable_k19, z.p2_uses, z.k21_children,
                    z.charge_per_source_mass_scaled,
                ));
                *sampled_this_r8 = true;
            }
        }
    }

    fn worker(
        e: Arc<E>,
        start: usize,
        end: usize,
        worker_index: usize,
        workers: usize,
        samples: Arc<Mutex<Vec<String>>>,
    ) -> WorkerResult {
        let mut wr = WorkerResult::default();
        for ri in (start + worker_index..end).step_by(workers) {
            let r = &e.records[ri];
            let mass = (r.size as i128) * (r.coefficient as i128);
            let mut first = HashMap::new();
            // Both caches are intentionally record-bounded.  This makes the
            // peak-memory bound independent of the 485-record full replay.
            let mut terminal = HashMap::new();
            let sample_this_r8 = (0..257).any(|j| j * (e.records.len() - 1) / 256 == ri);
            let mut sampled_this_r8 = false;
            // The six literal permutations of 2+3+4.  The sector index is
            // the lexicographic IDS position, fixed explicitly below.
            let specs = [
                (0usize, 0usize, 1usize, 2usize), // 234
                (1, 0, 2, 1),                    // 243
                (2, 1, 0, 2),                    // 324
                (4, 1, 2, 0),                    // 342
                (5, 2, 0, 1),                    // 423
                (6, 2, 1, 0),                    // 432
            ];
            for &(sector, d2, d3, d4) in &specs {
                for a in &e.factor[d2][0] {
                    for b in &e.factor[d3][1] {
                        for c in &e.factor[d4][2] {
                            let mut f: [Option<&[u8; 4]>; 3] = [None, None, None];
                            f[d2] = Some(a);
                            f[d3] = Some(b);
                            f[d4] = Some(c);
                            let q = [f[0].unwrap(), f[1].unwrap(), f[2].unwrap()];
                            emit(
                                make(r, q[0], q[1], q[2]), sector, mass, ri, q,
                                &e, &mut first, &mut terminal, &mut wr, &samples,
                                sample_this_r8, &mut sampled_this_r8,
                            );
                        }
                    }
                }
            }
            // The symmetric 3+3+3 sector occupies the fourth ID slot.
            for a in &e.factor[0][1] {
                for b in &e.factor[1][1] {
                    for c in &e.factor[2][1] {
                        emit(
                            make(r, a, b, c), 3, mass, ri, [a, b, c], &e,
                            &mut first, &mut terminal, &mut wr, &samples,
                            sample_this_r8, &mut sampled_this_r8,
                        );
                    }
                }
            }
            wr.peak_literal_first_keys_per_r8 =
                wr.peak_literal_first_keys_per_r8.max(first.len());
        }
        wr
    }

    pub fn run_main() {
        let begun = Instant::now();
        let args: Vec<String> = std::env::args().collect();
        let mut limit = None;
        let mut workers = 8usize;
        let mut output = "computations/unaudited-codex-orbit0-k21-direct-k17-22-2026-08-24/results_k21_direct_k17_22.json".to_string();
        let mut i = 1;
        while i < args.len() {
            match args[i].as_str() {
                "--limit-records" => {
                    limit = Some(args[i + 1].parse::<usize>().unwrap());
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
                _ => panic!("usage: evaluator [--limit-records N] [--workers N] [--output PATH]"),
            }
        }
        assert!((1..=8).contains(&workers));
        let e = Arc::new(parse());
        let declared = e.records.len();
        assert_eq!(declared, 485);
        let consumed = limit.unwrap_or(declared).min(declared);
        let samples = Arc::new(Mutex::new(Vec::new()));
        let mut jobs = Vec::new();
        for t in 0..workers {
            let ee = e.clone();
            let ss = samples.clone();
            jobs.push(thread::spawn(move || worker(ee, 0, consumed, t, workers, ss)));
        }
        let mut total = WorkerResult::default();
        for job in jobs {
            let x = job.join().unwrap();
            for j in 0..7 {
                total.sectors[j].add(x.sectors[j]);
            }
            for (k, v) in x.denominator_hist {
                *total.denominator_hist.entry(k).or_default() += v;
            }
            total.literal_first_lookups += x.literal_first_lookups;
            total.literal_first_misses += x.literal_first_misses;
            total.peak_literal_first_keys_per_r8 = total
                .peak_literal_first_keys_per_r8
                .max(x.peak_literal_first_keys_per_r8);
            total.terminal_profile_hits += x.terminal_profile_hits;
            total.terminal_profile_misses += x.terminal_profile_misses;
        }
        if consumed == declared {
            let expected = [
                11_174_400, 11_174_400, 11_174_400, 15_892_480,
                11_174_400, 11_174_400, 11_174_400,
            ];
            for j in 0..7 {
                assert_eq!(total.sectors[j].raw_heads, expected[j]);
            }
            assert_eq!(total.sectors.iter().map(|x| x.raw_heads).sum::<u64>(), 82_938_880);
            assert_eq!(total.sectors.iter().map(|x| x.pivotable_k17).sum::<u64>(), 81_076_480);
            assert_eq!(total.sectors.iter().map(|x| x.p1_uses).sum::<u64>(), 267_564_800);
            assert_eq!(total.sectors.iter().map(|x| x.k19_children).sum::<u64>(), 3_210_777_600);
        }
        let rows = (0..7).map(|j| {
            let z = total.sectors[j];
            format!(concat!(
                "    {{\"id\":\"{}\",\"raw_K17_heads\":{},",
                "\"pivotable_K17_heads\":{},\"selected_p1_uses\":{},",
                "\"K19_child_occurrences\":{},\"pivotable_K19_child_occurrences\":{},",
                "\"selected_p2_uses\":{},\"K21_terminal_occurrences\":{},",
                "\"full_occurrences\":{},\"irreducible_occurrences\":{},",
                "\"full_charge_scaled_U\":\"{}\",\"irreducible_charge_scaled_U\":\"{}\"}}"
            ), IDS[j], z.raw_heads, z.pivotable_k17, z.p1_uses,
                z.k19_children, z.pivotable_k19, z.p2_uses, z.k21_children,
                z.k21_children, z.k21_children, z.charge, z.charge)
        }).collect::<Vec<_>>().join(",\n");
        let hist = total.denominator_hist.iter().map(|(&(m1, m2), &n)|
            format!("\"{}_{}\":{}", m1, m2, n)
        ).collect::<Vec<_>>().join(",");
        let elapsed = begun.elapsed().as_secs_f64();
        assert!(elapsed < 600.0, "hard 600-second full/prefix runtime gate exceeded");
        let projected = elapsed * (declared as f64) / (consumed as f64);
        let status = if consumed == declared {
            "PASS_COMPLETE_SEVEN_D17_R_2_2_K21_CHARGE"
        } else {
            "PASS_BOUNDED_PREFIX_SEVEN_D17_R_2_2_K21_EVALUATOR"
        };
        let sample_path = format!("{}.samples.tsv", output);
        let mut sample_lines = vec![
            "id\tr8_index\tK17_row\tfactor0\tfactor1\tfactor2\tsource_mass\tm1\tp1\tpivotable_K19_children\tp2_uses\tK21_children\tcharge_per_source_mass_scaled_U".to_string()
        ];
        let mut distributed_samples = samples.lock().unwrap().clone();
        distributed_samples.sort();
        if consumed == declared {
            assert_eq!(distributed_samples.len(), 257);
        }
        sample_lines.extend(distributed_samples);
        let sample_tmp = format!("{}.tmp", sample_path);
        std::fs::write(&sample_tmp, format!("{}\n", sample_lines.join("\n"))).unwrap();
        rename(&sample_tmp, &sample_path).unwrap();
        let text = format!(concat!(
            "{{\n  \"status\":\"{}\",\n  \"scale_U\":\"{}\",\n",
            "  \"records_consumed\":{},\n  \"records_declared\":{},\n  \"workers\":{},\n",
            "  \"ids\":[\n{}\n  ],\n  \"covered_ids\":7,\n",
            "  \"all_K21_children_irreducible\":true,\n",
            "  \"literal_first_compression\":{{\"lookups\":{},\"misses\":{},",
            "\"hits\":{},\"peak_keys_per_R8_record\":{},",
            "\"proof\":\"key=(complete sorted literal K17 row,p1); equal keys generate identical literal first tails, second pivot sets, terminal tails, and 77 charges; source masses therefore combine by exact linearity\"}},\n",
            "  \"terminal_profile_cache\":{{\"hits\":{},\"misses\":{}}},\n",
            "  \"m1_m2_occurrence_hist\":{{{}}},\n",
            "  \"literal_provenance_ledger\":\"{}\",\n",
            "  \"sign_rule\":\"direct P coefficient=-M; first normalized response=+M/m1; second normalized response=-M/(m1*m2)\",\n",
            "  \"source\":\"authoritative filtered_k16_structure.bin replay of the seven explicit direct-K17 factor sectors only\",\n",
            "  \"scope\":\"exactly seven requested K21 lineage IDs; no other K21 ID or membership inference\",\n",
            "  \"elapsed_seconds\":{:.6},\n  \"projected_full_seconds_from_prefix\":{:.6}\n}}\n"
        ), status, U21, consumed, declared, workers, rows,
            total.literal_first_lookups, total.literal_first_misses,
            total.literal_first_lookups - total.literal_first_misses,
            total.peak_literal_first_keys_per_r8,
            total.terminal_profile_hits, total.terminal_profile_misses,
            hist, sample_path, elapsed, projected);
        let tmp = format!("{}.tmp", output);
        std::fs::write(&tmp, &text).unwrap();
        rename(tmp, output).unwrap();
        print!("{}", text);
    }
}

fn main() {
    run::run_main();
}
