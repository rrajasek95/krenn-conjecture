#!/usr/bin/env python3
"""W21-M2-GEO shared machinery.  UNAUDITED.  Exact arithmetic only.

Everything here is built on top of the verified core
    ../w21_c8core.py   (template, L/R split, L-free/R-free sets, per4, H engine)

THE PICTURE.  At R-site j in {4,5,6,7} the four cross blocks A_{i,j} (i in L)
supply 12 points of P^2,
        P^j_{i,c} = row c of A_{i,j}          (i in L, c in {0,1,2}),
grouped into 4 groups of 3.  For an L-word x the 4x3 matrix M_j^x has rows
P^j_{i,x_i}, and

        rank M_j^x <= 2   <=>   the four points P^j_{i,x_i} are COLLINEAR.

Mirror at L-site i: 12 points Q^i_{j,d} = column d of A_{i,j} (j in R,
d in {0,1,2}); rank N_i^y <= 2 <=> the four Q^i_{j,y_j} are collinear.

S_j := { x in {0,1,2}^4 : the transversal is collinear at j }  and S_j is a
UNION OF PRODUCT BOXES, one per line of the 12-point arrangement:
        line ell contributes  prod_i K_i(ell),  K_i(ell) = {c : P^j_{i,c} in ell}.
NOTE (contra W20): a contributing box need NOT be contained in the L-free set;
no equation forbids a collinear transversal at a non-L-free word.
"""
from __future__ import annotations

import os
import sys
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import w21_c8core as G                                              # noqa: E402

L, R = G.L, G.R
LPOS, RPOS = G.LPOS, G.RPOS
LFREE, RFREE = G.LFREE, G.RFREE
DEAD = G.DEAD
WORDS4 = tuple(product(range(3), repeat=4))


# ----------------------------------------------------------------- P^2 tools
def _f(v):
    return tuple(Fraction(a) for a in v)


def cross3(a, b):
    """cross product in C^3 (line through two points / point on two lines)."""
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot3(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def proj_eq(a, b):
    """do a, b represent the SAME point of P^2 (both assumed nonzero)?"""
    return all(z == 0 for z in cross3(a, b))


def normalise(v):
    """canonical representative of a point of P^2 over Q (first nonzero = 1)."""
    for z in v:
        if z != 0:
            return tuple(Fraction(a) / z for a in v)
    return None


# ----------------------------------------------------------- the arrangements
def points_R(blocks, j):
    """the 12 points at R-site j: dict (i,c) -> row c of A_{i,j}."""
    return {(i, c): _f(blocks[(i, j)][c]) for i in L for c in range(3)}


def points_L(blocks, i):
    """the 12 points at L-site i: dict (j,d) -> column d of A_{i,j}."""
    return {(j, d): _f([blocks[(i, j)][c][d] for c in range(3)])
            for j in R for d in range(3)}


def collinear_set(pts, groups, keys):
    """S = {word : the 4 chosen points are collinear}, brute force by rank."""
    out = set()
    for w in WORDS4:
        M = [pts[(groups[k], w[k])] for k in range(4)]
        if G.rank(M) <= 2:
            out.add(w)
    return out


def S_R(blocks, j):
    return collinear_set(points_R(blocks, j), L, None)


def S_L(blocks, i):
    return collinear_set(points_L(blocks, i), R, None)


# --------------------------------------------------------------- box structure
def boxes_of_site(pts, groups):
    """the LINE decomposition of the collinear set.

    Returns (boxes, S) where boxes is a list of (K_0,K_1,K_2,K_3) tuples of
    frozensets, one per line of the arrangement that carries a full
    transversal, and S the union of the boxes as a set of words.
    """
    keys = [(g, c) for g in groups for c in range(3)]
    # distinct points (as points of P^2)
    reps = {}
    for k in keys:
        n = normalise(pts[k])
        reps.setdefault(n, []).append(k)
    distinct = list(reps)
    lines = set()
    if len(distinct) == 1:                       # every line through the point
        lines.add(None)
    for a, b in combinations(distinct, 2):
        lines.add(normalise(cross3(a, b)))
    boxes, S = [], set()
    for ell in lines:
        if ell is None:
            K = [frozenset(range(3))] * 4
        else:
            K = []
            for gi, g in enumerate(groups):
                K.append(frozenset(c for c in range(3)
                                   if dot3(ell, pts[(g, c)]) == 0))
            if any(len(k) == 0 for k in K):
                continue
        boxes.append(tuple(K))
        S |= set(product(*[sorted(k) for k in K]))
    return boxes, S


def line_costs(pts, groups):
    """for every line of the arrangement: (#points on it, cost = #points-2)."""
    keys = [(g, c) for g in groups for c in range(3)]
    reps = {}
    for k in keys:
        reps.setdefault(normalise(pts[k]), []).append(k)
    distinct = list(reps)
    out = {}
    for a, b in combinations(distinct, 2):
        ell = normalise(cross3(a, b))
        n = sum(1 for k in keys if dot3(ell, pts[k]) == 0)
        out[ell] = (n, n - 2)
    return out


# --------------------------------------------------------------- obligations
def K_of_x(blocks, x):
    """the set of R-sites where the L-word x has a collinear transversal."""
    return frozenset(j for j in R if G.rank(G.M_j(blocks, x, j)) <= 2)


def I_of_y(blocks, y):
    """the set of L-sites where the R-word y has a collinear transversal."""
    return frozenset(i for i in L if G.rank(G.N_i(blocks, y, i)) <= 2)


def obligations(blocks):
    return ({x: K_of_x(blocks, x) for x in LFREE},
            {y: I_of_y(blocks, y) for y in RFREE})


# --------------------------------------------------- the permanent conditions
def per_fails_L(blocks, x):
    """the R-words y for which the pure permanent equation H_(x,y)=0 FAILS."""
    return [y for y in WORDS4 if G.per4(G.cross_matrix(blocks, x, y)) != 0]


def per_fails_R(blocks, y):
    return [x for x in WORDS4 if G.per4(G.cross_matrix(blocks, x, y)) != 0]


def all_mixed_failures(blocks):
    """H_w != 0 over all 6,558 mixed words (independent H engine).  Returns
    (n_failures, n_mixed, per_class counts)."""
    nfail = nmix = 0
    kinds = {"Lfree": 0, "Rfree": 0, "other": 0}
    for w in product(range(3), repeat=8):
        if len(set(w)) == 1:
            continue
        nmix += 1
        if G.H_value(blocks, G.C8_MEMBER, w) != 0:
            nfail += 1
            if G.lfree(w[:4]):
                kinds["Lfree"] += 1
            elif G.rfree(w[4:]):
                kinds["Rfree"] += 1
            else:
                kinds["other"] += 1
    return nfail, nmix, kinds


def constants(blocks):
    return [G.H_value(blocks, G.C8_MEMBER, (c,) * 8) for c in range(3)]


def cells_all_nonzero(blocks):
    """every template-occupied cell nonzero and every dead cell zero."""
    for e in G.EDGES:
        m = G.C8_MEMBER[G.EIDX[e]]
        for c in range(3):
            for d in range(3):
                occ = (m >> (3 * c + d)) & 1
                v = blocks[e][c][d]
                if occ and v == 0:
                    return False, ("zero at occupied", e, c, d)
                if not occ and v != 0:
                    return False, ("nonzero at dead", e, c, d)
    return True, None
