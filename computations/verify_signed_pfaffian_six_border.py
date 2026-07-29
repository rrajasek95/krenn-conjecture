#!/usr/bin/env python3
"""Exact audit of the signed six-site Pfaffian border family.

Each nonzero matrix cell is stored as ``(integer coefficient, t exponent)``.
The script enumerates all 15 perfect matchings and all 3^6 transverse
colorings.  No floating point arithmetic or Pfaffian library is used.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import product


N = 6
Q = 3


def perfect_matchings(vertices=tuple(range(N))):
    """Yield matchings in the recursive order used by the Pfaffian."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def crossing_sign(matching):
    """Return (-1)^(number of crossing pairs of matching arcs)."""
    crossings = sum(
        a < c < b < d or c < a < d < b
        for index, (a, b) in enumerate(matching)
        for c, d in matching[index + 1 :]
    )
    return -1 if crossings % 2 else 1


MATCHINGS = tuple(perfect_matchings())
assert len(MATCHINGS) == 15

# A cell key is (left vertex, right vertex, left color, right color).
# The value coeff*t**exponent is a Laurent monomial.
CELLS = {
    # Color 0: 01|23|45, with product t*t^(-1)*1 = 1.
    (0, 1, 0, 0): (1, 1),
    (2, 3, 0, 0): (1, -1),
    (4, 5, 0, 0): (1, 0),
    # Color 1: 02|14|35.
    (0, 2, 1, 1): (1, 0),
    (1, 4, 1, 1): (1, 0),
    (3, 5, 1, 1): (1, 0),
    # Color 2: 03|15|24.
    (0, 3, 2, 2): (1, 0),
    (1, 5, 2, 2): (1, 0),
    (2, 4, 2, 2): (1, 0),
}


def transverse_coefficient(coloring):
    """Return a Laurent polynomial as exponent -> integer coefficient."""
    answer = defaultdict(int)
    for matching in MATCHINGS:
        coefficient = crossing_sign(matching)
        exponent = 0
        for u, v in matching:
            cell = CELLS.get((u, v, coloring[u], coloring[v]))
            if cell is None:
                break
            scalar, valuation = cell
            coefficient *= scalar
            exponent += valuation
        else:
            answer[exponent] += coefficient
    return {exponent: value for exponent, value in answer.items() if value}


expected = {
    (0, 0, 0, 0, 0, 0): {0: 1},
    (1, 1, 1, 1, 1, 1): {0: 1},
    (2, 2, 2, 2, 2, 2): {0: 1},
    (0, 0, 2, 1, 2, 1): {1: -1},
}

observed = {}
for coloring in product(range(Q), repeat=N):
    coefficient = transverse_coefficient(coloring)
    if coefficient:
        observed[coloring] = coefficient

assert observed == expected

# Audit the four supporting matchings and their canonical Pfaffian signs.
supporting = {}
for coloring in expected:
    terms = []
    for matching in MATCHINGS:
        if all(
            (u, v, coloring[u], coloring[v]) in CELLS
            for u, v in matching
        ):
            terms.append((matching, crossing_sign(matching)))
    supporting[coloring] = terms

assert supporting[(0, 0, 0, 0, 0, 0)] == [
    (((0, 1), (2, 3), (4, 5)), 1)
]
assert supporting[(1, 1, 1, 1, 1, 1)] == [
    (((0, 2), (1, 4), (3, 5)), 1)
]
assert supporting[(2, 2, 2, 2, 2, 2)] == [
    (((0, 3), (1, 5), (2, 4)), 1)
]
assert supporting[(0, 0, 2, 1, 2, 1)] == [
    (((0, 1), (2, 4), (3, 5)), -1)
]

print("verified all 729 transverse coefficients")
print("Pf(K(t)) = Delta_(6,3) - t*e_0e_0e_2e_1e_2e_1")
print("the three uniform Pfaffian signs are +1; the defect sign is -1")
