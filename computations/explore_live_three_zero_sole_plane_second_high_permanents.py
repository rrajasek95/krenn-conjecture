#!/usr/bin/env python3
"""P/R/S permanent reconnaissance for the next sole-plane point (4,7)."""

from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import combinations, permutations

import sympy as sp

from explore_live_three_zero_minimal_three_extra_ccb import singular_status


PROFILE_MULTIPLICITIES = {
    "331": (3, 3, 1),
    "322": (3, 2, 2),
    "3211": (3, 2, 1, 1),
    "31111": (3, 1, 1, 1, 1),
    "2221": (2, 2, 2, 1),
    "22111": (2, 2, 1, 1, 1),
    "211111": (2, 1, 1, 1, 1, 1),
    "1111111": (1, 1, 1, 1, 1, 1, 1),
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
        localizer *= (value - 1) * (value + 1)
    for left, right in combinations(classes, 2):
        localizer *= (left - right) * (left + right)
    for value, multiplicity in zip(classes, multiplicities):
        if multiplicity >= 2:
            localizer *= value
    return classes, live, sp.expand(localizer)


def cleared_cauchy_permanent(rows, columns, variables):
    """Clear by the product of all entries' denominators.

    This may retain structural factors compared with a reduced numerator;
    those factors are units after localization, so it defines exactly the
    same vanishing locus and avoids an expensive multivariate gcd.
    """
    size = len(rows)
    assert len(columns) == size
    denominators = tuple(
        tuple(rows[i] + columns[j] for j in range(size))
        for i in range(size)
    )
    polynomial = sum(
        (
            sp.prod(
                denominators[i][j]
                for i in range(size)
                for j in range(size)
                if j != permutation[i]
            )
            for permutation in permutations(range(size))
        ),
        sp.S.Zero,
    )
    return sp.Poly(
        sp.expand(polynomial), *variables, domain=sp.QQ
    ).primitive()[1]


def unique_polynomials(expressions):
    answer = {}
    for polynomial in expressions:
        answer.setdefault(tuple(polynomial.terms()), polynomial.as_expr())
    return tuple(answer.values())


@lru_cache(maxsize=None)
def P_pivots(profile):
    variables, live, _localizer = profile_data(profile)
    indices = tuple(range(7))
    return unique_polynomials(
        cleared_cauchy_permanent(
            tuple(live[index] for index in left),
            (sp.S.One, sp.S.One)
            + tuple(
                live[index]
                for index in indices
                if index != marked and index not in left
            ),
            variables,
        )
        for marked in indices
        for left in combinations(
            tuple(index for index in indices if index != marked), 4
        )
    )


@lru_cache(maxsize=None)
def R_pivots(profile):
    variables, live, _localizer = profile_data(profile)
    indices = tuple(range(7))
    return unique_polynomials(
        cleared_cauchy_permanent(
            (sp.S.One,) + tuple(live[index] for index in left),
            (sp.S.One, sp.S.One)
            + tuple(
                live[index]
                for index in indices
                if index not in marked and index not in left
            ),
            variables,
        )
        for marked in combinations(indices, 2)
        for left in combinations(
            tuple(index for index in indices if index not in marked), 3
        )
    )


@lru_cache(maxsize=None)
def S_pivots(profile):
    variables, live, _localizer = profile_data(profile)
    indices = tuple(range(7))
    return unique_polynomials(
        cleared_cauchy_permanent(
            tuple(
                live[index]
                for index in indices
                if index not in marked and index != singleton
            ),
            (sp.S.One, sp.S.One, sp.S.One, live[singleton]),
            variables,
        )
        for marked in combinations(indices, 2)
        for singleton in indices
        if singleton not in marked
    )


FAMILIES = {"P": P_pivots, "R": R_pivots, "S": S_pivots}


def status(profile, family):
    variables, _live, localizer = profile_data(profile)
    pivots = FAMILIES[family](profile)
    return pivots, singular_status(pivots, variables, localizer=localizer)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=tuple(PROFILE_MULTIPLICITIES))
    parser.add_argument("--family", choices=tuple(FAMILIES))
    parser.add_argument(
        "--count-only", action="store_true",
        help="construct and deduplicate the numerators without Singular",
    )
    args = parser.parse_args()
    profiles = (args.profile,) if args.profile else tuple(PROFILE_MULTIPLICITIES)
    families = (args.family,) if args.family else tuple(FAMILIES)
    for profile in profiles:
        for family in families:
            pivots = FAMILIES[family](profile)
            if args.count_only:
                print(profile, family, "pivots", len(pivots), flush=True)
                continue
            _pivots, result = status(profile, family)
            print(
                profile, family, "pivots", len(pivots),
                "status", result.replace("\n", " "), flush=True,
            )


if __name__ == "__main__":
    main()
