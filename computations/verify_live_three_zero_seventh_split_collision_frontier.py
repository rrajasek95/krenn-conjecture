#!/usr/bin/env python3
"""Exact audit for the repeated-beta seventh-split frontier."""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp


MIN_FEASIBLE_P = 8
FORMAL_DIAGNOSTIC_P = 7


def elementary(values: tuple[sp.Expr, ...], degree: int) -> sp.Expr:
    if degree == 0:
        return sp.Integer(1)
    return sp.expand(
        sum(
            sp.prod(values[i] for i in chosen)
            for chosen in combinations(range(len(values)), degree)
        )
    )


def check_degree_bookkeeping() -> None:
    p, m = sp.symbols("p m", integer=True)
    k = p - 7
    assert sp.expand((k + 1) + 7 + m) == p + m + 1
    assert sp.expand((p + m + 1) - 2) == p + m - 1
    assert [(p + m - 1) - (p + 2) for m in range(3, 8)] == [0, 1, 2, 3, 4]
    assert MIN_FEASIBLE_P + 9 <= 2 * MIN_FEASIBLE_P + 1
    assert FORMAL_DIAGNOSTIC_P + 9 > 2 * FORMAL_DIAGNOSTIC_P + 1


def check_deleted_e7_descent() -> None:
    ten = sp.symbols("h0:10")
    i, j, k = 2, 0, 1
    delete_ij = tuple(v for index, v in enumerate(ten) if index not in (i, j))
    delete_ik = tuple(v for index, v in enumerate(ten) if index not in (i, k))
    common = tuple(v for index, v in enumerate(ten) if index not in (i, j, k))
    assert sp.expand(
        elementary(delete_ij, 7)
        - elementary(delete_ik, 7)
        - (ten[k] - ten[j]) * elementary(common, 6)
    ) == 0

    values = sp.symbols("v0:8")
    for degree in range(1, 7):
        lhs = sum(
            elementary(values[:i] + values[i + 1 :], degree)
            for i in range(len(values))
        )
        rhs = (len(values) - degree) * elementary(values, degree)
        assert sp.expand(lhs - rhs) == 0
        assert sp.expand(
            elementary(values, degree)
            - elementary(values[1:], degree)
            - values[0] * elementary(values[1:], degree - 1)
        ) == 0


def quadratic_residual_phi(
    a: sp.Expr,
    b: sp.Expr,
    c: sp.Expr,
    A: sp.Expr,
    B: sp.Expr,
    C: sp.Expr,
) -> sp.Expr:
    delta = (a - b) * (a - c) * (b - c)
    return sp.expand(
        -delta * A * B * C
        + (b - a) * (a + b - 2 * c) * A * B
        + (a - c) * (a + c - 2 * b) * A * C
        + (c - b) * (b + c - 2 * a) * B * C
        + 2 * (c - b) * A
        + 2 * (a - c) * B
        + 2 * (b - a) * C
    )


