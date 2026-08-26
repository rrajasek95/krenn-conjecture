#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
result_path = here / "results_referee.json"
plan_path = here / "NEXT3_EXACT_Q_HELD_PLAN.json"
result = json.loads(result_path.read_text())
plan = json.loads(plan_path.read_text())
assert result["status"] == "PASS_EXACT_Q_UNIT_IDEAL_GROUP13_ONLY"
assert result["producer_manifest_sha256"] == "4cf21dec8926b66934fecf998616a31bc06f990b35662a2c48a67d3343dcb5a8"
assert result["producer_result_sha256"] == "66b92e09f73ec629cf09bd235000d64298d4d7987987b95d5f2be088d499e77b"
assert result["source_Q_sha256"] == "336bc28a4affecb31ce32fa468eadb1317efea5fb3ee2d5acbd24fc5f320790a"
assert (result["variables"], result["input_generators"], result["groebner_basis_size"], result["unit_remainder"]) == (91, 6577, 1, 0)
assert result["wall_seconds"] == 24.033887499943376
assert result["peak_rss_bytes"] == 497045504
assert result["atomic_no_tmp"] is True
assert result["observed_later_three_lane_batch_or_relaunch"] is False
assert result["closed_groups"] == [0, 13] and result["closed_group_count"] == 2
assert result["total_group_count"] == 162 and result["representative_1_closed"] is False
assert result["next3_group_ids"] == [15, 17, 25]
assert result["next3_held_plan_sha256"] == hashlib.sha256(plan_path.read_bytes()).hexdigest()
assert plan["launch_authorized"] is False and plan["execution"]["sequential_only"] is True
assert plan["execution"]["maximum_lane_count"] == 3
assert plan["execution"]["automatic_relaunch"] is False
print(json.dumps({"status": "PASS", "result_sha256": hashlib.sha256(result_path.read_bytes()).hexdigest()}, sort_keys=True))
