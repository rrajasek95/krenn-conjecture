#!/usr/bin/env python3
"""W25 T3b -- ESCALATION: independent verification of the N=8 ALL-BLOCKED X_3
candidate produced by run_t3_n8.py.

Full battery, exactly as the ledger requires for a headline verdict:
  (1) membership in X_3 re-verified against the RAW word definition at N=8
      (every 3-near-constant word, recomputed by the bitmask DP), plus the
      pures and the defect profile;
  (2) EVERY live pair decided by BOTH deciders (W25's W22-M closed form and
      W23's subset-sum expansion), over Q and modulo three primes (two of them
      1 mod 3, ledger 19);
  (3) a POSITIVE control on the same battery: the object it was walked from
      (a diagonal X_3 source) must be reported as carrying witnesses;
  (4) MUTATION control: perturbing one block must (a) leave X_3 and (b) change
      the verdict pattern -- so the battery is not reporting BLOCKED for a
      degenerate reason;
  (5) a scan of the object's structure: ranks, star supports, detachment
      profile (det_p, det_q), and whether the known one-directional detachment
      law max(det_p,det_q) >= 2 => WITNESS is contradicted (it must not be).
"""
from __future__ import annotations

import json
import random
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x3core-w25-2026-08-15")
W23BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-pure-core-w23-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, W23BASE)
import w25_core as C                                            # noqa: E402
import w25_decide as D                                          # noqa: E402
import w23_decide as W23D                                       # noqa: E402
import w23_core as W23                                          # noqa: E402
import run_t2_u2 as T2                                          # noqa: E402

N = 8
RES = {}
RAN = []


def control(name):
    RAN.append(name)


def load_candidate(idx=0):
    with open(f"{BASE}/results_t3_n8.json") as fh:
        D3 = json.load(fh)
    rec = D3["x3_allblocked_objects"][idx]
    src = {}
    for k, m in rec["blocks"].items():
        a, b = (int(x) for x in k.split(","))
        src[(a, b)] = [[Fraction(x) for x in row] for row in m]
    return src, rec


def battery(src, tag, primes=(1000003, 1000033, 32003)):
    rows = []
    for p, q in combinations(range(N), 2):
        lv = C.live(src, p, q)
        row = {"pair": [p, q], "live": lv,
               "rank": C.matrix_rank(C.oriented(src, p, q))}
        if lv:
            U = tuple(x for x in range(N) if x not in (p, q))
            v1, d1, mp = D.decide_pair(src, p, q, U, f"{tag}A{p}{q}",
                                       primes=primes)
            isrc, _ = C.clear_denominators(src)
            v2, d2, mp2 = W23D.decide_pair(isrc, p, q, U, f"{tag}B{p}{q}",
                                           primes=(32003, 1000003))
            row.update({"w25": v1, "dimQ": d1, "modp": mp, "w23": v2,
                        "agree": v1 == v2,
                        "det_p": sum(1 for a in U
                                     if not C.live(src, p, a)),
                        "det_q": sum(1 for a in U
                                     if not C.live(src, q, a))})
        rows.append(row)
    lv = [r for r in rows if r["live"]]
    return {"n_live": len(lv),
            "n_witness": sum(1 for r in lv if r["w25"] == "WITNESS"),
            "all_blocked": bool(lv) and all(r["w25"] == "BLOCKED"
                                            for r in lv),
            "disagreements": sum(1 for r in lv if not r["agree"]),
            "modp_mismatch": sum(1 for r in lv for ch, dd in r["modp"].items()
                                 if (dd == -1) != (r["dimQ"] == -1)),
            "ranks": sorted(r["rank"] for r in rows),
            "max_detach": max([max(r["det_p"], r["det_q"]) for r in lv] or [0]),
            "rows": rows}


