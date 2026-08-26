#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((H/'results_referee.json').read_text())
assert r['status']=='PASS_EXACT_TWO_CHART_RESIDUAL_ONE_TORUS_COVER_DESIGN_ONLY';assert r['grading']['rank_over_Q']==72 and r['grading']['nullity_over_Q']==1;assert r['coordinate_scoring']['selected']=='a37_20';assert len(r['cover_proof']['sources'])==2 and r['scope']['singular_runs']==0 and r['scope']['mathematical_coverage_added'] is False
n=0
if (H/'FINAL_MANIFEST.sha256').exists():
 for line in (H/'FINAL_MANIFEST.sha256').read_text().splitlines():
  digest,name=line.split(None,1);p=(H/name.strip()).resolve();assert p.is_file() and sha(p)==digest;n+=1
print(json.dumps({'status':'PASS_REFEREE_VALIDATED','manifest_lines_checked':n,'solves':0},sort_keys=True))
