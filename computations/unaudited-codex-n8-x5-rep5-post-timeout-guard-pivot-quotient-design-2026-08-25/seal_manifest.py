#!/usr/bin/env python3
import hashlib,os
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1]
L=['REPORT.md','generate_design.py','rep5_p00_guardpivot_k0_Q.sing','rep5_p00_guardpivot_k1_Q.sing','rep5_p00_guardpivot_k2_Q.sing','results_design.json','seal_manifest.py','validate.py']
E=[R/'computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25/MANIFEST.sha256',R/'computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25/generate_design.py',R/'computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25/results_rep5_contraction_design.json',R/'computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-v2-2026-08-25/result.json',R/'computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-v2-2026-08-25/ATTEMPT.json',R/'computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-v2-terminal-referee-2026-08-25/FINAL_MANIFEST.sha256',R/'computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-v2-terminal-referee-2026-08-25/results_referee.json']
def s(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=[]
for n in L:p=H/n;assert p.is_file();a.append(f'{s(p)}  {n}')
for p in E:assert p.is_file();a.append(f'{s(p)}  {Path(os.path.relpath(p,H))}')
assert len(a)==15;t=H/'MANIFEST.sha256.tmp';t.write_text('\n'.join(a)+'\n');os.replace(t,H/'MANIFEST.sha256');print(s(H/'MANIFEST.sha256'))
