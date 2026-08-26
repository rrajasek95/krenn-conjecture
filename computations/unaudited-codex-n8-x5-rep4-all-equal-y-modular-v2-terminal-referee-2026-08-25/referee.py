#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
RUN=ROOT/"computations/unaudited-codex-n8-x5-rep4-all-equal-y-modular-held-v2-2026-08-25";REF=ROOT/"computations/unaudited-codex-n8-x5-rep4-all-equal-y-modular-held-v2-referee-2026-08-25"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def replay(path,base):
 for line in path.read_text().splitlines():
  d,n=line.split(None,1);p=Path(n.strip());p=p if p.is_absolute() else (base/p).resolve();assert h(p)==d,(p,h(p),d)
assert h(REF/"FINAL_MANIFEST.sha256")=="f8df0b985f0e2e5a825cb6ebc23e0527086da39f3264f1f4912999f22450579f";replay(REF/"FINAL_MANIFEST.sha256",REF)
assert h(RUN/"MANIFEST.sha256")=="27fe22cd124f15d85373db13cbbbed9ca0bb55e23b326247ba695689681012d0";replay(RUN/"MANIFEST.sha256",RUN);replay(RUN/"TERMINAL_MANIFEST.sha256",RUN)
a=json.loads((RUN/"ATTEMPT.json").read_text());x=json.loads((RUN/"result.json").read_text())
assert a["status"]=="ATTEMPT_CONSUMED" and a["relaunch_forbidden_even_if_no_result"] and a["prelaunch_census"]["match_count"]==0 and a["prelaunch_census"]["matches"]==[]
assert x["status"]=="UNIT_IDEAL_MODULAR_DIAGNOSTIC" and x["wrapper_returncode"]==0 and x["termination"] is None and x["stderr"]==""
assert x["stdout"].splitlines()[-6:]==["INPUT_VARIABLES=91","INPUT_GENERATORS=6577","GROEBNER_SIZE=1","UNIT_REMAINDER=0","STATUS=UNIT_IDEAL","Auf Wiedersehen."]
assert x["wall_seconds"]==7.624491041060537 and x["observed_peak_group_rss_bytes"]==726843392 and x["diagnostic_only"] and not x["mathematical_coverage"]
assert not x["exact_Q_launched"] and not x["second_lane_launched"] and not x["automatic_relaunch"] and not list(RUN.glob("*.tmp"))
out={"schema":"KRENN_X5_REP4_MODULAR_V2_TERMINAL_REFEREE_V1","status":"PASS_ONE_MODULAR_UNIT_DIAGNOSTIC_ONLY","field":"F_32003","variables":91,"generators":6577,"groebner_basis_size":1,"unit_remainder":0,"wall_seconds":x["wall_seconds"],"peak_rss_bytes":x["observed_peak_group_rss_bytes"],"result_sha256":h(RUN/"result.json"),"attempt_sha256":h(RUN/"ATTEMPT.json"),"mathematical_coverage":False,"exact_Q_launched":False,"second_lane_launched":False,"automatic_relaunch":False,"rep4_closed":False,"family_closed":False,"conjecture_closed":False}
(HERE/"results_referee.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps({"status":out["status"],"audit_sha256":h(HERE/"results_referee.json")},sort_keys=True))
