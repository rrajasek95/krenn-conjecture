#!/usr/bin/env python3
"""UNAUDITED PROBE W14 (monochrome transfer + certificate layers) -- core.

Pinned HEAD: see PINNED_HEAD.txt (c080b8a3ebf00525cbfcee209e473518758ff3d9).

Independent re-implementation of the uniform cap-error algebra of
notes/clean-pair-cap-exact-descent-target.md, written from the note's
definitions (NOT copied from W13/P1/P2), so that it can be cross-checked
against computations/unaudited-induction-w13-2026-08-15/w13_core.py.

Sites: P = 0, Q = 1, U = (2, ..., 2h+1); |U| = 2h; N = 2h + 2.
Blocks source[(u,v)] for u < v are 3x3 integer tables, row index = colour at u.

    E_w(K) = sum_{M perfect matching of U}
                 sum_{J subset M, |J| <= h-2}
                     s^{|J|} prod_{e in J} x_e prod_{f in M\\J} R_f(K)

with s = <K, A_pq>, x_{ab} = A_ab(w_a, w_b), and
R_{ab}(K) = <K, P_a (x) Q_b + P_b (x) Q_a>, P_a[i] = A_pa(i, w_a),
Q_a[j] = A_qa(j, w_a).

W14 additions (all exact):
  * rank-one evaluation  K = u (x) v   ->  the (u,v)-SLICE of the pair;
  * hafnian/elementary-symmetric closed form for the slice quantities;
  * the level functions G_j^{(u,v)}(w) that carry the transfer lemma.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, permutations
import random

COLORS = (0, 1, 2)
NCAP = 9


def kidx(i: int, j: int) -> int:
    return 3 * i + j


def require(cond, detail):
    if not cond:
        raise AssertionError(f"W14 CHECK FAILED: {detail}")


# --------------------------------------------------------------- matchings

@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple) -> tuple:
    if not vertices:
        return ((),)
    first, out = vertices[0], []
    for idx in range(1, len(vertices)):
        rest = vertices[1:idx] + vertices[idx + 1:]
        for tail in perfect_matchings(rest):
            out.append(((first, vertices[idx]),) + tail)
    return tuple(out)


@lru_cache(maxsize=None)
def partial_matchings(vertices: tuple, size: int) -> tuple:
    """All sets of `size` pairwise-disjoint unordered pairs from `vertices`."""
    if size == 0:
        return ((),)
    if len(vertices) < 2 * size:
        return ()
    out = []
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            a, b = vertices[i], vertices[j]
            rest = tuple(v for v in vertices if v not in (a, b))
            for tail in partial_matchings(rest, size - 1):
                if tail and (a, b) > tail[0]:
                    continue
                out.append(((a, b),) + tail)
    return tuple(out)


# --------------------------------------------------------------- polynomials

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


def poly_add(f: dict, g: dict) -> dict:
    out = dict(f)
    for m, c in g.items():
        out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c}


def poly_scale(f: dict, c) -> dict:
    return {} if c == 0 else {m: v * c for m, v in f.items()}


def poly_pow(f: dict, n: int) -> dict:
    out = {(): 1}
    for _ in range(n):
        out = poly_mul(out, f)
    return out


def poly_row(f: dict, degree: int, nvars: int = NCAP):
    idx = monomial_index(nvars, degree)
    vec = [0] * len(idx)
    for m, c in f.items():
        require(len(m) == degree, ("inhomogeneous", m, degree))
        vec[idx[m]] += c
    return vec


def poly_eval(f: dict, point) -> Fraction:
    """Evaluate a K-polynomial at a 9-vector."""
    total = Fraction(0)
    for m, c in f.items():
        term = Fraction(c)
        for v in m:
            term *= point[v]
        total += term
    return total


# ------------------------------------------------------------------ sources

def sites(h: int):
    U = tuple(range(2, 2 + 2 * h))
    return 0, 1, U


def block(source, u, v, cu, cv):
    return source[(u, v)][cu][cv] if u < v else source[(v, u)][cv][cu]


def random_source(h: int, rng, lo=-4, hi=4):
    P, Q, U = sites(h)
    src = {}
    for u, v in combinations((P, Q) + U, 2):
        src[(u, v)] = [[rng.randint(lo, hi) for _ in COLORS] for _ in COLORS]
    return src


def s_vector(source):
    return [source[(0, 1)][i][j] for i in COLORS for j in COLORS]


def s_poly(source) -> dict:
    v = s_vector(source)
    return {(k,): v[k] for k in range(NCAP) if v[k]}


def pq_vectors(source, h, word):
    """P_a, Q_a in colour space for the given word (dicts site -> 3-vector)."""
    P, Q, U = sites(h)
    slot = {a: n for n, a in enumerate(U)}
    Pv = {a: [block(source, P, a, i, word[slot[a]]) for i in COLORS] for a in U}
    Qv = {a: [block(source, Q, a, j, word[slot[a]]) for j in COLORS] for a in U}
    return Pv, Qv


def x_edge(source, h, word, a, b):
    P, Q, U = sites(h)
    slot = {u: n for n, u in enumerate(U)}
    return block(source, a, b, word[slot[a]], word[slot[b]])


# ------------------------------------------------- E_w (direct, independent)

def R_form(source, h, word, a, b) -> dict:
    Pv, Qv = pq_vectors(source, h, word)
    f = {}
    for i in COLORS:
        for j in COLORS:
            val = Pv[a][i] * Qv[b][j] + Pv[b][i] * Qv[a][j]
            if val:
                f[(kidx(i, j),)] = f.get((kidx(i, j),), 0) + val
    return f


def error_poly(source, h: int, word: tuple) -> dict:
    """E_w straight from the definition (W14's own expansion)."""
    P, Q, U = sites(h)
    sp = s_poly(source)
    total = {}
    for M in perfect_matchings(U):
        Rs = {e: R_form(source, h, word, *e) for e in M}
        xs = {e: x_edge(source, h, word, *e) for e in M}
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


# -------------------------------------------------- rank-one (u,v) machinery

def slice_R(source, h, word, u, v, a, b):
    """R_{ab} evaluated at the rank-one cap K = u (x) v."""
    Pv, Qv = pq_vectors(source, h, word)
    ua = sum(u[i] * Pv[a][i] for i in COLORS)
    ub = sum(u[i] * Pv[b][i] for i in COLORS)
    va = sum(v[j] * Qv[a][j] for j in COLORS)
    vb = sum(v[j] * Qv[b][j] for j in COLORS)
    return ua * vb + ub * va


def hafnian_slice(source, h, word, u, v, subset) -> Fraction:
    """sum over perfect matchings of `subset` of prod R^{(u,v)} (exact)."""
    total = 0
    for M in perfect_matchings(tuple(subset)):
        term = 1
        for a, b in M:
            term *= slice_R(source, h, word, u, v, a, b)
            if term == 0:
                break
        total += term
    return total


def hafnian_slice_closed(source, h, word, u, v, subset):
    """k! * sum_{|S|=k} prod_S (u.P) prod_{S^c} (v.Q)  -- the closed form."""
    Pv, Qv = pq_vectors(source, h, word)
    subset = tuple(subset)
    k = len(subset) // 2
    up = {a: sum(u[i] * Pv[a][i] for i in COLORS) for a in subset}
    vq = {a: sum(v[j] * Qv[a][j] for j in COLORS) for a in subset}
    total = 0
    for S in combinations(subset, k):
        term = 1
        for a in S:
            term *= up[a]
        for b in subset:
            if b not in S:
                term *= vq[b]
        total += term
    fact = 1
    for t in range(2, k + 1):
        fact *= t
    return fact * total


def G_level(source, h, word, u, v, j):
    """G_j^{(u,v)}(w) = sum_{|J|=j} x_J * Haf^{(u,v)}(U \\ V(J))."""
    P, Q, U = sites(h)
    total = 0
    for J in partial_matchings(U, j):
        weight = 1
        for a, b in J:
            weight *= x_edge(source, h, word, a, b)
            if weight == 0:
                break
        if weight == 0:
            continue
        used = {a for e in J for a in e}
        free = tuple(a for a in U if a not in used)
        total += weight * hafnian_slice(source, h, word, u, v, free)
    return total


def slice_error(source, h, word, u, v):
    """E_w evaluated at the rank-one cap K = u (x) v (the (u,v)-slice error)."""
    alpha = sum(u[i] * v[j] * source[(0, 1)][i][j] for i in COLORS
                for j in COLORS)
    total = 0
    for j in range(0, h - 1):
        total += alpha ** j * G_level(source, h, word, u, v, j)
    return total


def delta(c):
    return [1 if i == c else 0 for i in COLORS]


# ------------------------------------------------------- graded data z_{w,k}

def graded_error(source, h: int, word: tuple) -> dict:
    """{k: {(mu,nu): coeff}} with E_w = sum_k s^{h-k} iota_k(z_{w,k})."""
    P, Q, U = sites(h)
    Pv, Qv = pq_vectors(source, h, word)

    def sym_products(vec, subset):
        poly = {(): 1}
        for a in subset:
            lin = {(i,): vec[a][i] for i in COLORS if vec[a][i]}
            poly = poly_mul(poly, lin)
            if not poly:
                return {}
        return poly

    out = {}
    for k in range(2, h + 1):
        acc = {}
        for J in partial_matchings(U, h - k):
            weight = 1
            for a, b in J:
                weight *= x_edge(source, h, word, a, b)
                if weight == 0:
                    break
            if weight == 0:
                continue
            used = {a for e in J for a in e}
            free = tuple(a for a in U if a not in used)
            for S in combinations(free, k):
                T = tuple(a for a in free if a not in S)
                fp = sym_products(Pv, S)
                if not fp:
                    continue
                fq = sym_products(Qv, T)
                if not fq:
                    continue
                for mu, cp in fp.items():
                    for nu, cq in fq.items():
                        acc[(mu, nu)] = acc.get((mu, nu), 0) + weight * cp * cq
        out[k] = {key: c for key, c in acc.items() if c}
    return out


def z_eval(z_k, u, v):
    """Evaluate z in S^kV (x) S^kW as a bidegree-(k,k) form at (u,v)."""
    total = 0
    for (mu, nu), c in z_k.items():
        term = c
        for i in mu:
            term *= u[i]
        for j in nu:
            term *= v[j]
        total += term
    return total


@lru_cache(maxsize=None)
def iota(k: int, mu: tuple, nu: tuple) -> tuple:
    acc = {}
    for sigma in permutations(range(k)):
        key = tuple(sorted(kidx(mu[t], nu[sigma[t]]) for t in range(k)))
        acc[key] = acc.get(key, 0) + 1
    return tuple(sorted(acc.items()))


def iota_poly_of(z_k, k) -> dict:
    out = {}
    for (mu, nu), c in z_k.items():
        for m, cc in iota(k, mu, nu):
            out[m] = out.get(m, 0) + c * cc
    return {m: c for m, c in out.items() if c}


def graded_to_poly(source, h, z) -> dict:
    sp = s_poly(source)
    total = {}
    for k in range(2, h + 1):
        part = iota_poly_of(z[k], k)
        if h - k:
            part = poly_mul(part, poly_pow(sp, h - k))
        total = poly_add(total, part)
    return total


# ------------------------------------------------------- exact linear algebra

def rref_exact(rows):
    mat = [[Fraction(x) for x in r] for r in rows]
    ncols = len(mat[0]) if mat else 0
    pivots, row = [], 0
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


def reduce_vector(basis, pivots, target):
    vec = [Fraction(x) for x in target]
    for r, col in enumerate(pivots):
        if vec[col]:
            f = vec[col]
            vec = [a - f * b for a, b in zip(vec, basis[r])]
    return vec


def in_span(basis, pivots, target) -> bool:
    return all(x == 0 for x in reduce_vector(basis, pivots, target))


def solve_combination(rows, target):
    """Exact lambda with sum lambda_i rows[i] = target, or None."""
    n = len(rows)
    ncols = len(target)
    aug = [[Fraction(rows[i][c]) for i in range(n)] + [Fraction(target[c])]
           for c in range(ncols)]
    # Gaussian elimination on the (ncols x (n+1)) system
    piv_cols, row = [], 0
    for col in range(n):
        piv = None
        for r in range(row, len(aug)):
            if aug[r][col]:
                piv = r
                break
        if piv is None:
            continue
        aug[row], aug[piv] = aug[piv], aug[row]
        inv = 1 / aug[row][col]
        aug[row] = [x * inv for x in aug[row]]
        pr = aug[row]
        for r in range(len(aug)):
            if r != row and aug[r][col]:
                f = aug[r][col]
                aug[r] = [a - f * b for a, b in zip(aug[r], pr)]
        piv_cols.append(col)
        row += 1
        if row == len(aug):
            break
    for r in range(row, len(aug)):
        if aug[r][n] != 0 and all(aug[r][c] == 0 for c in range(n)):
            return None
    lam = [Fraction(0)] * n
    for r, col in enumerate(piv_cols):
        lam[col] = aug[r][n]
    return lam


# -------------------------------------------------------- L-monomial helpers

LNAMES = ("s", "k0", "k1", "k2")


def l_monomials(h):
    out = set()
    for combo in combinations_with_replacement(range(4), h):
        a = sum(1 for x in combo if x == 0)
        b = tuple(sum(1 for x in combo if x == c + 1) for c in COLORS)
        out.add((a, b))
    return sorted(out)


def mono_name(a, b):
    parts = []
    if a:
        parts.append("s" if a == 1 else f"s^{a}")
    for c in COLORS:
        if b[c] == 1:
            parts.append(f"k{c}")
        elif b[c] > 1:
            parts.append(f"k{c}^{b[c]}")
    return "".join(parts) if parts else "1"


def mono_poly(a, b, s_vec):
    sp = {(k,): s_vec[k] for k in range(NCAP) if s_vec[k]}
    poly = poly_pow(sp, a)
    for c in COLORS:
        for _ in range(b[c]):
            poly = poly_mul(poly, {(kidx(c, c),): 1})
    return poly


def det3(A):
    return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
            - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))


