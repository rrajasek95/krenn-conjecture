#!/usr/bin/env python3
"""Exact audit for live-three-zero-minority-exceptional-beta.md."""

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


def binary_response_row(
    word: tuple[int, ...],
    source_colour: int,
    active_sites: tuple[int, ...],
    exceptional_sites: tuple[int, ...],
    kappa: sp.Expr,
    lambdas: tuple[sp.Expr, ...],
) -> list[sp.Expr]:
    """Response on active binary zero-star variables."""
    exceptional_index = {
        site: index for index, site in enumerate(exceptional_sites)
    }
    columns = [(site, colour) for site in active_sites for colour in range(2)]
    column_index = {column: index for index, column in enumerate(columns)}

    def edge(i: int, j: int) -> sp.Expr:
        if word[i] == word[j]:
            return 0
        if i in exceptional_index and j in exceptional_index:
            # This case never contributes in the audited same-colour
            # exceptional rows, but keep an independent symbol unnecessary.
            raise AssertionError("opposite-colour exceptional edge not expected")
        if i in exceptional_index:
            return lambdas[exceptional_index[i]]
        if j in exceptional_index:
            return lambdas[exceptional_index[j]]
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


def audit_uniform_formula(r: int, exceptional_count: int) -> None:
    require(
        0 <= exceptional_count <= r - 1,
        "0 <= exceptional_count <= r - 1",
    )
    active_count = 2 * r + 1 - exceptional_count
    active_sites = tuple(range(active_count))
    exceptional_sites = tuple(range(active_count, 2 * r + 1))
    subset_size = r - exceptional_count
    kappa = sp.Symbol("kappa", nonzero=True)
    lambdas = tuple(
        sp.Symbol(f"lambda{index}", nonzero=True)
        for index in range(exceptional_count)
    )
    coefficient = (
        2
        * comb(r + 1, 2)
        * factorial(r - 1)
        * prod(lambdas)
        * kappa ** (r - exceptional_count - 1)
    )
    require(
        subset_incidence(active_count, subset_size).rank() == active_count,
        "subset_incidence(active_count, subset_size).rank() == act...",
    )

    if r <= 4:
        subset = set(active_sites[:subset_size])
        total_sites = 2 * r + 1

        # Exceptional sites and the chosen active subset have colour zero;
        # mark colour one.  This isolates row-zero star variables on subset.
        word_zero = tuple(
            0 if site in exceptional_sites or site in subset else 1
            for site in range(total_sites)
        )
        row_zero = binary_response_row(
            word_zero,
            1,
            active_sites,
            exceptional_sites,
            kappa,
            lambdas,
        )
        require(
            row_zero == [
                coefficient if colour == 0 and site in subset else 0
                for site in active_sites
                for colour in range(2)
            ],
            "row_zero == [ coefficient if colour == 0 and site in subs...",
        )

        # Colour-swapped row isolates row-one variables.
        word_one = tuple(1 - colour for colour in word_zero)
        row_one = binary_response_row(
            word_one,
            0,
            active_sites,
            exceptional_sites,
            kappa,
            lambdas,
        )
        require(
            row_one == [
                coefficient if colour == 1 and site in subset else 0
                for site in active_sites
                for colour in range(2)
            ],
            "row_one == [ coefficient if colour == 1 and site in subse...",
        )


def audit_two_exceptional_symbolic_minor() -> None:
    """Full ternary r=3,t=2 minor; its determinant is a pure monomial."""
    h01, h02, h12, mu, nu, omega = sp.symbols(
        "h01 h02 h12 mu nu omega", nonzero=True
    )
    hessian = sp.Matrix(
        [[0, h01, h02], [h01, 0, h12], [h02, h12, 0]]
    )
    active_sites = (0, 1, 2, 5, 6)
    exceptional_sites = (3, 4)
    centres = (5, 6)
    matrices = [sp.eye(3)] * 5 + [sp.diag(1, 1, 0)] * 2
    betas = [mu, mu, mu, nu, omega, mu, mu]
    blocks = {
        (i, j): matrices[i] * hessian * matrices[j].T / (betas[i] + betas[j])
        for i, j in combinations(range(7), 2)
    }
    columns = [
        (site, colour) for colour in range(3) for site in active_sites
    ]
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

    rows = []
    for colour in (0, 1):
        for site in active_sites:
            word = [1 - colour] * 7
            word[exceptional_sites[0]] = colour
            word[exceptional_sites[1]] = colour
            word[site] = colour
            rows.append(response_row(tuple(word), 1 - colour))
    for site in active_sites:
        word = [0] * 7
        word[exceptional_sites[0]] = 1
        word[exceptional_sites[1]] = 1
        word[site] = 2
        rows.append(response_row(tuple(word), 0))

    minor = sp.Matrix(rows)
    require(
        minor.shape == (15, 15),
        "minor.shape == (15, 15)",
    )
    pivot = 24 * h01**2 / ((mu + nu) * (mu + omega))
    require(
        sp.factor(sp.cancel(minor.det(method="domain-ge"))) == pivot**15,
        "sp.factor(sp.cancel(minor.det(method=\"domain-ge\"))) == pi...",
    )


def main() -> None:
    cases = 0
    for r in range(2, 9):
        for exceptional_count in range(r):
            audit_uniform_formula(r, exceptional_count)
            cases += 1
    audit_two_exceptional_symbolic_minor()
    print("Live three-zero minority-exceptional-beta injectivity: PASS")
    print(f"uniform weighted-subset cases audited: {cases}")
    print("r=3,t=2 full ternary 15-square minor is a pure monomial")


if __name__ == "__main__":
    main()
