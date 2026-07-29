#!/usr/bin/env python3
"""Exact audit of the binary principal-minor counterexample.

For alternating cycles of orders 4, 6, 8, and 10, this script verifies that
the full decorated matching tensor is binary GHZ and that every proper even
induced subset has at most one supported perfect matching.  Thus each
proper principal matching cofactor is zero or a single pure word.
"""

from __future__ import annotations

from itertools import combinations, product


def perfect_matchings(vertices: tuple[int, ...], edges: set[tuple[int, int]]):
    if not vertices:
        yield ()
        return
    v = vertices[0]
    for index in range(1, len(vertices)):
        w = vertices[index]
        edge = (min(v, w), max(v, w))
        if edge not in edges:
            continue
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest, edges):
            yield (edge,) + matching


def alternating_cycle(order: int):
    edges = {
        (min(v, (v + 1) % order), max(v, (v + 1) % order))
        for v in range(order)
    }
    edge_color = {}
    for v in range(0, order, 2):
        edge_color[(v, v + 1)] = 0
    for v in range(1, order - 1, 2):
        edge_color[(v, v + 1)] = 1
    edge_color[(0, order - 1)] = 1
    assert set(edge_color) == edges
    return edges, edge_color


def coefficient(vertices, matchings, edge_color, coloring):
    answer = 0
    for matching in matchings:
        if all(
            coloring[u] == edge_color[edge]
            and coloring[v] == edge_color[edge]
            for edge in matching
            for u, v in (edge,)
        ):
            answer += 1
    return answer


def audit_order(order: int):
    edges, edge_color = alternating_cycle(order)
    vertices = tuple(range(order))
    full_matchings = tuple(perfect_matchings(vertices, edges))
    assert len(full_matchings) == 2
    for coloring in product(range(2), repeat=order):
        expected = int(len(set(coloring)) == 1)
        assert coefficient(vertices, full_matchings, edge_color, coloring) == expected

    for size in range(0, order, 2):
        for subset in combinations(vertices, size):
            induced = tuple(perfect_matchings(subset, edges))
            assert len(induced) <= 1
            if induced:
                word = {}
                for edge in induced[0]:
                    for vertex in edge:
                        word[vertex] = edge_color[edge]
                assert set(word) == set(subset)


def main():
    for order in (4, 6, 8, 10):
        audit_order(order)
    print("PASS: binary cycle GHZ and all proper principal cofactors audited")


if __name__ == "__main__":
    main()
