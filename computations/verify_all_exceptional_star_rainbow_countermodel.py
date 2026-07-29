#!/usr/bin/env python3
"""Exact all-exceptional fixed-star countermodel to binary-face arguments.

Three one-factors of K6 have pairwise Hamilton unions.  Their nine unit
same-colour cells give every constant coefficient and every two-colour GHZ
restriction exactly, but their union has one additional rainbow matching.
At every fixed star, two of the three full common-power row equations hold;
the third fails in exactly the restriction of that one rainbow word.
Every internal rank-three graph is empty, so every star lies on the graph-
exceptional side of the three-hole gauge dichotomy.
"""

from __future__ import annotations

import itertools


VERTICES = tuple(range(6))
COLORS = (0, 1, 2)
FACTORS = (
    frozenset({(0, 1), (2, 3), (4, 5)}),
    frozenset({(1, 2), (3, 4), (0, 5)}),
    frozenset({(0, 3), (1, 5), (2, 4)}),
)
RAINBOW = frozenset({(0, 3), (1, 2), (4, 5)})
RAINBOW_WORD = (2, 1, 1, 2, 0, 0)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def source():
    result = {}
    for color, matching in enumerate(FACTORS):
        for edge in matching:
            result[edge] = {(color, color): 1}
    return result


def entry(edges, u: int, v: int, a: int, b: int) -> int:
    if u < v:
        return edges.get((u, v), {}).get((a, b), 0)
    return edges.get((v, u), {}).get((b, a), 0)


def matching_tensor(vertices: tuple[int, ...], edges):
    result = {}
    matchings = tuple(perfect_matchings(vertices))
    for coloring in itertools.product(COLORS, repeat=len(vertices)):
        local = dict(zip(vertices, coloring, strict=True))
        value = 0
        for matching in matchings:
            term = 1
            for u, v in matching:
                term *= entry(edges, u, v, local[u], local[v])
            value += term
        if value:
            result[coloring] = value
    return result


def insert(coloring, vertices, site, color):
    local = dict(zip(vertices, coloring, strict=True))
    return tuple(color if vertex == site else local[vertex] for vertex in VERTICES)


def fixed_star_row(edges, p: int, color: int):
    """Compute z_(p,color) q_p^2/2 from the actual common internal q_p."""
    j = next(
        vertex
        for edge in FACTORS[color]
        if p in edge
        for vertex in edge
        if vertex != p
    )
    complement = tuple(vertex for vertex in VERTICES if vertex not in (p, j))
    cofactor = matching_tensor(complement, edges)
    remaining = tuple(vertex for vertex in VERTICES if vertex != p)
    result = {}
    for coloring, value in cofactor.items():
        local = dict(zip(complement, coloring, strict=True))
        output = tuple(color if vertex == j else local[vertex] for vertex in remaining)
        result[output] = result.get(output, 0) + value
    return result


def is_cycle(edge_set) -> bool:
    adjacency = {vertex: set() for vertex in VERTICES}
    for u, v in edge_set:
        adjacency[u].add(v)
        adjacency[v].add(u)
    if any(len(neighbors) != 2 for neighbors in adjacency.values()):
        return False
    seen = {VERTICES[0]}
    frontier = [VERTICES[0]]
    while frontier:
        vertex = frontier.pop()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                frontier.append(neighbor)
    return len(seen) == len(VERTICES)


def main() -> None:
    edges = source()
    assert len(edges) == 9
    assert all(is_cycle(FACTORS[a] | FACTORS[b]) for a, b in itertools.combinations(COLORS, 2))

    supported = {
        frozenset(tuple(sorted(edge)) for edge in matching)
        for matching in perfect_matchings(VERTICES)
        if all(tuple(sorted(edge)) in edges for edge in matching)
    }
    assert supported == set(FACTORS) | {RAINBOW}

    tensor = matching_tensor(VERTICES, edges)
    expected = {(color,) * 6: 1 for color in COLORS}
    expected[RAINBOW_WORD] = 1
    assert tensor == expected

    # Every binary face is exactly binary GHZ; the only contamination uses
    # all three colors.
    for a, b in itertools.combinations(COLORS, 2):
        face = {
            coloring: value
            for coloring, value in tensor.items()
            if set(coloring) <= {a, b}
        }
        assert face == {(a,) * 6: 1, (b,) * 6: 1}

    # Audit the actual common-power fixed-star equations.  At p, precisely
    # the row whose color is RAINBOW_WORD[p] contains the extra restricted
    # rainbow word; the other two rows equal their pure targets exactly.
    for p in VERTICES:
        remaining = tuple(vertex for vertex in VERTICES if vertex != p)
        restricted_rainbow = tuple(RAINBOW_WORD[vertex] for vertex in remaining)
        for color in COLORS:
            row = fixed_star_row(edges, p, color)
            target = {(color,) * 5: 1}
            if color == RAINBOW_WORD[p]:
                target[restricted_rainbow] = 1
            assert row == target, (p, color, row)

    # Every internal aggregate edge has matrix rank at most one, so every
    # rank-three graph in every fixed-star deletion is empty.
    assert all(len(matrix) == 1 for matrix in edges.values())

    # Each cell is indispensable even for the retained constant/binary-face
    # constraints: it lies in the unique pure matching of its color.
    for edge, matrix in edges.items():
        reduced = dict(edges)
        del reduced[edge]
        reduced_tensor = matching_tensor(VERTICES, reduced)
        color = next(iter(matrix))[0]
        assert reduced_tensor.get((color,) * 6, 0) == 0

    print("three pairwise-Hamilton one-factors and four supported matchings: PASS")
    print("H_6 = Delta_(6,3) + e_211200")
    print("all three binary faces exact; every fixed star has exactly one failing row")
    print("all deleted rank-three graphs empty; every one of nine cells indispensable")


if __name__ == "__main__":
    main()
