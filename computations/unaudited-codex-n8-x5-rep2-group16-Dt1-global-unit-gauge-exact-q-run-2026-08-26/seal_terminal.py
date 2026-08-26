#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

here = Path(__file__).resolve().parent
r = json.loads((here / "result.json").read_text())
assert r["status"] == "UNIT_IDEAL_EXACT_Q" and r["mathematical_coverage"] is True
assert r["returncode"] == 0 and r["termination"] is None
assert r["variables"] == 61 and r["generators"] == 6568
assert all(token in r["stdout"] for token in ("INPUT_VARIABLES=61", "INPUT_GENERATORS=6568", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"))
assert r["other_chart_launched"] is r["automatic_relaunch"] is False
names = [
    "ATTEMPT.json", "PLAN.json", "REPORT.md", "RUNNER_INPUT_MANIFEST.sha256",
    "RUN_EXCLUSIVE.lock", "independent_referee_acceptance.json",
    "launch_clearance.json", "rep2_group16_Dt1_global_unit_gauge_runtime_Q.sing",
    "result.json", "run_one_lane.py", "seal_terminal.py",
]
lines = [f"{hashlib.sha256((here / name).read_bytes()).hexdigest()}  {name}" for name in names]
tmp = here / "TERMINAL_MANIFEST.sha256.tmp"
tmp.write_text("\n".join(lines) + "\n")
os.replace(tmp, here / "TERMINAL_MANIFEST.sha256")
print(hashlib.sha256((here / "TERMINAL_MANIFEST.sha256").read_bytes()).hexdigest())
