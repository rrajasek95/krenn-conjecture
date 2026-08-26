#!/usr/bin/env python3
"""Seal and replay the package-local manifest."""

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = (
    "REPORT.md",
    "build_census.py",
    "make_hostiles.py",
    "results_hostiles.json",
    "results_nine_block_induction_census.json",
    "seal_manifest.py",
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
        raise RuntimeError(("replay", name))
print(sha(manifest))
