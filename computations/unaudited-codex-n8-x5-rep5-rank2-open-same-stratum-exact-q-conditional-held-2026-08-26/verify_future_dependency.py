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
HELD = "687dd47c10265ad82421cd06e015db4a88982710dbdba370ac0fee82f5f5596b"
REFEREE_V1 = "1c33eea1ba807ef5502a1f3047844faaec05afe355858a3b041a0dd1584479f7"
REFEREE_V2 = "78ec2054761b8e6a6eeb3dc338f82338d02b48d25436a46b5cbcc37755d18a49"
MODULAR_SOURCE = "fd182135d5da6eda87e284a4f38f147fbf13bef14016c1ee300bb9bde6713c5a"


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
    for token in ("INPUT_VARIABLES=84", "INPUT_GENERATORS=6562", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"):
        assert token in stdout, f"missing modular transcript token {token}"


def validate_shape(binding: dict) -> None:
    assert set(binding) == {
        "schema", "status", "held_manifest_sha256", "held_referee_v1_manifest_sha256",
        "held_referee_v2_manifest_sha256", "producer_manifest_path", "producer_manifest_sha256",
        "producer_result_path", "producer_result_sha256", "referee_manifest_path",
        "referee_manifest_sha256", "referee_result_path", "referee_result_sha256",
        "modular_source_sha256", "field", "pivot_k", "t_open", "variables", "generators",
    }
    assert binding["schema"] == "KRENN_X5_REP5_OPEN84_FUTURE_MODULAR_UNIT_DEPENDENCY_V1"
    assert binding["status"] == "INDEPENDENTLY_SEALED_SAME_STRATUM_MODULAR_UNIT"
    assert binding["held_manifest_sha256"] == HELD
    assert binding["held_referee_v1_manifest_sha256"] == REFEREE_V1
    assert binding["held_referee_v2_manifest_sha256"] == REFEREE_V2
    assert binding["modular_source_sha256"] == MODULAR_SOURCE
    assert (binding["field"], binding["pivot_k"], binding["t_open"], binding["variables"], binding["generators"]) == ("F_32003", 2, 1, 84, 6562)
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
    assert producer["schema"] == "KRENN_X5_REP5_RANK2_OPEN_SMALLEST_MODULAR_RESULT_V1"
    assert producer["status"] == "UNIT_IDEAL_MODULAR_DIAGNOSTIC"
    assert (producer["field"], producer["pivot_k"], producer["t_open"], producer["variables"], producer["generators"]) == ("F_32003", 2, 1, 84, 6562)
    assert producer["source_sha256"] == MODULAR_SOURCE
    assert producer["termination"] is None and producer["returncode"] == 0
    assert producer["exact_Q_launched"] is producer["other_stratum_launched"] is producer["prior_consumed_k0_reused"] is producer["automatic_relaunch"] is False
    require_tokens(producer["stdout"])
    referee = json.loads(referee_result_path.read_text())
    assert referee["schema"] == "KRENN_X5_REP5_OPEN84_MODULAR_UNIT_TERMINAL_REFEREE_V1"
    assert referee["status"] == "PASS_INDEPENDENT_SAME_STRATUM_MODULAR_UNIT"
    assert referee["producer_manifest_sha256"] == binding["producer_manifest_sha256"]
    assert referee["producer_result_sha256"] == binding["producer_result_sha256"]
    assert referee["held_manifest_sha256"] == HELD
    assert referee["held_referee_v1_manifest_sha256"] == REFEREE_V1
    assert referee["held_referee_v2_manifest_sha256"] == REFEREE_V2
    assert referee["modular_source_sha256"] == MODULAR_SOURCE
    assert (referee["field"], referee["pivot_k"], referee["t_open"], referee["variables"], referee["generators"]) == ("F_32003", 2, 1, 84, 6562)
    assert referee["unit_transcript_replayed"] is True and referee["same_stratum_verified"] is True
    binding["binding_sha256"] = sha256(path)
    return binding


if __name__ == "__main__":
    verified = verify_dependency(HERE / "future_modular_unit_dependency.json")
    print(json.dumps({"status": "PASS", "binding_sha256": verified["binding_sha256"]}, sort_keys=True))
