#!/usr/bin/env python3
"""Seal only this package and its explicit external pins."""
from __future__ import annotations

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOCAL = (
    "EXTERNAL_PINS.sha256", "REPORT.md", "build_source.py", "held_plan.json", "hostile_tests.py",
    "independent_referee_acceptance.schema.json", "launch_clearance.schema.json", "modular_unit_dependency.json",
    "rep2_group016_62_Vt0_Vt1_Vt2_Q_strong.sing", "results_hostiles.json", "results_validation.json",
    "run_one_lane.py", "seal_manifest.py", "source_derivation.json", "validate.py", "verify_modular_unit_dependency.py",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


(HERE / "MANIFEST.sha256").write_text("\n".join(f"{sha(HERE / name)}  {name}" for name in LOCAL) + "\n")
print(sha(HERE / "MANIFEST.sha256"))
