#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
RUN=ROOT/"computations/unaudited-codex-n8-x5-rep5-guard-pivot-k0-modular-held-2026-08-25"
REF=ROOT/"computations/unaudited-codex-n8-x5-rep5-guard-pivot-k0-modular-held-referee-2026-08-25"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def replay(path,base):
 for line in path.read_text().splitlines():
  d,n=line.split(None,1);p=Path(n.strip());p=p if p.is_absolute() else (base/p).resolve();assert h(p)==d,(p,h(p),d)
assert h(REF/"FINAL_MANIFEST.sha256")=="025ab0ac7e165ce1821e4aee9d1a37502d51ee8c0884856d4a2963cb9a32bd6f";replay(REF/"FINAL_MANIFEST.sha256",REF)
assert h(REF/"independent_referee_acceptance.json")=="6aedc8ea5c333403db401bf28ac8216c2dca3f0002c943d8d4ac16cb791a5881"
assert h(RUN/"MANIFEST.sha256")=="e5d31332126ecbe9ca2af75d8c8a1af9a4cc9bc1ef2518b266356496e60bfff1";replay(RUN/"MANIFEST.sha256",RUN);replay(RUN/"TERMINAL_MANIFEST.sha256",RUN)
assert h(RUN/"rep5_p00_guardpivot_k0_p32003.sing")=="dc04c72252144d1a8ff798f49aa1130b1742fff342f21eaf02146b889e3370c1"
assert h(RUN/"run_one_lane.py")=="fdaaea4fead4ec7d47f0a513fa6b8c74a04e4821d1abb4751d32806f9cabc965"
att=json.loads((RUN/"ATTEMPT.json").read_text());assert att["status"]=="ATTEMPT_CONSUMED" and att["relaunch_forbidden_even_if_no_result"]
x=json.loads((RUN/"result.json").read_text())
assert x["status"]=="FAIL_CLOSED_RESOURCE_GATE" and x["termination"]=="NATIVE_WALL_CAP_240"
assert x["diagnostic_only"] and not x["mathematical_coverage"] and x["attempt_consumed"]
assert x["field"]=="F_32003" and x["pivot_k"]==0 and x["variables"]==88 and x["generators"]==6574
assert x["wall_seconds"]>=240 and x["wall_seconds"]<250 and x["observed_peak_group_rss_bytes"]<8589934592
assert x["stderr"]=="" and "INPUT_VARIABLES=88" in x["stdout"] and "INPUT_GENERATORS=6574" in x["stdout"]
assert "GROEBNER_SIZE=" not in x["stdout"] and "UNIT_REMAINDER=" not in x["stdout"] and "STATUS=" not in x["stdout"]
assert x["prelaunch_census"]["match_count"]==0 and x["prelaunch_census"]["unobservable_pids"]==0
assert not x["exact_Q_launched"] and not x["other_k_launched"] and not x["automatic_relaunch"]
assert x["held_manifest_sha256"]==h(RUN/"MANIFEST.sha256") and x["independent_referee_acceptance_sha256"]==h(RUN/"independent_referee_acceptance.json")
assert not list(RUN.rglob("*.tmp")) and len(list(RUN.glob("result.json")))==1
out={"schema":"KRENN_X5_REP5_GUARD_PIVOT_K0_MODULAR_TERMINAL_REFEREE_V1","status":"PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE","field":"F_32003","pivot_k":0,"variables":88,"generators":6574,"termination":"NATIVE_WALL_CAP_240","wall_seconds":x["wall_seconds"],"peak_rss_bytes":x["observed_peak_group_rss_bytes"],"result_sha256":h(RUN/"result.json"),"terminal_manifest_sha256":h(RUN/"TERMINAL_MANIFEST.sha256"),"mathematical_coverage":False,"exact_Q_launched":False,"other_k_launched":False,"automatic_relaunch":False,"attempt_consumed":True,"rep5_chart_closed":False,"seven_block_family_closed":False,"conjecture_closed":False}
(HERE/"results_referee.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":out["status"],"audit_sha256":h(HERE/"results_referee.json")},sort_keys=True))
