#!/usr/bin/env python3
from __future__ import annotations
import ctypes, hashlib, json, os, signal, subprocess, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
SOURCE=HERE/"rank1_orbit0_Q.sing"; CLEAR=HERE/"FRESH_CLEARANCE.json"; ATT=HERE/"attempt_exact_q"
PLAN=ROOT/"computations/unaudited-codex-n8-x5-rectangle-rank1-orbit0-p32003-pilot-referee-2026-08-25/EXACT_Q_SAME_CHART_HELD_PLAN.json"
SINGULAR=Path("/usr/local/Cellar/singular/4.4.1p5_3/bin/Singular")
GTIMEOUT=Path("/usr/local/Cellar/coreutils/9.11/bin/gtimeout")
PINS={SOURCE:"c062396aa8835e9c31d0e845a997d89f3b1d151f6494d36d5ba990cdadf9c44f",PLAN:"ab2c40e5d128a2e15de749c1c768518f85d9da85c92de6271efed30443ef5164",SINGULAR:"9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",GTIMEOUT:"1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95"}
NATIVE=480; WRAPPER=510; RSS_CAP_KIB=8*1024*1024; PROC_PIDTASKINFO=4

def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""): h.update(b)
 return h.hexdigest()
def atomic(path,data):
 tmp=path.with_suffix(path.suffix+".tmp")
 with tmp.open("xb") as f: f.write(data); f.flush(); os.fsync(f.fileno())
 os.replace(tmp,path)
def atom_json(path,obj): atomic(path,(json.dumps(obj,indent=2,sort_keys=True)+"\n").encode())
class Info(ctypes.Structure):
 _fields_=[("virtual_size",ctypes.c_uint64),("resident_size",ctypes.c_uint64),("total_user",ctypes.c_uint64),("total_system",ctypes.c_uint64),("threads_user",ctypes.c_uint64),("threads_system",ctypes.c_uint64),("policy",ctypes.c_int32),("faults",ctypes.c_int32),("pageins",ctypes.c_int32),("cow_faults",ctypes.c_int32),("messages_sent",ctypes.c_int32),("messages_received",ctypes.c_int32),("syscalls_mach",ctypes.c_int32),("syscalls_unix",ctypes.c_int32),("csw",ctypes.c_int32),("threadnum",ctypes.c_int32),("numrunning",ctypes.c_int32),("priority",ctypes.c_int32)]
