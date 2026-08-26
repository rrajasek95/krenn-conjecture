//! Exact scalar-only consumer for D14:222|R:2-3-2.
//!
//! The retained H16ORM1 decorated-pair ledger stores exact H-orbit masses of
//! `(literal K16 parent, selected p2)`.  Tail degree is not part of that
//! decorated object, so this consumer emits the representative's 32 K3 tails,
//! then applies every K19 pivot and the terminal K2 response.  H-invariance of
//! the 77-cycle functional makes a global K19/K21 row collection unnecessary.
#![allow(dead_code, unused_imports)]

include!(
    "../unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/run_hidden_children_prefix.rs"
);

use std::collections::BTreeMap;
use std::fs::metadata;

const INPUT: &str = "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin";
const MAGIC: &[u8; 8] = b"H16ORM1\0";
const HEADER: usize = 80;
const RECORD: usize = 53;
const EXPECTED_RECORDS: u64 = 101_545_723;
const EXPECTED_PAIR_WEIGHT_SUM: i128 = 146_230_609_431_055_564_800;
// `511_477_120` is the upstream labelled-use total before exact-zero pair
// keys are removed.  The retained nonzero H16ORM1 records carry the smaller
// witness-use sum below; `uses` is provenance, not a coefficient or mass.
const UPSTREAM_LABELLED_P2_USES_BEFORE_ZERO: u64 = 511_477_120;
const EXPECTED_RETAINED_PAIR_USES: u64 = 511_214_060;
const EXPECTED_ORBIT_ZERO: u64 = 305;
const EXPECTED_ORBIT_CHUNKS: u64 = 246;
const FULL_GATE_SECONDS: f64 = 600.0;

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct PairKey232 {
    row: Row,
    pivot: u8,
}

#[derive(Clone, Copy, Debug)]
struct PairRecord232 {
    key: PairKey232,
    weight_after_p2: i128,
    uses: u64,
    orbit: u16,
    stabilizer: u16,
}

#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
struct Delta {
    k19_children: u64,
    pivotable_k19_children: u64,
    selected_p3_uses: u64,
    k21_children: u64,
    pivotable_k19_weight_sum: i128,
    normalized_p3_weight_sum: i128,
    k21_weight_sum: i128,
    charge: i128,
}

impl Delta {
    fn add(&mut self, x: Delta) {
        self.k19_children += x.k19_children;
        self.pivotable_k19_children += x.pivotable_k19_children;
        self.selected_p3_uses += x.selected_p3_uses;
        self.k21_children += x.k21_children;
        self.pivotable_k19_weight_sum += x.pivotable_k19_weight_sum;
        self.normalized_p3_weight_sum += x.normalized_p3_weight_sum;
        self.k21_weight_sum += x.k21_weight_sum;
        self.charge += x.charge;
    }
}

#[derive(Clone, Copy, Debug, Default)]
struct Provenance {
    pivotable_k19_children: u64,
    signed_k19_weight: i128,
    selected_p3_uses: u64,
    k21_children: u64,
    charge: i128,
}

impl Provenance {
    fn add(&mut self, x: Provenance) {
        self.pivotable_k19_children += x.pivotable_k19_children;
        self.signed_k19_weight += x.signed_k19_weight;
        self.selected_p3_uses += x.selected_p3_uses;
        self.k21_children += x.k21_children;
        self.charge += x.charge;
    }
}

#[derive(Default)]
struct WorkerResult232 {
    start: u64,
    end: u64,
    pair_records: u64,
    pair_uses: u64,
    pair_weight_sum: i128,
    first_key: Option<PairKey232>,
    last_key: Option<PairKey232>,
    delta: Delta,
    provenance: BTreeMap<(u8, u8), Provenance>,
    stabilizers: BTreeMap<u16, u64>,
    cache_hits: u64,
    cache_misses: u64,
    cache_clears: u64,
    peak_cache_keys: usize,
    samples: Vec<(u64, String)>,
}

fn decode_pair(rec: &[u8; RECORD]) -> PairRecord232 {
    let mut row = [0; 24];
    row.copy_from_slice(&rec[..24]);
    PairRecord232 {
        key: PairKey232 { row: Row(row), pivot: rec[24] },
        weight_after_p2: i128::from_le_bytes(rec[25..41].try_into().unwrap()),
        uses: u64::from_le_bytes(rec[41..49].try_into().unwrap()),
        orbit: u16::from_le_bytes(rec[49..51].try_into().unwrap()),
        stabilizer: u16::from_le_bytes(rec[51..53].try_into().unwrap()),
    }
}

