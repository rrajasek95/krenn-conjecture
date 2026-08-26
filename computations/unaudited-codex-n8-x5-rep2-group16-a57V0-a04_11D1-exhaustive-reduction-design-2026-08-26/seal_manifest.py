#!/usr/bin/env python3
from __future__ import annotations
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
local=["REPORT.md","analyze.py","results_design.json","results_hostiles.json","seal_manifest.py","test_design.py","validate.py"]
local += sorted(str(p.relative_to(HERE)) for p in (HERE/"intermediate").rglob("*") if p.is_file())
local += sorted(str(p.relative_to(HERE)) for p in (HERE/"sources").glob("*.sing"))
external=["../unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-design-2026-08-26/MANIFEST.sha256","../unaudited-codex-n8-x5-rep2-group16-a57V0-a04_11-residual-split-design-2026-08-26/MANIFEST.sha256","../unaudited-codex-n8-x5-rep2-group16-a57V0-a04_11-residual-split-design-2026-08-26/sources/rep2_group16_Dt1_a04_11_D1_Q_design.sing"]
lines=[f"{sha(HERE/p)}  {p}" for p in local]+[f"{sha((HERE/p).resolve())}  {p}" for p in external]
(HERE/"MANIFEST.sha256").write_text("\n".join(lines)+"\n");print(sha(HERE/"MANIFEST.sha256"))
