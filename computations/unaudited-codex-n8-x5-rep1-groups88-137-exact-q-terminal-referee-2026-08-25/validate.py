#!/usr/bin/env python3
import hashlib,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
assert sha(HERE/'build_compatibility.py')=='16ef3dc703b2f68ff2f74a9e539c2f409cc8e6f4cf9878d1a638f9a80311be72'
assert sha(HERE/'results_referee.json')=='fd0c8ecb6b8ea1939819094b0f7734fc80fee7782754ff4df6c7f4a652c0cbb8'
x=json.loads((HERE/'results_referee.json').read_text());assert x['schema']=='KRENN_X5_REP1_GROUPS88_137_EXACT_Q_TERMINAL_REFEREE_V1' and x['status']=='PASS_ALL_50_EXACT_Q_UNIT_IDEALS'
assert x['baseline_closed_union']==list(range(88)) and x['groups_closed']==list(range(88,138)) and x['closed_union']==list(range(138))
assert x['compatibility_only'] and x['solver_runs_added']==0 and not x['mathematical_coverage_added']
print(json.dumps({'status':'PASS_EXACT_INTERFACE_COMPATIBILITY_ALIAS','closed_union':138,'solver_runs_added':0},sort_keys=True))
