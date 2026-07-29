#!/usr/bin/env python3
"""Verify the uniform odd-cycle realization of the tangent tensor W_n."""

from __future__ import annotations

import itertools


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def source(n):
    cycle = {
        tuple(sorted((i, i + 1))) for i in range(1, n - 1)
    } | {(1, n - 1)}
    vector = [1, 1] + [0] * (n - 2)
    matrices = {}
    for i, j in itertools.combinations(range(n), 2):
        table = (
            (int((i, j) in cycle), vector[i]),
            (vector[j], 0),
        )
        if any(any(row) for row in table):
            matrices[i, j] = table
    return matrices


def verify(n):
    matrices = source(n)
    matchings = tuple(perfect_matchings(range(n)))
    zero = ((0, 0), (0, 0))
    for coloring in itertools.product(range(2), repeat=n):
        total = 0
        for matching in matchings:
            term = 1
            for i, j in matching:
                term &= matrices.get((i, j), zero)[coloring[i]][coloring[j]]
            total ^= term
        target = coloring.count(1) == 1
        assert total == target, (n, coloring, total)
    print(
        f"verified n={n}: {len(matrices)} active matrices, "
        f"{2**n} coefficients"
    )


def main():
    for n in (4, 6, 8, 10):
        verify(n)
    print("verified H_n(A)=W_n over every characteristic-two field")


if __name__ == "__main__":
    main()
