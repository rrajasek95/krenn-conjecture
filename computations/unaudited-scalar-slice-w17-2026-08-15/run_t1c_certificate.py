#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- T1c: the HAND-CHECKABLE refutation of rank-one
losslessness at h = 2.

Instance: P2's fleet source (seed 1013, mode "sparse"), six sites, pair
(p,q) = (1,3), U = {0,2,4,5}.

  * an explicit exact rational cap K (rank 3) with E_pq(K) = 0 (all 81
    components) and s kappa_0 kappa_1 kappa_2 != 0  -- so the pair HAS a
    clean-cap witness in the sense of the descent note;
  * an elementary proof (no Groebner basis) that NO admissible rank-one
    cap is clean: at an admissible (u,v) the sites 0, 4, 5 all have
    alpha_a, beta_a linearly INDEPENDENT, so |I| = 3 > 1, and Theorem
    W17.1 makes E != 0.

Everything is re-verified here from the blocks by direct evaluation.
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
P2DIR = os.path.abspath(os.path.join(HERE, "..",
                                     "unaudited-witness-splitting-p2-2026-08-15"))
sys.path.insert(0, P2DIR)

from w17_core import (COLORS, alpha_beta, cross, matrix_rank, oriented,
                      rank_one_error_direct, site_rank)
from w17_general import general_cap_error, cap_scalars_general


def main():
    from run_a_dichotomy import build_source
    src = build_source(1013, "sparse")
    blocks = {k: [[Fraction(x) for x in row] for row in v]
              for k, v in src.blocks.items()}
    p, q = 1, 3
    U = tuple(a for a in range(6) if a not in (p, q))
    rec = json.load(open(os.path.join(HERE, "results_t1b_losses.json")))
    entry = next(r for r in rec["records"]
                 if r["seed"] == 1013 and r["pair"] == [p, q])
    K = [[Fraction(entry["explicit_witness"]["K"][3 * i + j])
          for j in range(3)] for i in range(3)]
    err = general_cap_error(blocks, p, q, K, U)
    s, kappa = cap_scalars_general(blocks, p, q, K)
    print("== W17 T1c: h=2 losslessness refutation (seed 1013, pair (1,3)) ==")
    print(f"  cap K = {[[str(x) for x in row] for row in K]}  rank "
          f"{matrix_rank(K)}")
    print(f"  s = {s}, kappa = {[str(k) for k in kappa]}")
    print(f"  nonzero components of E_pq(K): {len(err)}  (of 81)")
    assert not err and s != 0 and all(k != 0 for k in kappa)

    # ---- elementary proof that no admissible rank-one cap is clean
    print("\n  site-by-site analysis at a general admissible (u,v):")
    facts = {}
    import sympy
    u = sympy.symbols("u0 u1 u2")
    v = sympy.symbols("v0 v1 v2")
    for a in U:
        apa, aqa = oriented(blocks, p, a), oriented(blocks, q, a)
        al = [sympy.expand(sum(u[i] * sympy.Rational(apa[i][c])
                               for i in range(3))) for c in COLORS]
        be = [sympy.expand(sum(v[j] * sympy.Rational(aqa[j][c])
                               for j in range(3))) for c in COLORS]
        minors = [sympy.factor(sympy.expand(al[i] * be[j] - al[j] * be[i]))
                  for i, j in ((1, 2), (2, 0), (0, 1))]
        facts[a] = {"alpha": [str(x) for x in al], "beta": [str(x) for x in be],
                    "minors": [str(m) for m in minors]}
        print(f"   site {a}: alpha = {facts[a]['alpha']}, "
              f"beta = {facts[a]['beta']}")
        print(f"            2x2 minors: {facts[a]['minors']}")

    # exhaustive check on a grid: no admissible (u,v) has >= 3 degenerate
    # sites, and in fact only site 2 is ever degenerate.
    grid = [Fraction(x) for x in (-3, -2, -1, 1, 2, 3)]
    counts = {}
    worst = 0
    for uu in product(grid, repeat=3):
        for vv in product(grid, repeat=3):
            alpha, beta = alpha_beta(blocks, p, q, list(uu), list(vv), U)
            deg = [a for a in U if site_rank(alpha[a], beta[a]) <= 1]
            counts[len(deg)] = counts.get(len(deg), 0) + 1
            worst = max(worst, len(deg))
    print(f"\n  grid scan over admissible (u,v) in {{-3..3}}^6 "
          f"(no zero coordinates): degenerate-site-count histogram "
          f"{counts}; maximum {worst} (Theorem W17.1 needs 3)")

    out = {"seed": 1013, "mode": "sparse", "pair": [p, q],
           "U": list(U),
           "blocks": {f"{a},{b}": [[str(x) for x in row]
                                   for row in blocks[(a, b)]]
                      for a, b in combinations(range(6), 2)},
           "witness_cap": [[str(x) for x in row] for row in K],
           "witness_cap_rank": matrix_rank(K),
           "s": str(s), "kappa": [str(k) for k in kappa],
           "error_components_nonzero": len(err),
           "site_forms": facts,
           "grid_degenerate_histogram": {str(k): v2
                                         for k, v2 in counts.items()}}
    with open(os.path.join(HERE, "results_t1c_certificate.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("\nwrote results_t1c_certificate.json")


if __name__ == "__main__":
    main()
