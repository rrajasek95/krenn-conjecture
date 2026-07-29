#!/usr/bin/env python3
"""Exact audit for live-three-zero-all-exceptional-nine-live.md."""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import prod

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


def coupled_incidence_rank(modulus: int = 1009) -> tuple[int, int, int]:
    """Rank of the t=9 split operator on symmetric disjoint triples."""
    points = tuple(range(9))
    triples = tuple(combinations(points, 3))
    triple_index = {triple: index for index, triple in enumerate(triples)}
    variables = tuple(
        (left_index, right_index)
        for left_index, left in enumerate(triples)
        for right_index in range(left_index + 1, len(triples))
        if set(left).isdisjoint(triples[right_index])
    )
    variable_index = {variable: index for index, variable in enumerate(variables)}

    def variable(left_index: int, right_index: int) -> int:
        pair = (
            (left_index, right_index)
            if left_index < right_index
            else (right_index, left_index)
        )
        return variable_index[pair]

    # Sparse exact row reduction modulo a prime.  Full column rank modulo
    # a prime certifies full column rank over Q for this integer matrix.
    basis: dict[int, dict[int, int]] = {}
    row_count = 0
    for right_index, right in enumerate(triples):
        complement = tuple(point for point in points if point not in right)
        for marked_pair in combinations(complement, 2):
            left_pool = tuple(
                point for point in complement if point not in marked_pair
            )
            row = {
                variable(triple_index[left], right_index): 1
                for left in combinations(left_pool, 3)
            }
            row_count += 1
            while row:
                pivot = min(row)
                pivot_value = row[pivot]
                if pivot not in basis:
                    inverse = pow(pivot_value, -1, modulus)
                    basis[pivot] = {
                        column: value * inverse % modulus
                        for column, value in row.items()
                        if value % modulus
                    }
                    break
                pivot_row = basis[pivot]
                for column, value in pivot_row.items():
                    updated = (row.get(column, 0) - pivot_value * value) % modulus
                    if updated:
                        row[column] = updated
                    elif column in row:
                        del row[column]

    return row_count, len(variables), len(basis)


