#!/usr/bin/env python3
"""Exact triangular audit for one exceptional live site and one extra plane."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations

import sympy as sp


a, b, nu, direct_scale = sp.symbols("a b nu direct_scale")
H = sp.Matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
I = sp.eye(3)
D = sp.diag(1, 1, 0)
BETAS = (nu, 1, 1, 1, 1)
ACTIVE = (1, 2, 3, 4)
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
        return [sp.cancel(entry) for entry in row]

    return response


def audit_chart(extra, rows):
    response = response_builder(extra)
    killed = set()
    for word, source_left, source_right, pivot, coefficient in rows:
        row = response(word, source_left, source_right)
        pivot_index = COLUMN_INDEX[pivot]
        assert sp.cancel(row[pivot_index] - coefficient) == 0
        assert all(
            entry == 0 or index in killed or index == pivot_index
            for index, entry in enumerate(row)
        )
        killed.add(pivot_index)
    assert len(killed) == len(COLUMNS)


def main():
    alpha = 2 / (nu + 1)
    chart_01 = (
        ("02012", 0, 0, (4, 2), 1),
        ("02021", 0, 0, (3, 2), 1),
        ("02201", 0, 0, (2, 2), 1),
        ("02011", 1, 1, (2, 0), alpha),
        ("02101", 1, 1, (3, 0), alpha),
        ("12010", 0, 0, (3, 1), alpha),
        ("12100", 0, 0, (2, 1), alpha),
        ("22000", 0, 0, (1, 2), 3 * alpha),
        ("02110", 1, 1, (4, 0), alpha),
        ("12001", 0, 0, (4, 1), alpha),
        ("20011", 1, 1, (1, 0), alpha),
        ("21001", 0, 0, (1, 1), alpha),
    )
    chart_12 = (
        ("02012", 0, 0, (4, 2), 1),
        ("10121", 1, 1, (3, 2), 1),
        ("10211", 1, 1, (2, 2), 1),
        ("00110", 1, 1, (1, 0), 3 * alpha),
        ("01010", 1, 1, (2, 0), 3 * alpha),
        ("01100", 1, 1, (3, 0), 3 * alpha),
        ("10011", 0, 2, (3, 1), alpha),
        ("10101", 0, 2, (2, 1), alpha),
        ("11001", 0, 2, (1, 1), alpha),
        ("22010", 1, 1, (1, 2), alpha),
        ("02111", 1, 1, (4, 1), alpha),
        ("22010", 2, 2, (4, 0), 1),
    )
    chart_02 = (
        ("00121", 0, 0, (3, 2), 1),
        ("00211", 0, 0, (2, 2), 1),
        ("02012", 0, 0, (4, 2), 1),
        ("00111", 1, 2, (1, 0), alpha),
        ("01011", 1, 2, (2, 0), alpha),
        ("01101", 1, 2, (3, 0), alpha),
        ("10010", 0, 0, (3, 1), 3 * alpha),
        ("10100", 0, 0, (2, 1), 3 * alpha),
        ("11000", 0, 0, (1, 1), 3 * alpha),
        ("22010", 0, 0, (1, 2), alpha),
        ("12001", 0, 0, (4, 1), alpha),
        ("22010", 2, 2, (4, 0), 1),
    )
    audit_chart(
        sp.Matrix([[1, 0, a], [0, 1, b], [0, 0, 0]]),
        chart_01,
    )
    audit_chart(
        sp.Matrix([[a, 1, 0], [b, 0, 1], [0, 0, 0]]),
        chart_12,
    )
    audit_chart(
        sp.Matrix([[1, a, 0], [0, b, 1], [0, 0, 0]]),
        chart_02,
    )
    print("Live three-zero minimal extra-plane, one exceptional: PASS")
    print("three exact triangular 12-square response minors")
    print("all pivots independent of kernel parameters and direct-term scale")


if __name__ == "__main__":
    main()
