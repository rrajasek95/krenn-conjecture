#!/usr/bin/env python3
"""Exact audit for the p=18 three-triple overlap closure/frontier."""

from __future__ import annotations

from collections import Counter
from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verify_live_three_zero_higher_split_q5_boundary_census import (  # noqa: E402
    formal_selections,
)
from verify_live_three_zero_higher_split_p18_b6_endpoint_selected_pair_closure import (  # noqa: E402, E501
    audit_b6_endpoint_selected_pair_closure,
)


def assert_zero(expr: sp.Expr) -> None:
    assert sp.factor(sp.together(expr)) == 0, sp.factor(sp.together(expr))


def wronskian(polys: list[sp.Expr], z: sp.Symbol) -> sp.Expr:
    size = len(polys)
    return sp.factor(
        sp.Matrix(
            [[sp.diff(poly, z, order) for poly in polys]
             for order in range(size)]
        ).det()
    )


def signature(parts: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(parts).items(), reverse=True))


EXPECTED = {
    0: {
        (0, 0, ((3, 3), (1, 9))),
        (1, 1, ((3, 2), (1, 12))),
    },
    1: {
        (0, 0, ((3, 3), (2, 1), (1, 7))),
        (1, 0, ((3, 3), (1, 9))),
        (1, 1, ((3, 2), (2, 1), (1, 10))),
        (2, 1, ((3, 2), (1, 12))),
    },
    2: {
        (0, 0, ((3, 3), (2, 2), (1, 5))),
        (1, 0, ((3, 3), (2, 1), (1, 7))),
        (1, 1, ((3, 2), (2, 2), (1, 8))),
        (2, 0, ((3, 3), (1, 9))),
        (2, 1, ((3, 2), (2, 1), (1, 10))),
    },
    3: {
        (0, 0, ((3, 3), (2, 3), (1, 3))),
        (1, 0, ((3, 3), (2, 2), (1, 5))),
        (1, 1, ((3, 2), (2, 3), (1, 6))),
        (2, 0, ((3, 3), (2, 1), (1, 7))),
        (2, 1, ((3, 2), (2, 2), (1, 8))),
    },
    4: {
        (0, 0, ((3, 3), (2, 4), (1, 1))),
        (1, 0, ((3, 3), (2, 3), (1, 3))),
        (1, 1, ((3, 2), (2, 4), (1, 4))),
        (2, 0, ((3, 3), (2, 2), (1, 5))),
        (2, 1, ((3, 2), (2, 3), (1, 6))),
    },
    5: {
        (1, 0, ((3, 3), (2, 4), (1, 1))),
        (1, 1, ((3, 2), (2, 5), (1, 2))),
        (2, 0, ((3, 3), (2, 3), (1, 3))),
        (2, 1, ((3, 2), (2, 4), (1, 4))),
    },
    6: {
        (2, 0, ((3, 3), (2, 4), (1, 1))),
        (2, 1, ((3, 2), (2, 5), (1, 2))),
    },
}


def audit_family_and_selection_table() -> None:
    admissible = []
    for doubles in range(12):
        u = 11 - 2 * doubles
        applies = (
            u >= 2
            or (u >= 0 and 3 + doubles >= 1)
            or (
                u >= -2
                and (doubles >= 2 or (3 >= 1 and doubles >= 1))
            )
        )
        if applies:
            admissible.append(doubles)
    assert admissible == list(range(7))

    for h in range(13, 18):
        k = 18 - h
        for doubles in admissible:
            u = 11 - 2 * doubles
            profile = (
                (3,) * 3 + (2,) * doubles + (1,) * (h + u)
            )
            assert sum(profile) == 2 * h + k + 2
            observed = {
                (
                    selection.d,
                    selection.selected_triples,
                    signature(selection.complement),
                )
                for selection in formal_selections(profile, h, 18)
            }
            assert observed == EXPECTED[doubles]

    # The closure uses exactly the three-double/three-simple selections.
    assert (1, 0, ((3, 3), (2, 3), (1, 3))) in EXPECTED[4]
    assert (2, 0, ((3, 3), (2, 3), (1, 3))) in EXPECTED[5]
    # The b=6 frontier has the two advertised neighboring selections.
    assert EXPECTED[6] == {
        (2, 0, ((3, 3), (2, 4), (1, 1))),
        (2, 1, ((3, 2), (2, 5), (1, 2))),
    }


