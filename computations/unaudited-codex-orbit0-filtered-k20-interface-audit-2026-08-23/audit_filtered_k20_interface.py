#!/usr/bin/env python3
"""Exact K20 recurrence/interface audit; performs no K20 reduction."""
from hashlib import sha256
import json, math
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
K16=ROOT/'computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/results_filtered_k16_run.json'
K18=ROOT/'computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/results_k18_charge.json'
P19=ROOT/'computations/unaudited-codex-orbit0-k19-profile-census-2026-08-23/results_k19_profile_census.json'
C19=ROOT/'computations/unaudited-codex-orbit0-k19-charge-2026-08-23/results_k19_charge.json'
OUT=HERE/'results_filtered_k20_interface.json'
U=400_591_699_200

def digest(p):return sha256(p.read_bytes()).hexdigest()
def factors(n):
 d=2;o={}
 while d*d<=n:
  while n%d==0:o[d]=o.get(d,0)+1;n//=d
  d+=1
 if n>1:o[n]=1
 return o
def main(write=False):
 k16,k18,p19,c19=[json.loads(p.read_text()) for p in (K16,K18,P19,C19)]
 frozen=ROOT/'computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22/results_orbit0_k16_literal_residual.json'
 f=json.loads(frozen.read_text())
 assert f['collection']['reducible_K16_tail_occurrences']==75_691_040
 # Supersession guard: the frozen K16 artifact is an associated-graded normal.
 # It discarded pivotable K16 children, whose K4 and iterated K2 tails first
 # re-enter at K20.  Therefore the former two-factor interface is incomplete.
 retracted={
  'status':'RETRACTED_INCOMPLETE_K20_DAG_NO_PREFIX_RUN',
  'reason':(
   'The frozen K14-to-K16 collector discarded 75,691,040 pivotable K16 '
   'tail occurrences. Their higher tails were not serialized, so treating the '
   'retained frozen normal as an empty K14-derived K16 feed was invalid.'
  ),
  'missing_primitive_paths':[
   {'path':[2,4],'degree':'K14 -> K16 -> K20','minimum_denominator_depth':2},
   {'path':[2,2,2],'degree':'K14 -> K16 -> K18 -> K20','minimum_denominator_depth':3},
  ],
  'corrected_scope':(
   'The previously enumerated visible lineages remain partial associated-graded '
   'data, but they do not exhaust K20. No K18-profile prefix was launched or '
   'accepted after this guard.'
  ),
  'arithmetic_guard':(
   'The triple (2,2,2) chain requires depth-three arithmetic. An independent '
   'pivot-depth DP subsequently certified all 142 K20 triple products, maximum '
   '2240, with the same LCM U=400591699200. Thus arithmetic is not the blocker; '
   'the hidden source provenance is.'
  ),
  'smallest_next_step':(
   'Replay the 75,691,040 discarded literal K16 occurrences with source '
   'provenance, census their K4 feed and their pivotable K2 children, and audit '
   'all resulting two- and three-level denominator products before resuming the '
   'four visible K18 lineages.'
  ),
  'pinned':{str(p.relative_to(ROOT)):digest(p) for p in (K16,K18,P19,C19,frozen)},
 }
 logical=sha256(json.dumps(retracted,sort_keys=True,separators=(',',':')).encode()).hexdigest();retracted['logical_sha256']=logical
 if write:OUT.write_text(json.dumps(retracted,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':retracted['status'],'discarded_K16_occurrences':75_691_040,'logical_sha256':logical},indent=2))
 return
 assert c19['status']=='PASS_EXACT_K19_CHARGE_ONLY_NO_K19_ROW_COLLECTION'
 direct=485*60**3
 uses16=129_939_187
 from16=uses16*60
 uses17=p19['combined']['outgoing_pivot_uses']
 from17=uses17*32
 assert (direct,from16,from17)==(104_760_000,7_796_351_220,94_691_368_960)
 # Exact provider-level K18 parent counts exposed by the charge pass.
 km={'direct':'direct','K14_K4':'K14_K4','K15_K3':'K15_K3','K16_K2':'K16_K2'}
 p18={n:k18['components'][k]['full_compact_occurrences']-k18['components'][k]['K18_irreducible_occurrences'] for n,k in km.items()}
 assert p18=={'direct':137_817_600,'K14_K4':357_580_800,'K15_K3':923_253_760,'K16_K2':807_499_618}
 p18_total=sum(p18.values());upper_uses18=78*p18_total;upper18=12*upper_uses18
 # Exact product denominators already observed at the K17 page.
 product_sets={}
 for n in ('direct','k14','k15'):
  d=json.loads((ROOT/f'computations/unaudited-codex-orbit0-k19-profile-census-2026-08-23/stats_{n}.json').read_text())
  product_sets[n]=sorted(map(int,d['product_denominator_hist']))
 assert all(U%x==0 for xs in product_sets.values() for x in xs)
 known_lcm=math.lcm(*(x for xs in product_sets.values() for x in xs))
 assert known_lcm==1_517_392_800 and U%known_lcm==0
 hostile=(direct+from16+from17+upper18)*U*8_448
 result={
  'status':'PASS_EXACT_K20_INTERFACE_NO_K20_RUN',
  'degree_feeds':{
   'direct':'K8 + (4+4+4) = K20',
   'K16':'K16 + K4 = K20',
   'K17':'K17 + K3 = K20 (YES)',
   'K18':'K18 + K2 = K20',
   'K19':'minimum K19 + K2 = K21, so K19 cannot feed K20',
  },
  'lineages':[
   {'name':'direct_K20_444','sign':'negative','denominator_depth':0,'compact_operations_exact':direct},
   {'name':'direct_K16_to_K20_K4','sign':'positive','denominator_depth':1,'parent_pivot_uses_exact':uses16,'compact_operations_exact':from16,'nonzero_profile_keys_exact':1_033_323},
   {'name':'K14_to_K16_K2_then_K20_K4','sign':'negative','denominator_depth':2,'compact_operations_exact':0,'reason':'all frozen K14/K2 K16 rows are nonpivotable'},
   {'name':'direct_K17_to_K20_K3','sign':'positive','denominator_depth':1,'outgoing_profile_keys_exact':2_661_633},
   {'name':'K14_to_K17_K3_then_K20_K3','sign':'negative','denominator_depth':2,'outgoing_profile_keys_exact':13_844_092},
   {'name':'K15_to_K17_K2_then_K20_K3','sign':'negative','denominator_depth':2,'outgoing_profile_keys_exact':16_109_793},
   {'name':'direct_K18_to_K20_K2','sign':'positive','denominator_depth':1,'pivotable_parent_occurrences':p18['direct']},
   {'name':'K14_to_K18_K4_then_K20_K2','sign':'negative','denominator_depth':2,'pivotable_parent_occurrences':p18['K14_K4']},
   {'name':'K15_to_K18_K3_then_K20_K2','sign':'negative','denominator_depth':2,'pivotable_parent_occurrences':p18['K15_K3']},
   {'name':'direct_K16_to_K18_K2_then_K20_K2','sign':'negative','denominator_depth':2,'pivotable_parent_occurrences':p18['K16_K2']},
  ],
  'known_compact_work':{
   'direct_exact':direct,'K16_K4_exact':from16,'K17_K3_exact':from17,
   'K17_nonzero_key_sum':2_661_633+13_844_092+16_109_793,
   'K17_unweighted_union_keys_exact':p19['combined']['union_unique_enriched_keys'],
   'K17_unique_K3_tail_charge_eval_upper':32*p19['combined']['union_unique_enriched_keys'],
  },
  'missing_K18_interface':{
   'pivotable_parent_occurrences_by_lineage':p18,'pivotable_parent_occurrences_total':p18_total,
   'outgoing_pivot_uses_exact':None,'K2_compact_operations_exact':None,
   'outgoing_pivot_uses_upper':upper_uses18,'K2_compact_operations_upper':upper18,
   'missing_provenance':(
    'The K18 charge run retained scalar charges/evaluation counts only; its '
    'thread-local parent response profiles and coefficients were not serialized. '
    'Thus the outgoing K18 pivot counts/keys cannot be recovered from the frozen '
    'K18 result without replaying the four prefilter source streams.'
   ),
  },
  'corrected_integer_plan':{
   'U':U,'factorization':factors(U),'S_squared_over_U':(281_801_520**2)//U,
   'known_K17_product_lcm':known_lcm,'U_over_known_K17_product_lcm':U//known_lcm,
   'rule':'Represent every lineage numerator at scale U and assert U mod (m_first*m_second)=0 occurrencewise; one-step lineages use m_first=1.',
   'K18_guard':'Do not assume the missing K18 products: the profile census must stop on the first U remainder failure.',
   'hostile_i128_bound_using_K18_upper':hostile,'i128_safety_margin_floor':(2**127-1)//hostile,
  },
  'feasibility':{
   'verdict':'K20_CHARGE_NOT_READY; K18_PROFILE_CENSUS_IS_THE_REQUIRED_NEXT_GATE',
   'smallest_next_step':(
    'Replay the four prefilter K18 lineages into enriched outgoing-K2 profile keys '
    'only, checkpointed per lineage; record exact pivot uses, U product remainders, '
    'and sorted-key union. No K20 tail evaluation or row collection.'
   ),
   'cost_guard':(
    'The frozen K18 page has 2,226,151,778 pivotable provider-level parent '
    'occurrences. The rigorous uncached upper is 2,083,678,064,208 K2 tail '
    'operations. A prefix-measured 600s/12GB census is plausible; a full K20 '
    'charge run is not authorized before that census lands.'
   ),
  },
  'compact_level_guard':'Counts combine precollection source-pair and collected H-orbit providers and are engineering work counts, not a common literal mass census.',
  'scope':'Formula/sign/denominator/provenance/cost audit only; no K20 charge, rows, or K21 tails.',
  'pinned':{str(p.relative_to(ROOT)):digest(p) for p in (K16,K18,P19,C19)},
 }
 logical=sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest();result['logical_sha256']=logical
 if write:OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':result['status'],'known':[direct,from16,from17],'K18_upper':upper18,'logical_sha256':logical},indent=2))
if __name__=='__main__':
 import sys;main('--write-results' in sys.argv)
