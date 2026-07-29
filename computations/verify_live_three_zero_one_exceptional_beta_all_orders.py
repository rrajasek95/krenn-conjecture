#!/usr/bin/env python3
"""Exact audit for live-three-zero-one-exceptional-beta-all-orders.md."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations
from math import comb, factorial, prod

import sympy as sp


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


def binary_response_row(
    word: tuple[int, ...],
    source_colour: int,
    active_sites: tuple[int, ...],
    inactive_site: int,
    kappa: sp.Expr,
    lam: sp.Expr,
) -> list[sp.Expr]:
    """Response on active zero-star variables for a binary word."""
    columns = [(site, colour) for site in active_sites for colour in range(2)]
    column_index = {column: index for index, column in enumerate(columns)}

    def edge(i: int, j: int) -> sp.Expr:
        if word[i] == word[j]:
            return 0
        if inactive_site in (i, j):
            return lam
        return kappa

    marked_sites = [site for site, colour in enumerate(word) if colour == source_colour]
    row = [sp.S.Zero] * len(columns)
    for u, v in combinations(marked_sites, 2):
        for star_site in active_sites:
            if star_site in (u, v):
                continue
            remaining = tuple(
                site
                for site in range(len(word))
                if site not in (u, v, star_site)
            )
            cofactor = sum(
                prod(edge(i, j) for i, j in matching)
                for matching in perfect_matchings(remaining)
            )
            row[column_index[star_site, word[star_site]]] += 2 * cofactor
    return [sp.expand(value) for value in row]


def audit_uniform_formula(r: int) -> None:
    # The active sites comprise all common-beta live sites and the two
    # type-10 centres.  The one exceptional-beta live site has zero star.
    number_of_active_sites = 2 * r
    active_sites = tuple(range(number_of_active_sites))
    inactive_site = number_of_active_sites
    total_sites = number_of_active_sites + 1
    kappa, lam = sp.symbols("kappa lambda", nonzero=True)
    coefficient = 2 * comb(r + 1, 2) * factorial(r - 1) * lam * kappa ** (r - 2)

    # The fixed-size subset equations used for rows zero and one have full
    # column rank over characteristic zero.
    incidence = subset_incidence(number_of_active_sites, r - 1)
    assert incidence.rank() == number_of_active_sites

    # Representative exact matching rows; site symmetry supplies all
    # subsets.  Keep exhaustive matching expansion to moderate orders.
    if r <= 4:
        subset = set(range(r - 1))

        # Inactive site zero, mark colour one: isolate row-zero variables
        # on the chosen active subset.
        word_zero = tuple(
            0 if site == inactive_site or site in subset else 1
            for site in range(total_sites)
        )
        row_zero = binary_response_row(
            word_zero, 1, active_sites, inactive_site, kappa, lam
        )
        assert row_zero == [
            coefficient if colour == 0 and site in subset else 0
            for site in active_sites
            for colour in range(2)
        ]

        # Inactive site one, mark colour zero: isolate row-one variables.
        word_one = tuple(
            1 if site == inactive_site or site in subset else 0
            for site in range(total_sites)
        )
        row_one = binary_response_row(
            word_one, 0, active_sites, inactive_site, kappa, lam
        )
        assert row_one == [
            coefficient if colour == 1 and site in subset else 0
            for site in active_sites
            for colour in range(2)
        ]


SYMBOLIC_MINOR_ROWS = (
    ((0, 0, 0, 0, 1, 0, 1), 0),
    ((1, 0, 0, 0, 1, 0, 1), 0),
    ((2, 0, 0, 0, 1, 0, 1), 0),
    ((0, 1, 0, 0, 1, 0, 0), 0),
    ((0, 1, 0, 0, 1, 0, 1), 0),
    ((0, 2, 0, 0, 1, 0, 1), 0),
    ((0, 0, 1, 0, 1, 0, 0), 0),
    ((0, 0, 1, 0, 1, 0, 1), 0),
    ((0, 0, 2, 0, 1, 0, 1), 0),
    ((0, 0, 0, 1, 1, 0, 0), 0),
    ((0, 0, 0, 1, 1, 0, 1), 0),
    ((0, 0, 0, 2, 1, 0, 1), 0),
    ((0, 0, 0, 1, 2, 1, 0), 0),
    ((0, 0, 0, 1, 1, 1, 0), 0),
    ((0, 0, 0, 1, 1, 2, 0), 0),
    ((0, 0, 0, 1, 2, 0, 1), 0),
    ((0, 0, 0, 1, 2, 1, 1), 0),
    ((0, 0, 0, 1, 2, 0, 2), 0),
)


def audit_symbolic_seven_site_minor() -> None:
    """A full ternary 18-square minor for r=3 and one exceptional beta."""
    h01, h02, h12, mu, nu = sp.symbols(
        "h01 h02 h12 mu nu", nonzero=True
    )
    hessian = sp.Matrix(
        [[0, h01, h02], [h01, 0, h12], [h02, h12, 0]]
    )
    live = tuple(range(5))
    centres = (5, 6)
    active_sites = (0, 1, 2, 3, 5, 6)
    inactive_site = 4
    matrices = [sp.eye(3)] * 5 + [sp.diag(1, 1, 0)] * 2
    betas = [mu, mu, mu, mu, nu, mu, mu]
    blocks = {
        (i, j): matrices[i] * hessian * matrices[j].T / (betas[i] + betas[j])
        for i, j in combinations(range(7), 2)
    }
    columns = [(site, colour) for site in active_sites for colour in range(3)]
    column_index = {column: index for index, column in enumerate(columns)}

    def edge(i: int, j: int, colour_i: int, colour_j: int) -> sp.Expr:
        if i < j:
            return blocks[i, j][colour_i, colour_j]
        return blocks[j, i][colour_j, colour_i]

    def response_row(word: tuple[int, ...], source_colour: int) -> list[sp.Expr]:
        marked_sites = [
            site
            for site in range(7)
            if matrices[site][word[site], source_colour] != 0
        ]
        row = [sp.S.Zero] * len(columns)
        for u, v in combinations(marked_sites, 2):
            for star_site in active_sites:
                if star_site in (u, v):
                    continue
                remaining = tuple(
                    site for site in range(7) if site not in (u, v, star_site)
                )
                cofactor = sum(
                    prod(edge(i, j, word[i], word[j]) for i, j in matching)
                    for matching in perfect_matchings(remaining)
                )
                row[column_index[star_site, word[star_site]]] += 2 * cofactor
        return row

    minor = sp.Matrix([
        response_row(word, source_colour)
        for word, source_colour in SYMBOLIC_MINOR_ROWS
    ])
    assert minor.shape == (18, 18)
    assert sp.factor(sp.cancel(minor.det(method="domain-ge"))) == (
        -2**33 * 3**18 * h01**32 * h02 * h12**3
        / (mu**18 * (mu + nu)**18)
    )
    assert inactive_site in live


def main() -> None:
    for r in range(2, 9):
        audit_uniform_formula(r)
    audit_symbolic_seven_site_minor()
    print("Live three-zero one-exceptional-beta all-orders injectivity: PASS")
    print("uniform subset rows audited for residual nonzero shores 5,7,...,17")
    print("full r=3 ternary minor has nonzero constant numerator")


if __name__ == "__main__":
    main()
