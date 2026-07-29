#!/usr/bin/env python3
"""Exact audit of a primitive Z/8 base-locus lift and its frozen next jet.

The aggregate edge tables below have only diagonal endpoint colors.  Their
six-site hafnian tensor is

    2 Delta_(6,3) + 8 e_2 e_1 e_0 e_1 e_2 e_0

over the integers.  Consequently it is 2 Delta modulo eight.  At the lone
mixed coloring every selected base entry is even, so changing any aggregate
entry by a multiple of eight cannot change that coefficient modulo sixteen.
"""

from __future__ import annotations

import itertools


N = 6
Q = 3
BAD_COLORING = (2, 1, 0, 1, 2, 0)


def perfect_matchings(vertices=tuple(range(N))):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings())
ZERO = ((0, 0, 0),) * 3


def diagonal(color: int, value: int):
    table = [[0] * Q for _ in range(Q)]
    table[color][color] = value
    return tuple(tuple(row) for row in table)


SOURCE = {
    # Color 0: 01 | 25 | 34, with product 2.
    (0, 1): diagonal(0, 1),
    (2, 5): diagonal(0, 2),
    (3, 4): diagonal(0, 1),
    # Color 1: 02 | 13 | 45, with product 2.
    (0, 2): diagonal(1, 1),
    (1, 3): diagonal(1, 2),
    (4, 5): diagonal(1, 1),
    # Color 2: 04 | 12 | 35, with product 2.
    (0, 4): diagonal(2, 2),
    (1, 2): diagonal(2, 1),
    (3, 5): diagonal(2, 1),
}


def selected_values(source, coloring, matching):
    return tuple(
        source.get((u, v), ZERO)[coloring[u]][coloring[v]]
        for u, v in matching
    )


def coefficients(source):
    values = {}
    for coloring in itertools.product(range(Q), repeat=N):
        total = 0
        for matching in MATCHINGS:
            term = 1
            for value in selected_values(source, coloring, matching):
                term *= value
            total += term
        values[coloring] = total
    return values


def main():
    values = coefficients(SOURCE)
    exceptional = {}
    for coloring, value in values.items():
        target = 2 if len(set(coloring)) == 1 else 0
        if value != target:
            exceptional[coloring] = value - target
        assert value % 8 == target

    assert exceptional == {BAD_COLORING: 8}
    assert SOURCE[(0, 1)][0][0] % 2 == 1
    print("verified exact integer identity H(A)=2*Delta+8*e_210120")
    print("verified primitive source and H(A)=2*Delta modulo 8")

    # If A' = A + 8C, then modulo 16 only the linear correction can matter:
    # 8*C_e times the product of the other two selected base entries.  At the
    # bad coloring those products are all even, hence every correction is 0.
    for matching in MATCHINGS:
        selected = selected_values(SOURCE, BAD_COLORING, matching)
        for exceptional_edge in range(3):
            other_product = 1
            for index, value in enumerate(selected):
                if index != exceptional_edge:
                    other_product *= value
            assert other_product % 2 == 0
    assert values[BAD_COLORING] % 16 == 8
    print(
        "verified every lift A+8C retains mixed coefficient 8 modulo 16"
    )


if __name__ == "__main__":
    main()
