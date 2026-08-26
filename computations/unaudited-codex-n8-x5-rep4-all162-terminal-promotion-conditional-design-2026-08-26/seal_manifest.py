#!/usr/bin/env python3
"""Seal only the promotion package and explicit authoritative inputs."""
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
local=['REPORT.md','build_acceptance_schema.py','build_future_dependencies.py','build_promotion_design.py','future_dependencies.json','results_hostile_tests.json','results_terminal_promotion_design.json','seal_manifest.py','terminal_promotion_acceptance.schema.json','test_promotion_contract.py','validate.py'];design=json.loads((HERE/'results_terminal_promotion_design.json').read_text());entries=[]
for name in local:path=HERE/name;assert path.is_file();entries.append((sha(path),name))
for rel,want in sorted(design['pins'].items()):path=ROOT/rel;assert path.is_file() and sha(path)==want;entries.append((want,os.path.relpath(path,HERE)))
assert len(local)==11 and len(design['pins'])==21 and len(entries)==32;tmp=HERE/'MANIFEST.sha256.tmp';tmp.write_text(''.join(f'{digest}  {name}\n' for digest,name in entries));os.replace(tmp,HERE/'MANIFEST.sha256');print(json.dumps({'status':'SEALED_EXPLICIT_REP4_SCOPE_ZERO_RUN','local':11,'external':21,'lines':32,'manifest_sha256':sha(HERE/'MANIFEST.sha256')},sort_keys=True))
