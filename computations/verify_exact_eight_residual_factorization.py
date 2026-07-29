#!/usr/bin/env python3
"""Exact coefficient audit for the residual exact-eight factorization lemmas.

This script checks the canonical rank-one and rank-two plane-boundary
multiplication kernels, the two-by-two matrix identities used in the
factorization argument, and the square identity used when a response map
vanishes.  The accompanying note supplies the invariant reductions that
put arbitrary complex planes into these canonical coordinates.
"""

from __future__ import annotations

import sympy as sp


def basis(index: int) -> sp.Matrix:
    return sp.eye(3)[:, index]


def degree_one_product(
    left: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
    right: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    """Multiply two degree-one elements and return blocks 01, 02, 12."""

    return (
        left[0] * right[1].T + right[0] * left[1].T,
        left[0] * right[2].T + right[0] * left[2].T,
        left[1] * right[2].T + right[1] * left[2].T,
    )


def quadratic_times_star(
    blocks: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
    star: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
) -> sp.Matrix:
    """Multiply blocks 01, 02, 12 by a star and flatten in 0,1,2 order."""

    block_01, block_02, block_12 = blocks
    result = sp.zeros(27, 1)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[9 * i + 3 * j + k] = (
                    block_01[i, j] * star[2][k]
                    + block_02[i, k] * star[1][j]
                    + star[0][i] * block_12[j, k]
                )
    return result


def multiplication_matrix(
    blocks: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
) -> sp.Matrix:
    """Matrix of arbitrary degree-one multiplication by fixed blocks."""

    zero = sp.zeros(3, 1)
    columns = []
    for site in range(3):
        for color in range(3):
            star = [zero.copy(), zero.copy(), zero.copy()]
            star[site] = basis(color)
            columns.append(quadratic_times_star(blocks, tuple(star)))
    return sp.Matrix.hstack(*columns)


def audit_plane_boundary_kernels() -> None:
    """Both nonzero restriction ranks have exactly the common star plane."""

    e0, e1 = basis(0), basis(1)
    alternating = e0 * e1.T - e1 * e0.T

    rank_two = (alternating, -alternating, alternating)
    rank_two_map = multiplication_matrix(rank_two)
    rank_two_expected = sp.Matrix.hstack(
        sp.Matrix.vstack(e0, e0, e0),
        sp.Matrix.vstack(e1, e1, e1),
    )
    assert rank_two_map.rank() == 7
    assert rank_two_expected.rank() == 2
    assert rank_two_map * rank_two_expected == sp.zeros(27, 2)

    rank_one = (
        -e1 * e0.T,
        -e0 * e1.T + e1 * e0.T,
        e0 * e1.T,
    )
    rank_one_map = multiplication_matrix(rank_one)
    rank_one_expected = sp.Matrix.hstack(
        sp.Matrix.vstack(e0, e0, e0),
        sp.Matrix.vstack(e1, sp.zeros(3, 1), e1),
    )
    assert rank_one_map.rank() == 7
    assert rank_one_expected.rank() == 2
    assert rank_one_map * rank_one_expected == sp.zeros(27, 2)


def audit_rank_two_factorization() -> None:
    """The third edge becomes symmetric after the first two are imposed."""

    alpha, beta, gamma, delta = sp.symbols(
        "alpha beta gamma delta"
    )
    matrix_0 = sp.Matrix([[alpha, gamma], [beta, delta]])
    swap = sp.Matrix([[0, 1], [1, 0]])
    alternating = sp.Matrix([[0, 1], [-1, 0]])

    matrix_1_transpose = swap * matrix_0.inv() * alternating
    matrix_2_transpose = -swap * matrix_0.inv() * alternating
    assert sp.simplify(matrix_2_transpose + matrix_1_transpose) == sp.zeros(2)

    matrix_1 = matrix_1_transpose.T
    third_edge = -matrix_1 * swap * matrix_1.T
    assert sp.simplify(third_edge - third_edge.T) == sp.zeros(2)
    assert alternating - alternating.T != sp.zeros(2)


def audit_rank_one_factorization() -> None:
    """The exceptional component of the first factor vanishes."""

    alpha, beta, gamma, delta = sp.symbols(
        "alpha beta gamma delta"
    )
    determinant = alpha * delta - beta * gamma
    matrix_0 = sp.Matrix([[alpha, gamma], [beta, delta]])
    matrix_2 = sp.Matrix(
        [[alpha, -gamma], [beta, -delta]]
    ) / determinant
    coefficients = sp.Matrix([gamma, -alpha]) / determinant
    target_0 = sp.Matrix([0, -1])
    target_2 = sp.Matrix([0, 1])
    swap = sp.Matrix([[0, 1], [1, 0]])
    middle_block = sp.Matrix([[0, -1], [1, 0]])

    assert sp.simplify(matrix_0 * swap * matrix_2.T - middle_block) == sp.zeros(2)
    assert sp.simplify(matrix_0 * coefficients - target_0) == sp.zeros(2, 1)
    response = sp.simplify(matrix_2 * coefficients)
    expected = sp.Matrix(
        [
            2 * alpha * gamma / determinant**2,
            (alpha * delta + beta * gamma) / determinant**2,
        ]
    )
    assert sp.simplify(response - expected) == sp.zeros(2, 1)

    # If the nonzero exceptional component makes gamma nonzero, the first
    # coordinate equation response[0] = target_2[0] gives alpha = 0.
    exceptional_component = sp.simplify(coefficients[1].subs(alpha, 0))
    assert exceptional_component == 0
    first_regular_left = matrix_0[:, 0].subs(alpha, 0)
    first_regular_right = matrix_2[:, 0].subs(alpha, 0)
    assert first_regular_left == sp.Matrix([0, beta])
    assert first_regular_right == sp.Matrix([0, -1 / gamma])
    second_coordinate_residual = sp.factor(
        (response[1] - target_2[1]).subs(alpha, 0)
    )
    assert sp.simplify(
        second_coordinate_residual
        - (1 - beta * gamma) / (beta * gamma)
    ) == 0
    assert first_regular_right.subs(beta, 1 / gamma) == -first_regular_left.subs(
        beta, 1 / gamma
    )


def audit_zero_response_square_identity() -> None:
    """Check the factor two and alternating bracket in the zero-response case."""

    symbols = sp.symbols("a10:13 a20:23 A00:03 A10:13 A20:23")
    a1 = sp.Matrix(symbols[0:3])
    a2 = sp.Matrix(symbols[3:6])
    capital_0 = sp.Matrix(symbols[6:9])
    capital_1 = sp.Matrix(symbols[9:12])
    capital_2 = sp.Matrix(symbols[12:15])
    zero = sp.zeros(3, 1)

    tangent = (zero, a1, -a2)
    outside = (capital_0, capital_1, capital_2)
    actual = quadratic_times_star(
        degree_one_product(tangent, outside),
        outside,
    )

    expected = sp.zeros(27, 1)
    bracket = a1 * capital_2.T - capital_1 * a2.T
    for i in range(3):
        for j in range(3):
            for k in range(3):
                expected[9 * i + 3 * j + k] = (
                    2 * capital_0[i] * bracket[j, k]
                )
    assert sp.simplify(actual - expected) == sp.zeros(27, 1)


def main() -> None:
    audit_plane_boundary_kernels()
    audit_rank_two_factorization()
    audit_rank_one_factorization()
    audit_zero_response_square_identity()
    print("exact-eight residual factorization identities: PASS")


if __name__ == "__main__":
    main()
