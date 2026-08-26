#!/usr/bin/env python3
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((HERE/'results_referee.json').read_text());local=['REPORT.md','independent_referee_acceptance.json','referee.py','results_referee.json','seal_manifest.py'];e=[]
for n in local:p=HERE/n;assert p.is_file();e.append((sha(p),n))
for rel,h in sorted(r['pins'].items()):p=ROOT/rel;assert p.is_file() and sha(p)==h;e.append((h,os.path.relpath(p,HERE)))
assert len(e)==17;t=HERE/'FINAL_MANIFEST.sha256.tmp';t.write_text(''.join(f'{h}  {n}\n' for h,n in e));os.replace(t,HERE/'FINAL_MANIFEST.sha256');print(json.dumps({'status':'SEALED_HELD_APPROVAL_ONLY','lines':17,'manifest_sha256':sha(HERE/'FINAL_MANIFEST.sha256')},sort_keys=True))
