#!/usr/bin/env python3
"""Audit exact linear certificates for n=8 structural cell ceilings."""

from fractions import Fraction
from itertools import combinations, product
from itertools import permutations


N = 8
Q = 3
TARGETS = (
    ((0, 1), (2, 3), (4, 5), (6, 7)),
    ((0, 2), (1, 3), (4, 6), (5, 7)),
    ((0, 4), (1, 5), (2, 6), (3, 7)),
)
DUAL_ORBITS = (
    ((0, 0, 0, 0, 1, 1, 1, 1), 6, Fraction(3, 8)),
    ((0, 0, 1, 2, 2, 1, 0, 0), 12, Fraction(1, 8)),
    ((0, 1, 0, 2, 0, 2, 0, 1), 12, Fraction(1, 4)),
    ((0, 1, 0, 2, 2, 0, 1, 0), 24, Fraction(1, 16)),
    ((0, 1, 1, 0, 1, 0, 0, 1), 6, Fraction(1, 8)),
)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def target_automorphisms():
    """Compute the vertex/colour automorphisms without production code."""

    target_sets = tuple(frozenset(target) for target in TARGETS)
    answer = []
    for vertex_permutation in permutations(range(N)):
        images = tuple(
            frozenset(
                tuple(sorted((vertex_permutation[u], vertex_permutation[v])))
                for u, v in target
            )
            for target in TARGETS
        )
        for color_permutation in permutations(range(Q)):
            if all(
                images[color] == target_sets[color_permutation[color]]
                for color in range(Q)
            ):
                answer.append((vertex_permutation, color_permutation))
    assert len(answer) == 48
    return tuple(answer)


def image_coloring(coloring, automorphism):
    vertex_permutation, color_permutation = automorphism
    image = [None] * N
    for vertex in range(N):
        image[vertex_permutation[vertex]] = color_permutation[
            coloring[vertex]
        ]
    return tuple(image)


def forced_edges(coloring):
    return frozenset(
        edge
        for color, target in enumerate(TARGETS)
        for edge in target
        if coloring[edge[0]] == coloring[edge[1]] == color
    )


def local_edge_ceiling(coloring):
    forced = forced_edges(coloring)
    is_perfect_matching = (
        len(forced) == N // 2
        and len({vertex for edge in forced for vertex in edge}) == N
    )
    return 17 if is_perfect_matching else 21


def main():
    edges = tuple(combinations(range(N), 2))
    matchings = tuple(perfect_matchings(range(N)))
    assert len(edges) == 28
    assert len(matchings) == 105

    # Every edge of K8 belongs to the 15 matchings obtained by matching the
    # other six vertices.  Thus deleting at most six edges from K8 destroys
    # at most 6*15 of its 105 matchings (the union bound may overcount).
    # Consequently every graph with at least 22 edges has at least 15, and
    # in particular more than two, perfect matchings.
    incidences = {
        edge: sum(edge in matching for matching in matchings)
        for edge in edges
    }
    assert set(incidences.values()) == {15}
    for missing_edges in range(7):
        surviving_lower_bound = len(matchings) - 15 * missing_edges
        assert surviving_lower_bound >= 15 > 2

    # If a graph already contains one fixed perfect matching M, its other
    # 24 edges split into six K_{2,2} blocks between pairs of M-edges.  A
    # two-edge perfect matching in one block flips those two M-edges and
    # gives a second global perfect matching.  A block with no such flip has
    # at most two edges; a block with at most one flip has at most three.
    # With at most one global alternative, at most one block can have a flip,
    # so the graph has at most 4 + 5*2 + 3 = 17 edges.
    block_edges = ((0, 2), (0, 3), (1, 2), (1, 3))
    block_pairings = (
        frozenset(((0, 2), (1, 3))),
        frozenset(((0, 3), (1, 2))),
    )
    block_profiles = []
    for bits in product((0, 1), repeat=4):
        selected = frozenset(
            edge for edge, bit in zip(block_edges, bits) if bit
        )
        flips = sum(pairing <= selected for pairing in block_pairings)
        block_profiles.append((len(selected), flips))
    assert max(size for size, flips in block_profiles if flips == 0) == 2
    assert max(size for size, flips in block_profiles if flips <= 1) == 3
    fixed_matching_edge_ceiling = 4 + 5 * 2 + 3
    assert fixed_matching_edge_ceiling == 17

    mixed_colorings = Q ** N - Q
    diagonal_cells = len(edges) * Q
    appearances_per_cell = Q ** (N - 2)
    assert mixed_colorings == 6558
    assert diagonal_cells == 84
    assert appearances_per_cell == 729

    # If O and D are the off-diagonal and diagonal selected cells, summing
    # graph-edge counts over mixed colourings gives 729*O + 728*D.  Each
    # mixed graph has at most 21 edges by the calculation above.  Since
    # D <= 84, this bounds S=O+D as follows.
    universal_mixed_edge_budget = mixed_colorings * 21
    universal_support_ceiling = (
        universal_mixed_edge_budget + diagonal_cells
    ) // appearances_per_cell
    assert universal_support_ceiling == 189

    # For the orbit-40 targets, exactly six mixed colourings have four
    # forced edges covering all eight vertices, hence already contain a
    # perfect matching.  Their local ceiling is 17 rather than 21.
    forced_matching_colorings = []
    for coloring in product(range(Q), repeat=N):
        if len(set(coloring)) == 1:
            continue
        forced = forced_edges(coloring)
        if (len(forced) == N // 2
                and len({vertex for edge in forced for vertex in edge}) == N):
            forced_matching_colorings.append(coloring)
    assert len(forced_matching_colorings) == 6

    orbit40_mixed_edge_budget = (
        (mixed_colorings - len(forced_matching_colorings)) * 21
        + len(forced_matching_colorings) * fixed_matching_edge_ceiling
    )
    orbit40_support_ceiling = (
        orbit40_mixed_edge_budget + diagonal_cells
    ) // appearances_per_cell
    assert orbit40_support_ceiling == 188
    assert (appearances_per_cell * 189 - diagonal_cells
            > orbit40_mixed_edge_budget)

    # A much sharper exact fractional-cover certificate uses only 60 mixed
    # colourings in five target-automorphism orbits.  Their listed weights
    # cover every one of the 252 decorated cells with total weight exactly
    # one.  Weighting each valid local edge inequality by these fractions
    # therefore bounds the total support size directly.
    automorphisms = target_automorphisms()
    dual_weights = {}
    for representative, expected_size, weight in DUAL_ORBITS:
        orbit = {
            image_coloring(representative, automorphism)
            for automorphism in automorphisms
        }
        assert len(orbit) == expected_size
        assert all(len(set(coloring)) > 1 for coloring in orbit)
        assert not orbit.intersection(dual_weights)
        dual_weights.update({coloring: weight for coloring in orbit})
    assert len(dual_weights) == 60
    assert sum(
        local_edge_ceiling(coloring) == 17
        for coloring in dual_weights
    ) == 6

    for u, v, a, b in product(range(N), range(N), range(Q), range(Q)):
        if u >= v:
            continue
        coverage = sum(
            weight
            for coloring, weight in dual_weights.items()
            if coloring[u] == a and coloring[v] == b
        )
        assert coverage == 1, ((u, v, a, b), coverage)
    dual_budget = sum(
        weight * local_edge_ceiling(coloring)
        for coloring, weight in dual_weights.items()
    )
    assert dual_budget == 180

    print(
        "PASS structural ceilings: universal 189, orbit-40 double-count "
        "188, orbit-40 exact 60-coloring fractional cover 180"
    )


if __name__ == "__main__":
    main()
