#!/usr/bin/env python3
"""Fail-closed small-result validator for the seven-block rank referee."""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "run_referee.py"
RESULT = HERE / "results_seven_block_rank_activity_referee.json"
SOURCE_SHA256 = "6f06f348322754390449a54daf31b851f48f5ca8df1170b77c4b3f527a732790"
RESULT_SHA256 = "f5f74a17c6dccfc03ae266e7edbcb966ed200a0a14762cc671c23943765b1df7"
EXPECTED_STATUS = "PASS_EXACT_RANK_REDUCTION_AND_MATRIX_UNIT_SUBCLASS_CLOSED_GENERAL_LEMMA_OPEN"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(data):
    assert data["status"] == EXPECTED_STATUS
    assert data["scope"] == {
        "D12_read": False,
        "broad_solve": False,
        "exact_integer_rational_algebra": True,
        "full_conjecture_claim": False,
        "independent_negative_control_replay": True,
        "representatives": 6,
        "symbolic_response_maps": True,
    }
    records = data["six_representatives"]
    assert len(records) == 6
    assert [record["matrix_unit_alternative_word_occurrence_bound"] for record in records] == [56, 53, 52, 43, 47, 41]
    assert all(record["cap67_nonzero_symbolic_rows"] == 27 for record in records)
    assert all(record["symbolic_triangle_and_star_maps"] == 390 for record in records)
    assert all(record["matrix_unit_full_X5_impossible"] is True for record in records)
    reduction = data["determinantal_reduction"]
    assert reduction["formal_guard_identity"] == "L_67 vec(I3)=0"
    assert reduction["rank_consequence"] == "rank(L_67)<=8"
    assert data["canonical_formal_guard_reduction"]["R05"] == "A06*A57^T=0"
    factor = data["canonical_cap45_star2_factorization"]
    assert factor["forbidden_pairs_with_nonzero_symbolic_response"] == ["03", "06", "07"]
    replay = data["negative_control_replay"]
    assert replay["active_triangles"] == 0
    assert replay["active_stars"] == [{"cap": "16", "center": 2}, {"cap": "45", "center": 2}]
    assert replay["six_residuals"] == [1, 1, 1, 1, 1, 2]
    assert replay["nonzero_mixed_amplitudes"] == 114 and replay["full_X5"] is False
    reduction64 = data["all_64_factorized_star_reduction"]
    assert reduction64["unresolved_strata"] == 64
    assert reduction64["sealed_reduction_result_exactly_matched"] is True
    assert len(reduction64["choice_census"]) == 13
    assert sum(record["count"] for record in reduction64["choice_census"]) == 64
    assert data["general_dense_stratum"]["verdict"] == "OPEN"


def hostile_reject(mutator):
    data = json.loads(RESULT.read_text())
    mutator(data)
    try:
        validate(data)
    except AssertionError:
        return True
    return False


def main():
    assert sha256(SOURCE) == SOURCE_SHA256
    assert sha256(RESULT) == RESULT_SHA256
    data = json.loads(RESULT.read_text())
    validate(data)
    hostiles = {
        "false_general_promotion": hostile_reject(lambda d: d["general_dense_stratum"].update(verdict="PROVED")),
        "missing_representative": hostile_reject(lambda d: d["six_representatives"].pop()),
        "invalid_occurrence_bound": hostile_reject(lambda d: d["six_representatives"][0].update(matrix_unit_alternative_word_occurrence_bound=78)),
        "triangle_only_witness_misread": hostile_reject(lambda d: d["negative_control_replay"].update(active_stars=[])),
        "guard_equation_omission": hostile_reject(lambda d: d["canonical_formal_guard_reduction"].update(R05="OMITTED")),
    }
    assert all(hostiles.values())
    output = {
        "schema": "KRENN_X5_SEVEN_BLOCK_RANK_ACTIVITY_VALIDATION_V1",
        "status": "PASS_FAIL_CLOSED_RESULT_AND_HOSTILE_VALIDATION",
        "source_sha256": SOURCE_SHA256,
        "result_sha256": RESULT_SHA256,
        "hostile_tests": hostiles,
    }
    temporary = HERE / "results_validation.json.tmp"
    temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_validation.json")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
