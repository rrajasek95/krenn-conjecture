#!/usr/bin/env python3
"""UNAUDITED PROBE -- witness-splitting dichotomy, step P1 core library.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

Exact rational (integer/Fraction) constructors for the N=8 (h=3) clean-pair
cap data of notes/clean-pair-cap-exact-descent-target.md, built with the same
conventions as the committed checkers

    computations/verify_clean_pair_cap_exact_descent_target.py
    computations/verify_clean_pair_cap_exact_descent_symbolic.py

Sites: P=0, Q=1, U=(2,...,7).  Blocks A[(u,v)] for u<v are 3x3 tables
indexed [color_u][color_v] (endpoint-ordered exactly as ``edge_variable``
in the committed symbolic checker).

Objects (all exact):
    s(K)        = <K, A_pq>                          linear in K
    kappa_c(K)  = K(e_c^p, e_c^q) = K_cc             linear in K
    R_ab(K)     = K |- (A_pa A_qb + A_pb A_qa)       linear in K, in V_a (x) V_b
    r           = sum_{a<b in U} R_ab
    x           = sum_{a<b in U} A_ab
    6 E_pq(K)   = [3 s r^2 x + r^3]_full-support

E is TENSOR valued: its full-U-support component lives in (x)_{u in U} V_u,
i.e. 3^6 = 729 scalar components, each a cubic form in the nine coordinates
of K.  This library represents

    C[w][m] = coefficient of cubic K-monomial m in the component E_w,

for boundary words w in {0,1,2}^6 and the 165 cubic monomials m in 9
variables.  No floating point anywhere.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, product

P = 0
Q = 1
U = (2, 3, 4, 5, 6, 7)
B = (P, Q) + U
COLORS = (0, 1, 2)
# k-index of a cap coordinate K_{ij}: i is the P-colour, j the Q-colour.
NCAP = 9


def kidx(i: int, j: int) -> int:
    return 3 * i + j


def require(condition: object, detail: object) -> None:
    if not condition:
        raise AssertionError(detail)


# ---------------------------------------------------------------- matchings


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple:
    """Same recursion as the committed checkers."""
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


MATCHINGS_U = perfect_matchings(U)          # 15
MATCHINGS_B = perfect_matchings(B)          # 105
require(len(MATCHINGS_U) == 15, len(MATCHINGS_U))
require(len(MATCHINGS_B) == 105, len(MATCHINGS_B))

WORDS = tuple(product(COLORS, repeat=len(U)))       # 729, w[k] is site U[k]
WORD_INDEX = {w: n for n, w in enumerate(WORDS)}
SITE_SLOT = {site: n for n, site in enumerate(U)}

CUBIC_MONOMIALS = tuple(combinations_with_replacement(range(NCAP), 3))
require(len(CUBIC_MONOMIALS) == 165, len(CUBIC_MONOMIALS))
MONOMIAL_INDEX = {m: n for n, m in enumerate(CUBIC_MONOMIALS)}


# ---------------------------------------------------------------- sources


def edge_key(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def block(source: dict, u: int, v: int, cu: int, cv: int):
    """A_{u|v}(cu, cv) with endpoint order handled exactly once."""
    if u < v:
        return source[(u, v)][cu][cv]
    return source[(v, u)][cv][cu]


def zero_source():
    return {edge_key(u, v): [[0] * 3 for _ in range(3)]
            for u, v in combinations(B, 2)}


def source_variables() -> tuple:
    """The 28*9 = 252 endpoint-ordered source coordinates."""
    return tuple(
        ("A", u, v, cu, cv)
        for u, v in combinations(B, 2)
        for cu in COLORS
        for cv in COLORS
    )


def random_source(rng, lo: int = -6, hi: int = 6, zero_prob: Fraction = None):
    src = {}
    for u, v in combinations(B, 2):
        table = []
        for cu in COLORS:
            row = []
            for cv in COLORS:
                if zero_prob is not None and rng.random() < float(zero_prob):
                    row.append(0)
                else:
                    row.append(rng.randint(lo, hi))
            table.append(row)
        src[(u, v)] = table
    return src


# ---------------------------------------------------------------- linear forms


def form_s(source) -> tuple:
    """s(K) as a 9-vector of coefficients."""
    return tuple(source[(P, Q)][i][j] for i in COLORS for j in COLORS)


def form_kappa(c: int) -> tuple:
    return tuple(1 if k == kidx(c, c) else 0 for k in range(NCAP))


def form_R(source, a: int, b: int, ca: int, cb: int) -> tuple:
    """R_ab(ca, cb) as a 9-vector: K |- (A_pa A_qb + A_pb A_qa)."""
    out = []
    for i in COLORS:
        for j in COLORS:
            out.append(
                block(source, P, a, i, ca) * block(source, Q, b, j, cb)
                + block(source, P, b, i, cb) * block(source, Q, a, j, ca)
            )
    return tuple(out)


def eval_form(form: tuple, cap: tuple):
    return sum(form[k] * cap[k] for k in range(NCAP))


# ---------------------------------------------------------------- cubic algebra


def linear_times_linear(f: tuple, g: tuple) -> dict:
    out = {}
    for k1 in range(NCAP):
        c1 = f[k1]
        if not c1:
            continue
        for k2 in range(NCAP):
            c2 = g[k2]
            if not c2:
                continue
            key = (k1, k2) if k1 <= k2 else (k2, k1)
            out[key] = out.get(key, 0) + c1 * c2
    return out


def quadratic_times_linear(quad: dict, h: tuple, scale, acc: dict) -> None:
    """acc += scale * quad * h, accumulating cubic monomials."""
    if not scale:
        return
    for (k1, k2), cq in quad.items():
        cq = cq * scale
        if not cq:
            continue
        for k3 in range(NCAP):
            c3 = h[k3]
            if not c3:
                continue
            key = tuple(sorted((k1, k2, k3)))
            acc[key] = acc.get(key, 0) + cq * c3


def eval_cubic(cubic: dict, cap: tuple):
    total = 0
    for (k1, k2, k3), coef in cubic.items():
        total += coef * cap[k1] * cap[k2] * cap[k3]
    return total


# ---------------------------------------------------------------- E, symbolic in K


def error_row(source, word: tuple) -> dict:
    """The cubic form E_w(K), w a boundary word on U (w[n] is site U[n]).

    E_w = sum over the 15 perfect matchings M of U of
              s * sum_{e in M} A_e * prod_{f in M\\{e}} R_f
            + prod_{f in M} R_f
    which is the full-support component of (3 s r^2 x + r^3)/6:
    r^2 x contributes 2 orderings of the two r-factors, r^3 contributes 3!,
    so (3*2) and 6 both cancel the 6.
    """
    s = form_s(source)
    acc: dict = {}
    for matching in MATCHINGS_U:
        forms = []
        xvals = []
        for a, b in matching:
            ca = word[SITE_SLOT[a]]
            cb = word[SITE_SLOT[b]]
            forms.append(form_R(source, a, b, ca, cb))
            xvals.append(source[(a, b)][ca][cb])
        # r^3 part
        quad = linear_times_linear(forms[0], forms[1])
        quadratic_times_linear(quad, forms[2], 1, acc)
        # 3 s r^2 x part: one designated x-edge, the other two are R factors
        for e in range(3):
            if not xvals[e]:
                continue
            others = [forms[t] for t in range(3) if t != e]
            quad_e = linear_times_linear(others[0], others[1])
            quadratic_times_linear(quad_e, s, xvals[e], acc)
    return {m: c for m, c in acc.items() if c}


def error_matrix(source, words=None) -> dict:
    """{word: cubic dict}, the rows of the coefficient matrix C."""
    if words is None:
        words = WORDS
    return {w: error_row(source, w) for w in words}


# ------------------------------------------------- independent direct evaluator


def direct_r(source, cap: tuple) -> dict:
    """r(K) as {edge: 3x3 table}, numeric in K."""
    out = {}
    for a, b in combinations(U, 2):
        table = [[eval_form(form_R(source, a, b, ca, cb), cap) for cb in COLORS]
                 for ca in COLORS]
        out[(a, b)] = table
    return out


def direct_x(source) -> dict:
    return {(a, b): source[(a, b)] for a, b in combinations(U, 2)}


def direct_error_tensor(source, cap: tuple) -> dict:
    """E as a numeric tensor, computed independently of ``error_row``.

    Uses the square-zero algebra directly: degree-6 terms are indexed by the
    perfect matchings of U, r^2 x picks one x-edge and r^3 none.
    """
    s = eval_form(form_s(source), cap)
    rr = direct_r(source, cap)
    xx = direct_x(source)
    out = {}
    for w in WORDS:
        total = 0
        for matching in MATCHINGS_U:
            rvals = [rr[(a, b)][w[SITE_SLOT[a]]][w[SITE_SLOT[b]]]
                     for a, b in matching]
            xvals = [xx[(a, b)][w[SITE_SLOT[a]]][w[SITE_SLOT[b]]]
                     for a, b in matching]
            total += rvals[0] * rvals[1] * rvals[2]
            for e in range(3):
                prod_r = 1
                for t in range(3):
                    if t != e:
                        prod_r *= rvals[t]
                total += s * xvals[e] * prod_r
        out[w] = total
    return out


def cap_contraction(source, cap: tuple) -> dict:
    """K |- H_B(A), by brute force over the 105 perfect matchings of B."""
    out = {}
    for w in WORDS:
        colors = {P: None, Q: None}
        for n, site in enumerate(U):
            colors[site] = w[n]
        total = 0
        for matching in MATCHINGS_B:
            for i in COLORS:
                for j in COLORS:
                    colors[P] = i
                    colors[Q] = j
                    term = cap[kidx(i, j)]
                    if not term:
                        continue
                    for u, v in matching:
                        term *= block(source, u, v, colors[u], colors[v])
                        if not term:
                            break
                    total += term
        out[w] = total
    return out


def s_plus_r_exp_x(source, cap: tuple) -> dict:
    """[(s+r) exp(x)]_U, the right-hand side of eq. (12)."""
    s = eval_form(form_s(source), cap)
    rr = direct_r(source, cap)
    xx = direct_x(source)
    out = {}
    for w in WORDS:
        total = 0
        for matching in MATCHINGS_U:
            xvals = [xx[(a, b)][w[SITE_SLOT[a]]][w[SITE_SLOT[b]]]
                     for a, b in matching]
            rvals = [rr[(a, b)][w[SITE_SLOT[a]]][w[SITE_SLOT[b]]]
                     for a, b in matching]
            total += s * xvals[0] * xvals[1] * xvals[2]
            for e in range(3):
                prod = rvals[e]
                for t in range(3):
                    if t != e:
                        prod *= xvals[t]
                total += prod
        out[w] = total
    return out


def matching_tensor(blocks: dict) -> dict:
    """H_U(y) for {edge: 3x3 table}."""
    out = {}
    for w in WORDS:
        total = 0
        for matching in MATCHINGS_U:
            term = 1
            for a, b in matching:
                term *= blocks[(a, b)][w[SITE_SLOT[a]]][w[SITE_SLOT[b]]]
            total += term
        out[w] = total
    return out


def canonical_y(source, cap: tuple) -> dict:
    """y = x + r/s (needs s != 0)."""
    s = Fraction(eval_form(form_s(source), cap))
    require(s != 0, "canonical_y needs s != 0")
    rr = direct_r(source, cap)
    xx = direct_x(source)
    return {
        e: [[Fraction(xx[e][ca][cb]) + Fraction(rr[e][ca][cb]) / s
             for cb in COLORS] for ca in COLORS]
        for e in xx
    }


# ---------------------------------------------------------------- linear algebra


def to_fp(value, p: int) -> int:
    """Reduce an int/Fraction into F_p (denominators must be prime to p)."""
    if isinstance(value, Fraction):
        require(value.denominator % p != 0, "denominator divisible by p")
        return value.numerator % p * pow(value.denominator, p - 2, p) % p
    return value % p


def rank_mod_p(rows, ncols: int, p: int) -> int:
    """Rank over F_p.  A nonzero k x k minor mod p is a nonzero minor over Z,
    so for integer input this is a CERTIFIED lower bound on the rank over Q."""
    mat = [[to_fp(c, p) for c in row] for row in rows]
    rank = 0
    pivot_row = 0
    for col in range(ncols):
        sel = None
        for rrow in range(pivot_row, len(mat)):
            if mat[rrow][col]:
                sel = rrow
                break
        if sel is None:
            continue
        mat[pivot_row], mat[sel] = mat[sel], mat[pivot_row]
        inv = pow(mat[pivot_row][col], p - 2, p)
        pr = mat[pivot_row]
        pr[:] = [(v * inv) % p for v in pr]
        for rrow in range(len(mat)):
            if rrow != pivot_row and mat[rrow][col]:
                factor = mat[rrow][col]
                target = mat[rrow]
                target[:] = [(a - factor * b) % p for a, b in zip(target, pr)]
        pivot_row += 1
        rank += 1
        if pivot_row == len(mat):
            break
    return rank


def rank_exact(rows, ncols: int) -> int:
    """Exact rank over Q via fraction-free elimination on Fraction rows."""
    mat = [[Fraction(c) for c in row] for row in rows]
    rank = 0
    pivot_row = 0
    for col in range(ncols):
        sel = None
        for rrow in range(pivot_row, len(mat)):
            if mat[rrow][col]:
                sel = rrow
                break
        if sel is None:
            continue
        mat[pivot_row], mat[sel] = mat[sel], mat[pivot_row]
        pr = mat[pivot_row]
        pivot = pr[col]
        for rrow in range(pivot_row + 1, len(mat)):
            if mat[rrow][col]:
                factor = mat[rrow][col] / pivot
                target = mat[rrow]
                target[:] = [a - factor * b for a, b in zip(target, pr)]
        pivot_row += 1
        rank += 1
        if pivot_row == len(mat):
            break
    return rank


def dense_rows(matrix: dict, words=None) -> list:
    """C as dense integer rows over the 165 cubic monomials."""
    if words is None:
        words = tuple(matrix)
    out = []
    for w in words:
        row = [0] * len(CUBIC_MONOMIALS)
        for m, c in matrix[w].items():
            row[MONOMIAL_INDEX[m]] = c
        out.append(row)
    return out


def first_nonproportional_pair(rows):
    """Return (i, j, colA, colB) certifying rank >= 2, else None."""
    nonzero = [(n, row) for n, row in enumerate(rows) if any(row)]
    for a in range(len(nonzero)):
        ia, ra = nonzero[a]
        for b in range(a + 1, len(nonzero)):
            ib, rb = nonzero[b]
            for c1 in range(len(ra)):
                for c2 in range(c1 + 1, len(ra)):
                    minor = ra[c1] * rb[c2] - ra[c2] * rb[c1]
                    if minor:
                        return (ia, ib, c1, c2, minor)
    return None
