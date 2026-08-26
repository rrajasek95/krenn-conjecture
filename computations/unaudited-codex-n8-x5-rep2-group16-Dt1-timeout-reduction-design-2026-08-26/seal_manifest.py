#!/usr/bin/env python3
"""Seal the exact timeout-reduction design and its upstream terminal pins."""
from __future__ import annotations

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


local = (
    "REPORT.md",
    "analyze.py",
    "results_design.json",
    "results_hostiles.json",
    "seal_manifest.py",
    "test_design.py",
    "validate.py",
    "sources/rep2_group16_Dt1_it1_GLOBAL_UNIT_GAUGE_Q_design.sing",
)
external = (
    "../unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26/TERMINAL_MANIFEST.sha256",
    "../unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26/results/lane2_Dt1.json",
    "../unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26/sources/rep2_group016_67_Dt1_runtime_Q.sing",
)
lines = [f"{sha(HERE / name)}  {name}" for name in local]
lines.extend(f"{sha((HERE / name).resolve())}  {name}" for name in external)
(HERE / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print(sha(HERE / "MANIFEST.sha256"))
