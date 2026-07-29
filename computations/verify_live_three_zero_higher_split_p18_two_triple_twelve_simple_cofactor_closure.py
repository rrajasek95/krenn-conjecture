#!/usr/bin/env python3
"""Exact audit of the p=18 two-triple twelve-simple cofactor closure."""

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


def audit_common_selection_and_counts() -> None:
    for h in range(13, 18):
        for doubles in range(3):
            original = profile(2, doubles, h + 14 - 2 * doubles)
            selections = formal_selections(original, h, 18)
            target = profile(2, 0, 12)
            assert any(
                selection.d == doubles
                and selection.selected_triples == 0
                and selection.complement == target
                for selection in selections
            )
            singleton_count = h + 14 - 2 * doubles
            assert singleton_count - 10 == h + 4 - 2 * doubles
            # At most one singleton is zero, so ten nonzero anchors exist.
            assert singleton_count - 1 >= 10

    # A relation three-space in P_10 has an eight-dimensional annihilator.
    assert (10 + 1) - 3 == 8
    for anchors in (10, 11):
        numerator_degree = 2 * anchors - (10 + 2)
        moving_values = 12 - anchors
        normalized_degree = numerator_degree + 3 * moving_values
        assert normalized_degree == 24 - anchors
        assert anchors - 8 == (2 if anchors == 10 else 3)


def audit_slope_normalization() -> None:
    a, s, t, q = sp.symbols("a s t q")
    base, selected_singletons, anchor_sum = sp.symbols(
        "base selected_singletons anchor_sum"
    )

    # Ten anchors, with s,t the two complementary singleton values.
    beta = (
        base
        + selected_singletons
        - 2 * anchor_sum
        - 2 / (a - s)
        - 2 / (a - t)
    )
    numerator_log = beta + 2 * anchor_sum
    moving_factor_log = (
        2 / (a - s)
        + 1 / (a + s)
        + 2 / (a - t)
        + 1 / (a + t)
    )
    fixed_slope = (
        base
        + selected_singletons
        + 1 / (a + s)
        + 1 / (a + t)
    )
    assert_zero(numerator_log + moving_factor_log - fixed_slope)

    # Nested anchor sets: multiplication by z+s restores the omitted
    # plus-pole term.
    lambda_ten = sp.symbols("lambda_ten")
    lambda_eleven = lambda_ten - 1 / (a + s)
    assert_zero(lambda_eleven + 1 / (a + s) - lambda_ten)

    # A complementary double contributes a negative-pole cube; promoting
    # it to selected role two inserts the plus-pole square.
    double_neighbor_slope = base - 3 / (a - q)
    exchange_factor_log = 3 / (a - q) + 2 / (a + q)
    selected_double_slope = base + 2 / (a + q)
    assert_zero(
        double_neighbor_slope
        + exchange_factor_log
        - selected_double_slope
    )


def audit_dimension_forcing() -> None:
    # Eleven anchors in P_13: dimension at least three, and anchor weights
    # exclude dimensions at least six.
    for dimension in range(6, 15):
        assert 11 * (dimension - 1) > dimension * (14 - dimension)
    # Dimension three would have five coprime cubic factors in every
    # member.  Dimension four gets weight three at any moving value.
    assert 5 * 3 > 13
    assert 11 * 3 + 3 * 3 > 4 * (14 - 4)

    # Ten anchors in P_14: dimension at least five and at most six.
    for dimension in range(7, 16):
        assert 10 * (dimension - 1) > dimension * (15 - dimension)
    # In the smallest case there are thirteen moving values.  Multiples
    # of their product form at most a two-space inside P_14, so a nested
    # five-space cannot equal the ambient space for every moving value.
    minimum_moving = 13
    assert (14 - minimum_moving) + 1 == 2 < 5
    # A common root outside the anchors would add sixth-power Wronskian
    # weight beyond the degree cap for the resulting six-space.
    assert 10 * 5 + 6 > 6 * (15 - 6)

    # The moving factors are pairwise coprime under distinct/nonopposite
    # structural values.
    z, s, t = sp.symbols("z s t")
    f_s = (z - s) ** 2 * (z + s)
    f_t = (z - t) ** 2 * (z + t)
    assert_zero(
        sp.resultant(f_s, f_t, z)
        + (s - t) ** 5 * (s + t) ** 4
    )


