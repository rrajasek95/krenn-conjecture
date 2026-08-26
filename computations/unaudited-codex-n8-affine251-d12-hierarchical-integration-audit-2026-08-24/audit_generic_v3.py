#!/usr/bin/env python3
"""Independent exact referee for the sealed sharded-rank generic v3 A/B."""

from __future__ import annotations

import argparse
import copy
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
)


ROUND = 749
COLUMNS = 334_298
SUPPORT = 418
SEQUENTIAL_RESULT_SHA = "78f41eb6e70f04652f0c3738135f81da970cc5764c9fd7e99456ad1a9c0f9e20"
V3_RESULT_SHA = "cf0b7a3c7238df24fad17c1935db914d812ebfdb024f99f28982108f611abff2"
OUTPUT_CHECKPOINT_SHA = "dda7fb5100adfcc24264993899ec2404a3beec0e0f1e96b4f3dd83a2be7d8621"
OUTPUT_VECTORS_SHA = "93e3eeee9d7a356b4caaf59cae5c5b6671e64508004b448895d0296db0bd2bf1"
V3_SOURCE_SHA = "173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a"
V3_BINARY_SHA = "8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a"
V3_STDERR_SHA = "94af84b974e555e545b676f486eeda4414aa2bd9d14c7e4d8e3aab1eb7ad686c"
V3_WATCHDOG_SHA = "bd5eabdbc68d86f33e61104c3ac57dd881e919ccc36a9dfeb77b1116e79e3a35"
RANK_GATE_SOURCE_SHA = "d6e259fb67c9e51e3cd6c7c3d3684870a53c684584c0cf5b7fb1cc6b50a3ae44"
RANK_GATE_BINARY_SHA = "5ab53be4c8ae8770fec8bfb69c6f8d5e267386138d22b3b75787f10231e8a185"
RANK_GATE_RESULT_SHAS = (
    "42381082b8f88086da1f6ae9b8276411cd301251dfa218df6f969e69b01e7fb0",
    "e0c66bae143e0b40aacc5302eb2ea557a60c2231200682b9a524cc0c88bc11a8",
    "33b2cf32a25362940dea0f0023dc8d781cd37a40aae860cce5e44b0c79e52377",
)
RSS_LIMIT_KIB = 36 * 1024 * 1024


