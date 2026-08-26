#!/usr/bin/env python3
"""Install exact acceptance and a fresh one-use clearance after a clear process census."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic(path, value):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


for stale in ("BATCH_ATTEMPT.json", "batch_result.json", "results"):
    assert not (HERE / stale).exists(), f"refuse stale/relaunch artifact: {stale}"
ps = subprocess.run(["ps", "-axo", "pid=,command="], text=True, capture_output=True, check=True).stdout.splitlines()
heavy = [line for line in ps if "/usr/local/bin/Singular" in line or "libSingular" in line]
assert not heavy, ("overlapping Singular/libproc process", heavy)

pins = json.loads((HERE / "v2_pins.json").read_text())
manifest = HERE / "MANIFEST.sha256"
normalized = HERE / "normalized_dependencies.json"
runner = HERE / "run_groups126_161.py"
acceptance = {
    "schema": "KRENN_X5_REP4_GROUPS126_161_EXACT_Q_INDEPENDENT_ACCEPTANCE_V1",
    "status": "PASS_APPROVE_CONDITIONAL_REP4_GROUPS126_161_ONLY",
    "held_manifest_sha256": sha(manifest),
    "source_ledger_sha256": pins["source_ledger_sha256"],
    "dependency_verifier_sha256": pins["dependency_verifier_sha256"],
    "normalized_dependencies_sha256": sha(normalized),
    "runner_sha256": sha(runner),
    "required_closed_union": list(range(126)),
    "selected_group_ids": list(range(126, 162)),
    "maximum_lane_count": 36,
    "exact_Q_authorized": True,
    "parallel_authorized": False,
    "skip_reorder_relaunch_authorized": False,
}
atomic(HERE / "independent_referee_acceptance.json", acceptance)
clearance = {
    "schema": "KRENN_X5_REP4_GROUPS126_161_EXACT_Q_EXPLICIT_CLEARANCE_V1",
    "status": "CLEARED_CONDITIONAL_REP4_GROUPS126_161_ONLY",
    "held_manifest_sha256": sha(manifest),
    "independent_referee_acceptance_sha256": sha(HERE / "independent_referee_acceptance.json"),
    "source_ledger_sha256": pins["source_ledger_sha256"],
    "dependency_verifier_sha256": pins["dependency_verifier_sha256"],
    "normalized_dependencies_sha256": sha(normalized),
    "runner_sha256": sha(runner),
    "singular_sha256": "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    "gtimeout_sha256": "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
    "required_closed_union": list(range(126)),
    "selected_group_ids": list(range(126, 162)),
    "native_wall_seconds_each": 240,
    "wrapper_wall_seconds_each": 250,
    "rss_cap_bytes_each": 8589934592,
    "no_overlap_confirmed": True,
    "maximum_lane_count": 36,
    "parallel_authorized": False,
    "skip_reorder_relaunch_authorized": False,
}
atomic(HERE / "launch_clearance.json", clearance)
print(json.dumps({"status": "CLEARED_REP4_FINAL36_V2", "acceptance_sha256": sha(HERE / "independent_referee_acceptance.json"), "clearance_sha256": sha(HERE / "launch_clearance.json")}, sort_keys=True))
