#!/usr/bin/env python3
"""UNAUDITED PROBE (W19-CENSUS) -- shared library for THE (R) CENSUS at N=8.

UNAUDITED.  Nothing here is a proved claim of the repository.  Pinned HEAD
d377b71529c7b7f5c5670092de93630245b928dc (see ../PINNED_HEAD.txt).

EXACT ARITHMETIC ONLY.  Every number below is a Python int or a numpy
INTEGER (bitwise / comparison / sum over int64); no float appears in any
verdict path.  numpy is used only for integer bit masking, and every
numpy routine here is cross-checked against the pure-Python routines of
../w19_core.py in w19c_verify.py.

This module IMPORTS ../w19_core.py (probe W19's independent
re-implementation of the model) and never modifies it.  Everything named
`my_*` here is a SECOND, independent implementation written from the
model definition; agreement between the two is a control, not an
assumption.

KEY REFORMULATION USED THROUGHOUT (proved in w19c_verify.py by exhaustive
agreement with w19_core.support):

    For a template T and a word w let G_w(T) = { e : cell (w_u,w_v) of
    T[e] is occupied }.  Then support(T,w) = the set of perfect matchings
    of K_8 contained in G_w(T), so  fibre(T,w) = #PM(G_w(T)).

TOKEN CALCULUS (the (SC) condition, proved in w19c_verify.py by exhaustive
agreement with w19_core.sc_ok over all 512 masks / random templates):

    For e=(u,v), u<v: rows of T[e] are indexed by the colour at u and
    columns by the colour at v.  Put
        a_u(mask) = the unique COLUMN index of the occupied cells, if
                    unique, else None      (the colour e forces at v,
                    i.e. the demand (u, a_u) that e serves)
        a_v(mask) = the unique ROW index, if unique, else None.
    Then T is (SC)-admissible  <=>  for every vertex p the set of tokens
    { a_p(T[e]) : e incident to p } contains all of {0,1,2}.
    a_u and a_v are INDEPENDENT coordinates of the mask.
"""
from __future__ import annotations

import os
import sys
from itertools import combinations, permutations, product

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))

from w19_core import (  # noqa: E402
    EDGES, EIDX, PMS, PM_E, MIXED, CONSTS, WORDS, FULL, N, Q,
    support, gamma_edges, pms_inside, full_pm_indices, extras_at,
    effectively_clean, spanning_2conn, block_class, far_thin_colour,
    sc_servers, sc_ok, in_R, cells_of, cell, W8_IMMUNE,
)

NE = len(EDGES)          # 28
NW = len(WORDS)          # 6561

# ------------------------------------------------------------------ words --
WORD_IDX = {w: i for i, w in enumerate(WORDS)}
MIXED_MASK = np.array([1 if len(set(w)) > 1 else 0 for w in WORDS], dtype=np.int64)
MIXED_POS = np.nonzero(MIXED_MASK)[0]
CONST_POS = np.array([WORD_IDX[c] for c in CONSTS], dtype=np.int64)

# CELLI[e, wi] = 3*w_u + w_v  (the cell of edge e activated by word wi)
CELLI = np.zeros((NE, NW), dtype=np.int64)
for _ei, (_u, _v) in enumerate(EDGES):
    for _wi, _w in enumerate(WORDS):
        CELLI[_ei, _wi] = 3 * _w[_u] + _w[_v]

# PM_EMASK[mi] = 28-bit mask of the edges of perfect matching mi
PM_EMASK = np.array([sum(1 << ei for ei in es) for es in PM_E], dtype=np.int64)
POW2E = np.array([1 << ei for ei in range(NE)], dtype=np.int64)


# --------------------------------------------------------- independent PMs --
def my_pms_of_adj(adj):
    """All perfect matchings of the 8-vertex graph given by adjacency bitmasks.

    Independent of w19_core.PMS: a plain recursive enumeration.  Returns a
    list of frozensets of edges (as (u,v) pairs, u<v)."""
    out = []
    def rec(rem, acc):
        if rem == 0:
            out.append(frozenset(acc))
            return
        a = (rem & -rem).bit_length() - 1
        rest = rem & ~(1 << a)
        cand = adj[a] & rest
        while cand:
            b = (cand & -cand).bit_length() - 1
            cand &= cand - 1
            acc.append((a, b))
            rec(rest & ~(1 << b), acc)
            acc.pop()
    rec((1 << N) - 1, [])
    return out


