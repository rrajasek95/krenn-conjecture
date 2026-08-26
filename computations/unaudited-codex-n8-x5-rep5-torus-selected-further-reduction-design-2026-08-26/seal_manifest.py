#!/usr/bin/env python3
"""Seal the explicit reduction-design package and selected source pins."""
from __future__ import annotations
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
LOCAL=("REPORT.md","analyze.py","results_design.json","results_hostiles.json","seal_manifest.py","test_design.py","validate.py","sources/stage0_a37_201_Q_design.sing","sources/stage1_a37_200_closed_Q_design.sing")
EXTERNAL=("../unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26/MANIFEST.sha256","../unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26/sources/rep5_k2_t1_gauge_yn11_yn21_t01_t20_Q_design.sing","../unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-referee-2026-08-26/MANIFEST.sha256")
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lines=[f"{sha(HERE/name)}  {name}" for name in LOCAL]+[f"{sha((HERE/name).resolve())}  {name}" for name in EXTERNAL]
(HERE/"MANIFEST.sha256").write_text("\n".join(lines)+"\n")
print(sha(HERE/"MANIFEST.sha256"))
