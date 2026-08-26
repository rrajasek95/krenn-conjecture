#!/usr/bin/env python3
"""Seal this held package and only its explicit external inputs."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


local = [
    "REPORT.md", "build_plan.py", "build_sources.py", "canonical_census.json", "held_schedule.json",
    "independent_referee_acceptance.schema.json", "launch_clearance.schema.json", "results_hostile_tests.json",
    "run_first25.py", "seal_manifest.py", "source_ledger.json", "test_contract.py", "validate.py",
] + [f"sources/rep2_group{group_id:03d}_Q.sing" for group_id in range(1, 26)]
ledger = json.loads((HERE / "source_ledger.json").read_text())
entries = []
for relative in local:
    path = HERE / relative
    assert path.is_file()
    entries.append((sha256(path), relative))
for relative, expected in sorted(ledger["pins"].items()):
    path = ROOT / relative
    assert path.is_file() and sha256(path) == expected
    entries.append((expected, os.path.relpath(path, HERE)))
assert len(local) == 38 and len(ledger["pins"]) == 11 and len(entries) == 49
temporary = HERE / "MANIFEST.sha256.tmp"
temporary.write_text("".join(f"{digest}  {relative}\n" for digest, relative in entries))
os.replace(temporary, HERE / "MANIFEST.sha256")
print(json.dumps({"status": "SEALED_ZERO_RUN", "local": 38, "external": 11, "lines": 49, "manifest_sha256": sha256(HERE / "MANIFEST.sha256")}, sort_keys=True))
