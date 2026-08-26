#!/usr/bin/env python3
"""W26 -- THEOREM W26-M* : the L-VERTEX master relation (dual of W26-M).
UNAUDITED.  Exact only (sympy over Q).

Phi = sum_{T subset L, |T| even} haf(Lambda_T) prod_{p not in T} D_p
      haf(Rho_{sigma T})  is linear in the x_p-slice of each Gamma block at
an L-vertex p: the three L-blocks A_pa (a != p) and the sigma block
A_{p,sigma p}.  Writing

    Psi[D_p] = prod_{q!=p} D_q + sum_{q!=p} D_q l_ij r_{sigma i sigma j}
               ({i,j} = L\\{p,q})                    -- coefficient of D_p
    Xi_a     = r_{sigma p sigma a} D_b D_c + l_bc * hafR
               ({b,c} = L\\{p,a})                    -- coefficient of l_pa

the MASTER RELATION* is

    hafR * Psi[D_p]  =  sum_{a != p}  D_a * r_{sigma b sigma c} * Xi_a ,
                                       ({b,c} = L\\{p,a})

exactly dual to W26-M under  l <-> r,  hafL <-> hafR,  L <-> R.
Hence, multiplying the x_p-slice equation by hafR,

    hafR * Phi(x with x_p = s)  =  sum_{a != p} Xi_a * V_a(s),
    V_a(s) := D_a r_{sigma b sigma c} * A_{p,sigma p}[s][y_{sigma p}]
              + hafR * A_{pa}[s][x_a] ,

THREE vectors, for every m and every L-vertex p.  Dichotomy along any clean
family in which x_p runs over all three letters:
    det[V_a1,V_a2,V_a3] = 0    OR    Xi_a = 0 for all a != p.

COROLLARY*.  If the R-edge (sigma p, sigma a) is ABSENT then
Xi_a = l_bc * hafR, so the second branch forces hafR(y) = 0.  Absent edges:
(4,6) at m=25,26 -> (p,a) with {sigma p,sigma a}={4,6} i.e. {p,a}={1,3};
(5,7) at m=25,26,27 -> {p,a}={0,2}.  At m=25 also every sigma-block term
with p=3 or a=3 drops (A_36 absent).
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import combinations

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w26_core as C                                              # noqa: E402
import w26_psi as PS                                              # noqa: E402
import sympy as sp                                                # noqa: E402

OUT = {"_header": "UNAUDITED W26 Theorem W26-M* (L-vertex master relation)."}


def rsym(a, b, gs):
    e = (min(a, b), max(a, b))
    return PS.RS[e] if e in gs else sp.Integer(0)


def main():
    hafR_sym = {}
    ok_all = True
    rec = {}
    for m in (25, 26, 27, 28):
        gs = set(C.gamma_edges(C.TEMPLATES[m]))
        PH = PS.phi_sym(m)
        zsub = {PS.D[t]: 0 for t in range(4) if (t, C.SIG[t]) not in gs}
        zsub.update({PS.RS[e]: 0 for e in PS.RS if e not in gs})

        def Z(x):
            return sp.expand(sp.expand(x).subs(zsub))
        hafR = Z(rsym(4, 5, gs) * rsym(6, 7, gs)
                 + rsym(4, 6, gs) * rsym(5, 7, gs)
                 + rsym(4, 7, gs) * rsym(5, 6, gs))
        hafR_sym[m] = hafR
        for p in range(4):
            PsiD = Z(sp.diff(PH, PS.D[p])) if (p, C.SIG[p]) in gs \
                else sp.Integer(0)
            rhs = sp.Integer(0)
            for a in range(4):
                if a == p:
                    continue
                b, c = [t for t in range(4) if t not in (p, a)]
                lbc = PS.LL[(min(b, c), max(b, c))]
                Xi = Z(rsym(C.SIG[p], C.SIG[a], gs) * PS.D[b] * PS.D[c]
                       + lbc * hafR)
                # cross-check Xi against the true coefficient of l_pa
                lpa = PS.LL[(min(p, a), max(p, a))]
                Xi_true = Z(sp.diff(PH, lpa))
                if sp.simplify(sp.expand(Xi - Xi_true)) != 0:
                    print("  !! Xi mismatch m=%d p=%d a=%d" % (m, p, a))
                    ok_all = False
                rhs += Z(PS.D[a]) * rsym(C.SIG[b], C.SIG[c], gs) * Xi
            ok = sp.simplify(sp.expand(hafR * PsiD - rhs)) == 0
            ok_all &= ok
            rec["m%d_p%d" % (m, p)] = bool(ok)
            print("  m=%d p=%d  hafR*Psi[D%d] == sum_a D_a r_bc Xi_a : %s"
                  % (m, p, p, ok))
    OUT["dual_relation"] = rec
    OUT["dual_all_ok"] = bool(ok_all)
    # MUTATION control: use r_{sigma p sigma a} instead of r_{sigma b sigma c}
    bad = 0
    for m in (26, 28):
        gs = set(C.gamma_edges(C.TEMPLATES[m]))
        PH = PS.phi_sym(m)
        hafR = hafR_sym[m]
        for p in range(4):
            PsiD = sp.expand(sp.diff(PH, PS.D[p]))
            rhs = sp.Integer(0)
            for a in range(4):
                if a == p:
                    continue
                b, c = [t for t in range(4) if t not in (p, a)]
                lpa = PS.LL[(min(p, a), max(p, a))]
                Xi = sp.expand(sp.diff(PH, lpa))
                rhs += PS.D[a] * rsym(C.SIG[p], C.SIG[a], gs) * Xi   # WRONG
            bad += (sp.simplify(sp.expand(hafR * PsiD - rhs)) != 0)
    print("  MUTATION (wrong r index): fails %d/8 (want 8)" % bad)
    OUT["dual_mutation_fails"] = bad
    json.dump(OUT, open(os.path.join(HERE, "results_dual.json"), "w"),
              indent=1, default=str)
    print("wrote results_dual.json")


if __name__ == "__main__":
    main()
