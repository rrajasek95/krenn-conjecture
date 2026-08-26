#!/usr/bin/env python3
"""W24 -- THEOREM W24-A: the identically-vanishing-hafnian stratum is KILLED,
with an explicit certificate per m.  UNAUDITED.  Exact only.

THEOREM W24-A.  Fix m in {25,26,27,28}.  Let the Gamma blocks have ALL cells
nonzero and let haf_Gamma(w) = 0 for every one of the 6561 words (equivalently
the multilinear Gamma-hafnian form vanishes identically).  Then the residual
degree-<=1 system forces some live single cell to vanish; the point is KILLED.

CERTIFICATE.  Fix i in L and let L\\{i} = {p1,p2,p3}, e_a = (i, sigma(p_a)).
Put, at a word w,
    X_a = G_{p_b p_c} * D_{p_a}     ({b,c} = {1,2,3}\\{a}),   r_a = F_{p_a}
where G, D, F are as in w24_ident (an L-cell, a matching cell, an R-cell).
Then EXACTLY  (c_{e_1}, c_{e_2}, c_{e_3})^T = M (r_1,r_2,r_3)^T with
    M = [[0, X_3, X_2], [X_3, 0, X_1], [X_2, X_1, 0]],   det M = 2 X_1 X_2 X_3.
So if every edge occurring in some X_a lies in Gamma and every cell is
nonzero, det M != 0 in every characteristic != 2, hence the three
coefficients cannot vanish simultaneously at w.
Because c_{e_a} does not depend on w_i or on w_{sigma(p_a)}, a VIRTUAL word
v* can be edited into three SOLO words W_1, W_2, W_3 (W_a = v* with the two
coordinates of e_a overwritten by e_a's cell) with c_{e_a}(W_a) = c_{e_a}(v*)
and with e_a the ONLY live single active at W_a.  Under the hypothesis
haf_Gamma == 0 every row is homogeneous, so the row at W_a reads
c_{e_a}(W_a) z_{e_a} = 0; for the a with c_{e_a}(v*) != 0 this gives
z_{e_a} = 0.  QED.

This script enumerates, per m, all valid certificates (i, v*) -- checking the
solo property combinatorially and the det-M non-vanishing SYMBOLICALLY (all
the required edges present in Gamma) -- and then verifies the conclusion
numerically at the exact clean points that satisfy the hypothesis.
"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w24_core as C                                              # noqa: E402
import w24_pts as P                                               # noqa: E402
import w24_resid as RS                                            # noqa: E402
import w24_ident as ID                                            # noqa: E402

L = (0, 1, 2, 3)
SIG = {0: 7, 1: 4, 2: 5, 3: 6}


def certificates(m):
    """all (i, v*, [W_1,W_2,W_3], symbolic det-M nonvanishing) at level m."""
    T = C.TEMPLATES[m]
    gam = set(C.gamma_edges(T))
    sing = C.single_edges(T)
    live = {e for e in sing
            if C.has_pm(gam, tuple(v for v in range(8) if v not in e))}
    out = []
    for i in L:
        ps = [q for q in L if q != i]
        es = [(i, SIG[q]) for q in ps]
        if any(e not in live for e in es):
            continue
        # SYMBOLIC: X_a = G_{p_b p_c} D_{p_a}; G is always in Gamma (K_4 on L);
        # D_{p_a} = A_{p_a, sigma(p_a)} must be a Gamma edge.
        okX = all((min(q, SIG[q]), max(q, SIG[q])) in gam for q in ps)
        if not okX:
            out.append(dict(i=i, valid=False,
                            reason="a matching edge (p,sigma p) is missing"))
            continue
        found = []
        for v in C.MIXED:
            Ws = []
            ok = True
            for a, e in enumerate(es):
                w = list(v)
                w[e[0]] = sing[e][0]
                w[e[1]] = sing[e][1]
                w = tuple(w)
                if len(set(w)) == 1:
                    ok = False
                    break
                act = {f for f in live
                       if w[f[0]] == sing[f][0] and w[f[1]] == sing[f][1]}
                if act != {e}:
                    ok = False
                    break
                Ws.append(w)
            if ok:
                found.append((v, Ws))
            if len(found) >= 400:
                break
        out.append(dict(i=i, valid=bool(found), n_virtual=len(found),
                        example=None if not found else
                        dict(v=list(found[0][0]),
                             W=[list(x) for x in found[0][1]])))
    return out


def main():
    res = {"_header": "UNAUDITED W24 Theorem W24-A certificates."}
    for m in (25, 26, 27, 28):
        cs = certificates(m)
        res["m%d" % m] = cs
        print("m=%d certificates:" % m)
        for c in cs:
            if c.get("valid"):
                print("   i=%d VALID (%d virtual words); example v*=%s -> "
                      "solo words %s"
                      % (c["i"], c["n_virtual"], c["example"]["v"],
                         c["example"]["W"]))
            else:
                print("   i=%d invalid: %s" % (c["i"],
                                               c.get("reason", "no virtual "
                                                     "word with all three "
                                                     "solo")))
    # m=25 fallback certificate: c_(2,6) is a MONOMIAL at m=25,26,27
    print("\nm=25/26/27 FALLBACK: c_(2,6) = A_13[x1][x3]*A_07[x0][y7]*"
          "A_45[y4][y5] (a monomial; A_57 is absent from Gamma), so it is "
          "nonzero at EVERY word when all Gamma cells are.")
    mono = {}
    import random
    rng = random.Random(4242)
    for m in (25, 26, 27, 28):
        gam = C.gamma_edges(C.TEMPLATES[m])
        gs = set(gam)
        bad = 0
        for _ in range(300):
            bl = {e: [[Fraction(rng.randint(-9, 9) or 5, rng.randint(1, 4))
                       for _ in range(3)] for _ in range(3)] for e in gam}
            w = tuple(rng.randrange(3) for _ in range(8))
            x, y = w[:4], w[4:]
            pred = (bl[(1, 3)][x[1]][x[3]] * bl[(0, 7)][x[0]][y[3]]
                    * bl[(4, 5)][y[0]][y[1]])
            if pred != ID.coeff(bl, gs, (2, 6), w):
                bad += 1
        mono["m%d" % m] = bad
        print("   m=%d: monomial formula for c_(2,6) mismatches %d/300%s"
              % (m, bad, "  (expected to FAIL at m=28: A_57 present)"
                 if m == 28 else ""))
    res["c26_monomial_mismatches"] = mono

    # ---- verify the theorem's conclusion at the points satisfying it
    ver = []
    for m, tag, bl in P.stored_points():
        gs = set(C.gamma_edges(C.TEMPLATES[m]))
        if any(C.phi(bl, gs, w) != 0 for w in C.WORDS):
            continue                       # hypothesis of W24-A fails
        cs = [c for c in certificates(m) if c.get("valid")]
        okall = []
        for c in cs:
            v = tuple(c["example"]["v"])
            Ws = [tuple(x) for x in c["example"]["W"]]
            es = [(c["i"], SIG[q]) for q in L if q != c["i"]]
            cc = [ID.coeff(bl, gs, e, W) for e, W in zip(es, Ws)]
            okall.append((c["i"], [str(z) for z in cc],
                          any(z != 0 for z in cc)))
        d = RS.verdict(m, bl)
        ver.append(dict(m=m, tag=tag, certs=okall, forced=d["forced_zero"]))
        print("m=%d %-24s certificate coefficients nonzero: %s ; verdict "
              "forced cells %d"
              % (m, tag[:24], [o[2] for o in okall], len(d["forced_zero"])))
    res["verification"] = ver
    json.dump(res, open(os.path.join(HERE, "results_thmA.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
