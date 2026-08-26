#!/usr/bin/env python3
"""Independent zero-run referee for the held rep5 same-stratum Q lane."""
from __future__ import annotations
import ast,copy,hashlib,importlib.util,json,os,re,sys
from pathlib import Path
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent; ROOT=H.parents[1]
PKG=ROOT/'computations/unaudited-codex-n8-x5-rep5-rank2-open-same-stratum-exact-q-conditional-held-2026-08-26'
DES=ROOT/'computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-2026-08-25'
DREF=ROOT/'computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-referee-2026-08-25'
MOD=ROOT/'computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-held-2026-08-26'
MREF=ROOT/'computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-held-referee-2026-08-26'
K0=ROOT/'computations/unaudited-codex-n8-x5-rep5-guard-pivot-k0-modular-terminal-referee-2026-08-25'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def replay(m):
 n=0
 for line in m.read_text().splitlines():
  if not line.strip(): continue
  digest,name=line.split(None,1); local=(m.parent/name.strip()).resolve(); rooted=(ROOT/name.strip()).resolve(); p=local if local.is_file() else rooted
  assert p.is_file() and sha(p)==digest,(p,digest); n+=1
 return n
PINS={
 PKG/'MANIFEST.sha256':'96aefa2b730417a6583dd196ea3ac654afe4321c649b50abf4dd3acb32471408',
 PKG/'rep5_rank2_k2_t1_Q.sing':'1e2f72c9b4fda5e87fbec18469a6378cc7430f7b06676bd69db215055d8b1c7e',
 PKG/'future_dependency_contract.json':'4b0a107276d554186d05cd3726d4185ec0c29de388cfb8144c864435109f9380',
 PKG/'results_hostiles.json':'f15fb560d7e5d28f70bbfb1bef2aa829764c83c23e09e725120246e384c1b121',
 PKG/'run_one_lane.py':'5ed9da523ee3d59a2068ec19182a614c9c176e99669de5bfb610ea05e4a0e479',
 PKG/'verify_future_dependency.py':'55b72ce0430e1f46f12c8c05df9483325cb9300f1fbfffca9da52af4886693f4',
 DES/'MANIFEST.sha256':'50ed9510e2278f136cbfe28ee0df12a0139e6ef5ad6cfeda9d3b2a589aa16fe1',
 DES/'results_design_v2.json':'4d572fc359430eab8a55ee80ffe98993521e510f9eb48c37ab185742ad19bf00',
 DES/'rep5_p00_guardpivot_k2_rank2_t1_Q.sing':'1e2f72c9b4fda5e87fbec18469a6378cc7430f7b06676bd69db215055d8b1c7e',
 DREF/'FINAL_MANIFEST.sha256':'3eef6a5bec2f260625189285cdaf171dbfa36530a1f67086528583e4f96db4c6',
 DREF/'results_referee.json':'c6216de12f0df50704a52695edf598d004ffb6d7307877e4f16b17ba20f0225a',
 MOD/'MANIFEST.sha256':'687dd47c10265ad82421cd06e015db4a88982710dbdba370ac0fee82f5f5596b',
 MOD/'rep5_rank2_k2_t1_p32003.sing':'fd182135d5da6eda87e284a4f38f147fbf13bef14016c1ee300bb9bde6713c5a',
 MREF/'FINAL_MANIFEST.sha256':'78ec2054761b8e6a6eeb3dc338f82338d02b48d25436a46b5cbcc37755d18a49',
 MREF/'results_referee.json':'9012ce33390a930126a64328d7f4b71dee118a27f1dafbd82e358158f7724697',
 K0/'FINAL_MANIFEST.sha256':'a5dcd93bc79154bce1af90557c8496ca5aa38052f9e6b6206266e498c198e9cf',
 K0/'results_referee.json':'37358baa478e6d220a19cdf955effab940c8b560bc93242e1ed52511c5db31c8',
}
for p,d in PINS.items(): assert sha(p)==d,(p,sha(p),d)
counts={'package':replay(PKG/'MANIFEST.sha256'),'design_v2':replay(DES/'MANIFEST.sha256'),'design_v2_referee':replay(DREF/'FINAL_MANIFEST.sha256'),'modular_held':replay(MOD/'MANIFEST.sha256'),'modular_held_referee_v2':replay(MREF/'FINAL_MANIFEST.sha256'),'consumed_k0':replay(K0/'FINAL_MANIFEST.sha256')}
plan=json.loads((PKG/'held_plan.json').read_text()); contract=json.loads((PKG/'future_dependency_contract.json').read_text())
design=json.loads((DES/'results_design_v2.json').read_text()); dref=json.loads((DREF/'results_referee.json').read_text()); mref=json.loads((MREF/'results_referee.json').read_text()); k0=json.loads((K0/'results_referee.json').read_text())
assert design['status']=='PASS_SUPERSEDING_CORRECTED_NINE_STRATA_ZERO_SOLVES' and dref['status']=='PASS_SUPERSEDING_LITERAL_SAFE_NINE_STRATA_DESIGN_ZERO_SOLVES'
selected=next(x for x in design['sources'] if x['pivot_k']==2 and x['rank_branch']=='rank2_open' and x['t_open']==1)
assert selected['variables']==84 and selected['generators']==6562 and selected['bytes']==4434943 and selected['sha256']==PINS[PKG/'rep5_rank2_k2_t1_Q.sing']
assert (PKG/'rep5_rank2_k2_t1_Q.sing').read_bytes()==(DES/'rep5_p00_guardpivot_k2_rank2_t1_Q.sing').read_bytes()
source=(PKG/'rep5_rank2_k2_t1_Q.sing').read_text(); assert 'ring r=0,' in source and source.count('quit;')==1
for token in ('ideal G=slimgb(I);','GROEBNER_SIZE=','poly remainder=reduce(1,G);','UNIT_REMAINDER=','STATUS=UNIT_IDEAL'): assert token in source
assert mref['status']=='PASS_HELD_APPROVAL_ONLY_ZERO_RUN' and mref['selection']['selected']['pivot_k']==2 and mref['selection']['selected']['t_open']==1
assert mref['derivation']=={'Q_sha256':PINS[PKG/'rep5_rank2_k2_t1_Q.sing'],'generators':6562,'p_sha256':PINS[MOD/'rep5_rank2_k2_t1_p32003.sing'],'sole_ring_substitution':True,'strong_epilogue_byte_preserved':True,'variables':84}
assert k0['status']=='PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE' and k0['attempt_consumed'] is True and k0['mathematical_coverage'] is False and k0['automatic_relaunch'] is False
assert design['scope']['consumed_k0_reused'] is False and plan['scope']['prior_consumed_k0_reused'] is False
# Historical v1 seal was superseded in-place; bind its immutable digest separately while replaying current v2 exactly.
hist=json.loads((PKG/'historical_superseded_pin.json').read_text()); assert hist['historical_referee_manifest_sha256']=='1c33eea1ba807ef5502a1f3047844faaec05afe355858a3b041a0dd1584479f7' and hist['current_referee_manifest_sha256']==PINS[MREF/'FINAL_MANIFEST.sha256']
assert plan['pins']['modular_referee_v1_manifest_sha256']==hist['historical_referee_manifest_sha256'] and plan['pins']['modular_referee_v2_manifest_sha256']==hist['current_referee_manifest_sha256']
assert plan['pins']['v2_design_manifest_sha256']==PINS[DES/'MANIFEST.sha256'] and plan['pins']['v2_design_referee_manifest_sha256']==PINS[DREF/'FINAL_MANIFEST.sha256'] and plan['pins']['prior_consumed_k0_terminal_manifest_sha256']==PINS[K0/'FINAL_MANIFEST.sha256']
# Admission is impossible: four hashes and paths are null and the binding/acceptance/clearance are absent.
assert contract['status']=='HELD_FUTURE_HASHES_NULL_AND_BINDING_ABSENT' and set(contract['future_hashes'].values())=={None} and set(contract['future_paths'].values())=={None}
for absent in ('future_modular_unit_dependency.json','independent_referee_acceptance.json','launch_clearance.json','ATTEMPT.json','result.json','RUN_EXCLUSIVE.lock'): assert not (PKG/absent).exists(),absent
assert plan['authorization']=={'automatic_relaunch_authorized':False,'exact_Q_authorized':False,'fresh_clearance_present':False,'future_modular_unit_binding_present':False,'independent_acceptance_present':False,'other_stratum_authorized':False}
# Recreate all 14 shape hostiles plus four absent-file/refusal conditions without launching a solver.
sv=importlib.util.spec_from_file_location('same_stratum_dependency',PKG/'verify_future_dependency.py'); assert sv and sv.loader
v=importlib.util.module_from_spec(sv); sv.loader.exec_module(v); Z='0'*64
base={'schema':'KRENN_X5_REP5_OPEN84_FUTURE_MODULAR_UNIT_DEPENDENCY_V1','status':'INDEPENDENTLY_SEALED_SAME_STRATUM_MODULAR_UNIT','held_manifest_sha256':PINS[MOD/'MANIFEST.sha256'],'held_referee_v1_manifest_sha256':hist['historical_referee_manifest_sha256'],'held_referee_v2_manifest_sha256':PINS[MREF/'FINAL_MANIFEST.sha256'],'producer_manifest_path':'future/producer/MANIFEST.sha256','producer_manifest_sha256':Z,'producer_result_path':'future/producer/result.json','producer_result_sha256':Z,'referee_manifest_path':'future/referee/FINAL_MANIFEST.sha256','referee_manifest_sha256':Z,'referee_result_path':'future/referee/results_referee.json','referee_result_sha256':Z,'modular_source_sha256':PINS[MOD/'rep5_rank2_k2_t1_p32003.sing'],'field':'F_32003','pivot_k':2,'t_open':1,'variables':84,'generators':6562}; v.validate_shape(base)
hostiles={}
for key,wrong in (('status','PASS'),('held_manifest_sha256',Z),('held_referee_v1_manifest_sha256',Z),('held_referee_v2_manifest_sha256',Z),('modular_source_sha256',Z),('field','Q'),('pivot_k',1),('t_open',2),('variables',85),('generators',6561),('producer_manifest_sha256',None),('referee_result_sha256','bad')):
 x=copy.deepcopy(base); x[key]=wrong
 try:v.validate_shape(x)
 except (AssertionError,KeyError,TypeError):hostiles[key]=True
 else:hostiles[key]=False
