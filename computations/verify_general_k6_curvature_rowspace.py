#!/usr/bin/env python3
"""Exact lightweight audits for general-k6-curvature-rowspace.md."""

from fractions import Fraction
from itertools import combinations
from random import Random


if not __debug__:
    raise RuntimeError("run without -O: this audit uses assertions")


VERTICES = frozenset(range(6))
EDGES = tuple(combinations(range(6), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
S = ((0, 1), (2, 3), (0, 2), (1, 3))
R = tuple(edge for edge in EDGES if edge not in S)


def qvalue(q, edge):
    return Fraction(q.get(tuple(sorted(edge)), 0))


def complement_edge(e, f):
    if not set(e).isdisjoint(f):
        return None
    return tuple(sorted(VERTICES - set(e) - set(f)))


def hessian(q):
    return [
        [
            qvalue(q, complement_edge(e, f))
            if set(e).isdisjoint(f)
            else Fraction(0)
            for f in EDGES
        ]
        for e in EDGES
    ]


def curvature_covector(q):
    # kappa = q_01 q_23 - q_02 q_13.
    answer = [Fraction(0)] * len(EDGES)
    answer[EDGE_INDEX[(0, 1)]] = qvalue(q, (2, 3))
    answer[EDGE_INDEX[(2, 3)]] = qvalue(q, (0, 1))
    answer[EDGE_INDEX[(0, 2)]] = -qvalue(q, (1, 3))
    answer[EDGE_INDEX[(1, 3)]] = -qvalue(q, (0, 2))
    return answer


def hafnian4(q, vertices=(2, 3, 4, 5)):
    a, b, c, d = vertices
    return (
        qvalue(q, (a, b)) * qvalue(q, (c, d))
        + qvalue(q, (a, c)) * qvalue(q, (b, d))
        + qvalue(q, (a, d)) * qvalue(q, (b, c))
    )


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def matmul(left, right):
    right_t = transpose(right)
    return [
        [sum(a * b for a, b in zip(row, column)) for column in right_t]
        for row in left
    ]


def matsub(left, right):
    return [
        [a - b for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def submatrix(matrix, row_edges, column_edges):
    return [
        [matrix[EDGE_INDEX[e]][EDGE_INDEX[f]] for f in column_edges]
        for e in row_edges
    ]


def rref(matrix):
    source = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(source)
    column_count = len(source[0]) if source else 0
    pivot_row = 0
    pivots = []
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if source[row][column]),
            None,
        )
        if pivot is None:
            continue
        source[pivot_row], source[pivot] = source[pivot], source[pivot_row]
        scale = source[pivot_row][column]
        source[pivot_row] = [value / scale for value in source[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not source[row][column]:
                continue
            scale = source[row][column]
            source[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(source[row], source[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
    return source, tuple(pivots)


def rank(matrix):
    return len(rref(matrix)[1])


def augmented(matrix, vector):
    return [row + [value] for row, value in zip(matrix, vector)]


def determinant(matrix):
    source = [[Fraction(value) for value in row] for row in matrix]
    size = len(source)
    answer = Fraction(1)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if source[row][column]), None
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            source[column], source[pivot] = source[pivot], source[column]
            answer = -answer
        pivot_value = source[column][column]
        answer *= pivot_value
        for row in range(column + 1, size):
            if not source[row][column]:
                continue
            scale = source[row][column] / pivot_value
            for entry in range(column + 1, size):
                source[row][entry] -= scale * source[column][entry]
    return answer


def edge_vector(values):
    answer = [Fraction(0)] * len(EDGES)
    for edge, value in values.items():
        answer[EDGE_INDEX[tuple(sorted(edge))]] = Fraction(value)
    return answer


def schur_data(q):
    matrix = hessian(q)
    a = submatrix(matrix, S, S)
    b_block = submatrix(matrix, S, R)
    d = submatrix(matrix, R, R)
    q45 = qvalue(q, (4, 5))
    assert q45
    swap = [
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ]
    expected_a = [[q45 * value for value in row] for row in swap]
    assert a == expected_a
    a_inverse = [[Fraction(value, q45) for value in row] for row in swap]
    sigma = matsub(d, matmul(matmul(transpose(b_block), a_inverse), b_block))
    lambda_s = [curvature_covector(q)[EDGE_INDEX[edge]] for edge in S]
    b_vector = matvec(matmul(transpose(b_block), a_inverse), lambda_s)
    return matrix, sigma, b_vector


def check_schur_criterion():
    packets = [{edge: Fraction(1) for edge in EDGES}]
    rng = Random(20260730)
    for _ in range(24):
        q = {edge: Fraction(rng.randint(-2, 2)) for edge in EDGES}
        q[(2, 3)] = Fraction(rng.choice((-2, -1, 1, 2)))
        q[(4, 5)] = Fraction(rng.choice((-2, -1, 1, 2)))
        packets.append(q)

    for q in packets:
        matrix, sigma, b_vector = schur_data(q)
        lam = curvature_covector(q)
        assert rank(matrix) == 4 + rank(sigma)
        full_compatible = rank(augmented(matrix, lam)) == rank(matrix)
        schur_compatible = rank(augmented(sigma, b_vector)) == rank(sigma)
        assert full_compatible == schur_compatible


def check_uniform_point():
    q = {edge: Fraction(1) for edge in EDGES}
    matrix = hessian(q)
    assert matrix == transpose(matrix)
    assert determinant(matrix) == -1458
    assert rank(matrix) == 15


def check_sparse_guard():
    q = {edge: Fraction(1) for edge in ((0, 3), (1, 4), (2, 3), (4, 5))}
    beta = edge_vector({(0, 1): 1})
    lam = curvature_covector(q)
    matrix = hessian(q)
    witness = edge_vector({(0, 1): 1, (0, 5): -1, (1, 2): -1, (2, 5): 1})

    assert hafnian4(q) == 1
    assert dot(beta, lam) == 1
    assert dot(beta, edge_vector({(0, 1): hafnian4(q)})) == 1
    assert lam == beta
    assert matvec(matrix, witness) == [0] * 15
    assert dot(lam, witness) == 1
    assert rank(matrix) == 10
    assert rank(augmented(matrix, lam)) == 11


def check_corank_one_guard():
    support = {
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 3),
        (4, 5),
    }
    q = {edge: Fraction(int(edge in support)) for edge in EDGES}
    beta = edge_vector({(0, 1): 1})
    lam = curvature_covector(q)
    matrix = hessian(q)
    witness = edge_vector({(0, 2): 1, (0, 3): -1, (2, 4): -1, (3, 4): 1})

    assert hafnian4(q) == 1
    assert qvalue(q, (0, 1)) * qvalue(q, (2, 3)) == (
        qvalue(q, (0, 2)) * qvalue(q, (1, 3))
    )
    assert dot(beta, lam) == 1
    assert matvec(matrix, witness) == [0] * 15
    assert dot(lam, witness) == -1
    assert rank(matrix) == 14
    assert rank(augmented(matrix, lam)) == 15

    deleted = EDGE_INDEX[(0, 2)]
    cofactor = [
        [value for column, value in enumerate(row) if column != deleted]
        for row_index, row in enumerate(matrix)
        if row_index != deleted
    ]
    assert determinant(cofactor) == -128

    bordered = augmented(matrix, lam) + [lam + [Fraction(0)]]
    assert determinant(bordered) == 128

    q15_direction = hessian({(1, 5): Fraction(1)})
    restricted_derivative = dot(witness, matvec(q15_direction, witness))
    assert restricted_derivative == 4
    assert -128 * restricted_derivative == -512


def main():
    check_uniform_point()
    check_schur_criterion()
    check_sparse_guard()
    check_corank_one_guard()
    print("general K6 curvature row-space checks: PASS")
    print("  exact Schur packets: 25")
    print("  sparse guard ranks: 10 -> 11")
    print(
        "  corank-one guard ranks: 14 -> 15; bordered determinant: 128; "
        "restricted derivative: -512"
    )


if __name__ == "__main__":
    main()
