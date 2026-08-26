#!/usr/bin/env python3
"""Read-only independent audit of the anchor base81 exact-Q held plan."""
import ast,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
P=ROOT/"computations/unaudited-codex-n8-x5-anchor-base81-exact-q-held-plan-2026-08-25"
CAN=ROOT/"computations/unaudited-codex-n8-x5-anchor-no-rectangle-design-2026-08-25/canonical_reduced_full_x5_Q.sing"
EPI=ROOT/"computations/unaudited-codex-n8-x5-anchor-no-rectangle-base81-p32003-held-pilot-2026-08-25/SOLVER_EPILOGUE.sing"
MOD=ROOT/"computations/unaudited-codex-n8-x5-anchor-base81-p32003-terminal-referee-2026-08-25"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pins={P/"MANIFEST.sha256":"2a9818993a059993ab2510f188f5952af10245d8f75cb572405d4db77488ac8f",P/"HELD_EXACT_Q_PLAN.json":"053763f0e5534ce6e13a859d6bed1d137de3be0157e0cf42581df2a7a44907d8",P/"base81_exact_Q.sing":"85f75e489e80a12109a82da607d6d1e21498f825f17eea8486f41078b73b39bc",P/"run_exact_q.py":"b4d9d42c9902510ffcec6db125bfe39bf5cbc8e040f4efa8217dd1a0e4f9ecbb",CAN:"25b25aac93a336c36c0299c5d6ee9b2a984b5ca0e644170ef235af92f01124f3",EPI:"4e89c111ad7d0f708bce7296a0d209507dede12b4a2ccfce78be184ccc790500",MOD/"results_referee.json":"ea2cae691c5e8f0eb02d7ff0bf794a230809350c49a844f9374092c2b7532d1f",MOD/"FINAL_MANIFEST.sha256":"7bbaefcf6777a1273c3ab55349bc21106debfc5cf92576ccabe8a1336519ff01"}
for p,d in pins.items(): assert h(p)==d,(p,h(p),d)
n=0
for line in (P/"MANIFEST.sha256").read_text().splitlines():
 if not line.strip():continue
 d,raw=line.split(None,1); q=Path(raw.strip()); q=q if q.is_absolute() else P/q; assert q.is_file() and h(q)==d;q.resolve();n+=1
derived=CAN.read_text().replace("quit;\n",EPI.read_text(),1).encode(); src=P/"base81_exact_Q.sing"
assert src.read_bytes()==derived and len(derived)==420121
s=src.read_text(); assert s.count("ring r=0,")==1 and "ring r=32003," not in s
a=s.index("ring r=0,(")+len("ring r=0,("); b=s.index("),dp;",a); vs=[x.strip() for x in s[a:b].split(",")]; assert len(vs)==len(set(vs))==81
def tc(body):
 depth=0;count=1
 for c in body:
  if c=="(":depth+=1
  elif c==")":depth-=1;assert depth>=0
  elif c=="," and depth==0:count+=1
 assert depth==0;return count
i=s.index("ideal I=")+len("ideal I=");j=s.index(';\nprint("INPUT_VARIABLES=',i);assert tc(s[i:j])==6561
for t in ("ideal G=slimgb(I);","poly remainder=reduce(1,G);","quit;"):assert s.count(t)==1
r=(P/"run_exact_q.py").read_text();ast.parse(r)
for t in ("fresh_process_census()","process_group_rss_kib(process.pid)","start_new_session=True","NATIVE_WALL = 480","WRAPPER_WALL = 510","RSS_LIMIT_KIB = 8 * 1024 * 1024","atomic_bytes","os.replace","ATTEMPT.mkdir()",'automatic_relaunch": False','second_lane": False'):assert t in r,t
assert r.index("validate_clearance()")<r.index("fresh_process_census()",r.index("def launch"))<r.index("ATTEMPT.mkdir()")<r.index("process = subprocess.Popen")
plan=json.loads((P/"HELD_EXACT_Q_PLAN.json").read_text()); result=json.loads((P/"results_held.json").read_text()); refusal=json.loads((P/"REFUSAL_SCHEMA.json").read_text())
assert plan["lane"]=={"field":"Q","maximum_lanes":1,"native_wall_seconds":480,"wrapper_wall_seconds":510,"rss_cap_bytes":8589934592,"fresh_libproc_census":True,"process_group_rss":True,"atomic_outputs":True,"refuse_overwrite":True}
assert plan["solver_launches"]==0 and plan["automatic_relaunch"] is plan["second_lane"] is False
assert result["execution"]["solver_runs"]==0 and all(result["hostile_tests"].values())
assert refusal["properties"]["status"]["const"]=="REFUSED_ZERO_ARITHMETIC_NO_RELAUNCH"
for q in (P/"FRESH_CLEARANCE.json",P/"attempt_exact_q",P/"refusal.json"):assert not q.exists()
assert not list(P.glob("*.tmp")) and not list(P.glob("stdout*")) and not list(P.glob("stderr*")) and not list(P.glob("watchdog*"))
print(json.dumps({"status":"PASS_APPROVED_HELD_EXACT_Q_ZERO_RUNS","source_sha256":h(src),"runner_sha256":h(P/"run_exact_q.py"),"variables":81,"generators":6561,"manifest_entries":n},sort_keys=True))
