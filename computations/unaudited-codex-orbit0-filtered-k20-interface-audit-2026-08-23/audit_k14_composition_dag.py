#!/usr/bin/env python3
"""Complete ordered shift-composition ledger from K14 through K20."""
from hashlib import sha256
import json, math
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
COL=ROOT/'computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22/results_orbit0_k16_literal_residual.json'
K17=ROOT/'computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/results_filtered_k17_run.json'
K18=ROOT/'computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/results_k18_charge.json'
P19=ROOT/'computations/unaudited-codex-orbit0-k19-profile-census-2026-08-23/results_k19_profile_census.json'
C19=ROOT/'computations/unaudited-codex-orbit0-k19-charge-2026-08-23/results_k19_charge.json'
ARITH=ROOT/'computations/unaudited-codex-orbit0-k19-k24-arithmetic-plan-2026-08-23/results_k19_k24_arithmetic.json'
OLD=HERE/'results_filtered_k20_interface.json';OUT=HERE/'results_k14_composition_dag.json';U=400_591_699_200
def digest(p):return sha256(p.read_bytes()).hexdigest()
def comps(n):
 if n==0:return [()]
 return [c+(a,) for a in (2,3,4) if a<=n for c in comps(n-a)]
def main(write=False):
 col,k17,k18,p19,c19,old,arith=[json.loads(p.read_text()) for p in (COL,K17,K18,P19,C19,OLD,ARITH)]
 assert old['status'].startswith('RETRACTED')
 red16=col['collection']['reducible_K16_tail_occurrences'];irr16=col['collection']['irreducible_K16_tail_occurrences_before_collection']
 assert (red16,irr16)==(75_691_040,3_740_320)
 full17=211_816_960;irr17=k17['components']['K14_valid_average_K3']['raw_irreducible_occurrences'];red17=full17-irr17
 assert red17==197_414_400
 c18=k18['components']['K14_K4'];full18=c18['full_compact_occurrences'];irr18=c18['K18_irreducible_occurrences'];red18=full18-irr18
 assert (full18,irr18,red18)==(397_156_800,39_576_000,357_580_800)
 st14=json.loads((ROOT/'computations/unaudited-codex-orbit0-k19-profile-census-2026-08-23/stats_k14.json').read_text())
 products=sorted(map(int,st14['product_denominator_hist']));L=math.lcm(*products);assert L==1_517_392_800 and U%L==0
 triple=arith['hidden_higher_tail_guard']['K20_depth3_products'];assert len(triple)==142 and max(triple)==2240
 assert arith['hidden_higher_tail_guard']['K20_depth3_product_lcm']==U
 expected={14:[()],15:[],16:[(2,)],17:[(3,)],18:[(2,2),(4,)],19:[(2,3),(3,2)],20:[(2,2,2),(2,4),(3,3),(4,2)]}
 got={d:sorted(comps(d-14)) for d in range(14,21)};assert got==expected
 rows=[
  {'degree':14,'path':[],'sign':'negative','depth':0,'policy':[],'provenance':'complete factorized K14 head interface','status':'AVAILABLE'},
  {'degree':16,'path':[2],'sign':'positive','depth':1,'policy':['K14 valid-pivot average'],
   'counts':{'pivotable_discarded':red16,'irreducible_retained_occurrences':irr16},'provenance':'formula replayable; pivotable literal children not serialized','status':'PARENT_PROVENANCE_MISSING'},
  {'degree':17,'path':[3],'sign':'positive','depth':1,'policy':['K14 valid-pivot average'],
   'counts':{'full':full17,'pivotable_discarded':red17,'irreducible_retained':irr17},'provenance':'formula replayable; pivotable parents reconstructed only as response profiles later','status':'PROFILE_RECONSTRUCTED_NO_LITERAL_ROWS'},
  {'degree':18,'path':[4],'sign':'positive','depth':1,'policy':['K14 valid-pivot average'],
   'counts':{'full':full18,'pivotable':red18,'irreducible':irr18},'provenance':'scalar K18 charge only; outgoing parent profiles not serialized','status':'SCALAR_ONLY'},
  {'degree':18,'path':[2,2],'sign':'negative','depth':2,'policy':['K14 valid-pivot average','K16 all-available average'],
   'provenance':'depends on discarded raw path[2] K16 parents; absent from K18 charge','status':'MISSING'},
  {'degree':19,'path':[3,2],'sign':'negative','depth':2,'policy':['K14 valid-pivot average','K17 all-available average'],
   'counts':{'outgoing_pivot_uses':st14['outgoing_pivot_uses'],'K2_tail_operations':st14['K19_K2_tail_operations'],'weighted_nonzero_profile_keys':c19['components']['k17_k14_k2']['merged_weight_keys']},
   'provenance':'exact profile/weight charge interface, no literal K19 rows','status':'PROFILE_WEIGHT_AVAILABLE'},
  {'degree':19,'path':[2,3],'sign':'negative','depth':2,'policy':['K14 valid-pivot average','K16 all-available average'],
   'provenance':'depends on discarded raw path[2] K16 parents; absent from K19 charge','status':'MISSING'},
  {'degree':20,'path':[4,2],'sign':'negative','depth':2,'policy':['K14 valid-pivot average','K18 all-available average'],
   'counts':{'pivotable_K18_parents':red18},'provenance':'K18 parent profiles/weights were not serialized','status':'MISSING_OUTGOING_PROFILE'},
  {'degree':20,'path':[3,3],'sign':'negative','depth':2,'policy':['K14 valid-pivot average','K17 all-available average'],
   'counts':{'outgoing_pivot_uses':st14['outgoing_pivot_uses'],'K3_tail_operations':st14['outgoing_pivot_uses']*32,'unweighted_profile_keys':st14['unique_enriched_keys'],'weighted_nonzero_profile_keys':c19['components']['k17_k14_k2']['merged_weight_keys']},
   'provenance':'recoverable by changing frozen path[3,2] response-key tail degree from2 to3; not yet evaluated','status':'PROFILE_WEIGHT_RECOVERABLE'},
  {'degree':20,'path':[2,4],'sign':'negative','depth':2,'policy':['K14 valid-pivot average','K16 all-available average'],
   'provenance':'depends on 75,691,040 discarded raw path[2] K16 parents','status':'MISSING'},
  {'degree':20,'path':[2,2,2],'sign':'positive','depth':3,'policy':['K14 valid-pivot average','K16 all-available average','K18 all-available average'],
   'provenance':'both raw path[2] K16 parents and their pivotable path[2,2] K18 children are missing','status':'MISSING_DEPTH3'},
 ]
 result={
  'status':'PASS_COMPLETE_K14_COMPOSITION_DAG_AUDIT_NO_RUN',
  'ordered_compositions_by_degree':{str(d):[list(x) for x in got[d]] for d in got},
  'paths':rows,
  'hidden_discarded_parent_checkpoints':[
   {'degree':16,'path':[2],'discarded_occurrences':red16,'artifact':'K16 literal collector retained only nonpivotable normal'},
   {'degree':17,'path':[3],'discarded_occurrences':red17,'artifact':'K17 component checkpoint retained only nonpivotable normal; profile census later repaired response interface'},
   {'degree':18,'path':[4],'discarded_occurrences':red18,'artifact':'K18 charge retained only scalars/counts, no parent profile checkpoint'},
  ],
  'arithmetic':{
   'depth_at_most_2_scale_U':U,'observed_path_3_2_product_lcm':L,'all_observed_path_3_2_products_divide_U':True,
   'depth3_scale_U':U,'depth3_product_count':len(triple),'depth3_max_product':max(triple),
   'depth3_guard':'Independent pivot-depth DP certifies LCM U for all 142 K20 triple products; occurrencewise U remainder assertions remain mandatory.',
   'arithmetic_logical_sha256':arith['logical_sha256'],
  },
  'supersession':{'invalid_incomplete_logical':'ea7964f7d6a8120aa9251661a012fcc7965be18a63e9d0df9882fca9e488e57d','retraction_logical':old['logical_sha256']},
  'smallest_exact_next_step':'Replay path[2] discarded K16 parents first; census their outgoing K2/K3/K4 pivots, serialize path[2,2] K18 profiles, and compute the exact triple-denominator LCM before any general K18 prefix.',
  'scope':'K14-derived composition DAG only. Direct K15-K20 and other starting-degree source branches are separate.',
  'pinned':{str(p.relative_to(ROOT)):digest(p) for p in (COL,K17,K18,P19,C19,OLD,ARITH)},
 }
 logical=sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest();result['logical_sha256']=logical
 if write:OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':result['status'],'paths':len(rows),'missing':[r['path'] for r in rows if r['status'].startswith('MISSING')],'logical_sha256':logical},indent=2))
if __name__=='__main__':
 import sys;main('--write-results' in sys.argv)
