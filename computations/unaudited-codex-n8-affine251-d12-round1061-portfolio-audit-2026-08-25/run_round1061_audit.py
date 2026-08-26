#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
V4 = REPO / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25"
GENERIC = REPO / "computations/unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24"
WATCHDOG = GENERIC / "run_with_macos_rss_watchdog_v2.py"
PARENT_SOURCE = V4 / "sealed_v4_1/main.rs"
SOURCE = ROOT / "audit_source/src/main.rs"
BINARY = ROOT / "audit_source/sparse_d12_dual"
PROVIDER = REPO / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/canonical_triangle_pair_offdiag_full_p1073741827.ms"
PARENT_SOURCE_SHA = "3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"
SOURCE_SHA = "2cf629054e1b5e2350617b71114544b7d0c7a47f811b67b6dea4483e5e911230"
BINARY_SHA = "ade47c27a96314bb4391241a60a372c79e643a44b8a62a00054fffc576ccc7ce"
WATCHDOG_SHA = "53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


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
        "--support-cap", "100000", "--column-cap", "1000000", "--round-cap", "1061",
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
assert pins["status"] == "PASS_APFS_CLONED_FROZEN_ROUND1060_INPUTS"
assert pins["round1060_audit_manifest_sha256"] == "7c1649f025dfa9286955e4322a166ef2691a72443e8f1075adf4db6e4584365a"
assert sha256(PARENT_SOURCE) == PARENT_SOURCE_SHA
assert sha256(SOURCE) == SOURCE_SHA and sha256(BINARY) == BINARY_SHA
assert sha256(WATCHDOG) == WATCHDOG_SHA
for label in ("portfolio", "selected_control"):
    assert sha256(ROOT / label / "checkpoint.bin") == pins["source_checkpoint_sha256"]
    assert sha256(ROOT / label / "vectors.bin") == pins["source_vectors_sha256"]

watched("portfolio", native("portfolio", "auto", "best"))
portfolio = json.loads((ROOT / "portfolio/result.json").read_text())
assert portfolio["rounds_completed"] == 1061 and len(portfolio["rounds"]) == 1
selected = portfolio["rounds"][0]
assert selected["round"] == 1061
assert selected["selected_strategy"] in {"cold", "repair"}
assert selected["selected_pivot"] in {"first", "last", "rare"}
watched("selected_control", native(
    "selected_control", selected["selected_pivot"], selected["selected_strategy"]
))
print(json.dumps({"status": "RUNS_TERMINAL", "selected_strategy": selected["selected_strategy"],
                  "selected_pivot": selected["selected_pivot"]}, sort_keys=True))