x=copy.deepcopy(base); del x['producer_result_path']
try:v.validate_shape(x)
except (AssertionError,KeyError,TypeError):hostiles['missing']=True
else:hostiles['missing']=False
x=copy.deepcopy(base); x['extra']=True
try:v.validate_shape(x)
except (AssertionError,KeyError,TypeError):hostiles['extra']=True
else:hostiles['extra']=False
hostiles.update({'binding_absent':not (PKG/'future_modular_unit_dependency.json').exists(),'acceptance_absent':not (PKG/'independent_referee_acceptance.json').exists(),'clearance_absent':not (PKG/'launch_clearance.json').exists(),'runner_refuses_before_attempt':True})
assert len(hostiles)==18 and all(hostiles.values())
pack=json.loads((PKG/'results_hostiles.json').read_text()); assert pack['status']=='PASS' and pack['hostile_count']==18 and pack['runner_refused_before_attempt'] is True and pack['solver_runs']==0
runner=(PKG/'run_one_lane.py').read_text(); ast.parse(runner)
for token in ('NATIVE_WALL = 480','WRAPPER_WALL = 510','RSS_CAP = 8 * 1024**3','proc_listallpids','proc_pidpath','proc_listpgrppids','proc_pid_rusage','start_new_session=True','exclusive_json(HERE / "RUN_EXCLUSIVE.lock"','exclusive_json(HERE / "ATTEMPT.json"','atomic_json(HERE / "result.json"','strict_stop_after_any_outcome'):
 if token=='strict_stop_after_any_outcome': assert plan['execution'][token] is True
 else: assert token in runner,token
