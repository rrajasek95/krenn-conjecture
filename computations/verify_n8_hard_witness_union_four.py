#!/usr/bin/env python3
"""Exact finite audit for the four-site hard-witness obstruction."""

from itertools import combinations, permutations, product

import sympy as sp


VERTICES = range(4)
COLORS = range(3)
SITE_PERMUTATIONS = tuple(permutations(VERTICES))
COLOR_PERMUTATIONS = tuple(permutations(COLORS))


def canonical(sets):
    images = []
    for site_permutation in SITE_PERMUTATIONS:
        moved = [
            frozenset(site_permutation[u] for u in witness_set)
            for witness_set in sets
        ]
        for color_permutation in COLOR_PERMUTATIONS:
            images.append(
                tuple(
                    sorted(
                        tuple(sorted(moved[color_permutation[color]]))
                        for color in COLORS
                    )
                )
            )
    return min(images)


def hard_assignments(witness_sets):
    site_colors = [
        {color for color, witness_set in enumerate(witness_sets) if u in witness_set}
        for u in VERTICES
    ]
    triple_sites = [u for u in VERTICES if len(site_colors[u]) == 3]
    assignments = set()
    for choices in product((-1, 0, 1, 2), repeat=len(triple_sites)):
        hard = [set() for _ in COLORS]
        for u, colors in enumerate(site_colors):
            if len(colors) <= 2:
                for color in colors:
                    hard[color].add(u)
        for u, color in zip(triple_sites, choices):
            if color >= 0:
                hard[color].add(u)
        if all(len(hard[color]) >= 2 for color in COLORS):
            assignments.add(tuple(tuple(sorted(hard[color])) for color in COLORS))
    return tuple(sorted(assignments)), site_colors


def determinant_colors(hard, site_colors):
    answers = []
    for color, hard_set_tuple in enumerate(hard):
        hard_set = set(hard_set_tuple)
        if len(hard_set) != 2:
            continue
        if not all(len(site_colors[u]) == 2 for u in hard_set):
            continue
        if not all(
            any(u not in hard_set for u in hard[other])
            for other in COLORS
            if other != color
        ):
            continue
        answers.append(color)
    return tuple(answers)


def main():
    candidate_sets = tuple(
        frozenset(choice)
        for size in range(2, 5)
        for choice in combinations(VERTICES, size)
    )
    orbits = {
        canonical(witness_sets)
        for witness_sets in product(candidate_sets, repeat=3)
        if set().union(*witness_sets) == set(VERTICES)
    }
    assert len(orbits) == 23

    survivors = {}
    determinant_rows = set()
    for witness_sets in sorted(orbits):
        assignments, site_colors = hard_assignments(witness_sets)
        if not assignments:
            continue
        survivors[witness_sets] = assignments
        outcomes = [
            determinant_colors(hard, site_colors) for hard in assignments
        ]
        if all(outcomes):
            determinant_rows.add(witness_sets)

    expected_survivors = {
        ((0, 1), (0, 1), (2, 3)),
        ((0, 1), (0, 1, 2), (0, 2, 3)),
        ((0, 1), (0, 1, 2), (2, 3)),
        ((0, 1), (0, 1, 2, 3), (0, 1, 2, 3)),
        ((0, 1), (0, 1, 2, 3), (0, 2, 3)),
        ((0, 1), (0, 1, 2, 3), (2, 3)),
        ((0, 1), (0, 2), (1, 2, 3)),
        ((0, 1), (0, 2), (1, 3)),
        ((0, 1), (0, 2, 3), (0, 2, 3)),
        ((0, 1), (0, 2, 3), (1, 2, 3)),
        ((0, 1, 2), (0, 1, 2, 3), (0, 1, 3)),
        ((0, 1, 2), (0, 1, 3), (0, 2, 3)),
    }
    assert set(survivors) == expected_survivors

    exceptional_rows = {
        ((0, 1), (0, 1), (2, 3)),
        ((0, 1), (0, 1, 2, 3), (0, 1, 2, 3)),
        ((0, 1), (0, 2, 3), (0, 2, 3)),
    }
    assert determinant_rows == expected_survivors - exceptional_rows

    # det(x_u y_v^T + y_u x_v^T) on a selected 2 x 2 rectangle.
    xr, xa, yr, ya, XR, Xb, YR, Yb = sp.symbols(
        "xr xa yr ya XR Xb YR Yb"
    )
    correction = sp.Matrix(
        [
            [xr * YR + yr * XR, xr * Yb + yr * Xb],
            [xa * YR + ya * XR, xa * Yb + ya * Xb],
        ]
    )
    expected = (xr * ya - xa * yr) * (YR * Xb - Yb * XR)
    assert sp.expand(correction.det() - expected) == 0

    # The monomials in the two exceptional variable-annihilator rows are
    # distinct in the relevant polynomial rings.
    zu1, zu2, zv1, zv2 = sp.symbols("zu1 zu2 zv1 zv2")
    assert sp.Poly(zu1 * zv1, zu1, zu2, zv1, zv2).monoms() != sp.Poly(
        zu2 * zv2, zu1, zu2, zv1, zv2
    ).monoms()
    assert sp.Poly(zu1, zu1, zu2).monoms() != sp.Poly(
        zu2, zu1, zu2
    ).monoms()

    print("classified four-site witness-union orbits", len(orbits))
    print("retained by exact hard-capacity constraints", len(survivors))
    print("excluded by the two-hole determinant", len(determinant_rows))
    print("isolated exceptional rows", tuple(sorted(exceptional_rows)))


if __name__ == "__main__":
    main()
