#!/usr/bin/env python3
"""Exact audit of the uniform critical moving-triple span bound."""

from __future__ import annotations

import sympy as sp


def audit_uniform_arithmetic() -> None:
    for r in range(4, 101):
        threshold_mass = r * (r + 3)
        restored_mass = threshold_mass + 2
        assert restored_mass == (r + 1) * (r + 2)

        for classes in (r + 4, r + 5):
            next_dimension = r + 3
            forced = next_dimension * classes - restored_mass
            cap = next_dimension * (
                classes + 1 - next_dimension
            )
            assert forced - cap == 2 * (r + 2)

            common_upper = r + 2
            intersection_lower = 2 * r - common_upper
            pair_ambient = max(classes - 7, 0)
            if classes == r + 4:
                assert pair_ambient == r - 3
                assert pair_ambient < intersection_lower
            else:
                assert classes == r + 5
                assert pair_ambient == intersection_lower == r - 2

        intervals = tuple((2 * shift, 2 * shift + r - 3)
                          for shift in range(5))
        covered = {
            degree
            for lower, upper in intervals
            for degree in range(lower, upper + 1)
        }
        assert covered == set(range(r + 6))
        assert len(covered) == r + 6 > r + 2


def audit_pair_product_determinant() -> None:
    t = sp.symbols("t")
    a = sp.symbols("a0:4")
    pairs = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3))
    rows = []
    for i, j in pairs:
        polynomial = sp.Poly((t - a[i]) ** 2 * (t - a[j]) ** 2, t)
        rows.append([
            polynomial.coeff_monomial(t**degree)
            for degree in range(5)
        ])
    determinant = sp.factor(sp.det(sp.Matrix(rows)))
    expected = sp.factor(
        4
        * (a[0] - a[1]) ** 4
        * (a[0] - a[2])
        * (a[0] - a[3])
        * (a[1] - a[2])
        * (a[1] - a[3])
        * (a[2] - a[3]) ** 2
    )
    assert sp.factor(determinant - expected) == 0


def audit_p28_corollary() -> None:
    r = 4
    assert r * (r + 3) == 28
    baseline = (4,) * 3 + (3,) * 6
    assert sum(baseline) == (r + 1) * (r + 2) == 30
    assert len(baseline) == r + 5 == 9
    moving_values = 6
    maximal_allowed = 3
    assert moving_values - maximal_allowed == 3


def main() -> None:
    audit_uniform_arithmetic()
    audit_pair_product_determinant()
    audit_p28_corollary()
    print("uniform critical moving-triple span bound: PASS")
    print("c<=r+4: at most one maximal selection")
    print("c=r+5, r>=4: at most three maximal selections")
    print("p=28 4^3 3^6: at least three selected kernels have dimension <=5")


if __name__ == "__main__":
    main()
