#!/usr/bin/env python3
import hashlib,json,os
from pathlib import Path
H=Path(__file__).resolve().parent; ROOT=H.parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((H/'results_design.json').read_text())
local=['REPORT.md','build_design.py','results_design.json','results_hostiles.json','seal_manifest.py','test_design.py','validate.py']+[s['path'] for s in r['decomposition']['sources']];entries=[(sha(H/x),x) for x in local]
for rel,d in sorted(r['pins'].items()):assert sha(ROOT/rel)==d;entries.append((d,os.path.relpath(ROOT/rel,H)))
t=H/'MANIFEST.sha256.tmp';t.write_text(''.join(f'{d}  {p}\n' for d,p in entries));os.replace(t,H/'MANIFEST.sha256');print(json.dumps({'status':'SEALED_EXACT_DESIGN_ZERO_RUN','lines':len(entries),'manifest_sha256':sha(H/'MANIFEST.sha256')},sort_keys=True))
