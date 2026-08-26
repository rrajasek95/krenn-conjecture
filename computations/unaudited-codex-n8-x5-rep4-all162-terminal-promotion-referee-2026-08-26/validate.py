#!/usr/bin/env python3
import json
from pathlib import Path

r = json.loads((Path(__file__).parent / "results_referee.json").read_text())
assert r["status"] == "PASS_REP4_ALL162_PROMOTION_EXACT_SCOPE"
assert r["closed_union"] == list(range(162))
assert r["orbit_census"]["canonical_groups"] == 162
assert r["orbit_census"]["raw_members"] == 972
assert r["rank_zero_scope"]["scope"] == [0]
assert r["scope"]["rep4_closed"] is True
assert r["scope"]["cross_representative_promotion"] is False
assert r["scope"]["full_conjecture_closed"] is False
print("PASS")