fn validate_pair(x: PairRecord232, e: &Engine) -> ([u8; 12], u8) {
    assert!(x.key.row.0.windows(2).all(|w| w[0] <= w[1]));
    assert_ne!(x.weight_after_p2, 0);
    assert!(x.uses > 0);
    assert_eq!((x.orbit as u32) * (x.stabilizer as u32), 384);
    let sig16 = signature(&x.key.row.0, e);
    let pivots = available(sig16, e);
    assert!(pivots.contains(&(x.key.pivot as usize)));
    let m2 = pivots.len();
    assert!(m2 > 0 && m2 < 256);
    (sig16, m2 as u8)
}

fn response2_abstract_k21(key: PKey, e: &Engine, c: &CEnv) -> Resp {
    let mut out = Resp::default();
    for tail in &e.all_k2[key.pivot as usize] {
        let sig21 = child_sig(key.sig, key.pivot as usize, tail, e);
        assert!(
            !pivotable_sig(sig21, e),
            "realized abstract terminal-K2 response remained pivotable at K21",
        );
        let ck = abstract_ckey(&key.profile, key.pivot as usize, tail, e, c);
        out.full_n += 1;
        out.full_q += *c.dual.get(&ck).unwrap_or(&0);
    }
    assert_eq!(out.full_n, 12);
    out.irr_n = out.full_n;
    out.irr_q = out.full_q;
    out
}

fn eval_pair_cached(
    x: PairRecord232,
    e: &Engine,
    c: &CEnv,
    cache: &mut HashMap<PKey, Resp>,
    hits: &mut u64,
    misses: &mut u64,
    provenance: &mut BTreeMap<(u8, u8), Provenance>,
) -> (Delta, u8) {
    let (sig16, m2) = validate_pair(x, e);
    let p2 = x.key.pivot as usize;
    let mut out = Delta::default();
    for tail3 in &e.all_k3[p2] {
        out.k19_children += 1;
        let sig19 = child_sig(sig16, p2, tail3, e);
        let pivots3 = available(sig19, e);
        if pivots3.is_empty() {
            continue;
        }
        let row19 = replace_anchor(&x.key.row, &e.anchors[p2], tail3);
        let m3 = pivots3.len();
        assert_eq!(signature(&row19.0, e), sig19);
        assert_eq!(U % ((m2 as i128) * (m3 as i128)), 0);
        assert_eq!(x.weight_after_p2 % (m3 as i128), 0);
        let w3 = -x.weight_after_p2 / (m3 as i128);
        out.pivotable_k19_children += 1;
        out.pivotable_k19_weight_sum += x.weight_after_p2;
        let mut pv = Provenance {
            pivotable_k19_children: 1,
            signed_k19_weight: x.weight_after_p2,
            ..Provenance::default()
        };
        for p3 in pivots3 {
            out.selected_p3_uses += 1;
            out.normalized_p3_weight_sum += w3;
            let key = PKey {
                profile: path_profile(&row19, p3, e, c),
                sig: sig19,
                pivot: p3 as u8,
            };
            let response = if let Some(z) = cache.get(&key) {
                *hits += 1;
                *z
            } else {
                *misses += 1;
                let z = response2_abstract_k21(key, e, c);
                cache.insert(key, z);
                z
            };
            assert_eq!((response.full_n, response.irr_n), (12, 12));
            assert_eq!(response.full_q, response.irr_q);
            out.k21_children += response.full_n;
            out.k21_weight_sum += w3 * (response.full_n as i128);
            out.charge += w3 * (response.full_q as i128);
            pv.selected_p3_uses += 1;
            pv.k21_children += response.full_n;
            pv.charge += w3 * (response.full_q as i128);
        }
        provenance.entry((m2, m3 as u8)).or_default().add(pv);
    }
    assert_eq!(out.k19_children, 32);
    assert_eq!(out.k21_children, 12 * out.selected_p3_uses);
    assert_eq!(out.normalized_p3_weight_sum, -out.pivotable_k19_weight_sum);
    assert_eq!(out.k21_weight_sum, 12 * out.normalized_p3_weight_sum);
    (out, m2)
}