def check_moving_lemmas() -> None:
    x, a, b, c, u, v, w, gamma = sp.symbols("x a b c U V W gamma")
    chi = lambda anchor: -(x + gamma * anchor) / (x**2 - anchor**2)

    constant = sp.expand(u * (x**2 - a**2) - x - gamma * a)
    assert sp.Poly(constant, x).degree() == 2
    assert constant.coeff(x, 1) == -1

    ya = u + chi(a)
    yb = v + chi(b)
    linear = sp.together(yb - ya + (b - a) * ya * yb).as_numer_denom()[0]
    linear = sp.expand(linear)
    assert sp.Poly(linear, x).degree() <= 4
    assert sp.expand(linear.coeff(x, 3) - (a - b) * (u + v)) == 0
    assert sp.expand(linear.coeff(x, 4) - ((b - a) * u * v - u + v)) == 0
    branch_zero = (a - b) * (gamma - 1) * (
        x**2 - (a + b) * x - gamma * a * b
    )
    branch_two = -(a - b) * (gamma + 1) * (
        x**2 + (a + b) * x + gamma * a * b
    )
    assert sp.factor(linear.subs({u: 0, v: 0}) - branch_zero) == 0
    assert sp.factor(
        linear.subs({u: 2 / (a - b), v: -2 / (a - b)}) - branch_two
    ) == 0

    A, B, C = sp.symbols("A B C")
    phi = quadratic_residual_phi(a, b, c, A, B, C)
    moving = phi.subs({A: u + chi(a), B: v + chi(b), C: w + chi(c)})
    cleared = sp.cancel(
        moving * (x**2 - a**2) * (x**2 - b**2) * (x**2 - c**2)
    )
    assert sp.denom(cleared) == 1
    assert sp.Poly(cleared, x).degree() <= 6

    chi_at = lambda anchor, moving_value: -(
        moving_value + gamma * anchor
    ) / (moving_value**2 - anchor**2)
    difference_a = sp.cancel(
        sp.diff(phi, A).subs({B: v + chi_at(b, a), C: w + chi_at(c, a)})
        - sp.diff(phi, A).subs({B: v + chi_at(b, -a), C: w + chi_at(c, -a)})
    )
    difference_b = sp.cancel(
        sp.diff(phi, B).subs({A: u + chi_at(a, b), C: w + chi_at(c, b)})
        - sp.diff(phi, B).subs({A: u + chi_at(a, -b), C: w + chi_at(c, -b)})
    )
    difference_c = sp.cancel(
        sp.diff(phi, C).subs({A: u + chi_at(a, c), B: v + chi_at(b, c)})
        - sp.diff(phi, C).subs({A: u + chi_at(a, -c), B: v + chi_at(b, -c)})
    )

    linear_a = (
        (a**2 - b**2) * v
        + (a**2 - c**2) * w
        + 2 * a
        + (2 - gamma) * (b + c)
    )
    linear_b = (
        (a**2 - b**2) * u
        + (c**2 - b**2) * w
        + (gamma - 2) * (a + c)
        - 2 * b
    )
    linear_c = (
        (a**2 - c**2) * u
        + (b**2 - c**2) * v
        + (gamma - 2) * (a + b)
        - 2 * c
    )
    assert sp.factor(
        difference_a
        - 2 * a * (b - c) / ((a + b) * (a + c)) * linear_a
    ) == 0
    assert sp.factor(
        difference_b
        - 2 * b * (a - c) / ((a + b) * (b + c)) * linear_b
    ) == 0
    assert sp.factor(
        difference_c
        + 2 * c * (a - b) / ((a + c) * (b + c)) * linear_c
    ) == 0
    incompatibility = (
        -(b**2 - c**2) * linear_a
        - (a**2 - c**2) * linear_b
        + (a**2 - b**2) * linear_c
    )
    assert sp.factor(
        incompatibility - gamma * (a - b) * (a - c) * (b - c)
    ) == 0

    j = sp.symbols("j", integer=True, positive=True)
    direct_chi = j / (a + x) - (j + 1) / (x - a)
    assert sp.factor(
        direct_chi + (x + (2 * j + 1) * a) / (x**2 - a**2)
    ) == 0


def partitions(total: int, maximum: int | None = None):
    if total == 0:
        yield ()
        return
    if maximum is None:
        maximum = total
    for first in range(min(total, maximum), 0, -1):
        for tail in partitions(total - first, first):
            yield (first,) + tail


def leaves_singleton(profile: tuple[int, ...], takes: dict[int, int]) -> bool:
    return any(
        multiplicity - takes.get(index, 0) == 1
        for index, multiplicity in enumerate(profile)
    )


@cache
def short_witness(profile: tuple[int, ...]):
    for i, multiplicity in enumerate(profile):
        if multiplicity >= 7 and leaves_singleton(profile, {i: 7}):
            return (i, 7)
    for i, j in combinations(range(len(profile)), 2):
        for take_i in range(1, 7):
            take_j = 7 - take_i
            takes = {i: take_i, j: take_j}
            if (
                profile[i] >= take_i
                and profile[j] >= take_j
                and leaves_singleton(profile, takes)
            ):
                return (i, take_i, j, take_j)
    return None


