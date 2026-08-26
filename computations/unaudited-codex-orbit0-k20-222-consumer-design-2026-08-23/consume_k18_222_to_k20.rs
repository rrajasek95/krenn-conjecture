//! Prepared, not-yet-launched consumer for the hidden K14 [2,2,2] path.
//!
//! The production input is Generic's H18PIV2 checkpoint.  Each record is one
//! H-canonical pivotable K18 row with its signed H-orbit mass before the third
//! cancellation.  Since both the 77-cycle functional and the next-pivot
//! predicate are H-invariant row properties, their occurrencewise sums are
//! obtained by emitting every available p3 and its 12 K2 tails with
//! coefficient `w3=-w2/m3`; no child-row collection is required.
#![allow(dead_code, unused_imports)]
include!(
    "../unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/run_hidden_children_prefix.rs"
);

const INPUT_MAGIC: &[u8; 8] = b"H18PIV2\0";
const OUTPUT_MAGIC: &[u8; 8] = b"K20P222\0";
const INPUT_RECORD: usize = 80;
const OUTPUT_RECORD: usize = 120;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct Parent3 {
    row: Row,
    weight_before_p3: i128,
    input_index: u64,
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
    records: u64,
    pivot_uses: u64,
    children: u64,
    irreducible_children: u64,
    full: i128,
    irreducible: i128,
}

#[derive(Clone, Copy, Debug, Default)]
struct ProvenanceAgg {
    parents: u64,
    signed_parent_mass: i128,
    pivot_uses: u64,
    children: u64,
    irreducible_children: u64,
    full_charge: i128,
    irreducible_charge: i128,
}

fn decode_parent(input_index: u64, rec: &[u8; INPUT_RECORD]) -> Parent3 {
    let mut row = [0; 24];
    row.copy_from_slice(&rec[..24]);
    let mut witness_pair = [0; 24];
    witness_pair.copy_from_slice(&rec[40..64]);
    assert_eq!(rec[78], 1, "H18PIV2 record is not marked pivotable");
    Parent3 {
        row: Row(row),
        weight_before_p3: i128::from_le_bytes(rec[24..40].try_into().unwrap()),
        input_index,
        witness_pair: Row(witness_pair),
        p2: rec[64],
        t2: rec[65],
        pair_uses: u64::from_le_bytes(rec[66..74].try_into().unwrap()),
        orbit: u16::from_le_bytes(rec[74..76].try_into().unwrap()),
        stabilizer: u16::from_le_bytes(rec[76..78].try_into().unwrap()),
        m2: rec[79],
    }
}

fn encode_parent(x: Parent3) -> [u8; INPUT_RECORD] {
    let mut rec = [0; INPUT_RECORD];
    rec[..24].copy_from_slice(&x.row.0);
    rec[24..40].copy_from_slice(&x.weight_before_p3.to_le_bytes());
    rec[40..64].copy_from_slice(&x.witness_pair.0);
    rec[64] = x.p2;
    rec[65] = x.t2;
    rec[66..74].copy_from_slice(&x.pair_uses.to_le_bytes());
    rec[74..76].copy_from_slice(&x.orbit.to_le_bytes());
    rec[76..78].copy_from_slice(&x.stabilizer.to_le_bytes());
    rec[78] = 1;
    rec[79] = x.m2;
    rec
}

fn validate_parent(x: Parent3, e: &Engine) -> (Vec<usize>, i128) {
    assert_ne!(x.weight_before_p3, 0);
    assert!(x.m2 > 0 && x.pair_uses > 0);
    assert_eq!((x.orbit as u32) * (x.stabilizer as u32), 384);
    let sig = signature(&x.row.0, e);
    let pivots = available(sig, e);
    assert!(!pivots.is_empty());
    let m3 = pivots.len() as i128;
    // m1 is summarized into the signed orbit mass by the pinned producer.
    // This stage directly verifies the only new exact division; the frozen
    // arithmetic-plan theorem separately proves U clears all m1*m2*m3.
    assert_eq!(U % ((x.m2 as i128) * m3), 0);
    assert_eq!(x.weight_before_p3 % m3, 0);
    (pivots, -x.weight_before_p3 / m3)
}

