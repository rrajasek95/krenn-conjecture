#!/usr/bin/env python3
"""Fail-closed validator for the exact rectangle transport census."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


result = json.loads((HERE / "results_transport_census.json").read_text())
ledger = json.loads((HERE / "transport_ledger.json").read_text())

assert result["schema"] == "KRENN_X5_RECTANGLE12_TRANSPORT_CENSUS_V1"
assert result["status"] == "PASS_ALL_12_TRANSPORTED_TWO_SOURCE_CLASSES"
assert result["transport_ledger"] == {
    "path": "transport_ledger.json",
    "sha256": sha256(HERE / "transport_ledger.json"),
}
assert result["source_classes"] == [
    {"class": "A12_present", "representative_record": 0, "members": [0, 1, 4, 5, 8, 9]},
    {"class": "A12_absent", "representative_record": 2, "members": [2, 3, 6, 7, 10, 11]},
]
assert result["census"] == {
    "records": 12,
    "source_support_classes": 2,
    "records_per_class": 6,
    "rank3_exact_Q_closed_records": 12,
    "rank1_exact_design_records": 12,
    "rank2_exact_design_records": 12,
    "solver_runs": 0,
}
assert result["scope"] == {
    "rank3_transport_closed": True,
    "rank1_rank2_transport_design_only": True,
    "remaining_no_anchor_rectangle_records": 0,
    "other_unmapped_records": 4,
    "full_conjecture": False,
}
assert result["word_generator_transport_checks"] == 12 * 6 * 6561
assert len(ledger["records"]) == 12
assert [x["record_index"] for x in ledger["records"]] == list(range(12))

expected_outside = {
    0: "47", 1: "46", 2: "47", 3: "46",
    4: "37", 5: "36", 6: "37", 7: "36",
    8: "56", 9: "57", 10: "56", 11: "57",
}
for entry in ledger["records"]:
    index = entry["record_index"]
    assert entry["site_maps_from_reference"] == 1
    assert entry["colour_maps_per_site_map"] == 6
    assert entry["word_generators_checked"] == 6 * 6561
    assert entry["mapped_outside_factor"] == expected_outside[index]
    assert entry["rank3"]["status"] == "CLOSED_BY_EXACT_Q_TRANSPORT"
    assert entry["rank1"]["status"] == "EXACT_DESIGN_TRANSPORTED_NOT_SOLVED"
    assert entry["rank2"]["status"] == "EXACT_DESIGN_TRANSPORTED_NOT_SOLVED"

matrix = ledger["source_support_isomorphism_counts"]
on = {0, 1, 4, 5, 8, 9}
off = {2, 3, 6, 7, 10, 11}
for source in range(12):
    for target in range(12):
        expected = int((source in on and target in on) or (source in off and target in off))
        assert matrix[str(source)][str(target)] == expected

assert all(result["hostile_tests"].values())
print(json.dumps({"status": "PASS", "records": 12, "solver_runs": 0}, sort_keys=True))
