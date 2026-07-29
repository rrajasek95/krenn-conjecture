#!/usr/bin/env python3
"""Exact audit for the minority-exceptional one-extra-plane response."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations
from math import comb, factorial

import sympy as sp


p0, p1, p2 = sp.symbols("p0 p1 p2")
p = sp.Matrix([[p0, p1, p2]])
e0 = sp.Matrix([[1, 0, 0]])
e1 = sp.Matrix([[0, 1, 0]])
e2 = sp.Matrix([[0, 0, 1]])
zero = sp.zeros(1, 3)
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


def response_coefficients(rows, betas, source):
    sites = tuple(range(len(rows)))

    def edge(left, right):
        return (
            rows[left] * H * rows[right].T
        )[0] / (betas[left] + betas[right])

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
    return sp.Matrix(
        [
            [int(point in subset) for point in range(point_count)]
            for subset in combinations(range(point_count), subset_size)
        ]
    ).rank()


def audit_case(r, exceptional_count):
    t = exceptional_count
    assert 1 <= t <= r - 2
    active_count = 2 * r + 2 - t
    nus = sp.symbols(f"nu0:{t}")
    exceptional_betas = list(nus)
    exceptional_factor = sp.prod(1 / (1 + value) for value in nus)
    common_power = sp.Rational(1, 2) ** (r - t)
    common_factor = factorial(r) * exceptional_factor * common_power
    k_factor = (r + 1) * common_factor
    l_factor = (r + 2) * (r + 1) * common_factor
    m_factor = r * (r + 1) * common_factor

    # Family A for active row zero.
    subset_size = r + 1 - t
    rows = (
        [e0] * subset_size
        + [e1] * (active_count - subset_size)
        + [e0] * t
        + [p]
    )
    betas = [1] * active_count + exceptional_betas + [1]
    coefficients = response_coefficients(rows, betas, 1)
    expected = k_factor * ((r + 2) * p1 + r * p2)
    assert all(
        sp.cancel(coefficients[index] - expected) == 0
        for index in range(subset_size)
    )
    assert all(
        coefficients[index] == 0
        for index in range(subset_size, active_count)
    )
    assert coefficients[-1] == 0

    # Family B for active row zero; exceptional sites sit on the other side.
    subset_size_b = r + 3
    rows = (
        [e0] * subset_size_b
        + [e1] * (active_count - subset_size_b)
        + [e1] * t
        + [p]
    )
    coefficients = response_coefficients(rows, betas, 0)
    expected = l_factor * (p1 + p2)
    assert all(
        sp.cancel(coefficients[index] - expected) == 0
        for index in range(subset_size_b)
    )
    assert all(
        coefficients[index] == 0
        for index in range(subset_size_b, active_count)
    )
    assert coefficients[-1] == 0

    # Colour-swapped families for active row one.
    rows = (
        [e1] * subset_size
        + [e0] * (active_count - subset_size)
        + [e1] * t
        + [p]
    )
    coefficients = response_coefficients(rows, betas, 0)
    expected = k_factor * ((r + 2) * p0 + r * p2)
    assert all(
        sp.cancel(coefficients[index] - expected) == 0
        for index in range(subset_size)
    )
    assert coefficients[-1] == 0

    rows = (
        [e1] * subset_size_b
        + [e0] * (active_count - subset_size_b)
        + [e0] * t
        + [p]
    )
    coefficients = response_coefficients(rows, betas, 1)
    expected = l_factor * (p0 + p2)
    assert all(
        sp.cancel(coefficients[index] - expected) == 0
        for index in range(subset_size_b)
    )
    assert coefficients[-1] == 0

    # The extra star after the active binary rows have vanished.
    rows = (
        [e0] * (r - t)
        + [e1] * (r + 2)
        + [e0] * t
        + [p]
    )
    coefficients = response_coefficients(rows, betas, 1)
    assert sp.cancel(coefficients[-1] - l_factor) == 0

    # A zero third row at a type-10 centre is a singleton.
    other_active = active_count - 1
    rows = (
        [zero]
        + [e0] * (r + 2)
        + [e1] * (other_active - r - 2)
        + [e1] * t
        + [p.subs(p0, 0)]
    )
    betas_with_centre = [1] * active_count + exceptional_betas + [1]
    coefficients = response_coefficients(rows, betas_with_centre, 0)
    assert sp.cancel(coefficients[0] - l_factor * (p1 + p2)) == 0
    assert all(entry == 0 for entry in coefficients[1:])

    rows = (
        [zero]
        + [e0] * (r + 1)
        + [e1] * (other_active - r - 1)
        + [e1] * t
        + [p.subs(p0, 0)]
    )
    coefficients = response_coefficients(rows, betas_with_centre, 0)
    assert sp.cancel(coefficients[0] - m_factor * p2) == 0
    assert all(entry == 0 for entry in coefficients[1:])

    # Two common live third rows give a pair sum on a noncoordinate plane.
    remaining_active = active_count - 2
    rows = (
        [e2, e2]
        + [e0] * (r - t)
        + [e1] * r
        + [e0] * t
        + [p]
    )
    assert len(rows) == active_count + t + 1
    coefficients = response_coefficients(rows, betas, 2)
    pair_factor = 2 * common_factor * p2
    assert sp.cancel(coefficients[0] - pair_factor) == 0
    assert sp.cancel(coefficients[1] - pair_factor) == 0

    # Coordinate-plane final row: e is one more binary coordinate site.
    rows = (
        [e2]
        + [e0] * (r - t)
        + [e1] * (r + 2)
        + [e0] * t
    )
    betas_coordinate = [1] * (active_count + 1) + exceptional_betas
    coefficients = response_coefficients(rows, betas_coordinate, 1)
    assert sp.cancel(coefficients[0] - l_factor) == 0

    assert incidence_rank(active_count, subset_size) == active_count
    assert incidence_rank(active_count, subset_size_b) == active_count


def main():
    for case in ((3, 1), (4, 1), (4, 2)):
        audit_case(*case)
    print("Live three-zero extra-plane minority-exceptional: PASS")
    print("exact response counts: (r,t)=(3,1),(4,1),(4,2)")
    print("subset transforms, centre singletons, and pair sums verified")


if __name__ == "__main__":
    main()
