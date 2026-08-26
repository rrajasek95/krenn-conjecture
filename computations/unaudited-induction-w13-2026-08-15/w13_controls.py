#!/usr/bin/env python3
"""UNAUDITED PROBE W13 -- consolidated mutation / falsification controls.

Every checker in this directory must REJECT a deliberately corrupted input.

  K1  wrong K_2,3 vertex set in the Theorem W13.6 checker  -> must fail
  K2  wrong colour for the orphan pairs                    -> must fail
  K3  deleting one of the six cross edges                   -> must fail
  K4  the odd-relation finder must return None when the difference lattice
      genuinely has no odd relation (a hand-built even example)
  K5  the odd-relation finder must FIND the K_2,3 relation on a hand-built
      2x3 permanent configuration
  L1  a corrupted graded error (one sign flipped in R) must LEAVE L_h(A)
  L2  the truncated law Sigma_h + s Sigma_{h-1} (dropping s^{h-2}Sigma_2)
      must be violated by a real source component
  L3  a random quartic must NOT lie in L_4(A) (the law is not vacuous)
  L4  the h = 3 span must reproduce P1's independently measured 136
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w13_core import (COLORS, NCAP, graded_error, graded_to_poly, in_span_exact,
                      iota, kidx, monomials, poly_mul, poly_pow, random_source,
                      rref_exact, sigma_basis, sites)
from w13_rcell import odd_relation
from w13_task1_law import L_generators, poly_to_row, rank_mod_p_np, P1
from w13_task2_k23 import check as k23_check
import w13_task2_k23 as K23

OUT = {}


def must_fail(fn, name):
    try:
        fn()
    except AssertionError:
        print(f"  {name}: correctly REJECTED")
        return True
    print(f"  {name}: NOT REJECTED  <-- control failure")
    return False


def main():
    rng = random.Random(99)
    ok = {}

    print("== Task 2 checker controls ==")
    orig = K23.predicted_k23

    def bad_vertices(kind, n):
        N, cs, v, u, partner, marks = orig(kind, n)
        # replace one v by a vertex of the OTHER part: the six edges are no
        # longer all colour 0 (F_6 has several genuine K_2,3's, so a mere
        # permutation inside X is not a mutation)
        return N, cs, (v[0], v[1], u[0] - 2), u, partner, marks
    K23.predicted_k23 = bad_vertices
    ok["K1"] = must_fail(lambda: k23_check("F", 6), "K1 wrong K_2,3 vertices")
    K23.predicted_k23 = orig

    def bad_colour(kind, n):
        N, cs, v, u, partner, marks = orig(kind, n)
        cs2 = [set(map(tuple, s)) for s in cs]
        # move every colour-2 intra-part edge into colour 0: orphan pairs
        # can no longer be completed
        moved = {e for e in cs2[2] if (e[0] < n) == (e[1] < n)}
        cs2[2] -= moved
        cs2[0] |= moved
        return N, [sorted(s) for s in cs2], v, u, partner, marks
    K23.predicted_k23 = bad_colour
    ok["K2"] = must_fail(lambda: k23_check("F", 6), "K2 orphan pairs recoloured")
    K23.predicted_k23 = orig

    def drop_edge(kind, n):
        N, cs, v, u, partner, marks = orig(kind, n)
        cs2 = [set(map(tuple, s)) for s in cs]
        cs2[0].discard(tuple(sorted((v[0], u[0]))))
        return N, [sorted(s) for s in cs2], v, u, partner, marks
    K23.predicted_k23 = drop_edge
    ok["K3"] = must_fail(lambda: k23_check("F", 6), "K3 one cross edge deleted")
    K23.predicted_k23 = orig

    # K4: an even lattice -> no odd relation
    # three IDENTICAL difference vectors: the kernel is spanned by
    # (1,-1,0) and (0,1,-1), both of even coordinate sum, so no odd relation
    even = [(1, 0, 0), (1, 0, 0), (1, 0, 0)]
    r = odd_relation(even)
    print(f"  K4 even difference lattice: odd relation = {r} "
          f"({'correctly None' if r is None else 'CONTROL FAILURE'})")
    ok["K4"] = r is None
    # K5: the bare 2x3 permanent configuration must yield a 3-term relation
    # coordinates: e_{ab} for a in {0,1}, b in {0,1,2} -> index 3a+b
    def d(b, c):
        v = [0] * 6
        v[0 * 3 + b] += 1
        v[1 * 3 + c] += 1
        v[0 * 3 + c] -= 1
        v[1 * 3 + b] -= 1
        return tuple(v)
    k23 = [d(0, 1), d(1, 2), d(2, 0)]
    r5 = odd_relation(k23)
    print(f"  K5 bare K_2,3 permanent lattice: odd relation {r5} "
          f"(coefficient sum {sum(r5) if r5 else None})")
    ok["K5"] = r5 is not None and sum(r5) % 2 == 1

    print("\n== Task 1 checker controls ==")
    h = 4
    src = random_source(h, rng, lo=-3, hi=3)
    A = [0] * NCAP
    for i in COLORS:
        for j in COLORS:
            A[kidx(i, j)] = src[(0, 1)][i][j]
    rows, _ = L_generators(h, A)
    basis, pivots = rref_exact(rows)
    word = tuple(rng.randrange(3) for _ in range(2 * h))
    z = graded_error(src, h, word)
    poly = graded_to_poly(src, h, z)
    assert in_span_exact(basis, pivots, poly_to_row(poly, h))
    # L1: STRUCTURAL mutation -- rebuild the error with the endpoint-swapped
    # term of R subtracted instead of added (R = P_a (x) Q_b - P_b (x) Q_a).
    # The permanental symmetrisation is destroyed, so the law must fail.
    from w13_core import block, partial_matchings
    P, Q, U = sites(h)
    slot = {site: n for n, site in enumerate(U)}
    def mutated_error(source, word):
        sp = {(k,): A[k] for k in range(NCAP) if A[k]}
        def R_form(a, b):
            ca, cb = word[slot[a]], word[slot[b]]
            f = {}
            for i in COLORS:
                for j in COLORS:
                    val = (block(source, P, a, i, ca) * block(source, Q, b, j, cb)
                           - block(source, P, b, i, cb) * block(source, Q, a, j, ca))
                    if val:
                        f[(kidx(i, j),)] = val
            return f
        from w13_core import perfect_matchings, poly_add
        from itertools import combinations as comb
        total = {}
        for M in perfect_matchings(U):
            Rs = {e: R_form(*e) for e in M}
            xs = {e: source[e][word[slot[e[0]]]][word[slot[e[1]]]] for e in M}
            for jsize in range(0, h - 1):
                for J in comb(M, jsize):
                    weight = 1
                    for e in J:
                        weight *= xs[e]
                    if weight == 0:
                        continue
                    term = {(): weight}
                    for e in M:
                        if e in J:
                            continue
                        term = poly_mul(term, Rs[e])
                        if not term:
                            break
                    if not term:
                        continue
                    if jsize:
                        term = poly_mul(term, poly_pow(sp, jsize))
                    total = poly_add(total, term)
        return total
    bad = mutated_error(src, word)
    ok["L1"] = not in_span_exact(basis, pivots, poly_to_row(bad, h))
    print(f"  L1 sign-mutated R (antisymmetric instead of symmetric endpoint "
          f"exchange): stays in L_4 = {not ok['L1']}: "
          f"{'REJECTED' if ok['L1'] else 'CONTROL FAILURE'}")
    # L2: the truncated law must not contain E_w
    rows2 = []
    sp = {(k,): A[k] for k in range(NCAP) if A[k]}
    for k in (3, 4):
        for mu, nu in sigma_basis(k):
            g = dict(iota(k, mu, nu))
            if h - k:
                g = poly_mul(g, poly_pow(sp, h - k))
            rows2.append(poly_to_row(g, h))
    b2, p2 = rref_exact(rows2)
    ok["L2"] = not in_span_exact(b2, p2, poly_to_row(poly, h))
    print(f"  L2 truncated law Sigma_4 + s Sigma_3 (dim {len(p2)}): "
          f"E_w escapes it: {'REJECTED' if ok['L2'] else 'CONTROL FAILURE'}")
    # L3: a random quartic must not lie in L_4
    mons = monomials(NCAP, h)
    rand = {mons[rng.randrange(len(mons))]: rng.randint(1, 9) for _ in range(12)}
    ok["L3"] = not in_span_exact(basis, pivots, poly_to_row(rand, h))
    print(f"  L3 random quartic in L_4(A): "
          f"{'no (law is non-vacuous)' if ok['L3'] else 'CONTROL FAILURE'}")
    # L4: h = 3 span reproduces P1's 136
    h3 = 3
    src3 = random_source(h3, rng)
    A3f = [0] * NCAP
    for i in COLORS:
        for j in COLORS:
            A3f[kidx(i, j)] = src3[(0, 1)][i][j]
    keyorder = [(k, mu, nu) for k in range(2, h3 + 1)
                for mu, nu in sigma_basis(k)]
    kpos = {t: n for n, t in enumerate(keyorder)}
    zrows = []
    from itertools import product as iproduct
    for w in iproduct(range(3), repeat=2 * h3):
        zz = graded_error(src3, h3, w)
        row = [0] * len(keyorder)
        for k in range(2, h3 + 1):
            for (mu, nu), c in zz[k].items():
                row[kpos[(k, mu, nu)]] = c
        zrows.append(row)
    rk = rank_mod_p_np(zrows, P1)
    ok["L4"] = (rk == 136)
    print(f"  L4 h=3 span over all 729 words: {rk} "
          f"(P1 independently measured 136): "
          f"{'MATCH' if ok['L4'] else 'MISMATCH'}")

    OUT["controls"] = ok
    print(f"\n  {sum(1 for v in ok.values() if v)}/{len(ok)} controls behave "
          f"as required")
    with open(__file__.rsplit("/", 1)[0] + "/results_controls.json", "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print("wrote results_controls.json")


if __name__ == "__main__":
    main()
