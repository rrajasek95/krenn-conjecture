#!/usr/bin/env python3
"""W21-M2-GEO step 4: THE COVERING COMBINATORICS.  UNAUDITED.  Exact.

Three covering questions, kept strictly apart:

 (Q0)  W20's number.  Minimum number of product boxes CONTAINED IN the L-free
       set needed to cover it (expect 9, +9 mirror).
       *** The containment hypothesis is NOT justified by any equation: a line
       of the arrangement at R-site j may carry a collinear transversal at a
       NON-L-free word -- nothing forbids it.  So 9 is NOT a lower bound. ***

 (Q1)  The honest question.  A line ell of the 12-point arrangement at R-site j
       contributes the box prod_i K_i(ell).  Two DISTINCT lines meet in at most
       one point of P^2, so for two boxes of the same site
              sum_i |K_i(ell) cap K_i(ell')|  <=  1                    (*)
       (12 points pairwise distinct; coincidences = separate stratum).
       QUESTION: can a family obeying (*) cover the 30 L-free words WITHOUT
       being the single full box (= all 12 points of the site collinear)?

 (Q2)  Codimension budget.  A line carrying k of the 12 points costs k-2.
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import m2geo as X                                                   # noqa: E402

SUBS = [frozenset(s) for k in (1, 2, 3) for s in combinations(range(3), k)]
BOXES = [tuple(Z) for Z in product(SUBS, repeat=4)]
LF = frozenset(X.LFREE)
RF = frozenset(X.RFREE)
WORDS_OF = {Z: frozenset(product(*[sorted(k) for k in Z])) for Z in BOXES}
SIZE_OF = {Z: sum(len(k) for k in Z) for Z in BOXES}

# capacity(c) = the largest number of words a box of codim cost c can hold
CAP = {}
for Z in BOXES:
    c = SIZE_OF[Z] - 2
    CAP[c] = max(CAP.get(c, 0), len(WORDS_OF[Z]))
MAXC = max(CAP)


_G = [0] + [10 ** 6] * 200
for _k in range(1, 201):
    for _c, _cap in CAP.items():
        _G[_k] = min(_G[_k], _c + _G[max(0, _k - _cap)])


def cost_lb(m):
    """memoised DP lower bound: cheapest cost that can cover m words."""
    return _G[m]


def _search(target, allowed, key, bound):
    """generic exact branch and bound; key(Z) = cost, bound(rem) = lower bound
    on the remaining cost.  Returns (best, example)."""
    tgt = frozenset(target)
    cand = [(Z, WORDS_OF[Z] & tgt, key(Z)) for Z in allowed]
    cand = [c for c in cand if c[1]]
    cover_of = {w: [c for c in cand if w in c[1]] for w in tgt}
    best = [10 ** 6, None]

    def rec(rem, cost, chosen):
        if cost + bound(len(rem)) >= best[0]:
            return
        if not rem:
            best[0], best[1] = cost, list(chosen)
            return
        w0 = min(rem, key=lambda w: len(cover_of[w]))
        for Z, ws, c in sorted(cover_of[w0], key=lambda t: (t[2], -len(t[1]))):
            chosen.append(Z)
            rec(rem - ws, cost + c, chosen)
            chosen.pop()
    rec(tgt, 0, [])
    return best


def min_cover(target, allowed):
    mx = max((len(WORDS_OF[Z] & frozenset(target)) for Z in allowed), default=1)
    return _search(target, allowed, lambda Z: 1,
                   lambda m: (m + mx - 1) // mx)


def min_cost_cover(target, allowed):
    return _search(target, allowed, lambda Z: SIZE_OF[Z] - 2, cost_lb)


def compatible(Z, Z2):
    return sum(len(Z[i] & Z2[i]) for i in range(4)) <= 1


def q1_search(target, stop_at=None):
    """exhaustive: every family of >= 2 pairwise-(*)-compatible boxes; does any
    cover `target`?  Also returns the best partial coverage."""
    tgt = frozenset(target)
    # in a family of size >= 2 no box may have two full groups
    cand = [Z for Z in BOXES
            if (WORDS_OF[Z] & tgt) and sum(1 for k in Z if len(k) == 3) <= 1]
    cover_of = {w: [Z for Z in cand if w in WORDS_OF[Z]] for w in tgt}
    found, bestcov = [], [0, None]
    nodes = [0]

    def rec(rem, fam):
        nodes[0] += 1
        cov = len(tgt) - len(rem)
        if cov > bestcov[0]:
            bestcov[0], bestcov[1] = cov, list(fam)
        if not rem:
            found.append(list(fam))
            return
        if stop_at is not None and len(found) >= stop_at:
            return
        w0 = min(rem, key=lambda w: len(cover_of[w]))
        for Z in cover_of[w0]:
            if all(compatible(Z, Y) for Y in fam):
                fam.append(Z)
                rec(rem - WORDS_OF[Z], fam)
                fam.pop()
    rec(tgt, [])
    return found, bestcov, nodes[0]


def main():
    res = {"_header": "UNAUDITED W21-M2-GEO covering combinatorics, exact."}

    inside_L = [Z for Z in BOXES if WORDS_OF[Z] <= LF]
    inside_R = [Z for Z in BOXES if WORDS_OF[Z] <= RF]
    nL, exL = min_cover(LF, inside_L)
    nR, exR = min_cover(RF, inside_R)
    print("Q0  boxes inside L-free %d ; min cover = %d boxes   (W20 says 9)"
          % (len(inside_L), nL), flush=True)
    print("Q0  boxes inside R-free %d ; min cover = %d boxes" % (len(inside_R),
                                                                 nR),
          flush=True)
    cL, _ = min_cost_cover(LF, inside_L)
    print("Q0  min codim COST of such a cover = %d" % cL, flush=True)
    res.update(Q0_boxes_inside_Lfree=len(inside_L),
               Q0_min_cover_inside_Lfree=nL, Q0_min_cover_inside_Rfree=nR,
               Q0_min_cost_inside_Lfree=cL,
               Q0_example_cover_L=[[sorted(k) for k in Z] for Z in exL])

    n2, ex2 = min_cover(LF, BOXES)
    c2, ex2c = min_cost_cover(LF, BOXES)
    print("Q2  unrestricted boxes: min cover = %d box(es) %s"
          % (n2, [[sorted(k) for k in Z] for Z in ex2]), flush=True)
    print("Q2  unrestricted boxes: min codim COST = %d, example %s"
          % (c2, [[sorted(k) for k in Z] for Z in ex2c]), flush=True)
    res.update(Q2_min_cover_unrestricted=n2, Q2_min_cost_unrestricted=c2,
               Q2_min_cost_example=[[sorted(k) for k in Z] for Z in ex2c])

    fam, bestcov, nodes = q1_search(LF)
    print("Q1  (*)-compatible families of >=2 boxes covering all 30 L-free "
          "words: %d   [%d search nodes]" % (len(fam), nodes), flush=True)
    print("Q1  best partial coverage by such a family: %d/30  %s"
          % (bestcov[0], [[sorted(k) for k in Z] for Z in (bestcov[1] or [])]),
          flush=True)
    famR, bestcovR, nodesR = q1_search(RF)
    print("Q1  mirror: %d families ; best partial %d/30"
          % (len(famR), bestcovR[0]), flush=True)
    res.update(Q1_families_found=len(fam), Q1_best_partial=bestcov[0],
               Q1_best_family=[[sorted(k) for k in Z]
                               for Z in (bestcov[1] or [])],
               Q1_nodes=nodes, Q1_mirror_families=len(famR),
               Q1_mirror_best_partial=bestcovR[0])

    # MUTATION CONTROL: drop (*) and the same search must succeed.
    global compatible
    old = compatible
    compatible = lambda a, b: True                                  # noqa: E731
    famM, bestM, nodesM = q1_search(LF, stop_at=1)
    compatible = old
    print("Q1  MUTATION control ((*) dropped): %d families found (want > 0)"
          % len(famM), flush=True)
    res["Q1_mutation_families"] = len(famM)

    json.dump(res, open(os.path.join(HERE, "results_cover.json"), "w"),
              indent=1, default=str)
    print("done")


if __name__ == "__main__":
    main()
