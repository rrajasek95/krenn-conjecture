#!/usr/bin/env python3
"""Fail-closed verifier for the sealed rep2 closed-t modular UNIT prerequisite."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HEX64 = re.compile(r"[0-9a-f]{64}")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pinned(relative: str) -> Path:
    assert isinstance(relative, str) and relative and not relative.startswith("/")
    candidate = ROOT / relative
    resolved = candidate.resolve(strict=True)
    assert resolved == candidate.absolute(), "noncanonical or symlink dependency path"
    assert ROOT in resolved.parents and resolved.is_file()
    return resolved


def replay(manifest: Path, required: Path) -> None:
    seen: set[Path] = set()
    for raw in manifest.read_text().splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", raw)
        assert match, raw
        digest, relative = match.groups()
        assert not relative.startswith("/")
        target = (manifest.parent / relative).resolve(strict=True)
        assert ROOT in target.parents and target not in seen
        seen.add(target)
        assert target.is_file() and sha(target) == digest
    assert required.resolve() in seen


def validate_shape(value: dict) -> None:
    assert set(value) == {
        "schema", "status", "held_manifest_path", "held_manifest_sha256",
        "held_referee_manifest_path", "held_referee_manifest_sha256",
        "producer_terminal_manifest_path", "producer_terminal_manifest_sha256",
        "producer_result_path", "producer_result_sha256",
        "referee_terminal_manifest_path", "referee_terminal_manifest_sha256",
        "referee_result_path", "referee_result_sha256", "modular_source_sha256",
        "field", "chart", "variables", "generators",
    }
    assert value["schema"] == "KRENN_X5_REP2_GROUP16_CLOSED_T_MODULAR_UNIT_DEPENDENCY_V1"
    assert value["status"] == "INDEPENDENTLY_SEALED_SAME_CHART_MODULAR_UNIT"
    assert value["field"] == "F_32003"
    assert value["chart"] == "V(A67,A12,t0,t1,t2) intersect D(b0)"
    assert (value["variables"], value["generators"]) == (62, 6568)
    pins = {
        "held_manifest_sha256": "eefb9e1045f63f945fa62cc83119f171128575eb29d5a1d41b1aabf2e6a374c2",
        "held_referee_manifest_sha256": "d8f36615a10cc254a91fa6c555ebc764736747e1b69d33d66cc96ff222f32ef0",
        "producer_terminal_manifest_sha256": "31d3c4290de2214fed4846909e0a1309a3adf103ea9415bea35a391e0a87999b",
        "producer_result_sha256": "7c7d9c890863548ae7efc079284cc418a9fab7dbc427ac234e16bd8e55c4f06e",
        "referee_terminal_manifest_sha256": "2cfa80ecaa36de10f82a9dd1305683e7e50b3aa12c99a75cb75a20b536f34334",
        "referee_result_sha256": "07fabc04915cd909127774ae132eba470fa9917b9cf408ef220599b53a8448ff",
        "modular_source_sha256": "d7e57a3d43fb1280381660be2fea9c966eb086bd2aced3189b0f599030f5822b",
    }
    for key, expected in pins.items():
        assert isinstance(value[key], str) and HEX64.fullmatch(value[key]) and value[key] == expected


def verify_dependency(path: Path) -> dict:
    assert path.resolve().parent == HERE and path.name == "modular_unit_dependency.json"
    value = json.loads(path.read_text())
    validate_shape(value)
    held_manifest = pinned(value["held_manifest_path"])
    held_referee_manifest = pinned(value["held_referee_manifest_path"])
    producer_manifest = pinned(value["producer_terminal_manifest_path"])
    producer_result_path = pinned(value["producer_result_path"])
    referee_manifest = pinned(value["referee_terminal_manifest_path"])
    referee_result_path = pinned(value["referee_result_path"])
    assert sha(held_manifest) == value["held_manifest_sha256"]
    assert sha(held_referee_manifest) == value["held_referee_manifest_sha256"]
    assert sha(producer_manifest) == value["producer_terminal_manifest_sha256"]
    assert sha(producer_result_path) == value["producer_result_sha256"]
    assert sha(referee_manifest) == value["referee_terminal_manifest_sha256"]
    assert sha(referee_result_path) == value["referee_result_sha256"]
    replay(producer_manifest, producer_result_path)
    replay(referee_manifest, referee_result_path)
    producer = json.loads(producer_result_path.read_text())
    assert producer["schema"] == "KRENN_X5_REP2_GROUP16_CLOSED_T_MODULAR_RESULT_V1"
    assert producer["status"] == "UNIT_IDEAL_MODULAR_DIAGNOSTIC"
    assert (producer["field"], producer["chart"], producer["variables"], producer["generators"]) == (
        value["field"], value["chart"], 62, 6568,
    )
    assert producer["source_sha256"] == value["modular_source_sha256"]
    assert producer["termination"] is None and producer["returncode"] == 0
    assert producer["exact_Q_launched"] is producer["other_chart_launched"] is producer["automatic_relaunch"] is False
    lines = set(producer["stdout"].splitlines())
    assert {"INPUT_VARIABLES=62", "INPUT_GENERATORS=6568", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"} <= lines
    referee = json.loads(referee_result_path.read_text())
    assert referee["schema"] == "KRENN_X5_REP2_GROUP16_CLOSED_T_MODULAR_TERMINAL_REFEREE_V1"
    assert referee["status"] == "PASS_UNIT_IDEAL_MODULAR_DIAGNOSTIC_CHART_ONLY"
    assert referee["terminal_manifest_sha256"] == value["producer_terminal_manifest_sha256"]
    assert referee["result_sha256"] == value["producer_result_sha256"]
    assert referee["held_referee_manifest_sha256"] == value["held_referee_manifest_sha256"]
    assert referee["modular_chart_diagnostic_pass"] is True and referee["mathematical_coverage_promoted"] is False
    assert (referee["field"], referee["chart"], referee["variables"], referee["generators"]) == (
        value["field"], value["chart"], 62, 6568,
    )
    value["binding_sha256"] = sha(path)
    return value


if __name__ == "__main__":
    result = verify_dependency(HERE / "modular_unit_dependency.json")
    print(json.dumps({"status": "PASS", "binding_sha256": result["binding_sha256"]}, sort_keys=True))
