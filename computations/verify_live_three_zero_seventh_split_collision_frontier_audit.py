#!/usr/bin/env python3
"""Independent audit of the seventh-split repeated-beta frontier.

The main checker enumerates integer partitions and concrete class indices.
This audit instead enumerates bounded multiplicity histograms by dynamic
programming and allocates anchor/fixed/moving roles by class-size counts.
"""

from __future__ import annotations

from functools import cache
from itertools import product
from math import comb

import sympy as sp


MIN_FEASIBLE_P = 8
MAX_LOW_PART = 6
HANDLED = {"H", "S", "C", "L", "Q"}
METHOD = {"C": (1, 3), "L": (2, 5), "Q": (3, 7)}


def feasible(p: int) -> bool:
    r = p + 1
    t = p + 9
    return t <= 2 * r - 1


def check_feasibility() -> None:
    for p in range(-20, 101):
        assert feasible(p) == (p >= MIN_FEASIBLE_P)
    assert not feasible(7)
    assert feasible(8)


def partition_number(total: int) -> int:
    """Euler coin-change DP; independent of the histogram enumerator."""

    ways = [0] * (total + 1)
    ways[0] = 1
    for part in range(1, total + 1):
        for value in range(part, total + 1):
            ways[value] += ways[value - part]
    return ways[total]


