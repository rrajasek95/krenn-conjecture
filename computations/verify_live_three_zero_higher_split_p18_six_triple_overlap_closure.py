#!/usr/bin/env python3
"""Exact audit for the p=18 six-triple overlap closure."""

from __future__ import annotations

import sympy as sp


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


def wronskian(polys: list[sp.Expr], z: sp.Symbol) -> sp.Expr:
    size = len(polys)
    matrix = sp.Matrix(
        [[sp.diff(poly, z, order) for poly in polys] for order in range(size)]
    )
    return sp.factor(matrix.det())


def assert_zero(expr: sp.Expr) -> None:
    require(
        sp.factor(sp.together(expr)) == 0,
        sp.factor(sp.together(expr)),
    )


def audit_diagonal() -> None:
    for h in range(13, 18):
        k = 18 - h
        require(
            h + k == 18,
            "h + k == 18",
        )
        # The q=5 selected bound is equality and q=6 is strictly impossible.
        q5 = 5**2 - 2 * 5 - h - 2 + max(0, 5 - k)
        q6 = 6**2 - 2 * 6 - h - 2 + max(0, 6 - k)
        require(
            q5 == 0,
            "q5 == 0",
        )
        require(
            q6 == 10,
            "q6 == 10",
        )

        for d in range(3):
            singleton_count = h + 2 - 2 * d
            layer_count = d + singleton_count
            degree_cap = h + 3 - d
            require(
                layer_count == h + 2 - d,
                "layer_count == h + 2 - d",
            )
            require(
                degree_cap + 1 == layer_count + 2,
                "degree_cap + 1 == layer_count + 2",
            )
            # Five-dimensional kernel -> three-dimensional row relations.
            require(
                layer_count - ((degree_cap + 1) - 5) == 3,
                "layer_count - ((degree_cap + 1) - 5) == 3",
            )
            # The whole profile has the required total mass h+20=2h+k+2.
            require(
                18 + 2 * d + singleton_count == 2 * h + k + 2,
                "18 + 2 * d + singleton_count == 2 * h + k + 2",
            )
            # Selected Wronskian equality.
            forced = 3 * d + 4 * singleton_count + (5 - k)
            cap = 5 * (degree_cap + 1 - 5)
            require(
                forced == cap,
                "forced == cap",
            )


def audit_six_triple_normal_form() -> None:
    z = sp.symbols("z")
    roots = tuple(map(sp.Integer, (1, 2, 3, 4, 5, 6)))
    coeffs = tuple(map(sp.Integer, (2, -3, 5, 7, -11, 13)))
    R = sp.prod(z - root for root in roots)
    rhs = sum(
        coeff * sp.cancel(R / (z - root)) ** 4
        for root, coeff in zip(roots, coeffs)
    )
    require(
        sp.degree(rhs, z) <= 20,
        "sp.degree(rhs, z) <= 20",
    )
    assert_zero(rhs / R**4 - sum(
        coeff / (z - root) ** 4
        for root, coeff in zip(roots, coeffs)
    ))

    # At each root the unit in front of the fourth pole has its first
    # three derivatives zero, exactly as forced by S=P_2.
    for root, coeff in zip(roots, coeffs):
        unit = sp.cancel((z - root) ** 4 * rhs / R**4)
        require(
            sp.simplify(unit.subs(z, root)) == coeff,
            "sp.simplify(unit.subs(z, root)) == coeff",
        )
        for order in range(1, 4):
            require(
                sp.simplify(sp.diff(unit, z, order).subs(z, root)) == 0,
                "sp.simplify(sp.diff(unit, z, order).subs(z, root)) == 0",
            )


def audit_three_simple_space() -> None:
    z, x, r, s = sp.symbols("z x r s")
    basis = [
        (z - x) ** 2 * (z - r) ** 2,
        (z - x) ** 2 * (z - s) ** 2,
        (z - r) ** 2 * (z - s) ** 2,
    ]
    wr = wronskian(basis, z)
    target = (z - x) ** 2 * (z - r) ** 2 * (z - s) ** 2
    assert_zero(sp.diff(wr / target, z))
    require(
        wr != 0,
        "wr != 0",
    )

    nonzero_section = basis[-1]
    robin = -sp.diff(nonzero_section, z).subs(z, x) / nonzero_section.subs(z, x)
    assert_zero(robin + 2 / (x - r) + 2 / (x - s))

    pair_difference = 1 / x - 1 / (x + r) - 1 / (x + s)
    assert_zero(
        pair_difference - (r * s - x**2) / (x * (x + r) * (x + s))
    )


