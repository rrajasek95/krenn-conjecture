#!/usr/bin/env python3
"""Exact checks for the p=28 all-triple q=5 residual-quartic frontier."""

from __future__ import annotations

from itertools import combinations, permutations
from math import comb, factorial

import sympy as sp


def wronskian(polys: list[sp.Expr], z: sp.Symbol) -> sp.Expr:
    return sp.expand(
        sp.det(
            sp.Matrix(
                [[sp.diff(poly, z, order) for poly in polys]
                 for order in range(len(polys))]
            )
        )
    )


def check_kernel_dimensions() -> None:
    assert 3 + 3 + 3 - 2 * 4 == 1
    assert 4 + 4 + 4 - 2 * 5 == 2
    assert 3 * 4 == 12 > 10
    assert 3 + 3 - 5 == 1
    assert 3 + 4 - 5 == 2
    assert 5 + 6 - 1 == 10
    assert 2 * 10 - 1 == 19 < 20


def check_osculating_hyperplane_obstruction() -> None:
    t, b = sp.symbols("t b")
    ell = sp.symbols("l0:6")

    def functional(poly: sp.Expr) -> sp.Expr:
        expanded = sp.Poly(sp.expand(poly), t)
        return sp.expand(
            sum(ell[j] * expanded.coeff_monomial(t**j) for j in range(6))
        )

    assert sp.Poly(functional((t - b) ** 4), b).degree() == 4
    translates = sp.Matrix(
        [
            [sp.expand((t - value) ** 4).coeff(t, j) for j in range(5)]
            for value in range(5)
        ]
    )
    assert translates.det() != 0
    assert sp.Poly(t * (t - b) ** 4, t).coeff_monomial(t**5) == 1


def check_z4_normalization_and_degree() -> None:
    z, t = sp.symbols("z t", nonzero=True)
    transform = sp.Matrix(
        [
            [sp.Rational(1, 2), 0, sp.Rational(1, 2), 0],
            [sp.Rational(1, 2) / z, 0, -sp.Rational(1, 2) / z, 0],
            [0, sp.Rational(1, 2), 0, sp.Rational(1, 2)],
            [0, sp.Rational(1, 4) / z, 0, -sp.Rational(1, 4) / z],
        ]
    )
    assert sp.factor(transform.det()) == -1 / (8 * z**2)
    assert sp.simplify(z**2 * (2 * t).subs(t, z**2) / z**4) == 2

    max_degree = -1
    for degrees in combinations(range(5, 11), 4):
        for assignment in permutations(("E", "O", "Ep", "Op")):
            total = 0
            legal = True
            for degree, kind in zip(degrees, assignment):
                if kind == "E":
                    contribution = degree // 2
                elif kind == "O":
                    contribution = (degree - 1) // 2
                elif kind == "Ep":
                    contribution = degree // 2 - 1
                else:
                    contribution = (degree - 1) // 2 - 1
                legal &= contribution >= 0
                total += contribution
            if legal:
                max_degree = max(max_degree, total)
    assert max_degree == 14
    assert 14 - 10 == 4
    assert 10 + 5 > 14


def check_q6_developable_counts() -> None:
    assert sum((3, 4, 5, 6)) - 2 == 16
    assert (16 - 4) // 2 == 6 < 9

    possibilities = []
    for edge_degree in range(3, 20):
        total_ramification = 4 * (edge_degree - 3)
        for first_ramification in range(total_ramification + 1):
            if 3 * first_ramification > total_ramification:
                continue
            plucker_degree = 2 * edge_degree - 2 - first_ramification
            if plucker_degree <= 5:
                possibilities.append(
                    (edge_degree, plucker_degree, first_ramification)
                )
    assert possibilities == [(3, 4, 0), (4, 5, 1)]


def check_cone_p3_wronskians() -> None:
    z, a = sp.symbols("z a", nonzero=True)
    coeffs = sp.symbols("c0:7")
    phi = sum(coeffs[j] * z**j for j in range(7))
    gauge = (z - a) ** 2
    W = sp.factor(
        wronskian([gauge, gauge * z**2, gauge * z**4, phi], z)
    )
    assert sp.rem(
        sp.Poly(W, z), sp.Poly(z * (z - a) ** 3, z)
    ) == 0

    even_coefficients = [sp.symbols(f"r{index}_0:4") for index in range(3)]
    evens = [
        sum(row[j] * z ** (2 * j) for j in range(4))
        for row in even_coefficients
    ]
    jets = sp.Matrix(
        [
            [sp.diff(poly, z, order).subs(z, 0) for poly in evens + [phi]]
            for order in range(4)
        ]
    )
    assert sp.factor(jets.det()) == 0


