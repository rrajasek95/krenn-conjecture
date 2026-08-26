#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- h = 3 (eight sites) rank-one cap machinery.

The rank-one cap error at h = 3 (Lemma W17.0):

  E_w(u,v) = 6 e_3(alpha,beta)_w
             + 2 s(u,v) sum_{a<b in U} A_ab[w_a][w_b] e_2(alpha,beta|U\\{a,b})_w

with alpha_a = A_pa^T u (linear in u only) and beta_a = A_qa^T v (linear in
v only).  Every component is BIDEGREE (3,3): a sum of (u-cubic)*(v-cubic).
Polynomials are represented exactly as {(u-exponents, v-exponents): Fraction}.

Also here: the contraction laws of Theorem W17.4 (the perp-contraction), and
Singular query builders for
  (RK1)  exists (u,v): E = 0, u_c v_c != 0, u^T A_pq v != 0.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

from w17_core import COLORS, cross, oriented

ZERO3 = (0, 0, 0)


def bp_mul(f, g):
    out = {}
    for (mu1, mv1), c1 in f.items():
        for (mu2, mv2), c2 in g.items():
            key = ((mu1[0] + mu2[0], mu1[1] + mu2[1], mu1[2] + mu2[2]),
                   (mv1[0] + mv2[0], mv1[1] + mv2[1], mv1[2] + mv2[2]))
            out[key] = out.get(key, Fraction(0)) + c1 * c2
    return {k: c for k, c in out.items() if c != 0}


def bp_add(f, g):
    out = dict(f)
    for k, c in g.items():
        new = out.get(k, Fraction(0)) + c
        if new == 0:
            out.pop(k, None)
        else:
            out[k] = new
    return out


def bp_scale(f, lam):
    if lam == 0:
        return {}
    return {k: c * lam for k, c in f.items()}


def bp_lin_u(vec):
    out = {}
    for i, c in enumerate(vec):
        if c:
            mu = [0, 0, 0]
            mu[i] = 1
            out[(tuple(mu), ZERO3)] = Fraction(c)
    return out


def bp_lin_v(vec):
    out = {}
    for j, c in enumerate(vec):
        if c:
            mv = [0, 0, 0]
            mv[j] = 1
            out[(ZERO3, tuple(mv))] = Fraction(c)
    return out


def bp_str(f):
    """Singular polynomial string."""
    parts = []
    for (mu, mv), c in sorted(f.items()):
        mono = [f"({c.numerator}/{c.denominator})"]
        for i, e in enumerate(mu):
            if e:
                mono.append(f"u{i}^{e}" if e > 1 else f"u{i}")
        for j, e in enumerate(mv):
            if e:
                mono.append(f"v{j}^{e}" if e > 1 else f"v{j}")
        parts.append("*".join(mono))
    return "+".join(parts) if parts else "0"


def bp_eval(f, u, v):
    total = Fraction(0)
    for (mu, mv), c in f.items():
        term = c
        for i, e in enumerate(mu):
            term *= u[i] ** e
        for j, e in enumerate(mv):
            term *= v[j] ** e
        total += term
    return total


# ------------------------------------------------------------- ingredients


def star_forms(source, p, q, sites):
    """alpha[a][c] (u-linear) and beta[a][c] (v-linear) as bipolys."""
    alpha, beta = {}, {}
    for a in sites:
        apa, aqa = oriented(source, p, a), oriented(source, q, a)
        alpha[a] = [bp_lin_u([apa[i][c] for i in range(3)]) for c in COLORS]
        beta[a] = [bp_lin_v([aqa[j][c] for j in range(3)]) for c in COLORS]
    return alpha, beta


def s_bipoly(source, p, q):
    apq = oriented(source, p, q)
    out = {}
    for i in range(3):
        for j in range(3):
            if apq[i][j]:
                mu, mv = [0, 0, 0], [0, 0, 0]
                mu[i] = 1
                mv[j] = 1
                out[(tuple(mu), tuple(mv))] = Fraction(apq[i][j])
    return out


