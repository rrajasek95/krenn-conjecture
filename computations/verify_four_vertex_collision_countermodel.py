#!/usr/bin/env python3
"""Exact six-site countermodel to an intrinsic four-vertex jet identity."""

from __future__ import annotations

import itertools
from fractions import Fraction

from verify_color_collision_n_plus_two import perfect_matchings


X, Y, Z = range(3)
N = 6
VERTICES = tuple(range(N))
CORE = (0, 1, 2, 3)


Q0 = {
    (0, 1, X, X): 1,
    (2, 3, X, X): 1,
    (4, 5, X, X): 1,
    (0, 2, X, X): 1,
    (1, 3, X, X): 1,
    (1, 2, Y, Y): 1,
    (3, 4, Y, Y): 1,
    (0, 5, Y, Y): 1,
}

Q1 = {
    (0, 1, Z, X): Fraction(-1, 2),
    (0, 2, Z, X): Fraction(1, 2),
    (0, 1, X, Z): Fraction(-1, 2),
    (1, 3, Z, X): Fraction(1, 2),
    (0, 2, X, Z): Fraction(1, 2),
    (2, 3, Z, X): Fraction(-1, 2),
    (1, 3, X, Z): Fraction(1, 2),
    (2, 3, X, Z): Fraction(-1, 2),
}

Q2 = {
    (0, 1, Z, Z): Fraction(1, 4),
    (0, 2, Z, Z): Fraction(1, 4),
    (1, 3, Z, Z): Fraction(1, 4),
    (2, 3, Z, Z): Fraction(1, 4),
}


def base_coefficient(coloring):
    total = Fraction(0)
    for matching in perfect_matchings(VERTICES):
        term = Fraction(1)
        for u, v in matching:
            term *= Q0.get((u, v, coloring[u], coloring[v]), 0)
        total += term
    return total


def first_coefficient(coloring):
    total = Fraction(0)
    for matching in perfect_matchings(VERTICES):
        for exceptional in range(3):
            term = Fraction(1)
            for position, (u, v) in enumerate(matching):
                table = Q1 if position == exceptional else Q0
                term *= table.get((u, v, coloring[u], coloring[v]), 0)
            total += term
    return total


def second_coefficient(coloring):
    total = Fraction(0)
    for matching in perfect_matchings(VERTICES):
        # One Q2 cell and two Q0 cells.
        for exceptional in range(3):
            term = Fraction(1)
            for position, (u, v) in enumerate(matching):
                table = Q2 if position == exceptional else Q0
                term *= table.get((u, v, coloring[u], coloring[v]), 0)
            total += term
        # Two Q1 cells and one Q0 cell.
        for first, second in itertools.combinations(range(3), 2):
            term = Fraction(1)
            for position, (u, v) in enumerate(matching):
                table = Q1 if position in (first, second) else Q0
                term *= table.get((u, v, coloring[u], coloring[v]), 0)
            total += term
    return total


def direct_q2_cofactor(first, second):
    remaining = tuple(v for v in VERTICES if v not in (first, second))
    coloring = tuple(
        Z if v in (first, second) else X for v in VERTICES
    )
    total = Fraction(0)
    for matching in perfect_matchings(remaining):
        term = Fraction(1)
        for u, v in matching:
            term *= Q0.get((u, v, coloring[u], coloring[v]), 0)
        total += term
    return total


def main():
    for coloring in itertools.product((X, Y), repeat=N):
        expected = 2 if coloring == (X,) * N else int(coloring == (Y,) * N)
        assert base_coefficient(coloring) == expected, coloring

    for z_site in VERTICES:
        for rest in itertools.product((X, Y), repeat=N - 1):
            coloring = list(rest)
            coloring.insert(z_site, Z)
            coloring = tuple(coloring)
            assert first_coefficient(coloring) == 0, coloring

    for first, second in itertools.combinations(CORE, 2):
        remaining = tuple(v for v in VERTICES if v not in (first, second))
        for bits in itertools.product((X, Y), repeat=4):
            coloring = [None] * N
            coloring[first] = coloring[second] = Z
            for vertex, bit in zip(remaining, bits):
                coloring[vertex] = bit
            coloring = tuple(coloring)
            expected = Fraction(1, 2) if bits == (X,) * 4 else 0
            assert second_coefficient(coloring) == expected, (
                first, second, coloring, second_coefficient(coloring)
            )

    tail_coloring = (Z, X, X, X, Z, X)
    assert direct_q2_cofactor(0, 4) == 0
    assert second_coefficient(tail_coloring) == 0
    assert second_coefficient(tail_coloring) != Fraction(1, 2)

    print("verified H(q0)=2X+Y and dH_q0(Q1)=0")
    print("verified all six core quotient-pair equations over Q")
    print("verified core-tail pair 04 has coefficient 0 instead of 1/2")


if __name__ == "__main__":
    main()
