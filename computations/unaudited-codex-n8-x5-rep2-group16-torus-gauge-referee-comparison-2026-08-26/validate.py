#!/usr/bin/env python3
"""Fail-closed small-artifact validator; never invokes Singular."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

H = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


result = json.loads((H / "results_referee_comparison.json").read_text())
ledger = json.loads((H / "combined_57_ledger.json").read_text())
assert result["status"] == "PASS_TORUS_19_EXACT_AND_SOUND_57_INTERSECTION_ZERO_SOLVES"
producer = result["producer_audit"]
assert producer["manifest_sha256"] == "1492e69373819fda0c50afc4f1366e2d6da90e857c26f73c03c0212ffd879282"
assert producer["result_sha256"] == "ee790ac911229e4aefb4d5e7a0c5dd4d7428ce006d40f1f62621fc3d34302360"
assert producer["character_matrix_determinant"] == 1
assert producer["source_histogram"] == {"70_variables": 1, "78_variables": 9, "87_variables": 9}
assert len(producer["source_rebuilds"]) == 19
assert all(x["generators"] == 6577 and x["removed_symbols_absent"] for x in producer["source_rebuilds"])
assert producer["hostile_count_replayed"] == 14 and producer["hostiles_all_pass"]
assert producer["consumed_timeout"] == "NATIVE_WALL_CAP_240"
assert producer["consumed_timeout_mathematical_coverage"] is False
assert producer["timeout_reuse_or_relaunch_authorized"] is False
guard = result["guard_pivot_audit"]
assert guard["manifest_sha256"] == "6a781149041e8808d58a53af77059253fe0a0d4295052bfe34756a0f994a0aee"
assert guard["chart_count"] == 3 and guard["torus_stable"]
comparison = result["exact_comparison"]
assert comparison["intersection_chart_count"] == len(ledger) == 57
assert Counter((x["variables"], x["generators"]) for x in ledger) == Counter({(84, 6574): 27, (75, 6574): 27, (67, 6574): 3})
assert all(x["unique_generators"] == 6574 and x["trivial_generators"] == 0 for x in ledger)
assert comparison["combined_ledger_sha256"] == sha(H / "combined_57_ledger.json")
assert comparison["single_chart_closes_group16"] is False
pilot = result["smallest_exact_pilot"]
pilot_path = H / pilot["path"]
assert pilot_path.is_file() and sha(pilot_path) == pilot["sha256"]
assert (pilot["variables"], pilot["generators"], pilot["guard_pivot_k"]) == (67, 6574, 0)
assert pilot["sufficient_for_its_localization"] and not pilot["sufficient_for_group16"]
text = pilot_path.read_text()
variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
assert len(variables) == 67
assert not (set(re.findall(r"\b(?:beta|abar|a57_00|a67_\d\d|a12_\d\d)\b", text)))
assert 'ideal G=slimgb(I);' in text and 'poly remainder=reduce(1,G);' in text
assert result["scope"] == {
    "design_referee_only": True,
    "singular_runs": 0,
    "ideal_runs": 0,
    "group16_closed": False,
    "rep2_closed": False,
    "pilot_launch_authorized": False,
}
if (H / "MANIFEST.sha256").exists():
    for line in (H / "MANIFEST.sha256").read_text().splitlines():
        digest, name = line.split(None, 1)
        path = (H / name.strip()).resolve()
        assert path.is_file() and sha(path) == digest, (path, digest, sha(path))
assert not list(H.rglob("*.tmp"))
print(json.dumps({"status": "PASS_REFEREE_COMPARISON_VALIDATED_ZERO_SOLVES", "strata": 19, "intersections": 57, "pilot": [67, 6574], "singular_runs": 0}, sort_keys=True))
