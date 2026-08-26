// Exact prefix/interval producer for the two hidden-decorated K23 sinks.

const K23_PAIR_INPUT: &str = "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin";
const K23_PAIR_SHA256: &str = "22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8";
const K23_MAGIC: &[u8; 8] = b"H16ORM1\0";
const K23_HEADER: usize = 80;
const K23_RECORD: usize = 53;
const K23_RECORDS: u64 = 101_545_723;
const K23_PAIR_WEIGHT_SUM: i128 = 146_230_609_431_055_564_800;
const K23_PAIR_USES: u64 = 511_214_060;
const K23_CACHE_CAP: usize = 300_000;
const K23_MAX_NEW_KEYS_PER_PAIR: usize = 720;

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct K23PairKey { row: Row, pivot: u8 }

#[derive(Clone, Copy, Debug)]
struct K23Pair {
    key: K23PairKey,
    weight_after_p2: i128,
    uses: u64,
    orbit: u16,
    stabilizer: u16,
}

#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
struct K23Delta {
    first_children: u64,
    pivotable_intermediate: u64,
    selected_p3: u64,
    terminal_children: u64,
    pivotable_weight: i128,
    normalized_weight: i128,
    terminal_weight: i128,
    charge: i128,
}

impl K23Delta {
    fn add(&mut self, x: Self) {
        self.first_children += x.first_children;
        self.pivotable_intermediate += x.pivotable_intermediate;
        self.selected_p3 += x.selected_p3;
        self.terminal_children += x.terminal_children;
        self.pivotable_weight += x.pivotable_weight;
        self.normalized_weight += x.normalized_weight;
        self.terminal_weight += x.terminal_weight;
        self.charge += x.charge;
    }
}

#[derive(Default)]
struct K23Worker {
    start: u64,
    end: u64,
    records: u64,
    uses: u64,
    pair_weight: i128,
    first: Option<K23PairKey>,
    last: Option<K23PairKey>,
    d34: K23Delta,
    d43: K23Delta,
    hits34: u64,
    misses34: u64,
    clears34: u64,
    peak34: usize,
    hits43: u64,
    misses43: u64,
    clears43: u64,
    peak43: usize,
    stabilizers: std::collections::BTreeMap<u16, u64>,
    divisors34: std::collections::BTreeMap<(u8, u8), u64>,
    divisors43: std::collections::BTreeMap<(u8, u8), u64>,
    samples: Vec<(u64, String)>,
}

fn k23_decode(rec: &[u8; K23_RECORD]) -> K23Pair {
    let mut row = [0u8; 24];
    row.copy_from_slice(&rec[..24]);
    K23Pair {
        key: K23PairKey { row: Row(row), pivot: rec[24] },
        weight_after_p2: i128::from_le_bytes(rec[25..41].try_into().unwrap()),
        uses: u64::from_le_bytes(rec[41..49].try_into().unwrap()),
        orbit: u16::from_le_bytes(rec[49..51].try_into().unwrap()),
        stabilizer: u16::from_le_bytes(rec[51..53].try_into().unwrap()),
    }
}

fn k23_validate_pair(x: K23Pair, e: &Engine) -> ([u8; 12], u8) {
    assert!(x.key.row.0.windows(2).all(|w| w[0] <= w[1]));
    assert_ne!(x.weight_after_p2, 0);
    assert!(x.uses > 0);
    assert_eq!((x.orbit as u32) * (x.stabilizer as u32), 384);
    let sig = signature(&x.key.row.0, e);
    let pivots = available(sig, e);
    assert!(pivots.contains(&(x.key.pivot as usize)));
    assert!(!pivots.is_empty() && pivots.len() < 256);
    (sig, pivots.len() as u8)
}

fn k23_response4(key: PKey, e: &Engine, c: &CEnv) -> Resp {
    let mut out = Resp::default();
    for tail in &c.k4[key.pivot as usize] {
        let sig23 = child_sig(key.sig, key.pivot as usize, tail, e);
        assert!(!pivotable_sig(sig23, e), "terminal K4 response remained pivotable at K23");
        let ck = abstract_ckey(&key.profile, key.pivot as usize, tail, e, c);
        out.full_n += 1;
        out.full_q += *c.dual.get(&ck).unwrap_or(&0);
    }
    assert_eq!(out.full_n, 60);
    out.irr_n = out.full_n;
    out.irr_q = out.full_q;
    out
}

