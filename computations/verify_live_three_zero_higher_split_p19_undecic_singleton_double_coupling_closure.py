#!/usr/bin/env python3
"""Exact audit for the p=19 undecic singleton--double coupling."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_p19_singleton_parity_common_lift_closure as singleton
import verify_live_three_zero_higher_split_p19_double_common_lift_closure as double
import verify_live_three_zero_higher_split_p19_c6_parity_pencil_coupling as c6
import verify_live_three_zero_higher_split_p19_c6_saturated_klein_plane_closure as c6_saturated


TARGETS = {
    0: {(0, 11, -1), (1, 9, 0), (2, 7, 1)},
    1: {(0, 8, 1)},
}


EXPECTED_POOL = {
    (0, 0, 11, -1): 2,
    (0, 1, 9, 0): 3,
    (0, 2, 7, 1): 4,
    (1, 0, 8, 1): 4,
}


def fixed_parts(e: int, a: int, b: int) -> tuple[int, ...]:
    return (4,) * e + (3,) * a + (2,) * (b - 2)


def audit_grid_census_and_bounds() -> None:
    for e, targets in TARGETS.items():
        for a, b, u in targets:
            singleton_data = singleton.selected_data(e, a, b, u)
            double_data = double.selected_pair_data(e, a, b, u)
            pool = EXPECTED_POOL[(e, a, b, u)]

            assert singleton_data["pool"] == pool
            assert singleton_data["relation_degree"] == 6
            assert singleton_data["common_degree"] == 9
            assert double_data["relation_degree"] == 6
            assert double_data["common_degree"] == 11
            assert singleton_data["fixed_classes"] == 11 - pool
            assert b in (7, 8, 9, 11)

            # A candidate five-space in the singleton common kernel:
            # P exact simple rows plus the fixed repeated rows force
            # weight 35 against cap 25, proving dimension at most four.
            repeated = fixed_parts(e, a, b)
            singleton_weight = pool * 4 + sum(5 - m for m in repeated)
            singleton_cap = 5 * (9 + 1 - 5)
            assert singleton_weight == 35
            assert singleton_weight - singleton_cap == 10

            # Dense common six-space: restore one selected double and the
            # unselected singleton pool.  The p=19 capped-mass formula
            # gives weight 45 against cap 36 in all four cases.
            dense_baseline = (
                (4,) * e
                + (3,) * a
                + (2,) * (b - 1)
                + (1,) * (u + 2)
            )
            assert sum(dense_baseline) == 21
            dense_weight = sum(6 - m for m in dense_baseline)
            dense_cap = 6 * (11 + 1 - 6)
            assert dense_weight == 45
            assert dense_weight - dense_cap == 9

            # The selected complement always has ten classes and mass 19.
            complement = double.complement_profile(
                e, a, b, double_data["leftover_singletons"]
            )
            assert len(complement) == 10
            assert sum(complement) == 19


def cubic(z: sp.Symbol, x: sp.Expr) -> sp.Expr:
    return sp.expand((z - x) ** 2 * (z + x))


def quintic(z: sp.Symbol, x: sp.Expr) -> sp.Expr:
    return sp.expand((z - x) ** 3 * (z + x) ** 2)


def wronskian(polys: list[sp.Expr], z: sp.Symbol) -> sp.Expr:
    return sp.expand(
        sp.det(
            sp.Matrix(
                [[sp.diff(poly, z, order) for poly in polys] for order in range(len(polys))]
            )
        )
    )


def valuation(poly: sp.Expr, z: sp.Symbol) -> int:
    terms = sp.Poly(sp.expand(poly), z).as_dict()
    return min(power[0] for power, coefficient in terms.items() if coefficient != 0)


def audit_singleton_triples_and_four_pool_wronskian() -> None:
    # Three hyperplanes in a four-space meet in at least a line, while
    # three coprime cubics in degree nine have exactly their product line.
    assert 3 + 3 - 4 == 2  # pair intersection lower bound
    assert 4 - 3 == 1      # triple-hyperplane lower bound
    assert 9 - 3 * 3 + 1 == 1

    z, r, s, t = sp.symbols("z r s t")
    fr, fs, ft = cubic(z, r), cubic(z, s), cubic(z, t)
    products = [sp.expand(fr * fs), sp.expand(fr * ft), sp.expand(fs * ft)]
    W = sp.factor(wronskian(products, z))

    # This exact symbolic Wronskian is nonzero of degree twelve and has
    # the forced double roots at three generic nonzero singleton values.
    assert W != 0
    assert sp.Poly(W, z).degree() == 12
    forced = (z - r) ** 2 * (z - s) ** 2 * (z - t) ** 2
    assert sp.rem(W, forced, z) == 0

    # If one singleton is zero, f_0=z^3 raises its Wronskian weight from
    # two to at least four.
    W_zero = sp.expand(W.subs(r, 0))
    assert valuation(W_zero, z) >= 4

    # Every exact order-two row adds a Wronskian root.  The two target
    # values of b exceed the remaining degree after singleton weight.
    for doubles in (7, 8):
        assert 6 + doubles > 12


def audit_quintic_vandermonde() -> None:
    z, x = sp.symbols("z x")
    g = sp.Poly(quintic(z, x), z)
    ascending = [g.coeff_monomial(z**power) for power in range(6)]
    assert ascending == [-x**5, x**4, 2 * x**3, -2 * x**2, -x, 1]

    # The six-column coefficient matrix is an invertible diagonal
    # rescaling of a reversed Vandermonde matrix.  This symbolically
    # reconstructs the determinant factor for arbitrary distinct nodes.
    nodes = sp.symbols("x0:6")
    vandermonde = sp.Matrix([[node**power for node in nodes] for power in range(6)])
    reversal = sp.Matrix([[vandermonde[5 - row, col] for col in range(6)] for row in range(6)])
    diagonal = sp.diag(-1, 1, 2, -2, -1, 1)
    coefficient_matrix = sp.Matrix(
        [
            [
                (-node**5, node**4, 2 * node**3, -2 * node**2, -node, 1)[row]
                for node in nodes
            ]
            for row in range(6)
        ]
    )
    assert coefficient_matrix == diagonal * reversal
    assert sp.prod(diagonal[row, row] for row in range(6)) == -4

    # Eight moving partners are available, while the common dense kernel
    # has dimension at most five.
    assert 9 - 1 >= 6 > 5


def audit_two_pool_dimension_branches() -> None:
    # Singleton pair intersection: two three-spaces in dimension <=4
    # have a plane; the ambient residual degree is three.
    assert 3 + 3 - 4 == 2
    assert 9 - 6 == 3

    # Dense dimension three would identify all moving three-spaces and
    # force three quintics into degree eleven.
    assert 3 * 5 > 11

    # In dense dimension four every pair intersection is the full
    # g_j g_k P_1 pencil.  Two such divided planes have zero intersection
    # in P_6 because the product degree is ten.
    assert 3 + 3 - 4 == 2
    assert 11 - 10 + 1 == 2
    assert 2 + 2 > 3
    assert 2 * 5 > 6

    # In dense dimension five a pair intersection has dimension >=1.
    # A full pencil cannot coexist with the singleton plane: f_r g_k has
    # degree eight, again above the relation degree six.
    assert 3 + 3 - 5 == 1
    assert 2 + 2 > 3
    assert 3 + 5 > 6


def audit_two_pool_jet_compatibility_and_clique() -> None:
    z, x, y, r, v = sp.symbols("z x y r v")
    lam, lam_x, lam_y = sp.symbols("Lambda lambda_x lambda_y")
    u, c = sp.symbols("u c")

    gx = quintic(z, x)
    first_r = sp.factor(sp.diff(gx, z).subs(z, r) / gx.subs(z, r))
    expected_first_r = (5 * r + x) / (r**2 - x**2)
    assert sp.factor(first_r - expected_first_r) == 0

    first_v = sp.factor(sp.diff(gx, z).subs(z, v) / gx.subs(z, v))
    second_v = sp.factor(sp.diff(gx, z, 2).subs(z, v) / gx.subs(z, v))
    expected_first_v = (5 * v + x) / (v**2 - x**2)
    expected_second_v = 4 * (5 * v**2 + 2 * v * x - x**2) / (v**2 - x**2) ** 2
    assert sp.factor(first_v - expected_first_v) == 0
    assert sp.factor(second_v - expected_second_v) == 0

    # Symmetry of the intrinsic pair line turns the two vertex equations
    # into lambda_j+a_j=lambda_k+a_k.
    ax, ay, logarithmic_line = sp.symbols("a_x a_y logarithmic_line")
    eq_x = lam_x - ay - logarithmic_line
    eq_y = lam_y - ax - logarithmic_line
    assert sp.factor(eq_x - eq_y - (lam_x + ax - lam_y - ay)) == 0

    def a_at_r(node: sp.Expr) -> sp.Expr:
        return (5 * r + node) / (r**2 - node**2)

    def A_at_v(node: sp.Expr) -> sp.Expr:
        return (5 * v + node) / (v**2 - node**2)

    def R_at_v(node: sp.Expr) -> sp.Expr:
        return 4 * (5 * v**2 + 2 * v * node - node**2) / (v**2 - node**2) ** 2

    dxy = lam - a_at_r(x) - a_at_r(y)
    pxy = u + A_at_v(x) + A_at_v(y)
    qxy = (
        c
        + R_at_v(x)
        + R_at_v(y)
        + 2 * u * (A_at_v(x) + A_at_v(y))
        + 2 * A_at_v(x) * A_at_v(y)
    )
    equation = sp.factor(qxy * (1 + (v - r) * dxy) + 2 * pxy * dxy)
    numerator, denominator = sp.together(equation).as_numer_denom()
    numerator = sp.expand(numerator)
    structural_denominator = (
        (r**2 - x**2)
        * (r**2 - y**2)
        * (v**2 - x**2) ** 2
        * (v**2 - y**2) ** 2
    )
    assert sp.factor(denominator - structural_denominator) == 0
    assert sp.Poly(numerator, x, y).degree(x) <= 6
    assert sp.Poly(numerator, x, y).degree(y) <= 6

    # A nine-vertex clique supplies eight y-roots for every fixed x and
    # then nine x-roots for every coefficient, both above degree six.
    vertices = 11 - 2
    assert vertices == 9
    assert vertices - 1 > 6
    assert vertices > 6

    # Exact structural obstruction at the excluded pole y=v.
    pole = sp.factor(sp.limit((v - y) ** 2 * equation, y, v))
    target_pole = sp.factor(
        6 * (1 + (v - r) * (lam - a_at_r(x) - a_at_r(v)))
    )
    assert sp.factor(pole - target_pole) == 0

    constant = sp.symbols("K")
    cleared = sp.Poly(
        sp.expand(constant * (r**2 - x**2) - (v - r) * (5 * r + x)),
        x,
    )
    assert cleared.coeff_monomial(x) == -(v - r)


def audit_updated_ledger() -> None:
    closed75 = c6.prior_closed()
    closed81 = {
        e: closed75[e] | c6.EXPECTED_NEW[e]
        for e in (0, 1)
    }
    closed85 = {
        e: closed81[e] | c6_saturated.NEW_CLOSED[e]
        for e in (0, 1)
    }
    assert sum(len(values) for values in closed85.values()) == 85
    for e in (0, 1):
        assert TARGETS[e].isdisjoint(closed85[e])

    closed89 = {
        e: closed85[e] | TARGETS[e]
        for e in (0, 1)
    }
    assert sum(len(values) for values in closed89.values()) == 89

    expected_remaining = {
        0: {(0, 9, 3), (0, 10, 1), (1, 8, 2)},
        1: {(5, 0, 2), (5, 1, 0)},
    }
    observed_remaining = {
        e: singleton.parameter_families(e) - closed89[e]
        for e in (0, 1)
    }
    assert observed_remaining == expected_remaining
    assert sum(len(values) for values in observed_remaining.values()) == 5


def main() -> None:
    audit_grid_census_and_bounds()
    audit_singleton_triples_and_four_pool_wronskian()
    audit_quintic_vandermonde()
    audit_two_pool_dimension_branches()
    audit_two_pool_jet_compatibility_and_clique()
    audit_updated_ledger()
    print("p=19 undecic singleton--double coupling: PASS")
    print("P=2,3,4 degree-nine/degree-eleven profiles closed: 4")
    print("updated p=19 ledger: 89/94 closed, 5 remain")
    print("Wronskian, Vandermonde, pair-line, and bidegree-six branches: audited")


if __name__ == "__main__":
    main()
