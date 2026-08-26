#!/usr/bin/env python3
"""Materialize the null-hash two-stage dependency contract; never solve."""
import json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent
def atomic(path,value):
 tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n');os.replace(tmp,path)
deps=[
 {'name':'groups1_25','manifest_path':'computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256','result_path':'computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26/results_referee.json','result_schema':'KRENN_X5_REP4_FIRST25_EXACT_Q_TERMINAL_REFEREE_V1','result_status':'PASS_ALL_25_EXACT_Q_UNIT_IDEALS','groups_closed':list(range(1,26)),'manifest_sha256':None,'result_sha256':None,'satisfied':False},
 {'name':'groups26_75','manifest_path':'computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256','result_path':'computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26/results_referee.json','result_schema':'KRENN_X5_REP4_GROUPS26_75_EXACT_Q_TERMINAL_REFEREE_V1','result_status':'PASS_ALL_50_EXACT_Q_UNIT_IDEALS','groups_closed':list(range(26,76)),'manifest_sha256':None,'result_sha256':None,'satisfied':False}]
contract={'schema':'KRENN_X5_REP4_GROUPS76_125_FUTURE_DEPENDENCIES_V1','status':'UNSATISFIED_BOTH_NULL_HASH_PAIRS','baseline_closed_group':0,'required_closed_union':list(range(76)),'dependencies':deps,'satisfied':False,'admission':'both future manifests and results must exist, replay exactly, match strict schemas/statuses/group lists, and normalize to duplicate-free union 0..75; null hashes never authorize execution'}
atomic(HERE/'future_dependencies.json',contract)
print(json.dumps({'status':contract['status'],'dependencies':2,'null_hashes':4},sort_keys=True))
