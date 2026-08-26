#!/usr/bin/env python3
"""Seal and replay the compact combined referee package."""

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "MANIFEST.sha256"


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


names = sorted(path.name for path in HERE.iterdir() if path.is_file() and path.name != MANIFEST.name)
MANIFEST.write_text("".join(f"{digest(HERE / name)}  {name}\n" for name in names))
for line in MANIFEST.read_text().splitlines():
    expected, name = line.split("  ", 1)
    if digest(HERE / name) != expected:
        raise RuntimeError((name, "manifest replay"))
print(digest(MANIFEST))
