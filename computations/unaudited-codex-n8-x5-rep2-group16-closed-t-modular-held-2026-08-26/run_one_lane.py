#!/usr/bin/env python3
"""Refusal-locked single-use rep2 closed-t p32003 diagnostic runner."""
from __future__ import annotations
import ctypes,hashlib,json,os,re,signal,subprocess,time
from datetime import datetime,timezone
from pathlib import Path
assert __debug__
H=Path(__file__).resolve().parent;ROOT=H.parents[1];SOURCE=H/'rep2_group016_62_Vt0_Vt1_Vt2_p32003.sing';SINGULAR=Path('/usr/local/bin/Singular');GTIMEOUT=Path('/usr/local/bin/gtimeout')
SOURCE_SHA='d7e57a3d43fb1280381660be2fea9c966eb086bd2aced3189b0f599030f5822b';DERIV_SHA='4b38d63f5464075aa1b8814f5aa3031336426ed2de8516d7767c01d251e78050'
TIMEOUT=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-combined-smallest-modular-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256';DESIGN=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-design-2026-08-26/MANIFEST.sha256';REF=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-referee-2026-08-26/MANIFEST.sha256';TORUS=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-decomposition-design-2026-08-26/MANIFEST.sha256';GUARD=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-isomorphism-guard-pivot-design-2026-08-26/MANIFEST.sha256';COMBINED=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-referee-comparison-2026-08-26/MANIFEST.sha256'
TIMEOUT_SHA='ef85c2ee938da004226540d76e609feb9fae4261808f6ac755e9bfd8b268c73c';DESIGN_SHA='3d4d6fbc89f5adcc45032c37b1b038780761f479313575c59e4e8bd760da75fd';REF_SHA='e41de381875869a6ac206454b57e091b7ed1093f76aad4a9b71ed30929d3b3cd';TORUS_SHA='1492e69373819fda0c50afc4f1366e2d6da90e857c26f73c03c0212ffd879282';GUARD_SHA='6a781149041e8808d58a53af77059253fe0a0d4295052bfe34756a0f994a0aee';COMBINED_SHA='1a2dcba289d5f31e39be48c4f98ff44a6b0c6891841fd345df52f06abfd5525a'
SINGULAR_SHA='9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88';GTIMEOUT_SHA='1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95';NATIVE=240;WRAPPER=255;RSS_CAP=8*1024**3;POLL=.1;KILL=5;MAX_CLEAR=600
FORBIDDEN=('Singular','gtimeout','sparse_d12_dual','sparse_d12_dual_v4_1','sparse_d12_dual_fixed_lane','sparse_d12_dual_portfolio_audit')
class RU(ctypes.Structure):
 _fields_=[('uuid',ctypes.c_uint8*16),('user_time',ctypes.c_uint64),('system_time',ctypes.c_uint64),('pkg_idle_wkups',ctypes.c_uint64),('interrupt_wkups',ctypes.c_uint64),('pageins',ctypes.c_uint64),('wired_size',ctypes.c_uint64),('resident_size',ctypes.c_uint64),('phys_footprint',ctypes.c_uint64),('proc_start_abstime',ctypes.c_uint64),('proc_exit_abstime',ctypes.c_uint64),('child_user_time',ctypes.c_uint64),('child_system_time',ctypes.c_uint64),('child_pkg_idle_wkups',ctypes.c_uint64),('child_interrupt_wkups',ctypes.c_uint64),('child_pageins',ctypes.c_uint64),('child_elapsed_abstime',ctypes.c_uint64),('diskio_bytesread',ctypes.c_uint64),('diskio_byteswritten',ctypes.c_uint64)]
