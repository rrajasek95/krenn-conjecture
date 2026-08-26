#!/usr/bin/env python3
"""Independent fail-closed referee for the tree/hierarchical round-749 A/B."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import re
from pathlib import Path

from audit_hierarchical_integration import (
    BASELINE_CHECKPOINT_SHA,
    BASELINE_RESULT_SHA,
    BASELINE_VECTORS_SHA,
    PARENT_SOURCE_SHA,
    PRIME,
    Rejection,
    files_equal,
    parse_checkpoint,
    require,
    sha256_file,
    validate_replay_summary,
)


SEQUENTIAL_RESULT_SHA = "78f41eb6e70f04652f0c3738135f81da970cc5764c9fd7e99456ad1a9c0f9e20"
HIERARCHICAL_RESULT_SHA = "d0d10863ee64148471ac9961e772078f2f7f03c78762f492cb23d3b4ea4da12d"
OUTPUT_CHECKPOINT_SHA = "dda7fb5100adfcc24264993899ec2404a3beec0e0f1e96b4f3dd83a2be7d8621"
OUTPUT_VECTORS_SHA = "93e3eeee9d7a356b4caaf59cae5c5b6671e64508004b448895d0296db0bd2bf1"
SEALED_SOURCE_SHA = "af9c66d2a115c47d5363db4ac46bde8bd15ab6c262cf9e2b0a0931b834776a5b"
SEALED_BINARY_SHA = "b66761a196d98370487c44142a3d6ca695afc20f8f9d9bb4c33622c158ba5e6e"
HIERARCHICAL_STDERR_SHA = "81ace0e1fa67775946cd976133bf86771f3196243ffa3ce0087e6a362585ae94"
ROUND = 749
COLUMNS = 334_298
SUPPORT = 418
RSS_LIMIT_GIB = 36


def validate_control(result: dict, kernel: str) -> None:
    require(result.get("schema") == "KRENN_AFFINE251_D12_NATIVE_SPARSE_DUAL_V1",
            "control schema")
    require(result.get("status") == "INCOMPLETE_SEARCH_CAP" and
            result.get("incomplete_reason") == "ROUND_CAP", "control status")
    require((result.get("degree"), result.get("prime"), result.get("group_order")) ==
            (12, PRIME, 1440), "control field")
    require((result.get("provider_equations"), result.get("provider_terms_parsed"),
             result.get("provider_distinct_terms")) == (6561, 688_908, 688_906),
            "provider census")
    require((result.get("rounds_completed"), result.get("column_orbits_exposed"),
             result.get("dual_support")) == (ROUND, COLUMNS, SUPPORT), "output census")
    require((result.get("workers"), result.get("pivot_mode"), result.get("strategy"),
             result.get("incremental_basis"), result.get("elimination_kernel")) ==
            (16, "rare", "cold", False, kernel), "control mode")
    require((result.get("rss_limit_gib"), result.get("wall_limit_seconds")) ==
            (RSS_LIMIT_GIB, 120), "resource declarations")
    require(result.get("cached_vectors_loaded") == 333_199 and
            result.get("vectors_materialized_on_restore") == 0,
            "arbitrary resume did not use exact round748 cache")
    require(isinstance(result.get("rounds"), list) and len(result["rounds"]) == 1,
            "one-round control")
    record = result["rounds"][0]
    require((record.get("round"), record.get("columns"), record.get("new_columns"),
             record.get("dual_support"), record.get("new_support_rows"),
             record.get("selected_strategy"), record.get("selected_pivot")) ==
            (ROUND, COLUMNS, 1099, SUPPORT, 229, "cold", "rare"), "round census")
    for field in ("incident_seconds", "materialize_seconds", "solve_seconds"):
        require(isinstance(record.get(field), (int, float)) and math.isfinite(record[field])
                and record[field] >= 0, f"timer {field}")


def expect_reject(result: dict, kernel: str, label: str) -> None:
    try:
        validate_control(result, kernel)
    except (Rejection, KeyError, TypeError):
        return
    raise Rejection(f"hostile accepted: {label}")


def static_source_contract(source: Path) -> dict:
    text = source.read_text()
    required = [
        '"tree" | "vec" | "hierarchical"',
        'workers != 16 || pivot != "rare" || strategy != "cold" || incremental',
        'SparsePivot::Rare',
        'terms.sort_unstable_by_key(|term| term.rank)',
        'records.sort_unstable_by_key(|item| item.0)',
        'if levels != 4',
        'columns.iter().any(|column| sparse_pairing',
    ]
    missing = [fragment for fragment in required if fragment not in text]
    if ('rows_by_rank.sort_unstable_by' not in text and
            'ordered.sort_unstable_by' not in text):
        missing.append("rare total-order sort")
    require(not missing, f"integration source contract missing {missing}")
    return {
        "total_pivot_order": "(exposed_frequency,Mono)_ascending",
        "column_order": "native sorted Column ascending, contiguous quotient/remainder shards",
        "merge_order": "fixed 16-to-8-to-4-to-2-to-1; right records by ascending pivot rank",
        "all_column_postcondition_present": True,
        "unsupported_modes_fail_closed": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent-source", type=Path, required=True)
    parser.add_argument("--integration-source", type=Path, required=True)
    parser.add_argument("--integration-binary", type=Path, required=True)
    parser.add_argument("--sequential-result", type=Path, required=True)
    parser.add_argument("--hierarchical-result", type=Path, required=True)
    parser.add_argument("--sequential-checkpoint", type=Path, required=True)
    parser.add_argument("--hierarchical-checkpoint", type=Path, required=True)
    parser.add_argument("--sequential-vectors", type=Path, required=True)
    parser.add_argument("--hierarchical-vectors", type=Path, required=True)
    parser.add_argument("--round749-replay", type=Path, required=True)
    parser.add_argument("--hierarchical-stderr", type=Path, required=True)
    parser.add_argument("--hostile-modes", type=Path, required=True)
    parser.add_argument("--resource-evidence", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    require(sha256_file(args.parent_source) == PARENT_SOURCE_SHA, "restored parent source")
    sequential = json.loads(args.sequential_result.read_text())
    hierarchical = json.loads(args.hierarchical_result.read_text())
    require(sha256_file(args.sequential_result) == SEQUENTIAL_RESULT_SHA,
            "sequential result pin")
    require(sha256_file(args.hierarchical_result) == HIERARCHICAL_RESULT_SHA,
            "hierarchical result pin")
    validate_control(sequential, "tree")
    validate_control(hierarchical, "hierarchical")
    seq_checkpoint = parse_checkpoint(args.sequential_checkpoint, OUTPUT_CHECKPOINT_SHA)
    hier_checkpoint = parse_checkpoint(args.hierarchical_checkpoint, OUTPUT_CHECKPOINT_SHA)
    require((seq_checkpoint["round"], len(seq_checkpoint["columns"]),
             seq_checkpoint["support"]) == (ROUND, COLUMNS, SUPPORT),
            "sequential checkpoint census")
    require((hier_checkpoint["round"], len(hier_checkpoint["columns"]),
             hier_checkpoint["support"]) == (ROUND, COLUMNS, SUPPORT),
            "hierarchical checkpoint census")
    require(files_equal(args.sequential_checkpoint, args.hierarchical_checkpoint),
            "checkpoint byte identity")
    require(seq_checkpoint["candidate"] == hier_checkpoint["candidate"],
            "candidate map identity")
    require(sha256_file(args.sequential_vectors) == OUTPUT_VECTORS_SHA and
            sha256_file(args.hierarchical_vectors) == OUTPUT_VECTORS_SHA and
            files_equal(args.sequential_vectors, args.hierarchical_vectors),
            "cache byte identity")
    replay = json.loads(args.round749_replay.read_text())
    require(replay.get("schema") == "KRENN_AFFINE251_D12_CACHE_REPLAY_V1" and
            replay.get("status") == "PASS_ALL_COLUMNS" and
            (replay.get("round"), replay.get("columns_replayed"),
             replay.get("verification_failures")) == (ROUND, COLUMNS, 0),
            "round749 all-column replay")

    # Inspect the supplied integration source and bind it to the sealed A/B.
    source_contract = static_source_contract(args.integration_source)
    actual_source_sha = sha256_file(args.integration_source)
    actual_binary_sha = sha256_file(args.integration_binary)
    producer_pinned = (actual_source_sha == SEALED_SOURCE_SHA and
                       actual_binary_sha == SEALED_BINARY_SHA)
    mode_evidence = json.loads(args.hostile_modes.read_text())
    require(mode_evidence.get("schema") ==
            "KRENN_AFFINE251_D12_HIERARCHICAL_HOSTILE_MODES_V1" and
            mode_evidence.get("status") ==
            "PASS_ALL_UNSUPPORTED_MODES_REJECTED_BEFORE_IO" and
            mode_evidence.get("binary_sha256") == actual_binary_sha and
            len(mode_evidence.get("cases", {})) == 8 and
            all(record.get("pass") is True for record in mode_evidence["cases"].values()),
            "hostile binary mode evidence")

    seq_solve = sequential["rounds"][0]["solve_seconds"]
    hier_solve = hierarchical["rounds"][0]["solve_seconds"]
    speedup = seq_solve / hier_solve
    performance_pass = speedup >= 2.0
    require(sha256_file(args.hierarchical_stderr) == HIERARCHICAL_STDERR_SHA,
            "hierarchical phase log pin")
    phase_match = re.search(
        r"columns=(\d+) variables=(\d+) basis=(\d+) terms=(\d+) "
        r"rank=([0-9.]+)s materialize=([0-9.]+)s "
        r"local_eliminate_critical=([0-9.]+)s local_wall=([0-9.]+)s "
        r"merge=([0-9.]+)s backsolve=([0-9.]+)s verify=([0-9.]+)s support=(\d+)",
        args.hierarchical_stderr.read_text())
    require(phase_match is not None, "hierarchical phase log schema")
    values = phase_match.groups()
    require(tuple(map(int, values[:4])) == (COLUMNS, 21_066_364, 334_288, 34_083_985)
            and int(values[-1]) == SUPPORT, "hierarchical phase census")
    phase_names = ("rank", "materialize", "local_eliminate_critical", "local_wall",
                   "merge", "backsolve", "verify")
    phases = dict(zip(phase_names, map(float, values[4:11])))
    accounted = (phases["rank"] + phases["materialize"] + phases["local_wall"] +
                 phases["merge"] + phases["backsolve"] + phases["verify"])
    require(0 <= hier_solve - accounted < 0.25, "hierarchical phase accounting")
    preparation = phases["rank"] + phases["materialize"]
    promotion_budget = seq_solve / 2.0

    resource_pass = False
    resource_note = "no external macOS hard-RSS evidence"
    resource_details = {}
    if args.resource_evidence is not None:
        evidence = json.loads(args.resource_evidence.read_text())
        resource_pass = (evidence.get("schema") ==
                         "KRENN_AFFINE251_D12_MACOS_RSS_WATCHDOG_V1" and
                         evidence.get("status") == "PASS" and evidence.get("breach") is None and
                         evidence.get("returncode") == 0 and
                         evidence.get("atomic_outputs_clean") is True and
                         evidence.get("source_sha256") == actual_source_sha and
                         evidence.get("binary_sha256") == actual_binary_sha and
                         evidence.get("result_sha256") == HIERARCHICAL_RESULT_SHA and
                         evidence.get("rss_limit_kib") == RSS_LIMIT_GIB * 1024 * 1024 and
                         0 < evidence.get("peak_rss_kib", RSS_LIMIT_GIB * 1024 * 1024) <
                         RSS_LIMIT_GIB * 1024 * 1024)
        resource_note = "external evidence accepted" if resource_pass else "external evidence rejected"
        resource_details = {
            "evidence_sha256": sha256_file(args.resource_evidence),
            "observer": evidence.get("rss_observer"),
            "peak_rss_kib": evidence.get("peak_rss_kib"),
            "sample_count": evidence.get("sample_count"),
            "elapsed_seconds": evidence.get("elapsed_seconds"),
        }

    hostile_checks = []
    for label, field, value in [
        ("stale_schema", "schema", "STALE_V0"),
        ("wrong_round", "rounds_completed", 748),
        ("missing_column", "column_orbits_exposed", COLUMNS - 1),
        ("wrong_workers", "workers", 8),
    ]:
        hostile = copy.deepcopy(hierarchical); hostile[field] = value
        expect_reject(hostile, "hierarchical", label); hostile_checks.append(label)
    hostile = copy.deepcopy(hierarchical)
    hostile["rounds"][0]["selected_pivot"] = "first"
    expect_reject(hostile, "hierarchical", "wrong_pivot")
    hostile_checks.append("wrong_pivot")

    algebra_pass = True
    promotion_pass = algebra_pass and producer_pinned and resource_pass and performance_pass
    verdict = "PASS_PROMOTION" if promotion_pass else "FAIL_CLOSED_DO_NOT_PROMOTE"
    audit = {
        "schema": "KRENN_AFFINE251_D12_GENERIC_HIERARCHICAL_INTEGRATION_AUDIT_V1",
        "status": verdict,
        "restored_parent_source_sha256": PARENT_SOURCE_SHA,
        "accepted_round748_inputs": {
            "result_sha256": BASELINE_RESULT_SHA,
            "checkpoint_sha256": BASELINE_CHECKPOINT_SHA,
            "vectors_sha256": BASELINE_VECTORS_SHA,
        },
        "control_pins": {
            "sequential_result_sha256": SEQUENTIAL_RESULT_SHA,
            "hierarchical_result_sha256": HIERARCHICAL_RESULT_SHA,
            "checkpoint_sha256": OUTPUT_CHECKPOINT_SHA,
            "vectors_sha256": OUTPUT_VECTORS_SHA,
            "sealed_source_sha256": SEALED_SOURCE_SHA,
            "sealed_binary_sha256": SEALED_BINARY_SHA,
            "supplied_source_sha256": actual_source_sha,
            "supplied_binary_sha256": actual_binary_sha,
            "producer_bytes_retained": producer_pinned,
        },
        "schema_preservation": True,
        "arbitrary_resume": {
            "input_round": 748,
            "output_round": 749,
            "cached_vectors_loaded": 333199,
            "vectors_materialized_on_restore": 0,
        },
        "source_contract": source_contract,
        "byte_identity": {
            "candidate": True,
            "checkpoint": True,
            "vector_cache": True,
        },
        "all_column_replay": replay,
        "performance": {
            "sequential_solve_seconds": seq_solve,
            "hierarchical_solve_seconds": hier_solve,
            "sequential_over_hierarchical": speedup,
            "required_speedup": 2.0,
            "pass": performance_pass,
            "phase_log_sha256": HIERARCHICAL_STDERR_SHA,
            "phase_seconds": phases,
            "accounted_seconds": accounted,
            "unattributed_seconds": hier_solve - accounted,
            "rank_plus_materialize_seconds": preparation,
            "rank_plus_materialize_fraction": preparation / hier_solve,
            "two_x_promotion_budget_seconds": promotion_budget,
            "required_total_reduction_seconds": hier_solve - promotion_budget,
            "diagnosis": "Rare-rank construction and exact raw-Mono-to-packed-rank materialization dominate; parallel echelon work is not the bottleneck.",
        },
        "resource_gate": {
            "required_hard_limit_bytes": RSS_LIMIT_GIB * 1024**3,
            "pass": resource_pass,
            "note": resource_note,
            **resource_details,
        },
        "hostile_result_checks": hostile_checks,
        "hostile_binary_modes": {
            "evidence_sha256": sha256_file(args.hostile_modes),
            "binary_sha256": actual_binary_sha,
            "cases": sorted(mode_evidence["cases"]),
            "pass": True,
        },
        "promotion_gate": {
            "algebra": algebra_pass,
            "producer_provenance": producer_pinned,
            "resource": resource_pass,
            "performance": performance_pass,
            "pass": promotion_pass,
        },
        "scope": "One exact round748-to749 A/B only; no continuation or elimination rerun.",
    }
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, args.output)
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()
