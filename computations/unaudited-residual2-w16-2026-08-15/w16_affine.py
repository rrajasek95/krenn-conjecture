#!/usr/bin/env python3
"""W16 -- the AFFINE-LINEAR structure of the X_free clean layer (m=25..28).

For x in X_free every one of the 81 R-words is clean.  In the expansion
Phi(x,y) = sum_{S even} (prod_{i in S} c_i) haf_L(L\\S)(x) haf_R(R\\sigma S)(y)
the L-side enters ONLY through the seven scalars

  lam_x = P_L(x),  A01[x0][x1], A02[x0][x2], A03[x0][x3],
                   A12[x1][x2], A13[x1][x3], A23[x2][x3]

(each multiplying a vector of R-side data), and the S = L term
c_0c_1c_2c_3 carries NO L-scalar.  So, for FIXED R-side and cross data,
"Phi(x,.) = 0 on all 81 words" is an AFFINE-LINEAR feasibility question in
those seven scalars -- exactly the m=25 Step-A situation one level up.

This module measures, by exact rational linear algebra, how restrictive
that is: the rank of the 81 x 7 coefficient matrix, and whether the
inhomogeneous vector lies in its column span, for
  (a) generic R-data (all cells nonzero, no structure),
  (b) the J-point family (every Gamma block = t_e * J),
  (c) "all Gamma blocks rank one with consistent vertex vectors",
  (d) one prescribed factoring vertex, everything else generic.
"""
from __future__ import annotations
import os, sys, json, itertools
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w16_core import (W8_IMMUNE, EDGES, EIDX, FULL, full_pm_indices, PM_E,
                      cell)

HERE = os.path.dirname(os.path.abspath(__file__))
L = (0, 1, 2, 3)
R = (4, 5, 6, 7)
SIG = {0: 7, 1: 4, 2: 5, 3: 6}
LPAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def haf_R_sub(B, gam, verts, y):
    verts = tuple(sorted(verts))
    if not verts:
        return Fraction(1)
    tot = Fraction(0)
    a = verts[0]
    for i in range(1, len(verts)):
        b = verts[i]
        if (a, b) not in gam:
            continue
        rest = verts[1:i] + verts[i + 1:]
        tot += B[(a, b)][y[a - 4]][y[b - 4]] * haf_R_sub(B, gam, rest, y)
    return tot


def columns(B, gam, x):
    """the 81 x 7 coefficient matrix and the inhomogeneous vector."""
    ys = list(itertools.product(range(3), repeat=4))
    cols = {k: [] for k in ["lam"] + ["%d%d" % p for p in LPAIRS]}
    rhs = []
    for y in ys:
        def c(i):
            j = SIG[i]
            e = (min(i, j), max(i, j))
            return B[e][x[i]][y[j - 4]] if e in gam else Fraction(0)
        cols["lam"].append(haf_R_sub(B, gam, R, y))
        for (k, l) in LPAIRS:
            S = tuple(v for v in L if v not in (k, l))
            coef = Fraction(1)
            for i in S:
                coef *= c(i)
            coef *= haf_R_sub(B, gam, tuple(SIG[v] for v in (k, l)), y)
            cols["%d%d" % (k, l)].append(coef)
        t = Fraction(1)
        for i in L:
            t *= c(i)
        rhs.append(-t)
    return cols, rhs


def rank_and_feasible(cols, rhs):
    keys = list(cols)
    rows = [[cols[k][i] for k in keys] for i in range(len(rhs))]
    aug = [rows[i] + [rhs[i]] for i in range(len(rhs))]
    def rk(M, nc):
        M = [r[:] for r in M]
        r = 0
        for c in range(nc):
            sel = None
            for i in range(r, len(M)):
                if M[i][c]:
                    sel = i
                    break
            if sel is None:
                continue
            M[r], M[sel] = M[sel], M[r]
            pv = M[r][c]
            M[r] = [v / pv for v in M[r]]
            for i in range(len(M)):
                if i != r and M[i][c]:
                    f = M[i][c]
                    M[i] = [a - f * b for a, b in zip(M[i], M[r])]
            r += 1
        return r
    r1 = rk(rows, len(keys))
    r2 = rk(aug, len(keys) + 1)
    return r1, r2, (r1 == r2)


def lcg(seed):
    s = seed
    while True:
        s = (1103515245 * s + 12345) % (1 << 31)
        yield s


def make(kind, gam, seed):
    r = lcg(seed)
    def rn():
        return Fraction((next(r) % 15) - 7 or 4, (next(r) % 5) + 1)
    B = {}
    if kind == "generic":
        for e in gam:
            B[e] = [[rn() for _ in range(3)] for _ in range(3)]
    elif kind == "J":
        for e in gam:
            t = rn()
            B[e] = [[t] * 3 for _ in range(3)]
    elif kind == "rank1_vertexwise":
        vec = {v: [rn() for _ in range(3)] for v in range(8)}
        for (u, v) in gam:
            t = rn()
            B[(u, v)] = [[t * vec[u][i] * vec[v][j] for j in range(3)]
                         for i in range(3)]
    elif kind == "vertex4_only":
        for e in gam:
            B[e] = [[rn() for _ in range(3)] for _ in range(3)]
        vec4 = [rn() for _ in range(3)]
        for (u, v) in gam:
            if u == 4 or v == 4:
                w = [rn() for _ in range(3)]
                if u == 4:
                    B[(u, v)] = [[vec4[i] * w[j] for j in range(3)]
                                 for i in range(3)]
                else:
                    B[(u, v)] = [[w[i] * vec4[j] for j in range(3)]
                                 for i in range(3)]
    return B


def main():
    out = {}
    XF = [(x0, 2, 0, x3) for x0 in (1, 2) for x3 in (0, 1)]
    for m in (25, 26, 27, 28):
        T = W8_IMMUNE[m]
        gam = set(EDGES[i] for i, t in enumerate(T) if t == FULL)
        entry = {}
        for kind in ("generic", "J", "rank1_vertexwise", "vertex4_only"):
            rows = []
            for seed in (11, 23, 47):
                B = make(kind, gam, seed)
                if any(v == 0 for e in gam for row in B[e] for v in row):
                    continue
                fs = []
                for x in XF:
                    cols, rhs = columns(B, gam, x)
                    r1, r2, ok = rank_and_feasible(cols, rhs)
                    fs.append((r1, r2, ok))
                rows.append(dict(seed=seed, per_x=fs,
                                 all_feasible=all(f[2] for f in fs)))
            entry[kind] = rows
            print("m=%d %-18s ranks/feasible: %s" %
                  (m, kind, [(r["per_x"][0][0], r["per_x"][0][1],
                              r["all_feasible"]) for r in rows]))
        out[m] = entry
    json.dump(out, open(os.path.join(HERE, "results_affine.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
