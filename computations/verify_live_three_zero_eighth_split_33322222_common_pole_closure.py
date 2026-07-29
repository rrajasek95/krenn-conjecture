#!/usr/bin/env python3
"""Exact audit of the eighth-split ``(3^3,2^5)`` closure."""

from __future__ import annotations

import sympy as sp


def check_profile_and_selections() -> None:
    h, p, k = 8, 9, 1
    multiplicities = (3, 3, 3) + (2,) * 5
    assert sum(multiplicities) == p + h + 2 == 19

    for partial in range(3):
        takes = [0] * len(multiplicities)
        for triple in range(3):
            takes[triple] = 2 if triple == partial else 3
        complement = tuple(m - take for m, take in zip(multiplicities, takes))
        assert sum(takes) == h
        assert sum(complement) == p + 2 == 11
        assert complement[partial] == 1
        assert complement[3:] == (2,) * 5
        assert sum(take > 0 for take in takes) == 3

        denominator_degree = (k + 1) + sum(
            take + 1 for take in takes if take
        )
        numerator_cap = p + 3 - 1
        assert denominator_degree == 13
        assert numerator_cap == 11 == sum(complement)
        assert denominator_degree - numerator_cap == 2


def check_role_difference() -> None:
    x, y, mu = sp.symbols("x y mu", nonzero=True)

    def delta(r: int, value: sp.Expr) -> sp.Expr:
        return r / (value + mu) - (r + 1) / (value - mu)

    full_minus_partial = sp.factor(delta(3, x) - delta(2, x))
    expected = -2 * mu / (x**2 - mu**2)
    assert sp.factor(full_minus_partial - expected) == 0

    difference = sp.factor(
        (delta(3, x) - delta(2, x))
        - (delta(3, y) - delta(2, y))
    )
    expected_difference = sp.factor(
        2 * mu * (x - y) * (x + y)
        / ((x**2 - mu**2) * (y**2 - mu**2))
    )
    assert sp.factor(difference - expected_difference) == 0

    # With nonzero mu and structural denominators, equality of role
    # differences forces (x-y)(x+y)=0, both structurally forbidden.
    cleared = sp.factor(
        difference * (x**2 - mu**2) * (y**2 - mu**2)
    )
    assert cleared == 2 * mu * (x - y) * (x + y)


def main() -> None:
    check_profile_and_selections()
    check_role_difference()
    print("eighth-split (3^3,2^5) common-pole role-swap closure: PASS")
    print("three legal 3+3+2 selections and constant residual: exact")
    print("Delta_3-Delta_2=-2mu/(x^2-mu^2): exact")
    print("mu nonzero reduces equal roles to forbidden equal/opposite values")


if __name__ == "__main__":
    main()
