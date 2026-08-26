#!/usr/bin/env python3
"""Seal only this referee and its explicit source/provenance interface."""
import hashlib,os
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[1]
PROD=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-design-2026-08-26';PRIOR=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-referee-comparison-2026-08-26';TERM=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-combined-smallest-modular-terminal-referee-2026-08-26'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
local=[H/name for name in ('REPORT.md','audit.py','results_referee.json','seal_manifest.py','validate.py')]
external=[PROD/'MANIFEST.sha256',PROD/'results_design.json',PROD/'analyze_design.py',PROD/'rep2_group016_67_Dt1_Q.sing',PROD/'rep2_group016_67_Vt1_Dt2_Q.sing',PROD/'rep2_group016_67_Vt1_Vt2_Dt0_Q.sing',PROD/'rep2_group016_67_Vt0_Vt1_Vt2_Q.sing',PRIOR/'MANIFEST.sha256',PRIOR/'results_referee_comparison.json',PRIOR/'rep2_group016_torus_A67zero_A12zero_guardpivot_k0_Q.sing',TERM/'results_referee.json',TERM/'FINAL_MANIFEST.sha256']
paths=local+external;assert all(p.is_file() for p in paths);lines=[f'{sha(p)}  {os.path.relpath(p,H)}' for p in sorted(paths,key=lambda p:os.path.relpath(p,H))]
t=H/'MANIFEST.sha256.tmp';t.write_text('\n'.join(lines)+'\n');os.replace(t,H/'MANIFEST.sha256');print(f'sealed {len(lines)} explicit files')
