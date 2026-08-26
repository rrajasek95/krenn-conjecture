#!/usr/bin/env python3
"""Strict four-stage chain and every-column referee through round 849."""

import json
import os
from pathlib import Path
import time

from audit_round749 import checkpoint, replay_vectors, require, sha256, SOURCE_INPUT


ROOT = Path(__file__).resolve().parent
PRODUCTION = ROOT / "production_from_round749"
START_CHECKPOINT_SHA = "dda7fb5100adfcc24264993899ec2404a3beec0e0f1e96b4f3dd83a2be7d8621"
START_VECTORS_SHA = "93e3eeee9d7a356b4caaf59cae5c5b6671e64508004b448895d0296db0bd2bf1"
SOURCE_SHA = "173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a"
BINARY_SHA = "8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a"
WATCHDOG_V1_SHA = "a1e6104726303960b256c9a9f6217299a71a4be5c00bb77fe451bf62935ed19b"
WATCHDOG_V2_SHA = "53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"

EXPECTED = [
    {
        "name": "stage01", "begin": 750, "end": 778,
        "start_columns": 334298, "end_columns": 368432,
        "support": 556, "status": "INCOMPLETE_RESOURCE_GATE", "reason": "WALL_CAP",
        "result": "e1f6ab7d31f84de44d4b2cee1b156fa6f924cce7e736b680323801d31e6f153d",
        "checkpoint": "d8463c5aba89f3dde57ed9c92d57a4a8fb11fb2585a504b8e3b7f71078610345",
        "vectors": "805a5bb3194f146c38a10483203a72847728d1178feca01d835e415dcd6607e5",
        "watchdog": None,
    },
    {
        "name": "stage02", "begin": 779, "end": 805,
        "start_columns": 368432, "end_columns": 405259,
        "support": 518, "status": "INCOMPLETE_RESOURCE_GATE", "reason": "WALL_CAP",
        "result": "5d0d27971f8ddcb11f9e03e96afca5b952b6548e5dcf2de6bc682792b1facc1f",
        "checkpoint": "7cd46995e665591116cbb0f99fc087cd47688229082e55b92cdabeb7f2546415",
        "vectors": "c00f86587df398f59476b2fd3478b9ed1e449a65ecd8400ce6a711d68e380e57",
        "watchdog": "c44df39a18b4e37f2d82b4d96d5ecea1e57486addec45ad9e73e84e311960a25",
    },
    {
        "name": "stage03", "begin": 806, "end": 829,
        "start_columns": 405259, "end_columns": 442452,
        "support": 556, "status": "INCOMPLETE_RESOURCE_GATE", "reason": "WALL_CAP",
        "result": "37c66605e3fc55c37d25445eae9c46773ccee280d69cf07071dcddf9ce319f53",
        "checkpoint": "63c48ef7beb77c022d73c9d5912b191e414faab7c33608277f52deb57766e452",
        "vectors": "b9c2ab1382cfb1e3bcbeb2f814e384ecace292d8a06a45a136da9024d467de51",
        "watchdog": "fda7a511a221ebdc4f134730c4152467813c55edd87950cc97073a7d6c3e299e",
    },
    {
        "name": "stage04", "begin": 830, "end": 849,
        "start_columns": 442452, "end_columns": 460676,
        "support": 312, "status": "INCOMPLETE_SEARCH_CAP", "reason": "ROUND_CAP",
        "result": "ee0764c6496a9837024443c0fdcd6322b5fcba4770e015eaacf34188455832a7",
        "checkpoint": "ce87c58cf79ddebbc0f9ce39eb36f08b6bf85a8f0f764f7728c3565da13fab49",
        "vectors": "040b1b59bad7693fbd7ed71d8ff9f760b39b30943c77f452eae3b4047b5ac254",
        "watchdog": "80284d050ca6cd51e7c14b4d3dfd6ca53dcc0c2a51208a8c5ef7e63df78ebddf",
    },
]


