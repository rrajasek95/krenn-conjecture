#!/usr/bin/env python3
"""A6 / TARGET B item 8: Lemma W14.1 (hafnian closed form) + Theorem W14.2
(level law), re-derived and verified with A6's own engine.

A6's PROOFS (both elementary):
 W14.1  Expanding Haf(W') = sum_M prod_{(a,b) in M} (alpha_a beta_b +
        alpha_b beta_a) indexes terms by (M, orientation).  A term is
        prod_{S} alpha prod_{S^c} beta where S picks one endpoint of each
        edge, so |S| = k and M is a perfect matching between S and S^c;
        there are exactly k! such M for each S.  Hence Haf = k! sum_S ...
 W14.2  Regroup the matching sum of E_w by J: sum_M sum_{J subset M} =
        sum_{J partial matching} sum_{M superset J}, and the inner sum is
        the hafnian over U \\ V(J).  Hence E_w(u(x)v) = sum_j alpha^j G_j.

ALSO the factorial audit: eq (4) of the descent note carries 1/k! and
1/(h-k)!; A6 evaluates eq (4) LITERALLY in the square-free algebra and
compares with the matching-sum expansion.
"""
from __future__ import annotations

import json
import random
from fractions import Fraction
from itertools import product

import a6_bcore as B

out = {}
rng = random.Random(20260815)

# --------------------------------------------------- factorial audit (h=2,3)
fa = {}
for h in (2, 3):
    P, Q, U = B.sites(h)
    ok, tested = True, 0
    detail = []
    for trial in range(2 if h == 3 else 3):
        src = B.rnd_source(h, rng)
        sf = B.Ew_squarefree(src, h)
        words = [tuple(rng.randrange(3) for _ in range(2 * h)) for _ in range(6)]
        words += [tuple([c] * (2 * h)) for c in B.COL]
        for w in words:
            m = B.Ew_matchings(src, h, w)
            s = sf.get(w, {})
            s = {k: v for k, v in s.items() if v}
            m2 = {k: Fraction(v) for k, v in m.items()}
            tested += 1
            if s != m2:
                ok = False
                detail.append({"h": h, "word": list(w),
                               "sf_terms": len(s), "mm_terms": len(m2)})
    fa[h] = {"eq4_with_factorials_equals_matching_sum": ok, "checks": tested,
             "failures": detail[:3]}
out["factorial_audit"] = fa

# control: drop the 1/k! and the identity must BREAK
P, Q, U = B.sites(3)
src = B.rnd_source(3, rng)


def Ew_sf_nofact(src, h):
    n = 2 * h
    x, r = B.sf_x(src, h), B.sf_r(src, h)
    sp = B.s_form(src)
    tot = {}
    for k in range(2, h + 1):
        rk = {((), ()): {(): 1}}
        for _ in range(k):
            rk = B.sf_mul(rk, r, n)
        xj = {((), ()): {(): 1}}
        for _ in range(h - k):
            xj = B.sf_mul(xj, x, n)
        pr = B.sf_mul(rk, xj, n)
        spow = B.ppow(sp, h - k)
        for (T, c), poly in pr.items():
            if len(T) != n:
                continue
            tot[c] = B.padd(tot.get(c, {}), B.pmul(poly, spow))
    return tot


w0 = tuple(rng.randrange(3) for _ in range(6))
nf = Ew_sf_nofact(src, 3)
out["control_no_factorial_version_differs"] = (
    {k: Fraction(v) for k, v in nf.get(w0, {}).items()}
    != {k: Fraction(v) for k, v in B.Ew_matchings(src, 3, w0).items()})

