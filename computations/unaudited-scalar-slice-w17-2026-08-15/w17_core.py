#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- the RANK-ONE (scalar-slice) cap theory.

Pinned HEAD: see PINNED_HEAD.txt (9ceaf0a).

Object.  B even, |B| = N = 2h + 2, blocks A_uv in V_u (x) V_v, V = C^3.
For a pair (p,q), U = B \\ {p,q}, |U| = 2h.  A RANK-ONE cap is
K = u (x) v, i.e. K(e_i^p, e_j^q) = u_i v_j.  Then

    s        = <K, A_pq>   = u^T A_pq v                     (scalar)
    kappa_c  = K_cc        = u_c v_c
    alpha_a  = A_pa^T u  in V_a,      beta_a = A_qa^T v  in V_a
    R_ab     = alpha_a (x) beta_b + beta_a (x) alpha_b   in V_a (x) V_b

and the descent-note cap error (eq. (4) of
notes/clean-pair-cap-exact-descent-target.md) becomes

    E_pq(u (x) v) = sum_{k=2}^{h} s^{h-k} [ r^k/k! exp(x) ]_U
                  = sum_{k=2}^{h} s^{h-k} k!
                       sum_{|S| = 2k} e_{S,k}(alpha,beta) (x) Haf_{U\\S}(A)

  e_{S,k}(alpha,beta) = sum_{A subset S, |A| = k}
                          (x)_{a in A} alpha_a (x)_{b in S\\A} beta_b
  Haf_T(A)            = sum over perfect matchings M of T of (x)_{ab in M} A_ab

This is the exact TENSOR-valued analogue of W5's scalar closed form
(slice_core.slice_error_rank2) with the substitutions
u_a -> alpha_a, v_a -> beta_a, w_ab -> A_ab, s -> u^T A_pq v.
It is Lemma W17.0 below; three independent evaluators are provided and
asserted equal.

ADMISSIBILITY (the descent interface): u_c v_c != 0 for c = 0,1,2 and
s != 0.  "CLEAN" here is always the descent-note predicate E_pq(K) = 0
(all 3^{2h} components), restricted to rank-one caps -- this is the
predicate W14 re-based the U(N) chain on, and it is the tensor object
whose monochrome component is W5's scalar slice error.

All arithmetic exact (int / Fraction / sympy Rational).  No floats.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
import os
import subprocess
import tempfile

COLORS = (0, 1, 2)


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def ekey(u, v):
    return (u, v) if u < v else (v, u)


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple) -> tuple:
    """Same recursion as the committed checkers / P1 / P2 cores."""
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


# ------------------------------------------------------------------ sources


def oriented(source, u, v):
    """Block with row index = colour at u, column index = colour at v."""
    if u < v:
        return source[(u, v)]
    m = source[(v, u)]
    return [[m[j][i] for j in range(3)] for i in range(3)]


def matrix_rank(matrix):
    rows = [[Fraction(e) for e in row] for row in matrix]
    rank = 0
    for col in range(len(rows[0])):
        piv = None
        for i in range(rank, len(rows)):
            if rows[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        head = rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i][col] != 0:
                f = rows[i][col] / head[col]
                rows[i] = [a - f * b for a, b in zip(rows[i], head)]
        rank += 1
    return rank


def ghz_coefficient(source, word, n):
    """H_B(A)_word by brute force over the perfect matchings of B."""
    total = Fraction(0)
    for matching in perfect_matchings(tuple(range(n))):
        term = Fraction(1)
        for a, b in matching:
            term *= oriented(source, a, b)[word[a]][word[b]]
            if term == 0:
                break
        total += term
    return total


def ghz_defects(source, n):
    bad = []
    for word in product(COLORS, repeat=n):
        target = 1 if len(set(word)) == 1 else 0
        if ghz_coefficient(source, word, n) != target:
            bad.append(word)
    return bad


# ------------------------------------------------- rank-one cap ingredients


def cap_scalars(source, p, q, u, v):
    """s = u^T A_pq v and kappa_c = u_c v_c."""
    apq = oriented(source, p, q)
    s = sum(u[i] * apq[i][j] * v[j] for i in range(3) for j in range(3))
    return s, [u[c] * v[c] for c in COLORS]


