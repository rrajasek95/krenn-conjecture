//! Exact two-sink scalar consumer for D14:222|R:2-3-3 and R:2-4-2.
//!
//! The retained H16ORM1 decorated-pair ledger stores exact H-orbit masses of
//! `(literal K16 parent, selected p2)`.  Tail degree is not part of that
//! decorated object.  One logical scan fans each representative into (a) 32
//! K3 tails, every K19 pivot, then terminal K3, and (b) 60 K4 tails, every K20
//! pivot, then terminal K2.  H-invariance makes global intermediate/child row
//! collection unnecessary; the two exact scalar sinks remain separate.
#![allow(dead_code, unused_imports)]

include!(
    "../unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/run_hidden_children_prefix.rs"
);

use std::collections::BTreeMap;
use std::fs::metadata;

const INPUT: &str = "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin";
const EXPECTED_INPUT_SHA256: &str = "22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8";
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
const MAX_CACHE_KEYS_PER_WORKER_SINK: usize = 300_000;
const MAX_NEW_CACHE_KEYS_PER_PAIR: usize = 720; // 60 first tails times <=12 anchors.

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
    delta33: Delta,
    delta42: Delta,
    provenance33: BTreeMap<(u8, u8), Provenance>,
    provenance42: BTreeMap<(u8, u8), Provenance>,
    stabilizers: BTreeMap<u16, u64>,
    cache_hits: u64,
    cache_misses: u64,
    cache_clears: u64,
    peak_cache_keys: usize,
    cache42_hits: u64,
    cache42_misses: u64,
    cache42_clears: u64,
    peak_cache42_keys: usize,
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

fn response3_abstract_k22(key: PKey, e: &Engine, c: &CEnv) -> Resp {
    let mut out = Resp::default();
    for tail in &e.all_k3[key.pivot as usize] {
        let sig22 = child_sig(key.sig, key.pivot as usize, tail, e);
        assert!(
            !pivotable_sig(sig22, e),
            "realized abstract terminal-K3 response remained pivotable at K22",
        );
        let ck = abstract_ckey(&key.profile, key.pivot as usize, tail, e, c);
        out.full_n += 1;
        out.full_q += *c.dual.get(&ck).unwrap_or(&0);
    }
    assert_eq!(out.full_n, 32);
    out.irr_n = out.full_n;
    out.irr_q = out.full_q;
    out
}

fn response2_abstract_k22(key: PKey, e: &Engine, c: &CEnv) -> Resp {
    let mut out = Resp::default();
    for tail in &e.all_k2[key.pivot as usize] {
        let sig22 = child_sig(key.sig, key.pivot as usize, tail, e);
        assert!(!pivotable_sig(sig22, e), "terminal-K2 response remained pivotable at K22");
        let ck = abstract_ckey(&key.profile, key.pivot as usize, tail, e, c);
        out.full_n += 1;
        out.full_q += *c.dual.get(&ck).unwrap_or(&0);
    }
    assert_eq!(out.full_n, 12);
    out.irr_n = out.full_n;
    out.irr_q = out.full_q;
    out
}

fn eval_pair_cached33(
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
                let z = response3_abstract_k22(key, e, c);
                cache.insert(key, z);
                z
            };
            assert_eq!((response.full_n, response.irr_n), (32, 32));
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
    assert_eq!(out.k21_children, 32 * out.selected_p3_uses);
    assert_eq!(out.normalized_p3_weight_sum, -out.pivotable_k19_weight_sum);
    assert_eq!(out.k21_weight_sum, 32 * out.normalized_p3_weight_sum);
    (out, m2)
}

fn eval_pair_literal33(x: PairRecord232, e: &Engine, c: &CEnv) -> Delta {
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
            for tail3b in &e.all_k3[p3] {
                let sig22 = child_sig(sig19, p3, tail3b, e);
                assert!(!pivotable_sig(sig22, e));
                let row22 = replace_anchor(&row19, &e.anchors[p3], tail3b);
                assert_eq!(signature(&row22.0, e), sig22);
                let abstracted = abstract_ckey(&profile, p3, tail3b, e, c);
                let literal = literal_ckey(&row22, c);
                assert_eq!(abstracted, literal);
                out.k21_children += 1;
                out.k21_weight_sum += w3;
                out.charge += w3 * (*c.dual.get(&literal).unwrap_or(&0) as i128);
            }
        }
    }
    assert_eq!(out.k19_children, 32);
    assert_eq!(out.k21_children, 32 * out.selected_p3_uses);
    assert_eq!(out.normalized_p3_weight_sum, -out.pivotable_k19_weight_sum);
    assert_eq!(out.k21_weight_sum, 32 * out.normalized_p3_weight_sum);
    out
}

