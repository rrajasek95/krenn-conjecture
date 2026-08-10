#!/usr/bin/env python3
"""Test the first cycle/termination invariant after the second one-bad mate.

Take the smallest exact second-route residual from the pinned checker.  It
has two fresh private top words.  For each word, adjoin each of its fourteen
alternate decorated perfect matchings and audit the complete top/response
packet.  All 28 moves strictly enlarge support and create fresh singleton
row-word labels disjoint from every label seen earlier on the branch.  Thus
the first possible private-word cycle does not occur at this layer; the
finite cumulative-label potential strictly increases.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SECOND = "computations/verify_n8_one_bad_second_coupled_repair_residual.py"
SECOND_HASH = "67643e62ccefd0bd82cdcb3ad0ab8388e448ecbde66184516cc1e8fac2c03fae"
EXPECTED_DIGEST = "33334cdddef689629e5fc4d830c154070937abd2bd2fca0ff8753ee530d4ebbf"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_second():
    path = ROOT / SECOND
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == SECOND_HASH,
            f"dependency changed: {SECOND}: {actual}")
    spec = spec_from_file_location("one_bad_second_route", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cell(item):
    return tuple(item[0]), tuple(item[1])


def audit_third_routes(second):
    first = second.load_first()
    base = first.load_base()
    second_audit = second.audit_second_routes(first)
    record = second_audit["smallest_residual"]
    require((record["first_chart"], record["sharp_orbit"],
             record["witness"], record["second_route"]) == (0, 0, 1, 9),
            "the pinned smallest second-route residual changed")

    first_chart = first.audit_mates(base)["charts"][record["first_chart"]]
    packet = base.SHARP_REPRESENTATIVES[record["sharp_orbit"]]
    a_matching, b_matching, b_holes, c_matching, c_holes = packet
    source = (
        tuple((edge, (base.A, base.A)) for edge in a_matching)
        + tuple((edge, (base.B, base.B)) for edge in b_matching)
        + tuple((edge, (base.C, base.C)) for edge in c_matching)
    )
    mate = tuple(cell(item) for item in first_chart["mate"])
    second_cells = tuple(cell(item) for item in record["new_cells"])
    support = source + mate + second_cells
    require(len(support) == len(set(support)) == 11,
            "the smallest second-route support changed")

    # Seen labels include the original private cross word, both first-mate
    # top words (including the selected/repaired one), and every singleton
    # currently present after the second route.
    selected_channel = first_chart["channel"]
    require(selected_channel == "bc", "the pinned channel changed")
    fixed = ((b_holes[0], base.B), (c_holes[1], base.C))
    old_cross = first.endpoint_tensor(source, 2, fixed)
    require(len(old_cross) == 1, "the original private cross word changed")
    ancestor_labels = {(selected_channel, word) for word in old_cross}
    ancestor_labels |= {
        ("top", tuple(witness["word"]))
        for witness in first_chart["private_top_witnesses"]
    }
    ancestor_labels |= {
        (row, word)
        for row, word, monomial in second.defect_fibres(
            first, base, packet, support
        )
    }
    require(len(ancestor_labels) == 6,
            "the branch ancestor-label count changed")

    size_census = Counter()
    fresh_count_census = Counter()
    total_defect_census = Counter()
    repeated_ancestor_census = Counter()
    examples = []
    transitions = 0

    for defect_index, defect in enumerate(
            record["fresh_second_route_singletons"]):
        require(defect["row"] == "top",
                "a pinned fresh residual left the top row")
        word = tuple(defect["word"])
        trigger = frozenset(cell(item) for item in defect["monomial"])
        alternatives = 0
        for route_index, physical in enumerate(
                base.perfect_matchings(base.SITES)):
            route = tuple(
                (edge, (word[edge[0]], word[edge[1]]))
                for edge in physical
            )
            if frozenset(route) == trigger:
                continue
            missing = tuple(value for value in route if value not in support)
            require(missing, "an alternate third route was already supported")
            enlarged = support + missing
            selected_routes = second.decompositions(
                first, enlarged, 3, (), word
            )
            require(len(selected_routes) >= 2,
                    "a third route failed to repair its selected singleton")
            defects = second.defect_fibres(first, base, packet, enlarged)
            fresh = [
                value for value in defects
                if set(value[2]) & set(missing)
            ]
            require(fresh, "a third route created no fresh singleton")
            fresh_labels = {(row, output) for row, output, monomial in fresh}
            repeated = fresh_labels & ancestor_labels
            require(not repeated,
                    f"the first private-word cycle closed: {repeated}")

            alternatives += 1
            transitions += 1
            size_census[len(missing)] += 1
            fresh_count_census[len(fresh_labels)] += 1
            total_defect_census[len(defects)] += 1
            repeated_ancestor_census[len(repeated)] += 1
            if len(examples) < 4:
                examples.append({
                    "source_defect": defect_index,
                    "route_index": route_index,
                    "new_cells": [
                        [list(edge), list(colours)]
                        for edge, colours in missing
                    ],
                    "fresh_labels": [
                        [row, list(output)]
                        for row, output in sorted(fresh_labels)
                    ],
                })
        require(alternatives == 14,
                "a fresh private top word lost an alternate route")

    require(transitions == 28, "the bounded third-route census changed")
    require(size_census == Counter({2: 12, 3: 16}),
            f"third-route support increments changed: {size_census}")
    require(fresh_count_census == Counter({
        5: 8, 6: 4, 8: 2, 10: 4, 12: 10,
    }), f"third-route fresh-label census changed: {fresh_count_census}")
    require(repeated_ancestor_census == Counter({0: 28}),
            "a third route acquired an ancestor label")
    return {
        "starting_support_cells": len(support),
        "ancestor_row_word_labels": len(ancestor_labels),
        "fresh_private_top_words": 2,
        "alternate_routes_per_word": 14,
        "third_route_transitions": transitions,
        "support_increment_census": dict(sorted(size_census.items())),
        "fresh_label_count_census": dict(sorted(fresh_count_census.items())),
        "total_singleton_count_census": dict(
            sorted(total_defect_census.items())
        ),
        "ancestor_repeat_census": dict(
            sorted(repeated_ancestor_census.items())
        ),
        "minimum_fresh_labels": min(fresh_count_census),
        "examples": examples,
        "verdict": (
            "no cycle at the first post-second layer: every forced mate "
            "adds 2 or 3 cells and at least 5 new row-word singleton labels"
        ),
        "finite_potential": (
            "(localized support, cumulative row-word labels), ordered by "
            "strict inclusion; this layer strictly increases both entries"
        ),
        "scope": (
            "the 28 direct mates of the two fresh singleton words on the "
            "smallest second-route chart; no claim beyond this layer"
        ),
    }


def main():
    second = load_second()
    audit = audit_third_routes(second)
    ledger = {
        "second_route_dependency": {"path": SECOND, "sha256": SECOND_HASH},
        "private_word_third_route_potential": audit,
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    print(json.dumps(audit, indent=2, sort_keys=True))
    print("sha256:", digest)
    require(EXPECTED_DIGEST == "TO_BE_FILLED" or digest == EXPECTED_DIGEST,
            f"third-route potential ledger changed: {digest}")


if __name__ == "__main__":
    main()
