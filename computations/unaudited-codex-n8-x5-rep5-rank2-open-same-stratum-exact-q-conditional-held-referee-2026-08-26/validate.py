#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest(); r=json.loads((H/'results_referee.json').read_text())
assert r['status']=='PASS_HELD_ONLY_BLOCKED_ON_FUTURE_MODULAR_UNIT' and r['q_source_sha256']=='1e2f72c9b4fda5e87fbec18469a6378cc7430f7b06676bd69db215055d8b1c7e'
assert r['source_identity_to_v2_design'] is True and (r['variables'],r['generators'],r['pivot_k'],r['t_open'])==(84,6562,2,1)
assert r['dependency']=={'future_hashes_null':4,'future_paths_null':4,'binding_absent':True,'required_modular_source_sha256':'fd182135d5da6eda87e284a4f38f147fbf13bef14016c1ee300bb9bde6713c5a'}
assert r['provenance']['consumed_k0_reused'] is False and r['provenance']['modular_referee_v2_replayed'] is True
assert r['hostiles_passed']==18 and len(r['hostile_tests'])==18 and all(r['hostile_tests'].values())
assert r['scope']=={'held_approval_only':True,'exact_Q_authorized':False,'launch_authorized':False,'mathematical_coverage':False,'rep5_closed':False,'solver_runs':0,'relaunch_authorized':False}
m=H/'FINAL_MANIFEST.sha256'; n=0
if m.exists():
 for line in m.read_text().splitlines():
  d,p=line.split(None,1); q=(H/p.strip()).resolve(); assert q.is_file() and sha(q)==d; n+=1
assert not list(H.glob('*.tmp'))
print(json.dumps({'status':'PASS_HELD_ONLY_VALIDATED','manifest_lines_checked':n,'solver_runs':0},sort_keys=True))
