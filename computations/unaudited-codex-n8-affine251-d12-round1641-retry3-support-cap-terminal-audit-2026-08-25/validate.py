#!/usr/bin/env python3
import json
from pathlib import Path

d = json.loads((Path(__file__).parent / "results_terminal_audit.json").read_text())
assert d["status"] == "PASS_TERMINAL_SUPPORT_CAP_ZERO_COVERAGE_STOP_GEOMETRY"
assert d["census"] == {
    "input_columns": 4069711, "new_columns_exposed": 223328, "hybrid_columns": 4293039,
    "computed_rejected_support": 464887, "support_cap": 200000,
    "support_excess": 264887, "accepted_r1641_coverage": 0,
}
assert d["hybrid_headers"]["checkpoint_round"] == 1640
assert d["hybrid_headers"]["checkpoint_old_candidate_support"] == 76616
assert d["hybrid_headers"]["computed_next_support_not_committed"] == 464887
assert d["filesystem"]["dual_absent"] and d["filesystem"]["temporary_outputs_absent"]
assert d["disposition"]["quarantined_non_resumable"]
assert d["disposition"]["geometry_status"] == "STOPPED"
assert d["disposition"]["fourth_escalation_forbidden"]
print("PASS terminal retry3 SUPPORT_CAP audit")
