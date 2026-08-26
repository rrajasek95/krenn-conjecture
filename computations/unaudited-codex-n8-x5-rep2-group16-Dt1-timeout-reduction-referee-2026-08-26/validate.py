#!/usr/bin/env python3
import json
from pathlib import Path

here = Path(__file__).parent
r = json.loads((here / "results_referee.json").read_text())
p = json.loads((here / "HELD_PLAN.json").read_text())
assert r["status"] == "PASS_EXACT_61VAR_GLOBAL_UNIT_TORUS_GAUGE_AND_HELD_LANE"
assert r["literal_source_equivalence"]["slice_variables"] == 61
assert r["literal_source_equivalence"]["slice_generators"] == 6568
assert r["primitive_rank_two_minor_gcd"] == 1
assert r["chart_census"] == {"closed_refined_strata": 2, "original": 57, "other_unclosed_refined_chart": "V(t1,t2) intersect D(t0)", "refined": 60, "remaining": 58, "untouched_original_charts": 56}
assert p["status"] == "APPROVE_HELD_ZERO_RUNS"
assert p["attempts"] == 0 and p["launch_authorized"] is False
assert p["group16_closed_on_success"] is False and p["rep2_closed_on_success"] is False
print("PASS")
