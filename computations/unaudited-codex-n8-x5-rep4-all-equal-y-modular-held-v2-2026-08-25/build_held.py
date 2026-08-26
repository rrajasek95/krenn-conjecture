#!/usr/bin/env python3
"""Freshly derive rep4 source and seal v2 hardening; never launch."""
import hashlib,json,os
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1]
D=R/'computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25';Q=D/'rep4_guard_minor_tiny_y_Q.sing';S=H/'rep4_all_equal_y_i0_p00_x0_y0_d01_p32003.sing';RUN=H/'run_one_lane.py'
FAIL=R/'computations/unaudited-codex-n8-x5-rep4-all-equal-y-modular-terminal-second-referee-2026-08-25';SEM=R/'computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-v2-referee-2026-08-25'
PINS={D/'MANIFEST.sha256':'7f47c0567580aba565925b95860bace46ebaf5703aace4ec8aa100f48ec33e02',Q:'d46cdf77b9edafbc17a92ec851badba2db63640ec7324e024a83e29da04e121b',FAIL/'FINAL_MANIFEST.sha256':'b965154ba8acdd16c39dd074bc983a4d0e20ae13e24ff528ea1f16697ed0a074',FAIL/'results_referee.json':'9b43ae57ea42a4f281b2d3d758ee72817e38170a744171966486595f2591e89c',SEM/'FINAL_MANIFEST.sha256':'de9477718cef401aace156f2614b31cf576d761dd5d2b53a4f6c994f5d375771',SEM/'results_referee.json':'59089b5781ed0ef9a117f465e855f4da116ad60b52396ca08e620f1354e4ed4a'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for p,x in PINS.items():assert sha(p)==x,(p,sha(p),x)
q=Q.read_text();assert q.count('ring r=0,')==q.count('quit;')==1 and 'slimgb' not in q
epi='\n'.join(['ideal G=slimgb(I);','print("GROEBNER_SIZE="+string(size(G)));','poly remainder=reduce(1,G);','print("UNIT_REMAINDER="+string(remainder));','if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }','quit;'])
program=q.replace('ring r=0,','ring r=32003,',1).replace('quit;',epi,1)
t=S.with_suffix('.sing.tmp');t.write_text(program);os.replace(t,S)
assert sha(S)=='9471d6bbfb0af012c313cafa97e12f5b3cea380e6cefb0c8f355cb53def80524' and S.stat().st_size==1764288
runner=RUN.read_text();compile(runner,str(RUN),'exec');assert sha(RUN)=='975cb4baa7ca06fb1471fdd883a75ba2e27d61983a5ff5669676a0835242f2f0'
for token in ('proc_listallpids','proc_pidpath','proc_listpgrppids','count = LIBPROC.proc_listpgrppids','return [buffer[index] for index in range(count)','rusage observation failure for live group member','[str(GTIMEOUT), "--signal=TERM"','f"{WRAPPER_WALL}s"','MAX_CLEARANCE_LIFETIME_SECONDS = 600','clearance["no_overlap_confirmed"] is True','exclusive_json(HERE / "ATTEMPT.json"','not (HERE / stale).exists()'):
 assert token in runner,token
assert 'returned // ctypes.sizeof' not in runner
failure=json.loads((FAIL/'results_referee.json').read_text());assert failure['status']=='PASS_ZERO_PROOF_COVERAGE_EXACT_TRANSCRIPT_RESOURCE_OBSERVER_FAILED'
sem=json.loads((SEM/'results_referee.json').read_text());assert sem['status']=='PASS_APPROVED_HELD_ALL_SIX_DEFECTS_FIXED_ZERO_RUNS' and len(sem['defects_fixed'])==6
held={'schema':'KRENN_X5_REP4_ALL_EQUAL_Y_MODULAR_HELD_V2','status':'HELD_FRESH_ZERO_RUN_PENDING_INDEPENDENT_AUDIT','source':{'path':S.name,'sha256':sha(S),'bytes':S.stat().st_size,'freshly_derived_from_Q':True,'old_local_source_reused':False},'runner':{'path':RUN.name,'sha256':sha(RUN),'accepted_rep5_v2_semantics_referee_manifest':PINS[SEM/'FINAL_MANIFEST.sha256'],'correct_pid_count':True,'process_group_rss':True,'fail_closed_rusage':True,'fresh_process_census':True,'internal_wrapper_195':True,'nonce_expiry_no_overlap':True,'exclusive_attempt_marker':True,'stale_abrupt_refusal':True},'supersession':{'failure_manifest_sha256':PINS[FAIL/'FINAL_MANIFEST.sha256'],'failure_result_sha256':PINS[FAIL/'results_referee.json'],'old_clearance_result_attempt_reused':False,'old_lane_remains_consumed':True,'this_is_distinct_package_and_future_attempt':True},'limits':{'native_wall_seconds':180,'wrapper_wall_seconds':195,'rss_cap_bytes':8589934592,'maximum_clearance_lifetime_seconds':600},'scope':{'source_design_materialized':True,'acceptance_present':False,'clearance_present':False,'attempt_present':False,'result_present':False,'solver_runs':0,'exact_Q_authorized':False,'second_lane_authorized':False,'automatic_relaunch_authorized':False,'mathematical_coverage':False}}
tmp=H/'held_pilot.json.tmp';tmp.write_text(json.dumps(held,indent=2,sort_keys=True)+'\n');os.replace(tmp,H/'held_pilot.json')
print(json.dumps({'status':held['status'],'source_sha256':sha(S),'runner_sha256':sha(RUN),'solver_runs':0},sort_keys=True))
