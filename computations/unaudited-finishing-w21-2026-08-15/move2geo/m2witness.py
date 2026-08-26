#!/usr/bin/env python3
"""W21-M2-GEO step 3: EXPLICIT EXACT WITNESSES for the collinearity strata.

A "degenerate R-site j" means all 12 points of its arrangement lie on ONE line
ker(u_j) of P^2, i.e.  A_{i,j} u_j = 0  for every i in L.  A "degenerate L-site
i" means  v_i^T A_{i,j} = 0  for every j in R.  Blocks carrying both live in a
4-dimensional space (3-dimensional if the block is fat).

These witnesses decide, EXACTLY, whether the pure collinear-transversal
combinatorics can be satisfied at all -- the question W21 asked.
UNAUDITED.  Exact rational arithmetic only.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import m2geo as X                                                   # noqa: E402
import w21_c8core as G                                              # noqa: E402

L, R = X.L, X.R


# ------------------------------------------------------------ block builder
def solve_block(u, v, dead, rng, tries=400):
    """a 3x3 rational block with A u = 0 (if u), v^T A = 0 (if v), the dead
    cell zero and every other cell NONZERO.  Exact.  None if impossible."""
    cells = [(c, d) for c in range(3) for d in range(3)]
    rows = []                                       # linear constraints
    if u is not None:
        for c in range(3):
            rows.append({(c, d): u[d] for d in range(3)})
    if v is not None:
        for d in range(3):
            rows.append({(c, d): v[c] for c in range(3)})
    if dead is not None:
        rows.append({dead: Fraction(1)})
    # solve by gaussian elimination on the 9 unknowns
    Mtx = [[Fraction(r.get(cl, 0)) for cl in cells] for r in rows]
    piv, where = 0, {}
    for col in range(9):
        sel = None
        for i in range(piv, len(Mtx)):
            if Mtx[i][col]:
                sel = i
                break
        if sel is None:
            continue
        Mtx[piv], Mtx[sel] = Mtx[sel], Mtx[piv]
        pv = Mtx[piv][col]
        Mtx[piv] = [a / pv for a in Mtx[piv]]
        for i in range(len(Mtx)):
            if i != piv and Mtx[i][col]:
                f = Mtx[i][col]
                Mtx[i] = [a - f * b for a, b in zip(Mtx[i], Mtx[piv])]
        where[col] = piv
        piv += 1
    freecols = [c for c in range(9) if c not in where]
    for _ in range(tries):
        vals = [Fraction(0)] * 9
        for c in freecols:
            vals[c] = Fraction(rng.randint(-12, 12) or 5, rng.randint(1, 3))
        for col, r in where.items():
            vals[col] = -sum(Mtx[r][c] * vals[c] for c in freecols)
        A = [[Fraction(0)] * 3 for _ in range(3)]
        for k, (c, d) in enumerate(cells):
            A[c][d] = vals[k]
        ok = True
        for c in range(3):
            for d in range(3):
                if (c, d) == dead:
                    if A[c][d] != 0:
                        ok = False
                elif A[c][d] == 0:
                    ok = False
        if ok:
            return A
    return None


def build(degenerate_R, degenerate_L, seed=1, uu=None, vv=None):
    """blocks with the listed R-sites / L-sites fully collinear."""
    rng = random.Random(seed)
    if uu is None:
        uu = {j: (Fraction(1), Fraction(2 + j), Fraction(-1 - j)) for j in R}
    if vv is None:
        vv = {i: (Fraction(1), Fraction(-2 - i), Fraction(3 + i)) for i in L}
    bl = {}
    for e in G.EDGES:
        m = G.C8_MEMBER[G.EIDX[e]]
        bl[e] = [[Fraction(0)] * 3 for _ in range(3)]
        u, v = e
        if u in L and v in R:
            continue
        for c in range(3):
            for d in range(3):
                if (m >> (3 * c + d)) & 1:
                    bl[e][c][d] = Fraction(rng.randint(-9, 9) or 4,
                                           rng.randint(1, 3))
    for i in L:
        for j in R:
            A = solve_block(uu[j] if j in degenerate_R else None,
                            vv[i] if i in degenerate_L else None,
                            X.DEAD.get((i, j)), rng)
            if A is None:
                return None
            bl[(i, j)] = A
    return bl


def audit(name, bl, res, full_H=True):
    ok, why = X.cells_all_nonzero(bl)
    KX, IY = X.obligations(bl)
    minK = min(len(v) for v in KX.values())
    minI = min(len(v) for v in IY.values())
    nfailL = sum(1 for x in X.LFREE for y in X.WORDS4
                 if G.per4(G.cross_matrix(bl, x, y)) != 0)
    nfailR = sum(1 for y in X.RFREE for x in X.WORDS4
                 if G.per4(G.cross_matrix(bl, x, y)) != 0)
    d = dict(cells_ok=ok, why=str(why),
             min_collinear_R_sites_over_Lfree=minK,
             min_collinear_L_sites_over_Rfree=minI,
             K_histogram={k: sum(1 for v in KX.values() if len(v) == k)
                          for k in range(5)},
             I_histogram={k: sum(1 for v in IY.values() if len(v) == k)
                          for k in range(5)},
             per_failures_Lfree_of_2430=nfailL,
             per_failures_Rfree_of_2430=nfailR)
    if full_H:
        nfail, nmix, kinds = X.all_mixed_failures(bl)
        d["H_mixed_failures"] = nfail
        d["H_mixed_total"] = nmix
        d["H_failure_kinds"] = kinds
        d["constants"] = [str(c) for c in X.constants(bl)]
    res[name] = d
    print("%-28s cells_ok=%s  minK=%d minI=%d  perfail L/R=%d/%d  %s"
          % (name, ok, minK, minI, nfailL, nfailR,
             ("Hmixfail=%d/%d" % (d.get("H_mixed_failures", -1),
                                  d.get("H_mixed_total", -1)))
             if full_H else ""))
    return d


def main():
    res = {"_header": "UNAUDITED W21-M2-GEO explicit witnesses, exact."}
    # 1. ALL FOUR R-sites and ALL FOUR L-sites degenerate: every one of the 60
    #    collinear-transversal obligations (indeed all 8*81) is satisfied.
    bl = build(set(R), set(L), seed=7)
    assert bl is not None
    audit("all8_degenerate", bl, res)
    # sanity: every site's collinear set is EVERYTHING
    res["all8_S_sizes"] = dict(
        R={j: len(X.S_R(bl, j)) for j in R},
        L={i: len(X.S_L(bl, i)) for i in L})
    print("   S-sizes:", res["all8_S_sizes"])

    # 2. THREE R-sites + THREE L-sites degenerate (the cheap sufficient
    #    configuration for |K(x)| >= 3 everywhere).
    bl3 = build({4, 5, 6}, {0, 1, 2}, seed=11)
    assert bl3 is not None
    audit("R456_L012_degenerate", bl3, res)
    res["R456_L012_S_sizes"] = dict(
        R={j: len(X.S_R(bl3, j)) for j in R},
        L={i: len(X.S_L(bl3, i)) for i in L})
    print("   S-sizes:", res["R456_L012_S_sizes"])

    # 3. TWO R-sites + TWO L-sites degenerate (the minimum allowed by Lemma B).
    bl2 = build({4, 5}, {0, 1}, seed=13)
    assert bl2 is not None
    audit("R45_L01_degenerate", bl2, res)
    res["R45_L01_S_sizes"] = dict(
        R={j: len(X.S_R(bl2, j)) for j in R},
        L={i: len(X.S_L(bl2, i)) for i in L})
    print("   S-sizes:", res["R45_L01_S_sizes"])

    # 4. EXPLICIT-POINT CONTROL: a generic (non-degenerate) block set must show
    #    NO collinear transversals at all -- the detector is not vacuous.
    bl0 = G.random_blocks(random.Random(999))
    audit("generic_control", bl0, res, full_H=False)

    json.dump(res, open(os.path.join(HERE, "results_witness.json"), "w"),
              indent=1, default=str)
    print("done")


if __name__ == "__main__":
    main()
