#!/usr/bin/env python3
"""Seal and replay the exact second-factor design package."""
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-rep5-smallest67-factor-determinant-reduction-design-2026-08-26"
paths = [
    HERE / "build_design.py",
    HERE / "referee.py",
    HERE / "validate.py",
    HERE / "seal_manifest.py",
    HERE / "REPORT.md",
    HERE / "results_design.json",
    HERE / "results_referee.json",
    HERE / "results_hostiles.json",
    HERE / "sources/D_a04_00_Q_design.sing",
    HERE / "sources/V_a04_00_Q_design.sing",
    PARENT / "MANIFEST.sha256",
    PARENT / "results_design.json",
    PARENT / "results_referee.json",
    PARENT / "sources/V_a24_00_Q_design.sing",
]
lines = []
for path in paths:
    assert path.is_file(), path
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    relative = path.relative_to(HERE) if path.is_relative_to(HERE) else Path("..") / path.relative_to(HERE.parent)
    lines.append(f"{digest}  {relative}")
manifest = HERE / "MANIFEST.sha256"
manifest.write_text("\n".join(lines) + "\n")
for line in manifest.read_text().splitlines():
    digest, relative = line.split("  ", 1)
    assert hashlib.sha256((HERE / relative).read_bytes()).hexdigest() == digest
print({"status": "SEALED_SMALLEST66_SECOND_FACTOR_DESIGN", "lines": len(lines), "sha256": hashlib.sha256(manifest.read_bytes()).hexdigest()})
