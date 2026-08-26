#!/usr/bin/env python3
import ast,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
pins={'future_dependencies.json':'5173f8f03b8eb7feff428573cb6a0b2813ef1e6cb1d4c4696543c30585e522e4','source_ledger.json':'4aa023638d439fd1250b66593d93dd29dd4472831449ff571e2730bf6950b4ce','normalize_dependencies.py':'887762ea499c3dbf8b566987fe1ba234f518e72ba9733f6b96accd4435dee1fb','results_hostile_tests.json':'daffe98d8d0b993cd2c77166d5fc50829247317b187415825202b94516de2789','run_groups76_125.py':'c1aa9303186a1a1e1efaa867471192b69b746aac52741ad227d901db34cbe24a','held_schedule.json':'112db75eff06f88ba3eec339db97166cad05b3ab795569f83b62423653e3e169'}
for name,want in pins.items():assert sha(HERE/name)==want,(name,sha(HERE/name),want)
future=json.loads((HERE/'future_dependencies.json').read_text());assert future['status']=='UNSATISFIED_BOTH_NULL_HASH_PAIRS' and future['satisfied'] is False and future['required_closed_union']==list(range(76))
assert len(future['dependencies'])==2 and all(not d['satisfied'] and d['manifest_sha256'] is d['result_sha256'] is None for d in future['dependencies'])
for dep in future['dependencies']:assert not (ROOT/dep['manifest_path']).exists() and not (ROOT/dep['result_path']).exists()
ledger=json.loads((HERE/'source_ledger.json').read_text());lanes=ledger['lanes'];assert ledger['selection']['selected_group_ids']==list(range(76,126)) and len(lanes)==50
assert [x['ordinal'] for x in lanes]==list(range(1,51)) and sum(x['source_bytes'] for x in lanes)==92375820
for lane in lanes:
 path=HERE/lane['source_path'];assert sha(path)==lane['source_sha256'] and path.stat().st_size==lane['source_bytes'] and lane['variables']==91 and lane['generators']==6577
hostile=json.loads((HERE/'results_hostile_tests.json').read_text());assert hostile['status']=='PASS_16_HOSTILES_BOTH_FUTURES_ABSENT' and len(hostile['tests'])==16 and all(hostile['tests'].values()) and hostile['solver_runs']==0
schedule=json.loads((HERE/'held_schedule.json').read_text());assert schedule['execution']['order']==list(range(76,126)) and schedule['execution']['maximum_lane_count']==50 and schedule['execution']['native_wall_seconds_each']==240 and schedule['execution']['wrapper_wall_seconds_each']==250 and schedule['execution']['rss_cap_bytes_each']==8*1024**3
assert not any(schedule['execution'][k] for k in ('parallel','skip','reorder','relaunch')) and schedule['scope']['solver_launches']==schedule['scope']['result_files']==schedule['scope']['groups_newly_closed']==0
runner=(HERE/'run_groups76_125.py').read_text();ast.parse(runner);assert runner.count('subprocess.Popen(')==1 and runner.index("assert NORMALIZED.is_file()")<runner.index("exclusive(HERE/'BATCH_ATTEMPT.json'")<runner.index('subprocess.Popen(')
for name in ('normalized_dependencies.json','independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):assert not (HERE/name).exists(),name
assert not list(HERE.rglob('*.tmp'))
print(json.dumps({'status':'PASS_HELD_BOTH_DEPENDENCIES_ABSENT','selected':[76,125],'sources':50,'hostiles':16,'solver_runs':0},sort_keys=True))
