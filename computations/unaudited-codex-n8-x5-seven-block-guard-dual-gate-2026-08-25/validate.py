#!/usr/bin/env python3
"""Fail-closed validator for the seven-block full-family obligation package."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results_full_family_obligation.json"
MODULAR = HERE / "results_guard_dual_p32003.json"
METADATA = HERE / "ideal_metadata.json"


def logical_sha(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def validate_record(record):
    assert record["schema"] == "KRENN_X5_SEVEN_BLOCK_FULL_FAMILY_INCIDENCE_OBLIGATION_V1"
    assert record["status"] == "PASS_EXACT_SIX_REPRESENTATIVE_REDUCTION_GENERAL_DICHOTOMY_OPEN"
    assert record["census"]["full_family_representatives"] == 6
    assert record["census"]["full_family_supports_with_guard_mates"] == 12
    assert record["census"]["two_sandwich_candidates_on_representatives"] == 56
    assert record["census"]["candidate_count_by_representative"] == {"8": 2, "10": 4}
    assert len(record["six_full_family_representatives"]) == 6
    assert [item["candidate_count"] for item in record["six_full_family_representatives"]] == [8, 10, 8, 10, 10, 10]
    for item in record["six_full_family_representatives"]:
        assert len(item["guard"]["exact_matrix_equations"]) == 3
        assert len(item["six_distinguished_residual_equations_target_zero"]) == 6
        assert len(item["full_x5_6561_equation_sha256"]) == 64
        for star in item["two_sandwich_stars"]:
            assert star["response_row_space"] == "P tensor Q"
            assert len(star["inactivity_clause"]) == 4
            assert len(star["supported_forbidden_terms"]) == 2
            assert star["supported_forbidden_terms"][0]["response_pair"] != star["supported_forbidden_terms"][1]["response_pair"]
    canonical = record["canonical_cap45_star2_lemma"]
    assert canonical["exact_map"] == "K -> A04*K*[A35^T|A56|A57]"
    assert canonical["forbidden_response_pairs"] == ["03", "06", "07"]
    assert record["remaining_exact_dichotomy"]["not_proved"] is True
    gate = record["bounded_groebner_diagnostic"]
    assert gate["status"] == "INCOMPLETE_WALL_GATE"
    assert gate["mathematical_coverage"] is False
    assert record["scope"]["full_seven_block_closure"] is False


def expect_reject(record, mutation):
    hostile = copy.deepcopy(record)
    mutation(hostile)
    try:
        validate_record(hostile)
    except (AssertionError, KeyError, TypeError):
        return
    raise AssertionError("hostile mutation was accepted")


def main():
    record = json.loads(RESULT.read_text())
    validate_record(record)
    modular = json.loads(MODULAR.read_text())
    metadata = json.loads(METADATA.read_text())
    assert modular["status"] == "INCOMPLETE_WALL_GATE"
    assert modular["unit_ideal"] is False
    assert modular["mathematical_coverage"] is False
    assert metadata["counts"] == {
        "adjoint_equations": 9,
        "dual_variables": 27,
        "equations": 6597,
        "full_x5_equations": 6561,
        "guard_equations": 27,
        "mixed_equations": 6558,
        "pure_equations": 3,
        "source_variables": 99,
        "variables": 126,
    }

    hostiles = [
        lambda x: x.__setitem__("status", "PASS_CLOSED"),
        lambda x: x["census"].__setitem__("two_sandwich_candidates_on_representatives", 55),
        lambda x: x["six_full_family_representatives"][0]["guard"]["exact_matrix_equations"].pop(),
        lambda x: x["six_full_family_representatives"][0]["two_sandwich_stars"][0]["inactivity_clause"].pop(),
        lambda x: x["six_full_family_representatives"][0]["six_distinguished_residual_equations_target_zero"].pop(),
        lambda x: x["canonical_cap45_star2_lemma"].__setitem__("exact_map", "wrong"),
        lambda x: x["bounded_groebner_diagnostic"].__setitem__("mathematical_coverage", True),
        lambda x: x["scope"].__setitem__("full_seven_block_closure", True),
    ]
    for mutation in hostiles:
        expect_reject(record, mutation)

    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_FULL_FAMILY_OBLIGATION_VALIDATION_V1",
        "status": "PASS",
        "result_logical_sha256": logical_sha(record),
        "hostile_tests": len(hostiles),
        "modular_timeout_fail_closed": True,
        "rational_certificate_claimed": False,
    }
    output = HERE / "results_validation.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
