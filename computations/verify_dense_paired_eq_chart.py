#!/usr/bin/env python3
"""Exact audit of a dense four-site paired-EQ Pfaffian chart."""

from __future__ import annotations

import itertools


def pfaffian(matrix):
    if not matrix:
        return 1
    answer = 0
    for j in range(1, len(matrix)):
        keep = [index for index in range(len(matrix)) if index not in (0, j)]
        minor = [[matrix[row][column] for column in keep] for row in keep]
        answer += (-1) ** (j + 1) * matrix[0][j] * pfaffian(minor)
    return answer


def submatrix(matrix, indices):
    return [[matrix[row][column] for column in indices] for row in indices]


def main():
    e0 = (1, 0)
    e1 = (0, 1)
    # An edge ij carries one nonzero half-vector in L_i and one in L_j.
    half_vectors = {
        (0, 1): (e0, e0),
        (1, 2): (e1, e0),
        (2, 3): (e1, e0),
        (0, 3): (e1, e1),
        (0, 2): (e0, e1),
        (1, 3): (e1, e1),
    }
    matrix = [[0 for _ in range(8)] for _ in range(8)]
    for (i, j), (left, right) in half_vectors.items():
        block = [[left[row] * right[column] for column in range(2)] for row in range(2)]
        assert any(map(any, block))
        assert block[0][0] * block[1][1] - block[0][1] * block[1][0] == 0
        for row, column in itertools.product(range(2), repeat=2):
            matrix[2 * i + row][2 * j + column] = block[row][column]
            matrix[2 * j + column][2 * i + row] = -block[row][column]

    values = {}
    for size in range(5):
        for sites in itertools.combinations(range(4), size):
            modes = [2 * site + bit for site in sites for bit in range(2)]
            values[sites] = pfaffian(submatrix(matrix, modes))
            assert bool(values[sites]) == (size in (0, 4))
    assert abs(values[(0, 1, 2, 3)]) == 1
    assert len(half_vectors) == 6  # every inter-site block is nonzero
    print("verified dense paired EQ_4 chart over Z (and hence over every field)")
    print("paired principal Pfaffians:", values)


if __name__ == "__main__":
    main()
