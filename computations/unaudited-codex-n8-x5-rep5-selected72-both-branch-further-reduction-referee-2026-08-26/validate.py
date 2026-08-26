#!/usr/bin/env python3
import json
from pathlib import Path

r = json.loads((Path(__file__).parent / "results_referee.json").read_text())
assert r["status"] == "PASS_LITERAL_FOUR_SUBCHART_EXHAUSTIVE_COVER_DESIGN_ONLY"
assert r["combined"] == {"direct_implication_between_parents": False, "every_parent_point_covered": True, "parent_branches": 2, "subcharts": 4}
assert r["open_q1_replay"]["divided_generators"] == 486
assert r["closed_q0_replay"]["nullity_over_Q"] == 1
assert r["smallest_sound_next"]["path"] == "sources/closed_q0_V_a35_21_Q_design.sing"
assert r["scope"]["singular_runs"] == 0 and r["scope"]["rep5_closed"] is False
print("PASS")
