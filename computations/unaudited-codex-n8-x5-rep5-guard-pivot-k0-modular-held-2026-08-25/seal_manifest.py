#!/usr/bin/env python3
"""Seal only this package and its explicit provenance pins."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LOCAL = (
    "REPORT.md", "build_held_metadata.py", "build_package.py", "build_result.json",
    "held_pilot.json", "independent_referee_acceptance.schema.json",
    "launch_clearance.schema.json", "refusal_contract.json",
    "rep5_p00_guardpivot_k0_p32003.sing", "run_one_lane.py", "seal_manifest.py", "validate.py",
)
EXTERNAL = (
    ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-2026-08-25/MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-2026-08-25/rep5_p00_guardpivot_k0_Q.sing",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-referee-2026-08-25/FINAL_MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-referee-2026-08-25/HELD_DIAGNOSTIC_PLAN.json",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-v2-2026-08-25/run_one_lane.py",
    Path("/usr/local/bin/Singular"), Path("/usr/local/bin/gtimeout"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


lines = []
for name in LOCAL:
    path = HERE / name
    assert path.is_file(), path
    lines.append(f"{sha256(path)}  {name}")
for path in EXTERNAL:
    assert path.is_file(), path
    display = str(path) if path.is_absolute() and not str(path).startswith(str(ROOT)) else os.path.relpath(path, HERE)
    lines.append(f"{sha256(path)}  {display}")
assert len(lines) == 19 and len(lines) == len(set(lines))
(HERE / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print(sha256(HERE / "MANIFEST.sha256"))
