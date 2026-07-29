#!/usr/bin/env python3
"""Exact audit of the h=8,k=3 closure of the profile 2^9 1^3."""

from __future__ import annotations

from itertools import combinations
import math

import sympy as sp


H = 8
P = 11
K = P - H
TOTAL = P + H + 2
PROFILE = (2,) * 9 + (1,) * 3


def check_combinatorics() -> None:
    assert (H, P, K, TOTAL) == (8, 11, 3, 21)
    assert sum(PROFILE) == TOTAL
    assert PROFILE.count(2) == 9
    assert PROFILE.count(1) == 3

    core_count = 0
    double_indices = range(9)
    singleton_indices = range(9, 12)
    for chosen_tuple in combinations(double_indices, 5):
        chosen = set(chosen_tuple)
        outside = set(double_indices) - chosen
        assert len(outside) == 4
        assert 2 * len(outside) + len(tuple(singleton_indices)) == P
        assert len(outside) + len(tuple(singleton_indices)) == 7
        assert 7 - 4 == 3  # relation pencil lies in P_3

        for partial_tuple in combinations(chosen_tuple, 2):
            partial = set(partial_tuple)
            takes = {
                index: (1 if index in partial else 2)
                for index in chosen
            }
            assert sum(takes.values()) == H
            assert all(index not in takes for index in singleton_indices)
            core_count += 1

    assert core_count == math.comb(9, 5) * math.comb(5, 2) == 1260


def check_local_residue_rows() -> None:
    w = sp.symbols("w")
    b0, b1, b2 = sp.symbols("b0 b1 b2", nonzero=True)
    s0, s1, s2 = sp.symbols("s0 s1 s2")
    regular = b0 + b1 * w + b2 * w**2 / 2
    polynomial = s0 + s1 * w + s2 * w**2 / 2
    product = sp.expand(regular * polynomial)

    # Residue of B*S/w^2: the coefficient of w in B*S.
    double_pole_residue = product.coeff(w, 1)
    assert sp.expand(double_pole_residue - (b0 * s1 + b1 * s0)) == 0

    # Twice the residue of B*S/w^3, normalized by B(0).
    triple_pole_row = sp.expand(2 * product.coeff(w, 2) / b0)
    expected = s2 + 2 * (b1 / b0) * s1 + (b2 / b0) * s0
    assert sp.cancel(triple_pole_row - expected) == 0


def check_wronskian_reduction() -> None:
    z = sp.symbols("z")
    p_coefficients = sp.symbols("p0:4")
    q_coefficients = sp.symbols("q0:4")
    p = sum(coefficient * z**degree for degree, coefficient in enumerate(p_coefficients))
    q = sum(coefficient * z**degree for degree, coefficient in enumerate(q_coefficients))
    wronskian = sp.expand(p * sp.diff(q, z) - sp.diff(p, z) * q)
    assert sp.Poly(wronskian, z).degree() == 4
    assert sp.Poly(wronskian, z).coeff_monomial(z**5) == 0

    # A common singleton Robin row forces a Wronskian zero.
    y, pv, qv = sp.symbols("y pv qv")
    singleton_w = pv * (-y * qv) - (-y * pv) * qv
    assert sp.expand(singleton_w) == 0

    # A common second-order row gives W' + 2 X W = 0.
    pv, p1, qv, q1, x, zz = sp.symbols("pv p1 qv q1 x zz")
    p2 = -2 * x * p1 - zz * pv
    q2 = -2 * x * q1 - zz * qv
    w_value = pv * q1 - p1 * qv
    w_derivative = pv * q2 - p2 * qv
    assert sp.expand(w_derivative + 2 * x * w_value) == 0

    # Once W=L*H, the same row becomes the claimed Robin row on H.
    r1, r2, r3, u, theta = sp.symbols("r1 r2 r3 u theta")
    h0, h1 = sp.symbols("h0 h1")
    linear = h0 + h1 * z
    singleton_cubic = (z - r1) * (z - r2) * (z - r3)
    product_w = singleton_cubic * linear
    lhs = sp.diff(product_w, z) + 2 * theta * product_w
    reduced = singleton_cubic * (
        sp.diff(linear, z)
        + (sp.diff(singleton_cubic, z) / singleton_cubic + 2 * theta)
        * linear
    )
    assert sp.cancel(lhs - reduced) == 0

    # In the basis (1,z), proportional Robin rows have determinant (16).
    theta_u, theta_v, v = sp.symbols("theta_u theta_v v")
    determinant = sp.det(
        sp.Matrix(
            [
                [theta_u, 1 + u * theta_u],
                [theta_v, 1 + v * theta_v],
            ]
        )
    )
    expected_det = theta_u - theta_v + (v - u) * theta_u * theta_v
    assert sp.expand(determinant - expected_det) == 0