def rank3(A):
    rows = [[Fraction(x) for x in r] for r in A]
    r = 0
    for c in range(3):
        piv = None
        for i in range(r, 3):
            if rows[i][c]:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = 1 / rows[r][c]
        rows[r] = [x * inv for x in rows[r]]
        for i in range(3):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r


def no_zero_row_or_col(A):
    return (all(any(A[i][j] for j in COLORS) for i in COLORS)
            and all(any(A[i][j] for i in COLORS) for j in COLORS))


# ---------------------------------------------------------- Sigma_k / L_h(A)

@lru_cache(maxsize=None)
def sigma_basis(k):
    ms = monomials(3, k)
    return tuple((mu, nu) for mu in ms for nu in ms)


def sigma_rows(k, degree, s_vec):
    """Rows s^{degree-k} iota_k(e_mu (x) f_nu) in the S^degree monomial basis."""
    sp = {(i,): s_vec[i] for i in range(NCAP) if s_vec[i]}
    spow = poly_pow(sp, degree - k)
    rows = []
    for mu, nu in sigma_basis(k):
        poly = dict(iota(k, mu, nu))
        if degree - k:
            poly = poly_mul(poly, spow)
        rows.append(poly_row(poly, degree) if poly else [0] * len(
            monomial_index(NCAP, degree)))
    return rows


def L_rows(h, s_vec):
    rows = []
    for k in range(2, h + 1):
        rows.extend(sigma_rows(k, h, s_vec))
    return rows
