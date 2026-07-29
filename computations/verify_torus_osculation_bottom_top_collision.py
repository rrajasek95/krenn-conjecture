#!/usr/bin/env python3
"""Exact n=12 audit for the bottom/top torus-layer collision boundary."""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations


N = 12
M = 6
VERTICES = tuple(range(N))

P0 = ((0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11))
P1 = ((0, 11), (1, 2), (3, 4), (5, 6), (7, 8), (9, 10))
P2 = ((0, 2), (1, 7), (3, 5), (4, 10), (6, 8), (9, 11))
FACTORS = tuple(frozenset(matching) for matching in (P0, P1, P2))
SUPPORT = frozenset().union(*FACTORS)


def supported_perfect_matchings(support=SUPPORT, retained=VERTICES):
    retained = tuple(sorted(retained))
    adjacency = {vertex: set() for vertex in retained}
    for u, v in support:
        if u in adjacency and v in adjacency:
            adjacency[u].add(v)
            adjacency[v].add(u)

    @lru_cache(maxsize=None)
    def recurse(remaining):
        if not remaining:
            return ((),)
        u = remaining[0]
        remaining_set = set(remaining)
        answer = []
        for v in sorted(adjacency[u] & remaining_set):
            selected_edge = (u, v) if u < v else (v, u)
            tail_vertices = tuple(x for x in remaining if x not in (u, v))
            for tail in recurse(tail_vertices):
                answer.append(tuple(sorted((selected_edge,) + tail)))
        return tuple(answer)

    return recurse(retained)


def connected_after_deletion(deleted):
    retained = set(VERTICES) - set(deleted)
    adjacency = {vertex: set() for vertex in retained}
    for u, v in SUPPORT:
        if u in retained and v in retained:
            adjacency[u].add(v)
            adjacency[v].add(u)
    seed = min(retained)
    seen = {seed}
    frontier = [seed]
    while frontier:
        vertex = frontier.pop()
        for neighbor in adjacency[vertex] - seen:
            seen.add(neighbor)
            frontier.append(neighbor)
    return seen == retained


def crossing_count(matching, shore):
    return sum((u in shore) != (v in shore) for u, v in matching)


def coloring(matching):
    edge_color = {
        selected_edge: color
        for color, factor in enumerate(FACTORS)
        for selected_edge in factor
    }
    assert len(edge_color) == 3 * M
    answer = [-1] * N
    for u, v in matching:
        color = edge_color[(u, v)]
        answer[u] = color
        answer[v] = color
    assert -1 not in answer
    return tuple(answer)


def main():
    # Each binary face is exactly a Hamilton cycle with its two factors.
    for left, right in combinations(FACTORS, 2):
        pair_support = left | right
        degrees = Counter(vertex for selected_edge in pair_support for vertex in selected_edge)
        assert degrees == Counter({vertex: 2 for vertex in VERTICES})
        assert set(supported_perfect_matchings(pair_support)) == {
            tuple(sorted(left)),
            tuple(sorted(right)),
        }

    matchings = supported_perfect_matchings()
    assert len(matchings) == 8
    pure_matchings = {tuple(sorted(factor)) for factor in FACTORS}
    extra_matchings = tuple(matching for matching in matchings if matching not in pure_matchings)
    assert len(extra_matchings) == 5

    fibres = defaultdict(list)
    for matching in matchings:
        fibres[coloring(matching)].append(matching)
    assert len(fibres) == len(matchings)
    assert all(len(terms) == 1 for terms in fibres.values())

    # Every error matching is balanced: two edges, hence four sites, of
    # every color.  Under any one-color torus it occurs only in degree four.
    count_histogram = Counter()
    for matching in extra_matchings:
        edge_counts = tuple(len(set(matching) & factor) for factor in FACTORS)
        assert edge_counts == (2, 2, 2)
        induced = coloring(matching)
        assert tuple(induced.count(color) for color in range(3)) == (4, 4, 4)
        count_histogram[edge_counts] += 1
    assert count_histogram == Counter({(2, 2, 2): 5})

    for scaled_color in range(3):
        exponent_histogram = Counter()
        for induced in fibres:
            exponent_histogram[induced.count(scaled_color)] += 1
        # The two other pure words have degree zero, the five errors degree
        # four, and the scaled pure word degree twelve.
        assert exponent_histogram == Counter({4: 5, 0: 2, 12: 1})
        assert all(degree not in exponent_histogram for degree in (1, 2, 3))
        assert all(degree not in exponent_histogram for degree in range(5, 12))

    # The support itself supplies no literal six-site or tight-cut descent.
    for deleted_size in range(3):
        for deleted in combinations(VERTICES, deleted_size):
            assert connected_after_deletion(deleted)

    nontrivial_tight_shores = []
    for shore_size in (3, 5):
        for shore_tuple in combinations(VERTICES, shore_size):
            shore = frozenset(shore_tuple)
            if {crossing_count(matching, shore) for matching in matchings} == {1}:
                nontrivial_tight_shores.append(shore)
    assert not nontrivial_tight_shores

    six_cut_sizes = []
    closed_six_sets = []
    for shore_tuple in combinations(VERTICES, 6):
        shore = frozenset(shore_tuple)
        six_cut_sizes.append(crossing_count(SUPPORT, shore))
        if all(crossing_count(factor, shore) == 0 for factor in FACTORS):
            closed_six_sets.append(shore)
    assert min(six_cut_sizes) == 4
    assert not closed_six_sets

    print("verified n=12 pairwise-Hamilton collision model with 8 supported matchings")
    print("verified five singleton errors, all with edge counts (2,2,2) and site counts (4,4,4)")
    print("under every color scaling only degrees 0, 4, and 12 occur")
    print("verified 3-vertex-connectivity, no nontrivial tight odd shore, and six-cut minimum 4")


if __name__ == "__main__":
    main()