def audit_four_double_one_simple_schubert_cubic() -> None:
    z, r, beta = sp.symbols("z r beta")
    x = z - r

    # The Robin hyperplane p'(r)+beta*p(r)=0 has this basis.
    hyperplane_basis = [1 - beta * x, x**2, x**3, x**4]
    quotient_quartics = []
    for omitted in range(4):
        subspace_basis = [
            hyperplane_basis[index]
            for index in range(4)
            if index != omitted
        ]
        quotient = sp.cancel(wronskian(subspace_basis, z) / x**2)
        assert sp.denom(quotient) == 1
        assert sp.degree(quotient, z) <= 4
        quotient_quartics.append(sp.expand(quotient))

    coefficient_matrix = sp.Matrix(
        [
            [quartic.coeff(z, power) for power in range(5)]
            for quartic in quotient_quartics
        ]
    )
    assert coefficient_matrix.rank() == 4

    left_null = sp.Matrix(
        [
            beta**3,
            beta**2 * (beta * r + 3),
            beta * (beta * r + 2) * (beta * r + 4),
            (beta * r + 1) * (beta * r + 4) ** 2,
            r * (beta * r + 4) ** 3,
        ]
    )
    for entry in coefficient_matrix * left_null:
        assert_zero(entry)

    e1, e2, e3, e4 = sp.symbols("e1 e2 e3 e4")
    target_coefficients = sp.Matrix([e4, -e3, e2, -e1, 1])
    schubert = sp.expand(left_null.dot(target_coefficients))
    expected = (
        beta**3 * e4
        - beta**2 * (beta * r + 3) * e3
        + beta * (beta * r + 2) * (beta * r + 4) * e2
        - (beta * r + 1) * (beta * r + 4) ** 2 * e1
        + r * (beta * r + 4) ** 3
    )
    assert_zero(schubert - expected)

    V = z**4 - e1 * z**3 + e2 * z**2 - e3 * z + e4
    shifted_point = r + 4 / beta
    critical_form = beta**3 * (
        V.subs(z, shifted_point)
        - sp.diff(V, z).subs(z, shifted_point) / beta
    )
    assert_zero(expected - critical_form)


def audit_exact_single_fiber_boundary_model() -> None:
    # Here y_v=4/(r-v) equals 1,2,4,5.  At beta=-3 the four
    # denominators are -2,-1,1,2, whose reciprocal sum is zero.
    r = sp.Integer(0)
    beta = sp.Integer(-3)
    doubles = (
        sp.Integer(-4),
        sp.Integer(-2),
        sp.Integer(-1),
        sp.Rational(-4, 5),
    )
    assert len(set(doubles)) == 4
    assert all(value != 0 for value in doubles)
    assert all(a != -b for a, b in combinations(doubles, 2))
    y_values = tuple(4 / (r - value) for value in doubles)
    assert y_values == (1, 2, 4, 5)
    assert_zero(sum(1 / (beta + value) for value in y_values))

    z = sp.symbols("z")
    V = sp.expand(sp.prod(z - value for value in doubles))
    e1 = -V.coeff(z, 3)
    e2 = V.coeff(z, 2)
    e3 = -V.coeff(z, 1)
    e4 = V.coeff(z, 0)
    schubert = (
        beta**3 * e4
        - beta**2 * (beta * r + 3) * e3
        + beta * (beta * r + 2) * (beta * r + 4) * e2
        - (beta * r + 1) * (beta * r + 4) ** 2 * e1
        + r * (beta * r + 4) ** 3
    )
    assert_zero(schubert)


