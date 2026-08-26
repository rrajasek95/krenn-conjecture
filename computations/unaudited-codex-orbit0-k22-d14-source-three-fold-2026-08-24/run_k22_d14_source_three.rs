//! Exact source-linear K22 scalar fold for D14:222 paths R323, R332, R422.
#![allow(dead_code)]

mod run {
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

    use std::collections::BTreeMap;
    use std::fs::rename;

    const U: i128 = 400_591_699_200;
    const DECLARED_R8: usize = 485;
    const HEADS_PER_R8: usize = 12 * 12 * 12;
    const DECLARED_HEADS: usize = DECLARED_R8 * HEADS_PER_R8;
    const CACHE_CAP: usize = 3_000_000;
    const WALL_GATE_SECONDS: f64 = 600.0;
    const DEFAULT_OUT: &str = "computations/unaudited-codex-orbit0-k22-d14-source-three-fold-2026-08-24/results_k22_d14_source_three.json";

    #[derive(Clone, Copy)]
    struct Config {
        id: &'static str,
        first_degree: usize,
        second_degree: usize,
        terminal_degree: usize,
    }

    const CONFIGS: [Config; 3] = [
        Config { id: "D14:222|R:3-2-3", first_degree: 3, second_degree: 2, terminal_degree: 3 },
        Config { id: "D14:222|R:3-3-2", first_degree: 3, second_degree: 3, terminal_degree: 2 },
        Config { id: "D14:222|R:4-2-2", first_degree: 4, second_degree: 2, terminal_degree: 2 },
    ];

    #[derive(Clone, Copy, Eq, Hash, PartialEq)]
    struct PlanKey {
        sig: [u8; 12],
        pivot: u8,
        degree: u8,
    }

    #[derive(Clone)]
    struct PlanTail {
        tail_index: usize,
        child_sig: [u8; 12],
        pivots: Vec<usize>,
    }

    #[derive(Clone, Copy, Default)]
    struct Terminal {
        n: u64,
        q: i64,
    }

    #[derive(Clone)]
    struct Witness {
        p1: usize,
        t1: usize,
        p2: usize,
        t2: usize,
        p3: usize,
        m1: usize,
        m2: usize,
        m3: usize,
        row1: Row,
        row2: Row,
        sig2: [u8; 12],
        terminal_q: i64,
    }

    #[derive(Default)]
    struct HeadStat {
        p1: u64,
        first_children: u64,
        pivotable_first: u64,
        p2: u64,
        second_children: u64,
        pivotable_second: u64,
        p3: u64,
        terminal_children: u64,
        charge: i128,
        witness: Option<Witness>,
    }

    #[derive(Default)]
    struct PathSum {
        p1: u64,
        first_children: u64,
        pivotable_first: u64,
        p2: u64,
        second_children: u64,
        pivotable_second: u64,
        p3: u64,
        terminal_children: u64,
        charge: i128,
        first_plan_hits: u64,
        first_plan_misses: u64,
        second_plan_hits: u64,
        second_plan_misses: u64,
        terminal_hits: u64,
        terminal_misses: u64,
        terminal_cache_clears: u64,
        literal_row_hits: u64,
        literal_row_misses: u64,
        h1: BTreeMap<u8, u64>,
        h2: BTreeMap<u8, u64>,
        h3: BTreeMap<u8, u64>,
        hp: BTreeMap<u16, u64>,
        samples: BTreeMap<usize, (usize, String)>,
    }

    impl PathSum {
        fn add_head(&mut self, x: &HeadStat) {
            self.p1 += x.p1;
            self.first_children += x.first_children;
            self.pivotable_first += x.pivotable_first;
            self.p2 += x.p2;
            self.second_children += x.second_children;
            self.pivotable_second += x.pivotable_second;
            self.p3 += x.p3;
            self.terminal_children += x.terminal_children;
            self.charge += x.charge;
        }

