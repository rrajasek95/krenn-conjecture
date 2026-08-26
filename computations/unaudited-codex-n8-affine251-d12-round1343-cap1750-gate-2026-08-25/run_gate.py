#!/usr/bin/env python3
"""Run exact cap1500/cap1750 one-round equivalence after launch pins exist."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
V4 = REPO / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25"
SOURCE = V4 / "sealed_v4_1/main.rs"
BINARY = V4 / "sealed_v4_1/sparse_d12_dual"
WATCHDOG = REPO / "computations/unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/run_with_macos_rss_watchdog_v2.py"
PROVIDER = REPO / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/canonical_triangle_pair_offdiag_full_p1073741827.ms"
SOURCE_SHA = "3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"
BINARY_SHA = "79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048"
WATCHDOG_SHA = "53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def native(label, cap):
    directory = HERE / label
    return [
        str(BINARY), "--input", str(PROVIDER),
        "--output", str(directory / "result.json"),
        "--checkpoint", str(directory / "checkpoint.bin"),
        "--vector-cache", str(directory / "vectors.bin"),
        "--dual", str(directory / "dual.tsv"),
        "--prime", "1073741827", "--wall-seconds", "90", "--rss-gib", "36",
        "--workers", "16", "--pivot", "rare", "--strategy", "cold",
        "--elimination", "hierarchical", "--incremental", "no",
        "--portfolio-period", "256", "--portfolio-parallel", "yes",
        "--support-cap", "100000", "--column-cap", str(cap), "--round-cap", "1343",
    ]


def run(label, cap, checkpoint, vectors):
    directory = HERE / label
    assert not directory.exists(), f"refuse pre-existing output directory {directory}"
    directory.mkdir()
    subprocess.run(["cp", "-c", str(checkpoint), str(directory / "checkpoint.bin")], check=True)
    subprocess.run(["cp", "-c", str(vectors), str(directory / "vectors.bin")], check=True)
    wrapper = [
        sys.executable, str(WATCHDOG), "--rss-gib", "36", "--wall-seconds", "115",
        "--poll-seconds", "0.25", "--source", str(SOURCE),
        "--expected-source-sha256", SOURCE_SHA, "--expected-binary-sha256", BINARY_SHA,
        "--telemetry", str(directory / "watchdog.json"),
        "--stdout", str(directory / "stdout.log"), "--stderr", str(directory / "stderr.log"),
        "--", *native(label, cap),
    ]
    subprocess.run(wrapper, cwd=REPO, check=True)


pins_path = HERE / "LAUNCH_PINS.json"
assert pins_path.exists(), "launch interlock: round1342 Poincare pins absent"
pins = json.loads(pins_path.read_text())
assert pins["status"] == "PASS_FROZEN_SEALED_ROUND1342_INPUT"
assert sha256(SOURCE) == SOURCE_SHA and sha256(BINARY) == BINARY_SHA
assert sha256(WATCHDOG) == WATCHDOG_SHA
assert sha256(REPO / pins["poincare_manifest"]) == pins["poincare_manifest_sha256"]
assert sha256(REPO / pins["poincare_result"]) == pins["poincare_result_sha256"]
checkpoint = REPO / pins["checkpoint"]
vectors = REPO / pins["vectors"]
assert sha256(checkpoint) == pins["checkpoint_sha256"]
assert sha256(vectors) == pins["vectors_sha256"]
run("cap1500_control", 1500000, checkpoint, vectors)
run("cap1750_candidate", 1750000, checkpoint, vectors)
value = {"schema": "KRENN_AFFINE251_D12_ROUND1343_CAP_RUNNER_V1",
         "status": "RUNS_TERMINAL_PENDING_VALIDATION", "continued_beyond_round1343": False}
temporary = HERE / "runner_summary.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "runner_summary.json")
print(json.dumps(value, sort_keys=True))
