#!/usr/bin/env python3
"""Exact support audit for prism plus adjacent complement edges 01 and 13."""

from itertools import product


EDGES = (
    (0, 4), (1, 2), (2, 3), (2, 4),
    (1, 4), (0, 5), (1, 5), (3, 5),
)
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
PURE_MATCHINGS = (
    ((0, 4), (1, 2), (3, 5)),
    ((0, 4), (1, 5), (2, 3)),
    ((0, 5), (1, 4), (2, 3)),
)
CUBIC_VERTICES = (2, 4, 5)


def proper(edge_colors):
    return all(
        len({
            edge_colors[index]
            for index, edge in enumerate(EDGES)
            if vertex in edge
        }) == 3
        for vertex in CUBIC_VERTICES
    )


def coloring(matching, edge_colors):
    result = [None] * 6
    for edge in matching:
        color = edge_colors[EDGE_INDEX[edge]]
        result[edge[0]] = result[edge[1]] = color
    return tuple(result)


def arbitrary_triangle_supports(candidate, edge_colors):
    """Every matching using 01, 03, or 13 contains the forced edge 24."""
    color_24 = edge_colors[EDGE_INDEX[(2, 4)]]
    return candidate[2] == candidate[4] == color_24


checked = 0
for edge_colors in product(range(3), repeat=len(EDGES)):
    if not proper(edge_colors):
        continue
    checked += 1
    pure = [coloring(matching, edge_colors) for matching in PURE_MATCHINGS]
    for index, candidate in enumerate(pure):
        if len(set(candidate)) == 1:
            continue
        if arbitrary_triangle_supports(candidate, edge_colors):
            continue
        assert pure.count(candidate) > 1 or index >= 0
        # Exact audit below checks the stronger statement used in the proof:
        # at least one mixed pure coloring is unique and off the slice.
    bad = [
        candidate
        for candidate in pure
        if len(set(candidate)) > 1
        and not arbitrary_triangle_supports(candidate, edge_colors)
        and pure.count(candidate) == 1
    ]
    assert bad, edge_colors

assert checked == 216
print(
    "verified: all 216 proper colorings of the eight forced edges have a "
    "unique mixed pure-matching coefficient off the arbitrary-matrix slice"
)
