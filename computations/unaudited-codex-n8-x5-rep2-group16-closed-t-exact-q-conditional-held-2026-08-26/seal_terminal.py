#!/usr/bin/env python3
"""Seal the one-lane exact-Q terminal artifacts."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAMES = [
    "MANIFEST.sha256",
    "independent_referee_acceptance.json",
    "launch_clearance.json",
    "ATTEMPT.json",
    "RUN_EXCLUSIVE.lock",
    "result.json",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert all((HERE / name).is_file() for name in NAMES)
temporary = HERE / "TERMINAL_MANIFEST.sha256.tmp"
temporary.write_text("".join(f"{sha(HERE / name)}  {name}\n" for name in NAMES))
os.replace(temporary, HERE / "TERMINAL_MANIFEST.sha256")
print(sha(HERE / "TERMINAL_MANIFEST.sha256"))
