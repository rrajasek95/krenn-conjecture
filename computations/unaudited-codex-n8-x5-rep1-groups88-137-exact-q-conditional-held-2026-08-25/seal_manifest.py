#!/usr/bin/env python3
"""Seal the groups88..137 conditional held package and existing provenance."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LOCAL = (
    "REPORT.md", "build_plan.py", "build_runner.py", "build_sources.py",
    "future_groups38_87_dependency.json", "held_schedule.json",
    "independent_referee_acceptance.schema.json", "launch_clearance.schema.json",
    "normalize_future_dependency.py", "results_adapter_tests.json", "run_groups88_137.py",
    "seal_manifest.py", "source_ledger.json", "test_adapter.py", "validate.py",
)
EXTERNAL = (
    ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25/MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25/generate_minor_quotient.py",
    ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25/MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25/results_canonical_census.json",
    ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-referee-2026-08-25/FINAL_MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-2026-08-25/MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-2026-08-25/normalized_next25_dependency.json",
    ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-2026-08-25/run_next50_v2.py",
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
for gid in range(88, 138):
    name = f"sources/rep1_group{gid:03d}_Q.sing"
    path = HERE / name
    assert path.is_file(), path
    lines.append(f"{sha256(path)}  {name}")
for path in EXTERNAL:
    assert path.is_file(), path
    display = str(path) if not str(path).startswith(str(ROOT)) else os.path.relpath(path, HERE)
    lines.append(f"{sha256(path)}  {display}")
assert len(lines) == 75 and len(lines) == len(set(lines))
(HERE / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print(sha256(HERE / "MANIFEST.sha256"))
