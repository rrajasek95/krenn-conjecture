"""AUDIT A1 -- exact rational simplex (Fractions only).

Written from scratch for this audit.  W3 uses scipy's floating `linprog`
to FIND certificates and then re-checks them exactly; that route can only
certify FEASIBILITY, never infeasibility.  Deciding W3's dichotomy needs
exact infeasibility proofs on both sides, so this module implements a
complete Phase-I/Phase-II simplex with Bland's rule over Q.

Standard form:   min c.x   s.t.  Ax = b,  x >= 0.
"""

from __future__ import annotations

from fractions import Fraction

ZERO = Fraction(0)
ONE = Fraction(1)


class LPError(Exception):
    pass


def _pivot(T, basis, r, cidx):
    piv = T[r][cidx]
    if piv == 0:
        raise LPError("zero pivot")
    T[r] = [x / piv for x in T[r]]
    for i in range(len(T)):
        if i != r and T[i][cidx] != 0:
            f = T[i][cidx]
            T[i] = [a - f * b for a, b in zip(T[i], T[r])]
    basis[r] = cidx


def _simplex_core(T, basis, ncols, forbidden=()):
    """T is (m+1) x (ncols+1); last row is the (reduced) objective, last col
    the rhs.  Minimisation.  Bland's rule => finite termination."""
    m = len(T) - 1
    it = 0
    while True:
        it += 1
        if it > 200000:
            raise LPError("iteration limit")
        enter = -1
        for j in range(ncols):
            if j in forbidden:
                continue
            if T[m][j] < 0:
                enter = j
                break
        if enter < 0:
            return "optimal"
        leave = -1
        best = None
        for i in range(m):
            if T[i][enter] > 0:
                ratio = T[i][ncols] / T[i][enter]
                if best is None or ratio < best or (ratio == best and basis[i] < basis[leave]):
                    best = ratio
                    leave = i
        if leave < 0:
            return "unbounded"
        _pivot(T, basis, leave, enter)


def solve(A, b, c):
    """Returns (status, x, obj).  status in optimal/infeasible/unbounded."""
    m = len(A)
    n = len(A[0]) if m else 0
    A = [[Fraction(x) for x in row] for row in A]
    b = [Fraction(x) for x in b]
    c = [Fraction(x) for x in c]
    for i in range(m):
        if b[i] < 0:
            A[i] = [-x for x in A[i]]
            b[i] = -b[i]
    # ---- phase I
    ncols = n + m
    T = []
    for i in range(m):
        row = A[i] + [ONE if k == i else ZERO for k in range(m)] + [b[i]]
        T.append(row)
    obj = [ZERO] * n + [ONE] * m + [ZERO]
    T.append(obj)
    basis = [n + i for i in range(m)]
    # price out the artificial basis
    for i in range(m):
        T[m] = [a - b_ for a, b_ in zip(T[m], T[i])]
    st = _simplex_core(T, basis, ncols)
    if st != "optimal":
        raise LPError("phase I " + st)
    if T[m][ncols] != 0:                     # objective = -(sum artificials)
        return "infeasible", None, None
    # drive artificials out of the basis where possible
    for i in range(m):
        if basis[i] >= n:
            piv = -1
            for j in range(n):
                if T[i][j] != 0:
                    piv = j
                    break
            if piv >= 0:
                _pivot(T, basis, i, piv)
    keep = [i for i in range(m) if basis[i] < n]
    T2 = [T[i][:n] + [T[i][ncols]] for i in keep]
    basis2 = [basis[i] for i in keep]
    # ---- phase II
    T2.append(list(c) + [ZERO])
    mm = len(T2) - 1
    for i in range(mm):
        f = T2[mm][basis2[i]]
        if f != 0:
            T2[mm] = [a - f * b_ for a, b_ in zip(T2[mm], T2[i])]
    st = _simplex_core(T2, basis2, n)
    if st == "unbounded":
        return "unbounded", None, None
    x = [ZERO] * n
    for i in range(mm):
        x[basis2[i]] = T2[i][n]
    return "optimal", x, -T2[mm][n]


def feasible(A, b):
    """Is {x >= 0 : Ax = b} nonempty?  Returns (bool, witness)."""
    st, x, _ = solve(A, b, [ZERO] * (len(A[0]) if A else 0))
    return (st == "optimal"), x
