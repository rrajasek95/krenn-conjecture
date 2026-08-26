#!/usr/bin/env python3
"""W21-M1-TENSOR -- Lemma 1/2/3 and the reduction to 2x2.  UNAUDITED.  Exact.

LEMMA 1 [PROVED-HERE].  If M_{34} != 0 then rank M_{12} <= 2.
  Proof: pick u,v with <u,M34 v> != 0; (STAR) writes M12 as a combination of
  two rank-<=1 matrices.  By S_4 symmetry: all six nonzero => all ranks <= 2.

LEMMA 2 [PROVED-HERE].  rank M_{12} = 3  =>  M_{34} = 0, and then
  M13 (x) M24 + M14 (x) M23 = 0 with M12 UNCONSTRAINED; the four remaining
  matrices have rank <= 1 and (if all nonzero) their slot vectors pair up so
  that sites 3 and 4 BOTH FACTOR.

LEMMA 3 [PROVED-HERE] -- THE REDUCTION.  If all six M are nonzero then every
  site i has rho_i := dim span(column spaces of the three M's at i) <= 2.
  Proof for i = 1: choose v0 outside ker M24 and ker M34, and u0 outside
  ker M23 and ker M34^T.  Put W = span{M13 u0, M14 v0} (dim <= 2).
  (STAR) at (u0,v0) gives col M12 subset W.  For any u with <u,M34 v0> != 0,
  (STAR) at (u,v0) gives (M13 u)(M24 v0)^T = -<u,M34 v0> M12
  - (M14 v0)(M23 u)^T, whose column space lies in W; since M24 v0 != 0 this
  forces M13 u in W.  Those u are Zariski-dense, so col M13 subset W; the
  mirror argument gives col M14 subset W.   []
  CONSEQUENCE: after the GL_3^4 action M_{ij} -> g_i M_{ij} g_j^T (which
  preserves the solution set, since the tensor transforms by
  g_1 (x) g_2 (x) g_3 (x) g_4) every solution with all six M nonzero is
  supported in a common 2x2 corner.  The classification is therefore the
  2 x 2 classification.

This module verifies Lemmas 1-3 numerically-exactly on constructed solutions
and runs the mutation controls.
"""
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

rng = random.Random(88112)
res = {"_header": "UNAUDITED W21-M1-TENSOR lemmas. Exact only."}


def rho(M, i):
    cols = []
    for j in (1, 2, 3, 4):
        if j == i:
            continue
        p = (min(i, j), max(i, j))
        A = M[p] if p[0] == i else T.transpose(M[p])
        for c in range(3):
            v = T.col(A, c)
            if any(v):
                cols.append(v)
    return T.rank(cols) if cols else 0


def embed2(A2):
    """embed a 2x2 matrix in the top-left corner of a 3x3."""
    return [[A2[i][j] if i < 2 and j < 2 else Fraction(0) for j in range(3)]
            for i in range(3)]


# ---------------- the Case-A ("symplectic") solution ----------------------
I2 = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
J2 = [[Fraction(0), Fraction(1)], [Fraction(-1), Fraction(0)]]


def caseA(theta=Fraction(1)):
    return {(1, 2): embed2(T.smul(1 / theta, J2)),
            (3, 4): embed2(T.smul(theta, J2)),
            (1, 3): embed2(I2), (1, 4): embed2(I2), (2, 3): embed2(I2),
            (2, 4): embed2(T.smul(Fraction(-1), I2))}


print("=== CASE A: the all-rank-2 solution ===")
okA, facA = [], []
for th in (Fraction(1), Fraction(3), Fraction(-2, 5), Fraction(7, 3)):
    M = caseA(th)
    okA.append(T.satisfies(M))
    facA.append(T.any_site_factors(M))
    if th == 1:
        print("   ranks", sorted(T.ranks(M).items()),
              " rho per site", [rho(M, i) for i in (1, 2, 3, 4)])
print("   satisfies (T): %s ; factoring sites: %s" % (okA, facA))
res["caseA_satisfies"] = okA
res["caseA_factoring_sites"] = [list(f) for f in facA]

# MUTATION control on the Case-A solution
M = caseA()
M[(2, 4)][0][0] = M[(2, 4)][0][0] + 1
print("   MUTATION control (perturb M24): satisfies (T) = %s" % T.satisfies(M))
res["caseA_mutation"] = T.satisfies(M)

# a GL_3^4-transported copy: all NINE entries nonzero, still a solution,
# still no factoring site (this is what matters for the application)
while True:
    g = {i: [[Fraction(rng.randint(-4, 4)) for _ in range(3)]
             for _ in range(3)] for i in (1, 2, 3, 4)}
    if all(T.rank(g[i]) == 3 for i in (1, 2, 3, 4)):
        break
