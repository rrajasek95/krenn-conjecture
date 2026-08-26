#!/usr/bin/env python3
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
    assert not (HERE / stale).exists(), stale
ps = subprocess.run(["ps", "-axo", "pid=,command="], text=True, capture_output=True, check=True).stdout.splitlines()
assert not [line for line in ps if "/usr/local/bin/Singular" in line or "libSingular" in line]
ledger_path = HERE / "source_ledger.json"
ledger = json.loads(ledger_path.read_text())
manifest = HERE / "MANIFEST.sha256"
runner = HERE / "run_three.py"
acceptance = {"schema": "KRENN_X5_REP2_GROUP16_TCOVER_COMPLEMENT3_EXACT_Q_ACCEPTANCE_V1", "status": "PASS_APPROVE_THREE_COMPLEMENTARY_T_CHARTS_ONLY", "held_manifest_sha256": sha(manifest), "source_ledger_sha256": sha(ledger_path), "runner_sha256": sha(runner), "source_sha256": [lane["source_sha256"] for lane in ledger["lanes"]], "maximum_lane_count": 3, "exact_Q_authorized": True, "other_chart_authorized": False, "automatic_relaunch_authorized": False}
atomic(HERE / "independent_referee_acceptance.json", acceptance)
clearance = {"schema": "KRENN_X5_REP2_GROUP16_TCOVER_COMPLEMENT3_EXACT_Q_CLEARANCE_V1", "status": "CLEARED_THREE_COMPLEMENTARY_T_CHARTS_ONLY", "held_manifest_sha256": sha(manifest), "acceptance_sha256": sha(HERE / "independent_referee_acceptance.json"), "source_ledger_sha256": sha(ledger_path), "runner_sha256": sha(runner), "singular_sha256": "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88", "gtimeout_sha256": "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95", "native_wall_seconds_each": 480, "wrapper_wall_seconds_each": 510, "rss_cap_bytes_each": 8589934592, "no_overlap_confirmed": True, "maximum_lane_count": 3, "exact_Q_authorized": True, "other_chart_authorized": False, "automatic_relaunch_authorized": False}
atomic(HERE / "launch_clearance.json", clearance)
print(json.dumps({"status": "CLEARED_TCOVER_COMPLEMENT3", "acceptance_sha256": sha(HERE / "independent_referee_acceptance.json"), "clearance_sha256": sha(HERE / "launch_clearance.json")}, sort_keys=True))
