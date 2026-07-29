#!/usr/bin/env python3
"""Exact count audit for the common-beta one-extra-plane all-order proof."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations
from math import comb, factorial

import sympy as sp


p0, p1, p2, r_symbol = sp.symbols("p0 p1 p2 r")
p = sp.Matrix([[p0, p1, p2]])
e0 = sp.Matrix([[1, 0, 0]])
e1 = sp.Matrix([[0, 1, 0]])
e2 = sp.Matrix([[0, 0, 1]])
H = sp.Matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])


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


def response_coefficients(rows, source):
    sites = tuple(range(len(rows)))

    def edge(left, right):
        return (rows[left] * H * rows[right].T)[0] / 2

    def hafnian(vertices):
        return sum(
            (
                sp.prod(edge(left, right) for left, right in matching)
                for matching in perfect_matchings(tuple(vertices))
            ),
            sp.S.Zero,
        )

    coefficients = []
    for star in sites:
        value = sp.S.Zero
        for left, right in combinations(
            tuple(site for site in sites if site != star), 2
        ):
            marked = 2 * rows[left][source] * rows[right][source]
            if marked == 0:
                continue
            remaining = tuple(
                site
                for site in sites
                if site not in (star, left, right)
            )
            value += marked * hafnian(remaining)
        coefficients.append(sp.factor(sp.cancel(value)))
    return tuple(coefficients)


def incidence_rank(point_count, subset_size):
    subsets = tuple(combinations(range(point_count), subset_size))
    matrix = sp.Matrix(
        [
            [int(point in subset) for point in range(point_count)]
            for subset in subsets
        ]
    )
    return matrix.rank()


def audit_r(r):
    coordinate_count = 2 * r + 2
    scalar = sp.Rational((r + 1) * factorial(r), 2**r)

    # Row-zero subset family A: r+1 coordinate zeros, source 1.
    rows = [e0] * (r + 1) + [e1] * (r + 1) + [p]
    coefficients = response_coefficients(rows, 1)
    expected = scalar * ((r + 2) * p1 + r * p2)
    assert all(sp.cancel(coefficients[index] - expected) == 0 for index in range(r + 1))
    assert all(coefficients[index] == 0 for index in range(r + 1, coordinate_count + 1))

    # Row-zero subset family B: r+3 coordinate zeros, source 0.
    rows = [e0] * (r + 3) + [e1] * (r - 1) + [p]
    coefficients = response_coefficients(rows, 0)
    expected = (
        sp.Rational((r + 2) * (r + 1) * factorial(r), 2**r)
        * (p1 + p2)
    )
    assert all(sp.cancel(coefficients[index] - expected) == 0 for index in range(r + 3))
    assert all(coefficients[index] == 0 for index in range(r + 3, coordinate_count + 1))

    # The row-one families are the colour-swapped versions.
    rows = [e1] * (r + 1) + [e0] * (r + 1) + [p]
    coefficients = response_coefficients(rows, 0)
    expected = scalar * ((r + 2) * p0 + r * p2)
    assert all(sp.cancel(coefficients[index] - expected) == 0 for index in range(r + 1))
    assert all(coefficients[index] == 0 for index in range(r + 1, coordinate_count + 1))

    rows = [e1] * (r + 3) + [e0] * (r - 1) + [p]
    coefficients = response_coefficients(rows, 1)
    expected = (
        sp.Rational((r + 2) * (r + 1) * factorial(r), 2**r)
        * (p0 + p2)
    )
    assert all(sp.cancel(coefficients[index] - expected) == 0 for index in range(r + 3))
    assert all(coefficients[index] == 0 for index in range(r + 3, coordinate_count + 1))

    # Once coordinate binary rows vanish, this kills the entire extra star.
    rows = [e0] * (r + 2) + [e1] * r + [p]
    coefficients = response_coefficients(rows, 0)
    extra_coefficient = sp.Rational(
        (r + 2) * (r + 1) * factorial(r), 2**r
    )
    assert coefficients[-1] == extra_coefficient

    # A zero output row at either type-10 centre gives a singleton.
    rows = [sp.zeros(1, 3)] + [e0] * (r + 2) + [e1] * (r - 1) + [p.subs(p0, 0)]
    coefficients = response_coefficients(rows, 0)
    expected = extra_coefficient * (p1 + p2)
    assert sp.cancel(coefficients[0] - expected) == 0
    assert all(entry == 0 for entry in coefficients[1:])

    rows = [sp.zeros(1, 3)] + [e0] * (r + 1) + [e1] * r + [p.subs(p0, 0)]
    coefficients = response_coefficients(rows, 0)
    expected = sp.Rational(r * (r + 1) * factorial(r), 2**r) * p2
    assert sp.cancel(coefficients[0] - expected) == 0
    assert all(entry == 0 for entry in coefficients[1:])

    # On a noncoordinate plane, source 2 gives every live pair sum.
    rows = [e2, e2] + [e0] * r + [e1] * r + [p]
    coefficients = response_coefficients(rows, 2)
    pair_coefficient = sp.Rational(factorial(r), 2 ** (r - 1)) * p2
    assert sp.cancel(coefficients[0] - pair_coefficient) == 0
    assert sp.cancel(coefficients[1] - pair_coefficient) == 0

    # On the coordinate plane the one-ternary-letter row is a singleton
    # after all binary rows have vanished.
    rows = [e2] + [e0] * (r + 2) + [e1] * r
    coefficients = response_coefficients(rows, 0)
    assert coefficients[0] == extra_coefficient

    assert incidence_rank(coordinate_count, r + 1) == coordinate_count
    assert incidence_rank(coordinate_count, r + 3) == coordinate_count


def main():
    for r in range(2, 5):
        audit_r(r)

    # The two coefficient functionals used in each binary row are distinct.
    assert sp.Matrix([[r_symbol + 2, r_symbol], [1, 1]]).det() == 2

    print("Live three-zero one-extra-plane common-beta all orders: PASS")
    print("exact response counts checked for r=2,3,4")
    print("fixed-subset ranks and the noncoordinate pair-sum step verified")


if __name__ == "__main__":
    main()
