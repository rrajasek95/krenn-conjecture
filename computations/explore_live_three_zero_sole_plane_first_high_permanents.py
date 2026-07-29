#!/usr/bin/env python3
"""Exact forced-pair permanent ideals for the (r,t)=(3,6) frontier."""

from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import combinations, permutations

import sympy as sp

from explore_live_three_zero_minimal_three_extra_ccb import singular_status


PROFILE_MULTIPLICITIES = {
    "222": (2, 2, 2),
    "2211": (2, 2, 1, 1),
    "21111": (2, 1, 1, 1, 1),
    "111111": (1, 1, 1, 1, 1, 1),
}


@lru_cache(maxsize=None)
def profile_data(profile):
    multiplicities = PROFILE_MULTIPLICITIES[profile]
    classes = sp.symbols(
        " ".join(f"x{index}" for index in range(len(multiplicities)))
    )
    if not isinstance(classes, tuple):
        classes = (classes,)
    live = tuple(
        value
        for value, multiplicity in zip(classes, multiplicities)
        for _ in range(multiplicity)
    )
    localizer = sp.S.One
    for value in classes:
        # Exceptional classes avoid the common value 1, and every live--
        # centre denominator avoids -1.
        localizer *= (value-1)*(value+1)
    for left, right in combinations(classes, 2):
        localizer *= (left-right)*(left+right)
    for value, multiplicity in zip(classes, multiplicities):
        if multiplicity >= 2:
            localizer *= value
    return classes, live, sp.expand(localizer)


def cauchy_permanent(rows, columns):
    size = len(rows)
    assert len(columns) == size
    return sum(
        (
            sp.prod(
                1/(rows[index]+columns[permutation[index]])
                for index in range(size)
            )
            for permutation in permutations(range(size))
        ),
        sp.S.Zero,
    )


def numerator(expression, variables):
    value = sp.cancel(expression).as_numer_denom()[0]
    return sp.Poly(
        value, *variables, domain=sp.QQ
    ).primitive()[1].as_expr()


@lru_cache(maxsize=None)
def one_common_pivots(profile):
    variables, live, _localizer = profile_data(profile)
    pivots = []
    indices = tuple(range(6))
    for marked in indices:
        remaining = tuple(index for index in indices if index != marked)
        for left in combinations(remaining, 3):
            right = tuple(index for index in remaining if index not in left)
            polynomial = numerator(
                cauchy_permanent(
                    tuple(live[index] for index in left),
                    (sp.S.One,)+tuple(live[index] for index in right),
                ),
                variables,
            )
            if polynomial not in pivots:
                pivots.append(polynomial)
    return tuple(pivots)


@lru_cache(maxsize=None)
def two_common_pivots(profile):
    variables, live, _localizer = profile_data(profile)
    pivots = []
    indices = tuple(range(6))
    for marked in combinations(indices, 2):
        remaining = tuple(index for index in indices if index not in marked)
        for left in combinations(remaining, 2):
            right = tuple(index for index in remaining if index not in left)
            # The complementary choice is the transpose of the same matrix.
            if left > right:
                continue
            polynomial = numerator(
                cauchy_permanent(
                    (sp.S.One,)+tuple(live[index] for index in left),
                    (sp.S.One,)+tuple(live[index] for index in right),
                ),
                variables,
            )
            if polynomial not in pivots:
                pivots.append(polynomial)
    return tuple(pivots)


@lru_cache(maxsize=None)
def two_same_common_pivots(profile):
    """Coordinate-plane singleton pivots.

    Two exceptional sites form the source-22 marked pair.  Of the four
    remaining exceptional sites, three lie opposite the two non-target
    common-beta centres and one lies with them.  Removing the target star
    leaves the displayed three-by-three Cauchy permanent, with two equal
    common-beta columns.
    """
    variables, live, _localizer = profile_data(profile)
    pivots = []
    indices = tuple(range(6))
    for marked in combinations(indices, 2):
        remaining = tuple(index for index in indices if index not in marked)
        for singleton in remaining:
            left = tuple(index for index in remaining if index != singleton)
            polynomial = numerator(
                cauchy_permanent(
                    tuple(live[index] for index in left),
                    (sp.S.One, sp.S.One, live[singleton]),
                ),
                variables,
            )
            if polynomial not in pivots:
                pivots.append(polynomial)
    return tuple(pivots)


def status(profile, family):
    variables, _live, localizer = profile_data(profile)
    pivots = {
        "P": one_common_pivots,
        "R": two_common_pivots,
        "S": two_same_common_pivots,
    }[family](profile)
    result = singular_status(pivots, variables, localizer=localizer)
    return pivots, result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=tuple(PROFILE_MULTIPLICITIES))
    parser.add_argument("--family", choices=("P", "R", "S"))
    args = parser.parse_args()
    profiles = (args.profile,) if args.profile else tuple(PROFILE_MULTIPLICITIES)
    families = (args.family,) if args.family else ("P", "R", "S")
    for profile in profiles:
        for family in families:
            pivots, result = status(profile, family)
            print(
                profile, family, "pivots", len(pivots),
                "status", result.replace("\n", " "),
                flush=True,
            )


if __name__ == "__main__":
    main()
