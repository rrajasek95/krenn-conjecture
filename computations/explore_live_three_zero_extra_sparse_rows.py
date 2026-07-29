#!/usr/bin/env python3
"""Inspect sparse symbolic rows in the minimal one-extra response."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations, product

import sympy as sp


a, b, nu0, nu1, lam = sp.symbols("a b nu0 nu1 lambda")
H = sp.Matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
I = sp.eye(3)
D = sp.diag(1, 1, 0)
E = sp.Matrix([[1, 0, a], [0, 1, b], [0, 0, 0]])
P = (I, I, D, D, E)
BETAS = (nu0, nu1, 1, 1, 1)
ACTIVE = (2, 3, 4)
COLUMNS = tuple((site, colour) for colour in range(3) for site in ACTIVE)
COLUMN_INDEX = {column: index for index, column in enumerate(COLUMNS)}
Q = {
    (left, right): P[left] * H * P[right].T / (BETAS[left] + BETAS[right])
    for left, right in combinations(range(5), 2)
}


@lru_cache(maxsize=None)
def matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    return tuple(
        ((first, vertices[position]),) + tail
        for position in range(1, len(vertices))
        for tail in matchings(vertices[1:position] + vertices[position + 1 :])
    )


def edge(word, left, right):
    if left < right:
        return Q[left, right][word[left], word[right]]
    return Q[right, left][word[right], word[left]]


def hafnian(word, vertices):
    return sum(
        (
            sp.prod(edge(word, left, right) for left, right in matching)
            for matching in matchings(vertices)
        ),
        sp.S.Zero,
    )


def response_row(word, source_left, source_right):
    row = [sp.S.Zero] * len(COLUMNS)
    if source_left != source_right and {
        source_left,
        source_right,
    } == {0, 1}:
        for star_site in ACTIVE:
            remaining = tuple(site for site in range(5) if site != star_site)
            row[COLUMN_INDEX[star_site, word[star_site]]] += (
                lam * hafnian(word, remaining)
            )
    for u, v in combinations(range(5), 2):
        marked = (
            P[u][word[u], source_left] * P[v][word[v], source_right]
            + P[u][word[u], source_right] * P[v][word[v], source_left]
        )
        if marked == 0:
            continue
        for star_site in ACTIVE:
            if star_site in (u, v):
                continue
            remaining = tuple(
                site for site in range(5)
                if site not in (u, v, star_site)
            )
            row[COLUMN_INDEX[star_site, word[star_site]]] += (
                marked * hafnian(word, remaining)
            )
    return tuple(sp.factor(sp.cancel(entry)) for entry in row)


def main():
    sparse = {size: [] for size in range(1, 5)}
    singleton_counts = [0] * len(COLUMNS)
    for word in product(range(3), repeat=5):
        for source_left in range(3):
            for source_right in range(source_left, 3):
                row = response_row(word, source_left, source_right)
                support = tuple(index for index, entry in enumerate(row) if entry)
                if len(support) in sparse and len(sparse[len(support)]) < 80:
                    sparse[len(support)].append(
                        (word, source_left, source_right, support, row)
                    )
                if len(support) == 1:
                    singleton_counts[support[0]] += 1
    print("columns:", COLUMNS)
    print("singleton counts:", singleton_counts)
    for record in sparse[1]:
        word, source_left, source_right, support, row = record
        print(
            word,
            (source_left, source_right),
            COLUMNS[support[0]],
            row[support[0]],
        )


if __name__ == "__main__":
    main()
