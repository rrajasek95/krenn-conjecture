#!/usr/bin/env python3
"""Freeze four null future referee pairs for rep4 all-162 promotion."""
import json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent
def atomic(path,value):tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n');os.replace(tmp,path)
specs=[
 ('groups1_25',range(1,26),'unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26','KRENN_X5_REP4_FIRST25_EXACT_Q_TERMINAL_REFEREE_V1','PASS_ALL_25_EXACT_Q_UNIT_IDEALS'),
 ('groups26_75',range(26,76),'unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26','KRENN_X5_REP4_GROUPS26_75_EXACT_Q_TERMINAL_REFEREE_V1','PASS_ALL_50_EXACT_Q_UNIT_IDEALS'),
 ('groups76_125',range(76,126),'unaudited-codex-n8-x5-rep4-groups76-125-exact-q-terminal-referee-2026-08-26','KRENN_X5_REP4_GROUPS76_125_EXACT_Q_TERMINAL_REFEREE_V1','PASS_ALL_50_EXACT_Q_UNIT_IDEALS'),
 ('groups126_161',range(126,162),'unaudited-codex-n8-x5-rep4-groups126-161-exact-q-terminal-referee-2026-08-26','KRENN_X5_REP4_GROUPS126_161_EXACT_Q_TERMINAL_REFEREE_V1','PASS_ALL_36_EXACT_Q_UNIT_IDEALS')]
deps=[]
for name,groups,directory,schema,status in specs:deps.append({'name':name,'group_ids':list(groups),'manifest_path':f'computations/{directory}/FINAL_MANIFEST.sha256','result_path':f'computations/{directory}/results_referee.json','required_schema':schema,'required_status':status,'manifest_sha256':None,'result_sha256':None,'satisfied':False})
contract={'schema':'KRENN_X5_REP4_ALL162_FUTURE_PASS_DEPENDENCIES_V1','status':'UNSATISFIED_FOUR_NULL_HASH_PAIRS','sealed_group0':True,'dependencies':deps,'satisfied':False,'admission':'all eight future hashes must come from later independent terminal seals; no partial promotion'};atomic(HERE/'future_dependencies.json',contract);print(json.dumps({'status':contract['status'],'dependencies':4,'null_hashes':8},sort_keys=True))
