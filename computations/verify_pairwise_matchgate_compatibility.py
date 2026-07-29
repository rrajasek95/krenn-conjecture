#!/usr/bin/env python3
"""Exact audits for notes/pairwise-matchgate-compatibility.md."""

from __future__ import annotations

import itertools
from fractions import Fraction


def pfaffian(matrix):
    """Recursive exact Pfaffian in the displayed index order."""
    n = len(matrix)
    if n == 0:
        return Fraction(1)
    assert n % 2 == 0
    answer = Fraction(0)
    for j in range(1, n):
        keep = [k for k in range(n) if k not in (0, j)]
        minor = [[matrix[r][c] for c in keep] for r in keep]
        answer += (-1) ** (j + 1) * matrix[0][j] * pfaffian(minor)
    return answer


def inverse(matrix):
    """Gauss-Jordan inverse over Fraction."""
    n = len(matrix)
    augmented = [
        [Fraction(value) for value in row]
        + [Fraction(int(i == j)) for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [
                    left - scale * right
                    for left, right in zip(augmented[row], augmented[column])
                ]
    return [row[n:] for row in augmented]


def matmul(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right)))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def submatrix(matrix, indices):
    return [[matrix[i][j] for j in indices] for i in indices]


def audit_replacement_identity():
    # A generic exact n=4 chart with Pf(A)=9.
    a = [
        [0, 1, 2, 3],
        [-1, 0, 4, 5],
        [-2, -4, 0, 7],
        [-3, -5, -7, 0],
    ]
    b = [list(range(1 + 4 * i, 5 + 4 * i)) for i in range(4)]
    d = [
        [0, 2, 3, 4],
        [-2, 0, 5, 6],
        [-3, -5, 0, 7],
        [-4, -6, -7, 0],
    ]
    a = [[Fraction(value) for value in row] for row in a]
    b = [[Fraction(value) for value in row] for row in b]
    d = [[Fraction(value) for value in row] for row in d]
    ai = inverse(a)
    m = matmul(ai, b)
    q = add(d, matmul(matmul(transpose(b), ai), b))
    k = [a[i] + b[i] for i in range(4)] + [
        [-transpose(b)[i][j] for j in range(4)] + d[i]
        for i in range(4)
    ]

    # Interleave h_i,p_i, as in equation (5).
    g_grouped = [ai[i] + m[i] for i in range(4)] + [
        [-transpose(m)[i][j] for j in range(4)] + q[i]
        for i in range(4)
    ]
    interleave = tuple(value for i in range(4) for value in (i, 4 + i))
    g = submatrix(g_grouped, interleave)
    reference = pfaffian(a)
    assert reference == 9
    for size in range(5):
        for selected in itertools.combinations(range(4), size):
            selected = set(selected)
            transversal = [4 + i if i in selected else i for i in range(4)]
            paired = [value for i in sorted(selected) for value in (2 * i, 2 * i + 1)]
            assert (
                pfaffian(submatrix(k, transversal)) / reference
                == pfaffian(submatrix(g, paired))
            )


def pfaffian_f2(matrix):
    n = len(matrix)
    if n == 0:
        return 1
    answer = 0
    for j in range(1, n):
        keep = [k for k in range(n) if k not in (0, j)]
        minor = [[matrix[r][c] for c in keep] for r in keep]
        answer ^= matrix[0][j] & pfaffian_f2(minor)
    return answer


