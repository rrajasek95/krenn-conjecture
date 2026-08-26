#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((H/'results_referee.json').read_text())
assert r['schema']=='KRENN_X5_REP1_GROUPS38_87_EXACT_Q_TERMINAL_REFEREE_V1' and r['status']=='PASS_ALL_50_EXACT_Q_UNIT_IDEALS'
assert r['new_groups_closed']==50 and r['strict_order'] and not r['parallel'] and not r['skipped'] and not r['relaunch']
assert r['baseline_closed_union']==list(range(38)) and r['groups_closed']==list(range(38,88)) and r['closed_union']==list(range(88))
assert r['normalization_only'] and r['scope']=={'solver_runs':0,'new_arithmetic':False,'groups_newly_closed_by_binding':0}
m=H/'FINAL_MANIFEST.sha256'
if m.exists():
 for line in m.read_text().splitlines():
  if not line.strip():continue
  e,n=line.split(None,1);p=(m.parent/n.strip()).resolve();assert p.is_file() and sha(p)==e,p
print(json.dumps({'status':'PASS','groups':50,'runs':0},sort_keys=True))
