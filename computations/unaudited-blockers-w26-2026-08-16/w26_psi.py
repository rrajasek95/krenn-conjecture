#!/usr/bin/env python3
"""W26 -- the R-VERTEX SLICE LEMMA, machine-derived for every (m, k).
UNAUDITED.  Exact only (sympy over Q).

For k in R = {4,5,6,7} let B(k) be the Gamma blocks incident to k.  Phi is
LINEAR in the y_k-slice of each such block and involves no other
y_k-dependence, so

      Phi(x,y)  =  sum_{B in B(k)}  Psi_B(x, y_{R-k})  *  B[slice at y_k].

Hence, along any clean-word family in which y_k runs over all three letters
with the other coordinates fixed, the |B(k)| slice vectors of K^3 satisfy
sum Psi_B v_B = 0.  If |B(k)| = 3 and the three vectors are INDEPENDENT
then Psi_B = 0 for all three; this file computes, symbolically, what that
forces -- and in particular exhibits the contradiction at m=25/26 and the
forced value of the missing-edge cell at m=27.

|B(k)| = deg_R(k) + 1 if the sigma edge (sigma^-1 k, k) is present:
    m=25: k=4:3  k=5:3  k=6:2  k=7:3       (R = C_4, no (3,6))
    m=26: k=4:3  k=5:3  k=6:3  k=7:3       (R = C_4)
    m=27: k=4:4  k=5:3  k=6:4  k=7:3       (R = C_4 + (4,6))
    m=28: all 4                            (R = K_4)
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
import sympy as sp                                                # noqa: E402

OUT = {"_header": "UNAUDITED W26 R-vertex slice lemma, per (m,k)."}

# symbols
l01, l02, l03, l12, l13, l23 = sp.symbols("l01 l02 l03 l12 l13 l23")
LL = {(0, 1): l01, (0, 2): l02, (0, 3): l03,
      (1, 2): l12, (1, 3): l13, (2, 3): l23}
D = {p: sp.Symbol("D%d" % p) for p in range(4)}
RS = {(4, 5): sp.Symbol("r45"), (4, 6): sp.Symbol("r46"),
      (4, 7): sp.Symbol("r47"), (5, 6): sp.Symbol("r56"),
      (5, 7): sp.Symbol("r57"), (6, 7): sp.Symbol("r67")}
H = l01 * l23 + l02 * l13 + l03 * l12


def phi_sym(m):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))

    def rr(a, b):
        e = (min(a, b), max(a, b))
        return RS[e] if e in gs else sp.Integer(0)

    def dd(p):
        return D[p] if (p, C.SIG[p]) in gs else sp.Integer(0)
    hafR = rr(4, 5) * rr(6, 7) + rr(4, 6) * rr(5, 7) + rr(4, 7) * rr(5, 6)
    tot = dd(0) * dd(1) * dd(2) * dd(3) + H * hafR
    for i, j in combinations(range(4), 2):
        p, q = [t for t in range(4) if t not in (i, j)]
        tot += LL[(i, j)] * rr(C.SIG[i], C.SIG[j]) * dd(p) * dd(q)
    return sp.expand(tot)


def blocks_at(m, k):
    """the Gamma blocks touching k, as (label, symbol)."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    out = []
    p = C.SIGINV[k]
    if (p, k) in gs:
        out.append(("D%d" % p, D[p]))
    for k2 in C.R:
        if k2 == k:
            continue
        e = (min(k, k2), max(k, k2))
        if e in gs:
            out.append(("r%d%d" % e, RS[e]))
    return out


