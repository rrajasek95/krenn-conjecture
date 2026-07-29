#!/usr/bin/env python3
"""Exact audit for the p=18 four-triple overlap closure."""

from __future__ import annotations

from collections import Counter
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
        (0, 0, ((3, 4), (1, 6))),
        (1, 1, ((3, 3), (1, 9))),
    },
    1: {
        (0, 0, ((3, 4), (2, 1), (1, 4))),
        (1, 0, ((3, 4), (1, 6))),
        (1, 1, ((3, 3), (2, 1), (1, 7))),
        (2, 1, ((3, 3), (1, 9))),
    },
    2: {
        (0, 0, ((3, 4), (2, 2), (1, 2))),
        (1, 0, ((3, 4), (2, 1), (1, 4))),
        (1, 1, ((3, 3), (2, 2), (1, 5))),
        (2, 0, ((3, 4), (1, 6))),
        (2, 1, ((3, 3), (2, 1), (1, 7))),
    },
    3: {
        (0, 0, ((3, 4), (2, 3))),
        (1, 0, ((3, 4), (2, 2), (1, 2))),
        (1, 1, ((3, 3), (2, 3), (1, 3))),
        (2, 0, ((3, 4), (2, 1), (1, 4))),
        (2, 1, ((3, 3), (2, 2), (1, 5))),
    },
    4: {
        (1, 0, ((3, 4), (2, 3))),
        (1, 1, ((3, 3), (2, 4), (1, 1))),
        (2, 0, ((3, 4), (2, 2), (1, 2))),
        (2, 1, ((3, 3), (2, 3), (1, 3))),
    },
    5: {
        (2, 0, ((3, 4), (2, 3))),
        (2, 1, ((3, 3), (2, 4), (1, 1))),
    },
}


