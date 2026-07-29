#!/usr/bin/env python3
"""Exact k=5 census audit for the all-order formal-five-layer theorem."""

from collections import Counter
from itertools import combinations
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


H = 8
P = 13
K = P - H
TOTAL = P + H + 2

PREVIOUSLY_CLOSED = {
    (2,) * 11 + (1,),
    (2,) * 10 + (1,) * 3,
}

PROFILE_FOUR_FOUR_FIVE_TRIPLES = (4, 4) + (3,) * 5
PROFILE_FIVE_TRIPLES_FOUR_DOUBLES = (3,) * 5 + (2,) * 4
PROFILE_FOUR_TRIPLES_FIVE_DOUBLES_SINGLETON = (
    (3,) * 4 + (2,) * 5 + (1,)
)
EXPECTED_INCREMENT = {
    PROFILE_FOUR_FOUR_FIVE_TRIPLES,
    PROFILE_FIVE_TRIPLES_FOUR_DOUBLES,
    PROFILE_FOUR_TRIPLES_FIVE_DOUBLES_SINGLETON,
}


def zero_scenarios(profile):
    """Possible zero placements: none, or any original singleton class."""

    return (None,) + tuple(
        index for index, multiplicity in enumerate(profile) if multiplicity == 1
    )


def residual_multiplicities(profile, takes):
    return tuple(
        multiplicity - takes.get(index, 0)
        for index, multiplicity in enumerate(profile)
    )


def has_nonzero_singleton_guard(profile, takes, zero_index):
    residual = residual_multiplicities(profile, takes)
    return any(
        multiplicity == 1 and index != zero_index
        for index, multiplicity in enumerate(residual)
    )


def choice_has_ten_legal_cores(profile, chosen):
    pair_count = 0
    legal = True
    for lowered_pair in combinations(chosen, 2):
        takes = {
            index: (1 if index in lowered_pair else 2)
            for index in chosen
        }
        assert sum(takes.values()) == H
        for zero_index in zero_scenarios(profile):
            legal &= has_nonzero_singleton_guard(
                profile, takes, zero_index
            )
        pair_count += 1
    assert pair_count == 10
    return legal


def complement(profile, chosen):
    chosen_set = set(chosen)
    return tuple(
        sorted(
            (
                multiplicity - (2 if index in chosen_set else 0)
                for index, multiplicity in enumerate(profile)
                if multiplicity - (2 if index in chosen_set else 0) > 0
            ),
            reverse=True,
        )
    )


def obstructing_witnesses(profile):
    repeated_indices = tuple(
        index for index, multiplicity in enumerate(profile) if multiplicity >= 2
    )
    witnesses = []
    for chosen in combinations(repeated_indices, 5):
        if not choice_has_ten_legal_cores(profile, chosen):
            continue
        complementary_profile = complement(profile, chosen)
        classes = len(complementary_profile)
        simple_roots = complementary_profile.count(1)
        if classes < 5 or simple_roots > 2 * classes - 10:
            witnesses.append(
                (chosen, complementary_profile, classes, simple_roots)
            )
    return tuple(witnesses)


def minimum_nonzero_guard_histogram(profile, chosen):
    histogram = Counter()
    for lowered_pair in combinations(chosen, 2):
        takes = {
            index: (1 if index in lowered_pair else 2)
            for index in chosen
        }
        residual = residual_multiplicities(profile, takes)
        minimum_guards = min(
            sum(
                multiplicity == 1 and index != zero_index
                for index, multiplicity in enumerate(residual)
            )
            for zero_index in zero_scenarios(profile)
        )
        assert minimum_guards >= 1
        histogram[minimum_guards] += 1
    assert sum(histogram.values()) == 10
    return histogram


counts, frozen_tuple = frontier.census(H, P)
frozen = set(frozen_tuple)
assert (H, P, K, TOTAL) == (8, 13, 5, 23)
assert counts == {
    "H": 637,
    "S": 501,
    "C": 30,
    "L": 23,
    "R": 44,
    "Q": 19,
    "D": 1,
}
assert len(frozen) == 44
assert PREVIOUSLY_CLOSED <= frozen
open_before_increment = frozen - PREVIOUSLY_CLOSED
assert len(open_before_increment) == 42

