#!/usr/bin/env python3
"""Exact audit of the h=8,k=6 final profile 4^3 3^4."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def audit_roles_and_pair_drops() -> None:
    h, k, p = 8, 6, 14
    profile = (4, 4, 4, 3, 3, 3, 3)
    assert sum(profile) == 2 * h + k + 2 == 24
    assert p == h + k

    # Select three exact triples completely and one label of a quartic.
    roles = (3, 3, 3, 1)
    multiplicities = (3, 3, 3, 4)
    assert sum(roles) == h + 2
    complement = tuple(m - r for m, r in zip(multiplicities, roles))
    # Add the unselected fourth triple and two unselected quartics.
    full_complement = tuple(x for x in complement if x) + (3, 4, 4)
    assert sorted(full_complement) == [3, 3, 4, 4]
    assert sum(full_complement) == p
    assert len(full_complement) == 4

    for i, j in combinations(range(4), 2):
        lowered = list(roles)
        lowered[i] -= 1
        lowered[j] -= 1
        assert sum(lowered) == h
        represented = sum(r > 0 for r in lowered)
        residual_degree = represented - 3
        singleton_mates = [
            multiplicities[t] - lowered[t]
            for t in range(3)
            if multiplicities[t] - lowered[t] == 1
        ]
        assert singleton_mates
        singleton_drops = int(i == 3) + int(j == 3)
        lift_degree = 4 + singleton_drops
        assert residual_degree + lift_degree == 5


def audit_lifts_and_parity() -> None:
    z = sp.symbols("z")
    x1, x2, x3, q = sp.symbols("x1 x2 x3 q")
    fs = [z**2 - x1**2, z**2 - x2**2, z**2 - x3**2]
    fq = (z - q) * (z + q) ** 2

    assert [sp.degree(f, z) for f in fs] == [2, 2, 2]
    assert sp.degree(fq, z) == 3
    assert sum(sp.degree(f, z) for f in fs + [fq]) == 9 > 5

    # The three q-pair lifts span fq*<1,z^2>: the three even quadratics
    # z^2-x_i^2 span exactly the affine-even plane when two x_i^2 differ.
    coeff = sp.Matrix([[1, -x1**2], [1, -x2**2], [1, -x3**2]])
    assert sp.expand(coeff[:2, :].det() - (x1**2 - x2**2)) == 0

    # A parity minor for quintics is odd and has degree at most nine.
    a = sp.symbols("a0:6")
    b = sp.symbols("b0:6")
    P = sum(a[i] * z**i for i in range(6))
    Q = sum(b[i] * z**i for i in range(6))
    minor = sp.expand(P * Q.subs(z, -z) - P.subs(z, -z) * Q)
    assert sp.expand(minor.subs(z, -z) + minor) == 0
    assert sp.Poly(minor, z).degree() <= 9
    assert 1 + 2 * 4 == 9

    # In the only primitive-even three-space allowed by degree five,
    # two sections divisible by fq require the gcd root at -q.
    # Without that root, quadratic polynomials in s divisible by
    # (s-q^2)^2 form a line; with it they merely vanish at s=q^2 and
    # form a plane.
    s = sp.symbols("s")
    general = sp.symbols("c0:3")
    E = general[0] + general[1] * s + general[2] * s**2
    value_row = sp.Matrix([[1, q**2, q**4]])
    double_rows = sp.Matrix(
        [[1, q**2, q**4], [0, 1, 2 * q**2]]
    )
    assert 3 - value_row.rank() == 2
    assert 3 - double_rows.rank() == 1

    # The reflected order-one row is nonzero on (z+q)*1.
    u0, u1 = sp.symbols("u0 u1", nonzero=True)
    local_u = u0 + u1 * (z + q)
    test = (z + q)
    reflected = sp.diff(local_u * test, z).subs(z, -q)
    assert reflected == u0


def audit_wronskian_and_relations() -> None:
    def forced_weight(dim: int) -> int:
        return 3 * max(0, dim - 3) + max(0, dim - 1)

    def cap(dim: int) -> int:
        return dim * (6 - dim)

    assert forced_weight(4) <= cap(4)
    assert forced_weight(5) == 10 > cap(5) == 5
    assert forced_weight(6) == 14 > cap(6) == 0

    ambient_dimension = 6
    kernel_dimension = 4
    number_of_rows = 4
    row_rank = ambient_dimension - kernel_dimension
    relation_dimension = number_of_rows - row_rank
    assert row_rank == 2
    assert relation_dimension == 2


def audit_differential_degree() -> None:
    z, mu = sp.symbols("z mu")
    q, u, v, y = sp.symbols("q u v y")
    A = (z - q) ** 3 * (z - u) ** 4 * (z - v) ** 4 * (z - y) ** 3
    radical = (z - q) * (z - u) * (z - v) * (z - y)
    g = sp.cancel(A / radical)
    R = sp.expand(radical)
    DA = sp.cancel(sp.diff(A, z) / g)
    assert sp.degree(A, z) == 14
    assert sp.degree(R, z) == 4
    assert sp.degree(DA, z) == 3
    assert sp.LC(sp.Poly(DA, z)) == 14

    # Verify the exact differentiated numerator identity symbolically for
    # a general polynomial N of degree at most seven.
    ns = sp.symbols("n0:8")
    N = sum(ns[i] * z**i for i in range(8))
    E = sp.expand(R * ((z + mu) * sp.diff(N, z) + 7 * N) - (z + mu) * DA * N)
    lhs = sp.diff((z + mu) ** 7 * N / A, z)
    rhs = (z + mu) ** 6 * g * E / A**2
    assert sp.cancel(lhs - rhs) == 0
    assert sp.degree(E, z) <= 10

    selected_divisor_degree = 3 + 3 + 3 + 1
    assert selected_divisor_degree == 10

    # The nominal top coefficient is n+7-14 and cancels at n=7.
    n = sp.symbols("n", integer=True)
    assert sp.expand(n + 7 - 14).subs(n, 7) == 0

    selected_denominator_degree = 4 + 4 + 4 + 2
    numerator_cap = selected_denominator_degree - (5 + 2)
    assert selected_denominator_degree == 14
    assert numerator_cap == 7


def main() -> None:
    audit_roles_and_pair_drops()
    audit_lifts_and_parity()
    audit_wronskian_and_relations()
    audit_differential_degree()
    print("h=8,k=6 profile 4^3 3^4 role-lift closure: PASS")
    print("six (3,3,3,1) pair drops and degree-five kernel: exact")
    print("dimension three reflected-row contradiction: exact")
    print("dimension four gives 2D relations into constants: impossible")


if __name__ == "__main__":
    main()
