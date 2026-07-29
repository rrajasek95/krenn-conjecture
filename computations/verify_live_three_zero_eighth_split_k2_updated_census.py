#!/usr/bin/env python3
"""Exact audit of the updated h=8, k=2 collision census."""

from __future__ import annotations

from collections import Counter
from itertools import combinations
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


H = 8
P = 10
K = P - H
TOTAL = P + H + 2


def moving_role_witness(profile: tuple[int, ...]):
    """A three-class constant core with at least 2k+1 moving roles."""
    needed = 2 * K + 1
    for fixed_left, fixed_right in combinations(range(len(profile)), 2):
        for take_left in range(1, profile[fixed_left] + 1):
            for take_right in range(1, profile[fixed_right] + 1):
                moving_take = H - take_left - take_right
                if moving_take < 1:
                    continue
                candidates = []
                for moving in range(len(profile)):
                    if moving in (fixed_left, fixed_right):
                        continue
                    if profile[moving] < moving_take:
                        continue
                    takes = {
                        fixed_left: take_left,
                        fixed_right: take_right,
                        moving: moving_take,
                    }
                    if frontier.leaves_singleton(profile, takes):
                        candidates.append(moving)
                if len(candidates) >= needed:
                    return (
                        fixed_left,
                        take_left,
                        fixed_right,
                        take_right,
                        moving_take,
                        tuple(candidates),
                    )
    return None


def antiderivative_closes(profile: tuple[int, ...]) -> bool:
    classes = len(profile)
    excess = TOTAL - classes
    return (
        classes >= H + 1
        and 1 <= excess <= 8
        and frontier.every_value_core_legal(profile, H)
    )


def one_bad_core_closes(profile: tuple[int, ...]) -> bool:
    classes = len(profile)
    excess = TOTAL - classes
    return classes >= H + 1 and profile.count(1) == H and 1 <= excess <= 8


EXPECTED_MOVING_OLD_R = {
    (4, 4, 4, 2, 2, 2, 2),
    (3, 3, 3, 3, 3, 2, 2, 1),
    (3, 3, 3, 2, 2, 2, 2, 1, 1, 1),
    (3, 3, 2, 2, 2, 2, 2, 2, 1, 1),
    (3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1),
}


EXPECTED_ONE_BAD_OLD_R = {
    (3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1),
    (3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1),
    (2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1),
}


