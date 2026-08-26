#!/usr/bin/env python3
"""Run held round1363 portfolio/fixed/conditional cap gate after future pins exist."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCHEDULE = json.loads((HERE / "SCHEDULE.json").read_text())
SOURCE = REPO / SCHEDULE["engine"]["source"]
BINARY = REPO / SCHEDULE["engine"]["binary"]
WATCHDOG = REPO / SCHEDULE["engine"]["watchdog540"]
PROVIDER = REPO / SCHEDULE["engine"]["provider"]
ROUND1343 = REPO / SCHEDULE["provisional_lineage"]["round1343_package"]


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def clone(label, checkpoint, vectors):
    directory = HERE / label
    assert not directory.exists(), f"refuse pre-existing output {directory}"
    directory.mkdir()
    subprocess.run(["cp", "-c", str(checkpoint), str(directory / "checkpoint.bin")], check=True)
    subprocess.run(["cp", "-c", str(vectors), str(directory / "vectors.bin")], check=True)


def command(label, pivot, strategy, cap, native_wall, portfolio_period):
    directory = HERE / label
    return [
        str(BINARY), "--input", str(PROVIDER), "--output", str(directory / "result.json"),
        "--checkpoint", str(directory / "checkpoint.bin"), "--vector-cache", str(directory / "vectors.bin"),
        "--dual", str(directory / "dual.tsv"), "--prime", "1073741827",
        "--wall-seconds", str(native_wall), "--rss-gib", "36", "--workers", "16",
        "--pivot", pivot, "--strategy", strategy, "--elimination", "tree",
        "--incremental", "no", "--portfolio-period", str(portfolio_period),
        "--portfolio-parallel", "no", "--support-cap", "100000",
        "--column-cap", str(cap), "--round-cap", "1363",
    ]


def watched(label, native, wrapper_wall):
    directory = HERE / label
    wrapper = [
        sys.executable, str(WATCHDOG), "--rss-gib", "36", "--wall-seconds", str(wrapper_wall),
        "--poll-seconds", "0.25", "--source", str(SOURCE),
        "--expected-source-sha256", SCHEDULE["engine"]["source_sha256"],
        "--expected-binary-sha256", SCHEDULE["engine"]["binary_sha256"],
        "--telemetry", str(directory / "watchdog.json"), "--stdout", str(directory / "stdout.log"),
        "--stderr", str(directory / "stderr.log"), "--", *native,
    ]
    subprocess.run(wrapper, cwd=REPO, check=True)


pins_path = HERE / "FUTURE_INPUT_PINS.json"
assert pins_path.exists(), "launch interlock: round1362 FINAL_REPLAY_CLEAR pins absent"
pins = json.loads(pins_path.read_text())
assert pins["status"] == "PASS_FROZEN_INDEPENDENT_ROUND1362_FINAL_REPLAY_CLEAR"
assert sha256(ROUND1343 / "MANIFEST.sha256") == SCHEDULE["provisional_lineage"]["round1343_manifest_sha256"]
assert sha256(SOURCE) == SCHEDULE["engine"]["source_sha256"]
assert sha256(BINARY) == SCHEDULE["engine"]["binary_sha256"]
assert sha256(WATCHDOG) == SCHEDULE["engine"]["watchdog540_sha256"]
assert sha256(PROVIDER) == SCHEDULE["engine"]["provider_sha256"]
checkpoint, vectors = REPO / pins["checkpoint"], REPO / pins["vectors"]
assert sha256(REPO / pins["audit_result"]) == pins["audit_result_sha256"]
assert sha256(REPO / pins["audit_manifest"]) == pins["audit_manifest_sha256"]
assert sha256(checkpoint) == pins["checkpoint_sha256"]
assert sha256(vectors) == pins["vectors_sha256"]

clone("portfolio", checkpoint, vectors)
watched("portfolio", command("portfolio", "auto", "best", 1750000, 520, 1), 540)
portfolio = json.loads((HERE / "portfolio/result.json").read_text())
assert portfolio["status"] == "INCOMPLETE_SEARCH_CAP" and portfolio["incomplete_reason"] == "ROUND_CAP"
assert portfolio["rounds_completed"] == 1363 and len(portfolio["rounds"]) == 1
selected = portfolio["rounds"][0]
assert selected["selected_strategy"] in {"repair", "cold"}
assert selected["selected_pivot"] in {"first", "last", "rare"}

clone("selected_control", checkpoint, vectors)
watched("selected_control", command("selected_control", selected["selected_pivot"],
                                    selected["selected_strategy"], 1750000, 120, 256), 135)
cap_candidate_run = selected["selected_strategy"] == "cold" and selected["selected_pivot"] == "rare"
if cap_candidate_run:
    clone("cap2000_candidate", checkpoint, vectors)
    watched("cap2000_candidate", command("cap2000_candidate", "rare", "cold", 2000000, 120, 256), 135)
value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1363_INTERNAL_SEQUENTIAL_RUNNER_V1",
    "status": "RUNS_TERMINAL_PENDING_VALIDATION",
    "selected_strategy": selected["selected_strategy"],
    "selected_pivot": selected["selected_pivot"],
    "conditional_cap_candidate_run": cap_candidate_run,
    "continued_beyond_round1363": False,
}
temporary = HERE / "runner_summary.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "runner_summary.json")
print(json.dumps(value, sort_keys=True))
