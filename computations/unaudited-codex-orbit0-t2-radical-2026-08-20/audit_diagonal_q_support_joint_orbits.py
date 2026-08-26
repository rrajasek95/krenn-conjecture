#!/usr/bin/env python3
"""Exact joint branch/Q-support orbit census for sizes seven and eight.

This is the finite front end for any diagonal support classification.  Once
a cofactor branch is fixed, its stabilizer -- not the full B4 group -- acts
on Q supports.  It also isolates the cases killed immediately by

    H = sum_{s=0}^7 Q_s Q_{15-s}

on the pairconstant/triangle base: a support with no complementary live pair
has H=0 and cannot occur on the H-open locus.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_diagonal_q_support_joint_orbits.json"
IDENTITY = (HERE.parent /
            "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
            "audit_polarized_superpair_core_identity.py")
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
BRANCHES = (0, 1, 11)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def transform_mask(mask, switches, permutation):
    answer = 0
    for edge_index, (i, j) in enumerate(EDGES):
        bit = ((mask >> edge_index) & 1) ^ switches[i] ^ switches[j]
        target = EDGE_INDEX[tuple(sorted((permutation[i], permutation[j])))]
        answer |= bit << target
    return answer


def transform_q_index(index, switches, permutation):
    bits = tuple((index >> (3 - site)) & 1 for site in range(4))
    transformed = [0] * 4
    for site in range(4):
        transformed[permutation[site]] = bits[site] ^ switches[site]
    return sum(transformed[site] << (3 - site) for site in range(4))


GROUP = tuple((switches, permutation)
              for switches in product((0, 1), repeat=4)
              for permutation in permutations(range(4)))
require(len(GROUP) == 384, "full B4 size changed")


def support_orbits(branch, size):
    stabilizer = tuple(element for element in GROUP
                       if transform_mask(branch, *element) == branch)
    unseen = {sum(1 << index for index in subset)
              for subset in combinations(range(16), size)}
    records = []
    while unseen:
        representative = min(unseen)
        orbit = set()
        for switches, permutation in stabilizer:
            transformed = 0
            for index in range(16):
                if representative >> index & 1:
                    transformed |= 1 << transform_q_index(
                        index, switches, permutation)
            orbit.add(transformed)
        require(representative == min(orbit), "support representative changed")
        unseen -= orbit
        complementary_pairs = sum(
            (representative >> index & 1)
            and (representative >> (15 - index) & 1)
            for index in range(8))
        records.append((representative, len(orbit), complementary_pairs))
    return stabilizer, tuple(records)


def indices(mask):
    return [index for index in range(16) if mask >> index & 1]


def main():
    require(IDENTITY.is_file(), "polarized identity verifier is missing")
    branch_records = []
    totals = {7: Counter(), 8: Counter()}
    all_representatives = {}
    for size in (7, 8):
        for branch in BRANCHES:
            stabilizer, records = support_orbits(branch, size)
            histogram = Counter(row[2] for row in records)
            totals[size].update(histogram)
            all_representatives[(branch, size)] = {row[0] for row in records}
            branch_records.append({
                "branch_mask": branch,
                "support_size": size,
                "branch_stabilizer_size": len(stabilizer),
                "joint_support_orbits": len(records),
                "complementary_live_pair_histogram": {
                    str(key): value for key, value in sorted(histogram.items())},
                "zero_pair_orbits_immediately_excluded_on_H_open":
                    histogram[0],
                "positive_pair_orbits_requiring_algebra":
                    len(records) - histogram[0],
                "orbit_mass_check": sum(row[1] for row in records),
            })
            require(sum(row[1] for row in records)
                    == len(tuple(combinations(range(16), size))),
                    "support orbit mass changed")

    expected_counts = {
        (0, 7): 337, (1, 7): 1615, (11, 7): 337,
        (0, 8): 386, (1, 8): 1834, (11, 8): 386,
    }
    require({(row["branch_mask"], row["support_size"]):
             row["joint_support_orbits"] for row in branch_records}
            == expected_counts, "joint orbit count changed")
    require(totals[7] == {0: 240, 1: 1034, 2: 876, 3: 139},
            "size-seven complementary-pair histogram changed")
    require(totals[8] == {0: 80, 1: 712, 2: 1286, 3: 480, 4: 48},
            "size-eight complementary-pair histogram changed")

    # Normalize the exact mask-51 family by switches (0,1,1,0), obtaining
    # branch mask zero and this live support.  Its branch-stabilizer orbit is
    # one of the 386 equality candidates and has mass 24.
    family_support = sum(1 << index for index in
                         (0, 2, 3, 5, 7, 10, 12, 15))
    switches = (0, 1, 1, 0)
    permutation = (0, 1, 2, 3)
    require(transform_mask(51, switches, permutation) == 0,
            "family branch normalization changed")
    stabilizer0 = tuple(element for element in GROUP
                        if transform_mask(0, *element) == 0)
    family_orbit = set()
    for sw, perm in stabilizer0:
        transformed = 0
        for index in range(16):
            if family_support >> index & 1:
                transformed |= 1 << transform_q_index(index, sw, perm)
        family_orbit.add(transformed)
    family_representative = min(family_orbit)
    require(len(family_orbit) == 24
            and family_representative in all_representatives[(0, 8)],
            "known equality-family support orbit changed")

    result = {
        "status": "UNAUDITED exact joint branch/Q-support orbit census",
        "full_B4_size": len(GROUP),
        "branch_records": branch_records,
        "total_size7_joint_orbits": sum(totals[7].values()),
        "total_size7_complementary_live_pair_histogram": {
            str(key): value for key, value in sorted(totals[7].items())},
        "size7_immediate_H_identity_exclusions": totals[7][0],
        "size7_remaining_algebraic_cases": sum(totals[7].values()) - totals[7][0],
        "total_size8_joint_orbits": sum(totals[8].values()),
        "total_size8_complementary_live_pair_histogram": {
            str(key): value for key, value in sorted(totals[8].items())},
        "size8_immediate_H_identity_exclusions": totals[8][0],
        "size8_remaining_algebraic_cases": sum(totals[8].values()) - totals[8][0],
        "H_identity": "H=sum_{s=0}^7 Q_s Q_{15-s} on e=t=0",
        "H_identity_verifier": str(IDENTITY.relative_to(HERE.parent.parent)),
        "H_identity_verifier_sha256": sha256(IDENTITY.read_bytes()).hexdigest(),
        "known_weight0_equality_family": {
            "normalized_branch_mask": 0,
            "live_support": indices(family_support),
            "branch_stabilizer_orbit_size": len(family_orbit),
            "canonical_live_support": indices(family_representative),
            "canonical_live_support_mask": family_representative,
            "complementary_live_pairs": sum(
                (family_representative >> index & 1)
                and (family_representative >> (15 - index) & 1)
                for index in range(8)),
        },
        "scope": (
            "The zero-complement-pair exclusions are exact. The remaining "
            "2049 size-seven and 2526 size-eight cases are a finite algebraic "
            "classification target, not conclusions. The known family marks "
            "one nonempty size-eight orbit only."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("joint branch/Q-support orbit census: PASS")
    print("k7 total/trivial/remaining:", sum(totals[7].values()),
          totals[7][0], sum(totals[7].values()) - totals[7][0])
    print("k8 total/trivial/remaining:", sum(totals[8].values()),
          totals[8][0], sum(totals[8].values()) - totals[8][0])
    print("known equality support orbit:", len(family_orbit),
          indices(family_representative))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
