#!/usr/bin/env python3
"""Exact audit of the p=18 mixed six-simple/three-double cofactor closure."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verify_live_three_zero_higher_split_q5_boundary_census import (  # noqa: E402
    formal_selections,
)


def assert_zero(expr: sp.Expr) -> None:
    assert sp.factor(sp.together(expr)) == 0, sp.factor(sp.together(expr))


def profile(triples: int, doubles: int, singletons: int) -> tuple[int, ...]:
    return (3,) * triples + (2,) * doubles + (1,) * singletons


def wronskian(polys: list[sp.Expr], variable: sp.Symbol) -> sp.Expr:
    return sp.factor(
        sp.Matrix(
            [
                [sp.diff(poly, variable, order) for poly in polys]
                for order in range(len(polys))
            ]
        ).det()
    )


def audit_common_and_neighboring_selections() -> None:
    for h in range(13, 18):
        for doubles in range(3, 6):
            original = profile(2, doubles, h + 14 - 2 * doubles)
            selections = formal_selections(original, h, 18)
            common_target = profile(2, 3, 6)
            assert any(
                selection.d == doubles - 3
                and selection.selected_triples == 0
                and selection.complement == common_target
                for selection in selections
            )
            singleton_count = h + 14 - 2 * doubles
            assert singleton_count - 4 == h + 10 - 2 * doubles
            assert singleton_count - 1 >= 4

            if doubles == 5:
                assert any(
                    selection.d == 1
                    and selection.selected_triples == 0
                    and selection.complement == profile(2, 4, 4)
                    for selection in selections
                )

    # Common relation space P_7, annihilator dimension five.
    assert (7 + 1) - 3 == 5
    # Neighboring b=5 relation space P_6, annihilator dimension four.
    assert (6 + 1) - 3 == 4


def audit_mixed_principal_parts_and_degrees() -> None:
    # Three double denominators contribute degree nine.  Annihilating P_7
    # removes nine degrees at infinity.
    for simple_anchors, relation_count, moving_count in (
        (5, 3, 1),
        (4, 2, 2),
    ):
        actual_rows = simple_anchors + 3
        assert actual_rows - 5 == relation_count
        denominator_degree = 2 * simple_anchors + 3 * 3
        numerator_degree = denominator_degree - (7 + 2)
        assert numerator_degree == 2 * simple_anchors
        normalized_degree = numerator_degree + 3 * moving_count
        assert normalized_degree == 18 - simple_anchors

    # Match the order-three principal coefficients exactly.
    tau = sp.symbols("tau")
    f0, f1, f2, lam, alpha, delta = sp.symbols(
        "f0 f1 f2 lambda alpha delta"
    )
    local_numerator = f0 + f1 * tau + f2 * tau**2 / 2
    principal = sp.expand(local_numerator / tau**3)
    model = 2 * lam / tau**3 + 2 * alpha * lam / tau**2 + delta * lam / tau
    matching = {
        f0: 2 * lam,
        f1: 2 * alpha * lam,
        f2: 2 * delta * lam,
    }
    for exponent in (-3, -2, -1):
        assert_zero(
            principal.coeff(tau, exponent).subs(matching)
            - model.coeff(tau, exponent)
        )
    assert_zero(
        (f1 / f0 - alpha).subs({f0: 2 * lam, f1: 2 * alpha * lam})
    )
    assert_zero(
        (f2 / f0 - delta).subs({f0: 2 * lam, f2: 2 * delta * lam})
    )

    # Multiplication transports both normalized jets by the product rule.
    p0, p1, p2, m0, m1, m2 = sp.symbols("p0 p1 p2 m0 m1 m2")
    product_value = m0 * p0
    product_first = m1 * p0 + m0 * p1
    product_second = m2 * p0 + 2 * m1 * p1 + m0 * p2
    old_alpha = p1 / p0
    old_delta = p2 / p0
    log_first = m1 / m0
    ratio_second = m2 / m0
    assert_zero(product_first / product_value - old_alpha - log_first)
    assert_zero(
        product_second / product_value
        - old_delta
        - 2 * log_first * old_alpha
        - ratio_second
    )

    # Exact selected/complementary double multiplier.
    z, v, q = sp.symbols("z v q")
    exchange = (z - q) ** 3 * (z + q) ** 2
    exchange_log = sp.cancel(sp.diff(exchange, z) / exchange)
    assert_zero(exchange_log - 3 / (z - q) - 2 / (z + q))
    exchange_second = sp.cancel(sp.diff(exchange, z, 2) / exchange)
    expected_second = (
        exchange_log**2 - 3 / (z - q) ** 2 - 2 / (z + q) ** 2
    )
    assert_zero(exchange_second - expected_second)
    assert exchange.subs(z, v) != 0


def audit_dimension_forcing() -> None:
    # Five simple anchors plus three double two-jet anchors have effective
    # weight eleven.
    for dimension in range(6, 15):
        assert (5 + 2 * 3) * (dimension - 1) > dimension * (
            14 - dimension
        )
    assert 5 * 3 > 13
    assert 11 * 3 + 3 * 3 > 4 * (14 - 4)

    # Four simple anchors plus three double two-jet anchors have effective
    # weight ten in P_14.
    for dimension in range(7, 16):
        assert (4 + 2 * 3) * (dimension - 1) > dimension * (
            15 - dimension
        )
    minimum_moving = 13
    assert (14 - minimum_moving) + 1 == 2 < 5
    assert (4 * 5 + 3 * 10) + 6 > 6 * (15 - 6)

    # One rank-one three-jet system has the claimed doubled Wronskian
    # weight at a double value.
    for dimension in range(3, 7):
        vanishing = (0,) + tuple(range(3, dimension + 2))
        baseline = tuple(range(dimension))
        assert sum(vanishing) - sum(baseline) == 2 * (dimension - 1)


def audit_cofactor_and_interpolation() -> None:
    # A five-space hyperplane inherits fixed factor A^4 V^8 of degree 40.
    assert 4 * 4 + 3 * 8 == 40
    assert 5 * (15 - 5) == 50
    assert 50 - 40 - 5 == 5
    assert 14 - 5 == 9
    degrees = tuple(5 - order + 9 for order in range(4))
    assert degrees == (14, 13, 12, 11)

    for h in range(13, 18):
        b3_roots = h + 4
        b4_roots = h + 2
        b5_roots = (h + 2, h + 2, h, h)
        assert all(b3_roots > degree for degree in degrees)
        assert all(b4_roots > degree for degree in degrees)
        assert all(
            roots > degree for roots, degree in zip(b5_roots, degrees)
        )

    # Neighboring b=5: use the same four simple and three old double rows.
    assert (4 + 3) - 4 == 3
    fixed_denominator_degree = 2 * 4 + 3 * 3
    assert fixed_denominator_degree == 17
    assert fixed_denominator_degree - (6 + 2) == 9
    assert 9 + 5 == 14
    vanishing_sequence = (0, 1, 3, 4, 5)
    assert sum(vanishing_sequence) - sum(range(5)) == 3

    # Exact cofactor diagonal sign, reused in the mixed quotient.
    z, t = sp.symbols("z t")
    basis = [z**degree for degree in range(6)]
    cofactor = sp.Matrix(
        [[t**degree for degree in range(6)]]
        + [
            [sp.diff(poly, z, order) for poly in basis]
            for order in range(5)
        ]
    ).det()
    full_wronskian = wronskian(basis, z)
    assert_zero(cofactor - 288 * (z - t) ** 5)
    assert_zero(
        sp.cancel(cofactor / (t - z) ** 5) + full_wronskian / 120
    )

    # The ambient six-space has A^5 V^10.  After the hyperplane divisor,
    # the diagonal retains A V^2 of degree ten, versus residual degree six.
    assert 4 * 5 + 3 * 10 == 50
    assert (4 * 5 + 3 * 10) - (4 * 4 + 3 * 8) == 10
    assert 4 + 2 * 3 == 10
    assert (5 - 4) + (9 - 4) == 6 < 10


def main() -> None:
    audit_common_and_neighboring_selections()
    audit_mixed_principal_parts_and_degrees()
    audit_dimension_forcing()
    audit_cofactor_and_interpolation()
    print("p=18 two-triple six-simple/three-double cofactor closure PASS")
    print("closed uniformly: a=2, b=3,4,5")
    print("mixed effective anchor weights: 11 in P_13, 10 in P_14")
    print("cofactor quotient bidegree: (5,9)")
    print("b=5 companion double corrections: two order-three points")
    print("remaining a=2 families: b=6,7,8")


if __name__ == "__main__":
    main()
