#!/usr/bin/env python3
"""Normalize future sealed baseline0..87 plus strict PASS groups88..137."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SPEC = HERE / "future_groups88_137_dependency.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_record(terminal: dict, spec: dict) -> dict:
    assert terminal["schema"] == spec["required_future_result_schema"]
    assert terminal["status"] == spec["required_future_result_status"]
    assert terminal["new_groups_closed"] == 50
    assert terminal["strict_order"] is True and terminal["parallel"] is False
    assert terminal["skipped"] is False and terminal["relaunch"] is False
    baseline = terminal["baseline_closed_union"]
    future = terminal["groups_closed"]
    assert baseline == spec["expected_baseline_closed_union"] == list(range(88))
    assert future == spec["expected_future_groups_closed"] == list(range(88, 138))
    assert len(baseline) == len(set(baseline)) == 88
    assert len(future) == len(set(future)) == 50
    assert not set(baseline) & set(future)
    union = sorted(baseline + future)
    assert union == spec["required_closed_union"] == list(range(138))
    assert terminal["closed_union"] == union
    return {
        "schema": "KRENN_X5_REP1_GROUPS138_161_NORMALIZED_FUTURE_DEPENDENCY_V1",
        "status": "PASS_DERIVED_EXACT_CLOSED_UNION_0_137",
        "baseline_closed_union": baseline,
        "future_groups_closed": future,
        "closed_union": union,
        "set_proof": {"baseline_count": 88, "future_count": 50, "intersection": [], "union_count": 138, "missing": [], "extra": [], "duplicates": []},
    }


def load_and_normalize(expected_manifest_sha: str, expected_result_sha: str) -> dict:
    spec = json.loads(SPEC.read_text())
    assert spec["status"] == "UNSATISFIED_NULL_HASHES_BLOCK_LAUNCH" and spec["satisfied"] is False
    assert spec["future_manifest_sha256"] is None and spec["future_result_sha256"] is None
    assert len(expected_manifest_sha) == len(expected_result_sha) == 64
    assert all(char in "0123456789abcdef" for char in expected_manifest_sha + expected_result_sha)
    manifest = ROOT / spec["future_manifest_path"]
    result = ROOT / spec["future_result_path"]
    assert manifest.is_file() and result.is_file(), "HELD: future groups88..137 terminal dependency absent"
    assert sha256(manifest) == expected_manifest_sha and sha256(result) == expected_result_sha
    assert f"{expected_result_sha}  {spec['required_manifest_member']}" in manifest.read_text().splitlines()
    normalized = normalize_record(json.loads(result.read_text()), spec)
    normalized["pins"] = {"future_terminal_manifest_sha256": expected_manifest_sha, "future_terminal_result_sha256": expected_result_sha}
    return normalized
