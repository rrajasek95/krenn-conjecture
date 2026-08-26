#!/usr/bin/env python3
"""Independent held-package referee. Never invokes Singular or producer runners."""
from __future__ import annotations
import ast,hashlib,importlib.util,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PROD=ROOT/'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26'
BASE=ROOT/'computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25'
DESIGN=ROOT/'computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25'
PINS={PROD/'MANIFEST.sha256':'43c34a80cc55488e4840b5d04001211d21f8acbdc6fc62bc5cc5e0e366fc5b0a',PROD/'source_ledger.json':'4aa023638d439fd1250b66593d93dd29dd4472831449ff571e2730bf6950b4ce',PROD/'future_dependencies.json':'5173f8f03b8eb7feff428573cb6a0b2813ef1e6cb1d4c4696543c30585e522e4',PROD/'normalize_dependencies.py':'887762ea499c3dbf8b566987fe1ba234f518e72ba9733f6b96accd4435dee1fb',PROD/'results_hostile_tests.json':'daffe98d8d0b993cd2c77166d5fc50829247317b187415825202b94516de2789',PROD/'run_groups76_125.py':'c1aa9303186a1a1e1efaa867471192b69b746aac52741ad227d901db34cbe24a',BASE/'canonical_census.json':'5ee661f3fdfd0e35e75d92d6efe7700b83011049e1d74a712ba8918681f86c8a',DESIGN/'generate_design.py':'ca23dbcb4179753393b7b0b3cd81d5c73d2c1bd26da559b00ca5136524aa83dc'}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def atomic(path,value):tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n');os.replace(tmp,path)
for path,want in PINS.items():assert path.is_file() and sha(path)==want,(path,sha(path),want)
# Replay the producer seal exactly.
manifest_lines=0
for line in (PROD/'MANIFEST.sha256').read_text().splitlines():
 digest,name=line.split('  ',1);path=(PROD/name).resolve();assert path.is_file() and sha(path)==digest,name;manifest_lines+=1
assert manifest_lines==64
ledger=json.loads((PROD/'source_ledger.json').read_text());future=json.loads((PROD/'future_dependencies.json').read_text());hostiles=json.loads((PROD/'results_hostile_tests.json').read_text())
assert ledger['selection']['selected_group_ids']==list(range(76,126)) and ledger['selection']['required_closed_union']==list(range(76)) and len(ledger['lanes'])==50
assert future['status']=='UNSATISFIED_BOTH_NULL_HASH_PAIRS' and future['satisfied'] is False and future['required_closed_union']==list(range(76))
assert [d['groups_closed'] for d in future['dependencies']]==[list(range(1,26)),list(range(26,76))]
assert all(d['satisfied'] is False and d['manifest_sha256'] is d['result_sha256'] is None for d in future['dependencies'])
future_absence=[]
for dep in future['dependencies']:
 for key in ('manifest_path','result_path'):
  path=ROOT/dep[key];future_absence.append(str(path.relative_to(ROOT)));assert not path.exists(),path
assert hostiles['status']=='PASS_16_HOSTILES_BOTH_FUTURES_ABSENT' and len(hostiles['tests'])==16 and all(hostiles['tests'].values())
# Independently regenerate every exact-Q source from the pinned census/design.
census=json.loads((BASE/'canonical_census.json').read_text());spec=importlib.util.spec_from_file_location('independent_rep2_design',DESIGN/'generate_design.py');assert spec and spec.loader;m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);engine=m.load_engine();m.configure_engine(engine)
ep='''ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'''
source_bytes=0
for ordinal,gid in enumerate(range(76,126),1):
 lane=ledger['lanes'][ordinal-1];record=census['groups'][gid];assert lane['ordinal']==ordinal and lane['group_id']==gid and lane['canonical_chart']==record['canonical_chart'] and lane['variables']==91 and lane['generators']==6577
 q=m.build_program(engine,tuple(record['canonical_chart']));assert q.endswith('quit;\n') and q.count('quit;')==1;q=q[:-len('quit;\n')]+ep;data=q.encode();digest=hashlib.sha256(data).hexdigest();source=PROD/lane['source_path']
 assert digest==record['exact_Q_source_sha256']==lane['source_sha256']==sha(source) and len(data)==record['exact_Q_source_bytes']==lane['source_bytes']==source.stat().st_size;source_bytes+=len(data)
