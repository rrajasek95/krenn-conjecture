#!/usr/bin/env python3
"""Exact minors for the all-common-beta minimal extra-plane response."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


a, b = sp.symbols("a b")
H = sp.Matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
I = sp.eye(3)
D = sp.diag(1, 1, 0)
SITES = tuple(range(5))
COLUMNS = tuple((site, colour) for colour in range(3) for site in SITES)
COLUMN_INDEX = {column: index for index, column in enumerate(COLUMNS)}


def response_builder(extra):
    matrices = (I, I, D, D, extra)
    blocks = {
        (left, right): matrices[left] * H * matrices[right].T / 2
        for left, right in combinations(SITES, 2)
    }

    def edge(word, left, right):
        if left < right:
            return blocks[left, right][word[left], word[right]]
        return blocks[right, left][word[right], word[left]]

    def response(word_text, source):
        word = tuple(map(int, word_text))
        row = [sp.S.Zero] * len(COLUMNS)
        for left, right in combinations(SITES, 2):
            marked = (
                2
                * matrices[left][word[left], source]
                * matrices[right][word[right], source]
            )
            if marked == 0:
                continue
            for star_site in SITES:
                if star_site in (left, right):
                    continue
                remaining = tuple(
                    site
                    for site in SITES
                    if site not in (left, right, star_site)
                )
                assert len(remaining) == 2
                row[COLUMN_INDEX[star_site, word[star_site]]] += (
                    marked * edge(word, *remaining)
                )
        return tuple(sp.cancel(entry) for entry in row)

    return response


def determinant(response, labels):
    assert len(labels) == len(COLUMNS)
    return sp.factor(
        sp.cancel(
            sp.Matrix(
                [response(word, source) for word, source in labels]
            ).det(method="domain-ge")
        )
    )


CHART_01_A = (
    ("00000", 0),
    ("00010", 0),
    ("00011", 0),
    ("00012", 0),
    ("00020", 0),
    ("00100", 0),
    ("00110", 1),
    ("00200", 0),
    ("01000", 0),
    ("01010", 1),
    ("01100", 1),
    ("01111", 1),
    ("02000", 0),
    ("10000", 0),
    ("20000", 0),
)

CHART_01_B = (
    ("00010", 0),
    ("00011", 0),
    ("00012", 0),
    ("00100", 0),
    ("00110", 0),
    ("00111", 1),
    ("00120", 0),
    ("00210", 0),
    ("01000", 0),
    ("01010", 0),
    ("01100", 0),
    ("01110", 1),
    ("02010", 0),
    ("10010", 0),
    ("20010", 0),
)

CHART_01_C = (
    ("00001", 0),
    ("00010", 0),
    ("00011", 0),
    ("00012", 0),
    ("00021", 0),
    ("00100", 0),
    ("00101", 0),
    ("00110", 0),
    ("00201", 0),
    ("01000", 0),
    ("01001", 0),
    ("01110", 1),
    ("02001", 0),
    ("10001", 0),
    ("20001", 0),
)

CHART_12 = (
    ("00000", 0),
    ("00010", 0),
    ("00011", 0),
    ("00012", 0),
    ("00020", 0),
    ("00100", 0),
    ("00110", 1),
    ("00200", 0),
    ("01000", 0),
    ("01010", 1),
    ("01100", 1),
    ("01110", 1),
    ("02000", 0),
    ("10000", 0),
    ("20000", 0),
)

CHART_02 = (
    ("11110", 1),
    ("11100", 1),
    ("11101", 1),
    ("11102", 1),
    ("11120", 1),
    ("11010", 1),
    ("11000", 0),
    ("11210", 1),
    ("10110", 1),
    ("10100", 0),
    ("10010", 0),
    ("10000", 0),
    ("12110", 1),
    ("01110", 1),
    ("21110", 1),
)


def main():
    response_01 = response_builder(
        sp.Matrix([[1, 0, a], [0, 1, b], [0, 0, 0]])
    )
    determinants_01 = (
        determinant(response_01, CHART_01_A),
        determinant(response_01, CHART_01_B),
        determinant(response_01, CHART_01_C),
    )
    expected_01 = (
        2_125_764 * a**11,
        108 * (a + 3) ** 10 * (2 * a + 3) * (b + 3),
        -708_588
        * (a + 3)
        * (4 * a + 3)
        * (b + 1) ** 6
        * (a + 3 * b + 3) ** 2,
    )
    assert all(
        sp.cancel(actual - expected) == 0
        for actual, expected in zip(determinants_01, expected_01)
    )
    residual_b = sp.cancel(expected_01[1].subs(a, 0) / (b + 3))
    assert residual_b != 0 and not residual_b.free_symbols
    assert expected_01[2].subs({a: 0, b: -3}) != 0

    response_12 = response_builder(
        sp.Matrix([[a, 1, 0], [b, 0, 1], [0, 0, 0]])
    )
    response_02 = response_builder(
        sp.Matrix([[1, a, 0], [0, b, 1], [0, 0, 0]])
    )
    assert determinant(response_12, CHART_12) == 57_395_628
    assert determinant(response_02, CHART_02) == 57_395_628

    print("Live three-zero minimal extra-plane, common beta: PASS")
    print("chart 01: three exact minors with empty common zero set")
    print("charts 12 and 02: parameter-independent exact minors")


if __name__ == "__main__":
    main()
