#!/usr/bin/env python3
"""UNAUDITED PROBE W13 -- Task 2 (R1b): independent R_cell template engine.

Conventions follow computations/unaudited-uniform-n-a3-2026-08-15/a3_core.py
(monomial / R_cell regime) but every routine here is written from the
definition, so it is an INDEPENDENT verdict engine, not a wrapper.

An R_cell template on K_N assigns to each edge {u<v} either ABSENT or an
ordered colour label (a, b) (a at u, b at v).  A perfect matching M is
SUPPORTED if every edge of M is labelled; it then induces the unique word
c(M) in {0,1,2}^N.  fibre(c) = {supported M : c(M) = c}.

  pure fibres        c constant
  singleton-free     no MIXED word has |fibre| == 1        (kills O2)
  binomial fibre     mixed word with |fibre| == 2; gives w^d = -1,
                     d = chi(M+) - chi(M-) in Z^E
  O1 (odd circuit)   integer relation sum n_i d_i = 0 with sum n_i ODD
                     -> "1 = -1", the template is dead

R1b (A3): every singleton-free R_cell template with three nonzero pure fibres
has an odd relation.  A counterexample is a singleton-free template with three
nonempty pures whose binomial-difference lattice admits NO odd relation --
in particular any such template with NO binomial fibre at all.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations

import numpy as np

ABSENT = None


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple) -> tuple:
    if not vertices:
        return ((),)
    first = vertices[0]
    out = []
    for pos in range(1, len(vertices)):
        second = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1:]
        for tail in perfect_matchings(rest):
            out.append(((first, second),) + tail)
    return tuple(out)


@lru_cache(maxsize=None)
def edges(n: int) -> tuple:
    return tuple(combinations(range(n), 2))


@lru_cache(maxsize=None)
def edge_index(n: int) -> dict:
    return {e: i for i, e in enumerate(edges(n))}


@lru_cache(maxsize=None)
def matchings_as_edge_sets(n: int) -> tuple:
    idx = edge_index(n)
    return tuple(tuple(idx[e] for e in m)
                 for m in perfect_matchings(tuple(range(n))))


# ------------------------------------------------------- fibres (definition)

def fibre_table(n: int, labels):
    """{word: [matching indices]}, straight from the definition."""
    out = {}
    ms = perfect_matchings(tuple(range(n)))
    idx = edge_index(n)
    for k, m in enumerate(ms):
        word = [-1] * n
        ok = True
        for u, v in m:
            lab = labels[idx[(u, v)]]
            if lab is None:
                ok = False
                break
            word[u], word[v] = lab
        if ok:
            out.setdefault(tuple(word), []).append(k)
    return out


def is_mixed(word):
    return len(set(word)) > 1


def census(n, labels):
    table = fibre_table(n, labels)
    pures = [len(table.get(tuple([r] * n), ())) for r in range(3)]
    singles, binomials, hist = [], [], {}
    for word, mem in table.items():
        if not is_mixed(word):
            continue
        hist[len(mem)] = hist.get(len(mem), 0) + 1
        if len(mem) == 1:
            singles.append(word)
        elif len(mem) == 2:
            binomials.append((word, tuple(mem)))
    return {"pures": pures, "singletons": singles, "binomials": binomials,
            "hist": dict(sorted(hist.items())), "table": table}


# --------------------------------------------------- diagonal fast evaluator

def pm_table(n, adj):
    """pm[S] = # perfect matchings of the induced subgraph on bitmask S."""
    pm = np.zeros(1 << n, dtype=np.int64)
    pm[0] = 1
    for S in range(1, 1 << n):
        v = (S & -S).bit_length() - 1
        rest = S & ~(1 << v)
        total = 0
        cand = adj[v] & rest
        while cand:
            b = cand & -cand
            total += pm[rest & ~b]
            cand ^= b
        pm[S] = total
    return pm


@lru_cache(maxsize=None)
def word_masks(n):
    """For all 3^n words, the three vertex bitmasks, plus a mixed flag."""
    total = 3 ** n
    m = np.zeros((3, total), dtype=np.int64)
    counts = np.zeros((3, total), dtype=np.int16)
    k = np.arange(total)
    t = k.copy()
    for v in range(n):
        r = t % 3
        t //= 3
        for c in range(3):
            sel = (r == c)
            m[c][sel] |= (1 << v)
            counts[c][sel] += 1
    mixed = ~((counts[0] == n) | (counts[1] == n) | (counts[2] == n))
    return m, mixed


