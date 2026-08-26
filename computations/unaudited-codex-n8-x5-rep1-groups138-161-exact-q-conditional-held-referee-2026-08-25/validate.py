#!/usr/bin/env python3
"""Validate the sealed held-only referee package."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
r=json.loads((HERE/'results_referee.json').read_text())
assert r['schema']=='KRENN_X5_REP1_GROUPS138_161_EXACT_Q_CONDITIONAL_HELD_REFEREE_V1'
assert r['status']=='PASS_HELD_ONLY_FINAL_24_EXACT_Q_SOURCES_DEPENDENCY_ABSENT'
assert r['producer_manifest_sha256']=='25a708451a790a3984052519a5fd129182a54b3fbe65dbc85279b998d0667bf5'
assert r['source_ledger_sha256']=='ed416a9cc138abae890447995f04e084223fccfe0629da47c9e234e5c02e76be'
assert r['dependency_adapter_sha256']=='907519564535bc533e060dbef4545ccf2635234041af5d7e0a320db503991568'
assert r['producer_adapter_tests_sha256']=='4ad1323a6c4367dd124d37eb7fa4a61a7aaa17e9cace285ae7d57550ff3717a9'
assert r['runner_sha256']=='a942eb6a12512f334bc6bdbf1b023c1428c8372fda46032dbddfb84dcf554f8b'
assert r['selection']=={'group_ids':list(range(138,162)),'count':24,'strict_order':True,'total_source_bytes':42769236}
assert len(r['source_regeneration']['sources'])==24 and r['source_regeneration']['all_24_byte_exact'] and r['source_regeneration']['all_24_census_exact']
assert [x['group_id'] for x in r['source_regeneration']['sources']]==list(range(138,162))
assert all((x['variables'],x['generators'],x['raw_member_count'])==(91,6577,6) for x in r['source_regeneration']['sources'])
assert r['dependency']['hostile_count']==12 and all(r['dependency']['hostile_tests'].values())
assert r['dependency']['future_manifest_sha256'] is r['dependency']['future_result_sha256'] is None
assert r['dependency']['future_files_absent'] and r['dependency']['satisfied'] is False
assert r['runner_contract']['native_wall_seconds_each']==240 and r['runner_contract']['wrapper_wall_seconds_each']==250 and r['runner_contract']['rss_cap_bytes_each']==8589934592
assert r['runner_contract']['strict_sequential'] and r['runner_contract']['stop_first'] and not r['runner_contract']['parallel'] and not r['runner_contract']['relaunch']
assert r['scope']=={'held_approval_only':True,'launch_acceptance_materialized':False,'launch_clearance_materialized':False,'solver_runs':0,'result_files':0,'groups_newly_closed':0,'mathematical_coverage':False}
manifest=HERE/'FINAL_MANIFEST.sha256'
if manifest.exists():
 for line in manifest.read_text().splitlines():
  if not line.strip():continue
  expected,name=line.split(None,1);target=(manifest.parent/name.strip()).resolve();assert target.is_file() and sha(target)==expected,target
print(json.dumps({'status':'PASS','sources':24,'hostiles':12,'solver_runs':0},sort_keys=True))