def my_npm_graph(edges):
    """#perfect matchings of the graph on 8 vertices with these edges."""
    adj = [0] * N
    for (u, v) in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return len(my_pms_of_adj(adj))


def my_fibre(T, w):
    """fibre(T,w) computed from scratch: #PM of the activated graph."""
    adj = [0] * N
    for ei, (u, v) in enumerate(EDGES):
        if (T[ei] >> (3 * w[u] + w[v])) & 1:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    return len(my_pms_of_adj(adj))


# ----------------------------------------------------------------- tokens --
def my_tokens(mask):
    """(a_u, a_v) for a block on edge (u,v), u<v.  None where not unique."""
    if mask == 0:
        return (None, None)
    cs = [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]
    rows = set(i for i, _ in cs)
    cols = set(j for _, j in cs)
    return (next(iter(cols)) if len(cols) == 1 else None,
            next(iter(rows)) if len(rows) == 1 else None)


def my_sc_ok(T):
    have = [set() for _ in range(N)]
    for ei, (u, v) in enumerate(EDGES):
        au, av = my_tokens(T[ei])
        if au is not None:
            have[u].add(au)
        if av is not None:
            have[v].add(av)
    return all(len(s) == 3 for s in have)


def my_in_R(T):
    if not my_sc_ok(T):
        return False
    for w in CONSTS:
        if my_fibre(T, w) < 1:
            return False
    if not spanning_2conn([EDGES[i] for i, t in enumerate(T) if t == FULL]):
        return False
    for w in MIXED:
        if my_fibre(T, w) < 3:
            return False
    return True


# --------------------------------------------- fast (exact int) fibre bank --
def fibres_all_words(T):
    """np.int64[6561] of fibre sizes, all integer arithmetic."""
    Ta = np.asarray(T, dtype=np.int64).reshape(NE, 1)
    act = (Ta >> CELLI) & 1                       # (28, 6561) 0/1
    gmask = (act * POW2E.reshape(NE, 1)).sum(axis=0)   # (6561,) 28-bit graphs
    sub = (gmask.reshape(NW, 1) & PM_EMASK.reshape(1, -1)) == PM_EMASK.reshape(1, -1)
    return sub.sum(axis=1).astype(np.int64)


def graph_masks_all_words(T):
    Ta = np.asarray(T, dtype=np.int64).reshape(NE, 1)
    act = (Ta >> CELLI) & 1
    return (act * POW2E.reshape(NE, 1)).sum(axis=0)


def fast_in_R(T):
    """(R) membership, exact integer arithmetic; == w19_core.in_R (verified)."""
    if not my_sc_ok(T):
        return False
    ge = [EDGES[i] for i, t in enumerate(T) if t == FULL]
    if not spanning_2conn(ge):
        return False
    f = fibres_all_words(T)
    if int(f[CONST_POS].min()) < 1:
        return False
    return int(f[MIXED_POS].min()) >= 3


def fast_audit(T):
    f = fibres_all_words(T)
    ge = [EDGES[i] for i, t in enumerate(T) if t == FULL]
    cls = {}
    for c in ("zero", "single", "thin", "fat", "full"):
        cls[c] = sum(1 for t in T if block_class(t) == c)
    return dict(
        m=int(sum(1 for t in T if t)),
        sigma=int(sum(bin(int(t)).count("1") for t in T)),
        sc=bool(my_sc_ok(T)),
        n_gamma=len(ge),
        gamma=[list(e) for e in ge],
        gamma_span2conn=bool(spanning_2conn(ge)),
        gamma_pms=int(len(pms_inside(ge))),
        min_mixed_fibre=int(f[MIXED_POS].min()),
        min_const_fibre=int(f[CONST_POS].min()),
        classes=cls,
        in_R=bool(fast_in_R(T)),
    )


# ------------------------------------------------------------ graph tools ---
def edges_to_mask(edges):
    return sum(1 << EIDX[(min(u, v), max(u, v))] for (u, v) in edges)


def mask_to_edges(m):
    return [EDGES[i] for i in range(NE) if (m >> i) & 1]


def degseq(edges):
    d = [0] * N
    for u, v in edges:
        d[u] += 1
        d[v] += 1
    return d


_PERMS8 = list(permutations(range(N)))


