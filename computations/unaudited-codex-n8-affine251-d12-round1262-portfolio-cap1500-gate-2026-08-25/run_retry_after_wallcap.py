#!/usr/bin/env python3
"""Run the frozen one-round portfolio and conditional cap equivalence gate."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
AUDIT1061 = REPO / "computations/unaudited-codex-n8-affine251-d12-round1061-portfolio-audit-2026-08-25"
SOURCE = AUDIT1061 / "audit_source/src/main.rs"
BINARY = AUDIT1061 / "audit_source/sparse_d12_dual"
WATCHDOG = HERE / "run_with_macos_rss_watchdog_v2_155.py"
PROVIDER = REPO / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/canonical_triangle_pair_offdiag_full_p1073741827.ms"
PINS_PATH = HERE / "LAUNCH_PINS.json"
SOURCE_SHA = "2cf629054e1b5e2350617b71114544b7d0c7a47f811b67b6dea4483e5e911230"
BINARY_SHA = "ade47c27a96314bb4391241a60a372c79e643a44b8a62a00054fffc576ccc7ce"
WATCHDOG_SHA = "48fe528b15c31b8ed6446eb10628b0bcb598191efaac64dd59021881b80b1522"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def native(label, pivot, strategy, column_cap, native_wall=110):
    directory = HERE / label
    return [
        str(BINARY), "--input", str(PROVIDER),
        "--output", str(directory / "result.json"),
        "--checkpoint", str(directory / "checkpoint.bin"),
        "--vector-cache", str(directory / "vectors.bin"),
        "--dual", str(directory / "dual.tsv"),
        "--prime", "1073741827", "--wall-seconds", str(native_wall), "--rss-gib", "36",
        "--workers", "16", "--pivot", pivot, "--strategy", strategy,
        "--elimination", "tree", "--incremental", "no",
        "--portfolio-period", "1", "--portfolio-parallel", "yes",
        "--support-cap", "100000", "--column-cap", str(column_cap),
        "--round-cap", "1262",
    ]


def clone_inputs(label, checkpoint, vectors):
    directory = HERE / label
    assert not directory.exists(), f"refuse pre-existing output directory: {directory}"
    directory.mkdir()
    # APFS clone only: fail rather than silently perform a multi-GiB physical copy.
    subprocess.run(["cp", "-c", str(checkpoint), str(directory / "checkpoint.bin")], check=True)
    subprocess.run(["cp", "-c", str(vectors), str(directory / "vectors.bin")], check=True)


def watched(label, command, wrapper_wall=120):
    directory = HERE / label
    wrapper = [
        sys.executable, str(WATCHDOG), "--rss-gib", "36", "--wall-seconds", str(wrapper_wall),
        "--poll-seconds", "0.25", "--source", str(SOURCE),
        "--expected-source-sha256", SOURCE_SHA,
        "--expected-binary-sha256", BINARY_SHA,
        "--telemetry", str(directory / "watchdog.json"),
        "--stdout", str(directory / "stdout.log"),
        "--stderr", str(directory / "stderr.log"), "--", *command,
    ]
    subprocess.run(wrapper, cwd=REPO, check=True)


assert PINS_PATH.exists(), "launch interlock: run freeze_poincare_pins.py only after seal"
pins = json.loads(PINS_PATH.read_text())
assert pins["status"] == "PASS_FROZEN_SEALED_ROUND1261_INPUT"
checkpoint = REPO / pins["checkpoint"]
vectors = REPO / pins["vectors"]
assert sha256(REPO / pins["poincare_manifest"]) == pins["poincare_manifest_sha256"]
assert sha256(REPO / pins["poincare_result"]) == pins["poincare_result_sha256"]
assert sha256(checkpoint) == pins["checkpoint_sha256"]
assert sha256(vectors) == pins["vectors_sha256"]
assert sha256(SOURCE) == SOURCE_SHA and sha256(BINARY) == BINARY_SHA
assert sha256(WATCHDOG) == WATCHDOG_SHA

failure = HERE / "portfolio_failed120"
failure_audit = json.loads((HERE / "FAILURE_AUDIT.json").read_text())
failure_watch = json.loads((failure / "watchdog.json").read_text())
assert failure_audit["status"] == "PASS_FAIL_CLOSED_NO_STATE_ACCEPTED"
assert sha256(failure / "watchdog.json") == failure_audit["watchdog_sha256"]
assert failure_watch["breach"] == "WALL_CAP" and failure_watch["returncode"] == -15
assert not (failure / "result.json").exists()
assert sha256(failure / "checkpoint.bin") == pins["checkpoint_sha256"]
assert sha256(failure / "vectors.bin") == pins["vectors_sha256"]
assert not (HERE / "selected_control").exists()
assert not (HERE / "cap1500_candidate").exists()

clone_inputs("portfolio_retry155", checkpoint, vectors)
watched("portfolio_retry155", native("portfolio_retry155", "auto", "best", 1250000, 145), 155)
portfolio = json.loads((HERE / "portfolio_retry155/result.json").read_text())
assert portfolio["rounds_completed"] == 1262 and len(portfolio["rounds"]) == 1
selected = portfolio["rounds"][0]
assert selected["round"] == 1262
assert selected["selected_strategy"] in {"cold", "repair"}
assert selected["selected_pivot"] in {"first", "last", "rare"}

clone_inputs("selected_control", checkpoint, vectors)
watched("selected_control", native(
    "selected_control", selected["selected_pivot"], selected["selected_strategy"], 1250000
))

cap_run = selected["selected_strategy"] == "cold" and selected["selected_pivot"] == "rare"
if cap_run:
    clone_inputs("cap1500_candidate", checkpoint, vectors)
    watched("cap1500_candidate", native("cap1500_candidate", "rare", "cold", 1500000))

value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1262_RUNNER_SUMMARY_V1",
    "status": "RUNS_TERMINAL_PENDING_VALIDATION",
    "portfolio_label": "portfolio_retry155",
    "preserved_failed_attempt": "portfolio_failed120",
    "selected_strategy": selected["selected_strategy"],
    "selected_pivot": selected["selected_pivot"],
    "cap1500_candidate_run": cap_run,
    "continued_beyond_round1262": False,
}
temporary = HERE / "runner_summary.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "runner_summary.json")
print(json.dumps(value, sort_keys=True))
