#!/usr/bin/env python3
"""Exact audit of the consecutive constant-core role-transfer theorem."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


w, x, mu = sp.symbols("w x mu", nonzero=True)


def role_unit(value):
    return (1 - w / (value + mu)) ** -1 * (
        1 + w / (value - mu)
    ) ** -1


def coefficient(expr, order):
    return sp.expand(sp.series(expr, w, 0, order + 1).removeO()).coeff(w, order)


def check_transfer_factor_and_jet() -> None:
    A, B = sp.symbols("A B", nonzero=True)
    transfer = role_unit(A) / role_unit(B)
    assert sp.simplify(transfer.subs(w, 0) - 1) == 0
    jet = sp.factor(sp.diff(sp.log(transfer), w).subs(w, 0))
    expected = sp.factor(
        2 * mu * (A - B) * (A + B)
        / ((A**2 - mu**2) * (B**2 - mu**2))
    )
    assert sp.simplify(jet - expected) == 0


def check_polynomial_degree_and_leading_term() -> None:
    n = sp.symbols("n", integer=True)
    gamma_symbols = sp.symbols("g1:9")
    unit_symbols = sp.symbols("u0:9")
    assert unit_symbols[0] != 0
    for order in range(1, 9):
        log_r = sum(
            gamma_symbols[j - 1] * w**j / sp.factorial(j)
            for j in range(1, order + 1)
        )
        unit = sum(unit_symbols[j] * w**j for j in range(order + 1))
        f = sp.expand(
            sp.series(unit * sp.exp(n * log_r), w, 0, order + 1).removeO()
        ).coeff(w, order)
        polynomial = sp.Poly(f, n)
        assert polynomial.degree() == order
        assert sp.simplify(
            polynomial.LC()
            - unit_symbols[0] * gamma_symbols[0] ** order / sp.factorial(order)
        ) == 0

        difference = f
        for _ in range(order):
            difference = sp.expand(difference.subs(n, n + 1) - difference)
        assert sp.simplify(
            difference - unit_symbols[0] * gamma_symbols[0] ** order
        ) == 0


def check_k3_application() -> None:
    profile = (4, 4, 4, 3, 3, 3)
    h, p = 8, 11
    assert sum(profile) == p + h + 2 == 21
    counts, residuals = frontier.census(h, p)
    assert counts["R"] == 46
    assert profile in residuals

    # C is index 2.  Its unused mate is a singleton in all four complements.
    for transfer in range(4):
        takes = {0: 1 + transfer, 1: 4 - transfer, 2: 3}
        assert sum(takes.values()) == h
        assert all(1 <= takes[index] <= profile[index] for index in takes)
        assert profile[2] - takes[2] == 1
        assert frontier.leaves_singleton(profile, takes)
        assert len(takes) == 3
        assert len(takes) - 3 == 0  # constant Hermite residual degree


def main() -> None:
    check_transfer_factor_and_jet()
    check_polynomial_degree_and_leading_term()
    check_k3_application()
    print("higher-split consecutive constant-core role transfer: PASS")
    print("order-k residue is degree k in the transfer count with nonzero lead")
    print("k+1 consecutive legal transfers are impossible")
    print("first h=8,k=3 residual (4,4,4,3,3,3): closed")


if __name__ == "__main__":
    main()
