#!/usr/bin/env python3
"""Exact audit of the planar bipartite obstruction at n=10 and n=12.

The mathematical input is the already proved support-minimality and
cubic-vertex rigidity lemmas.  This audit checks the finite graph and
colour-support claims needed after those lemmas:

* no ten-vertex graph survives the Euler/high-degree-core count;
* every twelve-vertex planar bipartite degree pattern that survives is
  isomorphic to C4 x P3, with its four degree-four vertices on the middle
  C4; and
* every proper three-edge-colouring of the two cubic C4 shells either
  misses a constant colour coefficient or creates a mixed colouring with
  exactly one possible matching, all of whose edge cells are forced
  nonzero basis cells.

Only finite sets, integer counts, and exact graph algorithms are used.
"""

from __future__ import annotations

import itertools
from collections import defaultdict

import networkx as nx


Q = 3
CORE = tuple(range(4))
INNER = tuple(range(4, 8))
OUTER = tuple(range(8, 12))
VERTICES = CORE + INNER + OUTER


def cycle_edges(vertices: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(
        tuple(sorted((vertices[i], vertices[(i + 1) % len(vertices)])))
        for i in range(len(vertices))
    )


CORE_EDGES = cycle_edges(CORE)
INNER_EDGES = cycle_edges(INNER)
OUTER_EDGES = cycle_edges(OUTER)
INNER_SPOKES = tuple((i, 4 + i) for i in CORE)
OUTER_SPOKES = tuple((i, 8 + i) for i in CORE)
SHELL_EDGES = INNER_EDGES + OUTER_EDGES + INNER_SPOKES + OUTER_SPOKES
ALL_EDGES = set(CORE_EDGES + SHELL_EDGES)


def canonical_graph() -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(VERTICES)
    graph.add_edges_from(ALL_EDGES)
    return graph


def attachment_sets(
    core_vertices: tuple[int, int],
    cubic_vertices: tuple[int, int, int, int],
    demands: dict[int, int],
):
    """All simple attachments giving each core vertex degree two."""
    for first in itertools.combinations(cubic_vertices, 2):
        for second in itertools.combinations(cubic_vertices, 2):
            if any(
                int(vertex in first) + int(vertex in second) != demands[vertex]
                for vertex in cubic_vertices
            ):
                continue
            yield tuple((core_vertices[0], vertex) for vertex in first) + tuple(
                (core_vertices[1], vertex) for vertex in second
            )


def audit_twelve_vertex_graphs() -> None:
    """Enumerate the only possible extremal bipartite degree pattern."""
    # The middle C4 has two vertices on each bipartition shore.  A perfect
    # matching forces shores of size six, leaving four cubic vertices per
    # shore.  Their induced bipartite graph has eight edges; the remaining
    # degree at each cubic vertex is its demand for middle-C4 attachments.
    core_a = (0, 2)
    core_b = (1, 3)
    cubic_a = (4, 6, 8, 10)
    cubic_b = (5, 7, 9, 11)
    possible_cubic_edges = tuple(itertools.product(cubic_a, cubic_b))
    target = canonical_graph()

    attachment_cases = 0
    planar_cases = 0
    for cubic_edges in itertools.combinations(possible_cubic_edges, 8):
        degrees = {vertex: 0 for vertex in cubic_a + cubic_b}
        for left, right in cubic_edges:
            degrees[left] += 1
            degrees[right] += 1
        # A cubic vertex has at most two neighbours on the middle C4, so it
        # must have between one and three neighbours among the cubic set.
        if any(not 1 <= degrees[vertex] <= 3 for vertex in degrees):
            continue
        attach_to_b = tuple(
            attachment_sets(
                core_b,
                cubic_a,
                {vertex: 3 - degrees[vertex] for vertex in cubic_a},
            )
        )
        attach_to_a = tuple(
            attachment_sets(
                core_a,
                cubic_b,
                {vertex: 3 - degrees[vertex] for vertex in cubic_b},
            )
        )
        for first in attach_to_b:
            for second in attach_to_a:
                attachment_cases += 1
                graph = nx.Graph()
                graph.add_nodes_from(VERTICES)
                graph.add_edges_from(CORE_EDGES)
                graph.add_edges_from(cubic_edges)
                graph.add_edges_from(first)
                graph.add_edges_from(second)
                assert graph.number_of_edges() == 20
                assert sorted(dict(graph.degree()).values()) == [3] * 8 + [4] * 4
                assert nx.is_bipartite(graph)
                if not nx.is_connected(graph) or not nx.check_planarity(graph)[0]:
                    continue
                planar_cases += 1
                assert nx.is_isomorphic(graph, target)

    assert attachment_cases == 36_504
    assert planar_cases == 288


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        edge = tuple(sorted((first, second)))
        if edge not in ALL_EDGES:
            continue
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield (edge,) + tail


MATCHINGS = tuple(perfect_matchings(VERTICES))


def shell_colourings():
    """The eighteen proper three-edge-colourings of a cubic C4 shell."""
    answer = []
    for cycle_colours in itertools.product(range(Q), repeat=4):
        if any(
            cycle_colours[i] == cycle_colours[(i - 1) % 4] for i in range(4)
        ):
            continue
        spoke_colours = tuple(
            3 - cycle_colours[i] - cycle_colours[(i - 1) % 4]
            for i in range(4)
        )
        answer.append((cycle_colours, spoke_colours))
    assert len(answer) == 18
    return tuple(answer)


SHELL_COLOURINGS = shell_colourings()


def shell_map(inner_index: int, outer_index: int) -> dict[tuple[int, int], int]:
    inner_cycle, inner_spokes = SHELL_COLOURINGS[inner_index]
    outer_cycle, outer_spokes = SHELL_COLOURINGS[outer_index]
    answer: dict[tuple[int, int], int] = {}
    answer.update(zip(INNER_EDGES, inner_cycle, strict=True))
    answer.update(zip(OUTER_EDGES, outer_cycle, strict=True))
    answer.update(zip(INNER_SPOKES, inner_spokes, strict=True))
    answer.update(zip(OUTER_SPOKES, outer_spokes, strict=True))
    return answer


def possible_matching_terms(inner_index: int, outer_index: int):
    """Map each colouring to its possible matching/core-cell terms.

    A term is represented by the tuple of coloured core edges it uses.  An
    empty tuple is a shell-only matching and hence a product of forced
    nonzero scalar basis cells.
    """
    shell = shell_map(inner_index, outer_index)
    terms: dict[
        tuple[int, ...], list[tuple[tuple[tuple[int, int], int, int], ...]]
    ] = defaultdict(list)
    for matching in MATCHINGS:
        core_edges = tuple(edge for edge in matching if edge in CORE_EDGES)
        fixed = [-1] * len(VERTICES)
        for edge in matching:
            if edge in CORE_EDGES:
                continue
            colour = shell[edge]
            fixed[edge[0]] = colour
            fixed[edge[1]] = colour
        for values in itertools.product(range(Q), repeat=2 * len(core_edges)):
            colouring = fixed.copy()
            core_cells = []
            for position, edge in enumerate(core_edges):
                left_colour = values[2 * position]
                right_colour = values[2 * position + 1]
                colouring[edge[0]] = left_colour
                colouring[edge[1]] = right_colour
                core_cells.append((edge, left_colour, right_colour))
            assert -1 not in colouring
            terms[tuple(colouring)].append(tuple(core_cells))
    return terms


def audit_shell_obstruction() -> None:
    assert len(MATCHINGS) == 32
    viable_pairs = 0
    singleton_counts = []
    for inner_index in range(len(SHELL_COLOURINGS)):
        for outer_index in range(len(SHELL_COLOURINGS)):
            terms = possible_matching_terms(inner_index, outer_index)
            if any((colour,) * len(VERTICES) not in terms for colour in range(Q)):
                # That constant target coefficient is identically zero.
                continue
            viable_pairs += 1
            witnesses = [
                colouring
                for colouring, matching_terms in terms.items()
                if len(set(colouring)) > 1
                and len(matching_terms) == 1
                and matching_terms[0] == ()
            ]
            # This coefficient is one nonzero shell monomial and has no
            # possible cancellation term, whatever the four core matrices.
            assert witnesses
            singleton_counts.append(len(witnesses))

    assert viable_pairs == 108
    assert len(SHELL_COLOURINGS) ** 2 - viable_pairs == 216
    assert min(singleton_counts) == 6
    assert max(singleton_counts) == 7


def main() -> None:
    # For n=10, Euler gives |Q| <= n-8 = 2 for vertices of degree >=4,
    # while the high-degree-core lemma requires a bipartite cycle and hence
    # |Q| >= 4.  This integer check records the contradiction explicitly.
    assert 10 - 8 < 4
    audit_twelve_vertex_graphs()
    audit_shell_obstruction()
    print(
        "verified planar obstruction: n=10 impossible by degree count; "
        "n=12 has 288 labeled extremal graphs, all C4 x P3; all 324 shell "
        "colourings fail (216 miss a constant coefficient, 108 have a "
        "mixed singleton)"
    )


if __name__ == "__main__":
    main()