fn eval_pair_literal(x: PairRecord232, e: &Engine, c: &CEnv) -> Delta {
    let (sig16, m2) = validate_pair(x, e);
    let p2 = x.key.pivot as usize;
    let mut out = Delta::default();
    for tail3 in &e.all_k3[p2] {
        out.k19_children += 1;
        let row19 = replace_anchor(&x.key.row, &e.anchors[p2], tail3);
        let sig19 = child_sig(sig16, p2, tail3, e);
        assert_eq!(signature(&row19.0, e), sig19);
        let pivots3 = available(sig19, e);
        if pivots3.is_empty() {
            continue;
        }
        let m3 = pivots3.len();
        assert_eq!(U % ((m2 as i128) * (m3 as i128)), 0);
        assert_eq!(x.weight_after_p2 % (m3 as i128), 0);
        let w3 = -x.weight_after_p2 / (m3 as i128);
        out.pivotable_k19_children += 1;
        out.pivotable_k19_weight_sum += x.weight_after_p2;
        for p3 in pivots3 {
            out.selected_p3_uses += 1;
            out.normalized_p3_weight_sum += w3;
            let profile = path_profile(&row19, p3, e, c);
            for tail2 in &e.all_k2[p3] {
                let sig21 = child_sig(sig19, p3, tail2, e);
                assert!(!pivotable_sig(sig21, e));
                let row21 = replace_anchor(&row19, &e.anchors[p3], tail2);
                assert_eq!(signature(&row21.0, e), sig21);
                let abstracted = abstract_ckey(&profile, p3, tail2, e, c);
                let literal = literal_ckey(&row21, c);
                assert_eq!(abstracted, literal);
                out.k21_children += 1;
                out.k21_weight_sum += w3;
                out.charge += w3 * (*c.dual.get(&literal).unwrap_or(&0) as i128);
            }
        }
    }
    assert_eq!(out.k19_children, 32);
    assert_eq!(out.k21_children, 12 * out.selected_p3_uses);
    assert_eq!(out.normalized_p3_weight_sum, -out.pivotable_k19_weight_sum);
    assert_eq!(out.k21_weight_sum, 12 * out.normalized_p3_weight_sum);
    out
}

fn hex24(row: &Row) -> String {
    row.0.iter().map(|x| format!("{:02x}", x)).collect()
}

fn process_interval(
    input: &str,
    start: u64,
    end: u64,
    sample_indices: &HashSet<u64>,
    cache_chunk_records: u64,
    e: Arc<Engine>,
    c: Arc<CEnv>,
) -> WorkerResult232 {
    let mut out = WorkerResult232 { start, end, ..WorkerResult232::default() };
    if start == end {
        return out;
    }
    let mut f = File::open(input).unwrap();
    f.seek(SeekFrom::Start(HEADER as u64 + RECORD as u64 * start)).unwrap();
    let mut reader = BufReader::with_capacity(8 << 20, f);
    let mut cache: HashMap<PKey, Resp> = HashMap::new();
    let mut prior = None;
    for index in start..end {
        if index > start && (index - start) % cache_chunk_records == 0 {
            out.peak_cache_keys = out.peak_cache_keys.max(cache.len());
            cache.clear();
            out.cache_clears += 1;
        }
        let mut rec = [0; RECORD];
        reader.read_exact(&mut rec).unwrap();
        let pair = decode_pair(&rec);
        assert!(prior.map_or(true, |p| p < pair.key));
        prior = Some(pair.key);
        if out.first_key.is_none() {
            out.first_key = Some(pair.key);
        }
        out.last_key = Some(pair.key);
        out.pair_records += 1;
        out.pair_uses += pair.uses;
        out.pair_weight_sum += pair.weight_after_p2;
        *out.stabilizers.entry(pair.stabilizer).or_default() += 1;
        let (delta, m2) = eval_pair_cached(
            pair, &e, &c, &mut cache, &mut out.cache_hits,
            &mut out.cache_misses, &mut out.provenance,
        );
        out.delta.add(delta);
        if sample_indices.contains(&index) {
            let literal = eval_pair_literal(pair, &e, &c);
            assert_eq!(literal, delta);
            out.samples.push((index, format!(
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                index, hex24(&pair.key.row), pair.key.pivot,
                pair.weight_after_p2, pair.uses, pair.orbit, pair.stabilizer,
                m2, delta.k19_children, delta.pivotable_k19_children,
                delta.selected_p3_uses, delta.k21_children,
                delta.k21_weight_sum, delta.charge,
                (delta.selected_p3_uses > 0) as u8,
            )));
        }
    }
    out.peak_cache_keys = out.peak_cache_keys.max(cache.len());
    out
}

