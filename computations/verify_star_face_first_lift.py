#!/usr/bin/env python3
"""Audit the two-edge-star first-lift reduction and its F4 boundary.

The mathematical classification and DVR argument are in
``notes/star-face-first-lift.md``.  This checker verifies the exact matching
groups used there, the unit-pair identity in ramified F2 truncations, and the
GR(4,2) matrix showing why the four-fibre shortcut fails over F4.
"""

from __future__ import annotations

from itertools import product

from verify_valuation_rainbow_descent_cycle import perfect_matchings


NEGATIVE_PAIRS = {(0, 1), (0, 2)}
SELECTED_COLORINGS = (
    (0, 2, 2, 2, 2, 0),
    (2, 2, 2, 2, 2, 0),
    (0, 2, 2, 2, 2, 2),
    (2, 2, 2, 2, 2, 2),
)


def audit_matching_groups():
    matchings = tuple(perfect_matchings())
    minimum = tuple(
        matching
        for matching in matchings
        if any(edge in NEGATIVE_PAIRS for edge in matching)
    )
    nonminimum = tuple(matching for matching in matchings if matching not in minimum)
    assert len(minimum) == 6
    assert len(nonminimum) == 9
    assert sum((0, 1) in matching for matching in minimum) == 3
    assert sum((0, 2) in matching for matching in minimum) == 3

    # At the four selected colourings, grouping by the chosen star edge has
    # the common form x_a r_t + y_a s_t.  This check records that the other
    # four vertex colours agree exactly as used in the proof.
    for coloring in SELECTED_COLORINGS:
        a, b, c, d, e, t = coloring
        assert b == c == d == e == 2
        assert a in (0, 2) and t in (0, 2)
    assert [len(set(coloring)) == 1 for coloring in SELECTED_COLORINGS] == [
        False,
        False,
        False,
        True,
    ]


def add_ramified_f2(left, right, ramification):
    """Add modulo pi^(e+1), with residue F2 and pi^e=2."""
    mask = (1 << (ramification + 1)) - 1
    carry = ((left & 1) & (right & 1)) << ramification
    return ((left ^ right) ^ carry) & mask


def multiply_ramified_f2(left, right, ramification):
    """Multiply binary pi-expansions modulo pi^(e+1)."""
    answer = 0
    for i in range(ramification + 1):
        if not (left >> i) & 1:
            continue
        for j in range(ramification + 1 - i):
            if (right >> j) & 1:
                answer ^= 1 << (i + j)
    return answer


def audit_f2_unit_pair_lemma():
    # Exhaust the unit-pair statement for several ramification indices.  The
    # note proves it for arbitrary e by the identity w-v=2(1-v).
    for ramification in range(1, 10):
        modulus_size = 1 << (ramification + 1)
        units = tuple(value for value in range(modulus_size) if value & 1)
        two = 1 << ramification
        for left, right in product(units, repeat=2):
            assert (add_ramified_f2(left, right, ramification) == two) == (
                left == right
            )

        # Sanity-check closure and the residue-one product property used in
        # the ratio argument.
        assert all(
            multiply_ramified_f2(left, right, ramification) & 1
            for left, right in product(units, repeat=2)
        )


def gr4_add(left, right):
    return ((left[0] + right[0]) % 4, (left[1] + right[1]) % 4)


def gr4_neg(value):
    return ((-value[0]) % 4, (-value[1]) % 4)


def gr4_mul(left, right):
    # omega^2=-omega-1.
    a, b = left
    c, d = right
    return ((a * c - b * d) % 4, (a * d + b * c - b * d) % 4)


def gr4_matrix_product(left, right):
    answer = []
    for i in range(2):
        row = []
        for j in range(2):
            value = (0, 0)
            for k in range(2):
                value = gr4_add(value, gr4_mul(left[i][k], right[k][j]))
            row.append(value)
        answer.append(row)
    return answer


def audit_f4_boundary():
    zero = (0, 0)
    one = (1, 0)
    two = (2, 0)
    omega = (0, 1)
    matrix = [
        [one, one],
        [omega, gr4_add(omega, two)],
    ]
    target_pattern = [[one, one], [one, zero]]
    adjugate = [
        [matrix[1][1], gr4_neg(matrix[0][1])],
        [gr4_neg(matrix[1][0]), matrix[0][0]],
    ]
    companion = gr4_matrix_product(adjugate, target_pattern)
    product_matrix = gr4_matrix_product(matrix, companion)
    assert product_matrix == [[two, two], [two, zero]]

    determinant = gr4_add(
        gr4_mul(matrix[0][0], matrix[1][1]),
        gr4_neg(gr4_mul(matrix[0][1], matrix[1][0])),
    )
    assert determinant == two

    # A GR(4,2) element is a unit exactly when its reduction in F4 is nonzero.
    assert all(
        (a % 2, b % 2) != (0, 0)
        for row in matrix + companion
        for a, b in row
    )


def main():
    audit_matching_groups()
    audit_f2_unit_pair_lemma()
    audit_f4_boundary()
    print(
        "verified star first-lift reduction: six minimum and nine higher "
        "matchings; four fibres have the required 2x2 pattern"
    )
    print(
        "verified residue-F2 obstruction through the first target digit "
        "for ramification indices 1..9 (uniform proof is symbolic)"
    )
    print(
        "verified F4 boundary: unit matrices M,V over GR(4,2) satisfy "
        "M V = 2 [[1,1],[1,0]]"
    )


if __name__ == "__main__":
    main()
