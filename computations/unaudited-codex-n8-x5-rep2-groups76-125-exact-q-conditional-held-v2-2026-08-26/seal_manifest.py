#!/usr/bin/env python3
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PROD=ROOT/'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
local=['REPORT.md','build_plan.py','build_runner.py','dependency_verifier.py','held_schedule_v2.json','independent_referee_acceptance_v2.schema.json','launch_clearance_v2.schema.json','normalize_dependencies_v2.py','results_hostile_tests_v2.json','run_groups76_125_v2.py','seal_manifest.py','source_reference_ledger.json','test_v2.py','validate.py'];refs=json.loads((HERE/'source_reference_ledger.json').read_text());external={
 'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26/MANIFEST.sha256':'43c34a80cc55488e4840b5d04001211d21f8acbdc6fc62bc5cc5e0e366fc5b0a',
 'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26/source_ledger.json':'4aa023638d439fd1250b66593d93dd29dd4472831449ff571e2730bf6950b4ce',
 'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26/future_dependencies.json':'5173f8f03b8eb7feff428573cb6a0b2813ef1e6cb1d4c4696543c30585e522e4',
 'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26/normalize_dependencies.py':'887762ea499c3dbf8b566987fe1ba234f518e72ba9733f6b96accd4435dee1fb',
 'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26/run_groups76_125.py':'c1aa9303186a1a1e1efaa867471192b69b746aac52741ad227d901db34cbe24a',
 'computations/unaudited-codex-n8-x5-rep2-groups76-125-conditional-independent-referee-2026-08-26/FINAL_MANIFEST.sha256':'58910fda9efb0c9157822910ac5e641cd770cf69fe458f34bdd1a66537cd0c47',
 'computations/unaudited-codex-n8-x5-rep2-groups76-125-conditional-independent-referee-2026-08-26/results_independent_referee.json':'09109d866f5c4241bc8fbbde961dcc6f504f9d1dc09cc449bcfced7f14e0f08f',
 'computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25/canonical_census.json':'5ee661f3fdfd0e35e75d92d6efe7700b83011049e1d74a712ba8918681f86c8a',
 'computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25/generate_design.py':'ca23dbcb4179753393b7b0b3cd81d5c73d2c1bd26da559b00ca5136524aa83dc'}
for record in refs['sources']:external[record['path']]=record['sha256']
entries=[]
for name in local:path=HERE/name;assert path.is_file();entries.append((sha(path),name))
for rel,want in sorted(external.items()):path=ROOT/rel;assert path.is_file() and sha(path)==want;entries.append((want,os.path.relpath(path,HERE)))
assert len(local)==14 and len(external)==59 and len(entries)==73;tmp=HERE/'MANIFEST.sha256.tmp';tmp.write_text(''.join(f'{digest}  {name}\n' for digest,name in entries));os.replace(tmp,HERE/'MANIFEST.sha256');print(json.dumps({'status':'SEALED_V2_HELD_ZERO_RUN','lines':73,'manifest_sha256':sha(HERE/'MANIFEST.sha256')},sort_keys=True))
