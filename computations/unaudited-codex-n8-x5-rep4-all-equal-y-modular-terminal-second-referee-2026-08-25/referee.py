#!/usr/bin/env python3
"""Read-only independent referee for the failed-resource rep4 terminal lane."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/"computations/unaudited-codex-n8-x5-rep4-all-equal-y-modular-held-2026-08-25"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pins={RUN/"FINAL_MANIFEST.sha256":"661edff7d15edc81bedd30e5e30e7be0ccc7b5718084311ece141cc13a0bc0e0",RUN/"result.json":"03b0ea4377d26e2e8a50c7ac513e16f72ebee2f5fd260627c89de87376ddf9bd",RUN/"terminal_audit.json":"150b7de45c1a850bf452c1cbeb488d906667eb8e167e761b66cefb98155f361a",RUN/"rep4_all_equal_y_i0_p00_x0_y0_d01_p32003.sing":"9471d6bbfb0af012c313cafa97e12f5b3cea380e6cefb0c8f355cb53def80524",RUN/"run_one_lane.py":"1a0bee89d2f15cfaa82ad25110dc005952deb0bbbf696530e8e435a328065e7f"}
for p,d in pins.items():assert h(p)==d,(p,h(p),d)
n=0
for line in (RUN/"FINAL_MANIFEST.sha256").read_text().splitlines():
 if not line.strip():continue
 d,raw=line.split(None,1);p=Path(raw.strip());p=p if p.is_absolute() else RUN/p;assert p.is_file() and h(p)==d,p;n+=1
x=json.loads((RUN/"result.json").read_text());a=json.loads((RUN/"terminal_audit.json").read_text())
assert x["returncode"]==0 and x["termination"] is None and x["stderr"]==""
for line in ("INPUT_VARIABLES=91","INPUT_GENERATORS=6577","GROEBNER_SIZE=1","UNIT_REMAINDER=0","STATUS=UNIT_IDEAL"):assert x["stdout"].count(line)==1
assert 7.404 < x["wall_seconds"] < 7.406
assert x["observed_peak_rss_bytes"]==0 and x["observed_peak_process_group_count"]==0
assert x["mathematical_coverage"] is False and x["automatic_relaunch"] is False
assert x["exact_Q_launched"] is x["second_lane_launched"] is False and x["cross_representative_equivalence_used"] is False
assert a["status"]=="FAIL_CLOSED_RESOURCE_OBSERVER_WITH_EXACT_UNIT_TRANSCRIPT"
assert a["accepted_mathematical_coverage"] is False
assert a["failure"]["code"]=="PROCESS_GROUP_RSS_OBSERVER_COUNT_BUG"
runner=(RUN/"run_one_lane.py").read_text()
assert "count = returned // ctypes.sizeof(ctypes.c_int)" in runner
assert 'LIBPROC.proc_listpgrppids.restype = ctypes.c_int' in runner
assert not list(RUN.glob("*.tmp"))
print(json.dumps({"status":"PASS_ZERO_PROOF_COVERAGE_EXACT_TRANSCRIPT_RESOURCE_OBSERVER_FAILED","raw_result_sha256":h(RUN/"result.json"),"variables":91,"generators":6577,"basis_size":1,"unit_remainder":0,"wall_seconds":x["wall_seconds"],"manifest_entries":n},sort_keys=True))
