#!/usr/bin/env python3
"""A5 AUDIT of probe W13 -- fully independent core library.

Written from notes/clean-pair-cap-exact-descent-target.md ONLY.
No import of W13 code anywhere in this file.

Conventions (chosen to match the descent note; cross-checked against W13's
indexing separately in a5_compare.py):

  sites B = (p, q) + U with p = 0, q = 1, U = (2, ..., 2h+1), |U| = 2h.
  source[(u,v)] for u < v is a 3x3 table T with T[c_u][c_v] the coefficient
  of e_{c_u} (x) e_{c_v} in the block A_{uv} (endpoint-ordered by site index).

  Cap covector K has 9 coordinates K_{ij}; i is the p-slot colour, j the
  q-slot colour.  Polynomials in K are dicts  exponent-9-tuple -> coeff.

  s        = <K, A_pq>                          (eq. 10)
  R_{ab}   = K |_ (A_{p|a}A_{q|b} + A_{p|b}A_{q|a})   (eq. 11)
  x        = sum_{a<b in U} A_ab                (eq. 9)
  E_pq(K)  = sum_{k=2}^{h} s^{h-k} r^k x^{h-k} / (k! (h-k)!)   (eq. 4)
             computed in the square-free algebra, full-U-support part.

Everything exact: Python ints and Fractions.
"""
from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations, product
from math import factorial, gcd
import random

C3 = (0, 1, 2)
NV = 9  # nine cap coordinates


# ----------------------------------------------------------------- polynomials
# poly: dict[tuple(9 ints) -> coeff].  Independent keying from W13 (which uses
# sorted index tuples), deliberately.

ZERO = {}
ONE = {(0,) * NV: 1}


def var_poly(coeffs):
    """Linear form sum_v coeffs[v] K_v  as a poly."""
    out = {}
    for v, c in enumerate(coeffs):
        if c:
            e = [0] * NV
            e[v] = 1
            out[tuple(e)] = out.get(tuple(e), 0) + c
    return {m: c for m, c in out.items() if c}


def pmul(f, g):
    out = {}
    for mf, cf in f.items():
        for mg, cg in g.items():
            key = tuple(a + b for a, b in zip(mf, mg))
            out[key] = out.get(key, 0) + cf * cg
    return {m: c for m, c in out.items() if c}


def padd(f, g):
    out = dict(f)
    for m, c in g.items():
        out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c}


def pscale(f, c):
    if c == 0:
        return {}
    return {m: v * c for m, v in f.items()}


def ppow(f, n):
    out = dict(ONE)
    for _ in range(n):
        out = pmul(out, f)
    return out


@lru_cache(maxsize=None)
def deg_monoms(d):
    """All exponent 9-tuples of total degree d, in a fixed order."""
    out = []

    def rec(pos, rem, acc):
        if pos == NV - 1:
            out.append(tuple(acc + [rem]))
            return
        for e in range(rem, -1, -1):
            rec(pos + 1, rem - e, acc + [e])

    rec(0, d, [])
    return tuple(out)


@lru_cache(maxsize=None)
def monom_index(d):
    return {m: i for i, m in enumerate(deg_monoms(d))}


def poly_vec(f, d):
    idx = monom_index(d)
    vec = [0] * len(idx)
    for m, c in f.items():
        assert sum(m) == d, (m, d)
        vec[idx[m]] += c
    return vec


def vec_poly(vec, d):
    ms = deg_monoms(d)
    return {ms[i]: c for i, c in enumerate(vec) if c}


# ------------------------------------------------------------ square-free algebra
# element: dict[frozenset(sites) -> poly]

def sf_mul(A, B):
    out = {}
    for sa, fa in A.items():
        for sb, fb in B.items():
            if sa & sb:
                continue
            key = sa | sb
            prod = pmul(fa, fb)
            if not prod:
                continue
            out[key] = padd(out.get(key, {}), prod)
    return {k: v for k, v in out.items() if v}


def sf_pow(A, n):
    out = {frozenset(): dict(ONE)}
    for _ in range(n):
        out = sf_mul(out, A)
        if not out:
            return {}
    return out


# ------------------------------------------------------------------- geometry

def sites(h):
    return 0, 1, tuple(range(2, 2 + 2 * h))


def blk(source, u, v, cu, cv):
    """Coefficient of e_cu (x) e_cv in the block on {u,v}, endpoints named."""
    if u < v:
        return source[(u, v)][cu][cv]
    return source[(v, u)][cv][cu]