fn k23_response3(key: PKey, e: &Engine, c: &CEnv) -> Resp {
    let mut out = Resp::default();
    for tail in &e.all_k3[key.pivot as usize] {
        let sig23 = child_sig(key.sig, key.pivot as usize, tail, e);
        assert!(!pivotable_sig(sig23, e), "terminal K3 response remained pivotable at K23");
        let ck = abstract_ckey(&key.profile, key.pivot as usize, tail, e, c);
        out.full_n += 1;
        out.full_q += *c.dual.get(&ck).unwrap_or(&0);
    }
    assert_eq!(out.full_n, 32);
    out.irr_n = out.full_n;
    out.irr_q = out.full_q;
    out
}

fn k23_eval34_cached(
    x: K23Pair, e: &Engine, c: &CEnv, cache: &mut HashMap<PKey, Resp>,
    hits: &mut u64, misses: &mut u64,
    divisors: &mut std::collections::BTreeMap<(u8, u8), u64>,
) -> K23Delta {
    let (sig16, m2) = k23_validate_pair(x, e);
    let p2 = x.key.pivot as usize;
    let mut out = K23Delta::default();
    for tail3 in &e.all_k3[p2] {
        out.first_children += 1;
        let sig19 = child_sig(sig16, p2, tail3, e);
        let pivots3 = available(sig19, e);
        if pivots3.is_empty() { continue; }
        let row19 = replace_anchor(&x.key.row, &e.anchors[p2], tail3);
        assert_eq!(signature(&row19.0, e), sig19);
        let m3 = pivots3.len();
        assert_eq!(U % ((m2 as i128) * (m3 as i128)), 0);
        assert_eq!(x.weight_after_p2 % (m3 as i128), 0);
        let w3 = -x.weight_after_p2 / (m3 as i128);
        out.pivotable_intermediate += 1;
        out.pivotable_weight += x.weight_after_p2;
        *divisors.entry((m2, m3 as u8)).or_default() += 1;
        for p3 in pivots3 {
            out.selected_p3 += 1;
            out.normalized_weight += w3;
            let key = PKey { profile: path_profile(&row19, p3, e, c), sig: sig19, pivot: p3 as u8 };
            let response = if let Some(z) = cache.get(&key) {
                *hits += 1; *z
            } else {
                *misses += 1;
                let z = k23_response4(key, e, c);
                cache.insert(key, z);
                z
            };
            assert_eq!((response.full_n, response.irr_n), (60, 60));
            assert_eq!(response.full_q, response.irr_q);
            out.terminal_children += response.full_n;
            out.terminal_weight += w3 * response.full_n as i128;
            out.charge += w3 * response.full_q as i128;
        }
    }
    assert_eq!(out.first_children, 32);
    assert_eq!(out.terminal_children, 60 * out.selected_p3);
    assert_eq!(out.normalized_weight, -out.pivotable_weight);
    assert_eq!(out.terminal_weight, 60 * out.normalized_weight);
    out
}

