#!/usr/bin/env python3
import hashlib,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
LOCAL=('REPORT.md','build_plan.py','build_runner.py','build_sources.py','future_groups88_137_dependency.json','held_schedule.json','independent_referee_acceptance.schema.json','launch_clearance.schema.json','normalize_future_dependency.py','results_adapter_tests.json','run_groups138_161.py','seal_manifest.py','source_ledger.json','test_adapter.py','validate.py')
EXTERNAL=(ROOT/'computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25/MANIFEST.sha256',ROOT/'computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25/generate_minor_quotient.py',ROOT/'computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25/MANIFEST.sha256',ROOT/'computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25/results_canonical_census.json',ROOT/'computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-referee-2026-08-25/FINAL_MANIFEST.sha256',ROOT/'computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-conditional-held-2026-08-25/MANIFEST.sha256',ROOT/'computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-conditional-held-2026-08-25/source_ledger.json',ROOT/'computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-conditional-held-2026-08-25/run_groups88_137.py',Path('/usr/local/bin/Singular'),Path('/usr/local/bin/gtimeout'))
def sha(p):
 d=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(1<<20):d.update(b)
 return d.hexdigest()
lines=[]
for name in LOCAL:
 p=HERE/name;assert p.is_file();lines.append(f'{sha(p)}  {name}')
for gid in range(138,162):
 name=f'sources/rep1_group{gid:03d}_Q.sing';p=HERE/name;assert p.is_file();lines.append(f'{sha(p)}  {name}')
for p in EXTERNAL:
 assert p.is_file();display=str(p) if not str(p).startswith(str(ROOT)) else os.path.relpath(p,HERE);lines.append(f'{sha(p)}  {display}')
assert len(lines)==49 and len(lines)==len(set(lines));(HERE/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n');print(sha(HERE/'MANIFEST.sha256'))
