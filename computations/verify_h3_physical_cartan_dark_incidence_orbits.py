#!/usr/bin/env python3
"""Reduce the unresolved physical-Cartan incidence packets to S6 orbits.

The selected incidence census leaves 151,200 packets in which the chosen
target-full overlap already has rank (3,3), but its endpoint arm is absent
from both selected bright matchings.  Raw packet counts obscure whether the
remaining activity theorem has many genuinely different incidence types.

This checker quotients the exact packet inventory by every permutation of
the six internal sites (fixing the two cap endpoints), and also records the
coarser quotient after the global interchange of bright colours 1 and 2.
No source-row or activity conclusion is inferred from the orbit census.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
P, S = 6, 7
INTERNAL = tuple(range(6))
PINS = {
    "computations/verify_h3_physical_cartan_active_overlap_landing.py":
        "8161ab2f2b1c8de0db01a358d0ed4aad5b48779d04355ef0fc16a186b92c8cbd",
    "notes/h3-physical-cartan-active-overlap-landing.md":
        "8dea46f9b1d606ac4295afbee64865bc0967447be641de17246465361d7ab866",
}
EXPECTED_LEDGER_SHA256 = (
    "019a750af79c662e7e25498fdc7e76480960c54afb6ab9afa65fa8985c9a8fce"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def normalize_matching(matching):
    return tuple(sorted(tuple(sorted(edge)) for edge in matching))


def permute_matching(matching, permutation):
    site_map = dict(zip(INTERNAL, permutation, strict=True))
    site_map.update({P: P, S: S})
    return normalize_matching(
        (site_map[left], site_map[right]) for left, right in matching
    )


def permute_mask(mask, permutation):
    answer = 0
    for old, new in zip(INTERNAL, permutation, strict=True):
        if mask & (1 << old):
            answer |= 1 << new
    return answer


def symmetric_cycle_lengths(first, second):
    first_edges = set(first)
    second_edges = set(second)
    symmetric = first_edges ^ second_edges
    adjacency = {site: set() for site in range(8)}
    for left, right in symmetric:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = set()
    lengths = []
    for site in range(8):
        if site in seen or not adjacency[site]:
            continue
        stack = [site]
        component = set()
        while stack:
            current = stack.pop()
            if current in component:
                continue
            component.add(current)
            stack.extend(adjacency[current] - component)
        seen.update(component)
        require(all(len(adjacency[value]) == 2 for value in component),
                ("matching symmetric difference stopped being cycles", component))
        lengths.append(len(component))
    return tuple(sorted(lengths))


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))


    landing = load(
        "computations/verify_h3_physical_cartan_active_overlap_landing.py",
        "dark_orbit_landing",
    )
    direct = tuple(sorted((P, S)))
    bright = tuple(
        normalize_matching(matching)
        for matching in landing.matchings(tuple(range(8)))
        if direct not in normalize_matching(matching)
    )
    matching_index = {matching: index for index, matching in enumerate(bright)}
    require(len(bright) == len(matching_index) == 90,
            "bright matching inventory changed")

    group = tuple(permutations(INTERNAL))
    matching_actions = []
    mask_actions = []
    for permutation in group:
        matching_actions.append(tuple(
            matching_index[permute_matching(matching, permutation)]
            for matching in bright
        ))
        mask_actions.append(tuple(
            permute_mask(mask, permutation) for mask in range(1 << 6)
        ))

    records = set()
    candidate_records = set()
    candidate_tail_counts = Counter()
    branch_counts = Counter()
    branch_target_full_shared = Counter()
    for first_index, first in enumerate(bright):
        neighbour1 = landing.neighbour(first, S)
        for second_index, second in enumerate(bright):
            neighbour2 = landing.neighbour(second, S)
            for size in range(2, 7):
                for target_full in combinations(INTERNAL, size):
                    target_mask = sum(1 << site for site in target_full)
                    selected_full = set(target_full) & {neighbour1, neighbour2}
                    if neighbour1 != neighbour2 and selected_full:
                        continue
                    if neighbour1 == neighbour2:
                        branch = "shared"
                        branch_target_full_shared[
                            "shared_neighbour_in_F"
                            if neighbour1 in target_full
                            else "shared_neighbour_not_in_F"
                        ] += 1
                    else:
                        require(set(target_full).isdisjoint(
                            {neighbour1, neighbour2}),
                            "distinct residual stopped avoiding both neighbours")
                        branch = "avoiding"
                    records.add((first_index, second_index, target_mask))
                    branch_counts[branch] += 1

            for site in INTERNAL:
                if site not in {neighbour1, neighbour2}:
                    candidate_records.add((first_index, second_index, site))
                    common_internal_tails = {
                        edge for edge in set(first) & set(second)
                        if P not in edge and S not in edge and site not in edge
                    }
                    candidate_tail_counts[
                        "has_common_selected_internal_tail"
                        if common_internal_tails
                        else "no_common_selected_internal_tail"
                    ] += 1

    require(len(records) == 151200 and branch_counts == {
        "shared": 76950,
        "avoiding": 74250,
    }, ("dark packet inventory changed", len(records), branch_counts))
    require(branch_target_full_shared == {
        "shared_neighbour_in_F": 41850,
        "shared_neighbour_not_in_F": 35100,
    }, ("shared-neighbour split changed", branch_target_full_shared))
    require(len(candidate_records) == 33750,
            ("dark candidate-arm inventory changed", len(candidate_records)))
    require(sum(candidate_tail_counts.values()) == len(candidate_records),
            "candidate common-tail split changed")

    remaining = set(records)
    ordered_orbits = []
    colour_swap_orbits = []
    while remaining:
        seed = min(remaining)
        first_index, second_index, mask = seed
        orbit = {
            (matching_action[first_index], matching_action[second_index],
             mask_action[mask])
            for matching_action, mask_action in zip(
                matching_actions, mask_actions, strict=True)
        }
        orbit &= records
        require(orbit <= remaining,
                "internal S6 orbits overlapped after removal")
        remaining.difference_update(orbit)
        ordered_orbits.append((seed, len(orbit)))

    remaining = set(records)
    while remaining:
        seed = min(remaining)
        first_index, second_index, mask = seed
        orbit = set()
        for matching_action, mask_action in zip(
                matching_actions, mask_actions, strict=True):
            first_image = matching_action[first_index]
            second_image = matching_action[second_index]
            mask_image = mask_action[mask]
            orbit.add((first_image, second_image, mask_image))
            orbit.add((second_image, first_image, mask_image))
        orbit &= records
        require(orbit <= remaining,
                "S6 x bright-swap orbits overlapped after removal")
        remaining.difference_update(orbit)
        colour_swap_orbits.append((seed, len(orbit)))

    def invariant(seed):
        first_index, second_index, mask = seed
        first, second = bright[first_index], bright[second_index]
        neighbour1 = landing.neighbour(first, S)
        neighbour2 = landing.neighbour(second, S)
        target_full = {site for site in INTERNAL if mask & (1 << site)}
        common = set(first) & set(second)
        return {
            "branch": "shared" if neighbour1 == neighbour2 else "avoiding",
            "target_full_size": len(target_full),
            "shared_neighbour_target_full": (
                neighbour1 in target_full if neighbour1 == neighbour2 else None
            ),
            "common_physical_edges": len(common),
            "symmetric_cycle_lengths": list(symmetric_cycle_lengths(first, second)),
        }

    ordered_invariants = Counter()
    for seed, orbit_size in ordered_orbits:
        inv = invariant(seed)
        key = tuple(sorted((name, repr(value)) for name, value in inv.items()))
        ordered_invariants[(key, orbit_size)] += 1

    colour_swap_invariants = Counter()
    for seed, orbit_size in colour_swap_orbits:
        inv = invariant(seed)
        key = tuple(sorted((name, repr(value)) for name, value in inv.items()))
        colour_swap_invariants[(key, orbit_size)] += 1

    candidate_remaining = set(candidate_records)
    candidate_orbits = []
    while candidate_remaining:
        seed = min(candidate_remaining)
        first_index, second_index, site = seed
        orbit = set()
        for matching_action, permutation in zip(
                matching_actions, group, strict=True):
            site_image = permutation[site]
            first_image = matching_action[first_index]
            second_image = matching_action[second_index]
            orbit.add((first_image, second_image, site_image))
            orbit.add((second_image, first_image, site_image))
        orbit &= candidate_records
        require(orbit <= candidate_remaining,
                "candidate-arm orbits overlapped after removal")
        candidate_remaining.difference_update(orbit)
        candidate_orbits.append((seed, len(orbit)))

    def candidate_invariant(seed):
        first_index, second_index, site = seed
        first, second = bright[first_index], bright[second_index]
        neighbour1 = landing.neighbour(first, S)
        neighbour2 = landing.neighbour(second, S)
        partner1 = landing.neighbour(first, site)
        partner2 = landing.neighbour(second, site)
        return {
            "branch": "shared" if neighbour1 == neighbour2 else "avoiding",
            "site_is_P_neighbour_colour1": partner1 == P,
            "site_is_P_neighbour_colour2": partner2 == P,
            "same_site_partner": partner1 == partner2,
            "common_physical_edges": len(set(first) & set(second)),
            "common_internal_tail_avoiding_site": any(
                P not in edge and S not in edge and site not in edge
                for edge in set(first) & set(second)
            ),
            "symmetric_cycle_lengths": list(symmetric_cycle_lengths(first, second)),
        }

    candidate_invariants = Counter()
    candidate_examples = []
    for seed, orbit_size in candidate_orbits:
        inv = candidate_invariant(seed)
        key = tuple(sorted((name, repr(value)) for name, value in inv.items()))
        candidate_invariants[(key, orbit_size)] += 1
        first_index, second_index, site = seed
        candidate_examples.append({
            "matching1": [list(edge) for edge in bright[first_index]],
            "matching2": [list(edge) for edge in bright[second_index]],
            "candidate_site": site,
            "orbit_size": orbit_size,
            "invariant": inv,
        })


    return {
        "theorem": "physical Cartan dark incidence orbit reduction",
        "raw_dark_packets": len(records),
        "raw_branches": dict(sorted(branch_counts.items())),
        "shared_neighbour_split": dict(sorted(branch_target_full_shared.items())),
        "internal_site_symmetry_order": len(group),
        "ordered_bright_colour_orbits": len(ordered_orbits),
        "orbits_mod_global_bright_swap": len(colour_swap_orbits),
        "candidate_arm_records": len(candidate_records),
        "candidate_common_tail_split": dict(sorted(candidate_tail_counts.items())),
        "candidate_arm_orbits_mod_bright_swap": len(candidate_orbits),
        "ordered_orbit_size_histogram": dict(sorted(Counter(
            size for _seed, size in ordered_orbits
        ).items())),
        "colour_swap_orbit_size_histogram": dict(sorted(Counter(
            size for _seed, size in colour_swap_orbits
        ).items())),
        "ordered_invariant_orbit_histogram": {
            repr(key): count for key, count in sorted(
                ordered_invariants.items(), key=repr
            )
        },
        "colour_swap_invariant_orbit_histogram": {
            repr(key): count for key, count in sorted(
                colour_swap_invariants.items(), key=repr
            )
        },
        "candidate_invariant_orbit_histogram": {
            repr(key): count for key, count in sorted(
                candidate_invariants.items(), key=repr
            )
        },
        "candidate_orbit_examples": candidate_examples,
        "scope": (
            "incidence and physical matching symmetry only.  A physical "
            "Cartan direction at an arm absent from the two selected bright "
            "matchings is not declared active, and no complete-row "
            "dependence is inferred"
        ),
    }


def main():
    ledger = audit()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("dark-incidence orbit ledger changed", digest))
    print("h3 physical Cartan dark-incidence orbits: PASS")
    print("raw packets:", ledger["raw_dark_packets"])
    print("ordered S6 orbits:", ledger["ordered_bright_colour_orbits"])
    print("mod bright swap:", ledger["orbits_mod_global_bright_swap"])
    print("candidate arm orbits:", ledger["candidate_arm_orbits_mod_bright_swap"])
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
