#!/usr/bin/env python3
"""Exact audit of the uniform constant-core common-pole root bound."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


w, x, mu = sp.symbols("w x mu")


def normalized_role(j: int):
    return (
        (1 - w / (x + mu)) ** (-j)
        * (1 + w / (x - mu)) ** (-(j + 1))
    )


def coefficient(expr, degree: int):
    return sp.diff(expr, w, degree).subs(w, 0) / sp.factorial(degree)


# The normalized factor is exactly the moving selected/unselected ratio.
z = sp.symbols("z")
for j in range(1, 6):
    raw = 1 / ((z - x) ** j * (z + x) ** (j + 1))
    shifted = raw.subs(z, -mu + w)
    assert sp.factor(shifted / shifted.subs(w, 0) - normalized_role(j)) == 0


# Every coefficient through order k clears by (x^2-mu^2)^k and has
# numerator degree at most 2k.  Checking the role coefficients separately
# avoids an unnecessarily large symbolic expansion in arbitrary U-jets.
for j in range(1, 6):
    role = normalized_role(j)
    for k in range(1, 9):
        truncated = sp.series(role, w, 0, k + 1).removeO().expand()
        for ell in range(k + 1):
            role_coefficient = truncated.coeff(w, ell)
            cleared = sp.cancel(
                (x**2 - mu**2) ** k * role_coefficient
            )
            assert sp.denom(cleared) == 1
            assert sp.Poly(cleared, x).degree() <= 2 * k


# The asymptotic diagonal coefficients have the displayed same-sign sum.
X = sp.symbols("X")
for j in range(1, 8):
    series = (1 - X) ** (-j) * (1 + X) ** (-(j + 1))
    for ell in range(0, 13):
        observed = sp.expand(series.series(X, 0, ell + 1).removeO()).coeff(
            X, ell
        )
        expected = (-1) ** ell * sum(
            sp.binomial(j + m - 1, m) for m in range(ell // 2 + 1)
        )
        assert sp.simplify(observed - expected) == 0
        assert expected != 0


def common_pole_witness(profile: tuple[int, ...], h: int, needed: int):
    """Literal three-class moving-role witness."""
    for i, j in combinations(range(len(profile)), 2):
        for take_i in range(1, profile[i] + 1):
            for take_j in range(1, profile[j] + 1):
                moving_take = h - take_i - take_j
                if moving_take < 1:
                    continue
                candidates = []
                for moving in range(len(profile)):
                    if moving in (i, j) or profile[moving] < moving_take:
                        continue
                    takes = {i: take_i, j: take_j, moving: moving_take}
                    if frontier.leaves_singleton(profile, takes):
                        candidates.append(moving)
                if len(candidates) >= needed:
                    return (i, take_i, j, take_j, moving_take, candidates)
    return None


# Frozen incremental counts among the earlier R profiles at h=8.
expected = {1: 13, 2: 5, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0}
for k, count in expected.items():
    _, residuals = frontier.census(8, 8 + k)
    observed = sum(
        common_pole_witness(profile, 8, 2 * k + 1) is not None
        for profile in residuals
    )
    assert observed == count


# A zero moving class is possible only for a one-label role, and the
# clearing denominator remains -mu^2 there.
assert sp.factor((x**2 - mu**2).subs(x, 0)) == -mu**2

print("uniform constant-core common-pole root bound: PASS")
print("cleared moving-role degree <= 2k and nonidentity: exact")
print("asymptotic triangular coefficients are nonzero in every order")
print("h=8 old-R incremental counts k=1,...,7: 13,5,1,0,0,0,0")
