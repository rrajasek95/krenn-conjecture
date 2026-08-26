#!/usr/bin/env python3
"""W21-M1-TENSOR -- verification of the equivalent forms + mutation controls.
UNAUDITED.  Exact only."""
import json
import os
import random
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w21t_core as T                                           # noqa: E402

rng = random.Random(21072026)
res = {"_header": "UNAUDITED W21-M1-TENSOR form verification. Exact only."}

# ---- (1) SLICE form == the 81 equations, on RANDOM exact matrices ----------
bad_slice = bad_star = bad_group = 0
for _ in range(30):
    M = {p: T.rand_matrix(rng) for p in T.PAIRS}
    eqs = sorted(str(v) for v in T.all_equations(M))
    sl = sorted(str(T.slice_matrix(M, r, s)[a][b])
                for r in range(3) for s in range(3)
                for a in range(3) for b in range(3))
    if eqs != sl:
        bad_slice += 1
    # STAR at the standard basis reproduces SLICE
    for r in range(3):
        for s in range(3):
            e_r = [Fraction(int(k == r)) for k in range(3)]
            e_s = [Fraction(int(k == s)) for k in range(3)]
            if T.star_matrix(M, e_r, e_s) != T.slice_matrix(M, r, s):
                bad_star += 1
    # STAR at random u,v is a bilinear combination of the slices
    u = [Fraction(rng.randint(-5, 5)) for _ in range(3)]
    v = [Fraction(rng.randint(-5, 5)) for _ in range(3)]
    acc = T.zeros()
    for r in range(3):
        for s in range(3):
            acc = T.madd(acc, T.smul(u[r] * v[s], T.slice_matrix(M, r, s)))
    if acc != T.star_matrix(M, u, v):
        bad_star += 1
    # group matrices reproduce the tensor
    G0 = T.group_matrix(M, 0)
    G0b = T.madd([[T.matmul([[x] for x in sum(M[(1, 2)], [])],
                            [sum(M[(3, 4)], [])])[i][j]
                   for j in range(9)] for i in range(9)],
                 T.kron(M[(1, 3)], M[(2, 4)]),
                 [[M[(1, 4)][a][d] * M[(2, 3)][b][c] for c in range(3)
                   for d in range(3)] for a in range(3) for b in range(3)])
    if G0 != G0b:
        bad_group += 1
print("SLICE == 81 equations   : %d mismatches / 30" % bad_slice)
print("STAR  consistency       : %d mismatches / 300" % bad_star)
print("grouping (12|34) decomp : %d mismatches / 30" % bad_group)
res.update(slice_mismatches=bad_slice, star_mismatches=bad_star,
           group_mismatches=bad_group)

# ---- (2) a family of genuine solutions, to calibrate ----------------------
# All-rank-1 "GHZ-like" solutions: M_{ij} = t_{ij} * (e (x) e) collapses the
# hafnian to (sum over pairings t t) * (e(x)e(x)e(x)e); vanishing needs the
# scalar haf to vanish.
sols = []
for _ in range(200):
    e = {i: [Fraction(rng.randint(-4, 4) or 1) for _ in range(3)]
         for i in (1, 2, 3, 4)}
    t = {p: Fraction(rng.randint(-5, 5) or 2) for p in T.PAIRS}
    # force the scalar hafnian of t to vanish by solving for t[(3,4)]
    a = t[(1, 2)]
    b = (t[(1, 3)] * t[(2, 4)] + t[(1, 4)] * t[(2, 3)])
    if a == 0:
        continue
    t[(3, 4)] = -b / a
    if t[(3, 4)] == 0:
        continue
    M = {p: T.smul(t[p], T.outer(e[p[0]], e[p[1]])) for p in T.PAIRS}
    if T.satisfies(M):
        sols.append((M, T.ranks(M), T.any_site_factors(M)))
print("calibration: %d/200 all-rank-1 constructions satisfy (T); "
      "factoring sites in each: %s"
      % (len(sols), sorted({tuple(s[2]) for s in sols})))
res["rank1_family_hits"] = len(sols)
res["rank1_family_factoring"] = sorted(str(tuple(s[2])) for s in sols)[:3]

# ---- (3) MUTATION CONTROL: perturbing a solution must break (T) ----------
fired = 0
for M, _, _ in sols[:20]:
    M2 = {p: [r[:] for r in M[p]] for p in T.PAIRS}
    M2[(1, 2)][0][0] = M2[(1, 2)][0][0] + 1
    if not T.satisfies(M2):
        fired += 1
print("MUTATION control (perturb one entry of a solution): %d/20 firings"
      % fired)
res["mutation_firings"] = fired

# ---- (4) the RANK inequalities, on the calibration solutions -------------
viol = 0
for M, rk, _ in sols:
    P = rk[(1, 2)] * rk[(3, 4)]
    Q = rk[(1, 3)] * rk[(2, 4)]
    R = rk[(1, 4)] * rk[(2, 3)]
    if max(abs(P - Q), abs(Q - R), abs(P - R)) > 1:
        viol += 1
print("rank-product inequalities on the calibration solutions: %d violations"
      % viol)
res["rank_ineq_violations"] = viol

# ---- (5) MUTATION control for the rank-inequality checker ----------------
# a NON-solution with rank products far apart must be flagged
M = {p: T.rand_matrix(rng) for p in T.PAIRS}
rk = T.ranks(M)
P = rk[(1, 2)] * rk[(3, 4)]
Q = rk[(1, 3)] * rk[(2, 4)]
print("MUTATION control (random non-solution): rank products %d,%d,%d -- "
      "differences %s (checker would flag: %s), satisfies(T)=%s"
      % (P, Q, rk[(1, 4)] * rk[(2, 3)],
         max(abs(P - Q), abs(Q - rk[(1, 4)] * rk[(2, 3)])),
         max(abs(P - Q), abs(Q - rk[(1, 4)] * rk[(2, 3)])) > 1,
         T.satisfies(M)))
json.dump(res, open(os.path.join(HERE, "results_verify.json"), "w"),
          indent=1, default=str)
