#!/usr/bin/env python3
"""UNAUDITED PROBE (W10) -- mixed-exact sources with pure cancellation.

Pinned HEAD: see PINNED_HEAD.txt (c4eb9ebea3819d3e13e2ce12e7d2c37116a02845).
Plan: notes/2026-08-15-resolution-master-plan.md (v10 addendum, named follow-up).
NOTHING HERE IS A PROVED CLAIM OF THE PROJECT -- it is probe output.

THE QUESTION (W9 soft spot 1).  Does there exist a MIXED-EXACT source
(H_w = 0 for every non-constant word w; NO condition on the three constant
words) whose TEMPLATE has all three pure fibres NONEMPTY, but with
H_{c^N} = 0 for some colour c -- necessarily by cancellation among >= 2
nonzero matching products?

Model (matches w6_core.py / w9_core.py exactly, re-implemented here
independently as a cross-check):
  * N named vertices, K_N; every unordered pair uv carries an arbitrary
    3x3 matrix A_uv over Q (row index = colour at u, column index at v).
  * H(A)_w = sum over perfect matchings M of prod_{uv in M} A_uv[w_u][w_v].
  * EXACT      : H_w = 1 on the three constant words, 0 on all mixed words.
  * MIXED-EXACT: H_w = 0 on all mixed words (constants unconstrained).

Template/admissibility vocabulary (W9's w9_template.py, restated):
 (T4) each of the 3 constant words has fibre >= 1        "no missing pure"
 (T5) every vertex meets >= 3 nonempty blocks
 (T6) every (vertex, colour) slot carries a cell
 (S)  NO mixed word has fibre exactly 1                  "singleton-free"
ADMISSIBLE := (T4) and (T5) and (T6) and (S).

Exact arithmetic only (Fraction / int).  Floats appear only in scripts
explicitly labelled SEARCH, and every verdict derived from a float search is
re-verified exactly here.
"""

from __future__ import annotations

from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product

COLORS = (0, 1, 2)


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


# ------------------------------------------------------------ combinatorics

@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple) -> tuple:
    """All perfect matchings of the complete graph on ``vertices``."""
    if not vertices:
        return ((),)
    head = vertices[0]
    out = []
    for i in range(1, len(vertices)):
        rest = vertices[1:i] + vertices[i + 1:]
        for tail in perfect_matchings(rest):
            out.append(((head, vertices[i]),) + tail)
    return tuple(out)


def edges(size):
    return tuple(combinations(range(size), 2))


def zero_source(size):
    return {e: [[F(0)] * 3 for _ in range(3)] for e in edges(size)}


def oriented(source, u, v):
    if u < v:
        return source[(u, v)]
    t = source[(v, u)]
    return [[t[b][a] for b in COLORS] for a in COLORS]


# ------------------------------------------------------------------ hafnian

def hafnian_word(source, size, word):
    """H(A)_word, exact.  ``word`` is a tuple of length ``size``."""
    total = F(0)
    for M in perfect_matchings(tuple(range(size))):
        term = F(1)
        for u, v in M:
            x = source[(u, v)][word[u]][word[v]]
            if x == 0:
                term = F(0)
                break
            term *= x
        total += term
    return total


def full_tensor(source, size):
    return {w: hafnian_word(source, size, w)
            for w in product(COLORS, repeat=size)}


def mixed_defects(source, size):
    """Sorted list of mixed words with H_w != 0 (empty <=> MIXED-EXACT)."""
    bad = []
    for w in product(COLORS, repeat=size):
        if len(set(w)) == 1:
            continue
        if hafnian_word(source, size, w) != 0:
            bad.append(w)
    return bad


def pure_coefficients(source, size):
    return [hafnian_word(source, size, (c,) * size) for c in COLORS]


def is_mixed_exact(source, size):
    return not mixed_defects(source, size)


def is_exact(source, size):
    return is_mixed_exact(source, size) and \
        pure_coefficients(source, size) == [F(1), F(1), F(1)]


# ----------------------------------------------------------------- template

def template_of(source, size):
    return {e: frozenset((i, j) for i in COLORS for j in COLORS
                         if source[e][i][j] != 0)
            for e in edges(size)}


