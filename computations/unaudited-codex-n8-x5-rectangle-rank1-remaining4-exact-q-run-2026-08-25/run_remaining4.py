#!/usr/bin/env python3
from __future__ import annotations
import ctypes, hashlib, json, os, signal, subprocess, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
PLAN=ROOT/"computations/unaudited-codex-n8-x5-rectangle-rank1-remaining4-exact-q-held-plan-2026-08-25/HELD_PLAN.json"
REFEREE=ROOT/"computations/unaudited-codex-n8-x5-rectangle-rank1-remaining4-exact-q-held-plan-referee-2026-08-25/MANIFEST.sha256"
ORBIT0=ROOT/"computations/unaudited-codex-n8-x5-rectangle-rank1-orbit0-exact-q-run-2026-08-25/FINAL_MANIFEST.sha256"
CLEAR=HERE/"FRESH_CLEARANCE.json"; BATCH=HERE/"BATCH_RESULT.json"
SINGULAR=Path("/usr/local/Cellar/singular/4.4.1p5_3/bin/Singular"); GTIMEOUT=Path("/usr/local/Cellar/coreutils/9.11/bin/gtimeout")
LANES=[
 (1,HERE/"orbit1_Q.sing","e7a710e7fcc5514cabf1af9f52b4602ffd95864aa1254072e0345fac7300a607"),
 (2,HERE/"orbit2_Q.sing","39c345eccb667fde9dea0ec2d9a9bed6d80fe637282291ea46e2af445f0c0473"),
 (3,HERE/"orbit3_Q.sing","eaa523eba58edd9df905b5a00edd3084961f1de8075905c5866b093ee5101f9f"),
 (4,HERE/"orbit4_Q.sing","9d4230cbe52732a6cdd809bbe519a83cb3cee5b544378c29876b8e90e79ffcee")]
PINS={PLAN:"e85c4db6414a47d9fb76e4310ab4bd114fc787cda2d766e032a77f9312b08575",REFEREE:"8221f60dbf9da3fbf7e7bcc55916119798758d736088ce2e757d844832b1eb7b",ORBIT0:"b129fdc2775a1fadb5659409ed9f953351cb47d591cef4fc50f5a09276bfbc07",SINGULAR:"9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",GTIMEOUT:"1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",**{p:h for _,p,h in LANES}}
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
 matches=[]
 for pid in pids():
  if pid==os.getpid(): continue
  path=pathname(pid); base=Path(path).name.lower()
  if "singular" in base or "sparse_d12" in base: matches.append({"pid":pid,"path":path})
 return {"observer":"Darwin libproc","matches":matches,"pass":not matches}
def group_rss(pgid):
 total=members=0
 for pid in pids():
  try:
   if os.getpgid(pid)!=pgid: continue
  except (ProcessLookupError,PermissionError): continue
  x=Info(); size=ctypes.sizeof(x)
  if INFO(pid,PROC_PIDTASKINFO,0,ctypes.byref(x),size)==size: total+=x.resident_size//1024; members+=1
 if not members: raise OSError("no observable process-group member")
 return total,members
def terminate(p):
 try: os.killpg(p.pid,signal.SIGTERM)
 except ProcessLookupError:return
 try:p.wait(timeout=2)
 except subprocess.TimeoutExpired:
  try:os.killpg(p.pid,signal.SIGKILL)
  except ProcessLookupError:pass