def main() -> None:
    started = time.monotonic()
    require(sha256(ROOT / "control_hierarchical/checkpoint.bin") == START_CHECKPOINT_SHA,
            "round749 checkpoint pin")
    require(sha256(ROOT / "control_hierarchical/vectors.bin") == START_VECTORS_SHA,
            "round749 vector pin")
    require(sha256(ROOT / "sealed_v3/main.rs") == SOURCE_SHA, "source pin")
    require(sha256(ROOT / "sealed_v3/sparse_d12_dual") == BINARY_SHA, "binary pin")
    require(sha256(ROOT / "sealed_v3/run_with_macos_rss_watchdog.py")
            == WATCHDOG_V1_SHA, "stage1 watchdog pin")
    require(sha256(ROOT / "sealed_watchdog_v2/run_with_macos_rss_watchdog_v2.py")
            == WATCHDOG_V2_SHA, "stage2-4 watchdog pin")

    expected_rounds = []
    stage_records = []
    full_resource_wall = 0.0
    resource_peaks = []
    previous_columns = 334_298
    for index, expected in enumerate(EXPECTED):
        stage = PRODUCTION / expected["name"]
        result_path = stage / "result.json"
        checkpoint_path = stage / "checkpoint.bin"
        vectors_path = stage / "vectors.bin"
        require(sha256(result_path) == expected["result"], f"{expected['name']} result pin")
        require(sha256(checkpoint_path) == expected["checkpoint"],
                f"{expected['name']} checkpoint pin")
        require(sha256(vectors_path) == expected["vectors"], f"{expected['name']} vectors pin")
        result = json.loads(result_path.read_text())
        require(result["status"] == expected["status"]
                and result["incomplete_reason"] == expected["reason"],
                f"{expected['name']} terminal status")
        interval = list(range(expected["begin"], expected["end"] + 1))
        require([record["round"] for record in result["rounds"]] == interval,
                f"{expected['name']} interval")
        expected_rounds.extend(interval)
        require(result["cached_vectors_loaded"] == expected["start_columns"]
                == previous_columns, f"{expected['name']} input column census")
        require(result["column_orbits_exposed"] == expected["end_columns"]
                and result["dual_support"] == expected["support"],
                f"{expected['name']} output census")
        require(sum(record["new_columns"] for record in result["rounds"])
                == expected["end_columns"] - expected["start_columns"],
                f"{expected['name']} column growth")
        require(result["workers"] == 16 and result["pivot_mode"] == "rare"
                and result["strategy"] == "cold"
                and result["elimination_kernel"] == "hierarchical"
                and not result["incremental_basis"], f"{expected['name']} mode")
        for suffix in ("result.json.tmp", "checkpoint.bin.tmp", "vectors.bin.tmp"):
            require(not (stage / suffix).exists(), f"{expected['name']} atomic temporary")
        record = {
            "stage": expected["name"], "round_interval": interval,
            "result_sha256": expected["result"], "checkpoint_sha256": expected["checkpoint"],
            "vectors_sha256": expected["vectors"], "columns": expected["end_columns"],
            "support": expected["support"], "native_elapsed_seconds": result["elapsed_seconds"],
        }
        if index == 0:
            recovery = json.loads((stage / "RECOVERY.json").read_text())
            require(recovery["status"] == "PASS_EXACT_STATE_RESOURCE_TELEMETRY_INCOMPLETE",
                    "stage1 resource caveat")
            record["resource_status"] = "TELEMETRY_INCOMPLETE"
            record["recovery_sha256"] = sha256(stage / "RECOVERY.json")
            full_resource_wall += result["elapsed_seconds"]
        else:
            watchdog_path = stage / "watchdog.json"
            require(sha256(watchdog_path) == expected["watchdog"],
                    f"{expected['name']} watchdog pin")
            watchdog = json.loads(watchdog_path.read_text())
            require(watchdog["schema"] == "KRENN_AFFINE251_D12_MACOS_RSS_WATCHDOG_V2"
                    and watchdog["status"] == "PASS" and watchdog["breach"] is None
                    and watchdog["atomic_outputs_clean"] and watchdog["returncode"] == 0,
                    f"{expected['name']} watchdog result")
            require(watchdog["source_sha256"] == SOURCE_SHA
                    and watchdog["binary_sha256"] == BINARY_SHA
                    and watchdog["watchdog_sha256"] == WATCHDOG_V2_SHA,
                    f"{expected['name']} watchdog lineage")
            require(watchdog["peak_rss_kib"] < watchdog["rss_limit_kib"]
                    and watchdog["elapsed_seconds"] < watchdog["wall_limit_seconds"],
                    f"{expected['name']} resource bounds")
            record.update({
                "resource_status": "PASS", "watchdog_sha256": expected["watchdog"],
                "watchdog_elapsed_seconds": watchdog["elapsed_seconds"],
                "peak_rss_kib": watchdog["peak_rss_kib"],
                "rss_samples": watchdog["sample_count"],
            })
            full_resource_wall += watchdog["elapsed_seconds"]
            resource_peaks.append(watchdog["peak_rss_kib"])
        stage_records.append(record)
        previous_columns = expected["end_columns"]

    require(expected_rounds == list(range(750, 850)), "global 100-round interval")
    require(full_resource_wall < 540, "aggregate staged wall budget")
    final = PRODUCTION / "stage04"
    round_index, columns, candidate = checkpoint(final / "checkpoint.bin")
    require(round_index == 849 and len(columns) == 460_676 and len(candidate) == 312,
            "terminal checkpoint census")
    require((final / "vectors.bin").stat().st_size == 993_313_251,
            "terminal cache byte census")
    replay = replay_vectors(final / "vectors.bin", columns, candidate)

    result = {
        "schema": "KRENN_AFFINE251_D12_HIERARCHICAL_PRODUCTION_ROUND849_REFEREE_V1",
        "status": "PASS_EXACT_PRODUCTION_CONTINUATION_TO_ROUND849",
        "scope": "Exactly rounds 750..849 from accepted round749; no D12 completion claim.",
        "terminal_reason": "ROUND_CAP",
        "start_checkpoint_sha256": START_CHECKPOINT_SHA,
        "start_vectors_sha256": START_VECTORS_SHA,
        "source_input_sha256": sha256(SOURCE_INPUT),
        "producer_source_sha256": SOURCE_SHA,
        "producer_binary_sha256": BINARY_SHA,
        "stage1_resource_caveat": "PASS_EXACT_STATE_RESOURCE_TELEMETRY_INCOMPLETE",
        "stages": stage_records,
        "round_interval": [750, 849],
        "round_count": 100,
        "aggregate_staged_wall_seconds": round(full_resource_wall, 6),
        "complete_telemetry_stage_peak_rss_kib": max(resource_peaks),
        "terminal_round": round_index,
        "terminal_columns": len(columns),
        "terminal_candidate_support": len(candidate),
        "terminal_result_sha256": EXPECTED[-1]["result"],
        "terminal_checkpoint_sha256": EXPECTED[-1]["checkpoint"],
        "terminal_vectors_sha256": EXPECTED[-1]["vectors"],
        "terminal_full_replay": replay,
        "audit_elapsed_seconds": round(time.monotonic() - started, 6),
    }
    path = ROOT / "results_production_round849_referee.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


if __name__ == "__main__":
    main()
