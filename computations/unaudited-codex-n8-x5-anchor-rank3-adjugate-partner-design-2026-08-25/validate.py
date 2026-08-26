#!/usr/bin/env python3
"""Fail-closed validator for the anchor rank3 partner design."""
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


result = json.loads((HERE / "results_anchor_rank3_adjugate_partner_design.json").read_text())
assert result["schema"] == "KRENN_X5_ANCHOR_RANK3_ADJUGATE_PARTNER_DESIGN_V1"
assert result["status"] == "PASS_EXACT_PARTNER_RANK_STRATIFICATION_ONE_SMALLER_INPUT_NO_SOLVE"
assert result["adjugate_cancellation"]["matrix_entries_replayed"] == 18
assert result["starting_branch"]["ideal"] == {"variables": 82, "generators": 6562}

branches = result["branches"]
assert branches["partner_rank0"]["status"] == "CLOSED_SELECTED_CARRIER_ACTIVE"
assert branches["partner_rank1"]["counts"] == {
    "variables": 71, "generators": 2920, "raw_charts": 18, "S3_orbits": 4,
}
assert branches["partner_rank1"]["deduplication"] == {
    "raw_full_x5_words": 6561,
    "tautological_zero_words": 2916,
    "distinct_nonzero_full_x5_generators": 2918,
    "saturations": 2,
}
assert branches["partner_rank2"]["counts"] == {
    "variables": 78, "generators": 6563, "raw_charts": 90, "S3_orbits": 15,
}
assert branches["partner_rank3"]["counts"] == {
    "variables": 83, "generators": 6563, "raw_charts": 20, "S3_orbits": 6,
}

source_meta = result["canonical_input"]
source = HERE / source_meta["path"]
assert source_meta["sha256"] == sha256(source)
assert (source_meta["variables"], source_meta["generators"]) == (71, 2920)
text = source.read_text().lower()
assert "ring r=0," in text
assert "slimgb" not in text and "std(" not in text and "groebner" not in text
assert text.count("print(") == 2 and text.rstrip().endswith("quit;")

assert result["scope"] == {
    "inputs_materialized": 1,
    "solver_runs": 0,
    "full_rankA07_branch_closed": False,
    "full_conjecture": False,
}
assert all(result["hostile_tests"].values())
print(json.dumps({"status": "PASS", "variables": 71, "generators": 2920, "solver_runs": 0}, sort_keys=True))
