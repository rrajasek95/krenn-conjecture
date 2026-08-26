#!/usr/bin/env python3
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
    "sources/rep2_group16_Dt1_a04_11_D1_Q_design.sing",
    "sources/rep2_group16_Dt1_a04_11_V0_Q_design.sing",
)
external = (
    "../unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-design-2026-08-26/MANIFEST.sha256",
    "../unaudited-codex-n8-x5-rep2-group16-Vt1Vt2Dt0-residual-torus-design-2026-08-26/MANIFEST.sha256",
    "../unaudited-codex-n8-x5-rep2-group16-Vt1Vt2Dt0-residual-torus-design-2026-08-26/sources/rep2_group16_Dt1_a57_01_V0_Q_design.sing",
)
lines = [f"{sha(HERE / name)}  {name}" for name in local]
lines += [f"{sha((HERE / name).resolve())}  {name}" for name in external]
(HERE / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print(sha(HERE / "MANIFEST.sha256"))
