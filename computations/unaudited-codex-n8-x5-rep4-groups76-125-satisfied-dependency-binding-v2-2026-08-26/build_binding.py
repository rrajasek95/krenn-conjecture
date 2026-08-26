#!/usr/bin/env python3
"""Bind sealed rep4 groups 1..75 into the unchanged groups76..125 held batch."""
from __future__ import annotations
import hashlib, json, os, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = ROOT / "computations"
HELD = C / "unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-2026-08-26"
HELD_REF = C / "unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-referee-2026-08-26"
FIRST = C / "unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26"
FIRST_REF = C / "unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26"
SECOND = C / "unaudited-codex-n8-x5-rep4-groups26-75-exact-q-conditional-held-2026-08-26"
SECOND_REF = C / "unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26"

PINS = {
    HELD / "MANIFEST.sha256": "0d2d7cfce0ed9e862b573e4fdc5791b3384c7bd21fbd6e9ff9e663c79f387115",
    HELD / "source_ledger.json": "b311e566fab04932f0c49a285ac3190ae4ac7a02f102799a9a2c6b34a949e4bb",
    HELD / "run_groups76_125.py": "3e5a744b6017dc0ba4a4d9789039bb4697d20fd1b42332195dc015cfd1e91abd",
    HELD / "normalize_dependencies.py": "5afc90779b09c31950e30cb7f11cb198d9c37f5d655e6926fcfad2980561733c",
    HELD / "future_dependencies.json": "02e042533a68fb7a9a08d230caa7de915c3176e4d7e54b8f68a9704da7e6916e",
    HELD / "independent_referee_acceptance.schema.json": "f9b440bcd45fd3ca97f72f81c9426c3ef575665d43f3dc8225e0f1ba6d0f0e22",
    HELD_REF / "results_referee.json": "ce1105db2dedaa71bd7639df4cd758561500ad0430d9d2c55b12beaac40e928c",
    HELD_REF / "HELD_APPROVAL.json": "210579d2e3367ce954d4168cc174c24c0e81644f5197f780bea74f446ef5822a",
    HELD_REF / "FINAL_MANIFEST.sha256": "50e6f9aa6e7a5751c324393d7a158b63d535bd63999070fe46f85b5c7fb75118",
    FIRST / "batch_result.json": "6e982385c76686e743f740e4373b253a6a039c565e8cb6bd59a051cb189fc0dd",
    FIRST / "TERMINAL_MANIFEST.sha256": "8310384d0b26473fec57134cbb5f1b7c2c606e7b6a1af5dcefd5c5dfb3054260",
    FIRST_REF / "results_referee.json": "c2d13bbcf896321715c17353dd9970198eb3bce944e01b36dff24f9d3c5893fd",
    FIRST_REF / "FINAL_MANIFEST.sha256": "429d12d4135cc4cbe136481a6cd75fd5f254e4b646cfe3142b3dbe2f2f043b1d",
    SECOND / "batch_result.json": "67a36a426418ab7b65ea60aed934aed022c62e2b2ab5257b7512c9efd6a0298d",
    SECOND / "TERMINAL_MANIFEST.sha256": "b8ba01dcfb43cdf92244fe85703c5423a9186c6d44c73a73df2ea694f585ff98",
    SECOND_REF / "results_referee.json": "611d09abe73ef7032abf6280af3d9428e64d08db6aa731d1fde67ea004322e13",
    SECOND_REF / "FINAL_MANIFEST.sha256": "76cbf6f8ec9759cfb8f3ba7abc7d27b5e2aa13b24fce0201a6e17299fcd318e1",
}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def atomic(path: Path, value: object) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)

for path, expected in PINS.items():
    assert sha(path) == expected, (path, sha(path), expected)

spec = json.loads((HELD / "future_dependencies.json").read_text())
assert spec["status"] == "UNSATISFIED_BOTH_NULL_HASH_PAIRS" and spec["satisfied"] is False
assert spec["required_closed_union"] == list(range(76)) and spec["baseline_closed_group"] == 0
assert [d["name"] for d in spec["dependencies"]] == ["groups1_25", "groups26_75"]
assert all(d["satisfied"] is False and d["manifest_sha256"] is None and d["result_sha256"] is None for d in spec["dependencies"])

