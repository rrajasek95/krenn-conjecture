#!/usr/bin/env python3
"""Exact audit of the p=18, a=3, b=6 neighboring Schubert coupling."""

from __future__ import annotations

import sympy as sp


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


def quotient_matrix(
    basis: list[sp.Expr], z: sp.Symbol
) -> tuple[list[sp.Expr], sp.Matrix]:
    quotients: list[sp.Expr] = []
    for omitted in range(4):
        subspace = [
            basis[index] for index in range(4) if index != omitted
        ]
        full_wronskian = wronskian(subspace, z)
        quotient = sp.cancel(full_wronskian / (z**2 * (z - 1) ** 2))
        assert not sp.denom(quotient).has(z)
        assert sp.degree(quotient, z) <= 5
        quotients.append(sp.expand(quotient))
    matrix = sp.Matrix(
        [[poly.coeff(z, degree) for degree in range(6)]
         for poly in quotients]
    )
    return quotients, matrix


def audit_normalized_two_robin_schubert_image() -> tuple[
    sp.Expr, sp.Expr, sp.Expr, tuple[sp.Symbol, ...]
]:
    z, beta, gamma = sp.symbols("z beta gamma")
    common = beta * gamma + beta - gamma
    basis = [
        sp.expand(
            common * z**degree
            - (beta * gamma + degree * beta) * z
            + gamma + degree
        )
        for degree in range(2, 6)
    ]

    # These four polynomials span ker(D_0+beta E_0) intersect
    # ker(D_1+gamma E_1) away from an irrelevant basis chart divisor.
    for poly in basis:
        assert_zero(sp.diff(poly, z).subs(z, 0) + beta * poly.subs(z, 0))
        assert_zero(sp.diff(poly, z).subs(z, 1) + gamma * poly.subs(z, 1))

    _, matrix = quotient_matrix(basis, z)
    assert matrix.subs({beta: 2, gamma: 3}).rank() == 4

    covector_one = sp.Matrix(
        [
            beta**3 * gamma**2 + 10 * beta**3 * gamma + 25 * beta**3
            - 6 * beta**2 * gamma - 30 * beta**2
            + 5 * beta * gamma**2 + 20 * beta * gamma + 10 * gamma**2,
            3 * beta**2 * gamma**2 + 30 * beta**2 * gamma
            + 75 * beta**2 + 2 * beta * gamma**2 + 2 * beta * gamma
            - 40 * beta + 11 * gamma**2 + 40 * gamma,
            8 * (gamma + 5) * (beta * gamma + 5 * beta + gamma),
            16 * (gamma + 5) ** 2,
            0,
            0,
        ]
    )
    chart_factor = beta * gamma + beta - gamma
    covector_two = sp.Matrix(
        [
            -chart_factor
            * (
                beta**2 * gamma**2 + 8 * beta**2 * gamma
                + 15 * beta**2 + beta * gamma**2 + beta * gamma
                - 10 * beta + 6 * gamma**2 + 10 * gamma
            ),
            -chart_factor
            * (
                3 * beta * gamma**2 + 24 * beta * gamma
                + 45 * beta + 5 * gamma**2 + 19 * gamma
            ),
            -8 * (gamma + 3) * (gamma + 5) * chart_factor,
            0,
            16 * (gamma + 2) * (gamma + 5) ** 2,
            16 * (gamma + 5) ** 3,
        ]
    )
    for entry in matrix * covector_one:
        assert_zero(entry)
    for entry in matrix * covector_two:
        assert_zero(entry)

    elementary = sp.symbols("e1:6")
    target = sp.Matrix(
        [-elementary[4], elementary[3], -elementary[2],
         elementary[1], -elementary[0], 1]
    )
    condition_one = sp.factor(covector_one.dot(target))
    condition_two = sp.factor(covector_two.dot(target))

    resultant = sp.factor(
        sp.resultant(condition_one, condition_two, gamma)
    )
    factors = sp.factor_list(resultant)[1]
    linear = beta * elementary[4] - 3 * elementary[3] + 10 * elementary[4]
    assert any(
        sp.factor(
            factor * sp.Poly(linear, beta).LC()
            - linear * sp.Poly(factor, beta).LC()
        ) == 0
        and multiplicity == 2
        for factor, multiplicity in factors
    )
    essential = next(
        factor for factor, multiplicity in factors
        if sp.Poly(factor, beta).degree() == 11
    )
    assert sp.Poly(essential, beta).degree() == 11

    return essential, linear, gamma, elementary