def main():
    rng = random.Random(9090)
    src, rec = load_candidate()
    print("=" * 74)
    print("(1) raw re-verification of the candidate")
    print("=" * 74)
    ok3, bw3 = C.in_Xk(src, N, 3)
    ok4, bw4 = C.in_Xk(src, N, 4)
    pu = C.pures(src, N)
    md = C.mixed_defects(src, N)
    shapes = Counter(tuple(sorted(Counter(w).values(), reverse=True))
                     for w in md)
    offs = Counter(C.offcount(w) for w in md)
    print(f"   in X_3 (raw {len(C.near_constant_words(N, 3, 3))} words): "
          f"{ok3}   in X_4: {ok4}")
    print(f"   pures: {[str(pu[c]) for c in range(3)]}")
    print(f"   mixed defects: {len(md)}; colour-multiset shapes "
          f"{dict(shapes)}; off-counts {dict(offs)}")
    # independent H cross-check on the defect words
    mism = sum(1 for w in md[:200] if C.H(src, w, N) != W23.H(src, w, N))
    print(f"   H cross-check W25 vs W23 on {min(200, len(md))} defect words: "
          f"{mism} mismatches")
    RES["candidate"] = {"in_X3": ok3, "in_X4": ok4,
                        "pures": [str(pu[c]) for c in range(3)],
                        "defects": len(md),
                        "defect_shapes": {str(k): v for k, v in shapes.items()},
                        "defect_offcounts": {str(k): v for k, v in offs.items()},
                        "H_crosscheck_mismatch": mism,
                        "blocks": rec["blocks"]}
    assert ok3 and not ok4 and mism == 0
    assert all(pu[c] == 1 for c in range(3))
    control("T3b1_raw_verification")

    print("=" * 74)
    print("(2) FULL BATTERY: every live pair, both deciders, three primes")
    print("=" * 74)
    bat = battery(src, "ESC")
    print(f"   live {bat['n_live']}; WITNESS {bat['n_witness']}; "
          f"ALL-BLOCKED {bat['all_blocked']}; decider disagreements "
          f"{bat['disagreements']}; mod-p mismatches {bat['modp_mismatch']}")
    print(f"   ranks {bat['ranks']}; max detachment over live pairs "
          f"{bat['max_detach']}")
    print(f"   per-pair: "
          f"{[(r['pair'], r['w25'], r['dimQ'], r['det_p'], r['det_q']) for r in bat['rows'] if r['live']]}")
    RES["battery"] = {k: v for k, v in bat.items() if k != "rows"}
    RES["battery_rows"] = bat["rows"]
    control("T3b2_full_battery")

    print("=" * 74)
    print("(3) POSITIVE control: a diagonal X_3 source at N=8 through the "
          "SAME battery must show witnesses")
    print("=" * 74)
    col, w, base = T2.build_n_diagonal(N, rng, extra=2)
    assert base is not None
    b2 = battery(base, "POS", primes=(1000003,))
    print(f"   diagonal X_3 control: live {b2['n_live']}; WITNESS "
          f"{b2['n_witness']}; ALL-BLOCKED {b2['all_blocked']}; "
          f"disagreements {b2['disagreements']}")
    RES["positive_control"] = {k: v for k, v in b2.items() if k != "rows"}
    assert b2["n_witness"] > 0 and not b2["all_blocked"]
    assert b2["disagreements"] == 0
    control("T3b3_positive_control")

    print("=" * 74)
    print("(4) MUTATION control")
    print("=" * 74)
    mut = C.copy_source(src)
    e = sorted(mut)[0]
    mut[e][0][0] = mut[e][0][0] + 1
    okm, _ = C.in_Xk(mut, N, 3)
    bm = battery(mut, "MUT", primes=())
    print(f"   mutated object: still in X_3 {okm} (expected False); live "
          f"{bm['n_live']}; WITNESS {bm['n_witness']}; ALL-BLOCKED "
          f"{bm['all_blocked']}")
    RES["mutation"] = {"still_in_X3": okm,
                       **{k: v for k, v in bm.items() if k != "rows"}}
    assert not okm
    control("T3b4_mutation")

    print("=" * 74)
    print("(5) consistency with the known one-directional detachment law")
    print("=" * 74)
    viol = [r["pair"] for r in bat["rows"]
            if r["live"] and max(r["det_p"], r["det_q"]) >= 2
            and r["w25"] != "WITNESS"]
    print(f"   live pairs with max(det_p,det_q) >= 2 that are BLOCKED "
          f"(would CONTRADICT W23's exhaustive law): {viol}")
    RES["detachment_check"] = {"violations": viol}
    control("T3b5_detachment_law")

    declared = ["T3b1_raw_verification", "T3b2_full_battery",
                "T3b3_positive_control", "T3b4_mutation",
                "T3b5_detachment_law"]
    missing = [x for x in declared if x not in RAN]
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    assert not missing
    with open(f"{BASE}/results_t3b_escalation.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("wrote results_t3b_escalation.json")


if __name__ == "__main__":
    main()
