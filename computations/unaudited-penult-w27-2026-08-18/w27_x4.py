#!/usr/bin/env python3
"""W27 -- fast machinery for the X_k site systems at N = 8.

THE REDUCTION (W27-R1).  W25's site-linearity says: every k-near-constant word
has SOME colour at a fixed site z, so "A in X_k" is exactly the consistency of
three linear systems in the 3(N-1) star unknowns at z, whose coefficients are
the cofactors  C^z_y(w) = Haf_{B - z - y}(A)_w  --  which involve ONLY the
blocks not touching z.  Therefore

    X_k(N) is nonempty
        <=>  there is a source B on K_{N-1} (the sites != z) for which all
             three colour systems at z are consistent.

CONSISTENCY CRITERION.  The right-hand side is e_{const} (1 on the constant
word, 0 on every mixed word), so the colour-c system is consistent iff

    r_const^{(c)}  is NOT in the row span of the mixed-word rows,

equivalently iff the common kernel W_c = {x : (mixed rows) x = 0} is not
annihilated by r_const^{(c)}.  In particular a NECESSARY condition is
    rank(mixed rows) <= 3(N-1) - 1.

Everything here is computed modulo a large prime for speed (SCREENING ONLY);
every hit is re-verified exactly by W25's raw word test in the runners.
Ledger 19: two primes, both = 1 mod 3.
"""
from __future__ import annotations

import sys
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-penult-w27-2026-08-18")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import w27_core as W                                              # noqa: E402
C = W.C

P1 = 1000003          # = 1 mod 3
P2 = 1000033          # = 1 mod 3
N = 8


# ------------------------------------------------------------ mod-p sources

def src_mod(src, p, n=N, ncol=3):
    """Source (Fraction / int entries) -> nested dict of ints mod p."""
    out = {}
    for (a, b), m in src.items():
        row = []
        for i in range(ncol):
            r = []
            for j in range(ncol):
                x = m[i][j]
                if C.is_om(x):
                    raise ValueError("Q(omega) not supported in the mod-p "
                                     "screen; use the exact route")
                from fractions import Fraction as F
                f = F(x)
                r.append(f.numerator % p * pow(f.denominator % p, p - 2, p) % p)
            row.append(r)
        out[(a, b)] = row
    return out


def oriented_mod(sm, u, v, ncol=3):
    if u < v:
        return sm[(u, v)]
    m = sm[(v, u)]
    return [[m[j][i] for j in range(ncol)] for i in range(ncol)]


# ------------------------------------------------------- cofactor tables

def cof_tables(sm, p, n=N, ncol=3, sites=None):
    """cof[(z,y)][word_on_U] = Haf_{U}(A)_word,  U = all sites except z,y.
    word_on_U is a tuple in increasing site order.  `sites` restricts z."""
    tabs = {}
    for z in (range(n) if sites is None else sites):
        for y in range(n):
            if y == z:
                continue
            if (z, y) in tabs:
                continue
            U = tuple(x for x in range(n) if x not in (z, y))
            pms = W.all_pms(U)
            tab = {}
            for word in product(range(ncol), repeat=len(U)):
                wd = {U[i]: word[i] for i in range(len(U))}
                tot = 0
                for M in pms:
                    pr = 1
                    for (a, b) in M:
                        pr = pr * oriented_mod(sm, a, b, ncol)[wd[a]][wd[b]] % p
                        if pr == 0:
                            break
                    tot = (tot + pr) % p
                tab[word] = tot
            tabs[(z, y)] = tab
            tabs[(y, z)] = tab       # same U
    return tabs


def word_bank(n=N, ncol=3, kmax=4):
    """k-near-constant words, grouped by off-count."""
    out = {}
    for w in C.near_constant_words(n, ncol, kmax):
        out.setdefault(C.offcount(w, ncol), []).append(w)
    return out


def build_rows(tabs, words, z, c, n=N, ncol=3):
    """Rows (as dicts col->coeff) and rhs for the colour-c system at site z."""
    cols = [(y, d) for y in range(n) if y != z for d in range(ncol)]
    idx = {t: i for i, t in enumerate(cols)}
    rows, rhs, tags = [], [], []
    for w in words:
        if w[z] != c:
            continue
        row = [0] * len(cols)
        for y in range(n):
            if y == z:
                continue
            U = tuple(x for x in range(n) if x not in (z, y))
            key = tuple(w[x] for x in U)
            v = tabs[(z, y)][key]
            if v:
                j = idx[(y, w[y])]
                row[j] = row[j] + v
        rows.append(row)
        rhs.append(1 if len(set(w)) == 1 else 0)
        tags.append(w)
    return rows, rhs, tags, cols


# ------------------------------------------------------ mod-p linear algebra

class Echelon:
    """Incremental reduced-echelon basis of augmented rows over F_p.

    Rows are (ncols coefficients, 1 right-hand side).  `add` returns
    'PIVOT' (row was independent), 'ZERO' (row reduced away, rhs also 0) or
    'INCONSISTENT' (row reduced to 0 = nonzero)."""

    __slots__ = ("p", "ncols", "basis", "rank")

    def __init__(self, ncols, p):
        self.p = p
        self.ncols = ncols
        self.basis = [None] * ncols
        self.rank = 0

    def reduce(self, row, rhs=0):
        p, nc = self.p, self.ncols
        v = [x % p for x in row] + [rhs % p]
        for c in range(nc):
            if v[c]:
                b = self.basis[c]
                if b is None:
                    return c, v
                f = v[c]
                v = [(x - f * y) % p for x, y in zip(v, b)]
        return None, v

    def add(self, row, rhs=0):
        c, v = self.reduce(row, rhs)
        if c is None:
            return "INCONSISTENT" if v[self.ncols] else "ZERO"
        inv = pow(v[c], self.p - 2, self.p)
        v = [x * inv % self.p for x in v]
        self.basis[c] = v
        self.rank += 1
        return "PIVOT"


def rank_mod(rows, ncols, p):
    E = Echelon(ncols, p)
    for r in rows:
        E.add(r)
    return E.rank


def feasible_mod(rows, rhs, ncols, p):
    """(consistent?, rank(mixed rows), rank(all rows)).

    The mixed rows go in first (rhs = 0, so they can never be inconsistent);
    consistency is then exactly 'the constant row does not reduce to
    0 = nonzero', i.e. r_const is NOT in the row span of the mixed rows."""
    E = Echelon(ncols, p)
    consts = []
    for r, b in zip(rows, rhs):
        if b:
            consts.append((r, b))
        else:
            E.add(r, 0)
    rmix = E.rank
    ok = True
    for r, b in consts:
        st = E.add(r, b)
        if st == "INCONSISTENT":
            ok = False
            break
    return ok, rmix, E.rank


def site_report(tabs, words, z, p, n=N, ncol=3):
    out = []
    for c in range(ncol):
        rows, rhs, tags, cols = build_rows(tabs, words, z, c, n, ncol)
        ok, rmix, rall = feasible_mod(rows, rhs, len(cols), p)
        out.append({"colour": c, "n_rows": len(rows), "rank": rall,
                    "rank_mixed": rmix, "feasible": ok,
                    "kernel_dim": len(cols) - rall})
    return out
