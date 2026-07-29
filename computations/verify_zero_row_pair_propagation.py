#!/usr/bin/env python3
"""Exact audit for ``notes/zero-row-pair-propagation.md``."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

import verify_all_pair_missing_row_countermodel as k8
import verify_source_hessian_dichotomy as hessian


def oriented_row(matrices, endpoint, other, colour):
    edge = tuple(sorted((endpoint, other)))
    if edge not in matrices:
        return (Fraction(0),) * 3
    matrix = matrices[edge]
    if edge[0] == endpoint:
        return tuple(matrix[colour])
    return tuple(matrix[row][colour] for row in k8.COLORS)


def determinant(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def outer(left, right):
    return tuple(tuple(x * y for y in right) for x in left)


def to_modular(value):
    return value.numerator * pow(value.denominator, hessian.P - 2, hessian.P) % hessian.P


def audit_internal_hessian(matrices):
    internal = (2, 3, 4, 5, 6, 7)
    relabel = {vertex: index for index, vertex in enumerate(internal)}
    zero = tuple(tuple(Fraction(0) for _ in k8.COLORS) for _ in k8.COLORS)
    q = {}
    rank_three_edges = []
    for left, right in combinations(internal, 2):
        matrix = matrices.get((left, right), zero)
        q[relabel[left], relabel[right]] = [
            [to_modular(entry) for entry in row] for row in matrix
        ]
        if determinant(matrix):
            rank_three_edges.append((left, right))

    labels, columns = hessian.multiplication_columns(q, 6)
    assert hessian.sparse_column_rank(columns) == 130
    gauges = hessian.gauge_columns(q, labels, 6)
    assert hessian.linear_rank(gauges) == 5
    assert rank_three_edges == [(2, 5), (3, 4), (3, 6), (4, 5)]
    return rank_three_edges


def audit_boundary_failure(matrices):
    p, q = 0, 1
    i, j = 3, 6
    c, d = 1, 0
    p_i = oriented_row(matrices, p, i, c)
    p_j = oriented_row(matrices, p, j, c)
    s_i = oriented_row(matrices, q, i, d)
    assert p_i == (0, 0, 0)
    assert p_j == (0, Fraction(1, 53), 0)
    assert s_i == (1, 0, 0)

    internal_block = matrices[(i, j)]
    assert determinant(internal_block)

    # With p_(c,i)=0, the zero-block expression is s_(d,i) tensor p_(c,j).
    block = outer(s_i, p_j)
    assert block == (
        (0, Fraction(1, 53), 0),
        (0, 0, 0),
        (0, 0, 0),
    )
    assert determinant(internal_block)

    direct = matrices[tuple(sorted((p, q)))][c][d]
    assert direct == 0
    colouring = {vertex: 0 for vertex in k8.VERTICES}
    colouring[p] = c
    colouring[q] = d
    assert k8.coefficient(matrices, k8.VERTICES, colouring) == Fraction(20, 53)


def main():
    matrices, _ = k8.normalized_matrices()
    rank_three_edges = audit_internal_hessian(matrices)
    audit_boundary_failure(matrices)
    print("verified: deleted pair 01 has gauge-rigid internal Hessian rank 130/135")
    print(f"verified: disconnected rank-three graph {rank_three_edges}")
    print("verified: zero row at 03 fails to propagate across rank-three edge 36")
    print("verified: offending block=(1/53)e0*e1 and mixed coefficient=20/53")


if __name__ == "__main__":
    main()