fn eval_pair_cached42(
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
    for tail4 in &c.k4[p2] {
        out.k19_children += 1;
        let sig20 = child_sig(sig16, p2, tail4, e);
        let pivots3 = available(sig20, e);
        if pivots3.is_empty() { continue; }
        let row20 = replace_anchor(&x.key.row, &e.anchors[p2], tail4);
        let m3 = pivots3.len();
        assert_eq!(signature(&row20.0, e), sig20);
        assert_eq!(U % ((m2 as i128) * (m3 as i128)), 0);
        assert_eq!(x.weight_after_p2 % (m3 as i128), 0);
        let w3 = -x.weight_after_p2 / (m3 as i128);
        out.pivotable_k19_children += 1;
        out.pivotable_k19_weight_sum += x.weight_after_p2;
        let mut pv = Provenance { pivotable_k19_children: 1, signed_k19_weight: x.weight_after_p2, ..Provenance::default() };
        for p3 in pivots3 {
            out.selected_p3_uses += 1;
            out.normalized_p3_weight_sum += w3;
            let key = PKey { profile: path_profile(&row20, p3, e, c), sig: sig20, pivot: p3 as u8 };
            let response = if let Some(value) = cache.get(&key) {
                *hits += 1; *value
            } else {
                *misses += 1;
                let value = response2_abstract_k22(key, e, c);
                cache.insert(key, value);
                value
            };
            assert_eq!((response.full_n, response.irr_n), (12, 12));
            assert_eq!(response.full_q, response.irr_q);
            out.k21_children += response.full_n;
            out.k21_weight_sum += w3 * response.full_n as i128;
            out.charge += w3 * response.full_q as i128;
            pv.selected_p3_uses += 1;
            pv.k21_children += response.full_n;
            pv.charge += w3 * response.full_q as i128;
        }
        provenance.entry((m2, m3 as u8)).or_default().add(pv);
    }
    assert_eq!(out.k19_children, 60);
    assert_eq!(out.k21_children, 12 * out.selected_p3_uses);
    assert_eq!(out.normalized_p3_weight_sum, -out.pivotable_k19_weight_sum);
    assert_eq!(out.k21_weight_sum, 12 * out.normalized_p3_weight_sum);
    (out, m2)
}

