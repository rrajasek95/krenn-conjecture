#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
result = json.loads((HERE / "result.json").read_text())
assert result["schema"] == "KRENN_X5_REP1_GUARD_MINOR_ONE_LANE_DIAGNOSTIC_V1"
assert result["status"] == "UNIT_IDEAL_MODULAR_DIAGNOSTIC"
assert result["diagnostic_only"] is True and result["mathematical_coverage"] is False
assert result["chart"] == "all-equal-y/i0/p00/x0/y0/d01" and result["field"] == "F_32003"
assert result["termination"] is None and result["returncode"] == 0
assert result["wall_seconds"] < 300 and result["observed_peak_rss_bytes"] < 8 * 1024**3
assert "INPUT_GENERATORS=6577" in result["stdout"]
assert "GROEBNER_SIZE=1" in result["stdout"]
assert "UNIT_REMAINDER=0" in result["stdout"] and "STATUS=UNIT_IDEAL" in result["stdout"]
assert result["stderr"] == ""
assert result["second_lane_launched"] is False and result["exact_Q_launched"] is False
digest = hashlib.sha256((HERE / "result.json").read_bytes()).hexdigest()
print(json.dumps({"status": "PASS_DIAGNOSTIC_ONLY", "result_sha256": digest}, sort_keys=True))
