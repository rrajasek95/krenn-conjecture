#!/usr/bin/env python3
"""Exact selected-state dual obstruction to termwise P^2 straightening."""

from collections import Counter
from fractions import Fraction
from itertools import product


VERTICES = tuple(range(6))
COLORS = tuple(range(3))

P0 = ((0, 4), (1, 2), (3, 5))
P1 = ((0, 5), (1, 4), (2, 3))
P2 = ((0, 3), (1, 5), (2, 4))
SELECTED = (P0, P1, P2)
PRISM = frozenset(edge for matching in SELECTED for edge in matching)


def perfect_matchings(vertices=VERTICES):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        remaining = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remaining):
            yield tuple(sorted(((u, v),) + tail))


PM = tuple(perfect_matchings())


def h(edge):
    return Fraction(-3 if edge == (1, 2) else 1)


def lam(vertex, color):
    return Fraction(-1, 3) if (vertex, color) == (0, 0) else Fraction(1)


def entry(edge, left_color, right_color):
    if edge not in PRISM:
        return Fraction(0)
    u, v = edge
    return h(edge) * lam(u, left_color) * lam(v, right_color)


def term(matching, coloring):
    value = Fraction(1)
    for u, v in matching:
        value *= entry((u, v), coloring[u], coloring[v])
    return value


def decorated_exponents(matching, color):
    return Counter((u, v, color, color) for u, v in matching)


def main():
    assert len(PM) == 15
    supported = tuple(matching for matching in PM if set(matching) <= PRISM)
    assert len(supported) == 4
    assert set(SELECTED) < set(supported)
    assert sorted(product_h(matching) for matching in supported) == [
        Fraction(-3),
        Fraction(1),
        Fraction(1),
        Fraction(1),
    ]

    # The evaluation annihilates every fibre, not just the mixed generators.
    for coloring in product(COLORS, repeat=6):
        assert sum((term(matching, coloring) for matching in PM), Fraction(0)) == 0

    selected_values = []
    for color, matching in enumerate(SELECTED):
        coloring = (color,) * 6
        value = term(matching, coloring)
        assert value == 1
        selected_values.append(value)
        for u, v in matching:
            assert entry((u, v), color, color) != 0
    U = product_fraction(selected_values)
    assert U == 1 and U * U == 1

    # Each squared selected matching monomial has exactly one ordered
    # double-dimer factorization, even among all 15 x 15 matching pairs.
    for color, selected in enumerate(SELECTED):
        target = Counter(
            {occurrence: 2 for occurrence in decorated_exponents(selected, color)}
        )
        factorizations = []
        for left in PM:
            left_exp = decorated_exponents(left, color)
            for right in PM:
                if left_exp + decorated_exponents(right, color) == target:
                    factorizations.append((left, right))
        assert factorizations == [(selected, selected)]

    # P itself vanishes here: this is deliberately not a P^2 nonmembership
    # certificate.
    constant_fibres = []
    for color in COLORS:
        coloring = (color,) * 6
        constant_fibres.append(
            sum((term(matching, coloring) for matching in PM), Fraction(0))
        )
    assert constant_fibres == [0, 0, 0]

    print("double-dimer selected-state counterfunctional: PASS")
    print("all 729 fibre generators evaluate to zero; U=U^2=1")
    print("each selected doubled matching has one ordered factorization")
    print("scope audit: P evaluates to zero, so this does not decide P^2 membership")


def product_h(matching):
    return product_fraction(h(edge) for edge in matching)


def product_fraction(values):
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


if __name__ == "__main__":
    main()
