#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
path = here / "results_held.json"
result = json.loads(path.read_text())
assert result["status"] == "PASS_MATERIALIZED_SEALED_NOT_LAUNCHED"
assert result["plan_sha256"] == "e778f68f78c087a2d63f4491e0d67d9920302dc55cd2d39e80abc380f66c6ce4"
assert result["independent_manifest_sha256"] == "b1714d0a1d689ebae04017bf6ccb5120861996160cc4a37892542e3592e36761"
assert result["source_sha256"] == "1611c16c73323e7a85ee730ba055f9f2092873841698e8fcc4f5799571ccab04"
assert (result["source_bytes"], result["variables"], result["generators"]) == (1841468, 91, 6577)
assert result["no_external_process_listing"] is True
assert result["direct_libproc_census_and_process_group_rss"] is True
assert result["limits"] == {"lanes": 1, "native_wall_seconds": 240, "wrapper_wall_seconds": 250, "rss_limit_bytes": 8589934592}
assert result["atomic_refuse_overwrite_stop_no_relaunch"] is True
assert result["fresh_clearance_present"] is result["attempt_directory_present"] is result["process_launched"] is False
print(json.dumps({"status": "PASS", "result_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}, sort_keys=True))
