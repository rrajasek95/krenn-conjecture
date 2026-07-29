#!/usr/bin/env python3
"""Verify the singleton coefficients in the prism-plus-skew-cycle lemma.

The nine prism edges have the three same-color perfect matchings used in
notes/local-algebra.md.  Every complementary edge is allowed precisely the
six off-diagonal ordered color pairs.  For either alternating perfect
matching of the complementary C6, and for every choice of one unordered
pair-type on each of its three edges, this script verifies that some choice
of orientations gives a coloring supported by that perfect matching only.
"""

from itertools import combinations, product


VERTICES = tuple(range(6))
PAIR_TYPES = ((0, 1), (0, 2), (1, 2))

PRISM = {
    (0, 4): 0,
    (1, 2): 0,
    (3, 5): 0,
    (0, 5): 1,
    (1, 4): 1,
    (2, 3): 1,
    (0, 3): 2,
    (1, 5): 2,
    (2, 4): 2,
}

ALTERNATING_MATCHINGS = (
    ((0, 1), (2, 5), (3, 4)),
    ((0, 2), (1, 3), (4, 5)),
)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for v in vertices[1:]:
        rest = tuple(x for x in vertices if x not in (u, v))
        for matching in perfect_matchings(rest):
            yield ((u, v),) + matching


MATCHINGS = tuple(perfect_matchings(VERTICES))


def edge_supports(edge: tuple[int, int], coloring: tuple[int, ...]) -> bool:
    """Full chart support: fixed diagonal on the prism, off-diagonal on C6."""
    u, v = edge
    if edge in PRISM:
        return coloring[u] == coloring[v] == PRISM[edge]
    return coloring[u] != coloring[v]


def compatible_matchings(coloring: tuple[int, ...]):
    return tuple(
        matching
        for matching in MATCHINGS
        if all(edge_supports(edge, coloring) for edge in matching)
    )


def oriented_coloring(matching, pair_types, orientation):
    coloring = [None] * 6
    for (u, v), pair_type, bit in zip(matching, pair_types, orientation):
        ordered = pair_type if bit == 0 else pair_type[::-1]
        coloring[u], coloring[v] = ordered
    return tuple(coloring)


for matching in ALTERNATING_MATCHINGS:
    for pair_types in product(PAIR_TYPES, repeat=3):
        witnesses = []
        for orientation in product((0, 1), repeat=3):
            coloring = oriented_coloring(matching, pair_types, orientation)
            if compatible_matchings(coloring) == (matching,):
                witnesses.append((orientation, coloring))
        assert witnesses, (matching, pair_types)

print("verified 2 * 3^3 singleton pair-type triples")

