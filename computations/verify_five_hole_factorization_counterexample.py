#!/usr/bin/env python3
"""Verify an exact rational Delta_5 = [X Y D Q] factorization.

The example lies on the 011166 zero-cross mask boundary.  It is a local
five-hole response, not an eight-site Krenn realization: the full six-site
and two-hole compatibility used by the 011166 square obstruction is not
imposed here.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations, permutations, product


SITES = tuple(range(5))
COLOURS = tuple(range(3))
PAIRS = tuple(combinations(SITES, 2))


def matrix(rows):
    return tuple(tuple(F(value) for value in row) for row in rows)


def determinant(a):
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def inverse(a):
    assert determinant(a)
    augmented = [
        list(a[row]) + [F(row == column) for column in COLOURS]
        for row in COLOURS
    ]
    for column in COLOURS:
        pivot = next(row for row in range(column, 3)
                     if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in COLOURS:
            if row == column:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                left - scale * right
                for left, right in zip(
                    augmented[row], augmented[column], strict=True
                )
            ]
    answer = tuple(tuple(augmented[row][3 + column] for column in COLOURS)
                   for row in COLOURS)
    assert multiply(a, answer) == identity()
    return answer


def identity():
    return tuple(tuple(F(i == j) for j in COLOURS) for i in COLOURS)


def transpose(a):
    return tuple(tuple(a[j][i] for j in COLOURS) for i in COLOURS)


def multiply(a, b):
    return tuple(tuple(
        sum(a[i][k] * b[k][j] for k in COLOURS)
        for j in COLOURS
    ) for i in COLOURS)


def column(a, j):
    return tuple(a[i][j] for i in COLOURS)


def cross(left, right):
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


# Columns are the three rank-one summands in normalized species coordinates.
TARGET_COMPONENTS = (
    matrix(((1, 0, 0), (0, 1, 0), (0, 0, 1))),
    matrix(((0, 1, 4), (1, 0, 3), (0, 0, -3))),
    matrix(((0, 4, 1), (0, -3, 0), (1, 3, 0))),
    matrix(((-4, 0, 0), (3, 0, 1), (3, 1, 0))),
    matrix(((0, F(4, 3), F(4, 3)), (1, 0, 1), (1, 1, 0))),
)


NORMALIZED_Q = {
    (0, 1): matrix(((-F(8, 9), -1, 1), (-1, -F(1, 2), F(3, 4)),
                    (-1, -F(3, 4), 1))),
    (0, 2): matrix(((-F(8, 9), 1, -1), (-1, 1, -F(3, 4)),
                    (-1, F(3, 4), -F(1, 2)))),
    (0, 3): matrix(((F(16, 9), -1, -1), (1, -F(1, 2), -F(3, 4)),
                    (1, -F(3, 4), -F(1, 2)))),
    (0, 4): matrix(((-F(8, 9), -1, -1), (-1, -F(1, 2), -F(3, 4)),
                    (-1, -F(3, 4), -F(1, 2)))),
    (1, 2): matrix(((F(16, 9), -1, 1), (1, -F(1, 2), F(3, 4)),
                    (-1, F(3, 4), -F(1, 2)))),
    (1, 3): matrix(((-F(8, 9), 1, 1), (-1, 1, F(3, 4)),
                    (1, -F(3, 4), -F(1, 2)))),
    (1, 4): matrix(((F(16, 9), 1, 1), (1, 1, F(3, 4)),
                    (-1, -F(3, 4), -F(1, 2)))),
    (2, 3): matrix(((-F(8, 9), 1, 1), (1, -F(1, 2), -F(3, 4)),
                    (-1, F(3, 4), 1))),
    (2, 4): matrix(((F(16, 9), 1, 1), (-1, -F(1, 2), -F(3, 4)),
                    (1, F(3, 4), 1))),
    (3, 4): matrix(((-F(8, 9), -1, -1), (1, 1, F(3, 4)),
                    (1, F(3, 4), 1))),
}


def factor_response(families, quadratic):
    """Enumerate [X Y D Q] in named site order."""

    answer = {}
    for word in product(COLOURS, repeat=len(SITES)):
        value = F(0)
        for a, b in PAIRS:
            complement = tuple(site for site in SITES if site not in (a, b))
            for species_assignment in permutations(COLOURS):
                term = quadratic[a, b][word[a]][word[b]]
                for site, species in zip(
                    complement, species_assignment, strict=True
                ):
                    term *= families[species][site][word[site]]
                value += term
        answer[word] = value
    return answer


def rank_three_tensor(local_components):
    return {
        word: sum(
            product_value(local_components[site][word[site]][colour]
                          for site in SITES)
            for colour in COLOURS
        )
        for word in product(COLOURS, repeat=len(SITES))
    }


def product_value(values):
    answer = F(1)
    for value in values:
        answer *= value
    return answer


def main():
    assert tuple(determinant(local) for local in TARGET_COMPONENTS) == (
        F(1), F(3), F(3), F(4), F(8, 3)
    )

    standard_families = tuple(
        tuple(tuple(F(colour == species) for colour in COLOURS)
              for _site in SITES)
        for species in COLOURS
    )
    normalized_response = factor_response(
        standard_families, NORMALIZED_Q
    )
    normalized_target = rank_three_tensor(TARGET_COMPONENTS)
    assert normalized_response == normalized_target

    # Undo the five local basis matrices.  Their columns are now the actual
    # X,Y,D vectors, and every Q block transforms covariantly at its ends.
    local_bases = tuple(inverse(local) for local in TARGET_COMPONENTS)
    families = tuple(
        tuple(column(local_bases[site], species) for site in SITES)
        for species in COLOURS
    )
    transformed_q = {
        (a, b): multiply(
            multiply(local_bases[a], NORMALIZED_Q[a, b]),
            transpose(local_bases[b]),
        )
        for a, b in PAIRS
    }
    response = factor_response(families, transformed_q)
    delta = {
        word: F(len(set(word)) == 1)
        for word in product(COLOURS, repeat=len(SITES))
    }
    assert response == delta

    # The X,Y zero-cross masks are 33,444 in the displayed colour order;
    # sending old colour 2 to new colour 0 converts this to 11166.
    masks = tuple(
        sum(1 << colour for colour, value in enumerate(
            cross(families[0][site], families[1][site])
        ) if not value)
        for site in SITES
    )
    assert masks == (3, 3, 4, 4, 4)
    colour_image = {0: 1, 1: 2, 2: 0}
    relabelled = tuple(sorted(
        sum(1 << colour_image[colour] for colour in COLOURS
            if mask >> colour & 1)
        for mask in masks
    ))
    assert relabelled == (1, 1, 1, 6, 6)

    # D has explicit coordinate anchors of all three colours, as demanded
    # by the one-slice covering lemma, but the other local bases are mixed.
    d_vectors = families[2]
    assert d_vectors[0] == (0, 0, 1)
    assert d_vectors[2] == (1, 0, 0)
    assert d_vectors[3] == (0, 1, 0)

    print(
        "PASS exact five-hole factorization: 243 coefficients of "
        "Delta_5 verified over Q; local determinants=(1,3,3,4,8/3); "
        "zero-cross masks relabel to 11166"
    )


if __name__ == "__main__":
    main()