fn provenance_record(
    x: Parent3,
    child: Row,
    p3: usize,
    t3: usize,
    m3: usize,
    w3: i128,
) -> [u8; OUTPUT_RECORD] {
    let mut rec = [0; OUTPUT_RECORD];
    rec[..24].copy_from_slice(&child.0);
    rec[24..40].copy_from_slice(&w3.to_le_bytes());
    rec[40..48].copy_from_slice(&x.input_index.to_le_bytes());
    rec[48..54].copy_from_slice(&[x.p2, x.t2, p3 as u8, t3 as u8, x.m2, m3 as u8]);
    rec[54..62].copy_from_slice(&x.pair_uses.to_le_bytes());
    rec[62..64].copy_from_slice(&x.orbit.to_le_bytes());
    rec[64..66].copy_from_slice(&x.stabilizer.to_le_bytes());
    rec[66..90].copy_from_slice(&x.witness_pair.0);
    rec[90..114].copy_from_slice(&x.row.0);
    rec
}

fn emit_parent(
    x: Parent3,
    e: &Engine,
    c: &CEnv,
    charge: &mut Charge,
    mut provenance: Option<&mut BufWriter<File>>,
) {
    let (pivots, w3) = validate_parent(x, e);
    let m3 = pivots.len();
    charge.records += 1;
    for p3 in pivots {
        charge.pivot_uses += 1;
        for (t3, tail) in e.all_k2[p3].iter().enumerate() {
            let child = replace_anchor(&x.row, &e.anchors[p3], tail);
            let q = *c.dual.get(&literal_ckey(&child, c)).unwrap_or(&0) as i128;
            charge.children += 1;
            charge.full += w3 * q;
            let irreducible = available(signature(&child.0, e), e).is_empty();
            if irreducible {
                charge.irreducible_children += 1;
                charge.irreducible += w3 * q;
            }
            if let Some(w) = provenance.as_deref_mut() {
                w.write_all(&provenance_record(x, child, p3, t3, m3, w3)).unwrap();
            }
        }
    }
}

fn response2_abstract_k20(key: PKey, e: &Engine, c: &CEnv) -> Resp {
    let mut z = Resp::default();
    for tail in &e.all_k2[key.pivot as usize] {
        let ck = abstract_ckey(&key.profile, key.pivot as usize, tail, e, c);
        let q = *c.dual.get(&ck).unwrap_or(&0);
        z.full_n += 1;
        z.full_q += q;
        if !pivotable_sig(child_sig(key.sig, key.pivot as usize, tail, e), e) {
            z.irr_n += 1;
            z.irr_q += q;
        }
    }
    assert_eq!(z.full_n, 12);
    z
}

fn eval_parent_cached(
    x: Parent3,
    e: &Engine,
    c: &CEnv,
    cache: &mut HashMap<PKey, Resp>,
    cache_hits: &mut u64,
    cache_misses: &mut u64,
) -> (Charge, usize) {
    let (pivots, w3) = validate_parent(x, e);
    let m3 = pivots.len();
    let sig = signature(&x.row.0, e);
    let mut out = Charge {
        records: 1,
        ..Charge::default()
    };
    for p3 in pivots {
        out.pivot_uses += 1;
        let key = PKey {
            profile: path_profile(&x.row, p3, e, c),
            sig,
            pivot: p3 as u8,
        };
        let z = if let Some(z) = cache.get(&key) {
            *cache_hits += 1;
            *z
        } else {
            *cache_misses += 1;
            let z = response2_abstract_k20(key, e, c);
            cache.insert(key, z);
            z
        };
        out.children += z.full_n;
        out.irreducible_children += z.irr_n;
        out.full += w3 * z.full_q as i128;
        out.irreducible += w3 * z.irr_q as i128;
    }
    (out, m3)
}

fn add_charge(a: &mut Charge, b: Charge) {
    a.records += b.records;
    a.pivot_uses += b.pivot_uses;
    a.children += b.children;
    a.irreducible_children += b.irreducible_children;
    a.full += b.full;
    a.irreducible += b.irreducible;
}

fn hex24(row: &Row) -> String {
    row.0.iter().map(|x| format!("{:02x}", x)).collect()
}

