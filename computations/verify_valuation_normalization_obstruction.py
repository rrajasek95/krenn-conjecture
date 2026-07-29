#!/usr/bin/env python3
"""Exact audits for the 2-adic gauge-normalization obstruction.

Part 1 is an actual one-color n=6 solution H=1 over Q for which no local
diagonal gauge of determinant one can make all nonzero edges 2-integral.
Part 2 is a q=3 valuation vector satisfying every tropical coefficient
condition, with an F_2 solution of every initial form, but failing the same
gauge LP.  Part 2 is not asserted to lift to an exact q=3 solution.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product


N = 6
Q = 3


def perfect_matchings(vertices=tuple(range(N))):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for i, v in enumerate(vertices[1:], 1):
        rest = vertices[1:i] + vertices[i + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


PM = tuple(perfect_matchings())


def valuation_2(x):
    assert x
    numerator = abs(x.numerator)
    denominator = x.denominator
    value = 0
    while numerator % 2 == 0:
        numerator //= 2
        value += 1
    while denominator % 2 == 0:
        denominator //= 2
        value -= 1
    return value


def actual_q1_obstruction():
    matchings = (
        ((0, 1), (2, 3), (4, 5)),
        ((0, 2), (1, 3), (4, 5)),
        ((0, 5), (1, 2), (3, 4)),
    )
    weights = {
        (0, 1): Fraction(1, 2),
        (2, 3): Fraction(1),
        (4, 5): Fraction(1),
        (0, 2): Fraction(-1, 2),
        (1, 3): Fraction(1),
        (0, 5): Fraction(1),
        (1, 2): Fraction(1),
        (3, 4): Fraction(1),
    }
    supported = tuple(pm for pm in PM if all(edge in weights for edge in pm))
    assert supported == matchings
    terms = tuple(
        product_value
        for pm in supported
        for product_value in (
            weights[pm[0]] * weights[pm[1]] * weights[pm[2]],
        )
    )
    assert terms == (Fraction(1, 2), Fraction(-1, 2), Fraction(1))
    assert sum(terms) == 1

    # Projective properness does not preserve affine nonvanishing.  Scaling
    # every source edge by 2 gives a primitive integral representative, but
    # its reduction has only the adjacent edges 01 and 02 and hence no
    # perfect matching.  The characteristic-zero output has merely acquired
    # the common factor 2^(N/2)=8.
    integral_weights = {edge: 2 * value for edge, value in weights.items()}
    assert all(value.denominator == 1 for value in integral_weights.values())
    assert any(abs(value.numerator) % 2 for value in integral_weights.values())
    residue_support = {
        edge for edge, value in integral_weights.items() if value.numerator % 2
    }
    assert residue_support == {(0, 1), (0, 2)}
    assert not any(all(edge in residue_support for edge in pm) for pm in PM)
    scaled_terms = tuple(
        integral_weights[pm[0]]
        * integral_weights[pm[1]]
        * integral_weights[pm[2]]
        for pm in supported
    )
    assert sum(scaled_terms) == 8

    # The sum of the three perfect-matching incidence vectors is 3-regular.
    degrees = [0] * N
    total_valuation = 0
    for pm in matchings:
        for u, v in pm:
            degrees[u] += 1
            degrees[v] += 1
            total_valuation += valuation_2(weights[u, v])
    assert degrees == [3] * N
    assert total_valuation == -2
    print(
        "verified actual q=1 obstruction: H=1, dual valuation=-2; "
        "primitive projective reduction has H=0"
    )


def tropical_q3_obstruction():
    # Every cell on the two edges 01 and 02 has valuation -1; every cell on
    # every other underlying edge has valuation zero.
    def entry_valuation(u, v, _a, _b):
        return -1 if (u, v) in ((0, 1), (0, 2)) else 0

    # For every coloring, exactly the six matchings pairing vertex 0 with 1
    # or 2 have minimum valuation -1.  With all initial residues equal to one,
    # each initial coefficient is therefore 6=0 in characteristic two.
    for coloring in product(range(Q), repeat=N):
        term_values = []
        for pm in PM:
            term_values.append(
                sum(entry_valuation(u, v, coloring[u], coloring[v]) for u, v in pm)
            )
        minimum = min(term_values)
        minimizers = sum(value == minimum for value in term_values)
        assert minimum == -1 and minimizers == 6
        assert minimizers % 2 == 0

    # A color-zero dual certificate is the sum of these three matchings.
    dual_matchings = (
        ((0, 1), (2, 3), (4, 5)),
        ((0, 2), (1, 4), (3, 5)),
        ((0, 3), (1, 5), (2, 4)),
    )
    degrees = [0] * N
    total_valuation = 0
    for pm in dual_matchings:
        for u, v in pm:
            degrees[u] += 1
            degrees[v] += 1
            total_valuation += entry_valuation(u, v, 0, 0)
    assert degrees == [3] * N
    assert total_valuation == -2
    print(
        "verified q=3 tropical/initial-form obstruction: "
        "729 initial forms vanish over F_2, dual valuation=-2"
    )


if __name__ == "__main__":
    actual_q1_obstruction()
    tropical_q3_obstruction()
