#!/usr/bin/env python3
"""Exact lightweight checks for the two-stage K6 provenance obstruction."""

from fractions import Fraction
from itertools import combinations


if not __debug__:
    raise RuntimeError("run without -O: this exact checker uses assertions")


VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {e: i for i, e in enumerate(EDGES)}


def rank_and_det(matrix):
    """Return exact rational rank and determinant for a square matrix."""
    a = [[Fraction(x) for x in row] for row in matrix]
    n = len(a)
    rank = 0
    det = Fraction(1)
    for col in range(n):
        pivot = next((r for r in range(rank, n) if a[r][col]), None)
        if pivot is None:
            det = Fraction(0)
            continue
        if pivot != rank:
            a[rank], a[pivot] = a[pivot], a[rank]
            det = -det
        p = a[rank][col]
        det *= p
        a[rank] = [x / p for x in a[rank]]
        for r in range(rank + 1, n):
            if a[r][col]:
                factor = a[r][col]
                a[r] = [x - factor * y for x, y in zip(a[r], a[rank])]
        rank += 1
    return rank, det


def matvec(matrix, vector):
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def disjointness_matrix():
    return [
        [int(not set(e).intersection(f)) for e in EDGES]
        for f in EDGES
    ]


def top_coefficient(edge_vector):
    # At q_e = 1, the complement of each selected edge has three matchings.
    return 3 * sum(edge_vector)


def check_two_stage_identity():
    w = disjointness_matrix()
    # U is the all-one row.  U L has six in every edge coordinate, while
    # 2 M has twice the complementary K4 hafnian, hence also six.
    u_l = [sum(w[row][col] for row in range(15)) for col in range(15)]
    two_m = [2 * top_coefficient([int(j == col) for j in range(15)])
             for col in range(15)]
    assert u_l == two_m == [6] * 15
    return len(u_l)


def check_uniform_cycle_and_pencil():
    w = disjointness_matrix()
    rank, det = rank_and_det(w)
    assert rank == 15 and det == -1458

    cycle = [0] * 15
    for edge, value in { (0, 1): 1, (2, 3): 1,
                         (0, 3): -1, (1, 2): -1 }.items():
        cycle[EDGE_INDEX[edge]] = value
    assert matvec(w, cycle) == cycle
    assert sum(cycle) == 0  # not in im(U^*), and radial q is killed

    beta_pos = [0] * 15
    beta_neg = [0] * 15
    beta_pos[EDGE_INDEX[(0, 1)]] = 1
    beta_neg[EDGE_INDEX[(0, 3)]] = 1

    assert dot(cycle, beta_pos) == 1
    assert dot(cycle, beta_neg) == -1
    assert top_coefficient(beta_pos) == 3
    assert top_coefficient(beta_neg) == 3

    # No scalar a can make u-v = 2 a * 3(u+v) on both pencil generators.
    # The two required values would be a=1/6 and a=-1/6.
    required_a = (
        Fraction(dot(cycle, beta_pos), 2 * top_coefficient(beta_pos)),
        Fraction(dot(cycle, beta_neg), 2 * top_coefficient(beta_neg)),
    )
    assert required_a == (Fraction(1, 6), Fraction(-1, 6))
    assert required_a[0] != required_a[1]
    return det, required_a


def check_hankel_toeplitz_pairing():
    # A cubic c_0 u^3 + ... + c_3 v^3 has the three shifted columns.
    c = [2, -3, 5, 7]
    theta = [11, 13, 17, 19, 23, 29]
    toeplitz_columns = [
        [c[0], c[1], c[2], c[3], 0, 0],
        [0, c[0], c[1], c[2], c[3], 0],
        [0, 0, c[0], c[1], c[2], c[3]],
    ]
    direct = [dot(theta, column) for column in toeplitz_columns]
    hankel = [sum(c[k] * theta[k + j] for k in range(4)) for j in range(3)]
    assert direct == hankel
    return direct


def main():
    columns = check_two_stage_identity()
    det, required_a = check_uniform_cycle_and_pencil()
    hankel = check_hankel_toeplitz_pairing()
    print(f"two-stage multiplication: PASS ({columns} edge columns)")
    print(f"uniform K6 pullback: PASS (det={det})")
    print(f"rank-one pencil provenance guard: PASS (top scalars {required_a})")
    print(f"Macaulay transpose indexing: PASS ({hankel})")


if __name__ == "__main__":
    main()
