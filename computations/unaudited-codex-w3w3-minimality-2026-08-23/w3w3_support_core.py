#!/usr/bin/env python3
"""Exact occurrence-layer model for the PyTheus W3 x W3 experiment.

There are six output vertices and two endpoint colours.  A source coordinate
is a tuple ``(u, v, a, b)`` with ``u < v`` and endpoint colours ``a,b``.  A
perfect-matching occurrence for a word is present exactly when its three
source coordinates are present.

The Boolean screen imposes necessary conditions for an exact complex-weighted
realization:

* each of the nine target words occurs at least once; and
* no forbidden word occurs exactly once.

The second condition is sound because a single occurrence is a nonzero
Laurent monomial in the selected source weights and therefore cannot cancel.
It is only a necessary condition: supports surviving this screen still need
the phase/Laurent equations.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product


N = 6
COLOURS = (0, 1)
VERTICES = tuple(range(N))
WORDS = tuple(product(COLOURS, repeat=N))
TARGET_WORDS = frozenset(
    tuple(map(int, left + right))
    for left in ("001", "010", "100")
    for right in ("001", "010", "100")
)
SOURCES = tuple(
    (u, v, a, b)
    for u, v in combinations(VERTICES, 2)
    for a, b in product(COLOURS, repeat=2)
)
SOURCE_INDEX = {source: index for index, source in enumerate(SOURCES)}


def require(condition: bool, detail) -> None:
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices=VERTICES):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings())
require(len(MATCHINGS) == 15, len(MATCHINGS))
require(len(SOURCES) == 60, len(SOURCES))
require(len(TARGET_WORDS) == 9, len(TARGET_WORDS))


def source_for(edge: tuple[int, int], word: tuple[int, ...]):
    u, v = edge
    return (u, v, word[u], word[v])


OCCURRENCES = {
    word: tuple(
        tuple(source_for(edge, word) for edge in matching)
        for matching in MATCHINGS
    )
    for word in WORDS
}


def occurrence_counts(support):
    support = frozenset(tuple(source) for source in support)
    require(support <= frozenset(SOURCES), sorted(support - frozenset(SOURCES)))
    return {
        word: sum(all(source in support for source in occurrence)
                  for occurrence in OCCURRENCES[word])
        for word in WORDS
    }


def audit_target_cover(support, maximum_sources: int):
    support = tuple(sorted(tuple(source) for source in support))
    require(len(support) <= maximum_sources,
            ("source bound", len(support), maximum_sources))
    require(len(set(support)) == len(support), "duplicate sources")
    counts = occurrence_counts(support)
    for word in TARGET_WORDS:
        require(counts[word] >= 1, ("missing target", word))
    return {
        "support": [list(source) for source in support],
        "source_count": len(support),
        "target_multiplicities": {
            "".join(map(str, word)): counts[word]
            for word in sorted(TARGET_WORDS)
        },
    }


def audit_occurrence_support(support, maximum_sources: int):
    audited = audit_target_cover(support, maximum_sources)
    support = tuple(tuple(source) for source in audited["support"])
    counts = occurrence_counts(support)
    for word in frozenset(WORDS) - TARGET_WORDS:
        require(counts[word] != 1, ("forbidden singleton", word))
    return audited | {
        "multiplicity_histogram": {
            str(key): value for key, value in sorted(Counter(counts.values()).items())
        },
        "forbidden_nonzero_words": [
            "".join(map(str, word))
            for word in WORDS
            if word not in TARGET_WORDS and counts[word] > 0
        ],
    }


# The ten nonzero source coordinates in PyTheus's published exact solution.
PYTHEUS_TEN_SOURCE_SOLUTION = (
    (0, 2, 1, 0),
    (0, 4, 0, 0),
    (0, 5, 0, 0),
    (1, 2, 0, 1),
    (1, 2, 1, 0),
    (1, 4, 0, 0),
    (1, 5, 0, 0),
    (3, 4, 0, 1),
    (3, 4, 1, 0),
    (3, 5, 0, 1),
)
