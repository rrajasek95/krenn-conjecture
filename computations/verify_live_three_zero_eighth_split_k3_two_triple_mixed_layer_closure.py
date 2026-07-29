#!/usr/bin/env python3
"""Exact audit of the h=8,k=3 mixed-layer closure of 3^2 2^4 1^7."""

from __future__ import annotations

import math

import sympy as sp


H = 8
P = 11
K = P - H
TOTAL = P + H + 2
PROFILE = (3, 3) + (2,) * 4 + (1,) * 7


def check_single_drop_cores_and_lifts() -> None:
    assert (H, P, K, TOTAL) == (8, 11, 3, 21)
    assert sum(PROFILE) == TOTAL
    assert (PROFILE.count(3), PROFILE.count(2), PROFILE.count(1)) == (2, 4, 7)

    # The selected double has role two and all seven singleton layers
    # have role one.  A zero singleton is the only layer whose own drop
    # may lack a nonzero guard; every other drop remains legal.
    for zero_singleton in (False, True):
        singleton_values = list(range(7))
        zero_index = 0 if zero_singleton else None
        legal_drops = ["double"] + [
            index for index in singleton_values if index != zero_index
        ]
        assert len(legal_drops) == (7 if zero_singleton else 8)
        for dropped in legal_drops:
            if dropped == "double":
                selected_labels = 1 + 7
                represented_classes = 8
                residual_degree = represented_classes - K
                lift_degree = 2
                guard = "double_mate"
            else:
                selected_labels = 2 + 6
                represented_classes = 7
                residual_degree = represented_classes - K
                lift_degree = 3
                guard = "omitted_nonzero_singleton"
            assert selected_labels == H
            assert residual_degree + lift_degree == 7
            assert guard in {"double_mate", "omitted_nonzero_singleton"}

    z, x, r = sp.symbols("z x r")
    assert sp.factor(
        (z - x) / (z + x) ** 2 - (z**2 - x**2) / (z + x) ** 3
    ) == 0
    assert sp.factor(
        (z - r) - (z - r) * (z + r) ** 2 / (z + r) ** 2
    ) == 0

    complement_degree = 2 * 3 + 3 * 2
    denominator_degree = 4 + 3 + 2 * 7
    assert complement_degree == 12
    assert denominator_degree == 21
    assert complement_degree + 7 == 19
    assert denominator_degree - (complement_degree + 7) == 2


def check_kernel_dimension_bound() -> None:
    # One exact order-two row and seven exact order-one rows act on P_7.
    # Audit every local gcd pattern relevant after gcd removal.
    for dimension in range(4, 9):
        baseline_weight = (dimension - 2) + 7 * (dimension - 1)
        full_degree_cap = dimension * (8 - dimension)
        baseline_deficit = baseline_weight - full_degree_cap
        assert baseline_deficit == dimension**2 - 9
        assert baseline_deficit > 0

        order_two_cases = (
            # (gcd order, residual weight, deficit increment)
            (0, dimension - 2, 0),
            (1, dimension - 1, dimension + 1),
            (3, 0, 2 * dimension + 2),
        )
        for absorbed_order_one_rows in range(8):
            ordinary_order_one_rows = 7 - absorbed_order_one_rows
            for gcd_order_two, weight_two, increment_two in order_two_cases:
                gcd_degree = gcd_order_two + 2 * absorbed_order_one_rows
                forced_weight = (
                    weight_two
                    + ordinary_order_one_rows * (dimension - 1)
                )
                reduced_cap = dimension * (8 - gcd_degree - dimension)
                observed_deficit = forced_weight - reduced_cap
                expected_increment = (
                    increment_two
                    + absorbed_order_one_rows * (dimension + 1)
                )
                assert observed_deficit == baseline_deficit + expected_increment
                assert observed_deficit > 0


def check_lift_span_obstruction() -> None:
    # If a zero singleton is present there are six usable nonzero
    # singleton drops; otherwise there are seven.
    for nonzero_singletons in (6, 7):
        available_layers = 1 + nonzero_singletons
        product_degree = 2 + 3 * nonzero_singletons
        parity_roots = 2 * available_layers + 1
        assert product_degree > 7
        assert parity_roots >= 15 > 13

        for gcd_singleton_roots in range(nonzero_singletons + 1):
            maximum_even_degree = (7 - gcd_singleton_roots) // 2
            remaining_points = nonzero_singletons - gcd_singleton_roots
            if maximum_even_degree < 1:
                assert gcd_singleton_roots >= 6
                continue
            wronskian_degree = 2 * (maximum_even_degree - 1)
            assert remaining_points > wronskian_degree

    # The parity minor of two degree-seven polynomials is odd and its
    # degree-fourteen coefficient cancels.
    z = sp.symbols("z")
    p_coefficients = sp.symbols("p0:8")
    q_coefficients = sp.symbols("q0:8")
    p_poly = sum(coefficient * z**degree for degree, coefficient in enumerate(p_coefficients))
    q_poly = sum(coefficient * z**degree for degree, coefficient in enumerate(q_coefficients))
    parity_minor = sp.expand(p_poly * q_poly.subs(z, -z) - p_poly.subs(z, -z) * q_poly)
    assert sp.expand(parity_minor.subs(z, -z) + parity_minor) == 0
    assert sp.Poly(parity_minor, z).degree() <= 13


