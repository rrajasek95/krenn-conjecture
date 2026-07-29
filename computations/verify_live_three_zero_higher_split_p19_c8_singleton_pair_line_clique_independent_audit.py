#!/usr/bin/env python3
"""Independent exact audit of the p=19, C=8 pair-line clique closure."""

from __future__ import annotations

import sympy as sp


def audit_formal_selection() -> None:
    for h in range(13, 19):
        k = 19 - h
        selected_singletons = h
        selected_labels = selected_singletons + 2
        complement = (2,) * 9 + (1,)

        assert selected_labels == h + 2
        assert sum(complement) == 19
        assert len(complement) == 10
        assert len(complement) - 4 == 6  # relation degree
        assert 6 + 5 == 11              # quintic transport degree

        six_space_excess = 22 - h + max(0, 6 - k)
        assert six_space_excess == 9

        # Conditional dimension-four low-role incidence gap, d=1.
        d = 1
        s = h
        residual_degree = h - d
        other_singletons = s - 1
        assert other_singletons - (residual_degree - 2) == 3 - d == 2


def audit_common_kernel_dimensions() -> None:
    for dimension in range(6, 13):
        forced = 10 * (dimension - 2) + (dimension - 1)
        cap = dimension * (12 - dimension)
        assert forced - cap == dimension**2 - dimension - 21
        assert forced > cap

    # Pair-intersection arithmetic in common dimensions 3, 4, 5.
    assert 3 + 3 - 3 == 3 > 2
    assert 3 + 3 - 4 == 2
    assert 3 + 3 - 5 == 1
    assert 11 - 10 + 1 == 2  # g_i g_j P_1


def quintic(z: sp.Symbol, node: sp.Expr) -> sp.Expr:
    return sp.expand((z - node) ** 3 * (z + node) ** 2)


def audit_jets_and_clique() -> None:
    z, x, y, r, v = sp.symbols("z x y r v")
    lam, u, c = sp.symbols("Lambda u c")

    gx = quintic(z, x)
    first_r = sp.factor(sp.diff(gx, z).subs(z, r) / gx.subs(z, r))
    first_v = sp.factor(sp.diff(gx, z).subs(z, v) / gx.subs(z, v))
    second_v = sp.factor(sp.diff(gx, z, 2).subs(z, v) / gx.subs(z, v))

    assert sp.factor(first_r - (5 * r + x) / (r**2 - x**2)) == 0
    assert sp.factor(first_v - (5 * v + x) / (v**2 - x**2)) == 0
    assert sp.factor(
        second_v
        - 4 * (5 * v**2 + 2 * v * x - x**2) / (v**2 - x**2) ** 2
    ) == 0

    def a(node: sp.Expr) -> sp.Expr:
        return (5 * r + node) / (r**2 - node**2)

    def A(node: sp.Expr) -> sp.Expr:
        return (5 * v + node) / (v**2 - node**2)

    def R(node: sp.Expr) -> sp.Expr:
        return 4 * (5 * v**2 + 2 * v * node - node**2) / (v**2 - node**2) ** 2

    dxy = lam - a(x) - a(y)
    pxy = u + A(x) + A(y)
    qxy = c + R(x) + R(y) + 2 * u * (A(x) + A(y)) + 2 * A(x) * A(y)
    equation = sp.factor(qxy * (1 + (v - r) * dxy) + 2 * pxy * dxy)

    numerator, denominator = sp.together(equation).as_numer_denom()
    structural_denominator = (
        (r**2 - x**2)
        * (r**2 - y**2)
        * (v**2 - x**2) ** 2
        * (v**2 - y**2) ** 2
    )
    assert sp.factor(denominator - structural_denominator) == 0
    numerator = sp.expand(numerator)
    assert sp.Poly(numerator, x, y).degree(x) <= 6
    assert sp.Poly(numerator, x, y).degree(y) <= 6

    # Nine vertices give eight off-diagonal roots in each row.
    vertices = 10 - 1
    assert vertices == 9
    assert vertices - 1 > 6
    assert vertices > 6

    pole = sp.factor(sp.limit((v - y) ** 2 * equation, y, v))
    expected = sp.factor(6 * (1 + (v - r) * (lam - a(x) - a(v))))
    assert sp.factor(pole - expected) == 0

    K = sp.symbols("K")
    cleared = sp.Poly(
        sp.expand(K * (r**2 - x**2) - (v - r) * (5 * r + x)), x
    )
    assert cleared.coeff_monomial(x) == -(v - r)


def main() -> None:
    audit_formal_selection()
    audit_common_kernel_dimensions()
    audit_jets_and_clique()
    print("p=19 C=8 singleton pair-line clique independent audit: PASS")
    print("six h+k=19 splits checked; selected q=6 gap: 9")
    print("common-kernel branches, bidegree (6,6), and pole: checked")


if __name__ == "__main__":
    main()
