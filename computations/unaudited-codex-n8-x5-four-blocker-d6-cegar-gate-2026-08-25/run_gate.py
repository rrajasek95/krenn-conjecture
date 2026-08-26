#!/usr/bin/env python3
"""Run the four frozen blocker branches sequentially under independent watchdogs."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCHEDULE = json.loads((HERE / "SCHEDULE.json").read_text())


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


source = HERE / SCHEDULE["engine"]["source"]
binary = HERE / SCHEDULE["engine"]["binary"]
watchdog = REPO / SCHEDULE["watchdog"]["path"]
assert sha256(source) == SCHEDULE["engine"]["source_sha256"]
assert sha256(binary) == SCHEDULE["engine"]["binary_sha256"]
assert sha256(watchdog) == SCHEDULE["watchdog"]["sha256"]
assert sha256(REPO / SCHEDULE["source_contract"]["exporter"]) == SCHEDULE["source_contract"]["exporter_sha256"]
assert sha256(REPO / SCHEDULE["source_contract"]["canonical_manifest"]) == SCHEDULE["source_contract"]["canonical_manifest_sha256"]

records = []
for branch in SCHEDULE["branches"]:
    provider_spec = SCHEDULE["providers"][branch]
    provider = HERE / provider_spec["path"]
    assert sha256(provider) == provider_spec["sha256"]
    directory = HERE / f"branch_{branch}"
    assert not directory.exists(), f"refuse pre-existing branch output {directory}"
    directory.mkdir()
    native = [
        str(binary),
        "--branch", branch,
        "--input", str(provider),
        "--output", str(directory / "result.json"),
        "--selected", str(directory / "selected.tsv"),
        "--dual", str(directory / "dual.tsv"),
        "--prime", str(SCHEDULE["engine"]["prime"]),
        "--column-cap", str(SCHEDULE["engine"]["column_cap"]),
        "--wall-seconds", str(SCHEDULE["engine"]["native_wall_seconds"]),
    ]
    wrapper = [
        sys.executable, str(watchdog),
        "--rss-gib", str(SCHEDULE["engine"]["rss_gib"]),
        "--wall-seconds", str(SCHEDULE["engine"]["wrapper_wall_seconds"]),
        "--poll-seconds", "0.25",
        "--source", str(source),
        "--expected-source-sha256", SCHEDULE["engine"]["source_sha256"],
        "--expected-binary-sha256", SCHEDULE["engine"]["binary_sha256"],
        "--telemetry", str(directory / "watchdog.json"),
        "--stdout", str(directory / "stdout.log"),
        "--stderr", str(directory / "stderr.log"),
        "--", *native,
    ]
    completed = subprocess.run(wrapper, cwd=REPO, check=False)
    record = {
        "branch": branch,
        "wrapper_returncode": completed.returncode,
        "result_exists": (directory / "result.json").exists(),
        "watchdog_exists": (directory / "watchdog.json").exists(),
    }
    if record["result_exists"]:
        result = json.loads((directory / "result.json").read_text())
        record["engine_status"] = result["status"]
        record["selected_columns"] = result["selected_columns"]
        record["dual_support"] = result["dual_support"]
        record["elapsed_seconds"] = result["elapsed_seconds"]
    records.append(record)

summary = {
    "schema": "KRENN_X5_FOUR_BLOCKER_D6_CEGAR_RUNNER_SUMMARY_V1",
    "status": "FOUR_SEQUENTIAL_RUNS_TERMINAL_PENDING_INDEPENDENT_VALIDATION",
    "records": records,
    "continued_beyond_degree6": False,
    "d12_caches_read": False,
}
temporary = HERE / "runner_summary.json.tmp"
temporary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "runner_summary.json")
print(json.dumps(summary, sort_keys=True))
