#!/usr/bin/env python3
"""W21-M1-TENSOR -- EXPLICIT EXACT POINTS of every feasible 2x2 stratum.
UNAUDITED.  Exact only.  These are the mandatory explicit-point controls for
the two infeasibility verdicts (B2 and B3-star): the SAME saturation
pipeline reports these strata NONEMPTY, and here are the witnesses."""
import json
import os
import random
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w21t_core as T                                           # noqa: E402

rng = random.Random(9091)
F = Fraction
res = {"_header": "UNAUDITED W21-M1-TENSOR explicit stratum points. Exact."}


def emb(A2):
    return [[A2[i][j] if i < 2 and j < 2 else F(0) for j in range(3)]
            for i in range(3)]


def report(name, M, expect_rank2, expect_fac):
    rk = T.ranks(M)
    fac = T.any_site_factors(M)
    r2 = sorted(p for p in T.PAIRS if rk[p] == 2)
    ok = (T.satisfies(M) and r2 == sorted(expect_rank2)
          and sorted(fac) == sorted(expect_fac))
    print("%-14s satisfies=%-5s ranks=%s rank2=%s factoring=%s  MATCHES=%s"
          % (name, T.satisfies(M), [rk[p] for p in T.PAIRS], r2, fac, ok))
    res[name] = dict(satisfies=T.satisfies(M),
                     ranks={str(p): rk[p] for p in T.PAIRS},
                     factoring=fac, matches_prediction=ok,
                     point={str(p): [[str(x) for x in row] for row in M[p]]
                            for p in T.PAIRS})
    return ok


# ---- B0: all rank 1 -> all four sites factor ---------------------------
e = {i: [F(1), F(i), F(i * i)] for i in (1, 2, 3, 4)}
t = {(1, 2): F(1), (1, 3): F(2), (1, 4): F(3), (2, 3): F(5), (2, 4): F(7)}
t[(3, 4)] = -(t[(1, 3)] * t[(2, 4)] + t[(1, 4)] * t[(2, 3)]) / t[(1, 2)]
M_B0 = {p: T.smul(t[p], T.outer(e[p[0]], e[p[1]])) for p in T.PAIRS}
report("B0", M_B0, [], [1, 2, 3, 4])

# ---- B1: one rank 2 (M12) -> sites 3 and 4 factor ---------------------
al = [F(1), F(2), F(-1)]
be = [F(3), F(1), F(2)]
eta = [F(1), F(0), F(1)]
kap = [F(0), F(1), F(2)]
gam = [F(1), F(1), F(0)]
eps = [F(2), F(0), F(1)]
a, b, c, d = F(2), F(3), F(5), F(7)
M_B1 = {(3, 4): T.outer(al, be),
        (1, 3): T.outer(eta, [a * z for z in al]),
        (2, 3): T.outer(eps, [b * z for z in al]),
        (2, 4): T.outer(gam, [c * z for z in be]),
        (1, 4): T.outer(kap, [d * z for z in be])}
M_B1[(1, 2)] = T.madd(T.smul(-a * c, T.outer(eta, gam)),
                      T.smul(-b * d, T.outer(kap, eps)))
report("B1", M_B1, [(1, 2)], [3, 4])

# ---- B3-triangle: M12,M13,M23 rank 2 -> site 4 factors ----------------
alp = [F(1), F(1)]
gm = [F(1), F(0)]
kp = [F(0), F(1)]
a0 = [F(1), F(0)]
m0 = [F(0), F(1)]
mu = F(3)
a1 = [a0[i] + mu * kp[i] for i in range(2)]
m1 = [m0[i] - mu * gm[i] for i in range(2)]
M13_2 = [[a0[i], a1[i]] for i in range(2)]
M23_2 = [[m0[i], m1[i]] for i in range(2)]
M12_2 = T.madd(T.smul(F(-1), T.outer(a0, gm)), T.smul(F(-1), T.outer(kp, m0)))
be2 = [F(2), F(5)]
M_B3t = {(1, 2): emb(M12_2), (1, 3): emb(M13_2), (2, 3): emb(M23_2),
         (1, 4): emb(T.outer(kp, be2)), (2, 4): emb(T.outer(gm, be2)),
         (3, 4): emb(T.outer(alp, be2))}
report("B3triangle", M_B3t, [(1, 2), (1, 3), (2, 3)], [4])

# ---- A: all rank 2 -> NO site factors ---------------------------------
I2 = [[F(1), F(0)], [F(0), F(1)]]
J2 = [[F(0), F(1)], [F(-1), F(0)]]
th = F(3)
M_A = {(1, 2): emb(T.smul(1 / th, J2)), (3, 4): emb(T.smul(th, J2)),
       (1, 3): emb(I2), (1, 4): emb(I2), (2, 3): emb(I2),
       (2, 4): emb(T.smul(F(-1), I2))}
report("A", M_A, list(T.PAIRS), [])

# ---- a GL_3^4 transport of A with ALL 54 ENTRIES NONZERO --------------
found = None
for _ in range(4000):
    g = {i: [[F(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
         for i in (1, 2, 3, 4)}
    if any(T.rank(g[i]) < 3 for i in (1, 2, 3, 4)):
        continue
    Mg = {p: T.matmul(g[p[0]], T.matmul(M_A[p], T.transpose(g[p[1]])))
          for p in T.PAIRS}
    if all(x != 0 for p in T.PAIRS for row in Mg[p] for x in row):
        found = Mg
        break
if found:
    report("A_all_entries_nonzero", found, list(T.PAIRS), [])
else:
    print("no all-nonzero transport found in 4000 tries")
res["A_nonzero_transport_found"] = found is not None
json.dump(res, open(os.path.join(HERE, "results_points.json"), "w"),
          indent=1, default=str)
