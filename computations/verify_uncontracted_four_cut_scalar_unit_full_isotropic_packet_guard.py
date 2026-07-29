#!/usr/bin/env python3
"""Tiny exact audit for the scalar-unit full-isotropic-packet guard.

The script is dependency-free.  It works in the six-site square-zero
algebra and keeps alpha_i beta_j as formal bilinear coefficient labels.
"""

from collections import Counter
from fractions import Fraction
from itertools import product


COLOURS = range(3)
SITES = range(6)
EMPTY_WORD = (-1,) * 6


def clean(polynomial):
    return Counter({
        word: Fraction(value)
        for word, value in polynomial.items()
        if value
    })


def add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return clean(answer)


def scale(polynomial, scalar):
    return clean(Counter({
        word: Fraction(scalar) * value
        for word, value in polynomial.items()
    }))


def multiply(left, right):
    answer = Counter()
    for left_word, left_value in left.items():
        for right_word, right_value in right.items():
            if any(a >= 0 and b >= 0
                   for a, b in zip(left_word, right_word)):
                continue
            word = tuple(b if a < 0 else a
                         for a, b in zip(left_word, right_word))
            answer[word] += left_value * right_value
    return clean(answer)


def monomer(site, colour, coefficient=1):
    word = [-1] * 6
    word[site] = colour
    return Counter({tuple(word): Fraction(coefficient)})


def cell(left, right, colour):
    return multiply(monomer(left, colour), monomer(right, colour))


def pure(colour):
    return Counter({(colour,) * 6: Fraction(1)})


def formal_clean(polynomial):
    return {
        key: clean(value)
        for key, value in polynomial.items()
        if clean(value)
    }


def formal_multiply(formal, polynomial):
    return formal_clean({
        key: multiply(value, polynomial)
        for key, value in formal.items()
    })


def formal_subtract(left, right):
    answer = {key: value.copy() for key, value in left.items()}
    for key, polynomial in right.items():
        answer[key] = add(answer.get(key, Counter()), scale(polynomial, -1))
    return formal_clean(answer)


def isotropic_restriction(formal, alpha_two_zero):
    if alpha_two_zero:
        return formal_clean({
            key: value for key, value in formal.items() if key[0] != 2
        })
    return formal_clean({
        key: value for key, value in formal.items() if key[1] != 2
    })


def evaluate_formal(formal, alpha, beta):
    answer = Counter()
    for (left, right), polynomial in formal.items():
        answer.update(scale(polynomial, alpha[left] * beta[right]))
    return clean(answer)


def packet_difference(formal_f, z, xs, ys, direct_a, a, b):
    dressed = add(
        multiply(xs[a], ys[b]),
        scale(z, Fraction(direct_a[a][b], 2)),
    )
    left = formal_multiply(formal_f, dressed)
    right = {(a, a): pure(a)} if a == b else {}
    return formal_subtract(left, right)


def support(linear):
    return {
        site
        for word in linear
        for site, colour in enumerate(word)
        if colour >= 0
    }


def flatten_linear(linear):
    vector = [Fraction(0)] * 18
    for word, coefficient in linear.items():
        occupied = [(site, colour) for site, colour in enumerate(word)
                    if colour >= 0]
        assert len(occupied) == 1
        site, colour = occupied[0]
        vector[3 * site + colour] += coefficient
    return vector


def rational_rank(vectors):
    matrix = [list(vector) for vector in vectors]
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(rank, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                left - factor * right
                for left, right in zip(matrix[row], matrix[rank])
            ]
        rank += 1
    return rank


def build_guard():
    z = add(cell(2, 3, 0), cell(0, 4, 1))
    t = (monomer(0, 0), monomer(1, 1), Counter())
    v = (monomer(1, 0), monomer(2, 1), Counter())
    x = (monomer(4, 0), monomer(5, 1), Counter())
    y = (monomer(5, 0), monomer(3, 1), Counter())

    formal_f = {}
    for left, right in product(COLOURS, repeat=2):
        component = multiply(multiply(t[left], v[right]), z)
        if component:
            formal_f[left, right] = component
    return z, t, v, x, y, formal_clean(formal_f)


