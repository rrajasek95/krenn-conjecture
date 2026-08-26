#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

here=Path(__file__).resolve().parent
result_path=here/"result.json"; source=here/"rep1_minor_i0_p00_x0_y0_d01_Q.sing"
x=json.loads(result_path.read_text())
assert x["schema"]=="KRENN_X5_REP1_GUARD_MINOR_EXACT_Q_ONE_LANE_V1"
assert x["status"]=="UNIT_IDEAL_EXACT_Q_LOCALIZED_CHART"
assert x["localized_chart_closed"] is True and x["representative_closed"] is False
assert x["field"]=="Q" and x["source_Q_sha256"]==hashlib.sha256(source.read_bytes()).hexdigest()=="53f741ca9173877ef1bc21dba2546a82102a32140221068de1301d0b4635dadb"
assert x["termination"] is None and x["returncode"]==0
assert x["wall_seconds"]<240 and x["observed_peak_rss_bytes"]<8*1024**3
assert all(token in x["stdout"] for token in ("INPUT_GENERATORS=6577","GROEBNER_SIZE=1","UNIT_REMAINDER=0","STATUS=UNIT_IDEAL"))
assert x["stderr"]=="" and x["second_lane_launched"] is False and x["modular_relaunch"] is False and x["automatic_relaunch"] is False
print(json.dumps({"status":"PASS_EXACT_Q_LOCALIZED_CHART","result_sha256":hashlib.sha256(result_path.read_bytes()).hexdigest()},sort_keys=True))
