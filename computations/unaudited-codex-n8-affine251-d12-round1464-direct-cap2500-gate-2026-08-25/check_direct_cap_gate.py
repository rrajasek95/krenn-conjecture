#!/usr/bin/env python3
"""Exact referee for the direct round-1464 cap 2.25m -> 2.5m gate."""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import sys


BASE = Path(__file__).resolve().parent
REPO = BASE.parents[1]
CONTROL = BASE / "control_cap2250"
CANDIDATE = BASE / "candidate_cap2500"
INPUT = REPO / (
    "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/"
    "production_from_round1448_cap2250/stage04"
)
SOURCE_SHA = "3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"
BINARY_SHA = "79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048"
WATCHDOG_SHA = "48fe528b15c31b8ed6446eb10628b0bcb598191efaac64dd59021881b80b1522"
INPUT_CP = "1b4dde9f009b4343099190e293913818b3df88dfc34c27653e7cfcd4acf08c8e"
INPUT_CACHE = "46744c37b6c1ab30e6ce945a9f049e45683b4324470e661554f4ae4134b9d48c"
OUTPUT_CP = "0191363f5da4b5b74945dd48a51954195200957996c5d3ff43c5242c37a7c64f"
OUTPUT_CACHE = "9bb1b64f80def9014f0b031f4683da5bf00354b331cf2bc0541672ce02d67b29"


def fail(message: str) -> None:
    raise RuntimeError(message)


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        fail(f"{path}: non-object JSON")
    return value


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def normalize(value: dict, remove_cap: bool) -> dict:
    result = copy.deepcopy(value)
    for key in (
        "elapsed_seconds", "peak_rss_kib", "restore_seconds",
        "vector_cache_write_seconds", "checkpoint", "vector_cache", "dual",
    ):
        if key not in result:
            fail(f"missing normalization key {key}")
        del result[key]
    if remove_cap:
        del result["column_cap"]
    if len(result.get("rounds", [])) != 1:
        fail("gate must contain exactly one round")
    for key in ("incident_seconds", "materialize_seconds", "solve_seconds"):
        del result["rounds"][0][key]
    return result


def option_map(command: object) -> dict[str, str]:
    if not isinstance(command, list) or not command:
        fail("watchdog command is missing")
    result: dict[str, str] = {}
    index = 1
    while index < len(command):
        if index + 1 >= len(command) or not command[index].startswith("--"):
            fail("malformed watchdog command")
        if command[index] in result:
            fail(f"duplicate option {command[index]}")
        result[command[index]] = command[index + 1]
        index += 2
    return result


def validate_result(value: dict, cap: int) -> None:
    expected = {
        "status": "INCOMPLETE_SEARCH_CAP", "incomplete_reason": "ROUND_CAP",
        "rounds_completed": 1464, "column_orbits_exposed": 2054273,
        "dual_support": 2427, "cached_vectors_loaded": 2049529,
        "column_cap": cap, "workers": 16, "pivot_mode": "rare",
        "strategy": "cold", "elimination_kernel": "hierarchical",
        "incremental_basis": False, "wall_limit_seconds": 120,
        "rss_limit_gib": 36, "prime": 1073741827,
    }
    for key, wanted in expected.items():
        if value.get(key) != wanted:
            fail(f"result {key}: expected {wanted!r}, got {value.get(key)!r}")
    round_value = value["rounds"][0]
    for key, wanted in {
        "round": 1464, "columns": 2054273, "new_columns": 4744,
        "dual_support": 2427, "new_support_rows": 1301,
        "selected_strategy": "cold", "selected_pivot": "rare",
    }.items():
        if round_value.get(key) != wanted:
            fail(f"round {key}: expected {wanted!r}, got {round_value.get(key)!r}")


def validate_watchdog(value: dict, cap: int) -> None:
    for key, wanted in {
        "status": "PASS", "returncode": 0, "atomic_outputs_clean": True,
        "breach": None, "source_sha256": SOURCE_SHA,
        "binary_sha256": BINARY_SHA, "rss_limit_kib": 36 * 1024 * 1024,
        "wall_limit_seconds": 150,
    }.items():
        if value.get(key) != wanted:
            fail(f"watchdog {key}: expected {wanted!r}, got {value.get(key)!r}")
    if not 0 < value.get("peak_rss_kib", 0) < 36 * 1024 * 1024:
        fail("invalid RSS evidence")
    options = option_map(value.get("command"))
    for key, wanted in {
        "--wall-seconds": "120", "--rss-gib": "36", "--workers": "16",
        "--pivot": "rare", "--strategy": "cold",
        "--elimination": "hierarchical", "--incremental": "no",
        "--column-cap": str(cap), "--round-cap": "1464",
    }.items():
        if options.get(key) != wanted:
            fail(f"command {key}: expected {wanted!r}, got {options.get(key)!r}")