fn write_output_header(w: &mut BufWriter<File>, input_records: u64) {
    w.write_all(OUTPUT_MAGIC).unwrap();
    w.write_all(&U.to_le_bytes()).unwrap();
    w.write_all(&input_records.to_le_bytes()).unwrap();
    w.write_all(&0u64.to_le_bytes()).unwrap(); // selected p3 uses, finalized later
    w.write_all(&0u64.to_le_bytes()).unwrap(); // emitted children, finalized later
    w.write_all(&(OUTPUT_RECORD as u16).to_le_bytes()).unwrap();
    w.write_all(&[0; 30]).unwrap();
}

fn production(input: &str, output_json: &str, provenance_path: Option<&str>) {
    assert!(provenance_path.is_none(), "full K20 row provenance is forbidden in charge-only mode");
    let e = parse();
    let c = cenv();
    let mut r = BufReader::with_capacity(1 << 20, File::open(input).unwrap());
    let mut h = [0; 80];
    r.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8], INPUT_MAGIC);
    assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()), U);
    assert_eq!(u16::from_le_bytes(h[28..30].try_into().unwrap()) as usize, INPUT_RECORD);
    let n = u64::from_le_bytes(h[48..56].try_into().unwrap());

    let sample_indices: Vec<u64> = (0..257)
        .map(|j| j * (n - 1) / 256)
        .collect::<HashSet<_>>()
        .into_iter()
        .collect();
    let mut sample_indices = sample_indices;
    sample_indices.sort_unstable();
    let mut sample_at = 0usize;
    let mut sample_lines = vec!["input_index\trow\twitness_pair\tweight_before_p3\tm2\tm3\tpivot_uses\ttails\tirreducible_tails\tfull_charge_scaled\tirreducible_charge_scaled\tp2\tt2\tpair_uses\torbit\tstabilizer".to_string()];
    let mut charge = Charge::default();
    let mut response_cache: HashMap<PKey, Resp> = HashMap::new();
    let (mut cache_hits, mut cache_misses) = (0u64, 0u64);
    let mut provenance: std::collections::BTreeMap<(u8, u8), ProvenanceAgg> =
        std::collections::BTreeMap::new();
    for input_index in 0..n {
        let mut rec = [0; INPUT_RECORD];
        r.read_exact(&mut rec).unwrap();
        let x = decode_parent(input_index, &rec);
        let (delta, m3) = eval_parent_cached(
            x,
            &e,
            &c,
            &mut response_cache,
            &mut cache_hits,
            &mut cache_misses,
        );
        add_charge(&mut charge, delta);
        let a = provenance.entry((x.m2, m3 as u8)).or_default();
        a.parents += 1;
        a.signed_parent_mass += x.weight_before_p3;
        a.pivot_uses += delta.pivot_uses;
        a.children += delta.children;
        a.irreducible_children += delta.irreducible_children;
        a.full_charge += delta.full;
        a.irreducible_charge += delta.irreducible;
        if sample_at < sample_indices.len() && input_index == sample_indices[sample_at] {
            sample_at += 1;
            let mut literal = Charge::default();
            emit_parent(x, &e, &c, &mut literal, None);
            assert_eq!(literal, delta);
            sample_lines.push(format!(
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                input_index,
                hex24(&x.row),
                hex24(&x.witness_pair),
                x.weight_before_p3,
                x.m2,
                m3,
                delta.pivot_uses,
                delta.children,
                delta.irreducible_children,
                delta.full,
                delta.irreducible,
                x.p2,
                x.t2,
                x.pair_uses,
                x.orbit,
                x.stabilizer,
            ));
        }
    }
    let mut eof = [0];
    assert_eq!(r.read(&mut eof).unwrap(), 0);
    assert_eq!(sample_at, sample_indices.len());
    assert_eq!(charge.records, n);
    assert_eq!(charge.children, 12 * charge.pivot_uses);
    let prov_totals = provenance.values().fold(ProvenanceAgg::default(), |mut a, b| {
        a.parents += b.parents;
        a.signed_parent_mass += b.signed_parent_mass;
        a.pivot_uses += b.pivot_uses;
        a.children += b.children;
        a.irreducible_children += b.irreducible_children;
        a.full_charge += b.full_charge;
        a.irreducible_charge += b.irreducible_charge;
        a
    });
    assert_eq!(prov_totals.parents, charge.records);
    assert_eq!(prov_totals.pivot_uses, charge.pivot_uses);
    assert_eq!(prov_totals.children, charge.children);
    assert_eq!(prov_totals.irreducible_children, charge.irreducible_children);
    assert_eq!(prov_totals.full_charge, charge.full);
    assert_eq!(prov_totals.irreducible_charge, charge.irreducible);
    let sample_path = format!("{}.samples.tsv", output_json);
    let sample_tmp = format!("{}.tmp", sample_path);
    std::fs::write(&sample_tmp, format!("{}\n", sample_lines.join("\n"))).unwrap();
    rename(sample_tmp, &sample_path).unwrap();
    let hist = provenance
        .iter()
        .map(|(&(m2, m3), a)| format!(
            "\"{}_{}\":{{\"parents\":{},\"signed_parent_mass\":\"{}\",\"pivot_uses\":{},\"children\":{},\"irreducible_children\":{},\"full_charge_scaled\":\"{}\",\"irreducible_charge_scaled\":\"{}\"}}",
            m2, m3, a.parents, a.signed_parent_mass, a.pivot_uses, a.children,
            a.irreducible_children, a.full_charge, a.irreducible_charge
        ))
        .collect::<Vec<_>>()
        .join(",");
    let text = format!(
        "{{\n  \"status\":\"PASS_K20_222_IMMEDIATE_CHARGE\",\n  \"scale\":{},\n  \"input_pivotable_parent_orbits\":{},\n  \"input_weight_sum_scaled\":\"{}\",\n  \"selected_p3_uses\":{},\n  \"representative_tail_terms\":{},\n  \"irreducible_tail_terms\":{},\n  \"full_charge_scaled\":\"{}\",\n  \"irreducible_charge_scaled\":\"{}\",\n  \"response_cache\":{{\"distinct_keys\":{},\"hits\":{},\"misses\":{}}},\n  \"m2_m3_provenance\":{{{}}},\n  \"literal_sample_guard\":{{\"parents\":{},\"ledger\":\"{}\"}},\n  \"sign_rule\":\"w3=-w2/m3; input w2 carries the pinned prior U/(m1*m2) sign\",\n  \"linearity_scope\":\"77-charge and next-pivotability are H-invariant child-row properties, so signed H-orbit masses may be evaluated occurrencewise without child collection\",\n  \"lineage\":\"D14:222|R:2-2-2\",\n  \"scope\":\"immediate occurrencewise 77-charge with bounded aggregate/sample provenance; no canonical K20 row checkpoint, membership, or later tails\"\n}}\n",
        U, charge.records, prov_totals.signed_parent_mass, charge.pivot_uses,
        charge.children, charge.irreducible_children, charge.full, charge.irreducible,
        response_cache.len(), cache_hits, cache_misses, hist, sample_indices.len(), sample_path
    );
    let tmp = format!("{}.tmp", output_json);
    std::fs::write(&tmp, &text).unwrap();
    rename(tmp, output_json).unwrap();
    print!("{}", text);
}