def low_histograms(limit: int) -> dict[int, set[tuple[int, ...]]]:
    """DP all c=(c_1,...,c_6) with sum(m*c_m)<=limit."""

    states: set[tuple[int, tuple[int, ...]]] = {
        (0, (0,) * MAX_LOW_PART)
    }
    for multiplicity in range(1, MAX_LOW_PART + 1):
        extended: set[tuple[int, tuple[int, ...]]] = set()
        for subtotal, histogram in states:
            for count in range((limit - subtotal) // multiplicity + 1):
                updated = list(histogram)
                updated[multiplicity - 1] = count
                extended.add(
                    (subtotal + multiplicity * count, tuple(updated))
                )
        states = extended

    by_total = {total: set() for total in range(limit + 1)}
    for total, histogram in states:
        by_total[total].add(histogram)
    return by_total


def total_size(histogram: tuple[int, ...]) -> int:
    return sum((index + 1) * count for index, count in enumerate(histogram))


def add_class(
    histogram: tuple[int, ...], multiplicity: int
) -> tuple[int, ...]:
    enlarged = list(histogram)
    enlarged[multiplicity - 1] += 1
    return tuple(enlarged)


def enough_classes(
    histogram: tuple[int, ...], first: int, second: int
) -> bool:
    if first != second:
        return histogram[first - 1] > 0 and histogram[second - 1] > 0
    return histogram[first - 1] >= 2


@cache
def short_pattern(
    histogram: tuple[int, ...],
) -> tuple[int, int, int, int] | None:
    """Return two class sizes and their selected counts, if legal."""

    for first_size in range(1, MAX_LOW_PART + 1):
        for second_size in range(first_size, MAX_LOW_PART + 1):
            if not enough_classes(histogram, first_size, second_size):
                continue
            for first_take in range(1, first_size + 1):
                second_take = 7 - first_take
                if not 1 <= second_take <= second_size:
                    continue
                untouched_singletons = histogram[0]
                untouched_singletons -= int(first_size == 1)
                untouched_singletons -= int(second_size == 1)
                residual_singletons = untouched_singletons
                residual_singletons += int(first_size - first_take == 1)
                residual_singletons += int(second_size - second_take == 1)
                if residual_singletons > 0:
                    return first_size, first_take, second_size, second_take
    return None


def short_pattern_is_legal(
    histogram: tuple[int, ...], pattern: tuple[int, int, int, int]
) -> bool:
    first_size, first_take, second_size, second_take = pattern
    if not enough_classes(histogram, first_size, second_size):
        return False
    if first_take + second_take != 7:
        return False
    if not (1 <= first_take <= first_size and 1 <= second_take <= second_size):
        return False
    untouched = histogram[0] - int(first_size == 1) - int(second_size == 1)
    residual = untouched
    residual += int(first_size - first_take == 1)
    residual += int(second_size - second_take == 1)
    return residual > 0


def nonzero_inventory(
    histogram: tuple[int, ...], zero_singleton: bool
) -> tuple[int, ...]:
    inventory = list(histogram)
    if zero_singleton:
        assert inventory[0] >= 1
        inventory[0] -= 1
    return tuple(inventory)


def anchor_allocations(
    inventory: tuple[int, ...], anchor_count: int
):
    ranges = [range(min(count, anchor_count) + 1) for count in inventory]
    for allocation in product(*ranges):
        if sum(allocation) == anchor_count:
            yield allocation


# A moving pattern is
# (anchor count by multiplicity, fixed multiplicity, fixed-is-zero,
#  fixed selected count, moving selected count).
MovingPattern = tuple[tuple[int, ...], int, bool, int, int]


def candidate_count(
    histogram: tuple[int, ...],
    pattern: MovingPattern,
    zero_singleton: bool,
) -> int:
    anchors, fixed_size, fixed_is_zero, fixed_take, moving_take = pattern
    normal = list(nonzero_inventory(histogram, zero_singleton))
    if any(anchors[index] > normal[index] for index in range(MAX_LOW_PART)):
        return -1
    for index, count in enumerate(anchors):
        normal[index] -= count

    zero_available = int(zero_singleton)
    if fixed_is_zero:
        if fixed_size != 1 or fixed_take != 1 or not zero_available:
            return -1
        zero_available = 0
    else:
        if normal[fixed_size - 1] == 0 or not 1 <= fixed_take <= fixed_size:
            return -1
        normal[fixed_size - 1] -= 1

    base_singletons = anchors[1]
    base_singletons += int(fixed_size - fixed_take == 1)
    base_singletons += normal[0] + zero_available

    candidates = 0
    for moving_size, available in enumerate(normal, start=1):
        if moving_size < moving_take or available == 0:
            continue
        singleton_count = base_singletons
        singleton_count -= int(moving_size == 1)
        singleton_count += int(moving_size - moving_take == 1)
        if singleton_count > 0:
            candidates += available

    if zero_available and moving_take == 1:
        singleton_count = base_singletons - 1
        if singleton_count > 0:
            candidates += 1
    return candidates


@cache
def moving_pattern(
    histogram: tuple[int, ...],
    anchor_count: int,
    needed_candidates: int,
    zero_singleton: bool,
) -> MovingPattern | None:
    normal = nonzero_inventory(histogram, zero_singleton)
    for anchors in anchor_allocations(normal, anchor_count):
        after_anchors = [
            normal[index] - anchors[index] for index in range(MAX_LOW_PART)
        ]
        fixed_options = [
            (size, False)
            for size, available in enumerate(after_anchors, start=1)
            if available > 0
        ]
        if zero_singleton:
            fixed_options.append((1, True))

        for fixed_size, fixed_is_zero in fixed_options:
            for fixed_take in range(1, min(fixed_size, 6 - anchor_count) + 1):
                moving_take = 7 - anchor_count - fixed_take
                pattern = (
                    anchors,
                    fixed_size,
                    fixed_is_zero,
                    fixed_take,
                    moving_take,
                )
                if candidate_count(histogram, pattern, zero_singleton) >= needed_candidates:
                    return pattern
    return None


def moving_is_zero_robust(
    histogram: tuple[int, ...], anchor_count: int, needed_candidates: int
) -> bool:
    if moving_pattern(histogram, anchor_count, needed_candidates, False) is None:
        return False
    if histogram[0] == 0:
        return True
    return moving_pattern(histogram, anchor_count, needed_candidates, True) is not None


@cache
def classify_low(histogram: tuple[int, ...]) -> str:
    total = total_size(histogram)
    if histogram[0] == total:
        return "D"
    if short_pattern(histogram) is not None:
        return "S"
    if moving_is_zero_robust(histogram, 1, 3):
        return "C"
    if moving_is_zero_robust(histogram, 2, 5):
        return "L"
    if moving_is_zero_robust(histogram, 3, 7):
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


EXPECTED_TRIPLE_RESIDUALS = {
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
    13: set(),
}


def double_single_formula(doubles: int, singles: int) -> bool:
    return (
        (doubles >= 8 and singles >= 4)
        or (doubles >= 9 and singles >= 3)
        or (doubles >= 10 and singles >= 2)
        or doubles >= 11
    )


def check_histogram_census() -> dict[int, set[tuple[int, ...]]]:
    table = low_histograms(40)
    residuals_by_total: dict[int, set[tuple[int, ...]]] = {}

    for p in range(7, 32):
        total = p + 9
        low = table[total]
        counts = {label: 0 for label in ("H", "S", "C", "L", "Q", "R", "D")}
        counts["H"] = partition_number(total) - len(low)
        residuals: set[tuple[int, ...]] = set()
        for histogram in low:
            category = classify_low(histogram)
            counts[category] += 1
            if category == "R":
                residuals.add(histogram)
                assert all(histogram[index] == 0 for index in range(3, 6))
        residuals_by_total[total] = residuals

        assert sum(counts.values()) == partition_number(total)
        if p in EXPECTED_COUNTS:
            assert counts == EXPECTED_COUNTS[p]

        triple_residuals = {
            (histogram[2], histogram[1], histogram[0])
            for histogram in residuals
            if histogram[2] > 0
        }
        if p in EXPECTED_TRIPLE_RESIDUALS:
            assert triple_residuals == EXPECTED_TRIPLE_RESIDUALS[p]
        elif p >= 13:
            assert not triple_residuals

        for histogram in low:
            if any(histogram[index] for index in range(2, 6)):
                continue
            doubles, singles = histogram[1], histogram[0]
            if doubles == 0:
                assert classify_low(histogram) == "D"
                continue
            expected = double_single_formula(doubles, singles)
            assert (classify_low(histogram) == "Q") == expected
            assert (classify_low(histogram) == "R") == (not expected)

        if p >= 13:
            expected_residuals = {
                (p + 9 - 2 * doubles, doubles, 0, 0, 0, 0)
                for doubles in range(1, 8)
            }
            assert residuals == expected_residuals

    return residuals_by_total


def e_from_generating_function(
    values: tuple[sp.Expr, ...], degree: int, marker: sp.Symbol
) -> sp.Expr:
    generating = sp.Poly(
        sp.prod(1 + marker * value for value in values), marker
    )
    return generating.coeff_monomial(marker**degree)


def check_deleted_e7_descent() -> None:
    marker = sp.symbols("z")
    values = sp.symbols("h0:10")
    first, second, third = 2, 0, 1
    delete_first_second = tuple(
        value
        for index, value in enumerate(values)
        if index not in (first, second)
    )
    delete_first_third = tuple(
        value
        for index, value in enumerate(values)
        if index not in (first, third)
    )
    common = tuple(
        value
        for index, value in enumerate(values)
        if index not in (first, second, third)
    )
    subtraction = (
        e_from_generating_function(delete_first_second, 7, marker)
        - e_from_generating_function(delete_first_third, 7, marker)
        - (values[third] - values[second])
        * e_from_generating_function(common, 6, marker)
    )
    assert sp.expand(subtraction) == 0

    core = sp.symbols("w0:8")
    for degree in range(1, 7):
        full = e_from_generating_function(core, degree, marker)
        deleted_sum = sum(
            e_from_generating_function(
                core[:index] + core[index + 1 :], degree, marker
            )
            for index in range(len(core))
        )
        assert sp.expand(deleted_sum - (len(core) - degree) * full) == 0

        one_deleted = core[1:]
        recurrence = (
            full
            - e_from_generating_function(one_deleted, degree, marker)
            - core[0]
            * e_from_generating_function(one_deleted, degree - 1, marker)
        )
        assert sp.expand(recurrence) == 0

    for p in range(MIN_FEASIBLE_P, 80):
        assert comb(p, 7) > 0
        assert all(p - degree > 0 for degree in range(1, 7))


def check_witness_persistence(
    residuals_by_total: dict[int, set[tuple[int, ...]]]
) -> None:
    table = low_histograms(34)

    # Exact base: every collision residual from totals 22,...,28 is one of
    # the seven double/single tails.
    for total in range(22, 29):
        expected = {
            (total - 2 * doubles, doubles, 0, 0, 0, 0)
            for doubles in range(1, 8)
        }
        assert residuals_by_total[total] == expected

    # Preserve the actual short or moving pattern under one appended class.
    # Iteration then handles an arbitrary number of appended classes.
    for total in range(17, 29):
        for histogram in table[total]:
            category = classify_low(histogram)
            if category == "S":
                witness = short_pattern(histogram)
                assert witness is not None
                for multiplicity in range(1, 7):
                    assert short_pattern_is_legal(
                        add_class(histogram, multiplicity), witness
                    )
                continue
            if category not in METHOD:
                continue

            anchor_count, needed = METHOD[category]
            ordinary = moving_pattern(histogram, anchor_count, needed, False)
            assert ordinary is not None
            ordinary_candidates = candidate_count(histogram, ordinary, False)
            assert ordinary_candidates >= needed
            for multiplicity in range(1, 7):
                enlarged = add_class(histogram, multiplicity)
                assert (
                    candidate_count(enlarged, ordinary, False)
                    >= ordinary_candidates
                )

            # If the appended singleton is the unique zero, every old class
            # is nonzero and the old ordinary pattern persists verbatim.
            with_new_zero = add_class(histogram, 1)
            assert (
                candidate_count(with_new_zero, ordinary, True)
                >= ordinary_candidates
            )

            # If an old singleton is zero, retain the old zero-aware pattern
            # while appending any nonzero class.
            if histogram[0] > 0:
                zero_aware = moving_pattern(
                    histogram, anchor_count, needed, True
                )
                assert zero_aware is not None
                zero_candidates = candidate_count(histogram, zero_aware, True)
                assert zero_candidates >= needed
                for multiplicity in range(1, 7):
                    enlarged = add_class(histogram, multiplicity)
                    assert (
                        candidate_count(enlarged, zero_aware, True)
                        >= zero_candidates
                    )

    # Removing a part of size at most six from the first total above 28
    # cannot overshoot the finite base interval.
    assert all(22 <= 29 - part <= 28 for part in range(1, 7))


def main() -> None:
    check_feasibility()
    check_deleted_e7_descent()
    residuals = check_histogram_census()
    check_witness_persistence(residuals)
    print("independent seventh-split histogram/role-allocation audit: PASS")
    print("feasible range: p >= 8; p = 7 is formal only")
    print("OPEN for p >= 13: (2^d,1^(p+9-2d)), 1 <= d <= 7")


if __name__ == "__main__":
    main()
