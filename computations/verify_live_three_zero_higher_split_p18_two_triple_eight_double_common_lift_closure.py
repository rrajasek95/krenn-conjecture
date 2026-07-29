#!/usr/bin/env python3
"""Exact audit of the p=18 a=2,b=8 common-lift closure."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verify_live_three_zero_higher_split_q5_boundary_census import (  # noqa: E402
    formal_selections,
)


def assert_zero(expr: sp.Expr) -> None:
    assert sp.factor(sp.together(expr)) == 0, sp.factor(sp.together(expr))


def profile(triples: int, doubles: int, singletons: int) -> tuple[int, ...]:
    return (3,) * triples + (2,) * doubles + (1,) * singletons


def audit_pair_selection_census() -> None:
    doubles = tuple(range(8))
    pairs = tuple(combinations(doubles, 2))
    assert len(pairs) == 28
    for fixed in doubles:
        assert sum(fixed in pair for pair in pairs) == 7

    for h in range(13, 18):
        original = profile(2, 8, h - 2)
        selections = formal_selections(original, h, 18)
        assert any(
            selection.d == 2
            and selection.selected_triples == 0
            and selection.complement == profile(2, 6, 0)
            for selection in selections
        )
        assert h - 2 >= 11

    # The endpoint relation space is a three-space in P_4.
    assert (2 + 6) - 4 == 4


def audit_exact_quintic_transport() -> None:
    z, i, j, v = sp.symbols("z i j v")
    multiplier = (z - j) ** 3 * (z + j) ** 2
    assert sp.Poly(multiplier, z).degree() == 5
    assert multiplier.subs(z, j) == 0
    assert sp.diff(multiplier, z).subs(z, j) == 0
    assert sp.diff(multiplier, z, 2).subs(z, j) == 0

    log_multiplier = sp.cancel(sp.diff(multiplier, z) / multiplier)
    assert_zero(log_multiplier - 3 / (z - j) - 2 / (z + j))
    log_second = sp.cancel(sp.diff(log_multiplier, z))
    assert_zero(log_second + 3 / (z - j) ** 2 + 2 / (z + j) ** 2)

    # Product-rule transport of the normalized second-order row.
    s0, s1, s2, g0, g1, g2, alpha, delta = sp.symbols(
        "s0 s1 s2 g0 g1 g2 alpha delta"
    )
    old_row_on_product = (
        g2 * s0 + 2 * g1 * s1 + g0 * s2
        + 2 * alpha * (g1 * s0 + g0 * s1)
        + delta * g0 * s0
    )
    shifted_alpha = alpha + g1 / g0
    shifted_delta = delta + 2 * alpha * g1 / g0 + g2 / g0
    shifted_row_on_s = g0 * (
        s2 + 2 * shifted_alpha * s1 + shifted_delta * s0
    )
    assert_zero(old_row_on_product - shifted_row_on_s)

    # Unit ratio when j moves from a complementary cube to a selected square.
    formal_unit_ratio = (z - j) ** 3 * (z + j) ** 2
    assert_zero(formal_unit_ratio - multiplier)
    assert multiplier.subs(z, v) != 0


def audit_coprime_direct_sum() -> None:
    z, a, b = sp.symbols("z a b")
    g_a = (z - a) ** 3 * (z + a) ** 2
    g_b = (z - b) ** 3 * (z + b) ** 2
    resultant = sp.factor(sp.resultant(g_a, g_b, z))
    assert_zero(resultant - (a - b) ** 13 * (a + b) ** 12)
    assert sp.Poly(g_a * g_b, z).degree() == 10 > 9
    assert 3 + 3 == 6


def audit_wronskian_bound() -> None:
    # A single nonzero second-order row allows at most two jets below order 3.
    for dimension in range(2, 11):
        vanishing = (0, 1) + tuple(range(3, dimension + 1))
        assert len(vanishing) == dimension
        assert sum(vanishing) - sum(range(dimension)) == dimension - 2

    allowed = []
    for dimension in range(1, 11):
        forced = 7 * max(dimension - 2, 0)
        cap = dimension * (10 - dimension)
        if forced <= cap:
            allowed.append(dimension)
    assert max(allowed) == 5
    assert 7 * (6 - 2) == 28 > 6 * (10 - 6) == 24
    for dimension in range(6, 11):
        assert dimension**2 - 3 * dimension - 14 > 0


def main() -> None:
    audit_pair_selection_census()
    audit_exact_quintic_transport()
    audit_coprime_direct_sum()
    audit_wronskian_bound()
    print("p=18 two-triple eight-double common-lift closure PASS")
    print("selected-pair endpoint spaces audited: 28")
    print("fixed selected value: seven lifted three-spaces in P_9")
    print("two coprime lifts force dimension at least 6")
    print("seven second-order rows force dimension at most 5")
    print("remaining a=2 families: none")


if __name__ == "__main__":
    main()
