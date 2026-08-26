#!/usr/bin/env python3
import ast,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
CAN=ROOT/"computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25/rep4_guard_minor_tiny_y_Q.sing";EPI=ROOT/"computations/unaudited-codex-n8-x5-anchor-no-rectangle-base81-p32003-held-pilot-2026-08-25/SOLVER_EPILOGUE.sing"
MOD=ROOT/"computations/unaudited-codex-n8-x5-rep4-all-equal-y-modular-v2-terminal-referee-2026-08-25/FINAL_MANIFEST.sha256"
assert h(MOD)=="fb2a0ab3d036269b34476bf0a8c0f9d6871f7dd312c25efe2691fa1dbbea3cf0" and h(CAN)=="d46cdf77b9edafbc17a92ec851badba2db63640ec7324e024a83e29da04e121b" and h(EPI)=="4e89c111ad7d0f708bce7296a0d209507dede12b4a2ccfce78be184ccc790500"
derived=CAN.read_text().replace("quit;\n",EPI.read_text(),1).encode();src=HERE/"rep4_all_equal_y_exact_Q.sing"
assert len(derived)==1764284 and hashlib.sha256(derived).hexdigest()=="c90c69b11ca931677bc1de138bdfc8c1eb7618d5aee20744764e4a4b1b511019" and src.read_bytes()==derived
assert src.read_text().count("ring r=0,")==1 and "ring r=32003," not in src.read_text() and src.read_text().count("slimgb(I)")==1 and src.read_text().count("reduce(1,G)")==1
assert h(HERE/"HELD_EXACT_Q_PLAN.json")=="ed0a6b95a9cf6e228e22eb588c41de9f6b8140560e4eed853489375526dd31a0" and h(HERE/"run_exact_q.py")=="1892065935daf8ad47530fee138f48ed4a5d6a772320018f6e9d94cfddab894a";ast.parse((HERE/"run_exact_q.py").read_text())
r=(HERE/"run_exact_q.py").read_text();assert "proc_listallpids" in r and "proc_listpgrppids" in r and "proc_pid_rusage" in r and "start_new_session=True" in r and "exclusive_json" in r and "atomic_json" in r
assert "NATIVE_WALL = 480" in r and "WRAPPER_WALL = 510" in r and "RSS_CAP = 8 * 1024**3" in r
assert not (HERE/"independent_referee_acceptance.json").exists() and not (HERE/"launch_clearance.json").exists() and not (HERE/"ATTEMPT.json").exists() and not (HERE/"result.json").exists() and not list(HERE.glob("*.tmp"))
x=json.loads((HERE/"results_held.json").read_text());assert x["status"]=="READY_HELD_ZERO_RUNS_PENDING_INDEPENDENT_PLAN_AUDIT" and all(x["hostile_tests"].values()) and x["execution"]["solver_runs"]==0
print(json.dumps({"status":"PASS_HELD_ZERO_RUNS_PENDING_INDEPENDENT_AUDIT","source_sha256":h(src),"runner_sha256":h(HERE/"run_exact_q.py")},sort_keys=True))
