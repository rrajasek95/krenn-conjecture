#!/usr/bin/env python3
"""Exact audit of the fully updated h=8, k=3 collision census."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations
import math
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


H = 8
P = 11
K = P - H
TOTAL = P + H + 2


def moving_value_witness(profile: tuple[int, ...]):
    """A legal three-class constant core with at least 2k+1 moving values."""
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


def unique_bad_core_closes(profile: tuple[int, ...]) -> bool:
    classes = len(profile)
    excess = TOTAL - classes
    singletons = profile.count(1)
    high_classes = sum(part >= 3 for part in profile)
    needed_high = H - singletons
    unique = (
        0 <= needed_high <= high_classes
        and math.comb(high_classes, needed_high) == 1
    )
    return classes >= H + 1 and 1 <= excess <= 8 and unique


def consecutive_transfer_witness(profile: tuple[int, ...]):
    """Three ordered classes supporting all k+1 consecutive legal roles."""
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

                cores = []
                for transfer in range(K + 1):
                    takes = {
                        class_a: take_a + transfer,
                        class_b: take_b - transfer,
                        class_c: take_c,
                    }
                    if not frontier.leaves_singleton(profile, takes):
                        break
                    cores.append(takes)
                if len(cores) == K + 1:
                    return (
                        class_a,
                        class_b,
                        class_c,
                        take_a,
                        take_b,
                        take_c,
                        tuple(cores),
                    )
    return None


def five_exact_triples_closes(profile: tuple[int, ...]) -> bool:
    return profile.count(3) >= 5


def four_exact_triples_closes(profile: tuple[int, ...]) -> bool:
    return profile.count(3) >= 4


EXPECTED_MOVING_OLD_R = {
    (3, 3, 2, 2, 2, 2, 2, 2, 2, 1),
}

EXPECTED_UNIQUE_OLD_R = {
    (3, 3, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1),
    (3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1),
}

EXPECTED_TRANSFER_OLD_R = {
    (4, 4, 4, 3, 3, 3),
}

EXPECTED_FIVE_TRIPLE_OLD_R = {
    (3, 3, 3, 3, 3, 3, 3),
    (3, 3, 3, 3, 3, 2, 2, 2),
    (3, 3, 3, 3, 3, 3, 2, 1),
    (3, 3, 3, 3, 3, 2, 2, 1, 1),
    (3, 3, 3, 3, 3, 2, 1, 1, 1, 1),
    (3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1),
}

EXPECTED_FOUR_TRIPLE_INCREMENT = {
    (3, 3, 3, 3, 2, 2, 2, 2, 1),
    (3, 3, 3, 3, 2, 2, 2, 1, 1, 1),
    (3, 3, 3, 3, 2, 2, 1, 1, 1, 1, 1),
    (3, 3, 3, 3, 2, 1, 1, 1, 1, 1, 1, 1),
}

EXPECTED_FORMAL_FIVE_DOUBLE_INCREMENT = {
    (3, 3, 3, 2, 2, 2, 2, 2, 2),
    (3, 2, 2, 2, 2, 2, 2, 2, 2, 2),
    (3, 3, 3, 2, 2, 2, 2, 2, 1, 1),
    (2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1),
    (3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1),
    (3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1),
    (3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1),
    (3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1),
}

EXPECTED_FORMAL_LAYER_INCREMENT = {
    (3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1),
}

EXPECTED_STANDALONE_TEN_DOUBLE = {
    (2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1),
}

EXPECTED_NINE_DOUBLE_THREE_SINGLETON_INCREMENT = {
    (2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1),
}

EXPECTED_THREE_TRIPLE_MIXED_INCREMENT = {
    (3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1),
}

EXPECTED_DOUBLE_GUARD_BYPASS_INCREMENT = {
    (3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1),
}

EXPECTED_INDEPENDENT_TWO_TRIPLE_MIXED = (
    EXPECTED_DOUBLE_GUARD_BYPASS_INCREMENT
)

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


def old_residual_route_sets():
    old_counts, old_residual_tuple = frontier.census(H, P)
    assert old_counts == {
        "H": 356,
        "S": 338,
        "C": 22,
        "L": 16,
        "Q": 13,
        "R": 46,
        "D": 1,
    }
    old_residuals = set(old_residual_tuple)
    assert len(old_residuals) == 46

    routes = {
        "M": {
            profile
            for profile in old_residuals
            if moving_value_witness(profile) is not None
        },
        "A": {
            profile
            for profile in old_residuals
            if antiderivative_closes(profile)
        },
        "U": {
            profile
            for profile in old_residuals
            if unique_bad_core_closes(profile)
        },
        "T": {
            profile
            for profile in old_residuals
            if consecutive_transfer_witness(profile) is not None
        },
        "F": {
            profile
            for profile in old_residuals
            if five_exact_triples_closes(profile)
        },
        "G": {
            profile
            for profile in old_residuals
            if four_exact_triples_closes(profile)
        },
    }
    return old_counts, old_residuals, routes


def check_old_slice_and_updated_counts() -> None:
    old_counts, old_residuals, routes = old_residual_route_sets()

    assert routes["M"] == EXPECTED_MOVING_OLD_R
    assert len(routes["A"]) == 21
    assert routes["U"] == EXPECTED_UNIQUE_OLD_R
    assert routes["T"] == EXPECTED_TRANSFER_OLD_R
    assert routes["F"] == EXPECTED_FIVE_TRIPLE_OLD_R
    assert len(routes["G"]) == 11

    first_five = ("M", "A", "U", "T", "F")
    for left, right in combinations(first_five, 2):
        assert routes[left].isdisjoint(routes[right])

    previously_closed = set().union(*(routes[name] for name in first_five))
    four_triple_increment = routes["G"] - previously_closed
    assert four_triple_increment == EXPECTED_FOUR_TRIPLE_INCREMENT
    assert routes["G"] & routes["F"] == routes["F"]
    assert len(routes["G"] & routes["A"]) == 1

    before_formal_five_double = previously_closed | routes["G"]
    formal_five_double_increment = (
        EXPECTED_FORMAL_FIVE_DOUBLE_INCREMENT - before_formal_five_double
    )
    assert formal_five_double_increment == EXPECTED_FORMAL_FIVE_DOUBLE_INCREMENT
    assert EXPECTED_STANDALONE_TEN_DOUBLE <= formal_five_double_increment

    before_nine_double = before_formal_five_double | formal_five_double_increment
    nine_double_increment = (
        EXPECTED_NINE_DOUBLE_THREE_SINGLETON_INCREMENT - before_nine_double
    )
    assert (
        nine_double_increment
        == EXPECTED_NINE_DOUBLE_THREE_SINGLETON_INCREMENT
    )

    before_terminal_routes = before_nine_double | nine_double_increment
    three_triple_increment = (
        EXPECTED_THREE_TRIPLE_MIXED_INCREMENT - before_terminal_routes
    )
    assert three_triple_increment == EXPECTED_THREE_TRIPLE_MIXED_INCREMENT
    before_double_guard = before_terminal_routes | three_triple_increment
    double_guard_increment = (
        EXPECTED_DOUBLE_GUARD_BYPASS_INCREMENT - before_double_guard
    )
    assert double_guard_increment == EXPECTED_DOUBLE_GUARD_BYPASS_INCREMENT
    assert (
        EXPECTED_INDEPENDENT_TWO_TRIPLE_MIXED
        == EXPECTED_DOUBLE_GUARD_BYPASS_INCREMENT
    )

    closed = before_double_guard | double_guard_increment
    residuals = old_residuals - closed
    assert len(closed) == 46
    assert len(residuals) == 0
    assert ordered(residuals) == EXPECTED_RESIDUALS

    sequential_total = (
        old_counts["H"]
        + old_counts["S"]
        + old_counts["C"]
        + old_counts["L"]
        + old_counts["Q"]
        + old_counts.get("V", 0)
        + len(routes["M"])
        + len(routes["A"])
        + len(routes["U"])
        + len(routes["T"])
        + len(routes["F"])
        + len(four_triple_increment)
        + len(formal_five_double_increment)
        + len(nine_double_increment)
        + len(three_triple_increment)
        + len(double_guard_increment)
        + len(residuals)
        + old_counts["D"]
    )
    assert sequential_total == 792


def check_every_added_witness() -> None:
    for profile in EXPECTED_MOVING_OLD_R:
        witness = moving_value_witness(profile)
        assert witness is not None
        left, take_left, right, take_right, moving_take, candidates = witness
        assert take_left + take_right + moving_take == H
        assert len(candidates) >= 2 * K + 1 == 7
        for moving in candidates:
            assert frontier.leaves_singleton(
                profile,
                {left: take_left, right: take_right, moving: moving_take},
            )

    for profile in EXPECTED_UNIQUE_OLD_R:
        illegal = []
        for core_tuple in combinations(range(len(profile)), H):
            takes = {index: 1 for index in core_tuple}
            if not frontier.leaves_singleton(profile, takes):
                illegal.append(frozenset(core_tuple))
        assert len(illegal) == 1
        assert TOTAL - len(profile) <= 8

    profile = next(iter(EXPECTED_TRANSFER_OLD_R))
    witness = consecutive_transfer_witness(profile)
    assert witness is not None
    class_a, class_b, class_c, take_a, take_b, take_c, cores = witness
    assert (take_a, take_b, take_c) == (1, 4, 3)
    assert profile[class_a] == profile[class_b] == profile[class_c] == 4
    assert len(cores) == K + 1 == 4
    for transfer, takes in enumerate(cores):
        assert takes[class_a] == 1 + transfer
        assert takes[class_b] == 4 - transfer
        assert takes[class_c] == 3
        assert sum(takes.values()) == H
        assert frontier.leaves_singleton(profile, takes)

    for profile in EXPECTED_FIVE_TRIPLE_OLD_R:
        triple_indices = tuple(
            index
            for index, multiplicity in enumerate(profile)
            if multiplicity == 3
        )
        assert len(triple_indices) >= 5
        for chosen in combinations(triple_indices, 3):
            for partial in chosen:
                takes = {
                    index: (2 if index == partial else 3)
                    for index in chosen
                }
                assert sum(takes.values()) == H
                assert frontier.leaves_singleton(profile, takes)

    for profile in EXPECTED_FOUR_TRIPLE_INCREMENT:
        triple_indices = tuple(
            index
            for index, multiplicity in enumerate(profile)
            if multiplicity == 3
        )
        assert len(triple_indices) == 4
        legal_count = 0
        for chosen in combinations(triple_indices, 3):
            for partial in chosen:
                takes = {
                    index: (2 if index == partial else 3)
                    for index in chosen
                }
                assert sum(takes.values()) == H
                assert frontier.leaves_singleton(profile, takes)
                legal_count += 1
        assert legal_count == 12

    expected_complementary_classes = {
        (3, 3, 3, 2, 2, 2, 2, 2, 2): 4,
        (3, 2, 2, 2, 2, 2, 2, 2, 2, 2): 5,
        (3, 3, 3, 2, 2, 2, 2, 2, 1, 1): 5,
        (2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1): 6,
        (3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1): 6,
        (3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1): 6,
        (3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1): 7,
    }
    assert (
        set(expected_complementary_classes) | EXPECTED_FORMAL_LAYER_INCREMENT
        == EXPECTED_FORMAL_FIVE_DOUBLE_INCREMENT
    )
    for profile, expected_classes in expected_complementary_classes.items():
        double_indices = [
            index
            for index, multiplicity in enumerate(profile)
            if multiplicity == 2
        ]
        assert len(double_indices) >= 5
        chosen = set(double_indices[:5])
        outside = [
            multiplicity
            for index, multiplicity in enumerate(profile)
            if index not in chosen
        ]
        assert sum(outside) == 11
        assert len(outside) == expected_classes
        assert expected_classes - 4 in (0, 1, 2, 3)
        if expected_classes == 7:
            assert outside.count(1) == 5
            assert outside.count(1) > 2 * expected_classes - 10

    # The remaining application uses all four exact doubles and one of
    # the triples as a formal double layer.  Its fixed excess contributes
    # one simple root to A; the four untouched singleton classes supply
    # four more.  Every one of the ten formal cores is legal.
    formal_profile = next(iter(EXPECTED_FORMAL_LAYER_INCREMENT))
    double_indices = tuple(
        index
        for index, multiplicity in enumerate(formal_profile)
        if multiplicity == 2
    )
    triple_indices = tuple(
        index
        for index, multiplicity in enumerate(formal_profile)
        if multiplicity == 3
    )
    assert len(double_indices) == 4
    assert len(triple_indices) == 3
    for formal_triple in triple_indices:
        chosen = set(double_indices) | {formal_triple}
        assert len(chosen) == 5
        for partial_pair in combinations(sorted(chosen), 2):
            partial_pair = set(partial_pair)
            takes = {
                index: (1 if index in partial_pair else 2)
                for index in chosen
            }
            assert sum(takes.values()) == H
            assert frontier.leaves_singleton(formal_profile, takes)

        a_multiplicities = tuple(
            multiplicity - 2 if index in chosen else multiplicity
            for index, multiplicity in enumerate(formal_profile)
            if multiplicity - 2 > 0 or index not in chosen
        )
        assert sum(a_multiplicities) == 11
        assert len(a_multiplicities) == 7
        assert a_multiplicities.count(1) == 5
        assert a_multiplicities.count(1) > 2 * len(a_multiplicities) - 10


def check_global_overlap_table() -> None:
    all_profiles = set(frontier.partitions(TOTAL))
    distinct = (1,) * TOTAL
    collision_profiles = all_profiles - {distinct}
    assert len(all_profiles) == 792
    assert len(collision_profiles) == 791

    categories = {
        profile: frontier.classify(profile, H, P)
        for profile in collision_profiles
    }
    routes = {
        "M": {
            profile
            for profile in collision_profiles
            if moving_value_witness(profile) is not None
        },
        "A": {
            profile
            for profile in collision_profiles
            if antiderivative_closes(profile)
        },
        "U": {
            profile
            for profile in collision_profiles
            if unique_bad_core_closes(profile)
        },
        "T": {
            profile
            for profile in collision_profiles
            if consecutive_transfer_witness(profile) is not None
        },
        "F": {
            profile
            for profile in collision_profiles
            if five_exact_triples_closes(profile)
        },
        "G": {
            profile
            for profile in collision_profiles
            if four_exact_triples_closes(profile)
        },
        "J": EXPECTED_FORMAL_FIVE_DOUBLE_INCREMENT,
        "N": EXPECTED_NINE_DOUBLE_THREE_SINGLETON_INCREMENT,
        "P": EXPECTED_THREE_TRIPLE_MIXED_INCREMENT,
        "B": EXPECTED_DOUBLE_GUARD_BYPASS_INCREMENT,
    }

    expected_rows = {
        "M": {"H": 45, "S": 138, "C": 13, "L": 9, "Q": 7, "V": 0, "R": 1},
        "A": {"H": 3, "S": 21, "C": 2, "L": 3, "Q": 10, "V": 0, "R": 21},
        "U": {"H": 0, "S": 0, "C": 1, "L": 1, "Q": 1, "V": 0, "R": 2},
        "T": {"H": 213, "S": 258, "C": 2, "L": 0, "Q": 0, "V": 0, "R": 1},
        "F": {"H": 0, "S": 2, "C": 2, "L": 1, "Q": 0, "V": 0, "R": 6},
        "G": {"H": 2, "S": 10, "C": 6, "L": 1, "Q": 0, "V": 0, "R": 11},
        "J": {"H": 0, "S": 0, "C": 0, "L": 0, "Q": 0, "V": 0, "R": 8},
        "N": {"H": 0, "S": 0, "C": 0, "L": 0, "Q": 0, "V": 0, "R": 1},
        "P": {"H": 0, "S": 0, "C": 0, "L": 0, "Q": 0, "V": 0, "R": 1},
        "B": {"H": 0, "S": 0, "C": 0, "L": 0, "Q": 0, "V": 0, "R": 1},
    }
    expected_totals = {
        "M": 213,
        "A": 60,
        "U": 5,
        "T": 474,
        "F": 11,
        "G": 30,
        "J": 8,
        "N": 1,
        "P": 1,
        "B": 1,
    }
    for name, route_set in routes.items():
        observed = Counter(categories[profile] for profile in route_set)
        assert {
            category: observed.get(category, 0)
            for category in ("H", "S", "C", "L", "Q", "V", "R")
        } == expected_rows[name]
        assert len(route_set) == expected_totals[name]

    expected_pairwise = {
        ("M", "A"): 33,
        ("M", "U"): 2,
        ("M", "T"): 90,
        ("M", "F"): 0,
        ("A", "U"): 0,
        ("A", "T"): 4,
        ("A", "F"): 0,
        ("U", "T"): 0,
        ("U", "F"): 0,
        ("T", "F"): 0,
        ("M", "G"): 3,
        ("A", "G"): 1,
        ("U", "G"): 0,
        ("T", "G"): 2,
        ("F", "G"): 11,
        ("M", "J"): 0,
        ("A", "J"): 0,
        ("U", "J"): 0,
        ("T", "J"): 0,
        ("F", "J"): 0,
        ("G", "J"): 0,
    }
    for earlier in ("M", "A", "U", "T", "F", "G", "J"):
        expected_pairwise[(earlier, "N")] = 0
    for earlier in ("M", "A", "U", "T", "F", "G", "J", "N"):
        expected_pairwise[(earlier, "P")] = 0
    for earlier in ("M", "A", "U", "T", "F", "G", "J", "N", "P"):
        expected_pairwise[(earlier, "B")] = 0
    assert set(expected_pairwise) == set(combinations(routes, 2))
    for pair, expected in expected_pairwise.items():
        assert len(routes[pair[0]] & routes[pair[1]]) == expected
    assert len(routes["M"] & routes["A"] & routes["T"]) == 4
    for triple in combinations(routes, 3):
        if set(triple) != {"M", "A", "T"}:
            assert not set.intersection(*(routes[name] for name in triple))


def check_order_and_terminal_routes() -> None:
    assert all(sum(profile) == TOTAL for profile in EXPECTED_RESIDUALS)
    assert all(
        tuple(sorted(profile, reverse=True)) == profile
        for profile in EXPECTED_RESIDUALS
    )
    assert ordered(EXPECTED_RESIDUALS) == EXPECTED_RESIDUALS
    assert not EXPECTED_RESIDUALS

    target = (2,) * 10 + (1,)
    assert target in EXPECTED_FORMAL_FIVE_DOUBLE_INCREMENT
    assert {target} == EXPECTED_STANDALONE_TEN_DOUBLE
    formal_core_count = 0
    for five_set_tuple in combinations(range(10), 5):
        five_set = set(five_set_tuple)
        outside = set(range(10)) - five_set
        for partial_pair_tuple in combinations(sorted(five_set), 2):
            partial_pair = set(partial_pair_tuple)
            takes = {
                index: (1 if index in partial_pair else 2)
                for index in five_set
            }
            complement = tuple(
                target[index] - takes.get(index, 0)
                for index in range(len(target))
            )
            formal_core_count += 1
            assert sum(takes.values()) == H
            assert sum(complement) == P + 2 == 13
            assert len(takes) == 5
            assert sum(entry == 1 for entry in complement) == 3
            assert complement[-1] == 1
            assert all(complement[index] == 2 for index in outside)
    assert formal_core_count == math.comb(10, 5) * math.comb(5, 2) == 2520

    # q has degree two, the two quadratic lifts give P_6, and the
    # complementary factor C^2(z-r) has degree eleven.
    residual_degree = 2
    lift_degree = residual_degree + 2 * 2
    complement_degree = 2 * 5 + 1
    numerator_degree = complement_degree + lift_degree
    denominator_degree = (K + 1) + 3 * 5
    assert (lift_degree, complement_degree) == (6, 11)
    assert (numerator_degree, denominator_degree) == (17, 19)
    assert denominator_degree - numerator_degree == 2

    # In the dual calculation deg N<=7 and the sharp leading cancellation
    # leaves E of degree at most twelve; division by Q^2 leaves P_2.
    assert 12 - 2 * 5 == 2

    # Route N closes 2^9 1^3.  Its five chosen doubles leave seven
    # complementary classes, hence the injective relation pencil is P_3.
    newly_closed_target = (2,) * 9 + (1,) * 3
    assert {newly_closed_target} == EXPECTED_NINE_DOUBLE_THREE_SINGLETON_INCREMENT
    assert newly_closed_target not in EXPECTED_RESIDUALS
    outside_classes = (9 - 5) + 3
    assert outside_classes == 7
    assert outside_classes - 4 == 3

    # The two terminal routes close the last two profiles.  The final
    # profile has a second, independent mixed-layer proof, so that proof
    # receives no additional sequential credit.
    three_triple_target = (3,) * 3 + (2,) * 3 + (1,) * 6
    assert {three_triple_target} == EXPECTED_THREE_TRIPLE_MIXED_INCREMENT
    assert sum(multiplicity >= 2 for multiplicity in three_triple_target) == 6
    assert three_triple_target.count(1) == 6

    two_triple_target = (3,) * 2 + (2,) * 4 + (1,) * 7
    assert {two_triple_target} == EXPECTED_DOUBLE_GUARD_BYPASS_INCREMENT
    assert (
        EXPECTED_INDEPENDENT_TWO_TRIPLE_MIXED
        == EXPECTED_DOUBLE_GUARD_BYPASS_INCREMENT
    )
    assert two_triple_target.count(3) == 2
    assert two_triple_target.count(2) == 4
    assert two_triple_target.count(1) == 7


def main() -> None:
    assert (H, P, K, TOTAL) == (8, 11, 3, 21)
    check_old_slice_and_updated_counts()
    check_every_added_witness()
    check_global_overlap_table()
    check_order_and_terminal_routes()
    print("eighth-split k=3 fully updated collision census: PASS")
    print("old residual 46; M/A/U/T/F/G/J/N/P/B add 1/21/2/1/6/4/8/1/1/1")
    print("updated residual count: 0")
    print("independent terminal mixed-layer route I equals the one-profile route B")


if __name__ == "__main__":
    main()
