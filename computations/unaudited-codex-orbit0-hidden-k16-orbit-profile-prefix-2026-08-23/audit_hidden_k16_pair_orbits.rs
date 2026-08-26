// Exact bounded one-H-slice test of orbit-aware hidden-K16 -> K18/K2 collection.
//
// The frozen 29-byte path profile is deliberately retained only as a quotient
// diagnostic.  Literal K2 transport is performed on H-orbits of the decorated
// pair (literal parent row, selected second pivot).
include!("../unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/run_hidden_children_prefix.rs");

use std::collections::BTreeMap;

const NEW_ODIR: &str =
    "computations/unaudited-codex-orbit0-hidden-k16-orbit-profile-prefix-2026-08-23/";
const REFERENCE: &str =
    "computations/unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/k18_k2_canonical_prefix.bin";

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct PairKey {
    row: Row,
    pivot: u8,
}

#[derive(Clone, Copy, Debug, Default)]
struct PairAgg {
    weight: i128,
    uses: u64,
}

fn hex(bytes: &[u8]) -> String {
    const H: &[u8; 16] = b"0123456789abcdef";
    let mut s = String::with_capacity(2 * bytes.len());
    for &b in bytes {
        s.push(H[(b >> 4) as usize] as char);
        s.push(H[(b & 15) as usize] as char);
    }
    s
}

fn add_pair(map: &mut HashMap<PairKey, PairAgg>, key: PairKey, weight: i128) {
    use std::collections::hash_map::Entry;
    match map.entry(key) {
        Entry::Vacant(v) => {
            v.insert(PairAgg { weight, uses: 1 });
        }
        Entry::Occupied(mut o) => {
            let x = o.get_mut();
            x.weight += weight;
            x.uses += 1;
            if x.weight == 0 {
                o.remove();
            }
        }
    }
}

fn pivot_permutations(e: &Engine) -> Vec<[u8; 78]> {
    let mut lookup = HashMap::new();
    for (p, &a) in e.anchors.iter().enumerate() {
        assert_eq!(lookup.insert(a, p as u8), None);
    }
    let mut out = Vec::with_capacity(e.transforms.len());
    for t in &e.transforms {
        let mut pp = [0u8; 78];
        for (p, a) in e.anchors.iter().enumerate() {
            let mut moved = a.map(|c| t[c as usize]);
            moved.sort_unstable();
            pp[p] = *lookup.get(&moved).expect("H must permute the 78 anchors");
        }
        out.push(pp);
    }
    out
}

fn move_pair(key: PairKey, action: usize, e: &Engine, pp: &[[u8; 78]]) -> PairKey {
    let t = &e.transforms[action];
    let mut row = key.row.0.map(|c| t[c as usize]);
    row.sort_unstable();
    PairKey {
        row: Row(row),
        pivot: pp[action][key.pivot as usize],
    }
}

// Match the frozen canonical-row convention: minimize signature first, then
// literal row, with the decorated pivot as the final tie-breaker.
fn canonical_pair(
    key: PairKey,
    e: &Engine,
    pp: &[[u8; 78]],
    sig_actions: &mut HashMap<[u8; 12], Vec<usize>>,
) -> PairKey {
    let s = signature(&key.row.0, e);
    let actions = sig_actions.entry(s).or_insert_with(|| {
        let mut best = None;
        let mut keep = Vec::new();
        for (action, p) in e.permutations.iter().enumerate() {
            let x = sig_move(s, p);
            if best.map_or(true, |b| x < b) {
                best = Some(x);
                keep.clear();
                keep.push(action);
            } else if Some(x) == best {
                keep.push(action);
            }
        }
        keep
    });
    actions
        .iter()
        .map(|&action| move_pair(key, action, e, pp))
        .min()
        .unwrap()
}

fn orbit_stabilizer(
    key: PairKey,
    e: &Engine,
    pp: &[[u8; 78]],
    stabilizer_actions: &mut HashMap<[u8; 12], Vec<usize>>,
) -> (usize, usize) {
    // An action fixing the decorated pair must first fix its 12-anchor
    // signature.  Caching that much smaller candidate subgroup makes the
    // stabilizer audit usable in the full external-merge design.
    let s = signature(&key.row.0, e);
    let actions = stabilizer_actions.entry(s).or_insert_with(|| {
        e.permutations
            .iter()
            .enumerate()
            .filter_map(|(action, p)| (sig_move(s, p) == s).then_some(action))
            .collect()
    });
    let stabilizer = actions
        .iter()
        .filter(|&&action| move_pair(key, action, e, pp) == key)
        .count();
    assert!(stabilizer > 0 && 384 % stabilizer == 0);
    (384 / stabilizer, stabilizer)
}

