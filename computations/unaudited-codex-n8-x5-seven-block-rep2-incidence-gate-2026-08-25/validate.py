#!/usr/bin/env python3
"""Hostile fail-closed validation for the representative-2 audit."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent


def logical_sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate(record):
    assert record["schema"] == "KRENN_X5_SEVEN_BLOCK_REP2_AUDIT_V1"
    assert record["status"] == "PASS_DESIGN_AND_FAIL_CLOSED_REP2_REMAINS_UNRESOLVED"
    assert record["representative"]["id"] == 2
    assert record["representative"]["support_added"] == ["06", "14", "17", "23", "26", "56", "57"]
    assert record["representative"]["not_a_transport_of_rep0"] is True
    assert record["exact_progress"]["rank_one"].startswith("unresolved")
    assert record["exact_quotients"]["colour_swap_orbits"] == 10
    assert record["exact_quotients"]["smallest_pair01_chart"] == {
        "id": "rho0_sigma0", "variables": 80, "equations": 265,
    }
    assert record["failure_policy"]["all_failures_zero_coverage"] is True
    assert record["failure_policy"]["Q_not_promoted_from_modular"] is True
    assert record["failure_policy"]["no_rank2_run"] is True
    assert record["failure_policy"]["geometry_stopped_after_smallest_pair01_timeout"] is True
    assert record["scope"]["rep2_closed"] is False
    assert record["scope"]["all_six_full_family"] is False
    assert record["scope"]["all_64"] is False


def reject(record, mutation):
    hostile = copy.deepcopy(record)
    mutation(hostile)
    try:
        validate(hostile)
    except (AssertionError, KeyError, TypeError):
        return
    raise AssertionError("hostile mutation accepted")


def main():
    record = json.loads((HERE / "results_rep2_audit.json").read_text())
    validate(record)
    hostiles = [
        lambda x: x.__setitem__("status", "PASS_REP2_CLOSED"),
        lambda x: x["representative"].__setitem__("id", 0),
        lambda x: x["representative"].__setitem__("not_a_transport_of_rep0", False),
        lambda x: x["exact_progress"].__setitem__("rank_one", "closed"),
        lambda x: x["exact_quotients"].__setitem__("colour_swap_orbits", 9),
        lambda x: x["exact_quotients"]["smallest_pair01_chart"].__setitem__("variables", 79),
        lambda x: x["failure_policy"].__setitem__("all_failures_zero_coverage", False),
        lambda x: x["failure_policy"].__setitem__("Q_not_promoted_from_modular", False),
        lambda x: x["failure_policy"].__setitem__("no_rank2_run", False),
        lambda x: x["scope"].__setitem__("rep2_closed", True),
        lambda x: x["scope"].__setitem__("all_six_full_family", True),
        lambda x: x["scope"].__setitem__("all_64", True),
    ]
    for mutation in hostiles:
        reject(record, mutation)
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_REP2_VALIDATION_V1",
        "status": "PASS",
        "audit_logical_sha256": logical_sha(record),
        "hostile_tests": len(hostiles),
        "overclaim_rejected": True,
    }
    output = HERE / "results_validation.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
