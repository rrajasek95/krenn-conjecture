#!/usr/bin/env python3
"""Fail-closed final validator for round1262 portfolio/cap gate outputs."""
import hashlib
import json
import os
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = REPO / "computations/unaudited-codex-n8-affine251-d12-round1061-portfolio-audit-2026-08-25/audit_source/src/main.rs"
BINARY = REPO / "computations/unaudited-codex-n8-affine251-d12-round1061-portfolio-audit-2026-08-25/audit_source/sparse_d12_dual"
WATCHDOG = HERE / "run_with_macos_rss_watchdog_v2_155.py"


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


pins = json.loads((HERE / "LAUNCH_PINS.json").read_text())
summary = json.loads((HERE / "runner_summary.json").read_text())
assert pins["status"] == "PASS_FROZEN_SEALED_ROUND1261_INPUT"
assert summary["status"] == "RUNS_TERMINAL_PENDING_VALIDATION"
assert sha256(SOURCE) == "2cf629054e1b5e2350617b71114544b7d0c7a47f811b67b6dea4483e5e911230"
assert sha256(BINARY) == "ade47c27a96314bb4391241a60a372c79e643a44b8a62a00054fffc576ccc7ce"
assert sha256(WATCHDOG) == "48fe528b15c31b8ed6446eb10628b0bcb598191efaac64dd59021881b80b1522"

failure_audit = json.loads((HERE / "FAILURE_AUDIT.json").read_text())
failure_watch = json.loads((HERE / "portfolio_failed120/watchdog.json").read_text())
assert failure_audit["status"] == "PASS_FAIL_CLOSED_NO_STATE_ACCEPTED"
assert sha256(HERE / "portfolio_failed120/watchdog.json") == failure_audit["watchdog_sha256"]
assert failure_watch["breach"] == "WALL_CAP" and failure_watch["returncode"] == -15
assert not (HERE / "portfolio_failed120/result.json").exists()
assert sha256(HERE / "portfolio_failed120/checkpoint.bin") == pins["checkpoint_sha256"]
assert sha256(HERE / "portfolio_failed120/vectors.bin") == pins["vectors_sha256"]

labels = ["portfolio_retry155", "selected_control"]
if summary["cap1500_candidate_run"]:
    labels.append("cap1500_candidate")
results = {label: json.loads((HERE / label / "result.json").read_text()) for label in labels}
watches = {label: json.loads((HERE / label / "watchdog.json").read_text()) for label in labels}
for label in labels:
    result, watch = results[label], watches[label]
    assert result["status"] == "INCOMPLETE_SEARCH_CAP"
    assert result["incomplete_reason"] == "ROUND_CAP"
    assert result["rounds_completed"] == 1262
    assert result["cached_vectors_loaded"] == 1238541
    assert result["vectors_materialized_on_restore"] == 0
    assert len(result["rounds"]) == 1 and result["rounds"][0]["round"] == 1262
    assert watch["status"] == "PASS" and watch["returncode"] == 0
    assert watch["breach"] is None and watch["atomic_outputs_clean"]
    wall_limit = 155 if label == "portfolio_retry155" else 120
    assert watch["elapsed_seconds"] < wall_limit and watch["peak_rss_kib"] < 36 * 1024 * 1024
    command = watch["command"]
    assert argument(command, "--round-cap") == "1262"
    assert argument(command, "--workers") == "16"
    assert argument(command, "--elimination") == "tree"
    assert argument(command, "--portfolio-period") == "1"
    assert argument(command, "--portfolio-parallel") == "yes"
    assert argument(command, "--support-cap") == "100000"

portfolio_round = results["portfolio_retry155"]["rounds"][0]
selected = (portfolio_round["selected_strategy"], portfolio_round["selected_pivot"])
assert selected[0] in {"cold", "repair"} and selected[1] in {"first", "last", "rare"}
assert argument(watches["portfolio_retry155"]["command"], "--strategy") == "best"
assert argument(watches["portfolio_retry155"]["command"], "--pivot") == "auto"
assert argument(watches["portfolio_retry155"]["command"], "--column-cap") == "1250000"
assert argument(watches["portfolio_retry155"]["command"], "--wall-seconds") == "145"
assert argument(watches["selected_control"]["command"], "--strategy") == selected[0]
assert argument(watches["selected_control"]["command"], "--pivot") == selected[1]
assert argument(watches["selected_control"]["command"], "--column-cap") == "1250000"

round_fields = ["round", "columns", "new_columns", "dual_support", "new_support_rows",
                "selected_strategy", "selected_pivot"]
