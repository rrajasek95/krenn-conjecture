#!/usr/bin/env python3
"""A6 AUDIT -- fully independent engine for the K_8 / 3x3-block model.

Deliberately NOT importing w8_*/w12_*/w15_* code.  Different routes:
  * perfect matchings built as fixed-point-free involutions of S_8
    (filter over itertools.permutations), NOT by the recursive
    "match-the-lowest-unmatched" construction W15 uses;
  * polynomials as dict{ frozen exponent multiset (sorted tuple of
    integer var ids) -> int }, over Z (exact), with an independent
    sympy cross-check available;
  * template audit fields recomputed from scratch.

MODEL.  8 sites, colours {0,1,2}; a 3x3 block A_uv per edge u<v of K_8.
  H(A)_w = sum_{M perfect matching of K_8} prod_{uv in M} A_uv[w_u][w_v].
TEMPLATE: 9-bit mask per edge, bit 3i+j <=> cell (i,j) occupied.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product

N = 8
Q = 3
FULL = 511

EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}


# ---------------------------------------------------------------- matchings
def _matchings_via_involutions():
    """Perfect matchings of K_N as fixed-point-free involutions."""
    out = set()
    for p in permutations(range(N)):
        ok = True
        for i in range(N):
            if p[i] == i or p[p[i]] != i:
                ok = False
                break
        if ok:
            m = tuple(sorted({(min(i, p[i]), max(i, p[i])) for i in range(N)}))
            assert len(m) == N // 2
            out.add(m)
    return tuple(sorted(out))


MATCHINGS = _matchings_via_involutions()
assert len(MATCHINGS) == 105, len(MATCHINGS)
MATCH_EIDX = tuple(tuple(EIDX[e] for e in m) for m in MATCHINGS)

WORDS = tuple(product(range(Q), repeat=N))
CONST = tuple(tuple([c] * N) for c in range(Q))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)


def cell(ei, w):
    u, v = EDGES[ei]
    return 3 * w[u] + w[v]


def occ(T, ei, c):
    return (T[ei] >> c) & 1


def fibre(T, w):
    """Indices of matchings supported at w."""
    res = []
    for mi, eids in enumerate(MATCH_EIDX):
        if all(occ(T, e, cell(e, w)) for e in eids):
            res.append(mi)
    return res


def audit(T):
    m = sum(1 for t in T if t)
    sigma = sum(bin(t).count("1") for t in T)
    hist = {}
    for w in MIXED:
        s = len(fibre(T, w))
        hist[s] = hist.get(s, 0) + 1
    full = [EDGES[i] for i, t in enumerate(T) if t == FULL]
    singles = {EDGES[i]: (t.bit_length() - 1)
               for i, t in enumerate(T) if t and bin(t).count("1") == 1}
    partial = {EDGES[i]: t for i, t in enumerate(T)
               if t and t != FULL and bin(t).count("1") != 1}
    return dict(m=m, sigma=sigma, hist=hist, min_mixed=min(hist),
                consts=[len(fibre(T, w)) for w in CONST],
                full=full, singles=singles, partial=partial)


def gamma_matchings(T):
    """Matchings all of whose edges are FULL blocks (= F(Gamma))."""
    fulls = {i for i, t in enumerate(T) if t == FULL}
    return [mi for mi, eids in enumerate(MATCH_EIDX)
            if all(e in fulls for e in eids)]


# --------------------------------------------------- exact Z-polynomials
# monomial = sorted tuple of var ids (with repetition); coeff = int
def padd(a, b):
    o = dict(a)
    for m, c in b.items():
        n = o.get(m, 0) + c
        if n:
            o[m] = n
        else:
            o.pop(m, None)
    return o


def pneg(a):
    return {m: -c for m, c in a.items()}


def psub(a, b):
    return padd(a, pneg(b))


def pmul(a, b):
    o = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            mm = tuple(sorted(ma + mb))
            n = o.get(mm, 0) + ca * cb
            if n:
                o[mm] = n
            else:
                o.pop(mm, None)
    return o


def pmulmon(a, mon, c=1):
    mon = tuple(sorted(mon))
    return {tuple(sorted(m + mon)): v * c for m, v in a.items()}


def peval(a, val):
    t = Fraction(0)
    for m, c in a.items():
        x = Fraction(c)
        for v in m:
            x *= val[v]
        t += x
    return t


class Vars:
    """One variable per occupied cell."""

    def __init__(self, T):
        self.T = tuple(T)
        self.id = {}
        self.name = []
        for e in range(len(EDGES)):
            for c in range(9):
                if occ(T, e, c):
                    self.id[(e, c)] = len(self.name)
                    u, v = EDGES[e]
                    self.name.append("A%d%d_%d%d" % (u, v, c // 3, c % 3))

    def v(self, ei, c):
        return self.id[(ei, c)]

    def vw(self, uv, w):
        """variable for edge uv at the cell selected by word w."""
        ei = EIDX[uv]
        return self.id[(ei, cell(ei, w))]

    def __len__(self):
        return len(self.name)


def Hpoly(T, V, w):
    """H_w as an exact polynomial over Z in the occupied-cell variables."""
    out = {}
    for mi in fibre(T, w):
        mon = tuple(sorted(V.v(e, cell(e, w)) for e in MATCH_EIDX[mi]))
        out = padd(out, {mon: 1})
    return out


def poly_str(p, V):
    if not p:
        return "0"
    parts = []
    for m in sorted(p, key=lambda t: (len(t), t)):
        c = p[m]
        s = "*".join(V.name[i] for i in m) if m else "1"
        parts.append(("+ " if c > 0 else "- ") +
                     (("%d*" % abs(c)) if abs(c) != 1 else "") + s)
    return " ".join(parts).lstrip("+ ").strip()


M24 = [511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 0,
       128, 32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511]
