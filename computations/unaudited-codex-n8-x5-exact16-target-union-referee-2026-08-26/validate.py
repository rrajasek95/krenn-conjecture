#!/usr/bin/env python3
"""Replay the small static exact-16 target-union referee artifacts."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIMIT = 2 * 1024 * 1024
EXPECTED = "3caf456fcd37b963f22d7e70b914817a5fd71032dbea873729d6dc0d3dd50aae"


def need(value, detail):
    if not value:
        raise RuntimeError(detail)


for path in HERE.iterdir():
    if path.is_file():
        need(path.stat().st_size <= LIMIT, ("over-2MiB artifact", path.name, path.stat().st_size))

result = json.loads((HERE / "results_referee.json").read_text())
patch = json.loads((HERE / "selector_patch_metadata.json").read_text())
hostiles = json.loads((HERE / "hostile_tests.json").read_text())
ledger = json.loads((HERE / "independent_target_ledger.json").read_text())
cross_bytes = (HERE / "target_supports.ledger").read_bytes()

need(result["status"] == "PASS_STATIC_EXACT16_TARGET_UNION_REFEREE", "bad status")
need(result["limits"] == {
    "base_cnf_read": False,
    "base_cnf_written": False,
    "max_file_read_bytes": LIMIT,
    "solver_run": False,
}, "non-static scope")
need(result["census"]["exact16_unlabelled_graph_classes"] == 16, "class count")
need(result["normalization"]["raw_rooted_permuted_embeddings"] == 8928, "raw count")
need(result["normalization"]["deduplicated_witnesses"] == 5508, "dedup count")
need(len(ledger["witnesses"]) == 5508, "ledger count")

lines = cross_bytes.decode().splitlines()
need(len(lines) == 5508 and len(set(lines)) == 5508 and lines == sorted(lines), "cross-ledger order/dedup")
need(all(len(line.split("|")) == 16 for line in lines), "not exact16")
need(hashlib.sha256(cross_bytes).hexdigest() == EXPECTED, "cross-ledger hash")
need(lines == ["|".join(w["support_edges"]) for w in ledger["witnesses"]], "ledger mismatch")

need([row["variable"] for row in patch["block_variables"]] == list(range(226, 251)), "block vars")
need(patch["selector_variables"] == {
    "count": 5508,
    "first": 428248,
    "last": 433755,
    "witness_order": "independent_target_ledger.json witnesses order",
}, "selector vars")
need(patch["clause_template"]["clauses_per_selector"] == 25, "per-selector arithmetic")
need(patch["added_implication_clauses"] == 137700, "implication count")
need(patch["added_global_or_clauses"] == 1, "global OR count")
need(patch["added_clauses"] == 137701, "added clause count")
need(patch["patched_header"] == {"variables": 433755, "clauses": 3220873}, "header")
need(hostiles["status"] == "PASS_ALL_REJECTED", "hostiles")
need(hostiles["rejected_old_added_clause_count"] == 143209, "old arithmetic hostile")

print("PASS static exact16 target-union referee replay")
