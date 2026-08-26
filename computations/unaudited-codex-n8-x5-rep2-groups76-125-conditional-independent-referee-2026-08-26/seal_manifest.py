#!/usr/bin/env python3
import hashlib,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
local=['REPORT.md','audit.py','fabricated_stale_normalized_countermodel.json','results_independent_referee.json','seal_manifest.py']
pins={
 'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26/MANIFEST.sha256':'43c34a80cc55488e4840b5d04001211d21f8acbdc6fc62bc5cc5e0e366fc5b0a',
 'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26/source_ledger.json':'4aa023638d439fd1250b66593d93dd29dd4472831449ff571e2730bf6950b4ce',
 'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26/future_dependencies.json':'5173f8f03b8eb7feff428573cb6a0b2813ef1e6cb1d4c4696543c30585e522e4',
 'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26/normalize_dependencies.py':'887762ea499c3dbf8b566987fe1ba234f518e72ba9733f6b96accd4435dee1fb',
 'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26/results_hostile_tests.json':'daffe98d8d0b993cd2c77166d5fc50829247317b187415825202b94516de2789',
 'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26/run_groups76_125.py':'c1aa9303186a1a1e1efaa867471192b69b746aac52741ad227d901db34cbe24a',
 'computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25/canonical_census.json':'5ee661f3fdfd0e35e75d92d6efe7700b83011049e1d74a712ba8918681f86c8a',
 'computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25/generate_design.py':'ca23dbcb4179753393b7b0b3cd81d5c73d2c1bd26da559b00ca5136524aa83dc'}
entries=[]
for name in local:path=HERE/name;assert path.is_file();entries.append((sha(path),name))
for rel,want in sorted(pins.items()):path=ROOT/rel;assert path.is_file() and sha(path)==want;entries.append((want,os.path.relpath(path,HERE)))
assert len(entries)==13;tmp=HERE/'FINAL_MANIFEST.sha256.tmp';tmp.write_text(''.join(f'{digest}  {name}\n' for digest,name in entries));os.replace(tmp,HERE/'FINAL_MANIFEST.sha256');print(sha(HERE/'FINAL_MANIFEST.sha256'))
