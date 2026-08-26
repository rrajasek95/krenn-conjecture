#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((H/'results_referee.json').read_text())
assert r['schema']=='KRENN_X5_REP1_ALL162_TERMINAL_PROMOTION_CONDITIONAL_DESIGN_REFEREE_V1' and r['status']=='PASS_DESIGN_ONLY_CURRENT_0_87_SEALED_FUTURE_88_161_REQUIRED'
assert r['producer_manifest_sha256']=='df566e74f8048648605ab54b2ced3a513c6ff107310fca599384c2702df159d4' and r['producer_result_sha256']=='5ea7e89aab44a62e8a89d4ebc41bdaeb9826098be420dc1f3ed14ab4b2cba2a2'
assert r['authoritative_contraction']=={'raw_charts':972,'canonical_groups':162,'members_per_group':6,'y_groups':81,'z_groups':81,'y_raw':486,'z_raw':486,'two_minor_cover':True,'forward_reverse_localization':True}
assert r['rank_zero_clause']['scope']==[0] and not r['rank_zero_clause']['nonzero_rank_claims_used']
assert r['current_exact_seals']['closed_group_ids']==list(range(88))
assert r['future_slots']['groups88_137']['manifest_sha256'] is r['future_slots']['groups88_137']['result_sha256'] is None
assert r['future_slots']['groups138_161']['manifest_sha256'] is r['future_slots']['groups138_161']['result_sha256'] is None
assert r['prospective_union']['exact_union']==list(range(162)) and not r['prospective_union']['duplicates'] and not r['prospective_union']['missing']
assert len(r['hostile_tests'])==12 and all(r['hostile_tests'].values())
assert r['scope']=={'design_only':True,'promotion_authorized':False,'rep1_only':True,'cross_representative_promotion':False,'other_representatives_closed':[],'full_conjecture':False,'solver_runs':0}
m=H/'FINAL_MANIFEST.sha256'
if m.exists():
 for line in m.read_text().splitlines():
  if not line.strip():continue
  e,n=line.split(None,1);p=(m.parent/n.strip()).resolve();assert p.is_file() and sha(p)==e,p
print(json.dumps({'status':'PASS','current_closed':88,'future':74,'runs':0},sort_keys=True))
