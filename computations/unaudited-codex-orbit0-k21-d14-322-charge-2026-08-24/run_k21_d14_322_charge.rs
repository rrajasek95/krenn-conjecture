//! Exact source-linear scalar fold for singleton D14:222|R:3-2-2.
#![allow(dead_code)]

mod run {
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

    use std::collections::BTreeMap;
    use std::fs::rename;

    const U21: i128 = 400_591_699_200;
    const DECLARED_R8: usize = 485;
    const HEADS_PER_R8: usize = 12 * 12 * 12;
    const DECLARED_HEADS: usize = DECLARED_R8 * HEADS_PER_R8;
    const DEFAULT_OUT: &str = "computations/unaudited-codex-orbit0-k21-d14-322-charge-2026-08-24/results_k21_d14_322_charge.json";

    #[derive(Clone, Copy, Default)]
    struct Terminal {
        n: u64,
        q: i64,
    }

    #[derive(Clone)]
    struct Witness {
        p1: usize,
        t3: usize,
        p2: usize,
        t2: usize,
        p3: usize,
        m1: usize,
        m2: usize,
        m3: usize,
        row17: Row,
        row19: Row,
        terminal_q: i64,
    }

    #[derive(Default)]
    struct HeadStat {
        p1: u64,
        k17: u64,
        pivotable_k17: u64,
        p2: u64,
        k19: u64,
        pivotable_k19: u64,
        p3: u64,
        k21: u64,
        charge: i128,
        witness: Option<Witness>,
    }

    #[derive(Default)]
    struct Sum {
        heads: u64,
        source_mass: i128,
        source_mass_l1: i128,
        p1: u64,
        k17: u64,
        pivotable_k17: u64,
        p2: u64,
        k19: u64,
        pivotable_k19: u64,
        p3: u64,
        k21: u64,
        charge: i128,
        plan2_hits: u64,
        plan2_misses: u64,
        plan3_hits: u64,
        plan3_misses: u64,
        terminal_hits: u64,
        terminal_misses: u64,
        literal_row19_hits: u64,
        literal_row19_misses: u64,
        peak_terminal_keys_per_r8: usize,
        h1: BTreeMap<u8, u64>,
        h2: BTreeMap<u8, u64>,
        h3: BTreeMap<u8, u64>,
        hp: BTreeMap<u16, u64>,
        samples: BTreeMap<usize, (usize, String)>,
    }

    impl Sum {
        fn add(&mut self, x: Sum) {
            self.heads += x.heads;
            self.source_mass += x.source_mass;
            self.source_mass_l1 += x.source_mass_l1;
            self.p1 += x.p1;
            self.k17 += x.k17;
            self.pivotable_k17 += x.pivotable_k17;
            self.p2 += x.p2;
            self.k19 += x.k19;
            self.pivotable_k19 += x.pivotable_k19;
            self.p3 += x.p3;
            self.k21 += x.k21;
            self.charge += x.charge;
            self.plan2_hits += x.plan2_hits;
            self.plan2_misses += x.plan2_misses;
            self.plan3_hits += x.plan3_hits;
            self.plan3_misses += x.plan3_misses;
            self.terminal_hits += x.terminal_hits;
            self.terminal_misses += x.terminal_misses;
            self.literal_row19_hits += x.literal_row19_hits;
            self.literal_row19_misses += x.literal_row19_misses;
            self.peak_terminal_keys_per_r8 = self
                .peak_terminal_keys_per_r8.max(x.peak_terminal_keys_per_r8);
            for (key, value) in x.h1 { *self.h1.entry(key).or_default() += value; }
            for (key, value) in x.h2 { *self.h2.entry(key).or_default() += value; }
            for (key, value) in x.h3 { *self.h3.entry(key).or_default() += value; }
            for (key, value) in x.hp { *self.hp.entry(key).or_default() += value; }
            for (bin, candidate) in x.samples {
                let entry = self.samples.entry(bin).or_insert_with(|| candidate.clone());
                if candidate.0 < entry.0 { *entry = candidate; }
            }
        }
    }

