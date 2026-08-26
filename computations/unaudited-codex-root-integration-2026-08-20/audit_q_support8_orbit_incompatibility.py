#!/usr/bin/env python3
"""Exact B4 support audit for the characteristic-zero eight-Q family.

The four-supervertex symmetry is the full isometry group of the Boolean
4-cube: coordinate permutations followed by independent bit flips.  The
transversal mixed rows require

    supp(Q_c) intersect complement_bits(supp(Q_d)) = empty.

This checker proves that no two images of the support discovered in the
exact number-field family satisfy that condition.  It is a combinatorial
lemma only: it does not classify all possible characteristic-zero supports.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


OUT = Path(__file__).with_name("results_q_support8_orbit_incompatibility.json")
SEED = frozenset((1, 3, 4, 5, 6, 9, 10, 12))


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def bits(index: int) -> tuple[int, ...]:
    return tuple((index >> (3 - position)) & 1 for position in range(4))


def index(bits_: tuple[int, ...] | list[int]) -> int:
    return sum(bit << (3 - position) for position, bit in enumerate(bits_))


def act(support: frozenset[int], permutation: tuple[int, ...],
        flips: tuple[int, ...]) -> frozenset[int]:
    answer = set()
    for source in support:
        source_bits = bits(source)
        target_bits = [0] * 4
        for position in range(4):
            target_bits[permutation[position]] = source_bits[position] ^ flips[position]
        answer.add(index(target_bits))
    return frozenset(answer)


def complement_bits(support: frozenset[int]) -> frozenset[int]:
    return frozenset(15 - value for value in support)


def induced_cube_degrees(support: frozenset[int]) -> tuple[int, ...]:
    return tuple(sorted(sum((vertex ^ (1 << bit)) in support
                            for bit in range(4))
                        for vertex in support))


def main() -> None:
    group = tuple((permutation, flips)
                  for permutation in permutations(range(4))
                  for flips in product((0, 1), repeat=4))
    require(len(group) == 384, "B4 order changed")
    orbit = tuple(sorted({act(SEED, *element) for element in group},
                         key=lambda support: tuple(sorted(support))))
    require(len(orbit) == 96, "support orbit size changed")
    stabilizer = sum(act(SEED, *element) == SEED for element in group)
    require(stabilizer == 4 and len(orbit) * stabilizer == len(group),
            "orbit-stabilizer control failed")

    compatible = []
    for left_index, left in enumerate(orbit):
        for right_index, right in enumerate(orbit):
            if left.isdisjoint(complement_bits(right)):
                compatible.append((left_index, right_index))
    require(not compatible, "two support-orbit images became compatible")

    # For two size-eight supports, compatibility would force the right-hand
    # support uniquely.  Checking that this forced mate is absent is an
    # independent form of the same census.
    universe = frozenset(range(16))
    orbit_set = set(orbit)
    forced_mates = tuple(complement_bits(universe - left) for left in orbit)
    require(all(mate not in orbit_set for mate in forced_mates),
            "a forced complementary mate entered the orbit")
    seed_forced_mate = complement_bits(universe - SEED)
    seed_degrees = induced_cube_degrees(SEED)
    mate_degrees = induced_cube_degrees(seed_forced_mate)
    require(seed_degrees != mate_degrees,
            "the human-readable cube-degree separator disappeared")
    require(seed_degrees == (0, 1, 1, 1, 1, 2, 3, 3)
            and mate_degrees == (1, 1, 1, 1, 1, 1, 2, 4),
            "cube-degree control values changed")

    result = {
        "status": "UNAUDITED exact B4 support-orbit incompatibility",
        "seed_support": sorted(SEED),
        "group_order": len(group),
        "orbit_size": len(orbit),
        "stabilizer_size": stabilizer,
        "ordered_pair_count": len(orbit) ** 2,
        "compatible_ordered_pairs": len(compatible),
        "forced_mates_in_orbit": sum(mate in orbit_set for mate in forced_mates),
        "seed_forced_mate": sorted(seed_forced_mate),
        "seed_induced_cube_degrees": list(seed_degrees),
        "forced_mate_induced_cube_degrees": list(mate_degrees),
        "scope": (
            "Exact for the B4 orbit of the displayed eight-Q support only; "
            "it does not classify every characteristic-zero packet branch."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("Q-support-eight B4 incompatibility: PASS")
    print("orbit/stabilizer/pairs:", len(orbit), stabilizer, len(orbit) ** 2)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
