#!/usr/bin/env python3
"""Exact audit for live-three-zero-all-exceptional-eleven-live.md."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import factorial, prod

import sympy as sp


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    return tuple(
        ((first, vertices[position]),) + tail
        for position in range(1, len(vertices))
        for tail in perfect_matchings(
            vertices[1:position] + vertices[position + 1 :]
        )
    )


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


def coupled_incidence_rank(modulus: int = 1009) -> tuple[int, int, int]:
    """Modular diagnostic for disjoint unordered four-set variables."""
    points = tuple(range(11))
    four_sets = tuple(combinations(points, 4))
    four_index = {subset: index for index, subset in enumerate(four_sets)}
    variables = tuple(
        (left_index, right_index)
        for left_index, left in enumerate(four_sets)
        for right_index in range(left_index + 1, len(four_sets))
        if set(left).isdisjoint(four_sets[right_index])
    )
    variable_index = {variable: index for index, variable in enumerate(variables)}

    def variable(left_index: int, right_index: int) -> int:
        pair = (
            (left_index, right_index)
            if left_index < right_index
            else (right_index, left_index)
        )
        return variable_index[pair]

    basis: dict[int, dict[int, int]] = {}
    row_count = 0
    for right_index, right in enumerate(four_sets):
        complement = tuple(point for point in points if point not in right)
        for marked_pair in combinations(complement, 2):
            left_pool = tuple(
                point for point in complement if point not in marked_pair
            )
            row = {
                variable(four_index[left], right_index): 1
                for left in combinations(left_pool, 4)
            }
            row_count += 1
            while row:
                pivot = min(row)
                pivot_value = row[pivot]
                if pivot not in basis:
                    inverse = pow(pivot_value, -1, modulus)
                    basis[pivot] = {
                        column: value * inverse % modulus
                        for column, value in row.items()
                        if value % modulus
                    }
                    break
                pivot_row = basis[pivot]
                for column, value in pivot_row.items():
                    updated = (
                        row.get(column, 0) - pivot_value * value
                    ) % modulus
                    if updated:
                        row[column] = updated
                    elif column in row:
                        del row[column]
    return row_count, len(variables), len(basis)


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


def audit_double_confluent_borchardt() -> None:
    row_clusters = [
        (sp.Integer(2), 2),
        (sp.Integer(3), 1),
        (sp.Integer(5), 1),
        (sp.Integer(7), 1),
    ]
    column_clusters = [
        (sp.Integer(11), 2),
        (sp.Integer(13), 2),
        (sp.Integer(17), 1),
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


def audit_multiplicity_four_lemma() -> None:
    values = list(sp.symbols("h0:7", nonzero=True))
    i, j, k = 2, 0, 1

    def deleted_e4(left: int, right: int) -> sp.Expr:
        remaining = [
            value
            for index, value in enumerate(values)
            if index not in {left, right}
        ]
        return elementary(remaining, 4)

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

    # Audit the descent
    # e_q(W\i)=0 => e_q(W)=0 => e_{q-1}(W\i)=0.
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
    for selected in product(*[range(value + 1) for value in multiplicities]):
        if sum(selected) != 4:
            continue
        if sum(value > 0 for value in selected) > 2:
            continue
        remaining = [
            multiplicity - used
            for multiplicity, used in zip(multiplicities, selected)
        ]
        if 1 in remaining:
            return selected
    return None


def audit_collision_partition_reduction() -> int:
    checked = 0
    exceptional_one_double = (2, *([1] * 9))
    for multiplicities in partitions(11, 3):
        if multiplicities == (1,) * 11:
            continue
        if multiplicities == exceptional_one_double:
            continue
        selected = find_two_class_split(multiplicities)
        assert selected is not None, multiplicities
        remaining = [
            multiplicity - used
            for multiplicity, used in zip(multiplicities, selected)
        ]
        assert sum(remaining) == 7
        assert 1 in remaining

        # The non-top-row dual has denominator degree equal to the
        # number of labels in repeated classes of N.
        repeated_label_count = sum(value for value in remaining if value >= 2)
        assert repeated_label_count <= 6
        dual_numerator_degree = repeated_label_count - 2
        assert dual_numerator_degree < 5

        # At most two exceptional column classes plus the common column:
        # the primal numerator degree is at most p+1=6, below seven roots.
        column_class_count = sum(value > 0 for value in selected)
        assert column_class_count <= 2
        primal_numerator_degree = 5 + column_class_count - 1
        assert primal_numerator_degree < 7
        checked += 1
    return checked


def audit_one_double_residue() -> None:
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


def audit_distinct_quartic_obstruction() -> None:
    x, a, b, u, v = sp.symbols("x a b u v")
    psi_a = -(x + 3 * a) / (x**2 - a**2)
    psi_b = -(x + 3 * b) / (x**2 - b**2)
    y_a = u + psi_a
    y_b = v + psi_b
    determinant = y_b - y_a + (b - a) * y_a * y_b
    numerator = sp.Poly(
        sp.together(determinant).as_numer_denom()[0],
        x,
    )
    assert numerator.degree() == 4
    assert sp.factor(numerator.coeff_monomial(x**3)) == (a - b) * (u + v)
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
    special = sp.factor(
        numerator.as_expr().subs({
            u: -2 / (b - a),
            v: 2 / (b - a),
        })
    )
    assert sp.cancel(
        special
        + 4 * (a - b) * (
            x**2 + (a + b) * x + 3 * a * b
        )
    ) == 0


def audit_permanental_descent() -> None:
    triples = tuple(combinations(range(7), 3))
    four_sets = tuple(combinations(range(7), 4))
    inclusion = sp.Matrix([
        [int(set(triple).issubset(four_set)) for triple in triples]
        for four_set in four_sets
    ])
    assert inclusion.shape == (35, 35)
    assert inclusion.rank() == 35

    pairs = tuple(combinations(range(7), 2))
    triple_pair_inclusion = sp.Matrix([
        [int(set(pair).issubset(triple)) for pair in pairs]
        for triple in triples
    ])
    assert triple_pair_inclusion.rank() == len(pairs)


def audit_complete_selected_response() -> None:
    exceptional_sites = tuple(range(11))
    centres = (11, 12)
    columns = [(site, colour) for colour in range(3) for site in centres]
    column_index = {column: index for index, column in enumerate(columns)}
    hessian = (
        (Fraction(0), Fraction(1), Fraction(2)),
        (Fraction(1), Fraction(0), Fraction(3)),
        (Fraction(2), Fraction(3), Fraction(0)),
    )
    betas = tuple(map(Fraction, (*range(2, 13), 1, 1)))

    def p_entry(site: int, colour: int, source: int) -> int:
        return int(colour == source and (site < 11 or source < 2))

    def edge(word: tuple[int, ...], left: int, right: int) -> Fraction:
        if left in centres and word[left] == 2:
            return Fraction(0)
        if right in centres and word[right] == 2:
            return Fraction(0)
        return hessian[word[left]][word[right]] / (
            betas[left] + betas[right]
        )

    @lru_cache(maxsize=None)
    def hafnian(word: tuple[int, ...], vertices: tuple[int, ...]) -> Fraction:
        return sum(
            (
                prod(edge(word, left, right) for left, right in matching)
                for matching in perfect_matchings(vertices)
            ),
            Fraction(0),
        )

    def response_row(
        word: tuple[int, ...],
        source_left: int,
        source_right: int,
        include_direct: bool = True,
    ) -> list[Fraction]:
        row = [Fraction(0)] * 6
        direct_weight = (
            Fraction(1, 2)
            if include_direct
            and source_left != source_right
            and {source_left, source_right} == {0, 1}
            else Fraction(0)
        )
        if direct_weight:
            for star_site in centres:
                remaining = tuple(
                    site for site in range(13) if site != star_site
                )
                row[column_index[star_site, word[star_site]]] += (
                    direct_weight * hafnian(word, remaining)
                )
        for left, right in combinations(range(13), 2):
            marked_weight = (
                p_entry(left, word[left], source_left)
                * p_entry(right, word[right], source_right)
                + p_entry(left, word[left], source_right)
                * p_entry(right, word[right], source_left)
            )
            if not marked_weight:
                continue
            for star_site in centres:
                if star_site in (left, right):
                    continue
                remaining = tuple(
                    site
                    for site in range(13)
                    if site not in (left, right, star_site)
                )
                row[column_index[star_site, word[star_site]]] += (
                    marked_weight * hafnian(word, remaining)
                )
        return row

    right_exceptional = (0, 1, 2, 3)
    left_exceptional = (4, 5, 6, 7, 8)
    marked_pair = (9, 10)
    rows = []
    for colour in (0, 1):
        for target in centres:
            other = centres[0] if target == centres[1] else centres[1]
            word = [0] * 13
            for site in marked_pair:
                word[site] = 2
            for site in left_exceptional:
                word[site] = colour
            for site in right_exceptional:
                word[site] = 1 - colour
            word[target] = colour
            word[other] = 1 - colour
            rows.append(response_row(tuple(word), 2, 2))
    for target in centres:
        other = centres[0] if target == centres[1] else centres[1]
        word = [0] * 13
        for site in marked_pair:
            word[site] = 2
        for site in left_exceptional:
            word[site] = 0
        for site in right_exceptional:
            word[site] = 1
        word[target] = 2
        word[other] = 1
        rows.append(response_row(tuple(word), 2, 2))

    cofactor = sp.Matrix([
        [
            *[
                sp.Rational(1, betas[left] + betas[right])
                for right in right_exceptional
            ],
            sp.Rational(1, betas[left] + 1),
        ]
        for left in left_exceptional
    ])
    coefficient = 2 * permanent_dynamic(cofactor)
    minor = sp.Matrix(rows)
    assert minor == coefficient * sp.eye(6)

    direct_word = tuple(index % 2 for index in range(13))
    complete = response_row(direct_word, 0, 1, True)
    marked_only = response_row(direct_word, 0, 1, False)
    difference = [left - right for left, right in zip(complete, marked_only)]
    expected = [Fraction(0)] * 6
    for star_site in centres:
        remaining = tuple(site for site in range(13) if site != star_site)
        expected[column_index[star_site, direct_word[star_site]]] += (
            Fraction(1, 2) * hafnian(direct_word, remaining)
        )
    assert difference == expected
    assert any(difference)


def main() -> None:
    rows, columns, modular_rank = coupled_incidence_rank()
    assert (rows, columns, modular_rank) == (6930, 5775, 5313)
    audit_double_confluent_borchardt()
    audit_multiplicity_four_lemma()
    reduced_profiles = audit_collision_partition_reduction()
    assert reduced_profiles == 14
    audit_one_double_residue()
    audit_distinct_quartic_obstruction()
    audit_permanental_descent()
    audit_complete_selected_response()
    print("Live three-zero all-exceptional eleven-live injectivity: PASS")
    print(
        "coupled incidence over F_1009: "
        f"{rows} rows x {columns} columns; rank={modular_rank}"
    )
    print("double-confluent Borchardt quotient: exact 5-square")
    print("multiplicity >= 4 deletion lemma: exact")
    print(f"two-class collision profiles reduced: {reduced_profiles}")
    print("one-double residue and distinct quartic obstructions: exact")
    print("complete selected zero-star minor: diagonal 6-square")


if __name__ == "__main__":
    main()