# Exhaust every five-subset of repeated classes, not merely one canonical
# choice per multiplicity type.
choices_scanned = 0
fully_legal_choices = 0
core_zero_scenarios_audited = 0
observed_witnesses = {}
for candidate in open_before_increment:
    repeated = sum(multiplicity >= 2 for multiplicity in candidate)
    if repeated >= 5:
        choices_scanned += len(tuple(combinations(range(repeated), 5)))
    core_zero_scenarios_audited += (
        len(tuple(combinations(range(repeated), 5)))
        * 10
        * len(zero_scenarios(candidate))
    )

    legal_count = 0
    repeated_indices = tuple(
        index
        for index, multiplicity in enumerate(candidate)
        if multiplicity >= 2
    )
    for chosen in combinations(repeated_indices, 5):
        legal_count += choice_has_ten_legal_cores(candidate, chosen)
    fully_legal_choices += legal_count

    witnesses = obstructing_witnesses(candidate)
    if witnesses:
        observed_witnesses[candidate] = witnesses

assert choices_scanned == 1365
assert fully_legal_choices == 1104
assert core_zero_scenarios_audited == 44850
assert set(observed_witnesses) == EXPECTED_INCREMENT
assert sum(map(len, observed_witnesses.values())) == 7

expected_witness_counts = {
    PROFILE_FOUR_FOUR_FIVE_TRIPLES: 1,
    PROFILE_FIVE_TRIPLES_FOUR_DOUBLES: 5,
    PROFILE_FOUR_TRIPLES_FIVE_DOUBLES_SINGLETON: 1,
}
expected_signatures = {
    PROFILE_FOUR_FOUR_FIVE_TRIPLES: ((4, 4) + (1,) * 5, 7, 5),
    PROFILE_FIVE_TRIPLES_FOUR_DOUBLES: ((3,) * 4 + (1,), 5, 1),
    PROFILE_FOUR_TRIPLES_FIVE_DOUBLES_SINGLETON: (
        (3,) * 4 + (1,),
        5,
        1,
    ),
}
for candidate, witnesses in observed_witnesses.items():
    assert len(witnesses) == expected_witness_counts[candidate]
    for _, complementary_profile, classes, simple_roots in witnesses:
        assert sum(complementary_profile) == K + 8 == 13
        assert (
            complementary_profile,
            classes,
            simple_roots,
        ) == expected_signatures[candidate]
        assert classes >= 5
        assert simple_roots > 2 * classes - 10

# Directly audit the ten cores of one canonical witness of each profile.
canonical_choices = {
    PROFILE_FOUR_FOUR_FIVE_TRIPLES: (2, 3, 4, 5, 6),
    PROFILE_FIVE_TRIPLES_FOUR_DOUBLES: (0, 5, 6, 7, 8),
    PROFILE_FOUR_TRIPLES_FIVE_DOUBLES_SINGLETON: (4, 5, 6, 7, 8),
}
expected_guard_histograms = {
    PROFILE_FOUR_FOUR_FIVE_TRIPLES: Counter({3: 10}),
    PROFILE_FIVE_TRIPLES_FOUR_DOUBLES: Counter({3: 6, 1: 4}),
    PROFILE_FOUR_TRIPLES_FIVE_DOUBLES_SINGLETON: Counter({2: 10}),
}
for candidate, chosen in canonical_choices.items():
    assert choice_has_ten_legal_cores(candidate, chosen)
    assert (
        minimum_nonzero_guard_histogram(candidate, chosen)
        == expected_guard_histograms[candidate]
    )

open_after_increment = open_before_increment - EXPECTED_INCREMENT
assert len(open_after_increment) == 39
assert (2,) * 9 + (1,) * 5 in open_after_increment


print("k=5 all-order formal-five-layer increment: PASS")
print(
    f"exhaustive scan: {choices_scanned} choices, "
    f"{core_zero_scenarios_audited} core/zero scenarios"
)
print("new closures: 3 profiles from 7 witnesses")
print("updated ledger: 5 accepted, 39 open")
