#!/usr/bin/env python3
"""Exact audit for live-three-zero-third-split-collision-beta.md."""

from __future__ import annotations

from itertools import combinations
from math import factorial

import sympy as sp


def permanent_dynamic(matrix: sp.Matrix) -> sp.Expr:
    """Subset dynamic program for an exact square permanent."""
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
    kernel_power: int,
    row_value: sp.Expr,
    column_value: sp.Expr,
    row_order: int,
    column_order: int,
) -> sp.Expr:
    """Divided x/y derivative of (x+y)^(-kernel_power)."""
    total_order = row_order + column_order
    coefficient = (
        (-1) ** total_order
        * sp.rf(kernel_power, total_order)
        / (factorial(row_order) * factorial(column_order))
    )
    return coefficient / (row_value + column_value) ** (
        kernel_power + total_order
    )


def hermite_matrix(
    row_clusters: list[tuple[sp.Expr, int]],
    column_clusters: list[tuple[sp.Expr, int]],
    kernel_power: int,
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
                kernel_power,
                row_value,
                column_value,
                row_order,
                column_order,
            )
            for column_value, column_order in columns
        ]
        for row_value, row_order in rows
    ])


def audit_double_confluent_borchardt() -> None:
    row_clusters = [
        (sp.Integer(2), 2),
        (sp.Integer(3), 1),
        (sp.Integer(5), 1),
        (sp.Integer(7), 1),
    ]
    column_clusters = [
        (sp.Integer(11), 1),
        (sp.Integer(13), 1),
        (sp.Integer(17), 1),
        (sp.Integer(19), 2),
    ]
    repeated_rows = [
        value
        for value, multiplicity in row_clusters
        for _ in range(multiplicity)
    ]
    repeated_columns = [
        value
        for value, multiplicity in column_clusters
        for _ in range(multiplicity)
    ]
    cauchy = sp.Matrix([
        [1 / (row + column) for column in repeated_columns]
        for row in repeated_rows
    ])
    denominator = hermite_matrix(row_clusters, column_clusters, 1)
    numerator = hermite_matrix(row_clusters, column_clusters, 2)
    assert denominator.det(method="domain-ge") != 0
    quotient = sp.cancel(
        numerator.det(method="domain-ge")
        / denominator.det(method="domain-ge")
    )
    assert sp.cancel(quotient - permanent_dynamic(cauchy)) == 0


def elementary(values: list[sp.Expr], degree: int) -> sp.Expr:
    return sp.expand(sum(
        sp.prod(values[index] for index in subset)
        for subset in combinations(range(len(values)), degree)
    ))


def audit_high_multiplicity_lemma() -> None:
    values = list(sp.symbols("h0:6", nonzero=True))
    i, j, k = 2, 0, 1

    def deleted_e3(left: int, right: int) -> sp.Expr:
        remaining = [
            value
            for index, value in enumerate(values)
            if index not in {left, right}
        ]
        return elementary(remaining, 3)

    remainder = [
        value
        for index, value in enumerate(values)
        if index not in {i, j, k}
    ]
    difference = deleted_e3(i, j) - deleted_e3(i, k)
    assert sp.expand(difference - (values[k] - values[j]) * elementary(remainder, 2)) == 0

    total_pair_sum = sum(
        elementary([value for offset, value in enumerate(remainder) if offset != omit], 2)
        for omit in range(len(remainder))
    )
    assert sp.expand(
        total_pair_sum - (len(remainder) - 2) * elementary(remainder, 2)
    ) == 0


def audit_deleted_pair_plucker_duality() -> None:
    """Exact complementary-minor audit for a 7-by-5 full-rank matrix."""
    matrix = sp.Matrix([
        [sp.Integer(row + 2) ** column for column in range(5)]
        for row in range(7)
    ])
    kernel_basis = matrix.T.nullspace()
    assert len(kernel_basis) == 2
    kernel = sp.Matrix.hstack(*kernel_basis)
    signed_ratios: set[sp.Expr] = set()
    for left, right in combinations(range(7), 2):
        complement = [
            row for row in range(7) if row not in {left, right}
        ]
        deleted_pair_minor = matrix.extract(complement, range(5)).det()
        plucker_coordinate = kernel.extract(
            [left, right],
            range(2),
        ).det()
        assert plucker_coordinate != 0
        signed_ratios.add(sp.cancel(
            (-1) ** (left + right)
            * deleted_pair_minor
            / plucker_coordinate
        ))
    assert len(signed_ratios) == 1


def find_five_class_pattern(double_count: int, class_count: int, threshold: int) -> tuple[int, int, int, int, int]:
    """Find a,b,c,d,e for which each {a,b,x} hits threshold doubles."""
    classes = range(class_count)
    doubles = set(range(double_count))
    for a, b in combinations(classes, 2):
        remaining = [value for value in classes if value not in {a, b}]
        for c, d, e in combinations(remaining, 3):
            if all(
                len({a, b, variable} & doubles) >= threshold
                for variable in (c, d, e)
            ):
                return a, b, c, d, e
    raise AssertionError(
        (double_count, class_count, threshold),
    )


def audit_good_triples_and_vandermonde() -> int:
    profiles = 0
    for p in range(5, 17):
        total_labels = p + 5
        common_column_count = p - 3
        for double_count in range(total_labels // 2 + 1):
            singleton_count = total_labels - 2 * double_count
            class_count = double_count + singleton_count
            if class_count < 5:
                continue
            threshold = max(0, 8 - class_count)
            pattern = find_five_class_pattern(
                double_count,
                class_count,
                threshold,
            )
            a, b, *variables = pattern
            doubles = set(range(double_count))
            for variable in variables:
                hits = len({a, b, variable} & doubles)
                remaining_doubles = double_count - hits
                assert remaining_doubles <= common_column_count

                if remaining_doubles:
                    nodes = [sp.Integer(index + 2) for index in range(remaining_doubles)]
                    mu = sp.Integer(101)
                    powers = sp.Matrix([
                        [
                            (-1) ** order
                            * (order + 1)
                            / (node + mu) ** (order + 2)
                            for order in range(common_column_count)
                        ]
                        for node in nodes
                    ])
                    assert powers.rank() == remaining_doubles
            profiles += 1
    return profiles


def audit_residue_comparison() -> None:
    a, c, d = sp.symbols("a c d")
    comparison = (
        1 / (a + c)
        - 1 / (a + d)
        - 2 * (1 / (c - a) - 1 / (d - a))
    )
    mobius_equation = (
        (c - a) * (d - a)
        - 2 * (a + c) * (a + d)
    )
    assert sp.cancel(
        comparison
        - (c - d)
        * (a**2 + 3 * a * (c + d) + c * d)
        / ((a - c) * (a + c) * (a - d) * (a + d))
    ) == 0
    assert sp.expand(mobius_equation + a**2 + 3 * a * (c + d) + c * d) == 0


def main() -> None:
    audit_double_confluent_borchardt()
    audit_high_multiplicity_lemma()
    audit_deleted_pair_plucker_duality()
    profile_count = audit_good_triples_and_vandermonde()
    audit_residue_comparison()
    print("Live three-zero third split, collision beta: PASS")
    print("double-confluent Borchardt quotient: exact 5-square")
    print("multiplicity-at-least-three symmetric lemma: exact")
    print("deleted-pair/left-kernel Plucker duality: exact")
    print(f"single/double multiplicity profiles audited: {profile_count}")
    print("initial-jet base block: exact Vandermonde rank")
    print("repeated-multiset residue comparison: exact")


if __name__ == "__main__":
    main()
