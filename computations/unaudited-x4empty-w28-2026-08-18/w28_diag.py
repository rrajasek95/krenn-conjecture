#!/usr/bin/env python3
"""W28 -- the fast EXACT decision routine for DIAGONAL backgrounds at N = 8.

W28-DEC: for a diagonal background on V' = V - z the colour-c system at z has
only SEVEN unknowns x_y = A_zy[c][y-colour c] and its rows are

    P(S_1,S_2) * ( haf(t^c | S_0 - y) )_{y in S_0},
    P = haf(t^d|S_1) haf(t^e|S_2),

one per partition V' = S_0 + S_1 + S_2 with |S_0| odd and |S_1|, |S_2| even
(the words whose extension by c at z is k-near-constant), the constant word
being S_0 = V'.  Everything is memoised over the 2^7 vertex subsets, so one
decision costs a few thousand ring operations and is EXACT.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x4empty-w28-2026-08-18")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import w28_core as K                                              # noqa: E402

NS = 7
VP = tuple(range(NS))
_PARTS = {}


def parts(c, k=4):
    """[(S_0, S_1, S_2, is_constant)] for the colour-c system."""
    key = (c, k)
    if key in _PARTS:
        return _PARTS[key]
    d, e = [x for x in range(3) if x != c]
    out = []
    for s in range(1, NS + 1, 2):
        for S0 in combinations(VP, s):
            T = [x for x in VP if x not in S0]
            for m in range(0, len(T) + 1, 2):
                for S1 in combinations(T, m):
                    S2 = tuple(x for x in T if x not in S1)
                    w = [c] * 8
                    for y in S1:
                        w[y] = d
                    for y in S2:
                        w[y] = e
                    if K.offcount(tuple(w)) > k:
                        continue
                    out.append((S0, S1, S2, s == NS))
    out.sort(key=lambda r: (not r[3], len(r[0]), r[0]))
    _PARTS[key] = out
    return out


def haf_table(t, zero, one):
    """{subset : haf(t|subset)} over all even subsets of V'."""
    tab = {}
    for m in range(0, NS + 1, 2):
        for S in combinations(VP, m):
            tab[S] = K.haf_w(t, S, zero, one)
    return tab


def diag_feasible(ts, c, k=4, zero=None, one=None, early=True):
    """(feasible?, rank_mixed) for the colour-c system, EXACT."""
    if zero is None:
        zero, one = Fraction(0), Fraction(1)
    d, e = [x for x in range(3) if x != c]
    H = [haf_table(ts[i], zero, one) for i in range(3)]
    rows = []
    crow = None
    for (S0, S1, S2, isc) in parts(c, k):
        P = H[d][S1] * H[e][S2]
        if P == 0:
            continue
        row = [zero] * NS
        nz = False
        for y in S0:
            v = P * H[c][tuple(x for x in S0 if x != y)]
            row[y] = v
            nz = nz or v != 0
        if isc:
            crow = row
            continue
        if not nz:
            continue
        rows.append(row)
        if early and _rank(rows) == NS:
            return False, NS
    r = _rank(rows)
    if crow is None or all(x == 0 for x in crow):
        return False, r
    return (_rank(rows + [crow]) > r), r


def _rank(rows):
    m = [list(r) for r in rows]
    rk = 0
    for col in range(NS):
        p = None
        for i in range(rk, len(m)):
            if m[i][col] != 0:
                p = i
                break
        if p is None:
            continue
        m[rk], m[p] = m[p], m[rk]
        pv = m[rk][col]
        inv = pv.inv() if K.is_cyc(pv) else 1 / pv
        for i in range(len(m)):
            if i != rk and m[i][col] != 0:
                f = m[i][col] * inv
                m[i] = [a - f * b for a, b in zip(m[i], m[rk])]
        rk += 1
        if rk == len(m):
            break
    return rk


def free_sites(ts, c, zero=None, one=None):
    """The y in V' whose every even split of V' - y is inactive (W28-FREE)."""
    if zero is None:
        zero, one = Fraction(0), Fraction(1)
    d, e = [x for x in range(3) if x != c]
    H = [haf_table(ts[i], zero, one) for i in range(3)]
    out = []
    for y in VP:
        W = tuple(x for x in VP if x != y)
        ok = True
        for m in range(0, len(W) + 1, 2):
            for S1 in combinations(W, m):
                S2 = tuple(x for x in W if x not in S1)
                if H[d][S1] * H[e][S2] != 0:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            out.append(y)
    return out


def rung_profile(ts, ks=(1, 2, 3, 4), zero=None, one=None):
    out = {}
    for k in ks:
        n = sum(1 for c in range(3)
                if diag_feasible(ts, c, k, zero, one)[0])
        out[k] = n
        if n == 0:
            for kk in ks:
                if kk > k:
                    out[kk] = 0
            break
    return out
