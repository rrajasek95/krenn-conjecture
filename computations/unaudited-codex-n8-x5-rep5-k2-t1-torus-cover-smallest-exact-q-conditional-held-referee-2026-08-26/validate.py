#!/usr/bin/env python3
"""Replay the sealed held-only referee without invoking Singular."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest = HERE / "FINAL_MANIFEST.sha256"
seen = set()
for raw in manifest.read_text().splitlines():
    match = re.fullmatch(r"([0-9a-f]{64})  (.+)", raw)
    assert match
    digest, relative = match.groups()
    target = (HERE / relative).resolve(strict=True)
    assert ROOT in target.parents and target not in seen and sha(target) == digest
    seen.add(target)
result = json.loads((HERE / "results_referee.json").read_text())
approval = json.loads((HERE / "HELD_APPROVAL.json").read_text())
assert result["status"] == "PASS_HELD_ONLY_PENDING_INDEPENDENT_MODULAR_UNIT"
assert result["hostiles_passed"] == 16 and result["scope"]["solver_runs"] == 0
assert result["scope"]["exact_Q_authorized"] is result["scope"]["launch_authorized"] is False
assert approval["status"] == "HELD_APPROVAL_ONLY_NO_LAUNCH"
assert approval["producer_manifest_sha256"] == result["producer_manifest_sha256"]
print(json.dumps({"status": "PASS_SEALED_HELD_ONLY", "manifest_entries": len(seen), "solver_runs": 0}, sort_keys=True))
