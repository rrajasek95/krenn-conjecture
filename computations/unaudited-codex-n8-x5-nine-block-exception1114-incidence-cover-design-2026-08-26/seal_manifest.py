#!/usr/bin/env python3
"""Seal and replay only the explicit local design files."""

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = (
    "REPORT.md",
    "build_design.py",
    "carrier_ledger.json",
    "held_smallest_chart_plan.json",
    "incidence_cover_ledger.json",
    "make_hostiles.py",
    "rep1114_rank1_canonical_Q.sing",
    "results_exception1114_design.json",
    "results_hostiles.json",
    "seal_manifest.py",
    "torus_nullspace_basis.json",
    "validate.py",
)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


lines = []
for name in FILES:
    path = HERE / name
    if not path.is_file():
        raise RuntimeError(("missing", name))
    lines.append(f"{sha(path)}  {name}")
manifest = HERE / "MANIFEST.sha256"
manifest.write_text("\n".join(lines) + "\n")
for line in manifest.read_text().splitlines():
    expected, name = line.split("  ", 1)
    if sha(HERE / name) != expected:
        raise RuntimeError(("mismatch", name))
print(sha(manifest))
