#!/usr/bin/env python3
"""Replay the sealed terminal referee without running arithmetic."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


result = json.loads((HERE / "results_referee.json").read_text())
assert result["status"] == "PASS_ALL_50_EXACT_Q_UNIT_IDEALS"
assert result["groups_closed"] == list(range(76, 126))
assert result["closed_union_after_batch"] == list(range(126))
assert result["remaining_groups"] == list(range(126, 162))
assert result["rep4_closed_count"] == 126 and result["rep4_total_groups"] == 162
assert result["rep4_representative_closed"] is result["seven_block_family_closed"] is result["conjecture_closed"] is False
assert result["resource_clear"] is True
if (HERE / "FINAL_MANIFEST.sha256").exists():
    for raw in (HERE / "FINAL_MANIFEST.sha256").read_text().splitlines():
        digest, name = raw.split(None, 1)
        path = HERE / name.strip()
        assert path.is_file() and sha(path) == digest
print(json.dumps({"status": "PASS_REPLAY", "audit_sha256": sha(HERE / "results_referee.json")}, sort_keys=True))
