"""AUDIT A1 of probe W3 (2026-08-15).  INDEPENDENT re-implementation.

Deliberately different from w3_core.py:
  * cells are keyed by the tuple (u, v, i, j) with u < v, i = colour at u,
    j = colour at v -- a dict, not a flat index list;
  * Phi_word is computed as a HAFNIAN by recursive expansion on the lowest
    uncovered vertex, never by enumerating a global matching list;
  * a second, independent matching enumerator (via involutions of a
    permutation list) is used only for cross-checking the hafnian.

Nothing here reads or imports W3 code.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

COLS = (0, 1, 2)


def cellkey(u, v, i, j):
    """Canonical key.  (u,i)-(v,j) with the SMALLER VERTEX FIRST."""
    if u < v:
        return (u, v, i, j)
    return (v, u, j, i)


def all_cells(n):
    out = []
    for u in range(n):
        for v in range(u + 1, n):
            for i in COLS:
                for j in COLS:
                    out.append((u, v, i, j))
    return out


def all_words(n):
    return list(itertools.product(COLS, repeat=n))


# ---------------------------------------------------------------- hafnian


def haf(a, word, verts, zero=0, one=1):
    """Phi_word restricted to `verts` (a tuple), by recursive expansion on
    the first vertex.  `a` is a dict cellkey -> value (missing = 0)."""
    if not verts:
        return one
    head = verts[0]
    rest = verts[1:]
    total = zero
    for k, p in enumerate(rest):
        val = a.get(cellkey(head, p, word[head], word[p]), zero)
        if val == zero:
            continue
        sub = rest[:k] + rest[k + 1:]
        total = total + val * haf(a, word, sub, zero, one)
    return total


def phi(a, word, n, zero=0, one=1):
    return haf(a, word, tuple(range(n)), zero, one)


# ------------------------------------------- second, independent enumerator


def matchings_via_involutions(n):
    """All perfect matchings of K_n as frozensets of ordered pairs, produced
    by scanning permutations of range(n) and keeping fixed-point-free
    involutions.  Slow but completely independent of any recursion."""
    out = set()
    for perm in itertools.permutations(range(n)):
        ok = True
        for v in range(n):
            if perm[v] == v or perm[perm[v]] != v:
                ok = False
                break
        if ok:
            out.add(frozenset(frozenset((v, perm[v])) for v in range(n)))
    return sorted(out, key=lambda M: sorted(tuple(sorted(e)) for e in M))


def phi_by_enumeration(a, word, n, MS=None, zero=0, one=1):
    if MS is None:
        MS = matchings_via_involutions(n)
    total = zero
    for M in MS:
        prod = one
        for e in M:
            u, v = sorted(e)
            prod = prod * a.get(cellkey(u, v, word[u], word[v]), zero)
            if prod == zero:
                break
        total = total + prod
    return total


# ----------------------------------------------------------------- gauge


def gauge_apply(a, b, n):
    """b is a dict (v,c) -> value.  Returns the gauge transform of a."""
    out = {}
    for (u, v, i, j), val in a.items():
        out[(u, v, i, j)] = b[(u, i)] * b[(v, j)] * val
    return out


def nodes_of(key):
    u, v, i, j = key
    return ((u, i), (v, j))


def loads(y, n):
    """y: dict cellkey -> nonneg number.  Returns dict (v,c) -> load."""
    L = {(v, c): 0 for v in range(n) for c in COLS}
    for k, val in y.items():
        p, q = nodes_of(k)
        L[p] = L[p] + val
        L[q] = L[q] + val
    return L
