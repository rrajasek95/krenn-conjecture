#!/usr/bin/env python3
"""W20 -- RESIDUAL 2: the derived RANK conditions on the C_8 member, and the
covering arithmetic they impose.  UNAUDITED.  Exact integer arithmetic only.

INPUT (proved in w20_c8.py, 0 mismatches on 2430 + 2430 words):
  * x L-free  =>  H_(x,y) = per B(x,y) for ALL y;
  * y R-free  =>  H_(x,y) = per B(x,y) for ALL x.

CONSEQUENCE (Lemma W20-P, verified in w20_perlemma.py):
 (L) for every L-free x, the four column spans V_j^x < C^4 (j in R) cannot
     all be hyperplanes -- otherwise they would all equal one coordinate
     hyperplane {v_r = 0}, i.e. the whole row x_r of ALL FOUR blocks
     A_{r,j} (j in R) would vanish, impossible since every cross block has
     at most one dead cell.  So SOME 4x3 matrix
        M_j^x = [ A_{i,j}[x_i][d] ]_{i in L, d}      has rank <= 2,
     equivalently there is mu != 0 with (A_{i,j} mu)[x_i] = 0 for all i in L.
 (L+) if moreover x has NO dead cell (all 48 entries nonzero) then at most
     TWO of the V_j^x are hyperplanes (Lemma W20-P4c), so at least TWO of the
     M_j^x have rank <= 2.
 (R), (R+) the mirror statements, with
        N_i^y = [ A_{i,j}[s][y_j] ]_{s, j in R}       (3 x 4), rank <= 2,
     i.e. there is lambda != 0 with (lambda^T A_{i,j})[y_j] = 0 for all j.

The covered set of an R-site j is a UNION OF PRODUCT BOXES prod_i Z_i(mu),
Z_i(mu) = { r : mu . (row r of A_{i,j}) = 0 }: this module computes the
maximal boxes inside the L-free set, hence the covering arithmetic.
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
from w20_c8 import LFREE, RFREE, LS, RS, L, R, T, cross_mask     # noqa: E402
from w20_perlemma import per                                     # noqa: E402


def dead_free_L(x):
    """no dead cell among the 48 entries A_{i,j}[x_i][d]."""
    for a, i in enumerate(L):
        for j in R:
            for d in range(3):
                if not (cross_mask(i, j) >> (3 * x[a] + d)) & 1:
                    return False
    return True


def dead_free_R(y):
    for b, j in enumerate(R):
        for i in L:
            for s in range(3):
                if not (cross_mask(i, j) >> (3 * s + y[b])) & 1:
                    return False
    return True


# --------------------------------------------------- boxes in the free sets
def boxes_in(freeset, side_singles, side):
    """all maximal product boxes prod Z_i contained in the free set."""
    fs = set(freeset)
    subsets = [tuple(s) for k in range(1, 4)
               for s in product(*[[()]]) ] if False else None
    allZ = [tuple(z) for z in product(*[[(0,), (1,), (2,), (0, 1), (0, 2),
                                        (1, 2), (0, 1, 2)]] * 1)]
    opts = [(0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]
    good = []
    for Z in product(opts, repeat=4):
        ok = True
        for z in product(*Z):
            if z not in fs:
                ok = False
                break
        if ok:
            good.append(Z)
    # maximal ones
    maximal = []
    for Z in good:
        if not any(Z != Z2 and all(set(Z[i]) <= set(Z2[i]) for i in range(4))
                   for Z2 in good):
            maximal.append(Z)
    return good, maximal


def min_box_cover(freeset, boxes):
    """greedy + exact lower bound on the number of boxes needed."""
    fs = set(freeset)
    best = None
    # exact minimum by simple branch and bound (small instance)
    bx = [set(product(*Z)) & fs for Z in boxes]
    bx = [b for b in bx if b]
    order = sorted(range(len(bx)), key=lambda i: -len(bx[i]))
    bestn = [len(fs)]

    def rec(rem, used):
        if not rem:
            bestn[0] = min(bestn[0], used)
            return
        if used + (len(rem) + max(len(b) for b in bx) - 1) \
                // max(len(b) for b in bx) >= bestn[0]:
            return
        w = next(iter(rem))
        for i in order:
            if w in bx[i]:
                rec(rem - bx[i], used + 1)

    rec(frozenset(fs), 0)
    return bestn[0]


# ------------------------------------------- Lemma W20-P4c (three planes) --
def check_P4c(trials=3000, seed=11):
    """three hyperplanes + one vector with all coordinates nonzero:
    per(u, v, w, z) must NOT vanish identically."""
    import random
    from w20_perlemma import kernel_basis_vec
    rng = random.Random(seed)
    bad = 0
    tested = 0
    for _ in range(trials):
        u = [rng.randint(-5, 5) or 3 for _ in range(4)]
        ns = [tuple(rng.randint(-4, 4) for _ in range(4)) for _ in range(3)]
        if not all(any(nv) for nv in ns):
            continue
        bases = [kernel_basis_vec(nv) for nv in ns]
        tested += 1
        van = True
        for idx in product(range(3), repeat=3):
            if per([u] + [bases[k][idx[k]] for k in range(3)]) != 0:
                van = False
                break
        if van:
            bad += 1
    # MUTATION CONTROL: if u has a zero coordinate the statement is false
    fires = 0
    for _ in range(400):
        u = [0] + [rng.randint(-5, 5) or 3 for _ in range(3)]
        ns = [(1, 0, 0, 0)] * 3
        bases = [kernel_basis_vec(nv) for nv in ns]
        van = all(per([u] + [bases[k][idx[k]] for k in range(3)]) == 0
                  for idx in product(range(3), repeat=3))
        fires += van
    return dict(trials=tested, vanishing_with_all_nonzero_u=bad,
                mutation_control_zero_coordinate_vanishes=fires)


def main():
    res = {"_header": "UNAUDITED W20 residual-2 rank conditions. Exact only."}
    dfL = [x for x in LFREE if dead_free_L(x)]
    dfR = [y for y in RFREE if dead_free_R(y)]
    res["n_Lfree"] = len(LFREE)
    res["n_Rfree"] = len(RFREE)
    res["dead_free_Lfree"] = [list(x) for x in dfL]
    res["dead_free_Rfree"] = [list(y) for y in dfR]
    print("L-free words: %d, of which DEAD-CELL-FREE: %d  %s"
          % (len(LFREE), len(dfL), [list(x) for x in dfL]), flush=True)
    print("R-free words: %d, of which DEAD-CELL-FREE: %d  %s"
          % (len(RFREE), len(dfR), [list(y) for y in dfR]), flush=True)
    res["P4c_check"] = check_P4c()
    print("Lemma W20-P4c check:", res["P4c_check"], flush=True)
    good, maximal = boxes_in(LFREE, LS, L)
    res["n_boxes_in_Lfree"] = len(good)
    res["maximal_boxes_L"] = [[list(z) for z in Z] for Z in maximal]
    res["max_box_size_L"] = max(len(list(product(*Z))) for Z in good)
    print("product boxes inside the L-free set: %d (maximal: %d), largest "
          "box has %d words" % (len(good), len(maximal),
                                res["max_box_size_L"]), flush=True)
    mc = min_box_cover(LFREE, good)
    res["min_boxes_to_cover_Lfree"] = mc
    print("minimum number of boxes needed to cover the 30 L-free words: %d"
          % mc, flush=True)
    goodR, maximalR = boxes_in(RFREE, RS, R)
    res["max_box_size_R"] = max(len(list(product(*Z))) for Z in goodR)
    res["min_boxes_to_cover_Rfree"] = min_box_cover(RFREE, goodR)
    print("mirror: largest R-box %d words, minimum cover %d boxes"
          % (res["max_box_size_R"], res["min_boxes_to_cover_Rfree"]),
          flush=True)
    json.dump(res, open(os.path.join(HERE, "results_c8rank.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
