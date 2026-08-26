#!/usr/bin/env python3
"""W21-M1-TENSOR (B, mirror) -- the R-fixed reduction and the two-sided test.
UNAUDITED.  Exact only.

Mirror of the block reduction: fix a FULL-BOX R-word y (the X-box is full
for exactly y in {(1,2,0,0),(1,2,0,1),(2,2,0,0),(2,2,0,1)} in R-site order
4,5,6,7).  Then, whenever haf_R(y) != 0,
    Phi_(x,y) = haf_R(y) * haf_{K_4}( N^(y)(x) ),
    N^(y)_{(i,j)} = A_{ij} + (a^R_{sigma k, sigma l}(y)/haf_R(y))
                    * e_i^(y) (x) e_j^(y),
    e_i^(y) = COLUMN y_{sigma(i)} of the matching block A_{i,sigma(i)}
              (a vector indexed by the colour at the L-site i),
    {k,l} = {0,1,2,3} - {i,j},  sigma = 0->7, 1->4, 2->5, 3->6.
The slots of this K_4 are the L-sites themselves.

THE TWO-SIDED TEST measured here: at every exact clean point, does at least
one of the two reductions (L-fixed / R-fixed) exhibit a factoring reduced
site?  Equivalently, is the Case-A loophole ever open on BOTH sides at once?
"""
import json
import os
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PAR = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, PAR)
import w21t_core as TT                                          # noqa: E402
import w21_core as K                                            # noqa: E402
import w21_block as B                                           # noqa: E402
from w21t_apply import SLOT, to_tensor, load_points             # noqa: E402

RSING = {}
for (i, j), (a, b) in {(0, 4): (0, 0), (0, 5): (0, 1), (0, 6): (0, 2),
                       (1, 5): (1, 0), (1, 6): (1, 1), (1, 7): (0, 2),
                       (2, 4): (1, 0), (2, 6): (2, 1), (2, 7): (1, 2),
                       (3, 4): (2, 0), (3, 5): (2, 1),
                       (3, 7): (2, 2)}.items():
    RSING[(i, j)] = (a, b)


def xbox(y):
    """X_i(y) for i in L; y indexed by R-site order 4,5,6,7."""
    out = {i: set(range(3)) for i in B.L}
    for (i, j), (a, b) in RSING.items():
        if y[j - 4] == b:
            out[i].discard(a)
    return out


def full_box_R():
    return [y for y in product(range(3), repeat=4)
            if all(len(v) == 3 for v in xbox(y).values())]


def hafR_full(bl, gam, y):
    return B.hafR(bl, gam, y)


def N_of(bl, gam, y, i, j, P):
    """the mirror block N^(y)_{(i,j)} (row index = L-site i)."""
    e = (min(i, j), max(i, j))
    Ap = [[bl[e][r][s] for s in range(3)] for r in range(3)]
    k, l = [z for z in B.L if z not in (i, j)]
    a, b = B.SIG[k], B.SIG[l]
    er = (min(a, b), max(a, b))
    if er in set(gam):
        coef = bl[er][y[er[0] - 4]][y[er[1] - 4]]
    else:
        coef = Fraction(0)
    g = coef / P
    ei = [bl[(i, B.SIG[i])][r][y[B.SIG[i] - 4]] for r in range(3)]
    ej = [bl[(j, B.SIG[j])][r][y[B.SIG[j] - 4]] for r in range(3)]
    return [[Ap[r][s] + g * ei[r] * ej[s] for s in range(3)] for r in range(3)]


def main():
    res = {"_header": "UNAUDITED W21-M1-TENSOR mirror reduction. Exact."}
    fbL = B.full_box_words()
    fbR = full_box_R()
    print("full-box R words:", fbR)
    res["full_box_R_words"] = [list(y) for y in fbR]
    pts = load_points()
    for m in (26, 27, 28):
        T = K.W8_IMMUNE[m]
        gam = K.gamma_edges(T)
        clean = K.clean_words(T)
        rows = []
        print("=== m = %d ===" % m)
        for tag, bl in pts.get(m, []):
            orig = [t for t in range(8) if K.factors_at(bl, gam, t)]
            # L-fixed reduction
            Lfac = {}
            for x in fbL:
                P = B.hafL(bl, x)
                if P == 0:
                    continue
                MT = to_tensor({(i, j): B.M_of(bl, gam, x, i, j, P)
                                for (i, j) in B.LPAIRS})
                Lfac[x] = ([B.SIG[s - 1] for s in TT.any_site_factors(MT)],
                           sum(1 for p in TT.PAIRS if TT.rank(MT[p]) == 2))
            # R-fixed (mirror) reduction
            Rfac = {}
            for y in fbR:
                P = hafR_full(bl, gam, y)
                if P == 0:
                    continue
                NT = {(SLOT[i], SLOT[j]): N_of(bl, gam, y, i, j, P)
                      for (i, j) in B.LPAIRS}
                ok = all(TT.haf_value(NT, xx) == 0
                         for xx in product(range(3), repeat=4))
                Rfac[y] = ([s - 1 for s in TT.any_site_factors(NT)],
                           sum(1 for p in TT.PAIRS if TT.rank(NT[p]) == 2), ok)
            allL = sorted({s for v in Lfac.values() for s in v[0]})
            allR = sorted({s for v in Rfac.values() for s in v[0]})
            idok = all(v[2] for v in Rfac.values())
            print("  %-28s original=%s | L-reduction factoring R-sites=%s "
                  "(#rank2 %s) | R-reduction factoring L-sites=%s (#rank2 %s)"
                  " | mirror identity holds=%s"
                  % (tag, orig, allL, sorted({v[1] for v in Lfac.values()}),
                     allR, sorted({v[1] for v in Rfac.values()}), idok))
            rows.append(dict(tag=tag, original=orig, L_sides=allL,
                             R_sides=allR,
                             mirror_identity_holds=idok,
                             union_nonempty=bool(allL or allR),
                             union_subset_of_original=set(allL + allR)
                             <= set(orig)))
        res["m%d" % m] = rows
    json.dump(res, open(os.path.join(HERE, "results_mirror.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
