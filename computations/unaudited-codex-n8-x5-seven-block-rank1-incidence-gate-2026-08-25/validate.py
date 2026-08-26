#!/usr/bin/env python3
"""Fail-closed validator for the exact rank<=1 branch."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
AUDIT = HERE / "results_rank1_branch_audit.json"
METADATA = HERE / "rank1_ideal_metadata.json"
P_RESULT = HERE / "results_rank1_incidence_p32003.json"
Q_RESULT = HERE / "results_rank1_incidence_Q.json"


def logical_sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate_record(record):
    assert record["schema"] == "KRENN_X5_SEVEN_BLOCK_RANK1_BRANCH_AUDIT_V1"
    assert record["status"] == "PASS_EXACT_CANONICAL_RANK_LE1_TRIANGLE_OR_STAR_BRANCH"
    assert record["reduction"]["A56"] == "-u*(A26*v)^T"
    assert record["reduction"]["guard"] == ["A06*v=0", "(I-A17*A26)*v=0"]
    assert record["reduction"]["response_dual_dimension"] == 9
    assert record["reduction"]["source_variables_plus_witnesses"] == 103
    assert record["reduction"]["equations"] == 6582
    assert record["exact_rational_unit"]["groebner_size"] == 1
    assert record["exact_rational_unit"]["unit_remainder"] == 0
    assert record["literal_response_adjoint_replay"]["samples"] == 257
    assert record["next_branch"]["rank"] == 2
    assert record["scope"]["rank_le_one"] is True
    assert record["scope"]["rank_two"] is False
    assert record["scope"]["all_64_loci"] is False


def expect_reject(record, mutation):
    hostile = copy.deepcopy(record)
    mutation(hostile)
    try:
        validate_record(hostile)
    except (AssertionError, KeyError, TypeError):
        return
    raise AssertionError("hostile mutation was accepted")


def main():
    audit = json.loads(AUDIT.read_text())
    metadata = json.loads(METADATA.read_text())
    p_result = json.loads(P_RESULT.read_text())
    q_result = json.loads(Q_RESULT.read_text())
    validate_record(audit)
    assert metadata["substitutions"]["A56"] == "-u*(A26*v)^T"
    assert metadata["counts"]["variables"] == 103
    assert metadata["counts"]["equations"] == 6582
    assert p_result["status"] == "PASS_MODULAR_UNIT_DIAGNOSTIC"
    assert p_result["mathematical_coverage"] is False
    assert q_result["status"] == "PASS_RATIONAL_UNIT_IDEAL"
    assert q_result["mathematical_coverage"] is True
    assert q_result["stdout"] == "INPUT_GENERATORS=6582\nGROEBNER_SIZE=1\nUNIT_REMAINDER=0\nSTATUS=UNIT_IDEAL\n"

    hostiles = [
        lambda x: x.__setitem__("status", "PASS_ALL_64"),
        lambda x: x["reduction"].__setitem__("A56", "-A26*u*v^T"),
        lambda x: x["reduction"].__setitem__("response_dual_dimension", 27),
        lambda x: x["reduction"].__setitem__("equations", 6581),
        lambda x: x["exact_rational_unit"].__setitem__("unit_remainder", 1),
        lambda x: x["literal_response_adjoint_replay"].__setitem__("samples", 256),
        lambda x: x["scope"].__setitem__("rank_two", True),
        lambda x: x["scope"].__setitem__("all_64_loci", True),
    ]
    for mutation in hostiles:
        expect_reject(audit, mutation)

    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_RANK1_BRANCH_VALIDATION_V1",
        "status": "PASS",
        "audit_logical_sha256": logical_sha(audit),
        "hostile_tests": len(hostiles),
        "rational_unit_pinned": True,
        "modular_control_pinned": True,
        "std_timeout_not_promoted": True,
    }
    output = HERE / "results_validation.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
