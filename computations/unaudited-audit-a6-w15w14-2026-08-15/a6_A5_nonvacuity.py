#!/usr/bin/env python3
"""A6 / TARGET A step 4: NON-VACUITY, re-solved independently.

A6 constructs its OWN exact-rational point of the m=24 clean stratum
(not W15's build_point): all 108 full-block cells nonzero, every
effectively-clean mixed equation satisfied.  Construction (derived here):

  A01 = lam*(u (x) q)   A02 = g (x) h      A03 = g (x) (-t*l)
  A12 = k (x) (h/t)     A13 = k (x) l      A23 = arbitrary nonzero 3x3
  A07 = u (x) p         A14 = q (x) r      A56 = m (x) n
  A45 = e (x) m         A67 = n (x) f      A47[a][b] = -r_a p_b/lam - e_a f_b

Then P_L(x) = lam*u_{x0} q_{x1} A23[x2][x3],  P_R(y) = -m_{y5} n_{y6}
r_{y4} p_{y7}/lam, so Phi = P_L P_R + A07 A14 A23 A56 == 0 identically.
"""
from __future__ import annotations

import json
from fractions import Fraction as F
from itertools import product

import a6_engine as E

T = E.M24
V = E.Vars(T)
GM = set(E.gamma_matchings(T))
out = {}

FULLE = [(0, 1), (0, 2), (0, 3), (0, 7), (1, 2), (1, 3), (1, 4), (2, 3),
         (4, 5), (4, 7), (5, 6), (6, 7)]


def build(seed):
    """A6's own exact-rational clean point."""
    import random
    rng = random.Random(seed)

    def vec():
        return [F(rng.randint(1, 11), rng.randint(1, 6)) * rng.choice([1, -1])
                for _ in range(3)]

    u, q, p, r, m, n = vec(), vec(), vec(), vec(), vec(), vec()
    g, h, k, l, e, f = vec(), vec(), vec(), vec(), vec(), vec()
    lam = F(rng.randint(1, 9), rng.randint(1, 5))
    t = F(rng.randint(1, 9), rng.randint(1, 5))
    A23 = [[F(rng.randint(1, 11), rng.randint(1, 6)) * rng.choice([1, -1])
            for _ in range(3)] for _ in range(3)]
    val = {}

    def setb(uu, vv, M):
        for i in range(3):
            for j in range(3):
                val[V.v(E.EIDX[(uu, vv)], 3 * i + j)] = M[i][j]

    outer = lambda a, b, c=1: [[c * a[i] * b[j] for j in range(3)]
                               for i in range(3)]
    setb(0, 1, outer(u, q, lam))
    setb(0, 2, outer(g, h))
    setb(0, 3, outer(g, [-t * x for x in l]))
    setb(1, 2, outer(k, [x / t for x in h]))
    setb(1, 3, outer(k, l))
    setb(2, 3, A23)
    setb(0, 7, outer(u, p))
    setb(1, 4, outer(q, r))
    setb(5, 6, outer(m, n))
    setb(4, 5, outer(e, m))
    setb(6, 7, outer(n, f))
    setb(4, 7, [[-r[a] * p[b] / lam - e[a] * f[b] for b in range(3)]
                for a in range(3)])
    return val


def phi_at(val, w):
    """Phi(w) = sum over the 7 Gamma matchings (full-block cells only)."""
    tot = F(0)
    for mi in sorted(GM):
        t = F(1)
        for uv in E.MATCHINGS[mi]:
            t *= val[V.vw(uv, w)]
        tot += t
    return tot


eclean = [w for w in E.WORDS if set(E.fibre(T, w)) == GM]
SING = E.audit(T)["singles"]
sclean = [w for w in E.WORDS if all(
    not (w[u] == c // 3 and w[v] == c % 3) for (u, v), c in SING.items())]

rep = {}
for seed in (11, 22, 33):
    val = build(seed)
    zero = [V.name[k] for k, v in val.items() if v == 0]
    n_full_cells = len(val)
    bad_e = [w for w in eclean if len(set(w)) > 1 and phi_at(val, w) != 0]
    bad_s = [w for w in sclean if len(set(w)) > 1 and phi_at(val, w) != 0]
    phi_all_nonzero = sum(1 for w in E.WORDS if phi_at(val, w) != 0)
    # H_w computed the LONG way (full 105-matching sum restricted to the
    # template) must agree with Phi on effectively clean words
    agree = all(E.peval(E.Hpoly(T, V, w), val) == phi_at(val, w)
                for w in eclean[:400])
    rep[seed] = dict(full_block_cells=n_full_cells, zero_cells=zero,
                     n_effectively_clean_mixed=len([w for w in eclean
                                                    if len(set(w)) > 1]),
                     violated_effectively_clean=len(bad_e),
                     n_syntactically_clean_mixed=len([w for w in sclean
                                                      if len(set(w)) > 1]),
                     violated_syntactically_clean=len(bad_s),
                     words_with_Phi_nonzero_out_of_6561=phi_all_nonzero,
                     H_0_8=str(phi_at(val, (0,) * 8)),
                     Hpoly_agrees_with_Phi_on_clean=agree)
    if seed == 11:
        json.dump({V.name[k]: str(v) for k, v in sorted(val.items())},
                  open("a6_nonvacuity_point_seed11.json", "w"), indent=1)
out["A6_own_points"] = rep

# ---- mutation controls on this checker
val = build(11)
mut = {}
# perturb one cell that is visible to the clean system -> must break something
for cellname, (uv, ij) in [("A01_00", ((0, 1), (0, 0))),
                           ("A45_00", ((4, 5), (0, 0))),
                           ("A07_00", ((0, 7), (0, 0))),
                           ("A23_00", ((2, 3), (0, 0)))]:
    v2 = dict(val)
    vid = V.v(E.EIDX[uv], 3 * ij[0] + ij[1])
    v2[vid] = v2[vid] + 1
    broke = sum(1 for w in eclean if len(set(w)) > 1 and phi_at(v2, w) != 0)
    mut[cellname] = broke
out["mutation_perturb_one_cell_breaks_n_clean_eqs"] = mut

# a random (non-solution) point must violate many clean equations
import random
rng = random.Random(7)
rp = {k: F(rng.randint(1, 9), rng.randint(1, 5)) for k in val}
out["control_random_point_violations"] = sum(
    1 for w in eclean if len(set(w)) > 1 and phi_at(rp, w) != 0)

# ---- does the stratum FORCE H_{0^8} = 0 at these points?  (it must)
out["all_points_have_H_0_8_zero"] = all(r["H_0_8"] == "0"
                                        for r in rep.values())

json.dump(out, open("results_A5_nonvacuity.json", "w"), indent=1)
print(json.dumps(out, indent=1))