    fn plan2(
        s14: [u8; 12],
        p1: usize,
        e: &E,
    ) -> Vec<(usize, [u8; 12], Vec<usize>)> {
        let mut out = Vec::new();
        for (t3, tail) in e.tails[p1][1].iter().enumerate() {
            let s17 = child_sig(s14, p1, tail, e);
            let ps2 = avail(s17, e);
            if !ps2.is_empty() { out.push((t3, s17, ps2)); }
        }
        out
    }

    fn plan3(
        s17: [u8; 12],
        p2: usize,
        e: &E,
    ) -> Vec<(usize, [u8; 12], Vec<usize>)> {
        let mut out = Vec::new();
        for (t2, tail) in e.tails[p2][0].iter().enumerate() {
            let s19 = child_sig(s17, p2, tail, e);
            let ps3 = avail(s19, e);
            if !ps3.is_empty() { out.push((t2, s19, ps3)); }
        }
        out
    }

    // Close the eight boundary endpoints encoded by `profile` with a literal
    // K2 tail.  This is the same cycle key as constructing the 24-cell child,
    // but costs only an eight-vertex traversal; distributed samples replay the
    // literal construction independently.
    fn abstract_ckey(prof: &[u8; 29], p: usize, tail: &[u8; 4], e: &E) -> CKey {
        let mut endpoint = [-1i8; 24];
        for (i, &cell) in e.anchors[p].iter().enumerate() {
            let [u, v, a, b] = e.cells[cell as usize];
            endpoint[(3 * u + a) as usize] = (2 * i) as i8;
            endpoint[(3 * v + b) as usize] = (2 * i + 1) as i8;
        }
        let mut closure = [255u8; 8];
        for &cell in tail {
            let [u, v, a, b] = e.cells[cell as usize];
            let x = endpoint[(3 * u + a) as usize];
            let y = endpoint[(3 * v + b) as usize];
            assert!(x >= 0 && y >= 0);
            closure[x as usize] = y as u8;
            closure[y as usize] = x as u8;
        }
        assert!(closure.iter().all(|&x| x != 255));
        let mut seen = [false; 8];
        let mut parts = [0u8; 12];
        let mut n = 0;
        for start in 0..8 {
            if seen[start] { continue; }
            let mut stack = [0u8; 8];
            let (mut top, mut nodes, mut pathsum) = (1usize, 0u8, 0u16);
            stack[0] = start as u8;
            seen[start] = true;
            while top > 0 {
                top -= 1;
                let x = stack[top] as usize;
                nodes += 1;
                pathsum += prof[8 + x] as u16;
                for y in [prof[x], closure[x]] {
                    if !seen[y as usize] {
                        seen[y as usize] = true;
                        stack[top] = y;
                        top += 1;
                    }
                }
            }
            parts[n] = (pathsum / 2 + (nodes as u16) / 2) as u8;
            n += 1;
        }
        let closed = prof[16] as usize;
        for &x in &prof[17..17 + closed] { parts[n] = x; n += 1; }
        parts[..n].sort_unstable();
        let mut key = [0u8; 13];
        key[0] = n as u8;
        key[1..1 + n].copy_from_slice(&parts[..n]);
        CKey(key)
    }

