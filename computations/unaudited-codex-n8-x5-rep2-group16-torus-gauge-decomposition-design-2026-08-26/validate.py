#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent; ROOT=H.parents[1]; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((H/'results_design.json').read_text()); h=json.loads((H/'results_hostiles.json').read_text())
assert r['status']=='PASS_EXACT_19_STRATUM_DESIGN_ZERO_SOLVES' and r['decomposition']['stratum_count']==19 and r['decomposition']['variable_histogram']=={'70':1,'78':9,'87':9}
assert r['consumed_attempt']['status']=='FAIL_CLOSED_RESOURCE' and r['consumed_attempt']['termination']=='NATIVE_WALL_CAP_240' and r['consumed_attempt']['relaunch_authorized'] is False
assert r['torus']['unit_gauge_determinant']==1 and r['symmetry_obstruction']['transport_to_closed_group_found'] is False
assert h['status']=='PASS_14_HOSTILES_ZERO_RUN' and h['hostile_count']==14 and all(h['hostile_tests'].values()) and h['design_sha256']==sha(H/'results_design.json')
for s in r['decomposition']['sources']:
 p=H/s['path']; assert p.is_file() and sha(p)==s['sha256'] and p.stat().st_size==s['bytes']
for rel,d in r['pins'].items(): assert (ROOT/rel).is_file() and sha(ROOT/rel)==d
assert not list(H.rglob('*.tmp')) and not list(H.rglob('__pycache__')) and not list(H.glob('result.json'))
m=H/'MANIFEST.sha256';n=0
if m.exists():
 for line in m.read_text().splitlines():
  d,p=line.split(None,1);q=(H/p.strip()).resolve();assert q.is_file() and sha(q)==d;n+=1
print(json.dumps({'status':'PASS_DESIGN_VALIDATED_ZERO_RUN','strata':19,'manifest_lines_checked':n,'solver_runs':0},sort_keys=True))
