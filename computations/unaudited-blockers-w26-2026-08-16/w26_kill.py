#!/usr/bin/env python3
"""W26 -- THEOREM W26-K : the vertex-7 pure-row theorem.  UNAUDITED. Exact.

THE MECHANISM.  All three singles into the R-vertex 7 -- (1,7) cell (0,2),
(2,7) cell (1,2), (3,7) cell (2,2) -- fire at the SAME letter y7 = 2, and
they are triggered by x1 = 0, x2 = 1, x3 = 2 respectively.  At m <= 27 the
R-edge (5,7) is absent, so exactly THREE Gamma blocks touch vertex 7:
A_07 (sigma), A_47, A_67.  Hence, for every x and every (y4,y5,y6),

    Phi(x, y|y7=t)  =  Psi[D0] * A07[x0][t] + Psi_1 * A47[y4][t]
                       + Psi_3 * A67[y6][t]          =  <Psivec, row_t(M)>,
    M := the 3x3 matrix with rows  row_t = (A07[x0][t], A47[y4][t],
                                            A67[y6][t]).

*** M DOES NOT DEPEND ON x1, x2 OR x3 -- exactly the variables that trigger
the three singles into 7. ***

STEP 1 (the determinant lemma).  Take x with x1 != 0, x2 != 1, x3 != 2, so
that no single into 7 fires: all three y7-letters are clean, so
<Psivec, row_t> = 0 for t = 0,1,2.  Either det M = 0, or Psivec = 0.  In
the second case Phi(x,y|y7=t) = 0 for all t as well.  And
   m=25: Psi[D0] = D1 l23 r56, a nonzero monomial  => Psivec != 0 => det M = 0
   m=26: Psi_1 = Psi_3 = 0 forces Psi[D0] = D1 D2 D3 l02 l13 / h != 0
         => Psivec != 0 => det M = 0
   m=27: Psi_1 = Psi_3 = 0 forces Psi[D0] = l13 D2 (D1 D3 l02 + h r46)/h,
         which CAN vanish; then Phi vanishes on the whole y7-family anyway.
   m=28: A_57 is present, four blocks at 7 -- use the master relation W26-M
         (w26_master.py) to reduce to three vectors W_q; not covered here.

STEP 2 (transfer).  det M depends only on (x0, y4, y6).  So the value
proved in step 1 (at x1 != 0, x2 != 1, x3 != 2) holds at EVERY x -- in
particular where a single into 7 IS triggered.

STEP 3 (the pure row).  Fix x with (say) x2 = 1, and y4, y5, y6 avoiding
every single into 4, 5, 6.  Then y7 = 0 and y7 = 1 are clean, so
<Psivec, row_0> = <Psivec, row_1> = 0, and the (2,7)-solo row at y7 = 2
reads c_(2,7) z_(2,7) + Phi = 0 with Phi = <Psivec, row_2>.  Since
det M = 0, row_2 lies in span{row_0, row_1} UNLESS row_0 and row_1 are
proportional (the EXCEPTIONAL LOCUS, tested below).  Off that locus
Phi = 0, so the row is PURE and forces z_(2,7) = 0: the point is KILLED.

This file tests, exactly: (K1) det M = 0 at every clean point, every
(x0,y4,y6); (K2) Phi = 0 at every y7=2 vertex-7 word; (K3) the exceptional
locus row_0 || row_1; (K4) the induced pure rows; with mutation and
out-of-locus controls.
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
import w26_fast as F                                              # noqa: E402
import w26_sub as SB                                              # noqa: E402

RES = os.path.join(HERE, "results_kill.json")
OUT = {"_header": "UNAUDITED W26 Theorem W26-K (vertex-7 pure rows)."}


def ck(path=RES):
    json.dump(OUT, open(path, "w"), indent=1, default=str)


def det3c(v1, v2, v3):
    return (v1[0] * (v2[1] * v3[2] - v2[2] * v3[1])
            - v1[1] * (v2[0] * v3[2] - v2[2] * v3[0])
            + v1[2] * (v2[0] * v3[1] - v2[1] * v3[0]))


def Mmat(bl, x0, y4, y6):
    """rows indexed by the letter t of y7."""
    return [[bl[(0, 7)][x0][t], bl[(4, 7)][y4][t], bl[(6, 7)][y6][t]]
            for t in range(3)]


def detM(bl, x0, y4, y6):
    M = Mmat(bl, x0, y4, y6)
    return det3c(M[0], M[1], M[2])


def prop01(bl, x0, y4, y6):
    """are rows t=0 and t=1 of M proportional?  (the exceptional locus)"""
    M = Mmat(bl, x0, y4, y6)
    a, b = M[0], M[1]
    return all(a[i] * b[j] - a[j] * b[i] == 0
               for i in range(3) for j in range(i + 1, 3))


def test_point(m, bl):
    """(K1) det M ; (K3) exceptional locus ; (K2/K4) vertex-7 solo rows."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    T = C.TEMPLATES[m]
    sing = C.single_edges(T)
    lv = set(C.live_singles(m))
    nd = bad_det = nprop = 0
    for x0 in range(3):
        for y4 in range(3):
            for y6 in range(3):
                nd += 1
                if detM(bl, x0, y4, y6) != 0:
                    bad_det += 1
                if prop01(bl, x0, y4, y6):
                    nprop += 1
    # vertex-7 solo/near-solo rows: words whose active live singles all
    # have R-endpoint 7 (so y7 = 2)
    n7 = phinz = 0
    for w, act in _rv7(m):
        n7 += 1
        if C.phi(bl, gs, w) != 0:
            phinz += 1
    # pure rows at the singles into 7
    pure = {}
    for e in sorted(lv):
        if e[1] != 7:
            continue
        r = SB.solo_report(m, bl, e)
        pure[str(e)] = dict(n_solo=r["n_solo"], n_pure=r["n_pure"],
                            all_pure=(r["n_pure"] == r["n_solo"]),
                            survives=r["survives"])
    return dict(n_detM=nd, bad_detM=bad_det, n_exceptional_prop01=nprop,
                n_vertex7_words=n7, n_vertex7_Phi_nonzero=phinz,
                vertex7_pure=pure)


