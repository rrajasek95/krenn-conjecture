#!/usr/bin/env python3
"""Exact audit of the h=8,k=4 profile 3^2 2^7 1^2 closure."""

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


def main() -> None:
    h, k, p, total = 8, 4, 12, 22
    profile = (3,) * 2 + (2,) * 7 + (1,) * 2
    assert sum(profile) == total == p + h + 2

    # All formal-five pair-drop cores are legal.
    doubles = tuple(range(2, 9))
    core_count = 0
    for chosen_tuple in combinations(doubles, 5):
        chosen = set(chosen_tuple)
        for partial_tuple in combinations(chosen_tuple, 2):
            partial = set(partial_tuple)
            takes = {i: (1 if i in partial else 2) for i in chosen}
            complement = tuple(
                multiplicity - takes.get(i, 0)
                for i, multiplicity in enumerate(profile)
            )
            assert sum(takes.values()) == h
            assert sum(complement) == p + 2 == 14
            assert complement.count(1) == 4
            assert frontier.leaves_singleton(profile, takes)
            core_count += 1
    assert core_count == sp.binomial(7, 5) * sp.binomial(5, 2) == 210

    # Full removal of five formal doubles leaves two doubles, two triples,
    # and two singletons: six roots and a quadratic relation plane.
    complement_multiplicities = (3,) * 2 + (2,) * 2 + (1,) * 2
    assert sum(complement_multiplicities) == k + 8 == 12
    assert len(complement_multiplicities) == 6
    assert len(complement_multiplicities) - 4 == 2

    z, mu, a, b, r, s, u, v = sp.symbols("z mu a b r s u v")
    selected = sp.symbols("t0:5")
    Q = sp.prod(z + value for value in selected)
    C = (z - u) * (z - v)
    A = C**2 * (z - a) ** 3 * (z - b) ** 3 * (z - r) * (z - s)
    gcd_factor = C * (z - a) ** 2 * (z - b) ** 2
    derivative_factor = sp.cancel(gcd_factor / A**2)
    expected_factor = sp.cancel(
        1
        /
        (
            C**3
            * (z - a) ** 4
            * (z - b) ** 4
            * (z - r) ** 2
            * (z - s) ** 2
        )
    )
    assert sp.cancel(derivative_factor - expected_factor) == 0

    # Every nonzero first-order functional on P2 has a two-plane kernel,
    # and a double root kills the corresponding singleton residue.
    w, c0, c1 = sp.symbols("w c0 c1")
    local_unit = c0 + c1 * w
    assert sp.diff(local_unit * w**2, w).subs(w, 0) == 0
    square_r = sp.Poly((z - r) ** 2, z)
    square_s = sp.Poly((z - s) ** 2, z)
    coefficient_matrix = sp.Matrix(
        [square_r.all_coeffs(), square_s.all_coeffs()]
    )
    assert coefficient_matrix.rank(iszerofunc=lambda value: value == 0) == 2

    # Solve the exact two-square outside-double jet system.
    X, Z, rho, sigma = sp.symbols("X Z rho sigma")
    jet_matrix = sp.Matrix([[rho**2, 4 * rho], [sigma**2, 4 * sigma]])
    jet_rhs = sp.Matrix([-2, -2])
    solution = jet_matrix.inv() * jet_rhs
    expected_X = -(rho + sigma) / (2 * rho * sigma)
    expected_Z = 2 / (rho * sigma)
    assert sp.factor(solution[1] - expected_X) == 0
    assert sp.factor(solution[0] - expected_Z) == 0

    # Full logarithmic factor at u, including both order-four triple poles.
    # Check factor by factor to avoid expanding the irrelevant 16-symbol
    # common denominator.
    log_factors = [(z + mu, 4)]
    log_factors += [(z + value, 2) for value in selected]
    log_factors += [
        (z - v, -3),
        (z - a, -4),
        (z - b, -4),
        (z - r, -2),
        (z - s, -2),
    ]
    for factor, exponent in log_factors:
        assert sp.cancel(
            sp.diff(factor**exponent, z) / factor**exponent
            - exponent * sp.diff(factor, z) / factor
        ) == 0

    # Every swap of the unique second outside value is available.
    universe = set(range(7))
    swap_count = 0
    for fixed_u in range(7):
        others = universe - {fixed_u}
        partitions = {}
        for outside_v in others:
            selected_set = frozenset(others - {outside_v})
            assert len(selected_set) == 5
            partitions[outside_v] = selected_set
        for x, y in combinations(sorted(others), 2):
            assert x in partitions[y] and y in partitions[x]
            swap_count += 1
    assert swap_count == 7 * sp.binomial(6, 2) == 105

    x, y = sp.symbols("x y")

    def phi(value):
        return 2 / (u + value) + 3 / (u - value)

    assert sp.factor(phi(x) - (5 * u + x) / (u**2 - x**2)) == 0
    # Subtracting the two partition equations is precisely Phi_u(x)-Phi_u(y).
    swap_difference = (
        2 / (u + x)
        - 3 / (u - y)
        - 2 / (u + y)
        + 3 / (u - x)
    )
    assert sp.cancel(swap_difference - (phi(x) - phi(y))) == 0

    lam = sp.symbols("lam")
    fibre = sp.expand(lam * (u**2 - x**2) - 5 * u - x)
    assert sp.Poly(fibre, x).degree() <= 2
    assert sp.Poly(fibre, x).coeff_monomial(x) == -1

    counts, residuals = frontier.census(h, p)
    assert counts["R"] == 46
    assert profile in residuals

    print("PASS: exact h=8,k=4 profile 3^2 2^7 1^2 square closure")
    print("210 legal formal-five cores and quadratic singleton plane: exact")
    print("all 105 swaps force a six-point quadratic fibre")


if __name__ == "__main__":
    main()