def audit_family_and_selection_table() -> None:
    admissible = []
    for doubles in range(12):
        u = 8 - 2 * doubles
        applies = (
            u >= 2
            or (u >= 0 and 4 + doubles >= 1)
            or (
                u >= -2
                and (doubles >= 2 or (4 >= 1 and doubles >= 1))
            )
        )
        if applies:
            admissible.append(doubles)
    assert admissible == list(range(6))

    for h in range(13, 18):
        k = 18 - h
        for doubles in admissible:
            u = 8 - 2 * doubles
            profile = (
                (3,) * 4 + (2,) * doubles + (1,) * (h + u)
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

            if doubles <= 2:
                convenient = (
                    doubles,
                    0,
                    ((3, 4), (1, 6)),
                )
            else:
                convenient = (
                    doubles - 3,
                    0,
                    ((3, 4), (2, 3)),
                )
            assert convenient in observed


def robin_row(point: sp.Expr, beta: sp.Expr) -> list[sp.Expr]:
    return [
        beta,
        1 + beta * point,
        2 * point + beta * point**2,
        3 * point**2 + beta * point**3,
        4 * point**3 + beta * point**4,
    ]


def audit_degree_two_fiber() -> None:
    z, a, b, r, s, beta, gamma = sp.symbols(
        "z a b r s beta gamma"
    )
    rows = sp.Matrix([robin_row(r, beta), robin_row(s, gamma)])
    nullspace = rows.nullspace()
    assert len(nullspace) == 3
    polys = [
        sum(vector[index] * z**index for index in range(5))
        for vector in nullspace
    ]
    wr = wronskian(polys, z)
    base = (z - r) ** 2 * (z - s) ** 2
    quotient = sp.cancel(wr / base)
    assert sp.degree(sp.fraction(quotient)[0], z) == 2

    quotient_poly = sp.Poly(quotient, z)
    leading = quotient_poly.coeff_monomial(z**2)
    coefficient_z = quotient_poly.coeff_monomial(z)
    constant = quotient_poly.coeff_monomial(1)
    equation_z = sp.factor(
        sp.fraction(sp.together(coefficient_z + (a + b) * leading))[0]
    )
    equation_0 = sp.factor(
        sp.fraction(sp.together(constant - a * b * leading))[0]
    )

    resultant = sp.factor(sp.resultant(equation_z, equation_0, gamma))
    necessary = (
        (r - a) * (r - b) * (r - s) * beta**2
        + (
            2 * a * b
            - 5 * r * (a + b)
            + 3 * s * (a + b)
            + 8 * r**2
            - 6 * r * s
        )
        * beta
        + 4 * (4 * r - 2 * s - a - b)
    )
    ratio = sp.factor(sp.cancel(resultant / necessary))
    assert beta not in ratio.free_symbols
    assert gamma not in ratio.free_symbols
    assert ratio != 0


def audit_singleton_variation_cubic() -> None:
    a, b, r, s, lam, beta = sp.symbols("a b r s Lambda beta")
    necessary = (
        (r - a) * (r - b) * (r - s) * beta**2
        + (
            2 * a * b
            - 5 * r * (a + b)
            + 3 * s * (a + b)
            + 8 * r**2
            - 6 * r * s
        )
        * beta
        + 4 * (4 * r - 2 * s - a - b)
    )
    beta_actual = lam - 1 / (r + s) - 2 / (r - s)
    numerator, denominator = sp.fraction(
        sp.cancel(necessary.subs(beta, beta_actual))
    )
    assert sp.factor(denominator) == (r + s) ** 2
    assert sp.degree(numerator, s) <= 3

    A, B = sp.symbols("A B")
    shifted = sp.expand(numerator.subs({a: r + A, b: r + B}))
    coefficients = sp.Poly(shifted, s)
    c3 = sp.factor(coefficients.coeff_monomial(s**3))
    c2 = sp.factor(coefficients.coeff_monomial(s**2))
    c1 = sp.factor(coefficients.coeff_monomial(s))
    c0 = sp.factor(coefficients.coeff_monomial(1))
    assert_zero(c3 - (-A * B * lam**2 + 3 * (A + B) * lam - 8))
    assert_zero(c2 - r * c3 + A + B)
    assert_zero(c0 - r * c1 - r * (2 * A * B + r * (A + B)))

    for h in range(13, 18):
        assert h + 1 >= 14 > 3


def audit_three_double_hyperplane() -> None:
    z, v, a, b = sp.symbols("z v a b")
    e1 = v + a + b
    e2 = v * a + v * b + a * b
    e3 = v * a * b
    functional = sp.Matrix([1, e1 / 3, e2 / 3, e3])
    basis = [
        1 - z**3 / e3,
        z - e1 * z**3 / (3 * e3),
        z**2 - e2 * z**3 / (3 * e3),
    ]
    wr = wronskian(basis, z)
    target = (z - v) * (z - a) * (z - b)
    assert wr != 0
    assert_zero(sp.diff(wr / target, z))

    alpha = -1 / (v - a) - 1 / (v - b)
    delta = 6 / ((a - v) * (b - v))
    order_two_row = sp.Matrix(
        [
            delta,
            2 * alpha + delta * v,
            2 + 4 * alpha * v + delta * v**2,
            6 * v + 6 * alpha * v**2 + delta * v**3,
        ]
    )
    for coordinate in order_two_row - delta * functional:
        assert_zero(coordinate)


def audit_double_exchange() -> None:
    v, a, r = sp.symbols("v a r")
    exchange = (
        1 / (v + a)
        + 1 / (v - a)
        - 1 / (v + r)
        - 1 / (v - r)
    )
    expected = (
        2 * v * (a**2 - r**2)
        / ((v**2 - a**2) * (v**2 - r**2))
    )
    assert_zero(exchange - expected)


def audit_accessory_pencil() -> None:
    z = sp.symbols("z")
    roots = tuple(map(sp.Integer, (1, 2, 3, 4, 5)))
    J = sp.prod(z - root for root in roots)
    N = z**2 + z + 1

    # A quadratic numerator produces exactly one relation among the five
    # Robin rows on P_6.
    coefficients = []
    betas = []
    for root in roots:
        Ji = sp.cancel(J / (z - root))
        Ji_value = Ji.subs(z, root)
        coefficient = N.subs(z, root) / Ji_value**2
        beta = (
            sp.diff(N, z).subs(z, root) / N.subs(z, root)
            - 2 * sp.diff(Ji, z).subs(z, root) / Ji_value
        )
        coefficients.append(sp.factor(coefficient))
        betas.append(sp.factor(beta))

    for power in range(7):
        moment = sum(
            coefficient
            * (
                (power * root ** (power - 1) if power else 0)
                + beta * root**power
            )
            for root, coefficient, beta in zip(
                roots, coefficients, betas
            )
        )
        assert_zero(moment)

    principal_parts = sum(
        coefficient
        * (1 / (z - root) ** 2 + beta / (z - root))
        for root, coefficient, beta in zip(
            roots, coefficients, betas
        )
    )
    assert_zero(principal_parts - N / J**2)

    # Multiplication by f_s removes the s-dependent logarithmic terms.
    r, s, lam = sp.symbols("r s Lambda")
    n0, n1, n2 = sp.symbols("n0 n1 n2")
    quadratic = n0 + n1 * z + n2 * z**2
    fs = (z - s) ** 2 * (z + s)
    beta_shift = lam - 1 / (r + s) - 2 / (r - s)
    robin_equation = (
        sp.diff(quadratic, z).subs(z, r)
        - beta_shift * quadratic.subs(z, r)
    )
    accessory_equation = (
        sp.diff(quadratic * fs, z).subs(z, r)
        - lam * (quadratic * fs).subs(z, r)
    )
    assert_zero(
        accessory_equation
        - fs.subs(z, r) * robin_equation
    )

    # Two cubics have Wronskian degree at most four (the nominal degree
    # five cancels), which is the dimension bound in Section 6.
    u = sp.symbols("u0:4")
    v = sp.symbols("v0:4")
    cubic_u = sum(u[index] * z**index for index in range(4))
    cubic_v = sum(v[index] * z**index for index in range(4))
    cubic_wr = sp.expand(
        sp.diff(cubic_u, z) * cubic_v
        - cubic_u * sp.diff(cubic_v, z)
    )
    assert sp.degree(cubic_wr, z) <= 4

    # A pencil in P_5 has Wronskian degree at most eight.
    p = sp.symbols("p0:6")
    q = sp.symbols("q0:6")
    poly_p = sum(p[index] * z**index for index in range(6))
    poly_q = sum(q[index] * z**index for index in range(6))
    pencil_wr = sp.expand(
        sp.diff(poly_p, z) * poly_q
        - poly_p * sp.diff(poly_q, z)
    )
    assert sp.degree(pencil_wr, z) <= 8

    for h in range(13, 18):
        for doubles in range(3):
            candidate_count = h + 3 - 2 * doubles
            assert candidate_count >= 12 > 8


def main() -> None:
    audit_family_and_selection_table()
    audit_degree_two_fiber()
    audit_singleton_variation_cubic()
    audit_three_double_hyperplane()
    audit_double_exchange()
    audit_accessory_pencil()
    print("PASS: p=18 four-triple overlap closure audited exactly")


if __name__ == "__main__":
    main()
