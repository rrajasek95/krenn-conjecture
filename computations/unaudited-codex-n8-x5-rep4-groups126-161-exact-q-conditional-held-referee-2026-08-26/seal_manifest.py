#!/usr/bin/env python3
import hashlib,json,os
from pathlib import Path
H=Path(__file__).resolve().parent; ROOT=H.parents[1]; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
local=['HELD_APPROVAL.json','REPORT.md','referee.py','results_referee.json','seal_manifest.py','validate.py']; r=json.loads((H/'results_referee.json').read_text())
external=[
('computations/unaudited-codex-n8-x5-rep4-groups126-161-exact-q-conditional-held-2026-08-26/MANIFEST.sha256',r['producer_manifest_sha256']),
('computations/unaudited-codex-n8-x5-rep4-groups126-161-exact-q-conditional-held-2026-08-26/source_ledger.json',r['source_ledger_sha256']),
('computations/unaudited-codex-n8-x5-rep4-groups126-161-exact-q-conditional-held-2026-08-26/future_dependencies.json',r['future_dependencies_sha256']),
('computations/unaudited-codex-n8-x5-rep4-groups126-161-exact-q-conditional-held-2026-08-26/dependency_verifier.py',r['dependency_verifier_sha256']),
('computations/unaudited-codex-n8-x5-rep4-groups126-161-exact-q-conditional-held-2026-08-26/run_groups126_161.py',r['runner_sha256']),
('computations/unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26/canonical_census.json',r['authoritative_census_sha256'])]
entries=[(sha(H/x),x) for x in local]
for rel,d in external: assert sha(ROOT/rel)==d; entries.append((d,os.path.relpath(ROOT/rel,H)))
t=H/'FINAL_MANIFEST.sha256.tmp'; t.write_text(''.join(f'{d}  {p}\n' for d,p in entries)); os.replace(t,H/'FINAL_MANIFEST.sha256')
print(json.dumps({'status':'SEALED_HELD_ONLY','lines':len(entries),'manifest_sha256':sha(H/'FINAL_MANIFEST.sha256')},sort_keys=True))
