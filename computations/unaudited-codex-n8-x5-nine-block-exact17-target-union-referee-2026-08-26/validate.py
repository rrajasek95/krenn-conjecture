#!/usr/bin/env python3
"""Replay the compact exact-17 target-union referee artifacts."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = "f280c2b3223a9673c80d2aa7bfed7f97c0558fbc2dcb80f4ecac88f16c4b9dd8"


def need(value, detail):
    if not value:
        raise RuntimeError(detail)


result = json.loads((HERE / "results_referee.json").read_text())
patch = json.loads((HERE / "selector_patch_metadata.json").read_text())
hostiles = json.loads((HERE / "hostile_tests.json").read_text())
ledger_bytes = (HERE / "exact17_target_supports.ledger").read_bytes()
lines = ledger_bytes.decode().splitlines()

need(result["status"] == "PASS_STATIC_EXACT17_TARGET_UNION_REFEREE__FUTURE_BASE_HELD", "status")
need(result["non_action"] == {
    "future_base_materialized_here": False,
    "large_cnf_read": False,
    "large_cnf_written": False,
    "solver_run": False,
}, "non-action")
need(result["sealed_census_replay"]["exact17_degree4_records"] == 534, "records")
need(result["sealed_census_replay"]["unlabelled_graph_classes"] == 50, "classes")
need(result["normalization"] == {
    "deduplicated_support_masks": 18180,
    "ledger_bytes": 927180,
    "ledger_sha256": EXPECTED,
    "raw_rooted_permuted_embeddings": 24048,
}, "normalization")
need(len(lines) == 18180 and len(set(lines)) == 18180 and lines == sorted(lines), "ledger order/dedup")
need(all(len(line.split("|")) == 17 for line in lines), "not exact17")
need(hashlib.sha256(ledger_bytes).hexdigest() == EXPECTED, "ledger hash")

need(result["exceptions_outside_scope"] == {
    "closed_here": False,
    "degree_sequence": [3, 3, 3, 3, 5, 5, 5, 5],
    "essential_edges": 16,
    "reason": "no degree-four vertex; outside exact17 degree-four target union",
    "records": [1114, 1978, 2014, 2036],
}, "exceptions")

need([row["variable"] for row in patch["block_variables"]] == list(range(226, 251)), "block variables")
need(patch["future_base"]["path"] is None and patch["future_base"]["sha256"] is None, "future base prematurely bound")
need(patch["future_base"]["variables"] is None and patch["future_base"]["clauses"] is None, "future header prematurely bound")
need(patch["selector_count"] == 18180 and patch["added_variables"] == 18180, "selectors")
need(patch["implication_clauses"] == 454500, "implications")
need(patch["global_selector_or"] == 1 and patch["added_clauses"] == 454501, "clauses")
need(patch["patched_header_formula"] == {
    "clauses": "base_clauses+454501",
    "variables": "base_variables+18180",
}, "header formula")

need(hostiles["status"] == "PASS_ALL_REJECTED", "hostiles")
need(hostiles["normalization_omissions"] == {
    "missing_center_rooting": 13158,
    "missing_neighbour_permutation": 15393,
    "missing_outside_permutation": 15420,
    "missing_singleton_rooting": 14004,
}, "normalization hostiles")
need("1114" in hostiles["scope_rejections"]["include_exact16_no_degree4_records"], "exception hostile")

print("PASS nine-block exact17 target-union static replay")
