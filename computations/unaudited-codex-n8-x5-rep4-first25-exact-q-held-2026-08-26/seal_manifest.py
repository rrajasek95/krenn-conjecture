#!/usr/bin/env python3
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
local=['REPORT.md','build_plan.py','build_sources.py','canonical_census.json','held_schedule.json','independent_referee_acceptance.schema.json','launch_clearance.schema.json','results_hostile_tests.json','run_first25.py','seal_manifest.py','source_ledger.json','test_contract.py','validate.py']+[f'sources/rep4_group{i:03d}_Q.sing' for i in range(1,26)];l=json.loads((HERE/'source_ledger.json').read_text());e=[]
for name in local:path=HERE/name;assert path.is_file();e.append((sha(path),name))
for rel,h in sorted(l['pins'].items()):path=ROOT/rel;assert path.is_file() and sha(path)==h;e.append((h,os.path.relpath(path,HERE)))
assert len(local)==38 and len(l['pins'])==12 and len(e)==50;t=HERE/'MANIFEST.sha256.tmp';t.write_text(''.join(f'{h}  {n}\n' for h,n in e));os.replace(t,HERE/'MANIFEST.sha256');print(json.dumps({'status':'SEALED_ZERO_RUN','lines':50,'manifest_sha256':sha(HERE/'MANIFEST.sha256')},sort_keys=True))
