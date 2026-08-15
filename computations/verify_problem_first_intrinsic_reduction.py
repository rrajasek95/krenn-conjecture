#!/usr/bin/env python3
"""Audit the problem-first reduction and the literal thirteen-exit packet.

This checker does not claim the thirteen-exit lemma.  It pins the two exact
inputs that expose it, reconstructs the matching/cap classification, and
checks the logical minimal-counterexample reduction separately from the open
local theorem.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_c6_unspecialized_eqsystem_parent_antidiagonal_spair.py":
        "584c36d076224fcc437b70998a43091ffa0f19b35bfbe73fea0caf1d7ae9865a",
    "notes/2026-08-14-c6-unspecialized-eqsystem-parent-antidiagonal-spair.md":
        "b15dd110cf28826751e5f32e162c91c7990cf119ed4a1c0361403dcf4ad0a369",
    "computations/verify_n8_common_edge_dirty_signature_realization_no_go.py":
        "3ec852cc796040e29189f72ecc02152cd43db7cee1abfd7aad636ea41fe16530",
    "notes/2026-08-14-n8-common-edge-dirty-signature-realization-no-go.md":
        "1dc67039e32eaa0087f59a80b99adc89f306b3a0d5ef2e5662baa10d1af66427",
    "computations/verify_clean_pair_cap_exact_descent_symbolic.py":
        "d6507c2afa341ce5c15056feddf92b9a171e2a5c80652617b595c7c7cf35acf5",
    "proofs/six-site-arbitrary-complex-obstruction.md":
        "b36b2f9ccb577af0aebf897edfc9fa1f84d01ba0cf4ea49ac11799d992e00713",
    "computations/verify_c6_transverse_seed_spk6_certificate_lift_gate.py":
        "a46d212cc4ac1ddbd794c0e3eb163b342fccbd040619c0e9e6fe3fbe5d355270",
    "notes/2026-08-14-c6-transverse-seed-conditioned-spk6-certificate-lift.md":
        "bfa3b69d5287d8e4b13de32a844b305806d8cc1d74b41a6b173dc3d3e68236a5",
}
EXPECTED_LEDGER_SHA256 = "2228ee7d3af0445d13a4df1b4a318eca6a19645cab9aa31a4381525cb22074e8"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


def cycle_length(left: frozenset[tuple[int, int]],
                 right: frozenset[tuple[int, int]]) -> int:
    difference = left ^ right
    require(len(difference) in (4, 6), (left, right, difference))
    return len(difference)


def pin_inputs() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned input changed", relative,
                                     actual, expected))


def packet_audit() -> dict[str, object]:
    matchings = tuple(frozenset(matching)
                      for matching in perfect_matchings(tuple(range(6))))
    require(len(matchings) == 15 and len(set(matchings)) == 15,
            len(matchings))
    m0 = frozenset(((0, 5), (1, 2), (3, 4)))
    m1 = frozenset(((0, 1), (2, 5), (3, 4)))
    require(m0 in matchings and m1 in matchings and cycle_length(m0, m1) == 4,
            (m0, m1))
    exits = tuple(matching for matching in matchings
                  if matching not in (m0, m1))
    c4 = tuple(matching for matching in exits
               if min(cycle_length(matching, m0),
                      cycle_length(matching, m1)) == 4)
    c6 = tuple(matching for matching in exits
               if cycle_length(matching, m0) == 6
               and cycle_length(matching, m1) == 6)
    require((len(exits), len(c4), len(c6)) == (13, 9, 4),
            (len(exits), len(c4), len(c6)))

    direct = tuple(matching for matching in matchings
                   if (3, 4) in matching)
    crossed = tuple(matching for matching in matchings
                    if (3, 4) not in matching)
    require(len(direct) == 3 and len(crossed) == 12,
            (direct, crossed))
    third_direct = frozenset(((0, 2), (1, 5), (3, 4)))
    require(set(direct) == {m0, m1, third_direct}, direct)

    words = ("111001", "111221")
    residual_words = tuple(word[:3] + word[5] for word in words)
    cap_colours = tuple(word[3:5] for word in words)
    require(residual_words == ("1111", "1111"), residual_words)
    require(cap_colours == ("00", "22"), cap_colours)
    return {
        "perfect_matchings": len(matchings),
        "selected_parents": ["05|12|34", "01|25|34"],
        "parent_symmetric_difference": "C4",
        "exits": len(exits),
        "exit_alternating_cycle_types": {"C4_from_a_parent": len(c4),
                                          "C6_from_both": len(c6)},
        "cap_34_partition": {"direct": len(direct),
                             "crossed": len(crossed)},
        "third_direct": "02|15|34",
        "mixed_sections": list(words),
        "cap_colours": list(cap_colours),
        "common_residual_word": residual_words[0],
    }


def transform_matching(matching: tuple[tuple[int, int], ...],
                       permutation: tuple[int, ...]):
    return tuple(sorted(tuple(sorted((permutation[left], permutation[right])))
                        for left, right in matching))


def balanced_bipartition(edges: set[tuple[int, int]]):
    vertices = set(range(6))
    for left_tuple in combinations(range(6), 3):
        left = set(left_tuple)
        right = vertices - left
        if all((u in left) != (v in left) for u, v in edges):
            return tuple(sorted(left)), tuple(sorted(right))
    return None


def disjoint_channel_audit() -> dict[str, object]:
    """Classify the no-common-tail fine-channel hard core on six sites."""
    matchings = tuple(perfect_matchings(tuple(range(6))))
    site_permutations = tuple(permutations(range(6)))
    records = {}
    expected = {
        3: {"families": 80, "orbits": 2, "orbit_sizes": (20, 60),
            "closure_sizes": (4, 6)},
        4: {"families": 30, "orbits": 1, "orbit_sizes": (30,),
            "closure_sizes": (8,)},
        5: {"families": 6, "orbits": 1, "orbit_sizes": (6,),
            "closure_sizes": (15,)},
    }
    for size in (3, 4, 5):
        families = {
            tuple(sorted(family))
            for family in combinations(matchings, size)
            if len(set().union(*(set(matching) for matching in family)))
            == 3 * size
        }
        unseen = set(families)
        orbit_records = []
        while unseen:
            representative = min(unseen)
            orbit = {
                tuple(sorted(transform_matching(matching, permutation)
                             for matching in representative))
                for permutation in site_permutations
            }
            labelled_orbit = orbit & families
            unseen -= labelled_orbit
            edge_union = set().union(*(set(matching)
                                      for matching in representative))
            closure = tuple(matching for matching in matchings
                            if set(matching) <= edge_union)
            partition = balanced_bipartition(edge_union)
            contamination = None
            if partition is not None:
                left = set(partition[0])
                outside = tuple(matching for matching in matchings
                                if matching not in closure)
                profiles = []
                for matching in outside:
                    internal_left = sum(u in left and v in left
                                        for u, v in matching)
                    internal_right = sum(u not in left and v not in left
                                         for u, v in matching)
                    cross = 3 - internal_left - internal_right
                    profiles.append((internal_left, internal_right, cross))
                    require((internal_left, internal_right, cross) == (1, 1, 1),
                            (partition, matching, profiles[-1]))
                    require(any(set(matching) & set(fine)
                                for fine in closure), (matching, closure))
                contamination = {
                    "outside_fines": len(outside),
                    "outside_profile": "one L-edge, one R-edge, one cross-edge",
                    "every_outside_fine_has_common_tail_with_K33": True,
                }
            orbit_records.append({
                "representative": tuple(
                    "|".join(f"{left}{right}" for left, right in matching)
                    for matching in representative
                ),
                "labelled_orbit_size": len(labelled_orbit),
                "perfect_matching_closure_size": len(closure),
                "balanced_bipartition": partition,
                "outside_contamination": contamination,
            })
        actual = {
            "families": len(families),
            "orbits": len(orbit_records),
            "orbit_sizes": tuple(sorted(record["labelled_orbit_size"]
                                        for record in orbit_records)),
            "closure_sizes": tuple(sorted(
                record["perfect_matching_closure_size"]
                for record in orbit_records
            )),
        }
        require(actual == expected[size], (size, actual, expected[size]))
        records[str(size)] = {
            **actual,
            "representatives": tuple(sorted(
                orbit_records,
                key=lambda record: record["representative"],
            )),
        }
    return {
        "condition": "all fine matchings pairwise edge-disjoint",
        "maximum_channels": 5,
        "sizes": records,
        "consequence": (
            "after common-tail branches are removed, only four S6 channel "
            "geometries remain; every geometry has extra perfect matchings "
            "in its uncoloured edge-union closure"
        ),
        "K33_reduction": (
            "the closure-6 three-channel orbit is K3,3; contamination "
            "outside its six permutation fines always has a common-tail C4, "
            "so the genuinely tail-free contamination is a six-term "
            "endpoint-coloured permanent problem"
        ),
        "scope_warning": (
            "uncoloured matching closure does not by itself make the extra "
            "endpoint-coloured occurrences live"
        ),
    }


def uniform_tail_boundary_audit() -> dict[str, object]:
    local = frozenset(((0, 1), (2, 3), (4, 5), (6, 7)))
    crossing = frozenset(((0, 1), (2, 3), (4, 6), (5, 7)))
    third = frozenset(((0, 1), (2, 3), (4, 7), (5, 6)))
    common = local & crossing
    require(common == frozenset(((0, 1), (2, 3))), common)
    require(local ^ crossing == frozenset(
        ((4, 5), (6, 7), (4, 6), (5, 7))
    ), local ^ crossing)
    require(third - common == frozenset(((4, 7), (5, 6))), third)
    compatible = tuple(
        frozenset(matching)
        for matching in perfect_matchings(tuple(range(8)))
        if frozenset(matching) <= (local | crossing | third)
    )
    require(set(compatible) == {local, crossing, third}, compatible)
    return {
        "common_tail_lift": (
            "mixed singleton times a labelled Cartesian tail family"
        ),
        "first_nonlift_order": 8,
        "first_nonlift_word": "00000122",
        "two_occurrences": ["01|23|45|67", "01|23|46|57"],
        "literal_common_factor": "a01^00*a23^00",
        "residual_K22_matchings": ["45|67", "46|57"],
        "missing_third_matching": "47|56",
        "classification": (
            "one source-labelled K2,2 binomial with a two-edge common tail"
        ),
        "next_intrinsic_test": (
            "three-colour completion of this K2,2, including the missing "
            "matching and every crossing-tail contaminant"
        ),
    }


def induction_audit() -> dict[str, object]:
    # Audit the logical spine on arbitrarily long finite prefixes.  The
    # mathematical implication is ordinary well-ordering: a bad set has a
    # least even order; the trichotomy refutes it or constructs a smaller
    # bad representative/order.
    checked = []
    for maximum in range(6, 202, 2):
        bad_orders = set(range(6, maximum + 1, 2))
        bad_orders.discard(6)  # certified six-site obstruction
        while bad_orders:
            least = min(bad_orders)
            require(least >= 8, least)
            descended = least - 2
            # Under the open intrinsic trichotomy, unit/reduction refutes
            # the least source and a clean cap creates this smaller order.
            require(descended < least, (least, descended))
            require(descended == 6 or descended in range(8, least, 2),
                    (least, descended))
            bad_orders.remove(least)
        checked.append(maximum)
    return {
        "base_order": 6,
        "prefixes_checked": len(checked),
        "largest_even_order_checked": checked[-1],
        "logical_input": "intrinsic minimal-source trichotomy",
        "status_of_input": "OPEN",
        "conclusion_if_input_holds": "no bad even order",
    }


def build_ledger(mode: str) -> dict[str, object]:
    pin_inputs()
    return {
        "theorem": "problem-first intrinsic reduction scope",
        "mode": mode,
        "packet": packet_audit(),
        "no_common_tail_channels": disjoint_channel_audit(),
        "uniform_tail_boundary": uniform_tail_boundary_audit(),
        "induction": induction_audit(),
        "proved_inputs": {
            "six_site_obstruction": True,
            "clean_pair_descent": True,
            "degree_four_parent_packet": True,
            "common_edge_dirty_guard_refuted": True,
        },
        "open_claims_not_asserted": [
            "thirteen-exit lemma",
            "uniform terminal-ear recurrence",
            "full conjecture",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    arguments = parser.parse_args()
    ledger = build_ledger(arguments.mode)
    frozen = dict(ledger)
    frozen["mode"] = "all"
    digest = sha256(json.dumps(frozen, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    print(json.dumps({"status": "PASS", "mode": arguments.mode,
                      "ledger_sha256": digest,
                      "packet": ledger["packet"],
                      "open": ledger["open_claims_not_asserted"]},
                     sort_keys=True))


if __name__ == "__main__":
    main()
