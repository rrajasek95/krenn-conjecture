mod run {
    #![allow(dead_code)]
    include!("../unaudited-codex-orbit0-k19-profile-census-2026-08-23/run_k19_profile_census.rs");

    use std::fs::metadata;
    use std::io::{BufReader, Read, Seek, SeekFrom};

    const K19: &str = "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/";
    const K4_PATH: &str = "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin";
    const CYCLE_PATH: &str = "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin";
    const RESULT_PATH: &str = "computations/unaudited-codex-orbit0-k21-profile-ready-charge-2026-08-24/results_k21_profile_ready_charge.raw.json";
    const U: i128 = 400_591_699_200;
    const OLD_SCALE: i128 = (SCALE as i128) * (SCALE as i128);
    const SCALE_RATIO: i128 = OLD_SCALE / U;
    const WORKERS: usize = 8;
    const GATE_SECONDS: f64 = 600.0;
    const WEIGHT_HEADER: u64 = 16;
    const WEIGHT_RECORD: u64 = 59;
    const PROFILE_RECORD: u64 = 104;

    const K14_K4_PROFILE: &str = "computations/unaudited-codex-orbit0-k18-k14-full-profiles-2026-08-23/k14_k4_enriched_profiles.bin";
    const K15_K3_PROFILE: &str = "computations/unaudited-codex-orbit0-k15-k3-full-export-plan-2026-08-23/checkpoint_k15_k3_profiles_merged.bin";
    const K16_K2_PROFILE: &str = "computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23/checkpoint_k16_k2_profiles_merged.bin";

    #[derive(Clone, Copy, Default)]
    struct Q {
        records: u64,
        full_n: u64,
        irr_n: u64,
        full_charge: i128,
        irr_charge: i128,
        signed_weight: i128,
        l1_weight: i128,
        uses: u64,
        full_occurrences: u64,
        irr_occurrences: u64,
        key_guards: u64,
        witness_profile_replays: u64,
        literal_cycle_checks: u64,
    }

    impl Q {
        fn add(&mut self, x: Q) {
            self.records += x.records;
            self.full_n += x.full_n;
            self.irr_n += x.irr_n;
            self.full_charge += x.full_charge;
            self.irr_charge += x.irr_charge;
            self.signed_weight += x.signed_weight;
            self.l1_weight += x.l1_weight;
            self.uses += x.uses;
            self.full_occurrences += x.full_occurrences;
            self.irr_occurrences += x.irr_occurrences;
            self.key_guards += x.key_guards;
            self.witness_profile_replays += x.witness_profile_replays;
            self.literal_cycle_checks += x.literal_cycle_checks;
        }
    }

    #[derive(Clone)]
    struct Aux {
        tails: Vec<Vec<Vec<[u8; 4]>>>,
        tail_edges: Vec<Vec<Vec<[[u8; 2]; 4]>>>,
        dual: HashMap<[u8; 13], i64>,
    }

    #[derive(Clone, Copy, Eq, Hash, PartialEq)]
    struct IKey {
        sig: [u8; 12],
        pivot: u8,
        degree: u8,
    }

    #[derive(Clone, Copy)]
    struct Bounds {
        first: Option<Key>,
        last: Option<Key>,
    }

    #[derive(Clone, Copy)]
    enum ProfileKind { K14, K15, K16 }

    #[derive(Clone, Copy)]
    struct ProfileSpec {
        name: &'static str,
        path: &'static str,
        kind: ProfileKind,
        header: u64,
        expected_records: u64,
        expected_uses: u64,
        expected_weight: i128,
        target_degree: u8,
    }

    fn i128le(x: &[u8]) -> i128 { i128::from_le_bytes(x.try_into().unwrap()) }
    fn u64x(x: &[u8]) -> u64 { u64::from_le_bytes(x.try_into().unwrap()) }

    fn load_aux(e: &E) -> Aux {
        let mut tails = vec![vec![Vec::new(); 5]; 78];
        for p in 0..78 {
            tails[p][2] = e.tails[p][0].clone();
            tails[p][3] = e.tails[p][1].clone();
        }
        let b = read(K4_PATH).unwrap();
        assert_eq!(&b[..7], b"K18K4A1");
        let mut at = 7;
        for p in 0..78 {
            for _ in 0..60 {
                let mut t = [0u8; 4];
                t.copy_from_slice(&b[at..at + 4]);
                at += 4;
                tails[p][4].push(t);
            }
        }
        assert_eq!(at, b.len());
        assert!(tails.iter().all(|x| x[2].len() == 12 && x[3].len() == 32 && x[4].len() == 60));

        let mut tail_edges = vec![vec![Vec::new(); 5]; 78];
        for p in 0..78 {
            let mut label = [255u8; 24];
            for (i, &c) in e.anchors[p].iter().enumerate() {
                let [u, v, a, b] = e.cells[c as usize];
                label[(3 * u + a) as usize] = (2 * i) as u8;
                label[(3 * v + b) as usize] = (2 * i + 1) as u8;
            }
            for degree in 2..=4 {
                for tail in &tails[p][degree] {
                    let mut edges = [[0u8; 2]; 4];
                    for (i, &c) in tail.iter().enumerate() {
                        let [u, v, a, b] = e.cells[c as usize];
                        let x = label[(3 * u + a) as usize];
                        let y = label[(3 * v + b) as usize];
                        assert!(x < 8 && y < 8 && x != y);
                        edges[i] = [x, y];
                    }
                    tail_edges[p][degree].push(edges);
                }
            }
        }

        let c = read(CYCLE_PATH).unwrap();
        assert_eq!(&c[..8], b"K17CYC1\0");
        let mut z = 8 + 252 * 4;
        let n = u32le(&c[z..z + 4]) as usize;
        z += 4;
        let mut dual = HashMap::new();
        for _ in 0..n {
            let mut k = [0u8; 13];
            k.copy_from_slice(&c[z..z + 13]);
            z += 13;
            let v = i64::from_le_bytes(c[z..z + 8].try_into().unwrap());
            z += 8;
            assert!(dual.insert(k, v).is_none());
        }
        assert_eq!(z, c.len());
        Aux { tails, tail_edges, dual }
    }

    fn row_cycle(row: &Row, e: &E) -> [u8; 13] {
        let mut adj = [[0u8; 2]; 24];
        let mut deg = [0usize; 24];
        for &c in &row.0 {
            let [u, v, a, b] = e.cells[c as usize];
            let x = (3 * u + a) as usize;
            let y = (3 * v + b) as usize;
            assert!(deg[x] < 2 && deg[y] < 2);
            adj[x][deg[x]] = y as u8; deg[x] += 1;
            adj[y][deg[y]] = x as u8; deg[y] += 1;
        }
        assert!(deg.iter().all(|&d| d == 2));
        let mut seen = [false; 24];
        let mut parts = [0u8; 12];
        let mut n = 0usize;
        for st in 0..24 {
            if seen[st] { continue; }
            let mut stack = [0u8; 24];
            stack[0] = st as u8;
            let (mut top, mut len) = (1usize, 0u8);
            seen[st] = true;
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
        let mut deg = [0usize; 8];
        let mut edge = |a: usize, b: usize, weight: u8| {
            assert!(a < 8 && b < 8 && a != b && deg[a] < 2 && deg[b] < 2);
            adj[a][deg[a]] = (b as u8, weight); deg[a] += 1;
            adj[b][deg[b]] = (a as u8, weight); deg[b] += 1;
        };
        for a in 0..8 {
            let b = k.profile[a] as usize;
            if a < b { edge(a, b, k.profile[8 + a]); }
        }
        for &[a, b] in tail { edge(a as usize, b as usize, 1); }
        assert!(deg.iter().all(|&x| x == 2));

        let mut parts = [0u8; 12];
        let nc = k.profile[16] as usize;
        parts[..nc].copy_from_slice(&k.profile[17..17 + nc]);
        let mut n = nc;
        let mut seen = [false; 8];
        for st in 0..8 {
            if seen[st] { continue; }
            let mut stack = [0u8; 8];
            stack[0] = st as u8;
            let (mut top, mut open_length_twice) = (1usize, 0u16);
            seen[st] = true;
            while top > 0 {
                top -= 1;
                let x = stack[top] as usize;
                for &(y, weight) in &adj[x] {
                    open_length_twice += weight as u16;
                    if !seen[y as usize] {
                        seen[y as usize] = true;
                        stack[top] = y;
                        top += 1;
                    }
                }
            }
            assert_eq!(open_length_twice % 2, 0);
            parts[n] = (open_length_twice / 2) as u8;
            n += 1;
        }
        parts[..n].sort_unstable();
        let mut out = [0u8; 13];
        out[0] = n as u8;
        out[1..1 + n].copy_from_slice(&parts[..n]);
        out
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

    fn is_available(s: [u8; 12], e: &E) -> bool {
        e.piv.iter().any(|p| (0..12).all(|i| s[i] >= p[i]))
    }

    fn irr_mask(k: &Key, e: &E, aux: &Aux) -> u64 {
        let p = k.pivot as usize;
        let degree = k.degree as usize;
        let mut mask = 0u64;
        for (i, tail) in aux.tails[p][degree].iter().enumerate() {
            let child = child_sig(k.sig, p, tail, e);
            if !is_available(child, e) { mask |= 1u64 << i; }
        }
        mask
    }

    fn eval(k: &Key, weight: i128, uses: Option<u64>, e: &E, aux: &Aux,
            masks: &mut HashMap<IKey, u64>) -> Q {
        let p = k.pivot as usize;
        let degree = k.degree as usize;
        let ik = IKey { sig: k.sig, pivot: k.pivot, degree: k.degree };
        let mask = *masks.entry(ik).or_insert_with(|| irr_mask(k, e, aux));
        let mut q = Q::default();
        q.records = 1;
        q.signed_weight = weight;
        q.l1_weight = weight.abs();
        if let Some(u) = uses { q.uses = u; }
        for (i, edges) in aux.tail_edges[p][degree].iter().enumerate() {
            let charge = *aux.dual.get(&key_cycle_edges(k, edges)).unwrap_or(&0) as i128;
            q.full_n += 1;
            q.full_charge += weight * charge;
            if let Some(u) = uses { q.full_occurrences += u; }
            if mask & (1u64 << i) != 0 {
                q.irr_n += 1;
                q.irr_charge += weight * charge;
                if let Some(u) = uses { q.irr_occurrences += u; }
            }
        }
        q
    }

    fn literal_selftest(e: &E, aux: &Aux) -> u64 {
        let mut n = 0u64;
        for r in e.records.iter().take(8) {
            for a in e.factor[0][0].iter().take(4) {
                for b in e.factor[1][0].iter().take(4) {
                    for c in e.factor[2][0].iter().take(4) {
                        let row = make(r, a, b, c);
                        let s = sig(&row, e);
                        for p in avail(s, e) {
                            let mut k = Key { profile: profile(&row, p, e), sig: s, pivot: p as u8, degree: 2 };
                            profile_guard(&k);
                            for degree in 2..=4 {
                                k.degree = degree as u8;
                                for i in (0..aux.tails[p][degree].len()).step_by(7) {
                                    let literal = replace(&row, &e.anchors[p], &aux.tails[p][degree][i]);
                                    assert_eq!(key_cycle_edges(&k, &aux.tail_edges[p][degree][i]), row_cycle(&literal, e));
                                    n += 1;
                                }
                            }
                        }
                    }
                }
            }
        }
        assert_eq!(n, 83_968);
        n
    }

    fn weight_worker(path: &'static str, target_degree: u8, e: Arc<E>, aux: Arc<Aux>,
                     start: u64, end: u64, begun: Arc<Instant>) -> (Q, Bounds) {
        let mut file = File::open(path).unwrap();
        file.seek(SeekFrom::Start(WEIGHT_HEADER + WEIGHT_RECORD * start)).unwrap();
        let mut reader = BufReader::with_capacity(2 << 20, file);
        let mut q = Q::default();
        let mut masks = HashMap::new();
        let mut first = None;
        let mut last = None;
        for index in start..end {
            let mut z = [0u8; WEIGHT_RECORD as usize];
            reader.read_exact(&mut z).unwrap();
            let mut pr = [0u8; 29]; pr.copy_from_slice(&z[..29]);
            let mut sg = [0u8; 12]; sg.copy_from_slice(&z[29..41]);
            let stored = Key { profile: pr, sig: sg, pivot: z[41], degree: z[42] };
            assert_eq!(stored.degree, 2);
            if let Some(p) = last { assert!(p < stored); } else { first = Some(stored); }
            last = Some(stored);
            assert!((stored.pivot as usize) < e.anchors.len());
            assert!(avail(stored.sig, &e).contains(&(stored.pivot as usize)));
            profile_guard(&stored);
            let old = i128le(&z[43..59]);
            assert_ne!(old, 0);
            assert_eq!(old % SCALE_RATIO, 0);
            let weight = old / SCALE_RATIO;
            assert_ne!(weight, 0);
            let mut target = stored;
            target.degree = target_degree;
            q.add(eval(&target, weight, None, &e, &aux, &mut masks));
            q.key_guards += 1;
            if index % 250_000 == 0 { assert!(begun.elapsed().as_secs_f64() < GATE_SECONDS); }
        }
        (q, Bounds { first, last })
    }

    fn read_weight_group(name: &str, path: &'static str, target_degree: u8,
                         e: Arc<E>, aux: Arc<Aux>, begun: Arc<Instant>) -> Q {
        let mut h = [0u8; WEIGHT_HEADER as usize];
        File::open(path).unwrap().read_exact(&mut h).unwrap();
        assert_eq!(&h[..8], b"K19SUM1\0");
        let n = u64x(&h[8..16]);
        assert_eq!(metadata(path).unwrap().len(), WEIGHT_HEADER + WEIGHT_RECORD * n);
        assert!(target_degree == 3 || target_degree == 4);
        let mut jobs = Vec::new();
        for worker in 0..WORKERS {
            let start = n * worker as u64 / WORKERS as u64;
            let end = n * (worker as u64 + 1) / WORKERS as u64;
            let ee = e.clone(); let aa = aux.clone(); let bb = begun.clone();
            jobs.push(thread::spawn(move || weight_worker(path, target_degree, ee, aa, start, end, bb)));
        }
        let mut parts = Vec::new();
        for job in jobs { parts.push(job.join().unwrap()); }
        for i in 1..parts.len() { assert!(parts[i - 1].1.last.unwrap() < parts[i].1.first.unwrap()); }
        let mut total = Q::default();
        for (q, _) in parts { total.add(q); }
        assert_eq!(total.records, n);
        assert_eq!(total.key_guards, n);
        assert_eq!(total.full_n, n * aux.tails[0][target_degree as usize].len() as u64);
        eprintln!("PASS {name} records={} full={} irr={} charge={} irr_charge={}",
                  total.records, total.full_n, total.irr_n, total.full_charge, total.irr_charge);
        total
    }

    fn profile_header(spec: ProfileSpec) {
        let mut h = vec![0u8; spec.header as usize];
        File::open(spec.path).unwrap().read_exact(&mut h).unwrap();
        match spec.kind {
            ProfileKind::K14 => {
                assert_eq!(&h[..8], b"K14MRG1\0");
                assert_eq!(u64x(&h[8..16]) as i128, U);
                assert_eq!(u64x(&h[16..24]), 490);
                assert_eq!(u64x(&h[24..32]), 120_812_123);
                assert_eq!(u64x(&h[56..64]), spec.expected_records);
                assert_eq!(u64x(&h[72..80]), spec.expected_uses);
                assert_eq!(i128le(&h[40..56]), i128le(&h[80..96]));
                assert_eq!(i128le(&h[80..96]), spec.expected_weight);
                assert!(h[96..].iter().all(|&x| x == 0));
            }
            ProfileKind::K15 | ProfileKind::K16 => {
                let magic = match spec.kind { ProfileKind::K15 => b"K15MRG1\0", ProfileKind::K16 => b"K16MRG1\0", _ => unreachable!() };
                assert_eq!(&h[..8], magic);
                assert_eq!(u32le(&h[8..12]), 1);
                assert_eq!(u16::from_le_bytes(h[12..14].try_into().unwrap()) as u64, PROFILE_RECORD);
                assert_eq!(i128le(&h[16..32]), U);
                assert_eq!(u64x(&h[56..64]), spec.expected_records);
                assert_eq!(u64x(&h[72..80]), spec.expected_uses);
                assert_eq!(i128le(&h[80..96]), i128le(&h[96..112]));
                assert_eq!(i128le(&h[96..112]), spec.expected_weight);
            }
        }
        assert_eq!(metadata(spec.path).unwrap().len(), spec.header + PROFILE_RECORD * spec.expected_records);
    }

    fn profile_worker(spec: ProfileSpec, e: Arc<E>, aux: Arc<Aux>, start: u64, end: u64,
                      begun: Arc<Instant>) -> (Q, Bounds) {
        let mut file = File::open(spec.path).unwrap();
        file.seek(SeekFrom::Start(spec.header + PROFILE_RECORD * start)).unwrap();
        let mut reader = BufReader::with_capacity(2 << 20, file);
        let mut q = Q::default();
        let mut masks = HashMap::new();
        let mut first = None;
        let mut last = None;
        for index in start..end {
            let mut z = [0u8; PROFILE_RECORD as usize];
            reader.read_exact(&mut z).unwrap();
            let mut pr = [0u8; 29]; pr.copy_from_slice(&z[..29]);
            let mut sg = [0u8; 12]; sg.copy_from_slice(&z[29..41]);
            let order_key = Key { profile: pr, sig: sg, pivot: z[41], degree: 2 };
            if let Some(p) = last { assert!(p < order_key); } else { first = Some(order_key); }
            last = Some(order_key);
            let weight = i128le(&z[42..58]);
            let uses = u64x(&z[58..66]);
            assert_ne!(weight, 0);
            assert!(uses > 0);
            assert!((order_key.pivot as usize) < e.anchors.len());
            assert!(avail(order_key.sig, &e).contains(&(order_key.pivot as usize)));
            profile_guard(&order_key);

            let mut cells = [0u8; 24]; cells.copy_from_slice(&z[66..90]);
            let row = Row(cells);
            assert!(row.0.windows(2).all(|x| x[0] <= x[1]));
            assert_eq!(sig(&row, &e), order_key.sig);
            assert_eq!(profile(&row, order_key.pivot as usize, &e), order_key.profile);
            let source = u64x(&z[90..98]);
            let p1 = z[98] as usize;
            let tail1 = z[99] as usize;
            let p2 = z[100] as usize;
            let m1 = z[101] as i128;
            let m2 = z[102] as usize;
            let packet = z[103];
            assert_eq!(p2, order_key.pivot as usize);
            assert_eq!(avail(order_key.sig, &e).len(), m2);
            assert!(m1 > 0 && m2 > 0 && U % (m1 * m2 as i128) == 0);
            match spec.kind {
                ProfileKind::K14 => { assert!(source < 485 && p1 < 78 && tail1 < 60); assert_eq!(packet, 0); }
                ProfileKind::K15 => { assert!(source < 485 && p1 < 78 && tail1 < 32); assert!(packet < 3); }
                ProfileKind::K16 => { assert!(source < 24_097_095 && p1 < 78 && tail1 < 12); assert_eq!(packet, 255); }
            }

            let mut target = order_key;
            target.degree = spec.target_degree;
            q.add(eval(&target, weight, Some(uses), &e, &aux, &mut masks));
            q.key_guards += 1;
            q.witness_profile_replays += 1;
            if index == start || index + 1 == end || index % 100_000 == 0 {
                let degree = spec.target_degree as usize;
                for i in (0..aux.tails[p2][degree].len()).step_by(7) {
                    let literal = replace(&row, &e.anchors[p2], &aux.tails[p2][degree][i]);
                    assert_eq!(key_cycle_edges(&target, &aux.tail_edges[p2][degree][i]), row_cycle(&literal, &e));
                    q.literal_cycle_checks += 1;
                }
            }
            if index % 250_000 == 0 { assert!(begun.elapsed().as_secs_f64() < GATE_SECONDS); }
        }
        (q, Bounds { first, last })
    }

    fn read_profile_group(spec: ProfileSpec, e: Arc<E>, aux: Arc<Aux>, begun: Arc<Instant>) -> Q {
        profile_header(spec);
        let n = spec.expected_records;
        let mut jobs = Vec::new();
        for worker in 0..WORKERS {
            let start = n * worker as u64 / WORKERS as u64;
            let end = n * (worker as u64 + 1) / WORKERS as u64;
            let ee = e.clone(); let aa = aux.clone(); let bb = begun.clone();
            jobs.push(thread::spawn(move || profile_worker(spec, ee, aa, start, end, bb)));
        }
        let mut parts = Vec::new();
        for job in jobs { parts.push(job.join().unwrap()); }
        for i in 1..parts.len() { assert!(parts[i - 1].1.last.unwrap() < parts[i].1.first.unwrap()); }
        let mut total = Q::default();
        for (q, _) in parts { total.add(q); }
        assert_eq!(total.records, n);
        assert_eq!(total.key_guards, n);
        assert_eq!(total.witness_profile_replays, n);
        assert_eq!(total.uses, spec.expected_uses);
        assert_eq!(total.signed_weight, spec.expected_weight);
        assert_eq!(total.full_n, n * aux.tails[0][spec.target_degree as usize].len() as u64);
        assert_eq!(total.full_occurrences, spec.expected_uses * aux.tails[0][spec.target_degree as usize].len() as u64);
        eprintln!("PASS {} records={} full={} irr={} charge={} irr_charge={} literal_cycles={}",
                  spec.name, total.records, total.full_n, total.irr_n,
                  total.full_charge, total.irr_charge, total.literal_cycle_checks);
        total
    }

    fn json_group(name: &str, ids: &str, path: &str, source_format: &str,
                  stored_degree: u8, target_degree: u8, q: Q, has_uses: bool) -> String {
        let uses = if has_uses { q.uses.to_string() } else { "null".to_string() };
        let full_occ = if has_uses { q.full_occurrences.to_string() } else { "null".to_string() };
        let irr_occ = if has_uses { q.irr_occurrences.to_string() } else { "null".to_string() };
        format!(concat!(
            "{{\"name\":\"{}\",\"ids\":{},\"source_profile\":\"{}\",\"source_format\":\"{}\"," ,
            "\"stored_degree\":{},\"target_degree\":{},\"profile_records\":{},\"profile_tail_evaluations\":{},",
            "\"irreducible_profile_tail_evaluations\":{},\"input_profile_uses\":{},",
            "\"full_source_occurrences\":{},\"irreducible_source_occurrences\":{},",
            "\"input_weight_scaled_U\":\"{}\",\"l1_weight_scaled_U\":\"{}\",",
            "\"full_77_charge_scaled_U\":\"{}\",\"irreducible_77_charge_scaled_U\":\"{}\",",
            "\"exhaustive_key_guards\":{},\"literal_witness_profile_replays\":{},",
            "\"literal_profile_cycle_comparisons\":{},\"individual_id_charges\":{}}}"),
            name, ids, path, source_format, stored_degree, target_degree, q.records,
            q.full_n, q.irr_n, uses, full_occ, irr_occ, q.signed_weight, q.l1_weight,
            q.full_charge, q.irr_charge, q.key_guards, q.witness_profile_replays,
            q.literal_cycle_checks, if ids.matches(',').count() == 0 { "\"equal_to_group_scalar\"" } else { "null" })
    }

    pub fn run_main() {
        assert_eq!(OLD_SCALE, 79_412_096_674_310_400);
        assert_eq!(OLD_SCALE % U, 0);
        assert_eq!(SCALE_RATIO, 198_237);
        let begun = Arc::new(Instant::now());
        let e = Arc::new(parse());
        let aux = Arc::new(load_aux(&e));
        let global_literal = literal_selftest(&e, &aux);
        eprintln!("PASS global literal profile/cycle comparisons={global_literal}");

        let weight_k14 = read_weight_group("D14_R3_to_K4", concat!("computations/unaudited-codex-orbit0-k19-charge-2026-08-23/", "weights_k17_k14_k2.bin"), 4, e.clone(), aux.clone(), begun.clone());
        let profile_k14 = read_profile_group(ProfileSpec {
            name: "D14_R4_to_K3", path: K14_K4_PROFILE, kind: ProfileKind::K14,
            header: 256, expected_records: 18_217_226, expected_uses: 886_145_203,
            expected_weight: 496_321_127_773_883_596_800, target_degree: 3,
        }, e.clone(), aux.clone(), begun.clone());
        let weight_k15 = read_weight_group("D15_R2_to_K4", concat!("computations/unaudited-codex-orbit0-k19-charge-2026-08-23/", "weights_k17_k15_k2.bin"), 4, e.clone(), aux.clone(), begun.clone());
        let profile_k15 = read_profile_group(ProfileSpec {
            name: "D15_R3_to_K3", path: K15_K3_PROFILE, kind: ProfileKind::K15,
            header: 128, expected_records: 25_564_391, expected_uses: 2_311_887_188,
            expected_weight: 1_865_098_870_468_588_339_200, target_degree: 3,
        }, e.clone(), aux.clone(), begun.clone());
        let profile_k16 = read_profile_group(ProfileSpec {
            name: "D16_R2_to_K3", path: K16_K2_PROFILE, kind: ProfileKind::K16,
            header: 128, expected_records: 6_876_260, expected_uses: 1_604_299_948,
            expected_weight: 3_218_269_567_887_566_438_400, target_degree: 3,
        }, e.clone(), aux.clone(), begun.clone());

        let groups = [weight_k14, profile_k14, weight_k15, profile_k15, profile_k16];
        let mut total = Q::default();
        for q in groups { total.add(q); }
        let covered = concat!(
            "[\"D14:222|R:3-4\",\"D14:222|R:4-3\",",
            "\"D15:223|R:2-4\",\"D15:232|R:2-4\",\"D15:322|R:2-4\",",
            "\"D15:223|R:3-3\",\"D15:232|R:3-3\",\"D15:322|R:3-3\",",
            "\"D16:224|R:2-3\",\"D16:233|R:2-3\",\"D16:242|R:2-3\",",
            "\"D16:323|R:2-3\",\"D16:332|R:2-3\",\"D16:422|R:2-3\"]");
        let ids1 = "[\"D14:222|R:3-4\"]";
        let ids2 = "[\"D14:222|R:4-3\"]";
        let ids3 = "[\"D15:223|R:2-4\",\"D15:232|R:2-4\",\"D15:322|R:2-4\"]";
        let ids4 = "[\"D15:223|R:3-3\",\"D15:232|R:3-3\",\"D15:322|R:3-3\"]";
        let ids5 = "[\"D16:224|R:2-3\",\"D16:233|R:2-3\",\"D16:242|R:2-3\",\"D16:323|R:2-3\",\"D16:332|R:2-3\",\"D16:422|R:2-3\"]";
        let json_groups = [
            json_group("D14_R3_to_K4", ids1, &format!("{}weights_k17_k14_k2.bin", K19), "K19SUM1", 2, 4, weight_k14, false),
            json_group("D14_R4_to_K3", ids2, K14_K4_PROFILE, "K14MRG1", 4, 3, profile_k14, true),
            json_group("D15_R2_to_K4", ids3, &format!("{}weights_k17_k15_k2.bin", K19), "K19SUM1", 2, 4, weight_k15, false),
            json_group("D15_R3_to_K3", ids4, K15_K3_PROFILE, "K15MRG1", 3, 3, profile_k15, true),
            json_group("D16_R2_to_K3", ids5, K16_K2_PROFILE, "K16MRG1", 2, 3, profile_k16, true),
        ];
        let elapsed = begun.elapsed().as_secs_f64();
        assert!(elapsed < GATE_SECONDS);
        let text = format!(concat!(
            "{{\n  \"status\":\"PASS_EXACT_K21_14_PROFILE_READY_77_CHARGE_SUBTOTAL\",\n",
            "  \"scale_U\":\"{}\",\n  \"old_weight_scale\":\"{}\",\n  \"weight_scale_ratio\":{},\n",
            "  \"workers\":{},\n  \"coverage\":{{\"covered_count\":14,\"covered_ids\":{},\"strict_exact_set_guard\":true}},\n",
            "  \"groups\":[{}],\n",
            "  \"subtotal\":{{\"covered_DAG_paths\":14,\"profile_records\":{},\"profile_tail_evaluations\":{},",
            "\"irreducible_profile_tail_evaluations\":{},\"full_77_charge_scaled_U\":\"{}\",",
            "\"irreducible_77_charge_scaled_U\":\"{}\",\"exhaustive_key_guards\":{},",
            "\"literal_witness_profile_replays\":{},\"literal_profile_cycle_comparisons\":{}}},\n",
            "  \"global_literal_profile_cycle_selftest\":{},\n",
            "  \"individual_id_guard\":\"The D15 three-ID and D16 six-ID producers preaggregated weights; their exact group subtotals cannot be split source-faithfully.\",\n",
            "  \"scope\":\"exact charge for only the 14 named profile-ready derived K21 lineages from five frozen source-compressed interfaces; no row collection, no other K21 lineages, no K22/K23/K24 tails, and no membership or conjecture claim\",\n",
            "  \"elapsed_seconds\":{:.6}\n}}\n"),
            U, OLD_SCALE, SCALE_RATIO, WORKERS, covered, json_groups.join(",\n    "),
            total.records, total.full_n, total.irr_n, total.full_charge, total.irr_charge,
            total.key_guards, total.witness_profile_replays,
            total.literal_cycle_checks + global_literal, global_literal, elapsed);
        let tmp = format!("{}.tmp", RESULT_PATH);
        std::fs::write(&tmp, &text).unwrap();
        rename(&tmp, RESULT_PATH).unwrap();
        print!("{text}");
    }
}

fn main() { run::run_main(); }
