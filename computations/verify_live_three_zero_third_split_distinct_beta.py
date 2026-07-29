#!/usr/bin/env python3
"""Exact audit for live-three-zero-third-split-distinct-beta.md."""

from __future__ import annotations

from itertools import combinations
from math import factorial, prod

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


def audit_repeated_column_expansion() -> int:
    cases = 0
    for p in range(4, 10):
        k = p - 3
        # Exact rational entries avoid symbolic expansion while checking
        # the uniform Laplace formula for all tested sizes.
        row_factors = [sp.Rational(index + 2, index + 3) for index in range(p)]
        normalized = sp.Matrix([
            [sp.Rational(1, 2 + row + 2 * column) for column in range(3)]
            for row in range(p)
        ])
        cofactor = sp.Matrix([
            [row_factors[row] * normalized[row, column] for column in range(3)]
            + [row_factors[row]] * k
            for row in range(p)
        ])
        direct = permanent_dynamic(cofactor)
        split = (
            factorial(k)
            * prod(row_factors)
            * sum(
                permanent_dynamic(normalized.extract(rows, range(3)))
                for rows in combinations(range(p), 3)
            )
        )
        assert direct == split
        cases += 1
    return cases


def audit_confluent_borchardt() -> None:
    """Five-square exact collision of two common-beta columns."""
    epsilon = sp.Symbol("epsilon")
    rows = tuple(map(sp.Integer, (2, 3, 5, 7, 11)))
    exceptional_columns = tuple(map(sp.Integer, (13, 17, 19)))
    mu = sp.Integer(23)
    columns = (*exceptional_columns, mu, mu + epsilon)
    cauchy = sp.Matrix([
        [1 / (row + column) for column in columns]
        for row in rows
    ])
    squared = cauchy.applyfunc(lambda value: value**2)
    borchardt = sp.cancel(squared.det(method="domain-ge") / cauchy.det(method="domain-ge"))
    ordinary = permanent_dynamic(cauchy)
    assert sp.cancel(borchardt - ordinary) == 0

    repeated = sp.Matrix([
        [1 / (row + column) for column in (*exceptional_columns, mu, mu)]
        for row in rows
    ])
    denominator_confluent = sp.Matrix([
        [
            *[1 / (row + column) for column in exceptional_columns],
            1 / (row + mu),
            -1 / (row + mu) ** 2,
        ]
        for row in rows
    ])
    numerator_confluent = sp.Matrix([
        [
            *[1 / (row + column) ** 2 for column in exceptional_columns],
            1 / (row + mu) ** 2,
            -2 / (row + mu) ** 3,
        ]
        for row in rows
    ])
    quotient = sp.cancel(
        numerator_confluent.det(method="domain-ge")
        / denominator_confluent.det(method="domain-ge")
    )
    assert sp.cancel(quotient - permanent_dynamic(repeated)) == 0
    assert sp.cancel(sp.limit(borchardt, epsilon, 0) - quotient) == 0


def audit_degree_and_residue_identity() -> int:
    cases = 0
    for p in range(4, 13):
        k = p - 3
        denominator_degree = (k + 1) + 2 * 3
        numerator_degree_bound = denominator_degree - 2
        number_of_evaluation_nodes = p + 2
        assert denominator_degree == p + 4
        assert numerator_degree_bound == number_of_evaluation_nodes
        cases += 1

    a, c, d = sp.symbols("a c d")
    residue_difference = (
        1 / (a + c)
        - 1 / (a + d)
        - 2 * (1 / (c - a) - 1 / (d - a))
    )
    obstruction = a**2 + 3 * a * (c + d) + c * d
    expected = (
        (c - d)
        * obstruction
        / ((a - c) * (a + c) * (a - d) * (a + d))
    )
    assert sp.cancel(residue_difference - expected) == 0

    mobius_product = (c - a) * (d - a) / ((c + a) * (d + a))
    assert sp.cancel(mobius_product - 2 + obstruction / ((a + c) * (a + d))) == 0
    return cases


def main() -> None:
    expansion_cases = audit_repeated_column_expansion()
    audit_confluent_borchardt()
    degree_cases = audit_degree_and_residue_identity()
    print("Live three-zero third split, distinct beta: PASS")
    print(f"repeated-column permanent expansions audited: {expansion_cases}")
    print("five-square Borchardt collision and Hermite quotient: exact")
    print(f"degree/residue cases audited: {degree_cases}")
    print("residue comparison obstruction: a^2 + 3a(c+d) + cd")


if __name__ == "__main__":
    main()
