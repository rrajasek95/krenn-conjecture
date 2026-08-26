#!/usr/bin/env python3
"""Conditional refusal-locked sequential rep4 groups76..125 exact-Q runner."""
from __future__ import annotations
import ctypes,hashlib,json,os,signal,subprocess,time
from pathlib import Path
if not __debug__:raise RuntimeError('fail closed: assertions required')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];LEDGER=HERE/'source_ledger.json';NORMALIZED=HERE/'normalized_dependencies.json';SINGULAR=Path('/usr/local/bin/Singular');GTIMEOUT=Path('/usr/local/bin/gtimeout');LEDGER_SHA='b311e566fab04932f0c49a285ac3190ae4ac7a02f102799a9a2c6b34a949e4bb';SINGULAR_SHA='9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88';GTIMEOUT_SHA='1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95';SELECTED=tuple(range(76,126));NATIVE_WALL=240;WRAPPER_WALL=250;RSS_CAP=8*1024**3;POLL=.1;KILL_AFTER=5
class RUsage(ctypes.Structure):
 _fields_=[('uuid',ctypes.c_uint8*16),('user_time',ctypes.c_uint64),('system_time',ctypes.c_uint64),('pkg_idle_wkups',ctypes.c_uint64),('interrupt_wkups',ctypes.c_uint64),('pageins',ctypes.c_uint64),('wired_size',ctypes.c_uint64),('resident_size',ctypes.c_uint64),('phys_footprint',ctypes.c_uint64),('proc_start_abstime',ctypes.c_uint64),('proc_exit_abstime',ctypes.c_uint64),('child_user_time',ctypes.c_uint64),('child_system_time',ctypes.c_uint64),('child_pkg_idle_wkups',ctypes.c_uint64),('child_interrupt_wkups',ctypes.c_uint64),('child_pageins',ctypes.c_uint64),('child_elapsed_abstime',ctypes.c_uint64),('diskio_bytesread',ctypes.c_uint64),('diskio_byteswritten',ctypes.c_uint64)]
