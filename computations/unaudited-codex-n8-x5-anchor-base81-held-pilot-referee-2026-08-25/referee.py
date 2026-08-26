#!/usr/bin/env python3
import ast,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;PKG=ROOT/"computations/unaudited-codex-n8-x5-anchor-no-rectangle-base81-p32003-held-pilot-2026-08-25";DES=ROOT/"computations/unaudited-codex-n8-x5-anchor-no-rectangle-design-2026-08-25"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert h(PKG/"MANIFEST.sha256")=="f7e20f50dd921f600e993d361e4cdcf8a58a83b62b443533384562c0da13779b"
for line in (PKG/"MANIFEST.sha256").read_text().splitlines():
 d,n=line.split(None,1);p=PKG/n.strip();assert h(p)==d,(p,h(p),d)
q=DES/"canonical_reduced_full_x5_Q.sing";assert h(q)=="25b25aac93a336c36c0299c5d6ee9b2a984b5ca0e644170ef235af92f01124f3";s=q.read_text()
a=s.index("ring r=0,(")+len("ring r=0,(");b=s.index("),dp;",a);assert len(s[a:b].split(","))==81
a=s.index("ideal I=")+len("ideal I=");b=s.index(';\nprint("INPUT_VARIABLES',a);body=s[a:b];depth=0;n=1
for c in body:
 if c=="(":depth+=1
 elif c==")":depth-=1
 elif c=="," and depth==0:n+=1
assert depth==0 and n==6561
ep=(PKG/"SOLVER_EPILOGUE.sing").read_text();assert h(PKG/"SOLVER_EPILOGUE.sing")=="4e89c111ad7d0f708bce7296a0d209507dede12b4a2ccfce78be184ccc790500"
derived=s.replace("ring r=0,","ring r=32003,",1).replace("quit;",ep.rstrip(),1);assert derived==(PKG/"base81_p32003.sing").read_text() and h(PKG/"base81_p32003.sing")=="80495d946b3e3078a7538b4762e9151b612533cc2b1445269a1e24f30d3e5dc7"
runner=(PKG/"run_pilot.py").read_text();ast.parse(runner);assert h(PKG/"run_pilot.py")=="90b276285e87741b18f990eb94c4694379601fc1e6a65a4c6f186a2a6726ad8a"
for literal in ["NATIVE_WALL = 180","WRAPPER_WALL = 190","RSS_LIMIT_KIB = 8 * 1024 * 1024","fresh_process_census()","process_group_rss_kib(process.pid)","atomic_json(ATTEMPT / \"result.json\"","usage: run_pilot.py --check-held | --launch"]:assert literal in runner
assert runner.count("subprocess.Popen(")==1 and runner.index("validate_clearance()")<runner.index("subprocess.Popen(") and 'if ATTEMPT.exists() or REFUSAL.exists()' in runner
assert not (PKG/"FRESH_CLEARANCE.json").exists() and not (PKG/"attempt_p32003").exists() and not (PKG/"refusal.json").exists() and not list(PKG.glob("*.tmp"))
x=json.loads((HERE/"results_referee.json").read_text());assert x["status"]=="PASS_APPROVE_HELD_ZERO_RUNS" and x["execution"]["solver_runs"]==0
print(json.dumps({"status":x["status"],"result_sha256":h(HERE/"results_referee.json")}))
