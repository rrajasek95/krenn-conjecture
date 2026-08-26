#!/usr/bin/env python3
"""Hostile tests for exact all-162 group/raw transport and future dependency coverage."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(result: dict, future: dict) -> None:
    assert result["schema"] == "KRENN_X5_REP1_ALL162_TERMINAL_PROMOTION_CONDITIONAL_DESIGN_V1"
    assert result["status"] == "HELD_PROMOTION_THREE_FUTURE_PASS_SEALS_ABSENT"
    contraction = result["authoritative_contraction"]
    assert contraction["raw_charts"] == 972 and contraction["canonical_s3_charts"] == 162 and contraction["members_per_chart"] == 6
    assert contraction["y_groups"] == contraction["z_groups"] == 81
    assert contraction["y_raw"] == contraction["z_raw"] == 486
    assert result["rank_zero_structural_branch"]["representative_id"] == 1
    assert result["rank_zero_structural_branch"]["scope"] == [0]
    assert "L67=0" in result["rank_zero_structural_branch"]["outside_zero_implication"]
    shards = result["closure_shards"]
    assert [shard["group_ids"] for shard in shards] == [list(range(38)), list(range(38, 88)), list(range(88, 138)), list(range(138, 162))]
    flat = [group for shard in shards for group in shard["group_ids"]]
    assert len(flat) == len(set(flat)) == 162 and sorted(flat) == list(range(162))
    proof = result["prospective_union_proof"]
    assert proof == {"group_count": 162, "union": list(range(162)), "duplicates": [], "missing": [], "extra": [], "all_future_required": True}
    transport = result["raw_s3_transport"]
    assert [entry["group_id"] for entry in transport] == list(range(162))
    assert all(entry["raw_member_count"] == len(entry["raw_s3_members"]) == 6 for entry in transport)
    raw = [tuple(member) for entry in transport for member in entry["raw_s3_members"]]
    assert len(raw) == len(set(raw)) == 972
    assert sum(entry["family"] == "y" for entry in transport) == 81
    assert sum(entry["family"] == "z" for entry in transport) == 81
    assert sum(member[4] == "y" for member in raw) == 486
    assert sum(member[4] == "z" for member in raw) == 486
    assert result["scope"]["representative"] == "rep1 only"
    assert result["scope"]["cross_representative_transport"] is False
    assert result["scope"]["other_representatives_closed"] == [] and result["scope"]["full_conjecture"] is False
    assert future["status"] == "UNSATISFIED_THREE_NULL_HASH_PAIRS" and future["satisfied"] is False
    assert [item["group_ids"] for item in future["dependencies"]] == [list(range(38, 88)), list(range(88, 138)), list(range(138, 162))]
    assert all(item["manifest_sha256"] is item["result_sha256"] is None for item in future["dependencies"])


result = json.loads((HERE / "results_terminal_promotion_design.json").read_text())
future = json.loads((HERE / "future_dependencies.json").read_text())
validate(result, future)
hostiles = {}


def rejected(name: str, mutate) -> None:
    r, f = copy.deepcopy(result), copy.deepcopy(future)
    mutate(r, f)
    try:
        validate(r, f)
    except (AssertionError, KeyError, TypeError):
        hostiles[name] = True
    else:
        hostiles[name] = False


rejected("missing_group", lambda r, f: r["closure_shards"][2]["group_ids"].pop())
rejected("duplicate_group", lambda r, f: r["closure_shards"][2]["group_ids"].append(137))
rejected("extra_group", lambda r, f: r["closure_shards"][3]["group_ids"].append(162))
rejected("missing_raw_member", lambda r, f: r["raw_s3_transport"][0]["raw_s3_members"].pop())
rejected("duplicate_raw_member", lambda r, f: r["raw_s3_transport"][1]["raw_s3_members"].__setitem__(0, r["raw_s3_transport"][0]["raw_s3_members"][0]))
rejected("drop_y_group", lambda r, f: r["raw_s3_transport"][0].__setitem__("family", "z"))
first_z = next(index for index, entry in enumerate(result["raw_s3_transport"]) if entry["family"] == "z")
rejected("drop_z_raw", lambda r, f: r["raw_s3_transport"][first_z]["raw_s3_members"][0].__setitem__(4, "y"))
rejected("rank_zero_scope_removed", lambda r, f: r["rank_zero_structural_branch"].__setitem__("scope", []))
rejected("cross_rep_transport", lambda r, f: r["scope"].__setitem__("cross_representative_transport", True))
rejected("other_rep_closed", lambda r, f: r["scope"].__setitem__("other_representatives_closed", [2]))
rejected("future_null_treated_satisfied", lambda r, f: f.__setitem__("satisfied", True))
rejected("future_hash_injected", lambda r, f: f["dependencies"][0].__setitem__("manifest_sha256", "0" * 64))
assert all(hostiles.values()) and len(hostiles) == 12
test_result = {"schema": "KRENN_X5_REP1_ALL162_PROMOTION_HOSTILE_TESTS_V1", "status": "PASS_EXACT_LEDGER_AND_12_HOSTILES", "design_sha256": sha256(HERE / "results_terminal_promotion_design.json"), "future_dependencies_sha256": sha256(HERE / "future_dependencies.json"), "hostile_tests": hostiles, "hostile_count": 12, "solver_runs": 0}
temporary = HERE / "results_hostile_tests.json.tmp"
temporary.write_text(json.dumps(test_result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_hostile_tests.json")
print(json.dumps({"status": test_result["status"], "hostiles": 12}, sort_keys=True))
