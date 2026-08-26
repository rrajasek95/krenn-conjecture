#!/usr/bin/env python3
"""Independent exact-ledger referee; no Singular or source materialization."""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRODUCER = ROOT / "computations/unaudited-codex-n8-x5-rep2-all162-terminal-promotion-conditional-design-2026-08-26"
PRODUCER_MANIFEST_SHA = "a737bbc0da1b759500ab99ce352fedf7923f1cc25b9c9f997ef6df0079bcadb0"
PRODUCER_RESULT_SHA = "fb15f3148a89f6e6f5e76e0eb37aaef4963a470b088cf9891896ad0d7a3e630f"
CENSUS = ROOT / "computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25/canonical_census.json"
CENSUS_SHA = "5ee661f3fdfd0e35e75d92d6efe7700b83011049e1d74a712ba8918681f86c8a"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha256(PRODUCER / "MANIFEST.sha256") == PRODUCER_MANIFEST_SHA
seen = set()
for raw in (PRODUCER / "MANIFEST.sha256").read_text().splitlines():
    match = re.fullmatch(r"([0-9a-f]{64})  (.+)", raw); assert match
    digest, relative = match.groups(); target = (PRODUCER / relative).resolve(strict=True)
    assert ROOT in target.parents and target not in seen and sha256(target) == digest
    seen.add(target)
result_path = PRODUCER / "results_terminal_promotion_design.json"
assert result_path.resolve() in seen and sha256(result_path) == PRODUCER_RESULT_SHA
r = json.loads(result_path.read_text())
f = json.loads((PRODUCER / "future_dependencies.json").read_text())
h = json.loads((PRODUCER / "results_hostile_tests.json").read_text())
s = json.loads((PRODUCER / "terminal_promotion_acceptance.schema.json").read_text())
c = json.loads(CENSUS.read_text()); assert sha256(CENSUS) == CENSUS_SHA
assert c["status"] == "PASS_REGENERATED_AUTHORITATIVE_972_TO_162_CENSUS"
assert c["counts"] == {"canonical_groups": 162, "members_each": 6, "raw": 972, "y_groups": 81, "z_groups": 81}
assert r["authoritative_contraction"] == {
    "canonical_s3_charts": 162, "corrected_carrier": "A06^T*K*[A23^T|A35]", "forward_reverse_localization": True,
    "generators_each": 6577, "members_per_chart": 6, "raw_charts": 972, "variables_each": 91,
    "y_groups": 81, "y_raw": 486, "z_groups": 81, "z_raw": 486,
}
assert len(r["raw_s3_transport"]) == 162
raw_union = set()
perms = list(itertools.permutations(range(3)))
for census_group, transport in zip(c["groups"], r["raw_s3_transport"]):
    assert transport["group_id"] == census_group["group_id"]
    assert transport["canonical_chart"] == census_group["canonical_chart"]
    assert transport["family"] == census_group["family"]
    assert transport["exact_Q_source_sha256"] == census_group["exact_Q_source_sha256"]
    recorded = {tuple(member) for member in transport["raw_s3_members"]}
    assert recorded == {tuple(member) for member in census_group["raw_members"]} and len(recorded) == 6
    canonical = transport["canonical_chart"]
    regenerated = set()
    for perm in perms:
        image = [perm[canonical[index]] for index in range(4)] + [canonical[4], perm[canonical[5]]]
        image.extend(sorted((perm[canonical[6]], perm[canonical[7]])))
        regenerated.add(tuple(image))
    assert regenerated == recorded, f"raw S3 orbit mismatch at group {transport['group_id']}"
    assert raw_union.isdisjoint(recorded); raw_union |= recorded
assert len(raw_union) == 972
assert sum(group["family"] == "y" for group in r["raw_s3_transport"]) == 81
assert sum(group["family"] == "z" for group in r["raw_s3_transport"]) == 81
expected = [[0], list(range(1, 26)), list(range(26, 76)), list(range(76, 126)), list(range(126, 162))]
assert [entry["group_ids"] for entry in r["closure_shards"]] == expected
flat = [group for batch in expected for group in batch]
assert len(flat) == len(set(flat)) == 162 and sorted(flat) == list(range(162))
assert r["prospective_union_proof"] == {"group_count": 162, "union": list(range(162)), "duplicates": [], "missing": [], "extra": [], "all_four_future_batches_required": True}
ledger_specs = [
    ("computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25/source_ledger.json", "lanes", range(1, 26)),
    ("computations/unaudited-codex-n8-x5-rep2-groups26-75-exact-q-conditional-held-2026-08-26/source_ledger.json", "lanes", range(26, 76)),
    ("computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-v2-2026-08-26/source_reference_ledger.json", "sources", range(76, 126)),
    ("computations/unaudited-codex-n8-x5-rep2-groups126-161-exact-q-conditional-held-2026-08-26/source_ledger.json", "lanes", range(126, 162)),
]
for relative, key, group_ids in ledger_specs:
    entries = json.loads((ROOT / relative).read_text())[key]
    assert [entry["group_id"] for entry in entries] == list(group_ids)
    for entry in entries:
        group = c["groups"][entry["group_id"]]
        assert entry.get("source_sha256", entry.get("sha256")) == group["exact_Q_source_sha256"]
        assert entry["variables"] == 91 and entry["generators"] == 6577
        if "canonical_chart" in entry: assert entry["canonical_chart"] == group["canonical_chart"]
