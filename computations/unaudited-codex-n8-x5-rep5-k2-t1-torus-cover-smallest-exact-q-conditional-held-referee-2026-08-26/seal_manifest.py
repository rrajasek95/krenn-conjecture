#!/usr/bin/env python3
"""Seal only the explicit referee artifacts and two producer pins."""
from __future__ import annotations

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = (
    "REPORT.md", "HELD_APPROVAL.json", "referee.py", "results_referee.json", "seal_manifest.py", "validate.py",
)
EXTERNAL = (
    "../unaudited-codex-n8-x5-rep5-k2-t1-torus-cover-smallest-exact-q-conditional-held-2026-08-26/MANIFEST.sha256",
    "../unaudited-codex-n8-x5-rep5-k2-t1-torus-cover-smallest-exact-q-conditional-held-2026-08-26/rep5_k2_t1_torus_smallest_Q.sing",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


lines = [f"{digest(HERE / name)}  {name}" for name in FILES]
lines.extend(f"{digest((HERE / name).resolve())}  {name}" for name in EXTERNAL)
(HERE / "FINAL_MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print(digest(HERE / "FINAL_MANIFEST.sha256"))
