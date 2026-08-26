#!/usr/bin/env python3
"""Write only this package's explicit manifest scope; never scan computations."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LOCAL = [
    "REPORT.md",
    "build_held_pilot.py",
    "held_pilot.json",
    "launch_clearance.schema.json",
    "refusal_contract.json",
    "rep5_all_equal_y_i0_p00_x0_y0_d01_p32003.sing",
    "run_one_lane.py",
    "seal_manifest.py",
    "validate.py",
]
EXTERNAL = [
    ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25/MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25/generate_design.py",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25/results_rep5_contraction_design.json",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25/rep5_guard_minor_tiny_y_p32003.sing",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-referee-2026-08-25/FINAL_MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-referee-2026-08-25/HELD_MODULAR_PILOT.json",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-referee-2026-08-25/results_independent_referee.json",
    Path("/usr/local/bin/Singular"),
    Path("/usr/local/bin/gtimeout"),
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            value.update(chunk)
    return value.hexdigest()


lines = []
for name in LOCAL:
    path = HERE / name
    assert path.is_file(), path
    lines.append(f"{digest(path)}  {name}")
for path in EXTERNAL:
    assert path.is_file(), path
    display = str(path if str(path).startswith("/usr/") else Path(os.path.relpath(path, HERE)))
    lines.append(f"{digest(path)}  {display}")
assert len(lines) == len(LOCAL) + len(EXTERNAL) == 18
output = HERE / "MANIFEST.sha256"
temporary = output.with_suffix(".sha256.tmp")
temporary.write_text("\n".join(lines) + "\n")
os.replace(temporary, output)
print(digest(output))
