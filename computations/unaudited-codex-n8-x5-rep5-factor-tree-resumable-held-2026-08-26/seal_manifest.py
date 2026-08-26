#!/usr/bin/env python3
import hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;P=H.parent/'unaudited-codex-n8-x5-rep5-smallest65-third-factor-reduction-design-2026-08-26';O=H.parent/'unaudited-codex-n8-x5-rep5-strict-zero-recursive-factor-tree-capped-2026-08-26';paths=[H/'factor_tree_driver.py',H/'run_held.py',H/'prove_invariants.py',H/'build_held.py',H/'validate_held.py',H/'seal_manifest.py',H/'REPORT.md',H/'HELD_PLAN.json',H/'CLEARANCE_TEMPLATE.json',H/'results_invariants.json',H/'results_hostiles.json',P/'MANIFEST.sha256',P/'sources/V_a24_10_Q_design.sing',O/'MANIFEST.sha256',O/'results_capped_outcome.json',O/'results_referee.json'];lines=[]
for p in paths:assert p.is_file();digest=hashlib.sha256(p.read_bytes()).hexdigest();rel=p.relative_to(H) if p.is_relative_to(H) else Path('..')/p.relative_to(H.parent);lines.append(f'{digest}  {rel}')
m=H/'MANIFEST.sha256';m.write_text('\n'.join(lines)+'\n')
for line in m.read_text().splitlines():digest,rel=line.split('  ',1);assert hashlib.sha256((H/rel).read_bytes()).hexdigest()==digest
print({'status':'SEALED_REP5_FACTOR_TREE_HELD_ZERO_RUN','lines':len(lines),'sha256':hashlib.sha256(m.read_bytes()).hexdigest()})