    fn terminal_response(
        row19: &Row,
        s19: [u8; 12],
        p3: usize,
        e: &E,
        cache: &mut HashMap<RKey, (i64, i64, u64, u64)>,
        hits: &mut u64,
        misses: &mut u64,
    ) -> Terminal {
        let key = RKey {
            profile: profile(row19, p3, e),
            sig: s19,
            pivot: p3 as u8,
            degree: 2,
        };
        let z = if let Some(&z) = cache.get(&key) {
            *hits += 1;
            z
        } else {
            *misses += 1;
            let mut q = 0i64;
            let mut n = 0u64;
            for tail in &e.tails[p3][0] {
                assert!(avail(child_sig(s19, p3, tail, e), e).is_empty());
                let ck = abstract_ckey(&key.profile, p3, tail, e);
                q += *e.dual.get(&ck).unwrap_or(&0);
                n += 1;
            }
            let value = (q, q, n, n);
            cache.insert(key, value);
            value
        };
        let (full_q, irreducible_q, full_n, irreducible_n) = z;
        assert_eq!((full_n, irreducible_n), (12, 12));
        assert_eq!(full_q, irreducible_q);
        Terminal { n: full_n, q: full_q }
    }

    #[allow(clippy::too_many_arguments)]
    fn fold_head(
        row14: Row,
        mass: i128,
        e: &E,
        plans2: &mut HashMap<([u8; 12], u8), Vec<(usize, [u8; 12], Vec<usize>)>>,
        plans3: &mut HashMap<([u8; 12], u8), Vec<(usize, [u8; 12], Vec<usize>)>>,
        terminal: &mut HashMap<RKey, (i64, i64, u64, u64)>,
        row19_cache: &mut HashMap<Row, (usize, u64, i64, usize, i64)>,
        total: &mut Sum,
    ) -> HeadStat {
        let mut head = HeadStat::default();
        let s14 = sig(&row14, e);
        // A D14 row has ten active-colour incidences.  The R3/R2/R2
        // substitutions change this to 7, 5, and finally 3 respectively.
        assert_eq!(s14.iter().map(|&x| x as usize).sum::<usize>(), 10);
        let ps1 = valid(s14, e);
        let m1 = ps1.len();
        assert!(m1 > 0);
        assert_eq!(U21 % (m1 as i128), 0);
        *total.h1.entry(m1 as u8).or_default() += 1;
        for p1 in ps1 {
            head.p1 += 1;
            head.k17 += 32;
            let key2 = (s14, p1 as u8);
            if plans2.contains_key(&key2) {
                total.plan2_hits += 1;
            } else {
                total.plan2_misses += 1;
                let plan = plan2(s14, p1, e);
                plans2.insert(key2, plan);
            }
            let pp2 = plans2.get(&key2).unwrap();
            for &(t3, s17, ref ps2) in pp2 {
                head.pivotable_k17 += 1;
                let m2 = ps2.len();
                assert_eq!(U21 % ((m1 * m2) as i128), 0);
                *total.h2.entry(m2 as u8).or_default() += 1;
                let row17 = replace(&row14, &e.anchors[p1], &e.tails[p1][1][t3]);
                assert_eq!(sig(&row17, e), s17);
                for &p2 in ps2 {
                    head.p2 += 1;
                    head.k19 += 12;
                    let key3 = (s17, p2 as u8);
                    if plans3.contains_key(&key3) {
                        total.plan3_hits += 1;
                    } else {
                        total.plan3_misses += 1;
                        let plan = plan3(s17, p2, e);
                        plans3.insert(key3, plan);
                    }
                    let pp3 = plans3.get(&key3).unwrap();
                    for &(t2, s19, ref ps3) in pp3 {
                        head.pivotable_k19 += 1;
                        let m3 = ps3.len();
                        let product = m1 * m2 * m3;
                        assert_eq!(U21 % (product as i128), 0);
                        *total.h3.entry(m3 as u8).or_default() += 1;
                        *total.hp.entry(product as u16).or_default() += 1;
                        let row19 = replace(&row17, &e.anchors[p2], &e.tails[p2][0][t2]);
                        assert_eq!(sig(&row19, e), s19);
                        let unit = mass * U21 / (product as i128);
                        let (cached_m3, terminal_n, terminal_q, first_p3, first_q) =
                            if let Some(&z) = row19_cache.get(&row19) {
                                total.literal_row19_hits += 1;
                                z
                            } else {
                                total.literal_row19_misses += 1;
                                let mut n = 0;
                                let mut q = 0i64;
                                let mut first = None;
                                for &p3 in ps3 {
                                    let response = terminal_response(
                                        &row19, s19, p3, e, terminal,
                                        &mut total.terminal_hits, &mut total.terminal_misses,
                                    );
                                    n += response.n;
                                    q += response.q;
                                    if first.is_none() { first = Some((p3, response.q)); }
                                }
                                let (fp, fq) = first.unwrap();
                                let z = (m3, n, q, fp, fq);
                                row19_cache.insert(row19, z);
                                z
                            };
                        assert_eq!(cached_m3, m3);
                        head.p3 += m3 as u64;
                        head.k21 += terminal_n;
                        head.charge += unit * (terminal_q as i128);
                        if head.witness.is_none() {
                            head.witness = Some(Witness {
                                p1, t3, p2, t2, p3: first_p3, m1, m2, m3,
                                row17, row19, terminal_q: first_q,
                            });
                        }
                    }
                }
            }
        }
        assert_eq!(head.k17, 32 * head.p1);
        assert_eq!(head.k19, 12 * head.p2);
        assert_eq!(head.k21, 12 * head.p3);
        head
    }