fn eval_pair_literal42(x: PairRecord232, e: &Engine, c: &CEnv) -> Delta {
    let (sig16, m2) = validate_pair(x, e);
    let p2 = x.key.pivot as usize;
    let mut out = Delta::default();
    for tail4 in &c.k4[p2] {
        out.k19_children += 1;
        let row20 = replace_anchor(&x.key.row, &e.anchors[p2], tail4);
        let sig20 = child_sig(sig16, p2, tail4, e);
        assert_eq!(signature(&row20.0, e), sig20);
        let pivots3 = available(sig20, e);
        if pivots3.is_empty() { continue; }
        let m3 = pivots3.len();
        assert_eq!(U % ((m2 as i128) * (m3 as i128)), 0);
        assert_eq!(x.weight_after_p2 % m3 as i128, 0);
        let w3 = -x.weight_after_p2 / m3 as i128;
        out.pivotable_k19_children += 1;
        out.pivotable_k19_weight_sum += x.weight_after_p2;
        for p3 in pivots3 {
            out.selected_p3_uses += 1;
            out.normalized_p3_weight_sum += w3;
            let profile = path_profile(&row20, p3, e, c);
            for tail2 in &e.all_k2[p3] {
                let sig22 = child_sig(sig20, p3, tail2, e);
                assert!(!pivotable_sig(sig22, e));
                let row22 = replace_anchor(&row20, &e.anchors[p3], tail2);
                assert_eq!(signature(&row22.0, e), sig22);
                let abstracted = abstract_ckey(&profile, p3, tail2, e, c);
                let literal = literal_ckey(&row22, c);
                assert_eq!(abstracted, literal);
                out.k21_children += 1;
                out.k21_weight_sum += w3;
                out.charge += w3 * (*c.dual.get(&literal).unwrap_or(&0) as i128);
            }
        }
    }
    assert_eq!(out.k19_children, 60);
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
    let mut cache42: HashMap<PKey, Resp> = HashMap::new();
    let mut prior = None;
    for index in start..end {
        if index > start && (index - start) % cache_chunk_records == 0 {
            out.peak_cache_keys = out.peak_cache_keys.max(cache.len());
            out.peak_cache42_keys = out.peak_cache42_keys.max(cache42.len());
            cache.clear();
            cache42.clear();
            out.cache_clears += 1;
            out.cache42_clears += 1;
        }
        if cache.len() >= MAX_CACHE_KEYS_PER_WORKER_SINK {
            out.peak_cache_keys = out.peak_cache_keys.max(cache.len());
            cache.clear();
            out.cache_clears += 1;
        }
        if cache42.len() >= MAX_CACHE_KEYS_PER_WORKER_SINK {
            out.peak_cache42_keys = out.peak_cache42_keys.max(cache42.len());
            cache42.clear();
            out.cache42_clears += 1;
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
        let (delta33, m2) = eval_pair_cached33(
            pair, &e, &c, &mut cache, &mut out.cache_hits,
            &mut out.cache_misses, &mut out.provenance33,
        );
        let (delta42, m2b) = eval_pair_cached42(
            pair, &e, &c, &mut cache42, &mut out.cache42_hits,
            &mut out.cache42_misses, &mut out.provenance42,
        );
        assert!(cache.len() <= MAX_CACHE_KEYS_PER_WORKER_SINK + MAX_NEW_CACHE_KEYS_PER_PAIR);
        assert!(cache42.len() <= MAX_CACHE_KEYS_PER_WORKER_SINK + MAX_NEW_CACHE_KEYS_PER_PAIR);
        assert_eq!(m2, m2b);
        out.delta33.add(delta33);
        out.delta42.add(delta42);
        if sample_indices.contains(&index) {
            let literal33 = eval_pair_literal33(pair, &e, &c);
            let literal42 = eval_pair_literal42(pair, &e, &c);
            assert_eq!(literal33, delta33);
            assert_eq!(literal42, delta42);
            out.samples.push((index, format!(
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                index, hex24(&pair.key.row), pair.key.pivot,
                pair.weight_after_p2, pair.uses, pair.orbit, pair.stabilizer,
                m2, delta33.k19_children, delta33.pivotable_k19_children,
                delta33.selected_p3_uses, delta33.k21_children,
                delta33.k21_weight_sum, delta33.charge,
                delta42.k19_children, delta42.pivotable_k19_children,
                delta42.selected_p3_uses, delta42.k21_children,
                delta42.k21_weight_sum, delta42.charge,
                (delta33.selected_p3_uses > 0) as u8,
                (delta42.selected_p3_uses > 0) as u8,
            )));
        }
    }
    out.peak_cache_keys = out.peak_cache_keys.max(cache.len());
    out.peak_cache42_keys = out.peak_cache42_keys.max(cache42.len());
    out
}

fn merge_worker(total: &mut WorkerResult232, x: WorkerResult232) {
    total.pair_records += x.pair_records;
    total.pair_uses += x.pair_uses;
    total.pair_weight_sum += x.pair_weight_sum;
    total.delta33.add(x.delta33);
    total.delta42.add(x.delta42);
    total.cache_hits += x.cache_hits;
    total.cache_misses += x.cache_misses;
    total.cache_clears += x.cache_clears;
    total.peak_cache_keys = total.peak_cache_keys.max(x.peak_cache_keys);
    total.cache42_hits += x.cache42_hits;
    total.cache42_misses += x.cache42_misses;
    total.cache42_clears += x.cache42_clears;
    total.peak_cache42_keys = total.peak_cache42_keys.max(x.peak_cache42_keys);
    for (k, v) in x.provenance33 {
        total.provenance33.entry(k).or_default().add(v);
    }
    for (k, v) in x.provenance42 {
        total.provenance42.entry(k).or_default().add(v);
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
           cache_chunk_records: u64, global_samples: bool) {
    let begun = Instant::now();
    assert!((1..=8).contains(&workers));
    assert!(cache_chunk_records > 0);
    let declared = read_and_validate_header(input);
    let end = end_arg.unwrap_or(declared).min(declared);
    assert!(start < end && end <= declared);
    let count = end - start;
    let sample_indices: HashSet<u64> = if global_samples {
        (0..257)
            .map(|j| j * (declared - 1) / 256)
            .filter(|&index| start <= index && index < end)
            .collect()
    } else if count <= 257 {
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
    assert_eq!(total.delta33.k19_children, 32 * count);
    assert_eq!(total.delta33.k21_children, 32 * total.delta33.selected_p3_uses);
    assert_eq!(total.delta33.normalized_p3_weight_sum, -total.delta33.pivotable_k19_weight_sum);
    assert_eq!(total.delta33.k21_weight_sum, 32 * total.delta33.normalized_p3_weight_sum);
    assert_eq!(total.cache_hits + total.cache_misses, total.delta33.selected_p3_uses);
    assert_eq!(total.delta42.k19_children, 60 * count);
    assert_eq!(total.delta42.k21_children, 12 * total.delta42.selected_p3_uses);
    assert_eq!(total.delta42.normalized_p3_weight_sum, -total.delta42.pivotable_k19_weight_sum);
    assert_eq!(total.delta42.k21_weight_sum, 12 * total.delta42.normalized_p3_weight_sum);
    assert_eq!(total.cache42_hits + total.cache42_misses, total.delta42.selected_p3_uses);
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
    let provenance33_total = total.provenance33.values().fold(Provenance::default(), |mut a, &x| {
        a.add(x); a
    });
    assert_eq!(provenance33_total.pivotable_k19_children, total.delta33.pivotable_k19_children);
    assert_eq!(provenance33_total.signed_k19_weight, total.delta33.pivotable_k19_weight_sum);
    assert_eq!(provenance33_total.selected_p3_uses, total.delta33.selected_p3_uses);
    assert_eq!(provenance33_total.k21_children, total.delta33.k21_children);
    assert_eq!(provenance33_total.charge, total.delta33.charge);
    let provenance42_total = total.provenance42.values().fold(Provenance::default(), |mut a, &x| {
        a.add(x); a
    });
    assert_eq!(provenance42_total.pivotable_k19_children, total.delta42.pivotable_k19_children);
    assert_eq!(provenance42_total.signed_k19_weight, total.delta42.pivotable_k19_weight_sum);
    assert_eq!(provenance42_total.selected_p3_uses, total.delta42.selected_p3_uses);
    assert_eq!(provenance42_total.k21_children, total.delta42.k21_children);
    assert_eq!(provenance42_total.charge, total.delta42.charge);

    let elapsed = begun.elapsed().as_secs_f64();
    assert!(elapsed < FULL_GATE_SECONDS, "600-second interval gate exceeded; no result written");

    let sample_path = format!("{}.samples.tsv", output);
    let mut sample_lines = vec![
        "input_index\tK16_row\tp2\tweight_after_p2\tpair_uses\torbit\tstabilizer\tm2\tR233_K19_children\tR233_pivotable_K19_children\tR233_selected_p3_uses\tR233_K22_children\tR233_K22_weight_sum_scaled\tR233_charge_scaled\tR242_K20_children\tR242_pivotable_K20_children\tR242_selected_p3_uses\tR242_K22_children\tR242_K22_weight_sum_scaled\tR242_charge_scaled\tR233_nonzero_continuation\tR242_nonzero_continuation".to_string()
    ];
    sample_lines.extend(total.samples.into_iter().map(|x| x.1));
    let sample_tmp = format!("{}.tmp", sample_path);
    std::fs::write(&sample_tmp, format!("{}\n", sample_lines.join("\n"))).unwrap();
    rename(sample_tmp, &sample_path).unwrap();

    let prov33_json = total.provenance33.iter().map(|(&(m2, m3), p)| format!(
        "\"{}_{}\":{{\"pivotable_intermediate_children\":{},\"signed_intermediate_weight_scaled\":\"{}\",\"selected_next_pivots\":{},\"terminal_K22_children\":{},\"charge_scaled\":\"{}\"}}",
        m2, m3, p.pivotable_k19_children, p.signed_k19_weight,
        p.selected_p3_uses, p.k21_children, p.charge,
    )).collect::<Vec<_>>().join(",");
    let prov42_json = total.provenance42.iter().map(|(&(m2, m3), p)| format!(
        "\"{}_{}\":{{\"pivotable_intermediate_children\":{},\"signed_intermediate_weight_scaled\":\"{}\",\"selected_next_pivots\":{},\"terminal_K22_children\":{},\"charge_scaled\":\"{}\"}}",
        m2, m3, p.pivotable_k19_children, p.signed_k19_weight,
        p.selected_p3_uses, p.k21_children, p.charge,
    )).collect::<Vec<_>>().join(",");
    let stab_json = total.stabilizers.iter().map(|(s, n)| format!("\"{}\":{}", s, n))
        .collect::<Vec<_>>().join(",");
    let serial_projection = elapsed * (declared as f64) / (count as f64);
    let status = if start == 0 && end == declared {
        "PASS_COMPLETE_D14_222_K22_HIDDEN_PAIR_TWO_SINK_CHARGE"
    } else {
        "PASS_BOUNDED_INTERVAL_D14_222_K22_HIDDEN_PAIR_TWO_SINK_CHARGE"
    };
    let nonzero33_samples = sample_lines.iter().skip(1).filter(|line| {
        line.rsplit('\t').nth(1) == Some("1")
    }).count();
    let nonzero42_samples = sample_lines.iter().skip(1).filter(|line| line.ends_with("\t1")).count();
    let text = format!(concat!(
        "{{\n",
        "  \"status\":\"{}\",\n",
        "  \"covered_lineage_ids\":[\"D14:222|R:2-3-3\",\"D14:222|R:2-4-2\"],\n",
        "  \"scale_U\":\"{}\",\n",
        "  \"input\":\"{}\",\n",
        "  \"input_sha256_expected\":\"{}\",\n",
        "  \"input_schema\":\"H16ORM1: row24,p2_u8,weight_i128,uses_u64,orbit_u16,stabilizer_u16\",\n",
        "  \"input_records_declared\":{},\n",
        "  \"input_interval\":[{},{}],\n",
        "  \"input_records_consumed\":{},\n",
        "  \"upstream_labelled_p2_uses_before_zero\":{},\n",
        "  \"retained_nonzero_pair_witness_uses\":{},\n",
        "  \"pair_weight_sum_scaled\":\"{}\",\n",
        "  \"sinks\":{{\n",
        "    \"D14:222|R:2-3-3\":{{\"first_tail_degree\":3,\"intermediate_degree\":19,\"terminal_tail_degree\":3,\"first_tail_evaluations\":{},\"pivotable_intermediate_children\":{},\"selected_next_pivots\":{},\"terminal_K22_occurrences\":{},\"full_occurrences\":{},\"irreducible_occurrences\":{},\"pivotable_intermediate_weight_sum_scaled\":\"{}\",\"normalized_next_pivot_weight_sum_scaled\":\"{}\",\"terminal_K22_weight_sum_scaled\":\"{}\",\"full_charge_scaled\":\"{}\",\"irreducible_charge_scaled\":\"{}\",\"response_cache\":{{\"hits\":{},\"misses\":{},\"clears\":{},\"peak_keys_per_worker_chunk\":{},\"cache_chunk_pair_records\":{},\"hard_max_keys_per_worker_sink\":{}}},\"m2_m3_provenance\":{{{}}}}},\n",
        "    \"D14:222|R:2-4-2\":{{\"first_tail_degree\":4,\"intermediate_degree\":20,\"terminal_tail_degree\":2,\"first_tail_evaluations\":{},\"pivotable_intermediate_children\":{},\"selected_next_pivots\":{},\"terminal_K22_occurrences\":{},\"full_occurrences\":{},\"irreducible_occurrences\":{},\"pivotable_intermediate_weight_sum_scaled\":\"{}\",\"normalized_next_pivot_weight_sum_scaled\":\"{}\",\"terminal_K22_weight_sum_scaled\":\"{}\",\"full_charge_scaled\":\"{}\",\"irreducible_charge_scaled\":\"{}\",\"response_cache\":{{\"hits\":{},\"misses\":{},\"clears\":{},\"peak_keys_per_worker_chunk\":{},\"cache_chunk_pair_records\":{},\"hard_max_keys_per_worker_sink\":{}}},\"m2_m3_provenance\":{{{}}}}}\n",
        "  }},\n",
        "  \"stabilizer_histogram\":{{{}}},\n",
        "  \"literal_sample_guard\":{{\"records\":{},\"global_257_mode\":{},\"R233_nonzero_continuations\":{},\"R242_nonzero_continuations\":{},\"all_literal_K22_children_nonpivotable\":true,\"all_abstract_literal_cycle_keys_equal\":true,\"ledger\":\"{}\"}},\n",
        "  \"universal_terminality\":\"asserted for every realized cached abstract response key and every literal sample tail; every K22 signature is tested nonpivotable before full=irreducible\",\n",
        "  \"sign_rule\":\"input w2 is the exact coefficient after D14 R2 and selected K16 p2; first K3/K4 tail preserves w2; selecting an intermediate K19/K20 pivot gives w3=-w2/m3; exact U%(m2*m3)=0 and w2%m3=0 are asserted\",\n",
        "  \"linearity_scope\":\"each exact decorated H-orbit mass fans into both degree-separated terminal scalar sinks; H-invariant scalars permit direct folding without canonical K19/K20/K22 row output\",\n",
        "  \"workers\":{},\n",
        "  \"elapsed_seconds\":{:.6},\n",
        "  \"serial_full_projection_seconds\":{:.6},\n",
        "  \"scope\":\"strict two-ID K22 charge only; no K19/K20/K22 row checkpoint, K23 prolongation, residual, membership, or conjecture verdict\"\n",
        "}}\n"
    ), status, U, input, EXPECTED_INPUT_SHA256, declared, start, end, count,
        UPSTREAM_LABELLED_P2_USES_BEFORE_ZERO, total.pair_uses,
        total.pair_weight_sum,
        total.delta33.k19_children, total.delta33.pivotable_k19_children,
        total.delta33.selected_p3_uses, total.delta33.k21_children,
        total.delta33.k21_children, total.delta33.k21_children,
        total.delta33.pivotable_k19_weight_sum, total.delta33.normalized_p3_weight_sum,
        total.delta33.k21_weight_sum, total.delta33.charge, total.delta33.charge,
        total.cache_hits,
        total.cache_misses, total.cache_clears, total.peak_cache_keys,
        cache_chunk_records, MAX_CACHE_KEYS_PER_WORKER_SINK, prov33_json,
        total.delta42.k19_children, total.delta42.pivotable_k19_children,
        total.delta42.selected_p3_uses, total.delta42.k21_children,
        total.delta42.k21_children, total.delta42.k21_children,
        total.delta42.pivotable_k19_weight_sum, total.delta42.normalized_p3_weight_sum,
        total.delta42.k21_weight_sum, total.delta42.charge, total.delta42.charge,
        total.cache42_hits, total.cache42_misses, total.cache42_clears,
        total.peak_cache42_keys, cache_chunk_records, MAX_CACHE_KEYS_PER_WORKER_SINK, prov42_json,
        stab_json, sample_indices.len(), global_samples, nonzero33_samples,
        nonzero42_samples, sample_path, workers, elapsed, serial_projection,
    );
    let tmp = format!("{}.tmp", output);
    std::fs::write(&tmp, &text).unwrap();
    rename(tmp, output).unwrap();
    print!("{}", text);
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mut input = INPUT.to_string();
    let mut output = "computations/unaudited-codex-orbit0-k22-hidden-pair-fold-2026-08-24/results_hidden_pair_k22_charge.json".to_string();
    let mut start = 0u64;
    let mut end = None;
    let mut workers = 8usize;
    let mut cache_chunk_records = 100_000u64;
    let mut global_samples = false;
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--input" => { input = args[i + 1].clone(); i += 2; }
            "--output" => { output = args[i + 1].clone(); i += 2; }
            "--start" => { start = args[i + 1].parse().unwrap(); i += 2; }
            "--end" => { end = Some(args[i + 1].parse().unwrap()); i += 2; }
            "--workers" => { workers = args[i + 1].parse().unwrap(); i += 2; }
            "--cache-chunk-records" => { cache_chunk_records = args[i + 1].parse().unwrap(); i += 2; }
            "--global-samples" => { global_samples = true; i += 1; }
            _ => panic!("usage: consumer [--input PATH] [--output PATH] [--start N] [--end N] [--workers 1..8] [--cache-chunk-records N] [--global-samples]"),
        }
    }
    consume(&input, &output, start, end, workers, cache_chunk_records, global_samples);
}
