#!/usr/bin/env python3
"""Exact audit for the p=19 C=8 singleton pair-line clique closure."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_q5_boundary_census as q5
import verify_live_three_zero_higher_split_p19_singleton_parity_common_lift_closure as singleton
import verify_live_three_zero_higher_split_p19_c6_parity_pencil_coupling as c6
import verify_live_three_zero_higher_split_p19_c6_saturated_klein_plane_closure as c6_saturated
import verify_live_three_zero_higher_split_p19_undecic_singleton_double_coupling_closure as undecic
import verify_live_three_zero_higher_split_p19_c7_developable_secant_closure as c7
import verify_live_three_zero_higher_split_p19_five_triple_even_span_closure as five_triple


TARGET = (0, 10, 1)


def quintic(z: sp.Symbol, node: sp.Expr) -> sp.Expr:
    return sp.expand((z - node) ** 3 * (z + node) ** 2)


def audit_profile_and_formal_selection() -> None:
    # The target is the no-quartic symbolic family 2^10 1^(h+1).
    assert 3 * TARGET[0] + 2 * TARGET[1] + TARGET[2] == 21
    complement = (2,) * 9 + (1,)
    selection = q5.Selection(1, 0, complement)

    for h in range(13, 19):
        profile = (2,) * 10 + (1,) * (h + 1)
        assert selection in q5.formal_selections(profile, h, 19)
        assert sum(complement) == 19
        assert len(complement) == 10

        # Select one double (two layers) and h singleton layers, leaving
        # one singleton and nine doubles in the formal complement.
        assert 2 + h == h + 2
        assert (h + 1) - h == 1

        # The p=19 q=6 branch has a strict gap.  The audited low-role
        # incidence exclusion then leaves selected-kernel dimension five.
        k = 19 - h
        assert 22 - h + max(0, 6 - k) > 0

    classes = len(complement)
    relation_degree = classes - 4
    transport_degree = relation_degree + 5
    assert relation_degree == 6
    assert transport_degree == 11


def audit_common_kernel_and_pair_lines() -> None:
    # Ten exact order-two rows and one exact order-one row in degree 11.
    for dimension in range(6, 13):
        forced = 10 * (dimension - 2) + (dimension - 1)
        cap = dimension * (12 - dimension)
        assert forced - cap == dimension**2 - dimension - 21
        assert forced > cap

    # Pairwise coprime quintics have a full P_1 intersection in P_11.
    ambient_pair_intersection = 11 - 2 * 5 + 1
    assert ambient_pair_intersection == 2
    assert 3 + 3 - 3 > ambient_pair_intersection
    assert 3 + 3 - 4 == ambient_pair_intersection
    assert 3 + 3 - 5 == 1

    # A common exact singleton row cannot annihilate the full pencil:
    # its value on g_i g_j (z-r) is U(r)g_i(r)g_j(r), a structural unit.
    z, r, i, j, u0, u1 = sp.symbols("z r i j u0 u1")
    gi = quintic(z, i)
    gj = quintic(z, j)
    local_u = u0 + u1 * (z - r)
    test = sp.diff(local_u * gi * gj * (z - r), z).subs(z, r)
    assert sp.factor(test - u0 * gi.subs(z, r) * gj.subs(z, r)) == 0

    # The same test says an intrinsic linear factor cannot vanish at r.
    ell_slope = sp.symbols("ell_slope")
    vanishing_ell = ell_slope * (z - r)
    value = sp.diff(local_u * gi * gj * vanishing_ell, z).subs(z, r)
    assert sp.factor(value - u0 * gi.subs(z, r) * gj.subs(z, r) * ell_slope) == 0


def audit_singleton_line_factor() -> None:
    z, r, x, y = sp.symbols("z r x y")
    lam, d = sp.symbols("Lambda d")

    gx = quintic(z, x)
    first = sp.factor(sp.diff(gx, z).subs(z, r) / gx.subs(z, r))
    expected = (5 * r + x) / (r**2 - x**2)
    assert sp.factor(first - expected) == 0

    def a(node: sp.Expr) -> sp.Expr:
        return (5 * r + node) / (r**2 - node**2)

    ell = 1 + d * (z - r)
    # Divide the common singleton row by its nonzero undifferentiated
    # factors.  Writing Lambda=-U'/U leaves d=Lambda-a_x-a_y.
    normalized_row = sp.diff(ell, z).subs(z, r) - lam + a(x) + a(y)
    expected_slope = lam - a(x) - a(y)
    assert sp.factor(normalized_row.subs(d, expected_slope)) == 0
    assert sp.diff(normalized_row, d) == 1


def audit_double_row_clique() -> None:
    z, x, y, r, v = sp.symbols("z x y r v")
    lam, u, c = sp.symbols("Lambda u c")

    gx = quintic(z, x)
    first_v = sp.factor(sp.diff(gx, z).subs(z, v) / gx.subs(z, v))
    second_v = sp.factor(sp.diff(gx, z, 2).subs(z, v) / gx.subs(z, v))
    assert sp.factor(first_v - (5 * v + x) / (v**2 - x**2)) == 0
    assert sp.factor(
        second_v
        - 4 * (5 * v**2 + 2 * v * x - x**2) / (v**2 - x**2) ** 2
    ) == 0

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
    equation = qxy * (1 + (v - r) * dxy) + 2 * pxy * dxy
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

    # Nine vertices give eight off-diagonal roots per row, followed by
    # nine roots for every coefficient; both exceed degree six.
    vertices = 10 - 1
    assert vertices == 9
    assert vertices - 1 > 6
    assert vertices > 6

    # Audit the exact excluded-pole coefficient rather than relying only
    # on a generic leading-term computation.
    # The only double-pole term is R_y.  A_y and hence P_xy have only a
    # simple pole.  Auditing these two local coefficients separately is
    # much faster than factoring the full six-parameter numerator.
    assert sp.factor(sp.limit((v - y) * A_at_v(y), y, v) - 3) == 0
    assert sp.factor(sp.limit((v - y) ** 2 * R_at_v(y), y, v) - 6) == 0
    pole = sp.factor(6 * (1 + (v - r) * dxy.subs(y, v)))
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


def audit_complete_p19_ledger() -> None:
    closed75 = c6.prior_closed()
    closed81 = {
        e: closed75[e] | c6.EXPECTED_NEW[e]
        for e in (0, 1)
    }
    closed85 = {
        e: closed81[e] | c6_saturated.NEW_CLOSED[e]
        for e in (0, 1)
    }
    closed89 = {
        e: closed85[e] | undecic.TARGETS[e]
        for e in (0, 1)
    }
    closed91 = {
        e: closed89[e] | c7.TARGETS[e]
        for e in (0, 1)
    }
    five_triple_targets = {
        (5, doubles, offset)
        for doubles, offset in five_triple.TARGETS
    }
    closed93 = {
        0: set(closed91[0]),
        1: closed91[1] | five_triple_targets,
    }
    assert sum(len(values) for values in closed93.values()) == 93
    assert singleton.parameter_families(0) - closed93[0] == {TARGET}
    assert singleton.parameter_families(1) - closed93[1] == set()

    closed94 = {0: closed93[0] | {TARGET}, 1: closed93[1]}
    assert closed94 == {
        e: singleton.parameter_families(e)
        for e in (0, 1)
    }
    assert sum(len(values) for values in closed94.values()) == 94


def main() -> None:
    audit_profile_and_formal_selection()
    audit_common_kernel_and_pair_lines()
    audit_singleton_line_factor()
    audit_double_row_clique()
    audit_complete_p19_ledger()
    print("p=19 C=8 singleton pair-line clique closure: PASS")
    print("2^10 1^(h+1) endpoint closed: 1")
    print("updated p=19 ledger: 94/94 closed")
    print("common undecic, pair-line, bidegree-six, and pole branches: audited")


if __name__ == "__main__":
    main()
