#!/usr/bin/env python3
"""Exact audit for live-three-zero-common-power-star-injectivity.md.

The minimal residual has three live sites, two type-10 centres, and one
literal zero site.  Its cap is linear in the five blocks incident with the
zero site.  This script constructs that map over QQ, exhibits an explicit
45-by-45 nonsingular minor, and checks the beta-stratified symbolic
elimination used in the proof note.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

import sympy as sp


COLORS = range(3)
NONZERO_SITES = range(5)
ZERO_SITE = 5
I3 = sp.eye(3)
D10 = sp.diag(1, 1, 0)
P = (I3, I3, I3, D10, D10, sp.zeros(3))
H_RATIONAL = sp.Matrix([[0, 1, 2], [1, 0, 3], [2, 3, 0]])
B_RATIONAL = sp.Matrix(
    [[0, sp.Rational(1, 2), 0],
     [sp.Rational(1, 2), 0, 0],
     [0, 0, 0]]
)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def block_entry(
    blocks: dict[tuple[int, int], sp.Matrix],
    i: int,
    j: int,
    colour_i: int,
    colour_j: int,
) -> sp.Expr:
    if i < j:
        return blocks[i, j][colour_i, colour_j]
    return blocks[j, i][colour_j, colour_i]


def hafnian_coefficient(
    blocks: dict[tuple[int, int], sp.Matrix],
    word: tuple[int, ...],
    vertices: tuple[int, ...],
) -> sp.Expr:
    return sp.expand(sum(
        sp.prod(block_entry(blocks, i, j, word[i], word[j]) for i, j in matching)
        for matching in perfect_matchings(vertices)
    ))


STAR_VARIABLES = tuple(
    (site, site_colour, zero_colour)
    for site in NONZERO_SITES
    for site_colour in COLORS
    for zero_colour in COLORS
)
STAR_INDEX = {variable: index for index, variable in enumerate(STAR_VARIABLES)}


def cap_row(
    word: tuple[int, ...],
    source_left: int,
    source_right: int,
    blocks: dict[tuple[int, int], sp.Matrix],
    direct: sp.Matrix,
) -> list[sp.Expr]:
    """Coefficient row in the 45 arbitrary nonzero--zero block entries."""
    row = [sp.S.Zero] * len(STAR_VARIABLES)

    # In the direct term the zero site is paired to ``site`` and the other
    # four nonzero sites form a perfect matching.
    if direct[source_left, source_right] != 0:
        for site in NONZERO_SITES:
            rest = tuple(other for other in NONZERO_SITES if other != site)
            row[STAR_INDEX[site, word[site], word[ZERO_SITE]]] += (
                direct[source_left, source_right]
                * hafnian_coefficient(blocks, word, rest)
            )

    # The two marked factors occupy u,v.  Of the three remaining nonzero
    # sites, one is paired to the zero site and the other two use q.
    for u, v in combinations(NONZERO_SITES, 2):
        marked = (
            P[u][word[u], source_left] * P[v][word[v], source_right]
            + P[u][word[u], source_right] * P[v][word[v], source_left]
        )
        if marked == 0:
            continue
        remaining = [site for site in NONZERO_SITES if site not in (u, v)]
        for star_site in remaining:
            edge_sites = [site for site in remaining if site != star_site]
            row[STAR_INDEX[star_site, word[star_site], word[ZERO_SITE]]] += (
                marked
                * block_entry(
                    blocks,
                    edge_sites[0],
                    edge_sites[1],
                    word[edge_sites[0]],
                    word[edge_sites[1]],
                )
            )
    return [sp.expand(value) for value in row]


# Fifteen diagonal-source equations for one fixed colour at the zero site.
# Repeating them for the three zero-site colours gives the 45-row minor.
COMMON_BETA_MINOR_ROWS = (
    ((0, 0, 2, 1, 1), 0),
    ((0, 0, 2, 1, 1), 1),
    ((0, 0, 2, 1, 2), 0),
    ((0, 0, 2, 2, 1), 0),
    ((0, 1, 2, 0, 1), 0),
    ((0, 1, 2, 0, 1), 1),
    ((0, 1, 2, 1, 0), 0),
    ((0, 1, 2, 1, 0), 1),
    ((0, 2, 0, 1, 1), 1),
    ((0, 2, 1, 0, 1), 0),
    ((0, 2, 2, 0, 1), 0),
    ((1, 0, 2, 0, 1), 0),
    ((1, 0, 2, 0, 1), 1),
    ((2, 0, 2, 0, 1), 0),
    ((2, 2, 0, 0, 1), 0),
)


def audit_full_rational_map() -> None:
    blocks = {
        (i, j): P[i] * H_RATIONAL * P[j].T / 2
        for i, j in combinations(NONZERO_SITES, 2)
    }

    nonzero_rows = 0
    for word in product(COLORS, repeat=6):
        for source_left, source_right in product(COLORS, repeat=2):
            row = cap_row(word, source_left, source_right, blocks, B_RATIONAL)
            if any(row):
                nonzero_rows += 1
    assert nonzero_rows == 2718

    selected_rows = []
    for five_word, source_colour in COMMON_BETA_MINOR_ROWS:
        for zero_colour in COLORS:
            word = five_word + (zero_colour,)
            selected_rows.append(
                cap_row(word, source_colour, source_colour, blocks, B_RATIONAL)
            )
    minor = sp.Matrix(selected_rows)
    assert minor.shape == (45, 45)

    # The zero-site colour merely selects one column of each star block.
    # Thus the minor is K tensor I_3.
    one_column_indices = [3 * site_colour for site_colour in range(15)]
    one_column = minor.extract(range(0, 45, 3), one_column_indices)
    assert minor == sp.kronecker_product(one_column, sp.eye(3))
    assert one_column.det(method="domain-ge") == 2**8 * 3**10
    assert minor.det(method="domain-ge") == 2**24 * 3**30


def symbolic_internal_blocks(
    h01: sp.Expr,
    h02: sp.Expr,
    h12: sp.Expr,
    edge_weights: dict[tuple[int, int], sp.Expr],
) -> dict[tuple[int, int], sp.Matrix]:
    hessian = sp.Matrix([[0, h01, h02], [h01, 0, h12], [h02, h12, 0]])
    return {
        (i, j): edge_weights[i, j] * P[i] * hessian * P[j].T
        for i, j in combinations(NONZERO_SITES, 2)
    }


def one_zero_column_rows(
    blocks: dict[tuple[int, int], sp.Matrix],
    active_sites: tuple[int, ...],
    unique_marked_only: bool,
) -> list[tuple[list[sp.Expr], tuple[tuple[int, ...], int]]]:
    """Diagonal-cap rows for one fixed coordinate at the literal zero."""
    variables = tuple((site, colour) for site in active_sites for colour in COLORS)
    variable_index = {variable: index for index, variable in enumerate(variables)}
    answer = []
    for five_word in product(COLORS, repeat=5):
        word = five_word + (0,)
        for source_colour in COLORS:
            marked_sites = [
                site
                for site in NONZERO_SITES
                if P[site][word[site], source_colour] != 0
            ]
            if unique_marked_only and len(marked_sites) != 2:
                continue
            row = [sp.S.Zero] * len(variables)
            for u, v in combinations(marked_sites, 2):
                marked = 2 * P[u][word[u], source_colour] * P[v][word[v], source_colour]
                remaining = [site for site in NONZERO_SITES if site not in (u, v)]
                for star_site in remaining:
                    if star_site not in active_sites:
                        continue
                    edge_sites = [site for site in remaining if site != star_site]
                    row[variable_index[star_site, word[star_site]]] += (
                        marked
                        * block_entry(
                            blocks,
                            edge_sites[0],
                            edge_sites[1],
                            word[edge_sites[0]],
                            word[edge_sites[1]],
                        )
                    )
            row = [sp.expand(value) for value in row]
            if any(row):
                answer.append((row, (five_word, source_colour)))
    return answer


def is_nonzero_monomial(expression: sp.Expr, symbols: tuple[sp.Symbol, ...]) -> bool:
    polynomial = sp.Poly(sp.expand(expression), *symbols)
    return len(polynomial.terms()) == 1 and polynomial.terms()[0][1] != 0


def audit_beta_strata() -> None:
    """Audit the four possible numbers of beta-matched live star blocks."""
    h01, h02, h12 = sp.symbols("h01 h02 h12", nonzero=True)
    edge_weights = {
        edge: sp.Symbol(f"s{edge[0]}{edge[1]}", nonzero=True)
        for edge in combinations(NONZERO_SITES, 2)
    }
    arbitrary_blocks = symbolic_internal_blocks(h01, h02, h12, edge_weights)
    monomial_symbols = (h01, h02, h12, *edge_weights.values())

    # If k <= 2 live sites have beta mu, only those sites and the two
    # type-10 centres can have nonzero blocks to z.  Rows with a unique
    # marked pair give a triangular elimination whose pivots are single
    # nonzero q entries; it is valid for arbitrary nonzero edge scalars.
    triangular_counts = {}
    for live_count in range(3):
        active_sites = tuple(range(live_count)) + (3, 4)
        variables = tuple((site, colour) for site in active_sites for colour in COLORS)
        rows = one_zero_column_rows(arbitrary_blocks, active_sites, True)
        remaining = set(range(len(variables)))
        pivots = []
        while remaining:
            choice = None
            for row, metadata in rows:
                support = {index for index, value in enumerate(row) if value != 0}
                unresolved = support & remaining
                if len(unresolved) == 1:
                    pivot = next(iter(unresolved))
                    choice = (pivot, row[pivot], metadata)
                    break
            assert choice is not None, (live_count, tuple(variables[index] for index in remaining))
            pivot, coefficient, metadata = choice
            assert is_nonzero_monomial(coefficient, monomial_symbols), (
                live_count,
                metadata,
                sp.factor(coefficient),
            )
            pivots.append((variables[pivot], metadata, sp.factor(coefficient)))
            remaining.remove(pivot)
        triangular_counts[live_count] = len(pivots)
        assert len(pivots) == 3 * (live_count + 2)

    # If all three live sites have beta mu, all five nonzero sites share
    # beta mu.  Hence every internal scalar is 1/(2 mu).  The explicit
    # fifteen-row minor is nonzero for every invertible zero-diagonal H.
    mu = sp.Symbol("mu", nonzero=True)
    common_weights = {edge: 1 / (2 * mu) for edge in edge_weights}
    common_blocks = symbolic_internal_blocks(h01, h02, h12, common_weights)
    all_rows = one_zero_column_rows(common_blocks, tuple(NONZERO_SITES), True)
    row_lookup = {metadata: row for row, metadata in all_rows}
    common_minor = sp.Matrix([
        row_lookup[metadata] for metadata in COMMON_BETA_MINOR_ROWS
    ])
    assert common_minor.shape == (15, 15)
    assert sp.factor(common_minor.det(method="domain-ge")) == (
        8 * h02**5 * h12**10 / mu**15
    )

    assert triangular_counts == {0: 6, 1: 9, 2: 12}


def main() -> None:
    audit_full_rational_map()
    audit_beta_strata()
    print("Live three-zero common-power star injectivity: PASS")
    print("normalized map: 2718 nonzero rows x 45 columns; rank=45 over QQ")
    print("explicit minor determinant: 2^24 * 3^30")
    print("beta strata: active live counts 0,1,2 triangular; count 3 symbolic minor")


if __name__ == "__main__":
    main()