fn merge_worker(total: &mut WorkerResult232, x: WorkerResult232) {
    total.pair_records += x.pair_records;
    total.pair_uses += x.pair_uses;
    total.pair_weight_sum += x.pair_weight_sum;
    total.delta.add(x.delta);
    total.cache_hits += x.cache_hits;
    total.cache_misses += x.cache_misses;
    total.cache_clears += x.cache_clears;
    total.peak_cache_keys = total.peak_cache_keys.max(x.peak_cache_keys);
    for (k, v) in x.provenance {
        total.provenance.entry(k).or_default().add(v);
    }
    for (k, v) in x.stabilizers {
        *total.stabilizers.entry(k).or_default() += v;
    }
    total.samples.extend(x.samples);
}

fn read_and_validate_header(input: &str) -> u64 {
    let mut reader = BufReader::new(File::open(input).unwrap());
    let mut h = [0; HEADER];
    reader.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8], MAGIC);
    assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()), U);
    assert_eq!((
        u16::from_le_bytes(h[24..26].try_into().unwrap()),
        u16::from_le_bytes(h[26..28].try_into().unwrap()),
        u16::from_le_bytes(h[28..30].try_into().unwrap()),
        u16::from_le_bytes(h[30..32].try_into().unwrap()),
    ), (0, 0, RECORD as u16, 0));
    assert_eq!(u64::from_le_bytes(h[32..40].try_into().unwrap()), EXPECTED_ORBIT_CHUNKS);
    assert_eq!(u64::from_le_bytes(h[40..48].try_into().unwrap()), EXPECTED_ORBIT_ZERO);
    let records = u64::from_le_bytes(h[48..56].try_into().unwrap());
    assert_eq!(records, EXPECTED_RECORDS);
    assert_eq!(u64::from_le_bytes(h[56..64].try_into().unwrap()), 0);
    assert_eq!(i128::from_le_bytes(h[64..80].try_into().unwrap()), EXPECTED_PAIR_WEIGHT_SUM);
    assert_eq!(metadata(input).unwrap().len(), HEADER as u64 + RECORD as u64 * records);
    records
}

