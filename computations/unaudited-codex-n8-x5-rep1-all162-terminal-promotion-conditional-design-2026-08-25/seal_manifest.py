#!/usr/bin/env python3
"""Seal only this package plus the explicit authoritative inputs."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


local_names = [
    "REPORT.md",
    "build_acceptance_schema.py",
    "build_promotion_design.py",
    "future_dependencies.json",
    "results_hostile_tests.json",
    "results_terminal_promotion_design.json",
    "seal_manifest.py",
    "terminal_promotion_acceptance.schema.json",
    "test_promotion_contract.py",
    "validate.py",
]
design = json.loads((HERE / "results_terminal_promotion_design.json").read_text())
entries = []
for name in local_names:
    path = HERE / name
    assert path.is_file()
    entries.append((sha256(path), name))
for relative, expected in sorted(design["pins"].items()):
    path = ROOT / relative
    assert path.is_file() and sha256(path) == expected
    entries.append((expected, os.path.relpath(path, HERE)))
assert len(local_names) == 10 and len(design["pins"]) == 19 and len(entries) == 29
temporary = HERE / "MANIFEST.sha256.tmp"
temporary.write_text("".join(f"{digest}  {relative}\n" for digest, relative in entries))
os.replace(temporary, HERE / "MANIFEST.sha256")
print(json.dumps({"status": "SEALED_EXPLICIT_SCOPE", "local": 10, "external": 19, "lines": 29, "manifest_sha256": sha256(HERE / "MANIFEST.sha256")}, sort_keys=True))