@cache
def moving_witness(
    profile: tuple[int, ...],
    anchor_count: int,
    needed_candidates: int,
    zero_index: int | None,
):
    anchor_pool = [i for i in range(len(profile)) if i != zero_index]
    for anchors in combinations(anchor_pool, anchor_count):
        for fixed in range(len(profile)):
            if fixed in anchors:
                continue
            for fixed_take in range(
                1, min(6 - anchor_count, profile[fixed]) + 1
            ):
                moving_take = 7 - anchor_count - fixed_take
                candidates = []
                for moving in range(len(profile)):
                    if moving in anchors or moving == fixed:
                        continue
                    if profile[moving] < moving_take:
                        continue
                    takes = {anchor: 1 for anchor in anchors}
                    takes[fixed] = fixed_take
                    takes[moving] = moving_take
                    if leaves_singleton(profile, takes):
                        candidates.append(moving)
                if len(candidates) >= needed_candidates:
                    return anchors, fixed, fixed_take, moving_take, tuple(candidates)
    return None


def zero_scenarios(profile: tuple[int, ...]) -> tuple[int | None, ...]:
    # Repeated zero values violate the structural pair-sum condition.  All
    # singleton classes are symmetric, so one representative suffices.
    if 1 in profile:
        return None, profile.index(1)
    return (None,)


def method_works_for_every_zero_scenario(
    profile: tuple[int, ...], anchor_count: int, needed_candidates: int
) -> bool:
    return all(
        moving_witness(profile, anchor_count, needed_candidates, zero) is not None
        for zero in zero_scenarios(profile)
    )


@cache
def classify(profile: tuple[int, ...]) -> str:
    if profile == (1,) * sum(profile):
        return "D"
    if max(profile) >= 7:
        return "H"
    if short_witness(profile) is not None:
        return "S"
    if method_works_for_every_zero_scenario(profile, 1, 3):
        return "C"
    if method_works_for_every_zero_scenario(profile, 2, 5):
        return "L"
    if method_works_for_every_zero_scenario(profile, 3, 7):
        return "Q"
    return "R"


EXPECTED_COUNTS = {
    7: {"H": 95, "S": 96, "C": 11, "L": 4, "Q": 6, "R": 18, "D": 1},
    8: {"H": 134, "S": 119, "C": 13, "L": 7, "Q": 9, "R": 14, "D": 1},
    9: {"H": 186, "S": 151, "C": 14, "L": 10, "Q": 11, "R": 12, "D": 1},
    10: {"H": 255, "S": 182, "C": 18, "L": 13, "Q": 12, "R": 9, "D": 1},
    11: {"H": 345, "S": 226, "C": 19, "L": 14, "Q": 13, "R": 9, "D": 1},
    12: {"H": 461, "S": 269, "C": 22, "L": 16, "Q": 14, "R": 9, "D": 1},
    13: {"H": 611, "S": 325, "C": 25, "L": 17, "Q": 16, "R": 7, "D": 1},
}


TRIPLE_RESIDUALS = {
    7: {
        (3, 3, 1), (3, 2, 3), (3, 1, 5), (3, 0, 7),
        (2, 5, 0), (2, 4, 2), (2, 3, 4), (2, 2, 6),
        (1, 6, 1), (1, 4, 5),
    },
    8: {
        (3, 4, 0), (3, 3, 2), (3, 2, 4), (3, 1, 6),
        (2, 5, 1), (2, 3, 5),
    },
    9: {(6, 0, 0), (3, 4, 1), (3, 2, 5)},
    10: set(),
    11: set(),
    12: {(7, 0, 0)},
}


def double_single_closed(doubles: int, singles: int) -> bool:
    return (
        (doubles >= 8 and singles >= 4)
        or (doubles >= 9 and singles >= 3)
        or (doubles >= 10 and singles >= 2)
        or doubles >= 11
    )


