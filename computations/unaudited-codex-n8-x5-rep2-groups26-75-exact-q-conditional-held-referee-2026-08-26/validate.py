#!/usr/bin/env python3
import hashlib,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent;PKG=HERE.parent/'unaudited-codex-n8-x5-rep2-groups26-75-exact-q-conditional-held-2026-08-26'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
pins={HERE/'referee.py':'fbe881d830941ff0a37be711ded3a7747c5bf81b33d3af3a2997159864eb46df',HERE/'results_referee.json':'442f34d365e5954f5984b4780113c949e761488f2c27a8e782a9c70998b7cbba',HERE/'HELD_APPROVAL.json':'b65813b8907b51b93bf14c6c36b7efc9ba76bff69c30fc771a17500471b10803',PKG/'MANIFEST.sha256':'07c356ff169a8586add38bb8cb808977570a1ad83f001fb4918c5da163ef0f38',PKG/'source_ledger.json':'0a9ad8dfb140d8e601c88429c13945d1182ac6dffe2c7dcc022a1b353a1005e7',PKG/'future_dependency.json':'df9ec9aba49241c0d17853c9081917e48b134e16b51f382fee85f4f5f550651c',PKG/'normalize_dependency.py':'c4625a17f0368e94a1debed8c76126284f9a66e4dc0de929025046f2ca15e150',PKG/'run_groups26_75.py':'2cdcfa471e0432a734b9089a14f4f8443ea609b3517a6cd7f4bd853133b568b9'}
for path,want in pins.items():assert sha(path)==want,(path,sha(path),want)
r=json.loads((HERE/'results_referee.json').read_text());a=json.loads((HERE/'HELD_APPROVAL.json').read_text())
assert r['status']=='PASS_CONDITIONAL_HELD_GROUPS26_75_BLOCKED_ZERO_RUNS' and r['selected_group_ids']==list(range(26,76))
assert r['canonical_sources_verified']==50 and r['total_source_bytes']==92375796 and r['variables_each']==91 and r['generators_each']==6577
assert r['required_future_groups']==list(range(1,26)) and r['derived_union_if_satisfied']==list(range(26))
assert not r['dependency_satisfied'] and r['future_hashes']==[None,None] and not r['future_files_present'] and r['hostiles_passed']==12
assert r['strict_sequential_stop_first'] and r['limits_each']=={'native_wall_seconds':240,'wrapper_wall_seconds':250,'rss_cap_bytes':8*1024**3}
assert r['scope']['solver_runs']==0 and not r['scope']['launch_authorized'] and not r['scope']['mathematical_coverage']
assert a['status'].startswith('PASS_HELD_ONLY_BLOCKED_') and a['selected_group_ids']==list(range(26,76)) and not a['launch_authorized'] and a['solver_runs']==0
for name in ('normalized_dependency.json','independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):
 assert not (PKG/name).exists(),name
assert not list(PKG.rglob('*.tmp'))
print(json.dumps({'status':'PASS','held_only':True,'dependency_satisfied':False,'groups':[26,75],'sources':50,'solver_runs':0},sort_keys=True))