rank = r["rank_zero_structural_branch"]
assert rank["closed_rank_scope"] == [0] and rank["nonzero_rank_scope_not_claimed"] == [1, 2, 3]
carrier = json.loads((ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep2-exhaustive-carrier-closure-2026-08-25/results_rep2_exhaustive_carrier.json").read_text())
assert carrier["status"] == "PAIRING_ONLY_INCOMPLETE_REP2_NONZERO_RANKS"
assert carrier["proof"]["closed_rank_scope"] == [0] and carrier["proof"]["pairing_only_rank_scope"] == [1, 2, 3]
assert carrier["proof"]["zero_A57"] == rank["implications"]
first = json.loads((ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-run-2026-08-25/results_independent_referee.json").read_text())
second = json.loads((ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-second-referee-2026-08-25/results_referee.json").read_text())
assert first["status"] == "PASS_EXACT_Q_ONE_REFINED_CHART_ONLY" and first["unit_remainder"] == 0 and first["same_chart_closed"] is True
assert second["status"] == "PASS_EXACT_Q_ONE_REFINED_REP2_CHART_ONLY" and second["unit_ideal"] is True and second["unit_remainder"] == 0
assert first["source_sha256"] == second["source_sha256"] == c["groups"][0]["exact_Q_source_sha256"]
assert f["status"] == "UNSATISFIED_FOUR_NULL_HASH_PAIRS" and f["satisfied"] is False
assert [entry["group_ids"] for entry in f["dependencies"]] == expected[1:]
assert all(entry["manifest_sha256"] is entry["result_sha256"] is None for entry in f["dependencies"])
assert all(not (ROOT / entry[key]).exists() for entry in f["dependencies"] for key in ("manifest_path", "result_path"))
assert h["status"] == "PASS_EXACT_LEDGER_AND_13_HOSTILES" and h["hostile_count"] == 13 and all(h["hostile_tests"].values())
assert s["additionalProperties"] is False and set(s["required"]) == set(s["properties"])
assert s["properties"]["closed_group_ids"]["const"] == list(range(162))
assert s["properties"]["representative"]["const"] == "rep2"
assert r["scope"]["representative"] == "rep2 only" and r["scope"]["cross_representative_transport"] is False and r["scope"]["full_conjecture"] is False
assert r["scope"]["promotion_currently_authorized"] is False and r["scope"]["other_representatives_closed"] == [] and r["scope"]["solver_runs"] == 0
out = {
    "authoritative_census_sha256": CENSUS_SHA,
    "canonical_groups": 162, "raw_s3_members": 972, "raw_s3_orbits_rebuilt": 162,
    "current_exact_Q_closed_group_ids": [0], "future_exact_Q_required_group_ids": list(range(1, 162)),
    "future_hash_pairs": 4, "future_hashes_null": True, "future_paths_absent": True,
    "hostiles_replayed": 13, "manifest_replay": "PASS",
    "producer_manifest_sha256": PRODUCER_MANIFEST_SHA, "producer_result_sha256": PRODUCER_RESULT_SHA,
    "rank_zero_closed": True, "nonzero_rank_scope_not_promoted": [1, 2, 3],
    "schema": "KRENN_X5_REP2_ALL162_TERMINAL_PROMOTION_CONDITIONAL_REFEREE_V1",
    "scope": {"representative": "rep2 only", "cross_representative_transport": False, "full_conjecture": False, "solver_runs": 0, "mathematical_coverage": False},
    "status": "PASS_HELD_CONDITIONAL_DESIGN_ONLY_FOUR_FUTURE_PASS_SEALS_REQUIRED",
}
temporary = HERE / "results_referee.json.tmp"
temporary.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n"); os.replace(temporary, HERE / "results_referee.json")
print(json.dumps(out, sort_keys=True))
