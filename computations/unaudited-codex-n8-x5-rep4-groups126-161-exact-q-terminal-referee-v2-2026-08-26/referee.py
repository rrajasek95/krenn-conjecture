#!/usr/bin/env python3
"""Independent replay of the compatibility-repaired final rep4 batch."""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUN = ROOT / "computations/unaudited-codex-n8-x5-rep4-groups126-161-exact-q-held-v2-2026-08-26"
PINS = {
    RUN / "MANIFEST.sha256": "5da0b0f163a7f96cd00bd4dd3478bc06442e9a12036ddc86c27fb441815c3c3d",
    RUN / "TERMINAL_MANIFEST.sha256": "474c9de0e6657e668d1a84cd54c24de973c13446d0e9dbf2571ffd1aa12e3bf7",
    RUN / "batch_result.json": "e5fab9ff9cdfd161cc8b7eda07e4069824028a5ecd81c73d3e724fc46245bdb4",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay_manifest(path):
    listed = {}
    for line in path.read_text().splitlines():
        digest, name = line.split(None, 1)
        target = (path.parent / name.strip()).resolve()
        assert re.fullmatch(r"[0-9a-f]{64}", digest)
        assert target.is_file() and sha(target) == digest, (target, digest, sha(target))
        listed[target] = digest
    return listed


def atomic(path, value):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


for path, digest in PINS.items():
    assert path.is_file() and sha(path) == digest
held_entries = replay_manifest(RUN / "MANIFEST.sha256")
terminal_entries = replay_manifest(RUN / "TERMINAL_MANIFEST.sha256")
batch_path = RUN / "batch_result.json"
assert batch_path.resolve() in terminal_entries and terminal_entries[batch_path.resolve()] == PINS[batch_path]
batch = json.loads(batch_path.read_text())
assert batch["schema"] == "KRENN_X5_REP4_GROUPS126_161_BATCH_RESULT_V1"
assert batch["status"] == "PASS_ALL_36_UNIT"
assert batch["required_closed_union"] == list(range(126))
assert batch["strict_order"] == list(range(126, 162))
assert batch["stop"] is None and batch["skipped_after_stop"] == []
assert batch["parallel"] is batch["relaunch"] is False
assert [row["group_id"] for row in batch["completed"]] == list(range(126, 162))
assert all(row["status"] == "UNIT_IDEAL_EXACT_Q" for row in batch["completed"])

ledger = json.loads((RUN / "source_ledger.json").read_text())
lanes = {row["group_id"]: row for row in ledger["lanes"]}
walls = []
rss = []
for group_id in range(126, 162):
    result_path = RUN / "results" / f"group{group_id:03d}.json"
    assert result_path.resolve() in terminal_entries
    result = json.loads(result_path.read_text())
    lane = lanes[group_id]
    assert result["schema"] == "KRENN_X5_REP4_GROUPS126_161_LANE_RESULT_V1"
    assert result["status"] == "UNIT_IDEAL_EXACT_Q" and result["group_id"] == group_id
    assert result["source_sha256"] == lane["source_sha256"]
    assert result["termination"] is None and result["returncode"] == 0
    assert result["automatic_relaunch"] is False and result["stderr"] == ""
    required = {"INPUT_VARIABLES=91", "INPUT_GENERATORS=6577", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"}
    assert required <= set(result["stdout"].splitlines())
    batch_row = batch["completed"][group_id - 126]
    assert batch_row["result_sha256"] == sha(result_path)
    walls.append(result["wall_seconds"])
    rss.append(result["peak_group_rss_bytes"])

assert sorted(path.name for path in (RUN / "results").glob("group*.json")) == [f"group{i:03d}.json" for i in range(126, 162)]
normalized = json.loads((RUN / "normalized_dependencies.json").read_text())
assert normalized["closed_union"] == list(range(126))
assert normalized["status"] == "PASS_NORMALIZED_EXACT_CLOSED_UNION_0_125"
out = {
    "schema": "KRENN_X5_REP4_GROUPS126_161_EXACT_Q_TERMINAL_REFEREE_V2",
    "status": "PASS_ALL_36_EXACT_Q_UNIT_IDEALS",
    "groups_closed": list(range(126, 162)),
    "dependency_closed_union": list(range(126)),
    "closed_union_after_batch": list(range(162)),
    "strict_sequential": True,
    "parallel": False,
    "relaunch": False,
    "maximum_wall_seconds": max(walls),
    "aggregate_wall_seconds": sum(walls),
    "maximum_peak_rss_bytes": max(rss),
    "resource_clear": True,
    "held_manifest_sha256": sha(RUN / "MANIFEST.sha256"),
    "terminal_manifest_sha256": sha(RUN / "TERMINAL_MANIFEST.sha256"),
    "batch_result_sha256": sha(batch_path),
    "compatibility_repair_changed_mathematics": False,
    "rep4_canonical_groups_closed": True,
    "full_conjecture_closed": False,
}
atomic(HERE / "results_referee.json", out)
print(json.dumps({"status": out["status"], "groups": 36, "max_wall": max(walls), "max_rss": max(rss)}, sort_keys=True))
