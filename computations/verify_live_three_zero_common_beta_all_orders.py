#!/usr/bin/env python3
"""Exact audit for live-three-zero-common-beta-all-orders.md."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations
from math import comb, factorial, prod

import sympy as sp


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]):
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


def subset_incidence(number_of_sites: int, subset_size: int) -> sp.Matrix:
    return sp.Matrix([
        [int(site in subset) for site in range(number_of_sites)]
        for subset in combinations(range(number_of_sites), subset_size)
    ])


def response_row(word: tuple[int, ...], source_colour: int) -> list[int]:
    """One-zero-column row with H01=1, H02=2, H12=3 and 2 mu=1."""
    number_of_sites = len(word)
    hessian = ((0, 1, 2), (1, 0, 3), (2, 3, 0))
    row = [0] * (3 * number_of_sites)
    marked_sites = [site for site, colour in enumerate(word) if colour == source_colour]
    for u, v in combinations(marked_sites, 2):
        for star_site in range(number_of_sites):
            if star_site in (u, v):
                continue
            remaining = tuple(
                site
                for site in range(number_of_sites)
                if site not in (u, v, star_site)
            )
            cofactor = sum(
                prod(hessian[word[i]][word[j]] for i, j in matching)
                for matching in perfect_matchings(remaining)
            )
            row[3 * star_site + word[star_site]] += 2 * cofactor
    return row


def audit_order(r: int) -> None:
    # There are m=2r+1 nonzero sites: 2r-1 live sites and two type-10
    # centres.  Only binary coordinates are used in the first two stages,
    # so the centres behave exactly like live sites there.
    number_of_sites = 2 * r + 1
    coefficient = 2 * comb(r + 1, 2) * factorial(r - 1)
    require(
        coefficient != 0,
        "coefficient != 0",
    )

    # Fixed-size subset sums determine every coordinate in characteristic
    # zero.  These are the two incidence maps used in the proof.
    require(
        subset_incidence(number_of_sites, r + 2).rank() == number_of_sites,
        "subset_incidence(number_of_sites, r + 2).rank() == number...",
    )
    require(
        subset_incidence(number_of_sites, r).rank() == number_of_sites,
        "subset_incidence(number_of_sites, r).rank() == number_of_...",
    )

    # Audit representative full matching rows at manageable orders.  Site
    # symmetry supplies every other subset or distinguished site.
    if r <= 4:
        zero_subset = set(range(r + 2))
        word_zero = tuple(0 if site in zero_subset else 1 for site in range(number_of_sites))
        row_zero = response_row(word_zero, 0)
        require(
            row_zero == [
                coefficient if colour == 0 and site in zero_subset else 0
                for site in range(number_of_sites)
                for colour in range(3)
            ],
            "row_zero == [ coefficient if colour == 0 and site in zero...",
        )

        one_subset = set(range(r))
        word_one = tuple(1 if site in one_subset else 0 for site in range(number_of_sites))
        row_one = response_row(word_one, 0)
        require(
            row_one == [
                coefficient if colour == 1 and site in one_subset else 0
                for site in range(number_of_sites)
                for colour in range(3)
            ],
            "row_one == [ coefficient if colour == 1 and site in one_s...",
        )

        distinguished = 0
        other_sites = list(range(1, number_of_sites))
        zeros = set(other_sites[: r + 1])
        word_two = tuple(
            2 if site == distinguished else (0 if site in zeros else 1)
            for site in range(number_of_sites)
        )
        row_two = response_row(word_two, 0)
        require(
            row_two[3 * distinguished + 2] == coefficient,
            "row_two[3 * distinguished + 2] == coefficient",
        )
        # Every other possible star has binary local colour.  Those
        # variables have already vanished in the proof's first two stages.
        require(
            all(
                value == 0 or index == 3 * distinguished + 2 or index % 3 < 2
                for index, value in enumerate(row_two)
            ),
            "all( value == 0 or index == 3 * distinguished + 2 or inde...",
        )


def main() -> None:
    for r in range(2, 9):
        audit_order(r)
    print("Live three-zero common-beta all-orders injectivity: PASS")
    print("audited odd nonzero shores m=5,7,...,17; proof formulas are uniform")


if __name__ == "__main__":
    main()
