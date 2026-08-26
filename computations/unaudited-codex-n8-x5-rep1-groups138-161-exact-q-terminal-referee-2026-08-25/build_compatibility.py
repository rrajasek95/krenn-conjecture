#!/usr/bin/env python3
"""Exact interface/path alias for the audited rep1 groups 138..161 terminal."""
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROD = ROOT / "computations/unaudited-codex-n8-x5-rep1-groups138-161-exact-q-conditional-held-2026-08-25"
AUDIT = ROOT / "computations/unaudited-codex-n8-x5-rep1-groups138-161-exact-q-terminal-referee-2026-08-26"
PINS = {
    PROD / "batch_result.json": "68bcfa93ef90550bbc25510ec7a9a6e9256e1387b5f4bd23bd65f27d9708a2f6",
    PROD / "TERMINAL_MANIFEST.sha256": "e67f90ca128a817ac97b3fd0a7cad195f441db0575fe136ad9c3610c10a7a4a1",
    AUDIT / "results_referee.json": "27b684969194cebacdcca2b53b874a0e5d176e0bea9344ec64230b98b977ede2",
    AUDIT / "FINAL_MANIFEST.sha256": "6932c454d5c37856a881ee0ed0a866e47cd1ab4dbd92c881cb06548986377334",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(manifest):
    for line in manifest.read_text().splitlines():
        digest, name = line.split(None, 1)
        path = (manifest.parent / name.strip()).resolve()
        assert path.is_file() and sha(path) == digest, (path, digest)


def atomic(path, value):
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temp, path)


for path, expected in PINS.items():
    assert sha(path) == expected, (path, sha(path), expected)
replay(PROD / "TERMINAL_MANIFEST.sha256")
replay(AUDIT / "FINAL_MANIFEST.sha256")
audit = json.loads((AUDIT / "results_referee.json").read_text())
batch = json.loads((PROD / "batch_result.json").read_text())
assert audit["schema"] == "KRENN_X5_REP1_GROUPS138_161_EXACT_Q_TERMINAL_REFEREE_V1"
assert audit["status"] == "PASS_ALL_24_EXACT_Q_UNIT_IDEALS"
assert audit["dependency_closed_union_before_batch"] == list(range(138))
assert audit["groups_closed"] == list(range(138, 162))
assert audit["closed_union_after_batch"] == list(range(162))
assert batch["status"] == "PASS_ALL_24_UNIT" and batch["strict_order"] == list(range(138, 162))
assert [x["group_id"] for x in batch["completed"]] == list(range(138, 162))
assert batch["stop"] is None and batch["skipped_after_stop"] == []
assert not batch["parallel"] and not batch["relaunch"]
result = {
    "schema": "KRENN_X5_REP1_GROUPS138_161_EXACT_Q_TERMINAL_REFEREE_V1",
    "status": "PASS_ALL_24_EXACT_Q_UNIT_IDEALS",
    "new_groups_closed": 24,
    "strict_order": True,
    "parallel": False,
    "skipped": False,
    "relaunch": False,
    "baseline_closed_union": list(range(138)),
    "groups_closed": list(range(138, 162)),
    "closed_union": list(range(162)),
    "compatibility_only": True,
    "field_map": {
        "baseline_closed_union": "audited dependency_closed_union_before_batch",
        "closed_union": "audited closed_union_after_batch",
    },
    "underlying_producer_batch_sha256": PINS[PROD / "batch_result.json"],
    "underlying_producer_terminal_manifest_sha256": PINS[PROD / "TERMINAL_MANIFEST.sha256"],
    "underlying_audit_result_sha256": PINS[AUDIT / "results_referee.json"],
    "underlying_audit_manifest_sha256": PINS[AUDIT / "FINAL_MANIFEST.sha256"],
    "solver_runs_added": 0,
    "mathematical_coverage_added": False,
}
atomic(HERE / "results_referee.json", result)
print(json.dumps({"status": "PASS_EXACT_INTERFACE_COMPATIBILITY_ALIAS", "result_sha256": sha(HERE / "results_referee.json")}, sort_keys=True))