def main() -> int:
    cr = load(CONTROL / "result.json")
    xr = load(CANDIDATE / "result.json")
    cw = load(CONTROL / "watchdog.json")
    xw = load(CANDIDATE / "watchdog.json")
    validate_result(cr, 2_250_000)
    validate_result(xr, 2_500_000)
    validate_watchdog(cw, 2_250_000)
    validate_watchdog(xw, 2_500_000)

    cn = normalize(cr, False)
    xn = normalize(xr, False)
    differences = {key for key in cn.keys() | xn.keys() if cn.get(key) != xn.get(key)}
    if differences != {"column_cap"}:
        fail(f"normalized differences are {sorted(differences)}")
    if normalize(cr, True) != normalize(xr, True):
        fail("semantics differ after removing cap")

    observed = {
        "input_checkpoint": sha(INPUT / "checkpoint.bin"),
        "input_cache": sha(INPUT / "vectors.bin"),
        "control_checkpoint": sha(CONTROL / "checkpoint.bin"),
        "candidate_checkpoint": sha(CANDIDATE / "checkpoint.bin"),
        "control_cache": sha(CONTROL / "vectors.bin"),
        "candidate_cache": sha(CANDIDATE / "vectors.bin"),
    }
    expected = {
        "input_checkpoint": INPUT_CP, "input_cache": INPUT_CACHE,
        "control_checkpoint": OUTPUT_CP, "candidate_checkpoint": OUTPUT_CP,
        "control_cache": OUTPUT_CACHE, "candidate_cache": OUTPUT_CACHE,
    }
    if observed != expected:
        fail(f"artifact hash mismatch: {observed}")

    hostile = copy.deepcopy(xr)
    hostile["rounds"][0]["new_columns"] += 1
    if normalize(cr, True) == normalize(hostile, True):
        fail("changed-round hostile was accepted")
    hostile_watchdog = copy.deepcopy(xw)
    hostile_watchdog["atomic_outputs_clean"] = False
    try:
        validate_watchdog(hostile_watchdog, 2_500_000)
    except RuntimeError:
        pass
    else:
        fail("non-atomic hostile was accepted")

    result = {
        "schema": "KRENN_AFFINE251_D12_ROUND1464_DIRECT_CAP2500_GATE_V1",
        "status": "PASS_EXACT_DIRECT_CAP_EXTENSION_EQUIVALENCE",
        "input": {
            "round": 1463, "columns": 2049529,
            "checkpoint_sha256": INPUT_CP, "vector_cache_sha256": INPUT_CACHE,
            "independent_audit_manifest_sha256":
                "46e69f29a46d24fadd2163e301ad77127071981aad3c0ad2305882b214da6bbb",
        },
        "output": {
            "round": 1464, "columns": 2054273, "dual_support": 2427,
            "checkpoint_sha256": OUTPUT_CP, "vector_cache_sha256": OUTPUT_CACHE,
        },
        "caps": {"control": 2250000, "candidate": 2500000},
        "normalized_semantic_differences": ["column_cap"],
        "byte_identical_checkpoint": True,
        "byte_identical_vector_cache": True,
        "frozen": {
            "source_sha256": SOURCE_SHA, "binary_sha256": BINARY_SHA,
            "watchdog_155_source_sha256": WATCHDOG_SHA,
        },
        "telemetry": {
            "control_elapsed_seconds": cw["elapsed_seconds"],
            "control_peak_rss_kib": cw["peak_rss_kib"],
            "candidate_elapsed_seconds": xw["elapsed_seconds"],
            "candidate_peak_rss_kib": xw["peak_rss_kib"],
        },
        "portfolio_skipped": True,
        "hostiles": {
            "changed_round_semantics_rejected": True,
            "non_atomic_watchdog_rejected": True,
        },
        "continuation_accepted": False,
    }
    output = BASE / "results_round1464_direct_cap2500_gate.json"
    temporary = output.with_suffix(".json.tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, output)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
