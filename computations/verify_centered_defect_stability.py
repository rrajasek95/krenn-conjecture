#!/usr/bin/env python3
"""Small exact checks for the centered defect-stability theorem.

Graphs are represented by tuples of adjacency bitmasks, so the checker has
no third-party dependencies.  The default run checks the sharp examples,
the equality constructions used in the proof, and all 2^15 labelled graphs
on six vertices.  The substantially larger 2^21 seven-vertex census is
available only with --full.

The finite checks audit definitions and sharp constants; the uniform theorem
is proved in notes/centered-defect-stability.md.
"""

from __future__ import annotations

import argparse
from itertools import combinations
from typing import Iterable, Sequence


Graph = tuple[int, ...]
Edge = tuple[int, int]


def graph(n: int, edges: Iterable[Edge]) -> Graph:
    adjacency = [0] * n
    for u, v in edges:
        assert 0 <= u < n and 0 <= v < n and u != v
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    return tuple(adjacency)


def clique(vertices: Sequence[int]) -> set[Edge]:
    return {tuple(sorted(edge)) for edge in combinations(vertices, 2)}


def complete_bipartite(left: Sequence[int], right: Sequence[int]) -> set[Edge]:
    return {tuple(sorted((u, v))) for u in left for v in right}


def cycle(vertices: Sequence[int]) -> set[Edge]:
    return {
        tuple(sorted((vertices[i], vertices[(i + 1) % len(vertices)])))
        for i in range(len(vertices))
    }


def component_count(adjacency: Graph, removed: int | None = None) -> int:
    n = len(adjacency)
    active = (1 << n) - 1
    if removed is not None:
        active &= ~(1 << removed)
    unseen = active
    count = 0
    while unseen:
        count += 1
        frontier = unseen & -unseen
        unseen ^= frontier
        while frontier:
            reached = 0
            scan = frontier
            while scan:
                bit = scan & -scan
                scan ^= bit
                reached |= adjacency[bit.bit_length() - 1]
            reached &= unseen
            unseen ^= reached
            frontier = reached
    return count


def bipartite_component_count(
    adjacency: Graph, removed: int | None = None
) -> int:
    """Count bipartite components, including isolated vertices."""

    n = len(adjacency)
    active = (1 << n) - 1
    if removed is not None:
        active &= ~(1 << removed)
    unseen = active
    answer = 0
    while unseen:
        root = unseen & -unseen
        unseen ^= root
        side_zero = root
        side_one = 0
        frontier = root
        is_bipartite = True
        while frontier:
            neighbors = 0
            scan = frontier
            while scan:
                bit = scan & -scan
                scan ^= bit
                neighbors |= adjacency[bit.bit_length() - 1]
            neighbors &= active
            if neighbors & side_zero:
                is_bipartite = False
            new = neighbors & unseen
            unseen ^= new
            side_one |= new

            neighbors = 0
            scan = new
            while scan:
                bit = scan & -scan
                scan ^= bit
                neighbors |= adjacency[bit.bit_length() - 1]
            neighbors &= active
            if neighbors & side_one:
                is_bipartite = False
            frontier = neighbors & unseen
            unseen ^= frontier
            side_zero |= frontier
        answer += is_bipartite
    return answer


def minimum_degree(adjacency: Graph) -> int:
    return min(neighbors.bit_count() for neighbors in adjacency)


def safe_vertices(adjacency: Graph) -> list[int]:
    return [
        v
        for v in range(len(adjacency))
        if bipartite_component_count(adjacency, v) <= 1
    ]


def defective_vertices(adjacency: Graph) -> list[int]:
    return [
        v
        for v in range(len(adjacency))
        if bipartite_component_count(adjacency, v) >= 2
    ]


def cut_vertices(adjacency: Graph) -> list[int]:
    before = component_count(adjacency)
    return [
        v
        for v in range(len(adjacency))
        if component_count(adjacency, v) > before
    ]


def assert_theorem(adjacency: Graph) -> None:
    n = len(adjacency)
    if n >= 7 and minimum_degree(adjacency) >= 3:
        if bipartite_component_count(adjacency) <= 1:
            assert len(safe_vertices(adjacency)) >= 7


