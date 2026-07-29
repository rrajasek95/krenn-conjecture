#!/usr/bin/env python3
"""Finite smoke audit for the odd near-perfect gadget obstruction.

The proof is uniform; this script independently enumerates every ordered
pairwise edge-disjoint triple at odd orders five and seven, completes the
three near-one-factors at a new vertex, and checks that a fourth perfect
matching exists and that each induced colored fiber is a singleton.
"""

from __future__ import annotations

import itertools


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((min(first, second), max(first, second)),) + tail))


def near_matchings(n: int, exposed: int):
    vertices = tuple(vertex for vertex in range(n) if vertex != exposed)
    return tuple(perfect_matchings(vertices))


def audit(n: int) -> None:
    infinity = n
    families = tuple(near_matchings(n, terminal) for terminal in range(3))
    triples = 0
    for near in itertools.product(*families):
        edge_sets = tuple(set(matching) for matching in near)
        if any(edge_sets[r] & edge_sets[s] for r in range(3) for s in range(r + 1, 3)):
            continue
        triples += 1
        colored_edge: dict[tuple[int, int], int] = {}
        bases = []
        for color in range(3):
            external = (color, infinity)
            matching = tuple(sorted(near[color] + (external,)))
            bases.append(matching)
            for edge in matching:
                assert edge not in colored_edge
                colored_edge[edge] = color

        union_matchings = tuple(
            matching
            for matching in perfect_matchings(tuple(range(n + 1)))
            if all(edge in colored_edge for edge in matching)
        )
        mixed = tuple(matching for matching in union_matchings if matching not in bases)
        assert mixed

        def induced_coloring(matching):
            coloring = [-1] * (n + 1)
            for edge in matching:
                color = colored_edge[edge]
                for vertex in edge:
                    coloring[vertex] = color
            assert all(color >= 0 for color in coloring)
            return tuple(coloring)

        fibers: dict[tuple[int, ...], list[tuple[tuple[int, int], ...]]] = {}
        for matching in union_matchings:
            fibers.setdefault(induced_coloring(matching), []).append(matching)
        assert all(len(fibers[induced_coloring(matching)]) == 1 for matching in mixed)

    assert triples > 0
    print(f"VERIFIED n={n}: disjoint ordered triples={triples}")


def main() -> None:
    for n in (5, 7):
        audit(n)


if __name__ == "__main__":
    main()
