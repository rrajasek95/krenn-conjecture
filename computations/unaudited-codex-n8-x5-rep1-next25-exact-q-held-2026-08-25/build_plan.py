#!/usr/bin/env python3
"""Freeze the strict next-25 held schedule around the regenerated ledger."""
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ledger=json.loads((HERE/'source_ledger.json').read_text());runner=HERE/'run_next25.py'
SELECTED=[11,12,14]+list(range(16,38)); CLOSED=list(range(0,11))+[13,15]
assert sha(HERE/'source_ledger.json')=='67376d9ddc96b65f0c34d0f746c85703417d0fb3be88ce5d2cf90a601945c833'
assert sha(runner)=='ad655676b830652681cddd7aa7af46987713984bb63db7dc68157bf88800c268'
assert [x['group_id'] for x in ledger['lanes']]==SELECTED
assert ledger['selection']['excluded_closed_groups']==CLOSED
plan={
 'schema':'KRENN_X5_REP1_NEXT25_EXACT_Q_HELD_SCHEDULE_V1','status':'HELD_ZERO_RUNS_PENDING_INDEPENDENT_AUDIT',
 'selection':ledger['selection'],'lanes':ledger['lanes'],
 'source_ledger':{'path':'source_ledger.json','sha256':sha(HERE/'source_ledger.json'),'total_bytes':sum(x['source_bytes'] for x in ledger['lanes'])},
 'runner':{'path':'run_next25.py','sha256':sha(runner),'strict_sequential':True,'direct_libproc_process_group_rss':True,'fail_closed_rusage':True,'internal_gtimeout_wrapper':True,'atomic_per_lane_results':True,'single_use_batch_marker':True},
 'execution':{'native_wall_seconds_each':240,'wrapper_wall_seconds_each':250,'rss_cap_bytes_each':8589934592,'maximum_lane_count':25,'order':SELECTED,'parallel':False,'skip':False,'reorder':False,'relaunch':False,'stop_whole_batch_on':['NONUNIT','RESOURCE','PROCESS','SCHEMA_OR_TRANSCRIPT_MISMATCH']},
 'acceptance':{'field':'Q','variables':91,'generators':6577,'unit_requires':['returncode=0','termination=null','GROEBNER_SIZE=1','UNIT_REMAINDER=0','STATUS=UNIT_IDEAL'],'scope_each':'one canonical common-S3 group'},
 'clearance':{'independent_acceptance_required':True,'fresh_explicit_batch_clearance_required':True,'files_present_at_seal':0},
 'scope':{'source_regeneration_only':True,'solver_launches':0,'result_files':0,'attempt_markers':0,'clearances':0,'groups_newly_closed':0,'representative_closed':False,'mathematical_coverage':False},
}
tmp=HERE/'held_schedule.json.tmp';tmp.write_text(json.dumps(plan,indent=2,sort_keys=True)+'\n');os.replace(tmp,HERE/'held_schedule.json')
print(json.dumps({'status':plan['status'],'groups':plan['execution']['order'],'runner_sha256':sha(runner)},sort_keys=True))
