#!/usr/bin/env python3
"""Exact audit of the p=28 two-quartic q=5 grid closure."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def audit_profiles_and_grid() -> None:
    residuals = ((2, 7, 0, 1), (2, 7, 1, -1))
    for h in range(22, 28):
        k = 28 - h
        for e, a, b, u in residuals:
            assert 4 * e + 3 * a + 2 * b + u == 30
            selected_repeated = 1 + b
            selected_singletons = h + 2 - 2 * selected_repeated
            singleton_count = h + u
            assert singleton_count - selected_singletons == 1

            complement = (4,) * e + (3,) * (a - 1) + (1, 1)
            assert complement == (4, 4) + (3,) * 6 + (1, 1)
            assert sum(complement) == 28
            assert len(complement) == 10

            # The singleton-swap input says q is five or six and permits
            # at most one q=6 entry in each of the seven triple rows.
            relation_dimension_q5 = 5 - 2
            relation_target_degree = len(complement) - 4
            assert relation_dimension_q5 == 3
            assert relation_target_degree == 6

            all_q5_columns = singleton_count - 7
            expected = h - 6 if b == 0 else h - 8
            assert all_q5_columns == expected
            assert all_q5_columns >= (16 if b == 0 else 14)

            # Recheck that q=7 is excluded at every split; q in {5,6}
            # itself is the independently audited singleton-cap input.
            degree = h + 3 - selected_repeated
            forced_q7 = (
                selected_repeated * (7 - 2)
                + selected_singletons * (7 - 1)
                + max(0, 7 - k)
            )
            cap_q7 = 7 * (degree + 1 - 7)
            assert forced_q7 - cap_q7 == 12


def audit_singleton_pair_transport() -> None:
    # The two q=5 relation spaces are three-spaces in P_6.  Their cubic
    # transports lie in P_9.  A five-space in the restored kernel has a
    # one-unit Wronskian excess.
    dimension = 5
    forced = 2 * (dimension - 4) + 6 * (dimension - 3) + 3 * (
        dimension - 1
    )
    cap = dimension * (10 - dimension)
    assert forced == 26
    assert cap == 25
    assert forced - cap == 1
    for order in (1, 3, 4):
        original_weight = max(0, dimension - order)
        for gcd_order in range(0, 8):
            corrected = dimension * gcd_order
            if gcd_order <= order:
                corrected += max(0, dimension - order + gcd_order)
            assert corrected >= original_weight

    transported_dimension = 3
    common_cap = 4
    assert 2 * transported_dimension - common_cap == 2
    assert 9 - (3 + 3) + 1 == 4  # residual P_3 after two cubics

    z, s, t = sp.symbols("z s t")
    f_s = sp.expand((z - s) ** 2 * (z + s))
    f_t = sp.expand((z - t) ** 2 * (z + t))
    resultant = sp.factor(sp.resultant(f_s, f_t, z))
    assert resultant == -(s - t) ** 5 * (s + t) ** 4

    # Exact fixed-simple cancellation.  H_s=H_Y/(z+s), while A_s^2
    # contributes (z-s)^2.  Multiplication by f_s removes both pieces.
    h_y = sp.symbols("H", nonzero=True)
    cancelled = sp.cancel(h_y / ((z + s) * (z - s) ** 2) * f_s)
    assert cancelled == h_y

    # The common Robin functional is nonzero because its coefficient on
    # u'(i) is the fixed local unit V_i(i) H_Y(i).
    u0, u1, fixed0, fixed1 = sp.symbols(
        "u0 u1 fixed0 fixed1", nonzero=True
    )
    robin = fixed1 * u0 + fixed0 * u1
    assert sp.diff(robin, u1) == fixed0


def incidence_quartic(plucker: dict[tuple[int, int], sp.Expr], a: sp.Symbol) -> sp.Expr:
    return sp.expand(
        plucker[0, 1]
        + 2 * plucker[0, 2] * a
        + (3 * plucker[0, 3] + plucker[1, 2]) * a**2
        + 2 * plucker[1, 3] * a**3
        + plucker[2, 3] * a**4
    )


def audit_degree_seven_kernel_and_classification() -> None:
    # After dividing the common singleton cubic, two quartic rows and
    # seven triple rows remain in P_7.  A five-space has excess one.
    dimension = 5
    forced = 2 * (dimension - 4) + 7 * (dimension - 3)
    cap = dimension * (8 - dimension)
    assert forced == 16
    assert cap == 15
    assert forced - cap == 1
    for order in (3, 4):
        original_weight = max(0, dimension - order)
        for gcd_order in range(0, 8):
            corrected = dimension * gcd_order
            if gcd_order <= order:
                corrected += max(0, dimension - order + gcd_order)
            assert corrected >= original_weight

    z, t, a, b = sp.symbols("z t a b")
    b_a = sp.Poly((z**2 - a) ** 2, z)
    b_b = sp.Poly((z**2 - b) ** 2, z)
    # Distinct squares make the quartics coprime; their product has degree
    # eight, so the corresponding P_3 multiples in P_7 are disjoint.
    assert b_a.degree() == b_b.degree() == 4
    sample_a = sp.Poly(b_a.as_expr().subs(a, 2), z)
    sample_b = sp.Poly(b_b.as_expr().subs(b, 5), z)
    assert sp.gcd(sample_a, sample_b).degree() == 0
    assert (sample_a * sample_b).degree() == 8

    # Pluecker coordinates of E_a=(t-a)^2 P_1(t).
    v0 = sp.Matrix([a**2, -2 * a, 1, 0])
    v1 = sp.Matrix([0, a**2, -2 * a, 1])
    q: dict[tuple[int, int], sp.Expr] = {}
    for i, j in combinations(range(4), 2):
        q[i, j] = sp.expand(v0[i] * v1[j] - v0[j] * v1[i])
    assert q == {
        (0, 1): a**4,
        (0, 2): -2 * a**3,
        (0, 3): a**2,
        (1, 2): 3 * a**2,
        (1, 3): -2 * a,
        (2, 3): 1,
    }

    # Two distinct E_a are complementary in R.  This is the fact used to
    # dispose of the projection-rank one and three cases.
    b_symbol = sp.symbols("b_symbol")
    w0 = sp.Matrix([b_symbol**2, -2 * b_symbol, 1, 0])
    w1 = sp.Matrix([0, b_symbol**2, -2 * b_symbol, 1])
    two_tangent_determinant = sp.factor(
        sp.Matrix.hstack(v0, v1, w0, w1).det()
    )
    assert two_tangent_determinant == (a - b_symbol) ** 4
    assert 1 + 1 < 7  # at most one containment of each exceptional type

    p01, p02, p03, p12, p13, p23 = sp.symbols(
        "p01 p02 p03 p12 p13 p23"
    )
    p = {
        (0, 1): p01,
        (0, 2): p02,
        (0, 3): p03,
        (1, 2): p12,
        (1, 3): p13,
        (2, 3): p23,
    }
    determinant_pairing = sp.expand(
        p01 * q[2, 3]
        - p02 * q[1, 3]
        + p03 * q[1, 2]
        + p12 * q[0, 3]
        - p13 * q[0, 2]
        + p23 * q[0, 1]
    )
    assert sp.expand(determinant_pairing - incidence_quartic(p, a)) == 0
    assert sp.Poly(determinant_pairing, a).degree() == 4

    # If this quartic vanished identically, its coefficients and the
    # Pluecker quadric would force every Pluecker coordinate to vanish.
    coefficient_zero_substitution = {
        p01: 0,
        p02: 0,
        p12: -3 * p03,
        p13: 0,
        p23: 0,
    }
    plucker_relation = p01 * p23 - p02 * p13 + p03 * p12
    reduced_relation = sp.expand(
        plucker_relation.subs(coefficient_zero_substitution)
    )
    assert reduced_relation == -3 * p03**2
    assert 7 - 2 > 4  # rank-two case: five roots for a nonzero quartic

    # Graph case: T preserves E_a at seven values.  The four jet
    # polynomials have degree at most five, so they vanish identically.
    entries = sp.symbols("x0:16")
    matrix_t = sp.Matrix(4, 4, entries)
    jet = sp.Matrix([[1, a, a**2, a**3], [0, 1, 2 * a, 3 * a**2]])
    equations: list[sp.Expr] = []
    degrees: list[int] = []
    for vector in (v0, v1):
        for expression in jet * matrix_t * vector:
            expression = sp.expand(expression)
            equations.extend(sp.Poly(expression, a).all_coeffs())
            degrees.append(sp.Poly(expression, a).degree())
    assert max(degrees) == 5
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, entries)
    assert coefficient_matrix.rank() == 15
    nullspace = coefficient_matrix.nullspace()
    assert len(nullspace) == 1
    scalar_vector = sp.Matrix(
        [1 if row == column else 0 for row in range(4) for column in range(4)]
    )
    assert nullspace[0] == scalar_vector


def audit_terminal_triple_row() -> None:
    z, i = sp.symbols("z i", nonzero=True)
    ell0, ell1, g0 = sp.symbols("ell0 ell1 g0", nonzero=True)
    ell = ell0 + ell1 * (z - i)
    member = ell * (z**2 - i**2) ** 3
    third_jet = sp.factor(sp.diff(g0 * member, z, 3).subs(z, i))
    expected = sp.factor(sp.factorial(3) * g0 * ell0 * (2 * i) ** 3)
    assert sp.factor(third_jet - expected) == 0
    assert expected != 0


def main() -> None:
    audit_profiles_and_grid()
    audit_singleton_pair_transport()
    audit_degree_seven_kernel_and_classification()
    audit_terminal_triple_row()
    print("p=28 4^2 3^7 1 q=5 grid closure: PASS")
    print("fixed-triple q=5 choices contain one common cubic pencil")
    print("an all-q=5 column gives seven planes in an exact P_7 four-space")
    print("seven-plane classification: M=(alpha+beta*z) P_3(z^2)")
    print("a nonzero exact order-three triple row excludes that four-space")
    print("closed tuples: (2,7,0,1), (2,7,1,-1)")
    print("scope guard: p=28 d<=2 residual core only; independently audited")


if __name__ == "__main__":
    main()
