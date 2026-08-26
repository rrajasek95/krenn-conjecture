#!/usr/bin/env python3
"""Fail-closed validation of the held rep1 all-162 promotion contract."""
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text())


design = load("results_terminal_promotion_design.json")
future = load("future_dependencies.json")
hostiles = load("results_hostile_tests.json")
schema = load("terminal_promotion_acceptance.schema.json")

assert design["status"] == "HELD_PROMOTION_THREE_FUTURE_PASS_SEALS_ABSENT"
assert design["scope"] == {
    "representative": "rep1 only",
    "full_family": "all 972 localized raw charts of rep1 across both y/z partner-pivot families",
    "transport": "only common simultaneous S3 color renaming within each source-labelled rep1 chart",
    "cross_representative_transport": False,
    "other_representatives_closed": [],
    "full_conjecture": False,
    "promotion_currently_authorized": False,
    "solver_runs": 0,
}
assert design["rank_zero_structural_branch"]["scope"] == [0]
assert "L67=0" in design["rank_zero_structural_branch"]["outside_zero_implication"]
assert "retracted/nonzero pairing-only claims are not used" in design["rank_zero_structural_branch"]["source_pin_scope"]

shards = design["closure_shards"]
expected_shards = [list(range(38)), list(range(38, 88)), list(range(88, 138)), list(range(138, 162))]
assert [entry["group_ids"] for entry in shards] == expected_shards
flat = [value for part in expected_shards for value in part]
assert len(flat) == len(set(flat)) == 162 and sorted(flat) == list(range(162))
assert design["prospective_union_proof"] == {
    "group_count": 162,
    "union": list(range(162)),
    "duplicates": [],
    "missing": [],
    "extra": [],
    "all_future_required": True,
}

transport = design["raw_s3_transport"]
assert [entry["group_id"] for entry in transport] == list(range(162))
raw = [tuple(member) for entry in transport for member in entry["raw_s3_members"]]
assert all(entry["raw_member_count"] == len(entry["raw_s3_members"]) == 6 for entry in transport)
assert len(raw) == len(set(raw)) == 972
assert sum(entry["family"] == "y" for entry in transport) == 81
assert sum(entry["family"] == "z" for entry in transport) == 81
assert sum(member[4] == "y" for member in raw) == 486
assert sum(member[4] == "z" for member in raw) == 486

assert future["status"] == "UNSATISFIED_THREE_NULL_HASH_PAIRS" and future["satisfied"] is False
assert [entry["group_ids"] for entry in future["dependencies"]] == expected_shards[1:]
assert all(entry["manifest_sha256"] is entry["result_sha256"] is None for entry in future["dependencies"])
for entry in future["dependencies"]:
    assert not (ROOT / entry["manifest_path"]).exists()
    assert not (ROOT / entry["result_path"]).exists()

assert hostiles["status"] == "PASS_EXACT_LEDGER_AND_12_HOSTILES"
assert hostiles["hostile_count"] == len(hostiles["hostile_tests"]) == 12
assert all(hostiles["hostile_tests"].values())
assert hostiles["design_sha256"] == sha256(HERE / "results_terminal_promotion_design.json")
assert hostiles["future_dependencies_sha256"] == sha256(HERE / "future_dependencies.json")

assert schema["additionalProperties"] is False
assert set(schema["required"]) == set(schema["properties"])
props = schema["properties"]
assert props["closed_group_ids"]["const"] == list(range(162))
assert props["promotion_design_sha256"]["const"] == sha256(HERE / "results_terminal_promotion_design.json")
assert props["future_dependencies_sha256"]["const"] == sha256(HERE / "future_dependencies.json")


def accepts(instance: dict) -> bool:
    if set(instance) != set(schema["required"]):
        return False
    for key, rule in props.items():
        value = instance[key]
        if "const" in rule and value != rule["const"]:
            return False
        if rule.get("type") == "string" and not isinstance(value, str):
            return False
        if "pattern" in rule and (not isinstance(value, str) or re.fullmatch(rule["pattern"], value) is None):
            return False
    return True


good = {
    "schema": "KRENN_X5_REP1_ALL162_TERMINAL_PROMOTION_ACCEPTANCE_V1",
    "status": "PASS_PROMOTE_REP1_ALL_162_CANONICAL_GROUPS_ONLY",
    "held_design_manifest_sha256": "a" * 64,
    "promotion_design_sha256": sha256(HERE / "results_terminal_promotion_design.json"),
    "future_dependencies_sha256": sha256(HERE / "future_dependencies.json"),
    "groups38_87_manifest_sha256": "b" * 64,
    "groups38_87_result_sha256": "c" * 64,
    "groups88_137_manifest_sha256": "d" * 64,
    "groups88_137_result_sha256": "e" * 64,
    "groups138_161_manifest_sha256": "f" * 64,
    "groups138_161_result_sha256": "0" * 64,
    "closed_group_ids": list(range(162)),
    "raw_charts_closed": 972,
    "canonical_groups_closed": 162,
    "y_groups_closed": 81,
    "z_groups_closed": 81,
    "representative": "rep1",
    "cross_representative_transport": False,
    "full_conjecture": False,
}
assert accepts(good)
schema_hostiles = {}
for name, mutate in {
    "null_future_hash": lambda x: x.__setitem__("groups38_87_manifest_sha256", None),
    "malformed_future_hash": lambda x: x.__setitem__("groups88_137_result_sha256", "a" * 63),
    "missing_group": lambda x: x["closed_group_ids"].pop(),
    "cross_rep_true": lambda x: x.__setitem__("cross_representative_transport", True),
    "full_conjecture_true": lambda x: x.__setitem__("full_conjecture", True),
    "extra_property": lambda x: x.__setitem__("other_rep", 2),
}.items():
    candidate = copy.deepcopy(good)
    mutate(candidate)
    schema_hostiles[name] = not accepts(candidate)
assert all(schema_hostiles.values())

for forbidden in [
    "terminal_promotion_acceptance.json",
    "results_terminal_promotion.json",
    "future_terminal_seals.json",
]:
    assert not (HERE / forbidden).exists()
assert not list(HERE.glob("*.tmp"))
assert not list(HERE.glob("*.singular"))

for relative, expected in design["pins"].items():
    target = ROOT / relative
    assert target.is_file() and sha256(target) == expected, relative

manifest = HERE / "MANIFEST.sha256"
manifest_lines = 0
if manifest.exists():
    for line in manifest.read_text().splitlines():
        digest, relative = line.split("  ", 1)
        target = (HERE / relative).resolve()
        assert target.is_file() and sha256(target) == digest, relative
        manifest_lines += 1

result = {
    "schema": "KRENN_X5_REP1_ALL162_TERMINAL_PROMOTION_DESIGN_VALIDATION_V1",
    "status": "PASS_HELD_ZERO_RUN_THREE_FUTURE_SEALS_REQUIRED",
    "canonical_groups": 162,
    "raw_s3_members": 972,
    "y_z_groups": [81, 81],
    "current_exact_q_closed": list(range(38)),
    "future_exact_q_required": list(range(38, 162)),
    "schema_hostiles": schema_hostiles,
    "solver_runs": 0,
    "manifest_lines_checked": manifest_lines,
}
print(json.dumps(result, sort_keys=True))
