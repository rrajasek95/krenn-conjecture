#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- general-K cap error (for cross-checks against P1/P2
and for the rank-one-vs-general comparison).  Exact."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

from w17_core import COLORS, oriented, perfect_matchings, require


def R_general(source, p, q, K, a, b, ca, cb):
    """R_ab(K)_{ca,cb} = sum_ij K_ij (A_pa[i][ca] A_qb[j][cb]
                                      + A_pb[i][cb] A_qa[j][ca])."""
    apa, aqb = oriented(source, p, a), oriented(source, q, b)
    apb, aqa = oriented(source, p, b), oriented(source, q, a)
    total = Fraction(0)
    for i in range(3):
        for j in range(3):
            if K[i][j] == 0:
                continue
            total += K[i][j] * (apa[i][ca] * aqb[j][cb]
                                + apb[i][cb] * aqa[j][ca])
    return total


def general_cap_error(source, p, q, K, sites):
    """E_pq(K) by the matching expansion, any cap K (3x3)."""
    sites = tuple(sites)
    h = len(sites) // 2
    apq = oriented(source, p, q)
    s = sum(K[i][j] * apq[i][j] for i in range(3) for j in range(3))
    slot = {a: n for n, a in enumerate(sites)}
    out = {}
    for word in product(COLORS, repeat=len(sites)):
        total = Fraction(0)
        for matching in perfect_matchings(sites):
            for size in range(2, h + 1):
                for J in combinations(range(h), size):
                    Jset = set(J)
                    term = s ** (h - size)
                    if term == 0:
                        continue
                    for n, (a, b) in enumerate(matching):
                        ca, cb = word[slot[a]], word[slot[b]]
                        if n in Jset:
                            term *= R_general(source, p, q, K, a, b, ca, cb)
                        else:
                            term *= oriented(source, a, b)[ca][cb]
                        if term == 0:
                            break
                    total += term
        if total != 0:
            out[word] = total
    return out


def outer(u, v):
    return [[u[i] * v[j] for j in range(3)] for i in range(3)]


def cap_scalars_general(source, p, q, K):
    apq = oriented(source, p, q)
    s = sum(K[i][j] * apq[i][j] for i in range(3) for j in range(3))
    return s, [K[c][c] for c in COLORS]