first_batch = json.loads((FIRST / "batch_result.json").read_text())
first_ref = json.loads((FIRST_REF / "results_referee.json").read_text())
assert first_batch["status"] == "PASS_ALL_25_UNIT"
assert first_batch["strict_order"] == list(range(1, 26))
assert [x["group_id"] for x in first_batch["completed"]] == list(range(1, 26))
assert all(x["status"] == "UNIT_IDEAL_EXACT_Q" for x in first_batch["completed"])
assert first_batch["stop"] is None and first_batch["skipped_after_stop"] == []
assert first_batch["parallel"] is first_batch["relaunch"] is False
assert first_ref["schema"] == "KRENN_X5_REP4_FIRST25_EXACT_Q_TERMINAL_REFEREE_V1"
assert first_ref["status"] == "PASS_EXACT_GROUPS_1_25_UNIT"
assert first_ref["unit_groups_closed"] == list(range(1, 26))
assert first_ref["closed_union"] == list(range(26)) and first_ref["sealed_group0"] is True

second_batch = json.loads((SECOND / "batch_result.json").read_text())
second_ref = json.loads((SECOND_REF / "results_referee.json").read_text())
assert second_batch["status"] == "PASS_ALL_50_UNIT"
assert second_batch["strict_order"] == list(range(26, 76))
assert [x["group_id"] for x in second_batch["completed"]] == list(range(26, 76))
assert all(x["status"] == "UNIT_IDEAL_EXACT_Q" for x in second_batch["completed"])
assert second_batch["stop"] is None and second_batch["skipped_after_stop"] == []
assert second_batch["parallel"] is second_batch["relaunch"] is False
assert second_ref["schema"] == "KRENN_X5_REP4_GROUPS26_75_EXACT_Q_TERMINAL_REFEREE_V1"
assert second_ref["status"] == "PASS_ALL_50_EXACT_Q_UNIT_IDEALS"
assert second_ref["groups_closed"] == list(range(26, 76))
assert second_ref["dependency_closed_union_before_batch"] == list(range(26))
assert second_ref["closed_union_after_batch"] == list(range(76))
assert second_ref["parallel"] is second_ref["relaunch"] is second_ref["skipped"] is False

ledger = json.loads((HELD / "source_ledger.json").read_text())
lanes = ledger["lanes"]
assert [x["group_id"] for x in lanes] == list(range(76, 126))
assert [x["ordinal"] for x in lanes] == list(range(1, 51))
for lane in lanes:
    source = HELD / lane["source_path"]
    assert sha(source) == lane["source_sha256"] and source.stat().st_size == lane["source_bytes"]
source_bytes = sum(x["source_bytes"] for x in lanes)
assert source_bytes == 90617222

normalized = {
    "schema": "KRENN_X5_REP4_GROUPS1_75_NORMALIZED_DEPENDENCIES_V2",
    "status": "PASS_NORMALIZED_EXACT_CLOSED_UNION_0_75",
    "baseline_closed_group": 0,
    "dependencies": [
        {
            "name": "groups1_25",
            "producer_batch_sha256": PINS[FIRST / "batch_result.json"],
            "producer_terminal_manifest_sha256": PINS[FIRST / "TERMINAL_MANIFEST.sha256"],
            "referee_result_sha256": PINS[FIRST_REF / "results_referee.json"],
            "referee_manifest_sha256": PINS[FIRST_REF / "FINAL_MANIFEST.sha256"],
            "actual_result_schema": first_ref["schema"],
            "actual_result_status": first_ref["status"],
            "groups_closed": list(range(1, 26)),
        },
        {
            "name": "groups26_75",
            "producer_batch_sha256": PINS[SECOND / "batch_result.json"],
            "producer_terminal_manifest_sha256": PINS[SECOND / "TERMINAL_MANIFEST.sha256"],
            "referee_result_sha256": PINS[SECOND_REF / "results_referee.json"],
            "referee_manifest_sha256": PINS[SECOND_REF / "FINAL_MANIFEST.sha256"],
            "actual_result_schema": second_ref["schema"],
            "actual_result_status": second_ref["status"],
            "groups_closed": list(range(26, 76)),
        },
    ],
    "closed_union": list(range(76)),
    "duplicates": [], "missing": [], "extra": [],
    "normalization_note": "Binds actual sealed referee statuses; stale expected status literals in the null dependency template are not used.",
}
atomic(HERE / "normalized_dependencies.json", normalized)
normalized_sha = sha(HERE / "normalized_dependencies.json")