LIB=ctypes.CDLL("/usr/lib/libproc.dylib",use_errno=True); LIST=LIB.proc_listpids; PATH=LIB.proc_pidpath; INFO=LIB.proc_pidinfo
LIST.argtypes=[ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_int]; LIST.restype=ctypes.c_int
PATH.argtypes=[ctypes.c_int,ctypes.c_void_p,ctypes.c_uint32]; PATH.restype=ctypes.c_int
INFO.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_uint64,ctypes.c_void_p,ctypes.c_int]; INFO.restype=ctypes.c_int
def pids():
 n=LIST(1,0,None,0); assert n>0
 a=(ctypes.c_int*(n//4+64))(); got=LIST(1,0,a,ctypes.sizeof(a)); assert got>0
 return [x for x in a[:got//4] if x>0]
def pathname(pid):
 b=ctypes.create_string_buffer(4096); n=PATH(pid,b,len(b)); return b.value.decode(errors="replace") if n>0 else ""
def census():
 m=[]
 for pid in pids():
  if pid==os.getpid(): continue
  path=pathname(pid); base=Path(path).name.lower()
  if "singular" in base or "sparse_d12" in base: m.append({"pid":pid,"path":path})
 return {"observer":"Darwin libproc","matches":m,"pass":not m}
def group_rss(pgid):
 total=members=0
 for pid in pids():
  try:
   if os.getpgid(pid)!=pgid: continue
  except (ProcessLookupError,PermissionError): continue
  x=Info(); size=ctypes.sizeof(x)
  if INFO(pid,PROC_PIDTASKINFO,0,ctypes.byref(x),size)==size: total+=x.resident_size//1024; members+=1
 if not members: raise OSError("no observable member")
 return total,members
def terminate(p):
 try: os.killpg(p.pid,signal.SIGTERM)
 except ProcessLookupError: return
 try: p.wait(timeout=2)
 except subprocess.TimeoutExpired:
  try: os.killpg(p.pid,signal.SIGKILL)
  except ProcessLookupError: pass

for p,h in PINS.items(): assert sha(p)==h,(p,sha(p))
assert SOURCE.stat().st_size==519397 and not ATT.exists()
c=json.loads(CLEAR.read_text()); now=time.time()
assert set(c)=={"schema","status","plan_sha256","source_sha256","manager_clearance","resource_clearance","no_overlap_confirmed","launch_exactly_once","nonce","issued_unix_seconds","expires_unix_seconds"}
assert c["schema"]=="KRENN_X5_RECTANGLE_RANK1_ORBIT0_EXACT_Q_CLEARANCE_V1" and c["status"]=="EXPLICIT_MANAGER_AND_RESOURCE_CLEARANCE"
assert c["plan_sha256"]==PINS[PLAN] and c["source_sha256"]==PINS[SOURCE]
assert c["manager_clearance"] is c["resource_clearance"] is c["no_overlap_confirmed"] is c["launch_exactly_once"] is True
assert len(c["nonce"])>=16 and c["issued_unix_seconds"]<=now<=c["expires_unix_seconds"] and c["expires_unix_seconds"]-c["issued_unix_seconds"]<=900
ATT.mkdir(); pre=census(); atom_json(ATT/"preflight.json",{"schema":"KRENN_X5_RECTANGLE_RANK1_ORBIT0_EXACT_Q_PREFLIGHT_V1","clearance_sha256":sha(CLEAR),"census":pre})
if not pre["pass"]:
 atom_json(ATT/"result.json",{"schema":"KRENN_X5_RECTANGLE_RANK1_ORBIT0_EXACT_Q_RESULT_V1","status":"STOPPED_COMPETING_PROCESS_ZERO_ARITHMETIC"}); raise SystemExit(2)
atomic(ATT/SOURCE.name,SOURCE.read_bytes()); assert sha(ATT/SOURCE.name)==PINS[SOURCE]
outtmp=ATT/"stdout.log.tmp"; errtmp=ATT/"stderr.log.tmp"; started=time.monotonic(); samples=[]; breach=None
with outtmp.open("xb") as out, errtmp.open("xb") as err:
 p=subprocess.Popen([str(GTIMEOUT),"--signal=TERM","--kill-after=10",str(NATIVE),str(SINGULAR),"-q",str(ATT/SOURCE.name)],stdout=out,stderr=err,start_new_session=True)
 while p.poll() is None:
  elapsed=time.monotonic()-started
  try: rss,members=group_rss(p.pid)
  except OSError:
   try: p.wait(timeout=.5); break
   except subprocess.TimeoutExpired: breach="RSS_OBSERVER_FAILURE"; terminate(p); break
  samples.append({"elapsed_seconds":round(elapsed,6),"rss_kib":rss,"members":members})
  if rss>=RSS_CAP_KIB: breach="RSS_CAP"; terminate(p); break
  if elapsed>=WRAPPER: breach="WRAPPER_WALL_CAP"; terminate(p); break
  time.sleep(.25)
 rc=p.wait(); out.flush(); os.fsync(out.fileno()); err.flush(); os.fsync(err.fileno())
os.replace(outtmp,ATT/"stdout.log"); os.replace(errtmp,ATT/"stderr.log")
if breach is None and rc==124: breach="NATIVE_WALL_CAP"
elif breach is None and rc!=0: breach="SINGULAR_NONZERO"
parsed={}
for line in (ATT/"stdout.log").read_text(errors="replace").splitlines():
 if "=" in line:
  k,v=line.split("=",1)
  if k in {"INPUT_VARIABLES","INPUT_GENERATORS","GROEBNER_SIZE","UNIT_REMAINDER","STATUS"}: parsed[k]=v
unit=breach is None and rc==0 and parsed=={"INPUT_VARIABLES":"76","INPUT_GENERATORS":"6571","GROEBNER_SIZE":"1","UNIT_REMAINDER":"0","STATUS":"UNIT_IDEAL"}
wd={"schema":"KRENN_X5_RECTANGLE_RANK1_ORBIT0_EXACT_Q_WATCHDOG_V1","status":"PASS" if breach is None else "TERMINAL_FAILURE","elapsed_seconds":round(time.monotonic()-started,6),"returncode":rc,"breach":breach,"native_wall_seconds":NATIVE,"wrapper_wall_seconds":WRAPPER,"rss_limit_kib":RSS_CAP_KIB,"peak_rss_kib":max((x["rss_kib"] for x in samples),default=None),"samples":samples,"stdout_sha256":sha(ATT/"stdout.log"),"stderr_sha256":sha(ATT/"stderr.log"),"logs_atomic":not outtmp.exists() and not errtmp.exists(),"automatic_relaunch":False,"second_lane":False}
atom_json(ATT/"watchdog.json",wd)
result={"schema":"KRENN_X5_RECTANGLE_RANK1_ORBIT0_EXACT_Q_RESULT_V1","status":"UNIT_IDEAL_EXACT_Q_RANK1_ORBIT0" if unit else "TERMINAL_NONUNIT_OR_FAILURE","field":"Q","rank":1,"orbit":0,"chart":{"diagonal":0,"I":[0],"J":[0]},"source_sha256":sha(ATT/SOURCE.name),"source_bytes":SOURCE.stat().st_size,"parsed_stdout":parsed,"returncode":rc,"breach":breach,"unit_ideal":unit,"rank1_orbit0_closed":unit,"rank12_family_closed":False,"automatic_relaunch":False,"second_lane":False,"preflight_sha256":sha(ATT/"preflight.json"),"watchdog_sha256":sha(ATT/"watchdog.json")}
atom_json(ATT/"result.json",result); print(json.dumps({"status":result["status"],"result_sha256":sha(ATT/"result.json")},sort_keys=True)); raise SystemExit(0 if unit else 1)
