#!/usr/bin/env python3
"""Replay the compact combined target-union referee seal."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = "6bffb2962242725f8bd0603dfaeb91f64c2ee0e4430632b445b42e44d4a424d5"


def need(value, detail):
    if not value:
        raise RuntimeError(detail)


result = json.loads((HERE / "results_referee.json").read_text())
patch = json.loads((HERE / "selector_patch_metadata.json").read_text())
hostiles = json.loads((HERE / "hostile_tests.json").read_text())
ledger_bytes = (HERE / "combined_target_supports.ledger").read_bytes()
lines = ledger_bytes.decode().splitlines()

need(result["status"] == "PASS_STATIC_COMBINED_TARGET_UNION_REFEREE", "status")
need(result["non_action"] == {
    "large_base_cnf_read": False,
    "large_base_cnf_written": False,
    "materialized_nine_result_read": False,
    "solver_run": False,
}, "non-action scope")
need(result["eight_layer"]["graph_classes"] == 16, "eight classes")
need(result["eight_layer"]["raw_embeddings"] == 8928, "eight raw")
need(result["eight_layer"]["support_masks"] == 5508, "eight masks")
need(result["nine_layer"]["exact16_degree4_records"] == 1104, "nine records")
need(result["nine_layer"]["graph_classes"] == 85, "nine classes")
need(result["nine_layer"]["raw_embeddings"] == 43344, "nine raw")
need(result["nine_layer"]["support_masks"] == 33876, "nine masks")
need(result["combined"] == {
    "graph_class_intersection": 9,
    "graph_class_union": 92,
    "ledger_bytes": 1722816,
    "ledger_sha256": EXPECTED,
    "raw_embeddings_over_unique_classes": 47088,
    "support_intersection": 3492,
    "support_union": 35892,
}, "combined census")
need(len(lines) == 35892 and len(set(lines)) == 35892 and lines == sorted(lines), "ledger order/dedup")
need(all(len(line.split("|")) == 16 for line in lines), "not exact16")
need(hashlib.sha256(ledger_bytes).hexdigest() == EXPECTED, "ledger hash")

need([row["variable"] for row in patch["block_variables"]] == list(range(226, 251)), "block variables")
need(patch["selector_variables"] == {"first": 428248, "last": 464139, "count": 35892}, "selectors")
need(patch["clauses_per_selector"] == 25, "selector arity")
need(patch["selector_implications"] == 897300, "implications")
need(patch["global_selector_or"] == 1, "global OR")
need(patch["added_clauses"] == 897301, "clause delta")
need(patch["patched_header"] == {"variables": 464139, "clauses": 3980473}, "header")
need("never append to the narrow" in patch["composition_contract"], "composition contract")

narrow = result["narrow_materialization_comparison"]
need(narrow["narrow_ledger_is_subset"] is True and narrow["semantic_conflict"] is False, "narrow semantics")
need(narrow["bytewise_or_additive_composability"] is False, "must refuse additive composition")
need(narrow["cnf_sha256_from_small_metadata_not_rehashed"] == "dc5cd1cad3a062dc66a5788413e5c1e1799a1ed07e66266ad25cc195b470aafa", "narrow pin")

need(hostiles["status"] == "PASS_ALL_REJECTED", "hostiles")
need(hostiles["cross_layer"]["required_graph_class_overlap"] == 9, "class overlap hostile")
need(hostiles["cross_layer"]["required_cross_layer_support_overlap"] == 3492, "support overlap hostile")
need(hostiles["cross_layer"]["naive_sum_without_cross_dedup"] == 39384, "naive sum hostile")
need(hostiles["normalization_omissions"] == {
    "missing_center_rooting": 26460,
    "missing_neighbour_permutation": 30327,
    "missing_outside_permutation": 30342,
    "missing_singleton_rooting": 27612,
}, "normalization hostiles")
need("alias" in hostiles["selector"]["append_to_narrow_materialization"], "composition hostile")

print("PASS combined eight+nine exact16 target-union static replay")