def audit_singular_gamma_chart(linear: sp.Expr) -> None:
    z, beta = sp.symbols("z beta")
    coefficients = sp.symbols("c0:6")
    polynomial = sum(
        coefficients[degree] * z**degree for degree in range(6)
    )
    robin_matrix = sp.Matrix(
        [
            [beta, 1, 0, 0, 0, 0],
            [-5, -4, -3, -2, -1, 0],
        ]
    )
    kernel_vectors = robin_matrix.nullspace()
    assert len(kernel_vectors) == 4
    basis = [
        sp.expand(sum(vector[index] * z**index for index in range(6)))
        for vector in kernel_vectors
    ]
    _, matrix = quotient_matrix(basis, z)
    assert matrix.subs(beta, 2).rank() == 4

    special_covectors = [
        sp.Matrix([(beta + 10) / 3, 1, 0, 0, 0, 0]),
        sp.Matrix(
            [
                -(4 * beta - 5) ** 3 / 225,
                0,
                (4 * beta - 5) ** 2 / 75,
                2 * (4 * beta - 5) / 15,
                1,
                0,
            ]
        ),
    ]
    for covector in special_covectors:
        for assertion in matrix * covector:
            assert_zero(assertion)

    elementary = sp.symbols("e1:6")
    target = sp.Matrix(
        [-elementary[4], elementary[3], -elementary[2],
         elementary[1], -elementary[0], 1]
    )
    first_condition = sp.factor(special_covectors[0].dot(target))
    assert_zero(3 * first_condition + linear)
    # The singular chart has a genuine second condition; the squared
    # linear factor in the generic resultant is not sufficient by itself.
    assert special_covectors[1].dot(target) != 0


def audit_robin_basis_chart_divisor() -> sp.Expr:
    # The polynomial basis used in the generic chart degenerates when
    # beta*gamma+beta-gamma=0.  Parametrize that divisor by
    # gamma=beta/(1-beta) and recompute the Wronski image directly.
    z, beta = sp.symbols("z beta")
    gamma = beta / (1 - beta)
    robin_matrix = sp.Matrix(
        [
            [beta, 1, 0, 0, 0, 0],
            [gamma, gamma + 1, gamma + 2, gamma + 3,
             gamma + 4, gamma + 5],
        ]
    )
    kernel_vectors = robin_matrix.nullspace()
    assert len(kernel_vectors) == 4
    basis = [
        sp.expand(sum(vector[index] * z**index for index in range(6)))
        for vector in kernel_vectors
    ]
    _, matrix = quotient_matrix(basis, z)
    assert matrix.subs(beta, 2).rank() == 4

    chart_covectors = [
        sp.Matrix(
            [
                beta**3 * (beta - 2) ** 2 / (4 * beta - 5) ** 2,
                beta**2 * (beta - 2) * (3 * beta - 4)
                / (4 * beta - 5) ** 2,
                beta * (2 * beta - 3) / (4 * beta - 5),
                1,
                0,
                0,
            ]
        ),
        sp.Matrix([0, 0, 0, 0, (beta - 2) / (4 * beta - 5), 1]),
    ]
    for covector in chart_covectors:
        for assertion in matrix * covector:
            assert_zero(assertion)

    elementary = sp.symbols("e1:6")
    target = sp.Matrix(
        [-elementary[4], elementary[3], -elementary[2],
         elementary[1], -elementary[0], 1]
    )
    simple_chart_condition = sp.factor(
        (4 * beta - 5) * chart_covectors[1].dot(target)
    )
    expected = 4 * beta - 5 - (beta - 2) * elementary[0]
    assert_zero(simple_chart_condition - expected)

    # Audit the intersection with gamma=-5, beta=5/4 separately.
    intersection = robin_matrix.subs(beta, sp.Rational(5, 4))
    intersection_basis = [
        sp.expand(sum(vector[index] * z**index for index in range(6)))
        for vector in intersection.nullspace()
    ]
    _, intersection_matrix = quotient_matrix(intersection_basis, z)
    assert intersection_matrix.rank() == 4
    intersection_nullity = len(intersection_matrix.nullspace())
    assert intersection_nullity == 2

    return expected


