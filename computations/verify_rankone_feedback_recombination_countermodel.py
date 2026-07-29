#!/usr/bin/env python3
"""Audit the 12-site rank-one feedback recombination countermodel.

The model has exact pure coefficients (1,1,1).  Eleven mixed fibres are
opposite-weight binomials, and all eleven Laurent exponent differences are
the same four-cycle circulation.  In particular repeated matching-square
feedback can close without increasing the original fibre and without an
odd Laurent relation.  The model is not a Krenn counterexample: one hundred
other mixed fibres are singletons.
"""

from __future__ import annotations

from collections import Counter, defaultdict


Edge = tuple[int, int]
Matching = frozenset[Edge]
Cell = tuple[int, int, int]

ORDER = 12
VERTICES = tuple(range(ORDER))


def edge(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def matching(raw_edges: list[tuple[int, int]]) -> Matching:
    result = frozenset(edge(u, v) for u, v in raw_edges)
    assert len(result) == ORDER // 2
    assert Counter(vertex for uv in result for vertex in uv) == Counter(VERTICES)
    return result


P = matching([(1, 4), (2, 5), (0, 6), (3, 7), (8, 9), (10, 11)])
W = matching([(4, 2), (5, 1), (6, 3), (7, 0), (9, 10), (11, 8)])
Q = matching([(0, 2), (1, 3), (4, 8), (5, 9), (6, 10), (7, 11)])
P0 = matching([(0, 4), (1, 6), (2, 8), (3, 10), (5, 7), (9, 11)])
P2 = matching([(0, 1), (2, 3), (4, 5), (6, 11), (7, 9), (8, 10)])

C_WORD = (0, 0, 0, 0) + (1,) * 8
WORD_12 = (0, 1, 1, 0) + (1,) * 8
WORD_30 = (1, 0, 0, 1) + (1,) * 8


def build_cells() -> dict[Edge, Cell]:
    assert len(P | W | Q | P0 | P2) == 5 * ORDER // 2
    cells: dict[Edge, Cell] = {}

    for uv in P:
        cells[uv] = (1, 1, 1)
    for uv in W:
        u, v = uv
        cells[uv] = (C_WORD[u], C_WORD[v], -1 if uv == edge(9, 10) else 1)
    for uv in Q:
        cells[uv] = (1, 1, 1)
    for uv in P0:
        cells[uv] = (0, 0, 1)
    for uv in P2:
        cells[uv] = (2, 2, 1)
    return cells


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield frozenset()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            yield tail | {edge(first, second)}


def matching_word(mate: Matching, cells: dict[Edge, Cell]) -> tuple[int, ...]:
    word = [-1] * ORDER
    for uv in mate:
        u, v = uv
        word[u], word[v] = cells[uv][:2]
    assert all(color >= 0 for color in word)
    return tuple(word)


def matching_weight(mate: Matching, cells: dict[Edge, Cell]) -> int:
    value = 1
    for uv in mate:
        value *= cells[uv][2]
    return value


def fibres(cells: dict[Edge, Cell]):
    answer: dict[tuple[int, ...], list[Matching]] = defaultdict(list)
    support = set(cells)
    for mate in perfect_matchings(VERTICES):
        if mate <= support:
            answer[matching_word(mate, cells)].append(mate)
    return answer


def signed_difference(
    binomial: list[Matching], cells: dict[Edge, Cell]
) -> tuple[frozenset[Edge], frozenset[Edge]]:
    positive = [mate for mate in binomial if matching_weight(mate, cells) == 1]
    negative = [mate for mate in binomial if matching_weight(mate, cells) == -1]
    assert len(positive) == len(negative) == 1
    return positive[0] - negative[0], negative[0] - positive[0]


def main() -> None:
    cells = build_cells()
    all_fibres = fibres(cells)

    # Each supported block has exactly one coordinate, hence rank one.  The
    # displayed P0, P, P2 matchings give a mutual anchor at every port.
    for color, anchors in ((0, P0), (1, P), (2, P2)):
        for vertex in VERTICES:
            incident = [uv for uv in anchors if vertex in uv]
            assert len(incident) == 1
            assert cells[incident[0]][:2] == (color, color)

    pure_expected = {0: (1, 1), 1: (5, 1), 2: (1, 1)}
    for color, (size, coefficient) in pure_expected.items():
        fibre = all_fibres[(color,) * ORDER]
        assert len(fibre) == size
        assert sum(matching_weight(mate, cells) for mate in fibre) == coefficient

    for word in (C_WORD, WORD_12, WORD_30):
        fibre = all_fibres[word]
        assert len(fibre) == 2
        assert sorted(matching_weight(mate, cells) for mate in fibre) == [-1, 1]

    mixed = {
        word: fibre for word, fibre in all_fibres.items() if len(set(word)) > 1
    }
    histogram = Counter(len(fibre) for fibre in mixed.values())
    assert histogram == Counter({1: 100, 2: 11})

    binomials = [fibre for fibre in mixed.values() if len(fibre) == 2]
    assert all(
        sum(matching_weight(mate, cells) for mate in fibre) == 0
        for fibre in binomials
    )
    differences = {signed_difference(fibre, cells) for fibre in binomials}
    expected_difference = (
        frozenset({edge(8, 9), edge(10, 11)}),
        frozenset({edge(8, 11), edge(9, 10)}),
    )
    assert differences == {expected_difference}

    # Since every binomial row is the same nonzero vector d, an integer
    # dependency has coefficient sum zero.  No odd Laurent dependency exists.
    first_singleton_word = min(
        word for word, fibre in mixed.items() if len(fibre) == 1
    )
    assert first_singleton_word == (0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1)

    print("PASS rank-one feedback recombination countermodel")
    print("pure fibre sizes=(1,5,1), coefficients=(1,1,1)")
    print("mixed fibre histogram={1: 100, 2: 11}; all binomials cancel")
    print("all 11 Laurent rows equal one four-cycle circulation; no odd dependency")


if __name__ == "__main__":
    main()
