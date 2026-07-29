#!/usr/bin/env python3
"""Exact audit for live-three-zero-fifth-split-collision-beta.md."""

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
                    new_mask = mask | (1 << column)
                    following[new_mask] = (
                        following.get(new_mask, sp.S.Zero)
                        + value * matrix[row, column]
                    )
        values = following
    return values[(1 << size) - 1]


def audit_repeated_column_expansion() -> int:
    cases = 0
    for p in range(6, 11):
        k = p - 5
        row_factors = [
            sp.Rational(index + 2, index + 3)
            for index in range(p)
        ]
        normalized = sp.Matrix([
            [
                sp.Rational(1, 2 + row + 2 * column)
                for column in range(5)
            ]
            for row in range(p)
        ])
        cofactor = sp.Matrix([
            [
                *[
                    row_factors[row] * normalized[row, column]
                    for column in range(5)
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
                permanent_dynamic(normalized.extract(rows, range(5)))
                for rows in combinations(range(p), 5)
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


def audit_double_confluence_with_shared_class() -> None:
    # Fifth-split p=7, k=2.  The value 17 occurs on both shores; this
    # stress-tests the partially selected repeated class used below.
    row_clusters = [
        (sp.Integer(2), 2),
        (sp.Integer(3), 2),
        (sp.Integer(5), 2),
        (sp.Integer(17), 1),
    ]
    column_clusters = [
        (sp.Integer(11), 2),
        (sp.Integer(13), 2),
        (sp.Integer(17), 1),
        (sp.Integer(19), 2),
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
    denominator_determinant = denominator.det(method="domain-ge")
    assert denominator_determinant != 0
    assert sp.cancel(
        numerator.det(method="domain-ge") / denominator_determinant
        - permanent_dynamic(cauchy)
    ) == 0


def elementary(values: list[sp.Expr], degree: int) -> sp.Expr:
    return sp.expand(sum(
        sp.prod(values[index] for index in subset)
        for subset in combinations(range(len(values)), degree)
    ))


def audit_deleted_e5_descent() -> None:
    # The smallest fifth-split boundary has |N|=8.
    values = list(sp.symbols("h0:8", nonzero=True))
    i, j, k = 2, 0, 1

    def deleted_e5(left: int, right: int) -> sp.Expr:
        return elementary(
            [
                value
                for index, value in enumerate(values)
                if index not in {left, right}
            ],
            5,
        )

    remainder = [
        value
        for index, value in enumerate(values)
        if index not in {i, j, k}
    ]
    assert sp.expand(
        deleted_e5(i, j)
        - deleted_e5(i, k)
        - (values[k] - values[j]) * elementary(remainder, 4)
    ) == 0

    # Once all one-deletion e_d vanish, their sum kills e_d and
    # e_d(W)=e_d(W\i)+h_i e_{d-1}(W\i) descends one degree.
    witness_set = values[2:]
    for degree in (4, 3, 2, 1):
        deletion_sum = sum(
            elementary(
                [
                    value
                    for offset, value in enumerate(witness_set)
                    if offset != omit
                ],
                degree,
            )
            for omit in range(len(witness_set))
        )
        assert sp.expand(
            deletion_sum
            - (len(witness_set) - degree)
            * elementary(witness_set, degree)
        ) == 0
        for omit, value in enumerate(witness_set):
            deleted = [
                item
                for offset, item in enumerate(witness_set)
                if offset != omit
            ]
            assert sp.expand(
                elementary(witness_set, degree)
                - elementary(deleted, degree)
                - value * elementary(deleted, degree - 1)
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


def find_short_split(
    multiplicities: tuple[int, ...],
) -> tuple[int, ...] | None:
    for left, right in combinations(range(len(multiplicities)), 2):
        for left_count in range(1, min(5, multiplicities[left]) + 1):
            right_count = 5 - left_count
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


def classify_profile(multiplicities: tuple[int, ...]) -> str:
    label_count = sum(multiplicities)
    if max(multiplicities) >= 5:
        return "deleted_e5"
    if multiplicities == (1,) * label_count:
        return "distinct"
    if find_short_split(multiplicities) is not None:
        return "short_two_class"

    triples = multiplicities.count(3)
    if triples == 1 and all(value == 1 for value in multiplicities[1:]):
        return "triple_homogeneous"
    if triples == 1 and all(value == 2 for value in multiplicities[1:]):
        return "triple_homogeneous"

    assert all(value in {1, 2} for value in multiplicities), multiplicities
    doubles = multiplicities.count(2)
    singletons = multiplicities.count(1)
    assert doubles >= 1
    if doubles <= 3:
        assert singletons >= 7
        return "few_doubles_linear"
    if doubles == 4:
        assert singletons >= 2
        return "four_doubles_constant"
    assert doubles >= 5
    return "many_doubles_constant"


def audit_partition_exhaustion() -> tuple[int, dict[str, int]]:
    profile_count = 0
    route_counts: dict[str, int] = {}
    for p in range(6, 25):
        label_count = p + 7
        for multiplicities in partitions(label_count):
            profile_count += 1
            route = classify_profile(multiplicities)
            route_counts[route] = route_counts.get(route, 0) + 1

            if route == "short_two_class":
                selected = find_short_split(multiplicities)
                assert selected is not None
                remaining = [
                    multiplicity - used
                    for multiplicity, used in zip(multiplicities, selected)
                ]
                assert sum(selected) == 5
                assert sum(value > 0 for value in selected) <= 2
                assert sum(remaining) == p + 2
                assert 1 in remaining
                repeated_labels = sum(
                    value for value in remaining if value >= 2
                )
                assert repeated_labels - 2 < p
    return profile_count, route_counts


def audit_primal_degree_bounds() -> int:
    cases = 0
    for p in range(6, 25):
        k = p - 5
        for distinct_r_classes in range(1, 6):
            denominator_degree = (
                5 + distinct_r_classes + (k + 1)
            )
            numerator_degree = denominator_degree - 2
            residual_degree = numerator_degree - (p + 2)
            assert denominator_degree == p + distinct_r_classes + 1
            assert numerator_degree == p + distinct_r_classes - 1
            assert residual_degree == distinct_r_classes - 3
            if distinct_r_classes <= 2:
                assert numerator_degree < p + 2
            elif distinct_r_classes == 3:
                assert residual_degree == 0
            elif distinct_r_classes == 4:
                assert residual_degree == 1
            cases += 1
    return cases


def audit_singleton_jet_degree() -> int:
    cases = 0
    for p in range(6, 25):
        # A singleton among p+2 rows leaves at most p+1 labels in
        # repeated classes.  The non-top dual numerator is two degrees
        # below that repeated-label denominator and has p column zeros.
        for repeated_labels in range(p + 2):
            numerator_bound = repeated_labels - 2
            assert numerator_bound < p
            cases += 1
    return cases


def audit_constant_moving_class() -> None:
    a, x, u = sp.symbols("a x u")
    for selected_count in (1, 2):
        moving = (
            selected_count / (a + x)
            - (selected_count + 1) / (x - a)
        )
        compact = -(x + (2 * selected_count + 1) * a) / (x**2 - a**2)
        assert sp.cancel(moving - compact) == 0
        cleared = sp.Poly(
            sp.cancel((u + moving) * (x**2 - a**2)),
            x,
        )
        assert cleared.degree() <= 2
        assert cleared.coeff_monomial(x) == -1


def audit_linear_moving_quartic() -> None:
    x, a, b, u, v = sp.symbols("x a b u v")

    def psi(anchor: sp.Expr) -> sp.Expr:
        return -(x + 3 * anchor) / (x**2 - anchor**2)

    y_a = u + psi(a)
    y_b = v + psi(b)
    determinant = y_b - y_a + (b - a) * y_a * y_b
    numerator = sp.Poly(sp.together(determinant).as_numer_denom()[0], x)
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


def audit_route_cardinalities() -> int:
    cases = 0
    for p in range(6, 25):
        label_count = p + 7
        for doubles in range((label_count // 2) + 1):
            singletons = label_count - 2 * doubles
            if singletons < 0:
                continue
            if doubles == 0:
                continue
            if doubles <= 3:
                assert singletons >= 7
                # Two fixed singleton anchors and at least five movers.
                assert singletons - 2 >= 5
                # R=(2,1,1,1); at least one singleton remains in N.
                assert singletons - 3 >= 1
            elif doubles == 4:
                # A singleton anchor, one fixed double, three moving doubles.
                assert singletons >= 5
                assert doubles - 1 == 3
                # R=(2,2,1); unselected singleton classes remain in N.
                assert singletons - 1 >= 1
            else:
                # A partially selected double anchor, one fixed double,
                # and at least three moving double classes.
                assert doubles - 2 >= 3
                # R=(2,2,1); the second anchor copy is a singleton in N.
            cases += 1
    return cases


def audit_triple_route_cardinalities() -> int:
    cases = 0
    for p in range(6, 25):
        remainder_labels = p + 4
        # Triple plus singleton classes.
        assert remainder_labels >= 10
        assert remainder_labels - 1 >= 3
        # R=(3,1,1), and many untouched singleton classes remain.
        assert remainder_labels - 2 >= 1
        cases += 1

        # Triple plus double classes exists only at the matching parity.
        if remainder_labels % 2 == 0:
            double_classes = remainder_labels // 2
            assert double_classes >= 5
            assert double_classes - 1 >= 3
            # The selected anchor and moving classes each leave one copy.
            cases += 1
    return cases


def main() -> None:
    expansion_cases = audit_repeated_column_expansion()
    audit_double_confluence_with_shared_class()
    audit_deleted_e5_descent()
    profile_count, route_counts = audit_partition_exhaustion()
    degree_cases = audit_primal_degree_bounds()
    singleton_degree_cases = audit_singleton_jet_degree()
    audit_constant_moving_class()
    audit_linear_moving_quartic()
    cardinality_cases = audit_route_cardinalities()
    triple_cardinality_cases = audit_triple_route_cardinalities()

    print("Live three-zero fifth-split collision beta: PASS")
    print(f"repeated-column expansions audited: {expansion_cases}")
    print("double confluence with a row/column shared value: exact")
    print("deleted-e5 descent: exact")
    print(f"multiplicity profiles audited: {profile_count}")
    for route, count in sorted(route_counts.items()):
        print(f"  {route}: {count}")
    print(f"primal degree cases: {degree_cases}")
    print(f"singleton non-top dual degree cases: {singleton_degree_cases}")
    print("one- and two-label moving-class equations: nonzero quadratics")
    print("few-double linear residual: nonzero quartic")
    print(f"route cardinality cases: {cardinality_cases}")
    print(f"triple-route cardinality cases: {triple_cardinality_cases}")


if __name__ == "__main__":
    main()
