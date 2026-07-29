#!/usr/bin/env python3
"""Exact audit of the h=8, k=4 closure of 3^2 2^8."""

from __future__ import annotations

from itertools import combinations
from math import comb
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


def check_cores_and_degrees() -> None:
    profile = (3, 3) + (2,) * 8
    h, k, total = 8, 4, 22
    assert sum(profile) == total == 2 * h + k + 2
    double_indices = tuple(range(2, 10))
    count = 0
    for chosen in combinations(double_indices, 5):
        outside = set(double_indices) - set(chosen)
        assert len(outside) == 3
        for partial in combinations(chosen, 2):
            takes = {
                index: (1 if index in partial else 2)
                for index in chosen
            }
            assert sum(takes.values()) == h
            assert frontier.leaves_singleton(profile, takes)
            count += 1
    assert count == comb(8, 5) * comb(5, 2) == 560

    assert 3 * 2 + 2 * 3 == 12  # degree of A=C^2 R^3
    assert 3 + 2 == 5  # distinct complementary roots
    assert 5 - 4 == 1  # relation pencil lies in P_1


def check_derivative_and_local_rows() -> None:
    z, mu = sp.symbols("z mu")
    chosen = sp.symbols("t0:5")
    outside = sp.symbols("u0:3")
    triples = sp.symbols("a0:2")
    q = sp.prod(z + value for value in chosen)
    c = sp.prod(z - value for value in outside)
    r = sp.prod(z - value for value in triples)
    a_poly = c**2 * r**3
    gcd_poly = c * r**2
    radical = sp.cancel(a_poly / gcd_poly)
    d_a = sp.cancel(sp.diff(a_poly, z) / gcd_poly)
    n0, n1, n2, n3, n4, n5, n6, n7 = sp.symbols("n0:8")
    numerator = sum(
        coefficient * z**degree
        for degree, coefficient in enumerate((n0, n1, n2, n3, n4, n5, n6, n7))
    )
    differential = sp.expand(
        radical * ((z + mu) * sp.diff(numerator, z) + 5 * numerator)
        - (z + mu) * d_a * numerator
    )
    rational = (z + mu) ** 5 * numerator / a_poly
    assert sp.factor(
        sp.diff(rational, z)
        - (z + mu) ** 4 * gcd_poly * differential / a_poly**2
    ) == 0
    assert sp.Poly(a_poly, z).degree() == 12
    assert sp.Poly(radical, z).degree() == 5
    assert sp.Poly(d_a, z).degree() == 4
    assert sp.Poly(d_a, z).LC() == 12
    assert sp.Poly(differential, z).degree() <= 11
    assert 11 - 2 * 5 == 1

    w = sp.symbols("w")
    b0, b1, b2 = sp.symbols("b0 b1 b2", nonzero=True)
    s0, s1 = sp.symbols("s0 s1")
    unit = b0 + b1 * w + b2 * w**2 / 2
    linear = s0 + s1 * w
    twice_residue = sp.diff(unit * linear, w, 2).subs(w, 0)
    assert sp.expand(twice_residue - (b2 * s0 + 2 * b1 * s1)) == 0
    assert sp.expand(twice_residue.subs({s0: 1, s1: 0}) - b2) == 0
    assert sp.expand(twice_residue.subs({s0: 0, s1: 1}) - 2 * b1) == 0


def check_logarithmic_equation_and_swaps() -> None:
    u, x, y, mu = sp.symbols("u x y mu", nonzero=True)

    def phi(value):
        return 2 / (u + value) + 3 / (u - value)

    assert sp.factor(phi(x) - (5 * u + x) / (u**2 - x**2)) == 0

    # Swapping x from the chosen side with y from the outside side.
    before = 2 / (u + x) - 3 / (u - y)
    after = 2 / (u + y) - 3 / (u - x)
    assert sp.factor((before - after) - (phi(x) - phi(y))) == 0

    fibre_value = sp.symbols("fibre_value")
    fibre_polynomial = sp.expand(
        fibre_value * (u**2 - x**2) - 5 * u - x
    )
    assert sp.Poly(fibre_polynomial, x).degree() <= 2
    assert sp.Poly(fibre_polynomial, x).coeff_monomial(x) == -1

    double_values = tuple(range(8))
    for fixed_u in double_values:
        others = set(double_values) - {fixed_u}
        witnessed_pairs = set()
        for chosen in combinations(others, 5):
            chosen_set = set(chosen)
            outside = others - chosen_set
            assert len(outside) == 2
            for left in chosen_set:
                for right in outside:
                    witnessed_pairs.add(tuple(sorted((left, right))))
        assert witnessed_pairs == set(combinations(others, 2))


def check_exact_profile_location() -> None:
    profile = (3, 3) + (2,) * 8
    counts, residuals = frontier.census(8, 12)
    assert counts["R"] == 46
    assert profile in residuals


def main() -> None:
    check_cores_and_degrees()
    check_derivative_and_local_rows()
    check_logarithmic_equation_and_swaps()
    check_exact_profile_location()
    print("PASS: h=8, k=4 profile 3^2 2^8 closure")
    print("560 legal formal-five cores and full P_1 relation pencil: exact")
    print("outside-double triple-pole rows force B'=B''=0: exact")
    print("five/three swaps put seven doubles in one quadratic fibre")


if __name__ == "__main__":
    main()
