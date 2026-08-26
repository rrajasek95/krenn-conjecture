#!/usr/bin/env python3
import hashlib,json,pathlib

HERE=pathlib.Path(__file__).resolve().parent
HELD=HERE.parent/'unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-held-2026-08-26'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

expected={
    HELD/'MANIFEST.sha256':'687dd47c10265ad82421cd06e015db4a88982710dbdba370ac0fee82f5f5596b',
    HELD/'source_derivation.json':'194eabb95c628649489f232207a784092a7c5ff040ec82a98ff8ac18bdc6f411',
    HELD/'rep5_rank2_k2_t1_p32003.sing':'fd182135d5da6eda87e284a4f38f147fbf13bef14016c1ee300bb9bde6713c5a',
    HELD/'run_one_lane.py':'e459c779d54b93e58166b639ed29e0aa4e79b69b1366e65dc05b948381473ec7',
    HERE/'referee.py':'c72751fc4d1b1506ba3d36bc971a58c927c8274ae1516dc0a88b7eb021efce67',
    HERE/'results_referee.json':'9d0c26a6157d67728ddf600ed31b835082f80be934c1e44ddcde1082abe65e34',
}
for path,want in expected.items():
    assert sha(path)==want,(path,sha(path),want)

r=json.loads((HERE/'results_referee.json').read_text())
a=json.loads((HERE/'HELD_APPROVAL.json').read_text())
assert r['status']=='PASS_APPROVE_HELD_ONE_OPEN84_P32003_DIAGNOSTIC_ONLY'
assert r['selection']['candidate_count']==6 and r['selection']['six_way_tie_first_three_metrics']
assert (r['selection']['selected']['pivot_k'],r['selection']['selected']['t_open'])==(2,1)
assert r['source']['variables']==84 and r['source']['generators']==6562
assert r['source']['sole_ring_replacement'] and r['source']['epilogue_byte_preserved']
assert r['runner']['native_wall_seconds']==300 and r['runner']['wrapper_wall_seconds']==315
assert r['runner']['rss_cap_bytes']==8*1024**3 and r['runner']['maximum_lane_count']==1
assert r['nonreuse']['consumed_k0_zero_coverage'] and not r['nonreuse']['source_reused']
assert r['scope']['solver_runs']==r['scope']['attempts']==r['scope']['results']==0
assert not any(r['scope'][k] for k in ('launch_authorized','exact_Q_authorized','other_strata_authorized','automatic_relaunch_authorized','mathematical_coverage','rep5_closed'))
assert a['referee_result_sha256']==expected[HERE/'results_referee.json']
assert a['status'].startswith('PASS_HELD_ONLY_') and a['solver_runs']==0
assert not any(a[k] for k in ('launch_authorized','relaunch_authorized','automatic_relaunch_authorized','exact_Q_authorized','other_strata_authorized','mathematical_coverage'))
for name in ('independent_referee_acceptance.json','launch_clearance.json','attempt.json','result.json','stdout.log','stderr.log','watchdog.json','result.json.tmp'):
    assert not (HELD/name).exists(),name
print(json.dumps({'status':'PASS','held_only':True,'selected':[2,1],'variables':84,'generators':6562,'solver_runs':0},sort_keys=True))