round_records = {
    label: {key: results[label]["rounds"][0][key] for key in round_fields}
    for label in labels
}
assert round_records["portfolio_retry155"] == round_records["selected_control"]
checkpoint_hashes = {label: sha256(HERE / label / "checkpoint.bin") for label in labels}
vector_hashes = {label: sha256(HERE / label / "vectors.bin") for label in labels}
assert len({checkpoint_hashes["portfolio_retry155"], checkpoint_hashes["selected_control"]}) == 1
assert len({vector_hashes["portfolio_retry155"], vector_hashes["selected_control"]}) == 1

cap_required = selected == ("cold", "rare")
assert summary["cap1500_candidate_run"] == cap_required
assert (HERE / "cap1500_candidate").exists() == cap_required
if cap_required:
    assert round_records["cap1500_candidate"] == round_records["selected_control"]
    assert len(set(checkpoint_hashes.values())) == 1
    assert len(set(vector_hashes.values())) == 1
    control_command = watches["selected_control"]["command"]
    candidate_command = watches["cap1500_candidate"]["command"]
    assert len(control_command) == len(candidate_command)
    differences = [(index, left, right) for index, (left, right) in
                   enumerate(zip(control_command, candidate_command)) if left != right]
    # Output paths differ by directory; after normalizing them, only the cap value may differ.
    normalized_control = [item.replace("/selected_control/", "/RUN/") for item in control_command]
    normalized_candidate = [item.replace("/cap1500_candidate/", "/RUN/") for item in candidate_command]
    normalized_differences = [(index, left, right) for index, (left, right) in
                              enumerate(zip(normalized_control, normalized_candidate)) if left != right]
    assert normalized_differences == [(
        normalized_control.index("1250000"), "1250000", "1500000"
    )]

header = checkpoint_header(HERE / "selected_control/checkpoint.bin")
vectors = vectors_header(HERE / "selected_control/vectors.bin")
assert header["prime"] == 1073741827 and header["round"] == 1262
assert header["columns"] == round_records["selected_control"]["columns"]
assert header["support"] == round_records["selected_control"]["dual_support"]
assert vectors["prime"] == 1073741827 and vectors["provider"] == 9218588987274412661
assert vectors["columns"] == header["columns"]

artifacts = {}
for label in labels:
    for filename in ("result.json", "checkpoint.bin", "vectors.bin", "watchdog.json",
                     "stderr.log", "stdout.log"):
        artifacts[f"{label}/{filename}"] = sha256(HERE / label / filename)
value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1262_PORTFOLIO_CAP1500_AUDIT_V1",
    "status": "PASS_EXACT_ROUND1262_PORTFOLIO_AND_CONDITIONAL_CAP_EQUIVALENCE",
    "scope": "One exact round only; cap promotion is config-only and no continuation was run.",
    "input": pins,
    "portfolio": {
        "task_count": 6, "strategies": ["cold", "repair"],
        "pivots": ["first", "last", "rare"],
        "selected_strategy": selected[0], "selected_pivot": selected[1],
        "watchdog_seconds": watches["portfolio_retry155"]["elapsed_seconds"],
        "peak_rss_kib": watches["portfolio_retry155"]["peak_rss_kib"],
        "retry_geometry": {"native_wall_seconds": 145, "watchdog_wall_seconds": 155},
    },
    "fixed_replay": {
        "semantic_round_record_identical": True,
        "checkpoint_byte_identical": True,
        "vectors_byte_identical": True,
        "watchdog_seconds": watches["selected_control"]["elapsed_seconds"],
        "peak_rss_kib": watches["selected_control"]["peak_rss_kib"],
    },
    "cap1500": {
        "required_and_run": cap_required,
        "only_normalized_command_difference_is_column_cap": cap_required,
        "checkpoint_byte_identical": cap_required,
        "vectors_byte_identical": cap_required,
        "promotion_scope": "May change production command from --column-cap 1250000 to 1500000; no source patch.",
    },
    "output": {**header, "new_columns": round_records["selected_control"]["new_columns"],
               "new_support_rows": round_records["selected_control"]["new_support_rows"]},
    "output_checkpoint_sha256": checkpoint_hashes["selected_control"],
    "output_vectors_sha256": vector_hashes["selected_control"],
    "production_source_mutated": False,
    "continued_beyond_round1262": False,
    "artifact_sha256": artifacts,
}
temporary = HERE / "results_round1262_audit.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_round1262_audit.json")
print(json.dumps(value, sort_keys=True))