def sharp_guards() -> None:
    k33 = graph(6, complete_bipartite((0, 1, 2), (3, 4, 5)))
    assert minimum_degree(k33) == 3
    assert bipartite_component_count(k33) == 1
    assert safe_vertices(k33) == list(range(6))
    assert defective_vertices(k33) == []
    # At n=6 the premise "at least n-6 defects" is vacuous, while delta=3.
    assert len(defective_vertices(k33)) >= len(k33) - 6

    c6_k3_edges = cycle(tuple(range(6))) | clique((6, 7, 8))
    c6_k3 = graph(9, c6_k3_edges)
    assert minimum_degree(c6_k3) == 2
    assert bipartite_component_count(c6_k3) == 1
    assert safe_vertices(c6_k3) == list(range(6))
    assert defective_vertices(c6_k3) == [6, 7, 8]
    assert len(defective_vertices(c6_k3)) == len(c6_k3) - 6

    two_k33_edges = (
        complete_bipartite((0, 1, 2), (3, 4, 5))
        | complete_bipartite((6, 7, 8), (9, 10, 11))
    )
    two_k33 = graph(12, two_k33_edges)
    assert minimum_degree(two_k33) == 3
    assert bipartite_component_count(two_k33) == 2
    assert defective_vertices(two_k33) == list(range(12))


def equality_constructions() -> None:
    shared_edges = clique((0, 1, 2, 3)) | clique((0, 4, 5, 6))
    shared = graph(7, shared_edges)
    assert minimum_degree(shared) == 3
    assert cut_vertices(shared) == [0]
    assert len(shared) - len(cut_vertices(shared)) == 6
    assert safe_vertices(shared) == list(range(7))
    assert_theorem(shared)

    bridged_edges = clique((0, 1, 2, 3)) | clique((4, 5, 6, 7)) | {(0, 4)}
    bridged = graph(8, bridged_edges)
    assert minimum_degree(bridged) == 3
    assert cut_vertices(bridged) == [0, 4]
    assert len(bridged) - len(cut_vertices(bridged)) == 6
    assert safe_vertices(bridged) == list(range(8))
    assert_theorem(bridged)

    bipartite_leaf_edges = (
        complete_bipartite((0, 1, 2), (3, 4, 5))
        | complete_bipartite((0, 6, 7), (8, 9, 10))
    )
    bipartite_leaf = graph(11, bipartite_leaf_edges)
    assert minimum_degree(bipartite_leaf) == 3
    assert bipartite_component_count(bipartite_leaf) == 1
    assert cut_vertices(bipartite_leaf) == [0]
    assert len(bipartite_leaf) - len(cut_vertices(bipartite_leaf)) == 10
    assert len(safe_vertices(bipartite_leaf)) >= 10
    assert_theorem(bipartite_leaf)

    k33_k4_edges = (
        complete_bipartite((0, 1, 2), (3, 4, 5)) | clique((6, 7, 8, 9))
    )
    k33_k4 = graph(10, k33_k4_edges)
    assert minimum_degree(k33_k4) == 3
    assert bipartite_component_count(k33_k4) == 1
    assert len(safe_vertices(k33_k4)) >= 7
    assert_theorem(k33_k4)


def graph_from_edge_mask(n: int, edge_mask: int, edges: Sequence[Edge]) -> Graph:
    adjacency = [0] * n
    while edge_mask:
        bit = edge_mask & -edge_mask
        edge_mask ^= bit
        u, v = edges[bit.bit_length() - 1]
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    return tuple(adjacency)


def exhaustive_boundary(n: int) -> tuple[int, int]:
    edges = list(combinations(range(n), 2))
    qualifying = 0
    minimum_safe = n
    for edge_mask in range(1 << len(edges)):
        adjacency = graph_from_edge_mask(n, edge_mask, edges)
        if minimum_degree(adjacency) < 3:
            continue
        if bipartite_component_count(adjacency) > 1:
            continue
        qualifying += 1
        safe = len(safe_vertices(adjacency))
        minimum_safe = min(minimum_safe, safe)
        if n == 6:
            assert safe == 6
        else:
            assert safe >= 7
    assert qualifying > 0
    return qualifying, minimum_safe


def centered_fan_arithmetic() -> None:
    for source_order in range(8, 102, 2):
        n = source_order - 1
        fan_lower_bound = source_order - 7
        maximum_defective_under_theorem = n - 7
        assert fan_lower_bound == n - 6
        assert fan_lower_bound - maximum_defective_under_theorem == 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--full",
        action="store_true",
        help="also exhaust all 2^21 labelled graphs on seven vertices",
    )
    args = parser.parse_args()

    sharp_guards()
    print("sharp guards: PASS")
    equality_constructions()
    print("block-cut boundary constructions: PASS")
    centered_fan_arithmetic()
    print("centered fan arithmetic: PASS")

    qualifying, minimum_safe = exhaustive_boundary(6)
    print(
        "six-vertex exhaustive boundary: PASS "
        f"({qualifying} qualifying labelled graphs, minimum safe={minimum_safe})"
    )

    if args.full:
        qualifying, minimum_safe = exhaustive_boundary(7)
        print(
            "seven-vertex exhaustive theorem audit: PASS "
            f"({qualifying} qualifying labelled graphs, minimum safe={minimum_safe})"
        )
    else:
        print("seven-vertex 2^21 census: SKIPPED (run with --full)")


if __name__ == "__main__":
    main()
