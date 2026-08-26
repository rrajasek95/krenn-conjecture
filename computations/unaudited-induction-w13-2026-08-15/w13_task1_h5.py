#!/usr/bin/env python3
"""UNAUDITED PROBE W13 -- Task 1: the law and the taxonomy at h = 5 (N = 12).

Checks that Theorem W13.2 and the taxonomy are genuinely h-uniform:
  dim L_5(A) = 441 + 225 + 100 + 36 = 802 of C(13,5) = 1287  (codim 485);
  E_w in L_5(A) exactly, on an explicit N = 12 source;
  the degree-5 taxonomy: only the monochrome s^a kappa_c^{5-a} (a <= 3)
  survive for generic A_pq.
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w13_core import (COLORS, NCAP, graded_error, graded_to_poly, in_span_exact,
                      kidx, monomials, random_source, require, rref_exact,
                      sigma_basis)
from w13_task1_law import L_generators, poly_to_row, rank_mod_p_np, P1, P2
from w13_task1_taxonomy import det3, flat, l_monomials, mono_name, mono_poly

OUT = {}


def main():
    rng = random.Random(50505)
    h = 5
    ambient = len(monomials(NCAP, h))
    expected = sum((((k + 2) * (k + 1)) // 2) ** 2 for k in range(2, h + 1))
    print(f"== h = 5 (N = 12): ambient dim S^5 = {ambient}, "
          f"predicted dim L_5 = {expected} ==")

    A = [[rng.randint(-6, 6) for _ in range(3)] for _ in range(3)]
    while det3(A) == 0 or any(A[i][j] == 0 for i in range(3)
                              for j in range(3)):
        A = [[rng.randint(-6, 6) for _ in range(3)] for _ in range(3)]
    t0 = time.time()
    rows, _ = L_generators(h, flat(A))
    r1 = rank_mod_p_np(rows, P1)
    r2 = rank_mod_p_np(rows, P2)
    require(r1 == r2 == expected == len(rows), (r1, r2, expected, len(rows)))
    print(f"  dim L_5(A) = {r1} (direct sum of Sigma_5..Sigma_2), "
          f"codim {ambient - r1}   [{time.time() - t0:.0f}s]")
    OUT["dim_L5"] = r1
    OUT["ambient"] = ambient
    OUT["codim"] = ambient - r1

    # E_w in L_5 on a real N = 12 source (graded form; verified exactly)
    src = random_source(h, rng, lo=-3, hi=3)
    Af = [0] * NCAP
    for i in COLORS:
        for j in COLORS:
            Af[kidx(i, j)] = src[(0, 1)][i][j]
    rows2, _ = L_generators(h, Af)
    t0 = time.time()
    basis, pivots = rref_exact(rows2)
    print(f"  exact RREF of L_5(A_pq): dim {len(pivots)} "
          f"[{time.time() - t0:.0f}s]")
    words = [tuple(rng.randrange(3) for _ in range(2 * h)) for _ in range(3)]
    words.append(tuple([0] * (2 * h)))
    for w in words:
        t0 = time.time()
        z = graded_error(src, h, w)
        poly = graded_to_poly(src, h, z)
        ok = in_span_exact(basis, pivots, poly_to_row(poly, h))
        require(ok, ("E_w not in L_5", w))
        print(f"    word {''.join(map(str, w))}: E_w in L_5(A_pq) "
              f"EXACTLY over Q  [{time.time() - t0:.0f}s]")
    OUT["words_checked"] = [list(w) for w in words]

    # taxonomy at h = 5, generic A
    monos = l_monomials(h)
    members, excluded = [], []
    for a, b in monos:
        vec = [Fraction(x) for x in poly_to_row(mono_poly(a, b, flat(A)), h)]
        rows3, _ = L_generators(h, flat(A))
        break
    basisA, pivotsA = rref_exact(rows)
    for a, b in monos:
        vec = [Fraction(x) for x in poly_to_row(mono_poly(a, b, flat(A)), h)]
        for r, col in enumerate(pivotsA):
            if vec[col]:
                f = vec[col]
                vec = [x - f * y for x, y in zip(vec, basisA[r])]
        (members if all(x == 0 for x in vec) else excluded).append(
            mono_name(a, b))
    print(f"  degree-5 taxonomy at a generic A_pq: {len(monos)} L-monomials, "
          f"{len(members)} can block, {len(excluded)} excluded")
    print(f"    IN : {', '.join(members)}")
    OUT["taxonomy_generic"] = {"in": members, "excluded": excluded,
                               "n_monomials": len(monos)}
    predicted = sorted(mono_name(a, (b0, b1, b2))
                       for a in range(0, h - 1)
                       for c in range(3)
                       for b0, b1, b2 in [tuple((h - a) if t == c else 0
                                                for t in range(3))])
    require(sorted(members) == predicted, (sorted(members), predicted))
    print(f"    == exactly the {len(predicted)} monochrome monomials "
          f"s^a kappa_c^(5-a), a <= 3: PASS")
    with open(__file__.rsplit("/", 1)[0] + "/results_h5.json", "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print("wrote results_h5.json")


if __name__ == "__main__":
    main()
