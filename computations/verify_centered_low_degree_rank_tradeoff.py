#!/usr/bin/env python3
"""Tiny exact audit for the centered low-degree rank-tradeoff note.

The uniform theorem is proved by hand.  This dependency-free script checks
the two sharp rational solutions of

    e_c S_d^T + b_d P_c^T = lambda_cd M,  c != d,

including their ranks and exact zero-row ledgers.
"""

from fractions import Fraction


PAIRS = ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1))
E = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ZERO = (0, 0, 0)


def outer(left, right):
    return tuple(tuple(Fraction(x) * Fraction(y) for y in right) for x in left)


def add(left, right):
    return tuple(
        tuple(a + b for a, b in zip(row_left, row_right, strict=True))
        for row_left, row_right in zip(left, right, strict=True)
    )


def scale(value, matrix):
    return tuple(tuple(Fraction(value) * x for x in row) for row in matrix)


def transpose(matrix):
    return tuple(tuple(matrix[row][column] for row in range(3)) for column in range(3))


def rank(matrix):
    rows = [[Fraction(entry) for entry in row] for row in matrix]
    pivot_row = 0
    for column in range(3):
        pivot = next(
            (row for row in range(pivot_row, 3) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        divisor = rows[pivot_row][column]
        rows[pivot_row] = [entry / divisor for entry in rows[pivot_row]]
        for row in range(3):
            if row == pivot_row:
                continue
            coefficient = rows[row][column]
            if coefficient:
                rows[row] = [
                    entry - coefficient * base
                    for entry, base in zip(rows[row], rows[pivot_row], strict=True)
                ]
        pivot_row += 1
    return pivot_row


def column_matrix(columns):
    return transpose(columns)


def check_system(b_columns, aggregate, p_rows, s_rows, lambdas):
    assert len(lambdas) == len(PAIRS)
    for (c, d), multiplier in zip(PAIRS, lambdas, strict=True):
        lhs = add(outer(E[c], s_rows[d]), outer(b_columns[d], p_rows[c]))
        rhs = scale(multiplier, aggregate)
        assert lhs == rhs, ((c, d), lhs, rhs)


def check_rank_two_rank_one_star_witness():
    b_columns = (ZERO, ZERO, (1, 1, 0))
    aggregate = ((-1, -1, 0), (-1, 0, 0), (0, 0, 0))
    p_rows = ((1, 0, 0), (-1, -1, 0), (1, 1, 1))
    s_rows = (ZERO, ZERO, (0, 1, 0))
    lambdas = (0, -1, 0, 1, 0, 0)

    check_system(b_columns, aggregate, p_rows, s_rows, lambdas)
    assert rank(column_matrix(b_columns)) == 1
    assert rank(aggregate) == 2
    assert rank(p_rows) == 3
    assert tuple(row == ZERO for row in p_rows + s_rows) == (
        False,
        False,
        False,
        True,
        True,
        False,
    )


def check_rank_one_double_invertible_witness():
    b_columns = ((1, 0, 0), (1, 0, 1), (1, 1, 0))
    aggregate = ((1, 0, 0), (0, 0, 0), (0, 0, 0))
    p_rows = (ZERO, (1, 0, 0), (1, 0, 0))
    s_rows = (ZERO, (-1, 0, 0), (-1, 0, 0))
    lambdas = (-1, -1, 1, 1, 1, 1)

    check_system(b_columns, aggregate, p_rows, s_rows, lambdas)
    assert rank(column_matrix(b_columns)) == 3
    assert rank(aggregate) == 1
    assert tuple(row == ZERO for row in p_rows + s_rows) == (
        True,
        False,
        False,
        True,
        False,
        False,
    )


def main():
    check_rank_two_rank_one_star_witness()
    check_rank_one_double_invertible_witness()
    print("PASS: centered low-degree rank-tradeoff sharp witnesses")


if __name__ == "__main__":
    main()
