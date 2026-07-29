#!/usr/bin/env python3
"""Audit the uniform delocalized cancellation-mate construction.

For every even order n >= 8 the construction has four edge-disjoint
perfect matchings P0, P1, P2, N.  The first three are coordinate anchor
matchings.  Switching one of the two alternating components of P0 union P1
gives R.  At the induced mixed word, the complete fibre is {R, N}, while
R union N is one Hamilton alternating cycle.

This script checks the explicit construction at every even order up to a
requested bound.  The proof that P2 always exists is Dirac's theorem; the
small recursive routine merely chooses one such matching for the audit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache


Edge = tuple[int, int]
Matching = frozenset[Edge]
Cell = tuple[int, int, int]


def edge(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def perfect_matching_avoiding(n: int, forbidden: set[Edge]) -> Matching:
    """Choose a perfect matching in K_n minus forbidden, exactly."""

    @lru_cache(maxsize=None)
    def visit(remaining: tuple[int, ...]) -> tuple[Edge, ...] | None:
        if not remaining:
            return ()
        u = remaining[0]
        for index, v in enumerate(remaining[1:], start=1):
            uv = edge(u, v)
            if uv in forbidden:
                continue
            tail = remaining[1:index] + remaining[index + 1 :]
            completion = visit(tail)
            if completion is not None:
                return (uv,) + completion
        return None

    result = visit(tuple(range(n)))
    assert result is not None
    return frozenset(result)


def matching_components(n: int, first: Matching, second: Matching) -> list[set[int]]:
    assert first.isdisjoint(second)
    adjacency = {v: [] for v in range(n)}
    for u, v in first | second:
        adjacency[u].append(v)
        adjacency[v].append(u)
    assert all(len(adjacency[v]) == 2 for v in range(n))

    unseen = set(range(n))
    components = []
    while unseen:
        root = min(unseen)
        stack = [root]
        component = set()
        while stack:
            u = stack.pop()
            if u in component:
                continue
            component.add(u)
            stack.extend(adjacency[u])
        unseen -= component
        components.append(component)
    return components


def supported_fibre(
    n: int, word: tuple[int, ...], cells: dict[Edge, Cell]
) -> list[Matching]:
    """Enumerate only perfect matchings compatible with one fixed word."""

    adjacency = {v: [] for v in range(n)}
    for uv, (left_color, right_color, _weight) in cells.items():
        u, v = uv
        if word[u] == left_color and word[v] == right_color:
            adjacency[u].append(v)
            adjacency[v].append(u)

    answers: list[Matching] = []

    def visit(remaining: frozenset[int], chosen: list[Edge]) -> None:
        if not remaining:
            answers.append(frozenset(chosen))
            return
        u = min(remaining)
        for v in adjacency[u]:
            if v not in remaining:
                continue
            chosen.append(edge(u, v))
            visit(remaining - {u, v}, chosen)
            chosen.pop()

    visit(frozenset(range(n)), [])
    return answers


def matching_weight(matching: Matching, cells: dict[Edge, Cell]) -> int:
    value = 1
    for uv in matching:
        value *= cells[uv][2]
    return value


def build(order: int):
    assert order >= 8 and order % 2 == 0
    outside_pairs = (order - 4) // 2

    p0_a = {edge(0, 1), edge(2, 3)}
    p1_a = {edge(1, 2), edge(3, 0)}
    p0_b = {edge(v, v + 1) for v in range(4, order, 2)}
    p1_b = {edge(v, v + 1) for v in range(5, order - 1, 2)}
    p1_b.add(edge(order - 1, 4))

    p0 = frozenset(p0_a | p0_b)
    p1 = frozenset(p1_a | p1_b)
    switched = frozenset(p0_a | p1_b)

    # These are the switched matching's edges, oriented and cyclically
    # ordered.  Connecting the end of one pair to the start of the next
    # produces the delocalized mate N.
    oriented_pairs = [(0, 1), (4, order - 1), (2, 3)]
    for j in range(1, outside_pairs):
        pair = (2 * j + 3, 2 * j + 4)
        oriented_pairs.append(pair if j % 2 else pair[::-1])
    assert {edge(*pair) for pair in oriented_pairs} == set(switched)

    mate = frozenset(
        edge(oriented_pairs[index][1], oriented_pairs[(index + 1) % len(oriented_pairs)][0])
        for index in range(len(oriented_pairs))
    )
    assert len(mate) == order // 2
    assert p0.isdisjoint(p1)
    assert mate.isdisjoint(p0 | p1)

    # K_n minus three edge-disjoint one-factors has minimum degree n-4,
    # which is at least n/2.  Dirac gives a Hamilton cycle and hence a
    # fourth one-factor; here we choose it directly for the audit.
    p2 = perfect_matching_avoiding(order, set(p0 | p1 | mate))
    assert p2.isdisjoint(p0 | p1 | mate)

    word = tuple(0 if v < 4 else 1 for v in range(order))
    cells: dict[Edge, Cell] = {}

    def insert(matching: Matching, colors: tuple[int, ...], negative: Edge | None = None) -> None:
        for uv in matching:
            u, v = uv
            assert uv not in cells
            cells[uv] = (colors[u], colors[v], -1 if uv == negative else 1)

    insert(p0, (0,) * order)
    insert(p1, (1,) * order)
    insert(p2, (2,) * order)
    negative_edge = edge(1, 4)
    assert negative_edge in mate
    insert(mate, word, negative_edge)

    return p0, p1, p2, switched, mate, word, cells


def audit(order: int) -> None:
    p0, p1, p2, switched, mate, word, cells = build(order)

    assert sorted(len(component) for component in matching_components(order, p0, p1)) == [
        4,
        order - 4,
    ]
    assert [len(component) for component in matching_components(order, switched, mate)] == [
        order
    ]

    for color, selected in enumerate((p0, p1, p2)):
        fibre = supported_fibre(order, (color,) * order, cells)
        assert fibre == [selected]
        assert matching_weight(selected, cells) == 1

    mixed_fibre = supported_fibre(order, word, cells)
    assert set(mixed_fibre) == {switched, mate}
    assert matching_weight(switched, cells) == 1
    assert matching_weight(mate, cells) == -1
    assert sum(matching_weight(matching, cells) for matching in mixed_fibre) == 0

    # The opposite component switch is already a mixed singleton.
    p0_a = frozenset(uv for uv in p0 if max(uv) < 4)
    p0_b = p0 - p0_a
    p1_a = frozenset(uv for uv in p1 if max(uv) < 4)
    complementary_switch = p1_a | p0_b
    complementary_word = tuple(1 if vertex < 4 else 0 for vertex in range(order))
    complementary_fibre = supported_fibre(order, complementary_word, cells)
    assert complementary_fibre == [complementary_switch]
    assert matching_weight(complementary_switch, cells) == 1

    # More importantly, the Hamilton mate itself propagates to two new
    # singleton fibres.  Recoloring either complementary P1 chord of the
    # four-cycle deletes its endpoints from switched union mate; the two
    # remaining even paths have unique perfect matchings.
    chord_terms = []
    for chord in (edge(1, 2), edge(0, 3)):
        chord_word = list(word)
        for vertex in chord:
            chord_word[vertex] = 1
        chord_fibre = supported_fibre(order, tuple(chord_word), cells)
        assert len(chord_fibre) == 1
        assert chord in chord_fibre[0]
        assert matching_weight(chord_fibre[0], cells) in (-1, 1)
        chord_terms.append(chord_fibre[0])

    # The two propagated terms form an exact multiplicative matching
    # rectangle with the Hamilton mate and the color-one anchor matching.
    assert Counter(mate) + Counter(p1) == Counter(chord_terms[0]) + Counter(
        chord_terms[1]
    )
    assert matching_weight(mate, cells) * matching_weight(
        p1, cells
    ) == matching_weight(chord_terms[0], cells) * matching_weight(
        chord_terms[1], cells
    )

    # Every site has one displayed mutual coordinate anchor in each color.
    for vertex in range(order):
        for color, anchor_matching in enumerate((p0, p1, p2)):
            anchor_edges = [uv for uv in anchor_matching if vertex in uv]
            assert len(anchor_edges) == 1
            uv = anchor_edges[0]
            assert cells[uv][:2] == (color, color)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=40)
    args = parser.parse_args()
    assert args.max_order >= 8 and args.max_order % 2 == 0

    checked = list(range(8, args.max_order + 1, 2))
    for order in checked:
        audit(order)
    print(
        "PASS uniform cycle-switch localization countermodel: "
        f"even orders 8..{args.max_order}"
    )


if __name__ == "__main__":
    main()
