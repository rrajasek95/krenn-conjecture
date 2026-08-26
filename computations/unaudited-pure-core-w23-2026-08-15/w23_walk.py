#!/usr/bin/env python3
"""W23 -- the L1+L2 variety and the exact site-linear walk on it.

DEFINITION.  A word w on B is k-NEAR-CONSTANT if some colour g has
|{i : w_i != g}| <= k.  The 0-near-constant words are the three constant words
(the PURE equations); the 1-near-constant words add the one-off words (Lemma
W22-S = L1); the 2-near-constant words add the two-off words (THEOREM W23-L2).

    X_k(N) := { sources A : H_B(A)_w = [w constant] for every k-near-constant
                word w }.

So X_0 = pure equations only, X_1 = pures + L1, X_2 = pures + L1 + L2, and
X_{N} = the exact variety.  W22-1's all-blocked family lives OUTSIDE X_0.

SITE LINEARITY (W22-L).  H_B(A)_w = sum_{y != z} A_zy[w_z][w_y] C^z_y(w) with
C^z_y(w) = Haf_{B\\{z,y}}(A)_w INDEPENDENT of every block at z.  Hence the
condition "A in X_k" is, in the 3(N-1) star unknowns at any single site z,
THREE INDEPENDENT INHOMOGENEOUS LINEAR SYSTEMS (one per colour at z).  Solving
them and resampling the kernel walks X_k exactly.

All arithmetic exact.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-pure-core-w23-2026-08-15")
sys.path.insert(0, BASE)
import w23_core as C                                          # noqa: E402


def near_constant_words(n, ncol=3, k=2):
    """All words with at most k sites off some constant background."""
    out = set()
    for g in range(ncol):
        base = (g,) * n
        out.add(base)
        for size in range(1, k + 1):
            for S in combinations(range(n), size):
                for vals in product([d for d in range(ncol)], repeat=size):
                    w = list(base)
                    for i, s in enumerate(S):
                        w[s] = vals[i]
                    out.add(tuple(w))
    return sorted(out)


def cofactor_tensor(src, z, y, word, n, ncol=3):
    """C^z_y(w) = Haf_{B - z - y}(A) at w restricted."""
    rest = tuple(x for x in range(n) if x not in (z, y))
    return C.haf_word(src, {a: word[a] for a in rest}, rest, ncol)


def site_systems(src, z, n, words, ncol=3):
    """Three linear systems at z (one per colour at z) over the given words."""
    cols = [(y, d) for y in range(n) if y != z for d in range(ncol)]
    idx = {t: i for i, t in enumerate(cols)}
    out = {}
    for c in range(ncol):
        rows, rhs, tags = [], [], []
        for word in words:
            if word[z] != c:
                continue
            row = [Fraction(0)] * len(cols)
            for y in range(n):
                if y == z:
                    continue
                row[idx[(y, word[y])]] += Fraction(
                    cofactor_tensor(src, z, y, word, n, ncol))
            rows.append(row)
            rhs.append(Fraction(1) if len(set(word)) == 1 else Fraction(0))
            tags.append(word)
        out[c] = (rows, rhs, tags, cols)
    return out


def solve_linear(rows, rhs):
    """Exact solve.  Returns (particular, kernel basis) or (None, None)."""
    ncols = len(rows[0]) if rows else 0
    m = [list(r) + [b] for r, b in zip(rows, rhs)]
    piv = []
    r = 0
    for c in range(ncols):
        p = None
        for i in range(r, len(m)):
            if m[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        inv = Fraction(1) / m[r][c]
        m[r] = [x * inv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv.append(c)
        r += 1
    for i in range(r, len(m)):
        if m[i][ncols] != 0 and all(x == 0 for x in m[i][:ncols]):
            return None, None
    part = [Fraction(0)] * ncols
    for i, c in enumerate(piv):
        part[c] = m[i][ncols]
    kern = []
    for f in [c for c in range(ncols) if c not in piv]:
        v = [Fraction(0)] * ncols
        v[f] = Fraction(1)
        for i, c in enumerate(piv):
            v[c] = -m[i][f]
        kern.append(v)
    return part, kern


def apply_site_solution(src, z, sol, cols, n, ncol=3):
    out = {e: [row[:] for row in m] for e, m in src.items()}
    for c in range(ncol):
        for k, (y, d) in enumerate(cols):
            val = sol[c][k]
            if z < y:
                out[(z, y)][c][d] = val
            else:
                out[(y, z)][d][c] = val
    return out


def in_Xk(src, n, words, ncol=3):
    """Exact membership test for X_k, given the word list."""
    for w in words:
        tgt = 1 if len(set(w)) == 1 else 0
        if C.H(src, w, n, ncol) != tgt:
            return False, w
    return True, None


def walk_step(src, z, n, words, rng, ncol=3, spread=3, keep_particular=False):
    """One exact site-linear step on X_k at site z.  Returns a new source or
    None if the system is infeasible there."""
    sysd = site_systems(src, z, n, words, ncol)
    sol = {}
    dims = []
    for c in range(ncol):
        rows, rhs, tags, cols = sysd[c]
        part, kern = solve_linear(rows, rhs)
        if part is None:
            return None, None
        dims.append(len(kern))
        vec = list(part)
        if not keep_particular:
            for kv in kern:
                lam = Fraction(rng.randint(-spread, spread))
                if lam:
                    vec = [a + lam * b for a, b in zip(vec, kv)]
        sol[c] = vec
    cols = sysd[0][3]
    return apply_site_solution(src, z, sol, cols, n, ncol), dims
