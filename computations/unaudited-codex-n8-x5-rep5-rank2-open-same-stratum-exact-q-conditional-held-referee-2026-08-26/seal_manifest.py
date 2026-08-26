#!/usr/bin/env python3
import hashlib,json,os
from pathlib import Path
H=Path(__file__).resolve().parent; ROOT=H.parents[1]; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest(); r=json.loads((H/'results_referee.json').read_text())
local=['REPORT.md','referee.py','results_referee.json','seal_manifest.py','validate.py']; external=[('computations/unaudited-codex-n8-x5-rep5-rank2-open-same-stratum-exact-q-conditional-held-2026-08-26/MANIFEST.sha256',r['producer_manifest_sha256']),('computations/unaudited-codex-n8-x5-rep5-rank2-open-same-stratum-exact-q-conditional-held-2026-08-26/rep5_rank2_k2_t1_Q.sing',r['q_source_sha256'])]
entries=[(sha(H/x),x) for x in local]
for rel,d in external: assert sha(ROOT/rel)==d; entries.append((d,os.path.relpath(ROOT/rel,H)))
t=H/'FINAL_MANIFEST.sha256.tmp'; t.write_text(''.join(f'{d}  {p}\n' for d,p in entries)); os.replace(t,H/'FINAL_MANIFEST.sha256')
print(json.dumps({'status':'SEALED_HELD_ONLY','lines':len(entries),'manifest_sha256':sha(H/'FINAL_MANIFEST.sha256')},sort_keys=True))