    fn hex(row: &Row) -> String {
        row.0.iter().map(|x| format!("{:02x}", x)).collect()
    }

    fn worker(e: Arc<E>, ranges: Vec<(usize, usize)>) -> Sum {
        let mut total = Sum::default();
        let mut plans2 = HashMap::new();
        let mut plans3 = HashMap::new();
        // RKey is a complete response invariant, so this cache is exact across
        // R8 slices as well as within one slice.  Keeping it worker-local avoids
        // synchronization and bounds its lifetime to one evaluator invocation.
        let mut terminal = HashMap::new();
        let mut row19_cache = HashMap::new();
        for (start, end) in ranges {
            for ri in start..end {
                let r = &e.records[ri];
                let mass = (r.size as i128) * (r.coefficient as i128);
                for (a_index, a) in e.factor[0][0].iter().enumerate() {
                    for (b_index, b) in e.factor[1][0].iter().enumerate() {
                        for (c_index, c) in e.factor[2][0].iter().enumerate() {
                            let head_index = ri * HEADS_PER_R8 +
                                (a_index * 12 + b_index) * 12 + c_index;
                            let row14 = make(r, a, b, c);
                            total.heads += 1;
                            total.source_mass += mass;
                            total.source_mass_l1 += mass.abs();
                            row19_cache.clear();
                            let z = fold_head(
                                row14, mass, &e, &mut plans2, &mut plans3,
                                &mut terminal, &mut row19_cache, &mut total,
                            );
                            total.p1 += z.p1;
                            total.k17 += z.k17;
                            total.pivotable_k17 += z.pivotable_k17;
                            total.p2 += z.p2;
                            total.k19 += z.k19;
                            total.pivotable_k19 += z.pivotable_k19;
                            total.p3 += z.p3;
                            total.k21 += z.k21;
                            total.charge += z.charge;
                            if z.p3 > 0 && z.charge != 0 {
                                let bin = head_index * 257 / DECLARED_HEADS;
                                let witness = z.witness.unwrap();
                                let line = format!(
                                    "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                                    bin, head_index, ri, hex(&row14), mass,
                                    z.p1, z.k17, z.pivotable_k17, z.p2, z.k19,
                                    z.pivotable_k19, z.p3, z.k21, z.charge,
                                    witness.p1, witness.t3, witness.p2, witness.t2,
                                    witness.p3, witness.m1, witness.m2, witness.m3,
                                    witness.terminal_q,
                                    hex(&witness.row17), hex(&witness.row19),
                                );
                                total.samples.entry(bin).or_insert((head_index, line));
                            }
                        }
                    }
                }
                total.peak_terminal_keys_per_r8 =
                    total.peak_terminal_keys_per_r8.max(terminal.len());
            }
        }
        total
    }

