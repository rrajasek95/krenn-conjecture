#!/usr/bin/env python3
"""Fail-closed validator for the anchor/no-rectangle design package."""
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


result = json.loads((HERE / "results_anchor_no_rectangle_design.json").read_text())
ledger = json.loads((HERE / "all_carriers_ledger.json").read_text())
source = (HERE / "canonical_reduced_full_x5_Q.sing").read_text()

assert result["schema"] == "KRENN_X5_ANCHOR_NO_RECTANGLE_DESIGN_V1"
assert result["status"] == "PASS_EXACT_ONE_REDUCED_REPRESENTATIVE_RANK_DESIGN_NO_SOLVE"
assert result["census"] == {
    "records": 4,
    "literal_source_classes": 2,
    "reduced_full_x5_classes": 1,
    "carriers_per_record": 728,
    "word_transport_checks": 157464,
    "solver_runs": 0,
}
assert result["source_symmetry"]["literal_classes"] == [
    {"representative": 12, "members": [12, 13]},
    {"representative": 14, "members": [14, 15]},
]
assert result["source_symmetry"]["unique_mirror"] == [0, 2, 1, 3, 4, 5, 7, 6]
assert result["factorization"]["verified_words"] == 6561
assert result["factorization"]["transported_word_checks"] == 157464

ideal = result["full_x5_ideal"]
assert ideal["path"] == "canonical_reduced_full_x5_Q.sing"
assert ideal["sha256"] == sha256(HERE / ideal["path"])
assert ideal["variables"] == 81 and ideal["generators"] == 6561
assert ideal["solver_commands"] == 0
lower = source.lower()
assert "slimgb" not in lower and "std(" not in lower and "groebner" not in lower
assert source.count("print(") == 2 and source.rstrip().endswith("quit;")

assert result["all_carriers_ledger"] == {
    "path": "all_carriers_ledger.json",
    "sha256": sha256(HERE / "all_carriers_ledger.json"),
}
assert set(ledger["records"]) == {"12", "13", "14", "15"}
assert all(len(ledger["records"][key]) == 728 for key in ledger["records"])
assert all(sum(item["kind"] == "triangle" for item in ledger["records"][key]) == 560 for key in ledger["records"])
assert all(sum(item["kind"] == "star" for item in ledger["records"][key]) == 168 for key in ledger["records"])

rank = result["selected_rank_design"]
assert rank["rank0"]["status"] == "CLOSED_BY_ZERO_RESPONSE_MAP"
assert rank["rank1"]["status"] == "EXACT_INCIDENCE_DESIGN_NOT_SOLVED"
assert (rank["rank1"]["variables"], rank["rank1"]["generators"], rank["rank1"]["raw_charts"], rank["rank1"]["S3_orbits"]) == (85, 6568, 27, 5)
assert rank["rank2"]["status"] == "EXACT_INCIDENCE_DESIGN_NOT_SOLVED"
assert (rank["rank2"]["variables"], rank["rank2"]["generators"], rank["rank2"]["raw_charts"], rank["rank2"]["S3_orbits"]) == (89, 6568, 27, 5)
assert rank["rank3"]["status"] == "EXACT_SMALLER_IDEAL_NOT_SOLVED"
assert (rank["rank3"]["variables"], rank["rank3"]["generators"]) == (82, 6562)
assert result["scope"] == {"mathematically_closed_full_records": 0, "solver_runs": 0, "full_conjecture": False}
assert all(result["hostile_tests"].values())

print(json.dumps({"status": "PASS", "records": 4, "reduced_representatives": 1, "solver_runs": 0}, sort_keys=True))
