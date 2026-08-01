#!/usr/bin/env python3
"""Exact audit for live-three-zero-two-marked-exceptional-beta.md."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations
from math import factorial, prod

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


def binary_two_marked_row(
    word: tuple[int, ...],
    active_sites: tuple[int, ...],
    exceptional_sites: tuple[int, ...],
    marked_pair: tuple[int, int],
    kappa: sp.Expr,
    lambdas: tuple[sp.Expr, ...],
) -> list[sp.Expr]:
    """The x_2 z_2 response on active binary star variables.

    The two sites in ``marked_pair`` are the only sites of colour two, so
    they are the unique marked pair and disappear before the binary
    cofactor is evaluated.
    """
    exceptional_index = {
        site: index for index, site in enumerate(exceptional_sites)
    }
    columns = [(site, colour) for site in active_sites for colour in range(2)]
    column_index = {column: index for index, column in enumerate(columns)}

    def edge(i: int, j: int) -> sp.Expr:
        if word[i] == word[j]:
            return sp.S.Zero
        require(
            word[i] in (0, 1) and word[j] in (0, 1),
            "word[i] in (0, 1) and word[j] in (0, 1)",
        )
        if i in exceptional_index and j in exceptional_index:
            raise AssertionError("unmarked exceptional sites are monochromatic")
        if i in exceptional_index:
            return lambdas[exceptional_index[i]]
        if j in exceptional_index:
            return lambdas[exceptional_index[j]]
        return kappa

    row = [sp.S.Zero] * len(columns)
    for star_site in active_sites:
        remaining = tuple(
            site
            for site in range(len(word))
            if site not in (*marked_pair, star_site)
        )
        cofactor = sum(
            prod(edge(i, j) for i, j in matching)
            for matching in perfect_matchings(remaining)
        )
        row[column_index[star_site, word[star_site]]] += 2 * cofactor
    return [sp.expand(value) for value in row]


def audit_uniform_formula(r: int, exceptional_count: int) -> None:
    require(
        2 <= exceptional_count <= r + 1,
        "2 <= exceptional_count <= r + 1",
    )
    active_count = 2 * r + 1 - exceptional_count
    active_sites = tuple(range(active_count))
    exceptional_sites = tuple(range(active_count, 2 * r + 1))
    marked_pair = exceptional_sites[:2]
    unmarked_exceptional = exceptional_sites[2:]
    subset_size = r + 2 - exceptional_count
    kappa = sp.Symbol("kappa", nonzero=True)
    lambdas = tuple(
        sp.Symbol(f"lambda{index}", nonzero=True)
        for index in range(exceptional_count)
    )
    coefficient = (
        2
        * factorial(r - 1)
        * prod(lambdas[2:])
        * kappa ** (r - exceptional_count + 1)
    )

    incidence = subset_incidence(active_count, subset_size)
    require(
        1 <= subset_size < active_count,
        "1 <= subset_size < active_count",
    )
    require(
        incidence.rank() == active_count,
        "incidence.rank() == active_count",
    )

    if r <= 4:
        chosen = set(active_sites[:subset_size])
        total_sites = 2 * r + 1

        word_zero = tuple(
            2
            if site in marked_pair
            else 0
            if site in unmarked_exceptional or site in chosen
            else 1
            for site in range(total_sites)
        )
        row_zero = binary_two_marked_row(
            word_zero,
            active_sites,
            exceptional_sites,
            marked_pair,
            kappa,
            lambdas,
        )
        require(
            row_zero == [
                coefficient if colour == 0 and site in chosen else 0
                for site in active_sites
                for colour in range(2)
            ],
            "row_zero == [ coefficient if colour == 0 and site in chos...",
        )

        word_one = tuple(
            2 if colour == 2 else 1 - colour for colour in word_zero
        )
        row_one = binary_two_marked_row(
            word_one,
            active_sites,
            exceptional_sites,
            marked_pair,
            kappa,
            lambdas,
        )
        require(
            row_one == [
                coefficient if colour == 1 and site in chosen else 0
                for site in active_sites
                for colour in range(2)
            ],
            "row_one == [ coefficient if colour == 1 and site in chose...",
        )

        # Put the target active site in colour two as well.  Only the fixed
        # exceptional pair can be marked in the coefficient of its row-two
        # star variable, and the remaining binary cofactor has the same
        # monomial value.
        target = active_sites[0]
        zero_sites = set(active_sites[1:r])
        word_two = tuple(
            2
            if site in marked_pair or site == target
            else 1
            if site in unmarked_exceptional
            else 0
            if site in zero_sites
            else 1
            for site in range(total_sites)
        )
        remaining = tuple(
            site
            for site in range(total_sites)
            if site not in (*marked_pair, target)
        )
        exceptional_index = {
            site: index for index, site in enumerate(exceptional_sites)
        }

        def edge(i: int, j: int) -> sp.Expr:
            if word_two[i] == word_two[j]:
                return sp.S.Zero
            if i in exceptional_index:
                return lambdas[exceptional_index[i]]
            if j in exceptional_index:
                return lambdas[exceptional_index[j]]
            return kappa

        target_cofactor = sum(
            prod(edge(i, j) for i, j in matching)
            for matching in perfect_matchings(remaining)
        )
        require(
            sp.expand(2 * target_cofactor) == coefficient,
            "sp.expand(2 * target_cofactor) == coefficient",
        )


def audit_first_extreme_symbolic_minor() -> None:
    """Full ternary r=3,t=4 minor, including all off-block terms."""
    h01, h02, h12, mu = sp.symbols("h01 h02 h12 mu", nonzero=True)
    nus = sp.symbols("nu0:4", nonzero=True)
    hessian = sp.Matrix(
        [[0, h01, h02], [h01, 0, h12], [h02, h12, 0]]
    )

    # One common-beta live site, two type-10 centres, then four exceptional
    # live sites.  The first two exceptional sites are the marked pair.
    active_sites = (0, 1, 2)
    centres = (1, 2)
    exceptional_sites = (3, 4, 5, 6)
    marked_pair = exceptional_sites[:2]
    matrices = [sp.eye(3), sp.diag(1, 1, 0), sp.diag(1, 1, 0)]
    matrices += [sp.eye(3)] * 4
    betas = [mu, mu, mu, *nus]
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

    def response_row(word: tuple[int, ...]) -> list[sp.Expr]:
        marked_sites = [
            site
            for site in range(7)
            if matrices[site][word[site], 2] != 0
        ]
        row = [sp.S.Zero] * len(columns)
        for u, v in combinations(marked_sites, 2):
            marked_weight = 2 * matrices[u][word[u], 2] * matrices[v][word[v], 2]
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
                row[column_index[star_site, word[star_site]]] += (
                    marked_weight * cofactor
                )
        return [sp.cancel(value) for value in row]

    rows = []
    for colour in (0, 1):
        for target in active_sites:
            word = [1 - colour] * 7
            word[marked_pair[0]] = 2
            word[marked_pair[1]] = 2
            word[exceptional_sites[2]] = colour
            word[exceptional_sites[3]] = colour
            word[target] = colour
            rows.append(response_row(tuple(word)))

    for target in active_sites:
        word = [0] * 7
        word[marked_pair[0]] = 2
        word[marked_pair[1]] = 2
        word[exceptional_sites[2]] = 1
        word[exceptional_sites[3]] = 1
        word[target] = 2
        rows.append(response_row(tuple(word)))

    minor = sp.Matrix(rows)
    coefficient = 4 * h01**2 / ((mu + nus[2]) * (mu + nus[3]))
    require(
        minor.shape == (9, 9),
        "minor.shape == (9, 9)",
    )
    require(
        minor[:6, 6:] == sp.zeros(6, 3),
        "minor[:6, 6:] == sp.zeros(6, 3)",
    )
    require(
        all(
            sp.cancel(minor[row, column] - coefficient * int(row == column)) == 0
            for row in range(6)
            for column in range(6)
        ),
        "all( sp.cancel(minor[row, column] - coefficient * int(row...",
    )
    require(
        all(
            sp.cancel(minor[6 + row, 6 + column] - coefficient * int(row == column))
            == 0
            for row in range(3)
            for column in range(3)
        ),
        "all( sp.cancel(minor[6 + row, 6 + column] - coefficient *...",
    )
    require(
        sp.cancel(minor.det(method="domain-ge") - coefficient**9) == 0,
        "sp.cancel(minor.det(method=\"domain-ge\") - coefficient**9)...",
    )


def main() -> None:
    cases = 0
    for r in range(2, 9):
        for exceptional_count in range(2, r + 2):
            audit_uniform_formula(r, exceptional_count)
            cases += 1
    audit_first_extreme_symbolic_minor()
    print("Live three-zero two-marked exceptional-beta injectivity: PASS")
    print(f"uniform two-marked weighted-subset cases audited: {cases}")
    print("r=3,t=4 full ternary 9-square minor is a pure monomial")


if __name__ == "__main__":
    main()
