#!/usr/bin/env python3
"""Strict next50 executor using the audited baseline+next25 normalization adapter."""
from __future__ import annotations
import ctypes,hashlib,json,os,signal,subprocess,time
from normalize_next25_dependency import load_and_normalize
from pathlib import Path

if not __debug__: raise RuntimeError('fail closed: assertions required')
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
LEDGER=HERE/'source_ledger.json'; SINGULAR=Path('/usr/local/bin/Singular'); GTIMEOUT=Path('/usr/local/bin/gtimeout')
NORMALIZED_DEPENDENCY=HERE/'normalized_next25_dependency.json'
NORMALIZED_DEPENDENCY_SHA='29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76'
DEPENDENCY_ADAPTER_SHA='c9c3d365f0f2fb3c9a03656822b4112b245455745dd4f707367fff6c6c2e6d11'
LEDGER_SHA='1888166e62d1e475d745283e1b5c5225ed1aac8d5ac14a4be3543972d881e172'
SINGULAR_SHA='9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88'; GTIMEOUT_SHA='1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95'
NATIVE_WALL=240; WRAPPER_WALL=250; RSS_CAP=8*1024**3; POLL=.1; KILL_AFTER=5
SELECTED=tuple(range(38,88))

class RUsageInfoV2(ctypes.Structure):
 _fields_=[('uuid',ctypes.c_uint8*16),('user_time',ctypes.c_uint64),('system_time',ctypes.c_uint64),('pkg_idle_wkups',ctypes.c_uint64),('interrupt_wkups',ctypes.c_uint64),('pageins',ctypes.c_uint64),('wired_size',ctypes.c_uint64),('resident_size',ctypes.c_uint64),('phys_footprint',ctypes.c_uint64),('proc_start_abstime',ctypes.c_uint64),('proc_exit_abstime',ctypes.c_uint64),('child_user_time',ctypes.c_uint64),('child_system_time',ctypes.c_uint64),('child_pkg_idle_wkups',ctypes.c_uint64),('child_interrupt_wkups',ctypes.c_uint64),('child_pageins',ctypes.c_uint64),('child_elapsed_abstime',ctypes.c_uint64),('diskio_bytesread',ctypes.c_uint64),('diskio_byteswritten',ctypes.c_uint64)]
