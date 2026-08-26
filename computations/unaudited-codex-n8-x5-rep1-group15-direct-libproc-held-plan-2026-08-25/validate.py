#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parents[1]
census_dir = root / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25"
advice_dir = root / "computations/unaudited-codex-n8-x5-rep1-next3-zero-coverage-failure-referee-2026-08-25"
old_dir = root / "computations/unaudited-codex-n8-x5-rep1-next3-exact-q-batch-2026-08-25"

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

p = json.loads((here / "HELD_GROUP15_PLAN.json").read_text())
assert p["status"] == "HELD_NOT_LAUNCHED"
assert sha(advice_dir / "DISTINCT_GROUP15_DIRECT_LIBPROC_ADVICE.json") == p["authority"]["poincare_advice_sha256"] == "babc0f9e3893fc87f0ec3237960607182a25efe817a0df1125151e1523d88605"
assert sha(advice_dir / "FINAL_MANIFEST.sha256") == p["authority"]["advice_manifest_sha256"] == "2a22ca10d0121d79028955fa68106223d3815b4d81a4d69d8e116fd4a41f60d3"
assert sha(old_dir / "MANIFEST.sha256") == p["relationship_to_old_batch"]["old_batch_manifest_sha256"]
assert sha(census_dir / "MANIFEST.sha256") == p["pins"]["canonical_census_manifest_sha256"]
assert sha(census_dir / "results_canonical_census.json") == p["pins"]["canonical_census_result_sha256"]
census = json.loads((census_dir / "results_canonical_census.json").read_text())
records = [x for x in census["enumeration"]["records"] if x["group_id"] == 15]
assert len(records) == 1
r = records[0]
lane = p["lane"]
assert (r["canonical_chart"] == lane["canonical_chart"] and
        r["exact_Q_source_sha256"] == lane["source_sha256"] and
        r["exact_Q_source_bytes"] == lane["source_bytes"])
assert lane["group_id"] == 15 and lane["field"] == "Q"
assert (lane["native_wall_seconds"],lane["wrapper_wall_seconds"],lane["rss_limit_bytes"]) == (240,250,8589934592)
assert p["process_contract"]["external_process_listing_commands"] == []
assert "libproc" in p["process_contract"]["prelaunch_census"]
assert p["stop_policy"] == {"stop_after_any_terminal_outcome":True,"automatic_relaunch":False,"second_lane":False,"group17_or_group25":False,"patch_in_place":False}
assert p["scope"] == {"launched":False,"singular_process_created":False,"source_materialized":False,"accepted_coverage":0,"representative_1_closed":False}
assert p["relationship_to_old_batch"]["old_batch_status"] == "TERMINAL_ZERO_COVERAGE"
print(json.dumps({"status":"PASS_HELD_GROUP15_ONLY","launched":False,"old_plan_terminal":True},sort_keys=True))
