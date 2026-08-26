#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(name): return hashlib.sha256((HERE/name).read_bytes()).hexdigest()
r=json.loads((HERE/'result.json').read_text())
a=json.loads((HERE/'terminal_audit.json').read_text())
assert sha('result.json')=='03b0ea4377d26e2e8a50c7ac513e16f72ebee2f5fd260627c89de87376ddf9bd'
assert r['source_sha256']=='9471d6bbfb0af012c313cafa97e12f5b3cea380e6cefb0c8f355cb53def80524'
assert r['runner_sha256']=='1a0bee89d2f15cfaa82ad25110dc005952deb0bbbf696530e8e435a328065e7f'
assert r['returncode']==0 and r['termination'] is None and r['stderr']==''
for token in ('INPUT_VARIABLES=91','INPUT_GENERATORS=6577','GROEBNER_SIZE=1','UNIT_REMAINDER=0','STATUS=UNIT_IDEAL'):
 assert token in r['stdout'],token
assert r['observed_peak_rss_bytes']==0 and r['observed_peak_process_group_count']==0
runner=(HERE/'run_one_lane.py').read_text()
assert 'count = returned // ctypes.sizeof(ctypes.c_int)' in runner
assert a['status']=='FAIL_CLOSED_RESOURCE_OBSERVER_WITH_EXACT_UNIT_TRANSCRIPT'
assert a['accepted_mathematical_coverage'] is False
assert a['failure']['code']=='PROCESS_GROUP_RSS_OBSERVER_COUNT_BUG'
assert a['raw_result_sha256']==sha('result.json')
assert a['launch_clearance_sha256']==sha('launch_clearance.json')
assert a['resource_clearance_binding_sha256']==sha('RESOURCE_CLEARANCE_BINDING.json')
assert r['second_lane_launched'] is False and r['exact_Q_launched'] is False and r['automatic_relaunch'] is False
print(json.dumps({'status':a['status'],'raw_result_sha256':sha('result.json'),'accepted_coverage':False,'rerun':False},sort_keys=True))