def padded_rows(x, y):
    padded_x = []
    padded_y = []
    for colour in COLOURS:
        k = add(
            monomer(0, colour),
            monomer(1, colour),
            monomer(2, colour),
        )
        ell = add(
            monomer(0, colour),
            monomer(1, colour, 2),
            monomer(2, colour, 4),
        )
        padded_x.append(add(x[colour], k))
        padded_y.append(add(y[colour], ell))
    return tuple(padded_x), tuple(padded_y)


def audit_guard():
    z, t, v, basic_x, basic_y, formal_f = build_guard()

    z_squared = scale(multiply(z, z), Fraction(1, 2))
    expected_z_squared = multiply(cell(2, 3, 0), cell(0, 4, 1))
    assert z_squared == expected_z_squared
    assert z_squared

    expected_f = {
        (0, 0): Counter({
            (0, 0, 0, 0, -1, -1): Fraction(1)
        }),
        (1, 1): Counter({
            (1, 1, 1, -1, 1, -1): Fraction(1)
        }),
    }
    assert formal_f == expected_f
    assert not formal_multiply(formal_f, z)

    # U=E_22 has contraction alpha_2 beta_2.
    direct_u = [[0] * 3 for _ in COLOURS]
    direct_u[2][2] = 1
    for alpha, beta in (
        ((1, 2, 0), (3, 5, 7)),
        ((1, 2, 3), (3, 5, 0)),
        ((1, 2, 3), (3, 5, 7)),
    ):
        contraction = sum(
            alpha[i] * direct_u[i][j] * beta[j]
            for i, j in product(COLOURS, repeat=2)
        )
        assert contraction == alpha[2] * beta[2]

    padded_x, padded_y = padded_rows(basic_x, basic_y)
    direct_blocks = (
        ((2, -3, 5), (7, 11, -13), (17, -19, 23)),
        ((0, 1, 0), (-2, 0, 4), (5, 6, 7)),
    )

    checked_rows = 0
    for xs, ys in ((basic_x, basic_y), (padded_x, padded_y)):
        for direct_a in direct_blocks:
            for a, b in product(COLOURS, repeat=2):
                difference = packet_difference(
                    formal_f, z, xs, ys, direct_a, a, b
                )
                expected = (
                    {(2, 2): scale(pure(2), -1)}
                    if (a, b) == (2, 2) else {}
                )
                assert difference == expected
                assert not isotropic_restriction(
                    difference, alpha_two_zero=True
                )
                assert not isotropic_restriction(
                    difference, alpha_two_zero=False
                )
                checked_rows += 1

    # The sole residual in the formal non-isotropic continuation of the
    # nine packet equations evaluates to -X_2.  This is not a check of the
    # full non-isotropic 81-row contraction.
    blind = packet_difference(
        formal_f, z, padded_x, padded_y, direct_blocks[0], 2, 2
    )
    assert evaluate_formal(blind, (1, 1, 1), (1, 1, 1)) == scale(
        pure(2), -1
    )

    # Padding is killed before either open row can affect the packet.
    for a, b in product(COLOURS, repeat=2):
        assert formal_multiply(
            formal_f, multiply(padded_x[a], padded_y[b])
        ) == formal_multiply(
            formal_f, multiply(basic_x[a], basic_y[b])
        )

    assert min(len(support(row)) for row in padded_x) >= 3
    assert min(len(support(row)) for row in padded_y) >= 3
    assert rational_rank([flatten_linear(row) for row in padded_x]) == 3
    assert rational_rank([flatten_linear(row) for row in padded_y]) == 3
    for colour in COLOURS:
        diagonal = multiply(padded_x[colour], padded_y[colour])
        assert diagonal
        core_word = [-1] * 6
        core_word[0] = colour
        core_word[1] = colour
        assert diagonal[tuple(core_word)] == 3

    return (
        len(z_squared),
        len(formal_f),
        checked_rows,
        min(len(support(row)) for row in padded_x + padded_y),
    )


def main():
    z_terms, channels, rows, minimum_support = audit_guard()
    print(
        "scalar-unit full-isotropic packet guard: PASS; "
        f"z^[2] terms={z_terms}; F channels={channels}; "
        f"packet rows={rows}; padded minimum support={minimum_support}; "
        "blind row=(2,2)"
    )


if __name__ == "__main__":
    main()
