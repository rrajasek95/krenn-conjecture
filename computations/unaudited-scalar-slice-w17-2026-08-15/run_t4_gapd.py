#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- T4 (Gap D: pair existence) and the complex-only
|I| = 1 branch of Theorem W17.1.

Gap D asks what nondegeneracy is guaranteed at SOME pair of a minimal exact
source.  Two separate questions:

  D-rank-one (what the re-based descent actually needs): a pair with
    A_pq != 0.  Exactness gives this on a whole perfect matching per colour
    (haf of the colour-c diagonal weighting is the pure coefficient 1 != 0,
    so some perfect matching has all its colour-c diagonal entries nonzero).
    Admissibility of a rank-one cap is then a nonempty Zariski-open
    condition, so NO full-rank or nonzero-diagonal pair is needed.

  D-old (what W14's monochrome-transfer chain needed): a pair with A_pq of
    FULL RANK and nonzero diagonal.  Measured here on the committed
    near-exact eight-site sources.

Also: the |I| = 1 branch of Theorem W17.1 (three degenerate sites with
e_1 = e_2 = 0 on their ratios) has NO real solutions with the fourth site
nondegenerate -- it needs a primitive cube root of unity.  An explicit
exact instance over Q(omega) is built and verified here.
"""

from __future__ import annotations

import importlib.util
import json
import os
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

from w17_core import COLORS, matrix_rank, oriented, perfect_matchings


def pair_stats(source, n=8):
    live = [(a, b) for a, b in combinations(range(n), 2)
            if any(source[(a, b)][i][j] != 0 for i in range(3)
                   for j in range(3))]
    ranks = Counter(matrix_rank(source[(a, b)])
                    for a, b in combinations(range(n), 2))
    full = [(a, b) for a, b in combinations(range(n), 2)
            if matrix_rank(source[(a, b)]) == 3]
    diag3 = [(a, b) for a, b in combinations(range(n), 2)
             if all(source[(a, b)][c][c] != 0 for c in COLORS)]
    colour_graphs = {}
    for c in COLORS:
        edges = [(a, b) for a, b in combinations(range(n), 2)
                 if source[(a, b)][c][c] != 0]
        has_pm = any(all(tuple(sorted(e)) in set(edges) for e in M)
                     for M in perfect_matchings(tuple(range(n))))
        colour_graphs[c] = {"edges": len(edges), "has_perfect_matching": has_pm}
    return {"live_pairs": len(live), "rank_histogram": dict(ranks),
            "full_rank_pairs": full, "all_three_diagonal_pairs": diag3,
            "colour_diagonal_graphs": colour_graphs}


def omega_instance():
    """An exact Q(omega) instance of the |I| = 1 branch of Theorem W17.1:
    three sites degenerate with ratios (1, omega, omega^2) (so e_1 = e_2 = 0)
    and the fourth site NONdegenerate; the cap error vanishes identically."""
    import sympy
    w = sympy.Rational(-1, 2) + sympy.sqrt(3) * sympy.I / 2       # omega
    ratios = [sympy.Integer(1), w, w ** 2]
    e1 = sympy.simplify(sum(ratios))
    e2 = sympy.simplify(ratios[0] * ratios[1] + ratios[0] * ratios[2]
                        + ratios[1] * ratios[2])
    # alpha_a, beta_a chosen directly (any source realises them)
    alpha = {0: [sympy.Integer(1), 0, 0], 1: [0, sympy.Integer(1), 0],
             2: [0, 0, sympy.Integer(1)], 3: [sympy.Integer(1), 0, 0]}
    beta = {a: [sympy.simplify(x / ratios[a]) for x in alpha[a]]
            for a in (0, 1, 2)}
    beta[3] = [0, sympy.Integer(1), 0]         # site 3: independent of alpha
    total = {}
    for word in [(i, j, k, l) for i in range(3) for j in range(3)
                 for k in range(3) for l in range(3)]:
        val = sympy.Integer(0)
        for A in combinations(range(4), 2):
            term = sympy.Integer(1)
            for t in range(4):
                term *= (alpha[t][word[t]] if t in A else beta[t][word[t]])
            val += term
        val = sympy.simplify(2 * val)
        if val != 0:
            total[word] = str(val)
    return {"e1": str(e1), "e2": str(e2),
            "nonzero_error_components": len(total),
            "sample": dict(list(total.items())[:5])}


def main():
    t0 = time.time()
    print("== W17 T4: Gap D on the committed near-exact sources ==")
    out = {}
    for label, second in (("STAGE_A", False), ("STAGE_A_SECOND", True)):
        src = P1S.load_stage_a(second=second)
        st = pair_stats(src)
        out[label] = st
        print(f"  {label}: live pairs {st['live_pairs']}/28, block-rank "
              f"histogram {st['rank_histogram']}")
        print(f"    FULL-RANK pairs: {st['full_rank_pairs']}")
        print(f"    pairs with all three diagonal entries nonzero: "
              f"{st['all_three_diagonal_pairs']}")
        print(f"    colour diagonal graphs: {st['colour_diagonal_graphs']}")
    print("\n  |I| = 1 branch over Q(omega):")
    om = omega_instance()
    print(f"    e_1 = {om['e1']}, e_2 = {om['e2']}, nonzero error components "
          f"{om['nonzero_error_components']} (0 means the cap is CLEAN with "
          f"three degenerate sites and one nondegenerate site)")
    out["omega_branch"] = om
    with open(os.path.join(HERE, "results_t4_gapd.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print(f"\nwrote results_t4_gapd.json [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