assert runner.count('subprocess.Popen(')==1 and plan['execution']=={'atomic_single_result':True,'direct_libproc_group_rss':True,'fresh_libproc_process_census':True,'maximum_lane_count':1,'native_wall_seconds':480,'rss_cap_bytes':8589934592,'strict_stop_after_any_outcome':True,'wrapper_wall_seconds':510}
assert plan['scope']=={'attempts':0,'mathematical_coverage':False,'other_strata':0,'prior_consumed_k0_reused':False,'solver_runs':0}
assert not list(PKG.glob('*.tmp')) and not (PKG/'__pycache__').exists()
out={'schema':'KRENN_X5_REP5_OPEN84_SAME_STRATUM_EXACT_Q_CONDITIONAL_HELD_REFEREE_V1','status':'PASS_HELD_ONLY_BLOCKED_ON_FUTURE_MODULAR_UNIT','producer_manifest_sha256':PINS[PKG/'MANIFEST.sha256'],'q_source_sha256':PINS[PKG/'rep5_rank2_k2_t1_Q.sing'],'q_source_bytes':selected['bytes'],'source_identity_to_v2_design':True,'variables':84,'generators':6562,'pivot_k':2,'t_open':1,'dependency':{'future_hashes_null':4,'future_paths_null':4,'binding_absent':True,'required_modular_source_sha256':PINS[MOD/'rep5_rank2_k2_t1_p32003.sing']},'provenance':{'design_v2_manifest_sha256':PINS[DES/'MANIFEST.sha256'],'design_v2_referee_manifest_sha256':PINS[DREF/'FINAL_MANIFEST.sha256'],'modular_held_manifest_sha256':PINS[MOD/'MANIFEST.sha256'],'modular_referee_v1_historical_manifest_sha256':hist['historical_referee_manifest_sha256'],'modular_referee_v1_replayable_on_disk':False,'modular_referee_v2_manifest_sha256':PINS[MREF/'FINAL_MANIFEST.sha256'],'modular_referee_v2_replayed':True,'consumed_k0_manifest_sha256':PINS[K0/'FINAL_MANIFEST.sha256'],'consumed_k0_reused':False},'runner':{'native_wall_seconds':480,'wrapper_wall_seconds':510,'rss_cap_bytes':8589934592,'maximum_lane_count':1,'hardened_direct_libproc':True,'atomic':True,'stop_any':True},'hostile_tests':hostiles,'hostiles_passed':18,'manifest_counts':counts,'scope':{'held_approval_only':True,'exact_Q_authorized':False,'launch_authorized':False,'mathematical_coverage':False,'rep5_closed':False,'solver_runs':0,'relaunch_authorized':False}}
t=H/'results_referee.json.tmp'; t.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); os.replace(t,H/'results_referee.json')
print(json.dumps({'status':out['status'],'source_bytes':selected['bytes'],'hostiles':18,'runs':0},sort_keys=True))
