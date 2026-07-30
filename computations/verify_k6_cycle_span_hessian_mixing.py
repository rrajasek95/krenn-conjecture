#!/usr/bin/env python3
"""Exact lightweight check of cycle-span Hessian mixing."""

from fractions import Fraction

from verify_two_anchor_hessian_all_cycle_seven_row_guard import (
    curvature_covector,
    dot,
    edge_vector,
    hessian,
    matvec,
    rank,
)


if not __debug__:
    raise RuntimeError("run without -O: this exact checker uses assertions")


def linear_combination(coefficients, vectors):
    return [
        sum(
            Fraction(coefficient) * vector[index]
            for coefficient, vector in zip(coefficients, vectors)
        )
        for index in range(len(vectors[0]))
    ]


def main():
    matrix = hessian()
    kernel = edge_vector({(0, 1): 1, (0, 4): -1, (1, 2): -1, (2, 4): 1})
    beta = edge_vector({(0, 1): 1})
    normals = [
        curvature_covector(matched_edge, reverse)
        for matched_edge in ((2, 5), (3, 4))
        for reverse in (False, True)
    ]

    cap_values = [dot(normal, beta) for normal in normals]
    kernel_values = [dot(normal, kernel) for normal in normals]
    assert matrix == [list(column) for column in zip(*matrix)]
    assert matvec(matrix, kernel) == [Fraction(0)] * len(kernel)
    assert rank(matrix) == len(matrix) - 1
    assert cap_values == [1, 1, 1, 1]
    assert kernel_values == [1, 2, 1, 2]
    assert all(kernel_values)
    assert all(
        rank([row + [normal[index]] for index, row in enumerate(matrix)])
        == len(matrix)
        for normal in normals
    )

    coefficients = (2, -1, 0, 0)
    mixed = linear_combination(coefficients, normals)
    expected = edge_vector({(0, 1): 1, (1, 2): 1, (1, 5): -2, (2, 5): 1})
    assert mixed == expected
    assert dot(mixed, kernel) == 0
    assert dot(mixed, beta) == 1
    assert rank([row + [mixed[index]] for index, row in enumerate(matrix)]) == 14

    pullback = edge_vector(
        {
            (0, 2): Fraction(-3, 4),
            (0, 3): Fraction(3, 4),
            (0, 4): Fraction(-3, 4),
            (1, 2): Fraction(3, 4),
            (1, 3): Fraction(3, 4),
            (1, 5): Fraction(-3, 4),
            (2, 3): Fraction(-3, 4),
            (3, 4): Fraction(1, 4),
            (4, 5): Fraction(3, 4),
        }
    )
    assert matvec(matrix, pullback) == mixed

    print("cycle-span Hessian mixing: PASS")
    print("  individual kernel values: (1,2,1,2)")
    print("  mixture coefficients: (2,-1,0,0)")
    print("  mixed cap value: 1; augmented Hessian rank: 14")
    print("  explicit rational four-set pullback: PASS")


if __name__ == "__main__":
    main()
