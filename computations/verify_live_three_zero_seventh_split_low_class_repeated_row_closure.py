#!/usr/bin/env python3
"""Exact audit of the low-class seventh-split repeated-row closures."""

from __future__ import annotations

import sympy as sp


x, u, v, w = sp.symbols("x u v w")


def cleared_repeated_linear_row(node, first, zeroth):
    """Quartic row for q''+2Yq'+Mq on q=q0+q1*z.

    ``first`` is A and ``zeroth`` is L=A^2+K.
    """
    denominator = x**2 - node**2
    numerator = 3 * node - x
    p = (
        zeroth * denominator**2
        + 2 * first * numerator * denominator
        + 4 * (x**2 - 2 * node * x + 3 * node**2)
    )
    q = (
        node * p
        + 2 * first * denominator**2
        + 2 * numerator * denominator
    )
    return tuple(map(sp.expand, (p, q)))


def determinant(first, second):
    return sp.expand(first[0] * second[1] - first[1] * second[0])


def check_repeated_row() -> None:
    t, A, K = sp.symbols("t A K")
    d = x**2 - t**2
    psi = (3 * t - x) / d
    eta = (3 * x**2 - 2 * t * x + 3 * t**2) / d**2
    Y = A + psi
    M = Y**2 + K + eta
    expected = tuple(sp.cancel(d**2 * entry) for entry in (M, 2 * Y + t * M))
    actual = cleared_repeated_linear_row(t, A, A**2 + K)
    assert all(sp.factor(left - right) == 0 for left, right in zip(actual, expected))
    assert all(sp.Poly(entry, x).degree() <= 4 for entry in actual)
    for entry, evaluation in zip(actual, (1, t)):
        assert sp.factor(entry.subs(x, t) - 8 * t**2 * evaluation) == 0
        assert sp.factor(entry.subs(x, -t) - 24 * t**2 * evaluation) == 0


def check_pair_nonidentity() -> None:
    Au, Lu, Av, Lv = sp.symbols("Au Lu Av Lv")
    row_u = cleared_repeated_linear_row(u, Au, Lu)
    row_v = cleared_repeated_linear_row(v, Av, Lv)
    pair = determinant(row_u, row_v)
    assert sp.Poly(pair, x).degree() <= 8

    endpoint_v = [sp.factor((row_v[1] - u * row_v[0]).subs(x, sign * u)) for sign in (1, -1)]
    endpoint_u = [sp.factor((row_u[1] - v * row_u[0]).subs(x, sign * v)) for sign in (1, -1)]
    solved_v = sp.solve(endpoint_v, (Av, Lv), dict=True)
    solved_u = sp.solve(endpoint_u, (Au, Lu), dict=True)
    assert len(solved_v) == len(solved_u) == 1
    expected_v = {
        Av: (u - 3 * v) / (u**2 - v**2),
        Lv: -2 * (u + 3 * v) / ((u - v) * (u + v) ** 2),
    }
    expected_u = {
        Au: (3 * u - v) / (u**2 - v**2),
        Lu: 2 * (3 * u + v) / ((u - v) * (u + v) ** 2),
    }
    assert all(
        sp.factor(solved_v[0][symbol] - value) == 0
        for symbol, value in expected_v.items()
    )
    assert all(
        sp.factor(solved_u[0][symbol] - value) == 0
        for symbol, value in expected_u.items()
    )

    specialized = sp.factor(pair.subs({**solved_u[0], **solved_v[0]}))
    W = sp.cancel(
        specialized * (u - v) * (u + v) ** 4
        / (4 * (x**2 - u**2) * (x**2 - v**2))
    )
    W = sp.Poly(sp.expand(W), x)
    assert W.degree() == 4
    assert sp.factor(W.coeff_monomial(x**4) - (9 * u**2 + 22 * u * v + 9 * v**2)) == 0
    assert sp.factor(
        W.coeff_monomial(x**3)
        + 4 * (u + v) * (u**2 + 6 * u * v + v**2)
    ) == 0
    ratio = sp.symbols("ratio")
    assert sp.resultant(
        9 * ratio**2 + 22 * ratio + 9,
        ratio**2 + 6 * ratio + 1,
        ratio,
    ) == 1024


def coefficient_span_matrix(nodes):
    columns = []
    for node in nodes:
        first, zeroth = sp.symbols(f"A_{node} L_{node}")
        row = cleared_repeated_linear_row(node, first, zeroth)
        vector = sp.Matrix([
            sp.Poly(component, x).coeff_monomial(x**degree)
            for component in row
            for degree in range(5)
        ])
        columns.extend((
            vector.diff(zeroth),
            vector.diff(first),
            vector.subs({first: 0, zeroth: 0}),
        ))
    return sp.Matrix.hstack(*columns)


def check_shared_minor_and_four_anchor_obstruction() -> None:
    matrix = coefficient_span_matrix((u, v, w))
    assert matrix.shape == (10, 9)
    # Omit the constant coefficient of the second row component.
    rows = [index for index in range(10) if index != 5]
    maximal_minor = sp.factor(matrix.extract(rows, range(9)).det(method="domain-ge"))
    f = u**2 + v**2 + w**2 + 11 * (u * v + u * w + v * w)
    assert maximal_minor == 192 * (u - v) ** 3 * (u - w) ** 3 * (v - w) ** 3 * f

    sum_wz = -11 * (u + v)
    product_wz = u**2 + v**2 + 11 * u * v
    f_uwz = sp.expand(
        u**2 + (sum_wz**2 - 2 * product_wz)
        + 11 * (u * sum_wz + product_wz)
    )
    f_vwz = sp.expand(
        v**2 + (sum_wz**2 - 2 * product_wz)
        + 11 * (v * sum_wz + product_wz)
    )
    assert sp.factor(
        f_uwz - 10 * (u**2 + 22 * u * v + 13 * v**2)
    ) == 0
    assert sp.factor(
        f_vwz - 10 * (13 * u**2 + 22 * u * v + v**2)
    ) == 0
    assert sp.factor(
        f_uwz - f_vwz + 120 * (u - v) * (u + v)
    ) == 0


