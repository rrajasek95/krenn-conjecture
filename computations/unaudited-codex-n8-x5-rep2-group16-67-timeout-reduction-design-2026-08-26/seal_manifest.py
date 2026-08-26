#!/usr/bin/env python3
"""Write the deterministic package manifest (excluding itself)."""

from __future__ import annotations

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "MANIFEST.sha256"


def main() -> None:
    files = sorted(p for p in HERE.iterdir() if p.is_file() and p != MANIFEST)
    lines = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}" for p in files]
    MANIFEST.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
