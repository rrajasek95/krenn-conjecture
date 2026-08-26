#!/usr/bin/env python3
"""Fail-closed validator for internal sequential portfolio and cap equivalence."""
import hashlib
import json
import os
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCHEDULE = json.loads((HERE / "SCHEDULE.json").read_text())
SOURCE = REPO / "computations/unaudited-codex-n8-affine251-d12-round1061-portfolio-audit-2026-08-25/audit_source/src/main.rs"
BINARY = REPO / "computations/unaudited-codex-n8-affine251-d12-round1061-portfolio-audit-2026-08-25/audit_source/sparse_d12_dual"
WATCHDOG = HERE / "run_with_macos_rss_watchdog_v2_540.py"
DESIGN_AUDIT = REPO / "computations/unaudited-codex-n8-affine251-d12-round1262-internal-sequential-design-audit-2026-08-25"
FAILED = REPO / "computations/unaudited-codex-n8-affine251-d12-round1262-portfolio-cap1500-gate-2026-08-25"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def argument(command, flag):
    assert command.count(flag) == 1
    return command[command.index(flag) + 1]


def checkpoint_header(path):
    with path.open("rb") as stream:
        data = stream.read(44)
    assert data[:12] == b"AFF12CEG1\0\0\0"
    prime, round_number, columns, support = struct.unpack_from("<QQQQ", data, 12)
    assert path.stat().st_size == 44 + 15 * columns + 21 * support
    return {"prime": prime, "round": round_number, "columns": columns, "support": support}


def vectors_header(path):
    with path.open("rb") as stream:
        data = stream.read(44)
    assert data[:12] == b"AFF12VEC1\0\0\0"
    prime, provider, fingerprint, columns = struct.unpack_from("<QQQQ", data, 12)
    return {"prime": prime, "provider": provider, "fingerprint": fingerprint,
            "columns": columns, "bytes": path.stat().st_size}


assert sha256(SOURCE) == SCHEDULE["engine"]["source_sha256"]
assert sha256(BINARY) == SCHEDULE["engine"]["binary_sha256"]
assert sha256(WATCHDOG) == SCHEDULE["engine"]["watchdog540_sha256"]
assert sha256(DESIGN_AUDIT / "FINAL_MANIFEST.sha256") == \
    "4b2aa7f6823ae02ec51bbff95573d56d30d084550b2cf358404f75f3ee0a787f"
assert sha256(DESIGN_AUDIT / "results_design_audit.json") == \
    "8c6845c6178824cc1bccda54a234b2c2ab3b986f852d38e99e37b1f92a02111d"
for label, expected_watch in [
    ("portfolio_failed120", "6a6b28de20aa8e14f7dd9717d9457969beef3bb510faa10d24e5de9cc7b14477"),
    ("portfolio_failed155", "42f0f8b15c25101dfdefc6c5f3e5ebeb53a05f3f028ea6287ee091cc108042ec"),
]:
    directory = FAILED / label
    assert sha256(directory / "watchdog.json") == expected_watch
    failed_watch = json.loads((directory / "watchdog.json").read_text())
    assert failed_watch["breach"] == "WALL_CAP" and failed_watch["returncode"] == -15
    assert not (directory / "result.json").exists()

labels = ["portfolio", "selected_control", "cap1500_candidate"]
results = {label: json.loads((HERE / label / "result.json").read_text()) for label in labels}
watches = {label: json.loads((HERE / label / "watchdog.json").read_text()) for label in labels}
for label in labels:
    result, watch = results[label], watches[label]
    assert result["status"] == "INCOMPLETE_SEARCH_CAP" and result["incomplete_reason"] == "ROUND_CAP"
    assert result["rounds_completed"] == 1262 and len(result["rounds"]) == 1
    assert result["cached_vectors_loaded"] == 1238541 and result["vectors_materialized_on_restore"] == 0
    assert watch["status"] == "PASS" and watch["returncode"] == 0 and watch["breach"] is None
    assert watch["peak_rss_kib"] < 36 * 1024 * 1024
    command = watch["command"]
    assert argument(command, "--round-cap") == "1262"
    assert argument(command, "--workers") == "16"
    assert argument(command, "--elimination") == "tree"
    assert argument(command, "--incremental") == "no"
    assert argument(command, "--portfolio-period") == "1"
    assert argument(command, "--portfolio-parallel") == "no"