def diagonal_sizes(n, colour_edge_sets):
    """Fibre size of every word, via the product formula (diagonal templates)."""
    pms = []
    for es in colour_edge_sets:
        adj = [0] * n
        for u, v in es:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
        pms.append(pm_table(n, adj))
    m, mixed = word_masks(n)
    sizes = pms[0][m[0]] * pms[1][m[1]] * pms[2][m[2]]
    full = (1 << n) - 1
    pures = [int(pms[r][full]) for r in range(3)]
    return sizes, mixed, pures


def diagonal_labels(n, colour_edge_sets):
    idx = edge_index(n)
    lab = [None] * len(idx)
    for r, es in enumerate(colour_edge_sets):
        for e in es:
            lab[idx[tuple(sorted(e))]] = (r, r)
    return lab


# -------------------------------------------------------- odd-circuit search

def hnf_with_transform(rows):
    """(H, U, rank): U unimodular, U @ rows = H in row echelon form over Z."""
    m = len(rows)
    ncol = len(rows[0]) if m else 0
    H = [list(r) for r in rows]
    U = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
    pr = 0
    for col in range(ncol):
        tgt = None
        for r in range(pr, m):
            if H[r][col]:
                tgt = r
                break
        if tgt is None:
            continue
        H[pr], H[tgt] = H[tgt], H[pr]
        U[pr], U[tgt] = U[tgt], U[pr]
        for r in range(pr + 1, m):
            while H[r][col]:
                a, b = H[pr][col], H[r][col]
                if abs(b) >= abs(a):
                    f = b // a
                    H[r] = [x - f * y for x, y in zip(H[r], H[pr])]
                    U[r] = [x - f * y for x, y in zip(U[r], U[pr])]
                else:
                    H[pr], H[r] = H[r], H[pr]
                    U[pr], U[r] = U[r], U[pr]
        pr += 1
        if pr == m:
            break
    return H, U, pr


def odd_relation(diffs):
    """An integer relation with ODD coefficient sum, or None.

    The kernel lattice of the difference vectors is spanned by the rows of U
    below the rank; a relation is odd iff some kernel basis vector has odd
    coordinate sum (the parity map is linear on the lattice)."""
    if not diffs:
        return None
    H, U, rank = hnf_with_transform([list(d) for d in diffs])
    for r in range(rank, len(diffs)):
        if sum(U[r]) % 2:
            return U[r]
    return None


def difference_vectors(n, binomials):
    ms = matchings_as_edge_sets(n)
    ne = len(edges(n))
    out = []
    for word, (i, j) in binomials:
        d = [0] * ne
        for e in ms[i]:
            d[e] += 1
        for e in ms[j]:
            d[e] -= 1
        out.append((word, tuple(d)))
    return out


def verify_odd_relation(n, binomials, rel):
    """Check sum n_i d_i = 0 and sum n_i odd, from scratch."""
    diffs = [d for _, d in difference_vectors(n, binomials)]
    ne = len(edges(n))
    acc = [0] * ne
    for coeff, d in zip(rel, diffs):
        for k in range(ne):
            acc[k] += coeff * d[k]
    return all(x == 0 for x in acc) and sum(rel) % 2 == 1


# ------------------------------------------------------------ verdict

def verdict(n, labels, table=None):
    c = census(n, labels) if table is None else table
    pures_ok = all(p > 0 for p in c["pures"])
    singleton_free = not c["singletons"]
    rel = None
    if c["binomials"]:
        diffs = [d for _, d in difference_vectors(n, c["binomials"])]
        rel = odd_relation(diffs)
    return {
        "pures": c["pures"], "three_pures": pures_ok,
        "singleton_free": singleton_free,
        "n_singletons": len(c["singletons"]),
        "n_binomials": len(c["binomials"]),
        "hist": c["hist"],
        "odd_relation": rel,
        "O1_dead": rel is not None,
        "R1b_counterexample": (pures_ok and singleton_free and rel is None),
    }
