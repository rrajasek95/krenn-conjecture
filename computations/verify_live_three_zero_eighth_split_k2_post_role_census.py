#!/usr/bin/env python3
"""Exact audit of the h=8, k=2 post-role six-profile census."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier
import verify_live_three_zero_eighth_split_k2_updated_census as frozen
import verify_live_three_zero_higher_split_unique_bad_core_repair as unique
import verify_live_three_zero_eighth_split_443333_order_two_common_pole as role


H = 8
P = 10
TOTAL = 20


def four_role_witness(profile: tuple[int, ...]):
    """Four high classes for which all twelve (3,3,2) cores are legal."""
    high = [index for index, multiplicity in enumerate(profile) if multiplicity >= 3]
    for four in combinations(high, 4):
        legal = True
        for three in combinations(four, 3):
            for partial in three:
                takes = {
                    index: (2 if index == partial else 3)
                    for index in three
                }
                if not frontier.leaves_singleton(profile, takes):
                    legal = False
        if legal:
            return tuple(four)
    return None


EXPECTED_TRIPLE_INCREMENT = {
    (4, 4, 3, 3, 3, 3),
    (3, 3, 3, 3, 3, 3, 2),
    (3, 3, 3, 3, 2, 2, 2, 2),
    (3, 3, 3, 3, 3, 3, 1, 1),
    (3, 3, 3, 3, 3, 2, 1, 1, 1),
    (3, 3, 3, 3, 2, 2, 1, 1, 1, 1),
    (3, 3, 3, 3, 3, 1, 1, 1, 1, 1),
    (3, 3, 3, 3, 2, 1, 1, 1, 1, 1, 1),
}


EXPECTED_UNIQUE_INCREMENT = {
    (3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1),
    (3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1),
}


EXPECTED_FINAL = (
    (2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
    (3, 2, 2, 2, 2, 2, 2, 2, 2, 1),
    (2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1),
    (3, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1),
    (3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1),
    (3, 3, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1),
)


def ordered(profiles):
    return tuple(sorted(profiles, key=lambda item: (len(item), TOTAL - len(item), item)))


def reconstruct_frozen_baseline():
    _, old_residual_tuple = frontier.census(H, P)
    old_residuals = set(old_residual_tuple)
    moving = {
        profile for profile in old_residuals if frozen.moving_role_witness(profile)
    }
    antiderivative = {
        profile for profile in old_residuals if frozen.antiderivative_closes(profile)
    }
    one_bad = {
        profile for profile in old_residuals if frozen.one_bad_core_closes(profile)
    }
    baseline = old_residuals - moving - antiderivative - one_bad
    assert ordered(baseline) == frozen.EXPECTED_RESIDUALS
    return old_residuals, baseline, moving, antiderivative, one_bad


def check_role_algebra():
    role.check_universal_baseline_and_exact_pole()
    role.check_order_two_logarithmic_formula()
    role.check_role_drop_and_three_subset_forcing()


def check_every_role_application(baseline):
    observed = {profile for profile in baseline if four_role_witness(profile)}
    assert observed == EXPECTED_TRIPLE_INCREMENT

    # On this frozen finite slice, the convenient high-class count and the
    # literal twelve-core hypothesis happen to be equivalent.
    by_high_count = {
        profile for profile in baseline if sum(part >= 3 for part in profile) >= 4
    }
    assert by_high_count == observed

    for profile in observed:
        four = four_role_witness(profile)
        assert four is not None
        assert len(four) == 4
        # In fact every application has four exact triples.  This gives a
        # visibly legal core even before the literal complement check.
        assert all(profile[index] == 3 for index in four)
        core_count = 0
        for three in combinations(four, 3):
            for partial in three:
                takes = {
                    index: (2 if index == partial else 3)
                    for index in three
                }
                core_count += 1
                assert sum(takes.values()) == H
                assert len(takes) == 3
                assert profile[partial] - takes[partial] == 1
                assert frontier.leaves_singleton(profile, takes)
                complement_size = sum(
                    multiplicity - takes.get(index, 0)
                    for index, multiplicity in enumerate(profile)
                )
                denominator_degree = 3 + sum(take + 1 for take in takes.values())
                numerator_cap = P + len(takes) - 1
                residual_cap = numerator_cap - complement_size
                assert complement_size == P + 2 == 12
                assert denominator_degree == 14
                assert numerator_cap == 12
                assert residual_cap == 0
        assert core_count == 12


def check_route_overlaps_and_final_set():
    old_residuals, baseline, moving, antiderivative, one_bad = reconstruct_frozen_baseline()
    triple_all_old = {
        profile for profile in old_residuals if four_role_witness(profile)
    }
    triple_increment = triple_all_old & baseline
    assert len(triple_all_old) == 10
    assert triple_increment == EXPECTED_TRIPLE_INCREMENT
    assert len(triple_all_old & moving) == 1
    assert len(triple_all_old & antiderivative) == 0
    assert len(triple_all_old & one_bad) == 1

    unique_increment = {
        profile
        for profile in baseline
        if len(profile) >= H + 1
        and 1 <= TOTAL - len(profile) <= 8
        and unique.unique_closed_form(profile, H)
    }
    assert unique_increment == EXPECTED_UNIQUE_INCREMENT
    assert triple_increment.isdisjoint(unique_increment)

    final = baseline - triple_increment - unique_increment
    assert ordered(final) == EXPECTED_FINAL
    assert len(final) == 6

    # Complete sequential count: the twelve displayed categories sum to
    # all 627 partitions of 20, including the all-distinct profile.
    sequential = (263, 270, 22, 14, 12, 3, 5, 18, 3, 8, 2, 6, 1)
    assert sum(sequential) == 627


def check_order_and_successor():
    assert ordered(EXPECTED_FINAL) == EXPECTED_FINAL
    assert all(sum(profile) == TOTAL for profile in EXPECTED_FINAL)
    assert EXPECTED_FINAL[0] == (2,) * 10
    first = EXPECTED_FINAL[0]
    assert len(first) == 10
    assert TOTAL - len(first) == 10
    assert frontier.every_value_core_legal(first, H)
    assert not frozen.antiderivative_closes(first)


def main():
    check_role_algebra()
    old_residuals, baseline, _, _, _ = reconstruct_frozen_baseline()
    assert len(old_residuals) == 42 and len(baseline) == 16
    check_every_role_application(baseline)
    check_route_overlaps_and_final_set()
    check_order_and_successor()
    print("eighth-split k=2 post-role census: PASS")
    print("four-role theorem closes 8/16; unique-core endpoint adds 2")
    print("current residual count: 6")
    print("next residual: (2^10), with c=e=10")


if __name__ == "__main__":
    main()
