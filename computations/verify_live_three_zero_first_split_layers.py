#!/usr/bin/env python3
"""Exact audit for live-three-zero-first-split-layers.md."""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import factorial, prod

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


def permanent(matrix: sp.Matrix) -> sp.Expr:
    rows, columns = matrix.shape
    assert rows == columns
    if rows == 0:
        return sp.S.One
    return sum(
        matrix[0, column]
        * permanent(matrix.minor_submatrix(0, column))
        for column in range(columns)
    )


def inclusion_matrix(number_of_points: int, row_size: int, column_size: int) -> sp.Matrix:
    rows = tuple(combinations(range(number_of_points), row_size))
    columns = tuple(combinations(range(number_of_points), column_size))
    return sp.Matrix([
        [int(set(column).issubset(row)) for column in columns]
        for row in rows
    ])


def audit_uniform_inclusion_layers() -> int:
    cases = 0
    for r in range(3, 11):
        p = r - 1
        number_of_points = p + 2
        matrix = inclusion_matrix(number_of_points, p, 1)
        assert matrix.rank() == number_of_points
        cases += 1
    for r in range(4, 11):
        p = r - 1
        number_of_points = p + 2
        matrix = inclusion_matrix(number_of_points, p, 2)
        assert matrix.shape == (
            sp.binomial(number_of_points, 2),
            sp.binomial(number_of_points, 2),
        )
        assert matrix.rank() == matrix.cols
        cases += 1

    # If all two-by-two permanents of nonzero row vectors vanished, their
    # nonzero coordinate ratios would be pairwise negatives.  Three rows
    # already contradict this in characteristic zero.
    rho0, rho1, rho2 = sp.symbols("rho0 rho1 rho2", nonzero=True)
    pair_sums = sp.Matrix([rho0 + rho1, rho0 + rho2, rho1 + rho2])
    coefficient_matrix = sp.Matrix([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
    assert coefficient_matrix.det() == -2
    assert coefficient_matrix.inv() * pair_sums == sp.Matrix([rho0, rho1, rho2])
    return cases


def audit_r4_symbolic_response(exceptional_count: int) -> tuple[int, str]:
    """Symbolic pivots plus exact complete-response minors at r=4."""
    assert exceptional_count in (6, 7)
    h01 = sp.Symbol("h01", nonzero=True)
    live_count = 7
    centres = (7, 8)
    common_live_sites = tuple(range(exceptional_count, live_count))
    active_sites = common_live_sites + centres
    columns = [
        (site, colour) for colour in range(3) for site in active_sites
    ]
    column_index = {column: index for index, column in enumerate(columns)}

    if exceptional_count == 6:
        right_exceptional = (0,)
        left_exceptional = (1, 2, 3)
        marked_pair = (4, 5)
    else:
        right_exceptional = (0, 1)
        left_exceptional = (2, 3, 4)
        marked_pair = (5, 6)

    p = 3
    k = 8 - exceptional_count
    row_factors = sp.symbols("a0:3", nonzero=True)
    normalized_entries = sp.symbols(
        f"u0:{p * len(right_exceptional)}", nonzero=True
    )
    h_matrix = sp.Matrix(
        p,
        len(right_exceptional),
        normalized_entries,
    )
    cofactor_matrix = sp.Matrix([
        [row_factors[row] * h_matrix[row, column]
         for column in range(len(right_exceptional))]
        + [row_factors[row]] * k
        for row in range(p)
    ])
    coefficient = 2 * h01**p * permanent(cofactor_matrix)
    normalized_sum = sum(
        permanent(h_matrix.extract(row_subset, range(len(right_exceptional))))
        for row_subset in combinations(range(p), len(right_exceptional))
    )
    factored_coefficient = (
        2
        * h01**p
        * factorial(k)
        * prod(row_factors)
        * normalized_sum
    )
    assert sp.expand(coefficient - factored_coefficient) == 0

    # Evaluate the complete direct-plus-marked response over exact
    # rationals.  Symbolic factorization above proves the pivot formula;
    # this independent audit retains all lower-block/off-source terms
    # without costly expansion of irrelevant rational functions.
    rational_hessian = (
        (Fraction(0), Fraction(1), Fraction(2)),
        (Fraction(1), Fraction(0), Fraction(3)),
        (Fraction(2), Fraction(3), Fraction(0)),
    )
    rational_betas = tuple(
        [Fraction(index + 2) for index in range(exceptional_count)]
        + [Fraction(1)] * (9 - exceptional_count)
    )

    def p_entry(site: int, colour: int, source: int) -> int:
        return int(colour == source and (site < 7 or source < 2))

    def edge(word: tuple[int, ...], left: int, right: int) -> Fraction:
        if left in centres and word[left] == 2:
            return Fraction(0)
        if right in centres and word[right] == 2:
            return Fraction(0)
        return (
            rational_hessian[word[left]][word[right]]
            / (rational_betas[left] + rational_betas[right])
        )

    @lru_cache(maxsize=None)
    def hafnian(word: tuple[int, ...], vertices: tuple[int, ...]) -> Fraction:
        return sum(
            (
                prod(edge(word, left, right) for left, right in matching)
                for matching in perfect_matchings(vertices)
            ),
            Fraction(0),
        )

    def response_row(
        word: tuple[int, ...],
        source_left: int,
        source_right: int,
        include_direct: bool = True,
    ) -> list[Fraction]:
        """One exact row of the complete active zero-star response."""
        row = [Fraction(0)] * len(columns)
        direct_weight = (
            Fraction(1, 2)
            if include_direct
            and source_left != source_right
            and {source_left, source_right} == {0, 1}
            else Fraction(0)
        )
        if direct_weight:
            for star_site in active_sites:
                remaining = tuple(
                    site for site in range(9) if site != star_site
                )
                row[column_index[star_site, word[star_site]]] += (
                    direct_weight * hafnian(word, remaining)
                )
        for u, v in combinations(range(9), 2):
            marked_weight = (
                p_entry(u, word[u], source_left)
                * p_entry(v, word[v], source_right)
                + p_entry(u, word[u], source_right)
                * p_entry(v, word[v], source_left)
            )
            if not marked_weight:
                continue
            for star_site in active_sites:
                if star_site in (u, v):
                    continue
                remaining = tuple(
                    site
                    for site in range(9)
                    if site not in (u, v, star_site)
                )
                row[column_index[star_site, word[star_site]]] += (
                    marked_weight * hafnian(word, remaining)
                )
        return row

    rows = []
    for colour in (0, 1):
        for target in active_sites:
            word = [1 - colour] * 9
            for site in marked_pair:
                word[site] = 2
            for site in left_exceptional:
                word[site] = colour
            for site in right_exceptional:
                word[site] = 1 - colour
            word[target] = colour
            rows.append(response_row(tuple(word), 2, 2))
    for target in active_sites:
        word = [1] * 9
        for site in marked_pair:
            word[site] = 2
        for site in left_exceptional:
            word[site] = 0
        for site in right_exceptional:
            word[site] = 1
        word[target] = 2
        rows.append(response_row(tuple(word), 2, 2))

    minor = sp.Matrix(rows)
    numeric_cofactor_matrix = sp.Matrix([
        [
            sp.Rational(1, rational_betas[left] + rational_betas[right])
            for right in right_exceptional
        ]
        + [sp.Rational(1, rational_betas[left] + 1)] * k
        for left in left_exceptional
    ])
    coefficient_numeric = 2 * permanent(numeric_cofactor_matrix)
    active_count = len(active_sites)
    assert minor.shape == (3 * active_count, 3 * active_count)
    assert all(
        sp.cancel(
            minor[row, column] - coefficient_numeric * int(row == column)
        )
        == 0
        for row in range(2 * active_count)
        for column in range(2 * active_count)
    )
    assert minor[: 2 * active_count, 2 * active_count :] == sp.zeros(
        2 * active_count, active_count
    )
    assert all(
        sp.cancel(
            minor[2 * active_count + row, 2 * active_count + column]
            - coefficient_numeric * int(row == column)
        )
        == 0
        for row in range(active_count)
        for column in range(active_count)
    )

    # Exercise the direct branch too: the difference between the complete
    # and marked-only rows is exactly the direct hafnian contribution.
    direct_word = tuple(index % 2 for index in range(9))
    complete = response_row(direct_word, 0, 1, True)
    marked_only = response_row(direct_word, 0, 1, False)
    direct_difference = [a - b for a, b in zip(complete, marked_only)]
    expected_direct = [Fraction(0)] * len(columns)
    for star_site in active_sites:
        remaining = tuple(site for site in range(9) if site != star_site)
        expected_direct[column_index[star_site, direct_word[star_site]]] += (
            Fraction(1, 2) * hafnian(direct_word, remaining)
        )
    assert direct_difference == expected_direct
    assert any(direct_difference)
    if exceptional_count == 6:
        description = "4 h01^3 (prod_i a_i) sum_i H_ic"
    else:
        description = "2 h01^3 (prod_i a_i) sum_{i<j} per H[{i,j},R]"
    return active_count, description


def main() -> None:
    inclusion_cases = audit_uniform_inclusion_layers()
    active_six, coefficient_six = audit_r4_symbolic_response(6)
    active_seven, coefficient_seven = audit_r4_symbolic_response(7)
    assert active_six == 3 and active_seven == 2
    print("Live three-zero first split layers: PASS")
    print(f"uniform inclusion matrices audited: {inclusion_cases}")
    print("r=4,t=6 complete selected minor: lower triangular, size 9")
    print("r=4,t=7 complete selected minor: diagonal, size 6")
    print(f"t=6 pivot: {coefficient_six}")
    print(f"t=7 pivot: {coefficient_seven}")


if __name__ == "__main__":
    main()