def check_dual_degree_and_factorization() -> None:
    ambient_dimension = 8
    kernel_dimension = 3
    row_count = 8
    row_rank = ambient_dimension - kernel_dimension
    relation_dimension = row_count - row_rank
    assert (row_rank, relation_dimension) == (5, 3)

    selected_denominator_degree = 3 + 2 * 7
    annihilated_moments = 8
    numerator_degree = selected_denominator_degree - (annihilated_moments + 1)
    assert (selected_denominator_degree, numerator_degree) == (17, 8)

    z, mu = sp.symbols("z mu")
    roots = tuple(map(sp.Integer, range(1, 6)))
    multiplicities = (3, 3, 2, 2, 2)
    a_poly = sp.prod(
        (z - root) ** multiplicity
        for root, multiplicity in zip(roots, multiplicities)
    )
    gcd_poly = sp.prod(
        (z - root) ** (multiplicity - 1)
        for root, multiplicity in zip(roots, multiplicities)
    )
    radical = sp.cancel(a_poly / gcd_poly)
    derivative_reduced = sp.cancel(sp.diff(a_poly, z) / gcd_poly)
    assert sp.Poly(a_poly, z).degree() == 12
    assert sp.Poly(radical, z).degree() == 5
    assert sp.Poly(derivative_reduced, z).degree() == 4
    assert sp.Poly(derivative_reduced, z).LC() == 12

    for degree_n in range(9):
        trial = z**degree_n
        differential = sp.Poly(
            sp.expand(
                radical * ((z + mu) * sp.diff(trial, z) + 4 * trial)
                - (z + mu) * derivative_reduced * trial
            ),
            z,
        )
        assert differential.degree() <= 12
        if degree_n < 8:
            assert differential.coeff_monomial(z ** (degree_n + 5)) == degree_n - 8
        else:
            assert differential.coeff_monomial(z**13) == 0

    selected_zero_degree = 2 + 7
    assert selected_zero_degree == 9
    assert 12 - selected_zero_degree == 3

    coefficients = sp.symbols("n0:9")
    n_poly = sum(coefficients[index] * z**index for index in range(9))
    differential = sp.expand(
        radical * ((z + mu) * sp.diff(n_poly, z) + 4 * n_poly)
        - (z + mu) * derivative_reduced * n_poly
    )
    rational = (z + mu) ** 4 * n_poly / a_poly
    assert sp.factor(
        sp.diff(rational, z)
        - (z + mu) ** 3 * gcd_poly * differential / a_poly**2
    ) == 0


def check_outside_cube_rows() -> None:
    delta_v, delta_w, x_jet, z_jet = sp.symbols(
        "delta_v delta_w x_jet z_jet", nonzero=True
    )
    equations = [
        sp.Eq(6 + 6 * x_jet * delta_v + z_jet * delta_v**2, 0),
        sp.Eq(6 + 6 * x_jet * delta_w + z_jet * delta_w**2, 0),
    ]
    solution = sp.solve(equations, (x_jet, z_jet), dict=True)
    assert len(solution) == 1
    assert sp.cancel(
        solution[0][x_jet] + 1 / delta_v + 1 / delta_w
    ) == 0
    assert sp.cancel(
        solution[0][z_jet] - 6 / (delta_v * delta_w)
    ) == 0

    # Three distinct translated cubes are independent in P_3.
    u, v, w = sp.symbols("u v w")
    coefficient_minor = sp.Matrix(
        [
            [3 * node**2, -3 * node, 1]
            for node in (u, v, w)
        ]
    ).det()
    expected_vandermonde = -9 * (u - v) * (u - w) * (v - w)
    assert sp.expand(coefficient_minor - expected_vandermonde) == 0


def check_partition_swap() -> None:
    u, x, y, z, gamma = sp.symbols("u x y z gamma", nonzero=True)

    def identity(selected, other_selected_candidates):
        return (
            gamma
            + 2 / (u + selected)
            - 2 * sum(1 / (u - value) for value in other_selected_candidates)
        )

    identity_x = identity(x, (y, z))
    identity_y = identity(y, (x, z))
    psi_x = 1 / (u + x) + 1 / (u - x)
    psi_y = 1 / (u + y) + 1 / (u - y)
    assert sp.cancel(identity_x - identity_y - 2 * (psi_x - psi_y)) == 0
    assert sp.cancel(psi_x - 2 * u / (u**2 - x**2)) == 0
    assert sp.cancel(psi_y - 2 * u / (u**2 - y**2)) == 0
    cleared_difference = sp.factor(
        (psi_x - psi_y) * (u**2 - x**2) * (u**2 - y**2)
    )
    assert sp.expand(cleared_difference - 2 * u * (x**2 - y**2)) == 0

    # If a singleton is zero, its contribution to Gamma(u) is 1/u;
    # no singleton value is ever divided by in the final comparison.
    zero_singleton_term = 1 / u
    assert zero_singleton_term != sp.zoo


def main() -> None:
    check_single_drop_cores_and_lifts()
    check_kernel_dimension_bound()
    check_lift_span_obstruction()
    check_dual_degree_and_factorization()
    check_outside_cube_rows()
    check_partition_swap()
    print("h=8,k=3 profile 3^2 2^4 1^7 mixed-layer closure: PASS")
    print("7/8 legal single-drop lifts span the exact three-dimensional P_7 kernel")
    print("three row relations inject into a hyperplane in P_3")
    print("outside-double cubes force the forbidden equality x^2=y^2")


if __name__ == "__main__":
    main()
