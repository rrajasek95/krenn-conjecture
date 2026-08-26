#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
path = here / "results_referee.json"
advice_path = here / "DISTINCT_GROUP15_DIRECT_LIBPROC_ADVICE.json"
result = json.loads(path.read_text())
advice = json.loads(advice_path.read_text())
assert result["status"] == "PASS_FAIL_CLOSED_ZERO_COVERAGE_OLD_PLAN_TERMINAL"
assert result["producer_manifest_sha256"] == "e7d3e6bb528cf3614690aaf0b8f246975c87d9f6c8a681a8bc2f5c536037af32"
assert result["producer_failure_sha256"] == "d6c039db2db4154be5b0ef4afaa78d81314666284e5b025ded604bac41aa85fb"
assert result["accepted_coverage"] == 0
assert result["group15_directory_empty"] is True
assert result["group17_and_group25_absent"] is True
assert result["source_result_log_watchdog_tmp_files"] == 0
assert result["singular_process_created"] is False
assert all(result["old_plan"].values())
assert result["geometry"] == {"tested": False, "must_stop": False, "distinct_single_group15_contract_logically_permissible": True}
assert result["distinct_group15_advice_sha256"] == hashlib.sha256(advice_path.read_bytes()).hexdigest()
assert advice["launch_authorized"] is False
print(json.dumps({"status": "PASS", "result_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}, sort_keys=True))
