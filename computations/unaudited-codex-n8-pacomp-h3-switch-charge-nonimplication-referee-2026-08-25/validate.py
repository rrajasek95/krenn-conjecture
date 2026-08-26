#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
result = json.loads((HERE / "results_countermodel.json").read_text())
assert result["schema"] == "PACOMP_H3_SWITCH_CHARGE_NONIMPLICATION_COUNTERMODEL_V1"
assert result["status"] == "PASS_NO_IMPLICATION_MINIMAL_EXACT_COUNTERMODEL"
assert result["generous_switch_presentation"]["both_switch_families_present"] is True
assert result["generous_switch_presentation"]["boundary_rank"] == 3
assert result["generous_switch_presentation"]["L01_detector_value"] == 2
assert result["retained_face_presentation"]["boundary_rank"] == 3
assert result["retained_face_presentation"]["R_ret_detector_value"] == 1
assert result["smallest_countermodel"]["incoming_source"] == "0"
assert result["charge_product_factor"]["corrected_K14_K24_sum"] == "4564224"
assert result["charge_product_factor"]["interface_to_local_PAComp_source_image"] == "NONE"
assert result["scope"] == {"D12_reads": False, "PAComp_promotion": False, "conjecture_promotion": False, "h": 3, "solves": 0, "symbolic_only": True}
print(json.dumps({"status": "PASS", "promotion": "NONE"}, sort_keys=True))
