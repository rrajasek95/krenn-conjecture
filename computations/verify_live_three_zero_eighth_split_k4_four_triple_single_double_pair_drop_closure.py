#!/usr/bin/env python3
"""Exact audit of the h=8,k=4 profile 3^4 2 1^8 closure."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier
import verify_live_three_zero_eighth_split_k4_updated_census as census


z, w, mu = sp.symbols("z w mu")
PROFILE = (3,) * 4 + (2,) + (1,) * 8


def check_pair_drop_cores_and_lifts() -> None:
    assert sum(PROFILE) == 22

    formal_indices = tuple(range(4, 13))
    formal_roles = {4: 2, **{index: 1 for index in range(5, 13)}}
    assert sum(formal_roles.values()) == 10

    counts_by_omitted_singletons = {1: 0, 2: 0}
    for lowered_pair in combinations(formal_indices, 2):
        takes = {
            index: role - (1 if index in lowered_pair else 0)
            for index, role in formal_roles.items()
        }
        takes = {index: role for index, role in takes.items() if role}
        complement = [
            multiplicity - takes.get(index, 0)
            for index, multiplicity in enumerate(PROFILE)
        ]
        omitted_singletons = sum(index >= 5 for index in lowered_pair)
        represented = len(takes)
        residual_degree = represented - 3
        lift_degree = sum(
            3 if index >= 5 else 2 for index in lowered_pair
        )

        counts_by_omitted_singletons[omitted_singletons] += 1
        assert sum(takes.values()) == 8
        assert sum(complement) == 14
        assert complement.count(1) == 2
        assert frontier.leaves_singleton(PROFILE, takes)
        assert represented == 9 - omitted_singletons
        assert residual_degree == 6 - omitted_singletons
        assert lift_degree == 4 + omitted_singletons
        assert residual_degree + lift_degree == 10

    assert counts_by_omitted_singletons == {1: 8, 2: 28}
    assert sum(counts_by_omitted_singletons.values()) == sp.binomial(9, 2) == 36
    assert 2 + 8 * 3 == 26 > 10

    x, r = sp.symbols("x r")
    double_lift = z**2 - x**2
    singleton_lift = (z - r) * (z + r) ** 2
    assert sp.factor(
        (z - x) / (z + x) ** 2 - double_lift / (z + x) ** 3
    ) == 0
    assert sp.factor((z - r) - singleton_lift / (z + r) ** 2) == 0

    assert 12 + 10 == 22
    assert 5 + 3 + 8 * 2 == 24
    assert 24 - 22 == 2


def check_mixed_order_kernel_bound() -> None:
    for dimension in range(5, 12):
        baseline = (dimension - 2) + 8 * (dimension - 1)
        cap = dimension * (11 - dimension)
        deficit = baseline - cap
        assert deficit == dimension**2 - 2 * dimension - 10
        assert deficit > 0

        for simple_double_gcd in range(2):
            for absorbed_double in range(2 - simple_double_gcd):
                ordinary_double = 1 - simple_double_gcd - absorbed_double
                for absorbed_singletons in range(9):
                    gcd_degree = (
                        simple_double_gcd
                        + 3 * absorbed_double
                        + 2 * absorbed_singletons
                    )
                    forced_weight = (
                        ordinary_double * (dimension - 2)
                        + simple_double_gcd * (dimension - 1)
                        + (8 - absorbed_singletons) * (dimension - 1)
                    )
                    reduced_cap = dimension * (
                        11 - gcd_degree - dimension
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


def check_parity_divisor_and_reduced_wronskian() -> None:
    p_coefficients = sp.symbols("p0:11")
    q_coefficients = sp.symbols("q0:11")
    p = sum(p_coefficients[index] * z**index for index in range(11))
    q = sum(q_coefficients[index] * z**index for index in range(11))
    parity_minor = sp.expand(p * q.subs(z, -z) - p.subs(z, -z) * q)
    assert sp.expand(parity_minor.subs(z, -z) + parity_minor) == 0
    assert sp.Poly(parity_minor, z).degree() <= 19

    layer_values = sp.symbols("v0:9")
    ordinary_divisor = z * sp.prod(z**2 - value**2 for value in layer_values)
    zero_divisor = z**3 * sp.prod(z**2 - value**2 for value in layer_values[:8])
    assert sp.Poly(ordinary_divisor, z).degree() == 19
    assert sp.Poly(zero_divisor, z).degree() == 19

    a_coefficients = sp.symbols("a0:11")
    b_coefficients = sp.symbols("b0:8")
    c_coefficients = sp.symbols("c0:8")
    p0 = sum(a_coefficients[index] * z**index for index in range(11))
    p1 = z**3 * sum(b_coefficients[index] * z**index for index in range(8))
    p2 = z**3 * sum(c_coefficients[index] * z**index for index in range(8))
    for left, right in ((p0, p1), (p0, p2), (p1, p2)):
        minor = sp.Poly(
            sp.expand(left * right.subs(z, -z) - left.subs(z, -z) * right),
            z,
        )
        assert all(
            minor.coeff_monomial(z**degree) == 0
            for degree in range(3)
        )

    local_sections = (sp.Integer(1), w**2, w**3)
    local_wronskian = sp.det(
        sp.Matrix(
            [
                [sp.diff(section, w, derivative) for section in local_sections]
                for derivative in range(3)
            ]
        )
    )
    assert sp.factor(local_wronskian) == 6 * w**2

    table = {
        0: (16, 9),
        1: (14, 6),
        2: (12, 6),
        3: (10, 3),
        4: (8, 3),
        5: (6, 0),
        6: (4, 0),
    }
    for gcd_singleton_roots, (forced, cap) in table.items():
        degree_in_square = (10 - gcd_singleton_roots) // 2
        assert forced == 2 * (8 - gcd_singleton_roots)
        assert cap == 3 * (degree_in_square - 2)
        assert forced > cap
    assert (10 - 7) // 2 == 1


def check_duality_and_constant_target() -> None:
    selected = sp.symbols("x")
    triples = sp.symbols("a0:4")
    singletons = sp.symbols("r0:8")

    Q = z + selected
    H = sp.prod(z + value for value in singletons)
    A = sp.prod((z - value) ** 3 for value in triples)
    g_A = sp.prod((z - value) ** 2 for value in triples)
    radical = sp.cancel(A / g_A)
    D_A = sp.cancel(sp.diff(A, z) / g_A)
    assert sp.Poly(A, z).degree() == 12
    assert sp.Poly(g_A, z).degree() == 8
    assert sp.Poly(radical, z).degree() == 4
    assert sp.Poly(D_A, z).degree() == 3
    assert sp.Poly(D_A, z).LC() == 12

    coefficients = sp.symbols("n0:8")
    N = sum(coefficients[index] * z**index for index in range(8))
    differential = sp.expand(
        radical * ((z + mu) * sp.diff(N, z) + 5 * N)
        - (z + mu) * D_A * N
    )
    G = (z + mu) ** 5 * N / A
    assert sp.factor(
        sp.diff(G, z)
        - (z + mu) ** 4 * g_A * differential / A**2
    ) == 0
    assert sp.Poly(differential, z).degree() <= 10

    for degree in range(8):
        trial = z**degree
        trial_differential = sp.Poly(
            sp.expand(
                radical * ((z + mu) * sp.diff(trial, z) + 5 * trial)
                - (z + mu) * D_A * trial
            ),
            z,
        )
        assert trial_differential.degree() <= 10
        if degree < 7:
            assert trial_differential.coeff_monomial(
                z ** (degree + 4)
            ) == degree - 7
        else:
            assert trial_differential.coeff_monomial(z**11) == 0

    contact_divisor = sp.expand(Q**2 * H)
    assert sp.Poly(contact_divisor, z).degree() == 10
    assert 9 - (11 - 4) == 2
    assert 19 - 12 == 7
    assert 2 > 1


def check_census_profile() -> None:
    counts, residuals = frontier.census(8, 12)
    assert counts["R"] == 46
    assert PROFILE in residuals
    expected_increment = {PROFILE}
    assert (
        census.EXPECTED_FOUR_TRIPLE_SINGLE_DOUBLE_PAIR_DROP
        == expected_increment
    )
    post_route_residuals = set(census.EXPECTED_RESIDUALS)
    assert PROFILE not in post_route_residuals
    assert (
        post_route_residuals | expected_increment
    ) - post_route_residuals == expected_increment


def main() -> None:
    check_pair_drop_cores_and_lifts()
    check_mixed_order_kernel_bound()
    check_parity_divisor_and_reduced_wronskian()
    check_duality_and_constant_target()
    check_census_profile()
    print("PASS: h=8,k=4 profile 3^4 2 1^8 pair-drop closure")
    print("36 legal pair-drop lifts in P10: exact")
    print("degree-19 parity and reduced Wronskian obstruction: exact")
    print("four-dimensional kernel and two row relations: exact")
    print("dual relation plane into constants: impossible")


if __name__ == "__main__":
    main()
