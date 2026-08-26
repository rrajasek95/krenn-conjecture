#!/usr/bin/env python3
"""A7 SUB-AUDIT of W20 -- independent core for LEMMA W20-P.

Written from the statement, NOT from w20_perlemma.py.  Exact arithmetic only
(Python int / Fraction / GF(p) ints).  No floats anywhere.

Conventions used throughout this audit
--------------------------------------
per(v^1,...,v^n) = sum over bijections s:[n]->[n] of prod_j v^j_{s(j)}
                 = permanent of the n x n matrix whose COLUMNS are the v^j.
(The permanent is invariant under transposition and under permuting the
columns, so "rows" vs "columns" is immaterial; the symmetry in the columns
IS used below to reduce sweeps to multisets of normals.)

A hyperplane through the origin is V = ker(nv) = {v : sum_i nv_i v_i = 0}
for a nonzero normal nv.

"per vanishes on the product V_1 x ... x V_n" means
        per(v^1,...,v^n) = 0 for EVERY (v^1,...,v^n) in V_1 x ... x V_n.
Because per is multilinear in the columns this is equivalent to vanishing on
all tuples of basis vectors, which is what the exact test below checks.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

# ---------------------------------------------------------------- permanent
_MASKS_BY_POP: dict[int, list[list[int]]] = {}


def _masks_by_pop(n):
    if n not in _MASKS_BY_POP:
        tab = [[] for _ in range(n + 1)]
        for m in range(1 << n):
            tab[bin(m).count("1")].append(m)
        _MASKS_BY_POP[n] = tab
    return _MASKS_BY_POP[n]


def per(cols):
    """permanent of the matrix with these columns; subset DP, exact ring ops.

    Valid over any commutative ring (only + and * are used)."""
    n = len(cols)
    tab = _masks_by_pop(n)
    dp = {0: 1}
    for j in range(n):
        nxt = {}
        cj = cols[j]
        for mask, val in dp.items():
            for i in range(n):
                bit = 1 << i
                if mask & bit:
                    continue
                a = cj[i]
                if a:
                    k = mask | bit
                    nxt[k] = nxt.get(k, 0) + val * a
        dp = nxt
        if not dp:
            return 0
    return dp.get((1 << n) - 1, 0)


def per_bruteforce(cols):
    """independent permanent, by literal expansion over bijections."""
    n = len(cols)
    tot = 0
    for p in permutations(range(n)):
        t = 1
        for j in range(n):
            t *= cols[j][p[j]]
        tot += t
    return tot


# ------------------------------------------------------------ kernel bases
def kernel_basis(nv):
    """integer basis of ker(nv).  Pivot = LAST nonzero coordinate.

    b_i = nv[piv]*e_i - nv[i]*e_piv  for i != piv (n-1 vectors, independent).
    Scaling a basis vector by a nonzero constant does not change the span."""
    n = len(nv)
    piv = max(i for i in range(n) if nv[i])
    out = []
    for i in range(n):
        if i == piv:
            continue
        b = [0] * n
        b[i] = nv[piv]
        b[piv] = -nv[i]
        out.append(b)
    return out


def kernel_basis_modp(nv, p):
    n = len(nv)
    piv = max(i for i in range(n) if nv[i] % p)
    out = []
    for i in range(n):
        if i == piv:
            continue
        b = [0] * n
        b[i] = nv[piv] % p
        b[piv] = (-nv[i]) % p
        out.append(b)
    return out


# --------------------------------------------------- identical vanishing ---
_PROBE_C = ((1, 2, 3, 4, 5, 6, 7), (1, 3, 9, 27, 81, 243, 729))


def _combo(basis, coefs):
    n = len(basis[0])
    return [sum(coefs[k] * basis[k][i] for k in range(len(basis)))
            for i in range(n)]


def per_vanishes_on_product(bases):
    """EXACT: does per vanish identically on span(bases[0]) x ... ?

    Sound-and-complete by multilinearity: per == 0 on the product iff it is 0
    on every tuple of basis vectors.  A cheap non-vanishing certificate (one
    generic point) is tried first purely for speed; a nonzero value there
    already proves non-vanishing."""
    n = len(bases)
    for cs in _PROBE_C:
        pt = [_combo(bases[j], cs) for j in range(n)]
        if per(pt):
            return False
    dims = [len(b) for b in bases]
    for idx in product(*[range(d) for d in dims]):
        if per([bases[j][idx[j]] for j in range(n)]):
            return False
    return True


def per_vanishes_normals(normals):
    return per_vanishes_on_product([kernel_basis(nv) for nv in normals])


def per_vanishes_normals_modp(normals, p):
    bases = [kernel_basis_modp(nv, p) for nv in normals]
    n = len(bases)
    dims = [len(b) for b in bases]
    for idx in product(*[range(d) for d in dims]):
        if per([bases[j][idx[j]] for j in range(n)]) % p:
            return False
    return True


def is_common_coordinate(normals):
    """all V_j are the SAME coordinate hyperplane {v_r = 0}, i.e. every normal
    is a nonzero multiple of the same e_r."""
    n = len(normals[0])
    for r in range(n):
        if all(nv[r] and all(nv[i] == 0 for i in range(n) if i != r)
               for nv in normals):
            return True
    return False


def support(nv):
    return frozenset(i for i, x in enumerate(nv) if x)


# ------------------------------------------------------------- candidates --
def sign_reps(n, vals=(-1, 0, 1)):
    """one representative of each {v,-v} pair among nonzero vals^n.

    Since ker(nv) = ker(c*nv), sweeping these reps covers every hyperplane
    with a normal in vals^n."""
    seen, out = set(), []
    for v in product(vals, repeat=n):
        if not any(v):
            continue
        if v in seen:
            continue
        seen.add(v)
        seen.add(tuple(-x for x in v))
        out.append(v)
    return out
