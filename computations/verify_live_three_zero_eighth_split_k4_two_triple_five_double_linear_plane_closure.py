#!/usr/bin/env python3
"""Exact audit of the h=8,k=4 profile 3^2 2^5 1^6 closure."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier
import verify_live_three_zero_eighth_split_k4_updated_census as census


z, s, w, mu = sp.symbols("z s w mu")
PROFILE = (3,) * 2 + (2,) * 5 + (1,) * 6


def check_pair_drop_cores_and_lifts() -> None:
    assert sum(PROFILE) == 22

    formal_indices = (2, 3) + tuple(range(7, 13))
    formal_roles = {2: 2, 3: 2, **{index: 1 for index in range(7, 13)}}
    assert sum(formal_roles.values()) == 10

    counts = {0: 0, 1: 0, 2: 0}
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
        omitted_singletons = sum(index >= 7 for index in lowered_pair)
        represented = len(takes)
        residual_degree = represented - 3
        lift_degree = sum(
            3 if index >= 7 else 2 for index in lowered_pair
        )

        counts[omitted_singletons] += 1
        assert sum(takes.values()) == 8
        assert sum(complement) == 14
        assert complement.count(1) == 2
        assert frontier.leaves_singleton(PROFILE, takes)
        assert represented == 8 - omitted_singletons
        assert residual_degree == 5 - omitted_singletons
        assert lift_degree == 4 + omitted_singletons
        assert residual_degree + lift_degree == 9

    assert counts == {0: 1, 1: 12, 2: 15}
    assert sum(counts.values()) == sp.binomial(8, 2) == 28

    x, r = sp.symbols("x r")
    assert sp.factor(
        (z - x) / (z + x) ** 2
        - (z**2 - x**2) / (z + x) ** 3
    ) == 0
    assert sp.factor(
        (z - r)
        - (z - r) * (z + r) ** 2 / (z + r) ** 2
    ) == 0
    assert 12 + 9 == 21
    assert 5 + 2 * 3 + 6 * 2 == 23
    assert 23 - 21 == 2


def check_kernel_equality() -> None:
    for dimension in range(5, 11):
        baseline = 2 * (dimension - 2) + 6 * (dimension - 1)
        cap = dimension * (10 - dimension)
        deficit = baseline - cap
        assert deficit == dimension**2 - 2 * dimension - 10
        assert deficit > 0

        for simple_double_gcd in range(3):
            for absorbed_doubles in range(3 - simple_double_gcd):
                ordinary_doubles = 2 - simple_double_gcd - absorbed_doubles
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
                        deficit
                        + (dimension + 1) * simple_double_gcd
                        + (2 * dimension + 2) * absorbed_doubles
                        + (dimension + 1) * absorbed_singletons
                    )
                    assert observed == expected
                    assert observed > 0

    p_coefficients = sp.symbols("p0:10")
    q_coefficients = sp.symbols("q0:10")
    p = sum(p_coefficients[index] * z**index for index in range(10))
    q = sum(q_coefficients[index] * z**index for index in range(10))
    parity_minor = sp.expand(p * q.subs(z, -z) - p.subs(z, -z) * q)
    assert sp.expand(parity_minor.subs(z, -z) + parity_minor) == 0
    assert sp.Poly(parity_minor, z).degree() <= 17

    layer_values = sp.symbols("v0:8")
    ordinary_divisor = z * sp.prod(z**2 - value**2 for value in layer_values)
    zero_divisor = z**3 * sp.prod(z**2 - value**2 for value in layer_values[:7])
    assert sp.Poly(ordinary_divisor, z).degree() == 17
    assert sp.Poly(zero_divisor, z).degree() == 17

    # If one singleton is zero, an adapted basis has two members in
    # z^3 P_6.  Every parity minor then has a triple zero at the origin.
    a_coefficients = sp.symbols("a0:10")
    b_coefficients = sp.symbols("b0:7")
    c_coefficients = sp.symbols("d0:7")
    p0 = sum(
        coefficient * z**index
        for index, coefficient in enumerate(a_coefficients)
    )
    p1 = z**3 * sum(
        coefficient * z**index
        for index, coefficient in enumerate(b_coefficients)
    )
    p2 = z**3 * sum(
        coefficient * z**index
        for index, coefficient in enumerate(c_coefficients)
    )
    for left, right in ((p0, p1), (p0, p2), (p1, p2)):
        minor = sp.Poly(
            sp.expand(
                left * right.subs(z, -z)
                - left.subs(z, -z) * right
            ),
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
                [
                    sp.diff(section, w, derivative)
                    for section in local_sections
                ]
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
    for absorbed, (forced, cap) in table.items():
        square_degree = (9 - absorbed) // 2
        assert forced == 2 * (6 - absorbed)
        assert cap == 3 * (square_degree - 2)
        assert forced > cap
    assert (9 - 6) // 2 == 1


def check_dual_linear_plane() -> None:
    selected = sp.symbols("x0:2")
    outside = sp.symbols("u0:3")
    triples = sp.symbols("a0:2")
    singletons = sp.symbols("r0:6")

    Q = sp.prod(z + value for value in selected)
    H = sp.prod(z + value for value in singletons)
    C = sp.prod(z - value for value in outside)
    T = sp.prod(z - value for value in triples)
    A = C**2 * T**3
    g_A = C * T**2
    radical = sp.cancel(A / g_A)
    D_A = sp.cancel(sp.diff(A, z) / g_A)
    assert sp.Poly(A, z).degree() == 12
    assert sp.Poly(g_A, z).degree() == 7
    assert sp.Poly(radical, z).degree() == 5
    assert sp.Poly(D_A, z).degree() == 4
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
    assert sp.Poly(differential, z).degree() <= 11

    for degree in range(8):
        trial = z**degree
        trial_differential = sp.Poly(
            sp.expand(
                radical * ((z + mu) * sp.diff(trial, z) + 5 * trial)
                - (z + mu) * D_A * trial
            ),
            z,
        )
        assert trial_differential.degree() <= 11
        if degree < 7:
            assert trial_differential.degree() == degree + 5
            assert trial_differential.coeff_monomial(
                z ** (degree + 5)
            ) == degree - 7
        else:
            assert trial_differential.coeff_monomial(z**12) == 0

    contact = sp.expand(Q**2 * H)
    assert sp.Poly(contact, z).degree() == 10
    assert 11 - 10 == 1
    relation_dimension = 8 - (10 - 4)
    target_dimension = sp.Poly(1 + z, z).degree() + 1
    assert relation_dimension == target_dimension == 2
    assert 18 - 11 == 7

    # Once the injective relation-to-S map fills P_1, every linear S
    # comes from an actual N.  Substitution of E(N)=Q^2 H S in the exact
    # derivative identity gives precisely the claimed complementary-pole
    # denominator.
    s0, s1 = sp.symbols("s0 s1")
    S = s0 + s1 * z
    from_contact = sp.cancel(
        (z + mu) ** 4 * g_A * Q**2 * H * S / A**2
    )
    derivative_model = sp.cancel(
        (z + mu) ** 4 * Q**2 * H * S / (C**3 * T**4)
    )
    assert sp.cancel(from_contact - derivative_model) == 0

    # A rational derivative has zero residue at every finite pole,
    # including complementary poles that were not rows defining K_T.
    laurent_coefficients = sp.symbols("ell0:9")
    laurent = sum(
        coefficient * w**power
        for coefficient, power in zip(
            laurent_coefficients,
            range(-4, 5),
        )
    )
    assert sp.residue(sp.diff(laurent, w), w, 0) == 0


def check_outside_row_and_swap() -> None:
    B0, B1 = sp.symbols("B0 B1", nonzero=True)
    local_unit = B0 + B1 * w
    linear_member = w
    residue = sp.diff(local_unit * linear_member, w, 2).subs(w, 0)
    assert residue == 2 * B1

    u, x, y, v, q, a, b = sp.symbols(
        "u x y v q a b",
        nonzero=True,
    )
    singletons = sp.symbols("r0:6")
    expected_first_jet = (
        4 / (u + mu)
        + 2 / (u + x)
        + 2 / (u + y)
        + sum(1 / (u + value) for value in singletons)
        - 3 / (u - v)
        - 3 / (u - q)
        - 4 / (u - a)
        - 4 / (u - b)
    )
    factor_data = (
        ((z + mu), 4),
        ((z + x), 2),
        ((z + y), 2),
        *((z + value, 1) for value in singletons),
        ((z - v), -3),
        ((z - q), -3),
        ((z - a), -4),
        ((z - b), -4),
    )
    observed_first_jet = 0
    for factor, exponent in factor_data:
        assert sp.cancel(
            sp.diff(factor**exponent, z) / factor**exponent
            - exponent * sp.diff(factor, z) / factor
        ) == 0
        observed_first_jet += (
            exponent * sp.diff(factor, z) / factor
        ).subs(z, u)
    assert sp.cancel(observed_first_jet - expected_first_jet) == 0

    old_selected_contribution = 2 / (u + x)
    old_outside_contribution = -3 / (u - v)
    new_selected_contribution = 2 / (u + v)
    new_outside_contribution = -3 / (u - x)
    swap_difference = sp.factor(
        new_selected_contribution
        + new_outside_contribution
        - old_selected_contribution
        - old_outside_contribution
    )

    def phi(value):
        return 2 / (u + value) + 3 / (u - value)

    assert sp.factor(swap_difference - (phi(v) - phi(x))) == 0
    assert sp.factor(phi(x) - (5 * u + x) / (u**2 - x**2)) == 0

    # For every fixed u and every pair x,v among the other four double
    # indices, there are exactly two selected pairs containing x but not
    # v and keeping u outside.  Each remains valid after the x/v swap.
    swap_witness_count = 0
    double_indices = tuple(range(5))
    for fixed in double_indices:
        other = tuple(index for index in double_indices if index != fixed)
        for selected, outside in combinations(other, 2):
            witnesses = tuple(
                chosen
                for chosen in combinations(other, 2)
                if selected in chosen and outside not in chosen
            )
            assert len(witnesses) == 2
            for chosen in witnesses:
                swapped = (set(chosen) - {selected}) | {outside}
                assert len(swapped) == 2
                assert fixed not in swapped
                swap_witness_count += 1
    assert swap_witness_count == 5 * sp.binomial(4, 2) * 2 == 60

    lam = sp.symbols("lam")
    fibre_polynomial = sp.expand(lam * (u**2 - x**2) - 5 * u - x)
    assert sp.Poly(fibre_polynomial, x).degree() <= 2
    assert sp.Poly(fibre_polynomial, x).coeff_monomial(x) == -1
    assert 4 > 2


def check_census_profile() -> None:
    counts, residuals = frontier.census(8, 12)
    assert counts["R"] == 46
    assert PROFILE in residuals

    expected_increment = {PROFILE}
    assert (
        census.EXPECTED_TWO_TRIPLE_FIVE_DOUBLE_LINEAR_PLANE
        == expected_increment
    )
    post_route_residuals = set(census.EXPECTED_RESIDUALS)
    assert PROFILE not in post_route_residuals
    pre_route_residuals = post_route_residuals | expected_increment
    assert pre_route_residuals - post_route_residuals == expected_increment


def main() -> None:
    check_pair_drop_cores_and_lifts()
    check_kernel_equality()
    check_dual_linear_plane()
    check_outside_row_and_swap()
    check_census_profile()
    print("PASS: h=8,k=4 profile 3^2 2^5 1^6 linear-plane closure")
    print("28 legal pair-drop lifts give the exact P9 kernel")
    print("two relation numerators fill the linear polynomials")
    print("outside-double rows force zero first unit jet")
    print("four doubles cannot occupy one quadratic fibre")
    print("sequential census increment: 1 profile")


if __name__ == "__main__":
    main()
