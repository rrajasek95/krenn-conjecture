#!/usr/bin/env python3
from __future__ import annotations
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
local=("REPORT.md","analyze.py","results_design.json","results_hostiles.json","seal_manifest.py","test_design.py","validate.py","sources/rep2_group16_Dt1_it0_GLOBAL_UNIT_GAUGE_Q_design.sing")
external=("../unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-design-2026-08-26/MANIFEST.sha256","../unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26/MANIFEST.sha256","../unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26/TERMINAL_MANIFEST.sha256","../unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26/batch_result.json","../unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26/sources/rep2_group016_67_Vt1_Vt2_Dt0_runtime_Q.sing")
lines=[f"{sha(HERE/n)}  {n}" for n in local]+[f"{sha((HERE/n).resolve())}  {n}" for n in external]
(HERE/"MANIFEST.sha256").write_text("\n".join(lines)+"\n");print(sha(HERE/"MANIFEST.sha256"))
