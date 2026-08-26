#!/usr/bin/env python3
"""Materialize and run the single cleared rep1 group-13 exact-Q pilot."""
import ctypes,hashlib,importlib.util,json,os,signal,subprocess,time
from pathlib import Path

if not __debug__:raise RuntimeError("fail closed: assertions required")
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
BASE=ROOT/"computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25"
CENSUS=ROOT/"computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25"
REFEREE=ROOT/"computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-referee-2026-08-25"
SINGULAR=Path("/usr/local/bin/Singular");SOURCE=HERE/"rep1_group13_Q.sing"
PINS={
 BASE/"MANIFEST.sha256":"4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1",
 BASE/"generate_minor_quotient.py":"63a4a58344c4bfdce0406d243f881216ca53eaa71264926a28364a823f560ac8",
 CENSUS/"MANIFEST.sha256":"6ed49a2e534955569149eaf2fe80b05aa3513507b41fe44575679eef0271fcb1",
 CENSUS/"results_canonical_census.json":"5ef1acc6ee2b97e993ae930b4ba420ce5c1c8c9eac16995d3a31b5c7a3eb5161",
 REFEREE/"FINAL_MANIFEST.sha256":"f4779fdf166f008ac6ddf98b64a76cae1d1f81cccca1b51ef4b9a9a824b8cd5a",
 SINGULAR:"9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
}
CHART=(0,0,0,1,"z",0,0,2);EXPECTED="336bc28a4affecb31ce32fa468eadb1317efea5fb3ee2d5acbd24fc5f320790a";EXPECTED_BYTES=1841468
NATIVE_WALL=240;RSS_CAP=8*1024**3

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
def load():
 spec=importlib.util.spec_from_file_location("sealed_minor",BASE/"generate_minor_quotient.py");assert spec and spec.loader
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
for path,expected in PINS.items():assert sha(path)==expected,(path,sha(path),expected)
resource_clear=HERE/"RESOURCE_CLEAR.json"
assert resource_clear.exists(),"resource hold: fresh RESOURCE_CLEAR.json required"
resource_record=json.loads(resource_clear.read_text())
assert resource_record=={"status":"EXPLICIT_RESOURCE_CLEAR","group_id":13,"no_overlap_confirmed":True}
assert not (HERE/"result.json").exists()
ledger=json.loads((CENSUS/"results_canonical_census.json").read_text())["enumeration"]["records"][13]
assert ledger["canonical_chart"]==list(CHART) and ledger["exact_Q_source_sha256"]==EXPECTED and ledger["exact_Q_source_bytes"]==EXPECTED_BYTES
minor=load();base=minor.load_base();coordinate,p,q,r,kind,s,a,b=CHART
chart={"coordinate":coordinate,"outside":(p,q),"x_pivot":r,"q_kind":kind,"q_pivot":s,"minor_pair":(a,b)}
program=minor.build_program(base,chart,"0");assert hashlib.sha256(program.encode()).hexdigest()==EXPECTED and len(program.encode())==EXPECTED_BYTES
atomic(SOURCE,program);assert sha(SOURCE)==EXPECTED
started=time.monotonic();process=subprocess.Popen([str(SINGULAR),str(SOURCE)],cwd=HERE,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
print(json.dumps({"event":"STARTED","singular_pid":process.pid}),flush=True);peak=0;termination=None
while process.poll() is None:
 peak=max(peak,rss(process.pid));elapsed=time.monotonic()-started
 if peak>RSS_CAP:termination="RSS_CAP_8GIB"
 elif elapsed>NATIVE_WALL:termination="NATIVE_WALL_CAP_240"
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
unit=termination is None and process.returncode==0 and all(token in stdout for token in ("INPUT_GENERATORS=6577","GROEBNER_SIZE=1","UNIT_REMAINDER=0","STATUS=UNIT_IDEAL"))
nonunit=termination is None and process.returncode==0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout
status="UNIT_IDEAL_EXACT_Q_GROUP13" if unit else "NONUNIT_EXACT_Q_DIAGNOSTIC" if nonunit else "FAIL_CLOSED_RESOURCE_GATE" if termination else "FAIL_CLOSED_PROCESS"
record={"schema":"KRENN_X5_REP1_GROUP13_EXACT_Q_PILOT_V1","status":status,"group_id":13,"chart":list(CHART),"group_closed":unit,"representative_closed":False,"field":"Q","source_sha256":EXPECTED,"source_bytes":EXPECTED_BYTES,"native_wall_cap_seconds":240,"wrapper_wall_cap_seconds":250,"rss_cap_bytes":RSS_CAP,"wall_seconds":wall,"observed_peak_rss_bytes":peak,"termination":termination,"returncode":process.returncode,"stdout":stdout,"stderr":stderr,"pins":{str(path):value for path,value in PINS.items()},"second_lane_launched":False,"optional_microbatch_launched":False,"automatic_relaunch":False}
atomic(HERE/"result.json",json.dumps(record,indent=2,sort_keys=True)+"\n")
print(json.dumps({"event":"TERMINAL","status":status,"wall":wall,"peak":peak},sort_keys=True))