fn k23_eval43_cached(
    x: K23Pair, e: &Engine, c: &CEnv, cache: &mut HashMap<PKey, Resp>,
    hits: &mut u64, misses: &mut u64,
    divisors: &mut std::collections::BTreeMap<(u8, u8), u64>,
) -> K23Delta {
    let (sig16, m2) = k23_validate_pair(x, e);
    let p2 = x.key.pivot as usize;
    let mut out = K23Delta::default();
    for tail4 in &c.k4[p2] {
        out.first_children += 1;
        let sig20 = child_sig(sig16, p2, tail4, e);
        let pivots3 = available(sig20, e);
        if pivots3.is_empty() { continue; }
        let row20 = replace_anchor(&x.key.row, &e.anchors[p2], tail4);
        assert_eq!(signature(&row20.0, e), sig20);
        let m3 = pivots3.len();
        assert_eq!(U % ((m2 as i128) * (m3 as i128)), 0);
        assert_eq!(x.weight_after_p2 % (m3 as i128), 0);
        let w3 = -x.weight_after_p2 / (m3 as i128);
        out.pivotable_intermediate += 1;
        out.pivotable_weight += x.weight_after_p2;
        *divisors.entry((m2, m3 as u8)).or_default() += 1;
        for p3 in pivots3 {
            out.selected_p3 += 1;
            out.normalized_weight += w3;
            let key = PKey { profile: path_profile(&row20, p3, e, c), sig: sig20, pivot: p3 as u8 };
            let response = if let Some(z) = cache.get(&key) {
                *hits += 1; *z
            } else {
                *misses += 1;
                let z = k23_response3(key, e, c);
                cache.insert(key, z);
                z
            };
            assert_eq!((response.full_n, response.irr_n), (32, 32));
            assert_eq!(response.full_q, response.irr_q);
            out.terminal_children += response.full_n;
            out.terminal_weight += w3 * response.full_n as i128;
            out.charge += w3 * response.full_q as i128;
        }
    }
    assert_eq!(out.first_children, 60);
    assert_eq!(out.terminal_children, 32 * out.selected_p3);
    assert_eq!(out.normalized_weight, -out.pivotable_weight);
    assert_eq!(out.terminal_weight, 32 * out.normalized_weight);
    out
}

fn k23_eval34_literal(x: K23Pair, e: &Engine, c: &CEnv) -> K23Delta {
    let (sig16, m2) = k23_validate_pair(x, e);
    let p2 = x.key.pivot as usize;
    let mut out = K23Delta::default();
    for tail3 in &e.all_k3[p2] {
        out.first_children += 1;
        let sig19 = child_sig(sig16, p2, tail3, e);
        let row19 = replace_anchor(&x.key.row, &e.anchors[p2], tail3);
        assert_eq!(signature(&row19.0, e), sig19);
        let pivots3 = available(sig19, e);
        if pivots3.is_empty() { continue; }
        let m3 = pivots3.len();
        assert_eq!(U % (m2 as i128 * m3 as i128), 0);
        assert_eq!(x.weight_after_p2 % m3 as i128, 0);
        let w3 = -x.weight_after_p2 / m3 as i128;
        out.pivotable_intermediate += 1;
        out.pivotable_weight += x.weight_after_p2;
        for p3 in pivots3 {
            out.selected_p3 += 1;
            out.normalized_weight += w3;
            let profile = path_profile(&row19, p3, e, c);
            for tail4 in &c.k4[p3] {
                let sig23 = child_sig(sig19, p3, tail4, e);
                assert!(!pivotable_sig(sig23, e));
                let row23 = replace_anchor(&row19, &e.anchors[p3], tail4);
                assert_eq!(signature(&row23.0, e), sig23);
                let literal = literal_ckey(&row23, c);
                assert_eq!(abstract_ckey(&profile, p3, tail4, e, c), literal);
                out.terminal_children += 1;
                out.terminal_weight += w3;
                out.charge += w3 * *c.dual.get(&literal).unwrap_or(&0) as i128;
            }
        }
    }
    assert_eq!(out.terminal_children, 60 * out.selected_p3);
    assert_eq!(out.normalized_weight, -out.pivotable_weight);
    assert_eq!(out.terminal_weight, 60 * out.normalized_weight);
    out
}

