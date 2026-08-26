#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- T2(a): the h = 3 rank-one theory on the COMMITTED
near-exact eight-site source (STAGE_A, 6559/6561 GHZ rows correct; the two
defect words are the constants 0^8 and 1^8).

P1's ground truth: general-cap witnesses exist exactly at the pairs (0,2)
and (1,3) (explicit rank-3 caps, re-verified here), pair (2,3) undecided,
the other 25 pairs blocked.

Decided here for all 28 pairs, exactly:
  * the number of nonvanishing components of E_pq(u (x) v)  (out of 729);
  * whether an admissible rank-one (scalar-slice) witness exists;
  * an explicit exact rational witness (u,v) where one exists, verified by
    evaluating all 729 components and the four admissibility scalars;
  * the degeneracy profile of the witness (Theorem W17.4) and the internal
    block ranks, i.e. WHY those pairs and not the others.
"""

from __future__ import annotations

import importlib.util
import json
import os
import random
import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.abspath(os.path.join(HERE, ".."))
P1DIR = os.path.join(REPO, "unaudited-witness-splitting-p1-2026-08-15")
sys.path.insert(0, REPO)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


P1C = load_module("wsplit_core", os.path.join(P1DIR, "wsplit_core.py"))
P1S = load_module("wsplit_sources", os.path.join(P1DIR, "wsplit_sources.py"))

import w17_h3 as H3
from w17_core import (COLORS, alpha_beta, cap_scalars, matrix_rank, oriented,
                      rank_one_error_direct, run_singular, site_rank)


def internal_rank_profile(source, sites):
    return {f"{a},{b}": matrix_rank(oriented(source, a, b))
            for a, b in combinations(sites, 2)}


def search_rational_witness(source, p, q, sites, eqs, rng, tries=4000,
                            lo=-3, hi=3):
    """Exact search for an admissible rank-one witness with small integer
    entries; verified by the independent numeric evaluator."""
    for _ in range(tries):
        u = [Fraction(rng.randint(lo, hi)) for _ in range(3)]
        v = [Fraction(rng.randint(lo, hi)) for _ in range(3)]
        if any(x == 0 for x in u) or any(x == 0 for x in v):
            continue
        s, kappa = cap_scalars(source, p, q, u, v)
        if s == 0 or any(k == 0 for k in kappa):
            continue
        if any(H3.bp_eval(f, u, v) != 0 for f in eqs.values()):
            continue
        err = rank_one_error_direct(source, p, q, u, v, sites)
        if err:
            continue
        return {"u": [str(x) for x in u], "v": [str(x) for x in v],
                "s": str(s), "kappa": [str(k) for k in kappa]}
    return None


def analyse(source, label, p1verdicts=None, timeout=900):
    rows = []
    rng = random.Random(17)
    for p, q in combinations(range(8), 2):
        U = tuple(a for a in range(8) if a not in (p, q))
        t0 = time.time()
        eqs, s = H3.rank_one_equations_h3(source, p, q, U)
        tag = f"{label}_{p}{q}"
        live = bool(s)
        rk1 = None
        if live:
            out = run_singular(H3.rk1_query(list(eqs.values()), s, tag),
                               timeout=timeout)
            rk1 = H3.parse_rk1(out, tag)
        wit = None
        if rk1:
            wit = search_rational_witness(source, p, q, U, eqs, rng)
        row = {"pair": [p, q], "live": live, "nonzero_components": len(eqs),
               "rank_one_witness": rk1, "explicit": wit,
               "seconds": round(time.time() - t0, 1),
               "pair_block_rank": matrix_rank(oriented(source, p, q)),
               "star_p_ranks": [matrix_rank(oriented(source, p, a))
                                for a in U],
               "star_q_ranks": [matrix_rank(oriented(source, q, a))
                                for a in U],
               "internal_rank_hist": dict(Counter(
                   matrix_rank(oriented(source, a, b))
                   for a, b in combinations(U, 2)))}
        if wit:
            u = [Fraction(x) for x in wit["u"]]
            v = [Fraction(x) for x in wit["v"]]
            alpha, beta = alpha_beta(source, p, q, u, v, U)
            row["witness_site_ranks"] = {str(a): site_rank(alpha[a], beta[a])
                                         for a in U}
        if p1verdicts is not None:
            row["p1_verdict"] = p1verdicts.get(f"{p},{q}")
        rows.append(row)
        print(f"  {label} pair ({p},{q}): live {live}, comps "
              f"{len(eqs):3d}, rank-one {rk1}, explicit "
              f"{'yes' if wit else '-'} [{row['seconds']}s]")
    return rows


def main():
    t0 = time.time()
    print("== W17 T2(a): STAGE_A (committed near-exact eight-site source) ==")
    src = P1S.load_stage_a()
    cert = json.load(open(os.path.join(P1DIR, "witness_certificates.json")))
    # control: P1's committed rank-3 witness caps re-verified here
    from w17_general import general_cap_error
    control = {}
    for key in ("0,2", "1,3"):
        rec = cert[key]
        p, q = rec["pair"]
        U = tuple(a for a in range(8) if a not in (p, q))
        K = [[Fraction(rec["cap"][3 * i + j]) for j in range(3)]
             for i in range(3)]
        err = general_cap_error(src, p, q, K, U)
        control[key] = {"cap_rank": matrix_rank(K), "nonzero_components":
                        len(err)}
    print(f"  control (P1 caps re-verified): {control}")
    defects = P1S.ghz_defects(src)
    print(f"  GHZ defect count: {defects}")
    print(f"  internal/global block rank histogram: "
          f"{dict(Counter(matrix_rank(src[(a, b)]) for a, b in combinations(range(8), 2)))}")
    rows = analyse(src, "A", {"0,2": "witness", "1,3": "witness",
                              "2,3": "undecided"})
    n_rk1 = sum(1 for r in rows if r["rank_one_witness"])
    print(f"\n  rank-one witness pairs: {n_rk1}/28  -> "
          f"{[r['pair'] for r in rows if r['rank_one_witness']]}")
    print("\n== STAGE_A_SECOND ==")
    src2 = P1S.load_stage_a(second=True)
    print(f"  GHZ defect count: {P1S.ghz_defects(src2)}")
    rows2 = analyse(src2, "B")
    n2 = sum(1 for r in rows2 if r["rank_one_witness"])
    print(f"\n  rank-one witness pairs: {n2}/28 -> "
          f"{[r['pair'] for r in rows2 if r['rank_one_witness']]}")
    with open(os.path.join(HERE, "results_t2_stage_a.json"), "w") as fh:
        json.dump({"control": control, "defects": defects,
                   "stage_a": rows, "stage_a_second": rows2}, fh, indent=1,
                  default=str)
    print(f"\nwrote results_t2_stage_a.json [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
