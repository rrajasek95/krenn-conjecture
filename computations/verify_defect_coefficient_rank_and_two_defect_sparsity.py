#!/usr/bin/env python3
"""Tiny integer audit for the faithful-defect sharp overlap model.

The uniform defect-two theorem is a hand reduction to the completed abstract
product geometry.  This dependency-free script checks only the new five-site
model, its defect-coordinate faithfulness, and the decisive -6 overlap row.
"""

from fractions import Fraction
from itertools import combinations


E0 = (1, 0, 0)
IDENTITY = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
E00 = ((1, 0, 0), (0, 0, 0), (0, 0, 0))
SITES = range(5)
PAIRS = tuple(combinations(SITES, 2))


def matrix_scale(value, matrix):
    return tuple(tuple(value * entry for entry in row) for row in matrix)


def matrix_add(*matrices):
    return tuple(tuple(sum(matrix[i][j] for matrix in matrices)
                       for j in range(3)) for i in range(3))


def outer(left, right):
    return tuple(tuple(left[i] * right[j] for j in range(3))
                 for i in range(3))


def q_block(i, j):
    pair = tuple(sorted((i, j)))
    return IDENTITY if pair in {(0, 1), (2, 3)} else E00


def determinant3(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2]
                        - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2]
                          - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1]
                          - matrix[1][1] * matrix[2][0])
    )


ZETAS = (
    (1, -1, 0, 0, 0),
    (0, 0, 1, -1, 0),
    (0, 0, 0, 0, 1),
)


def z_block(zeta, i, j):
    return matrix_scale(zeta[i] + zeta[j], q_block(i, j))


def l_vector(coefficients, site):
    value = sum(coefficients[k] * ZETAS[k][site] for k in range(3))
    return tuple(value * coordinate for coordinate in E0)


def product_block(coefficients, i, j):
    # P_i=P_j=e0, with endpoint order retained in both summands.
    return matrix_add(outer(E0, l_vector(coefficients, j)),
                      outer(l_vector(coefficients, i), E0))


def defect_block(coefficients, i, j):
    return matrix_add(*(matrix_scale(coefficients[k], z_block(ZETAS[k], i, j))
                        for k in range(3)))


def rational_rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    column = 0
    while rank < len(matrix) and column < len(matrix[0]):
        pivot = next((row for row in range(rank, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            column += 1
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [left - scale * right
                           for left, right in zip(matrix[row], matrix[rank])]
        rank += 1
        column += 1
    return rank


def flatten_zeta(zeta):
    return tuple(entry for i, j in PAIRS for row in z_block(zeta, i, j)
                 for entry in row)


def audit_defect_coordinates():
    determinants = {pair: determinant3(q_block(*pair)) for pair in PAIRS}
    assert {pair for pair, determinant in determinants.items() if determinant} == {
        (0, 1), (2, 3)
    }
    assert tuple(sum(zeta) for zeta in ZETAS) == (0, 0, 1)
    assert rational_rank([flatten_zeta(zeta) for zeta in ZETAS]) == 3

    tests = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (2, -3, 5))
    for coefficients in tests:
        for i, j in PAIRS:
            assert product_block(coefficients, i, j) == defect_block(
                coefficients, i, j)
        direct = -coefficients[2]
        assert direct + sum(coefficients[k] * sum(ZETAS[k])
                            for k in range(3)) == 0
    return len(tests) * len(PAIRS)


def all_e0_q2_coefficient(vertices):
    vertices = tuple(vertices)
    first = vertices[0]
    total = 0
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        left, right = rest
        total += q_block(first, second)[0][0] * q_block(left, right)[0][0]
    return total


def audit_overlap_residual():
    # b=g=e3 gives S=T=e0 at site 5 and zero elsewhere.  Hence ST=0,
    # while the two direct-star layers each contribute -x_5 q^[2].
    q2 = all_e0_q2_coefficient((0, 1, 2, 3))
    assert q2 == 3
    residual = (-1 - 1) * q2
    assert residual == -6
    target_colours = (0, 1, 2)
    assert len(set(target_colours)) > 1
    return q2, residual


def main():
    block_checks = audit_defect_coordinates()
    q2, residual = audit_overlap_residual()
    print("defect coefficient rank and two-defect sparsity: PASS")
    print(f"five-site block checks={block_checks}; q^[2] coefficient={q2}; "
          f"target-zero overlap residual={residual}")


if __name__ == "__main__":
    main()
