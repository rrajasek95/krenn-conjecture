#!/usr/bin/env python3
"""Exact audit for the all-distinct t=r+7 sixth-split closure."""

from __future__ import annotations

from itertools import combinations

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.rings import ring


def triple_determinant_formula(
    a: sp.Expr,
    b: sp.Expr,
    c: sp.Expr,
    A: sp.Expr,
    B: sp.Expr,
    C: sp.Expr,
) -> sp.Expr:
    """Closed form for det(V, 1+tV, 2t+t^2 V) on three nodes."""
    return sp.expand(
        -(a - b) * (a - c) * (b - c) * A * B * C
        + (a - b) * (a + b - 2 * c) * A * B
        - (a - c) * (a - 2 * b + c) * A * C
        - (b - c) * (2 * a - b - c) * B * C
        - 2 * (b - c) * A
        + 2 * (a - c) * B
        - 2 * (a - b) * C
    )


def check_triple_determinant_formula() -> None:
    a, b, c, A, B, C = sp.symbols("a b c A B C")
    matrix = sp.Matrix(
        [
            [A, 1 + a * A, 2 * a + a**2 * A],
            [B, 1 + b * B, 2 * b + b**2 * B],
            [C, 1 + c * C, 2 * c + c**2 * C],
        ]
    )
    assert sp.expand(matrix.det() - triple_determinant_formula(a, b, c, A, B, C)) == 0


def endpoint_polynomial(
    nodes: tuple[sp.Symbol, ...],
    translations: tuple[sp.Symbol, ...],
    omitted: int,
    sign: str,
) -> sp.Expr:
    complement = [j for j in range(4) if j != omitted]
    values: list[sp.Expr] = []
    for j in complement:
        if sign == "+":
            shift = -2 / (nodes[j] + nodes[omitted])
        else:
            shift = -1 / (nodes[j] + nodes[omitted]) - 1 / (
                nodes[j] - nodes[omitted]
            )
        values.append(translations[j] + shift)
    return triple_determinant_formula(
        nodes[complement[0]],
        nodes[complement[1]],
        nodes[complement[2]],
        values[0],
        values[1],
        values[2],
    )


def check_endpoint_reduction() -> None:
    x, ti, tj, u = sp.symbols("x ti tj u")
    r, rp = sp.symbols("r rp")
    q = (tj - ti) * r
    qp = r + (tj - ti) * rp
    row = (x**2 - tj**2) * (qp + u * q) - (x - 3 * tj) * q

    plus = rp + (u - 2 / (ti + tj)) * r
    minus = rp + (
        u - 1 / (ti + tj) - 1 / (tj - ti)
    ) * r
    expected = -(tj - ti) ** 2 * (ti + tj)
    assert sp.factor(row.subs(x, ti) / plus - expected) == 0
    assert sp.factor(row.subs(x, -ti) / minus - expected) == 0


def check_quartet_linear_certificate() -> None:
    # Work directly in QQ(t0,t1,t2,t3)[u0,u1,u2,u3].  Equality in this
    # exact sparse polynomial ring audits every coefficient without asking
    # a general-purpose simplifier to expand one large common denominator.
    coefficient_field = QQ.frac_field("t0", "t1", "t2", "t3")
    t = list(coefficient_field.gens)
    polynomial_ring, u0, u1, u2, u3 = ring(
        "u0,u1,u2,u3", coefficient_field
    )
    u = [u0, u1, u2, u3]

    def phi_ring(local_nodes, values):
        a, b, c = local_nodes
        A, B, C = values
        return (
            -(a - b) * (a - c) * (b - c) * A * B * C
            + (a - b) * (a + b - 2 * c) * A * B
            - (a - c) * (a - 2 * b + c) * A * C
            - (b - c) * (2 * a - b - c) * B * C
            - 2 * (b - c) * A
            + 2 * (a - c) * B
            - 2 * (a - b) * C
        )

    def endpoint_ring(i: int, sign: str):
        complement = [j for j in range(4) if j != i]
        values = []
        for j in complement:
            if sign == "+":
                shift = -2 / (t[j] + t[i])
            else:
                shift = -1 / (t[j] + t[i]) - 1 / (t[j] - t[i])
            values.append(u[j] + shift)
        return phi_ring([t[j] for j in complement], values)

    lhs = polynomial_ring.zero
    for i in range(4):
        complement = [j for j in range(4) if j != i]
        delta_hat = coefficient_field.one
        for left, right in combinations(complement, 2):
            delta_hat *= t[right] - t[left]
        lhs += (endpoint_ring(i, "+") - endpoint_ring(i, "-")) / (
            t[i] * delta_hat
        )

    s_plus = coefficient_field.one
    for i, j in combinations(range(4), 2):
        s_plus *= t[i] + t[j]
    rhs = polynomial_ring.zero
    for i in range(4):
        sigma = coefficient_field.one
        for j in range(4):
            if i != j:
                sigma *= t[i] + t[j]
        rhs += sigma * u[i]
    rhs *= coefficient_field(-6) / s_plus
    assert lhs == rhs

    # At U=0 both endpoint systems have their displayed quadratic kernels.
    nodes = sp.symbols("t0:4", nonzero=True)
    z = sp.symbols("z")
    for i in range(4):
        complement = [j for j in range(4) if j != i]
        plus_kernel = sp.expand((z + nodes[i]) ** 2)
        minus_kernel = sp.expand(z**2 - nodes[i] ** 2)
        for j in complement:
            v_plus = -2 / (nodes[j] + nodes[i])
            v_minus = -1 / (nodes[j] + nodes[i]) - 1 / (
                nodes[j] - nodes[i]
            )
            assert sp.factor(
                sp.diff(plus_kernel, z).subs(z, nodes[j])
                + v_plus * plus_kernel.subs(z, nodes[j])
            ) == 0
            assert sp.factor(
                sp.diff(minus_kernel, z).subs(z, nodes[j])
                + v_minus * minus_kernel.subs(z, nodes[j])
            ) == 0