def run_lane(orbit,source,source_sha):
 att=HERE/f"attempt_orbit{orbit}"; att.mkdir(); pre=census(); atom_json(att/"preflight.json",{"schema":"KRENN_X5_RECTANGLE_RANK1_REMAINING4_PREFLIGHT_V1","orbit":orbit,"clearance_sha256":sha(CLEAR),"census":pre})
 if not pre["pass"]:
  result={"schema":"KRENN_X5_RECTANGLE_RANK1_REMAINING4_LANE_RESULT_V1","status":"STOPPED_COMPETING_PROCESS_ZERO_ARITHMETIC","orbit":orbit,"unit_ideal":False}; atom_json(att/"result.json",result); return result
 atomic(att/source.name,source.read_bytes()); assert sha(att/source.name)==source_sha
 outtmp=att/"stdout.log.tmp"; errtmp=att/"stderr.log.tmp"; started=time.monotonic(); samples=[]; breach=None
 with outtmp.open("xb") as out,errtmp.open("xb") as err:
  p=subprocess.Popen([str(GTIMEOUT),"--signal=TERM","--kill-after=10",str(NATIVE),str(SINGULAR),"-q",str(att/source.name)],stdout=out,stderr=err,start_new_session=True)
  while p.poll() is None:
   elapsed=time.monotonic()-started
   try:rss,members=group_rss(p.pid)
   except OSError:
    try:p.wait(timeout=.5);break
    except subprocess.TimeoutExpired:breach="RSS_OBSERVER_FAILURE";terminate(p);break
   samples.append({"elapsed_seconds":round(elapsed,6),"rss_kib":rss,"members":members})
   if rss>=RSS_CAP_KIB:breach="RSS_CAP";terminate(p);break
   if elapsed>=WRAPPER:breach="WRAPPER_WALL_CAP";terminate(p);break
   time.sleep(.25)
  rc=p.wait();out.flush();os.fsync(out.fileno());err.flush();os.fsync(err.fileno())
 os.replace(outtmp,att/"stdout.log");os.replace(errtmp,att/"stderr.log")
 if breach is None and rc==124:breach="NATIVE_WALL_CAP"
 elif breach is None and rc!=0:breach="SINGULAR_NONZERO"
 parsed={}
 for line in (att/"stdout.log").read_text(errors="replace").splitlines():
  if "=" in line:
   k,v=line.split("=",1)
   if k in {"INPUT_VARIABLES","INPUT_GENERATORS","GROEBNER_SIZE","UNIT_REMAINDER","STATUS"}:parsed[k]=v
 unit=breach is None and rc==0 and parsed=={"INPUT_VARIABLES":"76","INPUT_GENERATORS":"6571","GROEBNER_SIZE":"1","UNIT_REMAINDER":"0","STATUS":"UNIT_IDEAL"}
 wd={"schema":"KRENN_X5_RECTANGLE_RANK1_REMAINING4_WATCHDOG_V1","status":"PASS" if breach is None else "TERMINAL_FAILURE","orbit":orbit,"elapsed_seconds":round(time.monotonic()-started,6),"returncode":rc,"breach":breach,"native_wall_seconds":NATIVE,"wrapper_wall_seconds":WRAPPER,"rss_limit_kib":RSS_CAP_KIB,"peak_rss_kib":max((x["rss_kib"] for x in samples),default=None),"samples":samples,"stdout_sha256":sha(att/"stdout.log"),"stderr_sha256":sha(att/"stderr.log"),"logs_atomic":not outtmp.exists() and not errtmp.exists(),"automatic_relaunch":False,"parallel":False}
 atom_json(att/"watchdog.json",wd)
 result={"schema":"KRENN_X5_RECTANGLE_RANK1_REMAINING4_LANE_RESULT_V1","status":f"UNIT_IDEAL_EXACT_Q_ORBIT{orbit}" if unit else "TERMINAL_NONUNIT_OR_FAILURE","field":"Q","rank":1,"orbit":orbit,"source_sha256":sha(att/source.name),"source_bytes":source.stat().st_size,"parsed_stdout":parsed,"returncode":rc,"breach":breach,"unit_ideal":unit,"preflight_sha256":sha(att/"preflight.json"),"watchdog_sha256":sha(att/"watchdog.json"),"automatic_relaunch":False,"parallel":False};atom_json(att/"result.json",result);return result

for p,h in PINS.items():assert sha(p)==h,(p,sha(p))
assert all(p.stat().st_size==519397 for _,p,_ in LANES) and not BATCH.exists()
assert not any(HERE.glob("attempt_orbit*"))
c=json.loads(CLEAR.read_text());now=time.time();assert c=={"schema":"KRENN_X5_RECTANGLE_RANK1_REMAINING4_CLEARANCE_V1","status":"EXPLICIT_MANAGER_AND_RESOURCE_CLEARANCE","plan_sha256":PINS[PLAN],"referee_manifest_sha256":PINS[REFEREE],"orbit0_manifest_sha256":PINS[ORBIT0],"manager_clearance":True,"resource_clearance":True,"exact_order":[1,2,3,4],"maximum_lanes":4,"no_overlap_confirmed":True,"launch_exactly_once":True,"nonce":c["nonce"],"issued_unix_seconds":c["issued_unix_seconds"],"expires_unix_seconds":c["expires_unix_seconds"]}
assert len(c["nonce"])>=16 and c["issued_unix_seconds"]<=now<=c["expires_unix_seconds"] and c["expires_unix_seconds"]-c["issued_unix_seconds"]<=900
results=[]
for lane in LANES:
 result=run_lane(*lane);results.append({"orbit":lane[0],"result_sha256":sha(HERE/f"attempt_orbit{lane[0]}/result.json"),"status":result["status"]})
 if not result["unit_ideal"]:break
complete=len(results)==4 and all(x["status"].startswith("UNIT_IDEAL") for x in results)
batch={"schema":"KRENN_X5_RECTANGLE_RANK1_REMAINING4_BATCH_RESULT_V1","status":"PASS_ALL_FOUR_UNIT_IDEALS" if complete else "STOPPED_AT_FIRST_FAILURE","attempted_orbits":[x["orbit"] for x in results],"unattempted_orbits":[x for x in [1,2,3,4] if x not in [r["orbit"] for r in results]],"lane_results":results,"all_four_closed":complete,"rank1_family_closed_with_orbit0":complete,"rank2_closed":False,"automatic_relaunch":False,"parallel":False};atom_json(BATCH,batch);print(json.dumps({"status":batch["status"],"batch_sha256":sha(BATCH)},sort_keys=True));raise SystemExit(0 if complete else 1)