fn k23_eval43_literal(x: K23Pair, e: &Engine, c: &CEnv) -> K23Delta {
    let (sig16, m2) = k23_validate_pair(x, e);
    let p2 = x.key.pivot as usize;
    let mut out = K23Delta::default();
    for tail4 in &c.k4[p2] {
        out.first_children += 1;
        let sig20 = child_sig(sig16, p2, tail4, e);
        let row20 = replace_anchor(&x.key.row, &e.anchors[p2], tail4);
        assert_eq!(signature(&row20.0, e), sig20);
        let pivots3 = available(sig20, e);
        if pivots3.is_empty() { continue; }
        let m3 = pivots3.len();
        assert_eq!(U % (m2 as i128 * m3 as i128), 0);
        assert_eq!(x.weight_after_p2 % m3 as i128, 0);
        let w3 = -x.weight_after_p2 / m3 as i128;
        out.pivotable_intermediate += 1;
        out.pivotable_weight += x.weight_after_p2;
        for p3 in pivots3 {
            out.selected_p3 += 1;
            out.normalized_weight += w3;
            let profile = path_profile(&row20, p3, e, c);
            for tail3 in &e.all_k3[p3] {
                let sig23 = child_sig(sig20, p3, tail3, e);
                assert!(!pivotable_sig(sig23, e));
                let row23 = replace_anchor(&row20, &e.anchors[p3], tail3);
                assert_eq!(signature(&row23.0, e), sig23);
                let literal = literal_ckey(&row23, c);
                assert_eq!(abstract_ckey(&profile, p3, tail3, e, c), literal);
                out.terminal_children += 1;
                out.terminal_weight += w3;
                out.charge += w3 * *c.dual.get(&literal).unwrap_or(&0) as i128;
            }
        }
    }
    assert_eq!(out.terminal_children, 32 * out.selected_p3);
    assert_eq!(out.normalized_weight, -out.pivotable_weight);
    assert_eq!(out.terminal_weight, 32 * out.normalized_weight);
    out
}

fn k23_hex(row: &Row) -> String {
    row.0.iter().map(|x| format!("{:02x}", x)).collect()
}

fn k23_process(
    input: &str, start: u64, end: u64, sample_indices: &HashSet<u64>,
    cache_chunk: u64, e: Arc<Engine>, c: Arc<CEnv>,
) -> K23Worker {
    let mut out = K23Worker { start, end, ..K23Worker::default() };
    if start == end { return out; }
    let mut f = File::open(input).unwrap();
    f.seek(SeekFrom::Start(K23_HEADER as u64 + K23_RECORD as u64 * start)).unwrap();
    let mut reader = BufReader::with_capacity(8 << 20, f);
    let mut cache34: HashMap<PKey, Resp> = HashMap::new();
    let mut cache43: HashMap<PKey, Resp> = HashMap::new();
    let mut prior = None;
    for index in start..end {
        if index > start && (index - start) % cache_chunk == 0 {
            out.peak34 = out.peak34.max(cache34.len());
            out.peak43 = out.peak43.max(cache43.len());
            cache34.clear(); cache43.clear();
            out.clears34 += 1; out.clears43 += 1;
        }
        if cache34.len() >= K23_CACHE_CAP {
            out.peak34 = out.peak34.max(cache34.len()); cache34.clear(); out.clears34 += 1;
        }
        if cache43.len() >= K23_CACHE_CAP {
            out.peak43 = out.peak43.max(cache43.len()); cache43.clear(); out.clears43 += 1;
        }
        let mut rec = [0u8; K23_RECORD];
        reader.read_exact(&mut rec).unwrap();
        let pair = k23_decode(&rec);
        assert!(prior.map_or(true, |p| p < pair.key));
        prior = Some(pair.key);
        if out.first.is_none() { out.first = Some(pair.key); }
        out.last = Some(pair.key);
        out.records += 1;
        out.uses += pair.uses;
        out.pair_weight += pair.weight_after_p2;
        *out.stabilizers.entry(pair.stabilizer).or_default() += 1;
        let d34 = k23_eval34_cached(pair, &e, &c, &mut cache34, &mut out.hits34, &mut out.misses34, &mut out.divisors34);
        let d43 = k23_eval43_cached(pair, &e, &c, &mut cache43, &mut out.hits43, &mut out.misses43, &mut out.divisors43);
        assert!(cache34.len() <= K23_CACHE_CAP + K23_MAX_NEW_KEYS_PER_PAIR);
        assert!(cache43.len() <= K23_CACHE_CAP + K23_MAX_NEW_KEYS_PER_PAIR);
        out.d34.add(d34); out.d43.add(d43);
        if sample_indices.contains(&index) {
            assert_eq!(d34, k23_eval34_literal(pair, &e, &c));
            assert_eq!(d43, k23_eval43_literal(pair, &e, &c));
            out.samples.push((index, format!(
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                index, k23_hex(&pair.key.row), pair.key.pivot, pair.weight_after_p2,
                pair.uses, pair.orbit, pair.stabilizer, d34.first_children,
                d34.pivotable_intermediate, d34.selected_p3, d34.terminal_children,
                d34.terminal_weight, d34.charge, d43.first_children,
                d43.pivotable_intermediate, d43.selected_p3, d43.terminal_children,
                d43.terminal_weight, d43.charge,
                (d34.selected_p3 > 0) as u8, (d43.selected_p3 > 0) as u8,
            )));
        }
    }
    out.peak34 = out.peak34.max(cache34.len());
    out.peak43 = out.peak43.max(cache43.len());
    out
}