def alpha_beta(source, p, q, u, v, sites):
    """alpha_a = A_pa^T u, beta_a = A_qa^T v (vectors in V_a)."""
    alpha, beta = {}, {}
    for a in sites:
        apa, aqa = oriented(source, p, a), oriented(source, q, a)
        alpha[a] = [sum(u[i] * apa[i][c] for i in range(3)) for c in COLORS]
        beta[a] = [sum(v[j] * aqa[j][c] for j in range(3)) for c in COLORS]
    return alpha, beta


def _R_component(alpha, beta, a, b, ca, cb):
    return alpha[a][ca] * beta[b][cb] + beta[a][ca] * alpha[b][cb]


# ---------------------------------------------------------- evaluator (1)


def rank_one_error_direct(source, p, q, u, v, sites):
    """(1) E by the matching expansion: over perfect matchings M of U and
    subsets J of M with |J| >= 2 (the r-edges), the rest carrying A."""
    sites = tuple(sites)
    h = len(sites) // 2
    s, _ = cap_scalars(source, p, q, u, v)
    alpha, beta = alpha_beta(source, p, q, u, v, sites)
    slot = {a: n for n, a in enumerate(sites)}
    out = {}
    for word in product(COLORS, repeat=len(sites)):
        total = Fraction(0)
        for matching in perfect_matchings(sites):
            for size in range(2, h + 1):
                for J in combinations(range(h), size):
                    Jset = set(J)
                    term = s ** (h - size)
                    if term == 0:
                        continue
                    for n, (a, b) in enumerate(matching):
                        ca, cb = word[slot[a]], word[slot[b]]
                        if n in Jset:
                            term *= _R_component(alpha, beta, a, b, ca, cb)
                        else:
                            term *= oriented(source, a, b)[ca][cb]
                        if term == 0:
                            break
                    total += term
        if total != 0:
            out[word] = total
    return out


# ---------------------------------------------------------- evaluator (2)


def tensor_haf(source, sites, word_of):
    """Haf_T(A)_{word} for T = sites: sum over perfect matchings of T."""
    total = Fraction(0)
    for matching in perfect_matchings(tuple(sites)):
        term = Fraction(1)
        for a, b in matching:
            term *= oriented(source, a, b)[word_of[a]][word_of[b]]
            if term == 0:
                break
        total += term
    return total


def rank_one_error_closed(source, p, q, u, v, sites):
    """(2) E by the closed form  sum_k s^{h-k} k! sum_{|S|=2k}
    e_{S,k}(alpha,beta) (x) Haf_{U\\S}(A)   -- Lemma W17.0."""
    sites = tuple(sites)
    h = len(sites) // 2
    s, _ = cap_scalars(source, p, q, u, v)
    alpha, beta = alpha_beta(source, p, q, u, v, sites)
    slot = {a: n for n, a in enumerate(sites)}
    fact = [1, 1, 2, 6, 24, 120]
    out = {}
    for word in product(COLORS, repeat=len(sites)):
        word_of = {a: word[slot[a]] for a in sites}
        total = Fraction(0)
        for k in range(2, h + 1):
            for S in combinations(sites, 2 * k):
                rest = tuple(a for a in sites if a not in set(S))
                hafrest = tensor_haf(source, rest, word_of)
                if hafrest == 0:
                    continue
                esk = Fraction(0)
                for A in combinations(S, k):
                    Aset = set(A)
                    term = Fraction(1)
                    for a in S:
                        term *= (alpha[a][word_of[a]] if a in Aset
                                 else beta[a][word_of[a]])
                        if term == 0:
                            break
                    esk += term
                total += (s ** (h - k)) * fact[k] * esk * hafrest
        if total != 0:
            out[word] = total
    return out


# ---------------------------------------------------------- evaluator (3)


