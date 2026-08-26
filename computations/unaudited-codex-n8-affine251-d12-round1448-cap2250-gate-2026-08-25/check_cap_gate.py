#!/usr/bin/env python3
"""Fail-closed referee for the round-1448 2.0m -> 2.25m column-cap gate."""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import sys


BASE = Path(__file__).resolve().parent
REPO = BASE.parents[1]
CONTROL = BASE / "control_cap2000"
CANDIDATE = BASE / "candidate_cap2250"
INPUT = (
    REPO
    / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25"
    / "production_from_round1363_portfolio_cap2000/stage15_recovery_attempt2"
)
SOURCE_SHA = "3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"
BINARY_SHA = "79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048"
WATCHDOG_SOURCE_SHA = "53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"
INPUT_CHECKPOINT_SHA = "82d53e68e3f1bd483518996fed2dbffa80910163e8c7234f9ccce7c88afeb3cb"
INPUT_CACHE_SHA = "b806d22cac98ce4dd45928baf01401a8a7afaa12fcbd6d9c56f07cb1f9dab091"
OUTPUT_CHECKPOINT_SHA = "4a4ceb16738127a41af8f783265f745cccbf849b827f97d7e0618e609cf3055a"
OUTPUT_CACHE_SHA = "829028724fb39e37fd9ffb07d5d85094515a0a84e8634307fab17c2833e45007"


def fail(message: str) -> None:
    raise RuntimeError(message)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            value.update(block)
    return value.hexdigest()


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        fail(f"{path}: JSON root is not an object")
    return value


def semantic(value: dict, *, retain_cap: bool) -> dict:
    result = copy.deepcopy(value)
    for key in (
        "elapsed_seconds",
        "peak_rss_kib",
        "restore_seconds",
        "vector_cache_write_seconds",
        "checkpoint",
        "vector_cache",
        "dual",
    ):
        if key not in result:
            fail(f"missing expected normalized field {key}")
        del result[key]
    if not retain_cap:
        if "column_cap" not in result:
            fail("missing column_cap")
        del result["column_cap"]
    rounds = result.get("rounds")
    if not isinstance(rounds, list) or len(rounds) != 1:
        fail("expected exactly one round record")
    for key in ("incident_seconds", "materialize_seconds", "solve_seconds"):
        if key not in rounds[0]:
            fail(f"missing round timing {key}")
        del rounds[0][key]
    return result


def validate_result(value: dict, cap: int) -> None:
    expected = {
        "status": "INCOMPLETE_SEARCH_CAP",
        "incomplete_reason": "ROUND_CAP",
        "rounds_completed": 1448,
        "column_orbits_exposed": 1974608,
        "dual_support": 2131,
        "cached_vectors_loaded": 1970322,
        "column_cap": cap,
        "workers": 16,
        "pivot_mode": "rare",
        "strategy": "cold",
        "elimination_kernel": "hierarchical",
        "incremental_basis": False,
        "wall_limit_seconds": 90,
        "rss_limit_gib": 36,
        "prime": 1073741827,
    }
    for key, wanted in expected.items():
        if value.get(key) != wanted:
            fail(f"result {key}: expected {wanted!r}, got {value.get(key)!r}")
    round_value = value["rounds"][0]
    expected_round = {
        "round": 1448,
        "columns": 1974608,
        "new_columns": 4286,
        "dual_support": 2131,
        "new_support_rows": 1102,
        "selected_strategy": "cold",
        "selected_pivot": "rare",
    }
    for key, wanted in expected_round.items():
        if round_value.get(key) != wanted:
            fail(f"round {key}: expected {wanted!r}, got {round_value.get(key)!r}")


def command_map(command: list[str]) -> dict[str, str]:
    if not isinstance(command, list) or not command:
        fail("watchdog command absent")
    values: dict[str, str] = {}
    index = 1
    while index < len(command):
        key = command[index]
        if not key.startswith("--") or index + 1 >= len(command):
            fail("malformed watchdog command")
        if key in values:
            fail(f"duplicate command option {key}")
        values[key] = command[index + 1]
        index += 2
    return values


def validate_watchdog(value: dict, cap: int) -> None:
    expected = {
        "status": "PASS",
        "returncode": 0,
        "atomic_outputs_clean": True,
        "breach": None,
        "source_sha256": SOURCE_SHA,
        "binary_sha256": BINARY_SHA,
        "rss_limit_kib": 36 * 1024 * 1024,
        "wall_limit_seconds": 115,
    }
    for key, wanted in expected.items():
        if value.get(key) != wanted:
            fail(f"watchdog {key}: expected {wanted!r}, got {value.get(key)!r}")
    if not 0 < value.get("peak_rss_kib", 0) < 36 * 1024 * 1024:
        fail("watchdog RSS telemetry invalid")
    options = command_map(value.get("command"))
    wanted_options = {
        "--prime": "1073741827",
        "--wall-seconds": "90",
        "--rss-gib": "36",
        "--workers": "16",
        "--pivot": "rare",
        "--strategy": "cold",
        "--elimination": "hierarchical",
        "--incremental": "no",
        "--column-cap": str(cap),
        "--round-cap": "1448",
    }
    for key, wanted in wanted_options.items():
        if options.get(key) != wanted:
            fail(f"command {key}: expected {wanted!r}, got {options.get(key)!r}")


