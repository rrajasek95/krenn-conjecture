#!/usr/bin/env python3
"""AUDIT A4 -- fully independent engine for the Krenn-Gu N=8, d=3 model.

Written from the MODEL DEFINITION, not from any probe's code:

    sites 0..N-1, one 3x3 block A_uv per edge u<v of K_N (rows = colour at u,
    columns = colour at v).  For a word w in {0,1,2}^N,

        H(A)_w = sum over perfect matchings M of K_N of
                 prod_{uv in M} A_uv[w_u][w_v].

    EXACT: H_w = 1 on the d constant words, 0 on all mixed words.  The
    diagonal gauge rescales the constant values independently, so with a
    fixed template (support pattern) exactness is equivalent to: all
    occupied cells nonzero, every mixed fibre sum = 0, every constant fibre
    sum != 0.

Deliberate implementation differences from w12_core / w8_core:
  * perfect matchings by ITERATIVE bitmask enumeration (stack, not recursion
    on tuples);
  * fibres computed by enumerating matchings of the ACTIVE SUBGRAPH of the
    word (bitmask DP), never by filtering the global 105-list;
  * templates carried as frozensets of (edge,i,j) triples, bitmasks only at
    the I/O boundary;
  * fibre polynomials as canonical dict{frozenset(var) : int coeff}.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

Q = 3


# ------------------------------------------------------------ matchings

def _pms_bitmask(vertices, adj):
    """Perfect matchings of the graph on `vertices` with adjacency dict `adj`.

    Iterative: repeatedly take the LOWEST still-unmatched vertex and branch
    over its partners.  `adj[(u,v)]` truthy means the edge u-v may be used.
    Returns a list of frozensets of (u,v) pairs with u < v.
    """
    vs = tuple(sorted(vertices))
    n = len(vs)
    if n % 2:
        return []
    pos = {v: k for k, v in enumerate(vs)}
    full = (1 << n) - 1
    out = []
    stack = [(0, ())]                       # (matched-mask, partial matching)
    while stack:
        used, part = stack.pop()
        if used == full:
            out.append(frozenset(part))
            continue
        # lowest unmatched index
        k = 0
        while (used >> k) & 1:
            k += 1
        u = vs[k]
        for l in range(k + 1, n):
            if (used >> l) & 1:
                continue
            v = vs[l]
            e = (u, v) if u < v else (v, u)
            if adj.get(e):
                stack.append((used | (1 << k) | (1 << l), part + (e,)))
    return out


def all_perfect_matchings(vertices):
    vs = tuple(sorted(vertices))
    adj = {e: True for e in combinations(vs, 2)}
    return _pms_bitmask(vs, adj)


# ------------------------------------------------------------ templates

class Template:
    """Support pattern: a set of occupied cells (edge_index, i, j)."""

    def __init__(self, n_sites, occupied):
        self.n = n_sites
        self.edges = tuple(combinations(range(n_sites), 2))
        self.eidx = {e: k for k, e in enumerate(self.edges)}
        self.occ = frozenset(occupied)
        self._byedge = {}
        for (e, i, j) in self.occ:
            self._byedge.setdefault(e, set()).add((i, j))

    @classmethod
    def from_masks(cls, masks, n_sites=8):
        occ = set()
        for e, mask in enumerate(masks):
            for c in range(9):
                if (mask >> c) & 1:
                    occ.add((e, c // 3, c % 3))
        return cls(n_sites, occ)

    def to_masks(self):
        masks = [0] * len(self.edges)
        for (e, i, j) in self.occ:
            masks[e] |= 1 << (3 * i + j)
        return tuple(masks)

    def has(self, e, i, j):
        return (e, i, j) in self.occ

    def cells_of(self, e):
        return sorted(self._byedge.get(e, ()))

    def m(self):
        return len(self._byedge)

    def sigma(self):
        return len(self.occ)

    def active_edges(self, word):
        """Edges e=(u,v) with cell (w_u, w_v) occupied."""
        out = []
        for k, (u, v) in enumerate(self.edges):
            if (k, word[u], word[v]) in self.occ:
                out.append(k)
        return out

    # ---------------------------------------------------------- fibres
    def fibre_matchings(self, word, sites=None):
        """Supported perfect matchings of `sites` (default: all) on `word`.

        `word` is indexed by GLOBAL site number.  Returns frozensets of
        (u,v) vertex pairs.
        """
        if sites is None:
            sites = range(self.n)
        vs = tuple(sorted(sites))
        adj = {}
        for (u, v) in combinations(vs, 2):
            adj[(u, v)] = (self.eidx[(u, v)], word[u], word[v]) in self.occ
        return _pms_bitmask(vs, adj)

    def fibre_poly(self, word, sites=None):
        """Fibre polynomial: dict {frozenset of variables : coefficient}.

        Variables are (edge_index, i, j) triples -- i.e. cells.  Every
        monomial is squarefree of degree |sites|/2 and (model fact) the
        matchings give DISTINCT monomials, so every coefficient is 1; we
        still accumulate to make that verifiable.
        """
        poly = {}
        for M in self.fibre_matchings(word, sites):
            mono = frozenset((self.eidx[(u, v)], word[u], word[v])
                             for (u, v) in M)
            poly[mono] = poly.get(mono, 0) + 1
        return poly


def poly_eval(poly, values):
    """Exact evaluation of a fibre polynomial at a dict {cell: value}."""
    total = 0
    for mono, coeff in poly.items():
        term = coeff
        for var in mono:
            term *= values[var]
        total += term
    return total


def poly_mul(p, q):
    out = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            assert not (m1 & m2), "non-disjoint monomials"
            m = m1 | m2
            out[m] = out.get(m, 0) + c1 * c2
    return {m: c for m, c in out.items() if c}


def varname(tmpl, var):
    e, i, j = var
    u, v = tmpl.edges[e]
    return f"x_{u}{v}_{i}{j}"


def polystr(tmpl, poly):
    parts = []
    for mono in sorted(poly, key=lambda m: sorted(m)):
        c = poly[mono]
        body = "*".join(varname(tmpl, v) for v in sorted(mono))
        parts.append(body if c == 1 else f"{c}*{body}")
    return " + ".join(parts) if parts else "0"


# ------------------------------------------------------------ words

def words(n, q=Q):
    return product(range(q), repeat=n)


def is_mixed(word):
    return any(c != word[0] for c in word)


def constant_words(n, q=Q):
    return [(c,) * n for c in range(q)]
