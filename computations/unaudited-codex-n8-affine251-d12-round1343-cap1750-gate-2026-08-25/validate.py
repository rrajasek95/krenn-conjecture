#!/usr/bin/env python3
"""Fail-closed validator for the round1343 cap-only equivalence gate."""
import hashlib
import json
import os
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent


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


pins = json.loads((HERE / "LAUNCH_PINS.json").read_text())
summary = json.loads((HERE / "runner_summary.json").read_text())
assert pins["status"] == "PASS_FROZEN_SEALED_ROUND1342_INPUT"
assert summary["status"] == "RUNS_TERMINAL_PENDING_VALIDATION"
labels = ["cap1500_control", "cap1750_candidate"]
results = {label: json.loads((HERE / label / "result.json").read_text()) for label in labels}
watches = {label: json.loads((HERE / label / "watchdog.json").read_text()) for label in labels}
for label in labels:
    result, watch = results[label], watches[label]
    assert result["status"] == "INCOMPLETE_SEARCH_CAP" and result["incomplete_reason"] == "ROUND_CAP"
    assert result["rounds_completed"] == 1343 and len(result["rounds"]) == 1
    assert result["cached_vectors_loaded"] == 1491824 and result["vectors_materialized_on_restore"] == 0
    assert watch["status"] == "PASS" and watch["returncode"] == 0 and watch["breach"] is None
    assert watch["elapsed_seconds"] < 115 and watch["peak_rss_kib"] < 36 * 1024 * 1024
    command = watch["command"]
    for flag, value in [("--round-cap", "1343"), ("--workers", "16"),
                        ("--pivot", "rare"), ("--strategy", "cold"),
                        ("--elimination", "hierarchical"), ("--incremental", "no"),
                        ("--wall-seconds", "90"), ("--rss-gib", "36")]:
        assert argument(command, flag) == value
fields = ["round", "columns", "new_columns", "dual_support", "new_support_rows",
          "selected_strategy", "selected_pivot"]
records = {label: {key: results[label]["rounds"][0][key] for key in fields} for label in labels}
assert records[labels[0]] == records[labels[1]]
semantic_top_level_fields = [
    "schema", "status", "incomplete_reason", "degree", "prime", "group_order",
    "provider_equations", "provider_terms_parsed", "provider_distinct_terms",
    "seed_support", "column_orbits_exposed", "dual_support", "rounds_completed",
    "global_annihilation", "target_pairing", "workers", "pivot_mode", "strategy",
    "elimination_kernel", "incremental_basis", "portfolio_period",
    "portfolio_parallel", "support_cap", "wall_limit_seconds", "rss_limit_gib",
    "cached_vectors_loaded", "vectors_materialized_on_restore", "vector_cache_bytes",
]
semantic_top_levels = {
    label: {key: results[label][key] for key in semantic_top_level_fields}
    for label in labels
}
assert semantic_top_levels[labels[0]] == semantic_top_levels[labels[1]]
checkpoint_hashes = {label: sha256(HERE / label / "checkpoint.bin") for label in labels}
vector_hashes = {label: sha256(HERE / label / "vectors.bin") for label in labels}
assert len(set(checkpoint_hashes.values())) == 1 and len(set(vector_hashes.values())) == 1
assert all(not (HERE / label / "dual.tsv").exists() for label in labels)
control = watches[labels[0]]["command"]
candidate = watches[labels[1]]["command"]
left = [item.replace("/cap1500_control/", "/RUN/") for item in control]
right = [item.replace("/cap1750_candidate/", "/RUN/") for item in candidate]
differences = [(index, a, b) for index, (a, b) in enumerate(zip(left, right)) if a != b]
assert differences == [(left.index("1500000"), "1500000", "1750000")]
header = checkpoint_header(HERE / "cap1500_control/checkpoint.bin")
assert header["prime"] == 1073741827 and header["round"] == 1343
assert header["columns"] == records[labels[0]]["columns"]
assert header["support"] == records[labels[0]]["dual_support"]
value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1343_CAP1750_AUDIT_V1",
    "status": "PASS_EXACT_CAP1500_TO_CAP1750_EQUIVALENCE",
    "input": pins,
    "round_record": records[labels[0]],
    "semantic_top_level_fields": semantic_top_level_fields,
    "checkpoint_sha256": checkpoint_hashes[labels[0]],
    "vectors_sha256": vector_hashes[labels[0]],
    "dual_outputs_absent_for_incomplete_round_cap": True,
    "control_watchdog_seconds": watches[labels[0]]["elapsed_seconds"],
    "candidate_watchdog_seconds": watches[labels[1]]["elapsed_seconds"],
    "maximum_peak_rss_kib": max(watches[label]["peak_rss_kib"] for label in labels),
    "only_normalized_command_difference_is_cap": True,
    "production_mutated": False,
    "continued_beyond_round1343": False,
  }
temporary = HERE / "results_round1343_cap_audit.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_round1343_cap_audit.json")
print(json.dumps(value, sort_keys=True))
