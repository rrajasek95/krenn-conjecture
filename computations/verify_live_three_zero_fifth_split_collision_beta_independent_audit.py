#!/usr/bin/env python3
"""Independent adversarial audit of the fifth-split collision proof."""

from __future__ import annotations

from itertools import combinations
from math import factorial

import sympy as sp


def permanent(matrix: sp.Matrix) -> sp.Expr:
    values: dict[int, sp.Expr] = {0: sp.S.One}
    for row in range(matrix.rows):
        following: dict[int, sp.Expr] = {}
        for mask, value in values.items():
            for column in range(matrix.cols):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                following[new_mask] = (
                    following.get(new_mask, sp.S.Zero)
                    + value * matrix[row, column]
                )
        values = following
    return sp.factor(values[(1 << matrix.cols) - 1])


def jet(power: int, x: sp.Expr, y: sp.Expr, s: int, j: int) -> sp.Expr:
    order = s + j
    return (
        (-1) ** order
        * sp.rf(power, order)
        / (factorial(s) * factorial(j) * (x + y) ** (power + order))
    )


def hermite(
    rows: tuple[tuple[int, int], ...],
    columns: tuple[tuple[int, int], ...],
    power: int,
) -> sp.Matrix:
    row_jets = [
        (sp.Integer(value), order)
        for value, multiplicity in rows
        for order in range(multiplicity)
    ]
    column_jets = [
        (sp.Integer(value), order)
        for value, multiplicity in columns
        for order in range(multiplicity)
    ]
    return sp.Matrix([
        [jet(power, x, y, s, j) for y, j in column_jets]
        for x, s in row_jets
    ])


def literal_cauchy(
    rows: tuple[tuple[int, int], ...],
    columns: tuple[tuple[int, int], ...],
) -> sp.Matrix:
    row_values = [
        sp.Integer(value)
        for value, multiplicity in rows
        for _ in range(multiplicity)
    ]
    column_values = [
        sp.Integer(value)
        for value, multiplicity in columns
        for _ in range(multiplicity)
    ]
    return sp.Matrix([
        [sp.S.One / (x + y) for y in column_values]
        for x in row_values
    ])


def audit_simultaneous_confluence() -> int:
    # Both examples have a value class on both shores.  The second also
    # has a triple column cluster, so this is not merely ordinary row
    # confluence followed by the common-column case.
    cases = (
        (
            ((2, 2), (3, 1), (5, 3)),
            ((2, 1), (7, 2), (11, 2), (13, 1)),
        ),
        (
            ((2, 1), (3, 2), (5, 1), (7, 2)),
            ((3, 1), (11, 3), (13, 2)),
        ),
    )
    for rows, columns in cases:
        denominator = hermite(rows, columns, 1).det(method="domain-ge")
        numerator = hermite(rows, columns, 2).det(method="domain-ge")
        assert denominator != 0
        assert sp.cancel(
            numerator / denominator - permanent(literal_cauchy(rows, columns))
        ) == 0
    return len(cases)


def audit_top_row_deletions() -> int:
    # Fifth-split boundary p=6: |N|=8 and there are six columns.  The
    # value 2 is deliberately shared between rows and columns.
    rows = ((2, 3), (3, 2), (5, 1), (7, 2))
    columns = ((2, 1), (11, 2), (13, 2), (17, 1))
    global_numerator = hermite(rows, columns, 2)
    offsets = []
    offset = 0
    for _, multiplicity in rows:
        offsets.append(offset + multiplicity - 1)
        offset += multiplicity

    cases = 0
    for first, second in combinations(range(len(rows)), 2):
        deleted = global_numerator.copy()
        deleted.row_del(max(offsets[first], offsets[second]))
        deleted.row_del(min(offsets[first], offsets[second]))

        reduced_rows = tuple(
            (value, multiplicity - (index in {first, second}))
            for index, (value, multiplicity) in enumerate(rows)
            if multiplicity - (index in {first, second}) > 0
        )
        rebuilt = hermite(reduced_rows, columns, 2)
        assert deleted == rebuilt

        denominator = hermite(reduced_rows, columns, 1).det(
            method="domain-ge"
        )
        assert denominator != 0
        assert sp.cancel(
            deleted.det(method="domain-ge") / denominator
            - permanent(literal_cauchy(reduced_rows, columns))
        ) == 0
        cases += 1
    return cases


def elementary(values: list[sp.Expr], degree: int) -> sp.Expr:
    return sp.expand(sum(
        sp.prod(values[index] for index in subset)
        for subset in combinations(range(len(values)), degree)
    ))


def audit_deleted_e5() -> None:
    h = list(sp.symbols("h0:8"))
    j, k = 0, 1
    for i in range(2, 8):
        left = [h[index] for index in range(8) if index not in {i, j}]
        right = [h[index] for index in range(8) if index not in {i, k}]
        common = [h[index] for index in range(8) if index not in {i, j, k}]
        assert sp.expand(
            elementary(left, 5)
            - elementary(right, 5)
            - (h[k] - h[j]) * elementary(common, 4)
        ) == 0

    # Verify every identity used in the descent at its minimal size.
    w = h[2:]
    for degree in range(4, 0, -1):
        deleted = [
            elementary([value for index, value in enumerate(w) if index != i], degree)
            for i in range(len(w))
        ]
        assert sp.expand(
            sum(deleted) - (len(w) - degree) * elementary(w, degree)
        ) == 0
        for i in range(len(w)):
            w_without_i = [
                value for index, value in enumerate(w) if index != i
            ]
            assert sp.expand(
                elementary(w, degree)
                - elementary(w_without_i, degree)
                - w[i] * elementary(w_without_i, degree - 1)
            ) == 0


