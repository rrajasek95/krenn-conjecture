#!/usr/bin/env python3
"""W19 -- fast EXPLICIT search for rank-two (bracket) points of Phi == 0.

Companion to w19_bracket.py (which asks the same question by Groebner).
Here the search is finite and constructive:

  A_uv[i][j] = s_uv * det(p_u(i), p_v(j)),  p_t(c) in Q^2 generic.

Phi(w) = sum_{M in F(Gamma)} z_M X_M(w),  z_M = prod_{e in M} s_e,
X_M(w) = prod_{uv in M} det(p_u(w_u), p_v(w_v)).  Phi is multilinear of
degree one in each site, so vanishing on all 3^8 words is the same as the
bracket identity sum_M z_M [M] = 0.

STEP 1  compute the exact kernel K = {z : sum_M z_M X_M(w) = 0 for all w}.
STEP 2  enumerate SIGN assignments s: E -> {+1,-1} modulo the vertex gauge
        s_uv -> lam_u lam_v s_uv (which multiplies every matching monomial
        by prod_t lam_t, hence preserves the kernel), and test membership
        z(s) in K exactly.  2^(|E|-7) classes -- a complete finite search
        of the sign stratum.
STEP 3  if a sign assignment works, BUILD the explicit block matrices,
        verify Phi_w = 0 on all 6561 words by an independent exact
        evaluation, verify all 9|Gamma| cells are nonzero, and report the
        rank of every block and whether ANY site factors.

POSITIVE CONTROL: K_4 must be found feasible (Grassmann-Plucker), with the
explicit point exhibited and independently verified.
NEGATIVE CONTROL: C_4 (two matchings) must be found infeasible.
MUTATION CONTROL: a deliberately corrupted X_M table must change the
verdict on the K_4 control.
"""
from __future__ import annotations
import os
import sys
import json
import itertools
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w19_core import (EDGES, W8_IMMUNE, gamma_edges, rank_of)
from w19_bracket import (rref, kernel_basis, pdata, det2, matchings_of,
                         bracket_matrix, spanning_tree)


def in_span(basis, v, ncols):
    """exact membership of v in the row span of `basis`."""
    R, piv = rref(basis, ncols)
    w = list(v)
    for i, c in enumerate(piv):
        if w[c]:
            f = w[c]
            w = [a - f * b for a, b in zip(w, R[i])]
    return not any(w)


def sign_search(edges, n, P=None, verbose=False):
    if P is None:
        P = pdata(n, seed=7)
    words = list(itertools.product(range(3), repeat=n))
    Ms, rows = bracket_matrix(edges, n, P, words)
    ker = kernel_basis(rows, len(Ms))
    tree = set(spanning_tree(edges, n))
    free = [e for e in edges if e not in tree]
    hits = []
    for bits in range(1 << len(free)):
        s = {e: Fraction(1) for e in edges}
        for k, e in enumerate(free):
            if (bits >> k) & 1:
                s[e] = Fraction(-1)
        z = []
        for M in Ms:
            v = Fraction(1)
            for e in M:
                v *= s[e]
            z.append(v)
        if not ker:
            continue
        if in_span(ker, z, len(Ms)):
            hits.append({("%d%d" % e): int(s[e]) for e in edges})
            if verbose:
                print("   sign hit:", hits[-1], flush=True)
    return dict(n_matchings=len(Ms), kernel_dim=len(ker),
                n_sign_classes=1 << len(free), n_sign_hits=len(hits),
                sign_hits=hits[:5])


def build_point(edges, n, signs, P=None):
    """explicit blocks from a sign assignment; exact."""
    if P is None:
        P = pdata(n, seed=7)
    B = {}
    for (u, v) in edges:
        s = Fraction(signs["%d%d" % (u, v)])
        B[(u, v)] = [[s * det2(P[u][i], P[v][j]) for j in range(3)]
                     for i in range(3)]
    return B


def verify_point(edges, n, B):
    Ms = matchings_of(edges, n)
    bad = 0
    for w in itertools.product(range(3), repeat=n):
        tot = Fraction(0)
        for M in Ms:
            p = Fraction(1)
            for (u, v) in M:
                p *= B[(u, v)][w[u]][w[v]]
            tot += p
        if tot != 0:
            bad += 1
    zero_cells = sum(1 for e in edges for row in B[e] for x in row if x == 0)
    ranks = {("%d%d" % e): rank_of(B[e]) for e in edges}
    # site factorisation test
    fac = []
    for t in range(n):
        cols = []
        for (u, v) in edges:
            if u == t:
                for j in range(3):
                    cols.append([B[(u, v)][i][j] for i in range(3)])
            elif v == t:
                for j in range(3):
                    cols.append([B[(u, v)][j][i] for i in range(3)])
        if cols and rank_of([[cols[k][i] for k in range(len(cols))]
                             for i in range(3)]) == 1:
            fac.append(t)
    return dict(words_with_Phi_nonzero=bad, zero_cells=zero_cells,
                block_ranks=ranks, factoring_sites=fac)


def main():
    out = {}
    K4 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    C4 = [(0, 1), (1, 2), (2, 3), (0, 3)]
    r = sign_search(K4, 4, verbose=True)
    out["CONTROL_K4"] = r
    print("CONTROL K4 sign search:", r, flush=True)
    if r["sign_hits"]:
        B = build_point(K4, 4, r["sign_hits"][0])
        v = verify_point(K4, 4, B)
        out["CONTROL_K4_point"] = dict(
            signs=r["sign_hits"][0], blocks={("%d%d" % e):
                                             [[str(x) for x in row]
                                              for row in B[e]]
                                             for e in K4}, **v)
        print("CONTROL K4 explicit point:", v, flush=True)
    out["CONTROL_C4"] = sign_search(C4, 4)
    print("CONTROL C4 sign search:", out["CONTROL_C4"], flush=True)
    # MUTATION CONTROL: corrupt the bracket table -> K4 must stop working
    import w19_bracket as WB
    orig = WB.det2

    def bad_det(p, q):
        return p[0] * q[1] + p[1] * q[0]        # symmetric, not a bracket
    WB.det2 = bad_det
    globals()["det2"] = bad_det
    out["MUTATION_K4"] = sign_search(K4, 4)
    WB.det2 = orig
    globals()["det2"] = orig
    print("MUTATION K4 (symmetric fake bracket):", out["MUTATION_K4"],
          "(kernel_dim / hits must drop)", flush=True)

    for m in (25, 26, 27, 28):
        ge = gamma_edges(W8_IMMUNE[m])
        r = sign_search(ge, 8, verbose=True)
        out["W8_m%d" % m] = r
        print("W8 Gamma m=%d:" % m, r, flush=True)
        if r["sign_hits"]:
            B = build_point(ge, 8, r["sign_hits"][0])
            out["W8_m%d_point" % m] = verify_point(ge, 8, B)
            print("   explicit point:", out["W8_m%d_point" % m], flush=True)
    K8 = list(EDGES)
    r = sign_search(K8, 8)
    out["K8"] = r
    print("K8:", r, flush=True)
    json.dump(out, open(os.path.join(HERE, "results_bracket2.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