def check_tangent_p3_wronskians() -> None:
    z = sp.symbols("z")
    aa = sp.symbols("a0:3")
    bb = sp.symbols("b0:3")
    A = sum(aa[j] * z**j for j in range(3))
    B = sum(bb[j] * z**j for j in range(3))
    t = z**2
    cubic = [A, 2 * A * t + B, A * t**2 + 2 * B * t, B * t**2]
    jets = sp.Matrix(
        [
            [sp.expand(poly).coeff(z, order) * factorial(order)
             for poly in cubic]
            for order in range(4)
        ]
    )
    assert sp.factor(jets.det()) == 0

    cusp = sp.symbols("c")
    q0, q1, q2, q4 = sp.symbols("q0 q1 q2 q4")
    u = z**2 - cusp
    A4 = -4 * q4
    C4 = q0 + q1 * z + q2 * z**2 + q4 * z**4
    quartic = [
        A4,
        A4 * u**2 + 2 * C4,
        A4 * u**3 + 3 * C4 * u,
        A4 * u**4 + 4 * C4 * u**2,
    ]
    assert all(sp.Poly(poly, z).degree() <= 6 for poly in quartic)
    jets4 = sp.Matrix(
        [
            [sp.expand(poly).coeff(z, order) * factorial(order)
             for poly in quartic]
            for order in range(4)
        ]
    )
    assert sp.factor(jets4.det()) == 0

    # Independently solve the full degree-six section problem.  No omitted
    # A or C coefficient survives the high-degree cancellation equations.
    avec = sp.symbols("av0:7")
    cvec = sp.symbols("cv0:7")
    Afull = sum(avec[j] * z**j for j in range(7))
    Cfull = sum(cvec[j] * z**j for j in range(7))
    full = [
        Afull,
        Afull * u**2 + 2 * Cfull,
        Afull * u**3 + 3 * Cfull * u,
        Afull * u**4 + 4 * Cfull * u**2,
    ]
    equations = []
    for poly in full:
        equations.extend(
            coefficient
            for (degree,), coefficient in sp.Poly(sp.expand(poly), z).terms()
            if degree > 6
        )
    matrix, _ = sp.linear_eq_to_matrix(equations, avec + cvec)
    nullspace = matrix.nullspace()
    assert len(nullspace) == 4
    support = [
        {index for index, value in enumerate(vector) if value != 0}
        for vector in nullspace
    ]
    # c0,c1,c2 and the coupled pair a0=-4*c4.
    assert support == [{7}, {8}, {9}, {0, 11}]
    assert sp.simplify(nullspace[-1][0] / nullspace[-1][11]) == -4


