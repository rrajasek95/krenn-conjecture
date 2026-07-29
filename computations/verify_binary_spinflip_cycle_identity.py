#!/usr/bin/env python3
"""Exact audit of the binary spin-flip / alternating-cycle identity.

For a binary matching tensor H and the alternating form epsilon on C^2,
<H,H> expands over ordered pairs of perfect matchings.  The contraction for
one pair factors over the alternating-cycle components of their union.  This
script checks both descriptions over the integers at n=6 and also checks the
normalization <Delta_(6,2)(1,lambda), Delta_(6,2)(1,lambda)>=2 lambda.
"""

from __future__ import annotations

import itertools


N = 6
VERTICES = tuple(range(N))
EDGES = tuple((u, v) for u in VERTICES for v in range(u + 1, N))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for pos in range(1, len(vertices)):
        v = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for matching in perfect_matchings(rest):
            yield ((u, v),) + matching


PM = tuple(perfect_matchings(VERTICES))


def edge_value(matrices, edge, coloring):
    u, v = edge
    return matrices[edge][coloring[u]][coloring[v]]


def matching_tensor_coefficient(matrices, matching, coloring):
    answer = 1
    for edge in matching:
        answer *= edge_value(matrices, edge, coloring)
    return answer


def hafnian_tensor(matrices):
    return {
        coloring: sum(
            matching_tensor_coefficient(matrices, matching, coloring)
            for matching in PM
        )
        for coloring in itertools.product((0, 1), repeat=N)
    }


def spin_flip(tensor):
    """Contraction against epsilon^(tensor N), epsilon_01=1."""
    answer = 0
    for coloring, value in tensor.items():
        complement = tuple(1 - bit for bit in coloring)
        answer += (-1) ** sum(coloring) * value * tensor[complement]
    return answer


def matching_pair_contraction(matrices, left, right, vertices=VERTICES):
    """Direct epsilon contraction of two matching-product tensors."""
    answer = 0
    for coloring_on_vertices in itertools.product((0, 1), repeat=len(vertices)):
        coloring = dict(zip(vertices, coloring_on_vertices))
        complement = {v: 1 - coloring[v] for v in vertices}
        left_value = 1
        right_value = 1
        for edge in left:
            u, v = edge
            left_value *= matrices[edge][coloring[u]][coloring[v]]
        for edge in right:
            u, v = edge
            right_value *= matrices[edge][complement[u]][complement[v]]
        answer += (-1) ** sum(coloring_on_vertices) * left_value * right_value
    return answer


def union_components(left, right):
    adjacency = {v: set() for v in VERTICES}
    for u, v in set(left) | set(right):
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(VERTICES)
    answer = []
    while unseen:
        root = min(unseen)
        stack = [root]
        component = set()
        while stack:
            v = stack.pop()
            if v in component:
                continue
            component.add(v)
            stack.extend(adjacency[v] - component)
        unseen -= component
        answer.append(tuple(sorted(component)))
    return tuple(answer)


def component_factor(matrices, left, right, component):
    vertices = set(component)
    left_part = tuple(edge for edge in left if edge[0] in vertices)
    right_part = tuple(edge for edge in right if edge[0] in vertices)
    return matching_pair_contraction(
        matrices, left_part, right_part, vertices=component
    )


def deterministic_matrices():
    matrices = {}
    for edge_index, edge in enumerate(EDGES, start=1):
        matrices[edge] = (
            (edge_index, edge_index + 1),
            (2 - edge_index, 2 * edge_index + 1),
        )
    return matrices


def verify_general_identity():
    matrices = deterministic_matrices()
    tensor = hafnian_tensor(matrices)
    direct = spin_flip(tensor)

    expanded = 0
    for left in PM:
        for right in PM:
            pair_value = matching_pair_contraction(matrices, left, right)
            factored = 1
            for component in union_components(left, right):
                factored *= component_factor(matrices, left, right, component)
            assert pair_value == factored
            expanded += pair_value
    assert direct == expanded
    print(f"verified general n=6 spin-flip expansion: value={direct}")


def verify_ghz_normalization():
    zero = ((0, 0), (0, 0))
    matrices = {edge: zero for edge in EDGES}
    matching_zero = ((0, 1), (2, 3), (4, 5))
    matching_one = ((1, 2), (3, 4), (0, 5))
    for edge in matching_zero:
        matrices[edge] = ((1, 0), (0, 0))
    for edge in matching_one:
        matrices[edge] = ((0, 0), (0, 1))
    # Scale one all-one edge so that the full coefficient is lambda=7.
    matrices[(0, 5)] = ((0, 0), (0, 7))

    tensor = hafnian_tensor(matrices)
    for coloring, value in tensor.items():
        expected = 1 if not any(coloring) else 7 if all(coloring) else 0
        assert value == expected
    assert spin_flip(tensor) == 14
    print("verified GHZ normalization: lambda=7 and spin-flip=14")


if __name__ == "__main__":
    verify_general_identity()
    verify_ghz_normalization()