        fn add(&mut self, x: PathSum) {
            self.p1 += x.p1;
            self.first_children += x.first_children;
            self.pivotable_first += x.pivotable_first;
            self.p2 += x.p2;
            self.second_children += x.second_children;
            self.pivotable_second += x.pivotable_second;
            self.p3 += x.p3;
            self.terminal_children += x.terminal_children;
            self.charge += x.charge;
            self.first_plan_hits += x.first_plan_hits;
            self.first_plan_misses += x.first_plan_misses;
            self.second_plan_hits += x.second_plan_hits;
            self.second_plan_misses += x.second_plan_misses;
            self.terminal_hits += x.terminal_hits;
            self.terminal_misses += x.terminal_misses;
            self.terminal_cache_clears += x.terminal_cache_clears;
            self.literal_row_hits += x.literal_row_hits;
            self.literal_row_misses += x.literal_row_misses;
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

    #[derive(Default)]
    struct Sum {
        records: u64,
        heads: u64,
        source_mass: i128,
        source_mass_l1: i128,
        paths: [PathSum; 3],
        peak_terminal_cache_keys_per_worker: usize,
    }

    impl Sum {
        fn add(&mut self, x: Sum) {
            self.records += x.records;
            self.heads += x.heads;
            self.source_mass += x.source_mass;
            self.source_mass_l1 += x.source_mass_l1;
            self.peak_terminal_cache_keys_per_worker = self
                .peak_terminal_cache_keys_per_worker.max(x.peak_terminal_cache_keys_per_worker);
            for (target, source) in self.paths.iter_mut().zip(x.paths) { target.add(source); }
        }
    }

    fn plan(sig0: [u8; 12], pivot: usize, degree: usize, e: &E) -> Vec<PlanTail> {
        let mut out = Vec::new();
        for (tail_index, tail) in e.tails[pivot][degree - 2].iter().enumerate() {
            let child = child_sig(sig0, pivot, tail, e);
            let pivots = avail(child, e);
            if !pivots.is_empty() {
                out.push(PlanTail { tail_index, child_sig: child, pivots });
            }
        }
        out
    }

    fn abstract_ckey(prof: &[u8; 29], pivot: usize, tail: &[u8; 4], e: &E) -> CKey {
        let mut endpoint = [-1i8; 24];
        for (i, &cell) in e.anchors[pivot].iter().enumerate() {
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
            parts[n] = (pathsum / 2 + nodes as u16 / 2) as u8;
            n += 1;
        }
        let closed = prof[16] as usize;
        for &value in &prof[17..17 + closed] { parts[n] = value; n += 1; }
        parts[..n].sort_unstable();
        let mut key = [0u8; 13];
        key[0] = n as u8;
        key[1..1 + n].copy_from_slice(&parts[..n]);
        CKey(key)
    }

    fn terminal_response(
        row: &Row,
        sig0: [u8; 12],
        pivot: usize,
        degree: usize,
        e: &E,
        cache: &mut HashMap<RKey, Terminal>,
        path: &mut PathSum,
    ) -> Terminal {
        if cache.len() >= CACHE_CAP {
            cache.clear();
            path.terminal_cache_clears += 1;
        }
        let key = RKey { profile: profile(row, pivot, e), sig: sig0, pivot: pivot as u8, degree: degree as u8 };
        if let Some(&answer) = cache.get(&key) {
            path.terminal_hits += 1;
            return answer;
        }
        path.terminal_misses += 1;
        let mut answer = Terminal::default();
        for tail in &e.tails[pivot][degree - 2] {
            let sig22 = child_sig(sig0, pivot, tail, e);
            assert!(avail(sig22, e).is_empty(), "realized cached K22 response is not terminal");
            let key22 = abstract_ckey(&key.profile, pivot, tail, e);
            answer.n += 1;
            answer.q += *e.dual.get(&key22).unwrap_or(&0);
        }
        assert_eq!(answer.n, e.tails[pivot][degree - 2].len() as u64);
        cache.insert(key, answer);
        answer
    }

    #[allow(clippy::too_many_arguments)]
    fn fold_path(
        row14: Row,
        mass: i128,
        config: Config,
        e: &E,
        first_plans: &mut HashMap<PlanKey, Vec<PlanTail>>,
        second_plans: &mut HashMap<PlanKey, Vec<PlanTail>>,
        terminal_cache: &mut HashMap<RKey, Terminal>,
        literal_cache: &mut HashMap<(Row, u8), (usize, u64, i64, usize, i64)>,
        total: &mut PathSum,
    ) -> HeadStat {
        let mut head = HeadStat::default();
        let sig14 = sig(&row14, e);
        assert_eq!(sig14.iter().map(|&x| x as usize).sum::<usize>(), 10);
        let pivots1 = valid(sig14, e);
        let m1 = pivots1.len();
        assert!(m1 > 0 && U % m1 as i128 == 0);
        *total.h1.entry(m1 as u8).or_default() += 1;
        for p1 in pivots1 {
            head.p1 += 1;
            head.first_children += e.tails[p1][config.first_degree - 2].len() as u64;
            let key1 = PlanKey { sig: sig14, pivot: p1 as u8, degree: config.first_degree as u8 };
            if first_plans.contains_key(&key1) { total.first_plan_hits += 1; }
            else {
                total.first_plan_misses += 1;
                first_plans.insert(key1, plan(sig14, p1, config.first_degree, e));
            }
            for first in first_plans.get(&key1).unwrap() {
                head.pivotable_first += 1;
                let m2 = first.pivots.len();
                assert_eq!(U % (m1 * m2) as i128, 0);
                *total.h2.entry(m2 as u8).or_default() += 1;
                let row1 = replace(&row14, &e.anchors[p1],
                    &e.tails[p1][config.first_degree - 2][first.tail_index]);
                assert_eq!(sig(&row1, e), first.child_sig);
                for &p2 in &first.pivots {
                    head.p2 += 1;
                    head.second_children += e.tails[p2][config.second_degree - 2].len() as u64;
                    let key2 = PlanKey { sig: first.child_sig, pivot: p2 as u8, degree: config.second_degree as u8 };
                    if second_plans.contains_key(&key2) { total.second_plan_hits += 1; }
                    else {
                        total.second_plan_misses += 1;
                        second_plans.insert(key2, plan(first.child_sig, p2, config.second_degree, e));
                    }
                    for second in second_plans.get(&key2).unwrap() {
                        head.pivotable_second += 1;
                        let m3 = second.pivots.len();
                        let product = m1 * m2 * m3;
                        assert_eq!(U % product as i128, 0);
                        *total.h3.entry(m3 as u8).or_default() += 1;
                        *total.hp.entry(product as u16).or_default() += 1;
                        let row2 = replace(&row1, &e.anchors[p2],
                            &e.tails[p2][config.second_degree - 2][second.tail_index]);
                        assert_eq!(sig(&row2, e), second.child_sig);
                        let unit = mass * U / product as i128;
                        let cache_key = (row2, config.terminal_degree as u8);
                        let cached = if let Some(&value) = literal_cache.get(&cache_key) {
                            total.literal_row_hits += 1;
                            value
                        } else {
                            total.literal_row_misses += 1;
                            let mut n = 0u64;
                            let mut q = 0i64;
                            let mut first_response: Option<(usize, i64)> = None;
                            for &p3 in &second.pivots {
                                let response = terminal_response(
                                    &row2, second.child_sig, p3, config.terminal_degree,
                                    e, terminal_cache, total,
                                );
                                n += response.n;
                                q += response.q;
                                if first_response.is_none() ||
                                    (first_response.unwrap().1 == 0 && response.q != 0) {
                                    first_response = Some((p3, response.q));
                                }
                            }
                            let (first_p3, first_q) = first_response.unwrap();
                            let value = (m3, n, q, first_p3, first_q);
                            literal_cache.insert(cache_key, value);
                            value
                        };
                        let (cached_m3, terminal_n, terminal_q, first_p3, first_q) = cached;
                        assert_eq!(cached_m3, m3);
                        head.p3 += m3 as u64;
                        head.terminal_children += terminal_n;
                        head.charge += unit * terminal_q as i128;
                        if head.witness.is_none() ||
                            (head.witness.as_ref().unwrap().terminal_q == 0 && first_q != 0) {
                            head.witness = Some(Witness {
                                p1, t1: first.tail_index, p2, t2: second.tail_index,
                                p3: first_p3, m1, m2, m3, row1, row2,
                                sig2: second.child_sig, terminal_q: first_q,
                            });
                        }
                    }
                }
            }
        }
        assert_eq!(head.first_children,
            config.first_degree_tail_count() as u64 * head.p1);
        assert_eq!(head.second_children,
            config.second_degree_tail_count() as u64 * head.p2);
        assert_eq!(head.terminal_children,
            config.terminal_degree_tail_count() as u64 * head.p3);
        head
    }

    impl Config {
        fn tail_count(degree: usize) -> usize {
            match degree { 2 => 12, 3 => 32, 4 => 60, _ => unreachable!() }
        }
        fn first_degree_tail_count(self) -> usize { Self::tail_count(self.first_degree) }
        fn second_degree_tail_count(self) -> usize { Self::tail_count(self.second_degree) }
        fn terminal_degree_tail_count(self) -> usize { Self::tail_count(self.terminal_degree) }
    }

    fn hex(row: &Row) -> String {
        row.0.iter().map(|value| format!("{:02x}", value)).collect()
    }

    fn validate_literal(witness: &Witness, config: Config, e: &E) {
        let key = profile(&witness.row2, witness.p3, e);
        let mut q = 0i64;
        let mut n = 0u64;
        for tail in &e.tails[witness.p3][config.terminal_degree - 2] {
            let sig22 = child_sig(witness.sig2, witness.p3, tail, e);
            assert!(avail(sig22, e).is_empty());
            let row22 = replace(&witness.row2, &e.anchors[witness.p3], tail);
            assert_eq!(sig(&row22, e), sig22);
            let abstracted = abstract_ckey(&key, witness.p3, tail, e);
            let literal = ckey(&row22, e);
            assert!(abstracted == literal);
            q += *e.dual.get(&literal).unwrap_or(&0);
            n += 1;
        }
        assert_eq!(n, config.terminal_degree_tail_count() as u64);
        assert_eq!(q, witness.terminal_q);
    }

    fn sample_line(
        config: Config,
        bin: usize,
        head_index: usize,
        r8_index: usize,
        row14: &Row,
        mass: i128,
        stat: &HeadStat,
        witness: &Witness,
    ) -> String {
        format!(
            "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
            config.id, bin, head_index, r8_index, hex(row14), mass,
            stat.p1, stat.first_children, stat.pivotable_first, stat.p2,
            stat.second_children, stat.pivotable_second, stat.p3,
            stat.terminal_children, stat.charge, witness.p1, witness.t1,
            witness.p2, witness.t2, witness.p3, witness.m1, witness.m2,
            witness.m3, config.terminal_degree, witness.terminal_q,
            hex(&witness.row1), hex(&witness.row2),
            (witness.terminal_q != 0) as u8,
        )
    }

    fn worker(e: Arc<E>, ranges: Vec<(usize, usize)>) -> Sum {
        let mut total = Sum::default();
        let mut first_plans: HashMap<PlanKey, Vec<PlanTail>> = HashMap::new();
        let mut second_plans: HashMap<PlanKey, Vec<PlanTail>> = HashMap::new();
        let mut terminal_cache: HashMap<RKey, Terminal> = HashMap::new();
        let mut literal_cache: HashMap<(Row, u8), (usize, u64, i64, usize, i64)> = HashMap::new();
        for (start, end) in ranges {
            for r8_index in start..end {
                total.records += 1;
                let record = &e.records[r8_index];
                let mass = record.size as i128 * record.coefficient as i128;
                for (a_index, a) in e.factor[0][0].iter().enumerate() {
                    for (b_index, b) in e.factor[1][0].iter().enumerate() {
                        for (c_index, c) in e.factor[2][0].iter().enumerate() {
                            let head_index = r8_index * HEADS_PER_R8 +
                                (a_index * 12 + b_index) * 12 + c_index;
                            let row14 = make(record, a, b, c);
                            total.heads += 1;
                            total.source_mass += mass;
                            total.source_mass_l1 += mass.abs();
                            literal_cache.clear();
                            for (path_index, config) in CONFIGS.iter().copied().enumerate() {
                                let stat = fold_path(
                                    row14, mass, config, &e, &mut first_plans,
                                    &mut second_plans,
                                    &mut terminal_cache, &mut literal_cache,
                                    &mut total.paths[path_index],
                                );
                                total.paths[path_index].add_head(&stat);
                                if stat.p3 > 0 {
                                    let bin = head_index * 257 / DECLARED_HEADS;
                                    if !total.paths[path_index].samples.contains_key(&bin) {
                                        let witness = stat.witness.as_ref().unwrap();
                                        validate_literal(witness, config, &e);
                                        let line = sample_line(
                                            config, bin, head_index, r8_index,
                                            &row14, mass, &stat, witness,
                                        );
                                        total.paths[path_index].samples.insert(bin, (head_index, line));
                                    }
                                }
                            }
                        }
                    }
                }
                total.peak_terminal_cache_keys_per_worker = total
                    .peak_terminal_cache_keys_per_worker.max(terminal_cache.len());
            }
        }
        total
    }

    fn histogram<T: std::fmt::Display + Ord>(map: &BTreeMap<T, u64>) -> String {
        map.iter().map(|(key, value)| format!("\"{}\":{}", key, value))
            .collect::<Vec<_>>().join(",")
    }

    fn sink_json(config: Config, value: &PathSum) -> String {
        format!(concat!(
            "{{\"first_response_degree\":{},\"second_response_degree\":{},\"terminal_response_degree\":{},",
            "\"selected_p1_uses\":{},\"first_children\":{},\"pivotable_first_children\":{},",
            "\"selected_p2_uses\":{},\"second_children\":{},\"pivotable_second_children\":{},",
            "\"selected_p3_uses\":{},\"K22_terminal_occurrences\":{},\"full_occurrences\":{},\"irreducible_occurrences\":{},",
            "\"full_charge_scaled_U\":\"{}\",\"irreducible_charge_scaled_U\":\"{}\",",
            "\"first_denominator_hist\":{{{}}},\"second_denominator_hist\":{{{}}},",
            "\"third_denominator_hist\":{{{}}},\"product_denominator_hist\":{{{}}},",
            "\"plan_cache\":{{\"first_hits\":{},\"first_misses\":{},\"second_hits\":{},\"second_misses\":{}}},",
            "\"literal_preterminal_cache\":{{\"hits\":{},\"misses\":{},\"scope\":\"one source head, exact Row+terminal-degree key\"}},",
            "\"terminal_profile_cache\":{{\"hits\":{},\"misses\":{},\"clears_at_hard_cap\":{},\"hard_cap_keys_per_worker\":{}}},",
            "\"literal_samples\":{}}}"
        ), config.first_degree, config.second_degree, config.terminal_degree,
            value.p1, value.first_children, value.pivotable_first, value.p2,
            value.second_children, value.pivotable_second, value.p3,
            value.terminal_children, value.terminal_children, value.terminal_children,
            value.charge, value.charge, histogram(&value.h1), histogram(&value.h2),
            histogram(&value.h3), histogram(&value.hp), value.first_plan_hits,
            value.first_plan_misses, value.second_plan_hits, value.second_plan_misses,
            value.literal_row_hits, value.literal_row_misses, value.terminal_hits,
            value.terminal_misses, value.terminal_cache_clears, CACHE_CAP,
            value.samples.len())
    }

    pub fn run_main() {
        let begun = Instant::now();
        let args: Vec<String> = std::env::args().collect();
        let mut start = 0usize;
        let mut end = None;
        let mut distributed = None;
        let mut workers = 8usize;
        let mut output = DEFAULT_OUT.to_string();
        let mut i = 1;
        while i < args.len() {
            match args[i].as_str() {
                "--start-record" => { start = args[i + 1].parse().unwrap(); i += 2; }
                "--end-record" => { end = Some(args[i + 1].parse::<usize>().unwrap()); i += 2; }
                "--distributed-records" => { distributed = Some(args[i + 1].parse::<usize>().unwrap()); i += 2; }
                "--workers" => { workers = args[i + 1].parse().unwrap(); i += 2; }
                "--output" => { output = args[i + 1].clone(); i += 2; }
                _ => panic!("usage: evaluator [--start-record N --end-record N | --distributed-records N] [--workers 1..8] [--output PATH]"),
            }
        }
        assert!((1..=8).contains(&workers));
        assert!(distributed.is_none() || (start == 0 && end.is_none()));
        let end = end.unwrap_or(DECLARED_R8).min(DECLARED_R8);
        assert!(start < end);
        let consumed = distributed.unwrap_or(end - start).min(DECLARED_R8);
        let e = Arc::new(parse());
        assert_eq!(e.records.len(), DECLARED_R8);
        let mut ranges = vec![Vec::new(); workers];
        if distributed.is_some() {
            for sample in 0..consumed {
                let index = if consumed == 1 { DECLARED_R8 / 2 }
                    else { sample * (DECLARED_R8 - 1) / (consumed - 1) };
                ranges[sample % workers].push((index, index + 1));
            }
        } else {
            let pieces = workers * 8;
            for piece in 0..pieces {
                let (lo, hi) =
                (start + (end - start) * piece / pieces,
                 start + (end - start) * (piece + 1) / pieces);
                if lo < hi { ranges[piece % workers].push((lo, hi)); }
            }
        }
        let mut jobs = Vec::new();
        for worker_index in 0..workers {
            let ee = e.clone();
            let rr = std::mem::take(&mut ranges[worker_index]);
            jobs.push(thread::spawn(move || worker(ee, rr)));
        }
        let mut total = Sum::default();
        for job in jobs { total.add(job.join().unwrap()); }
        assert_eq!(total.records, consumed as u64);
        assert_eq!(total.heads, consumed as u64 * HEADS_PER_R8 as u64);
        for (config, value) in CONFIGS.iter().copied().zip(&total.paths) {
            assert_eq!(value.first_children, config.first_degree_tail_count() as u64 * value.p1);
            assert_eq!(value.second_children, config.second_degree_tail_count() as u64 * value.p2);
            assert_eq!(value.terminal_children, config.terminal_degree_tail_count() as u64 * value.p3);
            assert_eq!(value.literal_row_hits + value.literal_row_misses, value.pivotable_second);
        }
        let full = distributed.is_none() && start == 0 && end == DECLARED_R8;
        if full {
            assert_eq!(total.heads, 838_080);
            let value = &total.paths[0];
            assert_eq!(value.p1, 6_619_280);
            assert_eq!(value.first_children, 211_816_960);
            assert_eq!(value.pivotable_first, 197_414_400);
            assert_eq!(value.p2, 815_482_880);
            assert_eq!(value.second_children, 9_785_794_560);
            assert_eq!(value.pivotable_second, 2_969_658_880);
            assert_eq!(value.p3, 5_075_412_480);
            assert_eq!(value.terminal_children, 162_413_199_360);
            assert!(total.paths.iter().all(|value| value.samples.len() == 257));
        }
        let elapsed = begun.elapsed().as_secs_f64();
        assert!(elapsed < WALL_GATE_SECONDS, "hard 600-second interval gate exceeded; no result written");
        let projected = elapsed * DECLARED_R8 as f64 / consumed as f64;
        let sample_path = format!("{}.samples.tsv", output);
        let mut sample_lines = vec![
            "lineage_id\tsample_bin\thead_index\tr8_index\trow14\tsource_mass\tp1_uses\tfirst_children\tpivotable_first\tp2_uses\tsecond_children\tpivotable_second\tp3_uses\tK22_children\tcharge_scaled_U\twitness_p1\twitness_t1\twitness_p2\twitness_t2\twitness_p3\tm1\tm2\tm3\tterminal_degree\twitness_terminal_q\twitness_row1\twitness_row2\tnonzero_terminal_q".to_string()
        ];
        for path in &total.paths {
            sample_lines.extend(path.samples.values().map(|value| value.1.clone()));
        }
        let sample_tmp = format!("{}.tmp", sample_path);
        std::fs::write(&sample_tmp, format!("{}\n", sample_lines.join("\n"))).unwrap();
        rename(sample_tmp, &sample_path).unwrap();
        let status = if full {
            "PASS_COMPLETE_D14_222_K22_SOURCE_THREE_CHARGE"
        } else {
            "PASS_BOUNDED_D14_222_K22_SOURCE_THREE_EVALUATOR"
        };
        let sink_text = CONFIGS.iter().copied().zip(&total.paths)
            .map(|(config, value)| format!("\"{}\":{}", config.id, sink_json(config, value)))
            .collect::<Vec<_>>().join(",\n    ");
        let text = format!(concat!(
            "{{\n  \"status\":\"{}\",\n  \"covered_lineage_ids\":[\"{}\",\"{}\",\"{}\"],\n",
            "  \"scale_U\":\"{}\",\n  \"R8_record_interval\":[{},{}],\n  \"distributed_record_mode\":{},\n",
            "  \"R8_records_consumed\":{},\n  \"R8_records_declared\":{},\n  \"source_heads\":{},\n",
            "  \"source_mass_sum\":\"{}\",\n  \"source_mass_l1\":\"{}\",\n  \"sinks\":{{\n    {}\n  }},\n",
            "  \"all_realized_cached_K22_responses_terminal\":true,\n",
            "  \"literal_sample_guard\":{{\"records\":{},\"records_per_sink\":[{},{},{}],\"all_literal_K22_children_terminal\":true,\"all_abstract_literal_cycle_keys_equal\":true,\"ledger\":\"{}\"}},\n",
            "  \"sign_rule\":\"direct D14 coefficient=-M; three normalized response flips give terminal +M/(m1*m2*m3), implemented as source_mass*U/(m1*m2*m3)\",\n",
            "  \"compression_proof\":\"every row14 and both preterminal rows are literal; signature caches select only literal tail/pivot plans; exact Row+terminal-degree deduplication is source-head local; profile compression begins only at the terminal response\",\n",
            "  \"shared_fold_scope\":\"one source-head scan, three degree-separated exact sinks; terminal profile cache is shared only through complete RKey(profile,signature,pivot,degree)\",\n",
            "  \"terminal_cache_resource_guard\":{{\"hard_cap_keys_per_worker\":{},\"peak_keys_per_worker\":{}}},\n",
            "  \"workers\":{},\n  \"elapsed_seconds\":{:.6},\n  \"projected_full_seconds_from_consumed_records\":{:.6},\n",
            "  \"scope\":\"exactly three named D14 K22 scalar sinks; no K17/K18/K19/K20/K22 row output, K23, membership, or conjecture verdict\"\n}}\n"
        ), status, CONFIGS[0].id, CONFIGS[1].id, CONFIGS[2].id, U,
            start, end, distributed.is_some(), total.records, DECLARED_R8,
            total.heads, total.source_mass, total.source_mass_l1, sink_text,
            sample_lines.len() - 1, total.paths[0].samples.len(),
            total.paths[1].samples.len(), total.paths[2].samples.len(),
            sample_path, CACHE_CAP, total.peak_terminal_cache_keys_per_worker,
            workers, elapsed, projected);
        let tmp = format!("{}.tmp", output);
        std::fs::write(&tmp, &text).unwrap();
        rename(tmp, output).unwrap();
        print!("{}", text);
    }
}

fn main() { run::run_main(); }
