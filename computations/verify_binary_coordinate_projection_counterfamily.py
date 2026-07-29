#!/usr/bin/env python3
"""Exact finite sources for every coordinate binary projection at n >= 8.

At a vertex, a nonzero coordinate projection sends each of the three
ternary basis vectors to a multiple of one of the two binary basis vectors.
After a local bit flip, exactly one species is singled out.  The three
projected GHZ summands are therefore the indicator words of an ordered
three-part partition of the vertices.

This checker audits one unit-weight ten-cell source for every unordered
partition of eight into at most three parts.  It also performs every
one-step two-vertex subdivision used by the uniform extension proof.
"""

from __future__ import annotations

from collections import Counter
from itertools import product


Edge = tuple[int, int]
Cell = tuple[int, int]
Matching = tuple[Edge, ...]


BASE_MATCHINGS: dict[tuple[int, int, int], tuple[Matching, Matching, Matching]] = {
    (8, 0, 0): (
        ((0, 4), (1, 5), (2, 6), (3, 7)),
        ((0, 2), (1, 3), (4, 7), (5, 6)),
        ((0, 2), (1, 6), (3, 5), (4, 7)),
    ),
    (7, 1, 0): (
        ((0, 4), (1, 7), (2, 3), (5, 6)),
        ((0, 2), (1, 4), (3, 5), (6, 7)),
        ((0, 6), (1, 4), (2, 7), (3, 5)),
    ),
    (6, 2, 0): (
        ((0, 5), (1, 7), (2, 3), (4, 6)),
        ((0, 2), (1, 3), (4, 5), (6, 7)),
        ((0, 2), (1, 3), (4, 7), (5, 6)),
    ),
    (6, 1, 1): (
        ((0, 7), (1, 3), (2, 5), (4, 6)),
        ((0, 2), (1, 4), (3, 5), (6, 7)),
        ((0, 2), (1, 4), (3, 7), (5, 6)),
    ),
    (5, 3, 0): (
        ((0, 5), (1, 2), (3, 4), (6, 7)),
        ((0, 3), (1, 5), (2, 6), (4, 7)),
        ((0, 3), (1, 4), (2, 5), (6, 7)),
    ),
    (5, 2, 1): (
        ((0, 4), (1, 2), (3, 7), (5, 6)),
        ((0, 2), (1, 6), (3, 4), (5, 7)),
        ((0, 2), (1, 5), (3, 4), (6, 7)),
    ),
    (4, 4, 0): (
        ((0, 4), (1, 2), (3, 7), (5, 6)),
        ((0, 2), (1, 3), (4, 5), (6, 7)),
        ((0, 2), (1, 7), (3, 4), (5, 6)),
    ),
    (4, 3, 1): (
        ((0, 4), (1, 2), (3, 6), (5, 7)),
        ((0, 1), (2, 3), (4, 7), (5, 6)),
        ((0, 1), (2, 3), (4, 5), (6, 7)),
    ),
    (4, 2, 2): (
        ((0, 3), (1, 4), (2, 5), (6, 7)),
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0, 1), (2, 7), (3, 5), (4, 6)),
    ),
    (3, 3, 2): (
        ((0, 2), (1, 3), (4, 5), (6, 7)),
        ((0, 5), (1, 4), (2, 3), (6, 7)),
        ((0, 3), (1, 6), (2, 7), (4, 5)),
    ),
}


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def target_words(parts: tuple[int, int, int]) -> tuple[tuple[int, ...], ...]:
    answer = []
    start = 0
    for size in parts:
        answer.append(
            tuple(int(start <= vertex < start + size) for vertex in range(8))
        )
        start += size
    assert start == 8
    return tuple(answer)


def source_from_terms(
    words: tuple[tuple[int, ...], ...],
    matchings: tuple[Matching, Matching, Matching],
) -> dict[Edge, set[Cell]]:
    source: dict[Edge, set[Cell]] = {}
    for word, matching in zip(words, matchings, strict=True):
        for left, right in matching:
            source.setdefault((left, right), set()).add((word[left], word[right]))
    return source


def tensor_coefficients(order: int, source: dict[Edge, set[Cell]]):
    answer: Counter[tuple[int, ...]] = Counter()
    for matching in perfect_matchings(tuple(range(order))):
        choices = [tuple(source.get(edge, ())) for edge in matching]
        if any(not edge_choices for edge_choices in choices):
            continue
        for selected in product(*choices):
            word = [0] * order
            for (left, right), (left_bit, right_bit) in zip(
                matching, selected, strict=True
            ):
                word[left] = left_bit
                word[right] = right_bit
            answer[tuple(word)] += 1
    return answer


def private_cell(
    species: int,
    words: tuple[tuple[int, ...], ...],
    matchings: tuple[Matching, Matching, Matching],
) -> tuple[Edge, Cell]:
    occurrences: Counter[tuple[Edge, Cell]] = Counter()
    for word, matching in zip(words, matchings, strict=True):
        for edge in matching:
            occurrences[edge, (word[edge[0]], word[edge[1]])] += 1
    word = words[species]
    return next(
        (edge, (word[edge[0]], word[edge[1]]))
        for edge in matchings[species]
        if occurrences[edge, (word[edge[0]], word[edge[1]])] == 1
    )


def subdivide(
    source: dict[Edge, set[Cell]],
    selected: tuple[Edge, Cell],
    order: int,
) -> dict[Edge, set[Cell]]:
    """Replace one decorated cell uv by the path u-a-b-v.

    The selected species has bits 1,1 at the new vertices.  Every other
    species uses the internal path edge and has bits 0,0 there.
    """

    edge, cell = selected
    left, right = edge
    left_bit, right_bit = cell
    first_new, second_new = order, order + 1
    answer = {key: set(values) for key, values in source.items()}
    answer[edge].remove(cell)
    if not answer[edge]:
        del answer[edge]
    answer.setdefault((left, first_new), set()).add((left_bit, 1))
    answer.setdefault((first_new, second_new), set()).add((0, 0))
    answer.setdefault((right, second_new), set()).add((right_bit, 1))
    return answer


def main():
    assert set(BASE_MATCHINGS) == {
        (first, second, third)
        for first in range(8, -1, -1)
        for second in range(min(first, 8 - first), -1, -1)
        for third in (8 - first - second,)
        if second >= third >= 0
    }

    base_cell_counts = set()
    for parts, matchings in BASE_MATCHINGS.items():
        words = target_words(parts)
        source = source_from_terms(words, matchings)
        assert tensor_coefficients(8, source) == Counter(words)
        base_cell_counts.add(sum(map(len, source.values())))

        # Every target occurrence has a cell which belongs to no other one.
        selected = tuple(
            private_cell(species, words, matchings) for species in range(3)
        )
        assert len(set(selected)) == 3

        # Audit all three one-step extensions.  The source is still unit
        # weight, and its supported terms are exactly the extended targets.
        for species in range(3):
            expanded = subdivide(source, selected[species], 8)
            expanded_words = tuple(
                word + ((1, 1) if index == species else (0, 0))
                for index, word in enumerate(words)
            )
            assert tensor_coefficients(10, expanded) == Counter(expanded_words)

    assert base_cell_counts == {10}
    print(
        "PASS coordinate projection counterfamily: 10/10 order-eight "
        "partition types use ten cells; all 30 two-vertex extensions audited"
    )


if __name__ == "__main__":
    main()
