#!/usr/bin/env python3
"""W10 -- exact integer/rational linear algebra (no floats anywhere).

* ``rank_exact``  : rank over Q of a list-of-lists of Fractions/ints, by
  fraction-free row reduction with content removal (pure Python ints).
* ``nullspace_exact`` : an exact basis of the kernel over Q.
* ``solve_exact`` : one exact solution of M x = b, or None.
"""
from __future__ import annotations

from fractions import Fraction as F
from math import gcd


def _to_int_rows(mat):
    """Clear denominators row-wise; return list of integer lists."""
    rows = []
    for row in mat:
        fr = [F(x) for x in row]
        den = 1
        for x in fr:
            den = den * x.denominator // gcd(den, x.denominator)
        ir = [int(x * den) for x in fr]
        g = 0
        for x in ir:
            g = gcd(g, abs(x))
        if g > 1:
            ir = [x // g for x in ir]
        rows.append(ir)
    return rows


def rank_exact(mat):
    """Exact rank over Q."""
    if not mat:
        return 0
    rows = _to_int_rows(mat)
    ncols = len(rows[0])
    pivots = []          # (col, integer row)
    rank = 0
    for r in rows:
        cur = r[:]
        for col, prow in pivots:
            if cur[col]:
                a, b = prow[col], cur[col]
                cur = [a * x - b * y for x, y in zip(cur, prow)]
                g = 0
                for x in cur:
                    g = gcd(g, abs(x))
                if g > 1:
                    cur = [x // g for x in cur]
        col = next((c for c in range(ncols) if cur[c]), None)
        if col is not None:
            pivots.append((col, cur))
            rank += 1
    return rank


def rref_exact(mat, ncols):
    """Reduced row echelon form over Q (Fractions).  Returns (rows, pivotcols)."""
    rows = [[F(x) for x in row] for row in mat]
    pivot_cols = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        lead = rows[r][c]
        rows[r] = [x / lead for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        pivot_cols.append(c)
        r += 1
        if r == len(rows):
            break
    return rows[:r], pivot_cols


def nullspace_exact(mat, ncols):
    """Exact basis of {x : M x = 0} over Q."""
    rows, piv = rref_exact(mat, ncols)
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for fcol in free:
        vec = [F(0)] * ncols
        vec[fcol] = F(1)
        for i, pc in enumerate(piv):
            vec[pc] = -rows[i][fcol]
        basis.append(vec)
    return basis


def solve_exact(mat, rhs, ncols):
    """One exact solution of M x = rhs over Q, or None if inconsistent."""
    aug = [list(row) + [rhs[i]] for i, row in enumerate(mat)]
    rows, piv = rref_exact(aug, ncols + 1)
    if ncols in piv:
        return None                      # inconsistent
    x = [F(0)] * ncols
    for i, pc in enumerate(piv):
        x[pc] = rows[i][ncols]
    return x
