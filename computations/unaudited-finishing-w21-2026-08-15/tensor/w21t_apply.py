#!/usr/bin/env python3
"""W21-M1-TENSOR (B) -- apply the classification at m = 26, 27, 28.
UNAUDITED.  Exact only.

For each full-box L-word x with haf_L(x) != 0 the clean layer forces the
identically-vanishing K_4 hafnian on
   M^(x)_{(i,j)} = A_{sigma i, sigma j} + (a^L_{kl}(x)/haf_L(x)) c_i (x) c_j
(slots = the L-indices 0,1,2,3; sigma = 0->7, 1->4, 2->5, 3->6).
The classification (all six nonzero, after GL_3^4 everything is 2x2):
   B0  all rank 1                 -> all four reduced sites factor
   B1  exactly one rank 2         -> the two reduced sites off that edge factor
   B2  exactly two rank 2         -> EMPTY
   B3s three rank 2, star         -> EMPTY
   B3t three rank 2, triangle     -> the fourth reduced site factors
   A   all six rank 2             -> NO reduced site factors (the symplectic
                                     orbit; realisable with all entries != 0)
m=26: the R-edges (4,6) and (5,7) are absent, i.e. the COMPLEMENTARY PAIR of
slot-pairs {(1,3),(0,2)} both have no A-part, so both are rank <= 1; hence
Case A is excluded and (B2 empty) at most ONE M is rank 2: the configuration
is B0 or B1 and at least TWO reduced sites factor.
m=27: only (5,7) is absent -> the slot-pair (0,2) is rank <= 1, so Case A is
excluded there too (Case A needs all six of rank 2).
m=28: nothing is excluded a priori -- Case A is available, and that is
exactly the loophole.
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

SLOT = {0: 1, 1: 2, 2: 3, 3: 4}


def to_tensor(Ms):
    """parent's L-pair-keyed M's -> my slot-keyed M's (slots 1..4)."""
    return {(SLOT[i], SLOT[j]): Ms[(i, j)] for (i, j) in B.LPAIRS}


def load_points():
    out = {}
    for fn, key in ((os.path.join(PAR, "results_break.json"), "break"),):
        if not os.path.exists(fn):
            continue
        d = json.load(open(fn))
        for m in (26, 27, 28):
            for rec in d.get("m%d" % m, []):
                if "point" in rec:
                    bl = {}
                    for k, v in rec["point"].items():
                        e = tuple(int(x) for x in k.strip("()").split(","))
                        bl[e] = [[Fraction(x) for x in row] for row in v]
                    out.setdefault(m, []).append(
                        ("%s seed %d fac %s" % (key, rec["seed"],
                                                rec["factoring"]), bl))
    # W20's descent points
    sys.path.insert(0, PAR)
    from w21_pf import load_w20_points
    for m, lst in load_w20_points().items():
        for tag, bl in lst[:1]:
            out.setdefault(m, []).insert(0, ("w20 " + tag, bl))
    return out


def main():
    res = {"_header": "UNAUDITED W21-M1-TENSOR application. Exact only."}
    fb = B.full_box_words()
    pts = load_points()
    for m in (26, 27, 28):
        T = K.W8_IMMUNE[m]
        gam = K.gamma_edges(T)
        clean = K.clean_words(T)
        rows = []
        print("=== m = %d ===" % m)
        for tag, bl in pts.get(m, []):
            assert all(K.phi_value(bl, gam, w) == 0 for w in clean)
            orig_fac = [t for t in range(8) if K.factors_at(bl, gam, t)]
            for x in fb:
                P = B.hafL(bl, x)
                if P == 0:
                    rows.append(dict(tag=tag, x=list(x), hafL_zero=True))
                    print("  %-28s x=%s : haf_L = 0 (degenerate branch)"
                          % (tag, x))
                    continue
                Ms = {(i, j): B.M_of(bl, gam, x, i, j, P) for (i, j) in
                      B.LPAIRS}
                MT = to_tensor(Ms)
                ok = all(TT.haf_value(MT, y) == 0
                         for y in product(range(3), repeat=4))
                rk = TT.ranks(MT)
                nzero = [str(p) for p in TT.PAIRS if TT.is_zero(MT[p])]
                fac = TT.any_site_factors(MT)
                rho = []
                for i in (1, 2, 3, 4):
                    cols = []
                    for j in (1, 2, 3, 4):
                        if j == i:
                            continue
                        p = (min(i, j), max(i, j))
                        A = MT[p] if p[0] == i else TT.transpose(MT[p])
                        for c in range(3):
                            v = TT.col(A, c)
                            if any(v):
                                cols.append(v)
                    rho.append(TT.rank(cols) if cols else 0)
                n2 = sum(1 for p in TT.PAIRS if rk[p] == 2)
                rows.append(dict(tag=tag, x=list(x), identity_holds=ok,
                                 ranks={str(p): rk[p] for p in TT.PAIRS},
                                 n_rank2=n2, zero_blocks=nzero,
                                 reduced_factoring=fac, rho=rho,
                                 original_factoring=orig_fac))
                print("  %-28s x=%s : identity=%s ranks=%s (#rank2=%d) "
                      "zero=%s rho=%s reduced-factoring=%s"
                      % (tag, x, ok, [rk[p] for p in TT.PAIRS], n2,
                         nzero, rho, fac))
            print("     (original factoring sites: %s)" % orig_fac)
        res["m%d" % m] = rows
    json.dump(res, open(os.path.join(HERE, "results_apply.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
