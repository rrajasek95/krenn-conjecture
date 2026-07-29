#!/usr/bin/env python3
"""Exact audit of the three-simple, seven-double equality grid."""

from __future__ import annotations

import sympy as sp


x, y, a, b, U, V, scale = sp.symbols("x y a b U V scale")
c = sp.Integer(1)  # Common scaling normalizes the third anchor.


def phi(node, moving):
    return (5 * node - moving) / (moving**2 - node**2)


def simple_quadratic_row(node, constant):
    denominator = (x**2 - node**2) * (y**2 - node**2)
    local = constant + phi(node, x) + phi(node, y)
    row = (
        local,
        1 + node * local,
        2 * node + node**2 * local,
    )
    return tuple(sp.cancel(denominator * entry).expand() for entry in row)


def two_anchor_numerator(first, second):
    y_b = first + phi(b, y)
    y_c = second + phi(c, y)
    return sp.Poly(
        sp.cancel(
            (y**2 - b**2)
            * (y**2 - c**2)
            * (y_b - y_c + (c - b) * y_b * y_c)
        ),
        y,
    )


def check_bidegree_and_endpoint_shift() -> None:
    rows = (
        simple_quadratic_row(a, sp.symbols("C_a")),
        simple_quadratic_row(b, sp.symbols("C_b")),
        simple_quadratic_row(c, sp.symbols("C_c")),
    )
    assert all(
        sp.Poly(entry, x, y).degree(x) <= 2
        and sp.Poly(entry, x, y).degree(y) <= 2
        for row in rows
        for entry in row
    )
    determinant = sp.Poly(sp.Matrix(rows).det(method="domain-ge"), x, y)
    assert determinant.degree(x) <= 6 and determinant.degree(y) <= 6

    t = sp.symbols("t")
    delta = sp.factor(phi(t, a) - phi(t, -a))
    assert sp.factor(delta - 2 * a / (t**2 - a**2)) == 0


def check_four_endpoint_branches() -> None:
    q_minus = two_anchor_numerator(U, V)
    delta_b = 2 * a / (b**2 - a**2)
    delta_c = 2 * a / (c**2 - a**2)
    q_plus = two_anchor_numerator(U + delta_b, V + delta_c)

    cross_b = sp.factor(
        (a - b) ** 2 * q_plus.eval(b) * q_minus.eval(-b)
        - (a + b) ** 2 * q_minus.eval(b) * q_plus.eval(-b)
    )
    v_zero = (
        V * (b**2 - 1) * (a - 1)
        - a * b + 5 * a - b**2 + b - 4
    )
    v_one = (
        V * (b**2 - 1) * (a + 1)
        - a * b + 3 * a - b**2 - b + 4
    )
    expected_b = -96 * a * b**3 * (b - 1) ** 2 * v_zero * v_one / (
        (a - 1) * (a + 1)
    )
    assert sp.factor(cross_b - expected_b) == 0

    cross_c = sp.factor(
        (a - 1) ** 2 * q_plus.eval(1) * q_minus.eval(-1)
        - (a + 1) ** 2 * q_minus.eval(1) * q_plus.eval(-1)
    )
    u_zero = (
        U * (b**2 - 1) * (a - b)
        - 5 * a * b + a + 4 * b**2 - b + 1
    )
    u_one = (
        U * (b**2 - 1) * (a + b)
        - 3 * a * b + a - 4 * b**2 + b + 1
    )
    expected_c = -96 * a * (b - 1) ** 2 * u_zero * u_one / (
        (a - b) * (a + b)
    )
    assert sp.factor(cross_c - expected_c) == 0

    return q_minus, q_plus


def check_all_four_branches(q_minus, q_plus) -> None:
    u_branches = (
        (5 * a * b - a - 4 * b**2 + b - 1)
        / ((b**2 - 1) * (a - b)),
        (3 * a * b - a + 4 * b**2 - b - 1)
        / ((b**2 - 1) * (a + b)),
    )
    v_branches = (
        (a * b - 5 * a + b**2 - b + 4)
        / ((b**2 - 1) * (a - 1)),
        (a * b - 3 * a + b**2 + b - 4)
        / ((b**2 - 1) * (a + 1)),
    )
    relation_constants = ((34, 22), (22, 14))
    scale_branches = ((a - 1) / (a + 1), (a + 1) / (a - 1))
    expected_remainders = (
        ((384, 169, 5, 985, 29), (192, 89, 4, 571, 26)),
        ((96, 283, 13, 1163, 53), (96, 71, 5, 265, 19)),
    )
    expected_cross = ((24, -30), (120, -24))

    for i, u_value in enumerate(u_branches):
        for j, v_value in enumerate(v_branches):
            substitutions = {U: u_value, V: v_value}
            relation_constant = relation_constants[i][j]
            relation = b**2 - relation_constant * b + 1

            endpoint_a = sp.factor(q_minus.eval(a).subs(substitutions))
            expected_endpoint = -(
                (a - b) * (a + b) * (a - 1) * (a + 1) * relation
                / ((b - 1) * (b + 1) ** 2)
            )
            assert sp.factor(endpoint_a - expected_endpoint) == 0

            q_at_b = sp.factor(q_minus.eval(b).subs(substitutions))
            expected_q_at_b = (
                4 * b * (a - b) * (b - 1) * (b + 1) / (a - 1)
                if j == 0
                else 4 * b * (a - b) * (b - 1) ** 2 / (a + 1)
            )
            assert sp.factor(q_at_b - expected_q_at_b) == 0

            endpoint_scale = sp.factor(
                (a - b) * q_plus.eval(b).subs(substitutions)
                / ((a + b) * q_at_b)
            )
            assert sp.factor(endpoint_scale - scale_branches[j]) == 0

            identity = sp.Poly(
                sp.cancel(
                    (
                        (a - y) * q_plus.as_expr()
                        - scale_branches[j] * (a + y) * q_minus.as_expr()
                    ).subs(substitutions)
                ),
                y,
            )
            common, p5, q5, p4, q4 = expected_remainders[i][j]
            remainder5 = sp.factor(
                sp.rem(
                    sp.Poly(sp.together(identity.coeff_monomial(y**5)).as_numer_denom()[0], b),
                    sp.Poly(relation, b),
                ).as_expr()
            )
            remainder4 = sp.factor(
                sp.rem(
                    sp.Poly(sp.together(identity.coeff_monomial(y**4)).as_numer_denom()[0], b),
                    sp.Poly(relation, b),
                ).as_expr()
            )
            assert sp.factor(remainder5 - common * a * (p5 * b - q5)) == 0
            assert sp.factor(remainder4 + common * a * (p4 * b - q4)) == 0
            assert q5 * p4 - q4 * p5 == expected_cross[i][j]


def main() -> None:
    check_bidegree_and_endpoint_shift()
    q_minus, q_plus = check_four_endpoint_branches()
    check_all_four_branches(q_minus, q_plus)
    print("three-simple M=7 equality-grid audit: PASS")
    print("all four endpoint branches are inconsistent")
    print("p=8, (d,s)=(7,3) still lacks the Hermite rank dependence")


if __name__ == "__main__":
    main()