def audit_permanental_obstruction() -> None:
    # If all 3x3 permanents of a six-by-three nonzero matrix vanish,
    # writing each row as c_i (rho_i, sigma_i, 1) makes each permanent a
    # sum of the three pair permanents.  W_{3,2}(6) is injective.
    pairs = tuple(combinations(range(6), 2))
    triples = tuple(combinations(range(6), 3))
    inclusion = sp.Matrix([
        [int(set(pair).issubset(triple)) for pair in pairs]
        for triple in triples
    ])
    assert inclusion.shape == (20, 15)
    assert inclusion.rank() == 15

    rho0, rho1, rho2 = sp.symbols("rho0 rho1 rho2", nonzero=True)
    pair_sums = sp.Matrix([rho0 + rho1, rho0 + rho2, rho1 + rho2])
    pair_matrix = sp.Matrix([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
    assert pair_matrix.det() == -2
    assert pair_matrix.inv() * pair_sums == sp.Matrix([rho0, rho1, rho2])


def audit_symbolic_pivot_expansion() -> None:
    h01 = sp.Symbol("h01", nonzero=True)
    row_factors = sp.symbols("a0:4", nonzero=True)
    entries = sp.symbols("u0:12", nonzero=True)
    normalized = sp.Matrix(4, 3, entries)
    cofactor = sp.Matrix([
        [row_factors[row] * normalized[row, column] for column in range(3)]
        + [row_factors[row]]
        for row in range(4)
    ])
    direct = 2 * h01**4 * permanent(cofactor)
    split = (
        2
        * h01**4
        * prod(row_factors)
        * sum(
            permanent(normalized.extract(rows, range(3)))
            for rows in combinations(range(4), 3)
        )
    )
    assert sp.expand(direct - split) == 0

    # The coupled incidence variable is the symmetrically rescaled
    # Cauchy permanent, not the orientation-dependent H permanent.
    mu = sp.Rational(1)
    left_values = tuple(map(sp.Rational, (2, 3, 5)))
    right_values = tuple(map(sp.Rational, (7, 11, 13)))
    h_left_right = sp.Matrix([
        [
            (left + mu) / (left + right)
            for right in right_values
        ]
        for left in left_values
    ])
    h_right_left = sp.Matrix([
        [
            (right + mu) / (right + left)
            for left in left_values
        ]
        for right in right_values
    ])
    symmetric_from_left = prod(right + mu for right in right_values) * permanent(
        h_left_right
    )
    symmetric_from_right = prod(left + mu for left in left_values) * permanent(
        h_right_left
    )
    assert symmetric_from_left == symmetric_from_right


def audit_complete_selected_response() -> None:
    """Full direct-plus-marked response at one exact rational point."""
    exceptional_sites = tuple(range(9))
    centres = (9, 10)
    active_sites = centres
    columns = [(site, colour) for colour in range(3) for site in centres]
    column_index = {column: index for index, column in enumerate(columns)}
    hessian = (
        (Fraction(0), Fraction(1), Fraction(2)),
        (Fraction(1), Fraction(0), Fraction(3)),
        (Fraction(2), Fraction(3), Fraction(0)),
    )
    betas = tuple(map(Fraction, (*range(2, 11), 1, 1)))

    def p_entry(site: int, colour: int, source: int) -> int:
        return int(colour == source and (site < 9 or source < 2))

    def edge(word: tuple[int, ...], left: int, right: int) -> Fraction:
        if left in centres and word[left] == 2:
            return Fraction(0)
        if right in centres and word[right] == 2:
            return Fraction(0)
        return hessian[word[left]][word[right]] / (betas[left] + betas[right])

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
        row = [Fraction(0)] * 6
        direct_weight = (
            Fraction(1, 2)
            if include_direct
            and source_left != source_right
            and {source_left, source_right} == {0, 1}
            else Fraction(0)
        )
        if direct_weight:
            for star_site in centres:
                remaining = tuple(
                    site for site in range(11) if site != star_site
                )
                row[column_index[star_site, word[star_site]]] += (
                    direct_weight * hafnian(word, remaining)
                )
        for u, v in combinations(range(11), 2):
            marked_weight = (
                p_entry(u, word[u], source_left)
                * p_entry(v, word[v], source_right)
                + p_entry(u, word[u], source_right)
                * p_entry(v, word[v], source_left)
            )
            if not marked_weight:
                continue
            for star_site in centres:
                if star_site in (u, v):
                    continue
                remaining = tuple(
                    site
                    for site in range(11)
                    if site not in (u, v, star_site)
                )
                row[column_index[star_site, word[star_site]]] += (
                    marked_weight * hafnian(word, remaining)
                )
        return row

    right_exceptional = (0, 1, 2)
    left_exceptional = (3, 4, 5, 6)
    marked_pair = (7, 8)
    rows = []
    for colour in (0, 1):
        for target in centres:
            other = centres[0] if target == centres[1] else centres[1]
            word = [0] * 11
            for site in marked_pair:
                word[site] = 2
            for site in left_exceptional:
                word[site] = colour
            for site in right_exceptional:
                word[site] = 1 - colour
            word[target] = colour
            word[other] = 1 - colour
            rows.append(response_row(tuple(word), 2, 2))
    for target in centres:
        other = centres[0] if target == centres[1] else centres[1]
        word = [0] * 11
        for site in marked_pair:
            word[site] = 2
        for site in left_exceptional:
            word[site] = 0
        for site in right_exceptional:
            word[site] = 1
        word[target] = 2
        word[other] = 1
        rows.append(response_row(tuple(word), 2, 2))

    cofactor = sp.Matrix([
        [sp.Rational(1, betas[left] + betas[right]) for right in right_exceptional]
        + [sp.Rational(1, betas[left] + 1)]
        for left in left_exceptional
    ])
    coefficient = 2 * permanent(cofactor)
    minor = sp.Matrix(rows)
    assert minor == coefficient * sp.eye(6)

    # Exercise the direct branch of the complete evaluator independently.
    direct_word = tuple(index % 2 for index in range(11))
    complete = response_row(direct_word, 0, 1, True)
    marked_only = response_row(direct_word, 0, 1, False)
    difference = [left - right for left, right in zip(complete, marked_only)]
    expected = [Fraction(0)] * 6
    for star_site in centres:
        remaining = tuple(site for site in range(11) if site != star_site)
        expected[column_index[star_site, direct_word[star_site]]] += (
            Fraction(1, 2) * hafnian(direct_word, remaining)
        )
    assert difference == expected
    assert any(difference)


def main() -> None:
    rows, columns, rank = coupled_incidence_rank()
    assert (rows, columns, rank) == (1260, 840, 840)
    audit_permanental_obstruction()
    audit_symbolic_pivot_expansion()
    audit_complete_selected_response()
    print("Live three-zero all-exceptional nine-live injectivity: PASS")
    print(f"coupled incidence over F_1009: {rows} rows x {columns} columns; rank={rank}")
    print("local W_{3,2}(6): 20 rows x 15 columns; rank=15 over QQ")
    print("complete selected zero-star minor: diagonal 6-square")


if __name__ == "__main__":
    main()
