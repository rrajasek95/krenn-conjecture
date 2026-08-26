#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
result = json.loads((HERE / "results_referee.json").read_text())
assert result["status"] == "PASS_INDEPENDENT_NO_CROSS_REPRESENTATIVE_ISOMORPHISMS"
assert result["producer_pins"] == {
    "manifest_sha256": "67dd1446276a21321a550dc12c74e60ed4d78e1122848cb2b96b2c2f13f3b134",
    "result_sha256": "79d73aee9fdae65338557b3ba74032eb3395b113d46d5b29b6d289c6e6036cd6",
    "ledger_sha256": "ba6b0cc98309c860c1b91d024eb5effe050790ceae60ec1995385b8d7be73cd7",
}
support = result["support_referee"]
assert support["site_maps_tested"] == 645120
assert support["site_permutations_per_ordered_pair"] == 40320
assert support["isomorphism_counts"] == {
    str(a): {str(b): int(a == b) for b in (1, 2, 4, 5)} for a in (1, 2, 4, 5)
}
grading = result["grading_referee"]
assert grading["variables_per_chart"] == 91 and grading["generators_per_chart"] == 6577
assert grading["full_word_covariance_checks"] == 157464
assert len(grading["materialized_sources_checked"]) == 7
charts = result["chart_referee"]
assert charts["total_raw"] == charts["raw_chart_maps"] == 3888
assert charts["total_classes"] == 648 and charts["members_per_class"] == 6
assert charts["generator_family_maps"] == 25571376
assert charts["minor_sign_census"] == {"-1": 1944, "1": 1944}
scope = result["theorem_scope"]
assert scope["cross_generator_isomorphisms"] == 0
assert scope["solver_runs"] == 0 and scope["ideal_or_closure_claim"] is False
print(json.dumps({"status": "PASS", "result_sha256": sha(HERE / "results_referee.json")}, sort_keys=True))
