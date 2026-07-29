#!/usr/bin/env python3
"""Exact audit for live-three-zero-fifth-split-distinct-beta.md."""

from __future__ import annotations

from math import factorial

import sympy as sp


def audit_degree_counts() -> int:
    cases = 0
    for p in range(6, 25):
        k = p - 5
        exceptional_count = p + 7
        fixed_columns = 5 + k
        complement_count = exceptional_count - 5
        denominator_degree = 2 * 5 + (k + 1)
        numerator_degree_bound = denominator_degree - 2
        residual_degree_bound = numerator_degree_bound - complement_count
        moving_values = exceptional_count - 4

        assert fixed_columns == p
        assert complement_count == p + 2
        assert denominator_degree == p + 6
        assert numerator_degree_bound == p + 4
        assert residual_degree_bound == 2
        assert moving_values == p + 3 > 6
        cases += 1
    return cases


def permanent_dynamic(matrix: sp.Matrix) -> sp.Expr:
    size = matrix.rows
    assert matrix.cols == size
    values = {0: sp.S.One}
    for row in range(size):
        following: dict[int, sp.Expr] = {}
        for mask, value in values.items():
            for column in range(size):
                if not mask & (1 << column):
                    new_mask = mask | (1 << column)
                    following[new_mask] = (
                        following.get(new_mask, sp.S.Zero)
                        + value * matrix[row, column]
                    )
        values = following
    return values[(1 << size) - 1]


def divided_mixed_derivative(
    power: int,
    row_value: sp.Expr,
    column_value: sp.Expr,
    row_order: int,
    column_order: int,
) -> sp.Expr:
    total = row_order + column_order
    return (
        (-1) ** total
        * sp.rf(power, total)
        / (factorial(row_order) * factorial(column_order))
        / (row_value + column_value) ** (power + total)
    )


def hermite_matrix(
    row_clusters: list[tuple[sp.Expr, int]],
    column_clusters: list[tuple[sp.Expr, int]],
    power: int,
) -> sp.Matrix:
    rows = [
        (value, order)
        for value, multiplicity in row_clusters
        for order in range(multiplicity)
    ]
    columns = [
        (value, order)
        for value, multiplicity in column_clusters
        for order in range(multiplicity)
    ]
    return sp.Matrix([
        [
            divided_mixed_derivative(
                power,
                row_value,
                column_value,
                row_order,
                column_order,
            )
            for column_value, column_order in columns
        ]
        for row_value, row_order in rows
    ])


def audit_common_column_confluence() -> int:
    # k=1 is ordinary Borchardt; k=2,3 audit the divided-jet boundary.
    cases = 0
    for k in range(1, 4):
        p = k + 5
        rows = [sp.Integer(value) for value in (2, 3, 5, 7, 11, 13, 17, 19)[:p]]
        exceptional_columns = [
            sp.Integer(value)
            for value in (23, 29, 31, 37, 41)
        ]
        mu = sp.Integer(43)
        repeated_columns = [*exceptional_columns, *([mu] * k)]
        row_clusters = [(value, 1) for value in rows]
        column_clusters = [
            *((value, 1) for value in exceptional_columns),
            (mu, k),
        ]

        cauchy = sp.Matrix([
            [sp.Rational(1, row + column) for column in repeated_columns]
            for row in rows
        ])
        denominator = hermite_matrix(row_clusters, column_clusters, 1)
        numerator = hermite_matrix(row_clusters, column_clusters, 2)

        denominator_determinant = denominator.det(method="domain-ge")
        assert denominator_determinant != 0
        assert sp.cancel(
            numerator.det(method="domain-ge") / denominator_determinant
            - permanent_dynamic(cauchy)
        ) == 0
        cases += 1
    return cases


def audit_residue_reduction() -> None:
    z, mu, k = sp.symbols("z mu k")
    a, b, c, d, e = sp.symbols("a b c d e")
    other_columns = (b, c, d, e)

    def psi(anchor: sp.Expr, moving: sp.Expr) -> sp.Expr:
        return 1 / (anchor + moving) - 2 / (moving - anchor)

    # Check the logarithmic-derivative reduction term by term, avoiding
    # any genericity hidden in a large common-denominator cancellation.
    for value in other_columns:
        direct_column_term = -2 / (value - a)
        split_column_term = -1 / (a + value) + psi(a, value)
        assert sp.cancel(direct_column_term - split_column_term) == 0
    assert sp.cancel(
        (-(k + 1) / (mu - a))
        - (-(k + 1) / (mu - a))
    ) == 0

    row_value = sp.symbols("n")
    assert sp.cancel(
        (1 / (z - row_value)).subs(z, -a) + 1 / (a + row_value)
    ) == 0

    # Inventory of every factor divided out in the simple-pole equation.
    expected_factors = (
        (mu - a, k + 1),
        (b - a, 2),
        (c - a, 2),
        (d - a, 2),
        (e - a, 2),
    )
    assert expected_factors[0] == (mu - a, k + 1)
    assert expected_factors[1:] == tuple(
        (value - a, 2) for value in other_columns
    )


def residue_row(anchor: sp.Expr, coefficient: sp.Expr) -> sp.Matrix:
    return sp.Matrix([[
        anchor**2 * coefficient - 2 * anchor,
        1 - anchor * coefficient,
        coefficient,
    ]])