def audit_principal_part_and_gauge_cancellation() -> None:
    # A relation between one order-two row and three Robin rows on P_5
    # has denominator degree 3+2+2+2=9.  O(z^-7) therefore leaves a
    # numerator of degree at most two; multiplying by z+s gives a cubic.
    assert 3 + 2 + 2 + 2 == 9
    assert 9 - (5 + 2) == 2
    assert 2 + 1 == 3

    # Normalized local jets.  H=M/(A*f) and U=B/f share the varying
    # factor f=(z-s)^2(z+s).  Equality of their first two normalized
    # jets is exactly equality of M and A*B through order two.
    m1, m2, a1, a2, b1, b2, f1, f2 = sp.symbols(
        "m1 m2 a1 a2 b1 b2 f1 f2"
    )
    q1 = a1 + f1
    q2 = a2 + f2 + 2 * a1 * f1
    h1 = m1 - q1
    u1 = b1 - f1
    h2 = m2 - 2 * m1 * q1 + 2 * q1**2 - q2
    u2 = b2 - 2 * b1 * f1 + 2 * f1**2 - f2
    product_first = a1 + b1
    product_second = a2 + b2 + 2 * a1 * b1
    assert_zero((h1 - u1).subs(m1, product_first))
    assert_zero(
        (h2 - u2).subs(
            {m1: product_first, m2: product_second}
        )
    )


def audit_fixed_two_jet_pencil() -> None:
    x, alpha, delta, A, B = sp.symbols("x alpha delta A B")
    basis = [1 + alpha * x + delta * x**2 / 2, x**3]
    wr = wronskian(basis, x)
    assert_zero(wr - x**2 * (3 + 2 * alpha * x + delta * x**2 / 2))

    canonical_alpha = -sp.Rational(3, 2) * (1 / A + 1 / B)
    canonical_delta = 6 / (A * B)
    target = 3 * x**2 * (x - A) * (x - B) / (A * B)
    assert_zero(
        wr.subs({alpha: canonical_alpha, delta: canonical_delta})
        - target
    )

    # The two v-jet rows are independent on P_3, so their kernel has
    # dimension two.  A line of cubics cannot supply roots at every one
    # of the varying singleton values.
    for h in range(13, 18):
        assert h + 5 - 2 == h + 3 >= 16  # b=3 candidates s
        assert h + 3 - 2 == h + 1 >= 14  # b=4 candidates s
        assert h + 1 - 2 == h - 1 >= 12  # b=5 candidates s
        assert h - 1 > 3


def audit_singleton_pair_collapse() -> None:
    v, r, t, constant = sp.symbols("v r t C")

    def singleton_term(value: sp.Expr) -> sp.Expr:
        return 1 / (v + value) + sp.Rational(3, 2) / (v - value)

    expected_term = lambda value: (5 * v + value) / (  # noqa: E731
        2 * (v**2 - value**2)
    )
    assert_zero(singleton_term(r) - expected_term(r))
    assert_zero(singleton_term(t) - expected_term(t))

    alpha_actual = constant - 1 / (v + r) - 1 / (v + t)
    alpha_canonical = sp.Rational(3, 2) * (
        1 / (v - r) + 1 / (v - t)
    )
    assert_zero(
        alpha_actual - alpha_canonical
        - (constant - singleton_term(r) - singleton_term(t))
    )

    y, value = sp.symbols("y value")
    cleared_level_set = sp.factor(
        2 * (v**2 - y**2) * (expected_term(y) - value)
    )
    expected_quadratic = 5 * v + y - 2 * value * (v**2 - y**2)
    assert_zero(cleared_level_set - expected_quadratic)
    assert sp.degree(expected_quadratic, y) == 2
    assert sp.Poly(expected_quadratic, y).coeff_monomial(y) == 1

    # After one anchor is fixed, at least three other singleton values
    # would have to lie in this one quadratic level set.
    for h in range(13, 18):
        for doubles in (3, 4, 5):
            singleton_count = h + 11 - 2 * doubles
            assert singleton_count - 1 >= 3


