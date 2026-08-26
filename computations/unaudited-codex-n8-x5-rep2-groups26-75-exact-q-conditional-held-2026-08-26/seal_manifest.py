#!/usr/bin/env python3
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
local=['REPORT.md','build_plan.py','build_sources.py','future_dependency.json','held_schedule.json','independent_referee_acceptance.schema.json','launch_clearance.schema.json','normalize_dependency.py','results_hostile_tests.json','run_groups26_75.py','seal_manifest.py','source_ledger.json','test_dependency.py','validate.py']+[f'sources/rep2_group{i:03d}_Q.sing' for i in range(26,76)];l=json.loads((HERE/'source_ledger.json').read_text());e=[]
for name in local:path=HERE/name;assert path.is_file();e.append((sha(path),name))
for rel,h in sorted(l['pins'].items()):path=ROOT/rel;assert path.is_file() and sha(path)==h;e.append((h,os.path.relpath(path,HERE)))
assert len(local)==64 and len(l['pins'])==5 and len(e)==69;t=HERE/'MANIFEST.sha256.tmp';t.write_text(''.join(f'{h}  {n}\n' for h,n in e));os.replace(t,HERE/'MANIFEST.sha256');print(json.dumps({'status':'SEALED_CONDITIONAL_ZERO_RUN','lines':69,'manifest_sha256':sha(HERE/'MANIFEST.sha256')},sort_keys=True))