fn self_test() {
    let e = parse();
    let c = cenv();
    let prefix = "computations/unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/k18_k2_canonical_prefix.bin";
    let mut r = BufReader::new(File::open(prefix).unwrap());
    let mut h = [0; 64];
    r.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8], b"H18K2P1\0");
    let n = u64::from_le_bytes(h[48..56].try_into().unwrap());
    let mut parents = Vec::new();
    for input_index in 0..n {
        let mut rec = [0; 76];
        r.read_exact(&mut rec).unwrap();
        if rec[40] == 0 {
            continue;
        }
        let mut rr = [0; 24];
        rr.copy_from_slice(&rec[..24]);
        let row = Row(rr);
        let weight = i128::from_le_bytes(rec[24..40].try_into().unwrap());
        let ps = available(signature(&row.0, &e), &e);
        let m3 = ps.len() as i128;
        let m2 = rec[51];
        if U % ((m2 as i128) * m3) != 0 || weight % m3 != 0 {
            continue;
        }
        let mut witness_pair = [0; 24];
        witness_pair.copy_from_slice(&rec[52..76]);
        parents.push(Parent3 {
            row,
            weight_before_p3: weight,
            input_index,
            witness_pair: Row(witness_pair),
            p2: rec[49],
            t2: rec[50],
            pair_uses: 1,
            orbit: 384,
            stabilizer: 1,
            m2,
        });
        if parents.len() == 256 {
            break;
        }
    }
    assert_eq!(parents.len(), 256);
    // Compare occurrencewise evaluation with signed duplicate collection.
    let mut direct = Charge::default();
    let mut collected: HashMap<Row, i128> = HashMap::new();
    for &x in &parents {
        emit_parent(x, &e, &c, &mut direct, None);
        let (pivots, w3) = validate_parent(x, &e);
        for p3 in pivots {
            for tail in &e.all_k2[p3] {
                let child = replace_anchor(&x.row, &e.anchors[p3], tail);
                add(&mut collected, child, w3);
            }
        }
        assert_eq!(decode_parent(x.input_index, &encode_parent(x)), x);
    }
    let mut full = 0i128;
    let mut irreducible = 0i128;
    for (row, weight) in &collected {
        let q = *c.dual.get(&literal_ckey(row, &c)).unwrap_or(&0) as i128;
        full += weight * q;
        if !pivotable(row, &e) {
            irreducible += weight * q;
        }
    }
    assert_eq!((direct.full, direct.irreducible), (full, irreducible));
    println!(
        "{{\"status\":\"PASS_TINY_CONSUMER_TEST\",\"decorated_parents\":{},\"children\":{},\"collected_rows\":{},\"full_charge_scaled\":\"{}\",\"irreducible_charge_scaled\":\"{}\",\"production_launched\":false}}",
        direct.records, direct.children, collected.len(), direct.full, direct.irreducible
    );
}

