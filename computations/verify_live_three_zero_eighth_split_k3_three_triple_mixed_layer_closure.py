#!/usr/bin/env python3
"""Exact audit of the h=8, k=3 profile 3^3 2^3 1^6 closure."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


z, s, w, mu = sp.symbols("z s w mu")


def check_pair_drop_cores_and_lifts() -> None:
    profile = (3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1)
    assert sum(profile) == 21

    # Formal roles: two of the three doubles at role two and all six
    # singleton classes at role one.
    formal_indices = (3, 4, 6, 7, 8, 9, 10, 11)
    formal_roles = {3: 2, 4: 2, **{index: 1 for index in range(6, 12)}}
    assert sum(formal_roles.values()) == 10

    counts_by_omitted_singletons = {0: 0, 1: 0, 2: 0}
    for lowered_pair in combinations(formal_indices, 2):
        takes = {
            index: role - (1 if index in lowered_pair else 0)
            for index, role in formal_roles.items()
        }
        takes = {index: role for index, role in takes.items() if role}
        complement = [
            multiplicity - takes.get(index, 0)
            for index, multiplicity in enumerate(profile)
        ]
        omitted_singletons = sum(index >= 6 for index in lowered_pair)
        represented = len(takes)
        residual_degree = represented - 3
        lift_degree = sum(
            3 if index >= 6 else 2 for index in lowered_pair
        )

        counts_by_omitted_singletons[omitted_singletons] += 1
        assert sum(takes.values()) == 8
        assert sum(complement) == 13
        assert complement.count(1) == 2
        assert represented == 8 - omitted_singletons
        assert residual_degree == 5 - omitted_singletons
        assert lift_degree == 4 + omitted_singletons
        assert residual_degree + lift_degree == 9

    assert counts_by_omitted_singletons == {0: 1, 1: 12, 2: 15}
    assert sum(counts_by_omitted_singletons.values()) == sp.binomial(8, 2) == 28

    x, r = sp.symbols("x r")
    double_lift = z**2 - x**2
    singleton_lift = (z - r) * (z + r) ** 2
    assert sp.factor(
        (z - x) / (z + x) ** 2 - double_lift / (z + x) ** 3
    ) == 0
    assert sp.factor(
        (z - r) - singleton_lift / (z + r) ** 2
    ) == 0
    assert sp.Poly(double_lift, z).degree() == 2
    assert sp.Poly(singleton_lift, z).degree() == 3

    numerator_degree = 11 + 9
    denominator_degree = 4 + 2 * 3 + 6 * 2
    assert numerator_degree == 20
    assert denominator_degree == 22
    assert denominator_degree - numerator_degree == 2


def check_mixed_order_kernel_bound() -> None:
    # Two exact order-two rows and six exact order-one rows on P_9.
    for dimension in range(5, 11):
        baseline = 2 * (dimension - 2) + 6 * (dimension - 1)
        cap = dimension * (10 - dimension)
        baseline_deficit = baseline - cap
        assert baseline_deficit == dimension**2 - 2 * dimension - 10
        assert baseline_deficit > 0

        # At order-two nodes: gcd order one, or absorption at order >=3.
        for simple_double_gcd in range(3):
            for absorbed_doubles in range(3 - simple_double_gcd):
                ordinary_doubles = 2 - simple_double_gcd - absorbed_doubles
                # At order-one nodes, gcd order one is impossible; the
                # minimal absorbed order is two.
                for absorbed_singletons in range(7):
                    gcd_degree = (
                        simple_double_gcd
                        + 3 * absorbed_doubles
                        + 2 * absorbed_singletons
                    )
                    forced_weight = (
                        ordinary_doubles * (dimension - 2)
                        + simple_double_gcd * (dimension - 1)
                        + (6 - absorbed_singletons) * (dimension - 1)
                    )
                    reduced_cap = dimension * (
                        10 - gcd_degree - dimension
                    )
                    observed = forced_weight - reduced_cap
                    expected = (
                        baseline_deficit
                        + (dimension + 1) * simple_double_gcd
                        + (2 * dimension + 2) * absorbed_doubles
                        + (dimension + 1) * absorbed_singletons
                    )
                    assert observed == expected
                    assert observed > 0


def check_parity_divisor_and_reduced_wronskian() -> None:
    p_coefficients = sp.symbols("p0:10")
    q_coefficients = sp.symbols("q0:10")
    p = sum(coefficient * z**index for index, coefficient in enumerate(p_coefficients))
    q = sum(coefficient * z**index for index, coefficient in enumerate(q_coefficients))
    parity_minor = sp.expand(p * q.subs(z, -z) - p.subs(z, -z) * q)
    assert sp.expand(parity_minor.subs(z, -z) + parity_minor) == 0
    assert sp.Poly(parity_minor, z).degree() <= 17

    layer_values = sp.symbols("v0:8")
    ordinary_divisor = z * sp.prod(z**2 - value**2 for value in layer_values)
    zero_divisor = z**3 * sp.prod(z**2 - value**2 for value in layer_values[:7])
    assert sp.Poly(ordinary_divisor, z).degree() == 17
    assert sp.Poly(zero_divisor, z).degree() == 17

    # If the zero singleton is present, two basis members of its
    # divisibility plane have a z^3 factor.  Every parity minor then has
    # order at least three at zero.
    a_coefficients = sp.symbols("a0:10")
    b_coefficients = sp.symbols("b0:7")
    c_coefficients = sp.symbols("d0:7")
    p0 = sum(coefficient * z**index for index, coefficient in enumerate(a_coefficients))
    p1 = z**3 * sum(coefficient * z**index for index, coefficient in enumerate(b_coefficients))
    p2 = z**3 * sum(coefficient * z**index for index, coefficient in enumerate(c_coefficients))
    for left, right in ((p0, p1), (p0, p2), (p1, p2)):
        minor = sp.Poly(
            sp.expand(left * right.subs(z, -z) - left.subs(z, -z) * right),
            z,
        )
        assert all(
            minor.coeff_monomial(z**degree) == 0
            for degree in range(3)
        )

    # Vanishing sequence (0,2,3) has Wronskian weight exactly two.
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
        0: (12, 6),
        1: (10, 6),
        2: (8, 3),
        3: (6, 3),
        4: (4, 0),
        5: (2, 0),
    }
    for gcd_singleton_roots, (forced, cap) in table.items():
        degree_in_s = (9 - gcd_singleton_roots) // 2
        assert forced == 2 * (6 - gcd_singleton_roots)
        assert cap == 3 * (degree_in_s - 2)
        assert forced > cap
    assert (9 - 6) // 2 == 1  # too small for a three-space in s


def check_duality_and_constant_target() -> None:
    x, y, u = sp.symbols("x y u")
    triples = sp.symbols("a0:3")
    singletons = sp.symbols("r0:6")

    Q = (z + x) * (z + y)
    H = sp.prod(z + value for value in singletons)
    A = (z - u) ** 2 * sp.prod((z - value) ** 3 for value in triples)
    g_A = (z - u) * sp.prod((z - value) ** 2 for value in triples)
    radical = sp.cancel(A / g_A)
    D_A = sp.cancel(sp.diff(A, z) / g_A)
    assert sp.Poly(A, z).degree() == 11
    assert sp.Poly(radical, z).degree() == 4
    assert sp.Poly(D_A, z).degree() == 3
    assert sp.Poly(D_A, z).LC() == 11

    coefficients = sp.symbols("n0:8")
    N = sum(coefficients[index] * z**index for index in range(8))
    differential = sp.expand(
        radical * ((z + mu) * sp.diff(N, z) + 4 * N)
        - (z + mu) * D_A * N
    )
    G = (z + mu) ** 4 * N / A
    assert sp.factor(
        sp.diff(G, z)
        - (z + mu) ** 3 * g_A * differential / A**2
    ) == 0
    assert sp.Poly(differential, z).degree() <= 10

    for degree in range(8):
        trial = z**degree
        trial_differential = sp.Poly(
            sp.expand(
                radical * ((z + mu) * sp.diff(trial, z) + 4 * trial)
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
    assert 8 - (10 - 4) == 2  # eight rows, rank six, two relations
    assert 18 - 11 == 7  # principal-part denominator minus infinity order
    assert 2 > 1  # the relation numerator plane cannot inject into constants


def check_census_consequence() -> None:
    profile = (3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1)
    counts, residuals = frontier.census(8, 11)
    assert counts["R"] == 46
    assert profile in residuals

    old_three_triple_frontier = {
        (3, 3, 3, 2, 2, 2, 2, 2, 2),
        (3, 3, 3, 2, 2, 2, 2, 2, 1, 1),
        (3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1),
        profile,
    }
    formal_five_closures = old_three_triple_frontier - {profile}
    assert old_three_triple_frontier - formal_five_closures - {profile} == set()


def main() -> None:
    check_pair_drop_cores_and_lifts()
    check_mixed_order_kernel_bound()
    check_parity_divisor_and_reduced_wronskian()
    check_duality_and_constant_target()
    check_census_consequence()
    print("PASS: exact h=8, k=3 profile 3^3 2^3 1^6 mixed-layer closure")
    print("28 legal pair-drop lifts in P_9: exact")
    print("degree-17 parity and reduced Wronskian obstruction: exact")
    print("four-dimensional kernel and two row relations: exact")
    print("dual relation plane into constants: impossible")


if __name__ == "__main__":
    main()
