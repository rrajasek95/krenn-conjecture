#!/usr/bin/env python3
"""Normalize independently sealed baseline + next25 closure into closed_union 0..37."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASELINE = ROOT / "computations/unaudited-codex-n8-x5-rep1-next25-exact-q-held-referee-2026-08-25"
NEXT25 = ROOT / "computations/unaudited-codex-n8-x5-rep1-next25-exact-q-terminal-referee-2026-08-25"
BINDING = ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-next25-satisfied-binding-audit-2026-08-25"
PINS = {
    BASELINE / "FINAL_MANIFEST.sha256": "950e50ea1b1af733b5f20fad076357d29ee76a7b85009c7b93fcad76b1406c75",
    BASELINE / "results_referee.json": "a4a959cc1eb2392e64fc0c1d8e540deace8141ae43d50fbd7c30a14d6ef6c189",
    NEXT25 / "FINAL_MANIFEST.sha256": "b5de471b2cbd4f5197492c37f7f885f77059a9eced3e66830998c8edd5d62cde",
    NEXT25 / "results_referee.json": "a2599e9cee2739fb372e1d45db9625dc999510eb58407609cb581e73acbce450",
    BINDING / "FINAL_MANIFEST.sha256": "18e93f3a635496987e58320858bff91e93a965a72504bba7762a9e5675a6b341",
    BINDING / "results_binding.json": "e5f441d67b9e372e5946fd0de01b2bab0cc0d13b0bab729f8fceba3c0f3c0880",
}
EXPECTED_BASELINE = list(range(11)) + [13, 15]
EXPECTED_NEW = [11, 12, 14] + list(range(16, 38))
EXPECTED_UNION = list(range(38))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(baseline: dict, terminal: dict, binding: dict) -> dict:
    assert baseline["schema"] == "KRENN_X5_REP1_NEXT25_EXACT_Q_HELD_REFEREE_V1"
    assert baseline["status"] == "PASS_APPROVED_HELD_STRICT_REP1_NEXT25_ZERO_RUNS"
    baseline_ids = baseline["closed_baseline_group_ids"]
    assert baseline_ids == EXPECTED_BASELINE
    assert len(baseline_ids) == len(set(baseline_ids))
    assert terminal["schema"] == "KRENN_X5_REP1_NEXT25_EXACT_Q_TERMINAL_REFEREE_V1"
    assert terminal["status"] == "PASS_ALL_25_EXACT_Q_UNIT_IDEALS"
    assert terminal["new_groups_closed"] == 25
    assert terminal["strict_order"] is True and terminal["parallel"] is False
    assert terminal["skipped"] is False and terminal["relaunch"] is False
    new_ids = terminal["groups_closed"]
    assert new_ids == EXPECTED_NEW
    assert len(new_ids) == len(set(new_ids)) == 25
    assert not set(baseline_ids) & set(new_ids)
    closed_union = sorted(baseline_ids + new_ids)
    assert closed_union == EXPECTED_UNION and len(closed_union) == 38
    assert binding["schema"] == "KRENN_X5_REP1_NEXT50_NEXT25_SATISFIED_BINDING_AUDIT_V1"
    assert binding["status"] == "PASS_SATISFIED_NEXT25_PROOF_BINDING_HELD_ACCEPTANCE_NOT_LAUNCH_READY"
    assert binding["dependency_proof_satisfied"] is True
    assert binding["dependency_result_manifest_membership"] is True
    assert binding["runner_interface_satisfied"] is False
    assert binding["closed_union"] == closed_union
    assert binding["next25_terminal_referee_manifest_sha256"] == PINS[NEXT25 / "FINAL_MANIFEST.sha256"]
    assert binding["next25_terminal_referee_result_sha256"] == PINS[NEXT25 / "results_referee.json"]
    return {
        "schema": "KRENN_X5_REP1_NEXT50_NORMALIZED_NEXT25_DEPENDENCY_V2",
        "status": "PASS_NORMALIZED_BASELINE_PLUS_NEXT25_TO_CLOSED_UNION_0_37",
        "baseline_group_ids": baseline_ids,
        "next25_groups_closed": new_ids,
        "closed_union": closed_union,
        "set_proof": {"baseline_count": 13, "next25_count": 25, "intersection": [], "union_count": 38, "missing_from_0_37": [], "extra_outside_0_37": [], "duplicates": []},
        "pins": {
            "baseline_manifest_sha256": PINS[BASELINE / "FINAL_MANIFEST.sha256"],
            "baseline_result_sha256": PINS[BASELINE / "results_referee.json"],
            "next25_terminal_manifest_sha256": PINS[NEXT25 / "FINAL_MANIFEST.sha256"],
            "next25_terminal_result_sha256": PINS[NEXT25 / "results_referee.json"],
            "binding_audit_manifest_sha256": PINS[BINDING / "FINAL_MANIFEST.sha256"],
            "binding_audit_result_sha256": PINS[BINDING / "results_binding.json"],
        },
        "adapter_scope": "schema normalization only; no arithmetic and no launch authority",
    }


def load_and_normalize() -> dict:
    for path, expected in PINS.items():
        assert sha256(path) == expected, (path, sha256(path), expected)
    assert f"{PINS[BASELINE / 'results_referee.json']}  results_referee.json" in (BASELINE / "FINAL_MANIFEST.sha256").read_text().splitlines()
    assert f"{PINS[NEXT25 / 'results_referee.json']}  results_referee.json" in (NEXT25 / "FINAL_MANIFEST.sha256").read_text().splitlines()
    assert f"{PINS[BINDING / 'results_binding.json']}  results_binding.json" in (BINDING / "FINAL_MANIFEST.sha256").read_text().splitlines()
    return normalize(
        json.loads((BASELINE / "results_referee.json").read_text()),
        json.loads((NEXT25 / "results_referee.json").read_text()),
        json.loads((BINDING / "results_binding.json").read_text()),
    )


if __name__ == "__main__":
    result = load_and_normalize()
    temporary = HERE / "normalized_next25_dependency.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "normalized_next25_dependency.json")
    print(json.dumps({"status": result["status"], "closed_union": result["closed_union"]}, sort_keys=True))