#[derive(Clone, Copy)]
struct CheckpointMeta {
    count: u64,
    weight_sum: i128,
    pair_count: u64,
    generated_children: u64,
    sampled: u64,
    regenerated_tails: u64,
    sample_charge: i128,
}

fn scan_checkpoint(
    path: &str,
    magic: &[u8; 8],
    expected_flag: u8,
    expected_count: u64,
    expected_weight: i128,
    e: &Engine,
    c: &CEnv,
) -> CheckpointMeta {
    let mut r = BufReader::with_capacity(16 << 20, File::open(path).unwrap());
    let mut h = [0; 80];
    r.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8], magic);
    assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()), U);
    assert_eq!(u16::from_le_bytes(h[28..30].try_into().unwrap()), 80);
    let pair_count = u64::from_le_bytes(h[32..40].try_into().unwrap());
    let generated_children = u64::from_le_bytes(h[40..48].try_into().unwrap());
    let count = u64::from_le_bytes(h[48..56].try_into().unwrap());
    assert_eq!(count, expected_count);
    assert_eq!(h[56], expected_flag);
    assert!(h[57..64].iter().all(|&x| x == 0));
    let header_weight = i128::from_le_bytes(h[64..80].try_into().unwrap());
    assert_eq!(header_weight, expected_weight);
    assert_eq!(std::fs::metadata(path).unwrap().len(), 80 + 80 * count);

    let sample_indices: Vec<u64> = (0..257)
        .map(|j| j * (count - 1) / 256)
        .collect::<HashSet<_>>()
        .into_iter()
        .collect();
    let mut sample_indices = sample_indices;
    sample_indices.sort_unstable();
    let mut sample_at = 0usize;
    let mut prior: Option<[u8; 24]> = None;
    let mut weight_sum = 0i128;
    let mut sampled = 0u64;
    let mut regenerated_tails = 0u64;
    let mut sample_charge = 0i128;
    let mut canonical_cache = HashMap::new();
    for index in 0..count {
        let mut rec = [0; 80];
        r.read_exact(&mut rec).unwrap();
        let mut row_bytes = [0; 24];
        row_bytes.copy_from_slice(&rec[..24]);
        assert!(row_bytes.windows(2).all(|w| w[0] <= w[1]));
        assert!(prior.map_or(true, |p| p < row_bytes));
        prior = Some(row_bytes);
        let weight = i128::from_le_bytes(rec[24..40].try_into().unwrap());
        assert_ne!(weight, 0);
        weight_sum += weight;
        assert_eq!(rec[78], expected_flag);
        if sample_at < sample_indices.len() && index == sample_indices[sample_at] {
            sample_at += 1;
            sampled += 1;
            let mut witness = [0; 24];
            witness.copy_from_slice(&rec[40..64]);
            let witness = Row(witness);
            let p2 = rec[64] as usize;
            let t2 = rec[65] as usize;
            let uses = u64::from_le_bytes(rec[66..74].try_into().unwrap());
            let orbit = u16::from_le_bytes(rec[74..76].try_into().unwrap());
            let stabilizer = u16::from_le_bytes(rec[76..78].try_into().unwrap());
            let m2 = rec[79] as usize;
            assert!(uses > 0 && m2 > 0 && p2 < 78 && t2 < 12);
            assert_eq!((orbit as u32) * (stabilizer as u32), 384);
            let ps2 = available(signature(&witness.0, e), e);
            assert_eq!(ps2.len(), m2);
            assert!(ps2.contains(&p2));
            let raw_child = replace_anchor(&witness, &e.anchors[p2], &e.all_k2[p2][t2]);
            assert_eq!(canonical(raw_child, e, &mut canonical_cache), Row(row_bytes));

            let ps3 = available(signature(&row_bytes, e), e);
            assert_eq!(!ps3.is_empty(), expected_flag == 1);
            if expected_flag == 1 {
                let m3 = ps3.len() as i128;
                assert_eq!(U % ((m2 as i128) * m3), 0);
                assert_eq!(weight % m3, 0);
                let w3 = -weight / m3;
                for p3 in ps3 {
                    for tail in &e.all_k2[p3] {
                        let child = replace_anchor(&Row(row_bytes), &e.anchors[p3], tail);
                        let q = *c.dual.get(&literal_ckey(&child, c)).unwrap_or(&0) as i128;
                        sample_charge += w3 * q;
                        regenerated_tails += 1;
                    }
                }
            }
        }
    }
    let mut eof = [0];
    assert_eq!(r.read(&mut eof).unwrap(), 0);
    assert_eq!(sample_at, sample_indices.len());
    assert_eq!(weight_sum, header_weight);
    CheckpointMeta {
        count,
        weight_sum,
        pair_count,
        generated_children,
        sampled,
        regenerated_tails,
        sample_charge,
    }
}