def function_text(source: str, name: str) -> str:
    marker = f"fn {name}("
    start = source.find(marker)
    require(start >= 0, f"missing function {name}")
    brace = source.find("{", start)
    require(brace >= 0, f"missing function body {name}")
    depth = 0
    for index in range(brace, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[start:index + 1]
    raise Rejection(f"unterminated function {name}")


def validate_native_result(result: dict, kernel: str) -> None:
    require(result.get("schema") == "KRENN_AFFINE251_D12_NATIVE_SPARSE_DUAL_V1",
            "native result schema")
    require(result.get("status") == "INCOMPLETE_SEARCH_CAP" and
            result.get("incomplete_reason") == "ROUND_CAP", "one-round result status")
    require((result.get("degree"), result.get("prime"), result.get("group_order")) ==
            (12, PRIME, 1440), "native field")
    require((result.get("provider_equations"), result.get("provider_terms_parsed"),
             result.get("provider_distinct_terms")) == (6561, 688_908, 688_906),
            "provider census")
    require((result.get("rounds_completed"), result.get("column_orbits_exposed"),
             result.get("dual_support")) == (ROUND, COLUMNS, SUPPORT), "output census")
    require((result.get("workers"), result.get("pivot_mode"), result.get("strategy"),
             result.get("elimination_kernel"), result.get("incremental_basis")) ==
            (16, "rare", "cold", kernel, False), "solver mode")
    require(result.get("rss_limit_gib") == 36 and result.get("wall_limit_seconds") == 120,
            "resource declarations")
    require(result.get("cached_vectors_loaded") == 333_199 and
            result.get("vectors_materialized_on_restore") == 0,
            "round748 arbitrary resume")
    require(isinstance(result.get("rounds"), list) and len(result["rounds"]) == 1,
            "one-round scope")
    row = result["rounds"][0]
    require((row.get("round"), row.get("columns"), row.get("new_columns"),
             row.get("dual_support"), row.get("new_support_rows"),
             row.get("selected_strategy"), row.get("selected_pivot")) ==
            (ROUND, COLUMNS, 1099, SUPPORT, 229, "cold", "rare"), "round census")
    for field in ("incident_seconds", "materialize_seconds", "solve_seconds"):
        require(isinstance(row.get(field), (int, float)) and math.isfinite(row[field]) and
                row[field] >= 0, f"round timing {field}")


def validate_rank_gate(source: Path, binary: Path, results: list[Path]) -> dict:
    require(sha256_file(source) == RANK_GATE_SOURCE_SHA, "rank-gate source pin")
    require(sha256_file(binary) == RANK_GATE_BINARY_SHA, "rank-gate binary pin")
    require(len(results) == 3, "rank-gate repeat count")
    timings = []
    for index, (path, expected_sha) in enumerate(zip(results, RANK_GATE_RESULT_SHAS)):
        require(sha256_file(path) == expected_sha, f"rank-gate result pin {index}")
        result = json.loads(path.read_text())
        require(result.get("status") ==
                "PASS_EXACT_PARALLEL_HIERARCHICAL_ROUND660_PROMOTION_GATE",
                "rank-gate status")
        require((result.get("rank_mode"), result.get("rank_shards"), result.get("workers"),
                 result.get("candidate_identical"), result.get("all_equations_verified"),
                 result.get("verification_failures")) ==
                ("sharded", 16, 16, True, True, 0), "rank-gate method/result")
        require(result.get("output_checkpoint", {}).get("byte_identical") is True,
                "rank-gate checkpoint identity")
        timings.append(result["timings_seconds"]["rare_rank_and_materialize"])
    return {"repeat_seconds": timings, "repeat_count": 3, "all_exact": True}


def validate_v3_source(parent: Path, v3: Path) -> dict:
    require(sha256_file(parent) == PARENT_SOURCE_SHA, "parent source pin")
    require(sha256_file(v3) == V3_SOURCE_SHA, "v3 source pin")
    baseline = parent.read_text()
    source = v3.read_text()
    # Persistence functions must remain literally unchanged, so native resume
    # and serialized schemas do not rely merely on output coincidence.
    persistence = ("sparse_write_checkpoint", "sparse_read_checkpoint",
                   "sparse_write_vectors", "sparse_read_vectors")
    for name in persistence:
        require(function_text(baseline, name) == function_text(source, name),
                f"persistence function drift: {name}")
    required = [
        "struct HierarchicalFnvHasher(u64)",
        "0xcbf29ce484222325", "0x100000001b3",
        "HashMap<Mono, u32, BuildHasherDefault<HierarchicalFnvHasher>>",
        "let (equations, rows_by_rank, rank_metrics) = hierarchical_rank_and_materialize(",
        "columns, vectors, frequency, workers, 16, target, prime32",
        "let mut ordered: Vec<(u32, Mono)>", "ordered.sort_unstable()",
        "ordered.windows(2).any(|pair| pair[0] >= pair[1])",
        "hierarchical_row_hash(&row) as usize & (rank_shards - 1)",
        "rank_maps.iter().map(HashMap::len).sum::<usize>() != rows_by_rank.len()",
        "let base = columns.len() / workers", "let remainder = columns.len() % workers",
        "for worker in 0..workers", "let slice = &columns[begin..begin + count]",
        "handles.into_iter().map(|handle| handle.join()",
        "for mut chunk in chunk_results { equations.append(&mut chunk); }",
        "if equations.len() != columns.len()",
        "terms.sort_unstable_by_key(|term| term.rank)",
        "terms.windows(2).any(|pair| pair[0].rank >= pair[1].rank)",
        "columns.iter().any(|column| sparse_pairing",
    ]
    missing = [item for item in required if item not in source]
    require(not missing, f"v3 rank/source contract missing {missing}")
    return {
        "rank_shards": 16,
        "rank_order": "natural (checked-u32 frequency, Mono), independent of FNV shard",
        "lookup": "FNV-1a sharded maps; complete shard census",
        "materialization": "16 quotient/remainder source-column slices; joins and appends in source order",
        "persistence_functions_byte_identical": list(persistence),
        "postsolve_all_column_verification_present": True,
    }


def expect_result_reject(result: dict, label: str) -> None:
    try:
        validate_native_result(result, "hierarchical")
    except (Rejection, KeyError, TypeError):
        return
    raise Rejection(f"hostile result accepted: {label}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent-source", type=Path, required=True)
    parser.add_argument("--v3-source", type=Path, required=True)
    parser.add_argument("--v3-binary", type=Path, required=True)
    parser.add_argument("--sequential-result", type=Path, required=True)
    parser.add_argument("--v3-result", type=Path, required=True)
    parser.add_argument("--sequential-checkpoint", type=Path, required=True)
    parser.add_argument("--v3-checkpoint", type=Path, required=True)
    parser.add_argument("--sequential-vectors", type=Path, required=True)
    parser.add_argument("--v3-vectors", type=Path, required=True)
    parser.add_argument("--v3-stderr", type=Path, required=True)
    parser.add_argument("--watchdog", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--hostile-modes", type=Path, required=True)
    parser.add_argument("--rank-gate-source", type=Path, required=True)
    parser.add_argument("--rank-gate-binary", type=Path, required=True)
    parser.add_argument("--rank-gate-result", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source_contract = validate_v3_source(args.parent_source, args.v3_source)
    require(sha256_file(args.v3_binary) == V3_BINARY_SHA, "v3 binary pin")
    rank_gate = validate_rank_gate(args.rank_gate_source, args.rank_gate_binary,
                                   args.rank_gate_result)
    require(sha256_file(args.sequential_result) == SEQUENTIAL_RESULT_SHA,
            "sequential result pin")
    require(sha256_file(args.v3_result) == V3_RESULT_SHA, "v3 result pin")
    sequential = json.loads(args.sequential_result.read_text())
    v3 = json.loads(args.v3_result.read_text())
    validate_native_result(sequential, "tree")
    validate_native_result(v3, "hierarchical")

    sequential_checkpoint = parse_checkpoint(args.sequential_checkpoint, OUTPUT_CHECKPOINT_SHA)
    v3_checkpoint = parse_checkpoint(args.v3_checkpoint, OUTPUT_CHECKPOINT_SHA)
    for item in (sequential_checkpoint, v3_checkpoint):
        require((item["round"], len(item["columns"]), item["support"]) ==
                (ROUND, COLUMNS, SUPPORT), "checkpoint census")
    require(files_equal(args.sequential_checkpoint, args.v3_checkpoint) and
            sequential_checkpoint["candidate"] == v3_checkpoint["candidate"],
            "candidate/checkpoint byte identity")
    require(sha256_file(args.sequential_vectors) == OUTPUT_VECTORS_SHA and
            sha256_file(args.v3_vectors) == OUTPUT_VECTORS_SHA and
            files_equal(args.sequential_vectors, args.v3_vectors), "vector-cache byte identity")

    replay = json.loads(args.replay.read_text())
    require(replay.get("schema") == "KRENN_AFFINE251_D12_CACHE_REPLAY_V1" and
            replay.get("status") == "PASS_ALL_COLUMNS" and
            (replay.get("round"), replay.get("columns_replayed"),
             replay.get("terms_replayed"), replay.get("verification_failures")) ==
            (ROUND, COLUMNS, 33_907_235, 0), "independent all-column replay")

    require(sha256_file(args.v3_stderr) == V3_STDERR_SHA, "v3 phase log pin")
    phase_match = re.search(
        r"columns=(\d+) variables=(\d+) basis=(\d+) terms=(\d+) "
        r"ordered_sort=([0-9.]+)s rank_map=([0-9.]+)s materialize=([0-9.]+)s "
        r"rank_shard_min=(\d+) rank_shard_max=(\d+) "
        r"local_eliminate_critical=([0-9.]+)s local_wall=([0-9.]+)s "
        r"merge=([0-9.]+)s backsolve=([0-9.]+)s verify=([0-9.]+)s support=(\d+)",
        args.v3_stderr.read_text())
    require(phase_match is not None, "v3 phase log schema")
    values = phase_match.groups()
    require(tuple(map(int, values[:4])) == (COLUMNS, 21_066_364, 334_288, 34_083_985)
            and tuple(map(int, values[7:9])) == (1_203_599, 1_430_479)
            and int(values[-1]) == SUPPORT, "v3 phase census")
    phase_names = ("ordered_sort", "rank_map", "materialize", "local_eliminate_critical",
                   "local_wall", "merge", "backsolve", "verify")
    phases = dict(zip(phase_names, map(float, values[4:7] + values[9:14])))

    require(sha256_file(args.watchdog) == V3_WATCHDOG_SHA, "v3 watchdog pin")
    watchdog = json.loads(args.watchdog.read_text())
    require(watchdog.get("schema") == "KRENN_AFFINE251_D12_MACOS_RSS_WATCHDOG_V1" and
            watchdog.get("status") == "PASS" and watchdog.get("breach") is None and
            watchdog.get("returncode") == 0 and watchdog.get("atomic_outputs_clean") is True and
            watchdog.get("source_sha256") == V3_SOURCE_SHA and
            watchdog.get("binary_sha256") == V3_BINARY_SHA and
            watchdog.get("result_sha256") == V3_RESULT_SHA and
            watchdog.get("rss_limit_kib") == RSS_LIMIT_KIB and
            0 < watchdog.get("peak_rss_kib", RSS_LIMIT_KIB) < RSS_LIMIT_KIB,
            "v3 libproc 36GiB watchdog")

    hostile = json.loads(args.hostile_modes.read_text())
    require(hostile.get("status") == "PASS_ALL_UNSUPPORTED_MODES_REJECTED_BEFORE_IO" and
            hostile.get("binary_sha256") == V3_BINARY_SHA and len(hostile.get("cases", {})) == 8 and
            all(item.get("pass") is True for item in hostile["cases"].values()),
            "v3 hostile modes")
    hostile_results = []
    for label, field, value in (("schema", "schema", "STALE_V0"),
                                ("round", "rounds_completed", 748),
                                ("workers", "workers", 8),
                                ("columns", "column_orbits_exposed", COLUMNS - 1)):
        altered = copy.deepcopy(v3); altered[field] = value
        expect_result_reject(altered, label); hostile_results.append(label)

    tree_seconds = sequential["rounds"][0]["solve_seconds"]
    v3_seconds = v3["rounds"][0]["solve_seconds"]
    speedup = tree_seconds / v3_seconds
    require(tree_seconds == 11.050344 and speedup > 2.0, "strict >2x promotion threshold")
    accounted = (phases["ordered_sort"] + phases["rank_map"] + phases["materialize"] +
                 phases["local_wall"] + phases["merge"] + phases["backsolve"] +
                 phases["verify"])
    require(0 <= v3_seconds - accounted < 0.25, "v3 phase accounting")

    audit = {
        "schema": "KRENN_AFFINE251_D12_GENERIC_HIERARCHICAL_V3_AUDIT_V1",
        "status": "PASS_PROMOTE_EXACT_GENERIC_HIERARCHICAL_V3",
        "restored_parent_source_sha256": PARENT_SOURCE_SHA,
        "accepted_round748": {
            "result_sha256": BASELINE_RESULT_SHA,
            "checkpoint_sha256": BASELINE_CHECKPOINT_SHA,
            "vectors_sha256": BASELINE_VECTORS_SHA,
        },
        "v3_provenance": {
            "source_sha256": V3_SOURCE_SHA,
            "binary_sha256": V3_BINARY_SHA,
            "result_sha256": V3_RESULT_SHA,
            "stderr_sha256": V3_STDERR_SHA,
            "watchdog_sha256": V3_WATCHDOG_SHA,
        },
        "rank_gate_provenance": {
            "source_sha256": RANK_GATE_SOURCE_SHA,
            "binary_sha256": RANK_GATE_BINARY_SHA,
            "result_sha256s": list(RANK_GATE_RESULT_SHAS),
            **rank_gate,
        },
        "integrated_method": source_contract,
        "arbitrary_resume": {
            "input_round": 748, "output_round": 749,
            "cached_vectors_loaded": 333_199, "vectors_materialized_on_restore": 0,
        },
        "schema_preserved": True,
        "byte_identity": {
            "candidate": True, "checkpoint": True, "vector_cache": True,
            "checkpoint_sha256": OUTPUT_CHECKPOINT_SHA,
            "vectors_sha256": OUTPUT_VECTORS_SHA,
        },
        "all_column_replay": replay,
        "performance": {
            "tree_seconds": tree_seconds, "v3_seconds": v3_seconds,
            "speedup": speedup, "required_strictly_greater_than": 2.0,
            "pass": True, "phase_seconds": phases,
            "accounted_seconds": accounted, "unattributed_seconds": v3_seconds - accounted,
        },
        "resource_gate": {
            "pass": True, "observer": watchdog.get("rss_observer"),
            "rss_limit_kib": RSS_LIMIT_KIB, "peak_rss_kib": watchdog["peak_rss_kib"],
            "sample_count": watchdog["sample_count"], "elapsed_seconds": watchdog["elapsed_seconds"],
        },
        "hostile_modes": {
            "binary_cases": sorted(hostile["cases"]),
            "result_mutations": hostile_results,
            "pass": True,
        },
        "scope": "One exact round748-to749 A/B; no solver rerun or continuation by referee.",
    }
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, args.output)
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()
