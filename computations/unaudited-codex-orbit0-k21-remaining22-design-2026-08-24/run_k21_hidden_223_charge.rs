//! Exact charge-only consumer for D14:222|R:2-2-3.
//!
//! The input is the independently validated H18PIV2 checkpoint.  It stores
//! one H-canonical pivotable K18 row and its total signed H-orbit mass per
//! record.  The 77-cycle functional is H-invariant, and every K21 child is
//! terminal/nonpivotable, so the K3 response may be evaluated occurrencewise
//! without collecting K21 rows.
#![allow(dead_code, unused_imports)]

include!(
    "../unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/run_hidden_children_prefix.rs"
);

use std::collections::BTreeMap;

const INPUT_MAGIC: &[u8; 8] = b"H18PIV2\0";
const INPUT_RECORD: usize = 80;
const EXPECTED_RECORDS: u64 = 158_439_965;
const EXPECTED_INPUT_MASS: i128 = 724_159_651_336_720_220_160;
const EXPECTED_PAIR_ORBITS: u64 = 101_545_723;
const EXPECTED_PRIOR_CHILDREN: u64 = 1_218_548_676;
const EXPECTED_PIVOT_USES: u64 = 399_275_484;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct Parent3 {
    row: Row,
    weight_before_p3: i128,
    witness_pair: Row,
    p2: u8,
    t2: u8,
    pair_uses: u64,
    orbit: u16,
    stabilizer: u16,
    m2: u8,
}

#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
struct Charge {
    parents: u64,
    pivot_uses: u64,
    children: u64,
    value: i128,
}

#[derive(Clone, Copy, Debug, Default)]
struct ProvenanceAgg {
    parents: u64,
    signed_parent_mass: i128,
    pivot_uses: u64,
    children: u64,
    charge: i128,
}

fn decode_parent(rec: &[u8; INPUT_RECORD]) -> Parent3 {
    let mut row = [0; 24];
    row.copy_from_slice(&rec[..24]);
    let mut witness_pair = [0; 24];
    witness_pair.copy_from_slice(&rec[40..64]);
    assert_eq!(rec[78], 1, "H18PIV2 record is not pivotable");
    Parent3 {
        row: Row(row),
        weight_before_p3: i128::from_le_bytes(rec[24..40].try_into().unwrap()),
        witness_pair: Row(witness_pair),
        p2: rec[64],
        t2: rec[65],
        pair_uses: u64::from_le_bytes(rec[66..74].try_into().unwrap()),
        orbit: u16::from_le_bytes(rec[74..76].try_into().unwrap()),
        stabilizer: u16::from_le_bytes(rec[76..78].try_into().unwrap()),
        m2: rec[79],
    }
}

fn validate_parent(x: Parent3, e: &Engine) -> (Vec<usize>, i128) {
    assert_ne!(x.weight_before_p3, 0);
    assert!(x.m2 > 0 && x.pair_uses > 0);
    assert_eq!((x.orbit as u32) * (x.stabilizer as u32), 384);
    let pivots = available(signature(&x.row.0, e), e);
    assert!(!pivots.is_empty());
    let m3 = pivots.len() as i128;
    assert_eq!(U % ((x.m2 as i128) * m3), 0);
    assert_eq!(x.weight_before_p3 % m3, 0);
    (pivots, -x.weight_before_p3 / m3)
}

fn response3_abstract_k21(key: PKey, e: &Engine, c: &CEnv) -> Resp {
    let mut z = Resp::default();
    for tail in &e.all_k3[key.pivot as usize] {
        assert!(
            !pivotable_sig(
                child_sig(key.sig, key.pivot as usize, tail, e),
                e,
            ),
            "realized abstract K21 response key remained pivotable",
        );
        let ck = abstract_ckey(&key.profile, key.pivot as usize, tail, e, c);
        z.full_n += 1;
        z.full_q += *c.dual.get(&ck).unwrap_or(&0);
    }
    assert_eq!(z.full_n, 32);
    // The recurrence DAG proves that K20 is the last pivotable parent page;
    // K21 tails are all terminal.  Literal samples below replay this property.
    z.irr_n = z.full_n;
    z.irr_q = z.full_q;
    z
}

fn eval_parent_cached(
    x: Parent3,
    e: &Engine,
    c: &CEnv,
    cache: &mut HashMap<PKey, Resp>,
    hits: &mut u64,
    misses: &mut u64,
) -> (Charge, usize) {
    let (pivots, w3) = validate_parent(x, e);
    let m3 = pivots.len();
    let sig = signature(&x.row.0, e);
    let mut out = Charge { parents: 1, ..Charge::default() };
    for p3 in pivots {
        out.pivot_uses += 1;
        let key = PKey {
            profile: path_profile(&x.row, p3, e, c),
            sig,
            pivot: p3 as u8,
        };
        let z = if let Some(z) = cache.get(&key) {
            *hits += 1;
            *z
        } else {
            *misses += 1;
            let z = response3_abstract_k21(key, e, c);
            cache.insert(key, z);
            z
        };
        out.children += z.full_n;
        out.value += w3 * z.full_q as i128;
    }
    (out, m3)
}

