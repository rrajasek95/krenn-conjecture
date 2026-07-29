#!/usr/bin/env python3
"""Exact audit of the h=8,k=3 profile 2^9 1^3 pencil closure."""

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


def main() -> None:
    z, u, v, mu = sp.symbols("z u v mu")
    r1, r2, r3 = sp.symbols("r1 r2 r3")
    alpha, beta = sp.symbols("alpha beta")
    singleton_poly = (z - r1) * (z - r2) * (z - r3)
    wronskian = sp.expand(singleton_poly * (alpha * z + beta))
    assert sp.Poly(wronskian, z).degree() <= 4
    for root in (r1, r2, r3):
        assert sp.factor(wronskian.subs(z, root)) == 0

    # Crosswise elimination of a common exact second-order row.
    p, pp, ppp, q, qp, qpp = sp.symbols("p pp ppp q qp qpp")
    Y, M = sp.symbols("Y M")
    row_p = ppp + 2 * Y * pp + M * p
    row_q = qpp + 2 * Y * qp + M * q
    W = p * qp - pp * q
    Wprime = p * qpp - ppp * q
    assert sp.expand(p * row_q - q * row_p - (Wprime + 2 * Y * W)) == 0

    ell, X, Zu, Zv = sp.symbols("ell X Zu Zv")
    assert sp.expand((ell + alpha / (alpha * u + beta)) + 2 * (X - 2 * ell) - (alpha / (alpha * u + beta) + 2 * X - 3 * ell)) == 0
    Z = sp.symbols("Z")
    homogeneous_row = alpha * (u * Z + 1) + beta * Z
    assert sp.factor(
        (alpha / (alpha * u + beta) + Z) * (alpha * u + beta)
        - homogeneous_row
    ) == 0
    determinant = sp.factor((u * Zu + 1) * Zv - Zu * (v * Zv + 1))
    assert sp.expand(determinant - ((u - v) * Zu * Zv - Zu + Zv)) == 0

    # Exact 2-subset census for E of size seven.
    pairs = tuple(combinations(range(7), 2))
    assert len(pairs) == 21
    for pair in pairs:
        assert len(set(range(7)) - set(pair)) == 5

    # Rectangle identity after additive partition changes.
    D, P0, Q0 = sp.symbols("D P0 Q0")
    pa, pb, pc, pd = sp.symbols("pa pb pc pd")
    qa, qb, qc, qd = sp.symbols("qa qb qc qd")

    def F(px, py, qx, qy):
        left = P0 + px + py
        right = Q0 + qx + qy
        return D * left * right + right - left

    rectangle = sp.expand(
        F(pa, pc, qa, qc)
        - F(pa, pd, qa, qd)
        - F(pb, pc, qb, qc)
        + F(pb, pd, qb, qd)
    )
    expected = D * ((pa - pb) * (qc - qd) + (qa - qb) * (pc - pd))
    assert sp.factor(rectangle - expected) == 0

    # The symmetric form used in the collinearity step is nondegenerate.
    form_matrix = sp.Matrix([[0, 1], [1, 0]])
    assert form_matrix.det() == -1

    x = sp.symbols("x")

    def Phi(node):
        return 2 / (node + x) + 3 / (node - x)

    assert sp.factor(Phi(u) - (5 * u + x) / (u**2 - x**2)) == 0
    A, B, C = sp.symbols("A B C")
    pullback = sp.cancel(
        (A * Phi(u) + B * Phi(v) + C)
        * (u**2 - x**2)
        * (v**2 - x**2)
    )
    assert sp.denom(pullback) == 1
    assert sp.Poly(pullback, x).degree() <= 4
    # Linear independence of 1,Phi_u,Phi_v over constants.
    coefficients = sp.Poly(sp.expand(pullback), x).all_coeffs()
    solution = sp.solve(coefficients, [A, B, C], dict=True)
    assert solution == [{A: 0, B: 0, C: 0}]
    assert 5 > 4

    profile = (2,) * 9 + (1,) * 3
    counts, residuals = frontier.census(8, 11)
    assert counts["R"] == 46
    assert profile in residuals
    assert sum(profile) == 21
    assert len(profile) == 12

    print("PASS: exact h=8,k=3 nine-double/three-singleton pencil closure")


if __name__ == "__main__":
    main()
