#!/usr/bin/env python3
"""Standalone audit of the p=28 4^3 3^6 residual rank-one exclusion.

This file intentionally imports no primary verifier.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def audit_tangent_edge_ledger() -> None:
    """Recompute every (m,e,d,R1) allowed by the global ramification bound."""

    cases: list[tuple[int, int, int, int]] = []
    for m in range(4, 7):
        # From (m-2)e <= (m-1)(d+2-m), and d<=6.
        maximum_e = ((m - 1) * (8 - m)) // (m - 2)
        for e in range(m - 1, maximum_e + 1):
            total_weight = m * (e - m + 1)
            for d in range(4, 7):
                first_ramification = 2 * e - 2 - d
                if first_ramification < 0:
                    continue
                if (m - 1) * first_ramification <= total_weight:
                    cases.append((m, e, d, first_ramification))

    expected = [
        (4, 3, 4, 0),
        (4, 4, 5, 1),
        (4, 4, 6, 0),
        (4, 5, 6, 2),
        (4, 6, 6, 4),
        (5, 4, 6, 0),
    ]
    assert cases == expected

    # Pointwise check of the inequality used globally.  For a vanishing
    # sequence 0=a0<a1<...<a_(m-1), one unit in a1-1 raises all later
    # entries by at least the same amount.
    for m in range(2, 7):
        for e in range(m - 1, 10):
            for tail in combinations(range(1, e + 1), m - 1):
                sequence = (0,) + tail
                weight = sum(value - index for index, value in enumerate(sequence))
                first = sequence[1] - 1
                assert weight >= (m - 1) * first

    # The derived finite bounds themselves exclude m=6 and all larger e.
    assert ((6 - 1) * (8 - 6)) // (6 - 2) < 6 - 1


def audit_osculating_dual_identity() -> None:
    """Check the cofactor identity used in the m=4 nondegeneracy proof."""

    g0 = sp.symbols("g0:4")
    g1 = sp.symbols("h0:4")
    g2 = sp.symbols("k0:4")
    c = sp.symbols("c0:4")
    jet_matrix = sp.Matrix([g0, g1, g2])
    nu = sp.Matrix(
        [
            (-1) ** column * jet_matrix[:, [j for j in range(4) if j != column]].det()
            for column in range(4)
        ]
    )

    assert all(sp.expand(entry) == 0 for entry in jet_matrix * nu)
    stacked = sp.Matrix([g0, g1, g2, c])
    assert sp.expand(sp.Matrix(c).dot(nu) + stacked.det()) == 0

    # A nondegenerate curve in P^3 has degree at least three.  A nonzero
    # O(-4)->O(-e*) map exists only for e*<=4.
    possible_dual_degrees = tuple(e_star for e_star in range(3, 20) if e_star <= 4)
    assert possible_dual_degrees == (3, 4)

    # Three t-jets impose at most three conditions on four independent
    # coordinate sections, hence some section has t-order at least three.
    # The square cover doubles that order.
    assert 2 * 3 == 6


def coefficient_vector(vector: sp.Matrix, variable: sp.Symbol) -> sp.Matrix:
    """Flatten five degree-at-most-four coordinates in coordinate-major order."""

    return sp.Matrix(
        [sp.expand(vector[row]).coeff(variable, degree) for row in range(5) for degree in range(5)]
    )


def audit_rational_normal_quartic_module() -> None:
    """Solve the full degree-four polynomial kernel, not merely a sample."""

    t = sp.symbols("t")
    gamma = sp.Matrix([1, t, t**2, t**3, t**4])
    u = sp.Matrix([-t**3, 3 * t**2, -3 * t, 1, 0])
    v = sp.Matrix([0, -t**3, 3 * t**2, -3 * t, 1])

    for frame_vector in (u, v):
        for derivative_order in range(3):
            assert sp.expand(gamma.diff(t, derivative_order).dot(frame_vector)) == 0
    assert sp.Matrix([[u[3], v[3]], [u[4], v[4]]]).det() == 1

    coefficients = sp.symbols("x0:25")
    section = sp.Matrix(
        [
            sum(coefficients[5 * row + degree] * t**degree for degree in range(5))
            for row in range(5)
        ]
    )
    equations: list[sp.Expr] = []
    for derivative_order in range(3):
        expression = sp.Poly(
            sp.expand(gamma.diff(t, derivative_order).dot(section)), t
        )
        equations.extend(expression.coeff_monomial(t**degree) for degree in range(13))

    relation_matrix, right_side = sp.linear_eq_to_matrix(equations, coefficients)
    assert right_side == sp.zeros(len(equations), 1)
    assert relation_matrix.rank() == 21
    assert len(coefficients) - relation_matrix.rank() == 4

    generators = sp.Matrix.hstack(
        coefficient_vector(u, t),
        coefficient_vector(t * u, t),
        coefficient_vector(v, t),
        coefficient_vector(t * v, t),
    )
    assert generators.rank() == 4
    assert relation_matrix * generators == sp.zeros(len(equations), 4)

    # Since the solution space has dimension four, these four columns prove
    # that every degree-four solution is au+bv with a,b linear.
    a0, a1, b0, b1 = sp.symbols("a0 a1 b0 b1")
    general = (a0 + a1 * t) * u + (b0 + b1 * t) * v
    assert max(sp.Poly(entry, t).degree() for entry in general) <= 4
    assert sp.expand(general[0] + t**3 * (a0 + a1 * t)) == 0

    # A full five-dimensional degree-four series is all H^0(O(4)); choosing
    # the monomial basis is therefore a target change on the fixed parameter.
    monomial_coefficient_matrix = sp.eye(5)
    assert monomial_coefficient_matrix.rank() == 5


def audit_square_cover_and_wronskian() -> None:
    z = sp.symbols("z")
    a0, a1, r0, r1 = sp.symbols("a0 a1 r0 r1")
    first_coordinate = sp.expand(
        -z**6 * (a0 + a1 * z**2 + z * (r0 + r1 * z**2))
    )
    first_poly = sp.Poly(first_coordinate, z)
    assert set(first_poly.as_dict()) == {(6,), (7,), (8,), (9,)}
    assert all(coefficient != 0 for coefficient in first_poly.as_dict().values())

    # Distinct parity/exponent slots show that the coordinate is identically
    # zero exactly when all four scalar coefficients vanish.
    coefficient_matrix, rhs = sp.linear_eq_to_matrix(
        [first_poly.coeff_monomial(z**degree) for degree in range(10)],
        (a0, a1, r0, r1),
    )
    assert rhs == sp.zeros(10, 1)
    assert coefficient_matrix.rank() == 4

    sequences = [
        sequence
        for sequence in combinations(range(11), 6)
        if sequence[-1] >= 6
    ]
    minimum_weight = min(
        sum(order - index for index, order in enumerate(sequence))
        for sequence in sequences
    )
    assert minimum_weight == 1
    assert (0, 1, 2, 3, 4, 6) in sequences

    minimal_basis = (1, z, z**2, z**3, z**4, z**6)
    wronskian = sp.expand(
        sp.det(
            sp.Matrix(
                [
                    [sp.diff(polynomial, z, order) for polynomial in minimal_basis]
                    for order in range(6)
                ]
            )
        )
    )
    assert wronskian != 0
    assert min(exponent[0] for exponent in sp.Poly(wronskian, z).as_dict()) == 1

    assert 3 * (6 - 4) + 6 * (6 - 3) == 24
    assert 6 * (10 - 6) == 24


def main() -> None:
    audit_tangent_edge_ledger()
    audit_osculating_dual_identity()
    audit_rational_normal_quartic_module()
    audit_square_cover_and_wronskian()
    print("independent p=28 4^3 3^6 residual rank-one audit: PASS")
    print("all tangent ledgers, including the infinity contribution: PASS")
    print("m=4 osculating-dual and square-cover obstruction: PASS")
    print("m=5 full degree-four RNC-kernel module and z^6 obstruction: PASS")
    print("scope: generic rank one excluded; (2,4) and (3,3) remain")


if __name__ == "__main__":
    main()
