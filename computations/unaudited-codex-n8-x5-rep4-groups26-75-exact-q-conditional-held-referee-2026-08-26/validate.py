#!/usr/bin/env python3
import hashlib,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent;PKG=HERE.parent/'unaudited-codex-n8-x5-rep4-groups26-75-exact-q-conditional-held-2026-08-26'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
pins={HERE/'referee.py':'9e738aa14aec193c14747d5442ca8b43cfee58f1f21382cc8d7d2543f8e081a8',HERE/'results_referee.json':'6b2d15c8c0b27ef3e6d931bcba44b3471691baad913230cb03a9c6993b6587e4',HERE/'HELD_APPROVAL.json':'690da61862010e23a13351919c2f6c32091e3f9bfad6ddc312ec7b1091144ed9',PKG/'MANIFEST.sha256':'c79cf415a4dc6327dcaefa7f9f002a1f1f2b5af5afef2a80bab16d8cfc9ccbb6',PKG/'source_ledger.json':'48e9fb104efd69a1267f5ff1015a2142af33d481a430bebab2f794442afa8341',PKG/'future_dependency.json':'14914c42a19896d680a8cab0c154795ea15b7e8fae0d52b0a0b58e26c8f40a5d',PKG/'normalize_dependency.py':'3fca6f290c810bbf9e15d524de79510ab7c7bad11069890e85d12ab8843895a9',PKG/'run_groups26_75.py':'b29a78c495517ddb9c43147c5c9ec1091c921a63e4a8285cf7549d0926d721aa'}
for path,want in pins.items():assert sha(path)==want,(path,sha(path),want)
r=json.loads((HERE/'results_referee.json').read_text());a=json.loads((HERE/'HELD_APPROVAL.json').read_text())
assert r['status']=='PASS_CONDITIONAL_HELD_GROUPS26_75_BLOCKED_ZERO_RUNS' and r['selected_group_ids']==list(range(26,76))
assert r['canonical_sources_verified']==50 and r['total_source_bytes']==90617198 and r['variables_each']==91 and r['generators_each']==6577
assert r['required_future_groups']==list(range(1,26)) and r['derived_union_if_satisfied']==list(range(26)) and not r['dependency_satisfied'] and r['future_hashes']==[None,None] and not r['future_files_present'] and r['hostiles_passed']==12
assert r['strict_sequential_stop_first'] and r['limits_each']=={'native_wall_seconds':240,'wrapper_wall_seconds':250,'rss_cap_bytes':8*1024**3}
assert r['scope']['solver_runs']==0 and not r['scope']['launch_authorized'] and not r['scope']['mathematical_coverage']
assert a['status'].startswith('PASS_HELD_ONLY_BLOCKED_') and a['selected_group_ids']==list(range(26,76)) and not a['launch_authorized'] and a['solver_runs']==0
for name in ('normalized_dependency.json','independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):assert not (PKG/name).exists(),name
assert not list(PKG.rglob('*.tmp'))
print(json.dumps({'status':'PASS','held_only':True,'dependency_satisfied':False,'groups':[26,75],'sources':50,'solver_runs':0},sort_keys=True))
