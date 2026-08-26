#!/usr/bin/env python3
"""Retest the complete quadratic ledger inside the 19-row closure only."""

from pathlib import Path
import argparse
import json
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_colour_only_hamming_certificate import (
    EXPECTED_ACTIVE, build_generators, run_certificate,
)
from audit_first_edge_deviation_lift import EDGES, literal_target, literal_word
from audit_same_edge_second_order_lift import run_edge
from audit_two_edge_second_order_lift import DEFAULT_PAIRS, run_pair


RESULTS = HERE / "results_closure19_quadratic_lift.json"


def run_audit():
    closure_words = json.loads(
        (HERE / "results_first_edge_lift_support.json").read_text()
    )["union_words"]
    generator_map = {
        "".join(map(str, word)): (word, poly)
        for word, poly in build_generators()
    }
    generators = [generator_map[word] for word in closure_words]
    certificate = run_certificate()
    target = literal_target()
    literal_active = {
        word: literal_word(tuple(map(int, word))) for word in EXPECTED_ACTIVE
    }
    same_edge = {}
    for edge in EDGES:
        same_edge[f"{edge[0]}{edge[1]}"] = run_edge(
            edge, generators, certificate["active_multipliers"], target,
            literal_active,
        )
    mixed = {}
    for left, right in DEFAULT_PAIRS:
        label = f"{left[0]}{left[1]},{right[0]}{right[1]}"
        mixed[label] = run_pair(
            left, right, generators, certificate["active_multipliers"],
            target, literal_active,
        )
    nonzero = sum(item["nonzero"] for item in same_edge.values()) + sum(
        item["nonzero"] for item in mixed.values()
    )
    return {
        "status": (
            "PASS 19-row closure contains the tested quadratic lifts"
            if nonzero == 0 else
            "NONZERO quadratic obstruction outside 19-row closure"
        ),
        "closure_rows": len(generators),
        "same_edge_directions_checked": sum(item["checked"] for item in same_edge.values()),
        "mixed_pair_directions_checked": sum(item["checked"] for item in mixed.values()),
        "nonzero_remainders": nonzero,
        "same_edge_results": same_edge,
        "mixed_pair_results": mixed,
        "scope": (
            "All same-edge quadratic directions are exhaustive. Mixed-edge "
            "directions are exact only for the six stored geometry representatives."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = run_audit()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        RESULTS.write_text(text)
    if args.check_results and RESULTS.read_text() != text:
        raise RuntimeError("stored closure19 quadratic result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