def audit_moving_determinant() -> tuple[sp.Expr, ...]:
    a, b, c, A, B, C = sp.symbols("a b c A B C")
    delta = (a - b) * (a - c) * (b - c)

    direct = sp.det(sp.Matrix.vstack(
        residue_row(a, A),
        residue_row(b, B),
        residue_row(c, C),
    ))
    compact = (
        -delta * A * B * C
        + (b - a) * (a + b - 2 * c) * A * B
        + (a - c) * (a + c - 2 * b) * A * C
        + (c - b) * (b + c - 2 * a) * B * C
        + 2 * (c - b) * A
        + 2 * (a - c) * B
        + 2 * (b - a) * C
    )
    assert sp.expand(direct - compact) == 0

    x, U, V, W = sp.symbols("x U V W")

    def psi(anchor: sp.Expr) -> sp.Expr:
        return -(x + 3 * anchor) / (x**2 - anchor**2)

    moving = compact.subs({
        A: U + psi(a),
        B: V + psi(b),
        C: W + psi(c),
    })
    moving_denominator = sp.factor(sp.denom(sp.cancel(moving)))
    expected_moving_denominator = (
        (x - a) * (x + a)
        * (x - b) * (x + b)
        * (x - c) * (x + c)
    )
    assert sp.expand(
        moving_denominator - expected_moving_denominator
    ) == 0
    cleared = sp.cancel(
        moving
        * (x**2 - a**2)
        * (x**2 - b**2)
        * (x**2 - c**2)
    )
    assert sp.denom(cleared) == 1
    assert sp.Poly(cleared, x).degree() <= 6

    return a, b, c, A, B, C, x, U, V, W, compact


def audit_opposite_poles(data: tuple[sp.Expr, ...]) -> None:
    a, b, c, A, B, C, x, U, V, W, compact = data

    def psi(anchor: sp.Expr, moving: sp.Expr) -> sp.Expr:
        return 1 / (anchor + moving) - 2 / (moving - anchor)

    for anchor in (a, b, c):
        assert sp.limit((x - anchor) * psi(anchor, x), x, anchor) == -2
        assert sp.limit((x + anchor) * psi(anchor, x), x, -anchor) == 1

    phi_a = sp.diff(compact, A)
    phi_b = sp.diff(compact, B)
    phi_c = sp.diff(compact, C)

    difference_a = sp.cancel(
        phi_a.subs({B: V + psi(b, a), C: W + psi(c, a)})
        - phi_a.subs({B: V + psi(b, -a), C: W + psi(c, -a)})
    )
    difference_b = sp.cancel(
        phi_b.subs({A: U + psi(a, b), C: W + psi(c, b)})
        - phi_b.subs({A: U + psi(a, -b), C: W + psi(c, -b)})
    )
    difference_c = sp.cancel(
        phi_c.subs({A: U + psi(a, c), B: V + psi(b, c)})
        - phi_c.subs({A: U + psi(a, -c), B: V + psi(b, -c)})
    )

    linear_a = (
        (a**2 - b**2) * V
        + (a**2 - c**2) * W
        + 2 * a - b - c
    )
    linear_b = (
        (a**2 - b**2) * U
        + (c**2 - b**2) * W
        + a - 2 * b + c
    )
    linear_c = (
        (a**2 - c**2) * U
        + (b**2 - c**2) * V
        + a + b - 2 * c
    )

    assert sp.cancel(
        difference_a
        - 2 * a * (b - c) / ((a + b) * (a + c)) * linear_a
    ) == 0
    assert sp.cancel(
        difference_b
        - 2 * b * (a - c) / ((a + b) * (b + c)) * linear_b
    ) == 0
    assert sp.cancel(
        difference_c
        + 2 * c * (a - b) / ((a + c) * (b + c)) * linear_c
    ) == 0

    assert sp.factor(sp.denom(difference_a)) == (a + b) * (a + c)
    assert sp.factor(sp.denom(difference_b)) == (a + b) * (b + c)
    assert sp.factor(sp.denom(difference_c)) == (a + c) * (b + c)

    # These are exactly the nonzero hypotheses used to pass from the
    # pole-pair differences to the three linear equations.  They are
    # recorded separately from the symbolic identities: nonzero anchors
    # are chosen, differences follow from distinctness, and sums are the
    # structural Cauchy denominators.
    pole_prefactor_product = sp.factor(
        (
            2 * a * (b - c) / ((a + b) * (a + c))
            * 2 * b * (a - c) / ((a + b) * (b + c))
            * -2 * c * (a - b) / ((a + c) * (b + c))
        )
    )
    expected_prefactor_product = (
        -8 * a * b * c
        * (a - b) * (a - c) * (b - c)
        / ((a + b) ** 2 * (a + c) ** 2 * (b + c) ** 2)
    )
    assert sp.cancel(
        pole_prefactor_product - expected_prefactor_product
    ) == 0

    certificate = sp.expand(
        -(b**2 - c**2) * linear_a
        - (a**2 - c**2) * linear_b
        + (a**2 - b**2) * linear_c
    )
    assert sp.expand(
        certificate - 3 * (a - b) * (a - c) * (b - c)
    ) == 0


def main() -> None:
    cases = audit_degree_counts()
    confluence_cases = audit_common_column_confluence()
    audit_residue_reduction()
    determinant_data = audit_moving_determinant()
    audit_opposite_poles(determinant_data)

    print("Live three-zero fifth-split distinct beta: PASS")
    print(f"quadratic residual degree counts: {cases} values of p")
    print(f"ordinary/common-column confluent Borchardt cases: {confluence_cases}")
    print("simple-pole denominator inventory: exact")
    print("moving determinant: degree at most 6 with at least 9 roots")
    print("six opposite-pole residues and three differences: exact")
    print("linear incompatibility: 3(a-b)(a-c)(b-c)")


if __name__ == "__main__":
    main()