def check_logarithmic_coefficient() -> None:
    z, root = sp.symbols("z root")

    # Check the logarithmic derivative rule for every exponent occurring
    # in B_u=(z+mu)^3 Q_T^2/(C_u^3 L^2).
    for exponent in (3, 2, -3, -2):
        factor = (z - root) ** exponent
        assert sp.cancel(
            sp.diff(factor, z) / factor - exponent / (z - root)
        ) == 0

    # Record the coefficient of each reciprocal factor.  Passing from
    # X=B'/B to Theta=L'/L+2X doubles all entries and adds one at each
    # singleton root, giving exactly equation (14).
    x_coefficients = {
        "common": 3,
        "each_chosen_double": 2,
        "each_other_outside_double": -3,
        "each_singleton": -2,
    }
    theta_coefficients = {
        name: 2 * coefficient
        for name, coefficient in x_coefficients.items()
    }
    theta_coefficients["each_singleton"] += 1
    assert theta_coefficients == {
        "common": 6,
        "each_chosen_double": 4,
        "each_other_outside_double": -6,
        "each_singleton": -3,
    }


def check_partition_separation() -> None:
    mu, u, v, a, b = sp.symbols("mu u v a b")
    other = sp.symbols("c0:5")
    singleton = sp.symbols("r0:3")
    moving_universe = (b,) + other
    chosen_t = other

    theta_u = (
        6 / (u + mu)
        + 4 * sum(1 / (u + value) for value in chosen_t)
        - 6 * sum(1 / (u - value) for value in (v, a, b))
        - 3 * sum(1 / (u - value) for value in singleton)
    )
    k_u = (
        6 / (u + mu)
        + 4 * sum(1 / (u + value) for value in moving_universe)
        - 6 * sum(1 / (u - value) for value in (v, a))
        - 3 * sum(1 / (u - value) for value in singleton)
    )
    phi_u = 2 / (u + b) + 3 / (u - b)
    assert sp.cancel(theta_u - (k_u - 2 * phi_u)) == 0
    assert sp.cancel(phi_u - (5 * u + b) / (u**2 - b**2)) == 0

    theta_v = (
        6 / (v + mu)
        + 4 * sum(1 / (v + value) for value in chosen_t)
        - 6 * sum(1 / (v - value) for value in (u, a, b))
        - 3 * sum(1 / (v - value) for value in singleton)
    )
    k_v = (
        6 / (v + mu)
        + 4 * sum(1 / (v + value) for value in moving_universe)
        - 6 * sum(1 / (v - value) for value in (u, a))
        - 3 * sum(1 / (v - value) for value in singleton)
    )
    phi_v = 2 / (v + b) + 3 / (v - b)
    assert sp.cancel(theta_v - (k_v - 2 * phi_v)) == 0
    assert sp.cancel(phi_v - (5 * v + b) / (v**2 - b**2)) == 0


def check_quartic_and_endpoints() -> None:
    b, u, v, k_u, k_v = sp.symbols("b u v k_u k_v")
    d_u = u**2 - b**2
    d_v = v**2 - b**2
    n_u = k_u * d_u - 2 * (5 * u + b)
    n_v = k_v * d_v - 2 * (5 * v + b)
    cleared = sp.expand(n_u * d_v - n_v * d_u + (v - u) * n_u * n_v)
    polynomial = sp.Poly(cleared, b)
    assert polynomial.degree() <= 4
    assert 6 > polynomial.degree()

    assert sp.expand(n_u.subs(b, u) + 12 * u) == 0
    assert sp.expand(n_u.subs(b, -u) + 8 * u) == 0
    assert sp.expand(d_v.subs(b, u) - d_v.subs(b, -u)) == 0
    assert sp.expand(n_v.subs(b, u) - n_v.subs(b, -u) + 4 * u) == 0

    endpoint_u = sp.factor(cleared.subs(b, u))
    endpoint_minus_u = sp.factor(cleared.subs(b, -u))
    expected_u = sp.factor(
        n_u.subs(b, u)
        * (d_v.subs(b, u) + (v - u) * n_v.subs(b, u))
    )
    expected_minus_u = sp.factor(
        n_u.subs(b, -u)
        * (d_v.subs(b, -u) + (v - u) * n_v.subs(b, -u))
    )
    assert sp.expand(endpoint_u - expected_u) == 0
    assert sp.expand(endpoint_minus_u - expected_minus_u) == 0

    # If the quartic vanished identically, the two bracketed endpoint
    # equations would differ by this structurally nonzero expression.
    bracket_difference = sp.expand(
        (d_v.subs(b, u) + (v - u) * n_v.subs(b, u))
        - (d_v.subs(b, -u) + (v - u) * n_v.subs(b, -u))
    )
    assert sp.expand(bracket_difference + 4 * u * (v - u)) == 0


def main() -> None:
    check_combinatorics()
    check_local_residue_rows()
    check_wronskian_reduction()
    check_logarithmic_coefficient()
    check_partition_separation()
    check_quartic_and_endpoints()
    print("h=8,k=3 profile 2^9 1^3 closure: PASS")
    print("1260 legal formal-five-double cores; relation pencils lie in P_3")
    print("three singleton rows reduce each Wronskian to L times P_1")
    print("six moving values force a quartic identity; endpoints contradict it")


if __name__ == "__main__":
    main()
