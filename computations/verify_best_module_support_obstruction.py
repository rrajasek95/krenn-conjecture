#!/usr/bin/env python3
"""Combinatorial audit for the arbitrary-matrix obstruction on support U.

Under the cubic-vertex lemma, every edge of U is a nonzero same-color basis
edge and the colors at vertices 1,2,4,5 are proper.  This script verifies the
four perfect matchings and exhausts the resulting finite edge-colorings,
confirming that the four matching colorings can never all be constant.
"""

from __future__ import annotations

import itertools


VERTICES = tuple(range(6))
EDGES = (
    (0, 1), (0, 2), (0, 4), (0, 5), (1, 2),
    (1, 3), (2, 3), (3, 4), (3, 5), (4, 5),
)
CUBIC_VERTICES = (1, 2, 4, 5)


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


def induced_coloring(matching, edge_colors):
    coloring = [None] * len(VERTICES)
    for edge in matching:
        color = edge_colors[edge]
        for vertex in edge:
            coloring[vertex] = color
    return tuple(coloring)


def main():
    support = set(EDGES)
    matchings = tuple(
        matching
        for matching in perfect_matchings(VERTICES)
        if set(matching) <= support
    )
    assert matchings == (
        ((0, 1), (2, 3), (4, 5)),
        ((0, 2), (1, 3), (4, 5)),
        ((0, 4), (1, 2), (3, 5)),
        ((0, 5), (1, 2), (3, 4)),
    )
    assert all(
        sum(vertex in edge for edge in EDGES) == 3
        for vertex in CUBIC_VERTICES
    )
    assert all(any(vertex in edge for vertex in CUBIC_VERTICES) for edge in EDGES)

    proper_assignments = 0
    for values in itertools.product(range(3), repeat=len(EDGES)):
        edge_colors = dict(zip(EDGES, values))
        if any(
            len({edge_colors[edge] for edge in EDGES if vertex in edge}) != 3
            for vertex in CUBIC_VERTICES
        ):
            continue
        proper_assignments += 1
        colorings = tuple(induced_coloring(matching, edge_colors) for matching in matchings)
        assert len(set(colorings)) == len(matchings)
        assert not all(len(set(coloring)) == 1 for coloring in colorings)

    assert proper_assignments > 0
    print(f"verified perfect matchings={len(matchings)}")
    print(f"verified proper cubic-edge colorings={proper_assignments}")
    print("none makes all four matching colorings constant")


if __name__ == "__main__":
    main()
