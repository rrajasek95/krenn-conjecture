#!/usr/bin/env python3
"""UNAUDITED PROBE -- W5 (Lemma J.1b): the SCALAR monochrome-slice theory.

Pinned HEAD: 181a4c084a91f1518c2bdfe2f574b9a7df1b1830

The object.  For a scalar (single-colour) weighting w on the complete graph
K_N, N = 2h + 2, and a pair (p, q) with U = B \\ {p, q}, |U| = 2h, put

    s      = w_pq
    r_ab   = w_pa w_qb + w_pb w_qa           (a, b in U)      [rank-two!]
    x_ab   = w_ab                            (a, b in U)
    E_pq   = sum_{k=2}^{h} s^{h-k} [ r^k / k! * exp(x) ]_U

exactly as in notes/clean-pair-cap-exact-descent-target.md eq. (4), and as
implemented (h = 3, tensor-valued) in the P1 probe's ``wsplit_core.error_row``.
``E_pq`` here is the SCALAR slice error: for a ternary source A it is the
K_cc^3-coefficient of the monochrome boundary word c^{2h} (see
``monochrome_slice`` and the cross-check in run_b).

Three independent evaluators are provided and are asserted equal everywhere:

  (1) ``slice_error_direct``   -- matching sum, the P1 convention;
  (2) ``slice_error_contract`` -- s^h haf_U(x + r/s) - s^{h-1} haf_B(w)
                                  (the exact contraction identity, eq. (15));
  (3) ``slice_error_rank2``    -- sum_k s^{h-k} haf(r|_S) haf(x|_{U\\S}) with
                                  haf of the rank-two matrix r|_S, |S| = 2k,
                                  evaluated by the closed form
                                  haf(uv^T + vu^T)|_S = k! * e_{S,k}(u, v),
                                  e_{S,k} = sum_{|A| = k, A in S} u_A v_{S\\A}.

Evaluator (3) is the structural characterization used throughout:

    h = 2:  E_pq = 2 e_{U,2}(u, v)                       (NO x, NO s)
    h = 3:  E_pq = 6 e_{U,3}(u, v)
                   + 2 s sum_{a<b in U} w_ab e_{U\\{a,b},2}(u, v)

with u_a = w_pa, v_a = w_qa.  Equivalently, with the binary form
Phi(al, be) = prod_{a in U} (v_a al + u_a be), e_{S,k} is the middle
coefficient [al^k be^k] of the sub-product over S.

All arithmetic exact (int / Fraction / sympy).  No floating point.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations


# ------------------------------------------------------------------ matchings


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple) -> tuple:
    """Same recursion as the committed checkers / P1 core."""
    if not vertices:
        return ((),)
    first = vertices[0]
    out = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            out.append(((first, second),) + tail)
    return tuple(out)


def require(condition, detail) -> None:
    if not condition:
        raise AssertionError(detail)


def ekey(a, b):
    return (a, b) if a < b else (b, a)


# ------------------------------------------------------------------ hafnians


def haf(w: dict, sites: tuple):
    """Hafnian of the scalar weighting w restricted to ``sites`` (even)."""
    if len(sites) == 0:
        return 1
    total = 0
    for matching in perfect_matchings(tuple(sites)):
        term = 1
        for a, b in matching:
            term *= w[ekey(a, b)]
            if term == 0:
                break
        total += term
    return total


def haf_matrix(mat: dict, sites: tuple):
    """Hafnian of an explicit {edge: value} table on ``sites``."""
    return haf(mat, sites)


# ------------------------------------------------------------ the slice error


def _r_table(w: dict, p, q, sites: tuple) -> dict:
    return {ekey(a, b): w[ekey(p, a)] * w[ekey(q, b)]
            + w[ekey(p, b)] * w[ekey(q, a)]
            for a, b in combinations(sites, 2)}


def slice_error_direct(w: dict, p, q, sites: tuple):
    """(1) E_pq by the matching sum, h = |sites| / 2 (h = 2 or 3).

    h = 2:  sum_M r_{e1} r_{e2}
    h = 3:  sum_M [ r_{e1} r_{e2} r_{e3}
                    + s * (x_{e1} r_{e2} r_{e3} + ... ) ]
    """
    hh = len(sites) // 2
    require(hh in (2, 3), ("direct evaluator implemented for h in {2,3}", hh))
    s = w[ekey(p, q)]
    rr = _r_table(w, p, q, sites)
    total = 0
    for matching in perfect_matchings(tuple(sites)):
        rvals = [rr[ekey(a, b)] for a, b in matching]
        xvals = [w[ekey(a, b)] for a, b in matching]
        if hh == 2:
            total += rvals[0] * rvals[1]
        else:
            total += rvals[0] * rvals[1] * rvals[2]
            for e in range(3):
                prod = s * xvals[e]
                for t in range(3):
                    if t != e:
                        prod *= rvals[t]
                total += prod
    return total


def slice_error_contract(w: dict, p, q, sites: tuple):
    """(2) E_pq = s^h haf_U(x + r/s) - s^{h-1} haf_B(w).  Needs s != 0."""
    hh = len(sites) // 2
    s = Fraction(w[ekey(p, q)])
    require(s != 0, "contraction evaluator needs s != 0")
    rr = _r_table(w, p, q, sites)
    y = {e: Fraction(w[e]) + Fraction(rr[e]) / s for e in rr}
    full = tuple(sorted(tuple(sites) + (p, q)))
    value = s ** hh * haf(y, tuple(sites)) - s ** (hh - 1) * haf(w, full)
    if isinstance(value, Fraction) and value.denominator == 1:
        return value.numerator
    return value


def elem_uv(u: dict, v: dict, subset: tuple, k: int):
    """e_{S,k}(u, v) = sum over k-subsets A of S of prod_A u * prod_{S\\A} v."""
    total = 0
    for A in combinations(subset, k):
        term = 1
        Aset = set(A)
        for a in subset:
            term *= u[a] if a in Aset else v[a]
        total += term
    return total


def slice_error_rank2(w: dict, p, q, sites: tuple):
    """(3) E_pq via haf(rank-two) = k! e_{S,k}: the structural closed form."""
    hh = len(sites) // 2
    s = w[ekey(p, q)]
    u = {a: w[ekey(p, a)] for a in sites}
    v = {a: w[ekey(q, a)] for a in sites}
    fact = [1, 1, 2, 6]
    total = 0
    for k in range(2, hh + 1):
        for S in combinations(sites, 2 * k):
            rest = tuple(a for a in sites if a not in set(S))
            total += (s ** (hh - k)) * fact[k] * elem_uv(u, v, S, k) * haf(w, rest)
    return total


def slice_error(w: dict, p, q, sites: tuple, check: bool = False):
    value = slice_error_direct(w, p, q, sites)
    if check:
        require(value == slice_error_rank2(w, p, q, sites),
                ("evaluator (1) != (3)", p, q))
        if w[ekey(p, q)] != 0:
            require(value == slice_error_contract(w, p, q, sites),
                    ("evaluator (1) != (2)", p, q))
    return value


# ------------------------------------------------------------------ cofactors


def cofactor(w: dict, sites: tuple, p, q):
    """C_pq = haf(w | B \\ {p,q}) = d haf / d w_pq."""
    rest = tuple(a for a in sites if a not in (p, q))
    return haf(w, rest)


# ----------------------------------------------- multilinearity / derivatives


def abs_weighting(w: dict) -> dict:
    return {e: abs(v) for e, v in w.items()}


def slice_error_abs(w: dict, p, q, sites: tuple):
    """E_pq evaluated on |w|: an upper bound for |E_pq| (all monomials of the
    rank-two closed form have coefficient > 0), and zero exactly when the
    error polynomial has NO surviving monomial (cleanliness by SUPPORT)."""
    return slice_error_rank2(abs_weighting(w), p, q, sites)


def set_edge(w: dict, e, value) -> dict:
    out = dict(w)
    out[e] = value
    return out


def partial(func, w: dict, e):
    """d func / d w_e for a MULTILINEAR (square-free) function of the edges."""
    return func(set_edge(w, e, 1)) - func(set_edge(w, e, 0))


# ------------------------------------------------ ternary source <-> GHZ rows


def ghz_row(source: dict, word: tuple, n: int = 8):
    """H_B(A)_word by brute force over the perfect matchings of B."""
    total = 0
    for matching in perfect_matchings(tuple(range(n))):
        term = 1
        for a, b in matching:
            term *= source[ekey(a, b)][word[a]][word[b]]
            if term == 0:
                break
        total += term
    return total


def det3(mat) -> object:
    return (mat[0][0] * (mat[1][1] * mat[2][2] - mat[1][2] * mat[2][1])
            - mat[0][1] * (mat[1][0] * mat[2][2] - mat[1][2] * mat[2][0])
            + mat[0][2] * (mat[1][0] * mat[2][1] - mat[1][1] * mat[2][0]))


def rank3(mat) -> int:
    rows = [[Fraction(v) for v in row] for row in mat]
    rank = 0
    used = [False] * 3
    for col in range(3):
        sel = None
        for i in range(3):
            if not used[i] and rows[i][col]:
                sel = i
                break
        if sel is None:
            continue
        used[sel] = True
        piv = rows[sel]
        for i in range(3):
            if i != sel and rows[i][col]:
                f = rows[i][col] / piv[col]
                rows[i] = [a - f * b for a, b in zip(rows[i], piv)]
        rank += 1
    return rank


# ------------------------------------------------ ternary source -> scalar slice


def monochrome_slice(source: dict, colour: int, n: int = 8) -> dict:
    """w_c(u,v) = A_uv[c][c] for a ternary source given as {(u,v): 3x3}."""
    return {ekey(u, v): source[ekey(u, v)][colour][colour]
            for u, v in combinations(range(n), 2)}


# ------------------------------------------------------------------ random data


def random_weighting(rng, sites: tuple, lo=-6, hi=6, zero_prob=None) -> dict:
    out = {}
    for a, b in combinations(sites, 2):
        if zero_prob is not None and rng.random() < zero_prob:
            out[ekey(a, b)] = 0
        else:
            out[ekey(a, b)] = rng.randint(lo, hi)
    return out


def normalize_haf(w: dict, sites: tuple):
    """Scale w so that haf(w) = 1 (haf is homogeneous of degree |sites|/2)."""
    value = haf(w, sites)
    if value == 0:
        return None
    m = len(sites) // 2
    lam = Fraction(1, 1)
    # need lam^m * value = 1; work over Q only when an m-th root exists.
    # Instead we return the rational scaling of a SINGLE edge orbit is wrong;
    # use the site-gauge: scale one site's incident edges by 1/value.
    scaled = dict(w)
    site = sites[0]
    for b in sites:
        if b == site:
            continue
        scaled[ekey(site, b)] = Fraction(scaled[ekey(site, b)], 1) / value
    require(haf(scaled, sites) == 1, "normalisation failed")
    del lam, m
    return scaled
