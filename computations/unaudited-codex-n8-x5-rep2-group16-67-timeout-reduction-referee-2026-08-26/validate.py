#!/usr/bin/env python3
"""Fail-closed referee validator; no solver."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((H/'results_referee.json').read_text());assert r['status']=='PASS_EXACT_FOUR_STRATUM_REDUCTION_REFEREE_ZERO_SOLVES'
assert r['producer']['manifest_sha256']=='3d4d6fbc89f5adcc45032c37b1b038780761f479313575c59e4e8bd760da75fd' and r['producer']['result_sha256']=='10c7c360683bfc780645ccb16d7a9d5f50500cc3af8272b5f49f1f8c2451bf00'
assert r['source']=={'sha256':'2403105f5c6bf4860525220d0d2d036099b79ace67297c864767ae71b9e97339','variables':67,'generators':6574,'expanded_monomials':215640}
rank=r['ranks'];assert rank['coefficient_Q']==6561 and rank['support_Q']==47 and rank['exponent_Q']==67 and rank['affine_Q']==19
assert all(value==6561 for value in rank['coefficient_mod'].values()) and all(value==47 for value in rank['support_mod'].values()) and all(value==67 for value in rank['exponent_mod'].values()) and all(value==19 for value in rank['affine_mod'].values())
assert r['claim_audit']=={'all_67_amplitude_active':True,'exact_amplitude_linear_redundancy':0,'monic_graph_candidates':[],'no_inactive_redundancy_or_monic_overclaim':True}
assert r['guard_factorization']['identities_exact'] and r['guard_factorization']['d_b0_sat_unit_equation_exact']
cover=r['t_cover'];assert cover['exhaustive_disjoint_locally_closed_cover'] and cover['reversible'] and cover['all_sources_byte_rebuilt'] and cover['all_removed_identifiers_absent']
assert [(x['variables'],x['generators']) for x in cover['strata']]==[(64,6569),(63,6569),(64,6569),(62,6568)] and all(x['removed_identifiers_absent'] and x['forward_reverse_verified'] for x in cover['strata'])
t=r['timeout_binding'];assert t['result_sha256']=='d0f48380558bb663567083c744667f76fad18cb85cc47e0e93b857dc05cac68f' and t['attempt_consumed'] and t['termination']=='NATIVE_WALL_CAP_240' and t['mathematical_coverage'] is False and t['reuse_or_relaunch_authorized'] is False
c=r['prior_57_comparison'];assert (c['prior_chart_count'],c['subdivided_prior_charts'],c['unchanged_prior_charts'],c['replacement_t_charts'],c['resulting_global_chart_count'])==(57,1,56,4,60) and c['smallest_sound_shape']==[62,6568]
assert r['scope']=={'design_referee_only':True,'singular_runs':0,'ideal_runs':0,'smallest_pilot_launched':False,'group16_closed':False,'rep2_closed':False}
assert not list(H.rglob('*.tmp')) and not list(H.rglob('__pycache__'))
if (H/'MANIFEST.sha256').exists():
 for line in (H/'MANIFEST.sha256').read_text().splitlines():
  digest,name=line.split(None,1);path=(H/name.strip()).resolve();assert path.is_file() and sha(path)==digest
print(json.dumps({'status':'PASS_REDUCTION_REFEREE_VALIDATED','ranks':[6561,47,67,19],'strata':[[64,6569],[63,6569],[64,6569],[62,6568]],'global_cover':60,'solver_runs':0},sort_keys=True))
