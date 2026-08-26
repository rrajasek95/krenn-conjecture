#!/usr/bin/env python3
import hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;P=H.parent/'unaudited-codex-n8-x5-rep5-smallest65-third-factor-reduction-design-2026-08-26';N=H.parent/'unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-2026-08-25';R=H.parent/'unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-referee-2026-08-25';paths=[H/'build_outcome.py',H/'referee.py',H/'seal_manifest.py',H/'REPORT.md',H/'results_capped_outcome.json',H/'results_referee.json',H/'results_hostiles.json',P/'MANIFEST.sha256',P/'results_design.json',P/'results_referee.json',P/'sources/V_a24_10_Q_design.sing',N/'MANIFEST.sha256',N/'results_design_v2.json',R/'results_referee.json',R/'FINAL_MANIFEST.sha256'];lines=[]
for p in paths:assert p.is_file();digest=hashlib.sha256(p.read_bytes()).hexdigest();rel=p.relative_to(H) if p.is_relative_to(H) else Path('..')/p.relative_to(H.parent);lines.append(f'{digest}  {rel}')
m=H/'MANIFEST.sha256';m.write_text('\n'.join(lines)+'\n')
for line in m.read_text().splitlines():digest,rel=line.split('  ',1);assert hashlib.sha256((H/rel).read_bytes()).hexdigest()==digest
print({'status':'SEALED_CAPPED_FACTOR_TREE_OUTCOME','lines':len(lines),'sha256':hashlib.sha256(m.read_bytes()).hexdigest()})