LIBPROC=ctypes.CDLL('/usr/lib/libproc.dylib')
LIBPROC.proc_pid_rusage.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_void_p];LIBPROC.proc_pid_rusage.restype=ctypes.c_int
LIBPROC.proc_listpgrppids.argtypes=[ctypes.c_uint32,ctypes.c_void_p,ctypes.c_int];LIBPROC.proc_listpgrppids.restype=ctypes.c_int
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,v):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n');os.replace(t,p)
def exclusive(p,v):
 fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 with os.fdopen(fd,'w') as f:f.write(json.dumps(v,indent=2,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
def members(pgid):
 buf=(ctypes.c_int*4096)();count=LIBPROC.proc_listpgrppids(pgid,ctypes.byref(buf),ctypes.sizeof(buf))
 if not 0<=count<len(buf):raise RuntimeError('process-group census failure')
 return [buf[i] for i in range(count) if buf[i]>0]
def group_rss(pgid,alive):
 pids=members(pgid)
 if alive and not pids:raise RuntimeError('live wrapper has no observable group members')
 total=0
 for pid in pids:
  rec=RUsageInfoV2()
  if LIBPROC.proc_pid_rusage(pid,2,ctypes.byref(rec))!=0:
   if pid in members(pgid):raise RuntimeError(f'rusage failure for live member {pid}')
   continue
  total+=rec.resident_size
 return total,len(pids)
def terminate(process):
 try:os.killpg(process.pid,signal.SIGTERM)
 except ProcessLookupError:return
 deadline=time.monotonic()+KILL_AFTER
 while process.poll() is None and time.monotonic()<deadline:time.sleep(POLL)
 if process.poll() is None:
  try:os.killpg(process.pid,signal.SIGKILL)
  except ProcessLookupError:pass

assert sha(LEDGER)==LEDGER_SHA and sha(SINGULAR)==SINGULAR_SHA and sha(GTIMEOUT)==GTIMEOUT_SHA
ledger=json.loads(LEDGER.read_text());lanes=ledger['lanes']
assert [x['group_id'] for x in lanes]==list(SELECTED) and [x['ordinal'] for x in lanes]==list(range(1,51))
for lane in lanes:
 p=HERE/lane['source_path'];assert sha(p)==lane['source_sha256'] and p.stat().st_size==lane['source_bytes']
for stale in ('BATCH_ATTEMPT.json','batch_result.json','batch_result.json.tmp','results'):
 assert not (HERE/stale).exists(),f'no relaunch/partial reuse: {stale} exists'
assert not any(HERE.glob('*.tmp'))
manifest=HERE/'MANIFEST.sha256';acceptance=HERE/'independent_referee_acceptance.json';clearance=HERE/'launch_clearance.json'
assert manifest.is_file() and acceptance.is_file() and clearance.is_file(),'HELD: independent acceptance and explicit batch clearance required'
a=json.loads(acceptance.read_text());c=json.loads(clearance.read_text());runner_sha=sha(Path(__file__))
assert sha(HERE/'normalize_next25_dependency.py')==DEPENDENCY_ADAPTER_SHA
assert sha(NORMALIZED_DEPENDENCY)==NORMALIZED_DEPENDENCY_SHA
normalized=load_and_normalize()
assert normalized==json.loads(NORMALIZED_DEPENDENCY.read_text())
assert normalized['closed_union']==list(range(38))
future_manifest_sha=normalized['pins']['next25_terminal_manifest_sha256']
future_result_sha=normalized['pins']['next25_terminal_result_sha256']
baseline_manifest_sha=normalized['pins']['baseline_manifest_sha256']
baseline_result_sha=normalized['pins']['baseline_result_sha256']
binding_audit_manifest_sha=normalized['pins']['binding_audit_manifest_sha256']
binding_audit_result_sha=normalized['pins']['binding_audit_result_sha256']

assert a=={'schema':'KRENN_X5_REP1_NEXT50_EXACT_Q_NORMALIZED_INDEPENDENT_ACCEPTANCE_V2','status':'PASS_APPROVE_STRICT_NORMALIZED_NEXT50_BATCH_ONLY','held_manifest_sha256':sha(manifest),'source_ledger_sha256':LEDGER_SHA,'runner_sha256':runner_sha,'selected_group_ids':list(SELECTED),'maximum_lane_count':50,'dependency_adapter_sha256':DEPENDENCY_ADAPTER_SHA,'normalized_dependency_sha256':NORMALIZED_DEPENDENCY_SHA,'baseline_manifest_sha256':baseline_manifest_sha,'baseline_result_sha256':baseline_result_sha,'next25_terminal_manifest_sha256':future_manifest_sha,'next25_terminal_result_sha256':future_result_sha,'binding_audit_manifest_sha256':binding_audit_manifest_sha,'binding_audit_result_sha256':binding_audit_result_sha,'next25_terminal_closed_union':list(range(38)),'exact_Q_authorized':True,'parallel_authorized':False,'skip_reorder_relaunch_authorized':False}
assert c=={'schema':'KRENN_X5_REP1_NEXT50_EXACT_Q_NORMALIZED_EXPLICIT_CLEARANCE_V2','status':'CLEARED_STRICT_NORMALIZED_NEXT50_BATCH_ONLY','held_manifest_sha256':sha(manifest),'independent_referee_acceptance_sha256':sha(acceptance),'source_ledger_sha256':LEDGER_SHA,'runner_sha256':runner_sha,'singular_sha256':SINGULAR_SHA,'gtimeout_sha256':GTIMEOUT_SHA,'selected_group_ids':list(SELECTED),'dependency_adapter_sha256':DEPENDENCY_ADAPTER_SHA,'normalized_dependency_sha256':NORMALIZED_DEPENDENCY_SHA,'baseline_manifest_sha256':baseline_manifest_sha,'baseline_result_sha256':baseline_result_sha,'next25_terminal_manifest_sha256':future_manifest_sha,'next25_terminal_result_sha256':future_result_sha,'binding_audit_manifest_sha256':binding_audit_manifest_sha,'binding_audit_result_sha256':binding_audit_result_sha,'native_wall_seconds_each':NATIVE_WALL,'wrapper_wall_seconds_each':WRAPPER_WALL,'rss_cap_bytes_each':RSS_CAP,'no_overlap_confirmed':True,'maximum_lane_count':50,'parallel_authorized':False,'skip_reorder_relaunch_authorized':False}
exclusive(HERE/'BATCH_ATTEMPT.json',{'schema':'KRENN_X5_REP1_NEXT50_NORMALIZED_BATCH_ATTEMPT_V2','status':'CONSUMED_SINGLE_USE','group_ids':list(SELECTED),'manifest_sha256':sha(manifest),'acceptance_sha256':sha(acceptance),'clearance_sha256':sha(clearance),'dependency_adapter_sha256':DEPENDENCY_ADAPTER_SHA,'normalized_dependency_sha256':NORMALIZED_DEPENDENCY_SHA,'baseline_manifest_sha256':baseline_manifest_sha,'baseline_result_sha256':baseline_result_sha,'next25_terminal_manifest_sha256':future_manifest_sha,'next25_terminal_result_sha256':future_result_sha,'binding_audit_manifest_sha256':binding_audit_manifest_sha,'binding_audit_result_sha256':binding_audit_result_sha})
(HERE/'results').mkdir()
batch=[];stop=None
for lane in lanes:
 gid=lane['group_id'];source=HERE/lane['source_path'];started=time.monotonic();termination=None;peak=0;peak_members=0
 command=[str(GTIMEOUT),'--signal=TERM',f'--kill-after={KILL_AFTER}s',f'{WRAPPER_WALL}s',str(SINGULAR),str(source)]
 process=subprocess.Popen(command,cwd=HERE,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 while process.poll() is None:
  try:rss,n=group_rss(process.pid,True)
  except RuntimeError as error:termination='RESOURCE_OBSERVER_FAILURE:'+str(error);rss,n=peak,peak_members
  if rss>peak:peak,peak_members=rss,n
  elapsed=time.monotonic()-started
  if termination is None and peak>RSS_CAP:termination='RSS_CAP_8GIB'
  elif termination is None and elapsed>NATIVE_WALL:termination='NATIVE_WALL_CAP_240'
  if termination:terminate(process);break
  time.sleep(POLL)
 stdout,stderr=process.communicate();wall=time.monotonic()-started
 unit=termination is None and process.returncode==0 and all(x in stdout for x in ('INPUT_GENERATORS=6577','GROEBNER_SIZE=1','UNIT_REMAINDER=0','STATUS=UNIT_IDEAL'))
 nonunit=termination is None and process.returncode==0 and 'STATUS=NONUNIT_OR_UNRESOLVED' in stdout
 status='UNIT_IDEAL_EXACT_Q' if unit else 'NONUNIT_EXACT_Q' if nonunit else 'FAIL_CLOSED_RESOURCE' if termination else 'FAIL_CLOSED_PROCESS_OR_MISMATCH'
 record={'schema':'KRENN_X5_REP1_NEXT50_NORMALIZED_LANE_RESULT_V2','status':status,'ordinal':lane['ordinal'],'group_id':gid,'chart':lane['canonical_chart'],'source_sha256':lane['source_sha256'],'wall_seconds':wall,'peak_group_rss_bytes':peak,'peak_group_members':peak_members,'termination':termination,'wrapper_returncode':process.returncode,'stdout':stdout,'stderr':stderr,'diagnostic_scope_one_group':True,'automatic_relaunch':False}
 atomic(HERE/'results'/f'group{gid:03d}.json',record);batch.append({'group_id':gid,'status':status,'result_sha256':sha(HERE/'results'/f'group{gid:03d}.json')})
 if not unit:stop={'group_id':gid,'status':status};break
assert [x['group_id'] for x in batch]==list(SELECTED[:len(batch)])
batch_result={'schema':'KRENN_X5_REP1_NEXT50_NORMALIZED_BATCH_RESULT_V2','status':'PASS_ALL_50_UNIT' if stop is None else 'STOPPED_FAIL_CLOSED','strict_order':list(SELECTED),'completed':batch,'stop':stop,'skipped_after_stop':list(SELECTED[len(batch):]),'parallel':False,'relaunch':False}
atomic(HERE/'batch_result.json',batch_result)
print(json.dumps({'event':'TERMINAL','status':batch_result['status'],'completed':len(batch)},sort_keys=True))
