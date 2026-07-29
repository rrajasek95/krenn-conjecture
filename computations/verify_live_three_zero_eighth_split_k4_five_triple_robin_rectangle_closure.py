#!/usr/bin/env python3
"""Exact audit of the h=8,k=4 profile 3^5 2^2 1^3 closure."""

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


def main() -> None:
    h, k, p, total = 8, 4, 12, 22
    profile = (3,) * 5 + (2,) * 2 + (1,) * 3
    assert sum(profile) == total == p + h + 2

    triples = tuple(range(5))
    doubles = (5, 6)
    core_count = 0
    for selected_triples in combinations(triples, 3):
        chosen_tuple = doubles + selected_triples
        chosen = set(chosen_tuple)
        assert len(chosen) == 5
        for partial_tuple in combinations(chosen_tuple, 2):
            partial = set(partial_tuple)
            takes = {
                index: (1 if index in partial else 2)
                for index in chosen
            }
            assert sum(takes.values()) == h
            assert frontier.leaves_singleton(profile, takes)
            core_complement = tuple(
                multiplicity - takes.get(index, 0)
                for index, multiplicity in enumerate(profile)
            )
            assert sum(core_complement) == p + 2 == 14
            core_count += 1

        formal_complement = tuple(
            multiplicity - (2 if index in chosen else 0)
            for index, multiplicity in enumerate(profile)
            if multiplicity - (2 if index in chosen else 0) > 0
        )
        assert sum(formal_complement) == k + 8 == 12
        assert sorted(formal_complement) == [1] * 6 + [3] * 2
        assert len(formal_complement) == 8
        assert formal_complement.count(1) == 6
        assert len(formal_complement) - 4 == 4
        assert 2 * 4 - 2 == 6
    assert core_count == sp.binomial(5, 3) * sp.binomial(5, 2) == 100

    # Derive the exact derivative exponents from g/A^2.
    z, mu, u, v = sp.symbols("z mu u v")
    singleton_values = sp.symbols("r0:3")
    selected_values = sp.symbols("s0:3")
    formal_doubles = sp.symbols("delta0:2")
    L = sp.prod(z - value for value in singleton_values)
    U = sp.prod(z - value for value in selected_values)
    Q = sp.prod(
        z + value for value in formal_doubles + selected_values
    )
    A = L * U * (z - u) ** 3 * (z - v) ** 3
    gcd_factor = (z - u) ** 2 * (z - v) ** 2
    derivative_factor = sp.cancel(gcd_factor * Q**2 / A**2)
    expected_factor = sp.cancel(
        Q**2 / (L**2 * U**2 * (z - u) ** 4 * (z - v) ** 4)
    )
    assert sp.cancel(derivative_factor - expected_factor) == 0

    # Universal quartic Wronskian, accessory polynomial, and ODE.
    f_coeffs = sp.symbols("f0:5")
    g_coeffs = sp.symbols("g0:5")
    f = sum(f_coeffs[index] * z**index for index in range(5))
    g = sum(g_coeffs[index] * z**index for index in range(5))
    W = sp.expand(f * sp.diff(g, z) - sp.diff(f, z) * g)
    accessory = sp.expand(
        sp.diff(f, z) * sp.diff(g, z, 2)
        - sp.diff(f, z, 2) * sp.diff(g, z)
    )
    assert sp.Poly(W, z).degree() <= 6
    assert sp.Poly(accessory, z).degree() <= 4
    for solution in (f, g):
        ode = sp.expand(
            W * sp.diff(solution, z, 2)
            - sp.diff(W, z) * sp.diff(solution, z)
            + accessory * solution
        )
        assert ode == 0

    # If V(x_i)=-W'(x_i)Y_i at six simple roots, its interpolation has
    # z^5 coefficient -sum(Y_i).  Thus deg(V)<=4 forces the Robin sum.
    nodes = sp.symbols("x0:6")
    robin_coefficients = sp.symbols("Y0:6")
    node_W = sp.prod(z - node for node in nodes)
    interpolant = -sum(
        robin_coefficients[index]
        * sp.prod(z - nodes[j] for j in range(6) if j != index)
        for index in range(6)
    )
    assert sp.Poly(interpolant, z).coeff_monomial(z**5) == -sum(
        robin_coefficients
    )
    assert sp.limit(z * interpolant / node_W, z, sp.oo) == -sum(
        robin_coefficients
    )

    # Compute the complete Robin sum for a selected triple set, including
    # all nuisance parameters, then take one generic four-point rectangle.
    a, b, c, d, e = sp.symbols("a b c d e")
    triple_values = (a, b, c, d, e)
    r_values = sp.symbols("rho0:3")
    delta, epsilon = sp.symbols("delta epsilon")

    def robin_sum(selected):
        selected = tuple(selected)
        outside = tuple(
            value for value in triple_values if value not in selected
        )
        simple_roots = r_values + selected
        total_robin = 0
        for root in simple_roots:
            total_robin += 4 / (root + mu)
            total_robin += 2 / (root + delta) + 2 / (root + epsilon)
            total_robin += 2 * sum(1 / (root + value) for value in selected)
            total_robin -= 2 * sum(
                1 / (root - other)
                for other in simple_roots
                if other != root
            )
            total_robin -= 4 * sum(
                1 / (root - value) for value in outside
            )
        return total_robin

    rectangle = sp.factor(
        sp.cancel(
            robin_sum((e, a, c))
            - robin_sum((e, a, d))
            - robin_sum((e, b, c))
            + robin_sum((e, b, d))
        )
    )
    expected_rectangle = sp.factor(
        4
        * (a - b)
        * (c - d)
        * (a + b + c + d)
        / ((a + c) * (a + d) * (b + c) * (b + d))
    )
    assert sp.cancel(rectangle - expected_rectangle) == 0

    # All five four-subset sums being zero forces any two triple values
    # to coincide.
    total_triples = sum(triple_values)
    four_sums = tuple(total_triples - value for value in triple_values)
    for left, right in combinations(range(5), 2):
        assert sp.expand(four_sums[left] - four_sums[right]) == (
            triple_values[right] - triple_values[left]
        )

    counts, residuals = frontier.census(h, p)
    assert counts["R"] == 46
    assert profile in residuals

    print("PASS: exact h=8,k=4 profile 3^5 2^2 1^3 closure")
    print("100 legal formal-five cores and ten saturated quartic pencils")
    print("accessory residue sum gives the exact five-triple rectangle")


if __name__ == "__main__":
    main()
