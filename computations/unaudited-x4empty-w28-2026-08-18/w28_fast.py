#!/usr/bin/env python3
"""W28 -- fast mod-p engine for the FULL 21-unknown site systems at N = 8.

Screening only (ledger 19: two primes, both = 1 mod 3); every hit is
re-verified exactly by w28_core / w28_sym.  Site z = 7, background on K_7.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x4empty-w28-2026-08-18")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import w28_core as K                                              # noqa: E402

P1 = 1000003          # = 1 mod 3
P2 = 1000033          # = 1 mod 3
NS, Z, N = 7, 7, 8

# perfect matchings of each 6-subset of {0..6}
SIX = [tuple(x for x in range(NS) if x != y) for y in range(NS)]
PM6 = [K.all_pms(S) for S in SIX]


def to_mod(src7, p):
    out = {}
    for (a, b), m in src7.items():
        out[(a, b)] = [[(Fraction(x).numerator % p
                         * pow(Fraction(x).denominator % p, p - 2, p)) % p
                        for x in row] for row in m]
    return out


def orient_mod(sm, u, v):
    if u < v:
        return sm[(u, v)]
    m = sm[(v, u)]
    return [[m[j][i] for j in range(3)] for i in range(3)]


def cof_tables(sm, p):
    """tab[y][word-on-SIX[y]] = Haf over the six sites != y."""
    tabs = []
    for y in range(NS):
        S = SIX[y]
        pos = {s: i for i, s in enumerate(S)}
        pms = [[(pos[a], pos[b]) for (a, b) in M] for M in PM6[y]]
        blocks = {}
        for (a, b) in combinations(S, 2):
            blocks[(pos[a], pos[b])] = orient_mod(sm, a, b)
        tab = {}
        for word in product(range(3), repeat=6):
            tot = 0
            for M in pms:
                pr = 1
                for (i, j) in M:
                    pr = pr * blocks[(i, j)][word[i]][word[j]] % p
                    if pr == 0:
                        break
                tot += pr
            tab[word] = tot % p
        tabs.append(tab)
    return tabs


def words_for(c, k):
    """k-near-constant words on the 7 background sites with colour c at z,
    constant first."""
    out = []
    const = (c,) * NS
    for u in product(range(3), repeat=NS):
        if K.offcount(u + (c,)) <= k:
            out.append(u)
    out.sort(key=lambda u: (u != const, sum(1 for x in u if x != c), u))
    return out


def feasible(tabs, c, k, p, uord=None):
    """(feasible?, rank_mixed).  Mixed rows first; break as soon as the mixed
    rank is 21 (then no nonzero x survives and the constant row cannot be
    satisfied)."""
    if uord is None:
        uord = words_for(c, k)
    E = K.Ech(21, p)
    const = (c,) * NS
    crow = None
    for u in uord:
        row = [0] * 21
        for y in range(NS):
            S = SIX[y]
            row[3 * y + u[y]] = (row[3 * y + u[y]]
                                 + tabs[y][tuple(u[a] for a in S)]) % p
        if u == const:
            crow = row
            continue
        if any(row):
            if E.add(row, 0) == "PIVOT" and E.rank == 21:
                return False, 21
    if crow is None or not any(crow):
        return False, E.rank
    return (E.add(crow, 1) != "INCONSISTENT"), E.rank


def rung_profile(src7, p=P1, ks=(1, 2, 3, 4), colours=(0, 1, 2), uords=None):
    """{k: number of colours whose system is feasible}."""
    sm = to_mod(src7, p)
    tabs = cof_tables(sm, p)
    out = {}
    for k in ks:
        n = 0
        for c in colours:
            uo = None if uords is None else uords[(c, k)]
            if feasible(tabs, c, k, p, uo)[0]:
                n += 1
        out[k] = n
        if n == 0:
            for kk in ks:
                if kk > k:
                    out[kk] = 0
            break
    return out
