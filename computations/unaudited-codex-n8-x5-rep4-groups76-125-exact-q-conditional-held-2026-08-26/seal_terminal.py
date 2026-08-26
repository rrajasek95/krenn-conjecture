#!/usr/bin/env python3
"""Seal the immutable execution artifacts for the terminal groups76..125 batch."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
IDS = list(range(76, 126))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


names = [
    "normalized_dependencies.json",
    "independent_referee_acceptance.json",
    "launch_clearance.json",
    "BATCH_ATTEMPT.json",
    "batch_result.json",
] + [f"results/group{gid:03d}.json" for gid in IDS]
assert len(names) == 55 and len(set(names)) == 55
for name in names:
    assert (HERE / name).is_file(), name
temporary = HERE / "TERMINAL_MANIFEST.sha256.tmp"
temporary.write_text("".join(f"{sha(HERE / name)}  {name}\n" for name in names))
os.replace(temporary, HERE / "TERMINAL_MANIFEST.sha256")
print(sha(HERE / "TERMINAL_MANIFEST.sha256"))
