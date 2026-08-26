#!/usr/bin/env python3
"""V2 provenance-replaying sequential rep2 exact-Q groups76..125 executor."""
from __future__ import annotations
import ctypes,hashlib,json,os,signal,subprocess,time
from pathlib import Path
if not __debug__:raise RuntimeError('fail closed: assertions required')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PROD=ROOT/'computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-2026-08-26';LEDGER=PROD/'source_ledger.json';FUTURE=PROD/'future_dependencies.json';SOURCE_REFERENCE=HERE/'source_reference_ledger.json';VERIFIER=HERE/'dependency_verifier.py';NORMALIZED=HERE/'normalized_dependencies.json';SINGULAR=Path('/usr/local/bin/Singular');GTIMEOUT=Path('/usr/local/bin/gtimeout')
LEDGER_SHA='4aa023638d439fd1250b66593d93dd29dd4472831449ff571e2730bf6950b4ce';FUTURE_SHA='5173f8f03b8eb7feff428573cb6a0b2813ef1e6cb1d4c4696543c30585e522e4';SOURCE_REFERENCE_SHA='6f44241c35e197d557238a405c7549348a39e0f60d8f03f4d092eb3945ca9083';VERIFIER_SHA='42461b1d52f4909a3439a484d8b7b34b658c767a9ad246d9f4a98cc2929f30b1';SINGULAR_SHA='9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88';GTIMEOUT_SHA='1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95';SELECTED=tuple(range(76,126));NATIVE_WALL=240;WRAPPER_WALL=250;RSS_CAP=8*1024**3;POLL=.1;KILL_AFTER=5
class RUsage(ctypes.Structure):
 _fields_=[('uuid',ctypes.c_uint8*16),('user_time',ctypes.c_uint64),('system_time',ctypes.c_uint64),('pkg_idle_wkups',ctypes.c_uint64),('interrupt_wkups',ctypes.c_uint64),('pageins',ctypes.c_uint64),('wired_size',ctypes.c_uint64),('resident_size',ctypes.c_uint64),('phys_footprint',ctypes.c_uint64),('proc_start_abstime',ctypes.c_uint64),('proc_exit_abstime',ctypes.c_uint64),('child_user_time',ctypes.c_uint64),('child_system_time',ctypes.c_uint64),('child_pkg_idle_wkups',ctypes.c_uint64),('child_interrupt_wkups',ctypes.c_uint64),('child_pageins',ctypes.c_uint64),('child_elapsed_abstime',ctypes.c_uint64),('diskio_bytesread',ctypes.c_uint64),('diskio_byteswritten',ctypes.c_uint64)]
LIB=ctypes.CDLL('/usr/lib/libproc.dylib');LIB.proc_pid_rusage.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_void_p];LIB.proc_pid_rusage.restype=ctypes.c_int;LIB.proc_listpgrppids.argtypes=[ctypes.c_uint32,ctypes.c_void_p,ctypes.c_int];LIB.proc_listpgrppids.restype=ctypes.c_int
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def atomic(path,value):tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n');os.replace(tmp,path)
def exclusive(path,value):
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 with os.fdopen(fd,'w') as stream:stream.write(json.dumps(value,indent=2,sort_keys=True)+'\n');stream.flush();os.fsync(stream.fileno())
def members(pgid):
 buf=(ctypes.c_int*4096)();count=LIB.proc_listpgrppids(pgid,ctypes.byref(buf),ctypes.sizeof(buf))
 if not 0<=count<len(buf):raise RuntimeError('process-group census failure')
 return [buf[i] for i in range(count) if buf[i]>0]
def group_rss(pgid,alive):
 pids=members(pgid)
 if alive and not pids:raise RuntimeError('live wrapper has no observable process-group members')
 total=0
 for pid in pids:
  usage=RUsage()
  if LIB.proc_pid_rusage(pid,2,ctypes.byref(usage))!=0:
   if pid in members(pgid):raise RuntimeError(f'rusage failure for live member {pid}')
   continue
  total+=usage.resident_size
 return total,len(pids)
