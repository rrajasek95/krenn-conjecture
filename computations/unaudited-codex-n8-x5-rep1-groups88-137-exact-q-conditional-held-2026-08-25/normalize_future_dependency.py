#!/usr/bin/env python3
"""Fail-closed adapter for proven 0..37 plus future strict closure 38..87."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SPEC = HERE / "future_groups38_87_dependency.json"
BASELINE = ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-2026-08-25"
BASELINE_MANIFEST_SHA = "7b66f582d1edf79e1e75c4ca328808f3f77548f840f5c42cc082dcd0f53764da"
BASELINE_DEPENDENCY_SHA = "29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_records(baseline: dict, terminal: dict, spec: dict) -> dict:
    baseline_ids = baseline["closed_union"]
    assert baseline["schema"] == "KRENN_X5_REP1_NEXT50_NORMALIZED_NEXT25_DEPENDENCY_V2"
    assert baseline["status"] == "PASS_NORMALIZED_BASELINE_PLUS_NEXT25_TO_CLOSED_UNION_0_37"
    assert baseline_ids == spec["proven_baseline_closed_union"] == list(range(38))
    assert len(baseline_ids) == len(set(baseline_ids)) == 38
    assert terminal["schema"] == spec["required_future_result_schema"]
    assert terminal["status"] == spec["required_future_result_status"]
    assert terminal["new_groups_closed"] == 50
    assert terminal["strict_order"] is True and terminal["parallel"] is False
    assert terminal["skipped"] is False and terminal["relaunch"] is False
    future_ids = terminal["groups_closed"]
    assert future_ids == spec["expected_future_groups_closed"] == list(range(38, 88))
    assert len(future_ids) == len(set(future_ids)) == 50
    assert not set(baseline_ids) & set(future_ids)
    union = sorted(baseline_ids + future_ids)
    assert union == spec["required_closed_union"] == list(range(88))
    return {
        "schema": "KRENN_X5_REP1_GROUPS88_137_NORMALIZED_FUTURE_DEPENDENCY_V1",
        "status": "PASS_DERIVED_EXACT_CLOSED_UNION_0_87",
        "baseline_closed_union": baseline_ids,
        "future_groups_closed": future_ids,
        "closed_union": union,
        "set_proof": {"baseline_count": 38, "future_count": 50, "intersection": [], "union_count": 88, "missing": [], "extra": [], "duplicates": []},
    }


def load_and_normalize(expected_future_manifest_sha: str, expected_future_result_sha: str) -> dict:
    spec = json.loads(SPEC.read_text())
    assert spec["status"] == "UNSATISFIED_NULL_HASHES_BLOCK_LAUNCH" and spec["satisfied"] is False
    assert spec["future_manifest_sha256"] is None and spec["future_result_sha256"] is None
    assert len(expected_future_manifest_sha) == len(expected_future_result_sha) == 64
    assert all(char in "0123456789abcdef" for char in expected_future_manifest_sha + expected_future_result_sha)
    assert sha256(BASELINE / "MANIFEST.sha256") == BASELINE_MANIFEST_SHA
    assert sha256(BASELINE / "normalized_next25_dependency.json") == BASELINE_DEPENDENCY_SHA
    manifest = ROOT / spec["future_manifest_path"]
    result = ROOT / spec["future_result_path"]
    assert manifest.is_file() and result.is_file(), "HELD: future groups38..87 terminal dependency absent"
    assert sha256(manifest) == expected_future_manifest_sha
    assert sha256(result) == expected_future_result_sha
    assert f"{expected_future_result_sha}  {spec['required_manifest_member']}" in manifest.read_text().splitlines()
    normalized = normalize_records(
        json.loads((BASELINE / "normalized_next25_dependency.json").read_text()),
        json.loads(result.read_text()),
        spec,
    )
    normalized["pins"] = {
        "baseline_manifest_sha256": BASELINE_MANIFEST_SHA,
        "baseline_dependency_sha256": BASELINE_DEPENDENCY_SHA,
        "future_terminal_manifest_sha256": expected_future_manifest_sha,
        "future_terminal_result_sha256": expected_future_result_sha,
    }
    return normalized