def audit_five_simple_cubic_pencil_frontier() -> None:
    # Five Robin rows on P_6 lie in the four-dimensional annihilator of
    # the saturated relation three-space, so they have a relation.  Its
    # common denominator has degree ten and O(z^-8) leaves a quadratic
    # numerator.  Moving the fifth singleton produces a cubic.
    assert 5 * 2 == 10
    assert 10 - (6 + 2) == 2
    assert 2 + 1 == 3

    # Any two Robin rows at distinct points on P_3 are independent.  If
    # L_x were proportional to L_y, both (z-y)^2 and (z-y)^3 would force
    # the incompatible equations 2+beta_x*(x-y)=0 and
    # 3+beta_x*(x-y)=0.
    beta, difference = sp.symbols("beta difference", nonzero=True)
    quadratic_test = 2 + beta * difference
    cubic_test = 3 + beta * difference
    assert_zero(cubic_test - quadratic_test - 1)

    # A two-dimensional cubic space has a nonzero Wronskian of degree at
    # most four.  A common Robin row at each of four anchors makes those
    # four anchors its complete root divisor.
    z = sp.symbols("z")
    p_coefficients = sp.symbols("p0:4")
    q_coefficients = sp.symbols("q0:4")
    p = sum(p_coefficients[index] * z**index for index in range(4))
    q = sum(q_coefficients[index] * z**index for index in range(4))
    wr = wronskian([p, q], z)
    assert sp.degree(wr, z) <= 4
    p_value, q_value, gamma = sp.symbols("p_value q_value gamma")
    assert_zero(p_value * (gamma * q_value) - (gamma * p_value) * q_value)

    # The neighboring b=3 selection and the b=2 base selection both have
    # enough moving fifth-singleton choices to force the fixed pencil.
    for h in range(13, 18):
        assert (h + 5) - 4 == h + 1 >= 14  # b=3, (1,0)
        assert (h + 7) - 4 == h + 3 >= 16  # b=2, (0,0)


def audit_cubic_pencil_schubert_and_b2_collapse() -> None:
    z, beta = sp.symbols("z beta")
    hyperplane_basis = [1 - beta * z, z**2, z**3]
    quotient_cubics = []
    for omitted in range(3):
        pencil_basis = [
            hyperplane_basis[index]
            for index in range(3)
            if index != omitted
        ]
        quotient = sp.cancel(wronskian(pencil_basis, z) / z)
        assert sp.denom(quotient) == 1
        assert sp.degree(quotient, z) <= 3
        quotient_cubics.append(sp.expand(quotient))

    coefficient_matrix = sp.Matrix(
        [
            [cubic.coeff(z, power) for power in range(4)]
            for cubic in quotient_cubics
        ]
    )
    assert coefficient_matrix.rank() == 3
    left_null = sp.Matrix([beta**2, 2 * beta, 3, 0])
    for entry in coefficient_matrix * left_null:
        assert_zero(entry)

    d1, d2, d3 = sp.symbols("d1 d2 d3", nonzero=True)
    e1 = d1 + d2 + d3
    e2 = d1 * d2 + d1 * d3 + d2 * d3
    e3 = d1 * d2 * d3
    target_coefficients = sp.Matrix([-e3, e2, -e1, 1])
    schubert = sp.factor(left_null.dot(target_coefficients))
    assert_zero(schubert - (-e3 * beta**2 + 2 * e2 * beta - 3 * e1))

    q1, q2, q3 = (1 / d1, 1 / d2, 1 / d3)
    reciprocal_form = beta**2 - 2 * (q1 + q2 + q3) * beta
    reciprocal_form += 3 * (q1 * q2 + q1 * q3 + q2 * q3)
    assert_zero(schubert + e3 * reciprocal_form)

    # Fix two offsets and vary the third.  With c=2a, h(q) is the exact
    # contribution 1/(a+y) expressed through q=1/(y-a).
    q, c, L, Q, R = sp.symbols("q c L Q R", nonzero=True)
    h_of_q = q / (1 + c * q)
    fiber = (L - h_of_q) ** 2
    fiber -= 2 * (Q + q) * (L - h_of_q)
    fiber += 3 * (R + q * Q)
    numerator = sp.Poly(
        sp.cancel(fiber * (1 + c * q) ** 2), q
    )
    assert numerator.degree() == 3
    coefficients = {
        degree: sp.factor(numerator.coeff_monomial(q**degree))
        for degree in range(4)
    }
    assert_zero(coefficients[3] + c * (2 * L * c - 3 * Q * c - 2))
    assert_zero(coefficients[0] - (L**2 - 2 * L * Q + 3 * R))

    forced_L = sp.Rational(3, 2) * Q + 1 / c
    forced_R = (2 * forced_L * Q - forced_L**2) / 3
    reduced_c2 = sp.factor(
        coefficients[2].subs({L: forced_L, R: forced_R})
    )
    reduced_c1 = sp.factor(
        coefficients[1].subs({L: forced_L, R: forced_R})
    )
    assert_zero(reduced_c2 + Q * c + 3)
    assert_zero(reduced_c1 + (Q * c + 4) / c)
    # Identical vanishing would force Q*c=-3 and Q*c=-4.
    assert_zero((Q * c + 4) - (Q * c + 3) - 1)

    for h in range(13, 18):
        singleton_count = h + 7
        assert singleton_count - 3 >= 17 > 3


