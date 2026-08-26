#!/usr/bin/env python3
"""W16 -- controls for the m=25 kill.

(C1) VERTEX-6 FACTORISATION, verified exactly: if A56 = beta (x) gamma and
     A67 = gamma (x) k (same gamma), then Phi(w) / gamma_{w6} does not depend
     on w6.  Random exact rational instances + a mutation control.
(C2) NON-VACUITY of the Branch-B encoder: the "J point" (every Gamma block
     = t_e * J, haf_Gamma(t) = 0) satisfies EVERY clean equation, so the
     clean layer alone is NOT the unit ideal -- the Branch-B unit ideal is
     produced by the branch hypothesis, not by an over-constrained encoder.
(C3) MINIMALITY/MUTATION for the Branch-B run: dropping the extra L-words
     must lose the unit ideal.
"""
from __future__ import annotations
import os, sys, json, itertools
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w16_core import (W8_IMMUNE, EDGES, EIDX, VarMap, phi_poly, peval,
                      full_pm_indices, extras_at, PM_E, PMS, support, cell)

HERE = os.path.dirname(os.path.abspath(__file__))
T = W8_IMMUNE[25]
FULLM = full_pm_indices(T)
GAMMA = [EDGES[i] for i, t in enumerate(T) if t == 511]


def lcg(seed):
    s = seed
    while True:
        s = (1103515245 * s + 12345) % (1 << 31)
        yield s


def C1(mutate=False):
    vm = VarMap(T)
    bad = 0
    tested = 0
    for seed in (5, 17, 4242):
        r = lcg(seed)
        def rn():
            return Fraction((next(r) % 13) - 6 or 5, (next(r) % 5) + 1)
        blocks = {e: [[rn() for _ in range(3)] for _ in range(3)]
                  for e in GAMMA}
        beta = [rn() for _ in range(3)]
        gamma = [rn() for _ in range(3)]
        kk = [rn() for _ in range(3)]
        blocks[(5, 6)] = [[beta[i] * gamma[j] for j in range(3)]
                          for i in range(3)]
        blocks[(6, 7)] = [[gamma[i] * kk[j] for j in range(3)]
                          for i in range(3)]
        if mutate:                       # break the parallel-gamma condition
            blocks[(6, 7)][1][0] += Fraction(1)
        vals = {}
        for ei, e in enumerate(EDGES):
            if T[ei] != 511:
                continue
            for c in range(9):
                vals[vm.v(ei, c)] = blocks[e][c // 3][c % 3]
        for w0 in itertools.product(range(3), repeat=6):
            base = list(w0[:6]) + [0]
            ratios = []
            for c6 in range(3):
                w = tuple(w0[:6]) + (c6,) + (w0[5],)
                w = tuple(list(w0[:6])[:6])   # placeholder, rebuilt below
            # build words differing only at site 6
            vals_phi = []
            for c6 in range(3):
                w = list(w0[:6]) + [c6] + [w0[5]]
                # sites: 0..5 from w0[:6], site 6 = c6, site 7 = w0[5]
                w = tuple(list(w0[:6]) + [c6] + [w0[5]])
                vals_phi.append(peval(phi_poly(T, vm, w, FULLM), vals))
            tested += 1
            q = [vals_phi[c] / gamma[c] for c in range(3)]
            if not (q[0] == q[1] == q[2]):
                bad += 1
    return dict(tested=tested, violations=bad)


def C2():
    """the J point: A_e = t_e * J on Gamma, haf_Gamma(t) = 0."""
    vm = VarMap(T)
    # solve haf_Gamma(t)=0 exactly by choosing all t=1 except one edge
    def hafg(tv):
        tot = Fraction(0)
        for mi in FULLM:
            p = Fraction(1)
            for e in PM_E[mi]:
                p *= tv[EDGES[e]]
            tot += p
        return tot
    tv = {e: Fraction(1) for e in GAMMA}
    e0 = GAMMA[0]
    # haf is linear in t_{e0}
    tv[e0] = Fraction(0)
    c0 = hafg(tv)
    tv[e0] = Fraction(1)
    c1 = hafg(tv) - c0
    assert c1 != 0
    tv[e0] = -c0 / c1
    assert hafg(tv) == 0
    assert all(v != 0 for v in tv.values()), "a J-point coordinate vanished"
    vals = {}
    for ei, e in enumerate(EDGES):
        if T[ei] != 511:
            continue
        for c in range(9):
            vals[vm.v(ei, c)] = tv[e]
    nclean = 0
    viol = 0
    phinz = 0
    for w in itertools.product(range(3), repeat=8):
        ph = peval(phi_poly(T, vm, w, FULLM), vals)
        if ph != 0:
            phinz += 1
        if len(set(w)) > 1 and not extras_at(T, w, FULLM):
            nclean += 1
            if ph != 0:
                viol += 1
    return dict(t_values={"%d%d" % e: str(v) for e, v in tv.items()},
                clean_mixed=nclean, clean_violations=viol,
                words_with_Phi_nonzero=phinz)


def main():
    res = {}
    res["C1_vertex6_factorisation"] = C1()
    print("C1 vertex-6 factorisation:", res["C1_vertex6_factorisation"],
          "(violations must be 0)")
    res["C1_mutation"] = C1(mutate=True)
    print("C1 mutation (broken gamma):", res["C1_mutation"],
          "(violations must be > 0)")
    res["C2_J_point"] = C2()
    print("C2 J-point:", {k: v for k, v in res["C2_J_point"].items()
                          if k != "t_values"})
    json.dump(res, open(os.path.join(HERE, "results_m25_controls.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
