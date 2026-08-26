#!/usr/bin/env python3
import json
from pathlib import Path

r = json.loads((Path(__file__).parent / "results_referee.json").read_text())
assert r["status"] == "PASS_EXACT_61VAR_GLOBAL_UNIT_GAUGE_UNLAUNCHED"
assert r["literal_source_equivalence"]["slice_variables"] == 61
assert r["literal_source_equivalence"]["slice_generators"] == 6568
assert r["primitive_rank_two_minor_gcd"] == 1
assert r["batch_stop_preserved"] is True and r["previously_launched"] is False
assert r["scope"]["singular_runs"] == 0 and r["scope"]["rep2_closed"] is False
print("PASS")
