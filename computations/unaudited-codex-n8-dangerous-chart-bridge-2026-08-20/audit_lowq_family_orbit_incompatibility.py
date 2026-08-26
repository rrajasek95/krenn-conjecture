#!/usr/bin/env python3
"""Exact B4 support exclusion for the characteristic-zero |Q|=8 family.

The independently derived Laurent family has Q support
L={1,3,4,5,6,9,10,12}.  If another size-eight support L' satisfies all
polarized 4+4 rows with L, then L and complement(L') are disjoint and hence
L'=U\\complement(L).  This checker proves that required support is not in the
hyperoctahedral orbit of L.  It also records the small human obstruction: the
two induced subgraphs of the four-cube have different degree multisets.

This excludes only a mate from the same classified family orbit.  It does not
prove that all characteristic-zero size-eight branches lie in that orbit.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_lowq_family_orbit_incompatibility.json"
UNIVERSE = frozenset(range(16))
SUPPORT = frozenset((1, 3, 4, 5, 6, 9, 10, 12))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def bits(index):
    return tuple((index >> (3 - site)) & 1 for site in range(4))


def index(bit_vector):
    return sum(bit << (3 - site) for site, bit in enumerate(bit_vector))


def transform_word(word_index, permutation, flips):
    source = bits(word_index)
    target = [0] * 4
    for site in range(4):
        target[permutation[site]] = source[site] ^ flips[site]
    return index(target)


def transform_support(support, permutation, flips):
    return frozenset(transform_word(word, permutation, flips)
                     for word in support)


def complement_support(support):
    return frozenset(15 - word for word in support)


def cross_compatible(left, right):
    return left.isdisjoint(complement_support(right))


def cube_degree_multiset(support):
    return tuple(sorted(sum((word ^ (1 << coordinate)) in support
                            for coordinate in range(4))
                        for word in support))


def distance_profile_histogram(support):
    profiles = []
    for word in support:
        histogram = Counter((word ^ other).bit_count()
                            for other in support if other != word)
        profiles.append(tuple(sorted(histogram.items())))
    return {str(profile): multiplicity for profile, multiplicity
            in sorted(Counter(profiles).items(), key=lambda item: item[0])}


def main():
    required = UNIVERSE - complement_support(SUPPORT)
    require(len(SUPPORT) == len(required) == 8
            and cross_compatible(SUPPORT, required),
            "size-eight cross-complement formula failed")

    group = tuple((permutation, flips)
                  for permutation in permutations(range(4))
                  for flips in product((0, 1), repeat=4))
    require(len(group) == 384, "full B4 action size changed")
    orbit_counter = Counter(transform_support(SUPPORT, *element)
                            for element in group)
    orbit = frozenset(orbit_counter)
    stabilizer_sizes = set(orbit_counter.values())
    compatible_elements = tuple(element for element in group
                                if cross_compatible(
                                    SUPPORT,
                                    transform_support(SUPPORT, *element)))
    require(len(orbit) * next(iter(stabilizer_sizes)) == len(group)
            and len(stabilizer_sizes) == 1,
            "orbit-stabilizer control failed")
    require(required not in orbit and not compatible_elements,
            "the low-Q family acquired a B4-compatible mate")

    left_degrees = cube_degree_multiset(SUPPORT)
    required_degrees = cube_degree_multiset(required)
    require(left_degrees != required_degrees,
            "cube-degree obstruction disappeared")
    # Isometries of the Hamming cube preserve this degree multiset, giving a
    # hand-checkable proof independent of the exhaustive group action.
    require(all(cube_degree_multiset(image) == left_degrees for image in orbit),
            "B4 failed to preserve the cube degree invariant")

    result = {
        "status": "UNAUDITED exact low-Q family orbit incompatibility",
        "family_Q_support": sorted(SUPPORT),
        "required_size8_mate_support": sorted(required),
        "cross_complement_formula": (
            "for |L|=|L'|=8, L intersect complement(L')=empty iff "
            "L'=U\\complement(L)"
        ),
        "B4_group_size": len(group),
        "B4_orbit_size": len(orbit),
        "B4_stabilizer_size": next(iter(stabilizer_sizes)),
        "B4_elements_giving_cross_compatible_mate": len(compatible_elements),
        "required_support_in_B4_orbit": required in orbit,
        "family_cube_degree_multiset": list(left_degrees),
        "required_cube_degree_multiset": list(required_degrees),
        "family_distance_profile_histogram": distance_profile_histogram(SUPPORT),
        "required_distance_profile_histogram": distance_profile_histogram(required),
        "conclusion": (
            "No site permutation and independent clone flips transform the "
            "characteristic-zero size-eight family into a Q-cross-compatible "
            "mate. The induced four-cube degree multisets already distinguish "
            "the two required supports."
        ),
        "scope_guard": (
            "This is an orbit-level exclusion, not a classification of all "
            "H-live cofactor-viable size-eight branches and not yet a proof "
            "that the full diagonal 78+48+144 packet has no solution."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("low-Q family B4 incompatibility: PASS")
    print("orbit/stabilizer/compatible:", len(orbit),
          next(iter(stabilizer_sizes)), len(compatible_elements))
    print("cube degrees:", left_degrees, required_degrees)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