def rank_one_error_identity(source, p, q, u, v, sites):
    """(3) E from the cap identity  E = s^h Haf_U(y) - s^{h-1} K |_ H_B(A),
    y = x + r/s (needs s != 0).  Uses a brute-force contraction of the
    full N-site matching tensor for the second term."""
    sites = tuple(sites)
    n = len(sites) + 2
    h = len(sites) // 2
    s, _ = cap_scalars(source, p, q, u, v)
    require(s != 0, "identity evaluator needs s != 0")
    alpha, beta = alpha_beta(source, p, q, u, v, sites)
    slot = {a: n2 for n2, a in enumerate(sites)}
    # y_ab = A_ab + R_ab / s
    y = {}
    for a, b in combinations(sites, 2):
        blk = oriented(source, a, b)
        y[(a, b)] = [[Fraction(blk[ca][cb])
                      + Fraction(_R_component(alpha, beta, a, b, ca, cb), 1) / s
                      for cb in COLORS] for ca in COLORS]
    out = {}
    for word in product(COLORS, repeat=len(sites)):
        word_of = {a: word[slot[a]] for a in sites}
        hy = Fraction(0)
        for matching in perfect_matchings(sites):
            term = Fraction(1)
            for a, b in matching:
                aa, bb = (a, b) if a < b else (b, a)
                ca, cb = (word_of[a], word_of[b]) if a < b else (word_of[b],
                                                                 word_of[a])
                term *= y[(aa, bb)][ca][cb]
                if term == 0:
                    break
            hy += term
        # K |_ H_B(A) at this U-word: sum over the colours at p and q
        cap = Fraction(0)
        for i in COLORS:
            for j in COLORS:
                coeff = u[i] * v[j]
                if coeff == 0:
                    continue
                full = [0] * n
                for a in sites:
                    full[a] = word_of[a]
                full[p], full[q] = i, j
                cap += coeff * ghz_coefficient(source, tuple(full), n)
        value = s ** h * hy - s ** (h - 1) * cap
        if value != 0:
            out[word] = value
    return out


def rank_one_error(source, p, q, u, v, sites, check=False):
    value = rank_one_error_direct(source, p, q, u, v, sites)
    if check:
        require(value == rank_one_error_closed(source, p, q, u, v, sites),
                ("evaluator (1) != (2)", p, q))
        s, _ = cap_scalars(source, p, q, u, v)
        if s != 0:
            require(value == rank_one_error_identity(source, p, q, u, v, sites),
                    ("evaluator (1) != (3)", p, q))
    return value


def is_admissible(source, p, q, u, v):
    s, kappa = cap_scalars(source, p, q, u, v)
    return s != 0 and all(k != 0 for k in kappa)


# ------------------------------------------------- h = 2 structure theorem


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def site_rank(alpha_a, beta_a):
    """rank of T_a = [alpha_a | beta_a] : C^2 -> V_a  (0, 1 or 2)."""
    if all(x == 0 for x in alpha_a) and all(x == 0 for x in beta_a):
        return 0
    if any(x != 0 for x in cross(alpha_a, beta_a)):
        return 2
    return 1


def site_ratio(alpha_a, beta_a):
    """(lambda_a : mu_a) with alpha = lambda*gamma, beta = mu*gamma, for a
    site of rank <= 1.  Returns (0,0) at rank 0."""
    for c in COLORS:
        if alpha_a[c] != 0 or beta_a[c] != 0:
            gamma_c = c
            break
    else:
        return (Fraction(0), Fraction(0))
    g = alpha_a[gamma_c] if alpha_a[gamma_c] != 0 else beta_a[gamma_c]
    return (Fraction(alpha_a[gamma_c], 1) / g, Fraction(beta_a[gamma_c], 1) / g)


def ehom(lams, mus, j):
    """e^hom_j = sum_{|B| = j} prod_B lambda prod_{complement} mu."""
    n = len(lams)
    total = Fraction(0)
    for B in combinations(range(n), j):
        Bs = set(B)
        term = Fraction(1)
        for i in range(n):
            term *= lams[i] if i in Bs else mus[i]
        total += term
    return total


def h2_structure_predicate(source, p, q, u, v, sites):
    """Theorem W17.1: E_pq(u (x) v) = 0 at h = 2 iff, with I the set of
    rank-2 sites, e^hom_j(lambda, mu | U \\ I) = 0 for every j <= 2 with
    2 - j <= |I|.  Returns (predicate, diagnostics)."""
    sites = tuple(sites)
    require(len(sites) == 4, "h2 predicate needs |U| = 4")
    alpha, beta = alpha_beta(source, p, q, u, v, sites)
    ranks = {a: site_rank(alpha[a], beta[a]) for a in sites}
    I = [a for a in sites if ranks[a] == 2]
    rest = [a for a in sites if ranks[a] != 2]
    ratios = [site_ratio(alpha[a], beta[a]) for a in rest]
    lams = [r[0] for r in ratios]
    mus = [r[1] for r in ratios]
    conditions = {}
    ok = True
    for j in range(0, 3):
        if 2 - j <= len(I) and j <= len(rest):
            value = ehom(lams, mus, j)
            conditions[j] = value
            if value != 0:
                ok = False
        elif 2 - j <= len(I) and j > len(rest):
            conditions[j] = Fraction(0)     # empty sum
    return ok, {"ranks": ranks, "I": I, "rest": rest,
                "lambda": lams, "mu": mus, "conditions": conditions}


