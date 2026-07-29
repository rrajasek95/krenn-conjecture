#!/usr/bin/env python3
"""Exact audit of the updated h=8, k=4 collision census."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations
import math
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier
from verify_live_three_zero_eighth_split_all_order_formal_five_layer_duality import (
    formal_simple_witness,
)


H = 8
P = 12
K = P - H
TOTAL = P + H + 2


EXPECTED_SHADOW_INCREMENT = {
    (3,) + (2,) * 6 + (1,) * 7,
    (3, 3) + (2,) * 4 + (1,) * 8,
    (2,) * 7 + (1,) * 8,
}

EXPECTED_FORMAL_FIVE = {
    (4, 3, 3, 3, 3, 3, 3),
    (3, 3, 3, 3, 2, 2, 2, 2, 2),
    (3, 3, 3, 3, 3, 2, 2, 2, 1),
    (3, 3, 3, 2, 2, 2, 2, 2, 2, 1),
    (3, 3, 3, 3, 2, 2, 2, 2, 1, 1),
    (3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1),
}

EXPECTED_SIX_TRIPLE = {
    (4, 3, 3, 3, 3, 3, 3),
    (3, 3, 3, 3, 3, 3, 3, 1),
}

EXPECTED_LINEAR_PENCIL = {
    (3, 3) + (2,) * 8,
}

EXPECTED_SINGLETON_SQUARE = {
    (3,) + (2,) * 9 + (1,),
}

EXPECTED_ALL_DOUBLE = {
    (2,) * 11,
}

EXPECTED_FIVE_TRIPLE = {
    (3,) * 5 + (2,) * 2 + (1,) * 3,
}

EXPECTED_TEN_DOUBLE_TWO_SINGLETON = {
    (2,) * 10 + (1,) * 2,
}

EXPECTED_TWO_TRIPLE_SEVEN_DOUBLE_TWO_SINGLETON = {
    (3,) * 2 + (2,) * 7 + (1,) * 2,
}

EXPECTED_SATURATED_QUARTIC_MOMENTS = {
    (3,) * 4 + (2,) * 3 + (1,) * 4,
    (3,) * 3 + (2,) * 4 + (1,) * 5,
}

EXPECTED_FIVE_TRIPLE_MONIC_QUADRATIC = {
    (3,) * 5 + (2,) + (1,) * 5,
    (3,) * 5 + (1,) * 7,
}

EXPECTED_THREE_TRIPLE_THREE_DOUBLE_HYPERPLANE = {
    (3,) * 3 + (2,) * 3 + (1,) * 7,
}

EXPECTED_FOUR_TRIPLE_MIXED_LAYER = {
    (3,) * 4 + (2,) * 2 + (1,) * 6,
}

EXPECTED_FOUR_TRIPLE_SINGLE_DOUBLE_PAIR_DROP = {
    (3,) * 4 + (2,) + (1,) * 8,
}

EXPECTED_TWO_TRIPLE_FIVE_DOUBLE_LINEAR_PLANE = {
    (3,) * 2 + (2,) * 5 + (1,) * 6,
}

EXPECTED_NINE_DOUBLE_FOUR_SINGLETON_RAINBOW = {
    (2,) * 9 + (1,) * 4,
}

EXPECTED_RESIDUALS = ()


def ordered(profiles):
    return tuple(
        sorted(
            profiles,
            key=lambda profile: (
                len(profile),
                TOTAL - len(profile),
                profile,
            ),
        )
    )


def moving_value_witness(profile):
    needed = 2 * K + 1
    for left, right in combinations(range(len(profile)), 2):
        for take_left in range(1, profile[left] + 1):
            for take_right in range(1, profile[right] + 1):
                moving_take = H - take_left - take_right
                if moving_take < 1:
                    continue
                candidates = []
                for moving in range(len(profile)):
                    if moving in (left, right):
                        continue
                    if profile[moving] < moving_take:
                        continue
                    takes = {
                        left: take_left,
                        right: take_right,
                        moving: moving_take,
                    }
                    if frontier.leaves_singleton(profile, takes):
                        candidates.append(moving)
                if len(candidates) >= needed:
                    return (
                        left,
                        take_left,
                        right,
                        take_right,
                        moving_take,
                        tuple(candidates),
                    )
    return None


def consecutive_transfer_witness(profile):
    for class_a, class_b, class_c in permutations(range(len(profile)), 3):
        for take_a in range(1, H - 1):
            for take_b in range(1, H - take_a):
                take_c = H - take_a - take_b
                if take_a + K > profile[class_a]:
                    continue
                if take_b > profile[class_b] or take_b - K < 1:
                    continue
                if take_c > profile[class_c]:
                    continue
                cores = tuple(
                    {
                        class_a: take_a + transfer,
                        class_b: take_b - transfer,
                        class_c: take_c,
                    }
                    for transfer in range(K + 1)
                )
                if all(
                    frontier.leaves_singleton(profile, takes)
                    for takes in cores
                ):
                    return (
                        class_a,
                        class_b,
                        class_c,
                        take_a,
                        take_b,
                        take_c,
                        cores,
                    )
    return None


def legal_antiderivative_closes(profile):
    classes = len(profile)
    excess = TOTAL - classes
    return (
        classes >= H + 1
        and 1 <= excess <= 8
        and frontier.every_value_core_legal(profile, H)
    )


def double_guard_closes(profile):
    classes = len(profile)
    excess = TOTAL - classes
    return (
        classes >= H + 1
        and 1 <= excess <= 8
        and profile.count(2) >= 1
    )


def unique_bad_core_closes(profile):
    classes = len(profile)
    excess = TOTAL - classes
    singletons = profile.count(1)
    high = sum(multiplicity >= 3 for multiplicity in profile)
    needed = H - singletons
    return (
        classes >= H + 1
        and 1 <= excess <= 8
        and 0 <= needed <= high
        and math.comb(high, needed) == 1
    )


def check_frozen_slice_and_routes() -> None:
    counts, residual_tuple = frontier.census(H, P)
    assert counts == {
        "H": 480,
        "S": 411,
        "C": 28,
        "L": 21,
        "R": 46,
        "Q": 15,
        "D": 1,
    }
    residuals = set(residual_tuple)
    assert len(residuals) == 46

    routes = {
        "M": {
            profile
            for profile in residuals
            if moving_value_witness(profile) is not None
        },
        "A": {
            profile for profile in residuals if legal_antiderivative_closes(profile)
        },
        "B": {
            profile for profile in residuals if double_guard_closes(profile)
        },
        "U": {
            profile for profile in residuals if unique_bad_core_closes(profile)
        },
        "T": {
            profile
            for profile in residuals
            if consecutive_transfer_witness(profile) is not None
        },
        "J": {
            profile
            for profile in residuals
            if formal_simple_witness(profile) is not None
        },
        "F4": {
            profile for profile in residuals if profile.count(3) >= 6
        },
        "X4": EXPECTED_LINEAR_PENCIL & residuals,
        "N4": EXPECTED_SINGLETON_SQUARE & residuals,
        "A4": EXPECTED_ALL_DOUBLE & residuals,
        "P4": EXPECTED_FIVE_TRIPLE & residuals,
        "C4": EXPECTED_TEN_DOUBLE_TWO_SINGLETON & residuals,
        "S4": EXPECTED_TWO_TRIPLE_SEVEN_DOUBLE_TWO_SINGLETON & residuals,
        "W4": EXPECTED_SATURATED_QUARTIC_MOMENTS & residuals,
        "G4": EXPECTED_FIVE_TRIPLE_MONIC_QUADRATIC & residuals,
        "H4": EXPECTED_THREE_TRIPLE_THREE_DOUBLE_HYPERPLANE
        & residuals,
        "M4": EXPECTED_FOUR_TRIPLE_MIXED_LAYER & residuals,
        "E4": EXPECTED_FOUR_TRIPLE_SINGLE_DOUBLE_PAIR_DROP
        & residuals,
        "L4": EXPECTED_TWO_TRIPLE_FIVE_DOUBLE_LINEAR_PLANE
        & residuals,
        "RB4": EXPECTED_NINE_DOUBLE_FOUR_SINGLETON_RAINBOW
        & residuals,
    }

    assert not routes["M"]
    assert len(routes["A"]) == 21
    assert len(routes["B"]) == 20
    assert len(routes["A"] & routes["B"]) == 17
    assert routes["B"] - routes["A"] == EXPECTED_SHADOW_INCREMENT
    assert routes["U"] == EXPECTED_SHADOW_INCREMENT
    assert not routes["T"]
    assert routes["J"] == EXPECTED_FORMAL_FIVE
    assert routes["F4"] == EXPECTED_SIX_TRIPLE
    assert routes["J"] & routes["F4"] == {
        (4, 3, 3, 3, 3, 3, 3)
    }
    assert routes["X4"] == EXPECTED_LINEAR_PENCIL
    assert routes["N4"] == EXPECTED_SINGLETON_SQUARE
    assert routes["A4"] == EXPECTED_ALL_DOUBLE
    assert routes["P4"] == EXPECTED_FIVE_TRIPLE
    assert routes["C4"] == EXPECTED_TEN_DOUBLE_TWO_SINGLETON
    assert routes["S4"] == EXPECTED_TWO_TRIPLE_SEVEN_DOUBLE_TWO_SINGLETON
    assert routes["W4"] == EXPECTED_SATURATED_QUARTIC_MOMENTS
    assert routes["G4"] == EXPECTED_FIVE_TRIPLE_MONIC_QUADRATIC
    assert (
        routes["H4"]
        == EXPECTED_THREE_TRIPLE_THREE_DOUBLE_HYPERPLANE
    )
    assert routes["M4"] == EXPECTED_FOUR_TRIPLE_MIXED_LAYER
    assert (
        routes["E4"]
        == EXPECTED_FOUR_TRIPLE_SINGLE_DOUBLE_PAIR_DROP
    )
    assert (
        routes["L4"]
        == EXPECTED_TWO_TRIPLE_FIVE_DOUBLE_LINEAR_PLANE
    )
    assert (
        routes["RB4"]
        == EXPECTED_NINE_DOUBLE_FOUR_SINGLETON_RAINBOW
    )

    order = (
        "M",
        "A",
        "B",
        "U",
        "T",
        "J",
        "F4",
        "X4",
        "N4",
        "A4",
        "P4",
        "C4",
        "S4",
        "W4",
        "G4",
        "H4",
        "M4",
        "E4",
        "L4",
        "RB4",
    )
    expected_increments = {
        "M": 0,
        "A": 21,
        "B": 3,
        "U": 0,
        "T": 0,
        "J": 6,
        "F4": 1,
        "X4": 1,
        "N4": 1,
        "A4": 1,
        "P4": 1,
        "C4": 1,
        "S4": 1,
        "W4": 2,
        "G4": 2,
        "H4": 1,
        "M4": 1,
        "E4": 1,
        "L4": 1,
        "RB4": 1,
    }
    closed = set()
    for name in order:
        increment = routes[name] - closed
        assert len(increment) == expected_increments[name]
        closed |= routes[name]

    assert len(closed) == 46
    remaining = residuals - closed
    assert ordered(remaining) == EXPECTED_RESIDUALS
    assert not remaining

    sequential_total = (
        counts["H"]
        + counts["S"]
        + counts["C"]
        + counts["L"]
        + counts["Q"]
        + counts.get("V", 0)
        + sum(expected_increments.values())
        + len(remaining)
        + counts["D"]
    )
    assert sequential_total == 1002


def check_global_double_guard_scope() -> None:
    all_profiles = set(frontier.partitions(TOTAL))
    assert len(all_profiles) == 1002
    collision_profiles = all_profiles - {(1,) * TOTAL}
    guarded = {
        profile for profile in collision_profiles if double_guard_closes(profile)
    }
    assert len(guarded) == 45
    categories = Counter(
        frontier.classify(profile, H, P) for profile in guarded
    )
    assert categories == {
        "H": 1,
        "S": 11,
        "C": 2,
        "L": 3,
        "Q": 8,
        "R": 20,
    }
    for profile in guarded:
        assert len(profile) >= 9
        assert 1 <= TOTAL - len(profile) <= 8
        assert profile.count(2) >= 1


def check_every_local_increment() -> None:
    for profile in EXPECTED_FORMAL_FIVE:
        witness = formal_simple_witness(profile)
        assert witness is not None
        chosen, complement = witness
        assert len(chosen) == 5
        assert sum(complement) == K + H == 12
        classes = len(complement)
        simple = complement.count(1)
        assert classes < 5 or simple > 2 * classes - 10

    assert EXPECTED_SIX_TRIPLE - EXPECTED_FORMAL_FIVE == {
        (3, 3, 3, 3, 3, 3, 3, 1)
    }
    for profile in EXPECTED_SIX_TRIPLE:
        triples = tuple(
            index
            for index, multiplicity in enumerate(profile)
            if multiplicity == 3
        )
        assert len(triples) >= 6
        for chosen in combinations(triples, 3):
            for partial in chosen:
                takes = {
                    index: (2 if index == partial else 3)
                    for index in chosen
                }
                assert frontier.leaves_singleton(profile, takes)

    target = next(iter(EXPECTED_LINEAR_PENCIL))
    doubles = tuple(
        index
        for index, multiplicity in enumerate(target)
        if multiplicity == 2
    )
    assert len(doubles) == 8
    core_count = 0
    for chosen in combinations(doubles, 5):
        for partial in combinations(chosen, 2):
            takes = {
                index: (1 if index in partial else 2)
                for index in chosen
            }
            assert frontier.leaves_singleton(target, takes)
            core_count += 1
    assert core_count == math.comb(8, 5) * math.comb(5, 2) == 560

    singleton_square = next(iter(EXPECTED_SINGLETON_SQUARE))
    square_doubles = tuple(
        index
        for index, multiplicity in enumerate(singleton_square)
        if multiplicity == 2
    )
    assert len(square_doubles) == 9
    square_core_count = 0
    for chosen in combinations(square_doubles, 5):
        for partial in combinations(chosen, 2):
            takes = {
                index: (1 if index in partial else 2)
                for index in chosen
            }
            assert frontier.leaves_singleton(singleton_square, takes)
            square_core_count += 1
    assert square_core_count == math.comb(9, 5) * math.comb(5, 2) == 1260

    five_triple = next(iter(EXPECTED_FIVE_TRIPLE))
    five_triples = tuple(
        index
        for index, multiplicity in enumerate(five_triple)
        if multiplicity == 3
    )
    two_doubles = tuple(
        index
        for index, multiplicity in enumerate(five_triple)
        if multiplicity == 2
    )
    robin_core_count = 0
    for selected_triples in combinations(five_triples, 3):
        chosen = two_doubles + selected_triples
        assert len(chosen) == 5
        for partial in combinations(chosen, 2):
            takes = {
                index: (1 if index in partial else 2)
                for index in chosen
            }
            assert frontier.leaves_singleton(five_triple, takes)
            robin_core_count += 1
    assert robin_core_count == math.comb(5, 3) * math.comb(5, 2) == 100

    for local_route, double_count, expected_core_count in (
        (EXPECTED_TEN_DOUBLE_TWO_SINGLETON, 10, 2520),
        (EXPECTED_TWO_TRIPLE_SEVEN_DOUBLE_TWO_SINGLETON, 7, 210),
    ):
        profile = next(iter(local_route))
        doubles = tuple(
            index
            for index, multiplicity in enumerate(profile)
            if multiplicity == 2
        )
        assert len(doubles) == double_count
        local_core_count = 0
        for chosen in combinations(doubles, 5):
            for partial in combinations(chosen, 2):
                takes = {
                    index: (1 if index in partial else 2)
                    for index in chosen
                }
                assert frontier.leaves_singleton(profile, takes)
                local_core_count += 1
        assert local_core_count == expected_core_count

    moment_core_count = 0
    for profile in EXPECTED_SATURATED_QUARTIC_MOMENTS:
        triples = tuple(
            index
            for index, multiplicity in enumerate(profile)
            if multiplicity == 3
        )
        doubles = tuple(
            index
            for index, multiplicity in enumerate(profile)
            if multiplicity == 2
        )
        selected_triple_count = 5 - len(doubles)
        for selected_triples in combinations(triples, selected_triple_count):
            chosen = doubles + selected_triples
            assert len(chosen) == 5
            for partial in combinations(chosen, 2):
                takes = {
                    index: (1 if index in partial else 2)
                    for index in chosen
                }
                assert frontier.leaves_singleton(profile, takes)
                moment_core_count += 1
    assert moment_core_count == 90

    monic_quadratic_core_count = 0
    for profile in EXPECTED_FIVE_TRIPLE_MONIC_QUADRATIC:
        triples = tuple(
            index
            for index, multiplicity in enumerate(profile)
            if multiplicity == 3
        )
        assert len(triples) == 5
        for selected_triples in combinations(triples, 3):
            for partial in selected_triples:
                takes = {
                    index: (2 if index == partial else 3)
                    for index in selected_triples
                }
                assert sum(takes.values()) == H
                assert frontier.leaves_singleton(profile, takes)
                monic_quadratic_core_count += 1
    assert monic_quadratic_core_count == 2 * math.comb(5, 3) * 3 == 60

    hyperplane_profile = next(
        iter(EXPECTED_THREE_TRIPLE_THREE_DOUBLE_HYPERPLANE)
    )
    hyperplane_doubles = tuple(
        index
        for index, multiplicity in enumerate(hyperplane_profile)
        if multiplicity == 2
    )
    hyperplane_singletons = tuple(
        index
        for index, multiplicity in enumerate(hyperplane_profile)
        if multiplicity == 1
    )
    assert len(hyperplane_doubles) == 3
    assert len(hyperplane_singletons) == 7
    hyperplane_core_count = 0
    for formal_double in hyperplane_doubles:
        formal_roles = (formal_double,) + hyperplane_singletons
        for dropped_role in formal_roles:
            takes = {index: 1 for index in hyperplane_singletons}
            takes[formal_double] = 2
            takes[dropped_role] -= 1
            assert sum(takes.values()) == H
            assert frontier.leaves_singleton(hyperplane_profile, takes)
            hyperplane_core_count += 1
    assert hyperplane_core_count == 3 * 8 == 24

    mixed_profile = next(iter(EXPECTED_FOUR_TRIPLE_MIXED_LAYER))
    mixed_doubles = tuple(
        index
        for index, multiplicity in enumerate(mixed_profile)
        if multiplicity == 2
    )
    mixed_singletons = tuple(
        index
        for index, multiplicity in enumerate(mixed_profile)
        if multiplicity == 1
    )
    assert len(mixed_doubles) == 2
    assert len(mixed_singletons) == 6
    formal_roles = {
        **{index: 2 for index in mixed_doubles},
        **{index: 1 for index in mixed_singletons},
    }
    mixed_core_count = 0
    for lowered_pair in combinations(formal_roles, 2):
        takes = {
            index: role - (1 if index in lowered_pair else 0)
            for index, role in formal_roles.items()
        }
        takes = {index: role for index, role in takes.items() if role}
        assert sum(takes.values()) == H
        assert frontier.leaves_singleton(mixed_profile, takes)
        mixed_core_count += 1
    assert mixed_core_count == math.comb(8, 2) == 28

    pair_drop_profile = next(
        iter(EXPECTED_FOUR_TRIPLE_SINGLE_DOUBLE_PAIR_DROP)
    )
    pair_drop_doubles = tuple(
        index
        for index, multiplicity in enumerate(pair_drop_profile)
        if multiplicity == 2
    )
    pair_drop_singletons = tuple(
        index
        for index, multiplicity in enumerate(pair_drop_profile)
        if multiplicity == 1
    )
    assert len(pair_drop_doubles) == 1
    assert len(pair_drop_singletons) == 8
    formal_roles = {
        pair_drop_doubles[0]: 2,
        **{index: 1 for index in pair_drop_singletons},
    }
    pair_drop_core_count = 0
    for lowered_pair in combinations(formal_roles, 2):
        takes = {
            index: role - (1 if index in lowered_pair else 0)
            for index, role in formal_roles.items()
        }
        takes = {index: role for index, role in takes.items() if role}
        assert sum(takes.values()) == H
        assert frontier.leaves_singleton(pair_drop_profile, takes)
        pair_drop_core_count += 1
    assert pair_drop_core_count == math.comb(9, 2) == 36

    linear_plane_profile = next(
        iter(EXPECTED_TWO_TRIPLE_FIVE_DOUBLE_LINEAR_PLANE)
    )
    linear_plane_doubles = tuple(
        index
        for index, multiplicity in enumerate(linear_plane_profile)
        if multiplicity == 2
    )
    linear_plane_singletons = tuple(
        index
        for index, multiplicity in enumerate(linear_plane_profile)
        if multiplicity == 1
    )
    assert len(linear_plane_doubles) == 5
    assert len(linear_plane_singletons) == 6
    linear_plane_core_count = 0
    for selected_doubles in combinations(linear_plane_doubles, 2):
        formal_roles = {
            **{index: 2 for index in selected_doubles},
            **{index: 1 for index in linear_plane_singletons},
        }
        assert sum(formal_roles.values()) == 10
        for lowered_pair in combinations(formal_roles, 2):
            takes = {
                index: role - (1 if index in lowered_pair else 0)
                for index, role in formal_roles.items()
            }
            takes = {
                index: role for index, role in takes.items() if role
            }
            assert sum(takes.values()) == H
            assert frontier.leaves_singleton(
                linear_plane_profile,
                takes,
            )
            linear_plane_core_count += 1
    assert (
        linear_plane_core_count
        == math.comb(5, 2) * math.comb(8, 2)
        == 280
    )

    rainbow_profile = next(
        iter(EXPECTED_NINE_DOUBLE_FOUR_SINGLETON_RAINBOW)
    )
    rainbow_doubles = tuple(
        index
        for index, multiplicity in enumerate(rainbow_profile)
        if multiplicity == 2
    )
    rainbow_singletons = tuple(
        index
        for index, multiplicity in enumerate(rainbow_profile)
        if multiplicity == 1
    )
    assert len(rainbow_doubles) == 9
    assert len(rainbow_singletons) == 4
    rainbow_core_count = 0
    for selected_doubles in combinations(rainbow_doubles, 3):
        formal_roles = {
            **{index: 2 for index in selected_doubles},
            **{index: 1 for index in rainbow_singletons},
        }
        assert sum(formal_roles.values()) == 10
        for lowered_pair in combinations(formal_roles, 2):
            takes = {
                index: role - (1 if index in lowered_pair else 0)
                for index, role in formal_roles.items()
            }
            takes = {
                index: role for index, role in takes.items() if role
            }
            assert sum(takes.values()) == H
            assert frontier.leaves_singleton(rainbow_profile, takes)
            rainbow_core_count += 1
    assert (
        rainbow_core_count
        == math.comb(9, 3) * math.comb(7, 2)
        == 1764
    )


def check_ordered_residuals() -> None:
    assert EXPECTED_RESIDUALS == ()
    assert ordered(EXPECTED_RESIDUALS) == EXPECTED_RESIDUALS


def main() -> None:
    check_frozen_slice_and_routes()
    check_global_double_guard_scope()
    check_every_local_increment()
    check_ordered_residuals()
    print("PASS: updated exact h=8, k=4 collision census")
    print("frozen residuals 46; legal/shadow exchange closes 24")
    print("formal-five and fourteen fourth-order local routes close 22")
    print("exact residual frontier: empty")
    print("all 46 frozen residual profiles are closed")


if __name__ == "__main__":
    main()
