#!/usr/bin/env python3
"""W25 -- exact site-linear walk / projection on the ladder X_k.

SITE LINEARITY.  H_B(A)_w = sum_{y != z} A_zy[w_z][w_y] C^z_y(w) with
C^z_y(w) = Haf_{B-z-y}(A)_w independent of every block at z.  So "A in X_k" is,
in the 3(N-1) star unknowns at a SINGLE site z, three independent inhomogeneous
linear systems (one per colour at z).  Consequences used here:

  (P) Solving all three systems at ONE site z makes EVERY k-near-constant word
      exact, i.e. lands the source in X_k outright (every such word has some
      colour at z).  So "project into X_k" = "one feasible site solve".
  (W) Re-solving at other sites and resampling kernels walks X_k exactly.

Works over Q and over Q(omega) (w25_core.Om).
"""
from __future__ import annotations

import sys
from fractions import Fraction

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x3core-w25-2026-08-15")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import w25_core as C                                            # noqa: E402


def cofactor_tensor(src, z, y, word, n, ncol=C.NCOL):
    rest = tuple(x for x in range(n) if x not in (z, y))
    return C.haf_sub(src, {a: word[a] for a in rest}, rest, ncol)


def site_systems(src, z, n, k, ncol=C.NCOL, words=None):
    """Three linear systems at z (one per colour at z) for membership in X_k."""
    sample = src[(0, 1)][0][0]
    zz = C.zeroelt(sample)
    oo = C.oneelt(sample)
    if words is None:
        words = C.near_constant_words(n, ncol, k)
    cols = [(y, d) for y in range(n) if y != z for d in range(ncol)]
    idx = {t: i for i, t in enumerate(cols)}
    out = {}
    for c in range(ncol):
        rows, rhs, tags = [], [], []
        for word in words:
            if word[z] != c:
                continue
            row = [zz] * len(cols)
            for y in range(n):
                if y == z:
                    continue
                row[idx[(y, word[y])]] = (row[idx[(y, word[y])]]
                                          + cofactor_tensor(src, z, y, word,
                                                            n, ncol))
            rows.append(row)
            rhs.append(oo if len(set(word)) == 1 else zz)
            tags.append(word)
        out[c] = (rows, rhs, tags, cols)
    return out


def apply_site_solution(src, z, sol, cols, n, ncol=C.NCOL):
    out = C.copy_source(src)
    for c in range(ncol):
        for kk, (y, d) in enumerate(cols):
            val = sol[c][kk]
            if z < y:
                out[(z, y)][c][d] = val
            else:
                out[(y, z)][d][c] = val
    return out


def site_solve(src, z, n, k, rng=None, ncol=C.NCOL, spread=3,
               keep_particular=False, words=None, coeffs=None):
    """One exact site-linear solve at z.  Returns (new_src, kernel dims) or
    (None, None) if infeasible there."""
    sysd = site_systems(src, z, n, k, ncol, words)
    sol, dims = {}, []
    for c in range(ncol):
        rows, rhs, tags, cols = sysd[c]
        part, kern = C.solve_linear(rows, rhs, len(cols))
        if part is None:
            return None, None
        dims.append(len(kern))
        vec = list(part)
        if not keep_particular and rng is not None:
            for i, kv in enumerate(kern):
                if coeffs is not None:
                    lam = coeffs[c][i]
                else:
                    lam = Fraction(rng.randint(-spread, spread))
                    if C.is_om(rhs[0]) if rhs else False:
                        lam = C.Om(rng.randint(-spread, spread),
                                   rng.randint(-spread, spread))
                if lam != 0:
                    vec = [a + lam * b for a, b in zip(vec, kv)]
        sol[c] = vec
    cols = sysd[0][3]
    return apply_site_solution(src, z, sol, cols, n, ncol), dims


def site_dims(src, n, k, ncol=C.NCOL, words=None):
    """Per-site kernel dimensions (None where infeasible)."""
    out = []
    for z in range(n):
        sysd = site_systems(src, z, n, k, ncol, words)
        row = []
        for c in range(ncol):
            rows, rhs, tags, cols = sysd[c]
            part, kern = C.solve_linear(rows, rhs, len(cols))
            row.append(None if part is None else len(kern))
        out.append(row)
    return out


def walk(src, n, k, rng, steps=6, spread=2, ncol=C.NCOL, order=None):
    """Walk X_k.  Returns the final source, or None if a step was infeasible."""
    cur = src
    for t in range(steps):
        z = (order[t % len(order)] if order else t % n)
        nxt, dims = site_solve(cur, z, n, k, rng, ncol, spread)
        if nxt is None:
            return None
        cur = nxt
    return cur
