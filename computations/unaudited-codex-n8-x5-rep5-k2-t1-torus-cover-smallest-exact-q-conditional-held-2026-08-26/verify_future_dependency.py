#!/usr/bin/env python3
"""Fail-closed verifier for the future independently sealed modular UNIT prerequisite."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HEX64 = re.compile(r"[0-9a-f]{64}")
HELD = "21df0017be41a8ec9e4035b0902649cf9c8ed97d43c65c88a93d1db7f8bf6d72"
REFEREE = "16a32d07221def48a9e8388ca1e8b716cd71dfb44c2dc0cbea0bb22ab91203ab"
MODULAR_SOURCE = "c36bd3b77052487b43751b03f48849c76091ec121a04abc3305cb56ec6494a8b"
ASSIGNMENT = {"yn1": 1, "yn2": 1, "t0": 1, "t2": 0}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pinned_path(relative: str) -> Path:
    assert isinstance(relative, str) and relative and not relative.startswith("/")
    candidate = ROOT / relative
    resolved = candidate.resolve(strict=True)
    assert resolved == candidate.absolute(), "symlink or noncanonical dependency path"
    assert ROOT == resolved or ROOT in resolved.parents, "dependency escapes repository"
    assert resolved.is_file()
    return resolved


def replay_manifest(manifest: Path, required: Path) -> None:
    seen: set[Path] = set()
    for raw in manifest.read_text().splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", raw)
        assert match, f"malformed manifest line: {raw!r}"
        expected, relative = match.groups()
        assert not relative.startswith("/")
        target = (manifest.parent / relative).resolve(strict=True)
        assert ROOT == target or ROOT in target.parents, "manifest target escapes repository"
        assert target not in seen, "duplicate normalized manifest target"
        seen.add(target)
        assert target.is_file() and sha256(target) == expected, f"manifest replay mismatch: {relative}"
    assert required.resolve() in seen, "required result absent from manifest"


def require_tokens(stdout: object) -> None:
    assert isinstance(stdout, str)
    for token in ("INPUT_VARIABLES=73", "INPUT_GENERATORS=6561", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"):
        assert token in stdout, f"missing modular transcript token {token}"


def validate_shape(binding: dict) -> None:
    assert set(binding) == {
        "schema", "status", "held_manifest_sha256", "held_referee_manifest_sha256",
        "producer_manifest_path", "producer_manifest_sha256",
        "producer_result_path", "producer_result_sha256", "referee_manifest_path",
        "referee_manifest_sha256", "referee_result_path", "referee_result_sha256",
        "modular_source_sha256", "field", "assignment", "variables", "generators",
    }
    assert binding["schema"] == "KRENN_X5_REP5_TORUS_SMALLEST_FUTURE_MODULAR_UNIT_DEPENDENCY_V1"
    assert binding["status"] == "INDEPENDENTLY_SEALED_SAME_CHART_MODULAR_UNIT"
    assert binding["held_manifest_sha256"] == HELD
    assert binding["held_referee_manifest_sha256"] == REFEREE
    assert binding["modular_source_sha256"] == MODULAR_SOURCE
    assert (binding["field"], binding["assignment"], binding["variables"], binding["generators"]) == ("F_32003", ASSIGNMENT, 73, 6561)
    for key in ("producer_manifest_sha256", "producer_result_sha256", "referee_manifest_sha256", "referee_result_sha256"):
        assert isinstance(binding[key], str) and HEX64.fullmatch(binding[key])


def verify_dependency(path: Path) -> dict:
    assert path.resolve().parent == HERE and path.name == "future_modular_unit_dependency.json"
    binding = json.loads(path.read_text())
    validate_shape(binding)
    producer_manifest = pinned_path(binding["producer_manifest_path"])
    producer_result_path = pinned_path(binding["producer_result_path"])
    referee_manifest = pinned_path(binding["referee_manifest_path"])
    referee_result_path = pinned_path(binding["referee_result_path"])
    assert sha256(producer_manifest) == binding["producer_manifest_sha256"]
    assert sha256(producer_result_path) == binding["producer_result_sha256"]
    assert sha256(referee_manifest) == binding["referee_manifest_sha256"]
    assert sha256(referee_result_path) == binding["referee_result_sha256"]
    replay_manifest(producer_manifest, producer_result_path)
    replay_manifest(referee_manifest, referee_result_path)
    producer = json.loads(producer_result_path.read_text())
    assert producer["schema"] == "KRENN_X5_REP5_K2_T1_TORUS_SMALLEST_MODULAR_RESULT_V1"
    assert producer["status"] == "UNIT_IDEAL_MODULAR_DIAGNOSTIC"
    assert (producer["field"], producer["assignment"], producer["variables"], producer["generators"]) == ("F_32003", ASSIGNMENT, 73, 6561)
    assert producer["source_sha256"] == MODULAR_SOURCE
    assert producer["termination"] is None and producer["returncode"] == 0
    assert producer["exact_Q_launched"] is producer["other_chart_launched"] is producer["prior_timeout_reused"] is producer["automatic_relaunch"] is False
    require_tokens(producer["stdout"])
    referee = json.loads(referee_result_path.read_text())
    assert referee["schema"] == "KRENN_X5_REP5_K2_T1_TORUS_SMALLEST_MODULAR_UNIT_TERMINAL_REFEREE_V1"
    assert referee["status"] == "PASS_INDEPENDENT_SAME_CHART_MODULAR_UNIT"
    assert referee["producer_manifest_sha256"] == binding["producer_manifest_sha256"]
    assert referee["producer_result_sha256"] == binding["producer_result_sha256"]
    assert referee["held_manifest_sha256"] == HELD
    assert referee["held_referee_manifest_sha256"] == REFEREE
    assert referee["modular_source_sha256"] == MODULAR_SOURCE
    assert (referee["field"], referee["assignment"], referee["variables"], referee["generators"]) == ("F_32003", ASSIGNMENT, 73, 6561)
    assert referee["unit_transcript_replayed"] is True and referee["same_chart_verified"] is True
    binding["binding_sha256"] = sha256(path)
    return binding


if __name__ == "__main__":
    verified = verify_dependency(HERE / "future_modular_unit_dependency.json")
    print(json.dumps({"status": "PASS", "binding_sha256": verified["binding_sha256"]}, sort_keys=True))