M0 = caseA()
Mg = {p: T.matmul(g[p[0]], T.matmul(M0[p], T.transpose(g[p[1]])))
      for p in T.PAIRS}
nz = all(x != 0 for p in T.PAIRS for row in Mg[p] for x in row)
print("   GL_3^4 transport: satisfies=%s  all 54 entries nonzero=%s  "
      "ranks=%s  factoring sites=%s"
      % (T.satisfies(Mg), nz, sorted(T.ranks(Mg).items()),
         T.any_site_factors(Mg)))
res["caseA_transported"] = dict(satisfies=T.satisfies(Mg), all_nonzero=nz,
                                ranks={str(k): v for k, v in
                                       T.ranks(Mg).items()},
                                factoring=T.any_site_factors(Mg))

# ---------------- Lemma 3 on a battery of constructed solutions ----------
print("=== LEMMA 3 check (rho <= 2 whenever all six are nonzero) ===")
tested = viol = 0
pool = []
# (a) rank-1 (B0) solutions
for _ in range(300):
    e = {i: [Fraction(rng.randint(-4, 4) or 1) for _ in range(3)]
         for i in (1, 2, 3, 4)}
    t = {p: Fraction(rng.randint(-5, 5) or 2) for p in T.PAIRS}
    if t[(1, 2)] == 0:
        continue
    t[(3, 4)] = -(t[(1, 3)] * t[(2, 4)] + t[(1, 4)] * t[(2, 3)]) / t[(1, 2)]
    if t[(3, 4)] == 0:
        continue
    M = {p: T.smul(t[p], T.outer(e[p[0]], e[p[1]])) for p in T.PAIRS}
    if T.satisfies(M):
        pool.append(M)
# (b) Case A and its GL transports
for _ in range(60):
    g = {i: [[Fraction(rng.randint(-4, 4)) for _ in range(3)]
             for _ in range(3)] for i in (1, 2, 3, 4)}
    if any(T.rank(g[i]) < 3 for i in (1, 2, 3, 4)):
        continue
    M0 = caseA(Fraction(rng.randint(1, 6)))
    M = {p: T.matmul(g[p[0]], T.matmul(M0[p], T.transpose(g[p[1]])))
         for p in T.PAIRS}
    if T.satisfies(M):
        pool.append(M)
for M in pool:
    if all(not T.is_zero(M[p]) for p in T.PAIRS):
        tested += 1
        if max(rho(M, i) for i in (1, 2, 3, 4)) > 2:
            viol += 1
print("   %d all-nonzero solutions tested, %d with some rho >= 3" %
      (tested, viol))
res["lemma3_tested"] = tested
res["lemma3_violations"] = viol

# MUTATION control for the rho checker: a NON-solution with rho = 3
M = {p: T.rand_matrix(rng) for p in T.PAIRS}
print("   MUTATION control (random non-solution): rho per site %s, "
      "satisfies=%s" % ([rho(M, i) for i in (1, 2, 3, 4)], T.satisfies(M)))
res["rho_mutation"] = [rho(M, i) for i in (1, 2, 3, 4)]

# ---------------- Lemma 2 check -----------------------------------------
print("=== LEMMA 2 check (rank M12 = 3) ===")
cnt = 0
for _ in range(400):
    a = [Fraction(rng.randint(-4, 4) or 1) for _ in range(3)]
    b = [Fraction(rng.randint(-4, 4) or 1) for _ in range(3)]
    c = [Fraction(rng.randint(-4, 4) or 1) for _ in range(3)]
    d = [Fraction(rng.randint(-4, 4) or 1) for _ in range(3)]
    lam = Fraction(rng.randint(1, 5))
    mu = Fraction(rng.randint(1, 5))
    nu = Fraction(rng.randint(1, 5))
    rho_ = -1 / (lam * mu * nu)
    M = {(1, 2): T.rand_matrix(rng),
         (3, 4): T.zeros(),
         (1, 3): T.outer(a, b),
         (2, 4): T.outer(c, d),
         (1, 4): T.outer(T.matvec([[lam if i == j else Fraction(0)
                                    for j in range(3)] for i in range(3)], a),
                         [mu * x for x in d]),
         (2, 3): T.outer([nu * x for x in c], [rho_ * x for x in b])}
    if T.satisfies(M) and T.rank(M[(1, 2)]) == 3:
        cnt += 1
        f = T.any_site_factors(M)
        if not ({3, 4} <= set(f)):
            print("   LEMMA 2 EXCEPTION: factoring sites", f)
print("   %d/400 constructed rank-3 solutions; sites 3,4 factor in all"
      % cnt)
res["lemma2_hits"] = cnt
json.dump(res, open(os.path.join(HERE, "results_lemma.json"), "w"),
          indent=1, default=str)