def check_five_core_cauchy_system() -> None:
    anchors = sp.symbols("a0:5", nonzero=True)
    translations = sp.symbols("u0:5")
    sigma = [
        sp.prod(anchors[i] + anchors[j] for j in range(5) if j != i)
        for i in range(5)
    ]
    vector = sp.Matrix([translations[i] * sigma[i] for i in range(5)])
    matrix = sp.Matrix(
        5,
        5,
        lambda i, j: 0 if i == j else 1 / (anchors[i] + anchors[j]),
    )
    product = matrix * vector
    for omitted in range(5):
        quartet = sum(
            translations[i]
            * sp.prod(
                anchors[i] + anchors[j]
                for j in range(5)
                if j not in (i, omitted)
            )
            for i in range(5)
            if i != omitted
        )
        assert sp.factor(product[omitted] - quartet) == 0


def check_moving_core_polynomial() -> None:
    y = sp.symbols("y")
    anchors = sp.symbols("a0:4", nonzero=True)
    edge_symbols = {
        (i, j): sp.symbols(f"b{i}{j}") for i, j in combinations(range(4), 2)
    }
    base = sp.Matrix(
        4,
        4,
        lambda i, j: 0
        if i == j
        else edge_symbols[tuple(sorted((i, j)))],
    )
    w = sp.Matrix(sp.symbols("w0:4"))
    bordered = base.row_join(w)
    bordered = bordered.col_join(sp.Matrix([[*w.T, 0]]))
    assert sp.expand(bordered.det() + (w.T * base.adjugate() * w)[0]) == 0

    q = sp.prod(y + anchor for anchor in anchors)
    cleared_factors = [sp.cancel(q / (y + anchor)) for anchor in anchors]
    assert all(sp.Poly(factor, y).degree() == 3 for factor in cleared_factors)

    # This is Q(y)^2 times the bordered determinant, written without any
    # rational functions in y.
    cleared = -sum(
        base.adjugate()[i, j] * cleared_factors[i] * cleared_factors[j]
        for i in range(4)
        for j in range(4)
    )
    assert sp.Poly(cleared, y).degree() <= 6
    for i in range(4):
        expected = -base.adjugate()[i, i] * sp.prod(
            anchors[j] - anchors[i] for j in range(4) if j != i
        ) ** 2
        assert sp.expand(cleared.subs(y, -anchors[i]) - expected) == 0

    b, c, d = sp.symbols("b c d")
    three = sp.Matrix(
        [
            [0, 1 / (b + c), 1 / (b + d)],
            [1 / (b + c), 0, 1 / (c + d)],
            [1 / (b + d), 1 / (c + d), 0],
        ]
    )
    assert sp.factor(three.det() - 2 / ((b + c) * (b + d) * (c + d))) == 0


def check_count_and_fibre() -> None:
    p = sp.symbols("p", integer=True, positive=True)
    assert sp.expand((p + 8) - 4 - 1) == p + 3
    assert sp.expand((p + 3) - 6) == p - 3
    assert 7 - 3 >= 4

    a, y, lam = sp.symbols("a y lam", nonzero=True)
    psi = -(y + 3 * a) / (y**2 - a**2)
    numerator = sp.together(psi - lam).as_numer_denom()[0]
    assert sp.factor(-numerator - (lam * (y**2 - a**2) + y + 3 * a)) == 0
    assert sp.Poly(numerator, y).degree() == 2
    assert sp.expand(numerator).coeff(y, 1) == -1


def main() -> None:
    check_triple_determinant_formula()
    check_endpoint_reduction()
    check_quartet_linear_certificate()
    check_five_core_cauchy_system()
    check_moving_core_polynomial()
    check_count_and_fibre()
    print("sixth-split all-distinct five-core Cauchy closure: PASS")


if __name__ == "__main__":
    main()
