#!/usr/bin/env python3
"""UNAUDITED PROBE W13 (induction residuals R4/R1b) -- core library.

Pinned HEAD: see PINNED_HEAD.txt (0fedca2a868ac1835b39ed754f96551095f92c42).

Uniform-in-h cap-error algebra for the descent interface of
notes/clean-pair-cap-exact-descent-target.md.

Sites: P = 0, Q = 1, U = (2, ..., 2h+1); |U| = 2h; N = 2h + 2.
Blocks A[(u,v)], u < v, are 3x3 integer tables indexed [colour_u][colour_v],
endpoint-ordered exactly as in the committed symbolic checker and in
computations/unaudited-witness-splitting-p1-2026-08-15/wsplit_core.py.

The uniform cap error (eq. (4) of the descent note), cleared of factorials:

    E_w = sum_{M perfect matching of U}
              sum_{J subset M, |J| <= h-2}
                  s^{|J|} prod_{e in J} x_e prod_{f in M\\J} R_f

with s = <K, A_pq> a linear form in the nine cap coordinates K_ij,
x_e = A_e(w_a, w_b) a scalar, and R_f = P_a (x) Q_b + P_b (x) Q_a a linear
form in K, where P_a[i] = A_{p|a}(i, w_a) and Q_b[j] = A_{q|b}(j, w_b).

GRADED FORM (Theorem W13.2, proved in REPORT):
    E_w = sum_{k=2}^{h} s^{h-k} iota_k(z_{w,k}),   z_{w,k} in S^k V (x) S^k W,
where iota_k : S^kV (x) S^kW -> S^k(V (x) W) is the Cauchy inclusion onto the
lambda = (k) isotypic piece, iota_k((u_1...u_k)(x)(v_1...v_k))
          = sum_{sigma in S_k} prod_t <K, u_t (x) v_{sigma(t)}>.

All arithmetic here is exact (Python ints / Fractions).  numpy is used only
with int64 accumulators whose ranges are bounded and asserted.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, permutations, product
import random

COLORS = (0, 1, 2)
NCAP = 9


def kidx(i: int, j: int) -> int:
    """Cap coordinate index: i is the P-colour, j the Q-colour."""
    return 3 * i + j


def require(cond, detail):
    if not cond:
        raise AssertionError(detail)


# --------------------------------------------------------------- matchings

@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple) -> tuple:
    if not vertices:
        return ((),)
    first = vertices[0]
    out = []
    for idx in range(1, len(vertices)):
        second = vertices[idx]
        rest = vertices[1:idx] + vertices[idx + 1:]
        for tail in perfect_matchings(rest):
            out.append(((first, second),) + tail)
    return tuple(out)


@lru_cache(maxsize=None)
def partial_matchings(vertices: tuple, size: int) -> tuple:
    """All sets of `size` pairwise-disjoint unordered pairs from `vertices`."""
    if size == 0:
        return ((),)
    if len(vertices) < 2 * size:
        return ()
    out = []
    for a, b in combinations(vertices, 2):
        rest = tuple(v for v in vertices if v not in (a, b))
        if b < a:
            a, b = b, a
        for tail in partial_matchings(rest, size - 1):
            if tail and (a, b) > tail[0]:
                continue          # keep pairs in increasing order: no repeats
            out.append(((a, b),) + tail)
    return tuple(out)


# --------------------------------------------------------------- monomials

@lru_cache(maxsize=None)
def monomials(nvars: int, degree: int) -> tuple:
    return tuple(combinations_with_replacement(range(nvars), degree))


@lru_cache(maxsize=None)
def monomial_index(nvars: int, degree: int) -> dict:
    return {m: n for n, m in enumerate(monomials(nvars, degree))}


def poly_mul(f: dict, g: dict) -> dict:
    out = {}
    for mf, cf in f.items():
        for mg, cg in g.items():
            key = tuple(sorted(mf + mg))
            out[key] = out.get(key, 0) + cf * cg
    return {m: c for m, c in out.items() if c}


def poly_scale(f: dict, c) -> dict:
    if c == 0:
        return {}
    return {m: v * c for m, v in f.items()}


def poly_add(f: dict, g: dict) -> dict:
    out = dict(f)
    for m, c in g.items():
        out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c}


def poly_pow(f: dict, n: int) -> dict:
    out = {(): 1}
    for _ in range(n):
        out = poly_mul(out, f)
    return out


def poly_vector(f: dict, nvars: int, degree: int):
    idx = monomial_index(nvars, degree)
    vec = [0] * len(idx)
    for m, c in f.items():
        require(len(m) == degree, (m, degree))
        vec[idx[m]] += c
    return vec


# --------------------------------------------------- Cauchy inclusion iota_k

@lru_cache(maxsize=None)
def iota(k: int, mu: tuple, nu: tuple) -> tuple:
    """iota_k(e_mu (x) f_nu) as a sparse polynomial in the nine K-variables.

    Returned as a tuple of (monomial, coefficient) pairs, monomial a sorted
    k-tuple of cap indices.
    """
    require(len(mu) == k and len(nu) == k, (k, mu, nu))
    acc = {}
    for sigma in permutations(range(k)):
        key = tuple(sorted(kidx(mu[t], nu[sigma[t]]) for t in range(k)))
        acc[key] = acc.get(key, 0) + 1
    return tuple(sorted(acc.items()))


def iota_poly(k: int, mu: tuple, nu: tuple) -> dict:
    return dict(iota(k, mu, nu))


@lru_cache(maxsize=None)
def sigma_basis(k: int) -> tuple:
    """Spanning set of Sigma_k = S^kV (x) S^kW inside S^k(V (x) W)."""
    ms = monomials(3, k)
    return tuple((mu, nu) for mu in ms for nu in ms)


def sigma_matrix(k: int):
    """Rows = iota_k(e_mu (x) f_nu) in the S^k(9 vars) monomial basis."""
    idx = monomial_index(NCAP, k)
    rows = []
    for mu, nu in sigma_basis(k):
        row = [0] * len(idx)
        for m, c in iota(k, mu, nu):
            row[idx[m]] += c
        rows.append(row)
    return rows


# ------------------------------------------------------------------ sources

def sites(h: int):
    P, Q = 0, 1
    U = tuple(range(2, 2 + 2 * h))
    return P, Q, U


def edge_key(u, v):
    return (u, v) if u < v else (v, u)


def block(source, u, v, cu, cv):
    if u < v:
        return source[(u, v)][cu][cv]
    return source[(v, u)][cv][cu]


def random_source(h: int, rng, lo=-4, hi=4, zero_prob=0.0):
    P, Q, U = sites(h)
    B = (P, Q) + U
    src = {}
    for u, v in combinations(B, 2):
        tab = []
        for _ in COLORS:
            row = []
            for _ in COLORS:
                row.append(0 if rng.random() < zero_prob else rng.randint(lo, hi))
            tab.append(row)
        src[(u, v)] = tab
    return src


def form_s(source):
    """s(K) as a 9-vector; s = <K, A_pq>."""
    P, Q, _ = sites(1)
    return tuple(source[(P, Q)][i][j] for i in COLORS for j in COLORS)


def s_poly(source) -> dict:
    v = form_s(source)
    return {(k,): v[k] for k in range(NCAP) if v[k]}


# ----------------------------------------------- graded error z_{w,k} (exact)

def graded_error(source, h: int, word: tuple) -> dict:
    """{k: {(mu, nu): int}} with E_w = sum_k s^{h-k} iota_k(z_{w,k}).

    Pure Python ints; no floating point.
    """
    P, Q, U = sites(h)
    slot = {site: n for n, site in enumerate(U)}
    # P- and Q-vectors at each site, for this word
    Pv = {a: [block(source, P, a, i, word[slot[a]]) for i in COLORS] for a in U}
    Qv = {a: [block(source, Q, a, j, word[slot[a]]) for j in COLORS] for a in U}

    # symmetric-algebra products over subsets, by DP on subsets of U
    def subset_products(vec):
        prods = {(): {(): 1}}
        for a in U:
            lin = {(i,): vec[a][i] for i in COLORS if vec[a][i]}
            new = {}
            for S, f in prods.items():
                if a in S:
                    continue
                new[tuple(sorted(S + (a,)))] = poly_mul(f, lin) if lin else {}
            prods.update(new)
        return prods

    prodP = subset_products(Pv)
    prodQ = subset_products(Qv)

    out = {}
    for k in range(2, h + 1):
        acc = {}
        for J in partial_matchings(U, h - k):
            weight = 1
            for a, b in J:
                weight *= source[(a, b)][word[slot[a]]][word[slot[b]]]
                if weight == 0:
                    break
            if weight == 0:
                continue
            used = set()
            for a, b in J:
                used.add(a)
                used.add(b)
            free = tuple(a for a in U if a not in used)
            for S in combinations(free, k):
                T = tuple(a for a in free if a not in S)
                fp = prodP[S]
                if not fp:
                    continue
                fq = prodQ[T]
                if not fq:
                    continue
                for mu, cp in fp.items():
                    for nu, cq in fq.items():
                        key = (mu, nu)
                        acc[key] = acc.get(key, 0) + weight * cp * cq
        out[k] = {key: c for key, c in acc.items() if c}
    return out


def graded_to_poly(source, h: int, z: dict) -> dict:
    """Assemble E_w in the S^h(9 vars) monomial basis from graded data."""
    sp = s_poly(source)
    total = {}
    for k in range(2, h + 1):
        part = {}
        for (mu, nu), c in z[k].items():
            for m, cc in iota(k, mu, nu):
                part[m] = part.get(m, 0) + c * cc
        if h - k:
            part = poly_mul(part, poly_pow(sp, h - k))
        total = poly_add(total, part)
    return total


# ---------------------------------------- direct (independent) error, slow

def error_poly_direct(source, h: int, word: tuple) -> dict:
    """E_w expanded straight from the definition; independent of graded_error."""
    P, Q, U = sites(h)
    slot = {site: n for n, site in enumerate(U)}
    sp = s_poly(source)

    def R_form(a, b):
        ca, cb = word[slot[a]], word[slot[b]]
        f = {}
        for i in COLORS:
            for j in COLORS:
                val = (block(source, P, a, i, ca) * block(source, Q, b, j, cb)
                       + block(source, P, b, i, cb) * block(source, Q, a, j, ca))
                if val:
                    f[(kidx(i, j),)] = val
        return f

    total = {}
    for M in perfect_matchings(U):
        Rs = {e: R_form(*e) for e in M}
        xs = {e: source[e][word[slot[e[0]]]][word[slot[e[1]]]] for e in M}
        for jsize in range(0, h - 1):
            for J in combinations(M, jsize):
                weight = 1
                for e in J:
                    weight *= xs[e]
                if weight == 0:
                    continue
                term = {(): weight}
                for e in M:
                    if e in J:
                        continue
                    term = poly_mul(term, Rs[e])
                    if not term:
                        break
                if not term:
                    continue
                if jsize:
                    term = poly_mul(term, poly_pow(sp, jsize))
                total = poly_add(total, term)
    return total


# --------------------------------------------------------- linear algebra

def rank_mod_p(rows, p: int) -> int:
    """Exact rank over F_p by Gaussian elimination (Python ints)."""
    mat = [[x % p for x in r] for r in rows]
    ncols = len(mat[0]) if mat else 0
    rank = 0
    row = 0
    for col in range(ncols):
        piv = None
        for r in range(row, len(mat)):
            if mat[r][col]:
                piv = r
                break
        if piv is None:
            continue
        mat[row], mat[piv] = mat[piv], mat[row]
        inv = pow(mat[row][col], p - 2, p)
        mat[row] = [(x * inv) % p for x in mat[row]]
        pr = mat[row]
        for r in range(len(mat)):
            if r != row and mat[r][col]:
                f = mat[r][col]
                mat[r] = [(a - f * b) % p for a, b in zip(mat[r], pr)]
        row += 1
        rank += 1
        if row == len(mat):
            break
    return rank


def rref_exact(rows):
    """Reduced row echelon form over Q (Fractions).  Returns (rows, pivots)."""
    mat = [[Fraction(x) for x in r] for r in rows]
    ncols = len(mat[0]) if mat else 0
    pivots = []
    row = 0
    for col in range(ncols):
        piv = None
        for r in range(row, len(mat)):
            if mat[r][col]:
                piv = r
                break
        if piv is None:
            continue
        mat[row], mat[piv] = mat[piv], mat[row]
        inv = 1 / mat[row][col]
        mat[row] = [x * inv for x in mat[row]]
        pr = mat[row]
        for r in range(len(mat)):
            if r != row and mat[r][col]:
                f = mat[r][col]
                mat[r] = [a - f * b for a, b in zip(mat[r], pr)]
        pivots.append(col)
        row += 1
        if row == len(mat):
            break
    return mat[:row], pivots


def in_span_exact(basis_rref, pivots, target) -> bool:
    """Exact membership of `target` in the row space given its RREF."""
    vec = [Fraction(x) for x in target]
    for r, col in enumerate(pivots):
        if vec[col]:
            f = vec[col]
            vec = [a - f * b for a, b in zip(vec, basis_rref[r])]
    return all(x == 0 for x in vec)


# ------------------------------------------------------ apolarity with det

@lru_cache(maxsize=None)
def det_apolar(monomial: tuple):
    """Apply the differential operator prod_t d/dK_{monomial[t]} to det(Y).

    Returns the resulting polynomial in Y (dict keyed by sorted index tuples).
    For deg 3 this is a scalar (key ()); for deg > 3 it is 0.
    """
    # det(Y) = sum_{pi in S_3} sgn(pi) Y_{0,pi0} Y_{1,pi1} Y_{2,pi2}
    terms = {}
    for pi in permutations(range(3)):
        sgn = 1
        # parity of pi
        inv = sum(1 for a in range(3) for b in range(a + 1, 3) if pi[a] > pi[b])
        sgn = -1 if inv % 2 else 1
        key = tuple(sorted(kidx(i, pi[i]) for i in range(3)))
        terms[key] = terms.get(key, 0) + sgn
    out = {}
    for key, coef in terms.items():
        rest = list(key)
        ok = True
        for v in monomial:
            if v in rest:
                rest.remove(v)
            else:
                ok = False
                break
        if ok:
            out[tuple(rest)] = out.get(tuple(rest), 0) + coef
    return {m: c for m, c in out.items() if c}


def apolar_det(poly: dict) -> dict:
    """poly(d/dK) applied to det(Y)."""
    out = {}
    for m, c in poly.items():
        for key, cc in det_apolar(m).items():
            out[key] = out.get(key, 0) + c * cc
    return {m: c for m, c in out.items() if c}
