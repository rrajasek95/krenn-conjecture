#!/usr/bin/env python3
"""adv2 -- index-compiled exact evaluator (Fraction / F_p / exact ext ring).

UNAUDITED.  EXACT ONLY.  A point is a flat list P of 9*|Gamma| ring
elements; IDX[(e,a,b)] gives the slot.  Every hafnian we need is compiled
once into a list of index tuples per word, so evaluation is a pure
multiply-add over the ring with no dictionary work.

Validated cell-by-cell against a2lib (hence against w26_core.H_word).
"""
from __future__ import annotations

import os
import sys
from fractions import Fraction
from itertools import combinations

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a2lib as A                                                 # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction
WORDS = C.WORDS
WIDX = {w: i for i, w in enumerate(WORDS)}
MIXSET = set(C.MIXED)


class Fastm:
    """compiled geometry for one m."""
    _c = {}

    def __new__(cls, m):
        if m in cls._c:
            return cls._c[m]
        s = super().__new__(cls)
        s.m = m
        s.G = A.Geo(m)
        s.gam = list(s.G.gam)
        s.base = {e: 9 * k for k, e in enumerate(s.gam)}
        s.n = 9 * len(s.gam)
        s._haf = {}
        cls._c[m] = s
        return s

    def slot(self, e, a, b):
        return self.base[e] + 3 * a + b

    # --------------------------------------------------- compiled hafnians
    def pms(self, S):
        """perfect matchings of Gamma restricted to S."""
        S = tuple(sorted(S))
        out = []

        def rec(vs, acc):
            if not vs:
                out.append(tuple(acc))
                return
            a = vs[0]
            for i in range(1, len(vs)):
                b = vs[i]
                e = (a, b) if a < b else (b, a)
                if e in self.G.gs:
                    rec(vs[1:i] + vs[i + 1:], acc + [e])
        rec(S, [])
        return out

    def haf_table(self, S):
        """list over all 6561 words of the tuple of index-tuples."""
        S = tuple(sorted(S))
        if S in self._haf:
            return self._haf[S]
        ms = self.pms(S)
        tab = []
        for w in WORDS:
            tab.append(tuple(tuple(self.slot(e, w[e[0]], w[e[1]]) for e in M)
                             for M in ms))
        self._haf[S] = tab
        return tab

    def phi_tab(self):
        return self.haf_table(tuple(range(8)))

    def coef_tab(self, e):
        return self.haf_table(tuple(v for v in range(8) if v not in e))


def ev(P, terms):
    """sum of products of P at the given index tuples (generic ring)."""
    t = 0
    for mono in terms:
        p = P[mono[0]]
        for i in mono[1:]:
            p = p * P[i]
        t = t + p
    return t


def ev_p(P, terms, p):
    t = 0
    for mono in terms:
        q = P[mono[0]]
        for i in mono[1:]:
            q = q * P[i]
        t += q
    return t % p


# ---------------------------------------------------------------- helpers
def to_flat(m, bl):
    fm = Fastm(m)
    P = [None] * fm.n
    for e in fm.gam:
        for a in range(3):
            for b in range(3):
                P[fm.slot(e, a, b)] = bl[e][a][b]
    return P


def to_blocks(m, P):
    fm = Fastm(m)
    return {e: [[P[fm.slot(e, a, b)] for b in range(3)] for a in range(3)]
            for e in fm.gam}


def phi_all(m, P, p=None):
    fm = Fastm(m)
    tab = fm.phi_tab()
    if p is None:
        return [ev(P, t) for t in tab]
    return [ev_p(P, t, p) for t in tab]


def clean_ok(m, P, p=None):
    fm = Fastm(m)
    tab = fm.phi_tab()
    for w in fm.G.clean:
        v = ev(P, tab[WIDX[w]]) if p is None else ev_p(P, tab[WIDX[w]], p)
        if v != 0:
            return False
    return True


def allnz(m, P, p=None):
    if p is None:
        return all(x != 0 for x in P)
    return all(x % p != 0 for x in P)
