#!/usr/bin/env python3
"""W20 -- RESIDUAL 2: the empty-clean-layer stratum, via W19's explicit
C_8-Gamma member.  UNAUDITED.  Exact arithmetic only.

THE TEMPLATE (re-audited in w20_controls.py):  L = {0,1,2,3}, R = {4,5,6,7};
all 16 L-R blocks are occupied (8 FULL -- the Hamilton cycle Gamma -- and 8
FAT, each missing exactly one cell); inside L and inside R the six blocks
each carry ONE diagonal cell, following the proper 3-edge-colouring of K_4
(edge class r  ->  cell (r,r)).

THE L-FREE REDUCTION (this probe).  A perfect matching of K_8 uses 4, 2 or 0
cross (L-R) edges; the 2-cross and 0-cross ones consume at least one L-single
and at least one R-single.  An L-single on edge {k,l} of colour class r is
occupied at w only if w_k = w_l = r.  So call an L-word x L-FREE when no
L-single is active (no k<l in L with x_k = x_l = colour class of kl).  Then
for EVERY y,

        H_(x,y)  =  per B(x,y),        B(x,y)[i][j] = A_{i,j}[x_i][y_j]

(the 4 x 4 cross matrix, dead cells = 0), because only the 24 four-cross
matchings survive -- and those are exactly the 24 permutations L -> R.

Since per is multilinear in the COLUMNS of B and column j depends only on
y_j, the exact-source equations for a fixed L-free x say precisely:

    per vanishes identically on  V_4^x x V_5^x x V_6^x x V_7^x,
    V_j^x = span{ c_j^x(0), c_j^x(1), c_j^x(2) } < C^4,
    c_j^x(d)[i] = A_{i,j}[x_i][d].

Mirror statement with L and R exchanged for R-free y.
"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from itertools import permutations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w20_core as C                                            # noqa: E402

T = C.C8_MEMBER
L = (0, 1, 2, 3)
R = (4, 5, 6, 7)


def singles(T, side):
    """the one-cell blocks inside `side`, as {edge: (i,j)}."""
    out = {}
    for ei, (u, v) in enumerate(C.EDGES):
        if u in side and v in side and C.block_class(T[ei]) == "single":
            out[(u, v)] = C.cells_of(T[ei])[0]
    return out


LS = singles(T, L)
RS = singles(T, R)


def free_words(side, sing):
    """words on `side` activating NO single of that side."""
    out = []
    for z in product(range(3), repeat=4):
        pos = {s: k for k, s in enumerate(side)}
        ok = True
        for (u, v), (i, j) in sing.items():
            if z[pos[u]] == i and z[pos[v]] == j:
                ok = False
                break
        if ok:
            out.append(z)
    return out


LFREE = free_words(L, LS)
RFREE = free_words(R, RS)


def cross_mask(i, j):
    return T[C.EIDX[(i, j)]]


def Bmat(x, y):
    """the 4x4 cross matrix as a template-masked symbol table (i, j, cell)."""
    out = []
    for a, i in enumerate(L):
        row = []
        for b, j in enumerate(R):
            c = 3 * x[a] + y[b]
            row.append((i, j, x[a], y[b]) if (cross_mask(i, j) >> c) & 1
                       else None)
        out.append(row)
    return out


def per_terms(x, y):
    """the surviving permutation terms of per B(x,y)."""
    B = Bmat(x, y)
    out = []
    for p in permutations(range(4)):
        t = [B[a][p[a]] for a in range(4)]
        if all(t):
            out.append(t)
    return out


def check_Lfree_identity():
    """for every L-free x and EVERY y: support(T, (x,y)) = the 4-cross
    matchings, and they are exactly the surviving permutation terms."""
    bad = 0
    tested = 0
    for x in LFREE:
        for y in product(range(3), repeat=4):
            w = tuple(x) + tuple(y)
            sup = C.support(T, w)
            ncross = 0
            for mi in sup:
                m = C.PMS[mi]
                k = sum(1 for (u, v) in m if (u in L) != (v in L))
                if k != 4:
                    ncross += 1
            tested += 1
            if ncross:
                bad += 1
            if len(sup) != len(per_terms(x, y)):
                bad += 1
    return dict(n_Lfree=len(LFREE), tested=tested, mismatches=bad)


def check_Rfree_identity():
    bad = 0
    tested = 0
    for y in RFREE:
        for x in product(range(3), repeat=4):
            w = tuple(x) + tuple(y)
            sup = C.support(T, w)
            for mi in sup:
                m = C.PMS[mi]
                k = sum(1 for (u, v) in m if (u in L) != (v in L))
                if k != 4:
                    bad += 1
                    break
            tested += 1
    return dict(n_Rfree=len(RFREE), tested=tested, mismatches=bad)


def zero_pattern(x):
    """for L-free x: the 4x3 table of which c_j^x(d)[i] are dead cells."""
    out = {}
    for b, j in enumerate(R):
        cols = []
        for d in range(3):
            v = []
            for a, i in enumerate(L):
                c = 3 * x[a] + d
                v.append(1 if (cross_mask(i, j) >> c) & 1 else 0)
            cols.append(v)
        out[j] = cols
    return out


def main():
    res = {"_header": "UNAUDITED W20 residual 2: the C_8 member. Exact only."}
    res["L_singles"] = {str(k): list(v) for k, v in LS.items()}
    res["R_singles"] = {str(k): list(v) for k, v in RS.items()}
    res["n_Lfree"] = len(LFREE)
    res["n_Rfree"] = len(RFREE)
    res["Lfree_words"] = [list(x) for x in LFREE]
    res["Rfree_words"] = [list(y) for y in RFREE]
    print("L-singles:", res["L_singles"], flush=True)
    print("R-singles:", res["R_singles"], flush=True)
    print("L-free L-words: %d   R-free R-words: %d"
          % (len(LFREE), len(RFREE)), flush=True)
    res["Lfree_identity"] = check_Lfree_identity()
    print("L-free identity  H_w = per B(x,y)  for all y:",
          res["Lfree_identity"], flush=True)
    res["Rfree_identity"] = check_Rfree_identity()
    print("R-free identity:", res["Rfree_identity"], flush=True)
    # how many cross cells are dead in each column family
    zp = {}
    for x in LFREE:
        z = zero_pattern(x)
        nz = sum(1 for j in R for d in range(3) for i in range(4)
                 if z[j][d][i] == 0)
        zp[str(list(x))] = nz
    res["dead_cells_per_Lfree_word"] = zp
    print("dead cross cells per L-free word (histogram):", flush=True)
    from collections import Counter
    print("   ", Counter(zp.values()), flush=True)
    json.dump(res, open(os.path.join(HERE, "results_c8.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
