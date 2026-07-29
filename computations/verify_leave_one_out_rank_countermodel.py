#!/usr/bin/env python3
"""Exact audit of the leave-one-out rank/anchor countermodel.

The matrices below are not claimed to realize ternary equality.  They audit
the package of necessary *local* consequences currently available from the
two-vertex annihilation identities, forced anchors, cofactor activity, and
entry-minimal star irredundancy.
"""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp


N = 6
Q = 3
VERTICES = tuple(range(N))
EDGES = tuple(combinations(VERTICES, 2))

PAIRS = ((0, 2), (1, 4), (3, 5))
PAIR_OF = {vertex: index for index, pair in enumerate(PAIRS) for vertex in pair}
INVERTIBLE_EDGES = {tuple(sorted(pair)) for pair in PAIRS}

# L[(X,u)] is the coordinate factor at u on both edges from the two
# vertices of matched pair X to u.
L = {
    (0, 1): 1,
    (0, 3): 0,
    (0, 4): 2,
    (0, 5): 2,
    (1, 0): 0,
    (1, 2): 1,
    (1, 3): 2,
    (1, 5): 1,
    (2, 0): 1,
    (2, 1): 0,
    (2, 2): 0,
    (2, 4): 2,
}


def build_edges():
    answer = {}
    for u, v in EDGES:
        matrix = sp.zeros(Q, Q)
        if (u, v) in INVERTIBLE_EDGES:
            matrix = sp.eye(Q)
        else:
            row = L[PAIR_OF[v], u]
            column = L[PAIR_OF[u], v]
            matrix[row, column] = 1
        answer[u, v] = matrix
    return answer


A = build_edges()


def oriented(u, v):
    return A[u, v] if u < v else A[v, u].T


K = []
for omitted in range(Q):
    other = [color for color in range(Q) if color != omitted]
    matrix = sp.zeros(Q, Q)
    matrix[other[0], other[1]] = 1
    matrix[other[1], other[0]] = -1
    K.append(matrix)


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


def matching_tensor(vertices):
    vertices = tuple(vertices)
    answer = {}
    for coloring in product(range(Q), repeat=len(vertices)):
        colors = dict(zip(vertices, coloring))
        value = sp.Integer(0)
        for matching in perfect_matchings(vertices):
            value += sp.prod(
                oriented(u, v)[colors[u], colors[v]] for u, v in matching
            )
        if value:
            answer[coloring] = value
    return answer


def is_left_factor(matrix, coordinate):
    """Test matrix = e_coordinate d^T for some d (including d=0)."""
    return all(
        matrix[row, column] == 0
        for row in range(Q)
        if row != coordinate
        for column in range(Q)
    )


def is_right_factor(matrix, coordinate):
    """Test matrix = c e_coordinate^T for some c (including c=0)."""
    return all(
        matrix[row, column] == 0
        for column in range(Q)
        if column != coordinate
        for row in range(Q)
    )


# Exactly a perfect matching of blocks is invertible; all other blocks are
# nonzero singleton rank-one matrices.
assert {edge for edge, matrix in A.items() if matrix.rank() == 3} == INVERTIBLE_EDGES
assert all(
    matrix.rank() == 1 for edge, matrix in A.items() if edge not in INVERTIBLE_EDGES
)

# Corollary 5.2 and Theorem 6.1 of the annihilation note hold in a much
# stronger form: every outside vertex is a zero witness in every color for
# every invertible edge.
for p, q in INVERTIBLE_EDGES:
    outside = [u for u in VERTICES if u not in (p, q)]
    union_of_witnesses = set()
    for color in range(Q):
        witnesses = []
        for u in outside:
            cross_matrix = oriented(p, u) * K[color] * oriented(q, u).T
            if cross_matrix == sp.zeros(Q, Q):
                witnesses.append(u)
                union_of_witnesses.add(u)

                # The advertised off-color rank inequality is exact too.
                off = [s for s in range(Q) if s != color]
                assert (
                    oriented(p, u)[:, off].rank()
                    + oriented(q, u)[:, off].rank()
                    <= 2
                )
        assert witnesses == outside
    assert len(union_of_witnesses) == 4 >= 3

