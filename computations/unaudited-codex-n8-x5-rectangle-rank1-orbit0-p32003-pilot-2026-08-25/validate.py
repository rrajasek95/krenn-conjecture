#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parents[1]
transcript = Path("/Users/rishi/.codex/sessions/2026/08/20/rollout-2026-08-20T10-31-18-01a01d8b-85a9-7771-9c44-562a6432b402.jsonl")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

expected = {
    "rank1_orbit0_p32003_execute.sing":"7c34d1efbf74220f01a6ea150ede232b9f51f9168f15dd997ed2b204e8aacf9c",
    "run_pilot.py":"bf92688cdf807776971834dcd3d3a84c90de738145edf3f618c09e7798640b19",
    "SUPERSEDING_RESOURCE_CLEAR.json":"dd1583583bb950484116113525a477595f99e3f5594093c206ed93b5e0e03edc",
    "LAUNCH_BINDING.json":"6b4ce0d85bf5387bc9900f3678af575cb3048299c2fe5f150637524f5e24520c",
    "result.json":"17e1ded6a6f42929f3ac8feb92874bc1c1b72725a57fecf3c8e84f23eac9df9a",
}
for name,digest in expected.items(): assert sha(here/name)==digest,(name,sha(here/name),digest)
r=json.loads((here/"result.json").read_text()); p=json.loads((here/"RUN_PROVENANCE.json").read_text())
assert r["status"]==p["terminal_status"]=="UNIT_IDEAL_P32003_RANK1_ORBIT0"
assert (r["field"],r["rank"],r["orbit"])==("F_32003",1,0)
assert r["chart"]=={"diagonal":0,"I":[0],"J":[0]}
assert r["source_sha256"]==p["source_sha256"]==expected["rank1_orbit0_p32003_execute.sing"]
assert r["source_bytes"]==(here/"rank1_orbit0_p32003_execute.sing").stat().st_size==519401
assert r["returncode"]==0 and r["termination"] is None
assert r["orbit_closed_mod_p"] is True and r["exact_Q_closed"] is False and r["representative_closed"] is False
assert r["stderr"]==""
for token in ("INPUT_VARIABLES=76","INPUT_GENERATORS=6571","GROEBNER_SIZE=1","UNIT_REMAINDER=0","STATUS=UNIT_IDEAL"):
    assert r["stdout"].count(token)==1
assert r["second_lane_launched"] is False and r["exact_Q_launched"] is False and r["automatic_relaunch"] is False
assert r["wall_seconds"]==p["wall_seconds_reported_by_runner"]==14.562766416929662
assert r["observed_peak_rss_bytes"]==p["peak_rss_bytes_reported_by_runner"]==468594688 < r["rss_cap_bytes"]==8589934592
assert p["singular_pid"]==85073 and p["returncode"]==0
lines=transcript.read_bytes().splitlines(keepends=True)
for line_no,key in ((102109,"command_execution_line_sha256"),(102110,"tool_output_line_sha256")):
    assert hashlib.sha256(lines[line_no-1]).hexdigest()==p[key]
assert not any(path.suffix==".tmp" for path in here.iterdir())
assert not any("_Q" in path.name or path.name.endswith("_Q.sing") for path in here.iterdir())
source=(here/"rank1_orbit0_p32003_execute.sing").read_text()
assert source.count("ring r=32003,")==1 and "ring r=0," not in source
assert source.count("ideal G=slimgb(I);")==1 and source.count("reduce(1,G)")==1
binding=json.loads((here/"LAUNCH_BINDING.json").read_text()); clearance=json.loads((here/"SUPERSEDING_RESOURCE_CLEAR.json").read_text())
assert binding["runner_sha256"]==expected["run_pilot.py"] and binding["execution_source_sha256"]==expected["rank1_orbit0_p32003_execute.sing"]
assert binding["one_modular_lane_only"] is True and binding["no_exact_Q_or_second_chart_or_relaunch"] is True
assert clearance["one_p32003_lane_only"] is True and clearance["no_overlap_confirmed"] is True
print(json.dumps({"status":"PASS_PRODUCER_SEAL_MODULAR_RANK1_ORBIT0_ONLY","pid":85073,"result_sha256":expected["result.json"],"exact_Q_launched":False},sort_keys=True))