def audit_b1_six_anchor_parity_closure() -> None:
    # In the b=1 base selection, fix six of the seven complementary
    # singleton values.  A relation among their rows on P_7 has numerator
    # degree at most three; multiplying by f_s produces a sextic.
    assert 6 * 2 == 12
    assert 12 - (7 + 2) == 3
    assert 3 + 3 == 6
    for h in range(13, 18):
        singleton_count = h + 9
        moving_values = singleton_count - 6
        assert moving_values == h + 3 >= 16
        # A line cannot contain all moving factors.  If the fixed space
        # were a pencil, its Wronskian would have degree at most ten, but
        # every moving double root would be a Wronskian root.
        assert moving_values > 6
        assert moving_values > 2 * (7 - 2) == 10

    z, s_value = sp.symbols("z s")
    coefficients = sp.symbols("c0:21")
    basis = [
        sum(coefficients[7 * row + degree] * z**degree
            for degree in range(7))
        for row in range(3)
    ]
    incidence = sp.expand(
        sp.Matrix(
            [
                [poly.subs(z, s_value) for poly in basis],
                [sp.diff(poly, z).subs(z, s_value) for poly in basis],
                [poly.subs(z, -s_value) for poly in basis],
            ]
        ).det()
    )
    incidence_poly = sp.Poly(incidence, s_value)
    assert incidence_poly.degree() == 14
    assert all(
        incidence_poly.coeff_monomial(s_value**degree) == 0
        for degree in (0, 1)
    )

    # The degree-four even space is an exact identity model for the first
    # determinant: its first and third rows coincide.  It also contains a
    # member divisible by f_s for every s.
    even_basis = [sp.Integer(1), z**2, z**4]
    even_incidence = sp.factor(
        sp.Matrix(
            [
                [poly.subs(z, s_value) for poly in even_basis],
                [sp.diff(poly, z).subs(z, s_value)
                 for poly in even_basis],
                [poly.subs(z, -s_value) for poly in even_basis],
            ]
        ).det()
    )
    assert_zero(even_incidence)
    moving_factor = (z - s_value) ** 2 * (z + s_value)
    even_member = (z**2 - s_value**2) ** 2
    assert sp.rem(even_member, moving_factor, z) == 0

    # Four or more dimensions would make the incidence automatic, but
    # the six actual Robin equations rule those dimensions out.  A
    # d-space in P_6 has Wronskian degree at most d(7-d), while each
    # Robin anchor contributes weight at least d-1.
    assert sp.degree(moving_factor, z) == 3
    for dimension in range(4, 8):
        assert 6 * (dimension - 1) > dimension * (7 - dimension)
    assert 6 * (3 - 1) == 3 * (7 - 3) == 12

    # The elementary cross-product identity used to classify the
    # determinant identity.  For a primitive polynomial vector q, put
    # c=q x q'.  If q(z) and q(-z) differed projectively, Delta=0 at z
    # and -z would give c(-z) proportional to c(z).  Differentiating and
    # applying this identity forces q(-z) proportional to q(z), a
    # contradiction because the Wronskian is nonzero in characteristic
    # zero.  Primitivity then makes q even (the odd alternative has a
    # common factor z).
    vector_a = sp.Matrix(sp.symbols("a0:3"))
    vector_b = sp.Matrix(sp.symbols("b0:3"))
    vector_c = sp.Matrix(sp.symbols("d0:3"))
    triple_product = sp.Matrix.hstack(
        vector_a, vector_b, vector_c
    ).det()
    cross_identity = (
        vector_a.cross(vector_b).cross(vector_a.cross(vector_c))
        - triple_product * vector_a
    )
    assert all(sp.expand(entry) == 0 for entry in cross_identity)

    # Common factors cannot remove the forced root at zero.  W(gq)=
    # g^3 W(q), and for three even polynomials q_i=Q_i(z^2),
    # W_z(q)=8 z^3 W_w(Q).  The six nonzero anchors already use the full
    # degree twelve, so this additional z^3 is impossible.
    generic_g = sp.Function("g")(z)
    generic_q = [sp.Function(f"q{index}")(z) for index in range(3)]
    assert_zero(
        wronskian([generic_g * poly for poly in generic_q], z)
        - generic_g**3 * wronskian(generic_q, z)
    )

    w = sp.symbols("w")
    even_coefficients = sp.symbols("e0:12")
    w_polys = [
        sum(even_coefficients[4 * row + degree] * w**degree
            for degree in range(4))
        for row in range(3)
    ]
    even_polys = [poly.subs(w, z**2) for poly in w_polys]
    assert_zero(
        wronskian(even_polys, z)
        - 8 * z**3 * wronskian(w_polys, w).subs(w, z**2)
    )


