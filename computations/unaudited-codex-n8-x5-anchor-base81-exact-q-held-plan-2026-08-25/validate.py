#!/usr/bin/env python3
import ast,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
CAN=ROOT/"computations/unaudited-codex-n8-x5-anchor-no-rectangle-design-2026-08-25/canonical_reduced_full_x5_Q.sing"
EPI=ROOT/"computations/unaudited-codex-n8-x5-anchor-no-rectangle-base81-p32003-held-pilot-2026-08-25/SOLVER_EPILOGUE.sing"
MOD=ROOT/"computations/unaudited-codex-n8-x5-anchor-base81-p32003-terminal-referee-2026-08-25"
assert h(MOD/"FINAL_MANIFEST.sha256")=="7bbaefcf6777a1273c3ab55349bc21106debfc5cf92576ccabe8a1336519ff01"
assert h(CAN)=="25b25aac93a336c36c0299c5d6ee9b2a984b5ca0e644170ef235af92f01124f3" and CAN.stat().st_size==419891
assert h(EPI)=="4e89c111ad7d0f708bce7296a0d209507dede12b4a2ccfce78be184ccc790500"
derived=CAN.read_text().replace("quit;\n",EPI.read_text(),1).encode();src=HERE/"base81_exact_Q.sing"
assert len(derived)==420121 and hashlib.sha256(derived).hexdigest()=="85f75e489e80a12109a82da607d6d1e21498f825f17eea8486f41078b73b39bc" and src.read_bytes()==derived
assert src.read_text().count("ring r=0,")==1 and "ring r=32003," not in src.read_text()
assert src.read_text().count("slimgb(I)")==1 and src.read_text().count("reduce(1,G)")==1 and src.read_text().count("quit;")==1
assert h(HERE/"HELD_EXACT_Q_PLAN.json")=="053763f0e5534ce6e13a859d6bed1d137de3be0157e0cf42581df2a7a44907d8"
assert h(HERE/"run_exact_q.py")=="b4d9d42c9902510ffcec6db125bfe39bf5cbc8e040f4efa8217dd1a0e4f9ecbb";ast.parse((HERE/"run_exact_q.py").read_text())
plan=json.loads((HERE/"HELD_EXACT_Q_PLAN.json").read_text());assert not plan["launch_authorized"] and plan["solver_launches"]==0 and plan["lane"]=={"field":"Q","maximum_lanes":1,"native_wall_seconds":480,"wrapper_wall_seconds":510,"rss_cap_bytes":8589934592,"fresh_libproc_census":True,"process_group_rss":True,"atomic_outputs":True,"refuse_overwrite":True}
runner=(HERE/"run_exact_q.py").read_text();assert "Darwin libproc" in runner and "start_new_session=True" in runner and "os.replace" in runner
assert "NATIVE_WALL = 480" in runner and "WRAPPER_WALL = 510" in runner and "RSS_LIMIT_KIB = 8 * 1024 * 1024" in runner
assert not (HERE/"FRESH_CLEARANCE.json").exists() and not (HERE/"attempt_exact_q").exists() and not (HERE/"refusal.json").exists() and not list(HERE.glob("*.tmp"))
x=json.loads((HERE/"results_held.json").read_text());assert x["status"]=="READY_HELD_ZERO_RUNS_PENDING_INDEPENDENT_PLAN_AUDIT" and x["execution"]=={"solver_runs":0,"attempt_absent":True,"refusal_absent":True,"clearance_absent":True,"temporary_absent":True}
assert all(x["hostile_tests"].values())
print(json.dumps({"status":"PASS_HELD_ZERO_RUNS_PENDING_INDEPENDENT_AUDIT","source_sha256":h(src),"runner_sha256":h(HERE/"run_exact_q.py")},sort_keys=True))
