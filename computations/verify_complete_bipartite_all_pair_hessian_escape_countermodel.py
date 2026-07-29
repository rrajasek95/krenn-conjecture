#!/usr/bin/env python3
"""Exact audit of the all-pair complete-bipartite escape countermodel."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations
from math import factorial


D = (
    (Fraction(1), Fraction(1), Fraction(1)),
    (Fraction(1), Fraction(2), Fraction(4)),
    (Fraction(1), Fraction(3), Fraction(9)),
)
COLORS = range(3)


def determinant_3(matrix) -> Fraction:
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in COLORS) for i in COLORS)


def matrix_rank(matrix) -> int:
    rows = [list(row) for row in matrix]
    if not rows:
        return 0
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        value = rows[rank][column]
        rows[rank] = [entry / value for entry in rows[rank]]
        for i in range(len(rows)):
            if i == rank or rows[i][column] == 0:
                continue
            value = rows[i][column]
            rows[i] = [a - value * b for a, b in zip(rows[i], rows[rank], strict=True)]
        rank += 1
        if rank == len(rows):
            break
    return rank


def data(order: int):
    assert order % 2 == 0 and order >= 6
    s = order // 2
    left = tuple(range(s))
    right = tuple(range(s, 2 * s))
    diagonals = tuple(D[c][c] for c in COLORS)
    scales = tuple(Fraction(1, factorial(s) * diagonals[c] ** s) for c in COLORS)
    scaled = tuple(tuple(scales[i] * D[i][j] for j in COLORS) for i in COLORS)
    zero = tuple(tuple(Fraction(0) for _ in COLORS) for _ in COLORS)

    def stored_block(u: int, v: int):
        assert u < v
        if u in left and v in right:
            return scaled if u == 0 else D
        return zero

    def oriented_block(endpoint: int, neighbor: int):
        u, v = sorted((endpoint, neighbor))
        block = stored_block(u, v)
        return block if endpoint == u else transpose(block)

    return s, left, right, scales, stored_block, oriented_block


def connected(vertices, edges) -> bool:
    vertices = set(vertices)
    if not vertices:
        return True
    adjacency = {u: set() for u in vertices}
    for u, v in edges:
        if u in vertices and v in vertices:
            adjacency[u].add(v)
            adjacency[v].add(u)
    seen = set()
    stack = [next(iter(vertices))]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        stack.extend(adjacency[u] - seen)
    return seen == vertices


def bipartite(vertices, edges) -> bool:
    adjacency = {u: set() for u in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    colors = {}
    for start in vertices:
        if start in colors:
            continue
        colors[start] = 0
        stack = [start]
        while stack:
            u = stack.pop()
            for v in adjacency[u]:
                if v not in colors:
                    colors[v] = 1 - colors[u]
                    stack.append(v)
                elif colors[v] == colors[u]:
                    return False
    return True


def coefficient(order: int, word: tuple[int, ...]) -> Fraction:
    """Enumerate the actual source matchings as left-right bijections."""
    s, left, right, _, stored_block, _ = data(order)
    total = Fraction(0)
    for image in permutations(right):
        product = Fraction(1)
        for u, v in zip(left, image, strict=True):
            product *= stored_block(u, v)[word[u]][word[v]]
        total += product
    assert len(left) == s
    return total


def audit_formulas() -> None:
    assert determinant_3(D) == 2
    assert matrix_rank(D) == 3
    for s in range(3, 31):
        order = 2 * s
        _, _, _, scales, _, _ = data(order)
        for c in COLORS:
            pure = factorial(s) * scales[c] * D[c][c] ** s
            assert pure == 1

        # Pair 0,1 lies in the left shore.  The two named stars choose
        # ordered distinct right sites; the rest are bijected arbitrarily.
        count = s * (s - 1) * factorial(s - 2)
        one_term = scales[0] * D[0][1] * D[1][1] ** (s - 1)
        assert count == factorial(s)
        assert count * one_term == 2 ** (s - 1)


def audit_direct_enumeration() -> None:
    for s in range(3, 7):
        order = 2 * s
        for c in COLORS:
            assert coefficient(order, (c,) * order) == 1
        mixed = (0,) + (1,) * (order - 1)
        assert coefficient(order, mixed) == 2 ** (s - 1)


def audit_all_pair_charts() -> None:
    for s in range(3, 11):
        order = 2 * s
        _, left, right, _, stored_block, oriented_block = data(order)
        vertices = tuple(range(order))
        rank_three_edges = {
            (u, v)
            for u, v in combinations(vertices, 2)
            if matrix_rank(stored_block(u, v)) == 3
        }
        assert rank_three_edges == {(u, v) for u in left for v in right}

        for endpoint in vertices:
            row_supports = []
            for c in COLORS:
                support = {
                    neighbor
                    for neighbor in vertices
                    if neighbor != endpoint
                    and any(oriented_block(endpoint, neighbor)[c][d] for d in COLORS)
                }
                row_supports.append(support)
                assert len(support) == s

            # Reversal is literal, so right-endpoint rows are rows of D^T.
            if endpoint in right:
                neighbor = next(iter(left))
                assert oriented_block(endpoint, neighbor) == transpose(
                    stored_block(neighbor, endpoint)
                )

        for p, q in combinations(vertices, 2):
            internal = tuple(v for v in vertices if v not in (p, q))
            internal_edges = {
                edge for edge in rank_three_edges if edge[0] in internal and edge[1] in internal
            }
            assert connected(internal, internal_edges)
            assert bipartite(internal, internal_edges)

            # A retained invertible block makes each direct-sum star injective.
            for endpoint, deleted in ((p, q), (q, p)):
                retained_ranks = [
                    matrix_rank(oriented_block(endpoint, neighbor))
                    for neighbor in internal
                ]
                assert 3 in retained_ranks


def audit_vertex_connectivity() -> None:
    # Exhaust the defining lower bound kappa(K_s,s) >= s at small orders.
    for s in range(3, 9):
        vertices = tuple(range(2 * s))
        left = set(range(s))
        right = set(range(s, 2 * s))
        edges = {(u, v) for u in left for v in right}
        for removed_size in range(s):
            for removed in combinations(vertices, removed_size):
                remaining = tuple(v for v in vertices if v not in removed)
                assert connected(remaining, edges)

        # Removing an entire shore disconnects the remaining independent set.
        remaining = tuple(sorted(right))
        assert not connected(remaining, edges)


def main() -> None:
    audit_formulas()
    audit_direct_enumeration()
    audit_all_pair_charts()
    audit_vertex_connectivity()
    print("complete-bipartite all-pair Hessian escape countermodel: PASS")
    print("orders audited symbolically: 6..60")
    print("orders enumerated exactly: 6, 8, 10, 12")
    print("all-pair chart audit: 6..20")
    print("vertex-connectivity audit: K_3,3 through K_8,8")


if __name__ == "__main__":
    main()
