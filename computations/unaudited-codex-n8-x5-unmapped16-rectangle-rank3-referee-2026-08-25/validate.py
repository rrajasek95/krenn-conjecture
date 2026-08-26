#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
result = json.loads((HERE / "results_referee.json").read_text())
assert result["status"] == "PASS_EXACT_REDUCTION_DESIGN_ONLY_NO_CLOSURE"
assert result["guard_rank3"]["elimination"] == "A46=-A47*A26^T"
assert result["guard_rank3"]["one_sided_inverse"] == "A17*A26=I"
assert result["guard_rank3"]["two_sided_inverse"].startswith("A26*A17=I")
assert result["carrier_census"] == {
    "A12_absent": {"forced_zero_kernel": 22, "guard_undecided": 18, "total": 40},
    "A12_present": {"forced_zero_kernel": 10, "guard_undecided": 14, "total": 24},
}
assert result["guard_only_no_go"]["universal_carrier_exists"] is False
assert result["full_X5_projection"]["amplitude_inactive"] == ["A12", "A23"]
assert result["full_X5_projection"]["established_variables"] == 64
assert result["full_X5_projection"]["established_generators"] == 6571
assert result["smallest_sound_next_ideal"]["variables"] == 56
assert result["smallest_sound_next_ideal"]["generators"] == 6563
assert result["smallest_sound_next_ideal"]["status"] == "HELD_NOT_MATERIALIZED_NOT_RUN"
assert result["scope"] == {"D12_reads": False, "ideal_runs": 0, "rank3_closed": False, "transported_records": 0}
print(json.dumps({"status": "PASS", "runs": 0, "next": "HELD"}, sort_keys=True))
