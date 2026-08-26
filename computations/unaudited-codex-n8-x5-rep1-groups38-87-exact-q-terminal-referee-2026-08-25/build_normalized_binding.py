#!/usr/bin/env python3
"""Normalize the sealed groups38..87 terminal into the dependency interface."""
from __future__ import annotations
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PROD=ROOT/'computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-2026-08-25'
REF=ROOT/'computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-terminal-referee-2026-08-25'
PINS={PROD/'MANIFEST.sha256':'7b66f582d1edf79e1e75c4ca328808f3f77548f840f5c42cc082dcd0f53764da',PROD/'TERMINAL_MANIFEST.sha256':'fe4d9f2a1dcb54e0b15b660bfef6d52aca1fe1cb7960246e0958a5e95380cc92',PROD/'batch_result.json':'006893f6da40d00fe96df9f09ad2617e5a16edd7ac8677fe19ceec0991fd7a0b',PROD/'normalized_next25_dependency.json':'29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76',REF/'FINAL_MANIFEST.sha256':'a1aeb1444dcfdde38db7eb80d9759b360da1da66b4c456f4d371f2a8915dae7d',REF/'results_referee.json':'f6ab9c40f6909b057beb40dcf4a19f28f59df60521a16f1524cf85980e2871e4'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,v):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n');os.replace(t,p)
for p,h in PINS.items():assert sha(p)==h,(p,sha(p),h)
baseline=json.loads((PROD/'normalized_next25_dependency.json').read_text());batch=json.loads((PROD/'batch_result.json').read_text());ref=json.loads((REF/'results_referee.json').read_text())
assert baseline['closed_union']==list(range(38))
assert batch['schema']=='KRENN_X5_REP1_NEXT50_NORMALIZED_BATCH_RESULT_V2' and batch['status']=='PASS_ALL_50_UNIT'
assert batch['strict_order']==list(range(38,88)) and [x['group_id'] for x in batch['completed']]==list(range(38,88)) and all(x['status']=='UNIT_IDEAL_EXACT_Q' for x in batch['completed']) and batch['stop'] is None and batch['parallel'] is False and batch['relaunch'] is False
assert ref['schema']=='KRENN_X5_REP1_NEXT50_NORMALIZED_EXACT_Q_TERMINAL_REFEREE_V1' and ref['status']=='PASS_ALL_50_EXACT_Q_UNIT_IDEALS'
assert ref['groups_closed']==list(range(38,88)) and ref['closed_union_after_batch']==list(range(88)) and ref['new_groups_closed']==50 and ref['strict_order'] is True and ref['parallel'] is False and ref['skipped'] is False and ref['relaunch'] is False
out={'schema':'KRENN_X5_REP1_GROUPS38_87_EXACT_Q_TERMINAL_REFEREE_V1','status':'PASS_ALL_50_EXACT_Q_UNIT_IDEALS','new_groups_closed':50,'strict_order':True,'parallel':False,'skipped':False,'relaunch':False,'baseline_closed_union':list(range(38)),'groups_closed':list(range(38,88)),'closed_union':list(range(88)),'normalization_only':True,'pins':{str(p.relative_to(ROOT)):h for p,h in PINS.items()},'scope':{'solver_runs':0,'new_arithmetic':False,'groups_newly_closed_by_binding':0}}
atomic(HERE/'results_referee.json',out)
print(json.dumps({'status':out['status'],'groups':50,'union':88,'runs':0},sort_keys=True))
