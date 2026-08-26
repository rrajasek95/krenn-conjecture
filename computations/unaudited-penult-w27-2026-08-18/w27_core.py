#!/usr/bin/env python3
"""UNAUDITED PROBE W27 (the penultimate rung + the skeleton law) -- core.

Pinned HEAD: see PINNED_HEAD.txt.

Builds on W25 (w25_core / w25_walk / w25_decide) which is imported, not
re-implemented, EXCEPT for the pieces this probe needs independently:

  * DIAG_N: the monochrome-diagonal stratum at arbitrary even N.  W25-D0 says
    such a source is three edge sets L_0, L_1, L_2 of K_N with nonzero weights
    and (forced, see below) pairwise disjoint; then for a word w with colour
    classes S_0, S_1, S_2

        H_w = prod_c haf(t^c | S_c),

    so H_w = 0 whenever some |S_c| is odd (W25-D1).

  * THE X_k CONDITIONS ON THE DIAGONAL STRATUM at N = 8, spelled out by
    colour-class profile (see diag8_conditions below).

  * An independent hafnian (recursive over perfect matchings, NOT W25's bitmask
    DP) used as a cross-check.

All arithmetic exact.  No floats.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations

W25BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-x3core-w25-2026-08-15")
W23BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-pure-core-w23-2026-08-15")
for p in (W25BASE, W23BASE):
    if p not in sys.path:
        sys.path.insert(0, p)

import w25_core as C                                              # noqa: E402
import w25_walk as WK                                             # noqa: E402


# --------------------------------------------------------- matchings, masks

def all_pms(sites):
    """Every perfect matching of the vertex set `sites` (tuple of ints)."""
    sites = tuple(sites)
    if not sites:
        return [()]
    out = []
    h = sites[0]
    for k in range(1, len(sites)):
        rest = sites[1:k] + sites[k + 1:]
        for t in all_pms(rest):
            out.append(((h, sites[k]),) + t)
    return out


def pm_norm(M):
    return tuple(sorted(tuple(sorted(e)) for e in M))


class Graph:
    """Edge index bookkeeping for K_n."""

    def __init__(self, n):
        self.n = n
        self.E = list(combinations(range(n), 2))
        self.EI = {e: i for i, e in enumerate(self.E)}
        self.FULL = (1 << len(self.E)) - 1
        self.PMS = [pm_norm(M) for M in all_pms(range(n))]
        self.PMMASK = [self.mask(M) for M in self.PMS]

    def mask(self, edges):
        m = 0
        for e in edges:
            m |= 1 << self.EI[tuple(sorted(e))]
        return m

    def edges(self, mask):
        return [self.E[i] for i in range(len(self.E)) if mask >> i & 1]

    def pms_on(self, sites):
        return [pm_norm(M) for M in all_pms(tuple(sorted(sites)))]

    def npm_on(self, mask, sites):
        """# perfect matchings of (mask) inside the vertex subset `sites`."""
        if len(sites) % 2:
            return 0
        k = 0
        for M in self.pms_on(sites):
            if all((mask >> self.EI[e]) & 1 for e in M):
                k += 1
        return k


# ---------------------------------------------- independent hafnian (control)

def haf_pm(weight, sites):
    """Sum over perfect matchings -- deliberately NOT W25's bitmask DP."""
    sites = tuple(sorted(sites))
    if len(sites) % 2:
        return Fraction(0)
    tot = None
    for M in all_pms(sites):
        pr = None
        for (a, b) in M:
            w = weight(a, b)
            pr = w if pr is None else pr * w
        pr = Fraction(1) if pr is None else pr
        tot = pr if tot is None else tot + pr
    return Fraction(0) if tot is None else tot


# ------------------------------------------------- the diagonal stratum tools

def build_diag(n, Ls, weights, G=None):
    """Ls = (L0,L1,L2) as edge lists (or masks with G given); weights: dict
    (c, edge) -> value  OR  edge -> value (when the classes are disjoint)."""
    sample = next(iter(weights.values()))
    src = C.zero_source(n, 3, C.zeroelt(sample))
    for c, L in enumerate(Ls):
        ed = G.edges(L) if isinstance(L, int) else [tuple(sorted(e)) for e in L]
        for e in ed:
            v = weights[(c, e)] if (c, e) in weights else weights[e]
            src[e][c][c] = v
    return src


def colour_classes(word, ncol=3):
    out = [[] for _ in range(ncol)]
    for i, c in enumerate(word):
        out[c].append(i)
    return out


def diag_H(Ls_w, word, n, ncol=3):
    """H_w on the diagonal stratum: prod_c haf(t^c | S_c).  Ls_w[c] is a dict
    edge -> weight for colour c (missing = 0)."""
    tot = Fraction(1)
    for c in range(ncol):
        S = [i for i in range(n) if word[i] == c]
        if len(S) % 2:
            return Fraction(0)
        if not S:
            continue
        w = Ls_w[c]

        def wt(a, b, w=w):
            return w.get((a, b) if a < b else (b, a), Fraction(0))

        v = haf_pm(wt, S)
        if v == 0:
            return Fraction(0)
        tot = tot * v
    return tot


# ---------------------------------------------------------------- profiles

def profiles(n, ncol=3, kmax=None):
    """All colour-class size profiles (s_0,...,s_{ncol-1}) summing to n, with
    off-count = n - max(s) <= kmax if given."""
    out = []

    def rec(i, rem, acc):
        if i == ncol - 1:
            acc = acc + [rem]
            if kmax is None or n - max(acc) <= kmax:
                out.append(tuple(acc))
            return
        for v in range(rem + 1):
            rec(i + 1, rem - v, acc + [v])

    rec(0, n, [])
    return out


def live_profiles(n, ncol=3, kmax=None):
    """Profiles that are NOT automatically zero (all parts even) and are not
    the constant words."""
    out = []
    for p in profiles(n, ncol, kmax):
        if any(x % 2 for x in p):
            continue
        if max(p) == n:
            continue
        out.append(p)
    return out


__all__ = ["C", "WK", "Graph", "all_pms", "pm_norm", "haf_pm", "build_diag",
           "diag_H", "profiles", "live_profiles", "colour_classes"]
