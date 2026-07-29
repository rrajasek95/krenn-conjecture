#!/usr/bin/env python3
"""Exact audit of the rank-one cap seven-plane and its two normal residuals."""

from fractions import Fraction as F

from verify_polarized_paircap_counterexample import (
    paircap_example,
    polarized_coefficients,
    target,
)


def matrix_rank(rows):
    matrix = [[F(value) for value in row] for row in rows]
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def torus_matrix(a, b):
    return [
        F(1), F(1, a), F(1, b),
        F(a), F(1), F(a, b),
        F(b), F(b, a), F(1),
    ]


def basis_cell(row, column, value=1):
    matrix = [F(0)] * 9
    matrix[3 * row + column] = F(value)
    return matrix


def main():
    # Seven exact torus evaluations span the equal-diagonal seven-plane.
    points = ((1, 1), (2, 1), (3, 1), (1, 2), (1, 3), (2, 3), (3, 2))
    torus_basis = [torus_matrix(a, b) for a, b in points]
    assert matrix_rank(torus_basis) == 7
    assert all(row[0] == row[4] == row[8] for row in torus_basis)

    normal_one = [
        left - right
        for left, right in zip(basis_cell(1, 1), basis_cell(0, 0))
    ]
    normal_two = [
        left - right
        for left, right in zip(basis_cell(2, 2), basis_cell(0, 0))
    ]
    assert matrix_rank(torus_basis + [normal_one, normal_two]) == 9

    # The literal local pair source has F_00=Delta and every other F_ij=0.
    q, _, _, z = paircap_example()
    delta = target()
    assert polarized_coefficients(q, z) == delta

    zero = {word: F(0) for word in delta}
    pure = {
        color: {
            word: F(int(word == (color,) * 6))
            for word in delta
        }
        for color in range(3)
    }

    # Residual on N_1: (F_11-F_00)-(X_1-X_0)=-2X_1-X_2.
    residual_one = {
        word: zero[word] - delta[word] - pure[1][word] + pure[0][word]
        for word in delta
    }
    expected_one = {
        word: -2 * pure[1][word] - pure[2][word]
        for word in delta
    }
    assert residual_one == expected_one

    # Residual on N_2: (F_22-F_00)-(X_2-X_0)=-X_1-2X_2.
    residual_two = {
        word: zero[word] - delta[word] - pure[2][word] + pure[0][word]
        for word in delta
    }
    expected_two = {
        word: -pure[1][word] - 2 * pure[2][word]
        for word in delta
    }
    assert residual_two == expected_two

    assert sum(bool(value) for value in residual_one.values()) == 2
    assert sum(bool(value) for value in residual_two.values()) == 2
    print(
        "rank-one cap seven-plane transverse synchronization: PASS; "
        "span rank=7; normal complement=2; both normal residuals nonzero"
    )


if __name__ == "__main__":
    main()