def random_source(h, rng, lo=-4, hi=4, zero_prob=0.0, entries=None):
    p, q, U = sites(h)
    B = (p, q) + U
    src = {}
    for u, v in combinations(B, 2):
        tab = [[0] * 3 for _ in C3]
        for a in C3:
            for b in C3:
                if rng.random() < zero_prob:
                    tab[a][b] = 0
                elif entries is not None:
                    tab[a][b] = rng.choice(entries)
                else:
                    tab[a][b] = rng.randint(lo, hi)
        src[(u, v)] = tab
    return src


def s_form(source):
    """s as a linear poly in K."""
    p, q, _ = sites(1)
    coeffs = [source[(p, q)][i][j] for i in C3 for j in C3]
    return var_poly(coeffs)


def s_vector(source):
    p, q, _ = sites(1)
    return [source[(p, q)][i][j] for i in C3 for j in C3]


def R_linear(source, a, b, ca, cb):
    """(R_{ab})_{ca,cb} as a linear poly in K."""
    p, q, _ = sites(1)
    coeffs = [0] * NV
    for i in C3:
        for j in C3:
            coeffs[3 * i + j] = (blk(source, p, a, i, ca) * blk(source, q, b, j, cb)
                                 + blk(source, p, b, i, cb) * blk(source, q, a, j, ca))
    return var_poly(coeffs)


# ------------------------------------------ ROUTE 1: raw eq. (4) with factorials

def cap_error_raw(source, h, word):
    """E_w straight from eq. (4): sum_k s^{h-k} r^k x^{h-k} / (k!(h-k)!).

    All algebra done in the square-free algebra restricted to the fixed word
    (legitimate: the w-component of a disjoint-support product is the product
    of the factors' own w-components).  Fractions used for the factorials;
    the result is asserted integral for integral sources.
    """
    p, q, U = sites(h)
    slot = {u: n for n, u in enumerate(U)}
    xw, rw = {}, {}
    for a, b in combinations(U, 2):
        ca, cb = word[slot[a]], word[slot[b]]
        key = frozenset((a, b))
        xv = source[(a, b)][ca][cb]
        if xv:
            xw[key] = {(0,) * NV: Fraction(xv)}
        rf = R_linear(source, a, b, ca, cb)
        if rf:
            rw[key] = {m: Fraction(c) for m, c in rf.items()}
    sp = {m: Fraction(c) for m, c in s_form(source).items()}
    full = frozenset(U)
    total = {}
    rpow = {0: {frozenset(): dict(ONE)}}
    for k in range(1, h + 1):
        rpow[k] = sf_mul(rpow[k - 1], rw) if rw else {}
    xpow = {0: {frozenset(): dict(ONE)}}
    for k in range(1, h + 1):
        xpow[k] = sf_mul(xpow[k - 1], xw) if xw else {}
    for k in range(2, h + 1):
        term = sf_mul(rpow[k], xpow[h - k])
        f = term.get(full)
        if not f:
            continue
        f = pscale(f, Fraction(1, factorial(k) * factorial(h - k)))
        if h - k:
            f = pmul(f, ppow(sp, h - k))
        total = padd(total, f)
    out = {}
    for m, c in total.items():
        assert c.denominator == 1, ("non-integral cap error coefficient", m, c)
        out[m] = int(c)
    return out


# --------------------------------- ROUTE 2: configuration expansion (W13.1 form)

@lru_cache(maxsize=None)
def partial_matchings(verts, size):
    """All sets of `size` disjoint unordered pairs drawn from verts (a tuple)."""
    if size == 0:
        return ((),)
    if len(verts) < 2 * size:
        return ()
    out = []
    a = verts[0]
    # either a is unmatched ...
    for tail in partial_matchings(verts[1:], size):
        out.append(tail)
    # ... or a is matched to some b
    for i in range(1, len(verts)):
        b = verts[i]
        rest = verts[1:i] + verts[i + 1:]
        for tail in partial_matchings(rest, size - 1):
            out.append(((a, b),) + tail)
    return tuple(out)


