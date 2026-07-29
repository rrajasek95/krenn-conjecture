#!/usr/bin/env python3
"""Exact audits for examples in binary-entry-minimal-normal-form.md."""

from __future__ import annotations

import itertools
from fractions import Fraction

from verify_binary_spinflip_cycle_identity import perfect_matchings


VERTICES = tuple(range(6))
MATCHINGS = tuple(perfect_matchings(VERTICES))


def coefficient(cells, coloring):
    total = 0
    for matching in MATCHINGS:
        term = 1
        for u, v in matching:
            term *= cells.get(((u, v), (coloring[u], coloring[v])), 0)
        total += term
    return total


def verify_binary_n_plus_two():
    cells = {}
    for edge, value in zip(((0, 1), (2, 3), (4, 5)),
                           (Fraction(1, 2), 1, 1)):
        cells[(edge, (0, 0))] = value
    for edge in ((0, 5), (1, 2), (3, 4)):
        cells[(edge, (1, 1))] = 1
    cells[((0, 2), (0, 0))] = 1
    cells[((1, 3), (0, 0))] = Fraction(1, 2)

    assert len(cells) == 8
    for coloring in itertools.product((0, 1), repeat=6):
        expected = int(len(set(coloring)) == 1)
        assert coefficient(cells, coloring) == expected, coloring

    # Every displayed scalar cell has a nonzero coefficient derivative.
    for cell in cells:
        reduced = dict(cells)
        reduced[cell] = 0
        assert any(
            coefficient(reduced, coloring) != coefficient(cells, coloring)
            for coloring in itertools.product((0, 1), repeat=6)
        ), cell


def verify_three_pairwise_binary_restrictions():
    factors = (
        ((0, 1), (2, 3), (4, 5)),
        ((0, 5), (1, 2), (3, 4)),
        ((0, 3), (1, 5), (2, 4)),
    )
    cells = {
        (edge, (color, color)): 1
        for color, matching in enumerate(factors)
        for edge in matching
    }
    for pair in itertools.combinations(range(3), 2):
        for coloring in itertools.product(pair, repeat=6):
            expected = int(len(set(coloring)) == 1)
            assert coefficient(cells, coloring) == expected, (pair, coloring)

    mixed = (2, 1, 1, 2, 0, 0)
    assert coefficient(cells, mixed) == 1
    supported = []
    for matching in MATCHINGS:
        term = 1
        for u, v in matching:
            term *= cells.get(((u, v), (mixed[u], mixed[v])), 0)
        if term:
            supported.append(matching)
    assert supported == [((0, 3), (1, 2), (4, 5))]


def main():
    verify_binary_n_plus_two()
    verify_three_pairwise_binary_restrictions()
    print("verified active eight-cell exact binary realization")
    print("verified three entry-minimal binary restrictions coexist")
    print("verified unique ternary mixed coefficient on 03|12|45")


if __name__ == "__main__":
    main()
