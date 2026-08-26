#!/usr/bin/env python3
"""Seal the referee and its explicit producer/rejection pins."""
import hashlib, json, os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
result=json.loads((HERE/'results_referee.json').read_text())
entries=[]
for name in ('REPORT.md','referee.py','results_referee.json','seal_manifest.py'):
 path=HERE/name;assert path.is_file();entries.append((sha(path),name))
for relative,expected in sorted(result['pins'].items()):
 path=ROOT/relative;assert path.is_file() and sha(path)==expected;entries.append((expected,os.path.relpath(path,HERE)))
assert len(entries)==18
tmp=HERE/'FINAL_MANIFEST.sha256.tmp';tmp.write_text(''.join(f'{digest}  {name}\n' for digest,name in entries));os.replace(tmp,HERE/'FINAL_MANIFEST.sha256')
print(json.dumps({'status':'SEALED_REFEREE','lines':18,'manifest_sha256':sha(HERE/'FINAL_MANIFEST.sha256')},sort_keys=True))
