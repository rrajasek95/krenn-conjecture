#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=json.loads((H/'results_binding.json').read_text());r=json.loads((H/'results_referee.json').read_text());d=json.loads((H/'normalized_dependency.json').read_text());a=json.loads((H/'independent_referee_acceptance.json').read_text())
assert b['status']=='PASS_HELD_LAUNCH_READY_ZERO_RUNS_NO_CLEARANCE' and r['status']=='PASS_INDEPENDENT_HELD_LAUNCH_READY_ZERO_RUNS_NO_CLEARANCE'
assert d['closed_union']==list(range(26)) and d['groups_closed_by_future']==list(range(1,26))
assert a['selected_group_ids']==list(range(26,76)) and a['required_closed_union']==list(range(26)) and a['normalized_dependency_sha256']==sha(H/'normalized_dependency.json')
assert b['scope']=={'held_launch_ready_metadata':True,'launch_clearance_materialized':False,'solver_runs':0,'new_arithmetic':False,'mathematical_coverage_added':False}
n=0
if (H/'FINAL_MANIFEST.sha256').exists():
 for line in (H/'FINAL_MANIFEST.sha256').read_text().splitlines():
  h,x=line.split(None,1);p=(H/x.strip()).resolve();assert p.is_file() and sha(p)==h;n+=1
print(json.dumps({'status':'PASS_BINDING_VALIDATED_ZERO_RUN','manifest_lines_checked':n},sort_keys=True))
