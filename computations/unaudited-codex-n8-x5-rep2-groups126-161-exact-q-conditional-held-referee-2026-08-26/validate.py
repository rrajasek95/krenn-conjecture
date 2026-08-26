#!/usr/bin/env python3
import hashlib,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent;PKG=HERE.parent/'unaudited-codex-n8-x5-rep2-groups126-161-exact-q-conditional-held-2026-08-26'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
pins={HERE/'referee.py':'0913e09172041702e227d7d781298d041514fe8f5899142180f3f0d8a7a9e9ea',HERE/'results_referee.json':'223b1b2a344f5e8b11b804e084673c407bca91cd976a0d1150dbdb7c7e6577da',HERE/'HELD_APPROVAL.json':'ab2dd9b166383ab6358dcf0ab504c7b96eee7c76db82378e7b09128c422689dc',PKG/'MANIFEST.sha256':'83c87103e2414b48d37724ce803c747ee0d2c9a9f757353c172bb17226477147',PKG/'source_ledger.json':'c34b3616bef36d49c63904e676c540208a24dd2057eb176153ad03034db0b8a6',PKG/'future_dependencies.json':'ab8198b3c9745368e51f1f5c481d81b62823f7255d046a80e3d94a7c2cad0e9c',PKG/'dependency_verifier.py':'b784729f817f2986fac597009b65698e62fc8a0ba944447c21b95cd5dde29ff5',PKG/'run_groups126_161.py':'07281312d1b227c0a629b917485b39c04a976df9bb4fbbf17c2bd92459743407'}
for path,want in pins.items():assert sha(path)==want,(path,sha(path),want)
r=json.loads((HERE/'results_referee.json').read_text());a=json.loads((HERE/'HELD_APPROVAL.json').read_text())
assert r['status']=='PASS_CONDITIONAL_HELD_GROUPS126_161_BLOCKED_ZERO_RUNS' and r['selected_group_ids']==list(range(126,162))
assert r['canonical_sources_verified']==36 and r['total_source_bytes']==66529596 and r['variables_each']==91 and r['generators_each']==6577
assert r['required_future_groups']==[list(range(1,26)),list(range(26,76)),list(range(76,126))] and r['derived_union_if_satisfied']==list(range(126)) and not r['dependency_satisfied'] and r['future_hashes']==[None]*6 and not r['future_files_present']
assert r['runner_replays_all_six_terminal_artifacts_before_attempt'] and r['hostiles_passed']==21 and r['fabricated_or_stale_normalized_rejected'] and r['strict_sequential_stop_first']
assert r['limits_each']=={'native_wall_seconds':240,'wrapper_wall_seconds':250,'rss_cap_bytes':8*1024**3} and r['scope']['solver_runs']==0 and not r['scope']['launch_authorized'] and not r['scope']['mathematical_coverage']
assert a['status'].startswith('PASS_HELD_ONLY_BLOCKED_') and a['selected_group_ids']==list(range(126,162)) and not a['launch_authorized'] and a['solver_runs']==0
for name in ('normalized_dependencies.json','independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):assert not (PKG/name).exists(),name
assert not list(PKG.rglob('*.tmp'))
print(json.dumps({'status':'PASS','held_only':True,'dependencies_satisfied':False,'six_artifacts_replayed_at_launch':True,'groups':[126,161],'sources':36,'solver_runs':0},sort_keys=True))
