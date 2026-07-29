#!/usr/bin/env python3
"""Exact audits for notes/paired-pfaffian-local-rank.md.

The main example is the field-uniform paired Pfaffian whose transverse
output is

    e_0^tensor(n) + (e_1+e_2)^tensor(n).

It has a nonsingular hole block, satisfies every mixed equation containing
both color 0 and a nonzero color, and has all three constant coefficients
equal to one.  It deliberately leaves the fully switched {1,2} face alive.
"""

from __future__ import annotations

import itertools


N = 6
Q = 3
P0 = ((0, 1), (2, 3), (4, 5))
P1 = ((0, 5), (1, 2), (3, 4))


def pfaffian(matrix):
    if not matrix:
        return 1
    answer = 0
    for column in range(1, len(matrix)):
        keep = [index for index in range(len(matrix))
                if index not in (0, column)]
        minor = [[matrix[row][entry] for entry in keep] for row in keep]
        answer += (-1) ** (column + 1) * matrix[0][column] * pfaffian(minor)
    return answer


def submatrix(matrix, indices):
    return [[matrix[row][column] for column in indices] for row in indices]


def matrix_multiply(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right)))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def build_paired_matrix():
    # Local mode order is h_i,p_i,q_i.  Since A_0 is the canonical matching
    # matrix, H=A_0^{-1}=-A_0.  The P1 blocks on particles are all-ones
    # 2-by-2 matrices, making colors 1 and 2 indistinguishable.
    matrix = [[0 for _ in range(3 * N)] for _ in range(3 * N)]

    def set_entry(i, local_i, j, local_j, value):
        matrix[3 * i + local_i][3 * j + local_j] = value
        matrix[3 * j + local_j][3 * i + local_i] = -value

    for i, j in P0:
        set_entry(i, 0, j, 0, -1)
    for i, j in P1:
        for local_i, local_j in itertools.product((1, 2), repeat=2):
            set_entry(i, local_i, j, local_j, 1)
    return matrix


def paired_coordinate(matrix, coloring):
    indices = []
    for site, color in enumerate(coloring):
        if color:
            indices.extend((3 * site, 3 * site + color))
    return pfaffian(submatrix(matrix, indices))


def local_congruence(matrix, alpha, beta):
    size = 3 * N
    transform = [[int(i == j) for j in range(size)] for i in range(size)]
    for site in range(N):
        # New p_i=p_i+alpha_i h_i and q_i=q_i+beta_i h_i.
        transform[3 * site][3 * site + 1] = alpha[site]
        transform[3 * site][3 * site + 2] = beta[site]
    return matrix_multiply(transpose(transform),
                           matrix_multiply(matrix, transform))


def verify_countermodel_and_shears():
    matrix = build_paired_matrix()

    hole_indices = [3 * site for site in range(N)]
    hole_block = submatrix(matrix, hole_indices)
    assert pfaffian(hole_block) == -1

    values = {}
    for coloring in itertools.product(range(Q), repeat=N):
        value = paired_coordinate(matrix, coloring)
        expected = int(
            all(color == 0 for color in coloring)
            or all(color in (1, 2) for color in coloring)
        )
        assert value == expected, (coloring, value)
        values[coloring] = value
    assert sum(values.values()) == 1 + 2 ** N
    assert values[(0,) * N] == values[(1,) * N] == values[(2,) * N] == 1

    # Every two-site mixed coordinate vanishes.  Equivalently, every
    # inter-site block has its four 2-by-2 minors through (h,h) equal zero.
    for i, j in itertools.combinations(range(N), 2):
        block = [
            [matrix[3 * i + row][3 * j + column] for column in range(3)]
            for row in range(3)
        ]
        for row, column in itertools.product((1, 2), repeat=2):
            minor = block[0][0] * block[row][column] - block[0][column] * block[row][0]
            assert minor == 0
        if block[0][0]:
            # In this example the block is already supported only at hh.
            assert sum(bool(value) for row in block for value in row) == 1

    # Codeword-preserving shears make the H-supported blocks dense rank-one
    # blocks.  All 3^6 codeword Pfaffians remain unchanged, and the inverse
    # shears recover the pure-hh matching normalization.
    alpha = (1, 2, -1, 3, -2, 4)
    beta = (2, -1, 1, -3, 4, -2)
    sheared = local_congruence(matrix, alpha, beta)
    for coloring, value in values.items():
        assert paired_coordinate(sheared, coloring) == value

    for i, j in P0:
        block = [
            [sheared[3 * i + row][3 * j + column] for column in range(3)]
            for row in range(3)
        ]
        for rows in itertools.combinations(range(3), 2):
            for columns in itertools.combinations(range(3), 2):
                determinant = (
                    block[rows[0]][columns[0]] * block[rows[1]][columns[1]]
                    - block[rows[0]][columns[1]] * block[rows[1]][columns[0]]
                )
                assert determinant == 0

    recovered = local_congruence(sheared,
                                 tuple(-value for value in alpha),
                                 tuple(-value for value in beta))
    assert recovered == matrix


def verify_triangle_synchronization_logic():
    # If each of three vertices has at least one color for which its local
    # determinant is nonzero, choosing those three colors makes the triangle
    # product nonzero.  Hence vanishing for all 2^3 color choices forces one
    # vertex to vanish in both colors.  Exhaust the Boolean abstraction.
    colors = (0, 1)
    for zero_sets in itertools.product(
        tuple(frozenset(choice) for size in range(3)
              for choice in itertools.combinations(colors, size)),
        repeat=3,
    ):
        all_products_zero = all(
            any(coloring[vertex] in zero_sets[vertex] for vertex in range(3))
            for coloring in itertools.product(colors, repeat=3)
        )
        if all_products_zero:
            assert any(zero_set == frozenset(colors) for zero_set in zero_sets)


def main():
    verify_countermodel_and_shears()
    verify_triangle_synchronization_logic()
    print("verified field-uniform paired local-rank countermodel at n=6")
    print("verified codeword-preserving matching shear normalization")
    print("verified triangle synchronization implication")


if __name__ == "__main__":
    main()
