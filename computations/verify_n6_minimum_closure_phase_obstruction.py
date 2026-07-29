#!/usr/bin/env python3
"""Verify the first minimum unrestricted closure and its odd phase circuit.

This checker is solver-independent.  The accompanying optimization script
proves the cardinality minimum by exact RC2 plus universally valid lazy
singleton clauses; here we independently check its displayed 35-cell model,
all fibre sizes, and the three-binomial Laurent contradiction.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product


N = 6
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
    ((0, 1), (2, 3), (4, 5)),
    ((1, 2), (3, 4), (0, 5)),
    ((0, 2), (1, 4), (3, 5)),
)
EXTRAS = (
    (((0, 3), (1, 5), (2, 4)), (0, 0, 0, 1, 2, 2)),
    (((0, 4), (1, 3), (2, 5)), (0, 2, 1, 0, 1, 0)),
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
        (0, 1, 2, 0),
        (0, 2, 0, 1),
        (0, 2, 0, 2),
        (0, 2, 2, 1),
        (0, 3, 0, 2),
        (0, 3, 2, 1),
        (0, 3, 2, 2),
        (0, 4, 0, 0),
        (0, 4, 2, 0),
        (0, 4, 2, 1),
        (1, 5, 0, 0),
        (2, 5, 1, 2),
        (2, 5, 2, 0),
        (2, 5, 2, 2),
        (3, 5, 1, 0),
        (3, 5, 1, 2),
        (3, 5, 2, 0),
        (4, 5, 0, 2),
        (4, 5, 1, 0),
        (4, 5, 1, 2),
    }
)
SUPPORT = SEED | ADDED
ALL_CELLS = tuple(
    (u, v, a, b)
    for u, v in combinations(range(N), 2)
    for a, b in product(range(Q), repeat=2)
)


def fibres():
    matchings = tuple(perfect_matchings(range(N)))
    answer = {}
    for word in product(range(Q), repeat=N):
        terms = []
        for matching in matchings:
            decorated = tuple(
                cell(u, v, word[u], word[v]) for u, v in matching
            )
            if set(decorated) <= SUPPORT:
                terms.append(decorated)
        if terms:
            answer[word] = tuple(terms)
    return answer


def exponent_row(terms):
    assert len(terms) == 2
    return Counter(terms[0]) - Counter(terms[1]), Counter(terms[1]) - Counter(terms[0])


def signed_row(terms):
    positive, negative = exponent_row(terms)
    answer = Counter(positive)
    answer.subtract(negative)
    return +answer, +(-answer)


def add_signed_rows(summands):
    total = Counter()
    for coefficient, (positive, negative) in summands:
        if coefficient > 0:
            total.update({entry: coefficient * value for entry, value in positive.items()})
            total.subtract({entry: coefficient * value for entry, value in negative.items()})
        else:
            coefficient = -coefficient
            total.update({entry: coefficient * value for entry, value in negative.items()})
            total.subtract({entry: coefficient * value for entry, value in positive.items()})
    return +total, +(-total)


def dense_row(terms):
    counts = Counter(terms[0])
    counts.subtract(terms[1])
    return tuple(counts[cell] for cell in ALL_CELLS)


def unit_triangle_circuits(rows):
    locations = {}
    for index, row in enumerate(rows):
        locations.setdefault(row, []).append(index)
    circuits = set()
    for left in range(len(rows)):
        for right in range(left + 1, len(rows)):
            for left_sign in (-1, 1):
                for right_sign in (-1, 1):
                    target = tuple(
                        -(left_sign * a + right_sign * b)
                        for a, b in zip(rows[left], rows[right])
                    )
                    for third in locations.get(target, ()):
                        if third not in (left, right):
                            circuits.add(tuple(sorted((left, right, third))))
    return tuple(sorted(circuits))


def format_term(term):
    return " ".join(f"{u}{v};{a}{b}" for u, v, a, b in term)


def main():
    assert len(SEED) == 15
    assert len(ADDED) == 20 and SEED.isdisjoint(ADDED)
    assert len(SUPPORT) == 35

    all_fibres = fibres()
    pure_sizes = tuple(len(all_fibres[(colour,) * N]) for colour in range(Q))
    mixed = {
        word: terms
        for word, terms in all_fibres.items()
        if len(set(word)) > 1
    }
    histogram = Counter(map(len, mixed.values()))
    assert pure_sizes == (2, 1, 2)
    assert len(mixed) == 71 and histogram == Counter({2: 71})

    circuit_words = (
        (0, 0, 0, 0, 0, 2),
        (0, 0, 0, 1, 2, 2),
        (0, 1, 1, 1, 0, 2),
    )
    coefficients = (1, -1, -1)
    rows = tuple(signed_row(mixed[word]) for word in circuit_words)
    assert add_signed_rows(zip(coefficients, rows, strict=True)) == (Counter(), Counter())
    assert sum(coefficients) % 2 == 1

    ordered_mixed = tuple(sorted(mixed.items()))
    dense_rows = tuple(dense_row(terms) for _word, terms in ordered_mixed)
    triangles = unit_triangle_circuits(dense_rows)
    assert len(triangles) == 73
    assert (0, 4, 12) in triangles
    for triangle in triangles:
        assert any(
            all(
                sum(
                    signs[position] * dense_rows[row_index][column]
                    for position, row_index in enumerate(triangle)
                )
                == 0
                for column in range(len(ALL_CELLS))
            )
            for signs in product((-1, 1), repeat=3)
        )

    # Pin the exact six terms as a readable guard against ordering mistakes.
    expected = (
        (
            "01;00 23;00 45;02",
            "04;00 15;02 23;00",
        ),
        (
            "01;00 24;02 35;12",
            "03;01 15;02 24;02",
        ),
        (
            "03;01 12;11 45;02",
            "04;00 12;11 35;12",
        ),
    )
    assert tuple(
        tuple(format_term(term) for term in mixed[word])
        for word in circuit_words
    ) == expected

    print("PASS n=6 minimum-closure candidate phase obstruction")
    print("support=35 (seed 15 + minimum 20), pure sizes=(2,1,2)")
    print("mixed histogram={2:71}")
    print("odd circuit: D(000002)-D(000122)-D(011102)=0")
    print("all 73 unit three-row phase cores verified")


if __name__ == "__main__":
    main()
