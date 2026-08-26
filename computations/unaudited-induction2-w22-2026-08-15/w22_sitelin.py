#!/usr/bin/env python3
"""W22 -- SITE LINEARITY at general N (the N-uniform form of W20-L), and the
constructions it buys.

THEOREM W22-L (site linearity, general N, general blocks).  Fix a site z.
Every perfect matching of B covers z by exactly one edge, so for every word w

    H_B(A)_w  =  sum_{y != z}  A_zy(w_z, w_y) * C^z_y(w),
    C^z_y(w)  =  Haf_{B\\{z,y}}(A)_{w|_{B\\{z,y}}}       (independent of w_z).

Hence, with the 3(N-1) unknowns  v_c = ( A_zy(c,d) )_{y != z, d},
the exactness system is THREE INDEPENDENT INHOMOGENEOUS LINEAR SYSTEMS
(one per colour c at z):

    sum_{y != z} A_zy(c, w_y) C^z_y(w) = delta(w = c^B)     for every w with
                                                             w_z = c.

The coefficients C^z_y(w) involve only blocks AWAY from z.

CONSEQUENCES USED HERE
 (L-a) exact deformation: solving the homogeneous system (mixed words only)
       gives a LINEAR family of mixed-exact sources through any given one --
       the generator of rich test beds with full-rank blocks;
 (L-b) achievable pure profile: the reachable (H_{0^B}, H_{1^B}, H_{2^B}) from
       a site-z modification is an explicit affine image, decidable exactly;
 (L-c) the STAR IDENTITY (Lemma W22-S): taking the words that are constant = c
       off z gives, for an exact source,
            sum_{y != z} C^{(c)}_{zy} A_zy(., c) = e_c  in V_z,
       with C^{(c)}_{zy} = Haf(A^{(c)} | B\\{z,y}), A^{(c)}_uv = A_uv(c,c).
       Pairing with u in V_p (z = p) gives the CONTRACTION IDENTITY
            sum_{y != p} C^{(c)}_{py} (A_py^T u)_c = u_c,               (*)
       which is exactly the star data of the witness criterion at every pair
       through p.  This is the derivation asked for in J.1b-support.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-induction2-w22-2026-08-15")
sys.path.insert(0, BASE)
import w22_core as W                                        # noqa: E402


def cofactor_tensor(src, z, y, word, n, ncol=3):
    """C^z_y(w) = Haf_{B - z - y}(A) at w restricted."""
    rest = tuple(x for x in range(n) if x not in (z, y))
    tab = {(a, b): W.oriented(src, a, b, ncol) for a, b in combinations(rest, 2)}
    wo = {a: word[a] for a in rest}
    return W._haf_tensor(tab, rest, wo, ncol)


def site_systems(src, z, n, ncol=3, include_pures=True):
    """The three linear systems at site z.  Returns for each colour c a pair
    (rows, rhs) where a row is a list over the columns (y, d) [y != z,
    d in colours] in the fixed order below."""
    cols = [(y, d) for y in range(n) if y != z for d in range(ncol)]
    idx = {c: i for i, c in enumerate(cols)}
    out = {}
    for c in range(ncol):
        rows, rhs, tags = [], [], []
        for word in product(range(ncol), repeat=n):
            if word[z] != c:
                continue
            const = len(set(word)) == 1
            if const and not include_pures:
                continue
            row = [Fraction(0)] * len(cols)
            for y in range(n):
                if y == z:
                    continue
                row[idx[(y, word[y])]] += Fraction(
                    cofactor_tensor(src, z, y, word, n, ncol))
            rows.append(row)
            rhs.append(Fraction(1) if const else Fraction(0))
            tags.append(word)
        out[c] = (rows, rhs, tags, cols)
    return out


def solve_linear(rows, rhs):
    """Exact solve: returns (particular, kernel basis) or (None, kernel)."""
    m = [list(r) + [b] for r, b in zip(rows, rhs)]
    ncol = len(rows[0]) if rows else 0
    piv = []
    r = 0
    for c in range(ncol):
        p = None
        for i in range(r, len(m)):
            if m[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        head = m[r]
        inv = Fraction(1) / head[c]
        m[r] = [x * inv for x in head]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv.append(c)
        r += 1
    for i in range(r, len(m)):
        if m[i][ncol] != 0 and all(x == 0 for x in m[i][:ncol]):
            return None, None
    part = [Fraction(0)] * ncol
    for i, c in enumerate(piv):
        part[c] = m[i][ncol]
    free = [c for c in range(ncol) if c not in piv]
    kern = []
    for f in free:
        v = [Fraction(0)] * ncol
        v[f] = Fraction(1)
        for i, c in enumerate(piv):
            v[c] = -m[i][f]
        kern.append(v)
    return part, kern


def apply_site_solution(src, z, sol, cols, n, ncol=3):
    """Write a solution vector back into the site-z star blocks."""
    out = {e: [row[:] for row in m] for e, m in src.items()}
    for c in range(ncol):
        for k, (y, d) in enumerate(cols):
            val = sol[c][k]
            if z < y:
                out[(z, y)][c][d] = val
            else:
                out[(y, z)][d][c] = val
    return out


# ------------------------------------------------ the star identity (Lemma S)

def colour_slice(src, c, n, ncol=3):
    return {W.ekey(a, b): W.oriented(src, a, b, ncol)[c][c]
            for a, b in combinations(range(n), 2)}


def haf_scalar(w, sites):
    total = 0
    for M in W.perfect_matchings(tuple(sites)):
        term = 1
        for a, b in M:
            term *= w[W.ekey(a, b)]
            if term == 0:
                break
        total += term
    return total


def star_identity_residual(src, z, c, n, ncol=3):
    """LHS - RHS of  sum_{y != z} C^{(c)}_{zy} A_zy(., c) = e_c  in V_z."""
    wc = colour_slice(src, c, n, ncol)
    vec = [0] * ncol
    for y in range(n):
        if y == z:
            continue
        rest = tuple(x for x in range(n) if x not in (z, y))
        cof = haf_scalar(wc, rest)
        blk = W.oriented(src, z, y, ncol)
        for d in range(ncol):
            vec[d] += cof * blk[d][c]
    return [vec[d] - (1 if d == c else 0) for d in range(ncol)]


def contraction_identity_residual(src, p, u, c, n, ncol=3):
    """LHS - RHS of  sum_{y != p} C^{(c)}_{py} (A_py^T u)_c = u_c."""
    wc = colour_slice(src, c, n, ncol)
    tot = 0
    for y in range(n):
        if y == p:
            continue
        rest = tuple(x for x in range(n) if x not in (p, y))
        cof = haf_scalar(wc, rest)
        blk = W.oriented(src, p, y, ncol)
        alpha_c = sum(u[i] * blk[i][c] for i in range(ncol))
        tot += cof * alpha_c
    return tot - u[c]
