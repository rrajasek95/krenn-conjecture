#!/usr/bin/env python3
"""Exact q=2, n=8 obstruction to a scalar pair-cap reduction to n=6.

The source is obtained by subdividing edge 56 in the rational n=6 example
from ``notes/induction-route.md``.  It realizes Delta_(8,2) exactly.  Capping
vertices 1 and 5 by the diagonal covector gives old internal edges X and
first-jet edges R on U=(2,3,4,6,7,8).  The script verifies symbolically that

  H_U(alpha X + beta R)
    = alpha^2 beta e_0^6
      - 3/4 alpha beta^2 e_(0,0,1,0,0,0)
      + alpha^2(2 alpha+3 beta)/4 e_1^6.

Thus no alpha,beta produce a diagonal tensor with both diagonal
coefficients nonzero.
"""

from __future__ import annotations

import itertools

import sympy as sp


Q = 2
VERTICES = tuple(range(1, 9))
U = (2, 3, 4, 6, 7, 8)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def put(
    edges: dict[tuple[int, int], dict[tuple[int, int], sp.Expr]],
    u: int,
    v: int,
    entries: dict[tuple[int, int], sp.Expr | int],
) -> None:
    assert u < v
    edges[u, v] = {cell: sp.sympify(value) for cell, value in entries.items()}


def edge_entry(
    edges: dict[tuple[int, int], dict[tuple[int, int], sp.Expr]],
    u: int,
    v: int,
    color_u: int,
    color_v: int,
) -> sp.Expr:
    if u < v:
        return edges.get((u, v), {}).get((color_u, color_v), sp.S.Zero)
    return edges.get((v, u), {}).get((color_v, color_u), sp.S.Zero)


def matching_tensor(
    vertices: tuple[int, ...],
    edges: dict[tuple[int, int], dict[tuple[int, int], sp.Expr]],
) -> dict[tuple[int, ...], sp.Expr]:
    answer: dict[tuple[int, ...], sp.Expr] = {}
    matchings = tuple(perfect_matchings(vertices))
    for coloring in itertools.product(range(Q), repeat=len(vertices)):
        local_color = dict(zip(vertices, coloring, strict=True))
        coefficient = sp.S.Zero
        for matching in matchings:
            monomial = sp.S.One
            for u, v in matching:
                monomial *= edge_entry(
                    edges, u, v, local_color[u], local_color[v]
                )
            coefficient += monomial
        coefficient = sp.factor(coefficient)
        if coefficient != 0:
            answer[coloring] = coefficient
    return answer


def source() -> dict[tuple[int, int], dict[tuple[int, int], sp.Expr]]:
    edges: dict[tuple[int, int], dict[tuple[int, int], sp.Expr]] = {}
    put(edges, 1, 2, {(0, 0): 1, (1, 0): 1})
    put(edges, 3, 4, {(0, 0): 1})
    put(edges, 2, 4, {(0, 0): 1})
    put(edges, 1, 3, {(1, 0): -1})
    put(edges, 1, 6, {(1, 1): 1})
    put(edges, 2, 3, {(1, 1): 1})
    put(edges, 4, 5, {(1, 1): sp.Rational(3, 4)})
    put(edges, 1, 5, {(1, 1): sp.Rational(1, 2)})
    put(edges, 4, 6, {(1, 1): sp.Rational(1, 2)})

    # Subdivide the old color-0 edge 56 by the path 5-7-8-6.  Matchings
    # formerly using 56 use 57 and 68, while all others use the color-1
    # internal edge 78.
    put(edges, 5, 7, {(0, 0): 1})
    put(edges, 6, 8, {(0, 0): 1})
    put(edges, 7, 8, {(1, 1): 1})
    return edges


def pair_cap(
    edges: dict[tuple[int, int], dict[tuple[int, int], sp.Expr]],
    p: int,
    q: int,
) -> tuple[
    sp.Expr,
    dict[tuple[int, int], dict[tuple[int, int], sp.Expr]],
    dict[tuple[int, int], dict[tuple[int, int], sp.Expr]],
]:
    """Return s, internal X, and effective R for K=sum_i e_i^* tensor e_i^*."""

    remaining = tuple(vertex for vertex in VERTICES if vertex not in (p, q))
    scalar = sum(edge_entry(edges, p, q, color, color) for color in range(Q))
    internal = {
        edge: dict(matrix)
        for edge, matrix in edges.items()
        if edge[0] in remaining and edge[1] in remaining
    }
    effective: dict[tuple[int, int], dict[tuple[int, int], sp.Expr]] = {}

    for a, b in itertools.combinations(remaining, 2):
        matrix: dict[tuple[int, int], sp.Expr] = {}
        for color_a, color_b in itertools.product(range(Q), repeat=2):
            value = sp.S.Zero
            for cap_color in range(Q):
                value += edge_entry(edges, p, a, cap_color, color_a) * edge_entry(
                    edges, q, b, cap_color, color_b
                )
                value += edge_entry(edges, p, b, cap_color, color_b) * edge_entry(
                    edges, q, a, cap_color, color_a
                )
            if value != 0:
                matrix[color_a, color_b] = sp.factor(value)
        if matrix:
            effective[a, b] = matrix
    return sp.factor(scalar), internal, effective


def main() -> None:
    edges = source()
    assert matching_tensor(VERTICES, edges) == {
        (0,) * 8: sp.S.One,
        (1,) * 8: sp.S.One,
    }

    scalar, internal, effective = pair_cap(edges, 1, 5)
    assert scalar == sp.Rational(1, 2)
    assert effective == {
        (2, 4): {(0, 1): sp.Rational(3, 4)},
        (2, 7): {(0, 0): sp.S.One},
        (3, 4): {(0, 1): -sp.Rational(3, 4)},
        (4, 6): {(1, 1): sp.Rational(3, 4)},
    }

    alpha, beta = sp.symbols("alpha beta")
    combined: dict[tuple[int, int], dict[tuple[int, int], sp.Expr]] = {}
    for edge in set(internal) | set(effective):
        matrix: dict[tuple[int, int], sp.Expr] = {}
        for cell in set(internal.get(edge, {})) | set(effective.get(edge, {})):
            matrix[cell] = sp.factor(
                alpha * internal.get(edge, {}).get(cell, 0)
                + beta * effective.get(edge, {}).get(cell, 0)
            )
        combined[edge] = matrix

    expected = {
        (0, 0, 0, 0, 0, 0): alpha**2 * beta,
        (0, 0, 1, 0, 0, 0): -sp.Rational(3, 4) * alpha * beta**2,
        (1, 1, 1, 1, 1, 1): alpha**2 * (2 * alpha + 3 * beta) / 4,
    }
    assert matching_tensor(U, combined) == {
        coloring: sp.factor(value) for coloring, value in expected.items()
    }

    print("verified exact Delta_(8,2) source and non-closable 1,5 pair cap")
    for coloring, coefficient in expected.items():
        print("".join(map(str, coloring)), "=", sp.factor(coefficient))


if __name__ == "__main__":
    main()
