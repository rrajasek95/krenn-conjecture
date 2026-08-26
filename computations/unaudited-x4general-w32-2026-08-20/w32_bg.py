#!/usr/bin/env python3
"""W32 -- fast F_p engine for the W27-R1 background criterion (GENERAL blocks).

W27-R1 at N = 8: X_k is nonempty  <=>  some background on K_7 makes all three
colour systems consistent, where the colour-c system at the solve site z = 7
has 21 unknowns x_{y,d} = A_{zy}[c][d] and one row per word u in {0,1,2}^7:

    row_u [ (y, u_y) ] = haf_{V' - y}(bg)_u        (all other entries 0)
    rhs   = 1 if u = c^7 else 0,   rows kept iff offcount( (c,u) ) <= k.

W32 observation (used for a 3x speedup and for the ledger): the row vector
R_u does NOT depend on c -- the cofactors never see w_z.  The three colour
systems share one 2187 x 21 row matrix and differ only in (i) which
(3,3,2)-profile rows are dropped and (ii) which row carries rhs = 1.

Consistency <=> R_{c^7} is NOT in the row span of the retained mixed rows.
"""
from __future__ import annotations

import itertools
from functools import lru_cache

NC = 3
NBG = 7           # sites of the background 0..6; solve site z = 7
VP = tuple(range(NBG))


@lru_cache(maxsize=None)
def pms(sites):
    sites = tuple(sorted(sites))
    if len(sites) % 2:
        return ()
    if not sites:
        return ((),)
    h, rest = sites[0], sites[1:]
    out = []
    for i, x in enumerate(rest):
        for M in pms(rest[:i] + rest[i + 1:]):
            out.append(((h, x),) + M)
    return tuple(out)


EDGES = tuple(itertools.combinations(VP, 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
SIX = {y: tuple(x for x in VP if x != y) for y in VP}
PM6 = {y: pms(SIX[y]) for y in VP}
W6 = {y: tuple(itertools.product(range(NC), repeat=6)) for y in VP}
W6IDX = {y: {w: i for i, w in enumerate(W6[y])} for y in VP}
W7 = tuple(itertools.product(range(NC), repeat=NBG))
PROF332 = (3, 3, 2)


def _prof(word):
    return tuple(sorted((sum(1 for x in word if x == c) for c in range(NC)),
                        reverse=True))


def _off(word):
    return len(word) - max(sum(1 for x in word if x == c) for c in range(NC))


# rows dropped from colour c's system at level k: offcount((c,u)) > k.
# At k = 4 this is exactly "profile (c,u) = (3,3,2)" (W32 word ledger, T1).
DROP = {(c, k): frozenset(i for i, u in enumerate(W7)
                          if _off((c,) + u) > k)
        for c in range(NC) for k in range(1, 6)}
assert DROP[(0, 4)] == frozenset(i for i, u in enumerate(W7)
                                 if _prof((0,) + u) == PROF332)
CONSTROW = {c: next(i for i, u in enumerate(W7) if u == (c,) * NBG)
            for c in range(NC)}


def bg_flat(bg):
    """bg: dict (u,v)->3x3 (u<v, sites in 0..6)  ->  flat list [21][3][3]."""
    return [[[bg[e][a][b] % 0 if False else bg[e][a][b] for b in range(NC)]
             for a in range(NC)] for e in EDGES]


def cellf(F, u, v, a, b):
    if u < v:
        return F[EIDX[(u, v)]][a][b]
    return F[EIDX[(v, u)]][b][a]


def cofactors(F, p):
    """K[y][w6] = haf over V'-y of the word w6 (indexed by W6[y] order)."""
    K = {}
    for y in VP:
        S = SIX[y]
        Ms = PM6[y]
        arr = [0] * (3 ** 6)
        for wi, w in enumerate(W6[y]):
            wd = {S[i]: w[i] for i in range(6)}
            tot = 0
            for M in Ms:
                pr = 1
                for (a, b) in M:
                    c = cellf(F, a, b, wd[a], wd[b])
                    if c == 0:
                        pr = 0
                        break
                    pr = pr * c % p
                if pr:
                    tot = (tot + pr) % p
            arr[wi] = tot
        K[y] = arr
    return K


def rows_of(F, p):
    """The 2187 rows, each as a list of (col_index, value) with <= 7 entries."""
    K = cofactors(F, p)
    out = []
    for u in W7:
        r = []
        for y in VP:
            w6 = tuple(u[x] for x in SIX[y])
            v = K[y][W6IDX[y][w6]]
            if v:
                r.append((3 * y + u[y], v))
        out.append(r)
    return out


def feasible_colours(F, p, k=4, want_details=False):
    """Which colours c have R_{c^7} outside the span of the retained mixed
    rows.  Early-exits as soon as the mixed rank reaches 21."""
    rows = rows_of(F, p)
    res = []
    details = []
    for c in range(NC):
        drop = DROP[(c, min(k, 5))]
        ci = CONSTROW[c]
        basis = [None] * 21
        rank = 0
        full = False
        for i, r in enumerate(rows):
            if i == ci or i in drop:
                continue
            if not r:
                continue
            v = [0] * 21
            for (j, val) in r:
                v[j] = val
            for j in range(21):
                if v[j]:
                    if basis[j] is None:
                        inv = pow(v[j], p - 2, p)
                        basis[j] = [x * inv % p for x in v]
                        rank += 1
                        break
                    f = v[j]
                    bj = basis[j]
                    v = [(x - f * y) % p for x, y in zip(v, bj)]
            if rank == 21:
                full = True
                break
        if full:
            res.append(False)
            details.append({"colour": c, "mixed_rank": 21})
            continue
        # is the constant row in the span?
        v = [0] * 21
        for (j, val) in rows[ci]:
            v[j] = val
        for j in range(21):
            if v[j]:
                if basis[j] is None:
                    break
                f = v[j]
                v = [(x - f * y) % p for x, y in zip(v, basis[j])]
        outside = any(v)
        res.append(outside)
        details.append({"colour": c, "mixed_rank": rank, "outside": outside})
    return (res, details) if want_details else res


def score(F, p, k=4):
    return sum(1 for x in feasible_colours(F, p, k) if x)
