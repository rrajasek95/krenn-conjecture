#!/usr/bin/env python3
import hashlib, json, math, pathlib
from fractions import Fraction

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parent.parent
TAIL=ROOT/'computations/unaudited-codex-orbit0-k18-parent-stream-design-2026-08-23/results_parent_stream_prefix.json'
MODES={'k14':'K14_K4','k15':'K15_K3','k16':'K16_K2'}
PIV={'k14':357_580_800,'k15':923_253_760,'k16':807_499_618}
OUT_MAX={'k14':27_891_302_400,'k15':72_013_793_280,'k16':62_984_970_204}
OUT_PREFIX={'k14':595_014_451,'k15':2_475_206_400,'k16':2_883_936_436}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
ref=json.loads(TAIL.read_text())['components']
result={'status':'PASS_THREE_EXACT_RESTARTABLE_EXPORTER_PREFIXES','record_bytes':104,'scale_U':'400591699200','components':{}}
for mode,name in MODES.items():
    mpath=HERE/f'prefix_{mode}.manifest.json'; part=HERE/f'prefix_{mode}.part000000.bin'
    m=json.loads(mpath.read_text()); r=ref[name]
    checks={
      'generated':m['generated_parents']==r['generated_until_cap'],
      'pivotable':m['pivotable_parents']==r['pivotable_parents'],
      'outgoing':m['outgoing_pivot_uses']==r['outgoing_pivot_uses'],
      'keys':m['emitted_records_local_unique']==r['distinct_nonzero_profile_keys'],
      'weight':m['signed_weight_sum_scaled']==r['profile_weight_sum_scaled'],
      'denominators':m['m1_m2_hist']==r['m1_m2_hist'],
    }
    assert all(checks.values()),(mode,checks)
    projected_unique=Fraction(OUT_PREFIX[mode]*r['distinct_nonzero_profile_keys'],r['outgoing_pivot_uses'])
    elapsed=Fraction(str(m['elapsed_seconds']))
    wall=elapsed*PIV[mode]/50_000
    result['components'][mode]={
      'frozen_prefix_checks':checks,'manifest_sha256':sha(mpath),'part_sha256':sha(part),
      'part_bytes':part.stat().st_size,'measured_prefix_seconds':m['elapsed_seconds'],
      'exact_full_pivotable_parent_count':PIV[mode],
      'exact_hard_outgoing_use_upper':OUT_MAX[mode],
      'exact_hard_unmerged_record_bytes_upper':OUT_MAX[mode]*104,
      'prefix_projected_outgoing_uses':OUT_PREFIX[mode],
      'prefix_projected_unmerged_record_bytes':OUT_PREFIX[mode]*104,
      'prefix_ratio_projected_unique_records_ceiling':math.ceil(projected_unique),
      'prefix_ratio_projected_sorted_record_bytes_ceiling':math.ceil(projected_unique)*104,
      'kernel_only_linear_wall_projection_seconds':float(wall),
      'kernel_only_linear_wall_projection_formula':f'{m["elapsed_seconds"]}*{PIV[mode]}/50000',
    }
result['scope']={
  'executed':'three independently verified 50,000-pivotable-parent prefixes only',
  'not_executed':'full shards, cross-part merge, K20 response evaluation',
  'estimate_warning':'disk hard bounds are exact from frozen operation bounds; prefix-ratio disk and linear wall figures are planning estimates and exclude full external-merge overhead',
  'restart_contract':'a source-range shard is accepted only when its atomic manifest exists; sorted part files are atomic and incomplete orphan parts are ignored; parts require a later signed external merge',
}
out=HERE/'results_three_stream_exporter_prefixes.json';out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