def audit_simple_double_space() -> None:
    z, x, v = sp.symbols("z x v")
    l0 = sp.Integer(1)
    l1 = (2 * x + v) / 3
    l2 = (x**2 + 2 * x * v) / 3
    l3 = x**2 * v

    # A basis for the kernel of L_{x,v}; structural admissibility makes
    # x and v nonzero, so this chart is valid.
    basis = [
        1 - l0 * z**3 / l3,
        z - l1 * z**3 / l3,
        z**2 - l2 * z**3 / l3,
    ]
    wr = wronskian(basis, z)
    target = (z - x) ** 2 * (z - v)
    assert_zero(sp.diff(wr / target, z))
    require(
        wr != 0,
        "wr != 0",
    )

    beta = 3 / (v - x)
    robin_row = sp.Matrix(
        [beta, 1 + beta * x, 2 * x + beta * x**2, 3 * x**2 + beta * x**3]
    )
    functional = sp.Matrix([l0, l1, l2, l3])
    for coordinate in robin_row - beta * functional:
        assert_zero(coordinate)

    double_difference = 1 / x - 2 / (x + v)
    assert_zero(double_difference - (v - x) / (x * (x + v)))


def audit_local_units() -> None:
    z, x, mu, u, v, r, s, b, y = sp.symbols(
        "z x mu u v r s b y"
    )

    # One placeholder factor for each unchanged product is enough to audit
    # every logarithmic coefficient.  R_x=(z-b), H_0=(z+y).
    Rx = z - b
    H0 = z + y
    Q0 = z + u

    base_T = (z + mu) ** sp.Symbol("k", integer=True, positive=True) * Q0**2
    base_T *= (z + v) ** 2 * (z + r) * (z + s) * H0
    base_unit = base_T / Rx**4

    # d<=1 promotion: v is omitted from this comparison; retain the
    # unchanged Q0 and H0, add x at role two, and move r,s to A.
    promoted_unit = (
        (z + mu) ** sp.Symbol("k", integer=True, positive=True)
        * Q0**2
        * (z + x) ** 2
        * H0
        / (Rx**4 * (z - r) ** 2 * (z - s) ** 2)
    )
    promoted_log = sp.diff(sp.log(promoted_unit), z).subs(z, x)
    expected_promoted = (
        sp.Symbol("k", integer=True, positive=True) / (x + mu)
        + 2 / (x + u)
        + 1 / x
        + 1 / (x + y)
        - 4 / (x - b)
        - 2 / (x - r)
        - 2 / (x - s)
    )
    assert_zero(promoted_log - expected_promoted)

    # d=2 exchange: v moves from Q to a double complementary factor.
    exchanged_unit = (
        (z + mu) ** sp.Symbol("k", integer=True, positive=True)
        * Q0**2
        * (z + x) ** 2
        * H0
        / (Rx**4 * (z - v) ** 3)
    )
    exchanged_log = sp.diff(sp.log(exchanged_unit), z).subs(z, x)
    expected_exchanged = (
        sp.Symbol("k", integer=True, positive=True) / (x + mu)
        + 2 / (x + u)
        + 1 / x
        + 1 / (x + y)
        - 4 / (x - b)
        - 3 / (x - v)
    )
    assert_zero(exchanged_log - expected_exchanged)

    # The base unit has coefficient two at every selected double and one
    # at every selected singleton.
    base_log = sp.diff(sp.log(base_unit), z).subs(z, x)
    expected_base = (
        sp.Symbol("k", integer=True, positive=True) / (x + mu)
        + 2 / (x + u)
        + 2 / (x + v)
        + 1 / (x + r)
        + 1 / (x + s)
        + 1 / (x + y)
        - 4 / (x - b)
    )
    assert_zero(base_log - expected_base)


def main() -> None:
    audit_diagonal()
    audit_six_triple_normal_form()
    audit_three_simple_space()
    audit_simple_double_space()
    audit_local_units()
    print("PASS: p=18 six-triple overlap closure audited exactly")


if __name__ == "__main__":
    main()
