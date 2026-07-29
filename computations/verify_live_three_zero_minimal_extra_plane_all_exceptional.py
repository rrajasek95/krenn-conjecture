#!/usr/bin/env python3
"""Exact audit for the minimal all-exceptional extra-plane response."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations

import sympy as sp


a, b, nu0, nu1, direct_scale = sp.symbols(
    "a b nu0 nu1 direct_scale"
)
H = sp.Matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
I = sp.eye(3)
D = sp.diag(1, 1, 0)
BETAS = (nu0, nu1, 1, 1, 1)
ACTIVE = (2, 3, 4)
COLUMNS = tuple((site, colour) for colour in range(3) for site in ACTIVE)
COLUMN_INDEX = {column: index for index, column in enumerate(COLUMNS)}


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    return tuple(
        ((first, vertices[position]),) + tail
        for position in range(1, len(vertices))
        for tail in perfect_matchings(
            vertices[1:position] + vertices[position + 1 :]
        )
    )


def response_builder(extra):
    matrices = (I, I, D, D, extra)
    blocks = {
        (left, right): (
            matrices[left] * H * matrices[right].T
            / (BETAS[left] + BETAS[right])
        )
        for left, right in combinations(range(5), 2)
    }

    def edge(word, left, right):
        if left < right:
            return blocks[left, right][word[left], word[right]]
        return blocks[right, left][word[right], word[left]]

    def hafnian(word, vertices):
        return sum(
            (
                sp.prod(
                    edge(word, left, right)
                    for left, right in matching
                )
                for matching in perfect_matchings(vertices)
            ),
            sp.S.Zero,
        )

    def response(word_text, source_left, source_right):
        word = tuple(map(int, word_text))
        row = [sp.S.Zero] * len(COLUMNS)
        if (
            source_left != source_right
            and {source_left, source_right} == {0, 1}
        ):
            for star_site in ACTIVE:
                remaining = tuple(
                    site for site in range(5) if site != star_site
                )
                row[COLUMN_INDEX[star_site, word[star_site]]] += (
                    direct_scale * hafnian(word, remaining)
                )
        for left, right in combinations(range(5), 2):
            marked = (
                matrices[left][word[left], source_left]
                * matrices[right][word[right], source_right]
                + matrices[left][word[left], source_right]
                * matrices[right][word[right], source_left]
            )
            if marked == 0:
                continue
            for star_site in ACTIVE:
                if star_site in (left, right):
                    continue
                remaining = tuple(
                    site
                    for site in range(5)
                    if site not in (left, right, star_site)
                )
                row[COLUMN_INDEX[star_site, word[star_site]]] += (
                    marked * hafnian(word, remaining)
                )
        return sp.Matrix([[sp.cancel(entry) for entry in row]])

    return response


def assert_singleton(row, column, coefficient):
    expected = sp.zeros(1, len(COLUMNS))
    expected[0, COLUMN_INDEX[column]] = coefficient
    assert all(
        sp.cancel(left - right) == 0
        for left, right in zip(row, expected)
    )


def audit_chart_01():
    response = response_builder(
        sp.Matrix([[1, 0, a], [0, 1, b], [0, 0, 0]])
    )
    delta = 2 / (nu0 + nu1)
    epsilon = 2 / (nu1 + 1)
    rows = (
        ("02011", 1, (2, 0), delta),
        ("02101", 1, (3, 0), delta),
        ("02110", 1, (4, 0), delta),
        ("12100", 0, (2, 1), delta),
        ("12010", 0, (3, 1), delta),
        ("12001", 0, (4, 1), delta),
        ("02201", 0, (2, 2), epsilon),
        ("02021", 0, (3, 2), epsilon),
        ("22012", 2, (4, 2), sp.S.One),
    )
    for word, source, column, coefficient in rows:
        assert_singleton(
            response(word, source, source), column, coefficient
        )


def audit_triangular_chart(extra, singleton_rows, final_row, final_support):
    response = response_builder(extra)
    for word, source, column, coefficient in singleton_rows:
        assert_singleton(
            response(word, source, source), column, coefficient
        )
    row = response(final_row[0], final_row[1], final_row[1])
    expected = sp.zeros(1, len(COLUMNS))
    for column, coefficient in final_support:
        expected[0, COLUMN_INDEX[column]] = coefficient
    assert all(
        sp.cancel(left - right) == 0
        for left, right in zip(row, expected)
    )


def audit_chart_12():
    delta = 2 / (nu0 + nu1)
    alpha = 2 / (nu0 + 1)
    epsilon = 2 / (nu1 + 1)
    rows = (
        ("02010", 1, (2, 0), delta),
        ("02100", 1, (3, 0), delta),
        ("12101", 2, (2, 1), alpha),
        ("12011", 2, (3, 1), alpha),
        ("02111", 1, (4, 1), delta),
        ("01211", 1, (2, 2), alpha),
        ("01121", 1, (3, 2), alpha),
        ("02012", 0, (4, 2), epsilon),
    )
    audit_triangular_chart(
        sp.Matrix([[a, 1, 0], [b, 0, 1], [0, 0, 0]]),
        rows,
        ("02110", 1),
        (((4, 0), delta), ((2, 1), delta), ((3, 1), delta)),
    )


def audit_chart_02():
    delta = 2 / (nu0 + nu1)
    alpha = 2 / (nu0 + 1)
    epsilon = 2 / (nu1 + 1)
    rows = (
        ("02011", 2, (2, 0), alpha),
        ("02101", 2, (3, 0), alpha),
        ("12100", 0, (2, 1), delta),
        ("12010", 0, (3, 1), delta),
        ("12001", 0, (4, 1), delta),
        ("00211", 0, (2, 2), sp.S.One),
        ("00121", 0, (3, 2), sp.S.One),
        ("02012", 0, (4, 2), epsilon),
    )
    audit_triangular_chart(
        sp.Matrix([[1, a, 0], [0, b, 1], [0, 0, 0]]),
        rows,
        ("12000", 0),
        (((4, 0), delta), ((2, 0), delta), ((3, 0), delta)),
    )


def main():
    audit_chart_01()
    audit_chart_12()
    audit_chart_02()
    print("Live three-zero minimal extra-plane response: PASS")
    print("01 chart: exact diagonal 9-square")
    print("12 and 02 charts: eight singleton pivots plus one triangular row")
    print("all pivots independent of the two kernel parameters and direct term")


if __name__ == "__main__":
    main()
