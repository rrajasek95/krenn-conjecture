#!/usr/bin/env python3
"""Exact B4 orbit/compatibility referee for the char-zero support-eight family.

The sixteen Q-coordinates are indexed by bit strings on four supervertices,
with integer index ``b0 b1 b2 b3``.  Endpoint flips and supervertex
permutations generate B4.  Two colour supports A,B can pass the binary
cross-product packet only if A is disjoint from the bitwise complements of B.

This is deliberately a support theorem only: it classifies the orbit of one
proved characteristic-zero family, not every possible support-eight branch.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_lowq_support_b4_orbit.json"
BASE_SUPPORT = frozenset((1, 3, 4, 5, 6, 9, 10, 12))


def bits(index):
    return tuple((index >> (3 - site)) & 1 for site in range(4))


def index(bit_tuple):
    return sum(bit << (3 - site) for site, bit in enumerate(bit_tuple))


def act_index(value, permutation, flips):
    old = bits(value)
    new = [0] * 4
    for old_site in range(4):
        new[permutation[old_site]] = old[old_site]
    return index(tuple(new[site] ^ flips[site] for site in range(4)))


def act_support(support, permutation, flips):
    return frozenset(act_index(value, permutation, flips)
                     for value in support)


def complement_support(support):
    return frozenset(15 - value for value in support)


def compatible(left, right):
    return left.isdisjoint(complement_support(right))


def main():
    actions = tuple((permutation, flips)
                    for permutation in permutations(range(4))
                    for flips in product((0, 1), repeat=4))
    if len(actions) != 384:
        raise RuntimeError("B4 action count changed")

    orbit = frozenset(act_support(BASE_SUPPORT, *action)
                      for action in actions)
    stabilizer = tuple(action for action in actions
                       if act_support(BASE_SUPPORT, *action) == BASE_SUPPORT)
    compatible_pairs = tuple((left, right) for left in orbit for right in orbit
                             if compatible(left, right))

    # A one-coordinate deletion is a must-fire control: the same compatibility
    # test is then non-vacuous for every deletion orbit.
    deletion_controls = []
    for deleted in sorted(BASE_SUPPORT):
        seed = BASE_SUPPORT - {deleted}
        deletion_orbit = frozenset(act_support(seed, *action)
                                   for action in actions)
        count = sum(compatible(left, right)
                    for left in deletion_orbit for right in deletion_orbit)
        if count == 0:
            raise RuntimeError("deletion control unexpectedly has no pair")
        deletion_controls.append({
            "deleted_index": deleted,
            "orbit_size": len(deletion_orbit),
            "ordered_compatible_pairs": count,
        })

    if len(orbit) != 96 or len(stabilizer) != 4 or compatible_pairs:
        raise RuntimeError("support-eight B4 orbit census changed")

    result = {
        "status": "UNAUDITED exact support-orbit referee",
        "base_support": sorted(BASE_SUPPORT),
        "group_action": (
            "all 24 supervertex permutations times all 16 endpoint flips"
        ),
        "action_count": len(actions),
        "orbit_size": len(orbit),
        "stabilizer_size": len(stabilizer),
        "ordered_pairs_tested": len(orbit) ** 2,
        "ordered_compatible_pairs": len(compatible_pairs),
        "compatibility_condition": "A intersect complement(B) is empty",
        "deletion_must_fire_controls": deletion_controls,
        "scope": (
            "This excludes compatible colour pairs only when both supports "
            "lie in this one B4 orbit; classification of all characteristic-"
            "zero support-eight branches remains open."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("low-Q B4 support orbit: PASS")
    print("actions / orbit / stabilizer:", len(actions), len(orbit),
          len(stabilizer))
    print("ordered compatible / tested:", len(compatible_pairs),
          len(orbit) ** 2)
    print("deletion must-fire counts:",
          [row["ordered_compatible_pairs"] for row in deletion_controls])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
