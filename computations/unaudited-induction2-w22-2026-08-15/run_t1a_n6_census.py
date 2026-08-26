#!/usr/bin/env python3
"""W22 T1a -- the N = 6 (h = 2) blocking census by PURE STRATUM.

Question: is "every live pair blocked" compatible with mixed-exactness, and
does raising the number of SATISFIED PURE equations break it?

P_k = mixed-exact sources with exactly k nonzero pures.  At N = 6:
  P_0  constant-block family A_uv = t_uv J with haf(t) = 0        (W10)
  P_1  colour-0 on a perfect matching, colour-1 on a deficient one
  P_2  Delta_{6,2} padded to three colours
  P_3  EMPTY (six-site theorem + W10-G)

For every pair we decide, EXACTLY (Singular + Rabinowitsch):
  live            -- an admissible cap exists at all
  witness_rank1   -- an admissible rank-one cap with E_pq = 0 exists
  witness_general -- an admissible general cap with E_pq = 0 exists
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations

BASE = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-induction2-w22-2026-08-15"
sys.path.insert(0, BASE)
import w22_core as W                                       # noqa: E402
import w22_n6 as N6                                        # noqa: E402

N = 6
PAIRS = list(combinations(range(N), 2))
RES = {"sources": [], "controls": []}


def sites_of(p, q):
    return tuple(x for x in range(N) if x not in (p, q))


def census(src, label, do_general=True, verbose=True):
    ok_mixed = N6.is_mixed_exact(src, N)
    prof, pu = N6.pure_profile(src, N)
    rec = {"label": label, "mixed_exact": ok_mixed,
           "pure_profile": list(prof), "pures": [str(pu[c]) for c in range(3)],
           "pairs": []}
    for p, q in PAIRS:
        lv = N6.live(src, p, q)
        lvd = N6.live_diagonal(src, p, q)
        st = sites_of(p, q)
        entry = {"pair": [p, q], "live": lv, "live_diag": lvd}
        if lv:
            tag = f"{label.replace(' ', '_')}_{p}{q}"
            v1, d1 = N6.decide_pair_rank1(src, p, q, st, "R" + tag)
            entry["rank1"] = v1
            if do_general:
                vg, dg = N6.decide_pair_general(src, p, q, st, "G" + tag)
                entry["general"] = vg
                # SOUNDNESS: rank-one witness => general witness
                if v1 == "WITNESS" and vg == "BLOCKED":
                    entry["INCONSISTENT"] = True
        rec["pairs"].append(entry)
    lives = [e for e in rec["pairs"] if e["live"]]
    rec["n_live"] = len(lives)
    rec["n_blocked_general"] = sum(1 for e in lives
                                   if e.get("general") == "BLOCKED")
    rec["n_blocked_rank1"] = sum(1 for e in lives if e.get("rank1") == "BLOCKED")
    rec["all_live_blocked_general"] = (rec["n_blocked_general"] == len(lives))
    rec["all_live_blocked_rank1"] = (rec["n_blocked_rank1"] == len(lives))
    if verbose:
        print(f"  {label}: mixed_exact={ok_mixed} pures={prof} "
              f"live={rec['n_live']} blocked_gen={rec['n_blocked_general']} "
              f"blocked_r1={rec['n_blocked_rank1']} "
              f"ALL_BLOCKED={rec['all_live_blocked_general']}")
    return rec


def main():
    t0 = time.time()
    rng = random.Random(7717)

    # ---------------- P_0 : constant-block, haf(t) = 0 ----------------------
    print("== P_0 (constant-block, all pures 0) ==")
    made = 0
    tries = 0
    while made < 6 and tries < 400:
        tries += 1
        t = {e: rng.randint(-4, 4) for e in PAIRS}
        # force haf(t) = 0 by solving for one edge
        e0 = PAIRS[0]
        t[e0] = 0
        import w22_core as WW
        base = 0
        for M in WW.perfect_matchings(tuple(range(N))):
            term = 1
            for a, b in M:
                term *= t[WW.ekey(a, b)]
            base += term
        # coefficient of t[e0]
        t[e0] = 1
        one = 0
        for M in WW.perfect_matchings(tuple(range(N))):
            term = 1
            for a, b in M:
                term *= t[WW.ekey(a, b)]
            one += term
        coef = one - base
        if coef == 0:
            continue
        val = Fraction(-base, coef)
        t[e0] = val
        # clear denominators
        den = val.denominator
        t = {e: (v * den if e == e0 else v * den) for e, v in t.items()}
        t = {e: int(Fraction(v)) if Fraction(v).denominator == 1 else v
             for e, v in t.items()}
        if any(v == 0 for v in t.values()):
            continue
        src = N6.source_P0_constant(t, N)
        if not N6.is_mixed_exact(src, N):
            continue
        RES["sources"].append(census(src, f"P0_const_{made}"))
        made += 1

    # a diagonal-gauged constant-block source (rank-one blocks, not constant)
    t = {e: rng.randint(1, 4) for e in PAIRS}
    # fix haf = 0 as above on edge (0,1)
    import w22_core as WW

    def haf_t(tt):
        s = 0
        for M in WW.perfect_matchings(tuple(range(N))):
            term = 1
            for a, b in M:
                term *= tt[WW.ekey(a, b)]
            s += term
        return s
    t[(0, 1)] = 0
    b0 = haf_t(t)
    t[(0, 1)] = 1
    c0 = haf_t(t) - b0
    if c0 != 0:
        v = Fraction(-b0, c0)
        d = v.denominator
        t = {e: (int(v * d) if e == (0, 1) else int(val * d))
             for e, val in t.items()}
        src = N6.source_P0_constant(t, N)
        g = {u: [rng.randint(1, 3) for _ in range(3)] for u in range(N)}
        gs = N6.diag_gauge(src, g, N)
        RES["sources"].append(census(gs, "P0_gauged"))

    # ---------------- P_1 -------------------------------------------------
    print("== P_1 (one nonzero pure) ==")
    src = N6.source_P1(N)
    RES["sources"].append(census(src, "P1_matching_deficient"))

    # ---------------- P_2 -------------------------------------------------
    print("== P_2 (two nonzero pures: Delta_{6,2} padded) ==")
    src = N6.source_P2(N)
    RES["sources"].append(census(src, "P2_delta62"))
    # gauge + relabelled cycle variants
    for k, cyc in enumerate([[0, 2, 4, 1, 5, 3], [0, 1, 3, 5, 2, 4]]):
        s2 = N6.source_P2(N, cycle=cyc)
        RES["sources"].append(census(s2, f"P2_delta62_cycle{k}"))
    g = {u: [rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 3)]
         for u in range(N)}
    RES["sources"].append(census(N6.diag_gauge(N6.source_P2(N), g, N),
                                 "P2_delta62_gauged"))

    # ---------------- CONTROL: a generic (non-mixed-exact) source ----------
    print("== CONTROL: generic source (NOT mixed-exact) ==")
    src = {e: [[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]
           for e in PAIRS}
    RES["controls"].append(census(src, "CTRL_generic", do_general=True))

    RES["elapsed_s"] = round(time.time() - t0, 1)
    with open(f"{BASE}/results_t1a_n6_census.json", "w") as fh:
        json.dump(RES, fh, indent=1)
    print("\nelapsed", RES["elapsed_s"])


if __name__ == "__main__":
    main()
