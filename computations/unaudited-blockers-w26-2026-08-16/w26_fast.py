#!/usr/bin/env python3
"""W26 -- fast exact Phi via the L-subset expansion.  UNAUDITED.  Exact.

    Phi(x,y) = sum_{T subset of L, |T| even}
                 haf(Lambda|_T) * prod_{p not in T} D_p * haf(Rho|_{sigma T})
with Lambda = (A_ab[x_a][x_b])_{a,b in L}  (K_4, always present),
     D_p    = A_{p,sigma p}[x_p][y_{sigma p}]  (0 if that sigma edge is absent),
     Rho    = (A_jk[y_j][y_k])_{j,k in R}      (0 off the R-graph).
Verified against the from-the-definition engine in w26_core (w26_fastchk).
"""
from __future__ import annotations

import os
import sys
from fractions import Fraction
from itertools import combinations

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w26_core as C                                              # noqa: E402

LSUB = [()] + [t for t in combinations(C.L, 2)] + [tuple(C.L)]
RPAIR = {(4, 5): (6, 7), (4, 6): (5, 7), (4, 7): (5, 6)}


def _z(gs, e):
    return e in gs


def phi_fast(bl, m, w):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    x, y = w[:4], w[4:]
    Z = Fraction(0)

    def rr(j, k):
        e = (min(j, k), max(j, k))
        return bl[e][y[e[0] - 4]][y[e[1] - 4]] if e in gs else Z
    ll = {(a, b): bl[(a, b)][x[a]][x[b]] for a, b in combinations(C.L, 2)}
    D = {p: (bl[(p, C.SIG[p])][x[p]][y[C.SIG[p] - 4]]
             if (p, C.SIG[p]) in gs else Z) for p in C.L}
    hafL = (ll[(0, 1)] * ll[(2, 3)] + ll[(0, 2)] * ll[(1, 3)]
            + ll[(0, 3)] * ll[(1, 2)])
    hafR = (rr(4, 5) * rr(6, 7) + rr(4, 6) * rr(5, 7) + rr(4, 7) * rr(5, 6))
    tot = D[0] * D[1] * D[2] * D[3] + hafL * hafR
    for i, j in combinations(C.L, 2):
        p, q = [t for t in C.L if t not in (i, j)]
        tot += ll[(i, j)] * rr(C.SIG[i], C.SIG[j]) * D[p] * D[q]
    return tot


class Model:
    """precomputed per-m data for fast repeated evaluation."""

    def __init__(self, m):
        self.m = m
        self.T = C.TEMPLATES[m]
        self.gam = C.gamma_edges(self.T)
        self.gs = set(self.gam)
        self.clean = C.clean_words(m)
        self.live = C.live_singles(m)
        self.sing = C.single_edges(self.T)

    def phi(self, bl, w):
        return phi_fast(bl, self.m, w)

    def clean_ok(self, bl):
        return all(phi_fast(bl, self.m, w) == 0 for w in self.clean)

    def vanishing(self, bl):
        return all(phi_fast(bl, self.m, w) == 0 for w in C.WORDS)

    def allnz(self, bl):
        return all(bl[e][i][j] != 0 for e in self.gam
                   for i in range(3) for j in range(3))


def site_solve(mdl, bl, t, rng, lo=-6, hi=6):
    """re-solve the blocks incident to vertex t from the clean equations."""
    nb = sorted({s for e in mdl.gam for s in e if t in e and s != t})
    ncols = 3 * len(nb)
    rows = {0: [], 1: [], 2: []}
    for w in mdl.clean:
        r = [Fraction(0)] * ncols
        for k, s in enumerate(nb):
            vs = tuple(v for v in range(8) if v != t and v != s)
            r[3 * k + w[s]] += C.haf_on(bl, mdl.gs, vs, w)
        if any(r):
            rows[w[t]].append(r)
    newv = {}
    for c in range(3):
        Kb = C.kernel_basis(rows[c], ncols)
        if not Kb:
            return False
        for _ in range(300):
            co = [Fraction(rng.randint(lo, hi)) for _ in Kb]
            v = [sum(co[i] * Kb[i][j] for i in range(len(Kb)))
                 for j in range(ncols)]
            if all(zz != 0 for zz in v):
                break
        else:
            return False
        newv[c] = v
    save = {e: [r[:] for r in bl[e]] for e in mdl.gam}
    for k, s in enumerate(nb):
        e = (min(t, s), max(t, s))
        for c in range(3):
            for d in range(3):
                if e[0] == t:
                    bl[e][c][d] = newv[c][3 * k + d]
                else:
                    bl[e][d][c] = newv[c][3 * k + d]
    if not mdl.clean_ok(bl):
        for e in mdl.gam:
            bl[e] = save[e]
        return False
    return True


def make_point(mdl, rng, passes=5, order=None):
    bl = {e: [[Fraction(rng.randint(-6, 6) or 3, rng.randint(1, 3))
               for _ in range(3)] for _ in range(3)] for e in mdl.gam}
    order = list(range(8)) if order is None else list(order)
    for _ in range(passes):
        for t in order:
            site_solve(mdl, bl, t, rng)
    if mdl.clean_ok(bl) and mdl.allnz(bl):
        return bl
    return None
