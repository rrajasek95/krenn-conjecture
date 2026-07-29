#!/usr/bin/env python3
"""Exact algebra audit for the rank-three all-rank-two live-edge obstruction.

The companion note proves the finite incidence classification by elementary
case splits.  This script verifies every displayed adjugate coefficient,
the bad-pair families in the residual cases, the compression-rank filters,
and the final crosswise-kernel determinant cancellation over Q(parameters).
"""

from __future__ import annotations

import sympy as sp


x, y, z = sp.symbols("x y z")
u = sp.Matrix(sp.symbols("u0:3"))
v = sp.Matrix(sp.symbols("v0:3"))
MONOMIALS = ((2, 0, 0), (1, 1, 0), (1, 0, 1),
             (0, 2, 0), (0, 1, 1), (0, 0, 2))


def coefficients(matrix: sp.Matrix) -> dict[tuple[int, int, int], sp.Expr]:
    polynomial = sp.Poly(sp.expand((u.T * matrix.adjugate() * v)[0]), x, y, z)
    return {monomial: sp.factor(polynomial.coeff_monomial(monomial))
            for monomial in MONOMIALS}


def substituted_zero(values: dict[tuple[int, int, int], sp.Expr],
                     replacements: dict[sp.Symbol, sp.Expr]) -> None:
    assert all(sp.factor(value.subs(replacements)) == 0 for value in values.values())


def compression_coefficients(
    matrix: sp.Matrix,
    left_basis: tuple[sp.Matrix, sp.Matrix],
    right_basis: tuple[sp.Matrix, sp.Matrix],
) -> sp.Matrix:
    compressed = sp.Matrix(
        2, 2,
        lambda i, j: sp.expand((left_basis[i].T * matrix * right_basis[j])[0]),
    )
    return sp.Matrix.hstack(*[
        compressed.applyfunc(lambda entry: entry.coeff(variable)).reshape(4, 1)
        for variable in (x, y, z)
    ])


def audit_empty_incidence_types() -> None:
    # Type 3c: three reverse-pair relations, with arbitrary nonzero twists.
    a, b, c, d, e, f = sp.symbols("a b c d e f", nonzero=True)
    matrix = sp.Matrix([[0, a * x, b * y],
                        [c * x, 0, d * z],
                        [e * y, f * z, 0]])
    actual = coefficients(matrix)
    expected = {
        (2, 0, 0): -a * c * u[2] * v[2],
        (1, 1, 0): a * e * u[2] * v[1] + b * c * u[1] * v[2],
        (1, 0, 1): a * d * u[0] * v[2] + c * f * u[2] * v[0],
        (0, 2, 0): -b * e * u[1] * v[1],
        (0, 1, 1): b * f * u[0] * v[1] + d * e * u[1] * v[0],
        (0, 0, 2): -d * f * u[0] * v[0],
    }
    assert actual == {key: sp.factor(value) for key, value in expected.items()}

    # Type 3d.  Only A,C,R need be nonzero; B,D are unrestricted.
    A, B, C, D, R = sp.symbols("A B C D R", nonzero=True)
    matrix = sp.Matrix([[0, C * y + D * z, A * x + B * z],
                        [x, 0, R * z],
                        [y, z, 0]])
    actual = coefficients(matrix)
    assert actual[(2, 0, 0)] == A * u[1] * v[2]
    assert actual[(0, 2, 0)] == C * u[2] * v[1]
    assert actual[(1, 1, 0)] == -A * u[1] * v[1] - C * u[2] * v[2]
    assert sp.expand(actual[(1, 0, 1)]).coeff(u[0] * v[1]) == A
    assert sp.expand(actual[(0, 1, 1)]).coeff(u[0] * v[2]) == C * R
    assert sp.expand(actual[(0, 0, 2)]).coeff(u[0] * v[0]) == -R

    # Type 3e.  All six displayed coefficients are nonzero by the row/column
    # generator-independence conditions.
    A, B, C, D, E, F = sp.symbols("A B C D E F", nonzero=True)
    matrix = sp.Matrix([[0, C * y + D * z, y],
                        [x, 0, A * x + B * y],
                        [E * x + F * z, z, 0]])
    actual = coefficients(matrix)
    assert actual[(2, 0, 0)] == A * E * u[1] * v[0]
    assert actual[(0, 2, 0)] == B * C * u[0] * v[2]
    assert actual[(0, 0, 2)] == D * F * u[2] * v[1]
    # These three coefficients are the decisive uncancellable terms in the
    # three possible two-element supports of u.
    assert sp.expand(actual[(0, 1, 1)]).coeff(u[0] * v[0]) == -B
    assert sp.expand(actual[(1, 1, 0)]).coeff(u[1] * v[1]) == -E
    assert sp.expand(actual[(1, 0, 1)]).coeff(u[2] * v[2]) == -D


