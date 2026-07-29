#!/usr/bin/env python3
"""Exact diagnostic census for higher no-extra-singular collision strata.

The script deliberately distinguishes proved routing rules from residual
profiles.  It audits the uniform deleted-e_h, short-Hermite, and degree
0/1/2 moving-class rules, and the value-core exchange/Wronskian rule.
Nothing classified ``R`` is asserted impossible.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp


def partitions(total: int, maximum: int | None = None):
    """Integer partitions in weakly decreasing order."""
    if total == 0:
        yield ()
        return
    if maximum is None:
        maximum = total
    for first in range(min(total, maximum), 0, -1):
        for tail in partitions(total - first, first):
            yield (first,) + tail


def count_parts(profile: tuple[int, ...], h: int) -> tuple[int, ...]:
    counts = [0] * h
    for part in profile:
        assert 1 <= part < h
        counts[part] += 1
    return tuple(counts)


def leaves_singleton(profile: tuple[int, ...], takes: dict[int, int]) -> bool:
    return any(
        multiplicity - takes.get(index, 0) == 1
        for index, multiplicity in enumerate(profile)
    )


@cache
def short_witness(profile: tuple[int, ...], h: int):
    """Select h labels in at most two classes and leave a singleton row."""
    for i, multiplicity in enumerate(profile):
        if multiplicity >= h and leaves_singleton(profile, {i: h}):
            return (i, h)
    for i, j in combinations(range(len(profile)), 2):
        lower = max(1, h - profile[j])
        upper = min(h - 1, profile[i])
        for take_i in range(lower, upper + 1):
            take_j = h - take_i
            takes = {i: take_i, j: take_j}
            if profile[j] >= take_j and leaves_singleton(profile, takes):
                return (i, take_i, j, take_j)
    return None


def anchor_count_vectors(
    counts: tuple[int, ...], anchor_count: int, zero_singleton: bool
):
    """Multiplicity-count vectors for distinct, structurally nonzero anchors."""
    available = list(counts)
    if zero_singleton:
        assert available[1] >= 1
        available[1] -= 1

    chosen = [0] * len(counts)

    def recur(multiplicity: int, left: int):
        if multiplicity == len(counts):
            if left == 0:
                yield tuple(chosen)
            return
        maximum = min(left, available[multiplicity])
        for take in range(maximum + 1):
            chosen[multiplicity] = take
            yield from recur(multiplicity + 1, left - take)
        chosen[multiplicity] = 0

    yield from recur(1, anchor_count)


@cache
def moving_witness_by_counts(
    profile: tuple[int, ...],
    h: int,
    anchor_count: int,
    needed_candidates: int,
    zero_singleton: bool,
):
    """Exact type-compressed search for a legal moving-class family."""
    counts = count_parts(profile, h)
    for anchors in anchor_count_vectors(counts, anchor_count, zero_singleton):
        after_anchors = tuple(
            counts[m] - anchors[m] for m in range(len(counts))
        )
        for fixed_multiplicity in range(1, h):
            if after_anchors[fixed_multiplicity] == 0:
                continue
            largest_fixed_take = min(
                fixed_multiplicity, h - anchor_count - 1
            )
            for fixed_take in range(1, largest_fixed_take + 1):
                moving_take = h - anchor_count - fixed_take
                if moving_take < 1:
                    continue

                candidate_count = 0
                for moving_multiplicity in range(moving_take, h):
                    available = after_anchors[moving_multiplicity]
                    if moving_multiplicity == fixed_multiplicity:
                        available -= 1
                    if available <= 0:
                        continue

                    untouched_singletons = counts[1] - anchors[1]
                    if fixed_multiplicity == 1:
                        untouched_singletons -= 1
                    if moving_multiplicity == 1:
                        untouched_singletons -= 1

                    singleton_row = (
                        untouched_singletons > 0
                        or anchors[2] > 0
                        or fixed_multiplicity - fixed_take == 1
                        or moving_multiplicity - moving_take == 1
                    )
                    if singleton_row:
                        candidate_count += available

                if candidate_count >= needed_candidates:
                    return (
                        anchors,
                        fixed_multiplicity,
                        fixed_take,
                        moving_take,
                        candidate_count,
                    )
    return None


def moving_method_works(
    profile: tuple[int, ...],
    h: int,
    anchor_count: int,
    needed_candidates: int,
) -> bool:
    scenarios = (False, True) if 1 in profile else (False,)
    return all(
        moving_witness_by_counts(
            profile,
            h,
            anchor_count,
            needed_candidates,
            zero_singleton,
        )
        is not None
        for zero_singleton in scenarios
    )


def every_value_core_legal(profile: tuple[int, ...], h: int) -> bool:
    """Every one-label-per-class h-core leaves a singleton in its complement."""
    classes = len(profile)
    doubles = profile.count(2)
    singletons = profile.count(1)
    if classes < h:
        return False
    # An illegal core contains every singleton and no double.  It exists
    # exactly when at least h nondouble classes are available and s <= h.
    return singletons > h or classes - doubles < h


def wronskian_value_core_closes(
    profile: tuple[int, ...], h: int, p: int
) -> bool:
    """The exact sufficient range of the exchange/residue/Wronskian count."""
    classes = len(profile)
    k = p - h
    if classes < h + 1 or not every_value_core_legal(profile, h):
        return False
    threshold = 8 + max(0, 3 - k)
    return classes <= threshold


@cache
def classify(profile: tuple[int, ...], h: int, p: int) -> str:
    assert sum(profile) == p + h + 2
    assert p >= h + 1 and h >= 8
    if profile == (1,) * sum(profile):
        return "D"
    if max(profile) >= h:
        return "H"
    if short_witness(profile, h) is not None:
        return "S"
    if moving_method_works(profile, h, 1, 3):
        return "C"
    if moving_method_works(profile, h, 2, 5):
        return "L"
    if moving_method_works(profile, h, 3, 7):
        return "Q"
    if wronskian_value_core_closes(profile, h, p):
        return "V"
    return "R"


def check_degree_and_wronskian_bookkeeping() -> None:
    p, h, m, c, k = sp.symbols("p h m c k", integer=True)
    assert sp.expand((p - h + 1) + h + m) == p + m + 1
    assert sp.expand((p + m - 1) - (p + 2)) == m - 3

    # Full-core rational function: B has one factor per unselected mate.
    total = p + h + 2
    excess = total - c
    denominator_degree = (k + 1) + 2 * c
    numerator_cap = excess + c - 1
    assert sp.expand(
        denominator_degree.subs(k, p - h) - numerator_cap
    ) == 2 * (c - h)

    r, b, t, w = sp.symbols("r b t w", integer=True, nonnegative=True)
    forced = (c - b) * (r - 1) + w
    cap = r * (c - r - 2 * b - t)
    difference = sp.expand(forced - cap)
    assert sp.expand(
        difference - (r**2 - c + b * (r + 1) + r * t + w)
    ) == 0

    # At t=0 the order-k residue hyperplane omits order k from the
    # vanishing sequence, adding max(0,r-k) Wronskian weight.
    for kval in range(1, 8):
        for dimension in range(3, 15):
            sequence = [a for a in range(dimension + 1) if a != kval][
                :dimension
            ]
            weight = sum(a - i for i, a in enumerate(sequence))
            assert weight == max(0, dimension - kval)

    assert 8 + max(0, 3 - 1) == 10
    assert 8 + max(0, 3 - 2) == 9
    assert all(8 + max(0, 3 - kval) == 8 for kval in range(3, 9))


def check_value_core_legality_formula() -> None:
    """Exhaust the closed form against literal h-subset enumeration."""
    for h in range(3, 10):
        for classes in range(h, h + 5):
            for doubles in range(classes + 1):
                for singletons in range(classes - doubles + 1):
                    highs = classes - doubles - singletons
                    profile = (
                        (3,) * highs + (2,) * doubles + (1,) * singletons
                    )
                    literal = True
                    for core in combinations(range(classes), h):
                        selected = set(core)
                        legal = any(
                            (profile[i] == 2 and i in selected)
                            or (profile[i] == 1 and i not in selected)
                            for i in range(classes)
                        )
                        literal &= legal
                    assert every_value_core_legal(profile, h) == literal


def check_short_closed_form() -> None:
    """Audit the simple top-two characterization after H is removed."""
    for h in range(3, 13):
        for total in range(h + 3, 3 * h + 3):
            for profile in partitions(total):
                if max(profile) >= h:
                    continue
                top_two = profile[0] + profile[1]
                closed_form = top_two >= h + 1 or (
                    1 in profile and top_two >= h
                )
                assert (short_witness(profile, h) is not None) == closed_form


def check_type_compression() -> None:
    """Compare compressed moving witnesses with literal index searches."""

    def literal(
        profile: tuple[int, ...],
        h: int,
        anchor_count: int,
        needed: int,
        zero_index: int | None,
    ) -> bool:
        anchors_pool = [i for i in range(len(profile)) if i != zero_index]
        for anchors in combinations(anchors_pool, anchor_count):
            for fixed in range(len(profile)):
                if fixed in anchors:
                    continue
                upper = min(profile[fixed], h - anchor_count - 1)
                for fixed_take in range(1, upper + 1):
                    moving_take = h - anchor_count - fixed_take
                    candidates = 0
                    for moving in range(len(profile)):
                        if moving in anchors or moving == fixed:
                            continue
                        if profile[moving] < moving_take:
                            continue
                        takes = {anchor: 1 for anchor in anchors}
                        takes[fixed] = fixed_take
                        takes[moving] = moving_take
                        if leaves_singleton(profile, takes):
                            candidates += 1
                    if candidates >= needed:
                        return True
        return False

    for h in range(5, 10):
        for total in range(h + 4, h + 11):
            for profile in partitions(total):
                if max(profile) >= h or len(profile) > 11:
                    continue
                for anchors, needed in ((1, 3), (2, 5), (3, 7)):
                    for zero_singleton in ((False, True) if 1 in profile else (False,)):
                        zero_index = profile.index(1) if zero_singleton else None
                        compressed = moving_witness_by_counts(
                            profile, h, anchors, needed, zero_singleton
                        ) is not None
                        assert compressed == literal(
                            profile, h, anchors, needed, zero_index
                        )


def census(h: int, p: int) -> tuple[dict[str, int], tuple[tuple[int, ...], ...]]:
    counts: dict[str, int] = {}
    residuals = []
    for profile in partitions(p + h + 2):
        category = classify(profile, h, p)
        counts[category] = counts.get(category, 0) + 1
        if category == "R":
            residuals.append(profile)
    return counts, tuple(residuals)


def legal_represented_class_counts(
    profile: tuple[int, ...], h: int
) -> tuple[int, ...]:
    """All m for h-label selections whose complement has a singleton."""
    states = {(0, 0, False)}
    for multiplicity in profile:
        next_states = set()
        for selected, represented, has_singleton in states:
            for take in range(min(multiplicity, h - selected) + 1):
                next_states.add(
                    (
                        selected + take,
                        represented + int(take > 0),
                        has_singleton or multiplicity - take == 1,
                    )
                )
        states = next_states
    return tuple(
        sorted(
            represented
            for selected, represented, has_singleton in states
            if selected == h and has_singleton
        )
    )


def check_census_and_persistence() -> None:
    expected_counts = {
        (8, 9): {"H": 190, "S": 218, "C": 17, "L": 10,
                 "Q": 11, "V": 8, "R": 35, "D": 1},
        (8, 10): {"H": 263, "S": 270, "C": 22, "L": 14,
                  "Q": 12, "V": 3, "R": 42, "D": 1},
        (8, 11): {"H": 356, "S": 338, "C": 22, "L": 16,
                  "Q": 13, "R": 46, "D": 1},
        (8, 12): {"H": 480, "S": 411, "C": 28, "L": 21,
                  "Q": 15, "R": 46, "D": 1},
        (9, 10): {"H": 267, "S": 355, "C": 28, "L": 14,
                  "Q": 12, "V": 11, "R": 104, "D": 1},
        (9, 11): {"H": 364, "S": 452, "C": 30, "L": 16,
                  "Q": 13, "R": 126, "D": 1},
        (9, 12): {"H": 491, "S": 555, "C": 38, "L": 22,
                  "Q": 15, "R": 133, "D": 1},
        (9, 13): {"H": 656, "S": 689, "C": 44, "L": 27,
                  "Q": 20, "R": 138, "D": 1},
        (10, 11): {"H": 368, "S": 593, "C": 33, "L": 16,
                   "Q": 13, "R": 231, "D": 1},
        (10, 12): {"H": 499, "S": 741, "C": 43, "L": 22,
                   "Q": 15, "R": 254, "D": 1},
        (10, 13): {"H": 667, "S": 923, "C": 49, "L": 27,
                   "Q": 20, "R": 271, "D": 1},
        (10, 14): {"H": 887, "S": 1137, "C": 59, "L": 36,
                   "Q": 26, "R": 290, "D": 1},
        (11, 12): {"H": 503, "S": 912, "C": 49, "L": 22,
                   "Q": 15, "R": 456, "D": 1},
        (11, 13): {"H": 675, "S": 1151, "C": 58, "L": 27,
                   "Q": 20, "R": 504, "D": 1},
        (11, 14): {"H": 898, "S": 1426, "C": 71, "L": 36,
                   "Q": 26, "R": 552, "D": 1},
        (11, 15): {"H": 1184, "S": 1769, "C": 83, "L": 44,
                   "Q": 36, "R": 601, "D": 1},
        (12, 13): {"H": 679, "S": 1427, "C": 61, "L": 27,
                   "Q": 20, "R": 795, "D": 1},
        (12, 14): {"H": 906, "S": 1785, "C": 76, "L": 36,
                   "Q": 26, "R": 888, "D": 1},
        (12, 15): {"H": 1195, "S": 2224, "C": 89, "L": 44,
                   "Q": 36, "R": 976, "D": 1},
        (12, 16): {"H": 1569, "S": 2739, "C": 111, "L": 56,
                   "Q": 47, "R": 1081, "D": 1},
    }
    for parameters, expected in expected_counts.items():
        assert census(*parameters)[0] == expected

    expected_value_core = {
        (8, 9): {
            (3, 3, 3, 3, 2, 2, 1, 1, 1),
            (3, 3, 3, 2, 2, 2, 2, 1, 1),
            (3, 3, 3, 2, 2, 2, 1, 1, 1, 1),
            (3, 3, 2, 2, 2, 2, 2, 2, 1),
            (3, 3, 2, 2, 2, 2, 2, 1, 1, 1),
            (3, 2, 2, 2, 2, 2, 2, 2, 2),
            (3, 2, 2, 2, 2, 2, 2, 2, 1, 1),
            (2, 2, 2, 2, 2, 2, 2, 2, 2, 1),
        },
        (8, 10): {
            (3, 3, 3, 3, 2, 2, 2, 1, 1),
            (3, 3, 3, 2, 2, 2, 2, 2, 1),
            (3, 3, 2, 2, 2, 2, 2, 2, 2),
        },
        (9, 10): {
            (4, 4, 4, 2, 2, 1, 1, 1, 1, 1),
            (4, 4, 3, 2, 2, 2, 1, 1, 1, 1),
            (4, 4, 2, 2, 2, 2, 2, 1, 1, 1),
            (4, 3, 3, 3, 2, 2, 1, 1, 1, 1),
            (4, 3, 3, 2, 2, 2, 2, 1, 1, 1),
            (4, 3, 2, 2, 2, 2, 2, 2, 1, 1),
            (4, 2, 2, 2, 2, 2, 2, 2, 2, 1),
            (3, 3, 3, 3, 2, 2, 2, 1, 1, 1),
            (3, 3, 3, 2, 2, 2, 2, 2, 1, 1),
            (3, 3, 2, 2, 2, 2, 2, 2, 2, 1),
            (3, 2, 2, 2, 2, 2, 2, 2, 2, 2),
        },
    }
    observed_value_core: dict[tuple[int, int], set[tuple[int, ...]]] = {}
    for h in range(8, 14):
        for k in range(1, 5):
            p = h + k
            observed = {
                profile
                for profile in partitions(p + h + 2)
                if classify(profile, h, p) == "V"
            }
            if observed:
                observed_value_core[(h, p)] = observed
    assert observed_value_core == expected_value_core

    expected_base_seed_counts = {
        8: [43, 45, 46, 46, 44, 44, 40],
        9: [115, 126, 133, 138, 140, 140, 140, 140],
        10: [231, 254, 271, 290, 302, 318, 332, 349, 363],
        11: [456, 504, 552, 601, 650, 704, 757, 815, 872, 930],
        12: [795, 888, 976, 1081, 1182, 1299, 1412, 1540,
             1665, 1804, 1931],
    }
    for h, expected in expected_base_seed_counts.items():
        observed = []
        for k in range(1, h):
            counts, _ = census(h, h + k)
            observed.append(counts.get("R", 0) + counts.get("V", 0))
        assert observed == expected

    # Every double/single collision profile is invisible to H/S/C/L/Q for
    # h>=8.  V has only the explicitly small (h,k,c) window.
    for h in range(8, 15):
        for k in range(1, 6):
            p = h + k
            total = p + h + 2
            for doubles in range(1, total // 2 + 1):
                singles = total - 2 * doubles
                profile = (2,) * doubles + (1,) * singles
                category = classify(profile, h, p)
                assert category in {"V", "R"}
                assert (category == "V") == wronskian_value_core_closes(
                    profile, h, p
                )

    # A broad persistent family: if the two largest parts sum to at most
    # h-4, none of H/S/C/L/Q can even fill its prescribed selected core.
    # Outside the finite V window it is therefore genuinely residual for
    # the audited methods.
    for h in range(8, 15):
        for k in range(1, 6):
            p = h + k
            for profile in partitions(p + h + 2):
                if profile == (1,) * sum(profile):
                    continue
                if profile[0] >= h or len(profile) < 2:
                    continue
                if profile[0] + profile[1] <= h - 4:
                    assert classify(profile, h, p) in {"V", "R"}

    # Every genuine residual still has a legal Hermite selection using at
    # most h-1 represented classes, but this bound is sharp.  The absence of
    # S forces the lower bound three.
    for h in range(8, 15):
        for k in range(1, 6):
            p = h + k
            _, residuals = census(h, p)
            for profile in residuals:
                represented = legal_represented_class_counts(profile, h)
                assert represented
                assert 3 <= represented[0] <= h - 1

    sparse = (2,) + (1,) * 17
    assert classify(sparse, 8, 9) == "R"
    assert legal_represented_class_counts(sparse, 8)[0] == 7

    smallest = (4, 3, 3, 3, 3, 3)
    assert classify(smallest, 8, 9) == "R"
    assert len(smallest) == 6 < 8
    assert legal_represented_class_counts(smallest, 8) == (3, 4, 5, 6)
    _, first_residuals = census(8, 9)
    assert {profile for profile in first_residuals if len(profile) == 6} == {
        smallest
    }
    minimum_distribution: dict[int, int] = {}
    for profile in first_residuals:
        minimum = legal_represented_class_counts(profile, 8)[0]
        minimum_distribution[minimum] = minimum_distribution.get(minimum, 0) + 1
    assert minimum_distribution == {3: 19, 4: 11, 5: 2, 6: 2, 7: 1}


def main() -> None:
    check_degree_and_wronskian_bookkeeping()
    check_value_core_legality_formula()
    check_short_closed_form()
    check_type_compression()
    check_census_and_persistence()
    print("higher-split collision frontier diagnostic: PASS")
    print("value-core legality and high-order residue/Wronskian range: exact")
    print("R means unresolved by this checker's audited route set")


if __name__ == "__main__":
    main()
