//! Missing K18 [2,2] immediate charge from the merged hidden-parent profiles.
#![allow(dead_code, unused_imports)]
include!(
    "../unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/run_hidden_children_prefix.rs"
);

const MERGED: &str = "computations/unaudited-codex-orbit0-k14-hidden-k16-parent-full-2026-08-23/hidden_k16_second_pivot_profiles_full.bin";
const PLEDGER: &str = "computations/unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/hidden_child_profiles_prefix.bin";
const KCHECK: &str = "computations/unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/k18_k2_canonical_prefix.bin";
const ROUT: &str = "computations/unaudited-codex-orbit0-hidden-k16-k18-complete-charge-2026-08-23/results_missing_k18_22_charge.json";

fn response2_abstract(key: PKey, e: &Engine, c: &CEnv) -> Resp {
    let mut z = Resp::default();
    for t in &e.all_k2[key.pivot as usize] {
        let ck = abstract_ckey(&key.profile, key.pivot as usize, t, e, c);
        let q = *c.dual.get(&ck).unwrap_or(&0);
        z.full_n += 1;
        z.full_q += q;
        if !pivotable_sig(child_sig(key.sig, key.pivot as usize, t, e), e) {
            z.irr_n += 1;
            z.irr_q += q;
        }
    }
    z
}

fn prefix_profile_guard(e: &Engine, c: &CEnv) -> (i128, i128, u64) {
    let mut r = BufReader::new(File::open(PLEDGER).unwrap());
    let mut h = [0; 64];
    r.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8], b"HCPROF1\0");
    assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()), U);
    let n = u64::from_le_bytes(h[32..40].try_into().unwrap());
    assert_eq!(
        (n, u16::from_le_bytes(h[40..42].try_into().unwrap())),
        (62_678, 90)
    );
    let (mut fq, mut iq, mut checks) = (0i128, 0i128, 0u64);
    for _ in 0..n {
        let mut rec = [0; 90];
        r.read_exact(&mut rec).unwrap();
        let mut profile = [0; 29];
        profile.copy_from_slice(&rec[..29]);
        let mut sig = [0; 12];
        sig.copy_from_slice(&rec[29..41]);
        let key = PKey {
            profile,
            sig,
            pivot: rec[41],
        };
        let weight = i128::from_le_bytes(rec[42..58].try_into().unwrap());
        let mut rr = [0; 24];
        rr.copy_from_slice(&rec[66..90]);
        let row = Row(rr);
        assert_eq!(path_profile(&row, key.pivot as usize, e, c), key.profile);
        let az = response2_abstract(key, e, c);
        let mut lz = Resp::default();
        for t in &e.all_k2[key.pivot as usize] {
            let child = replace_anchor(&row, &e.anchors[key.pivot as usize], t);
            let ak = abstract_ckey(&key.profile, key.pivot as usize, t, e, c);
            let lk = literal_ckey(&child, c);
            assert_eq!(ak, lk);
            let q = *c.dual.get(&lk).unwrap_or(&0);
            lz.full_n += 1;
            lz.full_q += q;
            if !pivotable(&child, e) {
                lz.irr_n += 1;
                lz.irr_q += q
            }
            checks += 1
        }
        assert_eq!(
            (az.full_n, az.irr_n, az.full_q, az.irr_q),
            (lz.full_n, lz.irr_n, lz.full_q, lz.irr_q)
        );
        fq += weight * lz.full_q as i128;
        iq += weight * lz.irr_q as i128
    }
    assert_eq!(checks, 62_678 * 12);
    (fq, iq, checks)
}

fn canonical_checkpoint_guard(e: &Engine, c: &CEnv, expected: (i128, i128)) -> (u64, u64) {
    let mut r = BufReader::new(File::open(KCHECK).unwrap());
    let mut h = [0; 64];
    r.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8], b"H18K2P1\0");
    assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()), U);
    let n = u64::from_le_bytes(h[48..56].try_into().unwrap());
    assert_eq!(
        (n, u16::from_le_bytes(h[56..58].try_into().unwrap())),
        (694_172, 76)
    );
    let (mut fq, mut iq, mut pivotable_n) = (0i128, 0i128, 0u64);
    let mut prior = None;
    for _ in 0..n {
        let mut rec = [0; 76];
        r.read_exact(&mut rec).unwrap();
        let mut rr = [0; 24];
        rr.copy_from_slice(&rec[..24]);
        let row = Row(rr);
        assert!(prior.map_or(true, |x: Row| x < row));
        prior = Some(row);
        let w = i128::from_le_bytes(rec[24..40].try_into().unwrap());
        assert_ne!(w, 0);
        let stored = rec[40] != 0;
        assert_eq!(pivotable(&row, e), stored);
        if stored {
            pivotable_n += 1
        }
        let mut raw = [0; 24];
        raw.copy_from_slice(&rec[52..76]);
        let raw = Row(raw);
        assert_eq!(literal_ckey(&raw, c), literal_ckey(&row, c));
        let q = *c.dual.get(&literal_ckey(&row, c)).unwrap_or(&0) as i128;
        fq += w * q;
        if !stored {
            iq += w * q
        }
    }
    assert_eq!((fq, iq), expected);
    (n, pivotable_n)
}

