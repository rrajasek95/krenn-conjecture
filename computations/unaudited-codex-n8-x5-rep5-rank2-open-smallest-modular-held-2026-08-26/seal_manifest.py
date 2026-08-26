#!/usr/bin/env python3
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
local=['REPORT.md','build_contract.py','build_source.py','held_pilot.json','independent_referee_acceptance.schema.json','launch_clearance.schema.json','rep5_rank2_k2_t1_p32003.sing','run_one_lane.py','seal_manifest.py','source_derivation.json','validate.py'];d=json.loads((HERE/'source_derivation.json').read_text());entries=[]
for name in local:path=HERE/name;assert path.is_file();entries.append((sha(path),name))
for relative,expected in sorted(d['pins'].items()):path=ROOT/relative;assert path.is_file() and sha(path)==expected;entries.append((expected,os.path.relpath(path,HERE)))
assert len(entries)==17
tmp=HERE/'MANIFEST.sha256.tmp';tmp.write_text(''.join(f'{digest}  {name}\n' for digest,name in entries));os.replace(tmp,HERE/'MANIFEST.sha256');print(json.dumps({'status':'SEALED_HELD_ZERO_RUN','lines':17,'manifest_sha256':sha(HERE/'MANIFEST.sha256')},sort_keys=True))
