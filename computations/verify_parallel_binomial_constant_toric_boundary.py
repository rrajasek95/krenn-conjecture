#!/usr/bin/env python3
"""Verify universal constant cancellation on the 48-cell binomial support.

The earlier verifier exhibits one +/-1 weighting for which all fibres
cancel.  This checker proves the stronger statement needed at the corrected
boundary: *every* nonzero complex weighting that cancels all mixed
binomials also cancels each of the three complete constant fibres.

For each color the constant fibre has two terms.  Its exponent difference
is an odd signed sum of three mixed-fibre exponent differences.  Therefore
the three equations x**d=-1 force the constant term ratio to be -1.
"""

from __future__ import annotations

from itertools import product

from verify_parallel_binomial_incidence_countermodel import (
    COLORS,
    N,
    SUPPORT,
    fibre_terms,
    perfect_matchings,
)


CELLS = tuple(sorted(SUPPORT))
CELL_INDEX = {cell: index for index, cell in enumerate(CELLS)}


def supported_decorated_matchings(coloring):
    answer = []
    for matching in perfect_matchings():
        decorated = tuple(sorted(
            (u, v, coloring[u], coloring[v]) for u, v in matching
        ))
        if set(decorated) <= SUPPORT:
            answer.append(decorated)
    return tuple(answer)


def exponent_difference(left, right):
    answer = [0] * len(CELLS)
    for cell in left:
        answer[CELL_INDEX[cell]] += 1
    for cell in right:
        answer[CELL_INDEX[cell]] -= 1
    return tuple(answer)


# Each row lists (mixed coloring, integer coefficient).  The deterministic
# matching order above agrees with the orientation used in the identity.
CERTIFICATES = {
    0: (
        ((0, 0, 0, 0, 0, 2), +1),
        ((0, 0, 1, 0, 0, 0), +1),
        ((0, 0, 1, 0, 0, 2), -1),
    ),
    1: (
        ((0, 1, 0, 1, 0, 0), -1),
        ((0, 1, 1, 1, 0, 0), +1),
        ((1, 1, 0, 1, 1, 1), +1),
    ),
    2: (
        ((0, 0, 2, 0, 0, 2), -1),
        ((0, 2, 2, 0, 0, 2), +1),
        ((2, 0, 2, 2, 2, 2), +1),
    ),
}


def main():
    fibres = {
        coloring: supported_decorated_matchings(coloring)
        for coloring in product(COLORS, repeat=N)
    }
    assert all(
        len(terms) in (0, 2)
        for coloring, terms in fibres.items()
        if len(set(coloring)) > 1
    )

    for color in COLORS:
        pure = fibres[(color,) * N]
        assert len(pure) == 2
        pure_difference = exponent_difference(pure[0], pure[1])

        certificate = CERTIFICATES[color]
        assert all(len(fibres[coloring]) == 2
                   and len(set(coloring)) > 1
                   for coloring, _coefficient in certificate)
        mixed_differences = [
            exponent_difference(*fibres[coloring])
            for coloring, _coefficient in certificate
        ]
        coefficients = [coefficient for _coloring, coefficient in certificate]
        reconstructed = tuple(
            sum(coefficient * difference[column]
                for coefficient, difference in zip(
                    coefficients, mixed_differences
                ))
            for column in range(len(CELLS))
        )
        assert reconstructed == pure_difference
        assert sum(coefficients) % 2 == 1

        # Directly audit the logical consequence.  If every mixed ratio in
        # the certificate is -1, their displayed Laurent combination is
        # (-1)^(sum coefficients)=-1, hence the two pure monomials cancel.
        forced_pure_ratio = (-1) ** sum(coefficients)
        assert forced_pure_ratio == -1

    # Retain the independent numerical audit as a cross-check on orientations.
    assert all(
        sum(value for _decorated, value in fibre_terms((color,) * N)) == 0
        for color in COLORS
    )

    print(
        "verified universal toric boundary on the 48-cell support: for "
        "each color, three mixed binomials force its two constant terms "
        "to have ratio -1"
    )
    print(
        "consequence: no nonzero complex weighting on this support can "
        "cancel every mixed fibre while leaving even one constant sum nonzero"
    )


if __name__ == "__main__":
    main()
