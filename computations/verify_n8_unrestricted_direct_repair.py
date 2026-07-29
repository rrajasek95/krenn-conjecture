#!/usr/bin/env python3
"""Independently verify the displayed minimum direct repair at n=8."""

from __future__ import annotations

from collections import Counter
from itertools import product


N = 8
Q = 3


def cell(u, v, a, b):
    return (u, v, a, b) if u < v else (v, u, b, a)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


PURE = (
    ((0, 1), (2, 3), (4, 5), (6, 7)),
    ((1, 2), (3, 4), (5, 6), (0, 7)),
    ((0, 2), (1, 4), (3, 6), (5, 7)),
)
EXTRAS = (
    (((0, 3), (1, 5), (2, 6), (4, 7)), (1, 2, 0, 0, 2, 1, 1, 1)),
    (((0, 4), (1, 6), (2, 5), (3, 7)), (1, 1, 1, 2, 0, 0, 2, 1)),
)
SEED = frozenset(
    cell(u, v, colour, colour)
    for colour, matching in enumerate(PURE)
    for u, v in matching
) | frozenset(
    cell(u, v, word[u], word[v])
    for matching, word in EXTRAS
    for u, v in matching
)
ADDED = frozenset(
    {
        (0, 1, 1, 2),
        (0, 3, 2, 1),
        (0, 4, 0, 1),
        (1, 3, 0, 1),
        (1, 4, 1, 0),
        (2, 3, 1, 2),
        (2, 4, 0, 0),
        (2, 4, 2, 1),
        (2, 7, 0, 1),
        (3, 4, 0, 2),
        (3, 6, 2, 1),
        (5, 6, 0, 2),
        (5, 7, 1, 1),
    }
)


def fibres(support):
    matchings = tuple(perfect_matchings(range(N)))
    answer = {}
    for word in product(range(Q), repeat=N):
        terms = []
        for matching in matchings:
            decorated = tuple(
                cell(u, v, word[u], word[v]) for u, v in matching
            )
            if set(decorated) <= support:
                terms.append(decorated)
        if terms:
            answer[word] = tuple(terms)
    return answer


def mixed_histogram(all_fibres):
    return Counter(
        len(terms)
        for word, terms in all_fibres.items()
        if len(set(word)) > 1
    )


def main():
    assert len(SEED) == 20 and len(ADDED) == 13
    assert SEED.isdisjoint(ADDED)
    seed_fibres = fibres(SEED)
    assert mixed_histogram(seed_fibres) == Counter({1: 24, 2: 2})
    original_singletons = {
        word
        for word, terms in seed_fibres.items()
        if len(set(word)) > 1 and len(terms) == 1
    }
    assert len(original_singletons) == 24

    repaired = fibres(SEED | ADDED)
    assert all(len(repaired[word]) >= 2 for word in original_singletons)
    assert tuple(len(repaired[(colour,) * N]) for colour in range(Q)) == (1, 1, 1)
    histogram = mixed_histogram(repaired)
    assert histogram == Counter({1: 58, 2: 41, 3: 9, 4: 5, 5: 1, 6: 1, 8: 1})

    print("PASS n=8 unrestricted minimum direct-repair witness")
    print("support=33 (seed 20 + direct-repair optimum 13)")
    print("all 24 original singletons repaired; 58 new singletons remain")
    print("mixed histogram={1:58,2:41,3:9,4:5,5:1,6:1,8:1}")


if __name__ == "__main__":
    main()
