#!/usr/bin/env python3
"""Read-only referee for the strict rep1 groups 1..10 exact-Q schedule."""
import ast,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
P=ROOT/"computations/unaudited-codex-n8-x5-rep1-next10-exact-q-held-2026-08-25"
C=ROOT/"computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25/results_canonical_census.json"
G13=ROOT/"computations/unaudited-codex-n8-x5-rep1-group13-exact-q-referee-2026-08-25/results_referee.json"
G15=ROOT/"computations/unaudited-codex-n8-x5-rep1-group15-exact-q-terminal-referee-2026-08-25/results_referee.json"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pins={P/"MANIFEST.sha256":"33ac399cf348e8bad9de4987369ee43d5839063eb70a15f3dca07e97e10fb04a",P/"source_ledger.json":"9daee573bd3560b381920e72e95dcdb45246f7feaaae02ffcf24e373f6bb6fcd",P/"run_next10.py":"810ba01dc8823f9ea7c9064989720f5ba65b488d19c182ef00886cc8a4941d6b",C:"5ef1acc6ee2b97e993ae930b4ba420ce5c1c8c9eac16995d3a31b5c7a3eb5161",G13:"f156dd0fec67dcfe894e182a33778f4c0a688e39d71bf2d12b92d1cf4f377401",G15:"66d20e4a7991529826ee80288500c41707866d1fa7f0840bd680db927eb0f8a2"}
for p,d in pins.items():assert h(p)==d,(p,h(p),d)
n=0
for line in (P/"MANIFEST.sha256").read_text().splitlines():
 if not line.strip():continue
 d,raw=line.split(None,1);q=Path(raw.strip());q=q if q.is_absolute() else P/q;assert q.is_file() and h(q)==d,q;n+=1
ledger=json.loads((P/"source_ledger.json").read_text());census=json.loads(C.read_text());records={x["group_id"]:x for x in census["enumeration"]["records"]}
lanes=ledger["lanes"];assert [x["group_id"] for x in lanes]==list(range(1,11)) and [x["ordinal"] for x in lanes]==list(range(1,11))
assert ledger["selection"]=={"excluded_closed_groups":[0,13,15],"rule":"ten lowest eligible canonical group IDs in strict ascending order","selected_group_ids":list(range(1,11))}
assert json.loads(G13.read_text())["closed_groups"]==[0,13] and json.loads(G15.read_text())["status"]=="PASS_UNIT_IDEAL_EXACT_Q_GROUP15_ONLY"
def tc(body):
 dep=0;cnt=1
 for ch in body:
  if ch=="(":dep+=1
  elif ch==")":dep-=1;assert dep>=0
  elif ch=="," and dep==0:cnt+=1
 assert dep==0;return cnt
for lane in lanes:
 rec=records[lane["group_id"]];assert rec["closed"] is False
 assert lane["canonical_chart"]==rec["canonical_chart"] and lane["source_sha256"]==rec["exact_Q_source_sha256"] and lane["source_bytes"]==rec["exact_Q_source_bytes"]
 src=P/lane["source_path"];assert h(src)==lane["source_sha256"] and src.stat().st_size==lane["source_bytes"]
 s=src.read_text();a=s.index("ring r=0,(")+len("ring r=0,(");b=s.index("),dp;",a);vs=[x.strip() for x in s[a:b].split(",")];assert len(vs)==len(set(vs))==91
 i=s.index("ideal I=")+len("ideal I=");j=s.index(';\nprint("INPUT_GENERATORS=',i);assert tc(s[i:j])==6577
r=(P/"run_next10.py").read_text();ast.parse(r)
for token in ("proc_listpgrppids","group_rss(process.pid,True)","rusage failure for live member","command=[str(GTIMEOUT)","NATIVE_WALL=240","WRAPPER_WALL=250","RSS_CAP=8*1024**3","exclusive(HERE/'BATCH_ATTEMPT.json'","for lane in lanes:","if not unit:stop=","break","assert [x['group_id'] for x in batch]==list(range(1,1+len(batch)))","parallel':False","relaunch':False","os.replace(t,p)"):assert token in r,token
marker=r.index("exclusive(HERE/'BATCH_ATTEMPT.json'"); execution_loop=r.index("for lane in lanes:",marker)
assert r.count("subprocess.Popen(")==1 and marker<execution_loop<r.index("process=subprocess.Popen")
schedule=json.loads((P/"held_schedule.json").read_text());assert schedule["execution"]["order"]==list(range(1,11)) and schedule["execution"]["parallel"] is schedule["execution"]["skip"] is schedule["execution"]["reorder"] is schedule["execution"]["relaunch"] is False
assert schedule["execution"]["stop_whole_batch_on"]==["NONUNIT","RESOURCE","PROCESS","SCHEMA_OR_TRANSCRIPT_MISMATCH"]
schema=json.loads((P/"independent_referee_acceptance.schema.json").read_text());accept=json.loads((HERE/"independent_referee_acceptance.json").read_text());assert set(accept)==set(schema["required"])
for k,v in accept.items():
 if "const" in schema["properties"][k]:assert v==schema["properties"][k]["const"]
for stale in ("BATCH_ATTEMPT.json","batch_result.json","results","independent_referee_acceptance.json","launch_clearance.json"):assert not (P/stale).exists()
assert not list(P.glob("*.tmp"))
print(json.dumps({"status":"PASS_APPROVED_HELD_STRICT_REP1_NEXT10_ZERO_RUNS","group_ids":list(range(1,11)),"sources":10,"ledger_sha256":h(P/"source_ledger.json"),"runner_sha256":h(P/"run_next10.py"),"manifest_entries":n,"acceptance_sha256":h(HERE/"independent_referee_acceptance.json")},sort_keys=True))
