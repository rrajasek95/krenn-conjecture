#!/usr/bin/env python3
import hashlib,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent;PKG=HERE.parent/'unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-2026-08-26'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
pins={HERE/'referee.py':'c3c9dfce5680c7a7d721b9b94fb6fd5401fc5cf4b41ab9e3311c000e23ee19af',HERE/'results_referee.json':'ce1105db2dedaa71bd7639df4cd758561500ad0430d9d2c55b12beaac40e928c',HERE/'HELD_APPROVAL.json':'210579d2e3367ce954d4168cc174c24c0e81644f5197f780bea74f446ef5822a',PKG/'MANIFEST.sha256':'0d2d7cfce0ed9e862b573e4fdc5791b3384c7bd21fbd6e9ff9e663c79f387115',PKG/'source_ledger.json':'b311e566fab04932f0c49a285ac3190ae4ac7a02f102799a9a2c6b34a949e4bb',PKG/'future_dependencies.json':'02e042533a68fb7a9a08d230caa7de915c3176e4d7e54b8f68a9704da7e6916e',PKG/'normalize_dependencies.py':'5afc90779b09c31950e30cb7f11cb198d9c37f5d655e6926fcfad2980561733c',PKG/'run_groups76_125.py':'3e5a744b6017dc0ba4a4d9789039bb4697d20fd1b42332195dc015cfd1e91abd'}
for path,want in pins.items():assert sha(path)==want,(path,sha(path),want)
r=json.loads((HERE/'results_referee.json').read_text());a=json.loads((HERE/'HELD_APPROVAL.json').read_text())
assert r['status']=='PASS_CONDITIONAL_HELD_GROUPS76_125_BLOCKED_ZERO_RUNS' and r['selected_group_ids']==list(range(76,126))
assert r['canonical_sources_verified']==50 and r['total_source_bytes']==90617222 and r['variables_each']==91 and r['generators_each']==6577
assert r['required_future_groups']==[list(range(1,26)),list(range(26,76))] and r['derived_union_if_satisfied']==list(range(76)) and not r['dependency_satisfied'] and r['future_hashes']==[None]*4 and not r['future_files_present']
assert r['runner_reopens_and_rehashes_all_dependency_paths'] and r['hostiles_passed']==12 and r['strict_sequential_stop_first'] and r['limits_each']=={'native_wall_seconds':240,'wrapper_wall_seconds':250,'rss_cap_bytes':8*1024**3}
assert r['scope']['solver_runs']==0 and not r['scope']['launch_authorized'] and not r['scope']['mathematical_coverage']
assert a['status'].startswith('PASS_HELD_ONLY_BLOCKED_') and a['selected_group_ids']==list(range(76,126)) and not a['launch_authorized'] and a['solver_runs']==0
for name in ('normalized_dependencies.json','independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):assert not (PKG/name).exists(),name
assert not list(PKG.rglob('*.tmp'))
print(json.dumps({'status':'PASS','held_only':True,'dependencies_satisfied':False,'runner_rehashes_paths':True,'groups':[76,125],'sources':50,'solver_runs':0},sort_keys=True))