def check_mixed_bivariate_row_and_endpoint_identity() -> None:
    y, t, A, K = sp.symbols("y t A K")

    def phi(node, moving):
        return (5 * node - moving) / (moving**2 - node**2)

    def eta(node, moving):
        return sp.diff(phi(t, moving), t).subs(t, node)

    dx = x**2 - t**2
    dy = y**2 - t**2
    Y = A + phi(t, x) + phi(t, y)
    M = Y**2 + K + eta(t, x) + eta(t, y)
    repeated = [
        sp.cancel(dx**2 * dy**2 * entry).expand()
        for entry in (M, 2 * Y + t * M)
    ]
    assert all(sp.denom(entry) == 1 for entry in repeated)
    assert all(sp.Poly(entry, x, y).degree(x) <= 4 for entry in repeated)
    assert all(sp.Poly(entry, x, y).degree(y) <= 4 for entry in repeated)
    for entry, evaluation in zip(repeated, (1, t)):
        assert sp.factor(entry.subs(x, t) - 24 * t**2 * dy**2 * evaluation) == 0
        assert sp.factor(entry.subs(x, -t) - 48 * t**2 * dy**2 * evaluation) == 0

    a, C = sp.symbols("a C")
    da_x = x**2 - a**2
    da_y = y**2 - a**2
    simple_Y = C + phi(a, x) + phi(a, y)
    simple = [
        sp.cancel(da_x * da_y * entry).expand()
        for entry in (simple_Y, 1 + a * simple_Y)
    ]
    assert all(sp.Poly(entry, x, y).degree(x) <= 2 for entry in simple)
    assert all(sp.Poly(entry, x, y).degree(y) <= 2 for entry in simple)
    mixed = sp.Poly(determinant(repeated, simple), x, y)
    assert mixed.degree(x) <= 6 and mixed.degree(y) <= 6

    moving, anchor, repeated_node = sp.symbols("moving anchor repeated_node")
    plus, minus, scale = sp.symbols("Aplus Aminus scale")
    q_plus = plus * (moving**2 - anchor**2) + 5 * anchor - moving
    q_minus = minus * (moving**2 - anchor**2) + 5 * anchor - moving
    identity = sp.Poly(
        sp.expand(
            (repeated_node - moving) * q_plus
            - scale * (repeated_node + moving) * q_minus
        ),
        moving,
    )
    cubic = identity.coeff_monomial(moving**3)
    quadratic = identity.coeff_monomial(moving**2)
    linear = identity.coeff_monomial(moving)
    constant = identity.coeff_monomial(1)
    assert cubic == -plus - scale * minus
    assert quadratic == repeated_node * plus - repeated_node * scale * minus + scale + 1
    # Apply the two leading equations without dividing by any symbol.
    reduced_linear = sp.expand(linear.subs(scale * minus, -plus).subs(
        scale, -1 - 2 * repeated_node * plus
    ))
    reduced_constant = sp.expand(constant.subs(scale * minus, -plus).subs(
        scale, -1 - 2 * repeated_node * plus
    ))
    assert sp.factor(
        reduced_linear
        + 2 * repeated_node * (
            plus * (repeated_node - 5 * anchor) + 1
        )
    ) == 0
    assert sp.factor(
        reduced_constant
        + 2 * anchor * repeated_node * (
            plus * (anchor - 5 * repeated_node) - 5
        )
    ) == 0


POST_DR4 = {
    8: (4, 5, 6, 7, 8),
    9: (5, 6, 7, 8, 9),
    10: (6, 7, 8, 9),
    11: (7, 9, 10),
    12: (10,),
}
EXPECTED = {8: (7, 8)}


def check_legality_and_census() -> None:
    for p, doubles_list in POST_DR4.items():
        total = p + 9
        remaining = []
        for doubles in doubles_list:
            singles = total - 2 * doubles
            classes = doubles + singles

            # Three full doubles plus a simple-moving class.  For s>=2,
            # all c-3 outside classes are legal.  Nine roots are strict;
            # eight roots are closed by the shared-minor argument.
            repeated_closed = (
                doubles >= 4 and singles >= 2 and classes - 3 >= 8
            )

            # Either use a singleton anchor and leave another singleton,
            # or use one copy of a second double as the permanent guard.
            mixed_candidates = max(
                doubles - 1 if singles >= 2 else 0,
                doubles - 2 if doubles >= 2 else 0,
            )
            mixed_closed = mixed_candidates >= 7
            if not repeated_closed and not mixed_closed:
                remaining.append(doubles)
        assert tuple(remaining) == EXPECTED.get(p, ())

    assert (7, 3) == (7, 8 + 9 - 2 * 7)
    assert (8, 1) == (8, 8 + 9 - 2 * 8)


def main() -> None:
    check_repeated_row()
    check_pair_nonidentity()
    check_shared_minor_and_four_anchor_obstruction()
    check_mixed_bivariate_row_and_endpoint_identity()
    check_legality_and_census()
    print("low-class repeated-row seventh-split audit: PASS")
    print("shared degree-eight boundary c=11: CLOSED")
    print("mixed seven-value bivariate boundary: CLOSED")
    print("remaining profiles: p=8, (d,s)=(7,3),(8,1)")


if __name__ == "__main__":
    main()
