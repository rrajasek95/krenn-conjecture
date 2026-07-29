#!/usr/bin/env python3
"""Exact finite audit for the combinatorial case split in the prism+edge proof.

No numerical algebra is used.  The script enumerates the 3^9 colorings of
the prism edges, retains those proper at the four cubic vertices, and checks
that the four nonzero prism matching colorings plus the support of the fifth
matching cannot equal the three monochromatic target coefficients.
"""

from itertools import product


EDGES = (
    (0, 3), (0, 4), (0, 5), (1, 2), (1, 4),
    (1, 5), (2, 3), (2, 4), (3, 5),
)
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
CUBIC_VERTICES = (2, 3, 4, 5)
MATCHINGS = (
    ((0, 3), (1, 5), (2, 4)),
    ((0, 4), (1, 2), (3, 5)),
    ((0, 4), (1, 5), (2, 3)),
    ((0, 5), (1, 4), (2, 3)),
)


def matching_coloring(matching, edge_colors):
    coloring = [None] * 6
    for edge in matching:
        color = edge_colors[EDGE_INDEX[edge]]
        coloring[edge[0]] = color
        coloring[edge[1]] = color
    return tuple(coloring)


def proper_at_cubic_vertices(edge_colors):
    return all(
        len({
            edge_colors[index]
            for index, edge in enumerate(EDGES)
            if vertex in edge
        }) == 3
        for vertex in CUBIC_VERTICES
    )


def fifth_matching_supports(coloring, edge_colors):
    """N={01,24,35}; A_01 is arbitrary, while 24 and 35 are fixed-color."""
    color_24 = edge_colors[EDGE_INDEX[(2, 4)]]
    color_35 = edge_colors[EDGE_INDEX[(3, 5)]]
    return (
        coloring[2] == coloring[4] == color_24
        and coloring[3] == coloring[5] == color_35
    )


def could_equal_target(edge_colors):
    prism_colorings = [
        matching_coloring(matching, edge_colors)
        for matching in MATCHINGS
    ]

    # Every prism monomial is nonzero.  A mixed one must have another term
    # with the same coloring; the only possible fifth term has the support
    # tested above.  Distinct prism colorings could also cancel one another,
    # so compare exact multiplicities conservatively by grouping them.
    groups = {}
    for coloring in prism_colorings:
        groups.setdefault(coloring, 0)
        groups[coloring] += 1

    for coloring, multiplicity in groups.items():
        if len(set(coloring)) > 1 and not fifth_matching_supports(
            coloring, edge_colors
        ):
            # In fact properness makes multiplicity one; assert it explicitly.
            assert multiplicity == 1
            return False

    # Check whether each required constant coloring appears either among the
    # prism terms or in the support of N.  This is only a necessary condition,
    # so failure is an exact impossibility certificate.
    for color in range(3):
        constant = (color,) * 6
        if (
            constant not in groups
            and not fifth_matching_supports(constant, edge_colors)
        ):
            return False
    return True


proper_count = 0
for edge_colors in product(range(3), repeat=len(EDGES)):
    if not proper_at_cubic_vertices(edge_colors):
        continue
    proper_count += 1
    assert not could_equal_target(edge_colors), edge_colors

assert proper_count == 48
print(
    "verified: all 48 prism edge-colorings proper at vertices 2,3,4,5 "
    "are obstructed after adjoining arbitrary pair 01"
)
