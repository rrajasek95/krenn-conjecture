#!/usr/bin/env python3
"""Run built-in sequential six-task portfolio, fixed replay, and cap equivalence."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCHEDULE = json.loads((HERE / "SCHEDULE.json").read_text())
SOURCE = REPO / "computations/unaudited-codex-n8-affine251-d12-round1061-portfolio-audit-2026-08-25/audit_source/src/main.rs"
BINARY = REPO / "computations/unaudited-codex-n8-affine251-d12-round1061-portfolio-audit-2026-08-25/audit_source/sparse_d12_dual"
WATCHDOG = HERE / "run_with_macos_rss_watchdog_v2_540.py"
PROVIDER = REPO / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/canonical_triangle_pair_offdiag_full_p1073741827.ms"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def clone(label, checkpoint, vectors):
    directory = HERE / label
    assert not directory.exists(), f"refuse pre-existing directory {directory}"
    directory.mkdir()
    subprocess.run(["cp", "-c", str(checkpoint), str(directory / "checkpoint.bin")], check=True)
    subprocess.run(["cp", "-c", str(vectors), str(directory / "vectors.bin")], check=True)


def command(label, pivot, strategy, cap, native_wall, parallel):
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
        "--portfolio-period", "1", "--portfolio-parallel", parallel,
        "--support-cap", "100000", "--column-cap", str(cap), "--round-cap", "1262",
    ]


def watched(label, native, wrapper_wall):
    directory = HERE / label
    wrapper = [
        sys.executable, str(WATCHDOG), "--rss-gib", "36", "--wall-seconds", str(wrapper_wall),
        "--poll-seconds", "0.25", "--source", str(SOURCE),
        "--expected-source-sha256", SCHEDULE["engine"]["source_sha256"],
        "--expected-binary-sha256", SCHEDULE["engine"]["binary_sha256"],
        "--telemetry", str(directory / "watchdog.json"),
        "--stdout", str(directory / "stdout.log"),
        "--stderr", str(directory / "stderr.log"), "--", *native,
    ]
    subprocess.run(wrapper, cwd=REPO, check=True)


assert SCHEDULE["status"] == "FROZEN_READY"
assert sha256(SOURCE) == SCHEDULE["engine"]["source_sha256"]
assert sha256(BINARY) == SCHEDULE["engine"]["binary_sha256"]
assert sha256(WATCHDOG) == SCHEDULE["engine"]["watchdog540_sha256"]
checkpoint = REPO / SCHEDULE["input"]["checkpoint"]
vectors = REPO / SCHEDULE["input"]["vectors"]
manifest = REPO / "computations/unaudited-codex-n8-affine251-d12-v4-1-round1261-audit-2026-08-25/FINAL_MANIFEST.sha256"
assert sha256(manifest) == SCHEDULE["input"]["audit_manifest_sha256"]
assert sha256(checkpoint) == SCHEDULE["input"]["checkpoint_sha256"]
assert sha256(vectors) == SCHEDULE["input"]["vectors_sha256"]

clone("portfolio", checkpoint, vectors)
watched("portfolio", command("portfolio", "auto", "best", 1250000, 520, "no"), 540)
portfolio = json.loads((HERE / "portfolio/result.json").read_text())
assert portfolio["status"] == "INCOMPLETE_SEARCH_CAP" and portfolio["incomplete_reason"] == "ROUND_CAP"
assert portfolio["rounds_completed"] == 1262 and len(portfolio["rounds"]) == 1
selected = portfolio["rounds"][0]
assert selected["selected_strategy"] in {"repair", "cold"}
assert selected["selected_pivot"] in {"first", "last", "rare"}

clone("selected_control", checkpoint, vectors)
watched("selected_control", command("selected_control", selected["selected_pivot"],
                                    selected["selected_strategy"], 1250000, 110, "no"), 120)
clone("cap1500_candidate", checkpoint, vectors)
watched("cap1500_candidate", command("cap1500_candidate", selected["selected_pivot"],
                                     selected["selected_strategy"], 1500000, 110, "no"), 120)

value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1262_INTERNAL_PORTFOLIO_RUNNER_V1",
    "status": "RUNS_TERMINAL_PENDING_VALIDATION",
    "selected_strategy": selected["selected_strategy"],
    "selected_pivot": selected["selected_pivot"],
    "continued_beyond_round1262": False,
}
temporary = HERE / "runner_summary.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "runner_summary.json")
print(json.dumps(value, sort_keys=True))
