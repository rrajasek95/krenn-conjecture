#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((H/'results_referee.json').read_text());b=json.loads((H/'results_binding.json').read_text());a=json.loads((H/'HELD_ACCEPTANCE_V2.json').read_text())
assert r['schema']=='KRENN_X5_REP1_GROUPS88_137_SATISFIED_DEPENDENCY_BINDING_REFEREE_V2' and r['status']=='PASS_INDEPENDENT_HELD_LAUNCH_READY_ZERO_RUNS_NO_CLEARANCE'
assert r['closed_union']==list(range(88)) and r['selected_group_ids']==list(range(88,138)) and r['source_preservation']['source_count']==50 and r['source_preservation']['source_bytes']==89221428
assert b['status']=='PASS_HELD_LAUNCH_READY_ZERO_RUNS_NO_CLEARANCE' and a['status']=='PASS_HELD_LAUNCH_READY_DEPENDENCY_SATISFIED_NO_CLEARANCE'
assert r['scope']=={'held_launch_ready_metadata':True,'runner_acceptance_materialized':False,'launch_clearance_materialized':False,'solver_runs':0,'new_arithmetic':False,'groups_newly_closed':0,'mathematical_coverage_added':False}
m=H/'FINAL_MANIFEST.sha256'
if m.exists():
 for line in m.read_text().splitlines():
  if not line.strip():continue
  e,n=line.split(None,1);p=(m.parent/n.strip()).resolve();assert p.is_file() and sha(p)==e,p
print(json.dumps({'status':'PASS','union':88,'sources':50,'runs':0},sort_keys=True))
