#!/usr/bin/env python3
"""Independent audit of the p=28 4^3 3^6 even--odd span drop.

No code is imported from the primary checker.  This script reconstructs
the exact residual selections, common-kernel Wronskian bounds, coprime
pair intersections, five-product determinant, and even/odd direct sum.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


RESIDUALS = (
    (0, 10, 0, 0),
    (0, 10, 1, -2),
    (2, 7, 0, 1),
    (2, 7, 1, -1),
    (3, 6, 0, 0),
    (3, 6, 1, -2),
    (7, 0, 0, 2),
    (7, 0, 1, 0),
    (7, 0, 2, -2),
)


def check_exact_residual_applicability() -> None:
    assert all(4 * e + 3 * a + 2 * b + u == 30
               for e, a, b, u in RESIDUALS)
    covered = tuple(profile for profile in RESIDUALS
                    if profile[0] == 3 and profile[1] == 6)
    assert covered == ((3, 6, 0, 0), (3, 6, 1, -2))

    for h in range(22, 28):
        k = 28 - h
        for e, a, b, u in covered:
            fixed_doubles = b
            selected_repeated_layers = fixed_doubles + 1
            selected_singletons = h + 2 - 2 * selected_repeated_layers
            assert selected_singletons == h + u

            complement = (4,) * e + (3,) * (a - 1) + (1,)
            assert complement == (4, 4, 4, 3, 3, 3, 3, 3, 1)
            assert len(complement) == 9
            assert sum(complement) == 28

            # The q=6 selected-row inequality is exactly saturated for all
            # six p=28 splits.  The optional double is a fixed role-two
            # layer and is absent from the complementary relation profile.
            forced = (
                4 * selected_repeated_layers
                + 5 * selected_singletons
                + max(0, 6 - k)
            )
            selected_degree = h + 3 - selected_repeated_layers
            cap = 6 * (selected_degree + 1 - 6)
            assert forced == cap

            restored = (4,) * 3 + (3,) * 6
            assert len(restored) == 9
            assert sum(restored) == 30


def check_common_kernel_bound() -> None:
    baseline = (4,) * 3 + (3,) * 6
    ambient_degree = len(baseline)
    assert ambient_degree == 9
    for dimension, expected_gap in ((6, 0), (7, 12)):
        forced = sum(max(0, dimension - order) for order in baseline)
        cap = dimension * (ambient_degree + 1 - dimension)
        assert forced - cap == expected_gap

    # If a common kernel had dimension at least seven, a seven-subspace
    # would inherit all exact rows.  Its positive gap excludes it, so the
    # common kernel has dimension at most six.
    assert 12 > 0


def coefficient_vector(poly: sp.Expr, variable: sp.Symbol, degree: int) -> list[sp.Expr]:
    polynomial = sp.Poly(sp.expand(poly), variable)
    return [polynomial.coeff_monomial(variable**power)
            for power in range(degree + 1)]


def check_pair_intersection_identity() -> None:
    z = sp.symbols("z")
    values = (1, 2, 3, 4, 5, 6)
    factors = {value: sp.Poly((z**2 - value**2) ** 2, z)
               for value in values}

    for i, j in combinations(values, 2):
        assert factors[i].degree() == factors[j].degree() == 4
        assert sp.gcd(factors[i], factors[j]).degree() == 0
        product = factors[i] * factors[j]
        assert product.degree() == 8

        # B_i P_5 and B_j P_5 live in P_9.  Coprimality says every
        # common member is B_i B_j times a polynomial of degree <=1.
        pair_ambient_dimension = 9 - product.degree() + 1
        common_space_upper = 6
        intersection_lower = 4 + 4 - common_space_upper
        assert pair_ambient_dimension == intersection_lower == 2

        expected_basis = [product.as_expr(), z * product.as_expr()]
        matrix = sp.Matrix(
            [coefficient_vector(poly, z, 9) for poly in expected_basis]
        )
        assert matrix.rank() == 2


def check_five_product_span_and_direct_sum() -> None:
    t, z = sp.symbols("t z")
    a = sp.symbols("a0:4")
    pairs = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3))
    products = [(t - a[i]) ** 2 * (t - a[j]) ** 2 for i, j in pairs]
    coefficient_matrix = sp.Matrix(
        [coefficient_vector(poly, t, 4) for poly in products]
    )
    determinant = sp.factor(coefficient_matrix.det())
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

    # Check the same five-edge recipe for every four-subset of six
    # concrete distinct squares, independently of the symbolic factor.
    squares = (1, 4, 9, 16, 25, 36)
    for chosen in combinations(squares, 4):
        specialization = {a[index]: chosen[index] for index in range(4)}
        specialized = coefficient_matrix.subs(specialization)
        assert specialized.rank() == 5
        assert determinant.subs(specialization) != 0

    # Substitute t=z^2.  The five even products and their z multiples
    # form a block-diagonal coefficient matrix in degrees 0,...,9, with
    # two copies of the nonsingular five-by-five product matrix.
    even_products = [sp.expand(poly.subs(t, z**2)) for poly in products]
    ten_polynomials = even_products + [sp.expand(z * poly) for poly in even_products]
    ten_by_ten = sp.Matrix(
        [coefficient_vector(poly, z, 9) for poly in ten_polynomials]
    )
    even_columns = (0, 2, 4, 6, 8)
    odd_columns = (1, 3, 5, 7, 9)
    even_block = ten_by_ten.extract(range(5), even_columns)
    odd_block = ten_by_ten.extract(range(5, 10), odd_columns)
    even_to_odd = ten_by_ten.extract(range(5), odd_columns)
    odd_to_even = ten_by_ten.extract(range(5, 10), even_columns)
    assert even_block == coefficient_matrix
    assert odd_block == coefficient_matrix
    assert even_to_odd == sp.zeros(5)
    assert odd_to_even == sp.zeros(5)
    # After the even/odd column permutation, the matrix is block diagonal
    # with two copies of coefficient_matrix.  Its determinant is therefore
    # determinant**2; computing that large symbolic determinant directly
    # would only obscure this exact structural identity.
    assert determinant != 0

    specialization = {a[index]: (index + 1) ** 2 for index in range(4)}
    assert ten_by_ten.subs(specialization).rank() == 10
    assert 10 > 6


def main() -> None:
    check_exact_residual_applicability()
    check_common_kernel_bound()
    check_pair_intersection_identity()
    check_five_product_span_and_direct_sum()
    print("p=28 4^3 3^6 even--odd span independent audit: PASS")
    print("covered residual tuples: (3,6,0,0), (3,6,1,-2)")
    print("five even products plus odd multiples have exact rank 10")
    print("scope guard: selected-kernel dimension drop only")


if __name__ == "__main__":
    main()
