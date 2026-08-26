#!/usr/bin/env python3
"""A11 shared m=25 / R6 machinery + an INDEPENDENT (third-family) builder.

UNAUDITED.  From scratch; imports only a11_lib.

The builder rests on the cofactor identity itself: for a fixed site u,
Phi(w) = <S'(tau)_t, Q(w)> is LINEAR in the 9|N(u)| cells at u and Q(w)
uses no edge incident to u.  So the whole clean-word system
{Phi(w) = 0 : w clean} splits by the letter at u into three independent
linear systems, one per row of the u-blocks, and one exact solve at a single
site produces a point that is clean at EVERY clean word.  Different family
from W30's factory and from A10's multi-pass site walk.
"""
from __future__ import annotations

import os
import sys
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a11_lib as A  # noqa: E402


def kernel_basis(rows, K, n):
    """basis of the right kernel of the matrix with the given rows"""
    mat = [list(r) for r in rows]
    piv = {}
    r = 0
    for c in range(n):
        sel = None
        for i in range(r, len(mat)):
            if not K.iszero(mat[i][c]):
                sel = i
                break
        if sel is None:
            continue
        mat[r], mat[sel] = mat[sel], mat[r]
        iv = K.inv(mat[r][c])
        mat[r] = [K.mul(x, iv) for x in mat[r]]
        for i in range(len(mat)):
            if i != r and not K.iszero(mat[i][c]):
                f = mat[i][c]
                mat[i] = [K.sub(x, K.mul(f, y)) for x, y in zip(mat[i], mat[r])]
        piv[c] = r
        r += 1
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        v = [K.zero] * n
        v[fc] = K.one
        for c, rr in piv.items():
            v[c] = K.sub(K.zero, mat[rr][fc])
        basis.append(v)
    return basis


def clean_solve(m, K, rng, u):
    """Exact builder.  At site u the unknowns are the cells A_{u,s}[t][b]
    for s in N(u), letters t (row) and b (neighbour letter).  A clean word w
    with w_u = t contributes  sum_s A_{u,s}[t][w_s] * Q(w)_s = 0, which is
    linear in the 3|N(u)| unknowns of row t.  Solve each row's kernel."""
    tm = A.T(m)
    ns = tm.nbr[u]
    nvar = 3 * len(ns)                     # (s index, letter b) -> column
    bl = {}
    for e in sorted(tm.gamma):
        bl[e] = [[K.of(rng.randrange(1, K.p if K.p else 10 ** 6))
                  for _ in range(3)] for _ in range(3)]
    for t in range(3):
        rows = []
        for w in tm.clean_words:
            if w[u] != t:
                continue
            Q = A.cofactorQ(tm, bl, u, w, K)
            r = [K.zero] * nvar
            for j, s in enumerate(ns):
                r[3 * j + w[s]] = K.add(r[3 * j + w[s]], Q[j])
            rows.append(r)
        bas = kernel_basis(rows, K, nvar)
        if not bas:
            return None
        vec = None
        for _try in range(40):
            cand = [K.zero] * nvar
            for b in bas:
                lam = K.of(rng.randrange(1, K.p if K.p else 10 ** 6))
                cand = [K.add(x, K.mul(lam, y)) for x, y in zip(cand, b)]
            if all(not K.iszero(z) for z in cand):
                vec = cand
                break
        if vec is None:
            return None
        for j, s in enumerate(ns):
            for b in range(3):
                if u < s:
                    bl[(u, s)][t][b] = vec[3 * j + b]
                else:
                    bl[(s, u)][b][t] = vec[3 * j + b]
    return bl


