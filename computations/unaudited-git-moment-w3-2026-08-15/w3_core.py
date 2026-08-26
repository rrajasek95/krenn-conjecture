"""UNAUDITED PROBE (agent W3, Route A, 2026-08-15).

Repo HEAD pinned at 26ba69f7e643694c6a58464af6e9e1de9ec92f01.

Core exact machinery for the gauge-torus / moment analysis of the ternary
GHZ (Krenn-Gu) system.

Conventions (matching the repo's committed `(C(n,2), 3, 3)` layout):

  * vertices          V = {0,...,n-1}, n even
  * edges             all unordered pairs (u,v), u < v, indexed by EDGES
  * cells             s = (edge_index, i, j) with i the colour at u and
                      j the colour at v.  Total 9*C(n,2) cells.
  * words             c in {0,1,2}^n
  * gauge torus       T = (C^*)^{V x 3},  a_s |-> b_{u,i} b_{v,j} a_s
  * cell weight       m_s = e_{(u,i)} + e_{(v,j)} in Z^{3n}   ("node" basis)
  * node index        node(v,c) = 3*v + c

Nothing here is audited; it is a probe.
"""

from __future__ import annotations

import itertools
from fractions import Fraction
from functools import lru_cache

COLOURS = (0, 1, 2)
NCOL = 3


@lru_cache(maxsize=None)
def edges(n: int) -> tuple[tuple[int, int], ...]:
    return tuple(itertools.combinations(range(n), 2))


@lru_cache(maxsize=None)
def edge_index(n: int) -> dict[tuple[int, int], int]:
    return {e: k for k, e in enumerate(edges(n))}


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    head, rest = vertices[0], vertices[1:]
    out = []
    for k, partner in enumerate(rest):
        remainder = rest[:k] + rest[k + 1 :]
        for tail in perfect_matchings(remainder):
            out.append(((head, partner),) + tail)
    return tuple(out)


@lru_cache(maxsize=None)
def matchings(n: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    return perfect_matchings(tuple(range(n)))


@lru_cache(maxsize=None)
def cells(n: int) -> tuple[tuple[int, int, int], ...]:
    """All cells (edge_index, i, j)."""
    return tuple(
        (k, i, j) for k in range(len(edges(n))) for i in COLOURS for j in COLOURS
    )


@lru_cache(maxsize=None)
def cell_index(n: int) -> dict[tuple[int, int, int], int]:
    return {s: k for k, s in enumerate(cells(n))}


def node(v: int, c: int) -> int:
    return 3 * v + c


@lru_cache(maxsize=None)
def cell_nodes(n: int) -> tuple[tuple[int, int], ...]:
    """For each cell index, the pair of nodes (u,i),(v,j) it joins."""
    E = edges(n)
    out = []
    for (k, i, j) in cells(n):
        u, v = E[k]
        out.append((node(u, i), node(v, j)))
    return tuple(out)


@lru_cache(maxsize=None)
def words(n: int) -> tuple[tuple[int, ...], ...]:
    return tuple(itertools.product(COLOURS, repeat=n))


@lru_cache(maxsize=None)
def term_cells(n: int) -> dict[tuple[int, ...], tuple[tuple[int, ...], ...]]:
    """word -> tuple over matchings of the sorted tuple of cell indices used.

    The k-th entry corresponds to matchings(n)[k]; every matching contributes
    exactly one monomial to Phi_word, of degree n/2.
    """
    EI = edge_index(n)
    CI = cell_index(n)
    out: dict[tuple[int, ...], tuple[tuple[int, ...], ...]] = {}
    Ms = matchings(n)
    for w in words(n):
        per = []
        for M in Ms:
            idxs = []
            for (a, b) in M:
                u, v = (a, b) if a < b else (b, a)
                idxs.append(CI[(EI[(u, v)], w[u], w[v])])
            per.append(tuple(sorted(idxs)))
        out[w] = tuple(per)
    return out


def phi(n: int, a: dict[int, object] | list, word: tuple[int, ...]):
    """Phi_word for a cell-value vector `a` (indexable by cell index)."""
    total = 0
    for idxs in term_cells(n)[word]:
        prod = 1
        for s in idxs:
            prod = prod * a[s]
            if prod == 0:
                break
        total = total + prod
    return total


def support_of(a) -> frozenset[int]:
    return frozenset(k for k, x in enumerate(a) if x != 0)


def live_terms(n: int, S: frozenset[int], word: tuple[int, ...]) -> list[int]:
    """Indices of matchings whose monomial for `word` is supported inside S."""
    return [
        k for k, idxs in enumerate(term_cells(n)[word]) if all(s in S for s in idxs)
    ]


def is_pure(word: tuple[int, ...]) -> bool:
    return len(set(word)) == 1


def cell_weight(n: int, s: int) -> tuple[int, ...]:
    """m_s in Z^{3n}."""
    p, q = cell_nodes(n)[s]
    w = [0] * (3 * n)
    w[p] += 1
    w[q] += 1
    return tuple(w)


def gauge_weight(n: int, w: list[Fraction] | list[int], s: int):
    """<w, m_s> = w_{u,i} + w_{v,j}."""
    p, q = cell_nodes(n)[s]
    return w[p] + w[q]


def pi_char(n: int, c: int) -> tuple[int, ...]:
    """pi_c = sum_v e_{(v,c)} in Z^{3n} (the weight of the pure amplitude)."""
    out = [0] * (3 * n)
    for v in range(n):
        out[node(v, c)] = 1
    return tuple(out)


def restrict(a, S) -> list:
    return [x if k in S else 0 * x for k, x in enumerate(a)]
