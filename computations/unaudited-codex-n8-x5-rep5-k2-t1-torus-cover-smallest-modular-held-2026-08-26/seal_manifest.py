#!/usr/bin/env python3
"""Seal held package plus the explicit 16-source selection interface."""
import hashlib,os
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[1]
PROD=ROOT/'computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26';REF=ROOT/'computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-referee-2026-08-26';TIMEOUT=ROOT/'computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-terminal-referee-2026-08-26'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
local=[H/name for name in ('REPORT.md','build_contract.py','build_source.py','held_pilot.json','independent_referee_acceptance.schema.json','launch_clearance.schema.json','refusal_contract.json','rep5_k2_t1_gauge_yn11_yn21_t01_t20_p32003.sing','run_one_lane.py','seal_manifest.py','selection_ledger.json','source_derivation.json','validate.py')]
external=[PROD/'MANIFEST.sha256',PROD/'results_design.json',REF/'MANIFEST.sha256',REF/'results_referee.json',TIMEOUT/'FINAL_MANIFEST.sha256']+sorted((PROD/'sources').glob('*.sing'))
paths=local+external;assert len(list((PROD/'sources').glob('*.sing')))==16 and all(p.is_file() for p in paths)
lines=[f'{sha(p)}  {os.path.relpath(p,H)}' for p in sorted(paths,key=lambda p:os.path.relpath(p,H))]
t=H/'MANIFEST.sha256.tmp';t.write_text('\n'.join(lines)+'\n');os.replace(t,H/'MANIFEST.sha256');print(f'sealed {len(lines)} explicit files')
