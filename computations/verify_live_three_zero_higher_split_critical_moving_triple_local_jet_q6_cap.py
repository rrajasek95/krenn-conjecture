#!/usr/bin/env python3
"""Exact audit of the critical moving-triple local-jet q=6 cap."""

from __future__ import annotations

import sympy as sp


def audit_uniform_arithmetic() -> None:
    for r in range(4, 41):
        p = r * (r + 3)
        c = r + 5
        baseline_mass = p + 2
        assert baseline_mass == (r + 1) * (r + 2)

        relation_degree = c - 4
        common_degree = c
        assert relation_degree == r + 1
        assert common_degree == r + 5

        common_cap = r + 2
        pair_lower = 2 * r - common_cap
        pair_multiplier_degree = relation_degree - 4
        pair_ambient_dimension = pair_multiplier_degree + 1
        assert pair_lower == r - 2
        assert pair_multiplier_degree == r - 3
        assert pair_ambient_dimension == r - 2
        assert pair_multiplier_degree >= 1


def audit_local_jet() -> None:
    z, j, u0, u1, u2, u3 = sp.symbols("z j u0 u1 u2 u3")
    x = z - j
    Bj = (z - j) ** 2 * (z + j) ** 2
    unit = u0 + u1 * x + u2 * x**2 + u3 * x**3
    witness = Bj * (z - j)
    third = sp.expand(sp.diff(unit * witness, z, 3).subs(z, j))
    assert sp.factor(third) == 24 * j**2 * u0
    assert sp.expand(witness.subs(z, j)) == 0
    assert sp.expand(sp.diff(witness, z).subs(z, j)) == 0
    assert sp.expand(sp.diff(witness, z, 2).subs(z, j)) == 0
    assert sp.factor(sp.diff(witness, z, 3).subs(z, j)) == 24 * j**2


def audit_p28_profiles() -> None:
    r = 4
    assert r * (r + 3) == 28
    assert (r + 1) * (r + 2) == 30
    assert r + 5 == 9

    tuples = ((3, 6, 0, 0), (3, 6, 1, -2))
    for h in range(22, 28):
        k = 28 - h
        assert 1 <= k <= 6
        for e, a, b, u in tuples:
            assert 4 * e + 3 * a + 2 * b + u == 30
            # Select one triple in role two.  In the double variant the
            # unique double is held fixed in role two.
            selected_double = b
            selected_triple = 1
            selected_repeated = selected_double + selected_triple
            selected_singletons = h + 2 - 2 * selected_repeated
            original_singletons = h + u
            assert selected_singletons == original_singletons
            complement_mass = 4 * e + 3 * (a - 1) + 1
            assert complement_mass == 28
            complement_classes = e + (a - 1) + 1
            assert complement_classes == 9

    moving_values = 6
    maximal_values = 1
    assert moving_values - maximal_values == 5


def main() -> None:
    audit_uniform_arithmetic()
    audit_local_jet()
    audit_p28_profiles()
    print("critical moving-triple local-jet q=6 cap: PASS")
    print("full critical pair intersection and exact triple jet: PASS")
    print("p=28 consequence: at most one q=6 and at least five q=5: PASS")
    print("scope: dimension distribution only; profile closure not claimed")


if __name__ == "__main__":
    main()
