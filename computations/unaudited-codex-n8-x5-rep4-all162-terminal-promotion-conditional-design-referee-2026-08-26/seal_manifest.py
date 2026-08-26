#!/usr/bin/env python3
import hashlib,json,os
from pathlib import Path
H=Path(__file__).resolve().parent; ROOT=H.parents[1]; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
local=['REPORT.md','referee.py','results_referee.json','seal_manifest.py','validate.py']; r=json.loads((H/'results_referee.json').read_text())
external=[
 ('computations/unaudited-codex-n8-x5-rep4-all162-terminal-promotion-conditional-design-2026-08-26/MANIFEST.sha256',r['producer_manifest_sha256']),
 ('computations/unaudited-codex-n8-x5-rep4-all162-terminal-promotion-conditional-design-2026-08-26/results_terminal_promotion_design.json',r['producer_result_sha256'])]
entries=[(sha(H/x),x) for x in local]
for rel,d in external: assert sha(ROOT/rel)==d; entries.append((d,os.path.relpath(ROOT/rel,H)))
t=H/'FINAL_MANIFEST.sha256.tmp'; t.write_text(''.join(f'{d}  {p}\n' for d,p in entries)); os.replace(t,H/'FINAL_MANIFEST.sha256')
print(json.dumps({'status':'SEALED_DESIGN_ONLY','lines':len(entries),'manifest_sha256':sha(H/'FINAL_MANIFEST.sha256')},sort_keys=True))
