#!/usr/bin/env python3
"""Exact audit of the h=8,k=5 profile 3^3 2^7 closure."""

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier
import verify_live_three_zero_eighth_split_all_order_formal_five_layer_duality as formal_five


PROFILE = (3,) * 3 + (2,) * 7
z, mu = sp.symbols("z mu")


def check_formal_choices_and_cores() -> None:
    assert sum(PROFILE) == 23
    double_indices = tuple(range(3, 10))
    choice_count = core_count = 0
    for chosen in combinations(double_indices, 5):
        choice_count += 1
        for lowered in combinations(chosen, 2):
            takes = {i: (1 if i in lowered else 2) for i in chosen}
            complement = tuple(
                sorted(
                    (
                        multiplicity - takes.get(i, 0)
                        for i, multiplicity in enumerate(PROFILE)
                        if multiplicity - takes.get(i, 0) > 0
                    ),
                    reverse=True,
                )
            )
            assert sum(takes.values()) == 8
            assert frontier.leaves_singleton(PROFILE, takes)
            assert complement == (3,) * 3 + (2,) * 2 + (1,) * 2
            assert complement.count(1) == 2
            core_count += 1

        full_complement = tuple(
            sorted(
                (
                    multiplicity - (2 if i in chosen else 0)
                    for i, multiplicity in enumerate(PROFILE)
                    if multiplicity - (2 if i in chosen else 0) > 0
                ),
                reverse=True,
            )
        )
        assert full_complement == (3,) * 3 + (2,) * 2
        assert len(full_complement) == 5
        assert len(full_complement) - 4 == 1
    assert choice_count == sp.binomial(7, 5) == 21
    assert core_count == 21 * 10 == 210

    # Re-run the shared exact theorem audit used to obtain the injective
    # two-dimensional relation pencil.
    formal_five.check_uniform_algebra()


def check_exact_derivative() -> None:
    selected = sp.symbols("t0:5")
    outside = sp.symbols("u0:2")
    triples = sp.symbols("a0:3")
    Q = sp.prod(z + t for t in selected)
    C = sp.prod(z - u for u in outside)
    T = sp.prod(z - a for a in triples)
    A = C**2 * T**3
    g = C * T**2
    S = sp.symbols("s0") + sp.symbols("s1") * z
    claimed = sp.cancel(
        (z + mu) ** 5 * Q**2 * S / (C**3 * T**4)
    )
    from_differential = sp.cancel(
        (z + mu) ** 5 * g * Q**2 * S / A**2
    )
    assert sp.cancel(claimed - from_differential) == 0
    assert sp.degree(A, z) == 13
    assert sp.degree(C * T, z) == 5
    assert sp.degree(Q**2, z) == 10

    B0, B1 = sp.symbols("B0 B1", nonzero=True)
    w = sp.symbols("w")
    assert sp.diff((B0 + B1 * w) * w, w, 2).subs(w, 0) == 2 * B1


def check_swaps_and_fibre() -> None:
    indices = tuple(range(7))
    witness_count = 0
    for fixed in indices:
        others = tuple(i for i in indices if i != fixed)
        for x in others:
            for y in others:
                if x == y:
                    continue
                old_selected = set(indices) - {fixed, y}
                new_selected = set(indices) - {fixed, x}
                assert len(old_selected) == len(new_selected) == 5
                assert x in old_selected and y not in old_selected
                assert y in new_selected and x not in new_selected
                assert old_selected & new_selected == set(indices) - {
                    fixed,
                    x,
                    y,
                }
                witness_count += 1
    assert witness_count == 7 * 6 * 5 == 210

    u, x, y = sp.symbols("u x y")
    phi = lambda value: 2 / (u + value) + 3 / (u - value)
    old_new_difference = sp.factor(
        (2 / (u + y) - 3 / (u - x))
        - (2 / (u + x) - 3 / (u - y))
    )
    assert sp.factor(old_new_difference - (phi(y) - phi(x))) == 0
    assert sp.factor(phi(x) - (5 * u + x) / (u**2 - x**2)) == 0

    lam, t = sp.symbols("lam t")
    fibre = sp.Poly(lam * (u**2 - t**2) - 5 * u - t, t)
    assert fibre.degree() <= 2
    assert fibre.coeff_monomial(t) == -1
    assert 6 > 2


def check_census_membership() -> None:
    counts, residuals = frontier.census(8, 13)
    assert counts["R"] == 44
    assert PROFILE in residuals


def main() -> None:
    check_formal_choices_and_cores()
    check_exact_derivative()
    check_swaps_and_fibre()
    check_census_membership()
    print("k=5 seven-double formal linear plane: PASS")
    print("formal choices / legal cores: 21 / 210")
    print("six distinct doubles cannot lie in one quadratic fibre")


if __name__ == "__main__":
    main()
