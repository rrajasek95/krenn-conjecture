#!/usr/bin/env python3
import hashlib,os
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1]
L=['REPORT.md','build_held.py','held_pilot.json','independent_referee_acceptance.schema.json','launch_clearance.schema.json','refusal_contract.json','rep4_all_equal_y_i0_p00_x0_y0_d01_p32003.sing','run_one_lane.py','seal_manifest.py','validate.py']
E=[R/'computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25/MANIFEST.sha256',R/'computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25/rep4_guard_minor_tiny_y_Q.sing',R/'computations/unaudited-codex-n8-x5-rep4-all-equal-y-modular-terminal-second-referee-2026-08-25/FINAL_MANIFEST.sha256',R/'computations/unaudited-codex-n8-x5-rep4-all-equal-y-modular-terminal-second-referee-2026-08-25/results_referee.json',R/'computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-v2-referee-2026-08-25/FINAL_MANIFEST.sha256',R/'computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-v2-referee-2026-08-25/results_referee.json',Path('/usr/local/bin/Singular'),Path('/usr/local/bin/gtimeout')]
def s(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=[]
for n in L:p=H/n;assert p.is_file();a.append(f'{s(p)}  {n}')
for p in E:assert p.is_file();a.append(f'{s(p)}  {p if str(p).startswith("/usr/") else Path(os.path.relpath(p,H))}')
assert len(a)==18;t=H/'MANIFEST.sha256.tmp';t.write_text('\n'.join(a)+'\n');os.replace(t,H/'MANIFEST.sha256');print(s(H/'MANIFEST.sha256'))