# Audit the factor-allocation conclusions for every ordered rank-one edge.
# If A_pq=a b^T and a is not e_r, at least two C_u,r have left factor a;
# the symmetric right-factor assertion is checked independently.
for p, q in product(VERTICES, repeat=2):
    if p == q or oriented(p, q).rank() != 1:
        continue
    matrix = oriented(p, q)
    nonzero = [
        (row, column)
        for row, column in product(range(Q), repeat=2)
        if matrix[row, column]
    ]
    assert len(nonzero) == 1
    left_coordinate, right_coordinate = nonzero[0]
    for color in range(Q):
        cross_matrices = [
            oriented(p, u) * K[color] * oriented(q, u).T
            for u in VERTICES
            if u not in (p, q)
        ]
        if color != left_coordinate:
            assert sum(
                is_left_factor(cross_matrix, left_coordinate)
                for cross_matrix in cross_matrices
            ) >= 2
        if color != right_coordinate:
            assert sum(
                is_right_factor(cross_matrix, right_coordinate)
                for cross_matrix in cross_matrices
            ) >= 2

# Every edge has a genuinely nonzero complementary matching tensor.  The
# entries are nonnegative integers, so the checker also rules out a hidden
# cancellation in this activity assertion.
COFACTORS = {
    edge: matching_tensor(v for v in VERTICES if v not in edge) for edge in EDGES
}
assert all(COFACTORS[edge] for edge in EDGES)
assert all(value > 0 for tensor in COFACTORS.values() for value in tensor.values())

# Every ordered vertex/color has a directed active rank-one anchor whose
# factor at the opposite endpoint is the requested coordinate vector.
for p in VERTICES:
    for color in range(Q):
        anchors = []
        for u in VERTICES:
            if u == p:
                continue
            matrix = oriented(p, u)
            if (
                matrix.rank() == 1
                and is_right_factor(matrix, color)
                and any(matrix[:, color])
                and COFACTORS[tuple(sorted((p, u)))]
            ):
                anchors.append(u)
        assert anchors

# Finally audit the exact local-irredundancy condition supplied by an
# entry-minimal representative.  Each star has seven nonzero cells.  Its
# seven global contribution tensors are columns in the coloring basis and
# have rank seven over Q.  In fact each selected minor is unimodular.
minor_determinants = []
for p in VERTICES:
    columns = []
    for u in VERTICES:
        if u == p:
            continue
        matrix = oriented(p, u)
        edge = tuple(sorted((p, u)))
        remaining = [v for v in VERTICES if v not in edge]
        for left_color, right_color in product(range(Q), repeat=2):
            if matrix[left_color, right_color] == 0:
                continue
            atom = {}
            for coloring, coefficient in COFACTORS[edge].items():
                full = [None] * N
                full[p] = left_color
                full[u] = right_color
                for vertex, color in zip(remaining, coloring):
                    full[vertex] = color
                atom[tuple(full)] = coefficient
            columns.append(atom)

    assert len(columns) == 7
    rows = sorted(set().union(*(column.keys() for column in columns)))
    matrix = sp.Matrix(
        [[column.get(coloring, 0) for column in columns] for coloring in rows]
    )
    pivot_rows = matrix.T.rref()[1]
    assert len(pivot_rows) == 7
    determinant = matrix[list(pivot_rows), :].det()
    assert abs(determinant) == 1
    minor_determinants.append(determinant)

assert minor_determinants == [-1, 1, 1, -1, -1, -1]

print("verified three invertible blocks and twelve rank-one blocks")
print("verified all invertible- and rank-one-edge witness constraints")
print("verified active anchors and nonzero cofactors at every edge")
print("verified six unimodular rank-seven star contribution systems")