LIB=ctypes.CDLL('/usr/lib/libproc.dylib');LIB.proc_pid_rusage.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_void_p];LIB.proc_pid_rusage.restype=ctypes.c_int;LIB.proc_listpgrppids.argtypes=[ctypes.c_uint32,ctypes.c_void_p,ctypes.c_int];LIB.proc_listpgrppids.restype=ctypes.c_int
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,v):t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n');os.replace(t,p)
def exclusive(p,v):
 fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 with os.fdopen(fd,'w') as f:f.write(json.dumps(v,indent=2,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
def members(pgid):
 b=(ctypes.c_int*4096)();n=LIB.proc_listpgrppids(pgid,ctypes.byref(b),ctypes.sizeof(b))
 if not 0<=n<len(b):raise RuntimeError('process-group census failure')
 return [b[i] for i in range(n) if b[i]>0]
def group_rss(pgid,alive):
 pids=members(pgid)
 if alive and not pids:raise RuntimeError('live wrapper has no observable process-group members')
 total=0
 for pid in pids:
  r=RUsage()
  if LIB.proc_pid_rusage(pid,2,ctypes.byref(r))!=0:
   if pid in members(pgid):raise RuntimeError(f'rusage failure for live member {pid}')
   continue
  total+=r.resident_size
 return total,len(pids)
def terminate(p):
 try:os.killpg(p.pid,signal.SIGTERM)
 except ProcessLookupError:return
 deadline=time.monotonic()+KILL_AFTER
 while p.poll() is None and time.monotonic()<deadline:time.sleep(POLL)
 if p.poll() is None:
  try:os.killpg(p.pid,signal.SIGKILL)
  except ProcessLookupError:pass
assert sha(LEDGER)==LEDGER_SHA and sha(SINGULAR)==SINGULAR_SHA and sha(GTIMEOUT)==GTIMEOUT_SHA;assert NORMALIZED.is_file(),'HELD: future PASS groups1..25 and26..75 dependencies have not been normalized';dep=json.loads(NORMALIZED.read_text());assert dep['schema']=='KRENN_X5_REP4_GROUPS76_125_NORMALIZED_DEPENDENCIES_V1' and dep['status']=='PASS_NORMALIZED_EXACT_CLOSED_UNION_0_75' and dep['groups_closed_by_first']==list(range(1,26)) and dep['groups_closed_by_middle']==list(range(26,76)) and dep['closed_union']==list(range(76)) and dep['duplicates']==dep['missing']==dep['extra']==[]
for rel,want in zip(dep['dependency_manifest_paths'],dep['dependency_manifest_sha256']):assert sha(ROOT/rel)==want
for rel,want in zip(dep['dependency_result_paths'],dep['dependency_result_sha256']):assert sha(ROOT/rel)==want
l=json.loads(LEDGER.read_text());lanes=l['lanes'];assert [x['group_id'] for x in lanes]==list(SELECTED) and [x['ordinal'] for x in lanes]==list(range(1,51))
for x in lanes:p=HERE/x['source_path'];assert sha(p)==x['source_sha256'] and p.stat().st_size==x['source_bytes']
for stale in ('BATCH_ATTEMPT.json','batch_result.json','batch_result.json.tmp','results'):assert not (HERE/stale).exists(),f'no relaunch/partial reuse: {stale}'
assert not any(HERE.glob('*.tmp'));manifest=HERE/'MANIFEST.sha256';acceptance=HERE/'independent_referee_acceptance.json';clearance=HERE/'launch_clearance.json';assert manifest.is_file() and acceptance.is_file() and clearance.is_file(),'HELD: audit and clearance required';runner_sha=sha(Path(__file__));dep_sha=sha(NORMALIZED);a=json.loads(acceptance.read_text());c=json.loads(clearance.read_text())
assert a=={'schema':'KRENN_X5_REP4_GROUPS76_125_EXACT_Q_INDEPENDENT_ACCEPTANCE_V1','status':'PASS_APPROVE_CONDITIONAL_REP4_GROUPS76_125_ONLY','held_manifest_sha256':sha(manifest),'source_ledger_sha256':LEDGER_SHA,'normalized_dependencies_sha256':dep_sha,'runner_sha256':runner_sha,'required_closed_union':list(range(76)),'selected_group_ids':list(SELECTED),'maximum_lane_count':50,'exact_Q_authorized':True,'parallel_authorized':False,'skip_reorder_relaunch_authorized':False}
assert c=={'schema':'KRENN_X5_REP4_GROUPS76_125_EXACT_Q_EXPLICIT_CLEARANCE_V1','status':'CLEARED_CONDITIONAL_REP4_GROUPS76_125_ONLY','held_manifest_sha256':sha(manifest),'independent_referee_acceptance_sha256':sha(acceptance),'source_ledger_sha256':LEDGER_SHA,'normalized_dependencies_sha256':dep_sha,'runner_sha256':runner_sha,'singular_sha256':SINGULAR_SHA,'gtimeout_sha256':GTIMEOUT_SHA,'required_closed_union':list(range(76)),'selected_group_ids':list(SELECTED),'native_wall_seconds_each':NATIVE_WALL,'wrapper_wall_seconds_each':WRAPPER_WALL,'rss_cap_bytes_each':RSS_CAP,'no_overlap_confirmed':True,'maximum_lane_count':50,'parallel_authorized':False,'skip_reorder_relaunch_authorized':False}
exclusive(HERE/'BATCH_ATTEMPT.json',{'schema':'KRENN_X5_REP4_GROUPS76_125_ATTEMPT_V1','status':'CONSUMED_SINGLE_USE','group_ids':list(SELECTED),'manifest_sha256':sha(manifest),'dependencies_sha256':dep_sha,'acceptance_sha256':sha(acceptance),'clearance_sha256':sha(clearance)});(HERE/'results').mkdir();batch=[];stop=None
for lane in lanes:
 gid=lane['group_id'];source=HERE/lane['source_path'];start=time.monotonic();termination=None;peak=0;peak_members=0;cmd=[str(GTIMEOUT),'--signal=TERM',f'--kill-after={KILL_AFTER}s',f'{WRAPPER_WALL}s',str(SINGULAR),str(source)];p=subprocess.Popen(cmd,cwd=HERE,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 while p.poll() is None:
  try:rss,n=group_rss(p.pid,True)
  except RuntimeError as error:termination='RESOURCE_OBSERVER_FAILURE:'+str(error);rss,n=peak,peak_members
  if rss>peak:peak,peak_members=rss,n
  elapsed=time.monotonic()-start
  if termination is None and peak>RSS_CAP:termination='RSS_CAP_8GIB'
  elif termination is None and elapsed>NATIVE_WALL:termination='NATIVE_WALL_CAP_240'
  if termination:terminate(p);break
  time.sleep(POLL)
 stdout,stderr=p.communicate();wall=time.monotonic()-start;unit=termination is None and p.returncode==0 and all(x in stdout for x in ('INPUT_VARIABLES=91','INPUT_GENERATORS=6577','GROEBNER_SIZE=1','UNIT_REMAINDER=0','STATUS=UNIT_IDEAL'));nonunit=termination is None and p.returncode==0 and 'STATUS=NONUNIT_OR_UNRESOLVED' in stdout;status='UNIT_IDEAL_EXACT_Q' if unit else 'NONUNIT_EXACT_Q' if nonunit else 'FAIL_CLOSED_RESOURCE' if termination else 'FAIL_CLOSED_PROCESS_OR_MISMATCH';record={'schema':'KRENN_X5_REP4_GROUPS76_125_LANE_RESULT_V1','status':status,'ordinal':lane['ordinal'],'group_id':gid,'chart':lane['canonical_chart'],'source_sha256':lane['source_sha256'],'normalized_dependencies_sha256':dep_sha,'wall_seconds':wall,'peak_group_rss_bytes':peak,'peak_group_members':peak_members,'termination':termination,'returncode':p.returncode,'stdout':stdout,'stderr':stderr,'automatic_relaunch':False};path=HERE/'results'/f'group{gid:03d}.json';atomic(path,record);batch.append({'group_id':gid,'status':status,'result_sha256':sha(path)})
 if not unit:stop={'group_id':gid,'status':status};break
assert [x['group_id'] for x in batch]==list(SELECTED[:len(batch)]);result={'schema':'KRENN_X5_REP4_GROUPS76_125_BATCH_RESULT_V1','status':'PASS_ALL_50_UNIT' if stop is None else 'STOPPED_FAIL_CLOSED','required_closed_union':list(range(76)),'strict_order':list(SELECTED),'completed':batch,'stop':stop,'skipped_after_stop':list(SELECTED[len(batch):]),'parallel':False,'relaunch':False};atomic(HERE/'batch_result.json',result);print(json.dumps({'event':'TERMINAL','status':result['status'],'completed':len(batch)},sort_keys=True))
