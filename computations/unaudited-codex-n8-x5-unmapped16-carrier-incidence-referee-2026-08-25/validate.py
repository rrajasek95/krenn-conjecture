#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
result = json.loads((HERE / "results_referee.json").read_text())
assert result["schema"] == "KRENN_X5_UNMAPPED16_CARRIER_INCIDENCE_REFEREE_V1"
assert result["status"] == "PASS_EXACT_DESIGN_ONLY_ZERO_CLOSURE"
assert result["support_census"] == {
    "A12_absent_carriers_each": 40,
    "A12_absent_records": 8,
    "A12_present_carriers_each": 24,
    "A12_present_records": 8,
    "matchings_each": 8,
    "no_rectangle_records": 4,
    "orbit_ids": 8,
    "records": 16,
    "rectangle_records": 12,
}
assert len(result["record_audits"]) == 16
assert result["selected_orientation"]["factorization"] == "[A23^T|A26^T]*K*A47^T"
assert result["singular_rank_design"]["counts"]["1"]["A12_absent_variables"] == 77
assert result["singular_rank_design"]["counts"]["2"]["A12_present_variables"] == 93
assert "zero kernel" in result["invertible_branch_obstruction"]["precise_failure"]
assert result["scope"] == {"D12_reads": False, "ideal_runs": 0, "records_closed": 0, "transport_claim": False}
print(json.dumps({"status": "PASS", "closed": 0, "ideal_runs": 0}, sort_keys=True))