#[cfg(feature = "full_hidden_charge")]
fn main() {
    std::fs::create_dir_all(std::path::Path::new(ROUT).parent().unwrap()).unwrap();
    let begun = Instant::now();
    let e = parse();
    let c = cenv();
    let guard_start = Instant::now();
    let (pf, pi, checks) = prefix_profile_guard(&e, &c);
    let (crows, cpiv) = canonical_checkpoint_guard(&e, &c, (pf, pi));
    let guard_seconds = guard_start.elapsed().as_secs_f64();
    let mut r = BufReader::with_capacity(1 << 20, File::open(MERGED).unwrap());
    let mut h = [0; 32];
    r.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8], b"H16MER2\0");
    assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()), U);
    let n = u64::from_le_bytes(h[24..32].try_into().unwrap());
    assert_eq!(n, 6_229_700);
    let full_start = Instant::now();
    let (mut fq, mut iq, mut fnn, mut inn, mut wsum) = (0i128, 0i128, 0u64, 0u64, 0i128);
    let mut prior = None;
    for _ in 0..n {
        let mut rec = [0; 59];
        r.read_exact(&mut rec).unwrap();
        let mut profile = [0; 29];
        profile.copy_from_slice(&rec[..29]);
        let mut sig = [0; 12];
        sig.copy_from_slice(&rec[29..41]);
        let key = PKey {
            profile,
            sig,
            pivot: rec[41],
        };
        assert_eq!(rec[42], 0);
        assert!(prior.map_or(true, |x: PKey| x < key));
        prior = Some(key);
        let w = i128::from_le_bytes(rec[43..59].try_into().unwrap());
        assert_ne!(w, 0);
        wsum += w;
        let z = response2_abstract(key, &e, &c);
        fnn += z.full_n;
        inn += z.irr_n;
        fq += w * z.full_q as i128;
        iq += w * z.irr_q as i128
    }
    let mut eof = [0];
    assert_eq!(r.read(&mut eof).unwrap(), 0);
    assert_eq!(wsum, 146_230_609_431_055_564_800);
    let full_seconds = full_start.elapsed().as_secs_f64();
    let text=format!("{{\n  \"status\":\"PASS_FULL_MISSING_K18_22_IMMEDIATE_CHARGE\",\n  \"scale\":{},\n  \"merged_profiles\":{},\n  \"merged_weight_sum_scaled\":\"{}\",\n  \"full_profile_tail_terms\":{},\n  \"irreducible_profile_tail_terms\":{},\n  \"full_charge_scaled\":\"{}\",\n  \"irreducible_charge_scaled\":\"{}\",\n  \"linearity_theorem\":\"cycle charge and next-pivot predicate are functions of (profile,signature,pivot,K2 tail), so signed duplicate collection commutes with full/irreducible summation\",\n  \"literal_prefix_guard\":{{\"tail_checks\":{},\"full_charge_scaled\":\"{}\",\"irreducible_charge_scaled\":\"{}\",\"canonical_rows\":{},\"canonical_pivotable_rows\":{}}},\n  \"timing_seconds\":{{\"prefix_guards\":{:.6},\"full_abstract\":{:.6},\"total\":{:.6}}},\n  \"scope\":\"missing K18 [2,2] immediate charge only; no row storage or later tails\"\n}}\n",U,n,wsum,fnn,inn,fq,iq,checks,pf,pi,crows,cpiv,guard_seconds,full_seconds,begun.elapsed().as_secs_f64());
    let tmp = format!("{}.tmp", ROUT);
    std::fs::write(&tmp, &text).unwrap();
    rename(tmp, ROUT).unwrap();
    print!("{}", text)
}
