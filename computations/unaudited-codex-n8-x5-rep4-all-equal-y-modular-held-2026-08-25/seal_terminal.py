#!/usr/bin/env python3
import hashlib,os
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
LOCAL=['MANIFEST.sha256','RESOURCE_CLEARANCE_BINDING.json','TERMINAL_REPORT.md','independent_referee_acceptance.json','launch_clearance.json','result.json','seal_terminal.py','terminal_audit.json','validate_terminal.py']
EXTERNAL=[ROOT/'computations/unaudited-codex-n8-x5-rep4-all-equal-y-modular-held-referee-2026-08-25/FINAL_MANIFEST.sha256',ROOT/'computations/unaudited-codex-n8-x5-rep4-all-equal-y-modular-held-referee-2026-08-25/results_referee.json']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
lines=[]
for n in LOCAL:
 p=HERE/n; assert p.is_file(); lines.append(f'{sha(p)}  {n}')
for p in EXTERNAL:
 assert p.is_file(); lines.append(f'{sha(p)}  {Path(os.path.relpath(p,HERE))}')
assert len(lines)==11
tmp=HERE/'FINAL_MANIFEST.sha256.tmp';tmp.write_text('\n'.join(lines)+'\n');os.replace(tmp,HERE/'FINAL_MANIFEST.sha256')
print(sha(HERE/'FINAL_MANIFEST.sha256'))
