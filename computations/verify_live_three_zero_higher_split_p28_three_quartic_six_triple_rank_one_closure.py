#!/usr/bin/env python3
"""Exact checks for the p=28 4^3 3^6 residual rank-one closure."""

from __future__ import annotations

import sympy as sp


def admissible_tangent_ledgers() -> list[tuple[int, int, int, int]]:
    out: list[tuple[int, int, int, int]] = []
    for m in range(4, 7):
        for e in range(m - 1, 20):
            total_ramification = m * (e - m + 1)
            for d in range(4, 7):
                r1 = 2 * e - 2 - d
                if r1 < 0:
                    continue
                if (m - 1) * r1 <= total_ramification:
                    out.append((m, e, d, r1))
    return out


def check_rational_normal_quartic_frame() -> None:
    t = sp.symbols("t")
    gamma = sp.Matrix([1, t, t**2, t**3, t**4])
    u = sp.Matrix([-t**3, 3 * t**2, -3 * t, 1, 0])
    v = sp.Matrix([0, -t**3, 3 * t**2, -3 * t, 1])

    for vector in (u, v):
        assert sp.expand(gamma.dot(vector)) == 0
        assert sp.expand(gamma.diff(t).dot(vector)) == 0
        assert sp.expand(gamma.diff(t, 2).dot(vector)) == 0
    assert sp.Matrix.hstack(u, v).rank() == 2

    # If A*u+B*v has coordinate degree <=4, the first coordinate bounds
    # deg(A)<=1; the second then bounds deg(B)<=1.  Verify the sharp generic
    # degree-one case and the forced t^3 factor in the first coordinate.
    a0, a1, b0, b1 = sp.symbols("a0 a1 b0 b1")
    section = (a0 + a1 * t) * u + (b0 + b1 * t) * v
    assert max(sp.Poly(x, t).degree() for x in section) <= 4
    assert sp.factor(section[0]) == -t**3 * (a0 + a1 * t)


def check_square_cover_weight() -> None:
    # A nonzero section of order >=6 in a six-series forces its final
    # vanishing order to be >=6.  The unique minimum sequence has weight 1.
    minimum = (0, 1, 2, 3, 4, 6)
    assert sum(order - index for index, order in enumerate(minimum)) == 1
    assert 3 * (6 - 4) + 6 * (6 - 3) == 24
    assert 6 * (10 - 6) == 24


def main() -> None:
    expected = [
        (4, 3, 4, 0),
        (4, 4, 5, 1),
        (4, 4, 6, 0),
        (4, 5, 6, 2),
        (4, 6, 6, 4),
        (5, 4, 6, 0),
    ]
    assert admissible_tangent_ledgers() == expected
    check_rational_normal_quartic_frame()
    check_square_cover_weight()
    print("p=28 4^3 3^6 residual rank-one closure: PASS")
    print("admissible tangent ledgers:", expected)
    print("m=5 rational-normal-quartic frame and z^6 obstruction: PASS")
    print("m=4 osculating-dual square-cover obstruction ledger: PASS")


if __name__ == "__main__":
    main()