fn eval_parent_literal(x: Parent3, e: &Engine, c: &CEnv) -> Charge {
    let (pivots, w3) = validate_parent(x, e);
    let mut out = Charge { parents: 1, ..Charge::default() };
    for p3 in pivots {
        out.pivot_uses += 1;
        let profile = path_profile(&x.row, p3, e, c);
        for tail in &e.all_k3[p3] {
            let child = replace_anchor(&x.row, &e.anchors[p3], tail);
            assert!(available(signature(&child.0, e), e).is_empty());
            let literal = literal_ckey(&child, c);
            let abstracted = abstract_ckey(&profile, p3, tail, e, c);
            assert_eq!(literal, abstracted);
            out.children += 1;
            out.value += w3 * (*c.dual.get(&literal).unwrap_or(&0) as i128);
        }
    }
    out
}

fn add_charge(a: &mut Charge, b: Charge) {
    a.parents += b.parents;
    a.pivot_uses += b.pivot_uses;
    a.children += b.children;
    a.value += b.value;
}

fn hex24(row: &Row) -> String {
    row.0.iter().map(|x| format!("{:02x}", x)).collect()
}

fn consume(input: &str, output: &str, limit: Option<u64>) {
    let begun = Instant::now();
    let e = parse();
    let c = cenv();
    let mut r = BufReader::with_capacity(16 << 20, File::open(input).unwrap());
    let mut h = [0; 80];
    r.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8], INPUT_MAGIC);
    assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()), U);
    assert_eq!(u16::from_le_bytes(h[28..30].try_into().unwrap()) as usize, INPUT_RECORD);
    let pair_orbits = u64::from_le_bytes(h[32..40].try_into().unwrap());
    let prior_children = u64::from_le_bytes(h[40..48].try_into().unwrap());
    let declared = u64::from_le_bytes(h[48..56].try_into().unwrap());
    let declared_mass = i128::from_le_bytes(h[64..80].try_into().unwrap());
    assert_eq!(pair_orbits, EXPECTED_PAIR_ORBITS);
    assert_eq!(prior_children, EXPECTED_PRIOR_CHILDREN);
    assert_eq!(declared, EXPECTED_RECORDS);
    assert_eq!(declared_mass, EXPECTED_INPUT_MASS);
    let n = limit.unwrap_or(declared).min(declared);

    let sample_indices: HashSet<u64> = if n < 257 {
        (0..n).collect()
    } else {
        (0..257).map(|j| j * (n - 1) / 256).collect()
    };
    let mut sample_lines = vec![
        "input_index\trow\twitness_pair\tweight_before_p3\tm2\tm3\tpivot_uses\tK3_children\tcharge_scaled\tp2\tt2\tpair_uses\torbit\tstabilizer".to_string()
    ];
    let mut cache: HashMap<PKey, Resp> = HashMap::new();
    let (mut hits, mut misses) = (0u64, 0u64);
    let mut total = Charge::default();
    let mut mass = 0i128;
    let mut prior: Option<[u8; 24]> = None;
    let mut provenance: BTreeMap<(u8, u8), ProvenanceAgg> = BTreeMap::new();
    for index in 0..n {
        let mut rec = [0; INPUT_RECORD];
        r.read_exact(&mut rec).unwrap();
        let x = decode_parent(&rec);
        assert!(x.row.0.windows(2).all(|w| w[0] <= w[1]));
        assert!(prior.map_or(true, |p| p < x.row.0));
        prior = Some(x.row.0);
        mass += x.weight_before_p3;
        let (delta, m3) = eval_parent_cached(x, &e, &c, &mut cache, &mut hits, &mut misses);
        add_charge(&mut total, delta);
        let a = provenance.entry((x.m2, m3 as u8)).or_default();
        a.parents += 1;
        a.signed_parent_mass += x.weight_before_p3;
        a.pivot_uses += delta.pivot_uses;
        a.children += delta.children;
        a.charge += delta.value;
        if sample_indices.contains(&index) {
            let literal = eval_parent_literal(x, &e, &c);
            assert_eq!(literal, delta);
            sample_lines.push(format!(
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                index, hex24(&x.row), hex24(&x.witness_pair), x.weight_before_p3,
                x.m2, m3, delta.pivot_uses, delta.children, delta.value,
                x.p2, x.t2, x.pair_uses, x.orbit, x.stabilizer,
            ));
        }
    }
    assert_eq!(total.parents, n);
    assert_eq!(total.children, 32 * total.pivot_uses);
    if n == declared {
        let mut eof = [0];
        assert_eq!(r.read(&mut eof).unwrap(), 0);
        assert_eq!(mass, EXPECTED_INPUT_MASS);
        assert_eq!(total.pivot_uses, EXPECTED_PIVOT_USES);
        assert_eq!(total.children, 12_776_815_488);
    }
    let prov = provenance.values().fold(ProvenanceAgg::default(), |mut a, b| {
        a.parents += b.parents;
        a.signed_parent_mass += b.signed_parent_mass;
        a.pivot_uses += b.pivot_uses;
        a.children += b.children;
        a.charge += b.charge;
        a
    });
    assert_eq!(prov.parents, total.parents);
    assert_eq!(prov.signed_parent_mass, mass);
    assert_eq!(prov.pivot_uses, total.pivot_uses);
    assert_eq!(prov.children, total.children);
    assert_eq!(prov.charge, total.value);

    let sample_path = format!("{}.samples.tsv", output);
    let sample_tmp = format!("{}.tmp", sample_path);
    std::fs::write(&sample_tmp, format!("{}\n", sample_lines.join("\n"))).unwrap();
    rename(sample_tmp, &sample_path).unwrap();
    let hist = provenance.iter().map(|(&(m2, m3), a)| format!(
        "\"{}_{}\":{{\"parents\":{},\"signed_parent_mass_scaled\":\"{}\",\"pivot_uses\":{},\"K3_children\":{},\"charge_scaled\":\"{}\"}}",
        m2, m3, a.parents, a.signed_parent_mass, a.pivot_uses, a.children, a.charge
    )).collect::<Vec<_>>().join(",");
    let status = if n == declared {
        "PASS_COMPLETE_D14_222_R_2_2_3_K21_CHARGE"
    } else {
        "PASS_BOUNDED_PREFIX_D14_222_R_2_2_3_K21_CHARGE"
    };
    let text = format!(
        concat!(
            "{{\n",
            "  \"status\":\"{}\",\n",
            "  \"lineage_id\":\"D14:222|R:2-2-3\",\n",
            "  \"scale_U\":\"{}\",\n",
            "  \"input\":\"{}\",\n",
            "  \"input_records_consumed\":{},\n",
            "  \"input_records_declared\":{},\n",
            "  \"input_weight_sum_scaled\":\"{}\",\n",
            "  \"selected_p3_uses\":{},\n",
            "  \"K3_tail_occurrences\":{},\n",
            "  \"full_occurrences\":{},\n",
            "  \"irreducible_occurrences\":{},\n",
            "  \"full_charge_scaled\":\"{}\",\n",
            "  \"irreducible_charge_scaled\":\"{}\",\n",
            "  \"response_cache\":{{\"distinct_keys\":{},\"hits\":{},\"misses\":{}}},\n",
            "  \"m2_m3_provenance\":{{{}}},\n",
            "  \"literal_sample_guard\":{{\"parents\":{},\"all_K21_children_nonpivotable\":true,\"abstract_literal_cycle_keys_equal\":true,\"ledger\":\"{}\"}},\n",
            "  \"sign_rule\":\"w3=-w2/m3; input w2 already carries the prior U/(m1*m2) sign\",\n",
            "  \"linearity_scope\":\"the 77-cycle functional is H-invariant and K21 is terminal, so exact H-orbit masses are evaluated occurrencewise without K21 row collection\",\n",
            "  \"scope\":\"one exact K21 scalar lineage only; no K21 row checkpoint, K22 tail, residual assembly, membership, or conjecture verdict\",\n",
            "  \"elapsed_seconds\":{:.6}\n",
            "}}\n"
        ),
        status, U, input, n, declared, mass, total.pivot_uses, total.children,
        total.children, total.children, total.value, total.value,
        cache.len(), hits, misses, hist, sample_indices.len(), sample_path,
        begun.elapsed().as_secs_f64(),
    );
    let tmp = format!("{}.tmp", output);
    std::fs::write(&tmp, &text).unwrap();
    rename(tmp, output).unwrap();
    print!("{}", text);
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    assert!(args.len() == 3 || args.len() == 5,
        "usage: consumer INPUT.bin RESULT.json [--limit N]");
    let limit = if args.len() == 5 {
        assert_eq!(args[3], "--limit");
        Some(args[4].parse().unwrap())
    } else {
        None
    };
    consume(&args[1], &args[2], limit);
}
