#!/usr/bin/env python3
"""Run exactly one superseded rectangle rank1/orbit0 p32003 pilot."""
import ctypes, hashlib, json, os, signal, subprocess, time
from pathlib import Path
if not __debug__:raise RuntimeError("fail closed: assertions required")
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
SOURCE=HERE/"rank1_orbit0_p32003_execute.sing";SINGULAR=Path("/usr/local/bin/Singular")
HELD=ROOT/"computations/unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-referee-2026-08-25/STAGED_PILOT_HELD_PLAN.json"
FAILED=ROOT/"computations/unaudited-codex-n8-x5-rep1-next3-exact-q-batch-2026-08-25/MANIFEST.sha256"
PINS={SOURCE:"7c34d1efbf74220f01a6ea150ede232b9f51f9168f15dd997ed2b204e8aacf9c",HELD:"95120b83be0d16fb16b7814556c676caa7a01c1436e85ed884db98a210571c34",FAILED:"e7d3e6bb528cf3614690aaf0b8f246975c87d9f6c8a681a8bc2f5c536037af32",SINGULAR:"9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"}
NATIVE=180;RSS_CAP=8*1024**3
class RUsageInfoV2(ctypes.Structure):
 _fields_=[("uuid",ctypes.c_uint8*16),("user_time",ctypes.c_uint64),("system_time",ctypes.c_uint64),("pkg_idle_wkups",ctypes.c_uint64),("interrupt_wkups",ctypes.c_uint64),("pageins",ctypes.c_uint64),("wired_size",ctypes.c_uint64),("resident_size",ctypes.c_uint64),("phys_footprint",ctypes.c_uint64),("proc_start_abstime",ctypes.c_uint64),("proc_exit_abstime",ctypes.c_uint64),("child_user_time",ctypes.c_uint64),("child_system_time",ctypes.c_uint64),("child_pkg_idle_wkups",ctypes.c_uint64),("child_interrupt_wkups",ctypes.c_uint64),("child_pageins",ctypes.c_uint64),("child_elapsed_abstime",ctypes.c_uint64),("diskio_bytesread",ctypes.c_uint64),("diskio_byteswritten",ctypes.c_uint64)]
LIBPROC=ctypes.CDLL("/usr/lib/libproc.dylib");LIBPROC.proc_pid_rusage.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_void_p];LIBPROC.proc_pid_rusage.restype=ctypes.c_int
def rss(pid):
 record=RUsageInfoV2();return record.resident_size if LIBPROC.proc_pid_rusage(pid,2,ctypes.byref(record))==0 else 0
def sha(path):
 h=hashlib.sha256()
 with path.open("rb") as stream:
  while chunk:=stream.read(1<<20):h.update(chunk)
 return h.hexdigest()
def atomic(path,text):
 tmp=path.with_suffix(path.suffix+".tmp");tmp.write_text(text);os.replace(tmp,path)
for path,expected in PINS.items():assert sha(path)==expected,(path,sha(path),expected)
clear=HERE/"SUPERSEDING_RESOURCE_CLEAR.json";assert clear.exists(),"superseding clearance required"
record=json.loads(clear.read_text());assert record=={"status":"EXPLICIT_SUPERSEDING_RESOURCE_CLEAR","held_plan_sha256":PINS[HELD],"execution_source_sha256":PINS[SOURCE],"resource_clear_manifest_sha256":PINS[FAILED],"one_p32003_lane_only":True,"no_overlap_confirmed":True}
assert not (HERE/"result.json").exists()
started=time.monotonic();process=subprocess.Popen([str(SINGULAR),str(SOURCE)],cwd=HERE,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
print(json.dumps({"event":"STARTED","singular_pid":process.pid,"source_sha256":PINS[SOURCE]}),flush=True)
peak=0;termination=None
while process.poll() is None:
 peak=max(peak,rss(process.pid));elapsed=time.monotonic()-started
 if peak>RSS_CAP:termination="RSS_CAP_8GIB"
 elif elapsed>NATIVE:termination="NATIVE_WALL_CAP_180"
 if termination:
  try:os.killpg(process.pid,signal.SIGTERM)
  except ProcessLookupError:pass
  time.sleep(.2)
  if process.poll() is None:
   try:os.killpg(process.pid,signal.SIGKILL)
   except ProcessLookupError:pass
  break
 time.sleep(.1)
stdout,stderr=process.communicate();wall=time.monotonic()-started
unit=termination is None and process.returncode==0 and all(token in stdout for token in ("INPUT_VARIABLES=76","INPUT_GENERATORS=6571","GROEBNER_SIZE=1","UNIT_REMAINDER=0","STATUS=UNIT_IDEAL"))
nonunit=termination is None and process.returncode==0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout
status="UNIT_IDEAL_P32003_RANK1_ORBIT0" if unit else "NONUNIT_P32003_DIAGNOSTIC" if nonunit else "FAIL_CLOSED_RESOURCE_GATE" if termination else "FAIL_CLOSED_PROCESS"
out={"schema":"KRENN_X5_RECTANGLE_RANK1_ORBIT0_P32003_PILOT_V1","status":status,"field":"F_32003","rank":1,"orbit":0,"chart":{"diagonal":0,"I":[0],"J":[0]},"orbit_closed_mod_p":unit,"exact_Q_closed":False,"representative_closed":False,"source_sha256":PINS[SOURCE],"source_bytes":SOURCE.stat().st_size,"native_wall_cap_seconds":180,"wrapper_wall_cap_seconds":195,"rss_cap_bytes":RSS_CAP,"wall_seconds":wall,"observed_peak_rss_bytes":peak,"termination":termination,"returncode":process.returncode,"stdout":stdout,"stderr":stderr,"pins":{str(path):value for path,value in PINS.items()},"second_lane_launched":False,"exact_Q_launched":False,"automatic_relaunch":False}
atomic(HERE/"result.json",json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({"event":"TERMINAL","status":status,"wall":wall,"peak":peak},sort_keys=True))
