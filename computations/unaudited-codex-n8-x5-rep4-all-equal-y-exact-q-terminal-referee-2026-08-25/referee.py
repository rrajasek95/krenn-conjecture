#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
RUN=ROOT/"computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-held-plan-2026-08-25"
REF=ROOT/"computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-held-plan-referee-2026-08-25"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def replay(path,base):
 for line in path.read_text().splitlines():
  d,n=line.split(None,1);p=Path(n.strip());p=p if p.is_absolute() else (base/p).resolve();assert h(p)==d,(p,h(p),d)
assert h(REF/"FINAL_MANIFEST.sha256")=="a3c78897012074016ae2fd105d4a06d33d605a531aa65c7c52dc494b1988a947";replay(REF/"FINAL_MANIFEST.sha256",REF)
assert h(REF/"independent_referee_acceptance.json")=="e5e3a7ce1d048d126418f478bde7672cebc4436f7b3ac77161a0a67c4113f52a"
assert h(RUN/"MANIFEST.sha256")=="7b93ce7bee8ac3d8bad0384490ee511a819e9c4b1d800b776dc8016897a30d20";replay(RUN/"MANIFEST.sha256",RUN);replay(RUN/"TERMINAL_MANIFEST.sha256",RUN)
assert h(RUN/"HELD_EXACT_Q_PLAN.json")=="ed0a6b95a9cf6e228e22eb588c41de9f6b8140560e4eed853489375526dd31a0"
assert h(RUN/"rep4_all_equal_y_exact_Q.sing")=="c90c69b11ca931677bc1de138bdfc8c1eb7618d5aee20744764e4a4b1b511019"
assert h(RUN/"run_exact_q.py")=="1892065935daf8ad47530fee138f48ed4a5d6a772320018f6e9d94cfddab894a"
att=json.loads((RUN/"ATTEMPT.json").read_text());assert att["status"]=="ATTEMPT_CONSUMED" and att["relaunch_forbidden_even_if_no_result"]
x=json.loads((RUN/"result.json").read_text())
assert x["status"]=="UNIT_IDEAL_EXACT_Q_SAME_CHART" and x["mathematical_coverage"] and x["same_chart_only"]
assert x["field"]=="Q" and x["variables"]==91 and x["generators"]==6577
assert x["termination"] is None and x["wrapper_returncode"]==0 and x["stderr"]==""
required=["INPUT_VARIABLES=91","INPUT_GENERATORS=6577","GROEBNER_SIZE=1","UNIT_REMAINDER=0","STATUS=UNIT_IDEAL","Auf Wiedersehen."]
lines=x["stdout"].splitlines();assert lines[-6:]==required
assert x["wall_seconds"]<480 and x["observed_peak_group_rss_bytes"]<8589934592
assert x["prelaunch_census"]["match_count"]==0 and x["prelaunch_census"]["unobservable_pids"]==0
assert x["exact_Q_launched"] and not x["second_lane_launched"] and not x["automatic_relaunch"] and not x["rep2_equivalence_used"]
assert x["held_manifest_sha256"]==h(RUN/"MANIFEST.sha256") and x["independent_referee_acceptance_sha256"]==h(RUN/"independent_referee_acceptance.json")
assert not list(RUN.rglob("*.tmp")) and len(list(RUN.glob("result.json")))==1
out={"schema":"KRENN_X5_REP4_ALL_EQUAL_Y_EXACT_Q_TERMINAL_REFEREE_V1","status":"PASS_EXACT_Q_UNIT_IDEAL_REP4_ALL_EQUAL_Y_SAME_CHART","field":"Q","variables":91,"generators":6577,"groebner_basis_size":1,"unit_remainder":0,"source_sha256":h(RUN/"rep4_all_equal_y_exact_Q.sing"),"result_sha256":h(RUN/"result.json"),"wall_seconds":x["wall_seconds"],"peak_rss_bytes":x["observed_peak_group_rss_bytes"],"same_chart_closed":True,"second_lane_launched":False,"automatic_relaunch":False,"rep4_representative_closed":False,"seven_block_family_closed":False,"conjecture_closed":False,"terminal_manifest_sha256":h(RUN/"TERMINAL_MANIFEST.sha256")}
(HERE/"results_referee.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":out["status"],"audit_sha256":h(HERE/"results_referee.json")},sort_keys=True))
