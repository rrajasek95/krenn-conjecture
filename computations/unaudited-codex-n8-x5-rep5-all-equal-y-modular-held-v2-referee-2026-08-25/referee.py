#!/usr/bin/env python3
"""Read-only referee proving the six v1 rejection defects are repaired in v2."""
from __future__ import annotations
import ast, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
V2 = ROOT / "computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-v2-2026-08-25"
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25"
REJECTION = ROOT / "computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-referee-2026-08-25"
SOURCE = V2 / "rep5_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"
ORIGINAL = DESIGN / "rep5_guard_minor_tiny_y_p32003.sing"
RUNNER = V2 / "run_one_lane.py"

PINS = {
 V2/"MANIFEST.sha256":"5b34d345062f5abd65b04744394c80be0c9b6e31017dbb33118ae00be2990b22",
 V2/"held_pilot.json":"102b64290da614b9430ee9db090c4c4d22bd8a2295fa725764f72bb31d494f8b",
 SOURCE:"33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97",
 ORIGINAL:"33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97",
 RUNNER:"9eaef175601f51dcd7a50321fc80d02dc71ec81b91a8f13f02116d3b76cdadb9",
 REJECTION/"FINAL_MANIFEST.sha256":"02adea071c6f3eef5a4623ec25afb12f06dd38cec5426a7eed6ced74ff194dbb",
 REJECTION/"results_referee.json":"90ba1b91d1c7b27509227c74be7b03e0bb72aeac7ea8ab3a24ede4f39b500c14",
}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def replay(path,base):
 n=0
 for line in path.read_text().splitlines():
  if not line.strip(): continue
  d,raw=line.split(None,1); p=Path(raw.strip())
  if not p.is_absolute(): p=base/p
  assert p.is_file() and sha(p)==d,p; n+=1
 return n
def top_count(body):
 depth=0; count=1 if body.strip() else 0
 for c in body:
  if c=="(": depth+=1
  elif c==")": depth-=1; assert depth>=0
  elif c=="," and depth==0: count+=1
 assert depth==0; return count
for p,d in PINS.items(): assert sha(p)==d,(p,sha(p),d)
entries=replay(V2/"MANIFEST.sha256",V2)
assert SOURCE.read_bytes()==ORIGINAL.read_bytes() and SOURCE.stat().st_size==1950700
s=SOURCE.read_text(); a=s.index("ring r=32003,(")+len("ring r=32003,("); b=s.index("),dp;",a)
vars=[x.strip() for x in s[a:b].split(",")]; assert len(vars)==len(set(vars))==91
i=s.index("ideal I=")+len("ideal I="); j=s.index(';\nprint("INPUT_VARIABLES=',i); assert top_count(s[i:j])==6577
for t in ("ideal G=slimgb(I);","poly remainder=reduce(1,G);","quit;"): assert s.count(t)==1
r=RUNNER.read_text(); ast.parse(r)
repair_tokens={
 "NO_FRESH_PROCESS_CENSUS":["proc_listallpids","proc_pidpath","fresh_process_census()",'census["match_count"] == 0'],
 "RSS_OBSERVER_FAILS_OPEN":["def process_rss_bytes(pid: int) -> int | None",'raise RuntimeError(f"rusage observation failure for live group member {pid}")',"RESOURCE_OBSERVER_FAILURE:"],
 "RSS_NOT_PROCESS_GROUP_SUM":["proc_listpgrppids","process_group_pids(pgid)","total += rss"],
 "WRAPPER_NOT_ENFORCED_BY_PINNED_RUNNER":["command = [str(GTIMEOUT)", 'f"{WRAPPER_WALL}s"',"process = subprocess.Popen(command"],
 "CLEARANCE_NOT_FRESH_OR_SINGLE_USE":["nonce","issued_at_utc","expires_at_utc","MAX_CLEARANCE_LIFETIME_SECONDS = 600","no_overlap_confirmed","manager_clearance_confirmed","resource_clearance_confirmed"],
 "ABRUPT_FAILURE_CAN_BE_RELAUNCHED":["exclusive_json(HERE / \"ATTEMPT.json\"","relaunch_forbidden_even_if_no_result","ATTEMPT.json","result.json.tmp","stale temporary exists"],
}
for defect,tokens in repair_tokens.items():
 for token in tokens: assert token in r,(defect,token)
assert r.index("clearance_and_census()") < r.index("exclusive_json(HERE / \"ATTEMPT.json\"") < r.index("process = subprocess.Popen(command")
clear=json.loads((V2/"launch_clearance.schema.json").read_text()); acc_schema=json.loads((V2/"independent_referee_acceptance.schema.json").read_text())
assert clear["additionalProperties"] is False and set(clear["required"])==set(clear["properties"])
for key in ("nonce","issued_at_utc","expires_at_utc","no_overlap_confirmed","manager_clearance_confirmed","resource_clearance_confirmed","census_policy_sha256","expected_census_match_count"): assert key in clear["properties"]
assert clear["properties"]["native_wall_seconds"]=={"const":180} and clear["properties"]["wrapper_wall_seconds"]=={"const":195} and clear["properties"]["rss_cap_bytes"]=={"const":8589934592}
accept=json.loads((HERE/"independent_referee_acceptance.json").read_text())
assert set(accept)==set(acc_schema["required"])
for k,v in accept.items():
 if k in acc_schema["properties"] and "const" in acc_schema["properties"][k]: assert v==acc_schema["properties"][k]["const"]
held=json.loads((V2/"held_pilot.json").read_text()); refusal=json.loads((V2/"refusal_contract.json").read_text())
assert all(held["hostile_tests"].values()) and held["scope"]["ideal_runs"]==0 and held["scope"]["attempt_marker_created"] is False
assert set(refusal["defect_repairs"])==set(repair_tokens) and refusal["status"]=="ARMED_ZERO_LAUNCH_SINGLE_USE"
for stale in ("ATTEMPT.json","result.json","result.json.tmp","stdout.log","stderr.log","watchdog.json","independent_referee_acceptance.json","launch_clearance.json"): assert not (V2/stale).exists()
assert not list(V2.glob("*.tmp"))
print(json.dumps({"status":"PASS_APPROVED_HELD_ALL_SIX_DEFECTS_FIXED_ZERO_RUNS","source_sha256":sha(SOURCE),"runner_sha256":sha(RUNNER),"variables":91,"generators":6577,"defects_fixed":len(repair_tokens),"manifest_entries":entries,"acceptance_sha256":sha(HERE/"independent_referee_acceptance.json")},sort_keys=True))