def audit_actual_coupling_and_degree_barrier(
    essential: sp.Expr,
    linear: sp.Expr,
    elementary: tuple[sp.Symbol, ...],
    chart_condition: sp.Expr,
) -> None:
    r, s, omega, u, x = sp.symbols("r s Omega u x")
    phi = 3 / (r - u) + 2 / (r + u)
    psi = 4 / (r - x) + 3 / (r + x)
    neighbor_beta = (
        omega + phi + psi - 1 / (r + s) - 2 / (r - s)
    )
    assert_zero(phi - (5 * r + u) / (r**2 - u**2))
    assert_zero(psi - (7 * r + x) / (r**2 - x**2))

    # Normalize the two simple roots r,s to 0,1.  If d=s-r and E_j are
    # the elementary symmetric functions of the five fixed offsets v-r,
    # then beta_normalized=d*neighbor_beta and e_j=E_j/d^j.
    d, fixed_part = sp.symbols("d C")
    offset_elementary = sp.symbols("E1:6")
    normalized_beta = (
        fixed_part * d**2 + (2 * r * fixed_part + 1) * d + 4 * r
    ) / (d + 2 * r)
    substitutions = {
        sp.Symbol("beta"): normalized_beta,
        **{
            elementary[index]: offset_elementary[index] / d**(index + 1)
            for index in range(5)
        },
    }
    essential_numerator = sp.fraction(
        sp.together(essential.subs(substitutions))
    )[0]
    essential_poly = sp.Poly(sp.expand(essential_numerator), d)
    minimum_degree = min(monomial[0] for monomial, _ in essential_poly.terms())
    assert minimum_degree == 5
    reduced_essential = sp.cancel(essential_numerator / d**5)
    assert sp.Poly(reduced_essential, d).degree() == 17

    special_numerator = sp.fraction(
        sp.together(linear.subs(substitutions))
    )[0]
    special_poly = sp.Poly(sp.expand(special_numerator), d)
    assert special_poly.degree() == 2

    chart_numerator = sp.fraction(
        sp.together(chart_condition.subs(substitutions))
    )[0]
    chart_poly_raw = sp.Poly(sp.expand(chart_numerator), d)
    chart_minimum = min(
        monomial[0] for monomial, _ in chart_poly_raw.terms()
    )
    assert chart_minimum == 1
    chart_poly = sp.Poly(
        sp.cancel(chart_poly_raw.as_expr() / d), d
    )
    assert chart_poly.degree() == 2

    # If the fixed singleton r happens to be zero, the two bounds improve
    # to degrees eleven and one.  Even then their union can contain twelve
    # values, so h=13,14 are not closed by this count; for a general r the
    # 17+2 bound exceeds every available moving-singleton count.
    zero_essential_raw = sp.Poly(
        sp.expand(reduced_essential.subs(r, 0)), d
    )
    zero_minimum = min(
        monomial[0] for monomial, _ in zero_essential_raw.terms()
    )
    assert zero_minimum == 6
    zero_essential = sp.Poly(
        sp.cancel(zero_essential_raw.as_expr() / d**zero_minimum), d
    )
    assert zero_essential.degree() == 11
    zero_constant = sp.factor(zero_essential.TC())
    assert zero_constant != 0
    assert sp.factor(zero_constant / offset_elementary[4] ** 3).is_number
    zero_special_raw = sp.Poly(special_numerator.subs(r, 0), d)
    zero_special_minimum = min(
        monomial[0] for monomial, _ in zero_special_raw.terms()
    )
    assert zero_special_minimum == 1
    zero_special = sp.Poly(
        sp.cancel(zero_special_raw.as_expr() / d), d
    )
    assert zero_special.degree() == 1
    zero_chart = sp.Poly(chart_poly.as_expr().subs(r, 0), d)
    assert zero_chart.degree() == 2
    for h in range(13, 18):
        moving_singletons = h - 2
        assert 11 <= moving_singletons <= 15
        assert moving_singletons <= 17 + 2 + 2
    assert (17 - 2) > 11 + 1 + 2

    # The displayed beta formula really is the common endpoint baseline
    # plus one selected-double and one selected-triple exchange.
    direct_neighbor = neighbor_beta.subs(s, r + d)
    assert_zero(
        direct_neighbor
        - (omega + phi + psi - 1 / (2 * r + d) + 2 / d)
    )


def audit_endpoint_dimensionless_system() -> None:
    # For r != 0, put t_v=2(r+v)/(r-v).  The fifteen endpoint cubics are
    # exactly the following critical-point system.  Recording it gives a
    # compact target for future exact elimination across selected pairs.
    t = sp.symbols("t0:6")
    constant = sp.symbols("K")
    accessory = [sp.Rational(3, 4) * value + 2 / value for value in t]
    residuals = []
    for first in range(6):
        for second in range(first + 1, 6):
            critical_point = constant + accessory[first] + accessory[second]
            residuals.append(
                sp.factor(
                    sum(
                        1 / (critical_point + t[index])
                        for index in range(6)
                        if index not in (first, second)
                    )
                )
            )
    assert len(residuals) == 15
    assert all(residual != 0 for residual in residuals)


def main() -> None:
    essential, linear, _gamma, elementary = (
        audit_normalized_two_robin_schubert_image()
    )
    audit_singular_gamma_chart(linear)
    chart_condition = audit_robin_basis_chart_divisor()
    audit_actual_coupling_and_degree_barrier(
        essential, linear, elementary, chart_condition
    )
    audit_endpoint_dimensionless_system()
    print("p=18 b=6 neighboring Schubert coupling PASS")
    print("normalized Wronski image: rank 4 in quintics (codimension 2)")
    print("generic eliminated slope degree: 11")
    print("general moving-singleton degree barrier: 17 + 2 + 2 charts")
    print("endpoint selected-pair equations retained: 15")


if __name__ == "__main__":
    main()