def main() -> int:
    control_result = load(CONTROL / "result.json")
    candidate_result = load(CANDIDATE / "result.json")
    control_watchdog = load(CONTROL / "watchdog.json")
    candidate_watchdog = load(CANDIDATE / "watchdog.json")
    validate_result(control_result, 2_000_000)
    validate_result(candidate_result, 2_250_000)
    validate_watchdog(control_watchdog, 2_000_000)
    validate_watchdog(candidate_watchdog, 2_250_000)

    control_semantic = semantic(control_result, retain_cap=True)
    candidate_semantic = semantic(candidate_result, retain_cap=True)
    differing = {
        key
        for key in control_semantic.keys() | candidate_semantic.keys()
        if control_semantic.get(key) != candidate_semantic.get(key)
    }
    if differing != {"column_cap"}:
        fail(f"normalized semantic differences are {sorted(differing)}, not column_cap only")
    if semantic(control_result, retain_cap=False) != semantic(candidate_result, retain_cap=False):
        fail("normalized results differ after removing column_cap")

    hashes = {
        "input_checkpoint": digest(INPUT / "checkpoint.bin"),
        "input_cache": digest(INPUT / "vectors.bin"),
        "control_checkpoint": digest(CONTROL / "checkpoint.bin"),
        "candidate_checkpoint": digest(CANDIDATE / "checkpoint.bin"),
        "control_cache": digest(CONTROL / "vectors.bin"),
        "candidate_cache": digest(CANDIDATE / "vectors.bin"),
    }
    expected_hashes = {
        "input_checkpoint": INPUT_CHECKPOINT_SHA,
        "input_cache": INPUT_CACHE_SHA,
        "control_checkpoint": OUTPUT_CHECKPOINT_SHA,
        "candidate_checkpoint": OUTPUT_CHECKPOINT_SHA,
        "control_cache": OUTPUT_CACHE_SHA,
        "candidate_cache": OUTPUT_CACHE_SHA,
    }
    if hashes != expected_hashes:
        fail(f"artifact hashes differ: {hashes}")

    hostile_result = copy.deepcopy(candidate_result)
    hostile_result["rounds"][0]["columns"] += 1
    if semantic(control_result, retain_cap=False) == semantic(hostile_result, retain_cap=False):
        fail("hostile changed round semantics was not rejected")
    hostile_watchdog = copy.deepcopy(candidate_watchdog)
    hostile_watchdog["atomic_outputs_clean"] = False
    try:
        validate_watchdog(hostile_watchdog, 2_250_000)
    except RuntimeError:
        pass
    else:
        fail("hostile non-atomic watchdog was not rejected")

    result = {
        "schema": "KRENN_AFFINE251_D12_ROUND1448_CAP2250_GATE_V1",
        "status": "PASS_EXACT_CAP_EXTENSION_EQUIVALENCE",
        "input": {
            "round": 1447,
            "columns": 1970322,
            "checkpoint_sha256": INPUT_CHECKPOINT_SHA,
            "vector_cache_sha256": INPUT_CACHE_SHA,
            "independent_audit_manifest_sha256": "a60825d7f5c80b47ce3f74249a1727928cdec76559ae01fcc8ebc5e90bf71cd1",
        },
        "output": {
            "round": 1448,
            "columns": 1974608,
            "dual_support": 2131,
            "checkpoint_sha256": OUTPUT_CHECKPOINT_SHA,
            "vector_cache_sha256": OUTPUT_CACHE_SHA,
        },
        "caps": {"control": 2_000_000, "candidate": 2_250_000},
        "normalized_semantic_differences": ["column_cap"],
        "byte_identical_checkpoint": True,
        "byte_identical_vector_cache": True,
        "frozen_engine": {
            "source_sha256": SOURCE_SHA,
            "binary_sha256": BINARY_SHA,
            "watchdog_v2_sha256": WATCHDOG_SOURCE_SHA,
        },
        "telemetry": {
            "control_elapsed_seconds": control_watchdog["elapsed_seconds"],
            "control_peak_rss_kib": control_watchdog["peak_rss_kib"],
            "candidate_elapsed_seconds": candidate_watchdog["elapsed_seconds"],
            "candidate_peak_rss_kib": candidate_watchdog["peak_rss_kib"],
        },
        "hostiles": {
            "changed_round_semantics_rejected": True,
            "non_atomic_watchdog_rejected": True,
        },
    }
    output = BASE / "results_round1448_cap2250_gate.json"
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
