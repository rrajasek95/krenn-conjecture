#!/usr/bin/env python3
"""Fail-closed validation and hostiles for the exact 64-record coverage audit."""

from __future__ import annotations

import copy
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent


def validate(result):
    assert result["schema"] == "KRENN_X5_SEVEN_BLOCK_64_CARRIER_COVERAGE_V1"
    assert result["status"] == "PASS_MAPPING_48_PAIRING_ONLY_ZERO_CLOSURE"
    assert result["census"] == {"records": 64, "symmetry_orbits": 32, "pairing_only_records": 48, "pairing_only_orbits": 24, "mathematically_closed_records": 0, "unmapped_records": 16, "unmapped_orbits": 8}
    assert len(result["coverage"]) == 48 and len(result["uncovered"]) == 16
    assert sorted({item["orbit_id"] for item in result["coverage"]}) == list(range(8, 32))
    assert sorted({item["orbit_id"] for item in result["uncovered"]}) == list(range(8))
    assert sum(item["classification"] == "NO_GUARD_ANCHOR_06_OR_07" for item in result["uncovered"]) == 12
    assert sum(item["classification"] == "NO_OUTSIDE_R6_R7_RECTANGLE" for item in result["uncovered"]) == 4
    for item in result["coverage"]:
        assert item["identity_cap"] == "A03=I"
        assert len(item["carrier"]["terms"]) == 2
        assert item["carrier"]["common_block"] in ("06", "07")
    assert result["pairing_only_reduction"]["full_family_nonzero_A67_not_needed_for_pairing"] is True
    assert result["pairing_only_reduction"]["missing_diagonal_lemma"].startswith("For each record and i=0,1,2")
    assert result["no_go"]["all_64_closed"] is False
    assert result["eight_block_extension"] == {"attempted": False, "reason": "zero of 64 records are closed by the six pairing-only theorems; no monotone extension is claimed"}
    assert result["scope"] == {"complete_seven_block_theorem": False, "full_conjecture": False, "broad_computation": False}


def hostile(result, mutation):
    candidate = copy.deepcopy(result)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    result = json.loads((HERE / "results_64_carrier_coverage.json").read_text())
    validate(result)
    tests = {
        "coverage_overclaim": hostile(result, lambda x: x["census"].__setitem__("mathematically_closed_records", 48)),
        "drop_uncovered": hostile(result, lambda x: x["uncovered"].pop()),
        "wrong_orbit": hostile(result, lambda x: x["coverage"][0].__setitem__("orbit_id", 0)),
        "missing_carrier_term": hostile(result, lambda x: x["coverage"][0]["carrier"]["terms"].pop()),
        "wrong_identity_cap": hostile(result, lambda x: x["coverage"][0].__setitem__("identity_cap", "A04=I")),
        "all64_overclaim": hostile(result, lambda x: x["no_go"].__setitem__("all_64_closed", True)),
        "eight_block_overclaim": hostile(result, lambda x: x["eight_block_extension"].__setitem__("attempted", True)),
        "conjecture_overclaim": hostile(result, lambda x: x["scope"].__setitem__("full_conjecture", True)),
    }
    assert all(tests.values())
    output = {"schema": "KRENN_X5_64_CARRIER_COVERAGE_VALIDATION_V1", "status": "PASS", "hostile_tests": tests}
    temporary = HERE / "results_validation.json.tmp"
    temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    temporary.replace(HERE / "results_validation.json")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
