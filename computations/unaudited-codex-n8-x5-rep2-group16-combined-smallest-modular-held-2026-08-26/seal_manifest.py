#!/usr/bin/env python3
"""Seal only this held package and its explicit authoritative dependencies."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
REF = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-referee-comparison-2026-08-26"
TOR = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-decomposition-design-2026-08-26"
GUA = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-isomorphism-guard-pivot-design-2026-08-26"
TERM = ROOT / "computations/unaudited-codex-n8-x5-rep2-first25-exact-q-terminal-referee-2026-08-26"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


local = [
    H / "REPORT.md", H / "build_contract.py", H / "build_source.py",
    H / "held_pilot.json", H / "independent_referee_acceptance.schema.json",
    H / "launch_clearance.schema.json", H / "refusal_contract.json",
    H / "rep2_group016_torus_zerozero_guardpivot_k0_p32003.sing",
    H / "run_one_lane.py", H / "seal_manifest.py", H / "source_derivation.json",
    H / "validate.py",
]
external = [
    REF / "MANIFEST.sha256",
    REF / "rep2_group016_torus_A67zero_A12zero_guardpivot_k0_Q.sing",
    TOR / "MANIFEST.sha256", GUA / "MANIFEST.sha256", TERM / "FINAL_MANIFEST.sha256",
]
paths = local + external
assert all(path.is_file() for path in paths)
lines = [f"{sha(path)}  {os.path.relpath(path, H)}" for path in sorted(paths, key=lambda p: os.path.relpath(p, H))]
temporary = H / "MANIFEST.sha256.tmp"
temporary.write_text("\n".join(lines) + "\n")
os.replace(temporary, H / "MANIFEST.sha256")
print(f"sealed {len(lines)} explicit files")
