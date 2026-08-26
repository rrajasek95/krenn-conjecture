#!/usr/bin/env python3
"""Exact no-gap K23 direct-K15 merger with aggregate-only wall metadata.

The sealed v1 merger correctly validates every atomic shard, but incorrectly
feeds the sum of eight shard wall times back through the single-run <600 second
gate.  This version preserves the v1 source and production contract unchanged,
uses a distinct merged schema, and fail-closes on every shard individually.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import sys

import k23_direct_k15_contract as C


MERGED_ONLY_KEYS = {"shard_count", "elapsed_seconds_sum",
                    "maximum_shard_elapsed_seconds"}
SINGLE_RUN_WALL_KEYS = {"elapsed_seconds", "projected_full_seconds"}
MERGED_TOP_KEYS = (C.TOP_KEYS - SINGLE_RUN_WALL_KEYS) | MERGED_ONLY_KEYS


def atomic_json(path, value):
    C.require(not path.exists(), f"refuse overwrite: {path}")
    temporary = Path(str(path) + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def add_lists(rows, key):
    return [sum(row[key][index] for row in rows) for index in range(len(rows[0][key]))]


def validate_merged_result_data(answer, shards):
    """Validate merged content without misrepresenting aggregate wall time."""
    C.exact_keys(answer, MERGED_TOP_KEYS, "merged result")
    C.require(answer["status"] == "PASS_COMPLETE_GROUPED_DIRECT_K15_FOUR_SINK_K23_CHARGE",
              "merged status")
    C.require(answer["shard_count"] == len(C.INTERVALS) == len(shards),
              "merged shard count")
    walls = [row["elapsed_seconds"] for row in shards]
    C.require(all(type(value) in (int, float) and 0 <= value < 600 for value in walls),
              "atomic shard wall gate")
    C.require(abs(answer["elapsed_seconds_sum"] - sum(walls)) < 1e-9,
              "aggregate elapsed sum")
    C.require(abs(answer["maximum_shard_elapsed_seconds"] - max(walls)) < 1e-9,
              "maximum shard elapsed")

    # Reuse the sealed structural/arithmetic validator with valid single-run
    # wall metadata only in memory.  Those keys never enter the merged file.
    structural = dict(answer)
    for key in MERGED_ONLY_KEYS:
        structural.pop(key)
    maximum = answer["maximum_shard_elapsed_seconds"]
    structural["elapsed_seconds"] = maximum
    structural["projected_full_seconds"] = maximum
    C.validate_result_data(structural, (0, C.SLICES), production=False)

    # Hostile regression: the aggregate sum is not a valid single-run wall and
    # must still be rejected by the frozen shard/result contract.
    hostile = dict(structural)
    hostile["elapsed_seconds"] = answer["elapsed_seconds_sum"]
    hostile["projected_full_seconds"] = answer["elapsed_seconds_sum"]
    try:
        C.validate_result_data(hostile, (0, C.SLICES), production=False)
    except C.ContractError as error:
        C.require("elapsed wall gate" in str(error), "wrong hostile rejection")
    else:
        raise C.ContractError("aggregate wall time accepted as a single run")
    return True


def merged_result(shards):
    answer_sinks = {}
    for name, degrees in zip(C.NAMES, C.PATHS):
        rows = [shard["sinks"][name] for shard in shards]
        histogram = Counter()
        for row in rows:
            histogram.update(row["denominator_product_hist"])
        answer_sinks[name] = {
            "ids": C.IDS[name], "individual_id_charges": None, "degrees": degrees,
            "source_heads": sum(row["source_heads"] for row in rows),
            "source_mass": str(sum(int(row["source_mass"]) for row in rows)),
            "source_l1": str(sum(int(row["source_l1"]) for row in rows)),
            "stage_pivot_uses": add_lists(rows, "stage_pivot_uses"),
            "stage_tail_candidates": add_lists(rows, "stage_tail_candidates"),
            "stage_pivotable_children": add_lists(rows, "stage_pivotable_children"),
            "terminal_response_keys_evaluated": sum(row["terminal_response_keys_evaluated"] for row in rows),
            "terminal_K23_occurrences": sum(row["terminal_K23_occurrences"] for row in rows),
            "full_occurrences": sum(row["full_occurrences"] for row in rows),
            "irreducible_occurrences": sum(row["irreducible_occurrences"] for row in rows),
            "full_charge_scaled_U": str(sum(int(row["full_charge_scaled_U"]) for row in rows)),
            "irreducible_charge_scaled_U": str(sum(int(row["irreducible_charge_scaled_U"]) for row in rows)),
            "denominator_product_hist": dict(sorted(histogram.items(), key=lambda item: int(item[0]))),
        }
    walls = [shard["elapsed_seconds"] for shard in shards]
    answer = {
        "status": "PASS_COMPLETE_GROUPED_DIRECT_K15_FOUR_SINK_K23_CHARGE",
        "scale_U": str(C.U), "slice_interval": [0, C.SLICES],
        "source_slices": C.SLICES, "source_heads_per_slice": C.HEADS_PER_SLICE,
        "workers": 8, "sinks": answer_sinks,
        "packet_grouping_guard": C.PACKET_GUARD, "sign_rule": C.SIGN_RULE,
        "terminality": C.TERMINALITY, "scope": C.SCOPE,
        "shard_count": len(shards),
        "elapsed_seconds_sum": sum(walls),
        "maximum_shard_elapsed_seconds": max(walls),
    }
    validate_merged_result_data(answer, shards)
    for sink in answer_sinks.values():
        C.require((sink["source_heads"], int(sink["source_mass"]), int(sink["source_l1"])) ==
                  (6_704_640, 322_486_272, 3_085_516_800), "frozen full source census")
    return answer


def fragment(result, evidence_path, evidence_sha):
    groups = []
    for group_id, name in zip(C.GROUP_IDS, C.NAMES):
        scaled = int(result["sinks"][name]["full_charge_scaled_U"])
        value = Fraction(scaled, C.U)
        groups.append({
            "group_id": group_id, "ids": C.IDS[name],
            "full_scaled_U": str(scaled), "irreducible_scaled_U": str(scaled),
            "full": str(value), "irreducible": str(value),
            "evidence_path": str(evidence_path), "evidence_sha256": evidence_sha,
        })
    return {
        "degree": 23, "scale_U": C.U, "groups": groups,
        "scope": "strict grouped fragment for exactly 12 frozen K23 IDs; four direct-K15 source scalars counted once each",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard", type=Path, action="append", default=[])
    parser.add_argument("--merged-output", type=Path, required=True)
    parser.add_argument("--fragment-output", type=Path, required=True)
    parser.add_argument("--ledger-output", type=Path, required=True)
    args = parser.parse_args()
    try:
        C.require(len(args.shard) == 8, "exactly eight shards required")
        accepted = []
        for path in args.shard:
            data, digest = C.validate_result(path.resolve(), production=True)
            accepted.append((tuple(data["slice_interval"]), path.resolve(), digest, data))
        accepted.sort()
        C.validate_interval_set([row[0] for row in accepted])
        result = merged_result([row[3] for row in accepted])
        atomic_json(args.merged_output, result)
        merged_sha = C.sha256(args.merged_output)
        evidence_relative = args.merged_output.resolve().relative_to(C.ROOT.resolve())
        piece = fragment(result, evidence_relative, merged_sha)
        atomic_json(args.fragment_output, piece)
        fragment_sha = C.sha256(args.fragment_output)
        ledger = {
            "status": "PASS_K23_DIRECT_K15_EIGHT_SHARD_NO_GAP_MERGE_V2",
            "degree": 23, "scale_U": C.U,
            "intervals": [list(row[0]) for row in accepted],
            "shards": [{"interval": list(row[0]), "path": str(row[1].relative_to(C.ROOT)),
                        "sha256": row[2], "elapsed_seconds": row[3]["elapsed_seconds"]}
                       for row in accepted],
            "merged": {"path": str(args.merged_output.resolve().relative_to(C.ROOT)),
                       "sha256": merged_sha},
            "fragment": {"path": str(args.fragment_output.resolve().relative_to(C.ROOT)),
                         "sha256": fragment_sha},
            "strict_groups": C.GROUP_IDS,
            "strict_ids": [item for name in C.NAMES for item in C.IDS[name]],
            "full_source_census": {"slices": 485, "heads": 6704640,
                                   "mass": 322486272, "l1": 3085516800},
            "full_equals_irreducible": True,
            "wall_semantics": {
                "shard_count": result["shard_count"],
                "elapsed_seconds_sum": result["elapsed_seconds_sum"],
                "maximum_shard_elapsed_seconds": result["maximum_shard_elapsed_seconds"],
                "every_shard_below_600_seconds": True,
                "aggregate_as_single_run_hostile_test_rejected": True,
            },
            "engine_and_input_pins": {name: digest for name, (_path, digest) in C.PINS.items()},
        }
        atomic_json(args.ledger_output, ledger)
    except (C.ContractError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"REJECT: {error}", file=sys.stderr)
        raise SystemExit(2)
    print(json.dumps({"status": ledger["status"], "merged_sha256": merged_sha,
                      "fragment_sha256": fragment_sha,
                      "elapsed_seconds_sum": result["elapsed_seconds_sum"],
                      "maximum_shard_elapsed_seconds": result["maximum_shard_elapsed_seconds"]},
                     indent=2))


if __name__ == "__main__":
    main()