acceptance = {
    "schema": "KRENN_X5_REP4_GROUPS76_125_EXACT_Q_INDEPENDENT_ACCEPTANCE_V1",
    "status": "PASS_APPROVE_CONDITIONAL_REP4_GROUPS76_125_ONLY",
    "held_manifest_sha256": PINS[HELD / "MANIFEST.sha256"],
    "source_ledger_sha256": PINS[HELD / "source_ledger.json"],
    "normalized_dependencies_sha256": normalized_sha,
    "runner_sha256": PINS[HELD / "run_groups76_125.py"],
    "required_closed_union": list(range(76)),
    "selected_group_ids": list(range(76, 126)),
    "maximum_lane_count": 50,
    "exact_Q_authorized": True,
    "parallel_authorized": False,
    "skip_reorder_relaunch_authorized": False,
}
atomic(HERE / "independent_referee_acceptance.json", acceptance)
schema = json.loads((HELD / "independent_referee_acceptance.schema.json").read_text())
assert schema["additionalProperties"] is False
assert set(schema["required"]) == set(schema["properties"]) == set(acceptance)
for key, rule in schema["properties"].items():
    if "const" in rule:
        assert acceptance[key] == rule["const"]
    elif "pattern" in rule:
        assert re.fullmatch(rule["pattern"], acceptance[key])

result = {
    "schema": "KRENN_X5_REP4_GROUPS76_125_SATISFIED_DEPENDENCY_BINDING_V2",
    "status": "PASS_HELD_LAUNCH_READY_ZERO_RUNS_NO_CLEARANCE",
    "normalized_dependencies": normalized,
    "held_acceptance": acceptance,
    "set_proof": {
        "baseline": [0], "sealed_groups1_25": list(range(1, 26)),
        "sealed_groups26_75": list(range(26, 76)), "pairwise_intersections": [],
        "closed_union": list(range(76)), "missing": [], "extra": [], "duplicates": [],
    },
    "preservation": {
        "source_count": 50, "source_bytes": source_bytes,
        "all_source_hashes_replayed": True,
        "source_ledger_sha256_unchanged": PINS[HELD / "source_ledger.json"],
        "runner_sha256_unchanged": PINS[HELD / "run_groups76_125.py"],
        "sources_rewritten": 0, "runner_rewritten": False,
    },
    "lineage": {
        "first25_producer_batch_sha256": PINS[FIRST / "batch_result.json"],
        "first25_producer_terminal_manifest_sha256": PINS[FIRST / "TERMINAL_MANIFEST.sha256"],
        "first25_referee_result_sha256": PINS[FIRST_REF / "results_referee.json"],
        "first25_referee_manifest_sha256": PINS[FIRST_REF / "FINAL_MANIFEST.sha256"],
        "groups26_75_producer_batch_sha256": PINS[SECOND / "batch_result.json"],
        "groups26_75_producer_terminal_manifest_sha256": PINS[SECOND / "TERMINAL_MANIFEST.sha256"],
        "groups26_75_referee_result_sha256": PINS[SECOND_REF / "results_referee.json"],
        "groups26_75_referee_manifest_sha256": PINS[SECOND_REF / "FINAL_MANIFEST.sha256"],
        "held_manifest_sha256": PINS[HELD / "MANIFEST.sha256"],
        "held_referee_result_sha256": PINS[HELD_REF / "results_referee.json"],
        "held_referee_approval_sha256": PINS[HELD_REF / "HELD_APPROVAL.json"],
        "held_referee_manifest_sha256": PINS[HELD_REF / "FINAL_MANIFEST.sha256"],
    },
    "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
    "scope": {
        "held_launch_ready_metadata": True, "install_into_held_performed": False,
        "launch_clearance_materialized": False, "solver_runs": 0,
        "new_arithmetic": False, "mathematical_coverage_added": False,
    },
}
atomic(HERE / "results_binding.json", result)
print(json.dumps({"status": result["status"], "union": 76, "sources": 50, "runs": 0, "clearance": False}, sort_keys=True))
