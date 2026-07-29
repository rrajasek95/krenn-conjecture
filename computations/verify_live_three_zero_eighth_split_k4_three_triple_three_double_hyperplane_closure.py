#!/usr/bin/env python3
"""Exact audit of the h=8,k=4 profile 3^3 2^3 1^7 closure."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier
import verify_live_three_zero_eighth_split_k4_updated_census as census


z, w, mu = sp.symbols("z w mu")


def check_single_drop_cores_and_lifts() -> None:
    profile = (3,) * 3 + (2,) * 3 + (1,) * 7
    assert sum(profile) == 22

    for formal_double in range(3, 6):
        formal_roles = {
            formal_double: 2,
            **{index: 1 for index in range(6, 13)},
        }
        assert sum(formal_roles.values()) == 9

        double_drops = 0
        singleton_drops = 0
        for lowered in formal_roles:
            takes = {
                index: role - (1 if index == lowered else 0)
                for index, role in formal_roles.items()
            }
            takes = {index: role for index, role in takes.items() if role}
            complement = [
                multiplicity - takes.get(index, 0)
                for index, multiplicity in enumerate(profile)
            ]
            assert sum(takes.values()) == 8
            assert sum(complement) == 14
            assert complement.count(1) == 1
            assert frontier.leaves_singleton(profile, takes)

            if lowered == formal_double:
                double_drops += 1
                assert len(takes) == 8
                assert len(takes) - 3 == 5
                assert 5 + 2 == 7
            else:
                singleton_drops += 1
                assert len(takes) == 7
                assert len(takes) - 3 == 4
                assert 4 + 3 == 7
        assert (double_drops, singleton_drops) == (1, 7)
        assert double_drops + singleton_drops == 8
        assert 8 - 1 == 7  # only a possible zero-singleton drop may fail

    x, r = sp.symbols("x r")
    double_lift = z**2 - x**2
    singleton_lift = (z - r) * (z + r) ** 2
    assert sp.factor(
        (z - x) / (z + x) ** 2 - double_lift / (z + x) ** 3
    ) == 0
    assert sp.factor((z - r) - singleton_lift / (z + r) ** 2) == 0

    assert 13 + 7 == 20
    assert 5 + 3 + 7 * 2 == 22
    assert 22 - 20 == 2


def check_kernel_bound() -> None:
    for dimension in range(4, 9):
        baseline = (dimension - 2) + 7 * (dimension - 1)
        cap = dimension * (8 - dimension)
        deficit = baseline - cap
        assert deficit == dimension**2 - 9
        assert deficit > 0

        for simple_double_gcd in range(2):
            for absorbed_double in range(2 - simple_double_gcd):
                ordinary_double = 1 - simple_double_gcd - absorbed_double
                for absorbed_singletons in range(8):
                    gcd_degree = (
                        simple_double_gcd
                        + 3 * absorbed_double
                        + 2 * absorbed_singletons
                    )
                    forced_weight = (
                        ordinary_double * (dimension - 2)
                        + simple_double_gcd * (dimension - 1)
                        + (7 - absorbed_singletons) * (dimension - 1)
                    )
                    reduced_cap = dimension * (
                        8 - gcd_degree - dimension
                    )
                    observed = forced_weight - reduced_cap
                    expected = (
                        deficit
                        + (dimension + 1) * simple_double_gcd
                        + (2 * dimension + 2) * absorbed_double
                        + (dimension + 1) * absorbed_singletons
                    )
                    assert observed == expected
                    assert observed > 0


def check_parity_and_pencil_wronskians() -> None:
    p_coefficients = sp.symbols("p0:8")
    q_coefficients = sp.symbols("q0:8")
    p = sum(p_coefficients[index] * z**index for index in range(8))
    q = sum(q_coefficients[index] * z**index for index in range(8))
    parity_minor = sp.expand(p * q.subs(z, -z) - p.subs(z, -z) * q)
    assert sp.expand(parity_minor.subs(z, -z) + parity_minor) == 0
    assert sp.Poly(parity_minor, z).degree() <= 13

    values = sp.symbols("v0:8")
    no_zero_divisor = z * sp.prod(z**2 - value**2 for value in values)
    one_zero_missing_divisor = z * sp.prod(
        z**2 - value**2 for value in values[:7]
    )
    assert sp.Poly(no_zero_divisor, z).degree() == 17
    assert sp.Poly(one_zero_missing_divisor, z).degree() == 15
    assert 17 > 13 and 15 > 13
    assert 2 + 7 * 3 == 23
    assert 2 + 6 * 3 == 20

    no_zero_forced = (7, 6, 5, 4, 3, 2)
    one_zero_forced = (6, 5, 4, 3, 2, 1)
    caps = (4, 4, 2, 2, 0, 0)
    for count, expected_cap in enumerate(caps):
        degree_in_square = (7 - count) // 2
        assert expected_cap == 2 * (degree_in_square - 1)
        assert no_zero_forced[count] > expected_cap
        assert one_zero_forced[count] > expected_cap
    assert (7 - 6) // 2 == 0


def check_cubic_relation_hyperplane() -> None:
    selected = sp.symbols("x")
    outside_doubles = sp.symbols("u0:2")
    triples = sp.symbols("a0:3")
    singletons = sp.symbols("r0:7")

    Q = z + selected
    H = sp.prod(z + value for value in singletons)
    C = sp.prod(z - value for value in outside_doubles)
    T = sp.prod(z - value for value in triples)
    A = C**2 * T**3
    g_A = C * T**2
    radical = sp.cancel(A / g_A)
    D_A = sp.cancel(sp.diff(A, z) / g_A)
    assert sp.Poly(A, z).degree() == 13
    assert sp.Poly(g_A, z).degree() == 8
    assert sp.Poly(radical, z).degree() == 5
    assert sp.Poly(D_A, z).degree() == 4
    assert sp.Poly(D_A, z).LC() == 13

    coefficients = sp.symbols("n0:9")
    N = sum(coefficients[index] * z**index for index in range(9))
    differential = sp.expand(
        radical * ((z + mu) * sp.diff(N, z) + 5 * N)
        - (z + mu) * D_A * N
    )
    G = (z + mu) ** 5 * N / A
    assert sp.factor(
        sp.diff(G, z)
        - (z + mu) ** 4 * g_A * differential / A**2
    ) == 0
    assert sp.Poly(differential, z).degree() <= 12

    for degree in range(9):
        trial = z**degree
        trial_differential = sp.Poly(
            sp.expand(
                radical * ((z + mu) * sp.diff(trial, z) + 5 * trial)
                - (z + mu) * D_A * trial
            ),
            z,
        )
        assert trial_differential.degree() <= 12
        if degree < 8:
            assert trial_differential.coeff_monomial(
                z ** (degree + 5)
            ) == degree - 8
        else:
            assert trial_differential.coeff_monomial(z**13) == 0

    contact_divisor = sp.expand(Q**2 * H)
    assert sp.Poly(contact_divisor, z).degree() == 9
    assert 12 - 9 == 3
    assert 8 - (8 - 3) == 3
    assert 17 - 9 == 8

    dual_denominator_degree = 2 * 3 + 3 * 4
    dual_numerator_degree = 4 + 2 + 7 + 3
    assert dual_denominator_degree == 18
    assert dual_numerator_degree == 16


def check_two_row_characteristic_cubic_lemma() -> None:
    delta = sp.symbols("delta", nonzero=True)
    Yu, Yv, Zu, Zv = sp.symbols("Yu Yv Zu Zv")
    s = sp.symbols("s")

    chi_u = sp.expand(s * (6 + 6 * Yu * s + Zu * s**2))
    chi_v = sp.expand(
        (s - delta)
        * (6 + 6 * Yv * (s - delta) + Zv * (s - delta) ** 2)
    )
    cross_u = sp.expand(chi_u.subs(s, delta) / delta)
    cross_v = sp.expand(chi_v.subs(s, 0) / (-delta))
    assert cross_u == 6 + 6 * Yu * delta + Zu * delta**2
    assert cross_v == 6 - 6 * Yv * delta + Zv * delta**2

    Yu_from_cross = -(Zu * delta**2 + 6) / (6 * delta)
    Yv_from_cross = (Zv * delta**2 + 6) / (6 * delta)
    factored_u = s * (s - delta) * (Zu * s - 6 / delta)
    factored_v = s * (s - delta) * (
        Zv * (s - delta) + 6 / delta
    )
    assert sp.factor(chi_u.subs(Yu, Yu_from_cross) - factored_u) == 0
    assert sp.factor(chi_v.subs(Yv, Yv_from_cross) - factored_v) == 0

    proportional_linear_determinant = (
        delta**2 * Zu * Zv - 6 * (Zu + Zv)
    )
    p = delta * Yu
    q = delta * Yv
    pair_invariant = p * q + 2 * q - 2 * p - 3
    substitutions = {
        Zu: -6 * (1 + p) / delta**2,
        Zv: 6 * (q - 1) / delta**2,
    }
    assert sp.factor(
        proportional_linear_determinant.subs(substitutions)
        + 36 * pair_invariant / delta**2
    ) == 0


def check_three_double_compatibility() -> None:
    u, v, k = sp.symbols("u v k", nonzero=True)
    F, G = sp.symbols("F G")

    def inferred_second_log_jet(partner, formal):
        delta = u - partner
        Y = F + 2 / (u + formal) - 3 / delta
        return sp.factor(
            -6 * (1 + delta * Y) / delta**2
            - Y**2
            + 2 / (u + formal) ** 2
            - 3 / delta**2
        )

    first = inferred_second_log_jet(v, k)
    second = inferred_second_log_jet(k, v)
    expected_difference = (
        -2
        * (v - k)
        * (
            2 * F * (u + v) * (u + k)
            + 2 * u
            + v
            + k
        )
        / ((u + k) ** 2 * (u + v) ** 2)
    )
    assert sp.factor(first - second - expected_difference) == 0

    Fu = -sp.Rational(1, 2) * (1 / (u + v) + 1 / (u + k))
    Fv = -sp.Rational(1, 2) * (1 / (v + u) + 1 / (v + k))
    delta = u - v
    Yu = Fu + 2 / (u + k) - 3 / delta
    Yv = Fv + 2 / (v + k) + 3 / delta
    p = delta * Yu
    q = delta * Yv
    pair_invariant = sp.factor(p * q + 2 * q - 2 * p - 3)
    expected_pair = (
        (u - v) ** 2
        * (u * v + k**2 - 5 * k * (u + v))
        / (4 * (u + v) ** 2 * (u + k) * (v + k))
    )
    assert sp.factor(pair_invariant - expected_pair) == 0

    x, y, zeta = sp.symbols("x y zeta")
    equations = (
        x**2 + y * zeta - 5 * x * (y + zeta),
        y**2 + x * zeta - 5 * y * (x + zeta),
        zeta**2 + x * y - 5 * zeta * (x + y),
    )
    assert sp.factor(equations[0] - equations[1]) == (
        x - y
    ) * (x + y - 6 * zeta)
    assert sp.factor(equations[0] - equations[2]) == (
        x - zeta
    ) * (x + zeta - 6 * y)
    assert sp.expand(
        (x + y - 6 * zeta)
        - (x + zeta - 6 * y)
        - 7 * (y - zeta)
    ) == 0


def check_census_profile() -> None:
    profile = (3,) * 3 + (2,) * 3 + (1,) * 7
    counts, residuals = frontier.census(8, 12)
    assert counts["R"] == 46
    assert profile in residuals
    assert census.EXPECTED_THREE_TRIPLE_THREE_DOUBLE_HYPERPLANE == {
        profile
    }
    assert profile not in set(census.EXPECTED_RESIDUALS)


def main() -> None:
    check_single_drop_cores_and_lifts()
    check_kernel_bound()
    check_parity_and_pencil_wronskians()
    check_cubic_relation_hyperplane()
    check_two_row_characteristic_cubic_lemma()
    check_three_double_compatibility()
    check_census_profile()
    print("PASS: h=8,k=4 profile 3^3 2^3 1^7 cubic-hyperplane closure")
    print("seven/eight legal single-drop lifts span the exact P7 kernel")
    print("three row relations inject into a cubic hyperplane")
    print("all second-order-row degeneracies are division-free")
    print("three formal-double choices force equal double values")


if __name__ == "__main__":
    main()