def elem_bipoly(alpha, beta, word_of, subset, k):
    """e_k(alpha,beta) over `subset` at the given colours, by DP."""
    poly = [{(ZERO3, ZERO3): Fraction(1)}] + [{} for _ in range(len(subset))]
    for a in subset:
        av, bv = alpha[a][word_of[a]], beta[a][word_of[a]]
        new = [{} for _ in range(len(subset) + 1)]
        for j, cur in enumerate(poly):
            if not cur:
                continue
            if bv:
                new[j] = bp_add(new[j], bp_mul(cur, bv))
            if av and j + 1 <= len(subset):
                new[j + 1] = bp_add(new[j + 1], bp_mul(cur, av))
        poly = new
    return poly[k] if k < len(poly) else {}


def rank_one_equations_h3(source, p, q, sites):
    """{word: bipoly} for the nonzero components of E_pq(u (x) v)."""
    sites = tuple(sites)
    assert len(sites) == 6
    alpha, beta = star_forms(source, p, q, sites)
    s = s_bipoly(source, p, q)
    eqs = {}
    for word in product(COLORS, repeat=6):
        word_of = {a: word[n] for n, a in enumerate(sites)}
        total = bp_scale(elem_bipoly(alpha, beta, word_of, sites, 3),
                         Fraction(6))
        for a, b in combinations(sites, 2):
            coeff = oriented(source, a, b)[word_of[a]][word_of[b]]
            if coeff == 0:
                continue
            rest = tuple(t for t in sites if t not in (a, b))
            e2 = elem_bipoly(alpha, beta, word_of, rest, 2)
            if not e2:
                continue
            total = bp_add(total, bp_scale(bp_mul(s, e2), 2 * Fraction(coeff)))
        if total:
            eqs[word] = total
    return eqs, s


# -------------------------------------------------------- Singular queries


UV = ("u0", "u1", "u2", "v0", "v1", "v2")


def rk1_query(eqs, s, tag, extra=()):
    gens = [bp_str(f) for f in eqs]
    gens += [bp_str(f) for f in extra]
    prod = f"({bp_str(s)})*u0*u1*u2*v0*v1*v2"
    return "\n".join([
        f'ring RR=0,({",".join(UV)},t),dp;',
        "ideal Iw=" + (",".join(gens) if gens else "0") + ";",
        f"ideal Jw=Iw,t*({prod})-1;",
        f'"RK1 {tag} "+string(dim(std(Jw)));'])


def rk1_query_modular(eqs, s, tag, prime, extra=()):
    return rk1_query(eqs, s, tag, extra).replace("ring RR=0,",
                                                 f"ring RR={prime},")


def parse_rk1(output, tag):
    for line in output.splitlines():
        f = line.split()
        if f and f[0] == "RK1" and f[1] == tag:
            return int(f[2]) != -1
    return None


# ------------------------------------------- degeneracy / perp contraction


def perp_conditions(source, p, q, sites):
    """The bidegree-(1,1) forms  (alpha_a x beta_a) . A_ab  for all ordered
    (a,b), a != b in U  (Theorem W17.4: they all vanish at an admissible
    clean rank-one cap whose sites are all nondegenerate)."""
    sites = tuple(sites)
    alpha, beta = star_forms(source, p, q, sites)
    out = {}
    for a in sites:
        # phi = alpha_a x beta_a as a triple of bipolys (bidegree (1,1))
        phi = []
        for i, j in ((1, 2), (2, 0), (0, 1)):
            term = bp_add(bp_mul(alpha[a][i], beta[a][j]),
                          bp_scale(bp_mul(alpha[a][j], beta[a][i]),
                                   Fraction(-1)))
            phi.append(term)
        for b in sites:
            if b == a:
                continue
            blk = oriented(source, a, b)
            forms = []
            for cb in COLORS:
                acc = {}
                for ca in COLORS:
                    if blk[ca][cb]:
                        acc = bp_add(acc, bp_scale(phi[ca],
                                                   Fraction(blk[ca][cb])))
                forms.append(acc)
            out[(a, b)] = forms
    return out


def site_degeneracy(source, p, q, sites, u, v):
    """rank of T_a = [alpha_a | beta_a] for a numeric cap (u,v)."""
    from w17_core import alpha_beta, site_rank
    alpha, beta = alpha_beta(source, p, q, u, v, sites)
    return {a: site_rank(alpha[a], beta[a]) for a in sites}
