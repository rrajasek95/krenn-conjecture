#!/usr/bin/env python3
"""Audit the first-slice cubic obstruction on three one-factors.

The exhaustive part checks every perfect matching disjoint from the
standard Hamilton cycle through twelve vertices.  For each third factor it
constructs a perfect matching which uses one cross-parity chord or two
interlacing same-parity chords.  The sharpness part checks the balanced
twelve-site triple from ``torus-osculation-bottom-top-collision.md``.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def cycle_factors(n: int):
    half = n // 2
    p0 = frozenset((2 * j, 2 * j + 1) for j in range(half))
    p1 = frozenset(edge(2 * j + 1, (2 * j + 2) % n) for j in range(half))
    return p0, p1


def pair_consecutive(path: tuple[int, ...]):
    assert len(path) % 2 == 0
    return tuple(edge(path[j], path[j + 1]) for j in range(0, len(path), 2))


def one_chord_witness(n: int, chord: tuple[int, int]):
    u, v = sorted(chord)
    assert (u - v) % 2
    first_arc = tuple(range(u + 1, v))
    second_arc = tuple(range(v + 1, n)) + tuple(range(0, u))
    return frozenset((edge(u, v),) + pair_consecutive(first_arc) + pair_consecutive(second_arc))


def chords_interlace(first: tuple[int, int], second: tuple[int, int]):
    a, b = sorted(first)
    c, d = sorted(second)
    return (a < c < b < d) or (c < a < d < b)


def two_chord_witness(n: int, first: tuple[int, int], second: tuple[int, int]):
    assert chords_interlace(first, second)
    endpoints = sorted(first + second)
    arcs = []
    for position, start in enumerate(endpoints):
        stop = endpoints[(position + 1) % 4]
        if position < 3:
            path = tuple(range(start + 1, stop))
        else:
            path = tuple(range(start + 1, n)) + tuple(range(0, stop))
        assert len(path) % 2 == 0
        arcs.extend(pair_consecutive(path))
    return frozenset((edge(*first), edge(*second), *arcs))


def construct_witness(n: int, p2: frozenset[tuple[int, int]]):
    cross = next((selected for selected in p2 if (selected[0] - selected[1]) % 2), None)
    if cross is not None:
        return one_chord_witness(n, cross)

    even_chords = tuple(selected for selected in p2 if selected[0] % 2 == 0)
    odd_chords = tuple(selected for selected in p2 if selected[0] % 2 == 1)
    pair = next(
        (
            (even_chord, odd_chord)
            for even_chord in even_chords
            for odd_chord in odd_chords
            if chords_interlace(even_chord, odd_chord)
        ),
        None,
    )
    assert pair is not None
    return two_chord_witness(n, *pair)


def is_perfect_matching(n: int, matching):
    degrees = [0] * n
    for u, v in matching:
        degrees[u] += 1
        degrees[v] += 1
    return degrees == [1] * n


def exhaustive_witness_audit():
    counts = {}
    for n in (6, 8, 10, 12):
        p0, p1 = cycle_factors(n)
        cycle = p0 | p1
        audited = 0
        for raw in perfect_matchings(tuple(range(n))):
            p2 = frozenset(edge(*selected) for selected in raw)
            if p2 & cycle:
                continue
            witness = construct_witness(n, p2)
            assert is_perfect_matching(n, witness)
            assert witness <= cycle | p2
            assert 1 <= len(witness & p2) <= 2
            assert witness not in (p0, p1, p2)
            audited += 1
        assert audited
        counts[n] = audited
    return counts


N = 12
P0 = frozenset({(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11)})
P1 = frozenset({(0, 11), (1, 2), (3, 4), (5, 6), (7, 8), (9, 10)})
P2 = frozenset({(0, 2), (1, 7), (3, 5), (4, 10), (6, 8), (9, 11)})
FACTORS = (P0, P1, P2)
SUPPORT = frozenset().union(*FACTORS)


def supported_perfect_matchings(support=SUPPORT, retained=tuple(range(N))):
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
        first = remaining[0]
        answer = []
        for second in sorted(adjacency[first] & set(remaining)):
            rest = tuple(vertex for vertex in remaining if vertex not in (first, second))
            for tail in recurse(rest):
                answer.append(tuple(sorted((edge(first, second),) + tail)))
        return tuple(answer)

    return recurse(retained)


def connected(edge_set):
    adjacency = {vertex: set() for vertex in range(N)}
    for u, v in edge_set:
        adjacency[u].add(v)
        adjacency[v].add(u)
    seen = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in adjacency[vertex] - seen:
            seen.add(neighbor)
            frontier.append(neighbor)
    return len(seen) == N


def sharpness_audit():
    for left, right in combinations(FACTORS, 2):
        assert connected(left | right)
        assert set(supported_perfect_matchings(left | right)) == {
            tuple(sorted(left)),
            tuple(sorted(right)),
        }

    selected = {tuple(sorted(factor)) for factor in FACTORS}
    matchings = supported_perfect_matchings()
    assert len(matchings) == 8
    extras = tuple(matching for matching in matchings if matching not in selected)
    assert len(extras) == 5

    words = set()
    for matching in extras:
        edge_counts = tuple(len(set(matching) & factor) for factor in FACTORS)
        assert edge_counts == (2, 2, 2)
        word = [-1] * N
        for selected_edge in matching:
            color = next(color for color, factor in enumerate(FACTORS) if selected_edge in factor)
            for vertex in selected_edge:
                word[vertex] = color
        assert tuple(word).count(0) == tuple(word).count(1) == tuple(word).count(2) == 4
        assert tuple(word) not in words
        words.add(tuple(word))
        # Removing a site in any represented colour lowers its torus degree
        # from four to exactly three in the normalized component.
        for color in range(3):
            for vertex, value in enumerate(word):
                if value == color:
                    assert sum(entry == color for index, entry in enumerate(word) if index != vertex) == 3

    closed_six_sets = []
    for shore_tuple in combinations(range(N), 6):
        shore = frozenset(shore_tuple)
        if all(all((u in shore) == (v in shore) for u, v in factor) for factor in FACTORS):
            closed_six_sets.append(shore)
    assert not closed_six_sets


def main():
    counts = exhaustive_witness_audit()
    sharpness_audit()
    print(f"one-/two-chord witnesses through n=12: PASS {counts}")
    print("balanced n=12 first-slice cubic sharpness: PASS")
    print("balanced n=12 has no factor-closed six-set: PASS")


if __name__ == "__main__":
    main()
