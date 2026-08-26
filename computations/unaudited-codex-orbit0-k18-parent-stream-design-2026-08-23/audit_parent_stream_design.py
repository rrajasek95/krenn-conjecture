#!/usr/bin/env python3
"""Exact four-stream design for the scalar-only K18 parents feeding K20."""
from hashlib import sha256
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
K18=ROOT/'computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/results_k18_charge.json'
COMP=ROOT/'computations/unaudited-codex-orbit0-hidden-k16-k18-complete-charge-2026-08-23/results_complete_k18_charge.json'
K16=ROOT/'computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/results_filtered_k16_run.json'
DAG=ROOT/'computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json'
ARITH=ROOT/'computations/unaudited-codex-orbit0-k19-k24-arithmetic-plan-2026-08-23/results_k19_k24_arithmetic.json'
PREFIX=HERE/'results_parent_stream_prefix.json';SOURCE=HERE/'prefix_k18_parent_streams.rs';OUT=HERE/'results_parent_stream_design.json'
U=400_591_699_200

def req(x,d):
 if not x:raise AssertionError(d)
def sha(p):return sha256(p.read_bytes()).hexdigest()

def main():
 k18=json.loads(K18.read_text());comp=json.loads(COMP.read_text());k16=json.loads(K16.read_text());dag=json.loads(DAG.read_text());arith=json.loads(ARITH.read_text());pre=json.loads(PREFIX.read_text())
 req(pre['status']=='PASS_BOUNDED_FOUR_K18_PARENT_STREAM_PREFIXES',pre)
 mapping=comp['dag_coverage']['component_to_lineages'];required=set(dag['required_reachable_lineage_ids_by_degree']['20'])
 specs={
  'direct_K18':{'old':'direct','parents':'485 R8prime H-records; factor tails (2,4,4) and (3,3,4)','paths':[x.replace('|R:direct','|R:2') for x in mapping['direct_K18']], 'parent_weight':'w18=-rho*U','outgoing_weight':'w20=+rho*U/m2','m1':'1'},
  'K14_K4':{'old':'K14_K4','parents':'485 R8prime H-records; 12^3 K14 heads; frozen valid-pivot policy; 60 K4 tails','paths':[x+'-2' for x in mapping['K14_K4']], 'parent_weight':'w18=+rho*U/m1','outgoing_weight':'w20=-rho*U/(m1*m2)','m1':'|valid25(s14)|'},
  'K15_K3':{'old':'K15_K3','parents':'485 R8prime H-records; three (2,2,3) packets; all dividing pivots; 32 K3 tails','paths':[x+'-2' for x in mapping['K15_K3']], 'parent_weight':'w18=+rho*U/m1','outgoing_weight':'w20=-rho*U/(m1*m2)','m1':'|avail(s15)|'},
  'K16_K2':{'old':'K16_K2','parents':'checkpoint_direct_k16.bin only; all dividing pivots; 12 K2 tails. Frozen K14 response is disjoint and nonpivotable; hidden [2,2,2] is already separate.','paths':[x+'-2' for x in mapping['K16_K2']], 'parent_weight':'w18=-v16*U/m1','outgoing_weight':'w20=+v16*U/(m1*m2)','m1':'|avail(s16)|'},
 }
 req(sum(len(x['paths']) for x in specs.values())==16,'path count')
 req(all(set(x['paths'])<=required for x in specs.values()),specs)
 req(k16['K16_checkpoint']['direct_frozen_support_overlap']==0 and k16['K16_checkpoint']['removed_pivotable'][0]==24_003_767,k16['K16_checkpoint'])
 exact_first={'direct_K18':{'source_heads':152_251_200,'first_pivot_uses':0},'K14_K4':{'source_heads':838_080,'first_pivot_uses':6_619_280},'K15_K3':{'source_heads':6_704_640,'first_pivot_uses':55_934_080},'K16_K2':{'source_heads':24_003_767,'first_pivot_uses':129_939_187}}
 for name,s in specs.items():
  c=k18['components'][s['old']];full=c['full_compact_occurrences'];irr=c['K18_irreducible_occurrences'];piv=full-irr
  s.update(exact_first[name]);s['K18_parent_occurrences']=full;s['K18_pivotable_parent_occurrences']=piv;s['K18_irreducible_parent_occurrences']=irr
  s['hard_outgoing_pivot_use_bounds']=[piv,78*piv];s['hard_K2_tail_upper']=12*78*piv
  q=pre['components'][name];avg=q['outgoing_pivot_uses']/q['pivotable_parents'];s['prefix']={**q,'average_m2':avg,'linear_projected_outgoing_uses':round(avg*piv),'linear_projected_K2_tails':12*round(avg*piv),'projection_guard':'biased bounded prefix; planning estimate only, not a census'}
 req(sum(s['K18_pivotable_parent_occurrences'] for s in specs.values())==2_226_151_778,'piv total')
 req(sum(s['hard_K2_tail_upper'] for s in specs.values())==2_083_678_064_208,'upper')
 triple=arith['hidden_higher_tail_guard']['K20_depth3_products'];req(len(triple)==142 and max(triple)==2240 and arith['hidden_higher_tail_guard']['K20_depth3_product_lcm']==U,'arith')
 plan={
  'partitioning':'Direct/K14/K15: disjoint contiguous slices of the 485 R8prime H-records. K16: disjoint first-cell or record-index ranges of checkpoint_direct_k16.bin.',
  'worker_output':'Periodic sorted runs of (component, profile29, signature12, p2, signed i128 w20, counts, smallest source witness); flush at a fixed key cap.',
  'merge':'Per-component external merge, exact-zero deletion, denominator/mass ledger; evaluate the 12 literal K2 tails once per nonzero enriched key.',
  'symmetry':'No H-orbit expansion or parent-row checkpoint. R8 orbit size is already in rho, and cycle charge plus next pivotability are H-invariant.',
  'guards':['K14 uses frozen valid25 policy; all other pivots use all dividing pivots','assert source numerator divisibility by m1 and parent numerator divisibility by m2 occurrencewise','use U, not old K18 charge scale 281801520','keep all four component ledgers separate until their charges and the 16 lineage labels replay','K16 consumes direct checkpoint only; do not double-count hidden K14 [2,2,2]'],
  'parallel_minimum':'8 workers per component, at most two components concurrently; direct then K14 are the cheapest validation gates, K15 and K16 follow only after exact prefix/merge replay.'}
 result={'status':'PASS_EXACT_FOUR_K18_PARENT_STREAM_DESIGN_WITH_BOUNDED_PREFIXES','scope':'Design/prefix only; no full parent reconstruction or K20 charge run.','scale':U,'covered_remaining_K20_paths':16,'components':specs,'totals':{'K18_pivotable_parent_occurrences':2_226_151_778,'hard_K2_tail_upper':2_083_678_064_208,'prefix_pivotable_parents':sum(x['pivotable_parents'] for x in pre['components'].values()),'prefix_elapsed_seconds':pre['elapsed_seconds']},'arithmetic':{'K20_triple_products':142,'max_product':2240,'lcm':U},'minimal_parallel_plan':plan,'pinned':{str(p.relative_to(ROOT)):sha(p) for p in(K18,COMP,K16,DAG,ARITH,PREFIX,SOURCE)}}
 logical=json.dumps(result,sort_keys=True,separators=(',',':')).encode();result['logical_sha256']=sha256(logical).hexdigest();OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'paths':16,'pivotable':result['totals']['K18_pivotable_parent_occurrences'],'upper':result['totals']['hard_K2_tail_upper'],'logical':result['logical_sha256']},indent=2))

if __name__=='__main__':main()
