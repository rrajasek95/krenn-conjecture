#!/usr/bin/env python3
"""Exact audit for live-three-zero-all-exceptional-five-live.md."""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
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


def main() -> None:
    h01, h02, h12, b01, mu = sp.symbols(
        "h01 h02 h12 b01 mu", nonzero=True
    )
    nus = sp.symbols("nu0:5", nonzero=True)
    hessian = sp.Matrix(
        [[0, h01, h02], [h01, 0, h12], [h02, h12, 0]]
    )

    exceptional_sites = tuple(range(5))
    centres = (5, 6)
    matrices = [sp.eye(3)] * 5 + [sp.diag(1, 1, 0)] * 2
    betas = [*nus, mu, mu]
    blocks = {
        (i, j): matrices[i] * hessian * matrices[j].T / (betas[i] + betas[j])
        for i, j in combinations(range(7), 2)
    }
    columns = [(centre, colour) for colour in range(3) for centre in centres]
    column_index = {column: index for index, column in enumerate(columns)}
    direct = sp.Matrix([[0, b01, 0], [b01, 0, 0], [0, 0, 0]])

    def edge(i: int, j: int, colour_i: int, colour_j: int) -> sp.Expr:
        if i < j:
            return blocks[i, j][colour_i, colour_j]
        return blocks[j, i][colour_j, colour_i]

    def hafnian(word: tuple[int, ...], vertices: tuple[int, ...]) -> sp.Expr:
        return sum(
            prod(edge(i, j, word[i], word[j]) for i, j in matching)
            for matching in perfect_matchings(vertices)
        )

    def response_row(
        word: tuple[int, ...], source_left: int, source_right: int
    ) -> list[sp.Expr]:
        """One row of the complete six-column zero-star response."""
        row = [sp.S.Zero] * len(columns)

        # The direct coordinate factor supplies no diagonal-source term,
        # but it is included here for completeness for arbitrary sources.
        if direct[source_left, source_right] != 0:
            for star_site in centres:
                remaining = tuple(
                    site for site in range(7) if site != star_site
                )
                row[column_index[star_site, word[star_site]]] += (
                    direct[source_left, source_right]
                    * hafnian(word, remaining)
                )

        for u, v in combinations(range(7), 2):
            marked_weight = (
                matrices[u][word[u], source_left]
                * matrices[v][word[v], source_right]
                + matrices[u][word[u], source_right]
                * matrices[v][word[v], source_left]
            )
            if marked_weight == 0:
                continue
            for star_site in centres:
                if star_site in (u, v):
                    continue
                remaining = tuple(
                    site for site in range(7) if site not in (u, v, star_site)
                )
                cofactor = hafnian(word, remaining)
                row[column_index[star_site, word[star_site]]] += (
                    marked_weight * cofactor
                )
        return [sp.cancel(value) for value in row]

    def six_row_minor(a: int, b: int, c: int) -> tuple[sp.Matrix, sp.Expr]:
        marked_pair = tuple(
            site for site in exceptional_sites if site not in (a, b, c)
        )
        assert len(marked_pair) == 2
        rows = []
        for colour in (0, 1):
            for target in centres:
                other = centres[0] if target == centres[1] else centres[1]
                word = [0] * 7
                word[marked_pair[0]] = 2
                word[marked_pair[1]] = 2
                word[a] = colour
                word[b] = colour
                word[c] = 1 - colour
                word[target] = colour
                word[other] = 1 - colour
                rows.append(response_row(tuple(word), 2, 2))
        for target in centres:
            other = centres[0] if target == centres[1] else centres[1]
            word = [0] * 7
            word[marked_pair[0]] = 2
            word[marked_pair[1]] = 2
            word[a] = 0
            word[b] = 0
            word[c] = 1
            word[target] = 2
            word[other] = 1
            rows.append(response_row(tuple(word), 2, 2))

        coefficient = 2 * h01**2 * (
            1 / ((nus[a] + mu) * (nus[b] + nus[c]))
            + 1 / ((nus[b] + mu) * (nus[a] + nus[c]))
        )
        return sp.Matrix(rows), coefficient

    # Fix c and use three of the other four exceptional sites.  For every
    # pair among them, the complementary exceptional sites are the unique
    # marked pair.  Each resulting response minor is diagonal.
    c = 4
    a, b, d = 0, 1, 2
    candidates = ((a, b), (a, d), (b, d))
    coefficients = []
    for left, right in candidates:
        minor, coefficient = six_row_minor(left, right, c)
        assert minor.shape == (6, 6)
        assert all(
            sp.cancel(
                minor[row, column] - coefficient * int(row == column)
            )
            == 0
            for row in range(6)
            for column in range(6)
        )
        # The entrywise identity already proves det(minor)=coefficient**6;
        # asking SymPy to re-expand that determinant is needlessly costly.
        coefficients.append(coefficient)

    def normalized(left: int, right: int, coefficient: sp.Expr) -> sp.Expr:
        return sp.cancel(
            coefficient
            * (nus[left] + nus[c])
            * (nus[right] + nus[c])
            / (2 * h01**2)
        )

    n_ab = normalized(a, b, coefficients[0])
    n_ad = normalized(a, d, coefficients[1])
    n_bd = normalized(b, d, coefficients[2])
    g_a = (nus[a] + nus[c]) / (nus[a] + mu)
    g_b = (nus[b] + nus[c]) / (nus[b] + mu)
    g_d = (nus[d] + nus[c]) / (nus[d] + mu)
    assert sp.cancel(n_ab - (g_a + g_b)) == 0
    assert sp.cancel(n_ad - (g_a + g_d)) == 0
    assert sp.cancel(n_bd - (g_b + g_d)) == 0
    assert sp.cancel(n_ab + n_ad - n_bd - 2 * g_a) == 0

    # Enumerate every word and every ordered source pair at one admissible
    # rational point.  The symbolic minors above, not this specialization,
    # prove the uniform result; this is an independent complete-map audit.
    rational_hessian = (
        (Fraction(0), Fraction(1), Fraction(2)),
        (Fraction(1), Fraction(0), Fraction(3)),
        (Fraction(2), Fraction(3), Fraction(0)),
    )
    rational_betas = tuple(map(Fraction, (2, 3, 4, 5, 6, 1, 1)))

    def p_entry(site: int, colour: int, source: int) -> int:
        return int(colour == source and (site < 5 or source < 2))

    def rational_edge(
        word: tuple[int, ...], left: int, right: int
    ) -> Fraction:
        numerator = rational_hessian[word[left]][word[right]]
        if left in centres and word[left] == 2:
            return Fraction(0)
        if right in centres and word[right] == 2:
            return Fraction(0)
        return numerator / (rational_betas[left] + rational_betas[right])

    @lru_cache(maxsize=None)
    def rational_hafnian(
        word: tuple[int, ...], vertices: tuple[int, ...]
    ) -> Fraction:
        return sum(
            (
                prod(
                    rational_edge(word, left, right)
                    for left, right in matching
                )
                for matching in perfect_matchings(vertices)
            ),
            Fraction(0),
        )

    def rational_response(
        word: tuple[int, ...], source_left: int, source_right: int
    ) -> tuple[Fraction, ...]:
        row = [Fraction(0)] * 6
        direct_weight = (
            Fraction(1, 2)
            if {source_left, source_right} == {0, 1}
            and source_left != source_right
            else Fraction(0)
        )
        if direct_weight:
            for centre in centres:
                remaining = tuple(site for site in range(7) if site != centre)
                row[column_index[centre, word[centre]]] += (
                    direct_weight * rational_hafnian(word, remaining)
                )
        for u, v in combinations(range(7), 2):
            marked_weight = (
                p_entry(u, word[u], source_left)
                * p_entry(v, word[v], source_right)
                + p_entry(u, word[u], source_right)
                * p_entry(v, word[v], source_left)
            )
            if not marked_weight:
                continue
            for centre in centres:
                if centre in (u, v):
                    continue
                remaining = tuple(
                    site for site in range(7) if site not in (u, v, centre)
                )
                row[column_index[centre, word[centre]]] += (
                    marked_weight * rational_hafnian(word, remaining)
                )
        return tuple(row)

    basis: dict[int, list[Fraction]] = {}
    nonzero_rows = 0
    for word in product(range(3), repeat=7):
        for source_left, source_right in product(range(3), repeat=2):
            reduced = list(rational_response(word, source_left, source_right))
            if any(reduced):
                nonzero_rows += 1
            for pivot in sorted(basis):
                if reduced[pivot]:
                    scale = reduced[pivot]
                    reduced = [
                        value - scale * basis[pivot][column]
                        for column, value in enumerate(reduced)
                    ]
            if any(reduced):
                pivot = next(index for index, value in enumerate(reduced) if value)
                scale = reduced[pivot]
                basis[pivot] = [value / scale for value in reduced]
    assert len(basis) == 6

    print("Live three-zero all-exceptional five-live injectivity: PASS")
    print("three exact diagonal 6-square response minors reconstructed")
    print("minor-cover identity: N_ab + N_ad - N_bd = 2 g_a")
    print(
        f"complete rational response: {nonzero_rows} nonzero rows x 6 columns; rank=6"
    )


if __name__ == "__main__":
    main()
