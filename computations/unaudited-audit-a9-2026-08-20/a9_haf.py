#!/usr/bin/env python3
"""A9 AUDIT -- independent hafnian / diagonal-source layer.

Written from scratch for the audit of W29-T1.  Three independent routes:

  R1  haf_dp(t,S)   -- Laplace/DP recursion memoised on a bitmask.
  R2  haf_pm(t,S)   -- direct enumeration of perfect matchings.
  R3  H_word(A,w)   -- the RAW Krenn-Gu matching sum with full 3x3 blocks,
                       sum over PMs of prod A[edge][w(u)][w(v)].

The diagonal product formula H_w = prod_c haf(t^c | w^{-1}(c)) is a CLAIM;
R3 vs R1 is the test of it (never assumed).

Conventions: V = {0,...,N-1}; edges are sorted pairs; all arithmetic exact
(Fraction), with an optional mod-p mode for ledger 19.
"""
from __future__ import annotations

import itertools
from fractions import Fraction


def ek(a, b):
    return (a, b) if a < b else (b, a)


# --------------------------------------------------------------- R1: DP
def haf_dp(t, S, zero=None, one=None):
    """haf over the site list S by Laplace on the smallest element (memo)."""
    if zero is None:
        zero, one = Fraction(0), Fraction(1)
    S = tuple(sorted(S))
    memo = {}

    def rec(sub):
        if not sub:
            return one
        if len(sub) % 2:
            return zero
        if sub in memo:
            return memo[sub]
        w, rest = sub[0], sub[1:]
        acc = zero
        for i, u in enumerate(rest):
            v = t.get(ek(w, u), zero)
            if v == 0:
                continue
            acc = acc + v * rec(rest[:i] + rest[i + 1:])
        memo[sub] = acc
        return acc

    return rec(S)


# --------------------------------------------------------------- R2: PMs
_PM_CACHE = {}


def perfect_matchings(S):
    """All perfect matchings of the tuple S, as tuples of sorted pairs."""
    S = tuple(sorted(S))
    if S in _PM_CACHE:
        return _PM_CACHE[S]
    if len(S) % 2:
        out = []
    elif not S:
        out = [()]
    else:
        out = []
        a = S[0]
        for i in range(1, len(S)):
            b = S[i]
            rest = S[1:i] + S[i + 1:]
            for M in perfect_matchings(rest):
                out.append(tuple(sorted(((a, b),) + M)))
    _PM_CACHE[S] = out
    return out


def haf_pm(t, S, zero=None, one=None):
    if zero is None:
        zero, one = Fraction(0), Fraction(1)
    tot = zero
    for M in perfect_matchings(S):
        p = one
        for e in M:
            p = p * t.get(e, zero)
            if p == 0:
                break
        tot = tot + p
    return tot


# ------------------------------------------------------- R3: raw word sum
def H_word(A, w, V, zero=None, one=None):
    """RAW definition: sum over perfect matchings of V of the product of the
    block entries A[edge][w(u)][w(v)] (u<v).  A[edge] is a 3x3 nested list."""
    if zero is None:
        zero, one = Fraction(0), Fraction(1)
    tot = zero
    for M in perfect_matchings(tuple(V)):
        p = one
        for (u, v) in M:
            p = p * A[(u, v)][w[u]][w[v]]
            if p == 0:
                break
        tot = tot + p
    return tot


def diag_blocks(ts, V, zero=None):
    """The 3x3 blocks of the DIAGONAL source with weights ts = (t^0,t^1,t^2)."""
    if zero is None:
        zero = Fraction(0)
    A = {}
    for e in itertools.combinations(sorted(V), 2):
        A[e] = [[ts[i].get(e, zero) if i == j else zero for j in range(3)]
                for i in range(3)]
    return A


# ------------------------------------------------------ exactness testing
def even_profiles(n, ncol=3):
    out = []
    for a in range(0, n + 1, 2):
        for b in range(0, n - a + 1, 2):
            c = n - a - b
            if c % 2 == 0:
                out.append((a, b, c))
    return out


def ordered_partitions(V, ncol=3):
    """All ordered ncol-tuples of disjoint sets covering V."""
    V = tuple(sorted(V))
    for assign in itertools.product(range(ncol), repeat=len(V)):
        parts = tuple(tuple(v for v, a in zip(V, assign) if a == c)
                      for c in range(ncol))
        yield parts


def exact_violations_raw(ts, n, kmax=None, haf=haf_dp, stop=False):
    """Violations of EXACT (or of X_kmax) for the diagonal source ts on K_n,
    computed straight from the definition over ALL 3^n words.

    kmax=None -> full exactness; otherwise only words with off-count <= kmax.
    """
    V = tuple(range(n))
    bad = []
    for parts in ordered_partitions(V):
        sizes = [len(p) for p in parts]
        off = n - max(sizes)
        if kmax is not None and off > kmax:
            continue
        val = Fraction(1)
        for c in range(3):
            val = val * haf(ts[c], parts[c])
        if off == 0:                            # constant word
            if val != 1:
                bad.append(("PURE", parts, val))
                if stop:
                    return bad
        else:
            if val != 0:
                bad.append(("MIX", parts, val))
                if stop:
                    return bad
    return bad