def check_developable_p5_counts_and_models() -> None:
    for edge_degree in (4, 5):
        vertex_zeros = 10 - 2 * edge_degree
        nonvertex = 10 - vertex_zeros
        minor_degree = 4 * edge_degree - 12
        assert nonvertex == 2 * edge_degree > minor_degree

    possibilities = []
    for edge_degree in range(5, 30):
        total_ramification = 6 * (edge_degree - 5)
        for first_ramification in range(total_ramification + 1):
            if 5 * first_ramification > total_ramification:
                continue
            plucker_degree = 2 * edge_degree - 2 - first_ramification
            if plucker_degree <= 9:
                possibilities.append(
                    (edge_degree, plucker_degree, first_ramification)
                )
    assert possibilities == [(5, 8, 0), (6, 9, 1)]

    z = sp.symbols("z")
    aa = sp.symbols("a0:3")
    bb = sp.symbols("b0:3")
    A = sum(aa[j] * z**j for j in range(3))
    B = sum(bb[j] * z**j for j in range(3))
    t = z**2
    quintic = []
    for index in range(6):
        value = 0
        if index <= 4:
            value += comb(4, index) * A * t**index
        if index >= 1:
            value += comb(4, index - 1) * B * t ** (index - 1)
        quintic.append(sp.expand(value))
    jets = sp.Matrix(
        [
            [poly.coeff(z, order) * factorial(order) for poly in quintic]
            for order in range(6)
        ]
    )
    assert sp.factor(jets.det()) == 0

    cusp, q0, q1, q2, q4 = sp.symbols("c q0 q1 q2 q4")
    u = z**2 - cusp
    A6 = -6 * q4
    C6 = q0 + q1 * z + q2 * z**2 + q4 * z**4
    sextic = [A6] + [
        sp.expand(A6 * u**power + power * C6 * u ** (power - 2))
        for power in range(2, 7)
    ]
    assert all(sp.Poly(poly, z).degree() <= 10 for poly in sextic)
    W6 = sp.factor(wronskian(sextic, z))
    assert W6 == 0 or sp.rem(sp.Poly(W6, z), sp.Poly(z**6, z)) == 0
    coefficient_rank = sp.Matrix(
        [[poly.coeff(z, degree) for poly in sextic] for degree in range(11)]
    ).rank()
    assert coefficient_rank == 6

    # Exhaust the full degree-ten section problem for the cuspidal sextic.
    avec = sp.symbols("au0:11")
    cvec = sp.symbols("cu0:11")
    Afull = sum(avec[j] * z**j for j in range(11))
    Cfull = sum(cvec[j] * z**j for j in range(11))
    full = [Afull] + [
        sp.expand(Afull * u**power + power * Cfull * u ** (power - 2))
        for power in range(2, 7)
    ]
    equations = []
    for poly in full:
        equations.extend(
            coefficient
            for (degree,), coefficient in sp.Poly(sp.expand(poly), z).terms()
            if degree > 10
        )
    matrix, _ = sp.linear_eq_to_matrix(equations, avec + cvec)
    nullspace = matrix.nullspace()
    assert len(nullspace) == 4
    support = [
        {index for index, value in enumerate(vector) if value != 0}
        for vector in nullspace
    ]
    # c0,c1,c2 and the coupled pair a0=-6*c4 are the only possibilities.
    assert support == [{11}, {12}, {13}, {0, 15}]
    assert sp.simplify(nullspace[-1][0] / nullspace[-1][15]) == -6

    # Put the cusp at infinity.  The hyperplane series omits t^5, and
    # its saturated tangent frame is the derivative frame below.  Every
    # degree-ten point section has Wronskian degree at most 24, whereas
    # the exact six-space requires degree 30.
    gamma_inf = [t**6, t**4, t**3, t**2, t, sp.Integer(1)]
    delta_inf = [6 * t**5, 4 * t**3, 3 * t**2, 2 * t, sp.Integer(1), sp.Integer(0)]
    Ainf = -6 * (q2 + q1 * z + q4 * z**2)
    Cinf = q0 + q2 * z**2 + q1 * z**3 + q4 * z**4
    infinity_section = [
        sp.expand(Ainf * left + Cinf * right)
        for left, right in zip(gamma_inf, delta_inf)
    ]
    assert all(sp.Poly(poly, z).degree() <= 10 for poly in infinity_section)
    Winf = sp.expand(wronskian(infinity_section, z))
    assert Winf == 0 or sp.Poly(Winf, z).degree() <= 24 < 30


def check_local_simple_root_and_quartic() -> None:
    x = sp.symbols("x")
    basis = [sp.eye(6).col(j) for j in range(6)]
    positive = basis[0] + x * basis[2] + x**2 * basis[3] / 2
    negative = basis[1] + x * basis[2] + x**2 * basis[4] / 2
    four = sp.Matrix.hstack(
        positive, negative, sp.diff(positive, x), sp.diff(negative, x)
    )
    minor = sp.factor(four[[0, 1, 2, 4], :].det())
    assert minor.subs(x, 0) == 0
    assert sp.diff(minor, x).subs(x, 0) != 0
    assert sp.diff(positive, x, 3) == sp.zeros(6, 1)
    assert sp.Matrix.hstack(
        positive.subs(x, 0),
        sp.diff(positive, x).subs(x, 0),
        sp.diff(positive, x, 2).subs(x, 0),
    ).rank() == 3

    t = sp.symbols("t")
    quartic_columns = [
        basis[0], basis[1], basis[2] + t * basis[4],
        basis[3] + t**3 * basis[5]
    ]
    matrix = sp.Matrix.hstack(*quartic_columns)
    plucker = [
        sp.expand(matrix[list(rows), :].det())
        for rows in combinations(range(6), 4)
    ]
    assert max(sp.Poly(poly, t).degree() for poly in plucker if poly != 0) == 4
    assert any(sp.diff(poly, t) != 0 for poly in plucker)
    assert matrix.rank() == 4


def main() -> None:
    check_kernel_dimensions()
    check_osculating_hyperplane_obstruction()
    check_z4_normalization_and_degree()
    check_q6_developable_counts()
    check_cone_p3_wronskians()
    check_tangent_p3_wronskians()
    check_developable_p5_counts_and_models()
    check_local_simple_root_and_quartic()
    print("p=28 all-triple q=5 residual-quartic frontier: PASS")
    print("common kernel dimension five excluded; common kernel dimension six")
    print("every selected q=6 relation space excluded")
    print("survivor: nonzero decomposable Lambda^4-valued polynomial of degree <=4")


if __name__ == "__main__":
    main()
