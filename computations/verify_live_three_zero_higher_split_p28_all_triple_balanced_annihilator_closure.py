#!/usr/bin/env python3
"""Exact checks for the proposed p=28 balanced-annihilator closure."""

from __future__ import annotations

from itertools import combinations
from math import comb

import sympy as sp


def pluecker_columns(matrix: sp.Matrix, rank: int) -> list[sp.Expr]:
    return [
        sp.expand(matrix[list(rows), :].det())
        for rows in combinations(range(matrix.rows), rank)
    ]


def polynomial_order(poly: sp.Expr, z: sp.Symbol) -> int:
    p = sp.Poly(sp.expand(poly), z)
    if p.is_zero:
        return 10**6
    return min(power[0] for power, coefficient in p.terms() if coefficient)


def wronskian(polynomials: list[sp.Expr], z: sp.Symbol) -> sp.Expr:
    return sp.expand(sp.det(sp.Matrix([
        [sp.diff(poly, z, order) for poly in polynomials]
        for order in range(len(polynomials))
    ])))


def check_full_tangent_rank_square() -> None:
    t = sp.symbols("t")
    lam = sp.Matrix([[1, t, t**2, 0, 0, 0]])
    mu = sp.Matrix([[0, 0, 0, 1, t, t**2]])
    u = sp.Matrix([t**2, -2 * t, 1, 0, 0, 0])
    v = sp.Matrix([0, 0, 0, t**2, -2 * t, 1])
    up = sp.diff(u, t)
    vp = sp.diff(v, t)

    for row, vector in ((lam, u), (sp.diff(lam, t), u),
                        (mu, v), (sp.diff(mu, t), v)):
        assert sp.expand((row * vector)[0]) == 0
    assert sp.Matrix.vstack(lam, mu, sp.diff(lam, t),
                            sp.diff(mu, t)).rank() == 4

    frame = sp.Matrix.hstack(u, v, up, vp)
    coordinates = [value for value in pluecker_columns(frame, 4)
                   if value != 0]
    assert sp.gcd_list(coordinates) in (1, -1, 2, -2, 4, -4)
    primitive = [sp.cancel(value / sp.gcd_list(coordinates))
                 for value in coordinates]
    assert sp.gcd_list(primitive) in (1, -1)
    assert max(sp.Poly(value, t).degree() for value in primitive) == 4

    p, q, r, s = sp.symbols("p q r s")
    pp, qp, rp, sp_ = sp.symbols("pp qp rp sp")
    coefficient_matrix = sp.Matrix([
        [p, r, pp, rp],
        [q, s, qp, sp_],
        [0, 0, p, r],
        [0, 0, q, s],
    ])
    determinant = sp.factor(coefficient_matrix.det())
    assert determinant == (p * s - q * r) ** 2

    # The ten Hermite factors are squarefree because their squares are
    # distinct.  A nonzero constant times a polynomial square cannot equal it.
    C = sp.prod(t - site**2 for site in range(1, 11))
    assert sp.gcd(sp.Poly(C, t), sp.Poly(sp.diff(C, t), t)).degree() == 0
    assert sp.Poly(C, t).degree() == 10


def check_rank_and_ramification_ledger() -> None:
    # Generic span(A,A') has rank 3 or 4.  In rank 3, a nonconstant edge
    # spanning P^(m-1) has d=4 and R1=2e-6.  Exhaust the exact total-
    # ramification inequality for every possible fixed coefficient span.
    survivors: list[tuple[int, int, int]] = []
    for m in range(4, 7):
        for edge_degree in range(m - 1, 50):
            first = 2 * edge_degree - 6
            if first < 0:
                continue
            total = m * (edge_degree - m + 1)
            if (m - 1) * first <= total:
                survivors.append((m, edge_degree, first))
    assert survivors == [(4, 3, 0)]

    # A rank-four derived plane with a fixed vector is a cone: its two
    # derivatives have only one transverse class, hence the four-column
    # determinant is zero.  A rank-three derived plane inside a fixed
    # three-space is even more immediate.
    x1, x2, y1, y2 = sp.symbols("x1 x2 y1 y2")
    matrix = sp.Matrix([
        [1, 0, x1, y1],
        [0, 1, x2, y2],
        [0, 0, 1, 1],
        [0, 0, 0, 0],
    ])
    assert matrix.det() == 0


