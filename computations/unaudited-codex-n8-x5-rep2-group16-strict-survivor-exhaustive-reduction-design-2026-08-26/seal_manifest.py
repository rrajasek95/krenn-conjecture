#!/usr/bin/env python3
from __future__ import annotations
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
local=["REPORT.md","analyze.py","results_design.json","results_hostiles.json","seal_manifest.py","test_design.py","validate.py"]
local += [f"intermediate/step{i:02d}_{name}.sing" for i,name in enumerate([
"forced_zero_a14_11","forced_zero_a14_21","monic_graph_a14_12","monic_graph_a14_22","monic_graph_a14_02","monic_graph_a14_10","monic_graph_a14_20","monic_graph_a14_00","global_unit_gauge","forced_zero_a26_11","forced_zero_a26_01"],1)]
local += ["intermediate/torus_probe_09/results_design.json","intermediate/torus_probe_09/sources/rep2_group16_Dt1_a17_01_GLOBAL_UNIT_GAUGE_Q_design.sing"]
external=["../unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-design-2026-08-26/MANIFEST.sha256","../unaudited-codex-n8-x5-rep2-group16-a57V0-a04_11V0-monic-next-cover-design-2026-08-26/MANIFEST.sha256","../unaudited-codex-n8-x5-rep2-group16-a57V0-a04_11V0-monic-next-cover-design-2026-08-26/sources/rep2_group16_Dt1_a14_01_V0_Q_design.sing"]
lines=[f"{sha(HERE/p)}  {p}" for p in local]+[f"{sha((HERE/p).resolve())}  {p}" for p in external]
(HERE/"MANIFEST.sha256").write_text("\n".join(lines)+"\n");print(sha(HERE/"MANIFEST.sha256"))
