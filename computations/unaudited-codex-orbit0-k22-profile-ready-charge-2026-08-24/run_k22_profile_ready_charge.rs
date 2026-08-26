mod run {
    #![allow(dead_code)]
    include!("../unaudited-codex-orbit0-k19-profile-census-2026-08-23/run_k19_profile_census.rs");

    use std::fs::metadata;
    use std::io::{BufReader, Read, Seek, SeekFrom};

    const U: i128 = 400_591_699_200;
    const WORKERS: usize = 8;
    const GATE_SECONDS: f64 = 600.0;
    const K4_PATH: &str = "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin";
    const CYCLE_PATH: &str = "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin";
    const DIRECT_PROFILE: &str = "computations/unaudited-codex-orbit0-direct-k18-profile-census-2026-08-23/direct_k18_enriched_profiles.bin";
    const K14_PROFILE: &str = "computations/unaudited-codex-orbit0-k18-k14-full-profiles-2026-08-23/k14_k4_enriched_profiles.bin";
    const K15_PROFILE: &str = "computations/unaudited-codex-orbit0-k15-k3-full-export-plan-2026-08-23/checkpoint_k15_k3_profiles_merged.bin";
    const K16_PROFILE: &str = "computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23/checkpoint_k16_k2_profiles_merged.bin";
    const DEFAULT_RESULT: &str = "computations/unaudited-codex-orbit0-k22-profile-ready-charge-2026-08-24/results_k22_profile_ready_charge.raw.json";
    const DIRECT_HEADER: u64 = 256;
    const DIRECT_RECORD: u64 = 72;
    const PROFILE_RECORD: u64 = 104;

    #[derive(Clone)]
    struct Aux {
        tails: Vec<Vec<[u8; 4]>>,
        edges: Vec<Vec<[[u8; 2]; 4]>>,
        dual: HashMap<[u8; 13], i64>,
    }

    #[derive(Clone, Copy, Default)]
    struct Q {
        records: u64,
        tails: u64,
        charge: i128,
        signed_weight: i128,
        l1_weight: i128,
        uses: u64,
        occurrences: u64,
        key_guards: u64,
        terminal_guards: u64,
        witness_profile_replays: u64,
        literal_cycle_checks: u64,
    }

    impl Q {
        fn add(&mut self, x: Q) {
            self.records += x.records;
            self.tails += x.tails;
            self.charge += x.charge;
            self.signed_weight += x.signed_weight;
            self.l1_weight += x.l1_weight;
            self.uses += x.uses;
            self.occurrences += x.occurrences;
            self.key_guards += x.key_guards;
            self.terminal_guards += x.terminal_guards;
            self.witness_profile_replays += x.witness_profile_replays;
            self.literal_cycle_checks += x.literal_cycle_checks;
        }
    }

    #[derive(Clone, Copy)]
    enum Kind { Direct, K14, K15, K16 }

    #[derive(Clone, Copy)]
    struct Spec {
        name: &'static str,
        path: &'static str,
        kind: Kind,
        header: u64,
        record: u64,
        expected_records: u64,
        expected_uses: u64,
        expected_weight: i128,
        ids: &'static str,
        stored_path: &'static str,
    }

    #[derive(Clone)]
    struct Bounds { first: Option<Vec<u8>>, last: Option<Vec<u8>> }

    fn i128le(x: &[u8]) -> i128 { i128::from_le_bytes(x.try_into().unwrap()) }
    fn u64x(x: &[u8]) -> u64 { u64::from_le_bytes(x.try_into().unwrap()) }

    fn load_aux(e: &E) -> Aux {
        let b = read(K4_PATH).unwrap();
        assert_eq!(&b[..7], b"K18K4A1");
        let mut at = 7usize;
        let mut tails = vec![Vec::new(); 78];
        for p in 0..78 {
            for _ in 0..60 {
                let mut t = [0u8; 4];
                t.copy_from_slice(&b[at..at + 4]);
                at += 4;
                tails[p].push(t);
            }
        }
        assert_eq!(at, b.len());
        assert!(tails.iter().all(|x| x.len() == 60));

        let mut edges = vec![Vec::new(); 78];
        for p in 0..78 {
            let mut label = [255u8; 24];
            for (i, &cell) in e.anchors[p].iter().enumerate() {
                let [u, v, a, b] = e.cells[cell as usize];
                label[(3 * u + a) as usize] = (2 * i) as u8;
                label[(3 * v + b) as usize] = (2 * i + 1) as u8;
            }
            for tail in &tails[p] {
                let mut item = [[0u8; 2]; 4];
                for (i, &cell) in tail.iter().enumerate() {
                    let [u, v, a, b] = e.cells[cell as usize];
                    let x = label[(3 * u + a) as usize];
                    let y = label[(3 * v + b) as usize];
                    assert!(x < 8 && y < 8 && x != y);
                    item[i] = [x, y];
                }
                edges[p].push(item);
            }
        }

        let c = read(CYCLE_PATH).unwrap();
        assert_eq!(&c[..8], b"K17CYC1\0");
        let mut z = 8 + 252 * 4;
        let n = u32le(&c[z..z + 4]) as usize;
        z += 4;
        let mut dual = HashMap::new();
        for _ in 0..n {
            let mut key = [0u8; 13];
            key.copy_from_slice(&c[z..z + 13]);
            z += 13;
            let value = i64::from_le_bytes(c[z..z + 8].try_into().unwrap());
            z += 8;
            assert!(dual.insert(key, value).is_none());
        }
        assert_eq!(z, c.len());
        Aux { tails, edges, dual }
    }

    fn profile_guard(k: &Key) {
        let mut open_sum = 0usize;
        for i in 0..8 {
            let j = k.profile[i] as usize;
            assert!(j < 8 && j != i);
            assert_eq!(k.profile[j] as usize, i);
            assert!(k.profile[8 + i] > 0);
            assert_eq!(k.profile[8 + i], k.profile[8 + j]);
            if i < j { open_sum += k.profile[8 + i] as usize; }
        }
        let nc = k.profile[16] as usize;
        assert!(nc <= 12);
        assert!(k.profile[17..17 + nc].iter().all(|&x| x > 0));
        assert!(k.profile[17..17 + nc].windows(2).all(|x| x[0] <= x[1]));
        assert!(k.profile[17 + nc..].iter().all(|&x| x == 0));
        let closed_sum: usize = k.profile[17..17 + nc].iter().map(|&x| x as usize).sum();
        assert_eq!(open_sum + closed_sum, 20);
    }

    fn row_cycle(row: &Row, e: &E) -> [u8; 13] {
        let mut adj = [[0u8; 2]; 24];
        let mut degree = [0usize; 24];
        for &cell in &row.0 {
            let [u, v, a, b] = e.cells[cell as usize];
            let x = (3 * u + a) as usize;
            let y = (3 * v + b) as usize;
            assert!(degree[x] < 2 && degree[y] < 2);
            adj[x][degree[x]] = y as u8; degree[x] += 1;
            adj[y][degree[y]] = x as u8; degree[y] += 1;
        }
        assert!(degree.iter().all(|&d| d == 2));
        let mut seen = [false; 24];
        let mut parts = [0u8; 12];
        let mut n = 0usize;
        for start in 0..24 {
            if seen[start] { continue; }
            let mut stack = [0u8; 24];
            stack[0] = start as u8;
            let (mut top, mut len) = (1usize, 0u8);
            seen[start] = true;
            while top > 0 {
                top -= 1;
                let x = stack[top] as usize;
                len += 1;
                for &y in &adj[x] {
                    if !seen[y as usize] {
                        seen[y as usize] = true;
                        stack[top] = y;
                        top += 1;
                    }
                }
            }
            parts[n] = len;
            n += 1;
        }
        parts[..n].sort_unstable();
        let mut out = [0u8; 13];
        out[0] = n as u8;
        out[1..1 + n].copy_from_slice(&parts[..n]);
        out
    }

    fn key_cycle_edges(k: &Key, tail: &[[u8; 2]; 4]) -> [u8; 13] {
        let mut adj = [[(255u8, 0u8); 2]; 8];
        let mut degree = [0usize; 8];
        let mut edge = |a: usize, b: usize, weight: u8| {
            assert!(a < 8 && b < 8 && a != b && degree[a] < 2 && degree[b] < 2);
            adj[a][degree[a]] = (b as u8, weight); degree[a] += 1;
            adj[b][degree[b]] = (a as u8, weight); degree[b] += 1;
        };
        for a in 0..8 {
            let b = k.profile[a] as usize;
            if a < b { edge(a, b, k.profile[8 + a]); }
        }
        for &[a, b] in tail { edge(a as usize, b as usize, 1); }
        assert!(degree.iter().all(|&x| x == 2));
        let mut parts = [0u8; 12];
        let closed = k.profile[16] as usize;
        parts[..closed].copy_from_slice(&k.profile[17..17 + closed]);
        let mut n = closed;
        let mut seen = [false; 8];
        for start in 0..8 {
            if seen[start] { continue; }
            let mut stack = [0u8; 8];
            stack[0] = start as u8;
            let (mut top, mut twice) = (1usize, 0u16);
            seen[start] = true;
            while top > 0 {
                top -= 1;
                let x = stack[top] as usize;
                for &(y, weight) in &adj[x] {
                    twice += weight as u16;
                    if !seen[y as usize] {
                        seen[y as usize] = true;
                        stack[top] = y;
                        top += 1;
                    }
                }
            }
            assert_eq!(twice % 2, 0);
            parts[n] = (twice / 2) as u8;
            n += 1;
        }
        parts[..n].sort_unstable();
        let mut out = [0u8; 13];
        out[0] = n as u8;
        out[1..1 + n].copy_from_slice(&parts[..n]);
        out
    }

    fn terminal_key_guard(k: &Key, e: &E) {
        assert_eq!(k.sig.iter().map(|&x| x as usize).sum::<usize>(), 6);
        let p = k.pivot as usize;
        assert!(p < e.piv.len());
        assert_eq!(e.piv[p].iter().map(|&x| x as usize).sum::<usize>(), 4);
        assert!((0..12).all(|i| k.sig[i] >= e.piv[p][i]));
        // K4 restores no anchor incidence: the K22 child has sum 6-4=2.
        // Every K0 pivot signature has sum four, so no child can dominate one.
        assert!(e.piv.iter().all(|x| x.iter().map(|&v| v as usize).sum::<usize>() == 4));
    }

    fn evaluate_key(k: &Key, weight: i128, uses: u64, aux: &Aux) -> Q {
        let p = k.pivot as usize;
        let mut q = Q::default();
        q.records = 1;
        q.signed_weight = weight;
        q.l1_weight = weight.abs();
        q.uses = uses;
        q.key_guards = 1;
        q.terminal_guards = 1;
        for edges in &aux.edges[p] {
            let charge = *aux.dual.get(&key_cycle_edges(k, edges)).unwrap_or(&0) as i128;
            q.tails += 1;
            q.charge += weight * charge;
            q.occurrences += uses;
        }
        q
    }

    fn direct_witness_row(e: &E, lineage: u8, ri: u16, ix: [u8; 3]) -> Row {
        assert!(lineage < 6 && (ri as usize) < e.records.len());
        let record = &e.records[ri as usize];
        let index = [ix[0] as usize, ix[1] as usize, ix[2] as usize];
        if lineage < 3 {
            let low = lineage as usize;
            let other: Vec<_> = (0..3).filter(|&x| x != low).collect();
            let a = e.factor[low][0][index[low]];
            let b = e.factor[other[0]][2][index[other[0]]];
            let c = e.factor[other[1]][2][index[other[1]]];
            match low { 0 => make(record, &a, &b, &c), 1 => make(record, &b, &a, &c), _ => make(record, &b, &c, &a) }
        } else {
            let high = (lineage - 3) as usize;
            let other: Vec<_> = (0..3).filter(|&x| x != high).collect();
            let a = e.factor[other[0]][1][index[other[0]]];
            let b = e.factor[other[1]][1][index[other[1]]];
            let c = e.factor[high][2][index[high]];
            match high { 0 => make(record, &c, &a, &b), 1 => make(record, &a, &c, &b), _ => make(record, &a, &b, &c) }
        }
    }

    fn check_header(spec: Spec) {
        let mut header = vec![0u8; spec.header as usize];
        File::open(spec.path).unwrap().read_exact(&mut header).unwrap();
        match spec.kind {
            Kind::Direct => {
                assert_eq!(&header[..8], b"D18MRG1\0");
                assert_eq!(i128le(&header[8..24]), U);
                assert_eq!(u16::from_le_bytes(header[24..26].try_into().unwrap()), 0);
                assert_eq!(u16::from_le_bytes(header[26..28].try_into().unwrap()), 485);
                assert_eq!(u16::from_le_bytes(header[28..30].try_into().unwrap()) as u64, spec.record);
                assert_eq!(u64x(&header[176..184]), spec.expected_records);
                assert_eq!(i128le(&header[184..200]), spec.expected_weight);
                assert_eq!(u64x(&header[200..208]), spec.expected_uses);
            }
            Kind::K14 => {
                assert_eq!(&header[..8], b"K14MRG1\0");
                assert_eq!(u64x(&header[8..16]) as i128, U);
                assert_eq!(u64x(&header[56..64]), spec.expected_records);
                assert_eq!(u64x(&header[72..80]), spec.expected_uses);
                assert_eq!(i128le(&header[80..96]), spec.expected_weight);
            }
            Kind::K15 | Kind::K16 => {
                let magic = match spec.kind { Kind::K15 => b"K15MRG1\0", Kind::K16 => b"K16MRG1\0", _ => unreachable!() };
                assert_eq!(&header[..8], magic);
                assert_eq!(u32le(&header[8..12]), 1);
                assert_eq!(u16::from_le_bytes(header[12..14].try_into().unwrap()) as u64, spec.record);
                assert_eq!(i128le(&header[16..32]), U);
                assert_eq!(u64x(&header[56..64]), spec.expected_records);
                assert_eq!(u64x(&header[72..80]), spec.expected_uses);
                assert_eq!(i128le(&header[96..112]), spec.expected_weight);
            }
        }
        assert_eq!(metadata(spec.path).unwrap().len(), spec.header + spec.record * spec.expected_records);
    }

    fn profile_eval_worker(spec: Spec, e: Arc<E>, aux: Arc<Aux>, start: u64, end: u64,
              begun: Arc<Instant>) -> (Q, Bounds) {
        let mut file = File::open(spec.path).unwrap();
        file.seek(SeekFrom::Start(spec.header + spec.record * start)).unwrap();
        let mut reader = BufReader::with_capacity(2 << 20, file);
        let mut total = Q::default();
        let mut first = None;
        let mut last: Option<Vec<u8>> = None;
        for index in start..end {
            let mut z = vec![0u8; spec.record as usize];
            reader.read_exact(&mut z).unwrap();
            let (order, key, weight, uses, row) = match spec.kind {
                Kind::Direct => {
                    let order = z[..43].to_vec();
                    let lineage = z[0];
                    let mut profile_data = [0u8; 29]; profile_data.copy_from_slice(&z[1..30]);
                    let mut signature = [0u8; 12]; signature.copy_from_slice(&z[30..42]);
                    let key = Key { profile: profile_data, sig: signature, pivot: z[42], degree: 4 };
                    let row = direct_witness_row(&e, lineage, u16::from_le_bytes(z[67..69].try_into().unwrap()), [z[69], z[70], z[71]]);
                    (order, key, i128le(&z[43..59]), u64x(&z[59..67]), row)
                }
                Kind::K14 | Kind::K15 | Kind::K16 => {
                    let order = z[..42].to_vec();
                    let mut profile_data = [0u8; 29]; profile_data.copy_from_slice(&z[..29]);
                    let mut signature = [0u8; 12]; signature.copy_from_slice(&z[29..41]);
                    let key = Key { profile: profile_data, sig: signature, pivot: z[41], degree: 4 };
                    let mut cells = [0u8; 24]; cells.copy_from_slice(&z[66..90]);
                    let row = Row(cells);
                    assert!(row.0.windows(2).all(|x| x[0] <= x[1]));
                    let source = u64x(&z[90..98]);
                    let p1 = z[98] as usize;
                    let tail1 = z[99] as usize;
                    let p2 = z[100] as usize;
                    let m1 = z[101] as i128;
                    let m2 = z[102] as usize;
                    assert_eq!(p2, key.pivot as usize);
                    assert_eq!(avail(key.sig, &e).len(), m2);
                    assert!(m1 > 0 && m2 > 0 && U % (m1 * m2 as i128) == 0);
                    match spec.kind {
                        Kind::K14 => { assert!(source < 485 && p1 < 78 && tail1 < 60 && z[103] == 0); }
                        Kind::K15 => { assert!(source < 485 && p1 < 78 && tail1 < 32 && z[103] < 3); }
                        Kind::K16 => { assert!(source < 24_097_095 && p1 < 78 && tail1 < 12 && z[103] == 255); }
                        _ => unreachable!(),
                    }
                    (order, key, i128le(&z[42..58]), u64x(&z[58..66]), row)
                }
            };
            if let Some(prior) = &last { assert!(prior < &order); } else { first = Some(order.clone()); }
            last = Some(order);
            assert_ne!(weight, 0);
            assert!(uses > 0);
            assert_eq!(sig(&row, &e), key.sig);
            assert_eq!(profile(&row, key.pivot as usize, &e), key.profile);
            profile_guard(&key);
            terminal_key_guard(&key, &e);
            let mut q = evaluate_key(&key, weight, uses, &aux);
            q.witness_profile_replays = 1;
            if index == start || index + 1 == end || index % 100_000 == 0 {
                for tail_index in (0..60).step_by(7) {
                    let child = replace(&row, &e.anchors[key.pivot as usize], &aux.tails[key.pivot as usize][tail_index]);
                    assert_eq!(key_cycle_edges(&key, &aux.edges[key.pivot as usize][tail_index]), row_cycle(&child, &e));
                    q.literal_cycle_checks += 1;
                }
            }
            total.add(q);
            if index % 250_000 == 0 { assert!(begun.elapsed().as_secs_f64() < GATE_SECONDS); }
        }
        (total, Bounds { first, last })
    }

    fn read_group(spec: Spec, limit: Option<u64>, e: Arc<E>, aux: Arc<Aux>, begun: Arc<Instant>) -> Q {
        check_header(spec);
        let n = limit.map_or(spec.expected_records, |x| x.min(spec.expected_records));
        let mut jobs = Vec::new();
        for worker_index in 0..WORKERS {
            let start = n * worker_index as u64 / WORKERS as u64;
            let end = n * (worker_index as u64 + 1) / WORKERS as u64;
            let ee = e.clone(); let aa = aux.clone(); let bb = begun.clone();
            jobs.push(thread::spawn(move || profile_eval_worker(spec, ee, aa, start, end, bb)));
        }
        let mut parts = Vec::new();
        for job in jobs { parts.push(job.join().unwrap()); }
        for i in 1..parts.len() {
            if let (Some(left), Some(right)) = (&parts[i - 1].1.last, &parts[i].1.first) { assert!(left < right); }
        }
        let mut total = Q::default();
        for (q, _) in parts { total.add(q); }
        assert_eq!(total.records, n);
        assert_eq!(total.tails, n * 60);
        assert_eq!(total.key_guards, n);
        assert_eq!(total.terminal_guards, n);
        assert_eq!(total.witness_profile_replays, n);
        if n == spec.expected_records {
            assert_eq!(total.uses, spec.expected_uses);
            assert_eq!(total.signed_weight, spec.expected_weight);
            assert_eq!(total.occurrences, spec.expected_uses * 60);
        }
        eprintln!("PASS {} records={} tails={} charge={} literal_cycles={}", spec.name, total.records, total.tails, total.charge, total.literal_cycle_checks);
        total
    }

    fn json_group(spec: Spec, q: Q) -> String {
        format!(concat!(
            "{{\"name\":\"{}\",\"ids\":{},\"source_profile\":\"{}\",\"source_format\":\"{}\",",
            "\"stored_path\":\"{}\",\"target_degree\":4,\"profile_records\":{},\"profile_tail_evaluations\":{},",
            "\"irreducible_profile_tail_evaluations\":{},\"input_profile_uses\":{},\"source_occurrences\":{},",
            "\"input_weight_scaled_U\":\"{}\",\"l1_weight_scaled_U\":\"{}\",",
            "\"full_77_charge_scaled_U\":\"{}\",\"irreducible_77_charge_scaled_U\":\"{}\",",
            "\"exhaustive_key_guards\":{},\"universal_terminal_guards\":{},",
            "\"literal_witness_profile_replays\":{},\"literal_profile_cycle_comparisons\":{},",
            "\"individual_id_charges\":{}}}"),
            spec.name, spec.ids, spec.path,
            match spec.kind { Kind::Direct => "D18MRG1", Kind::K14 => "K14MRG1", Kind::K15 => "K15MRG1", Kind::K16 => "K16MRG1" },
            spec.stored_path, q.records, q.tails, q.tails, q.uses, q.occurrences,
            q.signed_weight, q.l1_weight, q.charge, q.charge, q.key_guards,
            q.terminal_guards, q.witness_profile_replays, q.literal_cycle_checks,
            if spec.ids.matches(',').count() == 0 { "\"equal_to_group_scalar\"" } else { "null" })
    }

    pub fn run_main() {
        let mut args = std::env::args().skip(1);
        let mut limit = None;
        let mut output = DEFAULT_RESULT.to_string();
        while let Some(arg) = args.next() {
            match arg.as_str() {
                "--prefix" => limit = Some(args.next().unwrap().parse::<u64>().unwrap()),
                "--output" => output = args.next().unwrap(),
                _ => panic!("unknown argument {arg}"),
            }
        }
        let specs = [
            Spec { name: "direct_D18_R4", path: DIRECT_PROFILE, kind: Kind::Direct, header: DIRECT_HEADER, record: DIRECT_RECORD,
                expected_records: 979_091, expected_uses: 252_631_784, expected_weight: -2_655_476_097_643_708_416_000,
                ids: "[\"D18:244|R:4\",\"D18:334|R:4\",\"D18:343|R:4\",\"D18:424|R:4\",\"D18:433|R:4\",\"D18:442|R:4\"]", stored_path: "direct D18" },
            Spec { name: "D14_R4_4", path: K14_PROFILE, kind: Kind::K14, header: 256, record: PROFILE_RECORD,
                expected_records: 18_217_226, expected_uses: 886_145_203, expected_weight: 496_321_127_773_883_596_800,
                ids: "[\"D14:222|R:4-4\"]", stored_path: "D14 R4" },
            Spec { name: "grouped_D15_R3_4", path: K15_PROFILE, kind: Kind::K15, header: 128, record: PROFILE_RECORD,
                expected_records: 25_564_391, expected_uses: 2_311_887_188, expected_weight: 1_865_098_870_468_588_339_200,
                ids: "[\"D15:223|R:3-4\",\"D15:232|R:3-4\",\"D15:322|R:3-4\"]", stored_path: "D15 R3" },
            Spec { name: "grouped_D16_R2_4", path: K16_PROFILE, kind: Kind::K16, header: 128, record: PROFILE_RECORD,
                expected_records: 6_876_260, expected_uses: 1_604_299_948, expected_weight: 3_218_269_567_887_566_438_400,
                ids: "[\"D16:224|R:2-4\",\"D16:233|R:2-4\",\"D16:242|R:2-4\",\"D16:323|R:2-4\",\"D16:332|R:2-4\",\"D16:422|R:2-4\"]", stored_path: "D16 R2" },
        ];
        let begun = Arc::new(Instant::now());
        let e = Arc::new(parse());
        assert!(e.piv.iter().all(|x| x.iter().map(|&v| v as usize).sum::<usize>() == 4));
        let aux = Arc::new(load_aux(&e));
        let mut values = Vec::new();
        for spec in specs { values.push(read_group(spec, limit, e.clone(), aux.clone(), begun.clone())); }
        let mut total = Q::default();
        for value in &values { total.add(*value); }
        let covered = concat!(
            "[\"D14:222|R:4-4\",",
            "\"D15:223|R:3-4\",\"D15:232|R:3-4\",\"D15:322|R:3-4\",",
            "\"D16:224|R:2-4\",\"D16:233|R:2-4\",\"D16:242|R:2-4\",\"D16:323|R:2-4\",\"D16:332|R:2-4\",\"D16:422|R:2-4\",",
            "\"D18:244|R:4\",\"D18:334|R:4\",\"D18:343|R:4\",\"D18:424|R:4\",\"D18:433|R:4\",\"D18:442|R:4\"]");
        let groups = specs.iter().zip(values.iter()).map(|(&s, &q)| json_group(s, q)).collect::<Vec<_>>().join(",\n    ");
        let full = limit.is_none();
        if full {
            assert_eq!(total.records, 51_636_968);
            assert_eq!(total.tails, 3_098_218_080);
            assert_eq!(total.key_guards, total.records);
            assert_eq!(total.terminal_guards, total.records);
            assert_eq!(total.witness_profile_replays, total.records);
        }
        let elapsed = begun.elapsed().as_secs_f64();
        assert!(elapsed < GATE_SECONDS);
        let text = format!(concat!(
            "{{\n  \"status\":\"{}\",\n  \"scale_U\":\"{}\",\n  \"workers\":{},\n",
            "  \"prefix_records_per_group\":{},\n",
            "  \"coverage\":{{\"covered_count\":{},\"covered_ids\":{},\"strict_exact_set_guard\":{}}},\n",
            "  \"groups\":[{}],\n",
            "  \"subtotal\":{{\"covered_DAG_paths\":{},\"profile_records\":{},\"profile_tail_evaluations\":{},",
            "\"irreducible_profile_tail_evaluations\":{},\"full_77_charge_scaled_U\":\"{}\",",
            "\"irreducible_77_charge_scaled_U\":\"{}\",\"exhaustive_key_guards\":{},",
            "\"universal_terminal_guards\":{},\"literal_witness_profile_replays\":{},",
            "\"literal_profile_cycle_comparisons\":{}}},\n",
            "  \"terminality\":\"Every K18 signature has anchor sum 6; every K0 pivot consumes 4 and a K4 tail restores 0, so every K22 child has sum 2<4 and is irreducible.\",\n",
            "  \"individual_id_guard\":\"The direct D18, D15, and D16 interfaces are group-aggregated; only D14 R4-4 is an individual scalar.\",\n",
            "  \"scope\":\"exact K22 charge only for the 16 named profile-ready IDs; no rows, source replays, K23/K24 run, membership, or conjecture claim\",\n",
            "  \"elapsed_seconds\":{:.6}\n}}\n"),
            if full { "PASS_EXACT_K22_16_PROFILE_READY_77_CHARGE_SUBTOTAL" } else { "PASS_PREFIX_ONLY_NO_K22_CHARGE_CLAIM" },
            U, WORKERS, limit.map_or("null".to_string(), |x| x.to_string()),
            if full { 16 } else { 0 }, covered, if full { "true" } else { "false" }, groups,
            if full { 16 } else { 0 }, total.records, total.tails, total.tails,
            total.charge, total.charge, total.key_guards, total.terminal_guards,
            total.witness_profile_replays, total.literal_cycle_checks, elapsed);
        let temporary = format!("{}.tmp", output);
        std::fs::write(&temporary, &text).unwrap();
        rename(&temporary, &output).unwrap();
        print!("{text}");
    }
}

fn main() { run::run_main(); }
