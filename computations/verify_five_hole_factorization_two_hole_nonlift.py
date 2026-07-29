#!/usr/bin/env python3
"""Exact two-hole obstruction for the rational five-hole factorization.

The point in ``verify_five_hole_factorization_counterexample.py`` solves

    Delta_5 = [X Y D Q]_{1^5}.

If it were obtained by contracting a six-site row of an n=8 solution at a
sixth site k, then contracting four of the five displayed sites by the
cross-product annihilators of the two uncontracted star families would
force five scalar four-site hafnians to vanish.  This script checks over Q
that all five are nonzero.  It does so for all three choices of which two
of X,Y,D are the uncontracted star families.
"""

from __future__ import annotations

from functools import reduce
from itertools import combinations

import verify_five_hole_factorization_counterexample as point


F = point.F
SITES = point.SITES
COLOURS = point.COLOURS
SPECIES_PAIRS = tuple(combinations(COLOURS, 2))


def dot_matrix(left, matrix, right):
    return sum(
        left[row] * matrix[row][column] * right[column]
        for row in COLOURS
        for column in COLOURS
    )


def edge_value(values, left, right):
    return values[tuple(sorted((left, right)))]


def hafnian_four(values, sites):
    a, b, c, d = sites
    return (
        edge_value(values, a, b) * edge_value(values, c, d)
        + edge_value(values, a, c) * edge_value(values, b, d)
        + edge_value(values, a, d) * edge_value(values, b, c)
    )


def product(values):
    return reduce(lambda left, right: left * right, values, F(1))


def main():
    local_bases = tuple(
        point.inverse(matrix) for matrix in point.TARGET_COMPONENTS
    )
    families = tuple(
        tuple(point.column(local_bases[site], species) for site in SITES)
        for species in COLOURS
    )
    quadratic = {
        edge: point.multiply(
            point.multiply(local_bases[edge[0]], matrix),
            point.transpose(local_bases[edge[1]]),
        )
        for edge, matrix in point.NORMALIZED_Q.items()
    }

    # Recheck that the data being obstructed really is the exact point.
    delta = {
        word: F(len(set(word)) == 1)
        for word in point.product(COLOURS, repeat=len(SITES))
    }
    assert point.factor_response(families, quadratic) == delta

    expected_masks = {
        (0, 1): (3, 3, 4, 4, 4),
        (0, 2): (5, 2, 5, 2, 2),
        (1, 2): (6, 1, 1, 6, 1),
    }
    expected_hafnians = {
        (0, 1): (F(-1, 64), F(-3, 64), F(3, 64), F(1, 16), F(1, 24)),
        (0, 2): (F(-1, 64), F(3, 64), F(-3, 64), F(1, 16), F(1, 24)),
        (1, 2): (F(-4, 81), F(4, 27), F(4, 27), F(-16, 81), F(32, 243)),
    }

    for species_pair in SPECIES_PAIRS:
        first, second = species_pair
        normals = tuple(
            point.cross(families[first][site], families[second][site])
            for site in SITES
        )
        assert all(any(normal) for normal in normals)

        masks = tuple(
            sum(1 << colour for colour in COLOURS if normal[colour] == 0)
            for normal in normals
        )
        assert masks == expected_masks[species_pair]

        scalar_edges = {
            edge: dot_matrix(
                normals[edge[0]], matrix, normals[edge[1]]
            )
            for edge, matrix in quadratic.items()
        }

        hafnians = []
        for open_site in SITES:
            contracted = tuple(site for site in SITES if site != open_site)

            # These are the three coefficients left on the two open sites
            # after the other four target legs are contracted by normals.
            target_weights = tuple(
                product(normals[site][colour] for site in contracted)
                for colour in COLOURS
            )
            assert target_weights == (F(0), F(0), F(0))

            cofactor = hafnian_four(scalar_edges, contracted)
            assert cofactor
            hafnians.append(cofactor)

        assert tuple(hafnians) == expected_hafnians[species_pair]

    print(
        "PASS exact two-hole nonlift: all 15 target contractions vanish "
        "but their complementary rational four-site hafnians are nonzero"
    )


if __name__ == "__main__":
    main()
