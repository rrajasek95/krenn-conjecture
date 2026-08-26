#!/usr/bin/env python3
import hashlib,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
pins={'build_binding.py':'36c207114037d67eb237e17f1a575adbff06499bb1ca3fc7aaf291918faa7c7f','results_binding.json':'90eebf42db7a07ccf87f8dd3f6ee58603414292921eac55e542b42f44cddeba0','normalized_dependency_v2.json':'e9da3672ec4ca72278764f4cc8aabc1441f9a7cbd37b41a79c3c6fc4cc4ad550','HELD_ACCEPTANCE_V2.json':'7004526b14842c7efed72fb4f266aae5741a3f530dfad0b2b98d7386872eaef6','held_acceptance_v2.schema.json':'e7e453429dd935a927cb52a21f24cfa8938be0f734b28f73f3415ef24c3aeb49','referee.py':'7822d863a0bcca064068b3e1072f0a766d994da314c7a7b20498d6e99611704a','results_referee.json':'b8529f9026af64c20325b6c05fbd649ddfd7a9d5a1e8009fe9a598242c40a5f7'}
for name,want in pins.items():assert sha(HERE/name)==want,(name,sha(HERE/name),want)
r=json.loads((HERE/'results_referee.json').read_text());a=json.loads((HERE/'HELD_ACCEPTANCE_V2.json').read_text());d=json.loads((HERE/'normalized_dependency_v2.json').read_text())
assert r['status']=='PASS_HELD_LAUNCH_READY_EXACT_UNION_0_137_ZERO_RUNS_NO_CLEARANCE' and r['closed_union']==list(range(138)) and r['selected_group_ids']==list(range(138,162)) and r['sources_preserved']==24 and r['source_bytes']==42769236
assert d['baseline_closed_union']==list(range(88)) and d['future_groups_closed']==list(range(88,138)) and d['closed_union']==list(range(138)) and d['set_proof']['intersection']==d['set_proof']['missing']==d['set_proof']['extra']==d['set_proof']['duplicates']==[]
assert a['selected_group_ids']==list(range(138,162)) and a['required_closed_union']==list(range(138)) and a['maximum_lane_count']==24 and not a['parallel_authorized'] and not a['skip_reorder_relaunch_authorized']
assert r['scope']=={'held_launch_ready':True,'launch_clearance_materialized':False,'launch_authorized_now':False,'solver_runs':0,'new_arithmetic':False,'mathematical_coverage_added':False}
print(json.dumps({'status':'PASS','held_launch_ready':True,'closed_union':138,'selected':[138,161],'solver_runs':0,'clearance':False},sort_keys=True))
