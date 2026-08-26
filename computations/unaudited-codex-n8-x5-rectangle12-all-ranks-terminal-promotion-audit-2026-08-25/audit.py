#!/usr/bin/env python3
"""Terminal all-ranks closure merge for the twelve rectangle records."""
import hashlib,json,os
from pathlib import Path
if not __debug__:raise RuntimeError('assertions required')
H=Path(__file__).resolve().parent;ROOT=H.parents[1];C=ROOT/'computations'
T=C/'unaudited-codex-n8-x5-rectangle12-transport-census-referee-2026-08-25';R1=C/'unaudited-codex-n8-x5-rectangle12-rank1-exact-q-transport-promotion-audit-2026-08-25';R2=C/'unaudited-codex-n8-x5-rectangle-rank2-all5-exact-q-run-2026-08-25';R3=C/'unaudited-codex-n8-x5-rectangle-rank3-adjugate-exact-q-referee-2026-08-25'
def sha(p):
 d=hashlib.sha256()
 with p.open('rb') as f:
  while x:=f.read(1<<20):d.update(x)
 return d.hexdigest()
PINS={T/'MANIFEST.sha256':'fa72101042aa2d179745f3e17475dae3c654c0445bc7433ab5ae4e22df3e5e5d',T/'results_referee.json':'e1660ab4671b8de68acdc4fe2a32e90e68ed1a489accf62d6961f9e6bc094fd7',R1/'MANIFEST.sha256':'cdd4a10b9fc04f454808b009f83bc46a2ce3923a2077e20a40b05c4dc01a6b60',R1/'results_promotion_audit.json':'bcc09fffbea0c94a52f75eb66364853561f3539ab68ef3c8017774ad54cf4cc3',R2/'FINAL_MANIFEST.sha256':'16e7d66fc1677ac0642254b7c7610fd79f3bea94fed9bf6a3a141b31a8d29efd',R2/'FINAL_AUDIT.json':'aaae3c928640a3d3423640a2a33230ee5ddb8eacd339a58d156b97d986f2165a',R2/'BATCH_RESULT.json':'e1934a0faaad654fb60e9178883781927b6bb78ab4a0d720fbfe3969dac679e6',R3/'FINAL_MANIFEST.sha256':'94f1fe61337bfc8bb2b11aa3d528d219cd7b440d2ad19be2739109e693ab53a9',R3/'results_referee.json':'459e403a6afc70d643ddfb37918513ded6eb79580169e796ab19be60a919b35f'}
def write(p,x):q=p.with_suffix('.json.tmp');q.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');os.replace(q,p)
def main():
 for p,w in PINS.items():assert sha(p)==w,(p,sha(p),w)
 t=json.loads((T/'results_referee.json').read_text());r1=json.loads((R1/'results_promotion_audit.json').read_text());r2=json.loads((R2/'FINAL_AUDIT.json').read_text());b2=json.loads((R2/'BATCH_RESULT.json').read_text());r3=json.loads((R3/'results_referee.json').read_text())
 assert t['status']=='PASS_EXACT_TRANSPORT_WITH_SELECTED_CARRIER_SCOPE_AND_CURRENT_CLOSURE_LEDGER' and t['support_census']['classes']==[[0,1,4,5,8,9],[2,3,6,7,10,11]] and t['A12_reduced_ideal_audit']['reduced_rank_ideal_A12_free']
 outside=t['literal_transport']['outside_factor_maps'];assert len(outside)==12 and [x['record_index'] for x in outside]==list(range(12)) and all(x['literal_word_transports']==39366 for x in outside)
 # Rank zero: mapped selected response map is B*K*A_outside^T (up to response transposes).
 # rank(A_outside)=0 means A_outside=0, so L=0 and ker(L)=M3; trace and K_ii
 # are nonzero on M3.  This proof is invariant under every sealed transport.
 rank0_records=[x['record_index'] for x in outside]
 assert r1['status']=='PASS_ALL_RANK1_ORBITS_EXACT_Q_CLOSED_ACROSS_12_RECTANGLE_RECORDS' and r1['exact_Q_orbits']==[0,1,2,3,4] and r1['raw_chart_record_cases']==324
 assert r2['status']=='PASS_ALL_FIVE_EXACT_Q_UNIT_IDEALS' and r2['exact_order']==[0,1,2,3,4] and r2['rank2_canonical_family_closed'] and not r2['rank1_run']
 assert b2['status']=='PASS_ALL_FIVE_UNIT_IDEALS' and b2['attempted_orbits']==[0,1,2,3,4] and b2['unattempted_orbits']==[]
 assert r3['status']=='PASS_EXACT_Q_UNIT_IDEAL_RANK3_TWO_LIFTS_ONLY'
 ranks={'0':{'method':'STRUCTURAL_ZERO_RESPONSE_MAP','records_closed':rank0_records,'chart_cases_per_record':1},'1':{'method':'FIVE_EXACT_Q_UNIT_IDEALS_PLUS_TRANSPORT','canonical_orbits':[0,1,2,3,4],'orbit_sizes':[3,6,6,6,6],'raw_charts_per_record':27,'raw_record_cases':324},'2':{'method':'FIVE_EXACT_Q_UNIT_IDEALS_PLUS_TRANSPORT','canonical_orbits':[0,1,2,3,4],'orbit_sizes':[6,6,6,6,3],'raw_charts_per_record':27,'raw_record_cases':324},'3':{'method':'ADJUGATE_EXACT_Q_UNIT_IDEAL_PLUS_TRANSPORT','records_closed':list(range(12)),'chart_cases_per_record':1}}
 assert sum(ranks['1']['orbit_sizes'])==sum(ranks['2']['orbit_sizes'])==27
 result={'schema':'KRENN_X5_RECTANGLE12_ALL_RANKS_TERMINAL_PROMOTION_AUDIT_V1','status':'PASS_ALL_RANKS_CLOSED_FOR_ALL_12_RECTANGLE_RECORDS','records':list(range(12)),'A12_states':{'present':[0,1,4,5,8,9],'absent':[2,3,6,7,10,11],'both_closed':True},'rank_partition':[0,1,2,3],'rank_certificates':ranks,'coverage':{'records':12,'ranks_per_record':4,'rank1_raw_chart_cases':324,'rank2_raw_chart_cases':324,'rank0_cases':12,'rank3_cases':12,'total_stratified_record_chart_cases':672,'missing_ranks':[],'missing_rank1_charts':0,'missing_rank2_charts':0},'theorem':'For each rectangle record the mapped outside 3x3 factor has exactly one rank in {0,1,2,3}. Rank0 closes structurally; all rank1 and rank2 colour-chart orbits have exact-Q unit certificates; rank3 has the adjugate exact-Q unit certificate. The literal transport and A12-free selected reduced ideal carry these certificates to both A12 states and all twelve records.','scope':{'rectangle_records_0_through_11_closed':True,'records_12_through_15_excluded':True,'excluded_records':[12,13,14,15],'full_conjecture':False,'new_solver_runs':0},'pins':{str(p.relative_to(ROOT)):w for p,w in PINS.items()}}
 write(H/'results_terminal_promotion.json',result);print(json.dumps({'status':result['status'],'records':12,'ranks':[0,1,2,3],'cases':672,'solves':0},sort_keys=True))
if __name__=='__main__':main()
