#!/usr/bin/env python3
"""W21-M2-SING: EXPLICIT exact rational points of known-feasible relaxations.

THE RANK-1 FAMILY.  Put  A_{i,j}[c][d] = K[i][j][c] * s[j][d].  Then for any
L-word x the matrix M_j^x (rows i, entries = row x_i of A_{i,j}) is the rank-1
matrix a^{(j),x} (x) s[j] with a^{(j),x}_i = K[i][j][x_i], hence

    per B(x,y) = (prod_j s[j][y_j]) * per(P^x),   P^x[i][j] = K[i][j][x_i],

so ALL 81 y-equations of the L-word x hold as soon as the single 4x4 scalar
permanent per(P^x) vanishes.  per is LINEAR in each row of P and row i of P^x
depends on x only through x_i, so a family of L-words that differ in a single
coordinate costs only one linear condition apiece.

This yields explicit ALL-NONZERO rational points for
  * the single-L-free-word system (81 equations), and
  * the two-dead-cell-free-word system (a) (162 equations),
which are exactly the known-feasible relaxations demanded by LEDGER 13(b).
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
import m2core as M
import m2sys as S
import w21_c8core as G

F = Fraction
ALLW = S.ALLW


def per4_scalar(P):
    return G.per4(P)


def rank1_point(kmap, smap):
    """kmap: dict (i,j,c) -> Fraction ; smap: dict (j,d) -> Fraction.
    Returns dict cell -> value for every cell whose (i,j,c) is in kmap."""
    val = {}
    for (i, j, c), k in kmap.items():
        for d in range(3):
            if M.occ(i, j, c, d):
                val[(i, j, c, d)] = k * smap[(j, d)]
    return val


def build_point(lwords, rows_value):
    """lwords: L-words to satisfy.  rows_value: dict (i,c) -> tuple over
    j=4..7 giving K[i][j][c].  Returns (val, checks)."""
    kmap = {}
    for (i, c), vec in rows_value.items():
        for k, j in enumerate(M.R):
            kmap[(i, j, c)] = F(vec[k])
    smap = {(j, d): F([1, 2, 3][d] + (j - 4)) for j in M.R for d in range(3)}
    val = rank1_point(kmap, smap)
    checks = []
    for x in lwords:
        P = [[kmap[(i, j, x[M.LPOS[i]])] for j in M.R] for i in M.L]
        checks.append((tuple(x), per4_scalar(P)))
    return val, checks


# ---------------------------------------------------------------- point P1
# rows i=0,1,2 of P all-ones  =>  every 3x3 all-ones minor has per = 6,
# so per(P^x) = 6 * sum_j K[3][j][x_3].
ROWS_A = {(0, 0): (1, 1, 1, 1),      # x_0 = 0   (used by x1 and x2)
          (1, 2): (1, 1, 1, 1),      # x_1 = 2
          (2, 1): (1, 1, 1, 1),      # x_2 = 1
          (3, 0): (1, 1, 1, -3),     # x_3 = 0   -> sum 0
          (3, 1): (1, 1, -3, 1)}     # x_3 = 1   -> sum 0

X1 = (0, 2, 1, 0)
X2 = (0, 2, 1, 1)


def report(tag, val, eqs, cells, labels):
    nz = [c for c in cells if val.get(c, F(0)) == 0]
    bad = [lb for p, lb in zip(eqs, labels) if M.p_eval(p, val) != 0]
    miss = [c for c in cells if c not in val]
    print("  %-28s cells=%3d  missing=%d  zero-cells=%d  "
          "violated eqs=%d / %d" % (tag, len(cells), len(miss), len(nz),
                                    len(bad), len(eqs)))
    return {"cells": len(cells), "missing": len(miss), "zero_cells": len(nz),
            "violated": len(bad), "neqs": len(eqs),
            "violated_examples": bad[:5]}


if __name__ == "__main__":
    out = {"_header": "UNAUDITED W21-M2-SING explicit feasible points"}
    print("EXPLICIT EXACT RATIONAL POINTS (rank-1 family)")

    val, checks = build_point([X1, X2], ROWS_A)
    print("  per(P^x) values:", [(x, str(v)) for x, v in checks])
    out["perP"] = {''.join(map(str, x)): str(v) for x, v in checks}

    e1, c1, l1 = S.sys_words(lwords=[X1])
    out["P1_single_x1"] = report("single word x1", val, e1, c1, l1)
    e2, c2, l2 = S.sys_words(lwords=[X2])
    out["P1_single_x2"] = report("single word x2", val, e2, c2, l2)
    ea, ca, la = S.sys_words(lwords=[X1, X2])
    out["P1_system_a"] = report("system (a): x1 & x2", val, ea, ca, la)

    # gauge the point onto the slice used by the Singular driver and re-check
    tree, free, nn, nc = S.gauge_fix(ca)
    lam, mu = M.gauge_to_slice({c: val[c] for c in ca}, tree)
    val2 = M.gauge_apply({c: val[c] for c in ca}, lam, mu)
    eqs_g = S.substitute(ea, set(tree))
    bad = sum(1 for p in eqs_g if M.p_eval(p, val2) != 0)
    onez = all(val2[c] == 1 for c in tree)
    nzall = all(v != 0 for v in val2.values())
    print("  gauged onto the slice: tree cells all 1 = %s, all-nonzero = %s, "
          "violated gauge-fixed eqs = %d / %d" % (onez, nzall, bad,
                                                  len(eqs_g)))
    out["P1_gauged"] = {"tree_all_one": bool(onez), "all_nonzero": bool(nzall),
                        "violated": bad, "neqs": len(eqs_g),
                        "ngauge": len(tree), "nfree": len(free)}

    # MUTATION CONTROL on the point checker: break one K entry, expect failures
    ROWS_BAD = dict(ROWS_A)
    ROWS_BAD[(3, 0)] = (1, 1, 1, -2)          # sum = 1 != 0
    valb, checksb = build_point([X1, X2], ROWS_BAD)
    badcnt = sum(1 for p in ea if M.p_eval(p, valb) != 0)
    print("  MUTATION (broken K row): violated eqs = %d / %d (want > 0)"
          % (badcnt, len(ea)))
    out["P1_mutation_violated"] = badcnt

    json.dump(out, open("results_points.json", "w"), indent=1, default=str)