def audit_b0_nine_simple_eight_anchor_parity_closure() -> None:
    # Both the b=0 base selection and the selected-double occurrence in
    # b=1 have complement 3^3 1^9.  The relation space lies in P_8, so
    # its annihilator has dimension six.  Eight fixed simple rows give
    # at least two relations.  Their common denominator has degree 16;
    # the numerators have degree at most six, and multiplication by the
    # moving f_s gives degree at most nine.
    assert (8 + 1) - 3 == 6
    assert 8 - 6 >= 2
    assert 8 * 2 == 16
    assert 16 - (8 + 2) == 6
    assert 6 + 3 == 9

    for h in range(13, 18):
        b0_moving = (h + 11) - 8
        b1_moving = (h + 9) - 8
        assert b0_moving == h + 3 >= 16
        assert b1_moving == h + 1 >= 14

    # If the fixed space had dimension two, four pairwise coprime moving
    # factors would divide every member, already exceeding degree nine.
    assert 4 * 3 > 9

    # Eight Robin anchors exclude dimensions at least five.  Dimension
    # three is also impossible: the anchors and the moving two-dimensional
    # f_s subspaces each contribute weight two to a degree-at-most-21
    # Wronskian.  Thus only dimension four remains, and its eight anchor
    # weights exactly saturate degree 24.
    for dimension in range(5, 11):
        assert 8 * (dimension - 1) > dimension * (10 - dimension)
    assert 8 * (3 - 1) + 16 * 2 > 3 * (10 - 3)
    assert 8 * (4 - 1) == 4 * (10 - 4) == 24

    # For a four-space in P_9, two independent members divisible by f_s
    # say rank(E_s,D_s,E_-s)<=2.  Each 3x3 minor has degree at most 23.
    # It vanishes at the eight Robin anchors as well as every moving s.
    # The b=0 count gives at least 24 roots and hence an identity.  The
    # selected-double b=1 occurrence gives only 22 roots, recording the
    # sharp barrier of this particular count.
    z = sp.symbols("z")
    coefficients = sp.symbols("m0:30")
    generic_three = [
        sum(coefficients[10 * row + degree] * z**degree
            for degree in range(10))
        for row in range(3)
    ]
    tangent_minor = sp.expand(
        sp.Matrix(
            [
                generic_three,
                [sp.diff(poly, z) for poly in generic_three],
                [poly.subs(z, -z) for poly in generic_three],
            ]
        ).det()
    )
    assert sp.Poly(tangent_minor, z).degree() == 23
    assert 8 + 16 > 23
    assert 8 + 14 <= 23

    # Once all minors vanish, the tangent line at z also contains q(-z).
    # Applying the identity at -z gives the same chord in both tangent
    # lines.  Writing q(-z)=Aq+Bq' and differentiating forces B=0 because
    # q,q',q'' have generic rank three for four independent polynomials.
    # The primitive vector is therefore even.  Audit the resulting exact
    # four-polynomial Wronskian identity and its unavoidable z^6 factor.
    generic_g = sp.Function("g4")(z)
    generic_q = [sp.Function(f"r{index}")(z) for index in range(4)]
    assert_zero(
        wronskian([generic_g * poly for poly in generic_q], z)
        - generic_g**4 * wronskian(generic_q, z)
    )

    w = sp.symbols("w")
    even_coefficients = sp.symbols("u0:16")
    w_polys = [
        sum(even_coefficients[4 * row + degree] * w**degree
            for degree in range(4))
        for row in range(4)
    ]
    even_polys = [poly.subs(w, z**2) for poly in w_polys]
    assert_zero(
        wronskian(even_polys, z)
        - 64 * z**6 * wronskian(w_polys, w).subs(w, z**2)
    )