fn validate_checkpoints(pivotable: &str, irreducible: &str, output_json: &str) {
    let begun = Instant::now();
    let e = parse();
    let c = cenv();
    let p = scan_checkpoint(
        pivotable,
        b"H18PIV2\0",
        1,
        158_439_965,
        724_159_651_336_720_220_160,
        &e,
        &c,
    );
    let i = scan_checkpoint(
        irreducible,
        b"H18IRR2\0",
        0,
        110_465_931,
        1_030_607_661_835_946_557_440,
        &e,
        &c,
    );
    assert_eq!((p.pair_count, i.pair_count), (101_545_723, 101_545_723));
    assert_eq!(
        (p.generated_children, i.generated_children),
        (1_218_548_676, 1_218_548_676)
    );
    assert_eq!(p.weight_sum + i.weight_sum, 1_754_767_313_172_666_777_600);
    let text = format!(
        "{{\n  \"status\":\"PASS_H18_CHECKPOINT_CONSUMER_SCHEMA\",\n  \"scale\":{},\n  \"pair_orbits\":{},\n  \"generated_K2_children\":{},\n  \"pivotable\":{{\"count\":{},\"weight_sum_scaled\":\"{}\",\"samples\":{},\"regenerated_K2_tails\":{},\"sample_charge_scaled\":\"{}\"}},\n  \"irreducible\":{{\"count\":{},\"weight_sum_scaled\":\"{}\",\"samples\":{}}},\n  \"full_order_scan\":true,\n  \"full_mass_recomputed\":true,\n  \"production_K20_launched\":false,\n  \"elapsed_seconds\":{:.6}\n}}\n",
        U,
        p.pair_count,
        p.generated_children,
        p.count,
        p.weight_sum,
        p.sampled,
        p.regenerated_tails,
        p.sample_charge,
        i.count,
        i.weight_sum,
        i.sampled,
        begun.elapsed().as_secs_f64(),
    );
    let tmp = format!("{}.tmp", output_json);
    std::fs::write(&tmp, &text).unwrap();
    rename(tmp, output_json).unwrap();
    print!("{}", text);
}

