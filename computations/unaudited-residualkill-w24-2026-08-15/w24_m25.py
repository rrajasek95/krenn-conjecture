#!/usr/bin/env python3
"""W24 -- the m=25 SLOT-6 FACTORISATION and the resulting case split.
UNAUDITED.  Exact only.

LEMMA W24-E (m=25).  At m=25 the Gamma graph is K_4(L) u C_4(R) u
{(0,7),(1,4),(2,5)}: the matching edge (3,6) is ABSENT (so d_3 = 0) and the
R-edges (4,6) = r_13 and (5,7) = r_02 are absent.  Hence, EXACTLY,
    Phi(x,y) = A_56[y5][y6] * P  +  A_67[y6][y7] * Q,
    P = hafL(x) * A_47[y4][y7] + l_23 * A_07[x0][y7] * A_14[x1][y4],
    Q = hafL(x) * A_45[y4][y5] + l_03 * A_14[x1][y4] * A_25[x2][y5],
with l_ab = A_ab[x_a][x_b] and hafL = l_01 l_23 + l_02 l_13 + l_03 l_12.
NEITHER P NOR Q DEPENDS ON y6.

LEMMA W24-F (m=25).  c_(2,6)(w) = A_13[x1][x3] * A_07[x0][y7] * A_45[y4][y5]
-- a MONOMIAL in Gamma cells, hence nonzero whenever all Gamma cells are.

THEOREM W24-G (m=25, CASE 1).  Let x satisfy x0 != 0, x1 != 1, x2 = 2,
x3 != 2 (so (2,6) is the only live single that can fire at (x,.); its cell
is (2,1), i.e. it fires exactly at y6 = 1).  If for some (y5,y7)
     A_56[y5][0] * A_67[2][y7]  !=  A_56[y5][2] * A_67[0][y7],
then the two clean equations at y6 = 0 and y6 = 2 force P = Q = 0, and the
y6 = 1 row then reads  0 + c_(2,6) z = 0  with c_(2,6) != 0, so z = 0:
the cell (2,6) is forced to vanish and the point is KILLED.
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
import w24_core as C                                              # noqa: E402
import w24_pts as P25                                             # noqa: E402
import w24_ident as ID                                            # noqa: E402

M = 25
GAM = C.gamma_edges(C.TEMPLATES[M])
GS = set(GAM)
PAIRINGS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def hafL(bl, x):
    return sum(bl[(i, j)][x[i]][x[j]] * bl[(k, l)][x[k]][x[l]]
               for (i, j), (k, l) in PAIRINGS)


def PQ(bl, x, y):
    hl = hafL(bl, x)
    l23 = bl[(2, 3)][x[2]][x[3]]
    l03 = bl[(0, 3)][x[0]][x[3]]
    Pv = hl * bl[(4, 7)][y[0]][y[3]] + l23 * bl[(0, 7)][x[0]][y[3]] \
        * bl[(1, 4)][x[1]][y[0]]
    Qv = hl * bl[(4, 5)][y[0]][y[1]] + l03 * bl[(1, 4)][x[1]][y[0]] \
        * bl[(2, 5)][x[2]][y[1]]
    return Pv, Qv


def phi_fact(bl, x, y):
    Pv, Qv = PQ(bl, x, y)
    return bl[(5, 6)][y[1]][y[2]] * Pv + bl[(6, 7)][y[2]][y[3]] * Qv


def c26(bl, x, y):
    return (bl[(1, 3)][x[1]][x[3]] * bl[(0, 7)][x[0]][y[3]]
            * bl[(4, 5)][y[0]][y[1]])


def main():
    out = {"_header": "UNAUDITED W24 m=25 factorisation + case split."}
    rng = random.Random(2525)
    # ---- (1) the factorisation, at RANDOM exact points (it is an identity)
    bad = badc = 0
    for _ in range(6):
        bl = {e: [[Fraction(rng.randint(-9, 9) or 5, rng.randint(1, 4))
                   for _ in range(3)] for _ in range(3)] for e in GAM}
        for _k in range(200):
            w = tuple(rng.randrange(3) for _ in range(8))
            x, y = w[:4], w[4:]
            if phi_fact(bl, x, y) != C.phi(bl, GS, w):
                bad += 1
            if c26(bl, x, y) != ID.coeff(bl, GS, (2, 6), w):
                badc += 1
    print("LEMMA W24-E (Phi = A56*P + A67*Q): %d/1200 mismatches" % bad)
    print("LEMMA W24-F (c_(2,6) monomial):    %d/1200 mismatches" % badc)
    out["E_mismatches"], out["F_mismatches"] = bad, badc
    # mutation controls on the ASSERTED formulas (an identity cannot be
    # broken by moving the point; mutate the formula instead)
    mb = 0
    for _k in range(200):
        bl = {e: [[Fraction(rng.randint(-9, 9) or 5, rng.randint(1, 4))
                   for _ in range(3)] for _ in range(3)] for e in GAM}
        w = tuple(rng.randrange(3) for _ in range(8))
        x, y = w[:4], w[4:]
        Pv, Qv = PQ(bl, x, y)
        wrong = bl[(5, 6)][y[1]][y[2]] * Qv + bl[(6, 7)][y[2]][y[3]] * Pv
        mb += (wrong != C.phi(bl, GS, w))
    print("MUTATION control (P and Q swapped): fails %d/200 (want ~200)" % mb)
    out["E_mutation_fails"] = mb

    # ---- (2) the isolating x-words for (2,6) at m=25
    XS = [x for x in product(range(3), repeat=4)
          if x[0] != 0 and x[1] != 1 and x[2] == 2 and x[3] != 2]
    print("m=25 x-words isolating the single (2,6): %d -> %s" % (len(XS), XS))
    out["isolating_x"] = [list(x) for x in XS]
    # sanity: at these x, (2,6) is the only live single that can fire
    sing = C.single_edges(C.TEMPLATES[M])
    live = [e for e in sing
            if C.has_pm(GS, tuple(v for v in range(8) if v not in e))]
    okiso = all({e for e in live if x[e[0]] == sing[e][0]} == {(2, 6)}
                for x in XS)
    print("   isolation verified:", okiso)
    out["isolation_ok"] = okiso

    # ---- (3) which case do the actual clean points fall in?
    recs = []
    for m, tag, bl in P25.stored_points():
        if m != M:
            continue
    # stored points are 26..28 only; generate m=25 points with own descent
    got = 0
    n = 0
    while got < 10 and n < 400:
        n += 1
        rng2 = random.Random(25_000_000 + n)
        order = list(range(8))
        rng2.shuffle(order)
        bl, clean = P25.descent(M, rng2, order=order, passes=3)
        if bl is None:
            continue
        if any(C.phi(bl, GS, w) != 0 for w in clean):
            continue
        if not all(bl[e][i][j] != 0 for e in GAM
                   for i in range(3) for j in range(3)):
            continue
        got += 1
        det = [(y5, y7, bl[(5, 6)][y5][0] * bl[(6, 7)][2][y7]
                - bl[(5, 6)][y5][2] * bl[(6, 7)][0][y7])
               for y5 in range(3) for y7 in range(3)]
        case1 = [d for d in det if d[2] != 0]
        # verify the theorem's conclusion directly
        killed = None
        if case1:
            y5, y7, _ = case1[0]
            x = XS[0]
            y = (0, y5, 1, y7)
            Pv, Qv = PQ(bl, x, y)
            killed = (Pv == 0 and Qv == 0
                      and C.phi(bl, GS, tuple(x) + y) == 0
                      and c26(bl, x, y) != 0)
        v = ID.sub_verdict(M, bl, XS, [(2, 6)])
        recs.append(dict(tag="descent %d" % n, n_case1_pairs=len(case1),
                         case1_kill_verified=killed,
                         sub_killed=v["killed"], sub_forced=v["forced"],
                         sub_incons=v["inconsistent"]))
        print("m=25 pt %-3d  CASE-1 (y5,y7) pairs with nonzero det: %d/9 | "
              "case-1 kill verified: %s | (2,6) subsystem killed: %s %s"
              % (n, len(case1), killed, v["killed"],
                 v["forced"] or ("INCONS" if v["inconsistent"] else "")),
              flush=True)
    out["m25_points"] = recs
    json.dump(out, open(os.path.join(HERE, "results_m25.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
