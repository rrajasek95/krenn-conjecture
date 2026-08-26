#!/usr/bin/env python3
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "results_seven_block_closure_referee.json").read_text())
assert data["status"] == "REJECT_COMPLETE_CLOSURE_EXACT_8_OF_64_PROVED"
assert data["census"] == {
    "boundary_records": 64,
    "two_sandwich_records": 64,
    "representative_supports_with_guard_mates": 12,
    "validly_covered_records": 8,
    "uncovered_records": 56,
    "uncovered_bad_activity_inference": 40,
    "uncovered_no_representative_support": 16,
}
assert len({(tuple(x["added"]), tuple(x["nonzero_variable_blocks"])) for x in data["covered"]}) == 8
assert len({(tuple(x["added"]), tuple(x["nonzero_variable_blocks"])) for x in data["uncovered"]}) == 56
assert {x["orbit_id"] for x in data["covered"]} == {8, 9, 10, 11}
assert {x["orbit_id"] for x in data["uncovered"]} == set(range(32)) - {8, 9, 10, 11}
hostile = data["tensor_referee"]["hostile_counterexample"]
assert hostile["identity_in_response_row_space"] is False
assert hostile["K00_identically_zero_on_kernel"] is True
assert hostile["star_active"] is False
print("PASS seven-block closure referee: exact proof coverage 8/64; uncovered 56/64")
