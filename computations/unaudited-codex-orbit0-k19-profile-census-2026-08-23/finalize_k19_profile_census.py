#!/usr/bin/env python3
from hashlib import sha256
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'results_k19_profile_census.json'
NAMES=('direct','k14','k15')
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main(write=False):
 stats={n:json.loads((HERE/f'stats_{n}.json').read_text()) for n in NAMES}
 union=json.loads((HERE/'results_key_union.json').read_text())
 assert [stats[n]['children'] for n in NAMES]==[82_938_880,211_816_960,671_208_960]
 assert [stats[n]['pivotable_children'] for n in NAMES]==[81_076_480,197_414_400,451_445_760]
 assert [stats[n]['outgoing_pivot_uses'] for n in NAMES]==[267_564_800,815_482_880,1_876_057_600]
 assert [stats[n]['unique_enriched_keys'] for n in NAMES]==[2_792_924,14_764_328,17_066_512]
 result={
  'status':'PASS_EXACT_PREFILTER_K17_PROFILE_CENSUS_NO_K19_TAILS',
  'lineages':{
   'direct':dict(stats['direct'],K19_response_sign='positive',denominator_depth=1),
   'K14_K3':dict(stats['k14'],K19_response_sign='negative',denominator_depth=2),
   'K15_K2':dict(stats['k15'],K19_response_sign='negative',denominator_depth=2),
  },
  'combined':{
   'prefilter_children':sum(stats[n]['children'] for n in NAMES),
   'pivotable_children':sum(stats[n]['pivotable_children'] for n in NAMES),
   'outgoing_pivot_uses':sum(stats[n]['outgoing_pivot_uses'] for n in NAMES),
   'uncached_K2_tail_operations':sum(stats[n]['K19_K2_tail_operations'] for n in NAMES),
   'sum_lineage_unique_keys':sum(stats[n]['unique_enriched_keys'] for n in NAMES),
   'union_unique_enriched_keys':union['union_unique_enriched_keys'],
   'unique_K2_tail_charge_evaluations':12*union['union_unique_enriched_keys'],
   'key_overlap_mask_counts':union['mask_counts'],
  },
  'denominator_guard':{
   'S':281_801_520,'uniform_scale':'S^2','uniform_scale_integer':281_801_520**2,
   'assertion':'The Rust census checked S^2 mod (first_pivot_count*second_pivot_count) = 0 for every outgoing pivot use.'
  },
  'elapsed_seconds_sum_lineages_and_merge':sum(stats[n]['elapsed_seconds'] for n in NAMES)+1.406,
  'feasibility':{
   'verdict':'YES_BOUNDED_CHARGE_ONLY_WITH_EXTERNAL_SORTED_COEFFICIENT_RUNS',
   'reason':(
    'The exact union has 25,163,280 response keys; a charge pass needs 301,959,360 '
    'unique K2-tail evaluations after coefficient aggregation. The key-only census '
    'finished in about 112 seconds and wrote 1.42 GiB. Use per-thread sorted '
    '(43-byte key,i128 weight) runs and an external merge to avoid a peak union HashMap.'
   ),
   'recommended_gate':'300 seconds / 8 GiB, atomic checkpoint after each lineage; then stream-merge and evaluate charges',
   'not_recommended':'one monolithic 180-second in-memory HashMap pass',
  },
  'scope':'Profiles and exact source-linear occurrence/denominator counts only; no K19 tail row, charge, or membership claim.',
 }
 pins=[HERE/'run_k19_profile_census.rs',HERE/'merge_k19_keys.rs',HERE/'results_key_union.json']
 pins += [HERE/f'keys_{n}.bin' for n in NAMES]
 result['pinned']={str(p.relative_to(ROOT)):digest(p) for p in pins}
 logical=sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 result['logical_sha256']=logical
 if write:OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':result['status'],'combined':result['combined'],'logical_sha256':logical},indent=2))
if __name__=='__main__':
 import sys;main('--write-results' in sys.argv)
