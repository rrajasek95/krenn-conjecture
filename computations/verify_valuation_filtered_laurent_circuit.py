#!/usr/bin/env python3
"""Audit the filtered Laurent circuit and its sharp tropical boundary.

The universal valuation lemma is proved in the accompanying note.  This
script checks its two finite inputs:

* the 31-cell plateau has an odd dependency among three exact binomials;
* the two-edge-star tropical point has six minima in every coefficient and
  nevertheless has a globally minimum, odd-coefficient monomial in the
  saved degree-nine integral residual.
"""

from __future__ import annotations

import gzip
import pickle
from itertools import product
from pathlib import Path

import verify_valuation_rainbow_descent_cycle as base
import verify_valuation_rainbow_plateau_completion as plateau


HERE = Path(__file__).resolve().parent
NEGATIVE_PAIRS = {(0, 1), (0, 2)}


def star_valuation(occurrence):
    u, v, _a, _b = occurrence
    return -1 if (u, v) in NEGATIVE_PAIRS else 0


def decode_row(code):
    valid_edges = tuple(
        (left, right)
        for left in range(18)
        for right in range(left + 1, 18)
        if left // 3 != right // 3
    )
    answer = []
    while code:
        low = code & -code
        edge_index = low.bit_length() - 1
        code ^= low
        left, right = valid_edges[edge_index]
        answer.append((left // 3, right // 3, left % 3, right % 3))
    return frozenset(answer)


def audit_plateau_circuit():
    entries = plateau.completed_entries()
    differences = []
    for coloring in plateau.LAURENT_COLORINGS:
        terms = tuple(
            network for network, _value in plateau.fibre_terms(entries, coloring)
        )
        assert len(terms) == 2  # The valuation gap is therefore infinite.
        differences.append(plateau.exponent_difference(entries, terms))

    assert tuple(
        differences[0][index] + differences[1][index]
        for index in range(len(entries))
    ) == differences[2]


def audit_star_boundary():
    # All 729 coefficient fibres have exactly six minimum terms.  At the
    # all-ones residue point their initial sums are 6=0 in characteristic 2.
    for coloring in product(base.COLORS, repeat=base.N):
        valuations = []
        for matching in base.perfect_matchings():
            valuations.append(
                sum(
                    star_valuation((u, v, coloring[u], coloring[v]))
                    for u, v in matching
                )
            )
        minimum = min(valuations)
        assert minimum == -1
        assert sum(value == minimum for value in valuations) == 6

    with (HERE / "degree9_source_ideal_char2_h27.pkl").open("rb") as stream:
        parity = pickle.load(stream)
    with gzip.open(
        HERE / "degree9_char2_first_integral_residual.pkl.gz", "rb"
    ) as stream:
        residual = pickle.load(stream)["coefficients"]

    row_valuations = []
    for code in parity["row_codes"]:
        row_valuations.append(sum(map(star_valuation, decode_row(code))))

    residual_minimum = min(
        value for value, coefficient in zip(row_valuations, residual) if coefficient
    )
    assert residual_minimum == -3

    row = 1589
    gamma = decode_row(parity["row_codes"][row])
    expected = frozenset(
        {
            (0, 2, 0, 2),
            (0, 2, 1, 1),
            (0, 1, 2, 2),
            (1, 2, 0, 0),
            (1, 5, 1, 1),
            (3, 5, 0, 2),
            (3, 4, 1, 2),
            (3, 4, 2, 1),
            (4, 5, 0, 0),
        }
    )
    assert gamma == expected
    assert residual[row] == -1
    assert sum(map(star_valuation, gamma)) == residual_minimum

    stubs = []
    for u, v, a, b in gamma:
        stubs.extend(((u, a), (v, b)))
    assert sorted(stubs) == [
        (vertex, color) for vertex in range(base.N) for color in base.COLORS
    ]

    # The lower bound -3 is structural: every negative occurrence meets
    # vertex zero, and a rainbow network has only its three color stubs.
    assert sum((u == 0 or v == 0) for u, v, _a, _b in gamma) == 3


def main():
    audit_plateau_circuit()
    audit_star_boundary()
    print(
        "verified filtered Laurent obstruction: the 31-cell plateau has "
        "an odd exact-binomial circuit d3=d1+d2"
    )
    print(
        "verified sharp boundary: all 729 star initial forms have six "
        "minima, while residual row 1589 has odd coefficient -1 and "
        "globally minimum rainbow valuation -3"
    )


if __name__ == "__main__":
    main()