fn read_reference() -> HashMap<Row, (i128, bool)> {
    let b = read(REFERENCE).unwrap();
    assert_eq!(&b[..8], b"H18K2P1\0");
    assert_eq!(i128::from_le_bytes(b[8..24].try_into().unwrap()), U);
    let n = u64::from_le_bytes(b[48..56].try_into().unwrap()) as usize;
    assert_eq!(u16::from_le_bytes(b[56..58].try_into().unwrap()), 76);
    assert_eq!(b.len(), 64 + 76 * n);
    let mut out = HashMap::with_capacity(n);
    for rec in b[64..].chunks_exact(76) {
        let mut row = [0u8; 24];
        row.copy_from_slice(&rec[..24]);
        let weight = i128::from_le_bytes(rec[24..40].try_into().unwrap());
        assert!(out.insert(Row(row), (weight, rec[40] != 0)).is_none());
    }
    out
}

#[cfg(not(feature = "full_orbit_k2"))]
fn main() {
    std::fs::create_dir_all(NEW_ODIR).unwrap();
    let begun = Instant::now();
    let e = parse();
    let c = cenv();
    let pp = pivot_permutations(&e);
    assert_eq!(pp.len(), 384);

    let mut r = BufReader::with_capacity(
        1 << 20,
        File::open(format!("{}parents_000_016.bin", HDIR)).unwrap(),
    );
    let mut header = [0u8; 40];
    r.read_exact(&mut header).unwrap();
    assert_eq!(&header[..8], b"H16RUN2\0");
    assert_eq!(i128::from_le_bytes(header[8..24].try_into().unwrap()), U);
    assert!(PARENTS <= u64::from_le_bytes(header[32..40].try_into().unwrap()));

    // First aggregate exact labelled decorated pairs.  This is already a
    // lossless reduction of repeated parent/pivot occurrences.
    let mut exact_pairs: HashMap<PairKey, PairAgg> = HashMap::new();
    let mut incoming_sum = 0i128;
    let mut outgoing = 0u64;
    for _parent in 0..PARENTS {
        let mut rec = [0u8; 64];
        r.read_exact(&mut rec).unwrap();
        let mut rr = [0u8; 24];
        rr.copy_from_slice(&rec[..24]);
        let row = Row(rr);
        let w1 = i128::from_le_bytes(rec[24..40].try_into().unwrap());
        let mut s = [0u8; 12];
        s.copy_from_slice(&rec[40..52]);
        assert_eq!(signature(&row.0, &e), s);
        let m2 = rec[60] as usize;
        let ps = available(s, &e);
        assert_eq!(ps.len(), m2);
        assert_eq!(w1 % m2 as i128, 0);
        let w2 = -w1 / m2 as i128;
        for p in ps {
            outgoing += 1;
            incoming_sum += w2;
            add_pair(
                &mut exact_pairs,
                PairKey { row, pivot: p as u8 },
                w2,
            );
        }
    }
    let exact_nonzero = exact_pairs.len();
    let input_done = begun.elapsed().as_secs_f64();

    // Canonicalize decorated pairs under H and carry total coefficient/mass.
    let mut pair_cache = HashMap::new();
    let mut sig_actions = HashMap::new();
    let mut pair_orbits: HashMap<PairKey, PairAgg> = HashMap::new();
    for (key, a) in &exact_pairs {
        let q = *pair_cache
            .entry(*key)
            .or_insert_with(|| canonical_pair(*key, &e, &pp, &mut sig_actions));
        use std::collections::hash_map::Entry;
        match pair_orbits.entry(q) {
            Entry::Vacant(v) => {
                v.insert(*a);
            }
            Entry::Occupied(mut o) => {
                let x = o.get_mut();
                x.weight += a.weight;
                x.uses += a.uses;
                if x.weight == 0 {
                    o.remove();
                }
            }
        }
    }
    let pair_orbit_nonzero = pair_orbits.len();
    assert_eq!(pair_orbits.values().map(|a| a.weight).sum::<i128>(), incoming_sum);
    let orbit_collect_done = begun.elapsed().as_secs_f64();

    let mut orbit_hist: BTreeMap<usize, usize> = BTreeMap::new();
    let mut stab_hist: BTreeMap<usize, usize> = BTreeMap::new();
    let mut sig_stab_action_hist: BTreeMap<usize, usize> = BTreeMap::new();
    let mut stabilizer_actions = HashMap::new();
    let mut orbit_data = HashMap::new();
    for &q in pair_orbits.keys() {
        let (os, ss) = orbit_stabilizer(q, &e, &pp, &mut stabilizer_actions);
        *orbit_hist.entry(os).or_default() += 1;
        *stab_hist.entry(ss).or_default() += 1;
        orbit_data.insert(q, (os, ss));
    }
    for actions in stabilizer_actions.values() {
        *sig_stab_action_hist.entry(actions.len()).or_default() += 1;
    }
    let stabilizer_done = begun.elapsed().as_secs_f64();

    // Decisive quotient guard: an identical stored PKey may contain several
    // distinct decorated H-orbits, so one witness/PKey cannot generate the
    // literal K2 family source-faithfully.
    let mut coarse_to_orbits: HashMap<PKey, HashSet<PairKey>> = HashMap::new();
    for &key in exact_pairs.keys() {
        let p = key.pivot as usize;
        let pk = PKey {
            profile: path_profile(&key.row, p, &e, &c),
            sig: signature(&key.row.0, &e),
            pivot: key.pivot,
        };
        let q = *pair_cache.get(&key).unwrap();
        coarse_to_orbits.entry(pk).or_default().insert(q);
    }
    let coarse_keys = coarse_to_orbits.len();
    let coarse_ambiguous = coarse_to_orbits.values().filter(|x| x.len() > 1).count();
    let coarse_max_pair_orbits = coarse_to_orbits.values().map(HashSet::len).max().unwrap();
    let coarse_pair_orbit_incidences: usize = coarse_to_orbits.values().map(HashSet::len).sum();
    let (bad_pk, bad_set) = coarse_to_orbits
        .iter()
        .filter(|(_, x)| x.len() > 1)
        .min_by_key(|(k, _)| **k)
        .unwrap();
    let mut bad_pairs: Vec<_> = bad_set.iter().copied().collect();
    bad_pairs.sort_unstable();
    let mut counterexample = format!(
        "profile_hex\tsignature_hex\tpivot\tdecorated_pair_orbits\n{}\t{}\t{}\t{}\n\nrow_hex\tpivot\n",
        hex(&bad_pk.profile),
        hex(&bad_pk.sig),
        bad_pk.pivot,
        bad_pairs.len(),
    );
    for q in bad_pairs.iter().take(2) {
        counterexample.push_str(&format!("{}\t{}\n", hex(&q.row.0), q.pivot));
    }
    std::fs::write(
        format!("{}coarse_profile_counterexample.tsv", NEW_ODIR),
        counterexample,
    )
    .unwrap();
    let quotient_guard_done = begun.elapsed().as_secs_f64();

    // Generate one 12-child family per decorated pair orbit, then use the
    // frozen child canonicalization.  Equivariance says this must equal the
    // literal occurrence-by-occurrence map; the exact checkpoint comparison
    // below is the bounded replay guard.
    let mut literal_children: HashMap<Row, i128> = HashMap::new();
    for (key, a) in &pair_orbits {
        for tail in &e.all_k2[key.pivot as usize] {
            let child = replace_anchor(&key.row, &e.anchors[key.pivot as usize], tail);
            add(&mut literal_children, child, a.weight);
        }
    }
    let generated_children = 12 * pair_orbit_nonzero;
    let literal_child_support = literal_children.len();
    let mut child_cache = HashMap::new();
    let mut children: HashMap<Row, i128> = HashMap::new();
    for (child, weight) in literal_children {
        let q = canonical(child, &e, &mut child_cache);
        add(&mut children, q, weight);
    }
    assert_eq!(children.values().sum::<i128>(), 12 * incoming_sum);
    let child_done = begun.elapsed().as_secs_f64();

    let reference = read_reference();
    let mut mismatches = 0usize;
    let mut pivotability_mismatches = 0usize;
    let mut union = HashSet::new();
    union.extend(reference.keys().copied());
    union.extend(children.keys().copied());
    for row in union {
        let got = children.get(&row).copied().unwrap_or(0);
        let want = reference.get(&row).map(|x| x.0).unwrap_or(0);
        if got != want {
            mismatches += 1;
        }
        if let Some((_, p)) = reference.get(&row) {
            if pivotable(&row, &e) != *p {
                pivotability_mismatches += 1;
            }
        }
    }
    assert_eq!(mismatches, 0);
    assert_eq!(pivotability_mismatches, 0);
    assert_eq!(children.len(), reference.len());
    let reference_done = begun.elapsed().as_secs_f64();

    // Compact, restartable orbit ledger for the bounded prefix.
    let mut pairs: Vec<_> = pair_orbits.into_iter().collect();
    pairs.sort_unstable_by_key(|x| x.0);
    let ledger = format!("{}decorated_pair_orbits_prefix.bin", NEW_ODIR);
    let mut w = BufWriter::new(File::create(&ledger).unwrap());
    w.write_all(b"H16PORB1").unwrap();
    w.write_all(&U.to_le_bytes()).unwrap();
    w.write_all(&0u16.to_le_bytes()).unwrap();
    w.write_all(&[0; 6]).unwrap();
    w.write_all(&(pairs.len() as u64).to_le_bytes()).unwrap();
    w.write_all(&53u16.to_le_bytes()).unwrap();
    w.write_all(&[0; 6]).unwrap();
    for (key, a) in &pairs {
        let (os, ss) = orbit_data[key];
        w.write_all(&key.row.0).unwrap();
        w.write_all(&[key.pivot]).unwrap();
        w.write_all(&a.weight.to_le_bytes()).unwrap();
        w.write_all(&a.uses.to_le_bytes()).unwrap();
        w.write_all(&(os as u16).to_le_bytes()).unwrap();
        w.write_all(&(ss as u16).to_le_bytes()).unwrap();
    }
    w.flush().unwrap();
    assert_eq!(std::fs::metadata(&ledger).unwrap().len(), 48 + 53 * pairs.len() as u64);

    let raw_children = 12 * outgoing as usize;
    let compression = raw_children as f64 / generated_children as f64;
    let pair_compression = outgoing as f64 / pair_orbit_nonzero as f64;
    let full_orbit_estimate = (6_229_700f64 / coarse_keys as f64 * pair_orbit_nonzero as f64).ceil() as u64;
    let full_children_estimate = 12 * full_orbit_estimate;
    let result = format!(
        concat!(
            "{{\n",
            "  \"status\": \"PASS_EXACT_DECORATED_PAIR_ORBIT_PREFIX\",\n",
            "  \"scope\": \"bounded H-slice-0 prefix; full counts are estimates only\",\n",
            "  \"parents\": {},\n",
            "  \"outgoing_labelled_parent_pivot_uses\": {},\n",
            "  \"exact_nonzero_decorated_pairs_before_H\": {},\n",
            "  \"decorated_pair_H_orbits_nonzero\": {},\n",
            "  \"coarse_profile_keys\": {},\n",
            "  \"coarse_keys_with_multiple_decorated_H_orbits\": {},\n",
            "  \"coarse_max_decorated_H_orbits\": {},\n",
            "  \"coarse_to_pair_orbit_incidences\": {},\n",
            "  \"raw_K2_children\": {},\n",
            "  \"orbit_generated_K2_children\": {},\n",
            "  \"literal_K2_support_before_child_H\": {},\n",
            "  \"canonical_K2_support\": {},\n",
            "  \"reference_mismatches\": {},\n",
            "  \"reference_pivotability_mismatches\": {},\n",
            "  \"pair_use_compression\": {:.9},\n",
            "  \"child_generation_compression\": {:.9},\n",
            "  \"orbit_size_histogram\": \"{:?}\",\n",
            "  \"stabilizer_size_histogram\": \"{:?}\",\n",
            "  \"signature_stabilizer_candidate_action_histogram\": \"{:?}\",\n",
            "  \"full_6229700_coarse_profile_scaled_orbit_estimate\": {},\n",
            "  \"full_scaled_generated_children_estimate\": {},\n",
            "  \"timing_seconds\": {{\"input_exact_pair_aggregation\": {:.6}, \"H_orbit_collection\": {:.6}, \"stabilizer_audit\": {:.6}, \"coarse_profile_guard\": {:.6}, \"K2_generation\": {:.6}, \"reference_compare\": {:.6}}},\n",
            "  \"elapsed_seconds\": {:.6}\n",
            "}}\n"
        ),
        PARENTS,
        outgoing,
        exact_nonzero,
        pair_orbit_nonzero,
        coarse_keys,
        coarse_ambiguous,
        coarse_max_pair_orbits,
        coarse_pair_orbit_incidences,
        raw_children,
        generated_children,
        literal_child_support,
        children.len(),
        mismatches,
        pivotability_mismatches,
        pair_compression,
        compression,
        orbit_hist,
        stab_hist,
        sig_stab_action_hist,
        full_orbit_estimate,
        full_children_estimate,
        input_done,
        orbit_collect_done - input_done,
        stabilizer_done - orbit_collect_done,
        quotient_guard_done - stabilizer_done,
        child_done - quotient_guard_done,
        reference_done - child_done,
        begun.elapsed().as_secs_f64(),
    );
    std::fs::write(format!("{}results_hidden_k16_pair_orbits.json", NEW_ODIR), &result).unwrap();
    print!("{}", result);
}
