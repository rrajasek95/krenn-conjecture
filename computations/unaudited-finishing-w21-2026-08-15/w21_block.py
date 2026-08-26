#!/usr/bin/env python3
"""W21 MOVE 1 -- THE BLOCK / SCHUR REDUCTION at m = 26, 27, 28.
UNAUDITED.  Exact rational arithmetic only.

THEOREM W21-B1 (the clean set is a forbidden-pair set) [verified exactly,
0/6558 mismatches at m = 26, 27, 28].
At m = 26, 27, 28 the template splits as L = {0,1,2,3}, R = {4,5,6,7} with
  * Gamma|_L = K_4  (all six blocks FULL),
  * Gamma|_R = C_4 (m=26) / K_4 - e (m=27) / K_4 (m=28),
  * the four cross Gamma edges form the PERFECT MATCHING
        0-7, 1-4, 2-5, 3-6,
  * the remaining twelve cross blocks are SINGLE cells:
        (0,4):(0,0) (0,5):(0,1) (0,6):(0,2)
        (1,5):(1,0) (1,6):(1,1) (1,7):(0,2)
        (2,4):(1,0) (2,6):(2,1) (2,7):(1,2)
        (3,4):(2,0) (3,5):(2,1) (3,7):(2,2)
A word (x,y) (x on L, y on R) is CLEAN iff it avoids all twelve forbidden
pairs, i.e. for each single (i,j) with cell (alpha,beta), NOT
(x_i = alpha and y_j = beta).  [Every single extends to a supported matching,
so the condition is also necessary.]  Consequently the clean set is the same
at m = 26, 27, 28 and, for a fixed x, the admissible y form a PRODUCT BOX
Y(x) = prod_j Y_j(x).  Exactly FOUR L-words have a FULL box:
    x in {(1,2,0,0), (1,2,0,1), (2,2,0,0), (2,2,0,1)},
and by the mirror computation exactly four R-words have a full X-box:
    y in {(1,2,0,0), (1,2,0,1), (2,2,0,0), (2,2,0,1)}  (in the order 4,5,6,7).

THEOREM W21-B2 (the Schur / block reduction) [proved; verified exactly].
Write a^L_{ij} = A_{ij}[x_i][x_j] (i<j in L), a^R_{jk} = A_{jk}[y_j][y_k],
d_i = A_{i sigma(i)}[x_i][y_sigma(i)] with sigma = (0->7, 1->4, 2->5, 3->6).
Splitting the perfect matchings of Gamma by how many of the four matching
edges they use (0, 2 or 4) gives, EXACTLY,

  Phi_(x,y) = haf_L(x) haf_R(y)
              + sum_{i<j in L} a^L_{ij} a^R_{sigma i sigma j} d_k d_l
              + d_0 d_1 d_2 d_3            ({k,l} = L - {i,j})

and, whenever haf_L(x) != 0, this equals haf_L(x) * haf_{K_4}(M^(x)(y)) with

  M^(x)_{sigma i sigma j} = A_{sigma i sigma j} + (a^L_{kl}(x)/haf_L(x))
                            * c_i^(x) (x) c_j^(x),
  c_i^(x) = row x_i of the matching block A_{i sigma(i)}   (a vector in C^3
                                                            indexed by y).

So for each of the FOUR full-box L-words x with haf_L(x) != 0 the clean
layer forces the IDENTICALLY-VANISHING K_4 HAFNIAN

    M_{45} (x) M_{67} + M_{46} (x) M_{57} + M_{47} (x) M_{56} = 0
    in (C^3)^{(x)4}  --  all 81 words y, constants included.

At m = 26 two of the six M's have NO A-part (the R-edges (4,6) and (5,7)
are absent), so M_{46} and M_{57} are RANK <= 1 outright; at m = 27 one is.
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
import w21_core as K                                            # noqa: E402
from w21_pf import load_w20_points                              # noqa: E402

L = (0, 1, 2, 3)
R = (4, 5, 6, 7)
SIG = {0: 7, 1: 4, 2: 5, 3: 6}
LPAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIRINGS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
SINGLES = {(0, 4): (0, 0), (0, 5): (0, 1), (0, 6): (0, 2),
           (1, 5): (1, 0), (1, 6): (1, 1), (1, 7): (0, 2),
           (2, 4): (1, 0), (2, 6): (2, 1), (2, 7): (1, 2),
           (3, 4): (2, 0), (3, 5): (2, 1), (3, 7): (2, 2)}


def box(x):
    """Y_j(x) for j in R, as a dict."""
    out = {j: set(range(3)) for j in R}
    for (i, j), (a, b) in SINGLES.items():
        if x[i] == a:
            out[j].discard(b)
    return out


def full_box_words():
    return [x for x in product(range(3), repeat=4)
            if all(len(v) == 3 for v in box(x).values())]


def hafL(bl, x):
    return sum(bl[(i, j)][x[i]][x[j]] * bl[(k, l)][x[k]][x[l]]
               for (i, j), (k, l) in PAIRINGS)


def hafR(bl, gam, y):
    ES = set(gam)
    t = Fraction(0)
    for (i, j), (k, l) in PAIRINGS:
        e1 = (SIG[i], SIG[j]) if SIG[i] < SIG[j] else (SIG[j], SIG[i])
        e2 = (SIG[k], SIG[l]) if SIG[k] < SIG[l] else (SIG[l], SIG[k])
        if e1 in ES and e2 in ES:
            t += (bl[e1][y[e1[0] - 4]][y[e1[1] - 4]]
                  * bl[e2][y[e2[0] - 4]][y[e2[1] - 4]])
    return t


def Mmat(bl, gam, x, i, j):
    """M^(x)_{sigma i, sigma j} as a 3x3 matrix in (y_{sigma i}, y_{sigma j}),
    NOT divided by haf_L: returns (Apart, coefficient, c_i, c_j) so callers
    can form haf_L * M or M itself."""
    a, b = SIG[i], SIG[j]
    e = (min(a, b), max(a, b))
    if e in set(gam):
        Ap = [[bl[e][r][s] if e[0] == a else bl[e][s][r] for s in range(3)]
              for r in range(3)]
    else:
        Ap = [[Fraction(0)] * 3 for _ in range(3)]
    k, l = [z for z in L if z not in (i, j)]
    coef = bl[(min(k, l), max(k, l))][x[k]][x[l]]
    ci = [bl[(i, SIG[i])][x[i]][d] for d in range(3)]
    cj = [bl[(j, SIG[j])][x[j]][d] for d in range(3)]
    return Ap, coef, ci, cj


def M_of(bl, gam, x, i, j, P):
    Ap, coef, ci, cj = Mmat(bl, gam, x, i, j)
    g = coef / P
    return [[Ap[r][s] + g * ci[r] * cj[s] for s in range(3)] for r in range(3)]


def hafK4_M(Ms, y):
    """M's keyed by the L-pair (i,j); y indexed by R-site order 4,5,6,7."""
    t = Fraction(0)
    for (i, j), (k, l) in PAIRINGS:
        t += (Ms[(i, j)][y[SIG[i] - 4]][y[SIG[j] - 4]]
              * Ms[(k, l)][y[SIG[k] - 4]][y[SIG[l] - 4]])
    return t