def main():
    print("=" * 76)
    res = {}
    for m in (25, 26, 27, 28):
        PH = phi_sym(m)
        # (0) sanity: the symbolic Phi reproduces the numeric Phi
        for k in C.R:
            bl = blocks_at(m, k)
            labs = [b[0] for b in bl]
            syms = [b[1] for b in bl]
            # linearity check + coefficient extraction
            psi = [sp.expand(sp.diff(PH, s)) for s in syms]
            rec = sp.expand(sum(p * s for p, s in zip(psi, syms)))
            lin_ok = sp.simplify(rec - PH) == 0
            key = "m%d_k%d" % (m, k)
            entry = dict(n_blocks=len(bl), blocks=labs,
                         linear_exact=bool(lin_ok),
                         psi={lab: str(sp.factor(p))
                              for lab, p in zip(labs, psi)})
            print("m=%d  k=%d  blocks=%s  Phi linear&exhaustive: %s"
                  % (m, k, labs, lin_ok))
            for lab, p in zip(labs, psi):
                print("      Psi[%-4s] = %s" % (lab, sp.factor(p)))
            if len(bl) == 3:
                # solve the two R-slice Psi's for their R-cells, put back
                rsyms = [s for lab, s in zip(labs, syms)
                         if lab.startswith("r")]
                dsym = [s for lab, s in zip(labs, syms)
                        if lab.startswith("D")]
                eqs = [p for lab, p in zip(labs, psi) if lab.startswith("r")]
                unk = []
                # each Psi[r..] is linear in exactly one *other* R cell
                for eq in eqs:
                    cand = [s for s in RS.values()
                            if s not in rsyms and sp.diff(eq, s) != 0]
                    unk.append(cand)
                sol = sp.solve(eqs, sum(unk, []), dict=True)
                entry["solve_unknowns"] = [str(u) for u in sum(unk, [])]
                if sol:
                    pd = [p for lab, p in zip(labs, psi)
                          if lab.startswith("D")][0]
                    red = sp.factor(sp.simplify(pd.subs(sol[0])))
                    entry["Psi_D_reduced"] = str(red)
                    print("      => with Psi[r*] = 0 :  Psi[%s] = %s"
                          % ([l for l in labs if l.startswith("D")][0], red))
                    # is it a nonzero monomial (a CONTRADICTION)?
                    num, den = sp.fraction(sp.together(red))
                    fac = sp.factor_list(sp.expand(num))
                    monomial = all(f[0].is_Symbol or f[0].is_Number
                                   for f in fac[1])
                    entry["contradiction_monomial"] = bool(monomial)
                    print("         numerator = %s   -> pure monomial "
                          "(=> CONTRADICTION when all cells nonzero): %s"
                          % (sp.factor(num), monomial))
            res[key] = entry
    OUT["per_mk"] = res

    # ---------- numeric control: the Psi decomposition equals Phi
    rng = random.Random(31415)
    bad = tot = 0
    for m in (25, 26, 27, 28):
        gam = C.gamma_edges(C.TEMPLATES[m])
        gs = set(gam)
        for _ in range(3):
            bl = {e: [[Fraction(rng.randint(-9, 9) or 5, rng.randint(1, 4))
                       for _ in range(3)] for _ in range(3)] for e in gam}
            for _t in range(40):
                w = tuple(rng.randrange(3) for _ in range(8))
                x, y = w[:4], w[4:]
                sub = {}
                for a, b in combinations(range(4), 2):
                    sub[LL[(a, b)]] = bl[(a, b)][x[a]][x[b]]
                for p in range(4):
                    e = (p, C.SIG[p])
                    sub[D[p]] = bl[e][x[p]][y[C.SIG[p] - 4]] \
                        if e in gs else 0
                for a, b in combinations(C.R, 2):
                    sub[RS[(a, b)]] = bl[(a, b)][y[a - 4]][y[b - 4]] \
                        if (a, b) in gs else 0
                val = phi_sym(m).subs(sub)
                tot += 1
                bad += (sp.Rational(val) != sp.Rational(C.phi(bl, gs, w)))
    print("=" * 76)
    print("CONTROL symbolic Phi vs definition: %d/%d mismatches" % (bad, tot))
    OUT["symbolic_phi_mismatch"] = bad
    OUT["symbolic_phi_tests"] = tot
    json.dump(OUT, open(os.path.join(HERE, "results_psi.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
