#!/usr/bin/env python3
"""Clean-room audit of the fixed-q eight-site pair-cap obstruction.

This checker does not import the discovery checker.  It expands powers by
repeated multiplication in the site-square-zero algebra, constructs every
top-coordinate linear form of ps*q^[3], and checks the final Gram system
with SymPy over QQ rather than Singular.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from math import factorial

import sympy as sp


SITE_COUNT = 8
COLOURS = range(3)
EMPTY = -1
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Fraction]
Mode = tuple[int, int]

# Literal unit cells of the fixed quadratic.  This is deliberately not
# reconstructed from the discovery checker's constants or helper routines.
Q_CELLS = (
    (2, 3, 0),
    (4, 5, 0),
    (6, 7, 0),
    (0, 1, 1),
    (3, 6, 1),
    (5, 7, 1),
    (0, 2, 2),
    (1, 4, 2),
    (5, 6, 2),
)

# A dot is an unoccupied site.  These are all nineteen expected monomials
# of q^[3], listed independently and compared with the algebra expansion.
EXPECTED_Q3_WORDS = (
    "..000000",
    "110000..",
    "1100..00",
    ".2002.00",
    "1100.1.1",
    "1100.22.",
    ".20021.1",
    ".200222.",
    "11..0000",
    "2.2.0000",
    "11.1001.",
    "2.21001.",
    "222.2.00",
    "11.1.111",
    "2.21.111",
    ".2.12111",
    "22212.1.",
    "222.21.1",
    "222.222.",
)


def partial_word(text: str) -> Monomial:
    assert len(text) == SITE_COUNT
    return tuple(EMPTY if value == "." else int(value) for value in text)


def cell_monomial(left: int, right: int, colour: int) -> Monomial:
    assert 0 <= left < right < SITE_COUNT and colour in COLOURS
    result = [EMPTY] * SITE_COUNT
    result[left] = result[right] = colour
    return tuple(result)


def merge(left: Monomial, right: Monomial) -> Monomial | None:
    result = []
    for left_value, right_value in zip(left, right):
        if left_value != EMPTY and right_value != EMPTY:
            return None
        result.append(right_value if left_value == EMPTY else left_value)
    return tuple(result)


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: defaultdict[Monomial, Fraction] = defaultdict(Fraction)
    for left_word, left_coefficient in left.items():
        for right_word, right_coefficient in right.items():
            word = merge(left_word, right_word)
            if word is not None:
                result[word] += left_coefficient * right_coefficient
    return {word: coefficient for word, coefficient in result.items() if coefficient}


def scale(poly: Polynomial, scalar: Fraction | int) -> Polynomial:
    scalar = Fraction(scalar)
    return {word: scalar * coefficient for word, coefficient in poly.items()}


def power(poly: Polynomial, exponent: int) -> Polynomial:
    unit = (EMPTY,) * SITE_COUNT
    result: Polynomial = {unit: Fraction(1)}
    for _ in range(exponent):
        result = multiply(result, poly)
    return result


def divided_power(poly: Polynomial, exponent: int) -> Polynomial:
    raw = power(poly, exponent)
    divisor = factorial(exponent)
    return {word: coefficient / divisor for word, coefficient in raw.items()}


def q_polynomial() -> Polynomial:
    return {
        cell_monomial(left, right, colour): Fraction(1)
        for left, right, colour in Q_CELLS
    }


def pair_basis_word(left: Mode, right: Mode) -> Monomial:
    (left_site, left_colour), (right_site, right_colour) = left, right
    assert left_site < right_site
    result = [EMPTY] * SITE_COUNT
    result[left_site] = left_colour
    result[right_site] = right_colour
    return tuple(result)


def ps_coordinate_forms(q3: Polynomial):
    """Return every coefficient form of ps*q^[3] in abstract R entries."""
    forms: defaultdict[Monomial, Counter[tuple[Mode, Mode]]] = defaultdict(Counter)
    for left_site, right_site in combinations(range(SITE_COUNT), 2):
        for left_colour, right_colour in product(COLOURS, repeat=2):
            left = (left_site, left_colour)
            right = (right_site, right_colour)
            pair_word = pair_basis_word(left, right)
            for q3_word, coefficient in q3.items():
                full_word = merge(pair_word, q3_word)
                if full_word is not None:
                    assert coefficient.denominator == 1
                    forms[full_word][(left, right)] += int(coefficient)
    return dict(forms)


def beta(left, right):
    return left[0] * right[1] + left[1] * right[0]


def exact_gram_inconsistency() -> None:
    symbols = sp.symbols(
        "pA sA pB sB pC sC pD sD pE sE pF sF"
    )
    vectors = {
        name: symbols[2 * index:2 * index + 2]
        for index, name in enumerate("ABCDEF")
    }
    A, B, C, D, E, F = (vectors[name] for name in "ABCDEF")
    equations = (
        4 * beta(A, B) - 1,
        4 * beta(C, D) - 1,
        4 * beta(E, F) - 1,
        beta(A, F),
        beta(B, F),
        beta(A, C),
        beta(C, F),
    )

    # The form has matrix [[0,1],[1,0]] and is nondegenerate over QQ/C.
    form_matrix = sp.Matrix(((0, 1), (1, 0)))
    assert form_matrix.det() == -1

    # Independent characteristic-zero elimination (the discovery checker
    # uses Singular; this clean-room audit uses SymPy's exact QQ engine).
    basis = sp.groebner(equations, *symbols, order="grevlex", domain=sp.QQ)
    assert len(basis.polys) == 1
    assert basis.polys[0].as_expr() == 1


def main() -> None:
    q = q_polynomial()
    assert len(q) == 9
    assert all(coefficient == 1 for coefficient in q.values())

    raw_q3 = power(q, 3)
    q3 = divided_power(q, 3)
    expected_q3 = {partial_word(word): Fraction(1) for word in EXPECTED_Q3_WORDS}
    assert raw_q3 == scale(expected_q3, factorial(3))
    assert q3 == expected_q3

    raw_q4 = power(q, 4)
    q4 = divided_power(q, 4)
    expected_q4 = {
        tuple(map(int, "11000000")): Fraction(1),
        tuple(map(int, "22212111")): Fraction(1),
    }
    assert raw_q4 == scale(expected_q4, factorial(4))
    assert q4 == expected_q4

    # This is the exact factor four: q*q^[3] = q^4/3! = 4*q^[4].
    assert multiply(q, q3) == scale(q4, 4)
    assert factorial(4) // factorial(3) == 4

    forms = ps_coordinate_forms(q3)
    assert len(forms) == 165
    assert sum(sum(form.values()) for form in forms.values()) == 171
    assert Counter(sum(form.values()) for form in forms.values()) == {1: 163, 4: 2}
    assert all(coefficient == 1 for form in forms.values() for coefficient in form.values())

    A, B = (0, 0), (1, 0)
    C, D = (2, 1), (4, 1)
    E, F = (3, 2), (7, 2)
    selected = {
        (0,) * 8: ((A, B), Fraction(1, 4)),
        (1,) * 8: ((C, D), Fraction(1, 4)),
        (2,) * 8: ((E, F), Fraction(1, 4)),
        (0, 2, 0, 0, 2, 2, 2, 2): ((A, F), Fraction(0)),
        (2, 0, 2, 1, 0, 0, 1, 2): ((B, F), Fraction(0)),
        (0, 2, 1, 1, 2, 1, 1, 1): ((A, C), Fraction(0)),
        (1, 1, 1, 1, 0, 0, 1, 2): ((C, F), Fraction(0)),
    }
    delta = {(colour,) * SITE_COUNT: Fraction(1) for colour in COLOURS}
    for word, (entry, forced_value) in selected.items():
        assert forms[word] == Counter({entry: 1})
        assert q4.get(word, Fraction(0)) == 0
        # Dividing (a*q+4ps)q^[3]=Delta by four gives
        # a*q^[4]+ps*q^[3]=Delta/4 on every coordinate.
        assert delta.get(word, Fraction(0)) / 4 == forced_value

    exact_gram_inconsistency()

    print("independent fixed-q eight-site pair-cap audit: PASS")
    print("repeated algebra multiplication gives all 19 q^[3] terms: PASS")
    print("repeated algebra multiplication gives both q^[4] terms: PASS")
    print("q*q^[3] = 4*q^[4] and Delta/4 rescaling: PASS")
    print("171 incidences on 165 words (163 singleton, two fourfold): PASS")
    print("seven singleton coordinates and absence of a*q^[4]: PASS")
    print("independent SymPy QQ Gram ideal is [1]: PASS")


if __name__ == "__main__":
    main()
