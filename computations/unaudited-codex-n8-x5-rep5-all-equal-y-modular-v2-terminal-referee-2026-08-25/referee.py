#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
RUN=ROOT/"computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-v2-2026-08-25"
REF=ROOT/"computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-v2-referee-2026-08-25"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def replay(path,base):
 for line in path.read_text().splitlines():
  d,n=line.split(None,1);p=Path(n.strip());p=p if p.is_absolute() else (base/p).resolve();assert h(p)==d,(p,h(p),d)
assert h(REF/"FINAL_MANIFEST.sha256")=="de9477718cef401aace156f2614b31cf576d761dd5d2b53a4f6c994f5d375771";replay(REF/"FINAL_MANIFEST.sha256",REF)
assert h(RUN/"MANIFEST.sha256")=="5b34d345062f5abd65b04744394c80be0c9b6e31017dbb33118ae00be2990b22";replay(RUN/"MANIFEST.sha256",RUN)
replay(RUN/"TERMINAL_MANIFEST.sha256",RUN)
att=json.loads((RUN/"ATTEMPT.json").read_text());x=json.loads((RUN/"result.json").read_text())
assert att["status"]=="ATTEMPT_CONSUMED" and att["relaunch_forbidden_even_if_no_result"]
assert att["prelaunch_census"]["match_count"]==0 and att["prelaunch_census"]["matches"]==[]
assert x["status"]=="FAIL_CLOSED_RESOURCE_GATE" and x["termination"]=="NATIVE_WALL_CAP_180"
assert x["wrapper_returncode"]==0 and x["wall_seconds"]==180.25413474999368 and x["observed_peak_group_rss_bytes"]==3723427840
assert x["stdout"].endswith("INPUT_VARIABLES=91\nINPUT_GENERATORS=6577\n") and "GROEBNER_SIZE=" not in x["stdout"] and "STATUS=" not in x["stdout"]
assert x["stderr"]=="" and x["diagnostic_only"] and not x["mathematical_coverage"]
assert not x["exact_Q_launched"] and not x["second_lane_launched"] and not x["automatic_relaunch"]
assert not (RUN/"watchdog.json").exists() and not list(RUN.glob("*.tmp"))
out={"schema":"KRENN_X5_REP5_MODULAR_V2_TERMINAL_REFEREE_V1","status":"PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE","result_sha256":h(RUN/"result.json"),"attempt_sha256":h(RUN/"ATTEMPT.json"),"source_sha256":x["source_sha256"],"variables":91,"generators":6577,"wall_seconds":x["wall_seconds"],"peak_rss_bytes":x["observed_peak_group_rss_bytes"],"termination":x["termination"],"unit_or_nonunit_result":False,"mathematical_coverage":False,"attempt_consumed":True,"automatic_relaunch":False,"exact_Q_launched":False,"second_lane_launched":False,"rep5_closed":False,"family_closed":False,"conjecture_closed":False}
(HERE/"results_referee.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":out["status"],"audit_sha256":h(HERE/"results_referee.json")},sort_keys=True))