def graph_canon(edges):
    """Canonical 28-bit form of a graph on 8 labelled vertices (brute force)."""
    es = set((min(u, v), max(u, v)) for (u, v) in edges)
    best = None
    for perm in _PERMS8:
        msk = 0
        for (a, b) in es:
            x, y = perm[a], perm[b]
            msk |= 1 << EIDX[(min(x, y), max(x, y))]
        if best is None or msk < best:
            best = msk
    return best


def graph_aut(edges):
    """The automorphism group of a graph on 8 vertices, as a list of perms."""
    es = set((min(u, v), max(u, v)) for (u, v) in edges)
    out = []
    for perm in _PERMS8:
        ok = True
        for (a, b) in es:
            x, y = perm[a], perm[b]
            if (min(x, y), max(x, y)) not in es:
                ok = False
                break
        if ok:
            out.append(perm)
    return out


# ------------------------------------------- fast canonical form of a graph -
_PERM_POW = None
_PERM_ACC = None


def _init_perm_tables():
    global _PERM_POW, _PERM_ACC
    if _PERM_POW is not None:
        return
    npm = len(_PERMS8)
    _PERM_POW = np.zeros((NE, npm), dtype=np.int64)
    for pi, p in enumerate(_PERMS8):
        for ei, (u, v) in enumerate(EDGES):
            x, y = p[u], p[v]
            _PERM_POW[ei, pi] = 1 << EIDX[(min(x, y), max(x, y))]
    _PERM_ACC = np.zeros(npm, dtype=np.int64)


def _orbit_vec(mask):
    _init_perm_tables()
    acc = _PERM_ACC
    acc[:] = 0
    m = mask
    while m:
        e = (m & -m).bit_length() - 1
        m &= m - 1
        np.add(acc, _PERM_POW[e], out=acc)
    return acc


def canon_mask(mask):
    """canonical 28-bit form of a graph given as a 28-bit edge mask."""
    return int(_orbit_vec(mask).min())


def aut_size_mask(mask):
    return int((_orbit_vec(mask) == mask).sum())


# ------------------------------------------------------------ group action --
def apply_site_perm(T, perm):
    """Relabel the sites by perm: new site perm[p] carries old site p."""
    out = [0] * NE
    for ei, (u, v) in enumerate(EDGES):
        x, y = perm[u], perm[v]
        mask = T[ei]
        nm = 0
        for c in range(9):
            if (mask >> c) & 1:
                i, j = c // 3, c % 3
                # cell (i,j): colour i at u, colour j at v
                if x < y:
                    nm |= 1 << (3 * i + j)
                else:
                    nm |= 1 << (3 * j + i)
        out[EIDX[(min(x, y), max(x, y))]] = nm
    return out


def apply_colour_perms(T, pis):
    """pis[p] is a permutation (tuple of length 3) of the colours at site p."""
    out = [0] * NE
    for ei, (u, v) in enumerate(EDGES):
        mask = T[ei]
        nm = 0
        for c in range(9):
            if (mask >> c) & 1:
                i, j = c // 3, c % 3
                nm |= 1 << (3 * pis[u][i] + pis[v][j])
        out[ei] = nm
    return out


S3 = list(permutations(range(3)))


# ----------------------------------------------------- SC completion count --
def sc_mask_count(k_u, k_v):
    """#masks in 0..510 whose token a_u avoids a set of size (3-k_u) ...

    Precisely: given that a_u is allowed to be None or any of k_u prescribed
    colours, and a_v None or any of k_v prescribed colours, the number of
    masks (excluding FULL) with those tokens."""
    return 478 + 4 * k_u + 4 * k_v + k_u * k_v


def count_sc_completions(gamma_mask):
    """EXACT number of templates T with Gamma(T) = the given edge set and T
    (SC)-admissible.  Inclusion-exclusion over the missing-colour sets."""
    free = [ei for ei in range(NE) if not (gamma_mask >> ei) & 1]
    fe = [EDGES[ei] for ei in free]
    tot = 0
    binom = [1, 3, 3, 1]
    sign = [1, -1, 1, -1]
    for svec in product(range(4), repeat=N):
        coef = 1
        for v in range(N):
            coef *= binom[svec[v]] * sign[svec[v]]
        if coef == 0:
            continue
        p = 1
        for (u, v) in fe:
            p *= sc_mask_count(3 - svec[u], 3 - svec[v])
        tot += coef * p
    return tot


# ------------------------------------------------------------ misc printing -
def fmt_T(T):
    return "[" + ",".join(str(int(x)) for x in T) + "]"
