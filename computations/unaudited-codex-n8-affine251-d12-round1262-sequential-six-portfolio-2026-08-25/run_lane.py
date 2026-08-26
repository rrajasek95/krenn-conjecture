#!/usr/bin/env python3
"""Run exactly one frozen fixed lane; never select or continue."""
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCHEDULE = HERE / "SCHEDULE.json"
SOURCE = REPO / "computations/unaudited-codex-n8-affine251-d12-round1061-portfolio-audit-2026-08-25/audit_source/src/main.rs"
BINARY = REPO / "computations/unaudited-codex-n8-affine251-d12-round1061-portfolio-audit-2026-08-25/audit_source/sparse_d12_dual"
WATCHDOG = REPO / "computations/unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/run_with_macos_rss_watchdog_v2.py"
PROVIDER = REPO / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/canonical_triangle_pair_offdiag_full_p1073741827.ms"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def checkpoint_header(path):
    with path.open("rb") as stream:
        data = stream.read(44)
    assert data[:12] == b"AFF12CEG1\0\0\0"
    prime, round_number, columns, support = struct.unpack_from("<QQQQ", data, 12)
    return prime, round_number, columns, support


if len(sys.argv) != 2 or not sys.argv[1].isdigit():
    raise SystemExit("usage: run_lane.py LANE_NUMBER")
lane_number = int(sys.argv[1])
schedule = json.loads(SCHEDULE.read_text())
assert schedule["status"] == "FROZEN_READY_LANE1"
lanes = {item["lane"]: item for item in schedule["execution_order"]}
assert set(lanes) == set(range(1, 7))
assert lane_number in lanes
lane = lanes[lane_number]
directory = HERE / lane["label"]
assert not directory.exists(), f"refuse pre-existing lane directory: {directory}"

input_spec = schedule["input"]
checkpoint = REPO / input_spec["checkpoint"]
vectors = REPO / input_spec["vectors"]
manifest = REPO / "computations/unaudited-codex-n8-affine251-d12-v4-1-round1261-audit-2026-08-25/FINAL_MANIFEST.sha256"
assert sha256(manifest) == input_spec["audit_manifest_sha256"]
assert sha256(checkpoint) == input_spec["checkpoint_sha256"]
assert sha256(vectors) == input_spec["vectors_sha256"]
assert checkpoint_header(checkpoint) == (1073741827, 1261, 1238541, 1065)
assert sha256(SOURCE) == schedule["producer"]["source_sha256"]
assert sha256(BINARY) == schedule["producer"]["binary_sha256"]
assert sha256(WATCHDOG) == schedule["producer"]["watchdog_sha256"]

directory.mkdir()
subprocess.run(["cp", "-c", str(checkpoint), str(directory / "checkpoint.bin")], check=True)
subprocess.run(["cp", "-c", str(vectors), str(directory / "vectors.bin")], check=True)
command = [
    str(BINARY), "--input", str(PROVIDER),
    "--output", str(directory / "result.json"),
    "--checkpoint", str(directory / "checkpoint.bin"),
    "--vector-cache", str(directory / "vectors.bin"),
    "--dual", str(directory / "dual.tsv"),
    "--prime", "1073741827", "--wall-seconds", "110", "--rss-gib", "36",
    "--workers", "16", "--pivot", lane["pivot"], "--strategy", lane["strategy"],
    "--elimination", "tree", "--incremental", "no",
    "--portfolio-period", "1", "--portfolio-parallel", "yes",
    "--support-cap", "100000", "--column-cap", "1250000", "--round-cap", "1262",
]
wrapper = [
    sys.executable, str(WATCHDOG), "--rss-gib", "36", "--wall-seconds", "120",
    "--poll-seconds", "0.25", "--source", str(SOURCE),
    "--expected-source-sha256", schedule["producer"]["source_sha256"],
    "--expected-binary-sha256", schedule["producer"]["binary_sha256"],
    "--telemetry", str(directory / "watchdog.json"),
    "--stdout", str(directory / "stdout.log"),
    "--stderr", str(directory / "stderr.log"), "--", *command,
]
subprocess.run(wrapper, cwd=REPO, check=True)
result = json.loads((directory / "result.json").read_text())
watch = json.loads((directory / "watchdog.json").read_text())
assert result["status"] == "INCOMPLETE_SEARCH_CAP" and result["incomplete_reason"] == "ROUND_CAP"
assert result["rounds_completed"] == 1262 and len(result["rounds"]) == 1
record = result["rounds"][0]
assert record["round"] == 1262
assert record["selected_strategy"] == lane["strategy"] and record["selected_pivot"] == lane["pivot"]
assert result["cached_vectors_loaded"] == 1238541 and result["vectors_materialized_on_restore"] == 0
assert watch["status"] == "PASS" and watch["returncode"] == 0 and watch["breach"] is None
assert watch["elapsed_seconds"] < 120 and watch["peak_rss_kib"] < 36 * 1024 * 1024
value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1262_FIXED_LANE_ACCEPTANCE_V1",
    "status": "PASS_CANDIDATE_NOT_SELECTED",
    "lane": lane,
    "round_record": record,
    "checkpoint_sha256": sha256(directory / "checkpoint.bin"),
    "vectors_sha256": sha256(directory / "vectors.bin"),
    "result_sha256": sha256(directory / "result.json"),
    "watchdog_sha256": sha256(directory / "watchdog.json"),
    "watchdog_elapsed_seconds": watch["elapsed_seconds"],
    "peak_rss_kib": watch["peak_rss_kib"],
    "selected": False,
    "continued_beyond_round1262": False,
}
temporary = directory / "lane_acceptance.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, directory / "lane_acceptance.json")
print(json.dumps(value, sort_keys=True))
