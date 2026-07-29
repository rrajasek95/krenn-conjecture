#!/usr/bin/env python3
"""Finite orbit census for ordinary-SDR, locally nonseparable packets.

After selecting an SDR and killing its good-site field axes, a selected
good pair is isolated.  A selected pair {0,v} through the deficient site
leaves an anchored packet consisting of {0,v} and an arbitrary subset of
the four good pairs {v,w}.  This script canonicalizes all such supports for
the five nonseparable local-matroid/K types.

This is a frontier census, not a common-power obstruction.
"""

from __future__ import annotations

from collections import Counter
from functools import cache
from itertools import combinations, permutations, product


BAD = 0
GOOD = tuple(range(1, 6))
GOOD_PAIRS = tuple(combinations(GOOD, 2))


TYPES = (
    ("circuit_k2", "circuit", frozenset((0, 1))),
    ("coincident_k1", "coincident", frozenset((0,))),
    ("coincident_k2", "coincident", frozenset((0, 1))),
    ("rank1_k1", "rank1", frozenset((0,))),
    ("rank1_k2", "rank1", frozenset((0, 1))),
)

NONSEPARABLE_K = {
    "circuit_k2": {frozenset((0, 1))},
    "coincident_k1": {frozenset((0,))},
    "coincident_k2": {
        frozenset((0,)), frozenset((2,)),
        frozenset((0, 1)), frozenset((1, 2)),
    },
    "rank1_k1": {
        frozenset(subset)
        for size in (1, 2) for subset in combinations(range(3), size)
    },
    "rank1_k2": {
        frozenset(subset)
        for size in (1, 2) for subset in combinations(range(3), size)
    },
}


def edge(u, v):
    return tuple(sorted((u, v)))


def map_family(family, site_permutation):
    return tuple(sorted(
        edge(site_permutation[u], site_permutation[v]) for u, v in family
    ))


@cache
def transformations(name):
    if name.endswith("_k1"):
        site_permutations = tuple(
            (0, 1) + tail for tail in permutations((2, 3, 4, 5))
        )
        field_orders = (
            ((0, 1, 2), (0, 2, 1))
            if name == "rank1_k1" else ((0, 1, 2),)
        )
        return tuple(
            (site_permutation, field_order)
            for site_permutation in site_permutations
            for field_order in field_orders
        )

    fixed_tail = tuple(permutations((3, 4, 5)))
    out = [
        ((0, 1, 2) + tail, (0, 1, 2))
        for tail in fixed_tail
    ]
    if name in {"circuit_k2", "rank1_k2"}:
        out.extend(
            ((0, 2, 1) + tail, (1, 0, 2))
            for tail in fixed_tail
        )
    return tuple(out)


def canonical(name, families):
    return min(
        tuple(
            map_family(families[old_field], site_permutation)
            for old_field in field_order
        )
        for site_permutation, field_order in transformations(name)
    )


def packet(anchor, arm_mask):
    arms = tuple(edge(anchor, w) for w in GOOD if w != anchor)
    return tuple(sorted(
        (edge(BAD, anchor),)
        + tuple(arm for index, arm in enumerate(arms) if arm_mask & (1 << index))
    ))


def labelled_supports(name):
    if name.endswith("_k1"):
        for arm_mask in range(16):
            incident = packet(1, arm_mask)
            for first, second in permutations(GOOD_PAIRS, 2):
                yield (incident, (first,), (second,))
        return

    for first_mask, second_mask in product(range(16), repeat=2):
        first = packet(1, first_mask)
        second = packet(2, second_mask)
        for outside in GOOD_PAIRS:
            yield (first, second, (outside,))


@cache
def census(name):
    counts = Counter()
    labelled = 0
    for families in labelled_supports(name):
        counts[canonical(name, families)] += 1
        labelled += 1
    expected = 16 * 90 if name.endswith("_k1") else 16 * 16 * 10
    assert labelled == expected
    assert sum(counts.values()) == expected
    return counts


def arm_count(family):
    return len(family) - 1


def arms(family):
    return frozenset(pair for pair in family if BAD not in pair)


def has_locally_separable_sdr(name, families):
    for choice in product(*families):
        if len(set(choice)) != 3:
            continue
        killed = frozenset(
            field for field, pair in enumerate(choice) if BAD in pair
        )
        if killed not in NONSEPARABLE_K[name]:
            return True
    return False


def audit_residual_structure(name, families):
    outside = families[2] if name.endswith("_k2") else None
    if name.endswith("_k1"):
        assert arms(families[0]) <= frozenset((families[1][0], families[2][0]))
    elif name == "circuit_k2":
        target = frozenset((outside[0],))
        assert arms(families[0]) <= target
        assert arms(families[1]) <= target
    elif name == "coincident_k2":
        assert arms(families[0]) <= frozenset((outside[0],))
    elif name == "rank1_k2":
        target = outside[0]
        first = arms(families[0]) - {target}
        second = arms(families[1]) - {target}
        assert not first or not second or first == second and len(first) == 1


def profile_census(representatives, k_size):
    profiles = Counter()
    for families in representatives:
        profile = tuple(arm_count(families[r]) for r in range(k_size))
        profiles[profile] += 1
    return profiles


@cache
def nonseparable_only_representatives(name):
    return tuple(
        families for families in sorted(census(name))
        if not has_locally_separable_sdr(name, families)
    )


def main():
    total_orbits = 0
    total_normalizable = 0
    total_parameter = 0
    total_residual = 0
    total_residual_normalizable = 0
    total_residual_parameter = 0
    for name, kind, killed in TYPES:
        counts = census(name)
        representatives = tuple(sorted(counts))
        k_size = len(killed)
        profiles = profile_census(representatives, k_size)
        normalizable = sum(
            count for profile, count in profiles.items() if max(profile) <= 3
        )
        parameter = len(representatives) - normalizable
        residual = nonseparable_only_representatives(name)
        for families in residual:
            audit_residual_structure(name, families)
        residual_profiles = profile_census(residual, k_size)
        residual_normalizable = sum(
            count for profile, count in residual_profiles.items()
            if max(profile) <= 3
        )
        total_orbits += len(representatives)
        total_normalizable += normalizable
        total_parameter += parameter
        total_residual += len(residual)
        total_residual_normalizable += residual_normalizable
        total_residual_parameter += len(residual) - residual_normalizable
        print({
            "type": name,
            "matroid": kind,
            "K": tuple(sorted(killed)),
            "labelled_supports": sum(counts.values()),
            "orbits": len(representatives),
            "normalizable_orbits": normalizable,
            "full_packet_parameter_orbits": parameter,
            "arm_profile_census": dict(sorted(profiles.items())),
            "nonseparable_only_orbits": len(residual),
            "nonseparable_only_normalizable": residual_normalizable,
            "nonseparable_only_parameter": len(residual) - residual_normalizable,
            "nonseparable_only_profiles": dict(sorted(residual_profiles.items())),
        })
    print({
        "total_orbits": total_orbits,
        "normalizable_orbits": total_normalizable,
        "full_packet_parameter_orbits": total_parameter,
        "nonseparable_only_orbits": total_residual,
        "nonseparable_only_normalizable": total_residual_normalizable,
        "nonseparable_only_parameter": total_residual_parameter,
    })
    print("sole-defect nonseparable packet orbit census: PASS")


if __name__ == "__main__":
    main()