# ------------------------------------------------- W14.1 hafnian closed form
haf = {"checks": 0, "fail": 0}
for h in (2, 3):
    P, Q, U = B.sites(h)
    for trial in range(3):
        src = B.rnd_source(h, rng)
        for _ in range(4):
            w = tuple(rng.randrange(3) for _ in range(2 * h))
            u = [rng.randint(-3, 3) for _ in B.COL]
            v = [rng.randint(-3, 3) for _ in B.COL]
            for size in (2, 4, 6):
                if size > 2 * h:
                    continue
                for sub in __import__("itertools").combinations(U, size):
                    haf["checks"] += 1
                    if (B.haf_slice(src, h, w, u, v, sub)
                            != B.haf_slice_closed(src, h, w, u, v, sub)):
                        haf["fail"] += 1
out["W14_1_hafnian_closed_form"] = haf
# mutation control: closed form with the WRONG factorial must fail somewhere
mism = 0
src = B.rnd_source(3, rng)
w = tuple(rng.randrange(3) for _ in range(6))
u = [1, 2, -1]
v = [3, -1, 2]
for sub in __import__("itertools").combinations(B.sites(3)[2], 4):
    direct = B.haf_slice(src, 3, w, u, v, sub)
    wrong = B.haf_slice_closed(src, 3, w, u, v, sub) // 2 * 1  # drop the 2!
    if direct != wrong:
        mism += 1
out["mutation_wrong_factorial_detected"] = mism > 0

# ------------------------------------------------------ W14.2 the level law
lev = {"rank_one_expansion_checks": 0, "rank_one_fail": 0,
       "colour_slice_checks": 0, "colour_slice_fail": 0,
       "z_level_checks": 0, "z_level_fail": 0}
for h in (2, 3):
    for trial in range(3):
        src = B.rnd_source(h, rng)
        for _ in range(3):
            w = tuple(rng.randrange(3) for _ in range(2 * h))
            E = B.Ew_matchings(src, h, w)
            for uv in ([[rng.randint(-3, 3) for _ in B.COL],
                        [rng.randint(-3, 3) for _ in B.COL]] for _ in range(3)):
                u, v = uv
                pt = [Fraction(u[i] * v[j]) for i in B.COL for j in B.COL]
                lhs = B.pev(E, pt)
                al = B.alpha_of(src, u, v)
                rhs = sum(al ** j * B.G_level(src, h, w, u, v, j)
                          for j in range(h - 1))
                lev["rank_one_expansion_checks"] += 1
                if lhs != rhs:
                    lev["rank_one_fail"] += 1
            for c in B.COL:
                dc = [1 if i == c else 0 for i in B.COL]
                pt = [Fraction(1) if n == 3 * c + c else Fraction(0)
                      for n in range(9)]
                lhs = B.pev(E, pt)
                sc = src[(0, 1)][c][c]
                rhs = sum(sc ** j * B.G_level(src, h, w, dc, dc, j)
                          for j in range(h - 1))
                lev["colour_slice_checks"] += 1
                if lhs != rhs:
                    lev["colour_slice_fail"] += 1
out["W14_2_level_law"] = lev

# mutation control: antisymmetric R (P_a Q_b - P_b Q_a) must break the law
orig = B.R_form


def R_anti(src, h, a, b, ca, cb):
    f = {}
    for i in B.COL:
        for j in B.COL:
            val = (B.blk(src, 0, a, i, ca) * B.blk(src, 1, b, j, cb)
                   - B.blk(src, 0, b, i, cb) * B.blk(src, 1, a, j, ca))
            if val:
                f[(B.kx(i, j),)] = f.get((B.kx(i, j),), 0) + val
    return {m: c for m, c in f.items() if c}


B.R_form = R_anti
src = B.rnd_source(3, rng)
w = tuple(rng.randrange(3) for _ in range(6))
u, v = [1, 1, 2], [2, -1, 1]
E = B.Ew_matchings(src, 3, w)
pt = [Fraction(u[i] * v[j]) for i in B.COL for j in B.COL]
al = B.alpha_of(src, u, v)
rhs = sum(al ** j * B.G_level(src, 3, w, u, v, j) for j in range(2))
out["mutation_antisymmetric_R_breaks_level_law"] = (B.pev(E, pt) != rhs)
B.R_form = orig

json.dump(out, open("results_B8_hafnian.json", "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