assert source_bytes==92375820
# Re-exercise the sealed adapter, then show the runner accepts its shape without reopening provenance.
adapter_spec=importlib.util.spec_from_file_location('producer_adapter',PROD/'normalize_dependencies.py');assert adapter_spec and adapter_spec.loader;adapter=importlib.util.module_from_spec(adapter_spec);adapter_spec.loader.exec_module(adapter)
first={'schema':future['dependencies'][0]['result_schema'],'status':future['dependencies'][0]['result_status'],'groups_closed':list(range(1,26))};middle={'schema':future['dependencies'][1]['result_schema'],'status':future['dependencies'][1]['result_status'],'groups_closed':list(range(26,76))}
fake_m=['a'*64,'b'*64];fake_r=['c'*64,'d'*64];fabricated=adapter.validate_payload(future,first,middle,fake_m,fake_r)
assert fabricated['status']=='PASS_NORMALIZED_EXACT_CLOSED_UNION_0_75' and fabricated['closed_union']==list(range(76)) and fabricated['duplicates']==fabricated['missing']==fabricated['extra']==[]
assert fabricated['dependency_manifest_sha256']==fake_m and fabricated['dependency_result_sha256']==fake_r and all(not (ROOT/p).exists() for p in fabricated['dependency_manifest_paths']+fabricated['dependency_result_paths'])
runner=(PROD/'run_groups76_125.py').read_text();ast.parse(runner)
assert "dependency['dependency_manifest_paths']" not in runner and "dependency['dependency_result_paths']" not in runner and 'ROOT/' not in runner
assert "len(dependency['dependency_manifest_sha256'])" in runner and "all(len(x)==64" in runner
runner_shape_accepts=(fabricated['schema']=='KRENN_X5_REP2_GROUPS76_125_NORMALIZED_DEPENDENCIES_V1' and fabricated['status']=='PASS_NORMALIZED_EXACT_CLOSED_UNION_0_75' and fabricated['groups_closed_by_first']==list(range(1,26)) and fabricated['groups_closed_by_middle']==list(range(26,76)) and fabricated['closed_union']==list(range(76)) and fabricated['duplicates']==fabricated['missing']==fabricated['extra']==[] and len(fabricated['dependency_manifest_sha256'])==len(fabricated['dependency_result_sha256'])==2 and all(len(x)==64 for x in fabricated['dependency_manifest_sha256']+fabricated['dependency_result_sha256']))
assert runner_shape_accepts
atomic(HERE/'fabricated_stale_normalized_countermodel.json',{'schema':'KRENN_X5_REP2_GROUPS76_125_STALE_NORMALIZED_COUNTERMODEL_V1','status':'PASS_COUNTERMODEL_RUNNER_DEPENDENCY_SHAPE_ACCEPTS_WITH_ALL_ARTIFACTS_ABSENT','normalized_payload':fabricated,'all_dependency_artifacts_absent':True,'runner_shape_accepts':True,'runner_reopens_manifest_paths':False,'runner_reopens_result_paths':False,'solver_runs':0})
for name in ('normalized_dependencies.json','independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):assert not (PROD/name).exists(),name
result={'schema':'KRENN_X5_REP2_GROUPS76_125_CONDITIONAL_INDEPENDENT_REFEREE_V1','status':'REJECT_HELD_RUNNER_DOES_NOT_REPLAY_DEPENDENCY_ARTIFACTS_ZERO_COVERAGE','producer_manifest_sha256':PINS[PROD/'MANIFEST.sha256'],'producer_manifest_lines_replayed':manifest_lines,'source_ledger_sha256':PINS[PROD/'source_ledger.json'],'authoritative_census_sha256':PINS[BASE/'canonical_census.json'],'adapter_sha256':PINS[PROD/'normalize_dependencies.py'],'runner_sha256':PINS[PROD/'run_groups76_125.py'],'sources_regenerated':50,'source_bytes':source_bytes,'source_mismatches':0,'future_dependency_pairs':2,'future_hashes_null':4,'future_artifacts_absent':future_absence,'producer_hostiles_passed':16,'new_counter_hostile':'fabricated/stale normalized payload with four 64-hex hashes passes every runner dependency assertion while all four artifacts are absent','runner_replay_gap':{'manifest_paths_reopened':False,'result_paths_reopened':False,'hashes_compared_to_files':False,'schema_status_groups_union_checked':True},'zero_run':{'singular_invocations':0,'producer_normalized_present':False,'producer_acceptance_present':False,'producer_clearance_present':False,'producer_attempt_present':False,'producer_results_present':False,'mathematical_coverage_added':False},'verdict':'held approval refused; supersede runner to reopen and hash all four dependency artifacts before acceptance/attempt/solve'}
atomic(HERE/'results_independent_referee.json',result);print(json.dumps({'status':result['status'],'sources_regenerated':50,'new_counter_hostile':'PASS','solver_runs':0},sort_keys=True))