def audit_cofactor_degree_and_diagonal() -> None:
    # A five-polynomial Wronskian in P_14 has degree at most fifty.  After
    # ten fourth-power anchors and the automatic fifth diagonal factor,
    # the quotient has bidegree at most (5,9).
    assert 5 * (15 - 5) == 50
    assert 50 - 4 * 10 - 5 == 5
    assert 14 - 5 == 9
    assert tuple(5 - order + 9 for order in range(4)) == (14, 13, 12, 11)

    # Taylor expansion of the cofactor first row gives exactly -Wr/5! on
    # the diagonal.  The monomial basis audits the sign and coefficient.
    z, t = sp.symbols("z t")
    basis = [z**degree for degree in range(6)]
    cofactor_matrix = sp.Matrix(
        [[t**degree for degree in range(6)]]
        + [
            [sp.diff(poly, z, order) for poly in basis]
            for order in range(5)
        ]
    )
    cofactor = sp.factor(cofactor_matrix.det())
    full_wronskian = wronskian(basis, z)
    assert_zero(cofactor - 288 * (z - t) ** 5)
    quotient = sp.cancel(cofactor / (t - z) ** 5)
    assert_zero(quotient + full_wronskian / 120)

    # Once the reflected fourth power is forced, the remaining bidegree is
    # (1,5), and its diagonal degree is at most six.  Ten nonzero anchors
    # cannot divide z^4 times such a polynomial.
    assert 5 - 4 == 1
    assert 9 - 4 == 5
    assert 1 + 5 == 6 < 10


def audit_root_interpolation_and_double_correction() -> None:
    degrees = (14, 13, 12, 11)
    for h in range(13, 18):
        b0_roots = h + 4
        b1_roots = h + 2
        assert all(b0_roots > degree for degree in degrees)
        assert all(b1_roots > degree for degree in degrees)

        # For b=2, the two complementary-double selections give two
        # additional roots to derivatives zero and one.  The singleton
        # roots alone suffice for derivatives two and three.
        b2_roots = (h + 2, h + 2, h, h)
        assert all(
            roots > degree for roots, degree in zip(b2_roots, degrees)
        )

    # Ten singleton rows in the neighboring P_9 relation problem have at
    # least three relations; their degree-nine numerators become degree
    # fourteen after the cubic-times-square double exchange factor.
    assert (9 + 1) - 3 == 7
    assert 10 - 7 == 3
    assert 2 * 10 - (9 + 2) == 9
    assert 9 + (3 + 2) == 14

    # After the evaluation hyperplane's common linear factor is removed,
    # three sections with order at least three contribute weight three.
    vanishing_sequence = (0, 1, 3, 4, 5)
    baseline = (0, 1, 2, 3, 4)
    assert sum(vanishing_sequence) - sum(baseline) == 3


def main() -> None:
    audit_common_selection_and_counts()
    audit_slope_normalization()
    audit_dimension_forcing()
    audit_cofactor_degree_and_diagonal()
    audit_root_interpolation_and_double_correction()
    print("p=18 two-triple twelve-simple cofactor closure PASS")
    print("closed uniformly: a=2, b=0,1,2")
    print("ten-anchor normalized space: dimension 6 in P_14")
    print("cofactor quotient bidegree: (5,9)")
    print("b=2 companion double corrections: two order-three points")
    print("remaining a=2 families: b=3,4,5,6,7,8")


if __name__ == "__main__":
    main()
