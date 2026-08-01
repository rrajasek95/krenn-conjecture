#!/usr/bin/env python3
"""Exact certificate for the minimal M2+M0+M1 response frontier."""

from __future__ import annotations

from itertools import product

import sympy as sp

from explore_live_three_zero_minimal_three_extra_response import (
    select_labels,
    symbolic_determinant,
)


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


LABELS_01 = (
    ((0, 0, 0, 0, 2, 1, 0), 0, 0),
    ((0, 0, 0, 2, 0, 1, 0), 0, 0),
    ((0, 0, 2, 0, 0, 1, 0), 0, 0),
    ((0, 0, 0, 1, 0, 1, 0), 1, 2),
    ((0, 0, 1, 0, 0, 1, 0), 1, 2),
    ((0, 1, 0, 0, 0, 1, 0), 1, 2),
    ((0, 1, 1, 1, 0, 1, 0), 0, 0),
    ((1, 0, 0, 0, 0, 1, 0), 1, 2),
    ((1, 0, 1, 1, 0, 1, 0), 0, 0),
    ((1, 1, 0, 1, 0, 1, 0), 0, 0),
    ((1, 1, 1, 0, 0, 1, 0), 0, 0),
    ((0, 0, 1, 1, 0, 1, 0), 1, 1),
    ((0, 0, 1, 1, 1, 2, 2), 0, 0),
    ((0, 2, 0, 1, 0, 1, 2), 1, 1),
    ((0, 2, 0, 1, 0, 2, 0), 1, 1),
    ((0, 2, 0, 1, 1, 1, 0), 1, 1),
    ((0, 2, 0, 1, 1, 2, 2), 0, 0),
    ((0, 2, 1, 1, 0, 2, 2), 0, 0),
    ((2, 0, 0, 1, 0, 1, 2), 1, 1),
)


def main() -> None:
    a, b, c, d, e, f = sp.symbols("a b c d e f")
    g = a * c + a * e + c * e
    q = g + 3 * a + 3 * c + 3 * e + 6
    expected = (
        -(2**37) * (3**10)
        * a**7 * b * c**8 * d * e**7 * f * (d - f)
        * g**2 * q**4
    )
    determinant = symbolic_determinant(("01", "01", "01"), LABELS_01)
    require(
        sp.expand(determinant - expected) == 0,
        "sp.expand(determinant - expected) == 0",
    )

    # Each of the 27 row-reduced kernel-chart products has generic full
    # rank.  This is an exact finite audit, not the missing uniform
    # no-common-zero proof on its exceptional parameter divisors.
    for charts in product(("01", "12", "02"), repeat=3):
        require(
            len(select_labels(charts, (2, 3, 5, 7, 11, 13))) == 19,
            "len(select_labels(charts, (2, 3, 5, 7, 11, 13))) == 19",
        )

    print("minimal three-extra complete response frontier: PASS")
    print("central 01^3 maximal-minor factorization: exact")
    print("all 27 row-plane chart products generically rank 19")


if __name__ == "__main__":
    main()
