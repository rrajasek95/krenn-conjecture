"""Exact check of the K6 matching-algebra middle-Lefschetz inverse."""

from fractions import Fraction
from itertools import combinations


EDGES = tuple(combinations(range(6), 2))


def disjointness_matrix():
    """Rows are complements of four-sets; columns are edges."""
    return [
        [Fraction(int(set(row).isdisjoint(col))) for col in EDGES]
        for row in EDGES
    ]


def inverse_candidate():
    def entry(left, right):
        overlap = len(set(left) & set(right))
        if overlap == 2:
            return Fraction(1, 2)
        if overlap == 1:
            return Fraction(-1, 6)
        return Fraction(1, 6)

    return [[entry(row, col) for col in EDGES] for row in EDGES]


def multiply(left, right):
    size = len(left)
    return [
        [sum(left[i][k] * right[k][j] for k in range(size))
         for j in range(size)]
        for i in range(size)
    ]


def determinant(matrix):
    work = [row[:] for row in matrix]
    value = Fraction(1)
    size = len(work)

    for col in range(size):
        pivot = next(row for row in range(col, size) if work[row][col])
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            value = -value

        pivot_value = work[col][col]
        value *= pivot_value
        for entry in range(col, size):
            work[col][entry] /= pivot_value

        for row in range(col + 1, size):
            scale = work[row][col]
            if not scale:
                continue
            for entry in range(col, size):
                work[row][entry] -= scale * work[col][entry]

    return value


def main():
    matrix = disjointness_matrix()
    candidate = inverse_candidate()
    identity = [
        [Fraction(int(i == j)) for j in range(len(EDGES))]
        for i in range(len(EDGES))
    ]

    assert multiply(matrix, candidate) == identity
    assert multiply(candidate, matrix) == identity
    assert determinant(matrix) == -1458
    print("K6 matching Lefschetz inverse: PASS")


if __name__ == "__main__":
    main()
