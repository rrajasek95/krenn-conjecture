#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent; ROOT=H.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((H/'results_referee.json').read_text()); a=json.loads((H/'HELD_APPROVAL.json').read_text())
assert r['status']=='PASS_CONDITIONAL_HELD_GROUPS126_161_BLOCKED_ZERO_RUNS' and r['selected_group_ids']==list(range(126,162))
assert r['canonical_sources_verified']==36 and r['variables_each']==91 and r['generators_each']==6577 and r['hostiles_passed']==21
assert r['dependency_satisfied'] is r['future_files_present'] is False and r['future_hashes']==[None]*6
assert r['scope']=={'held_approval_only':True,'launch_authorized':False,'solver_runs':0,'mathematical_coverage':False,'rep4_closed':False}
assert a['status']=='PASS_HELD_ONLY_BLOCKED_ON_ALL_THREE_EXACT_TERMINAL_BINDINGS' and a['future_terminal_hashes']==[None]*6 and a['launch_authorized'] is False
for forbidden in ('launch_clearance.json','independent_referee_acceptance.json','normalized_dependencies.json','BATCH_ATTEMPT.json','batch_result.json'): assert not (H.parent/forbidden).exists()
assert not list(H.glob('*.tmp'))
m=H/'FINAL_MANIFEST.sha256'; n=0
if m.exists():
 for line in m.read_text().splitlines():
  d,p=line.split(None,1); q=(H/p.strip()).resolve(); assert q.is_file() and sha(q)==d; n+=1
print(json.dumps({'status':'PASS_HELD_ONLY_VALIDATED','sources':36,'hostiles':21,'manifest_lines_checked':n,'solver_runs':0},sort_keys=True))
