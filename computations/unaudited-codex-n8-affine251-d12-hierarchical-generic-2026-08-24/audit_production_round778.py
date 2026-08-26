#!/usr/bin/env python3
"""Independent exact referee for the landed round-749 to round-778 stage."""

import json
import os
from pathlib import Path
import time

from audit_round749 import checkpoint, replay_vectors, require, sha256, SOURCE_INPUT


ROOT = Path(__file__).resolve().parent
STAGE = ROOT / "production_from_round749/stage01"
START_CHECKPOINT_SHA = "dda7fb5100adfcc24264993899ec2404a3beec0e0f1e96b4f3dd83a2be7d8621"
START_VECTORS_SHA = "93e3eeee9d7a356b4caaf59cae5c5b6671e64508004b448895d0296db0bd2bf1"
SOURCE_SHA = "173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a"
BINARY_SHA = "8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a"
ATTEMPTED_WATCHDOG_SHA = "a1e6104726303960b256c9a9f6217299a71a4be5c00bb77fe451bf62935ed19b"
REPAIRED_WATCHDOG_SHA = "53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"


def main() -> None:
    started = time.monotonic()
    require(sha256(ROOT / "control_hierarchical/checkpoint.bin") == START_CHECKPOINT_SHA,
            "accepted round749 checkpoint pin")
    require(sha256(ROOT / "control_hierarchical/vectors.bin") == START_VECTORS_SHA,
            "accepted round749 vector pin")
    require(sha256(ROOT / "sealed_v3/main.rs") == SOURCE_SHA, "producer source pin")
    require(sha256(ROOT / "sealed_v3/sparse_d12_dual") == BINARY_SHA,
            "producer binary pin")
    require(sha256(ROOT / "sealed_v3/run_with_macos_rss_watchdog.py")
            == ATTEMPTED_WATCHDOG_SHA, "attempted watchdog pin")
    require(sha256(ROOT / "run_with_macos_rss_watchdog_v2.py")
            == REPAIRED_WATCHDOG_SHA, "repaired watchdog pin")

    result_path = STAGE / "result.json"
    checkpoint_path = STAGE / "checkpoint.bin"
    vectors_path = STAGE / "vectors.bin"
    result = json.loads(result_path.read_text())
    require(result["schema"] == "KRENN_AFFINE251_D12_NATIVE_SPARSE_DUAL_V1",
            "result schema")
    require(result["status"] == "INCOMPLETE_RESOURCE_GATE"
            and result["incomplete_reason"] == "WALL_CAP", "terminal reason")
    require(result["rounds_completed"] == 778 and len(result["rounds"]) == 29,
            "strict 750..778 round count")
    require([record["round"] for record in result["rounds"]] == list(range(750, 779)),
            "round interval has a gap or duplicate")
    require(result["cached_vectors_loaded"] == 334_298
            and result["vectors_materialized_on_restore"] == 0,
            "round749 cache restore census")
    require(result["workers"] == 16 and result["pivot_mode"] == "rare"
            and result["strategy"] == "cold"
            and result["elimination_kernel"] == "hierarchical"
            and not result["incremental_basis"], "fixed solver mode")
    require(result["wall_limit_seconds"] == 95 and result["rss_limit_gib"] == 36,
            "native resource contract")
    require(sum(record["new_columns"] for record in result["rounds"])
            == result["column_orbits_exposed"] - 334_298, "column growth identity")
    last = result["rounds"][-1]
    require((last["columns"], last["dual_support"])
            == (result["column_orbits_exposed"], result["dual_support"]),
            "last/result census identity")

    round_index, columns, candidate = checkpoint(checkpoint_path)
    require(round_index == 778, "checkpoint round")
    require(len(columns) == result["column_orbits_exposed"] == 368_432,
            "checkpoint column census")
    require(len(candidate) == result["dual_support"] == 556,
            "checkpoint support census")
    require(vectors_path.stat().st_size == result["vector_cache_bytes"] == 793_603_080,
            "vector-cache byte census")
    for suffix in ("result.json.tmp", "checkpoint.bin.tmp", "vectors.bin.tmp"):
        require(not (STAGE / suffix).exists(), f"native atomic temporary remains: {suffix}")
    replay = replay_vectors(vectors_path, columns, candidate)

    hostiles = json.loads((ROOT / "results_watchdog_v2_hostiles.json").read_text())
    require(hostiles["status"] == "PASS"
            and hostiles["wrapper_sha256"] == REPAIRED_WATCHDOG_SHA,
            "repaired watchdog hostile evidence")
    output = {
        "schema": "KRENN_AFFINE251_D12_HIERARCHICAL_PRODUCTION_ROUND778_REFEREE_V1",
        "status": "PASS_EXACT_STATE_RESOURCE_TELEMETRY_INCOMPLETE",
        "scope": "Round749 to round778 arithmetic only; no later continuation accepted here.",
        "start_checkpoint_sha256": START_CHECKPOINT_SHA,
        "start_vectors_sha256": START_VECTORS_SHA,
        "source_input_sha256": sha256(SOURCE_INPUT),
        "producer_source_sha256": SOURCE_SHA,
        "producer_binary_sha256": BINARY_SHA,
        "attempted_watchdog_sha256": ATTEMPTED_WATCHDOG_SHA,
        "attempted_watchdog_verdict": (
            "RESOURCE_ENFORCEMENT_ACTIVE_UNTIL_NATURAL_CHILD_EXIT; "
            "TELEMETRY_SEAL_FAILED_ON_POST_EXIT_ZERO-MEMBER_RACE"),
        "observed_manual_rss_kib": [6_520_048, 6_500_064],
        "repaired_watchdog_sha256": REPAIRED_WATCHDOG_SHA,
        "repaired_watchdog_hostiles_sha256": sha256(
            ROOT / "results_watchdog_v2_hostiles.json"),
        "result_sha256": sha256(result_path),
        "checkpoint_sha256": sha256(checkpoint_path),
        "vectors_sha256": sha256(vectors_path),
        "stderr_tmp_sha256": sha256(STAGE / "stderr.log.tmp"),
        "round": round_index,
        "round_interval": [750, 778],
        "columns": len(columns),
        "candidate_support": len(candidate),
        "full_replay": replay,
        "audit_elapsed_seconds": round(time.monotonic() - started, 6),
    }
    path = ROOT / "results_production_round778_referee.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


if __name__ == "__main__":
    main()
