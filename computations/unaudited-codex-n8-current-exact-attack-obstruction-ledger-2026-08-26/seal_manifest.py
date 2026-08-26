#!/usr/bin/env python3
"""Seal only the bounded ledger package."""

import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = [
    "REPORT.md",
    "build_ledger.py",
    "results_attack_obstruction_ledger.json",
    "results_hostiles.json",
    "seal_manifest.py",
    "validate.py",
]


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    lines = []
    for name in FILES:
        path = HERE / name
        if not path.is_file():
            raise SystemExit(f"missing {name}")
        lines.append(f"{sha(path)}  {name}\n")
    tmp = HERE / "MANIFEST.sha256.tmp"
    tmp.write_text("".join(lines))
    os.replace(tmp, HERE / "MANIFEST.sha256")


if __name__ == "__main__":
    main()
