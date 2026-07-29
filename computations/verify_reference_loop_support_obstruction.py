#!/usr/bin/env python3
"""Verify the eight-vertex support counterexample in the accompanying note."""

from __future__ import annotations


VERTICES = frozenset(range(8))
M0 = frozenset({(0, 1), (2, 3), (4, 5), (6, 7)})
EDGES = frozenset(
    {
        (0, 1),
        (0, 4),
        (0, 5),
        (1, 2),
        (1, 3),
        (2, 3),
        (2, 7),
        (3, 7),
        (4, 5),
        (4, 6),
        (5, 6),
        (6, 7),
    }
)


def perfect_matchings(vertices: frozenset[int]):
    if not vertices:
        yield frozenset()
        return
    u = min(vertices)
    for v in sorted(vertices - {u}):
        edge = (min(u, v), max(u, v))
        if edge not in EDGES:
            continue
        for rest in perfect_matchings(vertices - {u, v}):
            yield rest | {edge}


def connected_edge_set(edges: frozenset[tuple[int, int]]) -> bool:
    support = {v for edge in edges for v in edge}
    seen = {next(iter(support))}
    while True:
        grown = seen | {
            v
            for edge in edges
            if seen.intersection(edge)
            for v in edge
        }
        if grown == seen:
            return seen == support
        seen = grown


def main() -> None:
    matchings = sorted(perfect_matchings(VERTICES), key=lambda m: sorted(m))
    assert len(matchings) == 5
    assert M0 in matchings
    assert {edge for matching in matchings for edge in matching} == set(EDGES)
    assert all(sum(v in edge for edge in EDGES) == 3 for v in VERTICES)

    for matching in matchings:
        if matching == M0:
            continue
        difference = matching ^ M0
        assert {v for edge in difference for v in edge} == set(VERTICES)
        assert connected_edge_set(difference)

    print("verified: 5 perfect matchings; 4 nontrivial differences are Hamilton cycles")
    for matching in matchings:
        print(" ", " ".join(f"{u}{v}" for u, v in sorted(matching)))


if __name__ == "__main__":
    main()
