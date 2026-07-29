#!/usr/bin/env python3
"""Exact audit for the selected-triple/Petersen rewrite barrier.

The construction is not a Krenn counterexample.  It has three exactly
normalized constant fibres and one exactly vanishing selected mixed fibre.
Its purpose is to show that replacing the selected fourth matching by a
cancellation mate can leave the three-one-factor (hence source-epsilon)
sector, even on a 3-connected matching-covered tight-cut-free support.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations


VERTICES = tuple(range(10))

SELECTED = (
    ((0, 1), (2, 3), (4, 9), (5, 6), (7, 8)),
    ((0, 4), (1, 2), (3, 8), (5, 9), (6, 7)),
    ((0, 5), (1, 6), (2, 7), (3, 4), (8, 9)),
)
FOURTH = ((0, 5), (1, 6), (2, 7), (3, 8), (4, 9))
MATE = ((0, 5), (1, 8), (2, 6), (3, 9), (4, 7))
MIXED_COLORING = (2, 2, 2, 1, 0, 2, 2, 2, 1, 0)


def canonical_edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices, edges=None):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position in range(1, len(vertices)):
        v = vertices[position]
        edge = canonical_edge(u, v)
        if edges is not None and edge not in edges:
            continue
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest, edges):
            yield tuple(sorted((edge,) + tail))


def components(vertices, edges):
    unseen = set(vertices)
    answer = []
    while unseen:
        seed = min(unseen)
        component = {seed}
        frontier = [seed]
        unseen.remove(seed)
        while frontier:
            u = frontier.pop()
            for a, b in edges:
                if a == u and b in unseen:
                    unseen.remove(b)
                    component.add(b)
                    frontier.append(b)
                elif b == u and a in unseen:
                    unseen.remove(a)
                    component.add(a)
                    frontier.append(a)
        answer.append(frozenset(component))
    return tuple(answer)


def main() -> None:
    selected_edges = [set(matching) for matching in SELECTED]
    assert all(len(edges) == 5 for edges in selected_edges)
    assert len(set().union(*selected_edges)) == 15
    assert set(FOURTH) <= set().union(*selected_edges)

    # One aggregate coordinate per displayed underlying pair.  Values are
    # triples (left colour, right colour, scalar weight).
    cells = {}
    for color, matching in enumerate(SELECTED):
        for edge in matching:
            cells[edge] = (color, color, 1)
    additions = {
        (1, 8): (2, 1, -1),
        (2, 6): (2, 2, 1),
        (3, 9): (1, 0, 1),
        (4, 7): (0, 2, 1),
    }
    assert not set(additions) & set(cells)
    cells.update(additions)
    assert len(cells) == 19

    def decorated_term(matching, coloring):
        value = 1
        for edge in matching:
            cell = cells.get(edge)
            if cell is None:
                return 0
            left, right, weight = cell
            if (coloring[edge[0]], coloring[edge[1]]) != (left, right):
                return 0
            value *= weight
        return value

    # Enumerate only support-graph matchings; every pair has one cell here.
    support = frozenset(cells)
    support_matchings = tuple(perfect_matchings(VERTICES, support))
    assert len(support_matchings) == 20
    fibres = defaultdict(list)
    for matching in support_matchings:
        coloring = [-1] * len(VERTICES)
        value = 1
        for edge in matching:
            left, right, weight = cells[edge]
            coloring[edge[0]], coloring[edge[1]] = left, right
            value *= weight
        fibres[tuple(coloring)].append((matching, value))

    # All three complete constant coefficients, not merely selected terms,
    # are exactly one and have unique support matchings.
    for color in range(3):
        fibre = fibres[(color,) * len(VERTICES)]
        assert fibre == [(SELECTED[color], 1)]

    # The fourth matching and its different-neighbour mate form the complete
    # selected mixed fibre and cancel exactly over Z.
    mixed_fibre = fibres[MIXED_COLORING]
    assert mixed_fibre == [(FOURTH, 1), (MATE, -1)]
    assert sum(value for _matching, value in mixed_fibre) == 0
    assert decorated_term(FOURTH, MIXED_COLORING) == 1
    assert decorated_term(MATE, MIXED_COLORING) == -1

    # This is deliberately not a counterexample: another mixed fibre is a
    # nonzero singleton.
    failing = (0, 0, 0, 0, 0, 0, 0, 2, 2, 2)
    assert sum(value for _matching, value in fibres[failing]) == 1

    # Removing FOURTH from the selected prism leaves two 5-cycles.  Adding
    # MATE instead gives the Petersen graph.  It has six perfect matchings,
    # and the complement of each is two odd 5-cycles.  Thus it has no
    # decomposition into three one-factors and contributes no matching
    # triple monomial to the three-copy epsilon expansion.
    complement = set().union(*selected_edges) - set(FOURTH)
    assert sorted(map(len, components(VERTICES, complement))) == [5, 5]
    replacement = frozenset(complement | set(MATE))
    petersen_matchings = tuple(perfect_matchings(VERTICES, replacement))
    assert len(petersen_matchings) == 6
    for matching in petersen_matchings:
        two_factor = replacement - set(matching)
        assert sorted(map(len, components(VERTICES, two_factor))) == [5, 5]

    # The full 19-edge underlying support already satisfies the strongest
    # graph-theoretic normal forms relevant to this route.
    covered = set().union(*map(set, support_matchings))
    assert covered == support
    for deleted_size in (0, 1, 2):
        for deleted in combinations(VERTICES, deleted_size):
            remaining = tuple(v for v in VERTICES if v not in deleted)
            induced = {
                edge for edge in support
                if edge[0] in remaining and edge[1] in remaining
            }
            assert len(components(remaining, induced)) == 1

    nontrivial_tight_cuts = []
    for shore_size in (3, 5, 7):
        for shore_tuple in combinations(VERTICES, shore_size):
            shore = frozenset(shore_tuple)
            crossing_counts = {
                sum((u in shore) != (v in shore) for u, v in matching)
                for matching in support_matchings
            }
            if crossing_counts == {1}:
                nontrivial_tight_cuts.append(shore_tuple)
    assert not nontrivial_tight_cuts

    print("verified three selected constant fibres: unique, coefficient 1")
    print("verified selected mixed fibre: two terms 1 and -1")
    print("verified replacement occurrence graph: Petersen, not 3-edge-colourable")
    print("verified 19-edge support: 3-connected, matching-covered, tight-cut-free")


if __name__ == "__main__":
    main()
