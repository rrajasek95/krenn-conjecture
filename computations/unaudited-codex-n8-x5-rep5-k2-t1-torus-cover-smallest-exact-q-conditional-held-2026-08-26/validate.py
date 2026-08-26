#!/usr/bin/env python3
"""Validate the conditional held exact-Q package without invoking Singular."""
from __future__ import annotations
import ast,hashlib,json,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=H/'rep5_k2_t1_torus_smallest_Q_base.sing';runtime=H/'rep5_k2_t1_torus_smallest_Q.sing'
assert sha(base)=='13c204f73bb82e263267ec977c19a10dba045541921375c2e7568ba48d5baba0'
assert sha(runtime)=='4c788634af62bf0a98a2e8ddc2ab337baca292081ecc48f955c3622b87aff637'
strong=b'''print("INPUT_GENERATORS="+string(size(I)));
ideal G=slimgb(I);
print("GROEBNER_SIZE="+string(size(G)));
poly remainder=reduce(1,G);
print("UNIT_REMAINDER="+string(remainder));
if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }
quit;
''';old=b'print("INPUT_GENERATORS="+string(size(I)));\nquit;\n'
assert runtime.read_bytes().replace(strong,old,1)==base.read_bytes()
for script in ('run_one_lane.py','verify_future_dependency.py','hostile_tests.py','validate.py','seal_manifest.py','build_source.py'):
 ast.parse((H/script).read_text())
for raw in (H/'EXTERNAL_PINS.sha256').read_text().splitlines():
 m=re.fullmatch(r'([0-9a-f]{64})  (.+)',raw);assert m
 d,relative=m.groups();target=(H/relative).resolve(strict=True);assert ROOT in target.parents and sha(target)==d
plan=json.loads((H/'held_plan.json').read_text());contract=json.loads((H/'future_dependency_contract.json').read_text())
assert plan['status'].startswith('HELD_ZERO_RUN')
assert plan['source']['base_Q_sha256']==sha(base) and plan['source']['sha256']==sha(runtime)
assert plan['source']['assignment']=={'t0':1,'t2':0,'yn1':1,'yn2':1}
assert plan['scope']=={'attempts':0,'mathematical_coverage':False,'other_charts':0,'prior_timeout_reused':False,'solver_runs':0}
assert all(v is None for v in contract['future_hashes'].values()) and all(v is None for v in contract['future_paths'].values())
for schema_name in ('independent_referee_acceptance.schema.json','launch_clearance.schema.json'):
 schema=json.loads((H/schema_name).read_text());assert schema['additionalProperties'] is False and set(schema['required'])==set(schema['properties'])
for absent in ('future_modular_unit_dependency.json','independent_referee_acceptance.json','launch_clearance.json','ATTEMPT.json','result.json','result.json.tmp','RUN_EXCLUSIVE.lock','stdout.log','stderr.log','watchdog.json'):
 assert not (H/absent).exists(),absent
assert not list(H.glob('*.tmp')) and not list(H.rglob('__pycache__'))
attempt=subprocess.run([sys.executable,str(H/'hostile_tests.py')],cwd=H,capture_output=True,text=True,timeout=15,check=True)
hostile=json.loads((H/'results_hostiles.json').read_text());assert hostile['status']=='PASS' and hostile['solver_runs']==0 and hostile['runner_refused_before_attempt'] is True
result={'schema':'KRENN_X5_REP5_TORUS_SMALLEST_SAME_CHART_EXACT_Q_CONDITIONAL_VALIDATION_V1','status':'PASS_ZERO_RUN_FAIL_CLOSED','dependency':{'future_binding_absent':True,'future_hashes_null':True,'future_paths_null':True,'independent_modular_unit_required':True},'execution':{'maximum_lane_count':1,'native_wall_seconds':480,'wrapper_wall_seconds':510,'rss_cap_bytes':8589934592,'direct_libproc_group_rss':True,'atomic':True,'stop_any':True},'hostile_count':hostile['hostile_count'],'pins':{'base_Q_sha256':sha(base),'runtime_Q_sha256':sha(runtime),'modular_held_manifest_sha256':plan['pins']['modular_held_manifest_sha256'],'modular_referee_manifest_sha256':plan['pins']['modular_held_referee_manifest_sha256'],'prior_timeout_manifest_sha256':plan['pins']['prior_timeout_referee_manifest_sha256']},'scope':{'solver_runs':0,'attempts':0,'mathematical_coverage':False,'rep5_closed':False}}
(H/'results_validation.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))
