#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((H/'results_referee.json').read_text());assert r['status']=='PASS_APPROVED_HELD_ZERO_RUN' and r['held_manifest_sha256']=='eefb9e1045f63f945fa62cc83119f171128575eb29d5a1d41b1aabf2e6a374c2' and r['exact_Q_sha256']=='43beb317cb0bc59b24f1d4c5613ef6baccd7ec064651e004c1f8eb4657d538fc' and r['modular_source_sha256']=='d7e57a3d43fb1280381660be2fea9c966eb086bd2aced3189b0f599030f5822b' and (r['variables'],r['generators'],r['attempts'],r['solver_runs'])==(62,6568,0,0) and r['mathematical_coverage'] is r['group16_closed'] is r['rep2_closed'] is False
for line in (H/'MANIFEST.sha256').read_text().splitlines():d,n=line.split(None,1);p=H/n.strip();assert p.is_file() and sha(p)==d
print('PASS_APPROVED_HELD_ZERO_RUN')
