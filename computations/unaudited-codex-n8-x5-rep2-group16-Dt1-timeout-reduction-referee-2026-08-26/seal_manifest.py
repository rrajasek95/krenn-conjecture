#!/usr/bin/env python3
import hashlib
import os
from pathlib import Path

here = Path(__file__).resolve().parent
names = [
    "HELD_PLAN.json",
    "REPORT.md",
    "referee_and_plan.py",
    "rep2_group16_Dt1_global_unit_gauge_runtime_Q.sing",
    "results_referee.json",
    "seal_manifest.py",
    "validate.py",
]
lines = [f"{hashlib.sha256((here / name).read_bytes()).hexdigest()}  {name}" for name in names]
tmp = here / "FINAL_MANIFEST.sha256.tmp"
tmp.write_text("\n".join(lines) + "\n")
os.replace(tmp, here / "FINAL_MANIFEST.sha256")
print(hashlib.sha256((here / "FINAL_MANIFEST.sha256").read_bytes()).hexdigest())
