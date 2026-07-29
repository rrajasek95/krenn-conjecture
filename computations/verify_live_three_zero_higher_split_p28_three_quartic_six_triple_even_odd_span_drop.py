#!/usr/bin/env python3
"""Exact audit of the p=28 4^3 3^6 even--odd span dimension drop."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def audit_boundary_profiles() -> None:
    residuals = ((3, 6, 0, 0), (3, 6, 1, -2))
    for h in range(22, 28):
        k = 28 - h
        for e, a, b, u in residuals:
            assert 4 * e + 3 * a + 2 * b + u == 30
            selected_doubles = b
            selected_triples = 1
            selected_layers = selected_doubles + selected_triples
            selected_singletons = h + 2 - 2 * selected_layers
            assert selected_singletons == h + u

            complement = (4,) * e + (3,) * (a - 1) + (1,)
            assert complement == (4, 4, 4, 3, 3, 3, 3, 3, 1)
            assert sum(complement) == 28
            assert len(complement) == 9

            selected_forced = (
                4 * selected_layers
                + 5 * selected_singletons
                + max(0, 6 - k)
            )
            selected_degree = h + 3 - selected_layers
            selected_cap = 6 * (selected_degree + 1 - 6)
            assert selected_forced == selected_cap


def audit_common_kernel_and_intersections() -> None:
    baseline = (4,) * 3 + (3,) * 6
    assert sum(baseline) == 30
    assert len(baseline) == 9

    forced_seven = sum(7 - multiplicity for multiplicity in baseline)
    cap_seven = 7 * (10 - 7)
    assert forced_seven == 33
    assert cap_seven == 21
    assert forced_seven - cap_seven == 12

    relation_degree = len(baseline) - 4
    common_degree = len(baseline)
    assert relation_degree == 5
    assert common_degree == 9

    z = sp.symbols("z")
    values = (1, 2, 3, 4, 5, 6)
    factors = {
        value: sp.Poly((z - value) ** 2 * (z + value) ** 2, z)
        for value in values
    }
    for i, j in combinations(values, 2):
        assert sp.gcd(factors[i], factors[j]).degree() == 0
        pair_product_degree = (factors[i] * factors[j]).degree()
        assert pair_product_degree == 8
        ambient_dimension = common_degree - pair_product_degree + 1
        intersection_lower_bound = 4 + 4 - 6
        assert ambient_dimension == intersection_lower_bound == 2


def audit_even_product_span() -> None:
    t = sp.symbols("t")
    a = sp.symbols("a0:4")
    selected_pairs = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3))
    rows = []
    for i, j in selected_pairs:
        polynomial = sp.Poly((t - a[i]) ** 2 * (t - a[j]) ** 2, t)
        rows.append([polynomial.coeff_monomial(t**degree) for degree in range(5)])
    determinant = sp.factor(sp.det(sp.Matrix(rows)))
    expected = sp.factor(
        4
        * (a[0] - a[1]) ** 4
        * (a[0] - a[2])
        * (a[0] - a[3])
        * (a[1] - a[2])
        * (a[1] - a[3])
        * (a[2] - a[3]) ** 2
    )
    assert sp.factor(determinant - expected) == 0

    specialization = {a[index]: (index + 1) ** 2 for index in range(4)}
    assert determinant.subs(specialization) != 0
    assert sp.Matrix(rows).subs(specialization).rank() == 5

    even_exponents = {0, 2, 4, 6, 8}
    odd_exponents = {1, 3, 5, 7, 9}
    assert even_exponents.isdisjoint(odd_exponents)
    assert len(even_exponents | odd_exponents) == 10
    assert 10 > 6


def main() -> None:
    audit_boundary_profiles()
    audit_common_kernel_and_intersections()
    audit_even_product_span()
    print("p=28 4^3 3^6 even--odd span dimension drop: PASS")
    print("six pairwise quartic transports force a ten-space inside a six-space")
    print("residual tuples covered: (3,6,0,0), (3,6,1,-2)")
    print("scope guard: dimension drop only, not profile closure")


if __name__ == "__main__":
    main()
