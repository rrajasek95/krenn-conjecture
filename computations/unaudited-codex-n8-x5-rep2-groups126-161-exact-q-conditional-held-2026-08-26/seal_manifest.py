#!/usr/bin/env python3
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
local=['REPORT.md','build_contract.py','build_plan.py','build_runner.py','build_sources.py','dependency_verifier.py','future_dependencies.json','held_schedule.json','independent_referee_acceptance.schema.json','launch_clearance.schema.json','normalize_dependencies.py','results_hostile_tests.json','run_groups126_161.py','seal_manifest.py','source_ledger.json','test_dependencies.py','validate.py']+[f'sources/rep2_group{i:03d}_Q.sing' for i in range(126,162)];ledger=json.loads((HERE/'source_ledger.json').read_text());entries=[]
for name in local:path=HERE/name;assert path.is_file();entries.append((sha(path),name))
for rel,want in sorted(ledger['pins'].items()):path=ROOT/rel;assert path.is_file() and sha(path)==want;entries.append((want,os.path.relpath(path,HERE)))
assert len(local)==53 and len(ledger['pins'])==5 and len(entries)==58;tmp=HERE/'MANIFEST.sha256.tmp';tmp.write_text(''.join(f'{digest}  {name}\n' for digest,name in entries));os.replace(tmp,HERE/'MANIFEST.sha256');print(json.dumps({'status':'SEALED_FINAL_REP2_CONDITIONAL_ZERO_RUN','lines':58,'manifest_sha256':sha(HERE/'MANIFEST.sha256')},sort_keys=True))
