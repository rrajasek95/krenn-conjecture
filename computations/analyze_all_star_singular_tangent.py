#!/usr/bin/env python3
"""Tangent-space audit for the all-star-singular binary incidence variety.

At the dense rational six-site base from
``notes/dense-diagonal-collision-spin-obstruction.md`` we impose

    H(q) = 2 X + Y,
    k_i H_{B minus {i}}(q) = 0  for every i,

where one nonzero kernel vector ``k_i`` is retained at each deleted star.
The script computes the exact Jacobian and reports whether infinitesimal
deformations can introduce off-diagonal binary cells.  This is a discovery
calculation, not a proof of global rigidity.
"""

from __future__ import annotations

import itertools

import sympy as sp


N = 6
COLORS = (0, 1)
EDGES = tuple(itertools.combinations(range(N), 2))
Q_VARS = tuple((u, v, a, b) for u, v in EDGES for a in COLORS for b in COLORS)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings(range(N)))


def dense_base():
    h = ((1, 1), (1, -1))
    answer = {}
    blocks = ((0, 1), (2, 3), (4, 5))
    scales = (sp.Rational(-1, 2), sp.Integer(1), sp.Integer(1))
    for (left, right), scale in zip(itertools.combinations(blocks, 2), scales):
        for row, u in enumerate(left):
            for column, v in enumerate(right):
                answer[(u, v, 0, 0)] = scale * h[row][column]
    for edge in blocks:
        answer[edge + (1, 1)] = sp.Integer(1)
    return answer


def cofactor(q, removed, coloring):
    vertices = tuple(v for v in range(N) if v not in removed)
    total = sp.Integer(0)
    for matching in perfect_matchings(vertices):
        total += sp.prod(q.get(edge + (coloring[edge[0]], coloring[edge[1]]), 0)
                         for edge in matching)
    return sp.expand(total)


def star_matrix(q, vertex):
    columns = []
    for other in range(N):
        if other == vertex:
            continue
        for color in COLORS:
            columns.append((other, color))
    rows = []
    for tail in itertools.product(COLORS, repeat=N - 1):
        coloring = list(tail)
        coloring.insert(vertex, None)
        row = []
        for other, color in columns:
            if coloring[other] != color:
                row.append(0)
            else:
                row.append(cofactor(q, {vertex, other}, coloring))
        rows.append(row)
    return columns, sp.Matrix(rows)


def matching_value(q, coloring):
    return sum(
        sp.prod(q.get(edge + (coloring[edge[0]], coloring[edge[1]]), 0)
                for edge in matching)
        for matching in MATCHINGS
    )


def main():
    q = dense_base()
    kernels = {}
    star_columns = {}
    for vertex in range(N):
        columns, matrix = star_matrix(q, vertex)
        kernel = matrix.nullspace()
        assert len(kernel) == 1, (vertex, len(kernel))
        kernels[vertex] = kernel[0]
        star_columns[vertex] = columns

    # Variables are all q entries followed by the ten coordinates of k_i.
    q_index = {key: index for index, key in enumerate(Q_VARS)}
    offset = len(Q_VARS)
    k_index = {}
    for vertex in range(N):
        for position, column in enumerate(star_columns[vertex]):
            k_index[(vertex,) + column] = offset
            offset += 1
    variable_count = offset
    rows = []

    # Linearization of the 64 base equations.
    for coloring in itertools.product(COLORS, repeat=N):
        row = [sp.Integer(0)] * variable_count
        for key, column in q_index.items():
            u, v, a, b = key
            if coloring[u] == a and coloring[v] == b:
                row[column] = cofactor(q, {u, v}, coloring)
        rows.append(row)

    # Linearization of M_i(q) k_i = 0.  The q derivative is obtained by
    # deleting the tangent companion edge and one further base edge.
    for vertex in range(N):
        columns = star_columns[vertex]
        kernel = kernels[vertex]
        for tail in itertools.product(COLORS, repeat=N - 1):
            coloring = list(tail)
            coloring.insert(vertex, None)
            row = [sp.Integer(0)] * variable_count
            for position, (other, color) in enumerate(columns):
                if coloring[other] != color:
                    continue
                kval = kernel[position]
                row[k_index[(vertex, other, color)]] += cofactor(
                    q, {vertex, other}, coloring
                )
                if kval == 0:
                    continue
                for u, v in EDGES:
                    if vertex in (u, v) or other in (u, v):
                        continue
                    a, b = coloring[u], coloring[v]
                    row[q_index[(u, v, a, b)]] += kval * cofactor(
                        q, {vertex, other, u, v}, coloring
                    )
            rows.append(row)

    jacobian = sp.Matrix(rows)
    rank = jacobian.rank()
    nullspace = jacobian.nullspace()
    print(f"jacobian={jacobian.rows}x{jacobian.cols} rank={rank} nullity={len(nullspace)}")

    offdiag = [q_index[key] for key in Q_VARS if key[2] != key[3]]
    projected = sp.Matrix([[vector[index] for vector in nullspace] for index in offdiag])
    projected_rank = projected.rank()
    print(f"offdiagonal-q projection rank={projected_rank} of {len(offdiag)} coordinates")
    if projected_rank:
        _, pivots = projected.rref()
        vector = nullspace[pivots[0]]
        support = [
            (key, sp.factor(vector[q_index[key]]))
            for key in Q_VARS
            if key[2] != key[3] and vector[q_index[key]] != 0
        ]
        print("first offdiagonal tangent support:")
        for item in support:
            print(item)

    # Sanity check the retained incidence point.
    for coloring in itertools.product(COLORS, repeat=N):
        expected = 2 if not any(coloring) else 1 if all(coloring) else 0
        assert matching_value(q, coloring) == expected
    for vertex in range(N):
        _, matrix = star_matrix(q, vertex)
        assert matrix * kernels[vertex] == sp.zeros(matrix.rows, 1)


if __name__ == "__main__":
    main()
