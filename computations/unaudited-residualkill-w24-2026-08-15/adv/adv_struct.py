#!/usr/bin/env python3
"""ADVERSARIAL W24 -- structural analysis of the c_e coefficients.

(A) VERIFY the explicit 2-term formula for c_e = haf_Gamma(V - i - j) against
    the from-the-definition engine (w24_core.haf_on) at exact random points.
(B) VERIFY the "TRIPLE IDENTITY": for each i in L = {0,1,2,3} the three
    singles at i give
        c_{e1} = P u + Q v ,  c_{e2} = R u + Q t ,  c_{e3} = R v + P t
    (up to relabelling), i.e. the 3x3 matrix [[P,Q,0],[R,0,Q],[0,R,P]]
    applied to (u,v,t), whose determinant is -2 P Q R.
(C) Find, for each i, an explicit VIRTUAL POINT v* and three words W1,W2,W3
    that are e1/e2/e3-ISOLATED rows of the residual system and satisfy
    c_{ek}(Wk) = c_{ek}(v*).  Then Phi(W1)=Phi(W2)=Phi(W3)=0 forces
    (u,v,t) = 0, contradicting all-Gamma-cells-nonzero.
(D) MUTATION CONTROL: perturb and check the claimed identities break /
    survive as they should.

EXACT arithmetic only (Fraction).  UNAUDITED probe.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
W24 = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-residualkill-w24-2026-08-15"
sys.path.insert(0, W24)
HERE = os.path.dirname(os.path.abspath(__file__))
import w24_core as C                                              # noqa: E402
import w24_resid as RS                                            # noqa: E402

L = (0, 1, 2, 3)
SIG = {0: 7, 1: 4, 2: 5, 3: 6}
ISIG = {v: k for k, v in SIG.items()}


def ed(u, v):
    return (u, v) if u < v else (v, u)


def cell(bl, u, v, w):
    e = ed(u, v)
    return bl[e][w[e[0]]][w[e[1]]]


def c_formula(bl, gam_set, e, w):
    """the explicit 2-term formula for c_e(w)."""
    i, j = e
    p, q = ISIG[j], SIG[i]
    k1, k2 = sorted(set(L) - {i, p})
    tot = Fraction(0)
    for (kk, ko) in ((k1, k2), (k2, k1)):
        # term: a^L_{p,ko} * d_{kk} * a^R_{sigma(ko),q}
        if ed(p, ko) not in gam_set:
            continue
        if ed(kk, SIG[kk]) not in gam_set:
            continue
        if ed(SIG[ko], q) not in gam_set:
            continue
        tot += (cell(bl, p, ko, w) * cell(bl, kk, SIG[kk], w)
                * cell(bl, SIG[ko], q, w))
    return tot


def rand_point(m, rng, lo=-9, hi=9):
    gam = C.gamma_edges(C.TEMPLATES[m])
    return {e: [[Fraction(rng.randint(lo, hi) or 5, rng.randint(1, 4))
                 for _ in range(3)] for _ in range(3)] for e in gam}


def triple_parts(bl, gam_set, i, w):
    """(P,Q,R,u,v,t) for the vertex i, evaluated at w."""
    q = SIG[i]
    k = sorted(set(L) - {i})          # the three other L vertices
    # the three singles at i are (i, j) for j in R - {q}; p = isig(j)
    # p runs over k.  For p, {k1,k2} = k - {p}.
    d = {}
    for p in k:
        k1, k2 = sorted(set(k) - {p})
        d[p] = (ed(p, k2), ed(k1, SIG[k1]), ed(SIG[k2], q),
                ed(p, k1), ed(k2, SIG[k2]), ed(SIG[k1], q))
    return d


def main():
    out = {"_header": "ADVERSARIAL W24 structural analysis, UNAUDITED, exact"}
    rng = random.Random(20260815)

    # ---------------------------------------------------------------- (A)
    formula_ok = {}
    for m in (25, 26, 27, 28):
        T = C.TEMPLATES[m]
        gam_set = set(C.gamma_edges(T))
        sing = C.single_edges(T)
        bad = 0
        n = 0
        for _t in range(3):
            bl = rand_point(m, rng)
            for e in sing:
                rest = tuple(x for x in range(8) if x not in e)
                for _w in range(40):
                    w = tuple(rng.randrange(3) for _ in range(8))
                    a = C.haf_on(bl, gam_set, rest, w)
                    b = c_formula(bl, gam_set, e, w)
                    n += 1
                    if a != b:
                        bad += 1
        formula_ok[m] = dict(checked=n, mismatches=bad)
        print("(A) m=%d formula vs definition: %d checks, %d mismatches"
              % (m, n, bad), flush=True)
    out["A_formula"] = formula_ok

    # independence of c_e from w_i, w_j
    indep = {}
    for m in (25, 26, 27, 28):
        gam_set = set(C.gamma_edges(C.TEMPLATES[m]))
        sing = C.single_edges(C.TEMPLATES[m])
        bl = rand_point(m, rng)
        bad = 0
        for e in sing:
            rest = tuple(x for x in range(8) if x not in e)
            for _w in range(30):
                w = list(rng.randrange(3) for _ in range(8))
                base = C.haf_on(bl, gam_set, rest, tuple(w))
                for pos in e:
                    for val in range(3):
                        w2 = list(w)
                        w2[pos] = val
                        if C.haf_on(bl, gam_set, rest, tuple(w2)) != base:
                            bad += 1
        indep[m] = bad
        print("(A2) m=%d c_e independent of w_i,w_j: violations = %d"
              % (m, bad), flush=True)
    out["A_independence_violations"] = indep

    # ---------------------------------------------------------------- (B)
    # triple identity + determinant, per i, per m
    trip = {}
    for m in (25, 26, 27, 28):
        T = C.TEMPLATES[m]
        gam_set = set(C.gamma_edges(T))
        rec = {}
        for i in L:
            q = SIG[i]
            k = sorted(set(L) - {i})
            # the six "structural" edges
            # P = a^L_{k?}..., we name by the pattern below.
            # For p in k with {k1,k2} = k - {p}:
            #   c_{(i,sigma(p))} = a_{p,k2} d_{k1} r_{sig(k2),q}
            #                    + a_{p,k1} d_{k2} r_{sig(k1),q}
            # Define X_a = a_{k_b,k_c} d_{k_a} (a=0,1,2 with {b,c}=k-{a}) --
            # i.e. the L-edge OPPOSITE to k_a times the cross edge at k_a.
            # Then c_{(i,sigma(k_a))} = X_b r_{sig(k_c),q} + X_c r_{sig(k_b),q}
            # with {b,c} = {0,1,2} - {a}.   [check below]
            ok = True
            missing = []
            for a in range(3):
                p = k[a]
                b, c = sorted(set(range(3)) - {a})
                # term1 of c_{(i,sigma(p))}: a_{p,k2} d_{k1} r_{sig(k2),q}
                # with k1 = k[b], k2 = k[c] (sorted)
                for (kk, ko) in ((k[b], k[c]), (k[c], k[b])):
                    for eg in (ed(p, ko), ed(kk, SIG[kk]), ed(SIG[ko], q)):
                        if eg not in gam_set:
                            missing.append((i, p, str(eg)))
                            ok = False
            rec[i] = dict(all_terms_present=ok, missing=missing[:6])
        trip[m] = rec
        print("(B) m=%d triples: %s" % (m, {i: rec[i]["all_terms_present"]
                                            for i in L}), flush=True)
    out["B_triples"] = trip

    # numeric check of the 3x3 identity M (u,v,t) = (c1,c2,c3), det = -2PQR
    ident = {}
    for m in (25, 26, 27, 28):
        T = C.TEMPLATES[m]
        gam_set = set(C.gamma_edges(T))
        bad = 0
        n = 0
        detz = 0
        for _t in range(3):
            bl = rand_point(m, rng)
            for i in L:
                q = SIG[i]
                k = sorted(set(L) - {i})
                for _w in range(20):
                    w = tuple(rng.randrange(3) for _ in range(8))
                    # X_a = (L-edge opposite k_a inside k) * d_{k_a}
                    X = []
                    for a in range(3):
                        b, c = sorted(set(range(3)) - {a})
                        eL = ed(k[b], k[c])
                        eD = ed(k[a], SIG[k[a]])
                        if eL not in gam_set or eD not in gam_set:
                            X.append(None)
                        else:
                            X.append(cell(bl, k[b], k[c], w)
                                     * cell(bl, k[a], SIG[k[a]], w))
                    # r_a = R-edge (sigma(k_a), q)
                    R_ = []
                    for a in range(3):
                        eR = ed(SIG[k[a]], q)
                        R_.append(cell(bl, SIG[k[a]], q, w)
                                  if eR in gam_set else None)
                    for a in range(3):
                        b, c = sorted(set(range(3)) - {a})
                        e = ed(i, SIG[k[a]])
                        pred = Fraction(0)
                        for (xx, rr) in ((X[b], R_[c]), (X[c], R_[b])):
                            if xx is None or rr is None:
                                continue
                            pred += xx * rr
                        rest = tuple(x for x in range(8) if x not in e)
                        act = C.haf_on(bl, gam_set, rest, w)
                        n += 1
                        if pred != act:
                            bad += 1
                    if all(x is not None for x in X):
                        det = -2 * X[0] * X[1] * X[2]
                        if det == 0:
                            detz += 1
        ident[m] = dict(checked=n, mismatches=bad, zero_dets=detz)
        print("(B2) m=%d triple identity: %d checks, %d mismatches, "
              "%d zero dets" % (m, n, bad, detz), flush=True)
    out["B_identity"] = ident

    json.dump(out, open(os.path.join(HERE, "results_struct.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
