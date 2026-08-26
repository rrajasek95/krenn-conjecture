#!/usr/bin/env python3
"""Fail-closed validation for round1363 portfolio/fixed/conditional cap equivalence."""
import hashlib
import json
import os
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
SCHEDULE = json.loads((HERE / "SCHEDULE.json").read_text())


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def argument(command, flag):
    assert command.count(flag) == 1
    return command[command.index(flag) + 1]


def normalized(command, label):
    return [item.replace(f"/{label}/", "/RUN/") for item in command]


def checkpoint_header(path):
    with path.open("rb") as stream:
        data = stream.read(44)
    assert data[:12] == b"AFF12CEG1\0\0\0"
    prime, round_number, columns, support = struct.unpack_from("<QQQQ", data, 12)
    assert path.stat().st_size == 44 + 15 * columns + 21 * support
    return {"prime": prime, "round": round_number, "columns": columns, "support": support}


pins = json.loads((HERE / "FUTURE_INPUT_PINS.json").read_text())
summary = json.loads((HERE / "runner_summary.json").read_text())
assert pins["status"] == "PASS_FROZEN_INDEPENDENT_ROUND1362_FINAL_REPLAY_CLEAR"
assert summary["status"] == "RUNS_TERMINAL_PENDING_VALIDATION"
labels = ["portfolio", "selected_control"]
if summary["conditional_cap_candidate_run"]:
    labels.append("cap2000_candidate")
results = {label: json.loads((HERE / label / "result.json").read_text()) for label in labels}
watches = {label: json.loads((HERE / label / "watchdog.json").read_text()) for label in labels}
for label in labels:
    result, watch = results[label], watches[label]
    assert result["status"] == "INCOMPLETE_SEARCH_CAP" and result["incomplete_reason"] == "ROUND_CAP"
    assert result["rounds_completed"] == 1363 and len(result["rounds"]) == 1
    assert result["cached_vectors_loaded"] == pins["checkpoint_header"]["columns"]
    assert result["vectors_materialized_on_restore"] == 0
    assert watch["status"] == "PASS" and watch["returncode"] == 0 and watch["breach"] is None
    assert watch["peak_rss_kib"] < 36 * 1024 * 1024
    for flag, value in [("--round-cap", "1363"), ("--workers", "16"),
                        ("--elimination", "tree"), ("--incremental", "no"),
                        ("--portfolio-parallel", "no")]:
        assert argument(watch["command"], flag) == value
assert watches["portfolio"]["elapsed_seconds"] < 540
assert argument(watches["portfolio"]["command"], "--wall-seconds") == "520"
assert argument(watches["portfolio"]["command"], "--pivot") == "auto"
assert argument(watches["portfolio"]["command"], "--strategy") == "best"
assert argument(watches["portfolio"]["command"], "--portfolio-period") == "1"
assert argument(watches["portfolio"]["command"], "--column-cap") == "1750000"
winner = (summary["selected_strategy"], summary["selected_pivot"])
fixed_command = watches["selected_control"]["command"]
assert argument(fixed_command, "--strategy") == winner[0]
assert argument(fixed_command, "--pivot") == winner[1]
assert argument(fixed_command, "--column-cap") == "1750000"
assert watches["selected_control"]["elapsed_seconds"] < 135

round_fields = ["round", "columns", "new_columns", "dual_support", "new_support_rows",
                "selected_strategy", "selected_pivot"]
records = {label: {key: results[label]["rounds"][0][key] for key in round_fields} for label in labels}
assert records["portfolio"] == records["selected_control"]
checkpoint_hashes = {label: sha256(HERE / label / "checkpoint.bin") for label in labels}
vector_hashes = {label: sha256(HERE / label / "vectors.bin") for label in labels}
assert checkpoint_hashes["portfolio"] == checkpoint_hashes["selected_control"]
assert vector_hashes["portfolio"] == vector_hashes["selected_control"]
assert all(not (HERE / label / "dual.tsv").exists() for label in labels)
cap_equivalence = None
if summary["conditional_cap_candidate_run"]:
    assert winner == ("cold", "rare")
    assert records["selected_control"] == records["cap2000_candidate"]
    assert checkpoint_hashes["selected_control"] == checkpoint_hashes["cap2000_candidate"]
    assert vector_hashes["selected_control"] == vector_hashes["cap2000_candidate"]
    left = normalized(fixed_command, "selected_control")
    right = normalized(watches["cap2000_candidate"]["command"], "cap2000_candidate")
    differences = [(index, a, b) for index, (a, b) in enumerate(zip(left, right)) if a != b]
    assert differences == [(left.index("1750000"), "1750000", "2000000")]
    cap_equivalence = {"status": "PASS_EXACT_CAP1750_TO_CAP2000_EQUIVALENCE",
                       "sole_normalized_difference_is_cap": True}
else:
    assert winner != ("cold", "rare")
    assert not (HERE / "cap2000_candidate").exists()
    cap_equivalence = {"status": "NOT_RUN_WINNER_WAS_NOT_COLD_RARE"}
header = checkpoint_header(HERE / "selected_control/checkpoint.bin")
assert header["round"] == 1363 and header["columns"] == records["selected_control"]["columns"]
assert header["support"] == records["selected_control"]["dual_support"]
value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1363_INTERNAL_SEQUENTIAL_AUDIT_V1",
    "status": "PASS_EXACT_INTERNAL_SIX_PORTFOLIO_AND_FIXED_REPLAY",
    "winner": {"strategy": winner[0], "pivot": winner[1]},
    "round_record": records["selected_control"],
    "portfolio_fixed_checkpoint_byte_identical": True,
    "portfolio_fixed_vectors_byte_identical": True,
    "cap_equivalence": cap_equivalence,
    "output_checkpoint_sha256": checkpoint_hashes["selected_control"],
    "output_vectors_sha256": vector_hashes["selected_control"],
    "maximum_peak_rss_kib": max(watches[label]["peak_rss_kib"] for label in labels),
    "production_mutated": False,
    "continued_beyond_round1363": False,
}
temporary = HERE / "results_round1363_audit.json.tmp"
temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_round1363_audit.json")
print(json.dumps(value, sort_keys=True))
