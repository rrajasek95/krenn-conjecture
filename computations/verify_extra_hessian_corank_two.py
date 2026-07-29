#!/usr/bin/env python3
"""Exact audit for extra-hessian-corank-two-propagation.md.

The theorem is proved symbolically in the note.  This checker audits the
normalizations of the curvature identities in the site-square-zero algebra
and tests gauge descent on a genuine nongauge kernel vector.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from math import factorial


N = 6
C = 3
R = N // 2
EMPTY = (-1,) * N


def add(*polys):
    out = {}
    for poly in polys:
        for monomial, value in poly.items():
            out[monomial] = out.get(monomial, Fraction(0)) + value
            if not out[monomial]:
                del out[monomial]
    return out


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return {m: scalar * v for m, v in poly.items() if scalar * v}


def mul(left, right):
    out = {}
    for a, av in left.items():
        for b, bv in right.items():
            if any(x >= 0 and y >= 0 for x, y in zip(a, b)):
                continue
            m = tuple(x if x >= 0 else y for x, y in zip(a, b))
            out[m] = out.get(m, Fraction(0)) + av * bv
            if not out[m]:
                del out[m]
    return out


def power(poly, exponent):
    out = {EMPTY: Fraction(1)}
    for _ in range(exponent):
        out = mul(out, poly)
    return out


def variable(site, color, value=1):
    monomial = [-1] * N
    monomial[site] = color
    return {tuple(monomial): Fraction(value)}


def cell(i, a, j, b, value=1):
    return mul(variable(i, a), variable(j, b, value))


def derivation(poly, weights):
    return {
        m: value * sum(weights[i] for i, color in enumerate(m) if color >= 0)
        for m, value in poly.items()
        if value * sum(weights[i] for i, color in enumerate(m) if color >= 0)
    }


def normalized_hessian(q, z):
    return scale(mul(z, power(q, R - 1)), Fraction(1, factorial(R - 1)))


def matching_power(q):
    return scale(power(q, R), Fraction(1, factorial(R)))


def second(q, u, v):
    return scale(mul(mul(u, v), power(q, R - 2)), Fraction(1, factorial(R - 2)))


def third(q, u, v, z):
    return scale(
        mul(mul(mul(u, v), z), power(q, R - 3)),
        Fraction(1, factorial(R - 3)),
    )


def deterministic_dense_data():
    q = {}
    for i, j in combinations(range(N), 2):
        for a, b in product(range(C), repeat=2):
            value = ((i + 2) * (j + 3) + 2 * a - 3 * b + a * b) % 11 - 5
            if value:
                q = add(q, cell(i, a, j, b, value))

    p = []
    s = []
    for c in range(C):
        pc = {}
        sc = {}
        for i in range(N):
            for a in range(C):
                pv = ((c + 1) * (i + 2) + 2 * a) % 7 - 3
                sv = ((c + 2) * (i + 1) - a) % 7 - 3
                if pv:
                    pc = add(pc, variable(i, a, pv))
                if sv:
                    sc = add(sc, variable(i, a, sv))
        p.append(pc)
        s.append(sc)

    a = [[Fraction((3 * c - 2 * d + 4) % 9 - 4) for d in range(C)] for c in range(C)]
    return q, p, s, a


def audit_pair_curvature():
    q, p, s, a = deterministic_dense_data()
    qtop = matching_power(q)
    lam = [[a[c][d] / R for d in range(C)] for c in range(C)]
    b = [[mul(p[c], s[d]) for d in range(C)] for c in range(C)]
    k = [
        [add(b[c][d], scale(q, lam[c][d])) for d in range(C)]
        for c in range(C)
    ]

    # K normalization: H(K)=H(ps)+a Q.
    for c, d in product(range(C), repeat=2):
        assert normalized_hessian(q, k[c][d]) == add(
            normalized_hessian(q, b[c][d]), scale(qtop, a[c][d])
        )

    # Raw rank-one minors and their normalized second-curvature form.
    for c, d, e, f in product(range(C), repeat=4):
        assert mul(b[c][d], b[e][f]) == mul(b[c][f], b[e][d])
        lhs = add(
            second(q, k[c][d], k[e][f]),
            scale(second(q, k[c][f], k[e][d]), -1),
        )
        rhs = add(
            scale(normalized_hessian(q, k[c][d]), (R - 1) * lam[e][f]),
            scale(normalized_hessian(q, k[e][f]), (R - 1) * lam[c][d]),
            scale(normalized_hessian(q, k[c][f]), -(R - 1) * lam[e][d]),
            scale(normalized_hessian(q, k[e][d]), -(R - 1) * lam[c][f]),
            scale(
                qtop,
                -R * (R - 1) * (
                    lam[c][d] * lam[e][f] - lam[c][f] * lam[e][d]
                ),
            ),
        )
        assert lhs == rhs

    # General cubic expansion.  In an actual pair solution the six H(K)
    # terms below vanish, leaving equation (26) of the note.
    c, d, e = 0, 1, 2
    left = ((c, d), (d, e), (e, c))
    right = ((c, e), (e, d), (d, c))
    assert mul(mul(b[c][d], b[d][e]), b[e][c]) == mul(
        mul(b[c][e], b[e][d]), b[d][c]
    )

    def cubic_side(indices):
        (i1, i2), (j1, j2), (h1, h2) = indices
        ks = (k[i1][i2], k[j1][j2], k[h1][h2])
        ls = (lam[i1][i2], lam[j1][j2], lam[h1][h2])
        cubic = third(q, *ks)
        pair_term = add(
            scale(second(q, ks[1], ks[2]), ls[0]),
            scale(second(q, ks[0], ks[2]), ls[1]),
            scale(second(q, ks[0], ks[1]), ls[2]),
        )
        hessian_term = add(
            scale(normalized_hessian(q, ks[2]), ls[0] * ls[1]),
            scale(normalized_hessian(q, ks[1]), ls[0] * ls[2]),
            scale(normalized_hessian(q, ks[0]), ls[1] * ls[2]),
        )
        return add(
            cubic,
            scale(pair_term, -(R - 2)),
            scale(hessian_term, (R - 1) * (R - 2)),
            scale(qtop, -R * (R - 1) * (R - 2) * ls[0] * ls[1] * ls[2]),
        )

    assert cubic_side(left) == cubic_side(right)


def audit_gauge_descent_on_extra_kernel():
    # Binary alternating Hamilton source, embedded in three colours.
    q = add(
        cell(0, 0, 1, 0, 2),
        cell(2, 0, 3, 0),
        cell(4, 0, 5, 0),
        cell(1, 1, 2, 1),
        cell(3, 1, 4, 1),
        cell(0, 1, 5, 1),
    )
    # The two unsupported same-shore cells from the nonintegrability note.
    z = add(cell(0, 1, 2, 1), cell(1, 0, 3, 0))
    assert not normalized_hessian(q, z)

    alpha = (2, -1, 3, -2, 1, -3)  # sum zero
    assert sum(alpha) == 0
    gauge = derivation(q, alpha)
    assert not normalized_hessian(q, gauge)
    # S(G,Z)=-H(D_alpha Z), exactly with the normalized factorials.
    assert add(second(q, gauge, z), normalized_hessian(q, derivation(z, alpha))) == {}

    # z is visibly nongauge: it has cells outside the support of q.
    assert any(m not in q for m in z)


def main():
    audit_pair_curvature()
    audit_gauge_descent_on_extra_kernel()
    print("extra-Hessian corank-two propagation identities: PASS")


if __name__ == "__main__":
    main()
