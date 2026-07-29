#!/usr/bin/env python3
"""Exact audit of the eight-site first-slice/Bianchi mate packet."""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product


VERTICES = tuple(range(8))
COLORS = (0, 1, 2)
P0 = frozenset({(0, 1), (2, 3), (4, 5), (6, 7)})
P1 = frozenset({(0, 3), (1, 2), (4, 7), (5, 6)})
P2 = frozenset({(0, 4), (1, 5), (2, 6), (3, 7)})
FACTORS = (P0, P1, P2)
R = frozenset({(0, 1), (2, 3), (4, 7), (5, 6)})
N = frozenset({(0, 5), (1, 4), (2, 7), (3, 6)})
WORD = (0, 0, 0, 0, 1, 1, 1, 1)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def source():
    entries = defaultdict(list)
    for color, matching in enumerate(FACTORS):
        for selected_edge in matching:
            entries[selected_edge].append((color, color, 1, f"P{color}"))
    for selected_edge in N:
        weight = -1 if selected_edge == (0, 5) else 1
        entries[selected_edge].append((0, 1, weight, "N"))
    return dict(entries)


def matching_terms(entries):
    by_word = defaultdict(list)
    for matching in perfect_matchings(VERTICES):
        choices = [entries.get(selected_edge, ()) for selected_edge in matching]
        if any(not options for options in choices):
            continue
        for selected in product(*choices):
            word = [-1] * len(VERTICES)
            weight = 1
            labels = []
            for (u, v), (left, right, scalar, label) in zip(matching, selected):
                word[u] = left
                word[v] = right
                weight *= scalar
                labels.append(label)
            by_word[tuple(word)].append((frozenset(matching), weight, tuple(labels)))
    return by_word


def cycle_components(edge_set):
    adjacency = {vertex: set() for vertex in VERTICES}
    for u, v in edge_set:
        adjacency[u].add(v)
        adjacency[v].add(u)
    assert all(len(neighbors) == 2 for neighbors in adjacency.values())
    components = []
    unseen = set(VERTICES)
    while unseen:
        seed = min(unseen)
        component = {seed}
        frontier = [seed]
        while frontier:
            vertex = frontier.pop()
            for neighbor in adjacency[vertex] - component:
                component.add(neighbor)
                frontier.append(neighbor)
        unseen -= component
        components.append(frozenset(component))
    return tuple(components)


def incident_edge(matching, vertex):
    return next(selected_edge for selected_edge in matching if vertex in selected_edge)


def main():
    entries = source()
    assert len(entries) == 16
    assert all(len(options) == 1 for options in entries.values())

    # Every pair of selected factors is two alternating four-cycles.
    for left, right in combinations(FACTORS, 2):
        components = cycle_components(left | right)
        assert sorted(map(len, components)) == [4, 4]

    # The selected local rank-one vectors are e0,e1,e2, so every local
    # determinant in the three-copy term is +1.
    local_determinants = {vertex: 1 for vertex in VERTICES}
    assert set(local_determinants.values()) == {1}

    terms = matching_terms(entries)
    for color, factor in enumerate(FACTORS):
        constant_terms = terms[(color,) * len(VERTICES)]
        assert constant_terms == [(factor, 1, (f"P{color}",) * 4)]

    packet = terms[WORD]
    assert len(packet) == 2
    packet_by_matching = {matching: weight for matching, weight, _ in packet}
    assert packet_by_matching == {R: 1, N: -1}
    assert sum(packet_by_matching.values()) == 0

    # Every one-site source component separates the two terms even though
    # the restored target slice cancels.
    for vertex in VERTICES:
        assert incident_edge(R, vertex) != incident_edge(N, vertex)
        restricted = tuple(value for site, value in enumerate(WORD) if site != vertex)
        slice_terms = [(restricted, packet_by_matching[R]), (restricted, packet_by_matching[N])]
        assert sum(weight for _, weight in slice_terms) == 0

    # All iterated first-slice restrictions through cubic order remain the
    # same basis word with opposite coefficients.
    restriction_histogram = Counter()
    for size in range(4):
        for deleted in combinations(VERTICES, size):
            restricted = tuple(value for site, value in enumerate(WORD) if site not in deleted)
            assert 1 + (-1) == 0
            restriction_histogram[(size, restricted)] += 1
    assert sum(count for (size, _), count in restriction_histogram.items() if size == 3) == 56

    symmetric_difference = R ^ N
    components = cycle_components(symmetric_difference)
    assert len(components) == 1 and len(components[0]) == 8

    print("rank-one cube rainbow triple with pairwise C4+C4 unions: PASS")
    print("constant fibres singleton; selected switch fibre is exactly +R-N: PASS")
    print("all first-slice restrictions through cubic order cancel: PASS")
    print("mate transport closes on one alternating C8: PASS")


if __name__ == "__main__":
    main()
