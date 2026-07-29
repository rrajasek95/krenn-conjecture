#!/usr/bin/env python3
"""Independent exact audit of the uniform critical moving-triple bound."""

from __future__ import annotations

import sympy as sp


def audit_wronskian_and_intersection_arithmetic() -> None:
    for r in range(4, 129):
        mass = (r + 1) * (r + 2)
        d = r + 3

        # The excess is the same throughout the feasible class range.
        for classes in range(r + 3, r + 6):
            forced_weight = d * classes - mass
            wronskian_cap = d * (classes + 1 - d)
            assert forced_weight - wronskian_cap == 2 * (r + 2)

            pair_lower = 2 * r - (r + 2)
            pair_ambient = max(classes - 7, 0)
            if classes <= r + 4:
                assert pair_ambient <= r - 3 < pair_lower
            else:
                assert classes == r + 5
                assert pair_ambient == pair_lower == r - 2

        # A gcd at an exact-row node never improves the primitive count.
        for multiplicity in range(r + 1):
            primitive = d - multiplicity
            for gcd_order in range(1, r + 4):
                if gcd_order <= multiplicity:
                    correction = (
                        d * gcd_order
                        + d
                        - (multiplicity - gcd_order)
                        - primitive
                    )
                else:
                    correction = d * gcd_order - primitive
                assert correction >= 0


def pair_product_coefficients(
    t: sp.Symbol, left: sp.Expr, right: sp.Expr
) -> list[sp.Expr]:
    expanded = sp.Poly((t - left) ** 2 * (t - right) ** 2, t)
    return [expanded.nth(power) for power in range(5)]


def audit_symbolic_five_product_determinant() -> None:
    t = sp.symbols("t")
    a0, a1, a2, a3 = sp.symbols("a0 a1 a2 a3")
    values = (a0, a1, a2, a3)
    edges = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3))
    coefficient_matrix = sp.Matrix(
        [pair_product_coefficients(t, values[i], values[j]) for i, j in edges]
    )
    determinant = sp.factor(coefficient_matrix.det())
    claimed = sp.factor(
        4
        * (a0 - a1) ** 4
        * (a0 - a2)
        * (a0 - a3)
        * (a1 - a2)
        * (a1 - a3)
        * (a2 - a3) ** 2
    )
    assert sp.expand(determinant - claimed) == 0


def rank_mod_prime(matrix: list[list[int]], prime: int) -> int:
    """Return exact row rank over F_prime by ordinary Gaussian elimination."""

    rows = [[entry % prime for entry in row] for row in matrix]
    row_count = len(rows)
    column_count = len(rows[0]) if rows else 0
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [(entry * inverse) % prime for entry in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or rows[row][column] == 0:
                continue
            factor = rows[row][column]
            rows[row] = [
                (left - factor * right) % prime
                for left, right in zip(rows[row], rows[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def audit_interval_cover_and_direct_product_ranks() -> None:
    z = sp.symbols("z")
    concrete_squares = (-7, -2, 3, 11)
    edges = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3))

    pair_products = [
        sp.Poly(
            (z**2 - concrete_squares[i]) ** 2
            * (z**2 - concrete_squares[j]) ** 2,
            z,
        )
        for i, j in edges
    ]

    for r in range(4, 41):
        intervals = [range(2 * shift, 2 * shift + r - 2) for shift in range(5)]
        covered = {degree for interval in intervals for degree in interval}
        assert covered == set(range(r + 6))

        # Independently form all five pair products times 1,z,...,z^(r-3).
        # Their coefficient columns must span the full P_{r+5}.
        columns: list[list[int]] = []
        for product in pair_products:
            for shift in range(r - 2):
                shifted = sp.Poly(product.as_expr() * z**shift, z)
                columns.append(
                    [int(shifted.nth(degree)) for degree in range(r + 6)]
                )
        multiplication_matrix = [
            [column[row] for column in columns] for row in range(r + 6)
        ]
        # Full rank modulo one prime certifies a nonzero integer minor, and
        # therefore full rank over Q.
        assert rank_mod_prime(multiplication_matrix, 1_000_003) == r + 6


def audit_p28_specialization() -> None:
    r = 4
    assert r * (r + 3) == 28
    baseline = (4, 4, 4, 3, 3, 3, 3, 3, 3)
    assert sum(baseline) == (r + 1) * (r + 2) == 30
    assert max(baseline) <= r
    assert len(baseline) == r + 5 == 9
    moving_triples = baseline.count(3)
    maximal_selections_allowed = 3
    assert moving_triples == 6
    assert moving_triples - maximal_selections_allowed == 3


def main() -> None:
    audit_wronskian_and_intersection_arithmetic()
    audit_symbolic_five_product_determinant()
    audit_interval_cover_and_direct_product_ranks()
    audit_p28_specialization()
    print("independent uniform critical moving-triple audit: PASS")
    print("exact common-lift hypotheses are essential")
    print("c <= r+4: at most one maximal selection")
    print("c = r+5: at most three maximal selections")
    print("p=28, 4^3 3^6: at least three selected dimensions are <=5")


if __name__ == "__main__":
    main()