# ------------------------------------------------------------------ Singular


def run_singular(script: str, timeout: int = 900):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    try:
        proc = subprocess.run(["Singular", "-q", "--no-warn", path],
                              capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(path)
    if proc.returncode != 0:
        raise RuntimeError(f"Singular failed: {proc.stderr[:2000]}")
    return proc.stdout


UV = tuple(f"u{c}" for c in COLORS) + tuple(f"v{c}" for c in COLORS)


# ------------------------------------------------ symbolic (u,v) equations


def sym_setup():
    import sympy
    u = sympy.symbols("u0 u1 u2")
    v = sympy.symbols("v0 v1 v2")
    return u, v


def sym_rank_one_equations(source, p, q, sites):
    """The components of E_pq(u (x) v) as sympy polynomials in (u,v),
    bidegree (h, h).  Uses the closed form (evaluator 2) symbolically."""
    import sympy
    u, v = sym_setup()
    sites = tuple(sites)
    h = len(sites) // 2
    apq = oriented(source, p, q)
    s = sympy.expand(sum(u[i] * sympy.Rational(apq[i][j]) * v[j]
                         for i in range(3) for j in range(3)))
    alpha, beta = {}, {}
    for a in sites:
        apa, aqa = oriented(source, p, a), oriented(source, q, a)
        alpha[a] = [sympy.expand(sum(u[i] * sympy.Rational(apa[i][c])
                                     for i in range(3))) for c in COLORS]
        beta[a] = [sympy.expand(sum(v[j] * sympy.Rational(aqa[j][c])
                                    for j in range(3))) for c in COLORS]
    slot = {a: n for n, a in enumerate(sites)}
    fact = [1, 1, 2, 6, 24, 120]
    eqs = {}
    for word in product(COLORS, repeat=len(sites)):
        word_of = {a: word[slot[a]] for a in sites}
        total = sympy.Integer(0)
        for k in range(2, h + 1):
            for S in combinations(sites, 2 * k):
                rest = tuple(a for a in sites if a not in set(S))
                hafrest = tensor_haf(source, rest, word_of)
                if hafrest == 0:
                    continue
                esk = sympy.Integer(0)
                for A in combinations(S, k):
                    Aset = set(A)
                    term = sympy.Integer(1)
                    for a in S:
                        term *= (alpha[a][word_of[a]] if a in Aset
                                 else beta[a][word_of[a]])
                    esk += term
                total += (s ** (h - k)) * fact[k] * sympy.Rational(hafrest) * esk
        total = sympy.expand(total)
        if total != 0:
            eqs[word] = total
    return eqs, s


def sympy_to_singular(expr):
    import sympy
    text = str(sympy.expand(expr))
    return text.replace("**", "^").replace(" ", "")


def rank_one_witness_query(eqs, s_expr, tag, extra=()):
    """Rabinowitsch: does an admissible rank-one witness exist?
    exists (u,v):  all E_w = 0, s != 0, u_c v_c != 0."""
    import sympy
    gens = [sympy_to_singular(e) for e in eqs]
    prod_str = "(" + sympy_to_singular(s_expr) + ")*u0*u1*u2*v0*v1*v2"
    lines = [f'ring RR=0,({",".join(UV)},t),dp;',
             "ideal Iw=" + (",".join(gens) if gens else "0") + ";"]
    for n, e in enumerate(extra):
        lines.append(f"Iw=Iw,{sympy_to_singular(e)};")
    lines += [f"ideal Jw=Iw,t*({prod_str})-1;",
              f'"RK1 {tag} "+string(dim(std(Jw)));']
    return "\n".join(lines)
