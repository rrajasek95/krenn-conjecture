#!/usr/bin/env python3
"""W26 -- LEMMA W26-1: the l_02 l_13 contradiction.  UNAUDITED.  Exact only.

CLAIM (m=26).  Let the Gamma blocks be a CLEAN point with all cells
nonzero.  Take any x = (x0,x1,x2,x3) and any y6-letter c such that the
words (x,(y4,y5,c,y7)) are CLEAN for (y4,y5,y7) in a full box.  Write
  alpha = A36[x3][c],  D0 = A07[x0][.],  D1 = A14[x1][.],  D2 = A25[x2][.],
  P = A45, S = A47, U = A56, V = A67,  l_ab = A_ab[x_a][x_b],
  h = hafL = l01 l23 + l02 l13 + l03 l12.
The clean equation is EXACTLY

  S[y4][y7]*(alpha l01 D2 + h U[y5][c])
+ P[y4][y5]*(alpha l12 D0 + h V[c][y7])
+ D1[y4]*(alpha D0 D2 + l03 D2 V[c][y7] + l23 D0 U[y5][c])   =  0.     (E)

Grouping (E) by y4 / y5 / y7 gives three vector equations; in EACH the
simultaneous vanishing of the three coefficients forces
      alpha * D0 * D1 * D2 * l02 * l13 / h  =  0,
impossible.  Hence at EVERY clean point the three vectors are DEPENDENT:

 (a) det[ A47[.][y7], A45[.][y5], A14[x1][.] ] = 0        all (y5,y7)
 (b) det[ A25[x2][.], A45[y4][.], A56[.][c]  ] = 0        all y4
 (c) det[ A07[x0][.], A47[y4][.], A67[c][.]  ] = 0        all y4

This file (1) verifies (E) as an identity, (2) verifies the algebraic
contradiction symbolically, (3) tests (a),(b),(c) at every stored and
fresh point, with mutation and out-of-locus controls.
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
import w26_core as C                                              # noqa: E402
import w26_pts as PT                                              # noqa: E402

OUT = {"_header": "UNAUDITED W26 Lemma W26-1."}
RNG = random.Random(26_1_2026)


def det3c(v1, v2, v3):
    return (v1[0] * (v2[1] * v3[2] - v2[2] * v3[1])
            - v1[1] * (v2[0] * v3[2] - v2[2] * v3[0])
            + v1[2] * (v2[0] * v3[1] - v2[1] * v3[0]))


def lvals(bl, x):
    return {(a, b): bl[(a, b)][x[a]][x[b]]
            for a in range(4) for b in range(4) if a < b}


def E_terms(bl, m, x, c, y4, y5, y7):
    """the three coefficients (K, L, N) of (E) and the three vectors."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    ll = lvals(bl, x)
    h = (ll[(0, 1)] * ll[(2, 3)] + ll[(0, 2)] * ll[(1, 3)]
         + ll[(0, 3)] * ll[(1, 2)])
    al = bl[(3, 6)][x[3]][c] if (3, 6) in gs else Fraction(0)
    D0 = bl[(0, 7)][x[0]][y7]
    D1 = bl[(1, 4)][x[1]][y4]
    D2 = bl[(2, 5)][x[2]][y5]
    S = bl[(4, 7)][y4][y7]
    P = bl[(4, 5)][y4][y5]
    U = bl[(5, 6)][y5][c]
    V = bl[(6, 7)][c][y7]
    K = al * ll[(0, 1)] * D2 + h * U
    Lc = al * ll[(1, 2)] * D0 + h * V
    Nc = al * D0 * D2 + ll[(0, 3)] * D2 * V + ll[(2, 3)] * D0 * U
    return K, Lc, Nc, S, P, D1, h, al


def check_identity():
    """(E) equals Phi at the word, for m=26 (no A46 column)."""
    print("=" * 74)
    bad = tot = 0
    gam = C.gamma_edges(C.TEMPLATES[26])
    gs = set(gam)
    for _ in range(6):
        bl = {e: [[Fraction(RNG.randint(-9, 9) or 5, RNG.randint(1, 4))
                   for _ in range(3)] for _ in range(3)] for e in gam}
        for _k in range(150):
            x = tuple(RNG.randrange(3) for _ in range(4))
            c = RNG.randrange(3)
            y4, y5, y7 = (RNG.randrange(3) for _ in range(3))
            K, Lc, Nc, S, P, D1, h, al = E_terms(bl, 26, x, c, y4, y5, y7)
            lhs = K * S + Lc * P + Nc * D1
            w = tuple(x) + (y4, y5, c, y7)
            tot += 1
            bad += (lhs != C.phi(bl, gs, w))
    print("(E) identity vs Phi at m=26 : %d/%d mismatches" % (bad, tot))
    OUT["E_identity_mismatch"] = bad
    OUT["E_identity_tests"] = tot
    # mutation: drop the alpha*D0*D2 piece of N
    badm = 0
    for _ in range(3):
        bl = {e: [[Fraction(RNG.randint(-9, 9) or 5, RNG.randint(1, 4))
                   for _ in range(3)] for _ in range(3)] for e in gam}
        for _k in range(40):
            x = tuple(RNG.randrange(3) for _ in range(4))
            c = RNG.randrange(3)
            y4, y5, y7 = (RNG.randrange(3) for _ in range(3))
            K, Lc, Nc, S, P, D1, h, al = E_terms(bl, 26, x, c, y4, y5, y7)
            ll = lvals(bl, x)
            D0 = bl[(0, 7)][x[0]][y7]
            D2 = bl[(2, 5)][x[2]][y5]
            Nbad = Nc - al * D0 * D2
            badm += ((K * S + Lc * P + Nbad * D1)
                     != C.phi(bl, gs, tuple(x) + (y4, y5, c, y7)))
    print("MUTATION (N missing alpha*D0*D2): fails %d/120 (want ~120)" % badm)
    OUT["E_mutation_fails"] = badm


