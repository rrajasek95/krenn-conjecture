#!/usr/bin/env python3
"""Build held v2 acceptance metadata for the now-satisfied 0..87 dependency."""
from __future__ import annotations
import hashlib,importlib.util,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
HELD=ROOT/'computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-conditional-held-2026-08-25'
HELD_REF=ROOT/'computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-conditional-held-referee-2026-08-25'
PROD=ROOT/'computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-2026-08-25'
TERM_REF=ROOT/'computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-terminal-referee-2026-08-25'
ALIAS=ROOT/'computations/unaudited-codex-n8-x5-rep1-groups38-87-exact-q-terminal-referee-2026-08-25'
PINS={HELD/'MANIFEST.sha256':'07ab0d198fc80b91025df7c892081f2aaaa94158014052246d7700095c054450',HELD/'source_ledger.json':'2d111140f7508cd2548f8d26f73352b454e8dd80d2fbe4056f55819b62dd239b',HELD/'run_groups88_137.py':'604b0b938389e44506d627eba8652d74cfe3d3ba10a932efcb6c4dbfeee987e5',HELD/'normalize_future_dependency.py':'87ef24aa0e88434fa01d336e86736e0d6d60925323f08b2ae7fdec9b3bb7a64a',HELD/'future_groups38_87_dependency.json':'1374fb5ed562ac0fd6b28ace616e09fbf011509555b02cb98996281d7188b380',HELD_REF/'results_referee.json':'cb9e28e03a6f3449cec78d344e7964c0fd90bd20bb4668ffa0bab1b156fe0bbf',HELD_REF/'HELD_APPROVAL.json':'e2bcfd41206c316487d8372bf5ccd56439381909fe3ff3cf50b4ca3c5238a519',HELD_REF/'FINAL_MANIFEST.sha256':'f664aa999331fa81309a5df1b69d17d3b32d2d3783d44e833b856bc803c60e39',PROD/'batch_result.json':'006893f6da40d00fe96df9f09ad2617e5a16edd7ac8677fe19ceec0991fd7a0b',PROD/'TERMINAL_MANIFEST.sha256':'fe4d9f2a1dcb54e0b15b660bfef6d52aca1fe1cb7960246e0958a5e95380cc92',PROD/'normalized_next25_dependency.json':'29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76',TERM_REF/'results_referee.json':'f6ab9c40f6909b057beb40dcf4a19f28f59df60521a16f1524cf85980e2871e4',TERM_REF/'FINAL_MANIFEST.sha256':'a1aeb1444dcfdde38db7eb80d9759b360da1da66b4c456f4d371f2a8915dae7d',ALIAS/'results_referee.json':'42e13d3e2103283e80f4f91af4d8433e21dc482435b945b3c252fa13452e7763',ALIAS/'FINAL_MANIFEST.sha256':'e6987baa4abf37de21e0466932f554ab9272da8a775ae89e5e25cfadd7ba17fc'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,v):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n');os.replace(t,p)
for p,h in PINS.items():assert sha(p)==h,(p,sha(p),h)
spec=importlib.util.spec_from_file_location('sealed_groups88_dependency_adapter',HELD/'normalize_future_dependency.py');assert spec and spec.loader
adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
normalized=adapter.load_and_normalize(PINS[ALIAS/'FINAL_MANIFEST.sha256'],PINS[ALIAS/'results_referee.json'])
assert normalized['status']=='PASS_DERIVED_EXACT_CLOSED_UNION_0_87' and normalized['baseline_closed_union']==list(range(38)) and normalized['future_groups_closed']==list(range(38,88)) and normalized['closed_union']==list(range(88))
ledger=json.loads((HELD/'source_ledger.json').read_text());assert [x['group_id'] for x in ledger['lanes']]==list(range(88,138))
for lane in ledger['lanes']:
 p=HELD/lane['source_path'];assert sha(p)==lane['source_sha256'] and p.stat().st_size==lane['source_bytes']
