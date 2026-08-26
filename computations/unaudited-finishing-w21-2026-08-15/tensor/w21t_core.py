#!/usr/bin/env python3
"""W21-M1-TENSOR core -- the identically-vanishing K_4 hafnian.
UNAUDITED.  Exact arithmetic only (Fraction / int).  No floats anywhere.

THE OBJECT.  Six 3x3 matrices M_{ij}, {i,j} a 2-subset of {1,2,3,4}
(stored with keys (1,2),(1,3),(1,4),(2,3),(2,4),(3,4)), subject to

  (T)  M12[y1][y2] M34[y3][y4] + M13[y1][y3] M24[y2][y4]
       + M14[y1][y4] M23[y2][y3] = 0     for all y in {0,1,2}^4.

EQUIVALENT FORMS (verified in w21t_verify.py):
  (SLICE)  for all r,s:  M34[r][s] * M12 + (M13 e_r)(M24 e_s)^T
                          + (M14 e_s)(M23 e_r)^T = 0     (3x3 matrices)
  (STAR)   for all u,v in C^3:
            <u, M34 v> M12 + (M13 u)(M24 v)^T + (M14 v)(M23 u)^T = 0
  and the five slot-permuted analogues of (SLICE)/(STAR).

  (RANK)   in the grouping (12|34) the 9x9 matrix is
             vec(M12) vec(M34)^T + Kron(M13,M24) + Kron(M14,M23).P
           so rank( Kron(M13,M24) + Kron(M14,M23).P ) <= 1, giving
             | r13 r24 - r14 r23 | <= 1,
           and cyclically  | r12 r34 - r14 r23 | <= 1,
                           | r12 r34 - r13 r24 | <= 1.

SYMMETRY.  S_4 permutes the slots (M_{ij} -> M_{sigma i, sigma j},
transposing when sigma reverses the order).  The gauge
M_{ij}[a][b] -> lam_{i,a} lam_{j,b} M_{ij}[a][b] (12 parameters) preserves
(T) up to the scalar prod_i lam_{i,y_i}, hence preserves the solution set.

SITE FACTORING.  Site i FACTORS when the three M's incident to i are all
rank <= 1 with a common i-side (row-index) vector.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True

PAIRS = tuple(combinations((1, 2, 3, 4), 2))
PAIRINGS = (((1, 2), (3, 4)), ((1, 3), (2, 4)), ((1, 4), (2, 3)))


def entry(M, i, j, yi, yj):
    """M_{ij} entry with the FIRST index belonging to slot i (i<j)."""
    return M[(i, j)][yi][yj]


def haf_value(M, y):
    """y is a dict slot -> colour (or a 4-tuple for slots 1..4)."""
    if not isinstance(y, dict):
        y = {k + 1: y[k] for k in range(4)}
    t = Fraction(0)
    for (a, b), (c, d) in PAIRINGS:
        t += M[(a, b)][y[a]][y[b]] * M[(c, d)][y[c]][y[d]]
    return t


def all_equations(M):
    return [haf_value(M, y) for y in product(range(3), repeat=4)]


def satisfies(M):
    return all(v == 0 for v in all_equations(M))


# ------------------------------------------------------------ linear algebra
def rref(rows, ncols):
    A = [list(r) for r in rows]
    piv, r = [], 0
    for c in range(ncols):
        sel = None
        for i in range(r, len(A)):
            if A[i][c]:
                sel = i
                break
        if sel is None:
            continue
        A[r], A[sel] = A[sel], A[r]
        pv = A[r][c]
        A[r] = [x / pv for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv.append(c)
        r += 1
        if r == len(A):
            break
    return A[:r], piv


def rank(Mx):
    if not Mx:
        return 0
    return len(rref(Mx, len(Mx[0]))[0])


def col(Mx, j):
    return [Mx[i][j] for i in range(len(Mx))]


def transpose(Mx):
    return [[Mx[i][j] for i in range(len(Mx))] for j in range(len(Mx[0]))]


def matmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)]
            for i in range(n)]


def matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def outer(u, v):
    return [[u[i] * v[j] for j in range(len(v))] for i in range(len(u))]


def madd(*Ms):
    n, m = len(Ms[0]), len(Ms[0][0])
    return [[sum(M[i][j] for M in Ms) for j in range(m)] for i in range(n)]


def smul(c, A):
    return [[c * x for x in row] for row in A]


def zeros(n=3, m=3):
    return [[Fraction(0)] * m for _ in range(n)]


def is_zero(A):
    return all(x == 0 for row in A for x in row)


# ------------------------------------------------------------ the two forms
def slice_matrix(M, r, s):
    """M34[r][s] M12 + (M13 e_r)(M24 e_s)^T + (M14 e_s)(M23 e_r)^T."""
    return madd(smul(M[(3, 4)][r][s], M[(1, 2)]),
                outer(col(M[(1, 3)], r), col(M[(2, 4)], s)),
                outer(col(M[(1, 4)], s), col(M[(2, 3)], r)))


def star_matrix(M, u, v):
    """<u, M34 v> M12 + (M13 u)(M24 v)^T + (M14 v)(M23 u)^T."""
    w = matvec(M[(3, 4)], v)
    c = sum(u[i] * w[i] for i in range(3))
    return madd(smul(c, M[(1, 2)]),
                outer(matvec(M[(1, 3)], u), matvec(M[(2, 4)], v)),
                outer(matvec(M[(1, 4)], v), matvec(M[(2, 3)], u)))


def kron(A, B):
    """rows (a,b) -> 3a+b, cols (c,d) -> 3c+d."""
    return [[A[a][c] * B[b][d] for c in range(3) for d in range(3)]
            for a in range(3) for b in range(3)]


def group_matrix(M, grouping=0):
    """the 9x9 matrix of the tensor in one of the three groupings."""
    if grouping == 0:                       # rows (y1,y2), cols (y3,y4)
        return [[haf_value(M, (a, b, c, d)) for c in range(3)
                 for d in range(3)] for a in range(3) for b in range(3)]
    if grouping == 1:                       # rows (y1,y3), cols (y2,y4)
        return [[haf_value(M, (a, c, b, d)) for c in range(3)
                 for d in range(3)] for a in range(3) for b in range(3)]
    return [[haf_value(M, (a, c, d, b)) for c in range(3)
             for d in range(3)] for a in range(3) for b in range(3)]


def ranks(M):
    return {p: rank(M[p]) for p in PAIRS}


def site_factors(M, i):
    """all three M's at slot i are rank <=1 with a common i-side vector."""
    vs = []
    for j in (1, 2, 3, 4):
        if j == i:
            continue
        p = (min(i, j), max(i, j))
        A = M[p] if p[0] == i else transpose(M[p])
        if rank(A) > 1:
            return False
        for c in range(3):
            v = col(A, c)
            if any(v):
                vs.append(v)
    if not vs:
        return True
    return rank(vs) <= 1


def any_site_factors(M):
    return [i for i in (1, 2, 3, 4) if site_factors(M, i)]


# ------------------------------------------------------------- constructors
def rand_matrix(rng, lo=-6, hi=6, den=3):
    return [[Fraction(rng.randint(lo, hi), rng.randint(1, den))
             for _ in range(3)] for _ in range(3)]


def rank1(u, v):
    return outer(u, v)