def seed_stratum(m, K, rng):
    """A rank-one seed: A_{u,v}[a][b] = c_uv * alpha_u(a) * alpha_v(b) makes
    Phi(w) = (prod_u alpha_u(w_u)) * haf(c), so tuning ONE c_e to kill the
    scalar Gamma hafnian gives a point with Phi == 0 at EVERY word -- clean,
    all cells nonzero, and on the vanishing stratum.  Phi is linear in c_e,
    so the tuning is one division."""
    tm = A.T(m)
    al = {u: [K.of(rng.randrange(1, K.p if K.p else 10 ** 6))
              for _ in range(3)] for u in range(8)}
    ce = {e: K.of(rng.randrange(1, K.p if K.p else 10 ** 6))
          for e in sorted(tm.gamma)}
    e0 = sorted(tm.gamma)[rng.randrange(len(tm.gamma))]
    # haf(c) = c_e0 * dA + dB  ->  choose c_e0 = -dB/dA
    dA = K.zero
    dB = K.zero
    for M in tm.gamma_pms:
        pr = K.one
        has = e0 in M
        for e in M:
            if e == e0:
                continue
            pr = K.mul(pr, ce[e])
        if has:
            dA = K.add(dA, pr)
        else:
            dB = K.add(dB, pr)
    if K.iszero(dA):
        return None
    ce[e0] = K.mul(K.sub(K.zero, dB), K.inv(dA))
    if K.iszero(ce[e0]):
        return None
    bl = {}
    for (u, v) in sorted(tm.gamma):
        bl[(u, v)] = [[K.mul(ce[(u, v)], K.mul(al[u][a], al[v][b]))
                       for b in range(3)] for a in range(3)]
    return bl


def site_resolve(m, bl, u, K, rng):
    """Re-solve the cells at site u from a random element of the kernel of
    the clean-word system.  The current point is already in that kernel, so
    it is never empty; a random element walks the clean variety."""
    tm = A.T(m)
    ns = tm.nbr[u]
    nvar = 3 * len(ns)
    for t in range(3):
        rows = []
        for w in tm.clean_words:
            if w[u] != t:
                continue
            Q = A.cofactorQ(tm, bl, u, w, K)
            r = [K.zero] * nvar
            for j, s in enumerate(ns):
                r[3 * j + w[s]] = K.add(r[3 * j + w[s]], Q[j])
            rows.append(r)
        bas = kernel_basis(rows, K, nvar)
        if not bas:
            return False
        vec = None
        for _try in range(40):
            cand = [K.zero] * nvar
            for b in bas:
                lam = K.of(rng.randrange(1, K.p if K.p else 10 ** 6))
                cand = [K.add(x, K.mul(lam, y)) for x, y in zip(cand, b)]
            if all(not K.iszero(z) for z in cand):
                vec = cand
                break
        if vec is None:
            return False
        for j, s in enumerate(ns):
            for b in range(3):
                if u < s:
                    bl[(u, s)][t][b] = vec[3 * j + b]
                else:
                    bl[(s, u)][b][t] = vec[3 * j + b]
    return True


def build_a11(m, K, rng, passes=3):
    """A11's third-family builder: rank-one stratum seed, then a random site
    walk on the clean variety."""
    bl = seed_stratum(m, K, rng)
    if bl is None:
        return None
    order = list(range(8))
    for _ in range(passes):
        rng.shuffle(order)
        for u in order:
            if not site_resolve(m, bl, u, K, rng):
                return None
    return bl


# --------------------------------------------------------- m=25 specifics
def untriggered_template(m=25, v=6):
    """the 7-coordinate assignments all three of whose completions are
    non-constant CLEAN words -- untriggered at ANY clean point (spine 4.2)."""
    tm = A.T(m)
    other = [u for u in range(8) if u != v]
    out = []
    for vals in product(range(3), repeat=7):
        w = [0] * 8
        for u, a in zip(other, vals):
            w[u] = a
        good = True
        for t in range(3):
            ww = tuple(w[:v] + [t] + w[v + 1:])
            if len(set(ww)) == 1 or tm.fired(ww):
                good = False
                break
        if good:
            out.append(tuple(w))
    return out


def BC_closed(tm, bl, w, K):
    """the two-term Q at m=25 / v=6 in CLOSED FORM, hand-derived from
    spine (1):  B = haf(Gamma-{6,7}) = hafL*r45 + l03*d1*d2 ,
                C = haf(Gamma-{6,5}) = hafL*r47 + l23*d0*d1 ."""
    def c(u, v, a, b):
        return A.cell(bl, tm, u, v, a, b, K)
    x, y = w[:4], w[4:]
    hl = A.hafL(tm, bl, w, K)
    r45 = c(4, 5, y[0], y[1])
    r47 = c(4, 7, y[0], y[3])
    l03 = c(0, 3, x[0], x[3])
    l23 = c(2, 3, x[2], x[3])
    d0 = c(0, 7, x[0], y[3])
    d1 = c(1, 4, x[1], y[0])
    d2 = c(2, 5, x[2], y[1])
    B = K.add(K.mul(hl, r45), K.mul(l03, K.mul(d1, d2)))
    C = K.add(K.mul(hl, r47), K.mul(l23, K.mul(d0, d1)))
    return B, C
