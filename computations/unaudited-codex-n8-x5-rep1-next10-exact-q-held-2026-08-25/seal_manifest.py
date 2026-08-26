#!/usr/bin/env python3
import hashlib,os
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1]
LOCAL=['REPORT.md','build_plan.py','build_sources.py','held_schedule.json','independent_referee_acceptance.schema.json','launch_clearance.schema.json','run_next10.py','seal_manifest.py','source_ledger.json','validate.py']+[f'sources/rep1_group{i:03d}_Q.sing' for i in range(1,11)]
EXT=[R/'computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25/MANIFEST.sha256',R/'computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25/generate_minor_quotient.py',R/'computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25/MANIFEST.sha256',R/'computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25/results_canonical_census.json',R/'computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-referee-2026-08-25/FINAL_MANIFEST.sha256',R/'computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-exact-q-2026-08-25/MANIFEST.sha256',R/'computations/unaudited-codex-n8-x5-rep1-group13-exact-q-referee-2026-08-25/FINAL_MANIFEST.sha256',R/'computations/unaudited-codex-n8-x5-rep1-group15-exact-q-terminal-referee-2026-08-25/FINAL_MANIFEST.sha256',Path('/usr/local/bin/Singular'),Path('/usr/local/bin/gtimeout')]
def s(p):return hashlib.sha256(p.read_bytes()).hexdigest()
lines=[]
for n in LOCAL:p=H/n;assert p.is_file();lines.append(f'{s(p)}  {n}')
for p in EXT:assert p.is_file();lines.append(f'{s(p)}  {p if str(p).startswith("/usr/") else Path(os.path.relpath(p,H))}')
assert len(lines)==30
t=H/'MANIFEST.sha256.tmp';t.write_text('\n'.join(lines)+'\n');os.replace(t,H/'MANIFEST.sha256');print(s(H/'MANIFEST.sha256'))
