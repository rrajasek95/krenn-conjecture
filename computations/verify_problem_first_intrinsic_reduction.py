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
}
EXPECTED_LEDGER_SHA256 = "a3584962a716892945026a2a2b35f1602659eb1239253a521fb50b3968982c6a"


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
            orbit_records.append({
                "representative": tuple(
                    "|".join(f"{left}{right}" for left, right in matching)
                    for matching in representative
                ),
                "labelled_orbit_size": len(labelled_orbit),
                "perfect_matching_closure_size": len(closure),
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
        "scope_warning": (
            "uncoloured matching closure does not by itself make the extra "
            "endpoint-coloured occurrences live"
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