assert watches["portfolio"]["elapsed_seconds"] < 540
assert argument(watches["portfolio"]["command"], "--wall-seconds") == "520"
assert argument(watches["portfolio"]["command"], "--pivot") == "auto"
assert argument(watches["portfolio"]["command"], "--strategy") == "best"
assert argument(watches["portfolio"]["command"], "--column-cap") == "1250000"
for label in ("selected_control", "cap1500_candidate"):
    assert watches[label]["elapsed_seconds"] < 120
    assert argument(watches[label]["command"], "--wall-seconds") == "110"
    assert argument(watches[label]["command"], "--pivot") == "rare"
    assert argument(watches[label]["command"], "--strategy") == "cold"

fields = ["round", "columns", "new_columns", "dual_support", "new_support_rows",
          "selected_strategy", "selected_pivot"]
records = {label: {key: results[label]["rounds"][0][key] for key in fields} for label in labels}
expected_record = {"round": 1262, "columns": 1240851, "new_columns": 2310,
                   "dual_support": 1098, "new_support_rows": 567,
                   "selected_strategy": "cold", "selected_pivot": "rare"}
assert all(record == expected_record for record in records.values())

checkpoint_hashes = {label: sha256(HERE / label / "checkpoint.bin") for label in labels}
vector_hashes = {label: sha256(HERE / label / "vectors.bin") for label in labels}
assert len(set(checkpoint_hashes.values())) == 1
assert len(set(vector_hashes.values())) == 1
control_command = watches["selected_control"]["command"]
candidate_command = watches["cap1500_candidate"]["command"]
normalized_control = [item.replace("/selected_control/", "/RUN/") for item in control_command]
normalized_candidate = [item.replace("/cap1500_candidate/", "/RUN/") for item in candidate_command]
differences = [(index, left, right) for index, (left, right) in
               enumerate(zip(normalized_control, normalized_candidate)) if left != right]
assert differences == [(normalized_control.index("1250000"), "1250000", "1500000")]

header = checkpoint_header(HERE / "selected_control/checkpoint.bin")
vector_header = vectors_header(HERE / "selected_control/vectors.bin")
assert header == {"prime": 1073741827, "round": 1262, "columns": 1240851, "support": 1098}
assert vector_header["prime"] == 1073741827 and vector_header["provider"] == 9218588987274412661
assert vector_header["columns"] == 1240851

artifacts = {}
for label in labels:
    for filename in ("result.json", "watchdog.json", "stderr.log", "stdout.log",
                     "checkpoint.bin", "vectors.bin"):
        artifacts[f"{label}/{filename}"] = sha256(HERE / label / filename)
value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1262_INTERNAL_SEQUENTIAL_AUDIT_V1",
    "status": "PASS_EXACT_INTERNAL_SIX_PORTFOLIO_AND_CAP1500_EQUIVALENCE",
    "portfolio": {"ordered_task_count": 6, "selected_strategy": "cold", "selected_pivot": "rare",
                  "watchdog_seconds": watches["portfolio"]["elapsed_seconds"],
                  "peak_rss_kib": watches["portfolio"]["peak_rss_kib"]},
    "fixed_replay": {"semantic_record_identical": True, "state_byte_identical": True,
                     "watchdog_seconds": watches["selected_control"]["elapsed_seconds"],
                     "peak_rss_kib": watches["selected_control"]["peak_rss_kib"]},
    "cap1500": {"only_normalized_command_difference_is_cap": True,
                "state_byte_identical": True,
                "watchdog_seconds": watches["cap1500_candidate"]["elapsed_seconds"],
                "peak_rss_kib": watches["cap1500_candidate"]["peak_rss_kib"]},
    "output": {**header, "new_columns": 2310, "new_support_rows": 567},
    "output_checkpoint_sha256": checkpoint_hashes["selected_control"],
    "output_vectors_sha256": vector_hashes["selected_control"],
    "output_vectors_header": vector_header,
    "failed_parallel_attempts_accepted_coverage": 0,
    "design_audit_sha256": "8c6845c6178824cc1bccda54a234b2c2ab3b986f852d38e99e37b1f92a02111d",
    "production_mutated": False,
    "continued_beyond_round1262": False,
    "artifact_sha256": artifacts,
}
temporary = HERE / "results_round1262_audit.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_round1262_audit.json")
print(json.dumps(value, sort_keys=True))
