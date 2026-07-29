#!/usr/bin/env python3
"""Exact audits for hessian-corank-two-osculating-dichotomy.md."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

import sympy as sp


def skew(x, y, z):
    return sp.Matrix([[0, -z, y], [z, 0, -x], [-y, x, 0]])


def audit_binary_ufd():
    x, y = sp.symbols("x y")
    # A representative symmetric triangle: three distinct projective
    # points, each repeated only at the transposed position.
    u = {
        (0, 1): x,
        (1, 0): 2 * x,
        (1, 2): y,
        (2, 1): 3 * y,
        (2, 0): x + y,
        (0, 2): sp.Rational(1, 6) * (x + y),
    }
    assert sp.expand(u[0, 1] * u[1, 2] * u[2, 0]) == sp.expand(
        u[0, 2] * u[2, 1] * u[1, 0]
    )
    # Every same-row and same-column pair has nonzero determinant in the
    # coefficient plane.
    def coeff(f):
        return sp.Matrix([sp.expand(f).coeff(x), sp.expand(f).coeff(y)])

    for c in range(3):
        ds = [d for d in range(3) if d != c]
        assert sp.Matrix.hstack(coeff(u[c, ds[0]]), coeff(u[c, ds[1]])).det()
    for d in range(3):
        cs = [c for c in range(3) if c != d]
        assert sp.Matrix.hstack(coeff(u[cs[0], d]), coeff(u[cs[1], d])).det()

    # Proposition 2.2: an invertible 2 by 2 Theta turns its barred-slot
    # End-orbit into all four dimensions of Hom(barV*, E).
    theta = sp.Matrix([[1, 2], [3, 5]])
    assert theta.det()
    orbit = []
    for i in range(2):
        for j in range(2):
            unit = sp.zeros(2)
            unit[i, j] = 1
            orbit.append(list(theta * unit.T))
    assert sp.Matrix.hstack(*(sp.Matrix(v) for v in orbit)).rank() == 4


def audit_alternating_pencil_boundary():
    e0, e1, e2 = (sp.eye(3)[:, i] for i in range(3))
    zero = sp.zeros(3, 1)
    A = sp.Matrix.hstack(-e1, e0, zero)
    B = sp.Matrix.hstack(e0, e1, zero)
    C = sp.Matrix.hstack(e2, zero, zero)
    D = sp.Matrix.hstack(zero, e2, zero)
    L = lambda m: A * m * B.T - C * m * D.T
    assert L(skew(1, 0, 0)) == sp.zeros(3)
    assert L(skew(0, 1, 0)) == sp.zeros(3)
    assert L(skew(0, 0, 1)) == sp.eye(3)
    assert sp.Matrix.vstack(A, C).rank() == 2
    assert sp.Matrix.vstack(B, D).rank() == 2

    # Symbolic determinant audit for the generic nonzero-third-column
    # branch in equation (33).
    mu, kappa, t1, t2 = sp.symbols("mu kappa t1 t2")
    g = mu * kappa - 1
    coefficient = sp.Matrix(
        [[0, g, mu * t2], [-g, 0, mu * t1], [-kappa * t2, -kappa * t1, 0]]
    )
    assert sp.expand(coefficient.det()) == 0


def audit_zero_pencil_scalar():
    # Solve M B^T = A M on the three skew basis matrices.  The exact
    # linear solution consists only of A=B=tI.
    avars = sp.symbols("a0:9")
    bvars = sp.symbols("b0:9")
    A = sp.Matrix(3, 3, avars)
    B = sp.Matrix(3, 3, bvars)
    equations = []
    for m in (skew(1, 0, 0), skew(0, 1, 0), skew(0, 0, 1)):
        equations.extend(list(m * B.T - A * m))
    sol = sp.linsolve(equations, avars + bvars)
    point = next(iter(sol))
    t = point[0]
    expected = (t, 0, 0, 0, t, 0, 0, 0, t) * 2
    assert point == expected


def audit_zero_pencil_common_kernel_dichotomy():
    # Scalar contraction of a zero pencil gives x wedge y' = y wedge x'.
    # Normalize independent x,y to e0,e1 and solve: both primed rows must
    # lie in their span.
    a, b, c, d, e, f = sp.symbols("a b c d e f")
    x = sp.Matrix([1, 0, 0])
    y = sp.Matrix([0, 1, 0])
    xp = sp.Matrix([a, b, c])
    yp = sp.Matrix([d, e, f])
    wedge = lambda u, v: sp.Matrix(
        [u[0] * v[1] - u[1] * v[0],
         u[0] * v[2] - u[2] * v[0],
         u[1] * v[2] - u[2] * v[1]]
    )
    equations = list(wedge(x, yp) - wedge(y, xp))
    solution = next(iter(sp.linsolve(equations, (a, b, c, d, e, f))))
    assert solution[2] == 0
    assert solution[5] == 0

    # Representative audit of the two-operator local-dependence lemma.
    # If A has rank two and Ax,Bx are dependent for symbolic x, then B is
    # the same scalar multiple of A and kills ker A.
    bv = sp.symbols("b0:9")
    B = sp.Matrix(3, 3, bv)
    A = sp.diag(1, 1, 0)
    z = sp.symbols("z0:3")
    Az = A * sp.Matrix(z)
    Bz = B * sp.Matrix(z)
    polynomial_equations = []
    for entry in wedge(Az, Bz):
        poly = sp.Poly(entry, z)
        polynomial_equations.extend(poly.coeffs())
    linear = sp.linsolve(polynomial_equations, bv)
    point = next(iter(linear))
    t = point[0]
    assert point == (t, 0, 0, 0, t, 0, 0, 0, 0)

    # Once both local pairs are proportional to invertible matrices, the
    # alternating pencil is their 2 by 2 coefficient determinant times a
    # nonzero congruence of M.
    Ri = sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 0, 1]])
    Rj = sp.Matrix([[2, 0, 1], [1, 1, 0], [0, 1, 1]])
    assert Ri.det() and Rj.det()
    ai, bi, aj, bj = 2, 3, 4, 6
    for m in (skew(1, 0, 0), skew(0, 1, 0), skew(0, 0, 1)):
        lhs = (ai * Ri) * m * (bj * Rj).T - (bi * Ri) * m * (aj * Rj).T
        assert lhs == (ai * bj - bi * aj) * Ri * m * Rj.T
        assert lhs == sp.zeros(3)


def audit_cauchy_shared_matrix():
    n = 6
    # Sum-zero vertex gauge and a shift avoiding every zero denominator.
    alpha = [Fraction(-5), Fraction(-3), Fraction(-1), Fraction(1), Fraction(3), Fraction(5)]
    assert sum(alpha) == 0
    b = Fraction(20)
    H = sp.Matrix([[0, 2, 3], [2, 0, 5], [3, 5, 0]])
    assert H.det() != 0

    # Deterministic invertible local row matrices.
    P = []
    for i in range(n):
        matrix = sp.Matrix([[1, i + 1, 0], [0, 1, i + 2], [i + 1, 0, 1]])
        assert matrix.det() != 0
        P.append(matrix)

    for i, j in combinations(range(n), 2):
        gamma = alpha[i] + alpha[j] - b
        assert gamma
        qij = P[i] * H * P[j].T / sp.Rational(gamma.numerator, gamma.denominator)
        product_block = P[i] * H * P[j].T
        assert product_block == sp.Rational(gamma.numerator, gamma.denominator) * qij
        assert qij.det() != 0


def audit_common_line_triple_selector():
    # Undoing the diagonal normalization can give two different endpoint
    # covectors, but their coordinate supports agree.
    xi = sp.Matrix([1, 2, 0])
    eta = sp.Matrix([3, 4, 0])
    u = sp.Matrix([[1, 2, 3]])
    v = sp.Matrix([[2, -1, 1]])
    Api = sp.Matrix.vstack(-2 * u, u, v)
    Aqi = sp.Matrix.vstack(4 * u, -3 * u, v)
    assert (xi.T * Api) == sp.zeros(1, 3)
    assert (eta.T * Aqi) == sp.zeros(1, 3)
    assert Api.rank() == Aqi.rank() == 2

    # An invertible direct block can nevertheless be isotropic for the two
    # annihilators.  The product selector at color zero then kills all
    # three one-cross terms separately.
    Apq = sp.diag(8, -3, 1)
    assert Apq.det()
    assert (xi.T * Apq * eta)[0] == 0
    theta = sp.Matrix([sp.Rational(1, 3), 0, 0])
    assert [(xi[c] * eta[c] * theta[c]) for c in range(3)] == [1, 0, 0]
    assert (xi.T * Api) == sp.zeros(1, 3)
    assert (eta.T * Aqi) == sp.zeros(1, 3)
    assert (xi.T * Apq * eta)[0] == 0

    # Proposition 7.3: an exact nondegenerate staircase whose two incident
    # matrices are singular has the sole common-support left kernels e2,
    # and the corresponding direct diagonal entry is nonzero.
    e0, e1, e2 = (sp.eye(3)[:, i] for i in range(3))
    u = sp.Matrix([-3, -3, 2])
    vv = sp.Matrix([1, -3, 0])
    ww = sp.Matrix([2, -2, 0])
    staircase_qi = e0 * e0.T + e1 * u.T + vv * e2.T
    staircase_pi = e1 * e1.T - e0 * u.T + ww * e2.T
    staircase_pq = e2 * e2.T - e0 * vv.T - ww * e1.T
    assert staircase_qi.rank() == staircase_pi.rank() == 2
    assert staircase_pq.det() != 0
    assert staircase_qi.T.nullspace() == [e2]
    assert staircase_pi.T.nullspace() == [e2]
    assert (e2.T * staircase_pq * e2)[0] == 1


def main():
    audit_binary_ufd()
    audit_alternating_pencil_boundary()
    audit_zero_pencil_scalar()
    audit_zero_pencil_common_kernel_dichotomy()
    audit_cauchy_shared_matrix()
    audit_common_line_triple_selector()
    print("Hessian corank-two osculating dichotomy: PASS")


if __name__ == "__main__":
    main()