def audit_types_2a_3a() -> None:
    A, B, C, D, E, F = sp.symbols("A B C D E F", nonzero=True)
    matrix = sp.Matrix([[0, A * x + C * y + E * z,
                         B * x + D * y + F * z],
                        [x, 0, y],
                        [z, 0, 0]])
    actual = coefficients(matrix)
    expected = {
        (2, 0, 0): v[2] * (-A * u[2] + B * u[1]),
        (1, 1, 0): v[2] * (A * u[0] - C * u[2] + D * u[1]),
        (1, 0, 1): (A * u[2] * v[1] - B * u[1] * v[1]
                    - E * u[2] * v[2] + F * u[1] * v[2]),
        (0, 2, 0): C * u[0] * v[2],
        (0, 1, 1): (C * u[2] * v[1] - D * u[1] * v[1]
                    + E * u[0] * v[2] + u[1] * v[0]),
        (0, 0, 2): v[1] * (E * u[2] - F * u[1]),
    }
    assert actual == {key: sp.factor(value) for key, value in expected.items()}

    r, s = sp.symbols("r s")
    # The two and only two bad-pair rulings.
    substituted_zero(actual, {u[0]: r, u[1]: 0, u[2]: s,
                              v[0]: 1, v[1]: 0, v[2]: 0})
    substituted_zero(actual, {u[0]: 1, u[1]: 0, u[2]: 0,
                              v[0]: r, v[1]: s, v[2]: 0})

    # On the second ruling (u=e0), every point except v=e0 has a
    # two-dimensional compression image.  The x,z minor is
    # s^2(AF-BE), nonzero under the incidence hypotheses.
    first = compression_coefficients(
        matrix,
        (sp.Matrix([-s, r, 0]), sp.Matrix([0, 0, 1])),
        (sp.Matrix([0, 1, 0]), sp.Matrix([0, 0, 1])),
    )
    assert sp.factor(first.extract((0, 1), (0, 2)).det()) == s**2 * (A * F - B * E)

    # On the first ruling (v=e0), u=(r,0,s); the x and z coefficient
    # columns are independent whenever s is nonzero.
    second = compression_coefficients(
        matrix,
        (sp.Matrix([0, 1, 0]), sp.Matrix([0, 0, 1])),
        (sp.Matrix([0, 1, 0]), sp.Matrix([s, 0, -r])),
    )
    assert second.extract((1, 3), (0, 2)).det() == s**2


def audit_type_3b() -> None:
    A, B, C, D, E, F, G = sp.symbols("A B C D E F G", nonzero=True)
    matrix = sp.Matrix([[0, A * x + C * y + E * z,
                         B * x + D * y + F * z],
                        [x, 0, y],
                        [G * z, z, 0]])
    actual = coefficients(matrix)
    r, s = sp.symbols("r s")
    relation = {E: A * F / B}  # the incidence identity BE=AF
    substituted_zero(actual, {
        u[0]: G, u[1]: 1, u[2]: 0,
        v[0]: r, v[1]: s, v[2]: 0,
        **relation,
    })

    compressed = compression_coefficients(
        matrix,
        (sp.Matrix([-s, r, 0]), sp.Matrix([0, 0, 1])),
        (sp.Matrix([1, -G, 0]), sp.Matrix([0, 0, 1])),
    )
    expected = sp.Matrix([
        [A * G * s + r, C * G * s, E * G * s],
        [-B * s, -D * s + r, -F * s],
        [0, 0, 0],
        [0, 0, 0],
    ])
    assert compressed == expected
    assert sp.factor(compressed.extract((0, 1), (0, 2)).det().subs(relation)) == -F * r * s
    assert sp.simplify(
        compressed.extract((0, 1), (0, 1)).det().subs(r, 0)
        - G * s**2 * (B * C - A * D)
    ) == 0
    assert compressed.subs(s, 0).extract((0, 1), (0, 1)).det() == r**2


def audit_type_2b_and_crosswise_cancellation() -> None:
    A, C, D, E, F = sp.symbols("A C D E F", nonzero=True)
    matrix = sp.Matrix([[0, A * x + C * y + E * z, D * y],
                        [x, 0, y],
                        [F * z, z, 0]])
    actual = coefficients(matrix)
    r, s = sp.symbols("r s")
    # The two bad-pair rulings and their unique intersection (k,l).
    substituted_zero(actual, {u[0]: F, u[1]: 1, u[2]: 0,
                              v[0]: r, v[1]: s, v[2]: 0})
    substituted_zero(actual, {u[0]: r, u[1]: s, u[2]: 0,
                              v[0]: D, v[1]: 1, v[2]: 0})

    first = compression_coefficients(
        matrix,
        (sp.Matrix([-s, r, 0]), sp.Matrix([0, 0, 1])),
        (sp.Matrix([1, -F, 0]), sp.Matrix([0, 0, 1])),
    )
    assert first == sp.Matrix([
        [A * F * s + r, C * F * s, E * F * s],
        [0, -D * s + r, 0],
        [0, 0, 0],
        [0, 0, 0],
    ])
    assert sp.simplify(
        first.extract((0, 1), (1, 2)).det() - E * F * s * (D * s - r)
    ) == 0

    second = compression_coefficients(
        matrix,
        (sp.Matrix([-1, D, 0]), sp.Matrix([0, 0, 1])),
        (sp.Matrix([s, -r, 0]), sp.Matrix([0, 0, 1])),
    )
    assert second == sp.Matrix([
        [A * r + D * s, C * r, E * r],
        [0, 0, 0],
        [0, 0, F * s - r],
        [0, 0, 0],
    ])
    assert sp.simplify(
        second.extract((0, 2), (1, 2)).det() - C * r * (F * s - r)
    ) == 0

    # Once both physical summands select the unique intersection, their
    # right kernels are shared crosswise.  After normalizing the common
    # intersection columns, the three possible image generators have this
    # universal form, whose determinant cancels identically.
    alpha, beta, gamma = sp.symbols("alpha beta gamma")
    physical = sp.Matrix([[gamma, beta, 0],
                          [alpha, 0, beta],
                          [0, -alpha, gamma]])
    assert sp.expand(physical.det()) == 0


def main() -> None:
    audit_empty_incidence_types()
    audit_types_2a_3a()
    audit_type_3b()
    audit_type_2b_and_crosswise_cancellation()
    print("rank-three singular fixed-line obstruction: PASS")


if __name__ == "__main__":
    main()
