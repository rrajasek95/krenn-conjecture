#!/usr/bin/env python3
"""Fail-closed validator for the exact rank-two/canonical all-ranks result."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
AUDIT = HERE / "results_rank2_branch_audit.json"


def logical_sha(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def validate_record(record):
    assert record["schema"] == "KRENN_X5_SEVEN_BLOCK_RANK2_BRANCH_AUDIT_V1"
    assert record["status"] == "PASS_EXACT_CANONICAL_ALL_RANKS_TRIANGLE_OR_STAR_BRANCH"
    assert record["rank_two_reduction"]["A56"] == "-U*(A26*V)^T"
    assert record["rank_two_reduction"]["guard"] == ["A06*V=0", "(I-A17*A26)*V=0"]
    assert record["rank_two_reduction"]["response_dual_dimension"] == 18
    assert record["rank_two_reduction"]["variables_per_chart"] == 120
    assert record["rank_two_reduction"]["equations_per_chart"] == 6589
    assert record["chart_coverage"]["ordered_failed_colour_and_minor_pairs"] == 27
    assert record["chart_coverage"]["rational_unit_charts"] == 5
    assert record["chart_coverage"]["modular_control_charts"] == 5
    assert record["literal_response_adjoint_replay"]["samples"] == 257
    assert record["literal_response_adjoint_replay"]["exact_integer"] is True
    assert record["transport_test"]["canonical_to_representative_transport_counts"] == [1, 0, 0, 0, 0, 0]
    assert record["transport_test"]["other_five_direct_transports"] == 0
    assert record["scope"]["canonical_representative_all_ranks"] is True
    assert record["scope"]["other_five_full_family_representatives"] is False
    assert record["scope"]["all_64_loci"] is False
    for chart in record["chart_coverage"]["charts"]:
        assert record["runs"][chart]["Q"]["mathematical_coverage"] is True
        assert record["runs"][chart]["p32003"]["mathematical_coverage"] is False


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
    validate_record(audit)
    hostiles = [
        lambda x: x.__setitem__("status", "PASS_ALL_64"),
        lambda x: x["rank_two_reduction"].__setitem__("A56", "-(A26*U)*V^T"),
        lambda x: x["rank_two_reduction"].__setitem__("response_dual_dimension", 27),
        lambda x: x["rank_two_reduction"].__setitem__("equations_per_chart", 6588),
        lambda x: x["chart_coverage"].__setitem__("ordered_failed_colour_and_minor_pairs", 26),
        lambda x: x["chart_coverage"].__setitem__("rational_unit_charts", 4),
        lambda x: x["literal_response_adjoint_replay"].__setitem__("samples", 256),
        lambda x: x["transport_test"].__setitem__("canonical_to_representative_transport_counts", [1, 1, 0, 0, 0, 0]),
        lambda x: x["scope"].__setitem__("other_five_full_family_representatives", True),
        lambda x: x["scope"].__setitem__("all_64_loci", True),
        lambda x: x["runs"]["all_equal"]["Q"].__setitem__("mathematical_coverage", False),
        lambda x: x["runs"]["all_distinct"]["p32003"].__setitem__("mathematical_coverage", True),
    ]
    for mutation in hostiles:
        expect_reject(audit, mutation)
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_RANK2_BRANCH_VALIDATION_V1",
        "status": "PASS",
        "audit_logical_sha256": logical_sha(audit),
        "hostile_tests": len(hostiles),
        "rational_units_pinned": 5,
        "modular_controls_pinned": 5,
        "transport_overclaim_rejected": True,
    }
    output = HERE / "results_validation.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
