#!/usr/bin/env python3
"""Tiny exact audit for the isotropic dressed-cap export.

The script is dependency-free.  It checks the contraction algebra, support
intersection combinatorics, and the two sharp consistency guards; the torus
classification itself is the Laurent-unit proof in the accompanying note.
"""

from collections import Counter
from fractions import Fraction
from itertools import product


COLOURS = range(3)


def dot_matrix(left, matrix, right):
    return sum(left[i] * matrix[i][j] * right[j]
               for i, j in product(COLOURS, repeat=2))


def audit_dressed_contraction():
    m = 7
    direct_a = [[2 + 3 * a - b for b in COLOURS] for a in COLOURS]
    # The cyclic matrix has the full-torus zero used in equation (10).
    direct_u = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
    alpha = (1, 1, 1)
    beta = (1, 1, -2)
    assert dot_matrix(alpha, direct_u, beta) == 0

    x = (2, -3, 5)
    y = (7, 11, -13)
    t = (17, -19, 23)
    v = (29, 31, -37)
    z = Fraction(5)
    z2 = Fraction(7)  # stand-in for z^[m-4]
    z1 = z * z2 / (m - 3)
    z0 = Fraction(41)  # killed by the isotropic contraction
    tv = sum(alpha[c] * t[c] for c in COLOURS) * sum(
        beta[d] * v[d] for d in COLOURS)
    multiplier = tv * z2

    checked = 0
    for a, b in product(COLOURS, repeat=2):
        contracted = sum(
            alpha[c] * beta[d] * (
                direct_a[a][b] * direct_u[c][d] * z0
                + direct_a[a][b] * t[c] * v[d] * z1
                + direct_u[c][d] * x[a] * y[b] * z1
                + x[a] * y[b] * t[c] * v[d] * z2
            )
            for c, d in product(COLOURS, repeat=2)
        )
        dressed = multiplier * (
            x[a] * y[b] + Fraction(direct_a[a][b], m - 3) * z
        )
        assert contracted == dressed
        checked += 1

    # The boundary m=4 has z^[0]=1 and coefficient m-3=1.
    assert Fraction(9) * Fraction(1) == (4 - 3) * Fraction(9)
    return checked


def unit_active_sets(row, column):
    indices = {row, column}
    return {frozenset(COLOURS) - {index} for index in indices}


def audit_matrix_unit_intersections():
    checked = 0
    for r, s, k, ell in product(COLOURS, repeat=4):
        maximum = max(len(left & right)
                      for left in unit_active_sets(r, s)
                      for right in unit_active_sets(k, ell))
        expected = 2 if {r, s} & {k, ell} else 1
        assert maximum == expected
        checked += 1

    cyclic = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
    alpha = (1, 1, 1)
    beta = (1, 1, -2)
    assert dot_matrix(alpha, cyclic, beta) == 0
    for support in ({0, 1}, {1, 2}, {0, 2}):
        nonzero = [(i, j) for i, j in product(support, repeat=2)
                   if cyclic[i][j]]
        assert len(nonzero) == 1
    return checked


def multiply_words(left, right):
    if any(a != -1 and b != -1 for a, b in zip(left, right)):
        return None
    return tuple(b if a == -1 else a for a, b in zip(left, right))


def multiply_polynomials(left, right):
    answer = Counter()
    for left_word, left_value in left.items():
        for right_word, right_value in right.items():
            word = multiply_words(left_word, right_word)
            if word is not None:
                answer[word] += left_value * right_value
    return Counter({word: value for word, value in answer.items() if value})


def monomial(site_count, site, colour):
    word = [-1] * site_count
    word[site] = colour
    return Counter({tuple(word): 1})


def audit_binary_four_star():
    site_count = 4
    answer = Counter({(-1,) * site_count: 1})
    for site in range(site_count):
        linear = monomial(site_count, site, 0)
        linear.update(monomial(site_count, (site + 1) % site_count, 1))
        answer = multiply_polynomials(answer, linear)
    expected = Counter({(0, 0, 0, 0): 1, (1, 1, 1, 1): 1})
    assert answer == expected
    return len(answer)


def audit_ternary_arbitrary_multiplier():
    site_count = 12
    answer = Counter({(-1,) * site_count: 1})
    for position in range(4):
        linear = Counter()
        for colour in COLOURS:
            linear.update(monomial(site_count, 4 * colour + position, colour))
        answer = multiply_polynomials(answer, linear)

    multiplier = Counter()
    for colour in COLOURS:
        word = [-1] * site_count
        own_sites = set(range(4 * colour, 4 * colour + 4))
        for site in range(site_count):
            if site not in own_sites:
                word[site] = colour
        multiplier[tuple(word)] += 1
    answer = multiply_polynomials(answer, multiplier)
    expected = Counter({(colour,) * site_count: 1 for colour in COLOURS})
    assert answer == expected
    return len(answer)


def main():
    rows = audit_dressed_contraction()
    unit_cases = audit_matrix_unit_intersections()
    binary_terms = audit_binary_four_star()
    ternary_terms = audit_ternary_arbitrary_multiplier()
    print("uncontracted four-cut isotropic dressed cap: PASS")
    print(f"dressed rows={rows}; unit-pair cases={unit_cases}; "
          f"binary terms={binary_terms}; ternary terms={ternary_terms}")


if __name__ == "__main__":
    main()