assert sum(x['source_bytes'] for x in ledger['lanes'])==89221428
dependency={'schema':'KRENN_X5_REP1_GROUPS88_137_SATISFIED_DEPENDENCY_V2','status':'PASS_EXACT_NORMALIZED_CLOSED_UNION_0_87','baseline_closed_union':list(range(38)),'future_groups_closed':list(range(38,88)),'closed_union':list(range(88)),'set_proof':{'baseline_count':38,'future_count':50,'intersection':[],'union_count':88,'missing':[],'extra':[],'duplicates':[]},'terminal_binding':{'manifest_sha256':PINS[ALIAS/'FINAL_MANIFEST.sha256'],'result_sha256':PINS[ALIAS/'results_referee.json']},'underlying_terminal':{'producer_batch_sha256':PINS[PROD/'batch_result.json'],'producer_terminal_manifest_sha256':PINS[PROD/'TERMINAL_MANIFEST.sha256'],'referee_result_sha256':PINS[TERM_REF/'results_referee.json'],'referee_manifest_sha256':PINS[TERM_REF/'FINAL_MANIFEST.sha256']}}
atomic(HERE/'normalized_dependency_v2.json',dependency)
acceptance={'schema':'KRENN_X5_REP1_GROUPS88_137_EXACT_Q_SATISFIED_DEPENDENCY_HELD_ACCEPTANCE_V2','status':'PASS_HELD_LAUNCH_READY_DEPENDENCY_SATISFIED_NO_CLEARANCE','held_manifest_sha256':PINS[HELD/'MANIFEST.sha256'],'held_referee_result_sha256':PINS[HELD_REF/'results_referee.json'],'held_referee_approval_sha256':PINS[HELD_REF/'HELD_APPROVAL.json'],'held_referee_manifest_sha256':PINS[HELD_REF/'FINAL_MANIFEST.sha256'],'source_ledger_sha256':PINS[HELD/'source_ledger.json'],'runner_sha256':PINS[HELD/'run_groups88_137.py'],'dependency_spec_sha256':PINS[HELD/'future_groups38_87_dependency.json'],'dependency_adapter_sha256':PINS[HELD/'normalize_future_dependency.py'],'terminal_binding_manifest_sha256':PINS[ALIAS/'FINAL_MANIFEST.sha256'],'terminal_binding_result_sha256':PINS[ALIAS/'results_referee.json'],'underlying_terminal_producer_batch_sha256':PINS[PROD/'batch_result.json'],'underlying_terminal_producer_manifest_sha256':PINS[PROD/'TERMINAL_MANIFEST.sha256'],'underlying_terminal_referee_result_sha256':PINS[TERM_REF/'results_referee.json'],'underlying_terminal_referee_manifest_sha256':PINS[TERM_REF/'FINAL_MANIFEST.sha256'],'required_closed_union':list(range(88)),'selected_group_ids':list(range(88,138)),'maximum_lane_count':50,'exact_Q_authorized':True,'parallel_authorized':False,'skip_reorder_relaunch_authorized':False,'launch_clearance_required':True,'launch_clearance_materialized':False,'solver_runs':0}
atomic(HERE/'HELD_ACCEPTANCE_V2.json',acceptance)
props={k:{'const':v} for k,v in acceptance.items()}
schema={'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','additionalProperties':False,'required':list(props),'properties':props}
atomic(HERE/'held_acceptance_v2.schema.json',schema)
result={'schema':'KRENN_X5_REP1_GROUPS88_137_SATISFIED_DEPENDENCY_BINDING_V2','status':'PASS_HELD_LAUNCH_READY_ZERO_RUNS_NO_CLEARANCE','normalized_dependency':dependency,'held_acceptance':acceptance,'preservation':{'source_count':50,'source_bytes':89221428,'source_ledger_sha256_unchanged':PINS[HELD/'source_ledger.json'],'runner_sha256_unchanged':PINS[HELD/'run_groups88_137.py'],'all_source_hashes_replayed':True},'pins':{str(p.relative_to(ROOT)):h for p,h in PINS.items()},'scope':{'solver_runs':0,'new_arithmetic':False,'source_files_rewritten':0,'runner_rewritten':False,'launch_clearance_materialized':False,'mathematical_coverage_added':False}}
atomic(HERE/'results_binding.json',result)
print(json.dumps({'status':result['status'],'closed_union':88,'sources_preserved':50,'runs':0,'clearance':False},sort_keys=True))