def inverse_f2(matrix):
    n = len(matrix)
    augmented = [
        [value & 1 for value in row] + [int(i == j) for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        for row in range(n):
            if row != column and augmented[row][column]:
                augmented[row] = [
                    left ^ right
                    for left, right in zip(augmented[row], augmented[column])
                ]
    return [row[n:] for row in augmented]


def matmul_f2(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right))) & 1
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def audit_replacement_identity_f2():
    # Reduction modulo two of the rational audit above.  Pf(A)=1 in F_2.
    a = [
        [0, 1, 0, 1],
        [1, 0, 0, 1],
        [0, 0, 0, 1],
        [1, 1, 1, 0],
    ]
    b = [[(1 + 4 * i + j) & 1 for j in range(4)] for i in range(4)]
    d = [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [1, 1, 0, 1],
        [0, 0, 1, 0],
    ]
    assert pfaffian_f2(a) == 1
    ai = inverse_f2(a)
    m = matmul_f2(ai, b)
    bt = transpose(b)
    correction = matmul_f2(matmul_f2(bt, ai), b)
    q = [[d[i][j] ^ correction[i][j] for j in range(4)] for i in range(4)]
    k = [a[i] + b[i] for i in range(4)] + [bt[i] + d[i] for i in range(4)]
    mt = transpose(m)
    g_grouped = [ai[i] + m[i] for i in range(4)] + [mt[i] + q[i] for i in range(4)]
    interleave = tuple(value for i in range(4) for value in (i, 4 + i))
    g = submatrix(g_grouped, interleave)
    for size in range(5):
        for selected_tuple in itertools.combinations(range(4), size):
            selected = set(selected_tuple)
            transversal = [4 + i if i in selected else i for i in range(4)]
            paired = [value for i in sorted(selected) for value in (2 * i, 2 * i + 1)]
            assert pfaffian_f2(submatrix(k, transversal)) == pfaffian_f2(
                submatrix(g, paired)
            )


def matching_matrix(n, matching):
    matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for u, v in matching:
        if u > v:
            u, v = v, u
        matrix[u][v] = 1
        matrix[v][u] = -1
    # Normalize its displayed-order Pfaffian to one.
    value = pfaffian(matrix)
    assert value in (1, -1)
    if value == -1:
        u, v = matching[0]
        matrix[u][v] *= -1
        matrix[v][u] *= -1
    assert pfaffian(matrix) == 1
    return matrix


def coefficient(matrices, coloring):
    total = Fraction(1)
    for color, matrix in enumerate(matrices):
        vertices = [i for i, value in enumerate(coloring) if value == color]
        if len(vertices) % 2:
            return Fraction(0)
        total *= pfaffian(submatrix(matrix, vertices))
    return total


def audit_three_pairwise_restrictions():
    matchings = (
        ((0, 1), (2, 3), (4, 5)),
        ((0, 5), (1, 2), (3, 4)),
        ((0, 3), (1, 5), (2, 4)),
    )
    matrices = tuple(matching_matrix(6, matching) for matching in matchings)
    for colors in itertools.combinations(range(3), 2):
        for coloring in itertools.product(colors, repeat=6):
            assert coefficient(matrices, coloring) == int(len(set(coloring)) == 1)
    mixed = (2, 1, 1, 2, 0, 0)
    assert coefficient(matrices, mixed) in (1, -1)


def audit_cyclic_factors(maximum_n=16):
    for n in range(4, maximum_n + 1, 2):
        modulus = n - 1
        infinity = modulus

        def factor(a):
            edges = [(infinity, a)]
            for j in range(1, (modulus - 1) // 2 + 1):
                edges.append(((a + j) % modulus, (a - j) % modulus))
            return tuple(edges)

        factors = tuple(factor(a) for a in range(3))
        for first, second in itertools.combinations(factors, 2):
            adjacency = {vertex: [] for vertex in range(n)}
            for edge in first + second:
                u, v = edge
                adjacency[u].append(v)
                adjacency[v].append(u)
            assert all(len(neighbors) == 2 for neighbors in adjacency.values())
            seen = set()
            current, previous = 0, None
            while current not in seen:
                seen.add(current)
                following = next(
                    neighbor for neighbor in adjacency[current] if neighbor != previous
                )
                previous, current = current, following
            assert len(seen) == n and current == 0


if __name__ == "__main__":
    audit_replacement_identity()
    audit_replacement_identity_f2()
    audit_three_pairwise_restrictions()
    audit_cyclic_factors()
    print("verified paired Pfaffian replacement identity over Q and F_2")
    print("verified all three pairwise EQ_6 restrictions and ternary defect")
    print("verified cyclic pairwise-Hamilton factors through n=16")