#[derive(Clone, Copy, Debug, Default)]
struct DirectProfileStat {
    full_n: u64,
    irreducible_n: u64,
    full_mass: i128,
    irreducible_mass: i128,
}

fn d20_worker(
    e: std::sync::Arc<Engine>,
    c: std::sync::Arc<CEnv>,
    samples: std::sync::Arc<HashSet<u64>>,
    start: usize,
    step: usize,
) -> (
    std::collections::BTreeMap<CKey, DirectProfileStat>,
    Vec<(u64, Row, CKey, i64, bool, i128)>,
) {
    let mut profiles = std::collections::BTreeMap::new();
    let mut sample_rows = Vec::new();
    for ri in (start..e.records.len()).step_by(step) {
        let r = &e.records[ri];
        let mass = -(r.coefficient as i128) * (r.size as i128) * U;
        let mut local = 0u64;
        for a in &e.factor_tails[0][2] {
            for b in &e.factor_tails[1][2] {
                for d in &e.factor_tails[2][2] {
                    let index = ri as u64 * 216_000 + local;
                    local += 1;
                    let row = make_row(r, a, b, d);
                    let key = literal_ckey(&row, &c);
                    let q = *c.dual.get(&key).unwrap_or(&0);
                    let irreducible = available(signature(&row.0, &e), &e).is_empty();
                    let z = profiles.entry(key).or_insert(DirectProfileStat::default());
                    z.full_n += 1;
                    z.full_mass += mass;
                    if irreducible {
                        z.irreducible_n += 1;
                        z.irreducible_mass += mass;
                    }
                    if samples.contains(&index) {
                        sample_rows.push((index, row, key, q, irreducible, mass));
                    }
                }
            }
        }
        assert_eq!(local, 216_000);
    }
    (profiles, sample_rows)
}

fn ckey_text(k: CKey) -> String {
    let n = k.0[0] as usize;
    k.0[1..1 + n]
        .iter()
        .map(|x| x.to_string())
        .collect::<Vec<_>>()
        .join("+")
}