fn k23_merge(a: &mut K23Worker, x: K23Worker) {
    a.records += x.records; a.uses += x.uses; a.pair_weight += x.pair_weight;
    a.d34.add(x.d34); a.d43.add(x.d43);
    a.hits34 += x.hits34; a.misses34 += x.misses34; a.clears34 += x.clears34; a.peak34 = a.peak34.max(x.peak34);
    a.hits43 += x.hits43; a.misses43 += x.misses43; a.clears43 += x.clears43; a.peak43 = a.peak43.max(x.peak43);
    for (k, v) in x.stabilizers { *a.stabilizers.entry(k).or_default() += v; }
    for (k, v) in x.divisors34 { *a.divisors34.entry(k).or_default() += v; }
    for (k, v) in x.divisors43 { *a.divisors43.entry(k).or_default() += v; }
    a.samples.extend(x.samples);
}

fn k23_header(input: &str) -> u64 {
    let mut r = BufReader::new(File::open(input).unwrap());
    let mut h = [0u8; K23_HEADER]; r.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8], K23_MAGIC);
    assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()), U);
    assert_eq!(u16::from_le_bytes(h[28..30].try_into().unwrap()), K23_RECORD as u16);
    assert_eq!(u64::from_le_bytes(h[32..40].try_into().unwrap()), 246);
    assert_eq!(u64::from_le_bytes(h[40..48].try_into().unwrap()), 305);
    let n = u64::from_le_bytes(h[48..56].try_into().unwrap());
    assert_eq!(n, K23_RECORDS);
    assert_eq!(i128::from_le_bytes(h[64..80].try_into().unwrap()), K23_PAIR_WEIGHT_SUM);
    assert_eq!(std::fs::metadata(input).unwrap().len(), K23_HEADER as u64 + K23_RECORD as u64 * n);
    n
}

fn k23_map_json(m: &std::collections::BTreeMap<(u8, u8), u64>) -> String {
    m.iter().map(|(&(a,b),n)| format!("\"{}_{}\":{}", a,b,n)).collect::<Vec<_>>().join(",")
}

fn k23_stab_json(m: &std::collections::BTreeMap<u16, u64>) -> String {
    m.iter().map(|(a,n)| format!("\"{}\":{}", a,n)).collect::<Vec<_>>().join(",")
}

