#!/usr/bin/env python3
"""Exact audit of the h=8,k=3 four-triple cubic-jet elimination."""

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


def main() -> None:
    u, tau, v, omega = sp.symbols("u tau v omega")
    D = u**2 - 1
    A = -(u + 7) / D
    B = 3 / (u + 1) ** 2 + 4 / (u - 1) ** 2
    C = 6 / (u + 1) ** 3 - 8 / (u - 1) ** 3
    q = tau - A

    R = sp.cancel(D**2 * (B + q - q**2 - v))
    S = sp.cancel(D**3 * (C + 2 * q**3 - 3 * q**2 - omega))
    assert sp.denom(R) == 1
    assert sp.denom(S) == 1

    L = sp.symbols("L")
    substitution = {v: -tau**2 + tau - L}
    R_L = sp.expand(R.subs(substitution))
    S_L = sp.expand(S.subs(substitution))

    expected_R = (
        L * u**4
        + (1 - 2 * tau) * u**3
        + (-2 * L - 14 * tau + 13) * u**2
        + (2 * tau - 13) * u
        + L
        + 14 * tau
        - 49
    )
    assert sp.expand(R_L - expected_R) == 0

    expected_S = (
        (2 * tau**3 - 3 * tau**2 - omega) * u**6
        + (6 * tau**2 - 6 * tau) * u**5
        + (-6 * tau**3 + 51 * tau**2 - 36 * tau + 3 * omega - 3) * u**4
        + (-12 * tau**2 + 96 * tau - 42) * u**3
        + (6 * tau**3 - 93 * tau**2 + 372 * tau - 3 * omega - 144) * u**2
        + (6 * tau**2 - 90 * tau + 330) * u
        - 2 * tau**3
        + 45 * tau**2
        - 336 * tau
        + omega
        + 819
    )
    assert sp.expand(S_L - expected_S) == 0

    pseudo_remainder = sp.prem(S_L, R_L, u)
    remainder_poly = sp.Poly(pseudo_remainder, u)
    c3, c2, c1, c0 = [
        remainder_poly.coeff_monomial(u**power) for power in (3, 2, 1, 0)
    ]

    P3 = (
        -56 * L**2
        - 32 * L * tau**2
        - 320 * L * tau
        + 101 * L
        - 224 * tau**3
        + 896 * tau**2
        - 357 * tau
        - 1432
    )
    P2 = 24 * L**2 + 128 * L * tau + 5 * L + 128 * tau**2 - 421 * tau + 810
    P1 = (
        -56 * L**2
        - 32 * L * tau**2
        - 155 * L
        - 224 * tau**3
        + 448 * tau**2
        + 155 * tau
        - 544
    )
    P0 = 3 * (8 * L**2 + 23 * L - 87 * tau + 110)
    certificate = sp.expand(P3 * c3 + P2 * c2 + P1 * c1 + P0 * c0)
    assert sp.factor(certificate - 26784 * L**3) == 0

    quotient = sp.pquo(S_L, R_L, u)
    assert sp.expand(L**3 * S_L - quotient * R_L - pseudo_remainder) == 0

    R_zero = sp.Poly(R_L.subs(L, 0), u)
    assert R_zero.degree() == 3
    assert R_zero.coeff_monomial(u**3) == 1 - 2 * tau
    assert R_zero.coeff_monomial(u**2).subs(tau, sp.Rational(1, 2)) == 6

    h, p = 8, 11
    counts, residuals = frontier.census(h, p)
    assert counts["R"] == 46
    profiles = (
        (3, 3, 3, 3, 2, 2, 2, 2, 1),
        (3, 3, 3, 3, 2, 2, 2, 1, 1, 1),
        (3, 3, 3, 3, 2, 2, 1, 1, 1, 1, 1),
        (3, 3, 3, 3, 2, 1, 1, 1, 1, 1, 1, 1),
    )
    for profile in profiles:
        assert profile in residuals
        triple_indices = tuple(i for i, multiplicity in enumerate(profile) if multiplicity == 3)
        assert len(triple_indices) == 4
        legal_count = 0
        for chosen in combinations(triple_indices, 3):
            for partial in chosen:
                takes = [0] * len(profile)
                for index in chosen:
                    takes[index] = 2 if index == partial else 3
                complement = [profile[index] - takes[index] for index in range(len(profile))]
                assert sum(takes) == h
                assert sum(value > 0 for value in takes) == 3
                assert complement.count(1) >= 1
                assert sum(complement) == 13
                legal_count += 1
        assert legal_count == 12

    print("PASS: exact h=8,k=3 four-triple cubic-jet elimination")


if __name__ == "__main__":
    main()