LIB=ctypes.CDLL('/usr/lib/libproc.dylib');LIB.proc_pid_rusage.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_void_p];LIB.proc_pid_rusage.restype=ctypes.c_int;LIB.proc_listpgrppids.argtypes=[ctypes.c_uint32,ctypes.c_void_p,ctypes.c_int];LIB.proc_listpgrppids.restype=ctypes.c_int;LIB.proc_listallpids.argtypes=[ctypes.c_void_p,ctypes.c_int];LIB.proc_listallpids.restype=ctypes.c_int;LIB.proc_pidpath.argtypes=[ctypes.c_int,ctypes.c_void_p,ctypes.c_uint32];LIB.proc_pidpath.restype=ctypes.c_int
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();canon=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def atomic(path,value):t=path.with_suffix(path.suffix+'.tmp');t.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n');os.replace(t,path)
def exclusive(path,value):
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 with os.fdopen(fd,'w') as f:f.write(json.dumps(value,indent=2,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
def allpids():b=(ctypes.c_int*65536)();n=LIB.proc_listallpids(ctypes.byref(b),ctypes.sizeof(b));assert 0<=n<len(b);return [b[i] for i in range(n) if b[i]>0]
def pidpath(pid):b=ctypes.create_string_buffer(4096);n=LIB.proc_pidpath(pid,ctypes.byref(b),ctypes.sizeof(b));return b.value[:n].decode() if n>0 else None
def census():
 matches=[];observed=unobservable=0
 for pid in allpids():
  if pid==os.getpid():continue
  path=pidpath(pid)
  if path is None:unobservable+=1;continue
  observed+=1
  if Path(path).name in FORBIDDEN:matches.append({'pid':pid,'path':path})
 policy={'method':'libproc proc_listallpids + proc_pidpath','forbidden_executable_basenames':list(FORBIDDEN),'self_pid_excluded':True};return {'policy':policy,'policy_sha256':canon(policy),'observed_paths':observed,'unobservable_pids':unobservable,'matches':matches,'match_count':len(matches),'captured_unix_seconds':time.time()}
def gpids(pgid):
 b=(ctypes.c_int*4096)();n=LIB.proc_listpgrppids(pgid,ctypes.byref(b),ctypes.sizeof(b))
 if not 0<=n<len(b):raise RuntimeError('process-group census failure')
 return [b[i] for i in range(n) if b[i]>0]
def grss(pgid):
 members=gpids(pgid)
 if not members:raise RuntimeError('live wrapper has no observable group members')
 total=0
 for pid in members:
  r=RU()
  if LIB.proc_pid_rusage(pid,2,ctypes.byref(r))!=0:
   if pid in gpids(pgid):raise RuntimeError(f'rusage failure live pid {pid}')
   continue
  total+=r.resident_size
 return total,len(members)
def utc(v):p=datetime.fromisoformat(v.replace('Z','+00:00'));assert p.tzinfo;return p.astimezone(timezone.utc)
assert sha(SOURCE)==SOURCE_SHA and sha(H/'source_derivation.json')==DERIV_SHA
for path,digest in ((TIMEOUT,TIMEOUT_SHA),(DESIGN,DESIGN_SHA),(REF,REF_SHA),(TORUS,TORUS_SHA),(GUARD,GUARD_SHA),(COMBINED,COMBINED_SHA),(SINGULAR,SINGULAR_SHA),(GTIMEOUT,GTIMEOUT_SHA)):assert sha(path)==digest
for name in ('ATTEMPT.json','result.json','result.json.tmp','stdout.log','stderr.log','watchdog.json','RUN_EXCLUSIVE.lock'):assert not (H/name).exists(),f'single-use refusal stale {name}'
assert not list(H.glob('*.tmp'));manifest=H/'MANIFEST.sha256';accept=H/'independent_referee_acceptance.json';clear=H/'launch_clearance.json';assert manifest.is_file() and accept.is_file() and clear.is_file(),'HELD: independent acceptance and fresh explicit clearance required'
msha=sha(manifest);rsha=sha(Path(__file__));a=json.loads(accept.read_text());assert a=={'schema':'KRENN_X5_REP2_GROUP16_CLOSED_T_MODULAR_ACCEPTANCE_V1','status':'PASS_APPROVE_ONE_CLOSED_T_P32003_DIAGNOSTIC_ONLY','held_manifest_sha256':msha,'source_derivation_sha256':DERIV_SHA,'source_sha256':SOURCE_SHA,'runner_sha256':rsha,'timeout_referee_manifest_sha256':TIMEOUT_SHA,'reduction_design_manifest_sha256':DESIGN_SHA,'reduction_referee_manifest_sha256':REF_SHA,'torus_producer_manifest_sha256':TORUS_SHA,'guard_pivot_manifest_sha256':GUARD_SHA,'combined_cover_manifest_sha256':COMBINED_SHA,'variables':62,'generators':6568,'maximum_lane_count':1,'exact_Q_authorized':False,'other_chart_authorized':False,'automatic_relaunch_authorized':False}
c=json.loads(clear.read_text());assert set(c)=={'schema','status','held_manifest_sha256','independent_referee_acceptance_sha256','source_sha256','runner_sha256','singular_sha256','gtimeout_sha256','nonce','issued_at_utc','expires_at_utc','maximum_lane_count','native_wall_seconds','wrapper_wall_seconds','rss_cap_bytes','no_overlap_confirmed','manager_clearance_confirmed','resource_clearance_confirmed','census_policy_sha256','expected_census_match_count','exact_Q_authorized','other_chart_authorized','automatic_relaunch_authorized'}
assert c['schema']=='KRENN_X5_REP2_GROUP16_CLOSED_T_MODULAR_CLEARANCE_V1' and c['status']=='CLEARED_ONE_CLOSED_T_P32003_DIAGNOSTIC_ONLY' and c['held_manifest_sha256']==msha and c['independent_referee_acceptance_sha256']==sha(accept) and c['source_sha256']==SOURCE_SHA and c['runner_sha256']==rsha and c['singular_sha256']==SINGULAR_SHA and c['gtimeout_sha256']==GTIMEOUT_SHA and re.fullmatch(r'[0-9a-f]{32}',c['nonce'])
issued,expires,now=utc(c['issued_at_utc']),utc(c['expires_at_utc']),datetime.now(timezone.utc);assert issued<=now<expires and 0<(expires-issued).total_seconds()<=MAX_CLEAR and c['maximum_lane_count']==1 and c['native_wall_seconds']==NATIVE and c['wrapper_wall_seconds']==WRAPPER and c['rss_cap_bytes']==RSS_CAP and c['no_overlap_confirmed'] is c['manager_clearance_confirmed'] is c['resource_clearance_confirmed'] is True and c['expected_census_match_count']==0 and c['exact_Q_authorized'] is c['other_chart_authorized'] is c['automatic_relaunch_authorized'] is False
pre=census();assert c['census_policy_sha256']==pre['policy_sha256'] and pre['match_count']==0,pre['matches'];exclusive(H/'RUN_EXCLUSIVE.lock',{'nonce':c['nonce'],'manifest_sha256':msha,'runner_sha256':rsha});exclusive(H/'ATTEMPT.json',{'schema':'KRENN_X5_REP2_GROUP16_CLOSED_T_MODULAR_ATTEMPT_V1','status':'ATTEMPT_CONSUMED','nonce':c['nonce'],'manifest_sha256':msha,'acceptance_sha256':sha(accept),'clearance_sha256':sha(clear),'source_sha256':SOURCE_SHA,'runner_sha256':rsha,'prelaunch_census':pre,'relaunch_forbidden_even_if_no_result':True})
command=[str(GTIMEOUT),'--signal=TERM',f'--kill-after={KILL}s',f'{WRAPPER}s',str(SINGULAR),str(SOURCE)];started=time.monotonic()
try:process=subprocess.Popen(command,cwd=H,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
except BaseException as error:atomic(H/'result.json',{'schema':'KRENN_X5_REP2_GROUP16_CLOSED_T_MODULAR_RESULT_V1','status':'FAIL_CLOSED_POPEN','error':repr(error),'attempt_consumed':True,'diagnostic_only':True,'mathematical_coverage':False,'automatic_relaunch':False});raise
print(json.dumps({'event':'STARTED','wrapper_pid':process.pid,'nonce':c['nonce']}),flush=True);peak=members=0;termination=None
while process.poll() is None:
 try:current,count=grss(process.pid)
 except RuntimeError as error:termination='RESOURCE_OBSERVER_FAILURE:'+str(error);current,count=peak,members
 if current>peak:peak,members=current,count
 elapsed=time.monotonic()-started
 if termination is None and peak>RSS_CAP:termination='RSS_CAP_8GIB'
 elif termination is None and elapsed>NATIVE:termination='NATIVE_WALL_CAP_240'
 if termination:
  try:os.killpg(process.pid,signal.SIGTERM)
  except ProcessLookupError:pass
  deadline=time.monotonic()+KILL
  while process.poll() is None and time.monotonic()<deadline:time.sleep(POLL)
  if process.poll() is None:
   try:os.killpg(process.pid,signal.SIGKILL)
   except ProcessLookupError:pass
  break
 time.sleep(POLL)
stdout,stderr=process.communicate();wall=time.monotonic()-started;unit=termination is None and process.returncode==0 and all(x in stdout for x in ('INPUT_VARIABLES=62','INPUT_GENERATORS=6568','GROEBNER_SIZE=1','UNIT_REMAINDER=0','STATUS=UNIT_IDEAL'));nonunit=termination is None and process.returncode==0 and 'STATUS=NONUNIT_OR_UNRESOLVED' in stdout;status='UNIT_IDEAL_MODULAR_DIAGNOSTIC' if unit else 'NONUNIT_MODULAR_DIAGNOSTIC' if nonunit else 'FAIL_CLOSED_RESOURCE_GATE' if termination else 'FAIL_CLOSED_PROCESS_OR_SCHEMA'
atomic(H/'result.json',{'schema':'KRENN_X5_REP2_GROUP16_CLOSED_T_MODULAR_RESULT_V1','status':status,'diagnostic_only':True,'mathematical_coverage':False,'attempt_consumed':True,'field':'F_32003','chart':'V(A67,A12,t0,t1,t2) intersect D(b0)','variables':62,'generators':6568,'command':command,'native_wall_cap_seconds':NATIVE,'wrapper_wall_seconds':WRAPPER,'rss_cap_bytes':RSS_CAP,'wall_seconds':wall,'peak_group_rss_bytes':peak,'peak_group_members':members,'termination':termination,'returncode':process.returncode,'source_sha256':SOURCE_SHA,'runner_sha256':rsha,'stdout':stdout,'stderr':stderr,'exact_Q_launched':False,'other_chart_launched':False,'prior_timeout_reused':False,'automatic_relaunch':False});print(json.dumps({'event':'TERMINAL','status':status,'wall':wall,'peak':peak},sort_keys=True))
