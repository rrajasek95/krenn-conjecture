#!/usr/bin/env python3
"""Exact audit for live-three-zero-fourth-split-layer.md."""

from __future__ import annotations

from itertools import combinations
from math import factorial, prod

import sympy as sp


def permanent_dynamic(matrix: sp.Matrix) -> sp.Expr:
    size = matrix.rows
    assert matrix.cols == size
    values = {0: sp.S.One}
    for row in range(size):
        following: dict[int, sp.Expr] = {}
        for mask, value in values.items():
            for column in range(size):
                if not mask & (1 << column):
                    following[mask | (1 << column)] = (
                        following.get(mask | (1 << column), sp.S.Zero)
                        + value * matrix[row, column]
                    )
        values = following
    return values[(1 << size) - 1]


def audit_repeated_column_expansion() -> int:
    cases = 0
    for p in range(5, 11):
        k = p - 4
        row_factors = [
            sp.Rational(index + 2, index + 3)
            for index in range(p)
        ]
        normalized = sp.Matrix([
            [
                sp.Rational(1, 2 + row + 2 * column)
                for column in range(4)
            ]
            for row in range(p)
        ])
        cofactor = sp.Matrix([
            [
                *[
                    row_factors[row] * normalized[row, column]
                    for column in range(4)
                ],
                *([row_factors[row]] * k),
            ]
            for row in range(p)
        ])
        direct = permanent_dynamic(cofactor)
        split = (
            factorial(k)
            * prod(row_factors)
            * sum(
                permanent_dynamic(normalized.extract(rows, range(4)))
                for rows in combinations(range(p), 4)
            )
        )
        assert direct == split
        cases += 1
    return cases


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


def audit_uniform_double_confluence() -> None:
    # p=6: two repeated exceptional column classes and k=2 common columns.
    row_clusters = [
        (sp.Integer(2), 2),
        (sp.Integer(3), 2),
        (sp.Integer(5), 1),
        (sp.Integer(7), 1),
    ]
    column_clusters = [
        (sp.Integer(11), 2),
        (sp.Integer(13), 2),
        (sp.Integer(17), 2),
    ]
    rows = [
        value
        for value, multiplicity in row_clusters
        for _ in range(multiplicity)
    ]
    columns = [
        value
        for value, multiplicity in column_clusters
        for _ in range(multiplicity)
    ]
    cauchy = sp.Matrix([
        [1 / (row + column) for column in columns]
        for row in rows
    ])
    denominator = hermite_matrix(row_clusters, column_clusters, 1)
    numerator = hermite_matrix(row_clusters, column_clusters, 2)
    assert denominator.det(method="domain-ge") != 0
    assert sp.cancel(
        numerator.det(method="domain-ge")
        / denominator.det(method="domain-ge")
        - permanent_dynamic(cauchy)
    ) == 0


def elementary(values: list[sp.Expr], degree: int) -> sp.Expr:
    return sp.expand(sum(
        sp.prod(values[index] for index in subset)
        for subset in combinations(range(len(values)), degree)
    ))


def audit_multiplicity_four_deletion() -> None:
    values = list(sp.symbols("h0:7", nonzero=True))
    i, j, k = 2, 0, 1

    def deleted_e4(left: int, right: int) -> sp.Expr:
        return elementary(
            [
                value
                for index, value in enumerate(values)
                if index not in {left, right}
            ],
            4,
        )

    remainder = [
        value
        for index, value in enumerate(values)
        if index not in {i, j, k}
    ]
    assert sp.expand(
        deleted_e4(i, j)
        - deleted_e4(i, k)
        - (values[k] - values[j]) * elementary(remainder, 3)
    ) == 0
    for degree in (3, 2, 1):
        deletion_sum = sum(
            elementary(
                [
                    value
                    for offset, value in enumerate(remainder)
                    if offset != omit
                ],
                degree,
            )
            for omit in range(len(remainder))
        )
        assert sp.expand(
            deletion_sum
            - (len(remainder) - degree) * elementary(remainder, degree)
        ) == 0


def partitions(
    total: int,
    maximum: int | None = None,
) -> tuple[tuple[int, ...], ...]:
    if total == 0:
        return ((),)
    if maximum is None:
        maximum = total
    output = []
    for first in range(min(total, maximum), 0, -1):
        for tail in partitions(total - first, first):
            output.append((first, *tail))
    return tuple(output)


def find_two_class_split(
    multiplicities: tuple[int, ...],
) -> tuple[int, ...] | None:
    for left, right in combinations(range(len(multiplicities)), 2):
        for left_count in range(1, min(4, multiplicities[left]) + 1):
            right_count = 4 - left_count
            if not 1 <= right_count <= multiplicities[right]:
                continue
            selected = [0] * len(multiplicities)
            selected[left] = left_count
            selected[right] = right_count
            remaining = [
                multiplicity - used
                for multiplicity, used in zip(multiplicities, selected)
            ]
            if 1 in remaining:
                return tuple(selected)
    return None


