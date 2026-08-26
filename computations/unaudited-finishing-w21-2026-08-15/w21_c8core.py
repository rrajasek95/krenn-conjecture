#!/usr/bin/env python3
"""W21 MOVE 2 shared core -- the C_8 member of the empty-clean stratum.
UNAUDITED.  Exact arithmetic only (Fraction / exact sparse polynomials).

THE TEMPLATE (verified below against w21_core / W20):
  L = {0,1,2,3}, R = {4,5,6,7}.
  Inside L: six SINGLE blocks following the proper 3-edge-colouring of K_4,
    (0,1)->(0,0)  (0,2)->(1,1)  (0,3)->(2,2)
    (2,3)->(0,0)  (1,3)->(1,1)  (1,2)->(2,2)
  Inside R: the mirror,
    (4,5)->(0,0)  (4,6)->(1,1)  (4,7)->(2,2)
    (6,7)->(0,0)  (5,7)->(1,1)  (5,6)->(2,2)
  All 16 cross blocks occupied: 8 FULL (the Hamilton cycle Gamma =
    (0,4),(0,5),(1,6),(1,7),(2,5),(2,7),(3,4),(3,6)) and 8 FAT with one
    dead cell each:
    (0,6):(1,0)  (0,7):(2,0)  (1,4):(0,0)  (1,5):(1,1)
    (2,4):(2,1)  (2,6):(0,0)  (3,5):(2,2)  (3,7):(2,1)

THE L-FREE REDUCTION (W20, reproduced here as a control).
  An L-word x is L-FREE when no L-single is active, i.e. no k<l in L with
  x_k = x_l = the colour class of the edge kl.  There are 30 L-free words.
  For an L-free x and EVERY R-word y,

      H_(x,y)  =  per B(x,y),      B(x,y)[i][j] = A_{i,j}[x_i][y_j]

  (i in L, j in R; dead cells are 0).  Mirror for R-free y.  30*81 + 81*30
  - 30*30 = 3,960 of the 6,558 mixed equations are PURE 4x4 PERMANENTS in
  the 16 cross blocks; the 12 single cells drop out entirely.

THE GEOMETRIC FORM (W21).  Fix an L-free x.  per is multilinear in the
COLUMNS of B and column j depends on y only through y_j, so the equations
{H_(x,y) = 0 : all y} say exactly

      per vanishes identically on V_4^x x V_5^x x V_6^x x V_7^x,
      V_j^x = column span of M_j^x,
      M_j^x = the 4 x 3 matrix whose row i (i in L) is ROW x_i of A_{i,j}.

Each V_j^x has dim <= 3.  By Lemma W20-P (per vanishes identically on a
product of n >= 3 hyperplanes iff all are the SAME coordinate hyperplane --
impossible here because every occupied cell is nonzero) at least one j has
rank M_j^x <= 2; by W20-P4c at least TWO j's do when x is dead-cell-free
(only x = (0,2,1,0) and (0,2,1,1)).

    rank M_j^x <= 2  <=>  the four points of P^2
        [row x_0 of A_{0,j}], [row x_1 of A_{1,j}],
        [row x_2 of A_{2,j}], [row x_3 of A_{3,j}]
    are COLLINEAR.  So each R-site j carries an arrangement of 12 points of
    P^2 (three rows from each of four blocks) and the L-free obligations are
    COLLINEAR-TRANSVERSAL conditions in it.  Mirror: each L-site i carries
    12 points (three COLUMNS from each of four blocks) and the R-free
    obligations are the mirror transversal conditions.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True

L = (0, 1, 2, 3)
R = (4, 5, 6, 7)
LPOS = {v: k for k, v in enumerate(L)}
RPOS = {v: k for k, v in enumerate(R)}

EDGES = tuple(combinations(range(8), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}

C8_MEMBER = [1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
             383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1]

L_SINGLES = {(0, 1): (0, 0), (0, 2): (1, 1), (0, 3): (2, 2),
             (1, 2): (2, 2), (1, 3): (1, 1), (2, 3): (0, 0)}
R_SINGLES = {(4, 5): (0, 0), (4, 6): (1, 1), (4, 7): (2, 2),
             (5, 6): (2, 2), (5, 7): (1, 1), (6, 7): (0, 0)}
DEAD = {(0, 6): (1, 0), (0, 7): (2, 0), (1, 4): (0, 0), (1, 5): (1, 1),
        (2, 4): (2, 1), (2, 6): (0, 0), (3, 5): (2, 2), (3, 7): (2, 1)}
CROSS = tuple((i, j) for i in L for j in R)


def occupied(i, j, c, d):
    """is cell (c,d) of the cross block (i,j) occupied?"""
    return DEAD.get((i, j)) != (c, d)


def lfree(x):
    for (u, v), (a, b) in L_SINGLES.items():
        if x[LPOS[u]] == a and x[LPOS[v]] == b:
            return False
    return True


def rfree(y):
    for (u, v), (a, b) in R_SINGLES.items():
        if y[RPOS[u]] == a and y[RPOS[v]] == b:
            return False
    return True


LFREE = tuple(x for x in product(range(3), repeat=4) if lfree(x))
RFREE = tuple(y for y in product(range(3), repeat=4) if rfree(y))
assert len(LFREE) == 30 and len(RFREE) == 30

DEADFREE_L = tuple(x for x in LFREE
                   if all(occupied(i, j, x[LPOS[i]], d)
                          for i in L for j in R for d in range(3)))
DEADFREE_R = tuple(y for y in RFREE
                   if all(occupied(i, j, c, y[RPOS[j]])
                          for i in L for j in R for c in range(3)))
assert DEADFREE_L == ((0, 2, 1, 0), (0, 2, 1, 1)) and DEADFREE_R == ()

PERM4 = tuple(permutations(range(4)))


def per4(M):
    return sum(M[0][p[0]] * M[1][p[1]] * M[2][p[2]] * M[3][p[3]]
               for p in PERM4)


# ------------------------------------------------------------------ engine
def _pms(vs):
    if not vs:
        return [()]
    a, rest = vs[0], vs[1:]
    out = []
    for i, b in enumerate(rest):
        sub = rest[:i] + rest[i + 1:]
        for m in _pms(sub):
            out.append(((a, b),) + m)
    return out


PMS = tuple(tuple(sorted(m)) for m in _pms(tuple(range(8))))


def cell_occ(T, e, w):
    u, v = e
    return (T[EIDX[e]] >> (3 * w[u] + w[v])) & 1


def H_value(blocks, T, w):
    """H_w exactly, from the definition (blocks: dict edge -> 3x3)."""
    tot = Fraction(0)
    for m in PMS:
        if not all(cell_occ(T, e, w) for e in m):
            continue
        p = Fraction(1)
        for (u, v) in m:
            p *= blocks[(u, v)][w[u]][w[v]]
        tot += p
    return tot


def cross_matrix(blocks, x, y):
    return [[blocks[(i, j)][x[LPOS[i]]][y[RPOS[j]]] for j in R] for i in L]


def M_j(blocks, x, j):
    """the 4 x 3 matrix of L-side rows at R-site j for the L-word x."""
    return [[blocks[(i, j)][x[LPOS[i]]][d] for d in range(3)] for i in L]


def N_i(blocks, y, i):
    """mirror: the 4 x 3 matrix of R-side columns at L-site i for R-word y."""
    return [[blocks[(i, j)][c][y[RPOS[j]]] for c in range(3)] for j in R]


def rank(M):
    M = [[Fraction(x) for x in row] for row in M]
    r, nr = 0, len(M)
    nc = len(M[0]) if M else 0
    for c in range(nc):
        piv = None
        for i in range(r, nr):
            if M[i][c]:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(nr):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == nr:
            break
    return r


def random_blocks(rng, T=None):
    """random exact rational blocks respecting the template's zero pattern."""
    T = C8_MEMBER if T is None else T
    bl = {}
    for ei, e in enumerate(EDGES):
        m = T[ei]
        bl[e] = [[Fraction(rng.randint(-9, 9) or 4, rng.randint(1, 4))
                  if (m >> (3 * c + d)) & 1 else Fraction(0)
                  for d in range(3)] for c in range(3)]
    return bl