def perm_form(source, S, T, word, slot):
    """Perm_k([ <K, P_a (x) Q_b> ]_{a in S, b in T}) as a poly in K."""
    p, q, _ = sites(1)
    k = len(S)
    assert len(T) == k
    Pv = {a: [blk(source, p, a, i, word[slot[a]]) for i in C3] for a in S}
    Qv = {b: [blk(source, q, b, j, word[slot[b]]) for j in C3] for b in T}
    acc = {}
    for sigma in permutations(range(k)):
        e = [0] * NV
        coef = 1
        term = dict(ONE)
        for t in range(k):
            a, b = S[t], T[sigma[t]]
            lin = var_poly([Pv[a][i] * Qv[b][j] for i in C3 for j in C3])
            if not lin:
                term = {}
                break
            term = pmul(term, lin)
            if not term:
                break
        if term:
            acc = padd(acc, term)
    return acc


def cap_error_config(source, h, word, jmax=None):
    """E_w via the configuration expansion, independent of cap_error_raw."""
    p, q, U = sites(h)
    slot = {u: n for n, u in enumerate(U)}
    sp = s_form(source)
    total = {}
    if jmax is None:
        jmax = h - 2
    for j in range(0, jmax + 1):          # |J| = j <= h-2
        for J in partial_matchings(U, j):
            weight = 1
            for a, b in J:
                weight *= source[(a, b)][word[slot[a]]][word[slot[b]]]
                if weight == 0:
                    break
            if weight == 0:
                continue
            used = set()
            for a, b in J:
                used.update((a, b))
            free = tuple(u for u in U if u not in used)
            k = h - j
            part = {}
            for S in combinations(free, k):
                T = tuple(u for u in free if u not in S)
                part = padd(part, perm_form(source, S, T, word, slot))
            if not part:
                continue
            part = pscale(part, weight)
            if j:
                part = pmul(part, ppow(sp, j))
            total = padd(total, part)
    return total


# --------------------------------------------------------- mutation variants
# Deliberately WRONG versions used only as controls: each must disagree with
# the correct routes.

def _raw_generic(source, h, word, kmax=None, factmode="correct", oneR=False):
    p, q, U = sites(h)
    slot = {u: n for n, u in enumerate(U)}
    xw, rw = {}, {}
    for a, b in combinations(U, 2):
        ca, cb = word[slot[a]], word[slot[b]]
        key = frozenset((a, b))
        xv = source[(a, b)][ca][cb]
        if xv:
            xw[key] = {(0,) * NV: Fraction(xv)}
        if oneR:
            coeffs = [blk(source, p, a, i, ca) * blk(source, q, b, j, cb)
                      for i in C3 for j in C3]
            rf = var_poly(coeffs)
        else:
            rf = R_linear(source, a, b, ca, cb)
        if rf:
            rw[key] = {m: Fraction(c) for m, c in rf.items()}
    sp = {m: Fraction(c) for m, c in s_form(source).items()}
    full = frozenset(U)
    total = {}
    rpow = {0: {frozenset(): dict(ONE)}}
    for k in range(1, h + 1):
        rpow[k] = sf_mul(rpow[k - 1], rw) if rw else {}
    xpow = {0: {frozenset(): dict(ONE)}}
    for k in range(1, h + 1):
        xpow[k] = sf_mul(xpow[k - 1], xw) if xw else {}
    if kmax is None:
        kmax = h
    for k in range(2, kmax + 1):
        term = sf_mul(rpow[k], xpow[h - k])
        f = term.get(full)
        if not f:
            continue
        if factmode == "correct":
            f = pscale(f, Fraction(1, factorial(k) * factorial(h - k)))
        elif factmode == "konly":
            f = pscale(f, Fraction(1, factorial(k)))
        if h - k:
            f = pmul(f, ppow(sp, h - k))
        total = padd(total, f)
    return total


def cap_error_raw_partial(source, h, word, kmax):
    return _raw_generic(source, h, word, kmax=kmax)


def cap_error_raw_badfact(source, h, word):
    return _raw_generic(source, h, word, factmode="konly")


def cap_error_config_oneR(source, h, word):
    return _raw_generic(source, h, word, oneR=True)


# ------------------------------------------------------ Sigma_k, independent basis

def segre_power_row(u, v, k):
    """(u^T K v)^k as a coefficient vector in the degree-k monomial basis."""
    lin = var_poly([u[i] * v[j] for i in C3 for j in C3])
    return poly_vec(ppow(lin, k), k)