fn consume(input: &str, output: &str, start: u64, end_arg: Option<u64>, workers: usize,
           cache_chunk_records: u64) {
    let begun = Instant::now();
    assert!((1..=8).contains(&workers));
    assert!(cache_chunk_records > 0);
    let declared = read_and_validate_header(input);
    let end = end_arg.unwrap_or(declared).min(declared);
    assert!(start < end && end <= declared);
    let count = end - start;
    let sample_indices: HashSet<u64> = if count <= 257 {
        (start..end).collect()
    } else {
        (0..257).map(|j| start + j * (count - 1) / 256).collect()
    };
    let e = Arc::new(parse());
    let c = Arc::new(cenv());
    let input_arc = Arc::new(input.to_string());
    let samples_arc = Arc::new(sample_indices.clone());
    let mut jobs = Vec::new();
    for worker in 0..workers {
        let lo = start + count * worker as u64 / workers as u64;
        let hi = start + count * (worker as u64 + 1) / workers as u64;
        let ee = e.clone();
        let cc = c.clone();
        let ii = input_arc.clone();
        let ss = samples_arc.clone();
        jobs.push(thread::spawn(move ||
            process_interval(&ii, lo, hi, &ss, cache_chunk_records, ee, cc)));
    }
    let mut total = WorkerResult232 { start, end, ..WorkerResult232::default() };
    let mut previous_last = None;
    for job in jobs {
        let x = job.join().unwrap();
        if let (Some(a), Some(b)) = (previous_last, x.first_key) {
            assert!(a < b);
        }
        if x.last_key.is_some() {
            previous_last = x.last_key;
        }
        merge_worker(&mut total, x);
    }
    assert_eq!(total.pair_records, count);
    assert_eq!(total.delta.k19_children, 32 * count);
    assert_eq!(total.delta.k21_children, 12 * total.delta.selected_p3_uses);
    assert_eq!(total.delta.normalized_p3_weight_sum, -total.delta.pivotable_k19_weight_sum);
    assert_eq!(total.delta.k21_weight_sum, 12 * total.delta.normalized_p3_weight_sum);
    assert_eq!(total.cache_hits + total.cache_misses, total.delta.selected_p3_uses);
    assert_eq!(total.samples.len(), sample_indices.len());
    total.samples.sort_by_key(|x| x.0);
    if start == 0 && end == declared {
        assert_eq!(total.pair_uses, EXPECTED_RETAINED_PAIR_USES);
        assert_eq!(total.pair_weight_sum, EXPECTED_PAIR_WEIGHT_SUM);
        assert_eq!(total.stabilizers, BTreeMap::from([
            (1, 99_314_228), (2, 2_212_958), (4, 16_210),
            (8, 2_099), (16, 224), (32, 4),
        ]));
    }
    let provenance_total = total.provenance.values().fold(Provenance::default(), |mut a, &x| {
        a.add(x); a
    });
    assert_eq!(provenance_total.pivotable_k19_children, total.delta.pivotable_k19_children);
    assert_eq!(provenance_total.signed_k19_weight, total.delta.pivotable_k19_weight_sum);
    assert_eq!(provenance_total.selected_p3_uses, total.delta.selected_p3_uses);
    assert_eq!(provenance_total.k21_children, total.delta.k21_children);
    assert_eq!(provenance_total.charge, total.delta.charge);

    let sample_path = format!("{}.samples.tsv", output);
    let mut sample_lines = vec![
        "input_index\tK16_row\tp2\tweight_after_p2\tpair_uses\torbit\tstabilizer\tm2\tK19_children\tpivotable_K19_children\tselected_p3_uses\tK21_children\tK21_weight_sum_scaled\tcharge_scaled\tnonzero_continuation".to_string()
    ];
    sample_lines.extend(total.samples.into_iter().map(|x| x.1));
    let sample_tmp = format!("{}.tmp", sample_path);
    std::fs::write(&sample_tmp, format!("{}\n", sample_lines.join("\n"))).unwrap();
    rename(sample_tmp, &sample_path).unwrap();

    let prov_json = total.provenance.iter().map(|(&(m2, m3), p)| format!(
        "\"{}_{}\":{{\"pivotable_K19_children\":{},\"signed_K19_weight_scaled\":\"{}\",\"selected_p3_uses\":{},\"K21_children\":{},\"charge_scaled\":\"{}\"}}",
        m2, m3, p.pivotable_k19_children, p.signed_k19_weight,
        p.selected_p3_uses, p.k21_children, p.charge,
    )).collect::<Vec<_>>().join(",");
    let stab_json = total.stabilizers.iter().map(|(s, n)| format!("\"{}\":{}", s, n))
        .collect::<Vec<_>>().join(",");
    let elapsed = begun.elapsed().as_secs_f64();
    if start == 0 && end == declared {
        assert!(elapsed < FULL_GATE_SECONDS, "600-second full-run gate exceeded");
    }
    let serial_projection = elapsed * (declared as f64) / (count as f64);
    let status = if start == 0 && end == declared {
        "PASS_COMPLETE_D14_222_R_2_3_2_K21_CHARGE"
    } else {
        "PASS_BOUNDED_PREFIX_D14_222_R_2_3_2_K21_CHARGE"
    };
    let nonzero_samples = sample_lines.iter().skip(1).filter(|x| x.ends_with("\t1")).count();
    let text = format!(concat!(
        "{{\n",
        "  \"status\":\"{}\",\n",
        "  \"lineage_id\":\"D14:222|R:2-3-2\",\n",
        "  \"scale_U\":\"{}\",\n",
        "  \"input\":\"{}\",\n",
        "  \"input_schema\":\"H16ORM1: row24,p2_u8,weight_i128,uses_u64,orbit_u16,stabilizer_u16\",\n",
        "  \"input_records_declared\":{},\n",
        "  \"input_interval\":[{},{}],\n",
        "  \"input_records_consumed\":{},\n",
        "  \"upstream_labelled_p2_uses_before_zero\":{},\n",
        "  \"retained_nonzero_pair_witness_uses\":{},\n",
        "  \"pair_weight_sum_scaled\":\"{}\",\n",
        "  \"K3_to_K19_tail_evaluations\":{},\n",
        "  \"pivotable_K19_children\":{},\n",
        "  \"selected_p3_uses\":{},\n",
        "  \"K21_terminal_occurrences\":{},\n",
        "  \"full_occurrences\":{},\n",
        "  \"irreducible_occurrences\":{},\n",
        "  \"pivotable_K19_weight_sum_scaled\":\"{}\",\n",
        "  \"normalized_p3_weight_sum_scaled\":\"{}\",\n",
        "  \"K21_weight_sum_scaled\":\"{}\",\n",
        "  \"full_charge_scaled\":\"{}\",\n",
        "  \"irreducible_charge_scaled\":\"{}\",\n",
        "  \"response_cache\":{{\"hits\":{},\"misses\":{},\"clears\":{},\"peak_keys_per_worker_chunk\":{},\"cache_chunk_pair_records\":{}}},\n",
        "  \"m2_m3_provenance\":{{{}}},\n",
        "  \"stabilizer_histogram\":{{{}}},\n",
        "  \"literal_sample_guard\":{{\"records\":{},\"nonzero_continuations\":{},\"all_literal_K21_children_nonpivotable\":true,\"all_abstract_literal_cycle_keys_equal\":true,\"ledger\":\"{}\"}},\n",
        "  \"sign_rule\":\"input w2 is the exact coefficient after D14 R2 and selected K16 p2; K3 preserves w2; terminal K2 response uses w3=-w2/m3\",\n",
        "  \"linearity_scope\":\"one representative K3 tail family per exact decorated H-orbit, weighted by total orbit mass; H-invariant terminal scalar permits direct folding without canonical K19/K21 row output\",\n",
        "  \"workers\":{},\n",
        "  \"elapsed_seconds\":{:.6},\n",
        "  \"serial_full_projection_seconds\":{:.6},\n",
        "  \"scope\":\"strict singleton K21 charge only; no K19/K21 row checkpoint, K22 prolongation, residual, membership, or conjecture verdict\"\n",
        "}}\n"
    ), status, U, input, declared, start, end, count,
        UPSTREAM_LABELLED_P2_USES_BEFORE_ZERO, total.pair_uses,
        total.pair_weight_sum, total.delta.k19_children,
        total.delta.pivotable_k19_children, total.delta.selected_p3_uses,
        total.delta.k21_children, total.delta.k21_children,
        total.delta.k21_children, total.delta.pivotable_k19_weight_sum,
        total.delta.normalized_p3_weight_sum, total.delta.k21_weight_sum,
        total.delta.charge, total.delta.charge, total.cache_hits,
        total.cache_misses, total.cache_clears, total.peak_cache_keys,
        cache_chunk_records, prov_json, stab_json, sample_indices.len(),
        nonzero_samples, sample_path, workers, elapsed, serial_projection,
    );
    let tmp = format!("{}.tmp", output);
    std::fs::write(&tmp, &text).unwrap();
    rename(tmp, output).unwrap();
    print!("{}", text);
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mut input = INPUT.to_string();
    let mut output = "computations/unaudited-codex-orbit0-k21-hidden-232-charge-2026-08-24/results_hidden_232_k21_charge.json".to_string();
    let mut start = 0u64;
    let mut end = None;
    let mut workers = 1usize;
    let mut cache_chunk_records = 100_000u64;
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--input" => { input = args[i + 1].clone(); i += 2; }
            "--output" => { output = args[i + 1].clone(); i += 2; }
            "--start" => { start = args[i + 1].parse().unwrap(); i += 2; }
            "--end" => { end = Some(args[i + 1].parse().unwrap()); i += 2; }
            "--workers" => { workers = args[i + 1].parse().unwrap(); i += 2; }
            "--cache-chunk-records" => { cache_chunk_records = args[i + 1].parse().unwrap(); i += 2; }
            _ => panic!("usage: consumer [--input PATH] [--output PATH] [--start N] [--end N] [--workers 1..8] [--cache-chunk-records N]"),
        }
    }
    consume(&input, &output, start, end, workers, cache_chunk_records);
}
