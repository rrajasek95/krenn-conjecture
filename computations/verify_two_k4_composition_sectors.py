#!/usr/bin/env python3
"""Exact sector and equivariant-ideal audit for the two-K4 chart."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, product

import sympy as sp
from flint import fmpq_mat, fmpz_mat

import explore_k4_k4_equivariant as equivariant


N, Q = 8, 3
SHORE_WORDS = tuple(product(range(Q), repeat=4))
SHORE_EDGES = tuple(combinations(range(4), 2))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def internal_colour(u, v):
    return (1, 2, 3).index(u ^ v)


def compatible_edges(word):
    return tuple(
        (u, v)
        for u, v in SHORE_EDGES
        if word[u] == word[v] == internal_colour(u, v)
    )


def polynomial_dictionary():
    coefficients, _matching_histogram = equivariant.enumerate_coefficients()
    symbols = sp.symbols("a b c d e f g")
    polynomials = {
        word: equivariant.to_sympy(
            equivariant.canonical_polynomial(counter), symbols
        )
        for word, counter in coefficients.items()
    }
    unique = {}
    for word, counter in coefficients.items():
        unique.setdefault(
            equivariant.canonical_polynomial(counter), word
        )
    return symbols, polynomials, unique


def reduce_f_square(polynomial):
    """Reduce an exponent-counter polynomial modulo 2*f^2+1."""

    answer = {}
    for exponent, coefficient in polynomial:
        f_power = exponent[5]
        reduced = list(exponent)
        reduced[5] = f_power % 2
        reduced = tuple(reduced)
        value = (
            Fraction(coefficient)
            * Fraction(-1, 2) ** (f_power // 2)
        )
        answer[reduced] = answer.get(reduced, Fraction()) + value
    return {key: value for key, value in answer.items() if value}


def audit_matching_sectors():
    matchings = tuple(perfect_matchings(range(N)))
    histogram = Counter(
        sum(u < 4 <= v for u, v in matching)
        for matching in matchings
    )
    assert len(matchings) == 105
    assert histogram == {0: 9, 2: 72, 4: 24}

    compatibility_histogram = Counter(
        len(compatible_edges(word)) for word in SHORE_WORDS
    )
    assert compatibility_histogram == {0: 30, 1: 48, 2: 3}
    assert all(
        len(compatible_edges((colour,) * 4)) == 2
        for colour in range(Q)
    )

    # Every function supported on the 51 live words is an edge-cylinder
    # response.  There are 54 natural generators and exactly three syzygies.
    live_words = tuple(
        word for word in SHORE_WORDS if compatible_edges(word)
    )
    generators = []
    for edge in SHORE_EDGES:
        remainder = tuple(site for site in range(4) if site not in edge)
        for residual_word in product(range(Q), repeat=2):
            generators.append((edge, remainder, residual_word))
    incidence = []
    for word in live_words:
        row = []
        for (u, v), remainder, residual_word in generators:
            row.append(int(
                word[u] == word[v] == internal_colour(u, v)
                and tuple(word[site] for site in remainder)
                == residual_word
            ))
        incidence.append(row)
    matrix = fmpz_mat(incidence)
    assert (matrix.nrows(), matrix.ncols(), matrix.rank()) == (51, 54, 51)
    _kernel, nullity = matrix.nullspace()
    assert nullity == 3


def audit_equivariant_obstruction():
    symbols, polynomials, unique = polynomial_dictionary()
    a, b, c, d, e, f, g = symbols
    assert len(polynomials) == 3**8
    assert len(unique) == 288

    def word(text):
        return tuple(map(int, text))

    # Two four-/six-term equation differences provide the complete branch.
    first = sp.expand(
        polynomials[word("00120000")]
        - polynomials[word("00110000")]
    )
    second = sp.expand(
        polynomials[word("00001200")]
        - polynomials[word("00001100")]
    )
    branch_factor = 2 * f**2 + 1
    assert sp.expand(first + (d - g) ** 2 * branch_factor) == 0
    assert sp.expand(second + (e - g) ** 2 * branch_factor) == 0

    # If the branch factor is nonzero, d=e=g.  Two more exact equation
    # differences then have incompatible constant terms.
    third = sp.expand(
        (
            polynomials[word("00221111")]
            - polynomials[word("00001111")]
        ).subs({d: g, e: g})
    )
    fourth = sp.expand(
        (
            polynomials[word("02021111")]
            - polynomials[word("00001111")]
        ).subs({d: g, e: g})
    )
    assert third == -2 * b * g - 2 * g**2 - 1
    assert fourth == -4 * b * g - 4 * g**2 - 1
    assert sp.expand(2 * third - fourth) == -1

    # On the other branch, f^2=-1/2.  Reduce all 288 exact equations in the
    # quotient Q[a,b,c,d,e,f,g]/(2*f^2+1).  The constant polynomial lies in
    # their rational linear span; RREF also returns an explicit certificate.
    reduced_rows = []
    row_words = []
    monomials = set()
    for polynomial, representative in unique.items():
        reduced = reduce_f_square(polynomial)
        reduced_rows.append(reduced)
        row_words.append(representative)
        monomials.update(reduced)
    monomials = tuple(sorted(monomials))
    monomial_index = {
        monomial: index for index, monomial in enumerate(monomials)
    }
    rows = [[0] * len(monomials) for _ in reduced_rows]
    for row, polynomial in zip(rows, reduced_rows):
        for monomial, coefficient in polynomial.items():
            row[monomial_index[monomial]] = str(coefficient)
    matrix = fmpq_mat(rows)
    assert (matrix.nrows(), matrix.ncols(), matrix.rank()) == (288, 190, 172)

    constant = [0] * len(monomials)
    constant[monomial_index[(0,) * len(equivariant.PARAMS)]] = 1
    assert fmpq_mat(rows + [constant]).rank() == 172

    # Recover and verify one concrete coefficient vector.  Free variables in
    # the transposed system are set to zero by reading its RREF.
    augmented_transpose = [
        list(column) + [rhs]
        for column, rhs in zip(zip(*rows), constant)
    ]
    rref, rank = fmpq_mat(augmented_transpose).rref()
    assert rank == 172
    multipliers = [Fraction() for _ in reduced_rows]
    for row_number in range(rref.nrows()):
        pivot = next(
            (
                column
                for column in range(len(reduced_rows))
                if rref[row_number, column]
            ),
            None,
        )
        if pivot is None:
            assert not rref[row_number, len(reduced_rows)]
            continue
        multipliers[pivot] = Fraction(
            str(rref[row_number, len(reduced_rows)])
        )
    assert sum(bool(value) for value in multipliers) == 165
    for column in range(len(monomials)):
        value = sum(
            multiplier * Fraction(str(rows[row][column]))
            for row, multiplier in enumerate(multipliers)
        )
        assert value == constant[column]


def main():
    audit_matching_sectors()
    audit_equivariant_obstruction()
    print(
        "PASS: sectors=9/72/24, shore compatibility=30/48/3, "
        "edge-cylinder rank=51/54, equivariant branches=elementary/RREF165"
    )


if __name__ == "__main__":
    main()