def sigma_rows_powers(k, rng, ntrials=None):
    """Spanning rows of Sigma_k built ONLY from powers (u (x) v)^k."""
    dim = ((k + 1) * (k + 2) // 2) ** 2
    if ntrials is None:
        ntrials = dim + 12
    rows = []
    # deterministic seeds first: all pairs of standard basis vectors and a few
    # small integer vectors, then random ones
    fixed = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1],
             [1, 1, 1], [1, -1, 0], [1, 2, 3], [2, -1, 1], [1, 3, -2], [3, 1, 1]]
    for u in fixed:
        for v in fixed:
            rows.append(segre_power_row(u, v, k))
    while len(rows) < ntrials:
        u = [rng.randint(-5, 5) for _ in C3]
        v = [rng.randint(-5, 5) for _ in C3]
        rows.append(segre_power_row(u, v, k))
    return rows


# --------------------------------------------------------- exact linear algebra
# Integer-preserving echelon form (all inputs integral).

def int_echelon(rows):
    """Return (echelon integer rows, pivot columns).  Exact over Q."""
    mat = [list(r) for r in rows]
    n = len(mat)
    ncols = len(mat[0]) if n else 0
    piv_cols = []
    r = 0
    for c in range(ncols):
        # find a pivot with smallest absolute value (keeps growth down)
        best, bestval = None, None
        for i in range(r, n):
            v = mat[i][c]
            if v:
                av = abs(v)
                if bestval is None or av < bestval:
                    best, bestval = i, av
        if best is None:
            continue
        mat[r], mat[best] = mat[best], mat[r]
        pr = mat[r]
        pv = pr[c]
        for i in range(r + 1, n):
            v = mat[i][c]
            if v:
                g = gcd(pv, v)
                a, b = pv // g, v // g
                row = mat[i]
                mat[i] = [a * row[t] - b * pr[t] for t in range(ncols)]
                cont = 0
                for t in mat[i]:
                    cont = gcd(cont, t)
                    if cont == 1:
                        break
                if cont > 1:
                    mat[i] = [t // cont for t in mat[i]]
        piv_cols.append(c)
        r += 1
        if r == n:
            break
    return mat[:r], piv_cols


def rank_exact(rows):
    if not rows:
        return 0
    return len(int_echelon(rows)[1])


def in_span_exact(ech, piv_cols, target):
    """Exact rational membership of `target` in the row space of `ech`."""
    vec = [Fraction(x) for x in target]
    for r, c in enumerate(piv_cols):
        if vec[c]:
            f = vec[c] / ech[r][c]
            row = ech[r]
            vec = [vec[t] - f * row[t] for t in range(len(vec))]
    return all(x == 0 for x in vec)


def nullspace_exact(rows, ncols):
    """Exact basis (integer vectors) of {x : M x = 0} for M with these rows."""
    if not rows:
        rows = [[0] * ncols]
    mat = [[Fraction(x) for x in r] for r in rows]
    n = len(mat)
    piv_cols = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, n):
            if mat[i][c]:
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        inv = 1 / mat[r][c]
        mat[r] = [x * inv for x in mat[r]]
        pr = mat[r]
        for i in range(n):
            if i != r and mat[i][c]:
                f = mat[i][c]
                mat[i] = [mat[i][t] - f * pr[t] for t in range(ncols)]
        piv_cols.append(c)
        r += 1
        if r == n:
            break
    free_cols = [c for c in range(ncols) if c not in set(piv_cols)]
    basis = []
    for fc in free_cols:
        vec = [Fraction(0)] * ncols
        vec[fc] = Fraction(1)
        for i, pc in enumerate(piv_cols):
            vec[pc] = -mat[i][fc]
        den = 1
        for x in vec:
            den = den * x.denominator // gcd(den, x.denominator)
        ivec = [int(x * den) for x in vec]
        g = 0
        for t in ivec:
            g = gcd(g, t)
        if g > 1:
            ivec = [t // g for t in ivec]
        basis.append(ivec)
    return basis, piv_cols


def perp_basis(rows, ncols):
    """Exact integer basis of the annihilator of the row space (hybrid:
    integer forward elimination, then rational back-substitution)."""
    ech, piv = int_echelon(rows)
    pivset = set(piv)
    free = [c for c in range(ncols) if c not in pivset]
    out = []
    for f in free:
        x = [Fraction(0)] * ncols
        x[f] = Fraction(1)
        for r in range(len(piv) - 1, -1, -1):
            c = piv[r]
            row = ech[r]
            acc = Fraction(0)
            for t in range(c + 1, ncols):
                if row[t] and x[t]:
                    acc += row[t] * x[t]
            x[c] = -acc / row[c]
        den = 1
        for v in x:
            den = den * v.denominator // gcd(den, v.denominator)
        iv = [int(v * den) for v in x]
        g = 0
        for t in iv:
            g = gcd(g, t)
        if g > 1:
            iv = [t // g for t in iv]
        out.append(iv)
    # self-check: every input row annihilates every basis vector
    for r in rows:
        for v in out:
            assert sum(a * b for a, b in zip(r, v)) == 0, "perp_basis self-check failed"
    return out


def product_is_exactly_zero(M, PH):
    """Exact test M @ PH.T == 0 for integer numpy arrays, via CRT:
    each entry V of the product satisfies |V| <= B; if V = 0 mod p for primes
    with prod p > 2B then V = 0.  All modular arithmetic stays < 2**62."""
    import numpy as np
    mm = int(np.abs(M).max()) if M.size else 0
    mp = int(np.abs(PH).max()) if PH.size else 0
    B = mm * mp * M.shape[1]
    primes = [46337, 46327, 46309, 46307, 46301, 46279, 46271, 46261,
              46237, 46229, 46219, 46199]
    used, prod = [], 1
    for p in primes:
        used.append(p)
        prod *= p
        if prod > 2 * B + 1:
            break
    assert prod > 2 * B + 1, ("not enough primes", B, prod)
    bad = 0
    for p in used:
        assert p * p * M.shape[1] < 2 ** 62
        A_ = (M % p).astype(np.int64)
        C_ = (PH % p).astype(np.int64)
        R = A_.dot(C_.T) % p
        bad += int(np.count_nonzero(R))
    return bad == 0, {"bound": B, "primes": used}


def rank_mod_p_np(rows, p):
    """Rank over F_p via numpy int64 elimination (p < 2**31 keeps products safe)."""
    import numpy as np
    assert p < 2 ** 31
    M = np.array([[int(x) % p for x in r] for r in rows], dtype=np.int64)
    n, ncols = M.shape
    r = 0
    for c in range(ncols):
        col = M[r:, c]
        nz = np.nonzero(col)[0]
        if nz.size == 0:
            continue
        i = r + int(nz[0])
        if i != r:
            M[[r, i]] = M[[i, r]]
        inv = pow(int(M[r, c]), p - 2, p)
        M[r] = (M[r] * inv) % p
        colvals = M[r + 1:, c].copy()
        nzr = np.nonzero(colvals)[0]
        if nzr.size:
            M[r + 1:][nzr] = (M[r + 1:][nzr] - colvals[nzr, None] * M[r][None, :]) % p
        r += 1
        if r == n:
            break
    return r


def rank_mod_p(rows, p):
    mat = [[x % p for x in r] for r in rows]
    n = len(mat)
    ncols = len(mat[0]) if n else 0
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, n):
            if mat[i][c]:
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        inv = pow(mat[r][c], p - 2, p)
        mat[r] = [(x * inv) % p for x in mat[r]]
        pr = mat[r]
        for i in range(n):
            if i != r and mat[i][c]:
                f = mat[i][c]
                mat[i] = [(mat[i][t] - f * pr[t]) % p for t in range(ncols)]
        r += 1
        if r == n:
            break
    return r


# ---------------------------------------------------------------- L_h machinery

def L_rows(h, svec, rng, kmin=2):
    """Spanning rows of L_h(A) = sum_{k=kmin..h} s^{h-k} Sigma_k, in degree h."""
    sp = var_poly(svec)
    rows = []
    for k in range(kmin, h + 1):
        spk = ppow(sp, h - k)
        for row in sigma_rows_powers(k, rng):
            f = vec_poly(row, k)
            if h - k:
                f = pmul(f, spk)
            rows.append(poly_vec(f, h))
    return rows


def kappa_monomial_vec(h, a, colours):
    """s^a * prod kappa_c  -- caller supplies s separately; see mono_vec."""
    raise NotImplementedError


def mono_vec(h, svec, a, cols):
    """Vector of the L-monomial s^a * prod_{c in cols} kappa_c  (len(cols)=h-a)."""
    assert a + len(cols) == h
    f = ppow(var_poly(svec), a)
    for c in cols:
        e = [0] * NV
        e[3 * c + c] = 1
        f = pmul(f, {tuple(e): 1})
    return poly_vec(f, h)


def all_words(h):
    return list(product(C3, repeat=2 * h))
