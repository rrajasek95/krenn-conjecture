#!/usr/bin/env python3
"""Exact audit for the transverse two-marked extra-plane response."""

from __future__ import annotations

from math import factorial

import sympy as sp

from verify_live_three_zero_extra_plane_minority_exceptional import (
    e0,
    e1,
    e2,
    p,
    p0,
    p1,
    p2,
    response_coefficients,
    zero,
)


def audit_case(r, exceptional_count, symbolic=True):
    t = exceptional_count
    assert 2 <= t <= min(2 * r, r + 2)
    active_count = 2 * r + 2 - t
    if symbolic:
        nus = list(sp.symbols(f"nu0:{t}"))
    else:
        nus = [sp.Integer(2 * index + 3) for index in range(t)]
    unmarked_factor = sp.prod(1 / (1 + value) for value in nus[2:])
    common_factor = (
        2
        * factorial(r)
        * unmarked_factor
        * sp.Rational(1, 2) ** (r - t + 2)
    )
    transverse_p = p.subs(p2, 0)

    # The first two exceptional sites are the forced source-22 marked pair.
    marked_rows = [e2, e2]
    marked_betas = nus[:2]
    unmarked_betas = nus[2:]

    # Active row zero: all unmarked exceptional sites are zero.
    subset_size = r + 3 - t
    rows = (
        [e0] * subset_size
        + [e1] * (active_count - subset_size)
        + marked_rows
        + [e0] * (t - 2)
        + [transverse_p]
    )
    betas = [1] * active_count + marked_betas + unmarked_betas + [1]
    coefficients = response_coefficients(rows, betas, 2)
    expected = common_factor * p1
    assert all(
        sp.cancel(coefficients[index] - expected) == 0
        for index in range(subset_size)
    )
    assert all(
        coefficients[index] == 0
        for index in range(subset_size, active_count)
    )
    assert coefficients[-1] == 0

    # Active row one is the colour-swapped family.
    rows = (
        [e1] * subset_size
        + [e0] * (active_count - subset_size)
        + marked_rows
        + [e1] * (t - 2)
        + [transverse_p]
    )
    coefficients = response_coefficients(rows, betas, 2)
    expected = common_factor * p0
    assert all(
        sp.cancel(coefficients[index] - expected) == 0
        for index in range(subset_size)
    )
    assert all(
        coefficients[index] == 0
        for index in range(subset_size, active_count)
    )
    assert coefficients[-1] == 0

    # Balanced binary cofactor kills the entire extra star.
    active_zeros = r + 2 - t
    rows = (
        [e0] * active_zeros
        + [e1] * (active_count - active_zeros)
        + marked_rows
        + [e0] * (t - 2)
        + [p]
    )
    coefficients = response_coefficients(rows, betas, 2)
    assert sp.cancel(coefficients[-1] - common_factor) == 0

    # A type-10 zero third row is a singleton.
    other_active = active_count - 1
    rows = (
        [zero]
        + [e0] * active_zeros
        + [e1] * (other_active - active_zeros)
        + marked_rows
        + [e0] * (t - 2)
        + [transverse_p]
    )
    coefficients = response_coefficients(rows, betas, 2)
    assert sp.cancel(coefficients[0] - common_factor * p1) == 0
    assert all(entry == 0 for entry in coefficients[1:])

    # The same word with a common live third row is a singleton after the
    # binary and extra blocks have vanished.
    if 2 * r - t > 0:
        rows = (
            [e2]
            + [e0] * active_zeros
            + [e1] * (other_active - active_zeros)
            + marked_rows
            + [e0] * (t - 2)
            + [transverse_p]
        )
        coefficients = response_coefficients(rows, betas, 2)
        assert sp.cancel(coefficients[0] - common_factor * p1) == 0


def main():
    audit_case(2, 2)
    audit_case(3, 3)
    audit_case(2, 4, symbolic=False)
    audit_case(3, 5, symbolic=False)
    print("Live three-zero extra-plane two-marked transverse: PASS")
    print("symbolic audits at (r,t)=(2,2),(3,3)")
    print("endpoint audits at (2,4),(3,5)")


if __name__ == "__main__":
    main()