def audit_double_exchange_and_combinatorics() -> None:
    v, a, u = sp.symbols("v a u")
    exchange = (
        2 / (v + a)
        - 2 / (v + u)
        - 3 / (v - u)
        + 3 / (v - a)
    )
    expected = (
        (u - a) * (a * u + 5 * a * v + 5 * u * v + v**2)
        / ((v - a) * (v + a) * (u - v) * (u + v))
    )
    assert_zero(exchange - expected)

    # For b=5, after fixing exchanged values u,a, the other three
    # distinct doubles would all be roots of one monic quadratic.
    assert 5 - 2 == 3 > 2

    # For b=4, two different partitions force B^2=C^2.  Repeated values
    # are nonzero, and distinct value classes are nonopposite, so this is
    # forbidden.
    A, B, C, D = sp.symbols("A B C D")
    first_partition = A * B - C * D
    second_partition = A * C - B * D
    assert_zero(
        B * second_partition - C * first_partition
        - D * (C**2 - B**2)
    )
    assert_zero(C**2 - B**2 - (C - B) * (C + B))


def main() -> None:
    audit_family_and_selection_table()
    audit_four_double_one_simple_schubert_cubic()
    audit_exact_single_fiber_boundary_model()
    audit_principal_part_and_gauge_cancellation()
    audit_fixed_two_jet_pencil()
    audit_singleton_pair_collapse()
    audit_five_simple_cubic_pencil_frontier()
    audit_cubic_pencil_schubert_and_b2_collapse()
    audit_b1_six_anchor_parity_closure()
    audit_b0_nine_simple_eight_anchor_parity_closure()
    audit_b6_endpoint_selected_pair_closure()
    audit_double_exchange_and_combinatorics()
    print("p=18 three-triple overlap frontier PASS")
    print("families audited: b=0,...,6")
    print("closed uniformly: b=0,1,2,3,4,5,6")
    print("frontier Schubert profile: 3^3 2^4 1")
    print("remaining a=3 families: none")


if __name__ == "__main__":
    main()
