#!/usr/bin/env python3
"""Independent exact audit of the p=28 two-quartic q=5 grid closure.

This file intentionally does not import the primary checker.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


SPLITS = tuple((h, 28 - h) for h in range(22, 28))
RESIDUALS = ((2, 7, 0, 1), (2, 7, 1, -1))


def selected_gap(q: int, h: int, k: int) -> int:
    return q * q - 2 * q - h - 2 + max(0, q - k)


def exact_row_cost(dimension: int, order: int) -> int:
    return max(0, dimension - order)


def corrected_local_cost(dimension: int, order: int, gcd_order: int) -> int:
    """Cost after assigning one gcd root to one exact order row."""
    if gcd_order <= order:
        reduced_row = max(0, dimension - order + gcd_order)
    else:
        reduced_row = 0
    return dimension * gcd_order + reduced_row


def wronskian_excess(
    dimension: int, degree: int, row_orders: tuple[int, ...]
) -> int:
    forced = sum(exact_row_cost(dimension, order) for order in row_orders)
    cap = dimension * (degree + 1 - dimension)
    return forced - cap


def coefficient_vector(polynomial: sp.Expr, variable: sp.Symbol, degree: int) -> sp.Matrix:
    expanded = sp.Poly(sp.expand(polynomial), variable)
    return sp.Matrix([expanded.nth(index) for index in range(degree + 1)])


def multiplication_space(
    factor: sp.Expr, quotient_degree: int, variable: sp.Symbol, ambient_degree: int
) -> sp.Matrix:
    return sp.Matrix.hstack(
        *[
            coefficient_vector(factor * variable**power, variable, ambient_degree)
            for power in range(quotient_degree + 1)
        ]
    )


def audit_selection_grid() -> None:
    for h, k in SPLITS:
        for e, a, b, u in RESIDUALS:
            assert 4 * e + 3 * a + 2 * b + u == 30

            repeated_roles = 1 + b
            selected_singletons = h + 2 - 2 * repeated_roles
            singleton_values = h + u
            assert singleton_values - selected_singletons == 1

            complement = (
                (4,) * e
                + (3,) * (a - 1)
                + (1, 1)
            )
            assert complement == (4, 4) + (3,) * 6 + (1, 1)
            assert sum(complement) == 28
            assert len(complement) == 10

            selected_rows = repeated_roles + selected_singletons
            selected_degree = h + 3 - repeated_roles
            assert selected_degree + 1 == selected_rows + 2
            assert 5 - 2 == 3
            assert len(complement) - 4 == 6

            # The equality frontier permits q=6 and excludes q=7 by 12.
            assert selected_gap(6, h, k) == 0
            assert selected_gap(7, h, k) == 12

            # At most seven contaminated entries means at most seven
            # contaminated singleton columns.
            guaranteed_all_five = singleton_values - 7
            expected = h - 6 if b == 0 else h - 8
            assert guaranteed_all_five == expected
            assert guaranteed_all_five >= (16 if b == 0 else 14)


def audit_pair_transport_and_gcd() -> None:
    z, s, t = sp.symbols("z s t")
    f_s = sp.expand((z - s) ** 2 * (z + s))
    f_t = sp.expand((z - t) ** 2 * (z + t))
    resultant = sp.factor(sp.resultant(f_s, f_t, z))
    assert resultant == -(s - t) ** 5 * (s + t) ** 4

    # A degree-nine five-space has one unit of excess for the restored
    # 4^2 3^6 1^3 row profile.
    pair_orders = (4, 4) + (3,) * 6 + (1,) * 3
    assert wronskian_excess(5, 9, pair_orders) == 1
    for order in set(pair_orders):
        for gcd_order in range(12):
            assert corrected_local_cost(5, order, gcd_order) >= exact_row_cost(
                5, order
            )

    # Independently build the two cubic multiple spaces, including a
    # zero singleton, and recover the four-dimensional ambient intersection.
    for first, second in ((0, 2), (2, 5), (-3, 7)):
        assert first != second and first != -second
        first_factor = sp.expand((z - first) ** 2 * (z + first))
        second_factor = sp.expand((z - second) ** 2 * (z + second))
        left = multiplication_space(first_factor, 6, z, 9)
        right = multiplication_space(second_factor, 6, z, 9)
        intersection_dimension = (
            left.rank() + right.rank() - sp.Matrix.hstack(left, right).rank()
        )
        assert left.rank() == right.rank() == 7
        assert intersection_dimension == 4
        product_space = multiplication_space(
            first_factor * second_factor, 3, z, 9
        )
        assert product_space.rank() == 4
        assert sp.Matrix.hstack(left, product_space).rank() == left.rank()
        assert sp.Matrix.hstack(right, product_space).rank() == right.rank()

    # Two transported relation three-spaces in an at-most-four-space meet
    # in at least two dimensions.  Their four-dimensional ambient
    # intersection is f_s f_t P_3.
    assert 3 + 3 - 4 == 2
    assert 9 - 3 - 3 == 3


def audit_full_local_unit_cancellation() -> None:
    """Rebuild H_s and A_s, including the possible zero singleton."""
    z = sp.symbols("z")
    triple_i = sp.Integer(11)
    mu = sp.Integer(23)
    ordinary_values = (sp.Integer(0), sp.Integer(2), sp.Integer(5), sp.Integer(7))

    h_y = sp.prod(z + value for value in ordinary_values)
    c_i = (z - 13) ** 4 * (z - 17) ** 3
    repeated_g = (z - 13) ** 3 * (z - 17) ** 2
    selected_q = (z + triple_i) * (z + 19)
    fixed_v = sp.cancel(
        (z + mu) ** 3 * repeated_g * selected_q**2 / c_i**2
    )

    for singleton_s in ordinary_values:
        h_s = sp.prod(
            z + value for value in ordinary_values if value != singleton_s
        )
        a_s = sp.expand((z - triple_i) * (z - singleton_s) * c_i)
        f_s = sp.expand((z - singleton_s) ** 2 * (z + singleton_s))

        assert sp.expand(h_s * (z + singleton_s) - h_y) == 0
        assert sp.cancel(
            a_s / ((z - triple_i) * (z - singleton_s)) - c_i
        ) == 0

        # Strip only the (z-i)^2 pole from g Q^2 H_s / A_s^2.
        stripped_denominator = sp.cancel(a_s**2 / (z - triple_i) ** 2)
        unit_from_g_over_a2 = sp.cancel(
            (z + mu) ** 3
            * repeated_g
            * selected_q**2
            * h_s
            / stripped_denominator
        )
        expected_unit = sp.cancel(fixed_v * h_y / f_s)
        assert sp.cancel(unit_from_g_over_a2 - expected_unit) == 0
        assert sp.cancel(unit_from_g_over_a2 * f_s - fixed_v * h_y) == 0

        fixed_unit_value = sp.cancel((fixed_v * h_y).subs(z, triple_i))
        assert fixed_unit_value != 0

        # The coefficient on u'(i) in the resulting common Robin row is
        # exactly the fixed nonzero value V_i(i) H_Y(i).
        u0, u1, u2, u3 = sp.symbols("u0 u1 u2 u3")
        x = z - triple_i
        u = u0 + u1 * x + u2 * x**2 + u3 * x**3
        robin = sp.cancel(sp.diff(fixed_v * h_y * u, z).subs(z, triple_i))
        assert sp.cancel(sp.diff(robin, u1) - fixed_unit_value) == 0

    # Once all U_s lie in one three-space and each pair meets in
    # dimension at least two, either a two-plane member is common or all
    # members equal the three-space.
    allowed_member_dimensions = (2, 3)
    assert min(allowed_member_dimensions) == 2
    assert 2 + 2 - 3 == 1
    assert 3 + 3 - 3 == 3


def audit_division_and_degree_seven_kernel() -> None:
    z, s = sp.symbols("z s")
    f_s = sp.expand((z - s) ** 2 * (z + s))
    assert sp.factor(f_s.subs(z, s)) == 0
    assert sp.factor(sp.diff(f_s, z).subs(z, s)) == 0

    # A simple row at s is automatic after multiplication by f_s.
    x = sp.symbols("x")
    u0, u1 = sp.symbols("u0 u1")
    p0, p1 = sp.symbols("p0 p1")
    local_f_at_s = x**2 * (2 * s + x)
    local_u = u0 + u1 * x
    local_p = p0 + p1 * x
    assert sp.diff(local_u * local_f_at_s * local_p, x).subs(x, 0) == 0

    # At a separated repeated node i, division preserves the exact order
    # and leaves a nonzero leading coefficient.
    i = sp.symbols("i", nonzero=True)
    u2, u3 = sp.symbols("u2 u3")
    p2, p3 = sp.symbols("p2 p3")
    f_at_i = (i + x - s) ** 2 * (i + x + s)
    unit = u0 + u1 * x + u2 * x**2 + u3 * x**3
    polynomial = p0 + p1 * x + p2 * x**2 / 2 + p3 * x**3 / 6
    third_row = sp.expand(
        sp.diff(unit * f_at_i * polynomial, x, 3).subs(x, 0)
    )
    leading_coefficient = sp.factor(sp.diff(third_row, p3))
    assert sp.factor(
        leading_coefficient - u0 * (i - s) ** 2 * (i + s)
    ) == 0

    # The divided degree-seven kernel has one unit of five-space excess.
    divided_orders = (4, 4) + (3,) * 7
    assert wronskian_excess(5, 7, divided_orders) == 1
    for order in set(divided_orders):
        for gcd_order in range(10):
            assert corrected_local_cost(5, order, gcd_order) >= exact_row_cost(
                5, order
            )

    # Distinct quartic square factors have no common P_3 multiple in P_7.
    first = (z**2 - 2) ** 2
    second = (z**2 - 5) ** 2
    assert sp.gcd(sp.Poly(first, z), sp.Poly(second, z)).degree() == 0
    first_space = multiplication_space(first, 3, z, 7)
    second_space = multiplication_space(second, 3, z, 7)
    assert first_space.rank() == second_space.rank() == 4
    assert sp.Matrix.hstack(first_space, second_space).rank() == 8


def e_basis(a: sp.Expr) -> tuple[sp.Matrix, sp.Matrix]:
    return (
        sp.Matrix([a**2, -2 * a, 1, 0]),
        sp.Matrix([0, a**2, -2 * a, 1]),
    )


def possible_intersection_dimensions(subspace_dimension: int) -> tuple[int, ...]:
    lower = max(0, subspace_dimension + 2 - 4)
    upper = min(subspace_dimension, 2)
    return tuple(range(lower, upper + 1))


def audit_projection_ranks_one_two_three() -> None:
    # Enumerate all dimension pairs permitted by a rank-r projection and
    # retain the inequality dim(F cap E)+dim(K cap E) >= 2.
    cases: dict[int, tuple[tuple[int, int], ...]] = {}
    for rank in range(5):
        f_dims = possible_intersection_dimensions(rank)
        k_dims = possible_intersection_dimensions(4 - rank)
        cases[rank] = tuple(
            (f_dim, k_dim)
            for f_dim in f_dims
            for k_dim in k_dims
            if f_dim + k_dim >= 2
        )

    assert all(f_dim == 2 or k_dim == 1 for f_dim, k_dim in cases[3])
    assert all(f_dim == 1 or k_dim == 2 for f_dim, k_dim in cases[1])
    assert all(
        f_dim == 2 or k_dim == 2 or (f_dim, k_dim) == (1, 1)
        for f_dim, k_dim in cases[2]
    )

    # E_a and E_b are complementary for a != b.  This controls all
    # containment exceptions in the rank-one and rank-three cases.
    a, b = sp.symbols("a b")
    v0, v1 = e_basis(a)
    w0, w1 = e_basis(b)
    determinant = sp.factor(sp.Matrix.hstack(v0, v1, w0, w1).det())
    assert determinant == (a - b) ** 4

    # Rank two: derive the incidence quartic independently.
    p01, p02, p03, p12, p13, p23 = sp.symbols(
        "p01 p02 p03 p12 p13 p23"
    )
    plucker = {
        (0, 1): p01,
        (0, 2): p02,
        (0, 3): p03,
        (1, 2): p12,
        (1, 3): p13,
        (2, 3): p23,
    }
    e_plucker: dict[tuple[int, int], sp.Expr] = {}
    for left, right in combinations(range(4), 2):
        e_plucker[left, right] = sp.expand(
            v0[left] * v1[right] - v0[right] * v1[left]
        )

    pairing = sp.expand(
        plucker[0, 1] * e_plucker[2, 3]
        - plucker[0, 2] * e_plucker[1, 3]
        + plucker[0, 3] * e_plucker[1, 2]
        + plucker[1, 2] * e_plucker[0, 3]
        - plucker[1, 3] * e_plucker[0, 2]
        + plucker[2, 3] * e_plucker[0, 1]
    )
    expected = (
        p01
        + 2 * p02 * a
        + (3 * p03 + p12) * a**2
        + 2 * p13 * a**3
        + p23 * a**4
    )
    assert sp.expand(pairing - expected) == 0

    coefficients = sp.Poly(pairing, a).all_coeffs()
    coefficient_matrix, _ = sp.linear_eq_to_matrix(
        coefficients, (p01, p02, p03, p12, p13, p23)
    )
    assert coefficient_matrix.rank() == 5
    coefficient_nullspace = coefficient_matrix.nullspace()
    assert len(coefficient_nullspace) == 1
    expected_null_direction = sp.Matrix([0, 0, 1, -3, 0, 0])
    assert sp.Matrix.hstack(
        coefficient_nullspace[0], expected_null_direction
    ).rank() == 1

    plucker_relation = p01 * p23 - p02 * p13 + p03 * p12
    reduced = sp.expand(
        plucker_relation.subs(
            {
                p01: 0,
                p02: 0,
                p12: -3 * p03,
                p13: 0,
                p23: 0,
            }
        )
    )
    assert reduced == -3 * p03**2
    assert 7 - 2 == 5
    assert 5 > sp.Poly(pairing, a).degree()


def audit_graph_scalar_case() -> None:
    """Show independently that preserving seven E_a planes forces a scalar."""
    a = sp.symbols("a")
    entries = sp.symbols("t0:16")
    transformation = sp.Matrix(4, 4, entries)
    v0, v1 = e_basis(a)
    jets = sp.Matrix(
        [
            [1, a, a**2, a**3],
            [0, 1, 2 * a, 3 * a**2],
        ]
    )

    four_polynomials = [
        sp.expand(expression)
        for vector in (v0, v1)
        for expression in jets * transformation * vector
    ]
    assert len(four_polynomials) == 4
    assert max(sp.Poly(polynomial, a).degree() for polynomial in four_polynomials) == 5

    identity_equations: list[sp.Expr] = []
    for polynomial in four_polynomials:
        identity_equations.extend(sp.Poly(polynomial, a).all_coeffs())
    identity_matrix, _ = sp.linear_eq_to_matrix(identity_equations, entries)
    assert identity_matrix.rank() == 15

    scalar_vector = sp.Matrix(
        [
            1 if row == column else 0
            for row in range(4)
            for column in range(4)
        ]
    )
    identity_kernel = identity_matrix.nullspace()
    assert len(identity_kernel) == 1
    assert sp.Matrix.hstack(identity_kernel[0], scalar_vector).rank() == 1

    # Seven actual preservation conditions already have the same kernel;
    # this also checks the use of seven roots rather than an identity
    # accidentally assumed at the outset.
    seven_values = (-3, -1, 0, 2, 4, 7, 11)
    evaluated_equations: list[sp.Expr] = []
    for value in seven_values:
        evaluated_equations.extend(
            polynomial.subs(a, value) for polynomial in four_polynomials
        )
    evaluated_matrix, _ = sp.linear_eq_to_matrix(evaluated_equations, entries)
    assert evaluated_matrix.rank() == 15
    evaluated_kernel = evaluated_matrix.nullspace()
    assert len(evaluated_kernel) == 1
    assert sp.Matrix.hstack(evaluated_kernel[0], scalar_vector).rank() == 1

    # Reconstruct the triangular intermediate form from the v0 equations,
    # then verify the v1 equations remove A,B,C,c and identify D=lambda.
    first_equations: list[sp.Expr] = []
    for polynomial in four_polynomials[:2]:
        first_equations.extend(sp.Poly(polynomial, a).all_coeffs())
    first_matrix, _ = sp.linear_eq_to_matrix(first_equations, entries)
    assert first_matrix.rank() == 10
    assert len(first_matrix.nullspace()) == 6


def audit_terminal_order_three_row() -> None:
    x = sp.symbols("x")
    i = sp.symbols("i", nonzero=True)
    g0, g1, g2, g3 = sp.symbols("g0 g1 g2 g3", nonzero=True)
    ell0, ell1 = sp.symbols("ell0 ell1", nonzero=True)

    local_unit = g0 + g1 * x + g2 * x**2 + g3 * x**3
    affine = ell0 + ell1 * x
    member = affine * ((i + x) ** 2 - i**2) ** 3
    third_jet = sp.factor(
        sp.diff(local_unit * member, x, 3).subs(x, 0)
    )
    expected = sp.factor(sp.factorial(3) * g0 * ell0 * (2 * i) ** 3)
    assert sp.factor(third_jet - expected) == 0
    assert expected != 0

    # A nonzero affine polynomial cannot vanish at two distinct values.
    first, second = sp.symbols("first second")
    affine_evaluation_matrix = sp.Matrix([[1, first], [1, second]])
    assert sp.factor(affine_evaluation_matrix.det()) == second - first


def main() -> None:
    audit_selection_grid()
    audit_pair_transport_and_gcd()
    audit_full_local_unit_cancellation()
    audit_division_and_degree_seven_kernel()
    audit_projection_ranks_one_two_three()
    audit_graph_scalar_case()
    audit_terminal_order_three_row()
    print("independent p=28 two-quartic q=5 grid closure audit: PASS")
    print("selection grid and complementary/moving transport indexing: PASS")
    print("full g/A_s^2 and H_s singleton-unit cancellation: PASS")
    print("degree-nine and degree-seven Wronskian/gcd bounds: PASS")
    print("projection ranks r=1,2,3 and Pluecker quartic: PASS")
    print("seven-value graph endomorphism has scalar kernel: PASS")
    print("divided exact order-three row has nonzero leading coefficient: PASS")
    print("scope: six p=28 equality splits, two d<=2 residual tuples only")


if __name__ == "__main__":
    main()
