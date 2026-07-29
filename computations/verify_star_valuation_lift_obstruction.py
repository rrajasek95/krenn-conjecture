#!/usr/bin/env python3
"""Exclude the all-ones residue lift of the two-edge star valuation over Q_2.

Edges 01 and 02 have valuation -1 in every color cell; all other cells have
valuation zero.  The generator initial forms vanish at the all-ones residue
point, but the equations modulo 4 have an exact rank-one inconsistency.
"""

from __future__ import annotations

import itertools
import sys

sys.path.insert(0, str(__file__).rsplit("/", 1)[0])

from test_diagonal_power2 import EDGE_INDEX, PM


N = 6
Q = 3
VARIABLES = 15 * Q * Q
NEGATIVE_EDGES = {(0, 1), (0, 2)}


def variable_index(u, v, a, b):
    return EDGE_INDEX[u, v] * Q * Q + a * Q + b


def linearized_row(coloring):
    """Return the mod-2 row obtained from 2 F_c modulo 4."""
    mask = 0
    for matching in PM:
        if not any(edge in NEGATIVE_EDGES for edge in matching):
            continue
        for u, v in matching:
            mask ^= 1 << variable_index(u, v, coloring[u], coloring[v])
    target = int(len(set(coloring)) == 1)
    return mask, target


def rank(rows, augmented):
    pivots = {}
    for mask, target in rows:
        value = mask | ((target if augmented else 0) << VARIABLES)
        while value:
            pivot = (value & -value).bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = value
                break
            value ^= pivots[pivot]
    return len(pivots)


def main():
    colorings = tuple(itertools.product(range(Q), repeat=N))
    rows = tuple(linearized_row(coloring) for coloring in colorings)
    assert rank(rows, False) == 45
    assert rank(rows, True) == 46

    # A four-equation certificate: vary the last two colors in a 2-by-2
    # rectangle while the first four vertices have color zero.
    witness_colorings = (
        (0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 1),
        (0, 0, 0, 0, 1, 0),
        (0, 0, 0, 0, 1, 1),
    )
    mask = 0
    target = 0
    for coloring in witness_colorings:
        row, rhs = linearized_row(coloring)
        mask ^= row
        target ^= rhs
    assert mask == 0 and target == 1
    print("verified Q_2 lift obstruction: rank 45/46")
    print(f"four-coloring witness={witness_colorings}")


if __name__ == "__main__":
    main()
