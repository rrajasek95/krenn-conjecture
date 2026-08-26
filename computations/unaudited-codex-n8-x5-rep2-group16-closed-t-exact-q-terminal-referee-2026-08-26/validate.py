#!/usr/bin/env python3
"""Replay the independent chart-local terminal seal."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


result = json.loads((HERE / "results_referee.json").read_text())
assert result["status"] == "PASS_UNIT_IDEAL_EXACT_Q_CLOSED_T_CHART_ONLY"
assert result["chart_exact_Q_coverage_promoted"] is True
assert result["single_chart_closes_group16"] is result["group16_closed"] is False
assert result["rep2_closed_union"] == list(range(16)) and result["rep2_closed_count"] == 16
assert result["rep2_closed"] is result["seven_block_family_closed"] is result["conjecture_closed"] is False
assert result["resource_clear"] is True
if (HERE / "FINAL_MANIFEST.sha256").exists():
    for raw in (HERE / "FINAL_MANIFEST.sha256").read_text().splitlines():
        digest, name = raw.split(None, 1)
        path = HERE / name.strip()
        assert path.is_file() and sha(path) == digest
print(json.dumps({"status": "PASS_REPLAY", "audit_sha256": sha(HERE / "results_referee.json")}, sort_keys=True))
