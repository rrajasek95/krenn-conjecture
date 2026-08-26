#!/usr/bin/env python3
"""AUDIT A8 -- fully independent core.  No import from any probe directory.

CONVENTIONS (taken from the problem statement, re-derived here):
  N even sites, blocks A_uv (3x3) with A_uv[i][j] = coeff of colour i at u,
  colour j at v.  Blocks live on the edges of K_N; A_vu = A_uv^T implicitly
  (we store one orientation and transpose on lookup).

  H_w(A) = sum_{M in PM(K_N)} prod_{(u,v) in M, u<v} A_uv[w_u][w_v]

  EXACT  : H_w = 1 on the three constant words, 0 on every mixed word.
  k-near-constant: some colour g with #{i : w_i != g} <= k.
  X_k    : H_w = [w constant] for every k-near-constant word.

Deliberately different code paths from the probes:
  * perfect matchings by recursive "lowest uncovered vertex" expansion,
    materialised as tuples of frozensets (probes use bitmask DP / DP tables);
  * H_w computed by the RAW word definition (sum over all PMs), never a
    product formula, unless explicitly cross-checking;
  * exact arithmetic only (int / Fraction / sympy Rational / GF(p) ints).
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product, permutations
import json
import os
import time

NCOL = 3
COLORS = (0, 1, 2)


def require(cond, detail):
    if not cond:
        raise AssertionError("A8 REQUIRE FAILED: " + str(detail))


# --------------------------------------------------------------- matchings

@lru_cache(maxsize=None)
def _pm_cached(vs):
    return tuple(perfect_matchings(vs))


def perfect_matchings(vertices):
    """All perfect matchings of the complete graph on `vertices`.

    Recursive: always match the smallest remaining vertex.  Returns a list of
    tuples of sorted 2-tuples (edges), each tuple sorted.
    """
    vs = tuple(sorted(vertices))
    if len(vs) % 2:
        return []
    if not vs:
        return [()]
    out = []
    u = vs[0]
    rest = vs[1:]
    for i, v in enumerate(rest):
        sub = rest[:i] + rest[i + 1:]
        for m in _pm_cached(sub):
            out.append(tuple(sorted(((u, v),) + m)))
    return out


def pm_of_graph(vertices, edgeset):
    """Perfect matchings of the graph (vertices, edgeset) -- edgeset a set of
    sorted 2-tuples."""
    return [m for m in perfect_matchings(vertices) if all(e in edgeset for e in m)]


def npm_of_graph(vertices, edgeset):
    return len(pm_of_graph(vertices, edgeset))


# --------------------------------------------------------------- words

def words(n, ncol=NCOL):
    return product(range(ncol), repeat=n)


def offcount(w, ncol=NCOL):
    """min over colours g of #{i : w_i != g}."""
    n = len(w)
    return min(n - w.count(g) for g in range(ncol))


def is_constant(w):
    return len(set(w)) == 1


def profile(w, ncol=NCOL):
    return tuple(w.count(g) for g in range(ncol))


# --------------------------------------------------------------- H, raw

def H_raw(A, w, pms):
    """A: dict {(u,v): 3x3 nested list}, u<v.  w: word.  pms: list of PMs."""
    tot = 0
    for m in pms:
        p = 1
        for (u, v) in m:
            p = p * A[(u, v)][w[u]][w[v]]
            if p == 0:
                break
        tot = tot + p
    return tot


def diag_blocks(t, n=None):
    """t: dict {c: {edge: weight}} -> block dict with diagonal 3x3 blocks.
    If n is given, EVERY edge of K_n gets a block (zeros off the support)."""
    edges = set()
    for c in t:
        edges |= set(t[c].keys())
    if n is not None:
        edges |= set(combinations(range(n), 2))
    A = {}
    for e in edges:
        M = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for c in COLORS:
            M[c][c] = t.get(c, {}).get(e, 0)
        A[e] = M
    return A


def haf(weights, S):
    """hafnian of the weight function `weights` (dict edge->val) on vertex set S."""
    S = tuple(sorted(S))
    if len(S) % 2:
        return 0
    tot = 0
    for m in perfect_matchings(S):
        p = 1
        for e in m:
            p = p * weights.get(e, 0)
            if p == 0:
                break
        tot = tot + p
    return tot


# --------------------------------------------------------------- ladder

def in_Xk(A, n, k, pms=None, ncol=NCOL, one=1, zero=0):
    """Membership in X_k by the RAW definition.  Returns (bool, first failure)."""
    if pms is None:
        pms = perfect_matchings(range(n))
    for w in words(n, ncol):
        if offcount(w, ncol) > k:
            continue
        val = H_raw(A, w, pms)
        want = one if is_constant(w) else zero
        if val != want:
            return False, (w, val, want)
    return True, None


def checkpoint(path, obj):
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=1, default=str)
    print("   [checkpoint] " + os.path.basename(path))
