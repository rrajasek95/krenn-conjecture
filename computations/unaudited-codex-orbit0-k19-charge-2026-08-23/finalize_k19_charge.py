#!/usr/bin/env python3
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
NAMES=('direct_k19','k15_k4','k16_direct_k3','k16_k14_k3','k17_direct_k2','k17_k14_k2','k17_k15_k2')
OUT=HERE/'results_k19_charge.json'
def digest(p):
 h=sha256()
 with p.open('rb') as f:
  while b:=f.read(8<<20):h.update(b)
 return h.hexdigest()
def frac(n,d):
 q=Fraction(n,d);return {'numerator':q.numerator,'denominator':q.denominator,'text':str(q)}
def main(write=False):
 ds={n:json.loads((HERE/f'results_{n}.json').read_text()) for n in NAMES}
 scale=281_801_520**2
 assert all(d['scale']==scale for d in ds.values())
 assert json.loads((HERE/'results_profile_charge_selftest.json').read_text())['comparisons']==83_968
 components={}
 for n,d in ds.items():
  components[n]={
   'full_evaluations':d['full_evaluations'],'K19_irreducible_evaluations':d['irreducible_evaluations'],
   'merged_weight_keys':d['merged_keys'],'external_merge_zero_keys':d['exact_zero_keys'],
   'full_charge_scaled':d['full_charge_scaled'],'K19_irreducible_charge_scaled':d['irreducible_charge_scaled'],
   'full_charge':frac(d['full_charge_scaled'],scale),
   'K19_irreducible_charge':frac(d['irreducible_charge_scaled'],scale),
  }
 full=sum(d['full_charge_scaled'] for d in ds.values())
 irr=sum(d['irreducible_charge_scaled'] for d in ds.values())
 result={
  'status':'PASS_EXACT_K19_CHARGE_ONLY_NO_K19_ROW_COLLECTION',
  'scale':scale,'components':components,
  'combined':{
   'full_charge_scaled':full,'K19_irreducible_charge_scaled':irr,
   'full_charge':frac(full,scale),'K19_irreducible_charge':frac(irr,scale),
   'nonzero_K19_irreducible_charge':irr!=0,
  },
  'guards':{
   'literal_profile_charge_selftest_comparisons':83_968,
   'run_header_fix':'Frozen thread runs use 7-byte K19WGT1 followed by u64; patched merge reads exactly 15 header bytes. First bad-reader attempt panicked before arithmetic and runs were not regenerated.',
   'denominators':'Every source occurrence asserted S^2 mod (first_pivot_count*second_pivot_count)=0.',
   'signs':'direct P=-R8prime*E0E1E2; each head reduction emits -c/m. K16 direct response is positive relative to direct, K14-derived response negative; K17 direct response positive, both prior-response lineages negative.',
   'zero_lineage':'K16_K14_K3 is exactly zero because every frozen K14/K2 K16 response row is already nonpivotable.',
  },
  'scope':'Exact 77-cycle charge before and after the K19 pivotability filter. No K19 row collection, K20 tail, or ideal-membership claim.',
 }
 pins=[HERE/'run_k19_weight_runs.rs',HERE/'merge_and_charge_k19.rs',HERE/'results_profile_charge_selftest.json']
 pins += [HERE/f'results_{n}.json' for n in NAMES]
 pins += [HERE/f'weights_{n}.bin' for n in NAMES if n!='direct_k19']
 result['pinned']={str(p.relative_to(ROOT)):digest(p) for p in pins}
 logical=sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 result['logical_sha256']=logical
 if write:OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':result['status'],'combined':result['combined'],'logical_sha256':logical},indent=2))
if __name__=='__main__':
 import sys;main('--write-results' in sys.argv)