def terminate(process):
 try:os.killpg(process.pid,signal.SIGTERM)
 except ProcessLookupError:return
 deadline=time.monotonic()+KILL_AFTER
 while process.poll() is None and time.monotonic()<deadline:time.sleep(POLL)
 if process.poll() is None:
  try:os.killpg(process.pid,signal.SIGKILL)
  except ProcessLookupError:pass

assert sha(LEDGER)==LEDGER_SHA and sha(FUTURE)==FUTURE_SHA and sha(SOURCE_REFERENCE)==SOURCE_REFERENCE_SHA and sha(VERIFIER)==VERIFIER_SHA and sha(SINGULAR)==SINGULAR_SHA and sha(GTIMEOUT)==GTIMEOUT_SHA
assert NORMALIZED.is_file(),'HELD: both future dependencies have not been normalized'
dependency=json.loads(NORMALIZED.read_text());assert dependency['schema']=='KRENN_X5_REP2_GROUPS76_125_NORMALIZED_DEPENDENCIES_V1' and dependency['status']=='PASS_NORMALIZED_EXACT_CLOSED_UNION_0_75' and dependency['groups_closed_by_first']==list(range(1,26)) and dependency['groups_closed_by_middle']==list(range(26,76)) and dependency['closed_union']==list(range(76)) and dependency['duplicates']==dependency['missing']==dependency['extra']==[]
assert len(dependency['dependency_manifest_sha256'])==len(dependency['dependency_result_sha256'])==2 and all(len(x)==64 for x in dependency['dependency_manifest_sha256']+dependency['dependency_result_sha256'])
from dependency_verifier import verify_payload
replay=verify_payload(json.loads(FUTURE.read_text()),dependency,ROOT);assert replay['status']=='PASS_REPLAYED_ALL_FOUR_DEPENDENCY_ARTIFACTS_EXACT_UNION_0_75' and replay['closed_union']==list(range(76))
ledger=json.loads(LEDGER.read_text());lanes=ledger['lanes'];assert [x['group_id'] for x in lanes]==list(SELECTED) and [x['ordinal'] for x in lanes]==list(range(1,51))
for lane in lanes:path=PROD/lane['source_path'];assert sha(path)==lane['source_sha256'] and path.stat().st_size==lane['source_bytes'] and lane['variables']==91 and lane['generators']==6577
for stale in ('BATCH_ATTEMPT.json','batch_result.json','batch_result.json.tmp','results'):assert not (HERE/stale).exists(),f'no relaunch/partial reuse: {stale}'
assert not any(HERE.glob('*.tmp'));manifest=HERE/'MANIFEST.sha256';acceptance=HERE/'independent_referee_acceptance.json';clearance=HERE/'launch_clearance.json';assert manifest.is_file() and acceptance.is_file() and clearance.is_file(),'HELD: audit and clearance required'
runner_sha=sha(Path(__file__));dependency_sha=sha(NORMALIZED);a=json.loads(acceptance.read_text());c=json.loads(clearance.read_text())
assert a=={'schema':'KRENN_X5_REP2_GROUPS76_125_EXACT_Q_INDEPENDENT_ACCEPTANCE_V2','status':'PASS_APPROVE_CONDITIONAL_REP2_GROUPS76_125_V2_ONLY','held_manifest_sha256':sha(manifest),'source_ledger_sha256':LEDGER_SHA,'source_reference_ledger_sha256':SOURCE_REFERENCE_SHA,'dependency_verifier_sha256':VERIFIER_SHA,'normalized_dependencies_sha256':dependency_sha,'runner_sha256':runner_sha,'required_closed_union':list(range(76)),'selected_group_ids':list(SELECTED),'maximum_lane_count':50,'exact_Q_authorized':True,'parallel_authorized':False,'skip_reorder_relaunch_authorized':False}
assert c=={'schema':'KRENN_X5_REP2_GROUPS76_125_EXACT_Q_EXPLICIT_CLEARANCE_V2','status':'CLEARED_CONDITIONAL_REP2_GROUPS76_125_V2_ONLY','held_manifest_sha256':sha(manifest),'independent_referee_acceptance_sha256':sha(acceptance),'source_ledger_sha256':LEDGER_SHA,'source_reference_ledger_sha256':SOURCE_REFERENCE_SHA,'dependency_verifier_sha256':VERIFIER_SHA,'normalized_dependencies_sha256':dependency_sha,'runner_sha256':runner_sha,'singular_sha256':SINGULAR_SHA,'gtimeout_sha256':GTIMEOUT_SHA,'required_closed_union':list(range(76)),'selected_group_ids':list(SELECTED),'native_wall_seconds_each':NATIVE_WALL,'wrapper_wall_seconds_each':WRAPPER_WALL,'rss_cap_bytes_each':RSS_CAP,'no_overlap_confirmed':True,'maximum_lane_count':50,'parallel_authorized':False,'skip_reorder_relaunch_authorized':False}
exclusive(HERE/'BATCH_ATTEMPT.json',{'schema':'KRENN_X5_REP2_GROUPS76_125_ATTEMPT_V1','status':'CONSUMED_SINGLE_USE','group_ids':list(SELECTED),'manifest_sha256':sha(manifest),'dependencies_sha256':dependency_sha,'acceptance_sha256':sha(acceptance),'clearance_sha256':sha(clearance)});(HERE/'results').mkdir();batch=[];stop=None
for lane in lanes:
 gid=lane['group_id'];source=HERE/lane['source_path'];start=time.monotonic();termination=None;peak=0;peak_members=0;command=[str(GTIMEOUT),'--signal=TERM',f'--kill-after={KILL_AFTER}s',f'{WRAPPER_WALL}s',str(SINGULAR),str(source)];process=subprocess.Popen(command,cwd=HERE,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 while process.poll() is None:
  try:rss,count=group_rss(process.pid,True)
  except RuntimeError as error:termination='RESOURCE_OBSERVER_FAILURE:'+str(error);rss,count=peak,peak_members
  if rss>peak:peak,peak_members=rss,count
  elapsed=time.monotonic()-start
  if termination is None and peak>RSS_CAP:termination='RSS_CAP_8GIB'
  elif termination is None and elapsed>NATIVE_WALL:termination='NATIVE_WALL_CAP_240'
  if termination:terminate(process);break
  time.sleep(POLL)
 stdout,stderr=process.communicate();wall=time.monotonic()-start;unit=termination is None and process.returncode==0 and all(x in stdout for x in ('INPUT_VARIABLES=91','INPUT_GENERATORS=6577','GROEBNER_SIZE=1','UNIT_REMAINDER=0','STATUS=UNIT_IDEAL'));nonunit=termination is None and process.returncode==0 and 'STATUS=NONUNIT_OR_UNRESOLVED' in stdout;status='UNIT_IDEAL_EXACT_Q' if unit else 'NONUNIT_EXACT_Q' if nonunit else 'FAIL_CLOSED_RESOURCE' if termination else 'FAIL_CLOSED_PROCESS_OR_MISMATCH';record={'schema':'KRENN_X5_REP2_GROUPS76_125_LANE_RESULT_V1','status':status,'ordinal':lane['ordinal'],'group_id':gid,'chart':lane['canonical_chart'],'source_sha256':lane['source_sha256'],'normalized_dependencies_sha256':dependency_sha,'wall_seconds':wall,'peak_group_rss_bytes':peak,'peak_group_members':peak_members,'termination':termination,'returncode':process.returncode,'stdout':stdout,'stderr':stderr,'automatic_relaunch':False};path=HERE/'results'/f'group{gid:03d}.json';atomic(path,record);batch.append({'group_id':gid,'status':status,'result_sha256':sha(path)})
 if not unit:stop={'group_id':gid,'status':status};break
assert [x['group_id'] for x in batch]==list(SELECTED[:len(batch)]);result={'schema':'KRENN_X5_REP2_GROUPS76_125_BATCH_RESULT_V1','status':'PASS_ALL_50_UNIT' if stop is None else 'STOPPED_FAIL_CLOSED','required_closed_union':list(range(76)),'strict_order':list(SELECTED),'completed':batch,'stop':stop,'skipped_after_stop':list(SELECTED[len(batch):]),'parallel':False,'relaunch':False};atomic(HERE/'batch_result.json',result);print(json.dumps({'event':'TERMINAL','status':result['status'],'completed':len(batch)},sort_keys=True))
