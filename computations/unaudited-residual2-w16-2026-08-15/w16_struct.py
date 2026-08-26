#!/usr/bin/env python3
"""W16 -- the STRUCTURE identity for family (R) and its exact verification.

THE IDENTITY (derived here, verified exactly below).  Let L = {0,1,2,3},
R = {4,5,6,7}; sigma the Gamma cross-matching (0-7, 1-4, 2-5, 3-6 in W8's
family; only some of those edges are in Gamma at m < 28).  Every perfect
matching of Gamma uses an even set S of cross edges, so

    Phi(x,y) = sum_{S subset L, |S| even}
                 (prod_{i in S} c_i(x_i)) haf_L(L\\S)(x) haf_R(R\\sigma(S))(y)

with c_i(x_i) = A_{i,sigma(i)}[x_i][y_{sigma(i)}] (0 if that edge is not in
Gamma).  FIX y.  Put rho = haf_R(R)(y) = P_R(y), and for an L-edge {i,j}
put k_ij = haf_R(R \\ sigma({k,l}))(y) where {k,l} = L\\{i,j} -- i.e. the
R-hafnian of the two R-vertices matched to the OTHER two L-vertices, and

    N_ij[x_i][x_j] = rho * A_ij[x_i][x_j] + k_ij * c_i(x_i) c_j(x_j).

THEN, IDENTICALLY IN ALL CELL VARIABLES AND ALL x,

    rho * Phi(x,y) = N_01 N_23 + N_02 N_13 + N_03 N_12      (Theorem W16-1)

because the coefficient of c_0c_1c_2c_3 on the right is
k_01 k_23 + k_02 k_13 + k_03 k_12 = haf_R(R)(y) = rho, matching the left.
The mirror identity (L <-> R) holds verbatim.

CONSEQUENCE USED THROUGHOUT (Theorem W16-2, "rank <= 2 law"): if a
3-term hafnian identity  N1[a][b]N2[c][d] + N3[a][c]N4[b][d] +
N5[a][d]N6[b][c] = 0  holds for ALL a,b,c,d, then freezing the two indices
that do NOT touch a chosen matrix exhibits that matrix, scaled by a
nonzero entry of its partner, as a sum of two rank-<=1 matrices; hence
every one of the six has rank <= 2.
"""
from __future__ import annotations
import os, sys, json
from itertools import product
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w16_core import (EDGES, EIDX, FULL, W8_IMMUNE, VarMap, cell, support,
                      PM_E, PMS, padd, psub, pmul, pscale, pmon, peval,
                      phi_poly, full_pm_indices, singles, word_clean,
                      extras_at, gamma_edges, pms_of_graph)

L = (0, 1, 2, 3)
R = (4, 5, 6, 7)
SIGMA = {0: 7, 1: 4, 2: 5, 3: 6}          # W8's Gamma cross matching
SIGMA_INV = {v: k for k, v in SIGMA.items()}


def in_gamma(T, u, v):
    return T[EIDX[(min(u, v), max(u, v))]] == FULL


def haf_sub(T, vm, w, verts):
    """sum over perfect matchings of Gamma restricted to `verts`"""
    verts = tuple(sorted(verts))
    if not verts:
        return {(): Fraction(1)}
    out = {}
    a = verts[0]
    for i in range(1, len(verts)):
        b = verts[i]
        if not in_gamma(T, a, b):
            continue
        rest = verts[1:i] + verts[i + 1:]
        sub = haf_sub(T, vm, w, rest)
        e = EIDX[(a, b)]
        out = padd(out, pmul({(vm.v(e, cell(e, w)),): Fraction(1)}, sub))
    return out


def cross_c(T, vm, w, i):
    """c_i(x_i) as a polynomial (a single variable), or 0 if not in Gamma"""
    j = SIGMA[i]
    if not in_gamma(T, i, j):
        return {}
    e = EIDX[(min(i, j), max(i, j))]
    return {(vm.v(e, cell(e, w)),): Fraction(1)}


def N_matrix(T, vm, w, i, j, side="L"):
    """N_ij for the fixed opposite-side word; returns the polynomial."""
    if side == "L":
        other = tuple(v for v in L if v not in (i, j))
        rho = haf_sub(T, vm, w, R)
        k = haf_sub(T, vm, w, tuple(SIGMA[v] for v in other))
    else:
        other = tuple(v for v in R if v not in (i, j))
        rho = haf_sub(T, vm, w, L)
        k = haf_sub(T, vm, w, tuple(SIGMA_INV[v] for v in other))
    e = EIDX[(min(i, j), max(i, j))]
    aij = {} if T[e] != FULL else {(vm.v(e, cell(e, w)),): Fraction(1)}
    ci = cross_c(T, vm, w, i if side == "L" else SIGMA_INV[i])
    cj = cross_c(T, vm, w, j if side == "L" else SIGMA_INV[j])
    return padd(pmul(rho, aij), pmul(k, pmul(ci, cj)))


def check_identity(T, side="L", verbose=False):
    """Verify rho*Phi = N N + N N + N N exactly on ALL 6561 words."""
    vm = VarMap(T)
    fullm = full_pm_indices(T)
    pairings = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))] \
        if side == "L" else [((4, 5), (6, 7)), ((4, 6), (5, 7)),
                             ((4, 7), (5, 6))]
    bad = 0
    for w in product(range(3), repeat=8):
        rho = haf_sub(T, vm, w, R if side == "L" else L)
        lhs = pmul(rho, phi_poly(T, vm, w, fullm))
        rhs = {}
        for (i, j), (k, l) in pairings:
            rhs = padd(rhs, pmul(N_matrix(T, vm, w, i, j, side),
                                 N_matrix(T, vm, w, k, l, side)))
        if psub(lhs, rhs):
            bad += 1
            if verbose and bad < 3:
                print("MISMATCH at", w)
    return bad


def main():
    out = {}
    for m in (24, 25, 26, 27, 28):
        T = W8_IMMUNE[m]
        bl = check_identity(T, "L")
        br = check_identity(T, "R")
        out[m] = dict(L_side_mismatches=bl, R_side_mismatches=br)
        print("m=%d  W16-1 identity mismatches: L-side %d, R-side %d"
              % (m, bl, br))
    # MUTATION CONTROL: corrupt one k_ij and require the check to FAIL.
    print("\nMUTATION CONTROLS (identity checker must reject wrong N):")
    g = globals()
    orig = g["N_matrix"]
    def bad_N(T, vm, w, i, j, side="L"):
        p = orig(T, vm, w, i, j, side)
        return pscale(p, 2) if (i, j) == (0, 2) else p
    def bad_N2(T, vm, w, i, j, side="L"):
        # drop the cross term entirely (N = rho*A only)
        if side == "L":
            other = tuple(v for v in L if v not in (i, j))
        else:
            other = tuple(v for v in R if v not in (i, j))
        rho = haf_sub(T, vm, w, R if side == "L" else L)
        e = EIDX[(min(i, j), max(i, j))]
        aij = {} if T[e] != FULL else {(vm.v(e, cell(e, w)),): Fraction(1)}
        del other
        return pmul(rho, aij)
    ctrl = {}
    for nm, fn in (("scale_N02_by_2", bad_N), ("drop_cross_term", bad_N2)):
        g["N_matrix"] = fn
        ctrl[nm] = check_identity(W8_IMMUNE[26], "L")
        print("  %-18s -> mismatches = %d (must be > 0)" % (nm, ctrl[nm]))
    g["N_matrix"] = orig
    out["mutation_controls"] = ctrl
    json.dump(out, open(os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "results_struct.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
