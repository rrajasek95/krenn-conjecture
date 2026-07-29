#!/usr/bin/env python3
"""Exact audit of the DR4 closure of the all-distinct t=r+6 sector.

The full four-anchor theorem is audited separately by the DR4 checkers.
This file verifies every algebraic and counting step needed to apply that
theorem to the sole-plane fourth-high layer.
"""

from __future__ import annotations

from itertools import permutations

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.rings import ring


def audit_row_bridge() -> None:
    """The sole-plane cleared row is exactly the DR4 row at t=-y."""
    x, y, u, z = sp.symbols("x y U z")
    basis = (sp.Integer(1), z, z**2, z**3)

    sole_rows = []
    dr4_rows = []
    for polynomial in basis:
        sole_rows.append(
            sp.expand(
                (x**2 - y**2)
                * (
                    sp.diff(polynomial, z).subs(z, -y)
                    + u * polynomial.subs(z, -y)
                )
                - (x + 3*y) * polynomial.subs(z, -y)
            )
        )
        t = -y
        dr4_rows.append(
            sp.expand(
                (x**2 - t**2)
                * (
                    sp.diff(polynomial, z).subs(z, t)
                    + u * polynomial.subs(z, t)
                )
                - (x - 3*t) * polynomial.subs(z, t)
            )
        )
    assert sole_rows == dr4_rows

    # The genuine zero-translation branch is the canonical DR4 kernel.
    gauge = (z - x) * (z + x) ** 2
    gauge_row = sp.expand(
        (x**2 - y**2) * sp.diff(gauge, z).subs(z, -y)
        - (x + 3*y) * gauge.subs(z, -y)
    )
    assert gauge_row == 0


def audit_sharp_degree_bound() -> None:
    """Build the universal sparse determinant and check degree at most eight."""
    polynomial_ring, x, a, b, c, d, A, B, C, D = ring(
        "x,a,b,c,d,A,B,C,D", QQ
    )
    anchors = (a, b, c, d)
    translations = (A, B, C, D)
    rows = []
    for y, u in zip(anchors, translations, strict=True):
        denominator = x*x - y*y
        rows.append(
            (
                u*denominator - x - 3*y,
                denominator - y*(u*denominator - x - 3*y),
                -2*y*denominator + y*y*(u*denominator - x - 3*y),
                3*y*y*denominator - y**3*(u*denominator - x - 3*y),
            )
        )

    determinant = polynomial_ring.zero
    for sigma in permutations(range(4)):
        inversions = sum(
            sigma[i] > sigma[j]
            for i in range(4)
            for j in range(i + 1, 4)
        )
        term = polynomial_ring.one
        for row_index in range(4):
            term *= rows[row_index][sigma[row_index]]
        determinant += (-1 if inversions % 2 else 1) * term

    x_degrees = {monomial[0] for monomial, _ in determinant.terms()}
    assert x_degrees == set(range(9))
    assert max(x_degrees) == 8

    # At U=0 the determinant vanishes identically, as the gauge above says.
    assert all(
        any(monomial[index] for index in range(5, 9))
        for monomial, _ in determinant.terms()
    )


def audit_root_and_fibre_counts() -> None:
    """Check the two strict cardinality inequalities used uniformly in r."""
    for r in range(7, 80):
        exceptional_count = r + 6
        moving_roots_for_a_fixed_four_core = exceptional_count - 4
        assert moving_roots_for_a_fixed_four_core == r + 2
        assert moving_roots_for_a_fixed_four_core > 8

        # An all-distinct structural set contains at most one zero.  After
        # fixing three nonzero anchors, these are the eligible fourth anchors.
        eligible_fourth_anchors = (exceptional_count - 1) - 3
        assert eligible_fourth_anchors == r + 2
        assert eligible_fourth_anchors > 2

    a, c, d, lam, y = sp.symbols("a c d lambda y")

    def psi(left, right):
        return 1/(left + right) - 2/(right - left)

    difference = sp.factor(sp.together(psi(a, c) - psi(a, d)))
    expected = sp.factor(
        (c-d) * (a**2 + 3*a*(c+d) + c*d)
        / ((a**2-c**2) * (a**2-d**2))
    )
    assert sp.factor(difference - expected) == 0

    fibre_equation = sp.together(psi(a, y) - lam).as_numer_denom()[0]
    expected_fibre = -(lam*(y**2-a**2) + y + 3*a)
    assert sp.expand(fibre_equation - expected_fibre) == 0
    assert sp.Poly(-expected_fibre, y).degree() == 2
    # Even when lambda=0 the coefficient of y is one, so this family never
    # becomes the zero polynomial and every fibre has cardinality at most two.
    assert sp.Poly(-expected_fibre, y).coeff_monomial(y) == 1


def main() -> None:
    audit_row_bridge()
    print("sole-plane cubic rows equal DR4 rows under t_i=-a_i: exact")
    audit_sharp_degree_bound()
    print("universal cleared determinant has sharp degree eight: exact")
    audit_root_and_fibre_counts()
    print("strict nine-root identity and quadratic-fibre contradiction: exact")
    print("sole-plane t=r+6 all-distinct DR4 closure: AUDIT PASS")


if __name__ == "__main__":
    main()