fn direct_d20(output_json: &str) {
    let begun = Instant::now();
    let e = std::sync::Arc::new(parse());
    let c = std::sync::Arc::new(cenv());
    assert!(e.factor_tails.iter().all(|f| f[2].len() == 60));
    let total = 485u64 * 216_000;
    let samples: HashSet<u64> = (0..257).map(|j| j * (total - 1) / 256).collect();
    let samples = std::sync::Arc::new(samples);
    let workers = 8usize;
    let mut jobs = Vec::new();
    for t in 0..workers {
        let ee = e.clone();
        let cc = c.clone();
        let ss = samples.clone();
        jobs.push(std::thread::spawn(move || d20_worker(ee, cc, ss, t, workers)));
    }
    let mut profiles: std::collections::BTreeMap<CKey, DirectProfileStat> =
        std::collections::BTreeMap::new();
    let mut sample_rows = Vec::new();
    for job in jobs {
        let (p, s) = job.join().unwrap();
        for (k, v) in p {
            let z = profiles.entry(k).or_default();
            z.full_n += v.full_n;
            z.irreducible_n += v.irreducible_n;
            z.full_mass += v.full_mass;
            z.irreducible_mass += v.irreducible_mass;
        }
        sample_rows.extend(s);
    }
    sample_rows.sort_unstable_by_key(|x| x.0);
    assert_eq!(sample_rows.len(), samples.len());
    let full_n: u64 = profiles.values().map(|x| x.full_n).sum();
    let irreducible_n: u64 = profiles.values().map(|x| x.irreducible_n).sum();
    assert_eq!(full_n, total);
    let full_charge: i128 = profiles
        .iter()
        .map(|(k, v)| v.full_mass * (*c.dual.get(k).unwrap_or(&0) as i128))
        .sum();
    let irreducible_charge: i128 = profiles
        .iter()
        .map(|(k, v)| v.irreducible_mass * (*c.dual.get(k).unwrap_or(&0) as i128))
        .sum();
    // The literal sample charge is independently reconstructed from the
    // stored q value rather than the profile histogram totals.
    let sample_full: i128 = sample_rows.iter().map(|x| x.5 * x.3 as i128).sum();
    let sample_irreducible: i128 = sample_rows
        .iter()
        .filter(|x| x.4)
        .map(|x| x.5 * x.3 as i128)
        .sum();
    let profile_path = format!("{}.profiles.tsv", output_json);
    let mut lines = vec!["cycle_partition\tfull_occurrences\tirreducible_occurrences\tfull_mass_scaled\tirreducible_mass_scaled\tdual".to_string()];
    for (k, v) in &profiles {
        lines.push(format!(
            "{}\t{}\t{}\t{}\t{}\t{}",
            ckey_text(*k), v.full_n, v.irreducible_n, v.full_mass,
            v.irreducible_mass, c.dual.get(k).unwrap_or(&0)
        ));
    }
    let tmp = format!("{}.tmp", profile_path);
    std::fs::write(&tmp, format!("{}\n", lines.join("\n"))).unwrap();
    rename(tmp, &profile_path).unwrap();
    let sample_path = format!("{}.samples.tsv", output_json);
    let mut slines = vec!["index\trow\tcycle_partition\tdual\tirreducible\tmass_scaled".to_string()];
    for (index, row, k, q, irreducible, mass) in &sample_rows {
        slines.push(format!("{}\t{}\t{}\t{}\t{}\t{}", index, hex24(row), ckey_text(*k), q, irreducible, mass));
    }
    let tmp = format!("{}.tmp", sample_path);
    std::fs::write(&tmp, format!("{}\n", slines.join("\n"))).unwrap();
    rename(tmp, &sample_path).unwrap();
    let text = format!(
        "{{\n  \"status\":\"PASS_DIRECT_D20_444_IMMEDIATE_CHARGE\",\n  \"dag_id\":\"D20:444|R:direct\",\n  \"scale\":{},\n  \"source_records\":485,\n  \"factor_K4_counts\":[60,60,60],\n  \"full_occurrences\":{},\n  \"irreducible_occurrences\":{},\n  \"cycle_profiles\":{},\n  \"full_charge_scaled\":\"{}\",\n  \"irreducible_charge_scaled\":\"{}\",\n  \"literal_sample_guard\":{{\"rows\":{},\"full_charge_scaled\":\"{}\",\"irreducible_charge_scaled\":\"{}\",\"ledger\":\"{}\"}},\n  \"profile_guard\":{{\"full_count_reconstructed\":{},\"irreducible_count_reconstructed\":{},\"ledger\":\"{}\"}},\n  \"scope\":\"direct D20 scalar 77-charge only; no row collection or K21 tails\",\n  \"elapsed_seconds\":{:.6}\n}}\n",
        U, full_n, irreducible_n, profiles.len(), full_charge, irreducible_charge,
        sample_rows.len(), sample_full, sample_irreducible, sample_path,
        full_n, irreducible_n, profile_path, begun.elapsed().as_secs_f64()
    );
    let tmp = format!("{}.tmp", output_json);
    std::fs::write(&tmp, &text).unwrap();
    rename(tmp, output_json).unwrap();
    print!("{}", text);
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() == 2 && args[1] == "--self-test" {
        self_test();
        return;
    }
    if args.len() == 5 && args[1] == "--validate-checkpoints" {
        validate_checkpoints(&args[2], &args[3], &args[4]);
        return;
    }
    if args.len() == 3 && args[1] == "--direct-d20" {
        direct_d20(&args[2]);
        return;
    }
    assert!(
        args.len() == 3 || args.len() == 5,
        "usage: consumer INPUT.bin RESULT.json [--provenance K20.bin], or --self-test"
    );
    let provenance = if args.len() == 5 {
        assert_eq!(args[3], "--provenance");
        Some(args[4].as_str())
    } else {
        None
    };
    production(&args[1], &args[2], provenance);
}
