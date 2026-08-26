#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((H/'results_referee.json').read_text())
assert r['status']=='PASS_DESIGN_ONLY_GROUP0_SEALED_FUTURE_1_161_REQUIRED'
assert r['authoritative_contraction']=={'raw_charts':972,'canonical_groups':162,'members_per_group':6,'y_groups':81,'z_groups':81,'y_raw':486,'z_raw':486,'variables_each':91,'generators_each':6577,'forward_reverse_localization':True}
assert r['rank_zero_clause']['scope']==[0] and r['rank_zero_clause']['nonzero_rank_claims_used'] is False
assert r['sealed_group0']['group_id']==0 and r['sealed_group0']['independent_q_seals']==2 and r['sealed_group0']['unit_remainder']==0
assert r['future_hashes_absent']==r['future_artifacts_absent']==8 and r['prospective_union']['exact_union']==list(range(162))
assert len(r['hostile_tests'])==16 and all(r['hostile_tests'].values()) and r['producer_hostiles_passed']==16
assert r['scope']=={'design_only':True,'promotion_authorized':False,'rep4_only':True,'cross_representative_promotion':False,'other_representatives_closed':[],'full_conjecture':False,'solver_runs':0}
m=H/'FINAL_MANIFEST.sha256'; n=0
if m.exists():
 for line in m.read_text().splitlines():
  d,p=line.split(None,1); q=(H/p.strip()).resolve(); assert q.is_file() and sha(q)==d; n+=1
assert not list(H.glob('*.tmp'))
print(json.dumps({'status':'PASS_DESIGN_ONLY_VALIDATED','manifest_lines_checked':n,'future_hashes_absent':8,'solver_runs':0},sort_keys=True))