EXPECTED_RESIDUALS = (
    (4, 4, 3, 3, 3, 3),
    (3, 3, 3, 3, 3, 3, 2),
    (3, 3, 3, 3, 2, 2, 2, 2),
    (3, 3, 3, 3, 3, 3, 1, 1),
    (3, 3, 3, 3, 3, 2, 1, 1, 1),
    (2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
    (3, 2, 2, 2, 2, 2, 2, 2, 2, 1),
    (3, 3, 3, 3, 2, 2, 1, 1, 1, 1),
    (3, 3, 3, 3, 3, 1, 1, 1, 1, 1),
    (2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1),
    (3, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1),
    (3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1),
    (3, 3, 3, 3, 2, 1, 1, 1, 1, 1, 1),
    (3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1),
    (3, 3, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1),
    (3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1),
)


def ordered(profiles):
    return tuple(sorted(profiles, key=lambda item: (len(item), TOTAL - len(item), item)))


def check_old_and_updated_counts():
    old_counts, old_residual_tuple = frontier.census(H, P)
    assert old_counts == {
        "H": 263,
        "S": 270,
        "C": 22,
        "L": 14,
        "Q": 12,
        "V": 3,
        "R": 42,
        "D": 1,
    }
    old_residuals = set(old_residual_tuple)
    assert len(old_residuals) == 42

    moving = {
        profile for profile in old_residuals if moving_role_witness(profile)
    }
    antiderivative = {
        profile for profile in old_residuals if antiderivative_closes(profile)
    }
    one_bad = {
        profile for profile in old_residuals if one_bad_core_closes(profile)
    }

    assert moving == EXPECTED_MOVING_OLD_R
    assert len(antiderivative) == 18
    assert one_bad == EXPECTED_ONE_BAD_OLD_R
    assert moving.isdisjoint(antiderivative)
    assert moving.isdisjoint(one_bad)
    assert antiderivative.isdisjoint(one_bad)

    residuals = old_residuals - moving - antiderivative - one_bad
    assert len(residuals) == 16
    assert ordered(residuals) == EXPECTED_RESIDUALS

    updated = dict(old_counts)
    updated["R"] -= len(moving | antiderivative | one_bad)
    assert updated["R"] == 16
    assert sum(old_counts.values()) == 627
    assert (
        old_counts["H"]
        + old_counts["S"]
        + old_counts["C"]
        + old_counts["L"]
        + old_counts["Q"]
        + old_counts["V"]
        + len(moving)
        + len(antiderivative)
        + len(one_bad)
        + len(residuals)
        + old_counts["D"]
        == 627
    )


def check_every_moving_witness():
    for profile in EXPECTED_MOVING_OLD_R:
        witness = moving_role_witness(profile)
        assert witness is not None
        left, take_left, right, take_right, moving_take, candidates = witness
        assert left != right
        assert take_left + take_right + moving_take == H
        assert len(candidates) >= 2 * K + 1 == 5
        assert len(set(candidates)) == len(candidates)
        for moving in candidates:
            assert moving not in (left, right)
            assert profile[moving] >= moving_take
            assert frontier.leaves_singleton(
                profile,
                {left: take_left, right: take_right, moving: moving_take},
            )


def check_one_bad_cores_literally():
    for profile in EXPECTED_ONE_BAD_OLD_R:
        singleton_set = {
            index for index, multiplicity in enumerate(profile) if multiplicity == 1
        }
        assert len(singleton_set) == H
        illegal = []
        for core_tuple in combinations(range(len(profile)), H):
            core = set(core_tuple)
            takes = {index: 1 for index in core}
            if not frontier.leaves_singleton(profile, takes):
                illegal.append(core)
        assert illegal == [singleton_set]

        for repeated in set(range(len(profile))) - singleton_set:
            special_nine_core = singleton_set | {repeated}
            assert len(special_nine_core) == H + 1
            for omitted in singleton_set:
                deletion = special_nine_core - {omitted}
                assert frontier.leaves_singleton(
                    profile, {index: 1 for index in deletion}
                )


def check_global_overlap_table():
    collision_profiles = set(frontier.partitions(TOTAL)) - {(1,) * TOTAL}
    assert len(collision_profiles) == 626
    old_category = {
        profile: frontier.classify(profile, H, P) for profile in collision_profiles
    }

    moving = {
        profile for profile in collision_profiles if moving_role_witness(profile)
    }
    antiderivative = {
        profile for profile in collision_profiles if antiderivative_closes(profile)
    }
    one_bad = {
        profile for profile in collision_profiles if one_bad_core_closes(profile)
    }

    expected_rows = {
        "M": {"H": 75, "S": 181, "C": 17, "L": 11, "Q": 7, "V": 2, "R": 5},
        "A": {"H": 3, "S": 18, "C": 2, "L": 4, "Q": 8, "V": 0, "R": 18},
        "O": {"H": 0, "S": 3, "C": 0, "L": 0, "Q": 2, "V": 0, "R": 3},
    }
    route_sets = {"M": moving, "A": antiderivative, "O": one_bad}
    for name, route_set in route_sets.items():
        observed = Counter(old_category[profile] for profile in route_set)
        assert observed.get("D", 0) == 0
        assert {key: observed.get(key, 0) for key in "HSCLQVR"} == expected_rows[name]
        assert len(route_set) == sum(expected_rows[name].values())

    assert len(moving) == 298
    assert len(antiderivative) == 53
    assert len(one_bad) == 8
    assert len(moving & antiderivative) == 29
    assert len(moving & one_bad) == 4
    assert len(antiderivative & one_bad) == 0
    assert len(moving & antiderivative & one_bad) == 0


def check_order_and_handoff():
    assert all(sum(profile) == TOTAL for profile in EXPECTED_RESIDUALS)
    assert all(tuple(sorted(profile, reverse=True)) == profile for profile in EXPECTED_RESIDUALS)
    assert ordered(EXPECTED_RESIDUALS) == EXPECTED_RESIDUALS
    assert EXPECTED_RESIDUALS[0] == (4, 4, 3, 3, 3, 3)
    assert EXPECTED_RESIDUALS[1] == (3, 3, 3, 3, 3, 3, 2)


def main():
    assert (H, P, K, TOTAL) == (8, 10, 2, 20)
    check_old_and_updated_counts()
    check_every_moving_witness()
    check_one_bad_cores_literally()
    check_global_overlap_table()
    check_order_and_handoff()
    print("eighth-split k=2 updated collision census: PASS")
    print("old residual 42; added routes M/A/O close 5/18/3 disjointly")
    print("updated residual count: 16")
    print("first residual: (4,4,3,3,3,3)")
    print("successor after an incremental first-profile closure: (3,3,3,3,3,3,2)")


if __name__ == "__main__":
    main()
