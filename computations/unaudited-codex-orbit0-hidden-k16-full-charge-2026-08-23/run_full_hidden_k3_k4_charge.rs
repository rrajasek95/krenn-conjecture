//! Full immediate cycle-charge repair for hidden paths [2,3] and [2,4].
#![allow(dead_code, unused_imports)]
include!(
    "../unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/run_hidden_children_prefix.rs"
);

const MERGED_PROFILES: &str = "computations/unaudited-codex-orbit0-k14-hidden-k16-parent-full-2026-08-23/hidden_k16_second_pivot_profiles_full.bin";
const PREFIX_LEDGER: &str = "computations/unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/hidden_child_profiles_prefix.bin";
const FOUT: &str = "computations/unaudited-codex-orbit0-hidden-k16-full-charge-2026-08-23/results_full_hidden_k3_k4_charge.json";

fn abstract_response(key: PKey, degree: usize, e: &Engine, c: &CEnv) -> Resp {
    let tails: &[[u8; 4]] = match degree {
        3 => &e.all_k3[key.pivot as usize],
        4 => &c.k4[key.pivot as usize],
        _ => unreachable!(),
    };
    let mut z = Resp::default();
    for t in tails {
        let ck = abstract_ckey(&key.profile, key.pivot as usize, t, e, c);
        let q = *c.dual.get(&ck).unwrap_or(&0);
        z.full_n += 1;
        z.full_q += q;
        let child = child_sig(key.sig, key.pivot as usize, t, e);
        if !pivotable_sig(child, e) {
            z.irr_n += 1;
            z.irr_q += q;
        }
    }
    z
}

fn replay_prefix(e: &Engine, c: &CEnv) -> (u64, u64, [i128; 4]) {
    let mut r = BufReader::with_capacity(1 << 20, File::open(PREFIX_LEDGER).unwrap());
    let mut h = [0u8; 64];
    r.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8], b"HCPROF1\0");
    assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()), U);
    let n = u64::from_le_bytes(h[32..40].try_into().unwrap());
    assert_eq!(
        (n, u16::from_le_bytes(h[40..42].try_into().unwrap())),
        (62_678, 90)
    );
    let mut checks = 0u64;
    let mut uses = 0u64;
    let mut q = [0i128; 4];
    for _ in 0..n {
        let mut rec = [0u8; 90];
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
        let multiplicity = u64::from_le_bytes(rec[58..66].try_into().unwrap());
        let mut row = [0; 24];
        row.copy_from_slice(&rec[66..90]);
        let row = Row(row);
        assert_eq!(path_profile(&row, key.pivot as usize, e, c), key.profile);
        uses += multiplicity;
        for degree in [3usize, 4] {
            // response() asserts every abstract cycle partition against the
            // literal child row.  Also compare the independent abstract-only
            // implementation used below.
            let literal = response(&row, key, degree, e, c);
            let abstract_only = abstract_response(key, degree, e, c);
            assert_eq!(
                (literal.full_n, literal.irr_n, literal.full_q, literal.irr_q),
                (
                    abstract_only.full_n,
                    abstract_only.irr_n,
                    abstract_only.full_q,
                    abstract_only.irr_q
                )
            );
            checks += literal.full_n;
            let base = if degree == 3 { 0 } else { 2 };
            q[base] += weight * literal.full_q as i128;
            q[base + 1] += weight * literal.irr_q as i128;
        }
    }
    assert_eq!(uses, 1_054_592);
    assert_eq!(checks, 5_766_376);
    assert_eq!(
        q,
        [
            -4_310_060_400_861_511_680,
            -3_762_784_545_831_124_992,
            460_536_785_434_312_704,
            440_759_609_843_318_784
        ]
    );
    (n, checks, q)
}

#[cfg(feature = "full_hidden_charge")]
fn main() {
    std::fs::create_dir_all(std::path::Path::new(FOUT).parent().unwrap()).unwrap();
    let begun = Instant::now();
    let e = parse();
    let c = cenv();
    let guard_start = Instant::now();
    let (guard_keys, guard_checks, guard_charge) = replay_prefix(&e, &c);
    let guard_seconds = guard_start.elapsed().as_secs_f64();
    let mut r = BufReader::with_capacity(1 << 20, File::open(MERGED_PROFILES).unwrap());
    let mut h = [0u8; 32];
    r.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8], b"H16MER2\0");
    assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()), U);
    let n = u64::from_le_bytes(h[24..32].try_into().unwrap());
    assert_eq!(n, 6_229_700);
    let full_start = Instant::now();
    let mut q = [0i128; 4];
    let mut tail_terms = [0u64; 4];
    let mut weight_sum = 0i128;
    let mut prior: Option<PKey> = None;
    for _ in 0..n {
        let mut rec = [0u8; 59];
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
        assert!(prior.map_or(true, |x| x < key));
        prior = Some(key);
        let weight = i128::from_le_bytes(rec[43..59].try_into().unwrap());
        assert_ne!(weight, 0);
        weight_sum += weight;
        for degree in [3usize, 4] {
            let z = abstract_response(key, degree, &e, &c);
            let base = if degree == 3 { 0 } else { 2 };
            q[base] += weight * z.full_q as i128;
            q[base + 1] += weight * z.irr_q as i128;
            tail_terms[base] += z.full_n;
            tail_terms[base + 1] += z.irr_n;
        }
    }
    let mut eof = [0u8; 1];
    assert_eq!(r.read(&mut eof).unwrap(), 0);
    assert_eq!(weight_sum, 146_230_609_431_055_564_800);
    let full_seconds = full_start.elapsed().as_secs_f64();
    let text = format!("{{\n  \"status\":\"PASS_FULL_HIDDEN_K3_K4_IMMEDIATE_CHARGE\",\n  \"scale\":{},\n  \"merged_profiles\":{},\n  \"merged_weight_sum_scaled\":\"{}\",\n  \"K19_path_23\":{{\"full_profile_tail_terms\":{},\"irreducible_profile_tail_terms\":{},\"full_charge_scaled\":\"{}\",\"irreducible_charge_scaled\":\"{}\"}},\n  \"K20_path_24\":{{\"full_profile_tail_terms\":{},\"irreducible_profile_tail_terms\":{},\"full_charge_scaled\":\"{}\",\"irreducible_charge_scaled\":\"{}\"}},\n  \"literal_guard\":{{\"keys\":{},\"tail_checks\":{},\"prefix_charges_scaled\":[\"{}\",\"{}\",\"{}\",\"{}\"]}},\n  \"timing_seconds\":{{\"literal_guard\":{:.6},\"full_abstract\":{:.6},\"total\":{:.6}}},\n  \"scope\":\"immediate 77-cycle charge only; no K2 collection or downstream reduction\"\n}}\n",U,n,weight_sum,tail_terms[0],tail_terms[1],q[0],q[1],tail_terms[2],tail_terms[3],q[2],q[3],guard_keys,guard_checks,guard_charge[0],guard_charge[1],guard_charge[2],guard_charge[3],guard_seconds,full_seconds,begun.elapsed().as_secs_f64());
    let tmp = format!("{}.tmp", FOUT);
    std::fs::write(&tmp, &text).unwrap();
    rename(tmp, FOUT).unwrap();
    print!("{}", text);
}
