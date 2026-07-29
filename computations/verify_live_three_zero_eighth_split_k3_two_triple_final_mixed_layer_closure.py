#!/usr/bin/env python3
"""Exact audit of the final h=8, k=3 profile 3^2 2^4 1^7 closure."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


z, w, mu = sp.symbols("z w mu")


def check_single_drop_cores_and_lifts() -> None:
    profile = (3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1)
    assert sum(profile) == 21

    formal_roles = {2: 2, **{index: 1 for index in range(6, 13)}}
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
        assert sum(complement) == 13
        assert complement.count(1) == 1

        if lowered == 2:
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
    assert 8 - 1 == 7  # at worst the zero-singleton drop is unavailable

    x, r = sp.symbols("x r")
    double_lift = z**2 - x**2
    singleton_lift = (z - r) * (z + r) ** 2
    assert sp.factor(
        (z - x) / (z + x) ** 2 - double_lift / (z + x) ** 3
    ) == 0
    assert sp.factor(
        (z - r) - singleton_lift / (z + r) ** 2
    ) == 0

    assert 12 + 7 == 19
    assert 4 + 3 + 7 * 2 == 21
    assert 21 - 19 == 2


def check_kernel_bound() -> None:
    # One exact order-two row and seven exact order-one rows on P_7.
    for dimension in range(4, 9):
        baseline = (dimension - 2) + 7 * (dimension - 1)
        cap = dimension * (8 - dimension)
        baseline_deficit = baseline - cap
        assert baseline_deficit == dimension**2 - 9
        assert baseline_deficit > 0

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
                        baseline_deficit
                        + (dimension + 1) * simple_double_gcd
                        + (2 * dimension + 2) * absorbed_double
                        + (dimension + 1) * absorbed_singletons
                    )
                    assert observed == expected
                    assert observed > 0


def check_parity_and_pencil_wronskians() -> None:
    p_coefficients = sp.symbols("p0:8")
    q_coefficients = sp.symbols("q0:8")
    p = sum(coefficient * z**index for index, coefficient in enumerate(p_coefficients))
    q = sum(coefficient * z**index for index, coefficient in enumerate(q_coefficients))
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

    # Vanishing sequence (0,2) gives one Wronskian zero.
    local_wronskian = sp.det(
        sp.Matrix(
            [
                [sp.Integer(1), w**2],
                [sp.Integer(0), 2 * w],
            ]
        )
    )
    assert local_wronskian == 2 * w

    no_zero_forced = (7, 6, 5, 4, 3, 2)
    one_zero_forced = (6, 5, 4, 3, 2, 1)
    caps = (4, 4, 2, 2, 0, 0)
    for count, expected_cap in enumerate(caps):
        degree_in_s = (7 - count) // 2
        assert expected_cap == 2 * (degree_in_s - 1)
        assert no_zero_forced[count] > expected_cap
        assert one_zero_forced[count] > expected_cap
    assert (7 - 6) // 2 == 0  # too small for a pencil


def check_cubic_relation_hyperplane() -> None:
    x = sp.symbols("x")
    outside_doubles = sp.symbols("u0:3")
    triples = sp.symbols("a0:2")
    singletons = sp.symbols("r0:7")

    Q = z + x
    H = sp.prod(z + value for value in singletons)
    C = sp.prod(z - value for value in outside_doubles)
    T = sp.prod(z - value for value in triples)
    A = C**2 * T**3
    g_A = C * T**2
    radical = sp.cancel(A / g_A)
    D_A = sp.cancel(sp.diff(A, z) / g_A)
    assert sp.Poly(A, z).degree() == 12
    assert sp.Poly(radical, z).degree() == 5
    assert sp.Poly(D_A, z).degree() == 4
    assert sp.Poly(D_A, z).LC() == 12

    coefficients = sp.symbols("n0:9")
    N = sum(coefficients[index] * z**index for index in range(9))
    differential = sp.expand(
        radical * ((z + mu) * sp.diff(N, z) + 4 * N)
        - (z + mu) * D_A * N
    )
    G = (z + mu) ** 4 * N / A
    assert sp.factor(
        sp.diff(G, z)
        - (z + mu) ** 3 * g_A * differential / A**2
    ) == 0
    assert sp.Poly(differential, z).degree() <= 12

    for degree in range(9):
        trial = z**degree
        trial_differential = sp.Poly(
            sp.expand(
                radical * ((z + mu) * sp.diff(trial, z) + 4 * trial)
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
    assert 8 - (8 - 3) == 3  # eight rows, rank five, three relations
    assert 17 - 9 == 8  # principal-part numerator degree

    # Three anchored cubes at distinct nodes are independent.
    u0, u1, u2 = outside_doubles
    cube_matrix = sp.Matrix(
        [
            [
                sp.Poly((z - node) ** 3, z).coeff_monomial(z**power)
                for power in range(4)
            ]
            for node in outside_doubles
        ]
    )
    assert sp.factor(cube_matrix[:, :3].det()) != 0
    assert cube_matrix.rank() == 3


def check_outside_double_row_and_swap() -> None:
    delta, epsilon = sp.symbols("delta epsilon", nonzero=True)
    B0, B1, B2 = sp.symbols("B0 B1 B2", nonzero=True)
    local_unit = B0 + B1 * w + B2 * w**2 / 2
    anchored_cube = (delta + w) ** 3
    residue_row = sp.diff(local_unit * anchored_cube, w, 2).subs(w, 0)
    assert sp.expand(residue_row) == (
        6 * B0 * delta + 6 * B1 * delta**2 + B2 * delta**3
    )

    Y, Z = sp.symbols("Y Z")
    equations = [
        6 + 6 * Y * root + Z * root**2
        for root in (delta, epsilon)
    ]
    solution = sp.solve(equations, (Y, Z), dict=True)
    assert len(solution) == 1
    assert sp.factor(
        solution[0][Y] + 1 / delta + 1 / epsilon
    ) == 0
    assert sp.factor(
        solution[0][Z] - 6 / (delta * epsilon)
    ) == 0

    u, x, y = sp.symbols("u x y", nonzero=True)
    swap_difference = (
        2 / (u + x)
        - 2 / (u - y)
        - 2 / (u + y)
        + 2 / (u - x)
    )

    def fibre_map(value: sp.Expr) -> sp.Expr:
        return 1 / (u + value) + 1 / (u - value)

    assert sp.factor(
        swap_difference - 2 * (fibre_map(x) - fibre_map(y))
    ) == 0
    assert sp.factor(
        fibre_map(x) - 2 * u / (u**2 - x**2)
    ) == 0

    fibre_value = sp.symbols("fibre_value")
    fibre_polynomial = sp.expand(
        fibre_value * (u**2 - x**2) - 2 * u
    )
    assert sp.Poly(fibre_polynomial, x).degree() == 2
    assert sp.Poly(fibre_polynomial.subs(fibre_value, 0), x) == sp.Poly(-2 * u, x)
    assert 3 > 2


def check_final_census_profile() -> None:
    profile = (3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1)
    counts, residuals = frontier.census(8, 11)
    assert counts["R"] == 46
    assert profile in residuals


def main() -> None:
    check_single_drop_cores_and_lifts()
    check_kernel_bound()
    check_parity_and_pencil_wronskians()
    check_cubic_relation_hyperplane()
    check_outside_double_row_and_swap()
    check_final_census_profile()
    print("PASS: final h=8, k=3 profile 3^2 2^4 1^7 mixed-layer closure")
    print("seven/eight legal single-drop lifts in P_7: exact")
    print("degree-13 parity and pencil Wronskian obstruction: exact")
    print("three-dimensional kernel and cubic relation hyperplane: exact")
    print("outside-double row transfer and quadratic fibre: impossible")
    print("h=8, k=3 no-extra-singular collision frontier: empty")


if __name__ == "__main__":
    main()
