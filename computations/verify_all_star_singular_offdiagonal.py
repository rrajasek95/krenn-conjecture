#!/usr/bin/env python3
"""Exact off-diagonal counterexample to all-star-singular rigidity at n=6.

For a binary quadratic source q and a vertex i, the full star map is

    F_i : direct_sum_{j != i} V_j -> tensor_{v != i} V_v,
    e_(j,a) |-> e_a^(j) H_{B minus {i,j}}(q).

The source below has H(q)=2 X+Y, contains two off-diagonal cells, every
nonzero cell is tensor-active, and every 32 by 10 matrix F_i is singular.
All arithmetic is integral.
"""

from __future__ import annotations

import itertools
from fractions import Fraction


N = 6
COLORS = (0, 1)
VERTICES = tuple(range(N))

# A key is (u,v,a,b), with u<v and endpoint colors a at u, b at v.
Q = {
    (0, 1, 0, 0): 2,
    (2, 3, 0, 0): 1,
    (4, 5, 0, 0): 1,
    (0, 5, 1, 1): 1,
    (1, 2, 1, 1): 1,
    (3, 4, 1, 1): 1,
    # A three-cell cancellation module.  Its two supported matching terms
    # have the same mixed coloring and weights -2 and +2.
    (0, 1, 0, 1): -2,  # genuinely off-diagonal: x_0 y_1
    (0, 4, 0, 0): -2,
    (1, 5, 1, 0): -1,  # genuinely off-diagonal: y_1 x_5
}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def hafnian_coefficient(q, vertices, coloring):
    """Coefficient of the indicated coloring on an even vertex subset."""
    total = 0
    for matching in perfect_matchings(vertices):
        term = 1
        for u, v in matching:
            term *= q.get((u, v, coloring[u], coloring[v]), 0)
        total += term
    return total


def star_matrix(q, vertex):
    """Return the ordered columns and exact matrix of F_vertex."""
    columns = tuple(
        (neighbor, color)
        for neighbor in VERTICES
        if neighbor != vertex
        for color in COLORS
    )
    remaining = tuple(v for v in VERTICES if v != vertex)
    rows = []
    for tail in itertools.product(COLORS, repeat=N - 1):
        coloring = dict(zip(remaining, tail))
        row = []
        for neighbor, color in columns:
            if coloring[neighbor] != color:
                row.append(0)
                continue
            complement = tuple(
                v for v in VERTICES if v not in (vertex, neighbor)
            )
            row.append(hafnian_coefficient(q, complement, coloring))
        rows.append(row)
    return columns, rows


def rank(matrix):
    work = [list(map(Fraction, row)) for row in matrix]
    pivot_row = 0
    columns = len(work[0]) if work else 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                left - scale * right
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def matrix_vector(matrix, vector):
    return tuple(
        sum(Fraction(entry) * Fraction(value) for entry, value in zip(row, vector))
        for row in matrix
    )


# Sparse kernel certificates in the column ordering returned by star_matrix.
# Each dictionary denotes sum coefficient * e_(neighbor,color).
KERNEL_CERTIFICATES = {
    0: {(1, 1): 1, (4, 0): 1},
    1: {(3, 0): 1},
    2: {(4, 0): 1},
    3: {(1, 0): 1},
    4: {(2, 0): 1},
    5: {(1, 0): 1, (1, 1): -1, (4, 0): 1},
}


def main():
    nonzero = {}
    for bits in itertools.product(COLORS, repeat=N):
        coloring = dict(enumerate(bits))
        value = hafnian_coefficient(Q, VERTICES, coloring)
        if value:
            nonzero[bits] = value
    assert nonzero == {(0,) * N: 2, (1,) * N: 1}

    # Every scalar cell has a nonzero common cofactor and is therefore
    # tensor-active.  In particular the two off-diagonal cells are not
    # dead decorations.
    for u, v, a, b in Q:
        complement = tuple(vertex for vertex in VERTICES if vertex not in (u, v))
        active = False
        for tail in itertools.product(COLORS, repeat=N - 2):
            coloring = dict(zip(complement, tail))
            if hafnian_coefficient(Q, complement, coloring):
                active = True
                break
        assert active, (u, v, a, b)

    ranks = []
    for vertex in VERTICES:
        columns, matrix = star_matrix(Q, vertex)
        current_rank = rank(matrix)
        ranks.append(current_rank)
        certificate = KERNEL_CERTIFICATES[vertex]
        vector = [certificate.get(column, 0) for column in columns]
        assert any(vector)
        assert matrix_vector(matrix, vector) == (Fraction(0),) * (2 ** (N - 1))
        assert current_rank < len(columns)

    assert ranks == [8, 7, 8, 7, 8, 9]
    print("verified H(q)=2X+Y on all 64 binary colorings")
    print("verified both off-diagonal cells and all nine cells are tensor-active")
    print("full-star ranks:", ranks, "nullities:", [10 - value for value in ranks])
    print("verified one explicit nonzero kernel vector for every F_i")


if __name__ == "__main__":
    main()
