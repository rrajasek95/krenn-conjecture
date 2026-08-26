#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
GENERIC = REPO / "computations/unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24"
WATCHDOG = GENERIC / "sealed_v3/run_with_macos_rss_watchdog.py"
SOURCE = GENERIC / "sealed_v3/main.rs"
BINARY = GENERIC / "sealed_v3/sparse_d12_dual"
PROVIDER = REPO / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/canonical_triangle_pair_offdiag_full_p1073741827.ms"
SOURCE_SHA = "173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a"
BINARY_SHA = "8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a"


def sha256(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def native(label, pivot, strategy):
    directory = ROOT / label
    return [
        str(BINARY), "--input", str(PROVIDER),
        "--output", str(directory / "result.json"),
        "--checkpoint", str(directory / "checkpoint.bin"),
        "--vector-cache", str(directory / "vectors.bin"),
        "--dual", str(directory / "dual.tsv"),
        "--prime", "1073741827", "--wall-seconds", "110", "--rss-gib", "36",
        "--workers", "16", "--pivot", pivot, "--strategy", strategy,
        "--elimination", "tree", "--incremental", "no",
        "--portfolio-period", "1", "--portfolio-parallel", "yes",
        "--support-cap", "100000", "--column-cap", "1000000", "--round-cap", "850",
    ]


def watched(label, command):
    directory = ROOT / label
    wrapper = [
        sys.executable, str(WATCHDOG), "--rss-gib", "36", "--wall-seconds", "120",
        "--poll-seconds", "0.25", "--source", str(SOURCE),
        "--expected-source-sha256", SOURCE_SHA,
        "--expected-binary-sha256", BINARY_SHA,
        "--telemetry", str(directory / "watchdog.json"),
        "--stdout", str(directory / "stdout.log"),
        "--stderr", str(directory / "stderr.log"), "--", *command,
    ]
    subprocess.run(wrapper, cwd=REPO, check=True)


pins = json.loads((ROOT / "INPUT_PINS.json").read_text())
assert pins["status"] == "PASS_APFS_CLONED_FROZEN_INPUTS"
assert sha256(SOURCE) == SOURCE_SHA and sha256(BINARY) == BINARY_SHA
for label in ("portfolio", "selected_control"):
    assert sha256(ROOT / label / "checkpoint.bin") == pins["source_checkpoint_sha256"]
    assert sha256(ROOT / label / "vectors.bin") == pins["source_vectors_sha256"]

watched("portfolio", native("portfolio", "auto", "best"))
portfolio = json.loads((ROOT / "portfolio/result.json").read_text())
assert portfolio["rounds_completed"] == 850 and len(portfolio["rounds"]) == 1
selected = portfolio["rounds"][0]
assert selected["round"] == 850
assert selected["selected_strategy"] in {"cold", "repair"}
assert selected["selected_pivot"] in {"first", "last", "rare"}
watched("selected_control", native(
    "selected_control", selected["selected_pivot"], selected["selected_strategy"]
))
print(json.dumps({"status": "RUNS_TERMINAL", "selected_strategy": selected["selected_strategy"],
                  "selected_pivot": selected["selected_pivot"]}, sort_keys=True))
