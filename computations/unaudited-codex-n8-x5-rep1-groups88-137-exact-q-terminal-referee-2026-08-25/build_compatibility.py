#!/usr/bin/env python3
"""Exact field/path compatibility alias for the audited groups88..137 terminal."""
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PROD=ROOT/'computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-conditional-held-2026-08-25';AUDIT=ROOT/'computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-terminal-referee-2026-08-26'
PINS={PROD/'batch_result.json':'a26b032d7f5c59df4106944daf71b98dfd87eea05340f844ee4e004c7e9e64a5',PROD/'TERMINAL_MANIFEST.sha256':'4fa50b0e3e02425e714da9669f6dd1e7678738881c824cf3583247b975123127',AUDIT/'results_referee.json':'1de758a809cc4563313d872413f8e505153754b96df57499d11057e45e8f8789',AUDIT/'FINAL_MANIFEST.sha256':'23d2a55826b7f211298f9dd9a071aae1e17e6e95df3964b3d3825b98c2e8b32e'}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def replay(manifest):
 for line in manifest.read_text().splitlines():
  digest,name=line.split(None,1);path=(manifest.parent/name.strip()).resolve();assert path.is_file() and sha(path)==digest,(path,digest)
def atomic(path,value):tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n');os.replace(tmp,path)
for path,want in PINS.items():assert sha(path)==want,(path,sha(path),want)
replay(PROD/'TERMINAL_MANIFEST.sha256');replay(AUDIT/'FINAL_MANIFEST.sha256')
audit=json.loads((AUDIT/'results_referee.json').read_text());batch=json.loads((PROD/'batch_result.json').read_text())
assert audit['schema']=='KRENN_X5_REP1_GROUPS88_137_EXACT_Q_TERMINAL_REFEREE_V1' and audit['status']=='PASS_ALL_50_EXACT_Q_UNIT_IDEALS'
assert audit['new_groups_closed']==50 and audit['strict_order'] and not audit['parallel'] and not audit['skipped'] and not audit['relaunch']
assert audit['dependency_closed_union_before_batch']==list(range(88)) and audit['groups_closed']==list(range(88,138)) and audit['closed_union_after_batch']==list(range(138))
assert batch['status']=='PASS_ALL_50_UNIT' and batch['strict_order']==list(range(88,138)) and [x['group_id'] for x in batch['completed']]==list(range(88,138)) and batch['stop'] is None and batch['skipped_after_stop']==[] and not batch['parallel'] and not batch['relaunch']
result={'schema':'KRENN_X5_REP1_GROUPS88_137_EXACT_Q_TERMINAL_REFEREE_V1','status':'PASS_ALL_50_EXACT_Q_UNIT_IDEALS','new_groups_closed':50,'strict_order':True,'parallel':False,'skipped':False,'relaunch':False,'baseline_closed_union':list(range(88)),'groups_closed':list(range(88,138)),'closed_union':list(range(138)),'compatibility_only':True,'field_map':{'baseline_closed_union':'audited dependency_closed_union_before_batch','closed_union':'audited closed_union_after_batch'},'underlying_producer_batch_sha256':PINS[PROD/'batch_result.json'],'underlying_producer_terminal_manifest_sha256':PINS[PROD/'TERMINAL_MANIFEST.sha256'],'underlying_audit_result_sha256':PINS[AUDIT/'results_referee.json'],'underlying_audit_manifest_sha256':PINS[AUDIT/'FINAL_MANIFEST.sha256'],'solver_runs_added':0,'mathematical_coverage_added':False}
atomic(HERE/'results_referee.json',result);print(json.dumps({'status':'PASS_EXACT_INTERFACE_COMPATIBILITY_ALIAS','result_sha256':sha(HERE/'results_referee.json'),'closed_union':138,'solver_runs_added':0},sort_keys=True))