def has_short_two_class_split(counts: tuple[int, int, int, int]) -> bool:
    # counts[m-1] is the number of classes of multiplicity m.  Search
    # over two actual, distinct classes without expanding a long profile.
    for left_type in range(1, 5):
        for right_type in range(1, 5):
            available = counts[left_type - 1]
            if left_type == right_type:
                if available < 2:
                    continue
            elif available < 1 or counts[right_type - 1] < 1:
                continue
            for left_used in range(1, left_type + 1):
                right_used = 5 - left_used
                if not 1 <= right_used <= right_type:
                    continue
                untouched_singletons = counts[0]
                if left_type == 1:
                    untouched_singletons -= 1
                if right_type == 1:
                    untouched_singletons -= 1
                if (
                    untouched_singletons > 0
                    or left_type - left_used == 1
                    or right_type - right_used == 1
                ):
                    return True
    return False


def expected_exception(counts: tuple[int, int, int, int]) -> str | None:
    singles, doubles, triples, quadruples = counts
    if quadruples:
        return None
    if triples >= 2:
        return None
    if triples == 1:
        if doubles and singles:
            return None
        if doubles == 0:
            return "triple_plus_singles"
        return "triple_plus_doubles"
    if doubles == 0:
        return "all_distinct"
    return "singles_and_doubles"


def audit_uniform_census() -> int:
    # A computational stress range much larger than the shipped p<=24
    # census.  The accompanying note gives the all-n case split.
    cases = 0
    for label_count in range(13, 121):
        for quadruples in range(label_count // 4 + 1):
            after_four = label_count - 4 * quadruples
            for triples in range(after_four // 3 + 1):
                after_three = after_four - 3 * triples
                for doubles in range(after_three // 2 + 1):
                    singles = after_three - 2 * doubles
                    counts = (singles, doubles, triples, quadruples)
                    short = has_short_two_class_split(counts)
                    exception = expected_exception(counts)
                    assert short == (exception is None), (label_count, counts)
                    cases += 1
    return cases


def audit_moving_equations() -> None:
    a, b, x, u, v = sp.symbols("a b x u v")
    for selected in (1, 2):
        chi = selected / (a + x) - (selected + 1) / (x - a)
        asserted = -(x + (2 * selected + 1) * a) / (x**2 - a**2)
        assert sp.cancel(chi - asserted) == 0
        polynomial = sp.Poly(
            sp.cancel((u + chi) * (x**2 - a**2)), x
        )
        assert polynomial.degree() <= 2
        assert polynomial.coeff_monomial(x) == -1

    def chi_one(anchor: sp.Expr) -> sp.Expr:
        return 1 / (anchor + x) - 2 / (x - anchor)

    y_a = u + chi_one(a)
    y_b = v + chi_one(b)
    determinant = y_b - y_a + (b - a) * y_a * y_b
    cleared = sp.Poly(
        sp.cancel(determinant * (x**2 - a**2) * (x**2 - b**2)),
        x,
    )
    assert cleared.degree() <= 4
    assert sp.expand(cleared.coeff_monomial(x**3) - (a - b) * (u + v)) == 0
    assert sp.expand(
        cleared.coeff_monomial(x**4) - (u * v * (b - a) - u + v)
    ) == 0
    assert sp.expand(
        cleared.as_expr().subs({u: 0, v: 0})
        - 2 * (a - b) * (x**2 - (a + b) * x - 3 * a * b)
    ) == 0
    assert sp.cancel(
        cleared.as_expr().subs({u: -2 / (b - a), v: 2 / (b - a)})
        + 4 * (a - b) * (x**2 + (a + b) * x + 3 * a * b)
    ) == 0


def audit_cardinalities_and_cleanup() -> int:
    cases = 0
    for p in range(6, 301):
        exceptional = p + 7
        k = p - 5
        active = k + 1
        assert exceptional - 5 == p + 2
        assert p + 2 - 2 == p
        assert 5 + k == p
        # After deleting the marked pair and the target star, the two
        # binary shores have size p.  A different active star leaves
        # sizes p+1 and p-1 and therefore has zero cofactor.
        assert p == 5 + (active - 1)
        assert p + 1 != 5 + (active - 2)

        triple_single_classes = exceptional - 3
        assert triple_single_classes - 1 >= 3
        if (exceptional - 3) % 2 == 0:
            triple_double_classes = (exceptional - 3) // 2
            assert triple_double_classes - 1 >= 3

        for doubles in range(1, exceptional // 2 + 1):
            singles = exceptional - 2 * doubles
            if singles < 0:
                continue
            if doubles <= 3:
                assert singles - 2 >= 5
                assert singles - 3 >= 1
            elif doubles == 4:
                assert singles >= 5
                assert doubles - 1 == 3
            else:
                assert doubles - 2 >= 3
            cases += 1
    return cases


def main() -> None:
    confluence_cases = audit_simultaneous_confluence()
    deletion_cases = audit_top_row_deletions()
    audit_deleted_e5()
    census_cases = audit_uniform_census()
    audit_moving_equations()
    cardinality_cases = audit_cardinalities_and_cleanup()
    print("Independent fifth-split collision audit: PASS")
    print(f"simultaneous row/column confluence cases: {confluence_cases}")
    print(f"top-row deletion/permanent cases: {deletion_cases}")
    print("deleted-e5 descent: exact at the p=6 boundary")
    print(f"multiplicity-count profiles through 120 labels: {census_cases}")
    print("moving-class quadratics and quartic obstruction: exact")
    print(f"cardinality and cleanup cases through p=300: {cardinality_cases}")


if __name__ == "__main__":
    main()
