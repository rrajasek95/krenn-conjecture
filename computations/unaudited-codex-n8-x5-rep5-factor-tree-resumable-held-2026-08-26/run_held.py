#!/usr/bin/env python3
"""Fail-closed direct-libproc wrapper for one future factor-tree lane. HELD."""
import argparse,ctypes,hashlib,json,os,signal,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(path,value):
 tmp=path.with_suffix(path.suffix+'.tmp');tmp.parent.mkdir(parents=True,exist_ok=True)
 with tmp.open('w') as f:json.dump(value,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
 os.replace(tmp,path)
class Info(ctypes.Structure):
 _fields_=[('virtual_size',ctypes.c_uint64),('resident_size',ctypes.c_uint64),('total_user',ctypes.c_uint64),('total_system',ctypes.c_uint64),('threads_user',ctypes.c_uint64),('threads_system',ctypes.c_uint64),('policy',ctypes.c_int32),('faults',ctypes.c_int32),('pageins',ctypes.c_int32),('cow_faults',ctypes.c_int32),('messages_sent',ctypes.c_int32),('messages_received',ctypes.c_int32),('syscalls_mach',ctypes.c_int32),('syscalls_unix',ctypes.c_int32),('csw',ctypes.c_int32),('threadnum',ctypes.c_int32),('numrunning',ctypes.c_int32),('priority',ctypes.c_int32)]
def group_rss(pgid):
 lib=ctypes.CDLL('/usr/lib/libproc.dylib',use_errno=True);lp=lib.proc_listpids;lp.argtypes=[ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_int];lp.restype=ctypes.c_int;pi=lib.proc_pidinfo;pi.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_uint64,ctypes.c_void_p,ctypes.c_int];pi.restype=ctypes.c_int;needed=lp(1,0,None,0)
 if needed<=0:raise OSError('proc_listpids size failed')
 ids=(ctypes.c_int*(needed//4+32))();returned=lp(1,0,ids,ctypes.sizeof(ids));total=members=0
 for pid in ids[:returned//4]:
  if pid<=0:continue
  try:
   if os.getpgid(pid)!=pgid:continue
  except (ProcessLookupError,PermissionError):continue
  info=Info();size=ctypes.sizeof(info)
  if pi(pid,4,0,ctypes.byref(info),size)==size:total+=info.resident_size//1024;members+=1
 if members==0:raise OSError('no observable process-group members')
 return total,members
def stop(process):
 try:os.killpg(process.pid,signal.SIGTERM)
 except (ProcessLookupError,PermissionError):return
 try:process.wait(timeout=2)
 except subprocess.TimeoutExpired:
  try:os.killpg(process.pid,signal.SIGKILL)
  except (ProcessLookupError,PermissionError):pass
def main():
 p=argparse.ArgumentParser();p.add_argument('--plan',type=Path,required=True);p.add_argument('--clearance',type=Path,required=True);p.add_argument('--driver',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--checkpoint-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--telemetry',type=Path,required=True);p.add_argument('--stdout',type=Path,required=True);p.add_argument('--stderr',type=Path,required=True);p.add_argument('--exclusive-marker',type=Path,required=True);a=p.parse_args()
 plan=json.loads(a.plan.read_text());clear=json.loads(a.clearance.read_text())
 if plan['status']!='APPROVED_HELD_ZERO_RUN' or clear.get('approved') is not True:raise SystemExit('manager clearance absent')
 if clear.get('schema')!='KRENN_X5_REP5_FACTOR_TREE_CLEARANCE_V1' or clear.get('nonce') in (None,'REPLACE_ME') or clear.get('nonce')!=clear.get('expected_nonce'):raise SystemExit('bad clearance nonce')
 if datetime.fromisoformat(clear['expires_utc'].replace('Z','+00:00'))<=datetime.now(timezone.utc):raise SystemExit('clearance expired')
 pins={'plan_sha256':sha(a.plan),'driver_sha256':sha(a.driver),'source_sha256':sha(a.source)}
 for key,value in pins.items():
  if clear.get(key)!=value:raise SystemExit(f'{key} mismatch')
 if clear.get('rss_gib')!=8 or clear.get('native_wall_seconds')!=480 or clear.get('wrapper_wall_seconds')!=510 or clear.get('max_new_nodes')!=25000 or clear.get('global_node_cap')!=2000000:raise SystemExit('resource geometry mismatch')
 for path in (a.output,a.telemetry,a.stdout,a.stderr):
  if path.exists():raise SystemExit(f'refuse existing output {path}')
 a.exclusive_marker.parent.mkdir(parents=True,exist_ok=True)
 try:fd=os.open(a.exclusive_marker,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
 except FileExistsError:raise SystemExit('exclusive marker exists')
 os.write(fd,(clear['nonce']+'\n').encode());os.fsync(fd);os.close(fd)
 command=[sys.executable,str(a.driver),'--source',str(a.source),'--source-sha256',pins['source_sha256'],'--checkpoint-dir',str(a.checkpoint_dir),'--max-new-nodes','25000','--global-node-cap','2000000','--checkpoint-every','250','--output',str(a.output)]
 started=time.monotonic();samples=[];breach=None;stdout_tmp=a.stdout.with_suffix(a.stdout.suffix+'.tmp');stderr_tmp=a.stderr.with_suffix(a.stderr.suffix+'.tmp')
 try:
  with stdout_tmp.open('wb') as out,stderr_tmp.open('wb') as err:
   process=subprocess.Popen(command,stdout=out,stderr=err,start_new_session=True)
   last_sample=None
   while process.poll() is None:
    elapsed=time.monotonic()-started
    try:
     rss,members=group_rss(process.pid);last_sample={'elapsed_seconds':round(elapsed,6),'rss_kib':rss,'members':members};samples.append(last_sample)
     if rss>8*1024*1024:breach='RSS_CAP'
    except OSError as exc:
     if process.poll() is None:breach=f'LIBPROC_FAILURE:{exc}'
    if elapsed>=510:breach='WALL_CAP'
    if breach:stop(process);break
    time.sleep(.25)
   rc=process.wait()
  os.replace(stdout_tmp,a.stdout);os.replace(stderr_tmp,a.stderr)
  result_exists=a.output.exists();status=None
  if result_exists:
   try:status=json.loads(a.output.read_text()).get('status')
   except Exception:status='UNPARSEABLE'
  telemetry={'schema':'KRENN_X5_REP5_FACTOR_TREE_WATCHDOG_V1','status':'PASS' if breach is None and rc==0 else 'FAIL','breach':breach,'returncode':rc,'elapsed_seconds':round(time.monotonic()-started,6),'peak_rss_kib':max((x['rss_kib'] for x in samples),default=None),'last_successful_sample':samples[-1] if samples else None,'samples':samples,'result_exists':result_exists,'engine_status':status,'checkpoint_current_exists':(a.checkpoint_dir/'CURRENT.json').exists(),'pins':pins,'command':command};atomic(a.telemetry,telemetry)
  return 0 if telemetry['status']=='PASS' else 1
 finally:
  try:a.exclusive_marker.unlink()
  except FileNotFoundError:pass
if __name__=='__main__':raise SystemExit(main())
