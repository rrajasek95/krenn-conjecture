#!/usr/bin/env python3
"""Independent fail-closed r1448 cap2.0m -> cap2.25m equivalence audit."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PLAN = json.loads((HERE / "AUDIT_PLAN.json").read_text())
ROOT = REPO / PLAN["producer_root"]
LABELS = ["control_cap2000", "candidate_cap2250"]
SOURCE_SHA = "3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"
BINARY_SHA = "79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048"
WATCHDOG_SHA = "53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"
PRIME = 1073741827


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def argument(command: list[str], flag: str) -> str:
    require(command.count(flag) == 1, f"command must contain {flag} exactly once")
    index = command.index(flag)
    require(index + 1 < len(command), f"missing value for {flag}")
    return command[index + 1]


def checkpoint_header(path: Path) -> dict[str, int]:
    with path.open("rb") as stream:
        data = stream.read(44)
    require(data[:12] == b"AFF12CEG1\0\0\0", f"bad checkpoint magic: {path}")
    prime, round_number, columns, support = struct.unpack_from("<QQQQ", data, 12)
    require(path.stat().st_size == 44 + 15 * columns + 21 * support,
            f"checkpoint length mismatch: {path}")
    return {"prime": prime, "round": round_number, "columns": columns,
            "support": support, "bytes": path.stat().st_size}


def normalized_command(command: list[str], label: str) -> list[str]:
    marker = f"/{label}/"
    return [item.replace(marker, "/RUN/") for item in command]


require(PLAN["status"] == "READY_WAITING_FOR_BOTH_TERMINAL_CANDIDATES", "bad plan status")
required = ["result.json", "checkpoint.bin", "vectors.bin", "watchdog.json", "stderr.log"]
for label in LABELS:
    for name in required:
        require((ROOT / label / name).is_file(), f"terminal artifact absent: {label}/{name}")
    require(not any((ROOT / label).glob("*.tmp")), f"temporary output remains in {label}")

results = {label: json.loads((ROOT / label / "result.json").read_text()) for label in LABELS}
watches = {label: json.loads((ROOT / label / "watchdog.json").read_text()) for label in LABELS}
caps = PLAN["labels"]
record_fields = ["round", "columns", "new_columns", "dual_support", "new_support_rows",
                 "selected_strategy", "selected_pivot"]
semantic_fields = [
    "schema", "status", "incomplete_reason", "degree", "prime", "group_order",
    "provider_equations", "provider_terms_parsed", "provider_distinct_terms",
    "seed_support", "column_orbits_exposed", "dual_support", "rounds_completed",
    "global_annihilation", "target_pairing", "workers", "pivot_mode", "strategy",
    "elimination_kernel", "incremental_basis", "portfolio_period", "portfolio_parallel",
    "support_cap", "wall_limit_seconds", "rss_limit_gib", "cached_vectors_loaded",
    "vectors_materialized_on_restore", "vector_cache_bytes",
]
records: dict[str, dict[str, object]] = {}
semantics: dict[str, dict[str, object]] = {}
for label in LABELS:
    result, watch = results[label], watches[label]
    require(result["status"] == "INCOMPLETE_SEARCH_CAP", f"bad result status: {label}")
    require(result["incomplete_reason"] == "ROUND_CAP", f"bad stop reason: {label}")
    require(result["rounds_completed"] == 1448 and len(result["rounds"]) == 1,
            f"not exact singleton r1448: {label}")
    require(result["cached_vectors_loaded"] == 1970322, f"wrong restored cache count: {label}")
    require(result["vectors_materialized_on_restore"] == 0,
            f"input cache was rematerialized: {label}")
    require(result["column_cap"] == caps[label], f"wrong result cap: {label}")
    require(watch["status"] == "PASS" and watch["returncode"] == 0 and watch["breach"] is None,
            f"watchdog failure: {label}")
    require(watch["elapsed_seconds"] < 115, f"wrapper wall gate exceeded: {label}")
    require(watch["peak_rss_kib"] < 36 * 1024 * 1024, f"RSS gate exceeded: {label}")
    require(watch["atomic_outputs_clean"] is True, f"atomic output telemetry failed: {label}")
    require(watch["source_sha256"] == SOURCE_SHA and watch["binary_sha256"] == BINARY_SHA,
            f"source/binary pin mismatch: {label}")
    require(watch["watchdog_sha256"] == WATCHDOG_SHA, f"watchdog pin mismatch: {label}")
    require(watch["result_sha256"] == sha256(ROOT / label / "result.json"),
            f"watchdog result pin mismatch: {label}")
    command = watch["command"]
    expected = {
        "--round-cap": "1448", "--column-cap": str(caps[label]), "--workers": "16",
        "--pivot": "rare", "--strategy": "cold", "--elimination": "hierarchical",
        "--incremental": "no", "--wall-seconds": "90", "--rss-gib": "36",
        "--prime": str(PRIME),
    }
    for flag, value in expected.items():
        require(argument(command, flag) == value, f"command mismatch {label} {flag}")
    records[label] = {key: result["rounds"][0][key] for key in record_fields}
    semantics[label] = {key: result[key] for key in semantic_fields}

control, candidate = LABELS
require(records[control] == records[candidate], "round records differ")
require(semantics[control] == semantics[candidate], "semantic result fields differ")
left = normalized_command(watches[control]["command"], control)
right = normalized_command(watches[candidate]["command"], candidate)
require(len(left) == len(right), "command lengths differ")
differences = [(index, a, b) for index, (a, b) in enumerate(zip(left, right)) if a != b]
require(differences == [(left.index("2000000"), "2000000", "2250000")],
        f"normalized command diff is not cap-only: {differences}")

checkpoint_hashes = {label: sha256(ROOT / label / "checkpoint.bin") for label in LABELS}
vector_hashes = {label: sha256(ROOT / label / "vectors.bin") for label in LABELS}
require(len(set(checkpoint_hashes.values())) == 1, "checkpoint bytes differ")
require(len(set(vector_hashes.values())) == 1, "cache bytes differ")
headers = {label: checkpoint_header(ROOT / label / "checkpoint.bin") for label in LABELS}
require(headers[control] == headers[candidate], "checkpoint headers differ")
header = headers[control]
require(header["prime"] == PRIME and header["round"] == 1448, "wrong endpoint header")
require(header["columns"] == records[control]["columns"], "checkpoint/result column mismatch")
require(header["support"] == records[control]["dual_support"], "checkpoint/result support mismatch")
require(all(not (ROOT / label / "dual.tsv").exists() for label in LABELS),
        "dual output must be absent at incomplete round cap")

value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1448_CAP2250_INDEPENDENT_AUDIT_V1",
    "status": "PASS_EXACT_CAP2000_TO_CAP2250_EQUIVALENCE",
    "input_round": 1447,
    "input_audit_sha256": PLAN["input_audit_sha256"],
    "input_manifest_sha256": PLAN["input_manifest_sha256"],
    "round_record": records[control],
    "checkpoint_header": header,
    "checkpoint_sha256": checkpoint_hashes[control],
    "vectors_sha256": vector_hashes[control],
    "control_result_sha256": sha256(ROOT / control / "result.json"),
    "candidate_result_sha256": sha256(ROOT / candidate / "result.json"),
    "control_watchdog_sha256": sha256(ROOT / control / "watchdog.json"),
    "candidate_watchdog_sha256": sha256(ROOT / candidate / "watchdog.json"),
    "maximum_peak_rss_kib": max(watches[label]["peak_rss_kib"] for label in LABELS),
    "maximum_elapsed_seconds": max(watches[label]["elapsed_seconds"] for label in LABELS),
    "exact_byte_equality": {"checkpoint": True, "vectors": True},
    "only_normalized_command_difference_is_cap": True,
    "dual_outputs_absent": True,
    "continued_beyond_round1448": False,
    "production_mutated": False,
}
temporary = HERE / "results_round1448_cap2250_audit.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_round1448_cap2250_audit.json")
print(json.dumps(value, sort_keys=True))
