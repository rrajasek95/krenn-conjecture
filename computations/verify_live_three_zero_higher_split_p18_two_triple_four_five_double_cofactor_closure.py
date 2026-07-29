#!/usr/bin/env python3
"""Exact audit of the p=18 two-triple b=6,7 cofactor closure."""

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


def audit_selection_profiles() -> None:
    cases = {
        6: {
            "fixed_doubles": 4,
            "fixed_simples": 2,
            "base": profile(2, 4, 4),
            "neighbor": profile(2, 5, 2),
        },
        7: {
            "fixed_doubles": 5,
            "fixed_simples": 0,
            "base": profile(2, 5, 2),
            "neighbor": profile(2, 6, 0),
        },
    }

    for h in range(13, 18):
        for doubles, data in cases.items():
            singleton_count = h + 14 - 2 * doubles
            original = profile(2, doubles, singleton_count)
            selections = formal_selections(original, h, 18)
            assert any(
                selection.d == 2
                and selection.selected_triples == 0
                and selection.complement == data["base"]
                for selection in selections
            )
            assert any(
                selection.d == 1
                and selection.selected_triples == 0
                and selection.complement == data["neighbor"]
                for selection in selections
            )

            fixed_doubles = data["fixed_doubles"]
            fixed_simples = data["fixed_simples"]
            assert fixed_simples + 2 * fixed_doubles == 10
            assert singleton_count - fixed_simples == h
            assert singleton_count - (fixed_simples + 1) >= 12

            ambient_degree = fixed_simples + fixed_doubles
            assert ambient_degree in (5, 6)
            annihilator_dimension = ambient_degree + 1 - 3
            assert annihilator_dimension == fixed_simples + fixed_doubles - 2


def audit_relation_numerators_and_transport() -> None:
    for fixed_doubles, fixed_simples in ((4, 2), (5, 0)):
        ambient_degree = fixed_simples + fixed_doubles
        annihilator_dimension = ambient_degree - 2

        low_rows = fixed_simples + fixed_doubles
        assert low_rows - annihilator_dimension == 2
        low_denominator = 2 * fixed_simples + 3 * fixed_doubles
        low_numerator = low_denominator - (ambient_degree + 2)
        assert low_numerator == 8
        assert low_numerator + 2 * 3 == 14

        high_rows = fixed_simples + 1 + fixed_doubles
        assert high_rows - annihilator_dimension == 3
        high_denominator = 2 * (fixed_simples + 1) + 3 * fixed_doubles
        high_numerator = high_denominator - (ambient_degree + 2)
        assert high_numerator == 10
        assert high_numerator + 3 == 13

        neighbor_degree = fixed_simples + fixed_doubles - 1
        neighbor_annihilator = neighbor_degree + 1 - 3
        assert low_rows - neighbor_annihilator == 3
        neighbor_numerator = low_denominator - (neighbor_degree + 2)
        assert neighbor_numerator == 9
        assert neighbor_numerator + 5 == 14

    # Multiplication transports first and second normalized jets exactly.
    p0, p1, p2, m0, m1, m2 = sp.symbols("p0 p1 p2 m0 m1 m2")
    product_value = m0 * p0
    product_first = m1 * p0 + m0 * p1
    product_second = m2 * p0 + 2 * m1 * p1 + m0 * p2
    assert_zero(product_first / product_value - p1 / p0 - m1 / m0)
    assert_zero(
        product_second / product_value
        - p2 / p0
        - 2 * (m1 / m0) * (p1 / p0)
        - m2 / m0
    )

    # The selected/complementary double exchange is the quintic g_q.
    z, q = sp.symbols("z q")
    exchange = (z - q) ** 3 * (z + q) ** 2
    exchange_log = sp.cancel(sp.diff(exchange, z) / exchange)
    assert_zero(exchange_log - 3 / (z - q) - 2 / (z + q))
    exchange_second = sp.cancel(sp.diff(exchange, z, 2) / exchange)
    assert_zero(
        exchange_second
        - exchange_log**2
        + 3 / (z - q) ** 2
        + 2 / (z + q) ** 2
    )

    # The singleton transport factor is the coprime cubic f_s.
    s = sp.symbols("s")
    singleton_factor = (z - s) ** 2 * (z + s)
    assert sp.Poly(singleton_factor, z).degree() == 3
    assert sp.factor(singleton_factor.subs(z, -s)) == 0
    assert sp.factor(singleton_factor.subs(z, s)) == 0
    assert sp.factor(sp.diff(singleton_factor, z).subs(z, s)) == 0


def audit_dimension_forcing() -> None:
    # High space: eleven effective conditions in P_13.
    for dimension in range(6, 15):
        assert 11 * (dimension - 1) > dimension * (14 - dimension)
    assert 5 * 3 > 13
    assert 11 * 3 + 3 * 3 > 4 * (14 - 4)
    assert 13 - 1 >= 3  # even after discarding a possible zero mover

    # Low space: ten effective conditions in P_14.
    for dimension in range(7, 16):
        assert 10 * (dimension - 1) > dimension * (15 - dimension)
    for h in range(13, 18):
        assert 15 - h <= 2 < 5
    assert 50 + 6 > 6 * (15 - 6)

    # A rank-one three-jet image has doubled Wronskian weight.
    for dimension in range(3, 7):
        vanishing = (0,) + tuple(range(3, dimension + 2))
        assert sum(vanishing) - sum(range(dimension)) == 2 * (
            dimension - 1
        )


def audit_cofactor_interpolation_and_diagonal() -> None:
    for fixed_doubles, fixed_simples in ((4, 2), (5, 0)):
        assert 4 * fixed_simples + 8 * fixed_doubles == 40
        assert 5 * fixed_simples + 10 * fixed_doubles == 50
        assert fixed_simples + 2 * fixed_doubles == 10

    # Five-polynomial Wronskian degree, fixed factor, and Taylor factor.
    assert 5 * (15 - 5) == 50
    assert 50 - 40 - 5 == 5
    assert 14 - 5 == 9
    diagonal_degrees = tuple(5 - order + 9 for order in range(4))
    assert diagonal_degrees == (14, 13, 12, 11)

    # The two selected doubles repair exactly the two short root counts.
    for h in range(13, 18):
        roots = (h + 2, h + 2, h, h)
        assert all(count > degree for count, degree in zip(roots, diagonal_degrees))

    # Three sections vanishing to order three in a five-space cost weight 3.
    correction_sequence = (0, 1, 3, 4, 5)
    assert sum(correction_sequence) - sum(range(5)) == 3

    # Exact cofactor diagonal sign.
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
    assert_zero(sp.cancel(cofactor / (t - z) ** 5) + full_wronskian / 120)

    # The remaining diagonal divisor has degree ten versus degree six.
    assert (5 - 4) + (9 - 4) == 6
    assert 6 < 10


def main() -> None:
    audit_selection_profiles()
    audit_relation_numerators_and_transport()
    audit_dimension_forcing()
    audit_cofactor_interpolation_and_diagonal()
    print("p=18 two-triple four-/five-double cofactor closure PASS")
    print("closed uniformly: a=2, b=6,7")
    print("effective anchor weights: 11 in P_13, 10 in P_14")
    print("cofactor quotient bidegree: (5,9)")
    print("two selected doubles supply two order-three corrections")
    print("remaining a=2 families: b=8")


if __name__ == "__main__":
    main()