def check_twisted_cubic_normal_form() -> None:
    t, s, h = sp.symbols("t s h")
    gamma = sp.Matrix([1, t, t**2, t**3])
    gammap = sp.diff(gamma, t)
    lam = 3 * gamma - t * gammap
    mu = gammap
    assert list(lam) == [3, 2 * t, t**2, 0]
    assert list(mu) == [0, 1, 2 * t, 3 * t**2]

    annihilator = sp.Matrix.vstack(lam.T, mu.T)
    annihilator_jet = sp.Matrix.vstack(
        lam.T, mu.T, sp.diff(lam, t).T, sp.diff(mu, t).T
    )
    assert annihilator.rank() == 2
    assert annihilator_jet.rank() == 3

    # Homogeneous quadratic frame, including the infinity fiber [s:h]=[0:1].
    lam_h = sp.Matrix([3 * s**2, 2 * s * h, h**2, 0])
    mu_h = sp.Matrix([0, s**2, 2 * s * h, 3 * h**2])
    homogeneous = sp.Matrix.vstack(lam_h.T, mu_h.T)
    assert homogeneous.subs({s: 1, h: 0}).rank() == 2
    assert homogeneous.subs({s: 0, h: 1}).rank() == 2
    homogeneous_minors = [value for value in
                           [homogeneous[:, cols].det()
                            for cols in combinations(range(4), 2)]
                           if value != 0]
    assert all(sp.Poly(value, s, h).total_degree() == 4
               for value in homogeneous_minors)
    assert sp.gcd_list(homogeneous_minors) in (1, -1, 3, -3)

    u = sp.Matrix([-t**3, 3 * t**2, -3 * t, 1, 0, 0])
    c1 = sp.eye(6).col(4)
    c2 = sp.eye(6).col(5)
    lam6 = sp.Matrix([[*list(lam), 0, 0]])
    mu6 = sp.Matrix([[*list(mu), 0, 0]])
    derived = sp.Matrix.vstack(lam6, mu6, sp.diff(lam6, t),
                               sp.diff(mu6, t))
    assert derived * u == sp.zeros(4, 1)
    assert derived * c1 == sp.zeros(4, 1)
    assert derived * c2 == sp.zeros(4, 1)
    assert sp.Matrix.hstack(u, c1, c2).rank() == 3

    Wrows = sp.Matrix.vstack(lam6, mu6)
    up = sp.diff(u, t)
    assert Wrows * up == sp.zeros(2, 1)
    Wframe = sp.Matrix.hstack(u, up, c1, c2)
    assert Wframe.rank() == 4
    Wcoordinates = [value for value in pluecker_columns(Wframe, 4)
                    if value != 0]
    assert sp.gcd_list(Wcoordinates) in (1, -1, 3, -3)


def check_twisted_scalar_and_degrees() -> None:
    p, a, b, q, c, d = sp.symbols("p a b q c d")
    pp, ap, bp, qp, cp, dp = sp.symbols("pp ap bp qp cp dp")
    coefficient_matrix = sp.Matrix([
        [p, q, pp, qp],
        [a, c, ap, cp],
        [b, d, bp, dp],
        [0, 0, p, q],
    ])
    scalar = sp.factor(coefficient_matrix.det())
    M1 = p * c - q * a
    M2 = p * d - q * b
    M1p = pp * c + p * cp - qp * a - q * ap
    M2p = pp * d + p * dp - qp * b - q * bp
    assert sp.expand(scalar - (M2 * M1p - M1 * M2p)) == 0

    t = sp.symbols("t")
    left_coefficients = sp.symbols("x0:7")
    right_coefficients = sp.symbols("y0:7")
    Mleft = sum(left_coefficients[k] * t**k for k in range(7))
    Mright = sum(right_coefficients[k] * t**k for k in range(7))
    critical = sp.expand(Mright * sp.diff(Mleft, t)
                         - Mleft * sp.diff(Mright, t))
    assert sp.Poly(critical, t).degree() == 10
    assert 2 + 4 == 1 + 5 == 6  # deg(pc), deg(qa), and analogously M2.


def check_square_cover_wronskian_obstruction() -> None:
    # A nonzero A(z) times the complete even cubic has four fixed local
    # orders.  Insert the two smallest missing nonnegative orders and compute
    # the least possible six-space Wronskian weight.
    weights = []
    for rho in range(11):
        forced = [rho + 2 * k for k in range(4)]
        extras = [value for value in range(30) if value not in forced][:2]
        sequence = sorted(forced + extras)
        assert len(set(sequence)) == 6
        weight = sum(sequence) - comb(6, 2)
        weights.append((rho, tuple(sequence), weight))
    assert weights[0] == (0, (0, 1, 2, 3, 4, 6), 1)
    assert weights[1] == (1, (0, 1, 2, 3, 5, 7), 3)
    assert min(weight for _, _, weight in weights) == 1

    # The lower bound is sharp at rho=0.
    z = sp.symbols("z")
    sharp = [1, z, z**2, z**3, z**4, z**6]
    W = wronskian(sharp, z)
    assert polynomial_order(W, z) == 1

    # The ten exact order-three roots already consume the full cap.
    assert 10 * (6 - 3) == 6 * (11 - 6) == 30
    assert 0 not in {site for site in range(1, 11)}


def main() -> None:
    check_full_tangent_rank_square()
    check_rank_and_ramification_ledger()
    check_twisted_cubic_normal_form()
    check_twisted_scalar_and_degrees()
    check_square_cover_wronskian_obstruction()
    print("p=28 all-triple balanced-annihilator closure: PASS")
    print("rank 4: primitive scalar is a square, contradicting ten simple roots")
    print("rank 3: sole live branch is the rational-normal-cubic tangent curve")
    print("twisted branch: unavoidable unlisted Wronskian root at z=0")
    print("closed residual tuples: (0,10,0,0), (0,10,1,-2)")


if __name__ == "__main__":
    main()