def check_contradiction():
    """K = L = N = 0  =>  alpha D0 D2 l02 l13 = 0  (symbolic, sympy)."""
    import sympy as sp
    l01, l02, l03, l12, l13, l23 = sp.symbols("l01 l02 l03 l12 l13 l23")
    al, D0, D2, U, V = sp.symbols("al D0 D2 U V")
    h = l01 * l23 + l02 * l13 + l03 * l12
    K = al * l01 * D2 + h * U
    Lc = al * l12 * D0 + h * V
    Nc = al * D0 * D2 + l03 * D2 * V + l23 * D0 * U
    # solve K = 0, L = 0 for U, V (h != 0), substitute into N
    Us = sp.solve(K, U)[0]
    Vs = sp.solve(Lc, V)[0]
    Nsub = sp.simplify(Nc.subs({U: Us, V: Vs}))
    target = sp.simplify(al * D0 * D2 * l02 * l13 / h)
    ok = sp.simplify(Nsub - target) == 0
    print("=" * 74)
    print("SYMBOLIC: N|_{K=L=0}  =  alpha*D0*D2*l02*l13/h   ->", ok)
    print("          N|_{K=L=0}  =", sp.factor(Nsub))
    OUT["symbolic_contradiction"] = bool(ok)
    OUT["symbolic_N"] = str(sp.factor(Nsub))
    # the h = 0 branch: if h = 0 then K = al*l01*D2 != 0, so K = 0 is
    # already impossible -- record that too.
    OUT["h_zero_branch"] = ("if h=0 then K = al*l01*D2 != 0, so K=0 fails: "
                            "the coefficient system is unsatisfiable "
                            "regardless of h")
    return ok


def clean_x_c(m, x, c):
    """the (y4,y5,y7) box for which (x,(y4,y5,c,y7)) is clean, or None."""
    T = C.TEMPLATES[m]
    sing = C.single_edges(T)
    lv = set(C.live_singles(m))
    box = {4: set(range(3)), 5: set(range(3)), 7: set(range(3))}
    for e, (a, b) in sing.items():
        if e not in lv or x[e[0]] != a:
            continue
        j = e[1]
        if j == 6:
            if b == c:
                return None
        else:
            box[j].discard(b)
    if not all(box.values()):
        return None
    return box


def test_lemma(m, bl, label):
    """(a),(b),(c) at every admissible (x,c)."""
    viol = []
    n = 0
    for x in product(range(3), repeat=4):
        for c in range(3):
            box = clean_x_c(m, x, c)
            if box is None:
                continue
            if len(set(x)) == 1 and len(box[4]) and False:
                pass
            for y5 in sorted(box[5]):
                for y7 in sorted(box[7]):
                    n += 1
                    d = det3c([bl[(4, 7)][t][y7] for t in range(3)],
                              [bl[(4, 5)][t][y5] for t in range(3)],
                              bl[(1, 4)][x[1]])
                    # (a) needs the FULL y4 range
                    if len(box[4]) == 3 and d != 0:
                        viol.append(("a", list(x), c, y5, y7, str(d)))
            for y4 in sorted(box[4]):
                if len(box[5]) == 3:
                    d = det3c(bl[(2, 5)][x[2]],
                              bl[(4, 5)][y4],
                              [bl[(5, 6)][t][c] for t in range(3)])
                    if d != 0:
                        viol.append(("b", list(x), c, y4, None, str(d)))
                if len(box[7]) == 3:
                    d = det3c(bl[(0, 7)][x[0]],
                              bl[(4, 7)][y4],
                              bl[(6, 7)][c])
                    if d != 0:
                        viol.append(("c", list(x), c, y4, None, str(d)))
    return n, viol


def main():
    check_identity()
    check_contradiction()
    print("=" * 74)
    print("LEMMA W26-1 (a)(b)(c) at stored points (m=26 only -- the "
          "argument as stated needs the A46 column absent)")
    recs = []
    for m, tag, bl in PT.stored_points():
        if m != 26:
            continue
        n, viol = test_lemma(m, bl, tag)
        recs.append(dict(m=m, tag=tag, n_tests=n, n_violations=len(viol),
                         van=PT.vanishing_stratum(m, bl),
                         examples=viol[:3]))
        print("  m=26 %-24s tests=%d  VIOLATIONS=%d  van=%s"
              % (tag[:24], n, len(viol), PT.vanishing_stratum(m, bl)),
              flush=True)
    OUT["stored_m26"] = recs
    # ---- CONTROL: the lemma must FAIL at a NON-clean point (out of locus)
    gam = C.gamma_edges(C.TEMPLATES[26])
    bad = 0
    for _ in range(5):
        bl = {e: [[Fraction(RNG.randint(-9, 9) or 5, RNG.randint(1, 4))
                   for _ in range(3)] for _ in range(3)] for e in gam}
        n, viol = test_lemma(26, bl, "random")
        bad += (len(viol) > 0)
    print("OUT-OF-LOCUS CONTROL: random (non-clean) points violating "
          "(a)/(b)/(c): %d/5  (want 5 -- else the test is vacuous)" % bad)
    OUT["out_of_locus_violations"] = bad
    json.dump(OUT, open(os.path.join(HERE, "results_lem1.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
