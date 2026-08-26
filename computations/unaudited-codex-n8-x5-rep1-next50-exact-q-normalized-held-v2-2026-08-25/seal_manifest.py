#!/usr/bin/env python3
"""Seal the normalized superseding package and its explicit provenance."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LOCAL = (
    "REPORT.md", "build_plan_v2.py", "build_result.json", "build_superseding.py",
    "held_schedule_v2.json", "independent_referee_acceptance.schema.json",
    "launch_clearance.schema.json", "normalize_next25_dependency.py",
    "normalized_next25_dependency.json", "results_adapter_tests.json",
    "run_next50_v2.py", "seal_manifest.py", "source_ledger.json", "test_adapter.py", "validate.py",
)
EXTERNAL = (
    ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-conditional-held-2026-08-25/MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-conditional-held-2026-08-25/source_ledger.json",
    ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-conditional-held-2026-08-25/run_next50.py",
    ROOT / "computations/unaudited-codex-n8-x5-rep1-next25-exact-q-held-referee-2026-08-25/FINAL_MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep1-next25-exact-q-held-referee-2026-08-25/results_referee.json",
    ROOT / "computations/unaudited-codex-n8-x5-rep1-next25-exact-q-terminal-referee-2026-08-25/FINAL_MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep1-next25-exact-q-terminal-referee-2026-08-25/results_referee.json",
    ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-next25-satisfied-binding-audit-2026-08-25/FINAL_MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-next25-satisfied-binding-audit-2026-08-25/results_binding.json",
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
for gid in range(38, 88):
    name = f"sources/rep1_group{gid:03d}_Q.sing"
    path = HERE / name
    assert path.is_file(), path
    lines.append(f"{sha256(path)}  {name}")
for path in EXTERNAL:
    assert path.is_file(), path
    display = str(path) if not str(path).startswith(str(ROOT)) else os.path.relpath(path, HERE)
    lines.append(f"{sha256(path)}  {display}")
assert len(lines) == 76 and len(lines) == len(set(lines))
(HERE / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print(sha256(HERE / "MANIFEST.sha256"))
