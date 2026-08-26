#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
RUN=ROOT/"computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-modular-held-2026-08-25";DES=ROOT/"computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert h(RUN/"FINAL_MANIFEST.sha256")=="61a0cce060ff20eba9fe2b3438f468a636ca97a92f41283c72da90aa39ef5415"
for line in (RUN/"FINAL_MANIFEST.sha256").read_text().splitlines():
 d,n=line.split(None,1);p=Path(n.strip());p=p if p.is_absolute() else RUN/p;assert h(p)==d,(p,h(p),d)
assert h(RUN/"result.json")=="d2fbadc777e9331f86070663b99ea7b5ded6e010d750d25b5ddb156a8d071d85" and h(RUN/"run_one_lane.py")=="845bf7928d88b0c1109bc157fbca104423adc76408d1f98b9d470a93df0a180a" and h(RUN/"rep2_all_equal_y_i0_p00_x0_y0_d01_p32003.sing")=="95147044a1703357db2045f393bea44759a854cf5d178b9329b150460ca9abe1"
x=json.loads((RUN/"result.json").read_text());assert x["status"]=="UNIT_IDEAL_MODULAR_DIAGNOSTIC" and x["returncode"]==0 and x["termination"] is None and x["stderr"]==""
assert x["wall_seconds"]==10.12898795795627 and x["observed_peak_rss_bytes"]==700071936 and x["mathematical_coverage"] is False
lines={a:b for a,b in (line.split("=",1) for line in x["stdout"].splitlines() if "=" in line and line.split("=",1)[0] in {"INPUT_VARIABLES","INPUT_GENERATORS","GROEBNER_SIZE","UNIT_REMAINDER","STATUS"})};assert lines=={"INPUT_VARIABLES":"91","INPUT_GENERATORS":"6577","GROEBNER_SIZE":"1","UNIT_REMAINDER":"0","STATUS":"UNIT_IDEAL"}
assert x["exact_Q_launched"] is x["second_lane_launched"] is x["automatic_relaunch"] is False
q=(DES/"rep2_corrected_guard_minor_tiny_y_Q.sing").read_text();ep="\n".join(["ideal G=slimgb(I);",'print("GROEBNER_SIZE="+string(size(G)));',"poly remainder=reduce(1,G);",'print("UNIT_REMAINDER="+string(remainder));','if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',"quit;"])
derived=q.replace("quit;",ep,1).encode();assert len(derived)==1861246 and hashlib.sha256(derived).hexdigest()=="5574a13572a1d68e60cffd97645b143123ee7fdf0c190861f63b796d2f0e1baf"
plan=json.loads((HERE/"EXACT_Q_SAME_CHART_HELD_PLAN.json").read_text());assert plan["status"]=="HELD_NOT_RUN_REQUIRES_EXPLICIT_MANAGER_RESOURCE_CLEARANCE" and not plan["launch_authorized"] and plan["solver_launches"]==0 and not plan["execution_source_materialized"] and not plan["runner_present"] and not plan["clearance_present"]
audit=json.loads((HERE/"results_referee.json").read_text());assert audit["status"]=="PASS_ONE_MODULAR_UNIT_DIAGNOSTIC_ONLY" and audit["mathematical_coverage"] is False
print(json.dumps({"status":audit["status"],"result_sha256":h(HERE/"results_referee.json"),"held_q_plan_sha256":h(HERE/"EXACT_Q_SAME_CHART_HELD_PLAN.json")}))