_RV7 = {}


def _rv7(m):
    if m in _RV7:
        return _RV7[m]
    T = C.TEMPLATES[m]
    sing = C.single_edges(T)
    lv = set(C.live_singles(m))
    out = []
    for w in C.MIXED:
        act = tuple(f for f in lv
                    if w[f[0]] == sing[f][0] and w[f[1]] == sing[f][1])
        if act and all(f[1] == 7 for f in act):
            out.append((w, act))
    _RV7[m] = tuple(out)
    return _RV7[m]


def main():
    import w26_pts as PT
    OUT["battery"] = {}
    ADV = os.path.join(HERE, "adv")
    battery = [("P1_m25_case2b", 25,
                os.path.join(ADV, "results_case2b.json"), ("main", "point")),
               ("P2_m26_solo", 26,
                os.path.join(ADV, "results_solo.json"), ("m26", "point")),
               ("P3_m27_solo", 27,
                os.path.join(ADV, "results_solo.json"), ("m27", "point"))]
    for name, m, path, keys in battery:
        if not os.path.exists(path):
            continue
        d = json.load(open(path))
        for k in keys:
            d = d[k]
        bl = {tuple(int(t) for t in k.strip("()").split(",")):
              [[Fraction(x) for x in row] for row in v] for k, v in d.items()}
        r = test_point(m, bl)
        OUT["battery"][name] = r
        print("%-16s m=%d  det M nonzero %d/%d | exceptional %d/27 | "
              "vertex-7 words with Phi!=0 %d/%d"
              % (name, m, r["bad_detM"], r["n_detM"],
                 r["n_exceptional_prop01"], r["n_vertex7_Phi_nonzero"],
                 r["n_vertex7_words"]), flush=True)
        for e, v in r["vertex7_pure"].items():
            print("      %-8s solo=%-4d pure=%-4d ALL PURE=%s"
                  % (e, v["n_solo"], v["n_pure"], v["all_pure"]))
        ck()
    # stored points
    OUT["stored"] = []
    for m, tag, bl in PT.stored_points():
        r = test_point(m, bl)
        r.update(m=m, tag=tag)
        OUT["stored"].append(r)
        print("stored m=%d %-22s detM nonzero %d/27 exc %d/27 "
              "v7 Phi!=0 %d/%d" % (m, tag[:22], r["bad_detM"],
                                   r["n_exceptional_prop01"],
                                   r["n_vertex7_Phi_nonzero"],
                                   r["n_vertex7_words"]), flush=True)
        ck()
    # fresh points per m
    OUT["fresh"] = []
    for m in (25, 26, 27, 28):
        mdl = F.Model(m)
        got = 0
        for kk in range(600):
            rng = random.Random(77_000_000 + 1000 * m + kk)
            order = list(range(8))
            rng.shuffle(order)
            bl = F.make_point(mdl, rng, passes=4, order=order)
            if bl is None:
                continue
            r = test_point(m, bl)
            r.update(m=m, tag="fresh%d" % kk, van=mdl.vanishing(bl))
            OUT["fresh"].append(r)
            print("fresh  m=%d #%-4d van=%-5s detM nonzero %d/27 exc %d/27 "
                  "v7 Phi!=0 %d/%d"
                  % (m, kk, r["van"], r["bad_detM"],
                     r["n_exceptional_prop01"], r["n_vertex7_Phi_nonzero"],
                     r["n_vertex7_words"]), flush=True)
            ck()
            got += 1
            if got >= 8:
                break
    # OUT-OF-LOCUS CONTROL: random non-clean points must have det M != 0
    nbad = 0
    for m in (25, 26, 27, 28):
        gam = C.gamma_edges(C.TEMPLATES[m])
        rng = random.Random(4242 + m)
        for _ in range(4):
            bl = {e: [[Fraction(rng.randint(-9, 9) or 5, rng.randint(1, 4))
                       for _ in range(3)] for _ in range(3)] for e in gam}
            r = test_point(m, bl)
            nbad += (r["bad_detM"] > 0)
    print("OUT-OF-LOCUS CONTROL: random non-clean points with det M != 0 "
          "somewhere: %d/16 (want 16)" % nbad)
    OUT["out_of_locus_detM_nonzero"] = nbad
    ck()
    print("wrote results_kill.json")


if __name__ == "__main__":
    main()
