#!/usr/bin/env python3
"""Exact audit for the p=19 moving-triple common-lift closure."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_q5_boundary_census as q5
import verify_live_three_zero_higher_split_p19_singleton_parity_common_lift_closure as singleton
import verify_live_three_zero_higher_split_p19_double_common_lift_closure as double


EXPECTED = {
    0: {(6, 2, -1), (7, 0, 0), (7, 1, -2)},
    1: {(5, 2, -2)},
}


def selected_triple_data(e: int, a: int, b: int, u: int) -> dict[str, int]:
    assert a >= 1
    if b >= 1:
        d = 2
        selected_doubles = 1
    else:
        d = 1
        selected_doubles = 0
    selected_singletons = None  # h-dependent; only its offset matters
    leftover_singletons = u - 2 + 2 * d
    remaining_doubles = b - selected_doubles
    # One selected triple leaves one complementary singleton at its value.
    complement_classes = (
        e
        + (a - 1)
        + remaining_doubles
        + leftover_singletons
        + 1
    )
    return {
        "d": d,
        "selected_doubles": selected_doubles,
        "leftover_singletons": leftover_singletons,
        "remaining_doubles": remaining_doubles,
        "complement_classes": complement_classes,
        "relation_degree": complement_classes - 4,
        "common_degree": complement_classes,
    }


def complement_profile(
    e: int, a: int, remaining_doubles: int, leftover_singletons: int
) -> tuple[int, ...]:
    return tuple(
        sorted(
            (4,) * e
            + (3,) * (a - 1)
            + (2,) * remaining_doubles
            + (1,) * (leftover_singletons + 1),
            reverse=True,
        )
    )


def route_applies(e: int, a: int, b: int, u: int) -> bool:
    if a < 1:
        return False
    data = selected_triple_data(e, a, b, u)
    if data["leftover_singletons"] < 0:
        return False
    degree = data["common_degree"]
    return (degree <= 7 and a >= 2) or (degree == 8 and a >= 6)


def audit_exact_families() -> None:
    observed = {0: set(), 1: set()}
    for e in (0, 1):
        for a, b, u in singleton.parameter_families(e):
            if not route_applies(e, a, b, u):
                continue
            observed[e].add((a, b, u))
            data = selected_triple_data(e, a, b, u)

            if b == 0:
                expected_degree = (21 - 2 * a) if e == 0 else (18 - 2 * a)
            else:
                expected_degree = (
                    (22 - 2 * a - b)
                    if e == 0
                    else (19 - 2 * a - b)
                )
            assert data["common_degree"] == expected_degree
            assert data["relation_degree"] + 4 == expected_degree

            complement = complement_profile(
                e,
                a,
                data["remaining_doubles"],
                data["leftover_singletons"],
            )
            assert sum(complement) == 19
            assert sum(min(part, 6) for part in complement) == 19
            assert len(complement) == data["complement_classes"]

            for h in range(13, 19):
                profile = singleton.profile_from_parameters(
                    h, e, a, b, u
                )
                selection = q5.Selection(data["d"], 1, complement)
                assert selection in q5.formal_selections(profile, h, 19)
                selected_singletons = h + 2 - 2 * data["d"]
                total_singletons = h + u
                assert total_singletons - selected_singletons == data[
                    "leftover_singletons"
                ]
                k = 19 - h
                assert 22 - h + max(0, 6 - k) > 0

            # Replacing the residual simple at the selected triple by a
            # baseline triple adds exactly two to the capped mass.  A
            # common six-space violates its Wronskian cap by nine.
            baseline_parts = list(complement)
            baseline_parts.remove(1)
            baseline_parts.append(3)
            forced_weight = sum(
                max(0, 6 - part) for part in baseline_parts
            )
            cap = 6 * (data["common_degree"] + 1 - 6)
            assert forced_weight - cap == 9

    assert observed == EXPECTED
    assert sum(len(values) for values in observed.values()) == 4


def audit_quartic_transport_and_third_jet() -> None:
    z, x, v = sp.symbols("z x v", nonzero=True)
    quartic = (z - x) ** 2 * (z + x) ** 2

    # The selected rational denominator has order two and its role-two
    # plus factor; the baseline triple denominator has order four.
    assert sp.factor(
        quartic / (z - x) ** 4
        - (z + x) ** 2 / (z - x) ** 2
    ) == 0

    r0, r1, r2 = sp.symbols("r0 r1 r2")
    local_r = r0 + r1 * (z - x) + r2 * (z - x) ** 2
    transported = (z - x) ** 2 * local_r
    assert sp.diff(transported, z, 3).subs(z, x) == 6 * r1

    # Exact normalized jets of B_x at a tested triple v.
    a_jet = sp.factor(sp.diff(quartic, z).subs(z, v) / quartic.subs(z, v))
    assert sp.factor(a_jet - 4 * v / (v**2 - x**2)) == 0
    b_jet = sp.factor(
        sp.diff(quartic, z, 2).subs(z, v) / quartic.subs(z, v)
    )
    c_jet = sp.factor(
        sp.diff(quartic, z, 3).subs(z, v) / quartic.subs(z, v)
    )
    assert sp.factor(b_jet - (a_jet**2 / 2 + a_jet / v)) == 0
    assert sp.factor(c_jet - 3 * a_jet**2 / (2 * v)) == 0

    # A_x=A_y implies x^2=y^2; structural nonopposition then gives x=y.
    y = sp.symbols("y")
    ay = 4 * v / (v**2 - y**2)
    assert sp.factor(
        (a_jet - ay) * (v**2 - x**2) * (v**2 - y**2)
        - 4 * v * (x - y) * (x + y)
    ) == 0


def audit_complete_graph_alternating_difference() -> None:
    a, b, c, d, constant, linear = sp.symbols(
        "a b c d constant linear"
    )
    fa, fb, fc, fd = sp.symbols("fa fb fc fd")

    # Reconstruct the normalized third derivative before absorbing the
    # one-index terms.  For B_x, b(a)=a^2/2+a/v and
    # c(a)=3a^2/(2v).
    v, alpha, beta, gamma = sp.symbols("v alpha beta gamma", nonzero=True)

    def second(x: sp.Expr) -> sp.Expr:
        return x**2 / 2 + x / v

    def third(x: sp.Expr) -> sp.Expr:
        return 3 * x**2 / (2 * v)

    normalized_third = (
        gamma
        + third(a)
        + third(b)
        + 3 * beta * (a + b)
        + 3 * alpha * (second(a) + second(b) + 2 * a * b)
        + 3 * (second(a) * b + second(b) * a)
    )
    one_a = third(a) + 3 * beta * a + 3 * alpha * second(a)
    one_b = third(b) + 3 * beta * b + 3 * alpha * second(b)
    reduced = sp.factor(normalized_third - gamma - one_a - one_b)
    expected_reduced = a * b * (
        6 * alpha + 6 / v + sp.Rational(3, 2) * (a + b)
    )
    assert sp.factor(reduced - expected_reduced) == 0

    def pair(x: sp.Expr, y: sp.Expr, fx: sp.Expr, fy: sp.Expr) -> sp.Expr:
        return constant + fx + fy + x * y * (
            linear + sp.Rational(3, 2) * (x + y)
        )

    alternating = sp.expand(
        pair(a, c, fa, fc)
        - pair(a, d, fa, fd)
        - pair(b, c, fb, fc)
        + pair(b, d, fb, fd)
    )
    target = (a - b) * (c - d) * (
        linear + sp.Rational(3, 2) * (a + b + c + d)
    )
    assert sp.factor(alternating - target) == 0

    # Five distinct values cannot give the same sum on every four-subset.
    values = sp.symbols("a0:5")
    sums = [sum(values[j] for j in range(5) if j != i) for i in range(5)]
    for i in range(1, 5):
        assert sp.factor(sums[i] - sums[0]) == values[0] - values[i]


def audit_intersections_and_ledger() -> None:
    for degree in range(4, 13):
        pair_dimension = max(degree - 8 + 1, 0)
        if degree <= 7:
            assert pair_dimension == 0
        if degree == 8:
            assert pair_dimension == 1

    singleton_closed = {0: set(), 1: set()}
    for e in (0, 1):
        for a, b, u in singleton.parameter_families(e):
            data = singleton.selected_data(e, a, b, u)
            if data["pool"] >= 1 and data["fixed_classes"] <= 5:
                singleton_closed[e].add((a, b, u))
        assert EXPECTED[e].isdisjoint(singleton_closed[e])
        assert EXPECTED[e].isdisjoint(double.EXPECTED[e])

    combined = sum(
        len(singleton_closed[e] | double.EXPECTED[e] | EXPECTED[e])
        for e in (0, 1)
    )
    assert combined == 75
    assert sum(len(singleton.parameter_families(e)) for e in (0, 1)) == 94

    expected_remaining = {
        0: {
            (0, 8, 5), (0, 9, 3), (0, 10, 1), (0, 11, -1),
            (1, 7, 4), (1, 8, 2), (1, 9, 0),
            (2, 6, 3), (2, 7, 1), (3, 5, 2), (4, 4, 1),
            (6, 0, 3), (6, 1, 1),
        },
        1: {
            (0, 7, 3), (0, 8, 1), (1, 6, 2),
            (2, 5, 1), (5, 0, 2), (5, 1, 0),
        },
    }
    observed_remaining = {}
    for e in (0, 1):
        observed_remaining[e] = (
            singleton.parameter_families(e)
            - singleton_closed[e]
            - double.EXPECTED[e]
            - EXPECTED[e]
        )
    assert observed_remaining == expected_remaining

    class_counts: dict[int, int] = {}
    for e in (0, 1):
        for a, b, _u in observed_remaining[e]:
            fixed_classes = e + a + max(b - 2, 0)
            class_counts[fixed_classes] = (
                class_counts.get(fixed_classes, 0) + 1
            )
    assert class_counts == {6: 12, 7: 4, 8: 2, 9: 1}


def main() -> None:
    audit_exact_families()
    audit_quartic_transport_and_third_jet()
    audit_complete_graph_alternating_difference()
    audit_intersections_and_ledger()
    print("p=19 moving-triple common-lift closure: PASS")
    print("new moving-triple families: 4")
    print("combined new p=19 ledger: 75/94 closed, 19 remain")
    print("quartic transport and third-jet complete graph: audited")


if __name__ == "__main__":
    main()