def audit_uniform_partition_exhaustion() -> tuple[int, int]:
    profile_count = 0
    two_class_count = 0
    for p in range(5, 19):
        label_count = p + 6
        for multiplicities in partitions(label_count):
            profile_count += 1
            if max(multiplicities) >= 4:
                case = "high"
            elif multiplicities == (1,) * label_count:
                case = "distinct"
            elif all(value == 2 for value in multiplicities):
                assert p % 2 == 0
                case = "all_double"
            elif multiplicities[0] == 2 and multiplicities.count(2) == 1:
                case = "one_double"
            else:
                selected = find_two_class_split(multiplicities)
                assert selected is not None, (p, multiplicities)
                remaining = [
                    multiplicity - used
                    for multiplicity, used in zip(multiplicities, selected)
                ]
                assert sum(remaining) == p + 2
                assert 1 in remaining

                repeated_label_count = sum(
                    value for value in remaining if value >= 2
                )
                # Dual non-top relation: degree <= repeated labels - 2
                # and p column-jet zeros.
                assert repeated_label_count <= p + 1
                assert repeated_label_count - 2 < p

                exceptional_column_classes = sum(
                    value > 0 for value in selected
                )
                assert exceptional_column_classes <= 2
                # Primal relation: degree <= p + m_R - 1 and p+2 roots.
                assert p + exceptional_column_classes - 1 < p + 2
                case = "two_class"
                two_class_count += 1
            assert case in {
                "high",
                "distinct",
                "all_double",
                "one_double",
                "two_class",
            }
    return profile_count, two_class_count


def audit_one_double_residue_and_degrees() -> int:
    degree_cases = 0
    for p in range(5, 19):
        k = p - 4
        denominator_degree = (k + 1) + 3 + 2 + 2
        numerator_degree = denominator_degree - 2
        assert denominator_degree == p + 4
        assert numerator_degree == p + 2
        degree_cases += 1

    b, c, d = sp.symbols("b c d")
    comparison = (
        1 / (b + c)
        - 1 / (b + d)
        - 2 * (1 / (c - b) - 1 / (d - b))
    )
    obstruction = b**2 + 3 * b * (c + d) + c * d
    assert sp.cancel(
        comparison
        - (c - d)
        * obstruction
        / ((b - c) * (b + c) * (b - d) * (b + d))
    ) == 0
    return degree_cases


def audit_all_double_duality() -> int:
    cases = 0
    for p in range(6, 19, 2):
        k = p - 4
        row_denominator_degree = p + 2
        row_numerator_degree = p
        column_zero_count = 2 + 2 + k
        assert row_numerator_degree == column_zero_count

        primal_denominator_degree = (2 + 1) + (2 + 1) + (k + 1)
        primal_numerator_degree = primal_denominator_degree - 2
        assert primal_denominator_degree == p + 3
        assert primal_numerator_degree == p + 1 < p + 2
        cases += 1

    x, b, c = sp.symbols("x b c")
    pair_swap = (
        -2 / (x + b)
        + 2 / (x + c)
        - 2 / (c - x)
        + 2 / (b - x)
    )
    assert sp.cancel(
        pair_swap
        + 4
        * x
        * (b - c)
        * (b + c)
        / ((x - b) * (x + b) * (x - c) * (x + c))
    ) == 0
    return cases


def audit_distinct_quartic_and_degrees() -> int:
    degree_cases = 0
    for p in range(5, 19):
        k = p - 4
        denominator_degree = (k + 1) + 2 * 4
        numerator_degree = denominator_degree - 2
        assert denominator_degree == p + 5
        assert numerator_degree == p + 3
        assert numerator_degree - (p + 2) == 1
        assert p + 3 > 4
        degree_cases += 1

    x, a, b, u, v = sp.symbols("x a b u v")
    y_a = u - (x + 3 * a) / (x**2 - a**2)
    y_b = v - (x + 3 * b) / (x**2 - b**2)
    numerator = sp.Poly(
        sp.together(
            y_b - y_a + (b - a) * y_a * y_b
        ).as_numer_denom()[0],
        x,
    )
    assert numerator.degree() == 4
    assert sp.expand(
        numerator.coeff_monomial(x**3) - (a - b) * (u + v)
    ) == 0
    assert sp.expand(
        numerator.coeff_monomial(x**4)
        - (u * v * (b - a) - u + v)
    ) == 0
    assert sp.expand(
        numerator.as_expr().subs({u: 0, v: 0})
        - 2 * (a - b) * (
            x**2 - (a + b) * x - 3 * a * b
        )
    ) == 0
    assert sp.cancel(
        numerator.as_expr().subs({
            u: -2 / (b - a),
            v: 2 / (b - a),
        })
        + 4 * (a - b) * (
            x**2 + (a + b) * x + 3 * a * b
        )
    ) == 0
    return degree_cases


def main() -> None:
    expansion_cases = audit_repeated_column_expansion()
    audit_uniform_double_confluence()
    audit_multiplicity_four_deletion()
    profile_count, two_class_count = audit_uniform_partition_exhaustion()
    one_double_cases = audit_one_double_residue_and_degrees()
    all_double_cases = audit_all_double_duality()
    distinct_cases = audit_distinct_quartic_and_degrees()
    print("Live three-zero fourth split layer: PASS")
    print(f"repeated-column expansions audited: {expansion_cases}")
    print("simultaneous row/column confluence: exact 6-square")
    print(
        "multiplicity profiles audited: "
        f"{profile_count} total, {two_class_count} initial-jet reductions"
    )
    print(f"one-double degree/residue cases: {one_double_cases}")
    print(f"all-double duality cases: {all_double_cases}")
    print(f"distinct quartic degree cases: {distinct_cases}")


if __name__ == "__main__":
    main()
