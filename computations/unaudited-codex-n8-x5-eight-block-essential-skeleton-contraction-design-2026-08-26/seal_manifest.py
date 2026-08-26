#!/usr/bin/env python3
"""Write and immediately replay the package-local manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "MANIFEST.sha256"
FILES = (
    "REPORT.md",
    "build_design.py",
    "held_pilot_plan.json",
    "make_hostiles.py",
    "orbit1_diagonal_i0_k0_all00_p32003.sing",
    "orbit1_diagonal_i0_k0_all00_q.sing",
    "results_essential_skeleton_contraction_design.json",
    "results_hostiles.json",
    "seal_manifest.py",
    "validate.py",
)


def sha(path: Path) -> str:
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
MANIFEST.write_text("\n".join(lines) + "\n")
for line in MANIFEST.read_text().splitlines():
    expected, name = line.split("  ", 1)
    observed = sha(HERE / name)
    if observed != expected:
        raise RuntimeError((name, observed, expected))
print(sha(MANIFEST))