    fn histogram<T: std::fmt::Display + Ord>(map: &BTreeMap<T, u64>) -> String {
        map.iter().map(|(key, value)| format!("\"{}\":{}", key, value))
            .collect::<Vec<_>>().join(",")
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
                "--limit-records" => { limit = Some(args[i + 1].parse::<usize>().unwrap()); i += 2; }
                "--distributed-records" => { distributed = Some(args[i + 1].parse::<usize>().unwrap()); i += 2; }
                "--workers" => { workers = args[i + 1].parse().unwrap(); i += 2; }
                "--output" => { output = args[i + 1].clone(); i += 2; }
                _ => panic!("usage: evaluator [--limit-records N | --distributed-records N] [--workers N] [--output PATH]"),
            }
        }
        assert!(limit.is_none() || distributed.is_none());
        assert!((1..=8).contains(&workers));
        let consumed = distributed.or(limit).unwrap_or(DECLARED_R8).min(DECLARED_R8);
        let e = Arc::new(parse());
        assert_eq!(e.records.len(), DECLARED_R8);
        let pieces = workers * 8;
        let mut ranges = vec![Vec::new(); workers];
        for piece in 0..pieces {
            let (start, end) = if distributed.is_some() {
                let width_start = consumed * piece / pieces;
                let width_end = consumed * (piece + 1) / pieces;
                let base = DECLARED_R8 * piece / pieces;
                (base, (base + width_end - width_start).min(DECLARED_R8))
            } else {
                (consumed * piece / pieces, consumed * (piece + 1) / pieces)
            };
            if start < end { ranges[piece % workers].push((start, end)); }
        }
        let mut jobs = Vec::new();
        for w in 0..workers {
            let ee = e.clone();
            let rr = std::mem::take(&mut ranges[w]);
            jobs.push(thread::spawn(move || worker(ee, rr)));
        }
        let mut total = Sum::default();
        for job in jobs { total.add(job.join().unwrap()); }
        if consumed == DECLARED_R8 && distributed.is_none() {
            assert_eq!(total.heads, 838_080);
            assert_eq!(total.p1, 6_619_280);
            assert_eq!(total.k17, 211_816_960);
            assert_eq!(total.pivotable_k17, 197_414_400);
            assert_eq!(total.p2, 815_482_880);
            assert_eq!(total.k19, 9_785_794_560);
            assert_eq!(total.samples.len(), 257);
        }
        assert_eq!(total.k17, 32 * total.p1);
        assert_eq!(total.k19, 12 * total.p2);
        assert_eq!(total.k21, 12 * total.p3);
        assert_eq!(total.literal_row19_hits + total.literal_row19_misses,
            total.pivotable_k19);
        let elapsed = begun.elapsed().as_secs_f64();
        assert!(elapsed < 600.0, "hard 600-second gate exceeded");
        let projected = elapsed * (DECLARED_R8 as f64) / (consumed as f64);
        let sample_path = format!("{}.samples.tsv", output);
        let mut sample_lines = vec![
            "sample_bin\thead_index\tr8_index\trow14\tsource_mass\tp1_uses\tK17_candidates\tpivotable_K17\tp2_uses\tK19_candidates\tpivotable_K19\tp3_uses\tK21_children\tcharge_scaled_U\twitness_p1\twitness_t3\twitness_p2\twitness_t2\twitness_p3\tm1\tm2\tm3\twitness_terminal_q\twitness_row17\twitness_row19".to_string()
        ];
        sample_lines.extend(total.samples.values().map(|x| x.1.clone()));
        let sample_tmp = format!("{}.tmp", sample_path);
        std::fs::write(&sample_tmp, format!("{}\n", sample_lines.join("\n"))).unwrap();
        rename(sample_tmp, &sample_path).unwrap();
        let status = if consumed == DECLARED_R8 && distributed.is_none() {
            "PASS_COMPLETE_SINGLETON_D14_222_R_3_2_2_K21_CHARGE"
        } else {
            "PASS_BOUNDED_PREFIX_SINGLETON_D14_222_R_3_2_2_K21_EVALUATOR"
        };
        let text = format!(concat!(
            "{{\n  \"status\":\"{}\",\n  \"lineage_id\":\"D14:222|R:3-2-2\",\n  \"covered_ids\":1,\n  \"scale_U\":\"{}\",\n",
            "  \"R8_records_consumed\":{},\n  \"R8_records_declared\":{},\n  \"source_heads\":{},\n  \"source_mass_sum\":\"{}\",\n  \"source_mass_l1\":\"{}\",\n",
            "  \"selected_p1_uses\":{},\n  \"K17_candidates\":{},\n  \"pivotable_K17_children\":{},\n  \"selected_p2_uses\":{},\n",
            "  \"K19_candidates\":{},\n  \"pivotable_K19_children\":{},\n  \"selected_p3_uses\":{},\n  \"K21_terminal_occurrences\":{},\n",
            "  \"full_occurrences\":{},\n  \"irreducible_occurrences\":{},\n  \"full_charge_scaled_U\":\"{}\",\n  \"irreducible_charge_scaled_U\":\"{}\",\n",
            "  \"all_K21_children_irreducible\":true,\n",
            "  \"first_denominator_hist\":{{{}}},\n  \"second_denominator_hist\":{{{}}},\n  \"third_denominator_hist\":{{{}}},\n  \"product_denominator_hist\":{{{}}},\n",
            "  \"signature_plan_cache\":{{\"stage2_hits\":{},\"stage2_misses\":{},\"stage3_hits\":{},\"stage3_misses\":{}}},\n",
            "  \"literal_row19_cache\":{{\"hits\":{},\"misses\":{},\"scope\":\"one source head\"}},\n",
            "  \"terminal_profile_cache\":{{\"hits\":{},\"misses\":{},\"peak_keys_per_worker\":{}}},\n",
            "  \"literal_samples\":{},\n  \"literal_sample_ledger\":\"{}\",\n",
            "  \"sign_rule\":\"direct coefficient=-M; three normalized response flips give terminal +M/(m1*m2*m3)\",\n",
            "  \"compression_proof\":\"signature caches choose only literal tail/pivot plans; literal row17 and row19 provenance is retained through p1 and p2, and profile compression begins only at terminal p3\",\n",
            "  \"scope\":\"exact singleton D14:222|R:3-2-2 scalar only; no K21 row collection, K22, other path, or membership inference\",\n",
            "  \"workers\":{},\n  \"elapsed_seconds\":{:.6},\n  \"projected_full_seconds_from_prefix\":{:.6}\n}}\n"
        ), status, U21, consumed, DECLARED_R8, total.heads, total.source_mass,
            total.source_mass_l1, total.p1, total.k17, total.pivotable_k17,
            total.p2, total.k19, total.pivotable_k19, total.p3, total.k21,
            total.k21, total.k21, total.charge, total.charge,
            histogram(&total.h1), histogram(&total.h2), histogram(&total.h3),
            histogram(&total.hp), total.plan2_hits, total.plan2_misses,
            total.plan3_hits, total.plan3_misses, total.literal_row19_hits,
            total.literal_row19_misses, total.terminal_hits,
            total.terminal_misses, total.peak_terminal_keys_per_r8,
            total.samples.len(), sample_path, workers, elapsed, projected);
        let tmp = format!("{}.tmp", output);
        std::fs::write(&tmp, &text).unwrap();
        rename(tmp, output).unwrap();
        print!("{}", text);
    }
}

fn main() { run::run_main(); }