def fibre(template, size, word):
    """# perfect matchings all of whose edges carry cell (w_u, w_v)."""
    n = 0
    for M in perfect_matchings(tuple(range(size))):
        if all((word[u], word[v]) in template[(u, v)] for u, v in M):
            n += 1
    return n


def all_fibres(template, size):
    return {w: fibre(template, size, w) for w in product(COLORS, repeat=size)}


def audit(template, size):
    """Full admissibility audit (T4/T5/T6/S) + census, exact integers."""
    f = all_fibres(template, size)
    live = [e for e in template if template[e]]
    m = len(live)
    Sigma = sum(len(template[e]) for e in live)
    beta = sum(1 for e in live if len(template[e]) == 1)
    deg = [0] * size
    slots = set()
    for (u, v) in live:
        deg[u] += 1
        deg[v] += 1
        for a, b in template[(u, v)]:
            slots.add((u, a))
            slots.add((v, b))
    pure_fib = [f[(c,) * size] for c in COLORS]
    singletons = [w for w, n in f.items() if n == 1 and len(set(w)) > 1]
    T4 = all(x >= 1 for x in pure_fib)
    T5 = (min(deg) if size else 0) >= 3
    T6 = len(slots) == 3 * size
    S = not singletons
    hist = {}
    for w, n in f.items():
        if len(set(w)) > 1:
            hist[n] = hist.get(n, 0) + 1
    return {"m": m, "Sigma": Sigma, "beta": beta,
            "degrees": deg, "min_degree": min(deg) if size else 0,
            "slots_covered": len(slots), "slots_needed": 3 * size,
            "T4_pure_fibres": pure_fib, "T4": T4,
            "T5": T5, "T6": T6, "S": S,
            "n_mixed_singletons": len(singletons),
            "ADMISSIBLE": bool(T4 and T5 and T6 and S),
            "mixed_fibre_histogram": dict(sorted(hist.items()))}


def pure_terms(source, size, colour):
    """The individual nonzero matching products contributing to H_{c^N}."""
    out = []
    for M in perfect_matchings(tuple(range(size))):
        term = F(1)
        for u, v in M:
            term *= source[(u, v)][colour][colour]
        if term != 0:
            out.append((M, term))
    return out


# -------------------------------------------------------------------- gauge

def apply_gauge(source, size, g):
    """A_uv[i][j] -> g[u][i]*g[v][j]*A_uv[i][j].  ``g``: list of 3-lists."""
    out = {}
    for (u, v) in edges(size):
        out[(u, v)] = [[g[u][i] * g[v][j] * source[(u, v)][i][j]
                        for j in COLORS] for i in COLORS]
    return out


def gauge_to_exact(source, size):
    """If mixed-exact with all three pures nonzero, return an EXACT gauge
    equivalent; else None.  Uses only vertex 0's gauge freedom."""
    p = pure_coefficients(source, size)
    if any(x == 0 for x in p):
        return None
    g = [[F(1)] * 3 for _ in range(size)]
    for c in COLORS:
        g[0][c] = F(1) / p[c]
    return apply_gauge(source, size, g)


# ---------------------------------------------------------------- printing

def src_repr(source, size):
    return {f"{u},{v}": [[str(x) for x in row] for row in source[(u, v)]]
            for (u, v) in edges(size) if any(any(r) for r in source[(u, v)])}


def src_from_repr(d, size):
    out = zero_source(size)
    for k, mat in d.items():
        u, v = (int(t) for t in k.split(","))
        out[(u, v)] = [[F(x) for x in row] for row in mat]
    return out


# ------------------------------------------------- constant-block ("J") family

def constant_block_source(size, weights):
    """A_uv = weights[(u,v)] * J_3 (the all-ones 3x3).  Then H_w = haf(weights)
    for EVERY word w, so haf(weights) = 0  =>  MIXED-EXACT."""
    out = zero_source(size)
    for e in edges(size):
        t = weights.get(e, F(0))
        out[e] = [[F(t)] * 3 for _ in range(3)]
    return out


def scalar_hafnian(size, weights):
    total = F(0)
    for M in perfect_matchings(tuple(range(size))):
        term = F(1)
        for e in M:
            term *= weights.get(e, F(0))
            if term == 0:
                break
        total += term
    return total


def count_pm_of_graph(size, edgeset):
    return sum(1 for M in perfect_matchings(tuple(range(size)))
               if all(e in edgeset for e in M))
