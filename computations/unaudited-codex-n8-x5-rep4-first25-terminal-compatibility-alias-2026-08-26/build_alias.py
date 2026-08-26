#!/usr/bin/env python3
"""Replay the sealed first-25 terminal proof and expose its unit groups uniformly."""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UPSTREAM = ROOT / "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26"
UPSTREAM_MANIFEST_SHA = "429d12d4135cc4cbe136481a6cd75fd5f254e4b646cfe3142b3dbe2f2f043b1d"
UPSTREAM_RESULT_SHA = "c2d13bbcf896321715c17353dd9970198eb3bce944e01b36dff24f9d3c5893fd"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic(path: Path, value: object) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


manifest = UPSTREAM / "FINAL_MANIFEST.sha256"
result_path = UPSTREAM / "results_referee.json"
assert sha(manifest) == UPSTREAM_MANIFEST_SHA
assert sha(result_path) == UPSTREAM_RESULT_SHA
listed = {}
for line in manifest.read_text().splitlines():
    digest, name = line.split(None, 1)
    path = (manifest.parent / name.strip()).resolve()
    assert re.fullmatch(r"[0-9a-f]{64}", digest)
    assert path.is_file() and sha(path) == digest
    listed[path] = digest
assert result_path.resolve() in listed
assert listed[result_path.resolve()] == UPSTREAM_RESULT_SHA

upstream = json.loads(result_path.read_text())
assert upstream["schema"] == "KRENN_X5_REP4_FIRST25_EXACT_Q_TERMINAL_REFEREE_V1"
assert upstream["status"] == "PASS_EXACT_GROUPS_1_25_UNIT"
assert upstream["unit_groups_closed"] == list(range(1, 26))
assert upstream["closed_union"] == list(range(26))
assert upstream["closed_count"] == 26
assert upstream["strict_sequential"] is True
assert upstream["resource_clear"] is True

alias = {
    "schema": "KRENN_X5_REP4_FIRST25_TERMINAL_COMPATIBILITY_ALIAS_V1",
    "status": "PASS_ALIAS_EXACT_GROUPS_1_25_UNIT",
    "groups_closed": list(range(1, 26)),
    "closed_union": list(range(26)),
    "upstream_manifest_path": str(manifest.relative_to(ROOT)),
    "upstream_manifest_sha256": UPSTREAM_MANIFEST_SHA,
    "upstream_result_path": str(result_path.relative_to(ROOT)),
    "upstream_result_sha256": UPSTREAM_RESULT_SHA,
    "field_mapping": {"groups_closed": "unit_groups_closed"},
    "mathematical_claim_changed": False,
    "solver_runs": 0,
}
atomic(HERE / "compatibility_result.json", alias)
print(json.dumps({"status": alias["status"], "groups": [1, 25], "solver_runs": 0}, sort_keys=True))