def profile_type(profile: tuple[int, ...]) -> tuple[int, int, int]:
    return profile.count(3), profile.count(2), profile.count(1)


def check_census() -> None:
    residuals_by_total: dict[int, set[tuple[int, ...]]] = {}
    for p in range(FORMAL_DIAGNOSTIC_P, 20):
        profiles = list(partitions(p + 9))
        counts: dict[str, int] = {}
        residuals = set()
        for profile in profiles:
            category = classify(profile)
            counts[category] = counts.get(category, 0) + 1
            if category == "R":
                residuals.add(profile)
                assert max(profile) <= 3
        residuals_by_total[p + 9] = residuals
        if p in EXPECTED_COUNTS:
            assert counts == EXPECTED_COUNTS[p]

        triple_types = {
            profile_type(profile)
            for profile in residuals
            if 3 in profile
        }
        if p <= 12:
            assert triple_types == TRIPLE_RESIDUALS[p]
        else:
            assert triple_types == set()

        for profile in profiles:
            if set(profile) <= {1, 2} and profile != (1,) * (p + 9):
                d, s = profile.count(2), profile.count(1)
                assert (classify(profile) == "Q") == double_single_closed(d, s)
                assert (classify(profile) == "R") == (not double_single_closed(d, s))

        if p >= 13:
            expected = {
                (2,) * doubles + (1,) * (p + 9 - 2 * doubles)
                for doubles in range(1, 8)
            }
            assert residuals == expected

    # Exact finite base for the monotone reduction in the note.
    for total in range(22, 29):
        residuals = residuals_by_total[total]
        assert all(set(profile) <= {1, 2} for profile in residuals)
        assert residuals == {
            (2,) * doubles + (1,) * (total - 2 * doubles)
            for doubles in range(1, 8)
        }

    # Directly audit upward persistence of every concrete witness throughout
    # the finite base range.  This supports the class-removal induction.
    for total in range(16, 29):
        for profile in partitions(total):
            if classify(profile) not in {"H", "S", "C", "L", "Q"}:
                continue
            for added_multiplicity in range(1, 7):
                enlarged = tuple(sorted(profile + (added_multiplicity,), reverse=True))
                assert classify(enlarged) in {"H", "S", "C", "L", "Q"}

    # A new singleton may itself be the unique zero.  In that case an old
    # no-zero moving witness uses only old, hence nonzero, anchors and remains
    # legal after the new zero singleton is appended untouched.  If the zero
    # remains on an old singleton, the old zero-scenario witness persists.
    moving_method = {"C": (1, 3), "L": (2, 5), "Q": (3, 7)}
    for total in range(16, 29):
        for profile in partitions(total):
            category = classify(profile)
            if category not in moving_method:
                continue
            anchor_count, needed = moving_method[category]
            old_no_zero = moving_witness(
                profile, anchor_count, needed, zero_index=None
            )
            assert old_no_zero is not None
            enlarged = profile + (1,)
            new_zero_index = len(enlarged) - 1
            assert moving_witness(
                enlarged, anchor_count, needed, zero_index=new_zero_index
            ) is not None

            if 1 in profile:
                old_zero_index = profile.index(1)
                old_zero = moving_witness(
                    profile, anchor_count, needed, zero_index=old_zero_index
                )
                assert old_zero is not None
                assert moving_witness(
                    enlarged,
                    anchor_count,
                    needed,
                    zero_index=old_zero_index,
                ) is not None


def main() -> None:
    check_degree_bookkeeping()
    check_deleted_e7_descent()
    check_moving_lemmas()
    check_census()
    print("seventh-split repeated-beta closures and exact residual census: PASS")
    print("feasible range: p >= 8 (p = 7 retained only as a formal diagnostic)")
    print("OPEN for p>=13: (2^d,1^(p+9-2d)), 1 <= d <= 7")


if __name__ == "__main__":
    main()
