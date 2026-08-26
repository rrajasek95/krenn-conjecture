#!/usr/bin/env python3
"""Launch the frozen sole-reader 11-edge scan from AUDIT_PLAN.json."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
plan_path = HERE / "AUDIT_PLAN.json"
assert sha256(plan_path.read_bytes()).hexdigest() == "1dc6466bdde6b4fb67aca27bac0facdceac0e71472ba9b7d778a33b084be59cc"
plan = json.loads(plan_path.read_text())
producer = ROOT / plan["production_root"]
arguments = [
    str(HERE / "scan_chain_once"),
    str(HERE / "results_round1613_single_pass_replay.json"),
    str(ROOT / plan["input"]["checkpoint"]),
    str(ROOT / plan["input"]["vectors"]),
]
for stage in plan["stages"]:
    directory = producer / stage["name"]
    arguments.extend([str(directory / "checkpoint.bin"),
                      str(directory / "vectors.bin")])
subprocess.run(arguments, check=True)
