#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
def s(p):return hashlib.sha256(p.read_bytes()).hexdigest()
h=json.loads((H/'held_pilot.json').read_text());assert h['status']=='HELD_FRESH_ZERO_RUN_PENDING_INDEPENDENT_AUDIT'
assert s(H/'rep4_all_equal_y_i0_p00_x0_y0_d01_p32003.sing')=='9471d6bbfb0af012c313cafa97e12f5b3cea380e6cefb0c8f355cb53def80524'
assert s(H/'run_one_lane.py')=='975cb4baa7ca06fb1471fdd883a75ba2e27d61983a5ff5669676a0835242f2f0'
r=(H/'run_one_lane.py').read_text();compile(r,str(H/'run_one_lane.py'),'exec')
assert 'returned // ctypes.sizeof' not in r
for x in ('proc_listallpids','proc_pidpath','proc_listpgrppids','range(count)','rusage observation failure for live group member','[str(GTIMEOUT), "--signal=TERM"','f"{WRAPPER_WALL}s"','MAX_CLEARANCE_LIFETIME_SECONDS = 600','exclusive_json(HERE / "ATTEMPT.json"','not (HERE / stale).exists()'):assert x in r,x
for n in ('independent_referee_acceptance.schema.json','launch_clearance.schema.json'):
 q=json.loads((H/n).read_text());assert q['additionalProperties'] is False and set(q['required'])==set(q['properties'])
assert json.loads((H/'refusal_contract.json').read_text())['old_execution_artifacts_reused'] is False
for n in ('independent_referee_acceptance.json','launch_clearance.json','ATTEMPT.json','result.json','result.json.tmp','stdout.log','stderr.log','watchdog.json'):assert not (H/n).exists(),n
assert not any(H.glob('*.tmp'))
print(json.dumps({'status':'PASS_FRESH_V2_HELD_ZERO_RUN','source_sha256':s(H/'rep4_all_equal_y_i0_p00_x0_y0_d01_p32003.sing'),'runner_sha256':s(H/'run_one_lane.py'),'old_artifacts_reused':False},sort_keys=True))
