#!/usr/bin/env python3
"""Seal only this referee package and its explicit authoritative inputs."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
TOR = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-decomposition-design-2026-08-26"
GUA = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-isomorphism-guard-pivot-design-2026-08-26"
RUN = ROOT / "computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25"
DES = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25"

local = [
    H / "REPORT.md",
    H / "combined_57_ledger.json",
    H / "referee_compare.py",
    H / "rep2_group016_torus_A67zero_A12zero_guardpivot_k0_Q.sing",
    H / "results_referee_comparison.json",
    H / "seal_manifest.py",
    H / "validate.py",
]
external = [
    TOR / "MANIFEST.sha256",
    TOR / "results_design.json",
    TOR / "results_hostiles.json",
    TOR / "build_design.py",
    GUA / "MANIFEST.sha256",
    GUA / "results_group16_design.json",
    GUA / "rep2_group016_guardpivot_k0_Q.sing",
    GUA / "rep2_group016_guardpivot_k1_Q.sing",
    GUA / "rep2_group016_guardpivot_k2_Q.sing",
    RUN / "TERMINAL_MANIFEST.sha256",
    RUN / "batch_result.json",
    RUN / "results/group016.json",
    RUN / "sources/rep2_group016_Q.sing",
    DES / "generate_design.py",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


paths = local + external
assert all(path.is_file() for path in paths)
lines = [f"{sha(path)}  {os.path.relpath(path, H)}" for path in sorted(paths, key=lambda p: os.path.relpath(p, H))]
tmp = H / "MANIFEST.sha256.tmp"
tmp.write_text("\n".join(lines) + "\n")
os.replace(tmp, H / "MANIFEST.sha256")
print(f"sealed {len(lines)} explicit files")