fn k23_consume(input: &str, output: &str, start: u64, end_arg: Option<u64>, workers: usize, cache_chunk: u64) {
    let begun = Instant::now();
    assert!((1..=8).contains(&workers)); assert!(cache_chunk > 0);
    let declared = k23_header(input);
    let end = end_arg.unwrap_or(declared).min(declared);
    assert!(start < end && end <= declared);
    let count = end - start;
    let sample_indices: HashSet<u64> = if count <= 257 {
        (start..end).collect()
    } else {
        (0..257).map(|j| start + j * (count - 1) / 256).collect()
    };
    let e = Arc::new(parse()); let c = Arc::new(cenv());
    let input = Arc::new(input.to_string()); let samples = Arc::new(sample_indices.clone());
    let mut jobs = Vec::new();
    for worker in 0..workers {
        let lo = start + count * worker as u64 / workers as u64;
        let hi = start + count * (worker as u64 + 1) / workers as u64;
        let (ee, cc, ii, ss) = (e.clone(), c.clone(), input.clone(), samples.clone());
        jobs.push(thread::spawn(move || k23_process(&ii, lo, hi, &ss, cache_chunk, ee, cc)));
    }
    let mut total = K23Worker { start, end, ..K23Worker::default() };
    let mut last = None;
    for job in jobs {
        let x = job.join().unwrap();
        if let (Some(a), Some(b)) = (last, x.first) { assert!(a < b); }
        if x.last.is_some() { last = x.last; }
        k23_merge(&mut total, x);
    }
    assert_eq!(total.records, count);
    assert_eq!(total.d34.first_children, 32 * count);
    assert_eq!(total.d34.terminal_children, 60 * total.d34.selected_p3);
    assert_eq!(total.hits34 + total.misses34, total.d34.selected_p3);
    assert_eq!(total.d43.first_children, 60 * count);
    assert_eq!(total.d43.terminal_children, 32 * total.d43.selected_p3);
    assert_eq!(total.hits43 + total.misses43, total.d43.selected_p3);
    assert_eq!(total.samples.len(), sample_indices.len());
    if start == 0 && end == declared {
        assert_eq!(total.uses, K23_PAIR_USES); assert_eq!(total.pair_weight, K23_PAIR_WEIGHT_SUM);
    }
    total.samples.sort_by_key(|x| x.0);
    let sample_path = format!("{}.samples.tsv", output);
    let mut lines = vec!["input_index\tK16_row\tp2\tweight_after_p2\tpair_uses\torbit\tstabilizer\tR234_first_children\tR234_pivotable_intermediate\tR234_selected_p3\tR234_terminal_K23\tR234_terminal_weight_scaled\tR234_charge_scaled\tR243_first_children\tR243_pivotable_intermediate\tR243_selected_p3\tR243_terminal_K23\tR243_terminal_weight_scaled\tR243_charge_scaled\tR234_nonzero\tR243_nonzero".to_string()];
    lines.extend(total.samples.iter().map(|x| x.1.clone()));
    let sample_tmp = format!("{}.tmp", sample_path);
    std::fs::write(&sample_tmp, format!("{}\n", lines.join("\n"))).unwrap(); rename(sample_tmp, &sample_path).unwrap();
    let nonzero34 = lines.iter().skip(1).filter(|x| x.rsplit('\t').nth(1) == Some("1")).count();
    let nonzero43 = lines.iter().skip(1).filter(|x| x.ends_with("\t1")).count();
    let elapsed = begun.elapsed().as_secs_f64();
    assert!(elapsed < 600.0, "interval exceeded hard 600-second publication gate");
    let projection = elapsed * declared as f64 / count as f64;
    let status = if start == 0 && end == declared { "PASS_COMPLETE_K23_HIDDEN_DECORATED_PAIR_TWO_SINK" } else { "PASS_BOUNDED_K23_HIDDEN_DECORATED_PAIR_TWO_SINK" };
    let text = format!(concat!(
        "{{\n  \"status\":\"{}\",\n  \"covered_lineage_ids\":[\"D14:222|R:2-3-4\",\"D14:222|R:2-4-3\"],\n",
        "  \"scale_U\":\"{}\",\n  \"input\":\"{}\",\n  \"input_sha256_expected\":\"{}\",\n  \"input_records_declared\":{},\n  \"input_interval\":[{},{}],\n  \"input_records_consumed\":{},\n",
        "  \"retained_pair_uses\":{},\n  \"pair_weight_sum_scaled\":\"{}\",\n  \"sinks\":{{\n",
        "    \"D14:222|R:2-3-4\":{{\"first_tail_degree\":3,\"intermediate_degree\":19,\"terminal_tail_degree\":4,\"first_tail_evaluations\":{},\"pivotable_intermediate_children\":{},\"selected_p3\":{},\"terminal_K23_occurrences\":{},\"full_occurrences\":{},\"irreducible_occurrences\":{},\"pivotable_weight_scaled\":\"{}\",\"normalized_p3_weight_scaled\":\"{}\",\"terminal_weight_scaled\":\"{}\",\"full_charge_scaled\":\"{}\",\"irreducible_charge_scaled\":\"{}\",\"cache\":{{\"hits\":{},\"misses\":{},\"clears\":{},\"peak_keys\":{}}},\"m2_m3_histogram\":{{{}}}}},\n",
        "    \"D14:222|R:2-4-3\":{{\"first_tail_degree\":4,\"intermediate_degree\":20,\"terminal_tail_degree\":3,\"first_tail_evaluations\":{},\"pivotable_intermediate_children\":{},\"selected_p3\":{},\"terminal_K23_occurrences\":{},\"full_occurrences\":{},\"irreducible_occurrences\":{},\"pivotable_weight_scaled\":\"{}\",\"normalized_p3_weight_scaled\":\"{}\",\"terminal_weight_scaled\":\"{}\",\"full_charge_scaled\":\"{}\",\"irreducible_charge_scaled\":\"{}\",\"cache\":{{\"hits\":{},\"misses\":{},\"clears\":{},\"peak_keys\":{}}},\"m2_m3_histogram\":{{{}}}}}\n  }},\n",
        "  \"stabilizer_histogram\":{{{}}},\n  \"literal_witness_guard\":{{\"records\":{},\"R234_nonzero\":{},\"R243_nonzero\":{},\"all_terminal_K23_nonpivotable\":true,\"all_abstract_literal_cycle_keys_equal\":true,\"ledger\":\"{}\"}},\n",
        "  \"sign_rule\":\"ledger w2 is the exact coefficient after selected p2; first tail preserves w2; selected intermediate pivot gives w3=-w2/m3; U%(m2*m3)=0 and w2%m3=0 asserted occurrencewise\",\n",
        "  \"universal_terminality\":\"all 60 K4 or 32 K3 tails are exhaustively tested nonpivotable for every realized cached (profile,signature,p3) key before full=irreducible\",\n",
        "  \"workers\":{},\n  \"cache_chunk_records\":{},\n  \"elapsed_seconds\":{:.6},\n  \"linear_full_projection_seconds\":{:.6},\n",
        "  \"scope\":\"strict two-ID scalar K23 prefix/interval only; no rows, K24, membership, or conjecture verdict\"\n}}\n"
    ), status, U, input, K23_PAIR_SHA256, declared, start, end, count, total.uses, total.pair_weight,
        total.d34.first_children, total.d34.pivotable_intermediate, total.d34.selected_p3, total.d34.terminal_children, total.d34.terminal_children, total.d34.terminal_children, total.d34.pivotable_weight, total.d34.normalized_weight, total.d34.terminal_weight, total.d34.charge, total.d34.charge, total.hits34, total.misses34, total.clears34, total.peak34, k23_map_json(&total.divisors34),
        total.d43.first_children, total.d43.pivotable_intermediate, total.d43.selected_p3, total.d43.terminal_children, total.d43.terminal_children, total.d43.terminal_children, total.d43.pivotable_weight, total.d43.normalized_weight, total.d43.terminal_weight, total.d43.charge, total.d43.charge, total.hits43, total.misses43, total.clears43, total.peak43, k23_map_json(&total.divisors43),
        k23_stab_json(&total.stabilizers), sample_indices.len(), nonzero34, nonzero43, sample_path, workers, cache_chunk, elapsed, projection);
    let tmp = format!("{}.tmp", output); std::fs::write(&tmp, &text).unwrap(); rename(tmp, output).unwrap(); print!("{}", text);
}

pub fn k23_main() {
    let args: Vec<String> = std::env::args().collect();
    let mut input = K23_PAIR_INPUT.to_string();
    let mut output = "computations/unaudited-codex-orbit0-k23-hidden-decorated-pair-2026-08-24/results_prefix4096.json".to_string();
    let mut start = 0u64; let mut end = None; let mut workers = 8usize; let mut cache_chunk = 100_000u64;
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--input" => { input = args[i+1].clone(); i += 2; },
            "--output" => { output = args[i+1].clone(); i += 2; },
            "--start" => { start = args[i+1].parse().unwrap(); i += 2; },
            "--end" => { end = Some(args[i+1].parse().unwrap()); i += 2; },
            "--workers" => { workers = args[i+1].parse().unwrap(); i += 2; },
            "--cache-chunk-records" => { cache_chunk = args[i+1].parse().unwrap(); i += 2; },
            _ => panic!("usage: producer [--input PATH] [--output PATH] [--start N] [--end N] [--workers 1..8] [--cache-chunk-records N]"),
        }
    }
    k23_consume(&input, &output, start, end, workers, cache_chunk);
}