def main():
    res = {"_header": "UNAUDITED W21 block/Schur reduction (move 1). Exact."}
    fb = full_box_words()
    res["full_box_L_words"] = [list(x) for x in fb]
    print("full-box L words:", fb)
    rng = random.Random(4242)
    pts = load_w20_points()
    for m in (26, 27, 28):
        T = K.W8_IMMUNE[m]
        gam = K.gamma_edges(T)
        clean = K.clean_words(T)
        entry = {}
        # (1) the expansion identity, at RANDOM exact points (an identity)
        bad = 0
        for _ in range(3):
            bl = {e: [[Fraction(rng.randint(-9, 9) or 5, rng.randint(1, 4))
                       for _ in range(3)] for _ in range(3)] for e in gam}
            for _k in range(60):
                w = tuple(rng.randrange(3) for _ in range(8))
                x, y = w[:4], w[4:]
                d = {i: bl[(i, SIG[i])][x[i]][y[SIG[i] - 4]] for i in L}
                tot = hafL(bl, x) * hafR(bl, gam, y)
                for (i, j) in LPAIRS:
                    a, b = SIG[i], SIG[j]
                    e = (min(a, b), max(a, b))
                    if e not in set(gam):
                        continue
                    kk, ll = [z for z in L if z not in (i, j)]
                    tot += (bl[(i, j)][x[i]][x[j]]
                            * (bl[e][y[e[0] - 4]][y[e[1] - 4]])
                            * d[kk] * d[ll])
                tot += d[0] * d[1] * d[2] * d[3]
                if tot != K.phi_value(bl, gam, w):
                    bad += 1
        entry["expansion_mismatches"] = bad
        print("m=%d  block expansion: %d mismatches / 180" % (m, bad))

        # (2) at the exact clean points: the K_4 tensor identity at full-box x
        pt = []
        for tag, bl in pts[m][:1]:
            assert all(K.phi_value(bl, gam, w) == 0 for w in clean)
            rows = []
            for x in fb:
                P = hafL(bl, x)
                if P == 0:
                    rows.append(dict(x=list(x), hafL=0, note="hafL vanishes"))
                    continue
                Ms = {(i, j): M_of(bl, gam, x, i, j, P) for (i, j) in LPAIRS}
                nz = sum(1 for y in product(range(3), repeat=4)
                         if hafK4_M(Ms, y) != 0)
                ranks = {str((SIG[i], SIG[j])): K.rank_of(Ms[(i, j)], 3)
                         for (i, j) in LPAIRS}
                rows.append(dict(x=list(x), hafL=str(P),
                                 nonvanishing_of_81=nz, M_ranks=ranks))
                print("   m=%d %s x=%s: hafL!=0, K_4 tensor identity fails on "
                      "%d/81 words; rank M = %s"
                      % (m, tag, x, nz, sorted(ranks.items())))
            pt.append(dict(tag=tag, full_box=rows))
        entry["points"] = pt
        res["m%d" % m] = entry

    # MUTATION CONTROL: perturb one block at a clean point; the tensor
    # identity must then FAIL somewhere.
    T = K.W8_IMMUNE[28]
    gam = K.gamma_edges(T)
    tag, bl = pts[28][0]
    bad = {e: [r[:] for r in bl[e]] for e in gam}
    bad[(4, 5)][0][0] = bad[(4, 5)][0][0] + 1
    fails = []
    for x in fb:
        P = hafL(bad, x)
        if P == 0:
            continue
        Ms = {(i, j): M_of(bad, gam, x, i, j, P) for (i, j) in LPAIRS}
        fails.append(sum(1 for y in product(range(3), repeat=4)
                         if hafK4_M(Ms, y) != 0))
    res["mutation_control_perturbed_45"] = fails
    print("MUTATION control (perturb block (4,5) at the m=28 clean point): "
          "tensor identity now fails on %s of 81 words per full-box x" % fails)
    json.dump(res, open(os.path.join(HERE, "results_block.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
