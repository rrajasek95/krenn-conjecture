#!/usr/bin/env python3
import hashlib,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent
RUN=HERE.parent/'unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
pins={HERE/'referee.py':'5ee633be7b0dac2e2e80256126877aed3ba6335a4b91d2bb022a2766465b7e18',HERE/'results_referee.json':'62d4bcd4edcae051ee0637adf4f3e2d685730b34fc65a54ae92890db3d0edbc8',RUN/'MANIFEST.sha256':'d6c098fb885ad9faac566b6f01a9e94f01aa6a8b4a61562ec4fa14f66b44a029',RUN/'source_ledger.json':'59cbe8e6464be1774bbf9310cacae4ef4c9cf076f6185926716881b376718587',RUN/'run_first25.py':'0f85a651c70da8582451987fd56801fb44bdb6c2c611361f4a399d1d1034809e'}
for path,want in pins.items():assert sha(path)==want,(path,sha(path),want)
r=json.loads((HERE/'results_referee.json').read_text());a=json.loads((HERE/'HELD_APPROVAL.json').read_text())
assert r['status']=='PASS_APPROVE_HELD_STRICT_REP4_FIRST25_ZERO_RUN'
assert r['raw_charts']==972 and r['canonical_groups']==162 and r['members_each']==6 and (r['y_groups'],r['z_groups'])==(81,81)
assert r['closed_group_id']==0 and r['selected_group_ids']==list(range(1,26)) and r['sources_byte_identical']==25
assert r['variables_each']==91 and r['generators_each']==6577
assert r['native_wall_seconds_each']==240 and r['wrapper_wall_seconds_each']==250 and r['rss_cap_bytes_each']==8*1024**3
assert r['strict_sequential'] and r['stop_first'] and not any(r[k] for k in ('parallel','skip','reorder','relaunch','solver_runs','mathematical_coverage_added','rep4_closed','conjecture_closed'))
assert a['referee_result_sha256']==pins[HERE/'results_referee.json'] and a['selected_group_ids']==list(range(1,26))
assert a['solver_runs']==0 and not any(a[k] for k in ('launch_authorized','relaunch_authorized','automatic_relaunch_authorized','parallel_authorized','skip_or_reorder_authorized','mathematical_coverage_added'))
for name in ('independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):
    assert not (RUN/name).exists(),name
assert not list(RUN.rglob('*.tmp'))
print(json.dumps({'status':'PASS','held_only':True,'groups':[1,25],'sources':25,'solver_runs':0},sort_keys=True))
