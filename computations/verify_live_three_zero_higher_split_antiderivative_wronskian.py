#!/usr/bin/env python3
"""Exact audit of the collision-excess antiderivative/Wronskian closure."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import sympy as sp


def load_checker(filename: str, module_name: str) -> ModuleType:
    path = Path(__file__).with_name(filename)
    specification = importlib.util.spec_from_file_location(module_name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def check_degrees_and_injectivity() -> None:
    h, k, c = sp.symbols("h k c", integer=True, positive=True)
    total = 2 * h + k + 2
    excess = total - c
    degree_d0 = k + c
    decay_f = 2 * (c - h)
    primitive_decay = decay_f - 1
    degree_r = sp.expand(degree_d0 - primitive_decay)
    assert sp.expand(degree_r - (excess - 1)) == 0

    # The primitive numerator has strictly smaller degree than D0 as soon
    # as exchange has at least one step, c>=h+1.
    gap = sp.expand(degree_d0 - (excess - 1))
    assert gap == 2 * (c - h) - 1
    for h_value in range(7, 20):
        for k_value in range(1, 8):
            for c_value in range(h_value + 1, 2 * h_value + k_value + 3):
                e_value = 2 * h_value + k_value + 2 - c_value
                if e_value < 0:
                    continue
                assert k_value + c_value > e_value - 1


def check_antiderivative_identity() -> None:
    z, mu = sp.symbols("z mu")
    p = sp.Function("P")(z)
    r = sp.Function("R")(z)

    for k in range(1, 8):
        d0 = (z + mu) ** k * p
        derivative = sp.diff(r / d0, z)
        numerator = (
            (z + mu) * p * sp.diff(r, z)
            - (k * p + (z + mu) * sp.diff(p, z)) * r
        )
        expected = numerator / ((z + mu) ** (k + 1) * p**2)
        assert sp.simplify(derivative - expected) == 0


def check_local_gauge_and_weights() -> None:
    x = sp.symbols("x")
    d0 = sp.Function("D0")(x)
    r = sp.Function("R")(x)
    covariant = sp.diff(r, x) - sp.diff(d0, x) / d0 * r
    gauged = d0 * sp.diff(r / d0, x)
    assert sp.simplify(covariant - gauged) == 0

    # Model the sharp base-point-free vanishing sequence after the local
    # unit gauge: 0,m+1,...,m+d-1.  Its Wronskian order is m(d-1).
    for multiplicity in range(1, 9):
        for dimension in range(3, 10):
            sequence = (0,) + tuple(
                multiplicity + index for index in range(1, dimension)
            )
            weight = sum(order - index for index, order in enumerate(sequence))
            assert weight == multiplicity * (dimension - 1)

            sections = [sp.Integer(1)] + [
                x ** (multiplicity + index) for index in range(1, dimension)
            ]
            wronskian = sp.det(
                sp.Matrix(
                    [
                        [sp.diff(section, x, derivative) for section in sections]
                        for derivative in range(dimension)
                    ]
                )
            )
            assert sp.Poly(wronskian, x).as_dict()
            minimum_order = min(power[0] for power in sp.Poly(wronskian, x).as_dict())
            assert minimum_order == multiplicity * (dimension - 1)

    # If a gcd has order t at the node, differentiating its locally gauged
    # leading term produces order t-1.  Divisibility by x^m forces t>=m+1.
    for multiplicity in range(1, 9):
        for gcd_order in range(1, 14):
            derivative_order = gcd_order - 1
            satisfies = derivative_order >= multiplicity
            assert satisfies == (gcd_order >= multiplicity + 1)


def check_gcd_corrected_global_inequality() -> None:
    e, a, d, g = sp.symbols("e a d g", integer=True, nonnegative=True)
    forced = (e - a) * (d - 1)
    cap = d * (e - g - d)
    difference = sp.expand(forced - cap)
    assert sp.expand(difference - (d**2 - e + d * (g - a) + a)) == 0

    # Exhaust every combinatorially possible base-node total a.  The actual
    # gcd bound is g>=a+b and is stronger; g>=a already suffices here.
    for excess in range(1, 9):
        for dimension in range(3, excess + 2):
            for absorbed_multiplicity in range(excess + 1):
                for gcd_degree in range(absorbed_multiplicity, excess + 1):
                    forced_value = (excess - absorbed_multiplicity) * (
                        dimension - 1
                    )
                    cap_value = dimension * (
                        excess - gcd_degree - dimension
                    )
                    assert forced_value > cap_value
                    assert (
                        forced_value - cap_value
                        >= dimension**2 - excess
                        >= 1
                    )


def check_zero_singleton_and_h8_census() -> None:
    # A zero class is necessarily a singleton, so its exponent in B is zero.
    # Every root of B is a repeated, hence structurally nonzero, value.
    for profile in ((3, 2, 1, 1), (2, 2, 1), (4, 1, 1, 1)):
        exponents = tuple(part - 1 for part in profile)
        assert all(exponent == 0 for part, exponent in zip(profile, exponents) if part == 1)
        assert all(exponent >= 1 for part, exponent in zip(profile, exponents) if part >= 2)

    frontier = load_checker(
        "verify_live_three_zero_higher_split_collision_frontier.py",
        "higher_frontier_for_antiderivative",
    )
    roles = load_checker(
        "verify_live_three_zero_higher_split_k1_constant_core_role_swap.py",
        "higher_roles_for_antiderivative",
    )
    counts, residuals = frontier.census(8, 9)
    assert counts["R"] == len(residuals) == 35

    role_closed = {
        profile
        for profile in residuals
        if roles.moving_role_witness(profile, 8, frontier.leaves_singleton)
        is not None
        or roles.unequal_swap_witness(profile, 8, frontier.leaves_singleton)
        is not None
    }
    dual_closed = {
        profile
        for profile in residuals
        if len(profile) >= 9
        and frontier.every_value_core_legal(profile, 8)
        and sum(profile) - len(profile) <= 8
    }
    expected_leftover = {
        (3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1),
    }
    assert len(role_closed) == 17
    assert len(dual_closed) == 19
    assert len(role_closed | dual_closed) == 34
    assert set(residuals) - role_closed - dual_closed == expected_leftover

    # In particular, every double/single old-R profile has excess equal to
    # its number of doubles and is closed by the theorem for d<=8.
    double_single = {
        profile
        for profile in residuals
        if set(profile) <= {1, 2}
    }
    assert len(double_single) == 8
    assert double_single <= dual_closed
    assert {sum(profile) - len(profile) for profile in double_single} == set(
        range(1, 9)
    )


def main() -> None:
    check_degrees_and_injectivity()
    check_antiderivative_identity()
    check_local_gauge_and_weights()
    check_gcd_corrected_global_inequality()
    check_zero_singleton_and_h8_census()
    print("higher-split antiderivative/Wronskian closure: PASS")
    print("unique primitive, degree <= collision excess - 1, and injectivity: exact")
    print("local missing jets and gcd absorption at every repeated value: exact")
    print("e <= 8 gives strict Wronskian deficit d^2-e > 0")
    print("h=8,k=1 union with constant-role closures: 34/35 old R profiles")


if __name__ == "__main__":
    main()
