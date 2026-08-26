#!/usr/bin/env python3
"""Fail-closed validation and hostile tests for the rep3 carrier theorem."""

from __future__ import annotations

import copy
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent


def validate(record):
    assert record["schema"] == "KRENN_X5_SEVEN_BLOCK_REP3_LOW_RANK_CARRIER_V1"
    assert record["status"] == "PAIRING_ONLY_INCOMPLETE_NONZERO_RANKS"
    assert record["representative_id"] == 3
    assert record["selection"]["selected"] == 3
    assert record["selection"]["supported_perfect_matchings"] == {"1": 12, "3": 12, "4": 12, "5": 12}
    assert record["selection"]["minimum_star_terms"] == {"1": 2, "3": 2, "4": 2, "5": 2}
    assert record["selection"]["full_x5_total_term_tiebreak"] == {"1": 38718, "3": 37260, "4": 40176, "5": 41634}
    assert record["exact_guard"] == ["A06*A37^T=0", "A37^T+A17*A36^T=0", "A26*A37^T+A36^T=0"]
    assert record["carrier"]["factorization_up_to_output_permutation"] == "A06^T*K*[A35|A37]"
    assert record["carrier"]["cap"] == "03" and record["carrier"]["star_center"] == 4
    assert record["proof"]["all_nonzero_ranks_pairing_scope"].startswith("The same argument")
    assert record["proof"]["missing_diagonal_lemma"].startswith("For every i=0,1,2")
    assert record["exact_Q_rank1_witness"]["cap03_pairing"] == "trace(K)=1"
    assert record["scope"] == {
        "rep3_closed": False,
        "rank_zero_closed": True,
        "nonzero_ranks_pairing_only": True,
        "rep0_transport_used": False,
        "rep2_transport_used": False,
        "other_representatives_claimed": [],
        "full_X5_equations_used": False,
    }


def hostile(record, mutation):
    candidate = copy.deepcopy(record)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    record = json.loads((HERE / "results_rep3_low_rank_carrier.json").read_text())
    validate(record)
    tests = {
        "wrong_rep": hostile(record, lambda x: x.__setitem__("representative_id", 2)),
        "wrong_guard_orientation": hostile(record, lambda x: x["exact_guard"].__setitem__(0, "A06*A37=0")),
        "wrong_carrier": hostile(record, lambda x: x["carrier"].__setitem__("factorization_up_to_output_permutation", "A06*K*[A35|A37]")),
        "transport_overclaim": hostile(record, lambda x: x["scope"].__setitem__("rep0_transport_used", True)),
        "other_rep_overclaim": hostile(record, lambda x: x["scope"]["other_representatives_claimed"].append(1)),
        "missing_witness_pairing": hostile(record, lambda x: x["exact_Q_rank1_witness"].pop("cap03_pairing")),
        "wrong_selection": hostile(record, lambda x: x["selection"].__setitem__("selected", 1)),
    }
    assert all(tests.values())
    output = {"schema": "KRENN_X5_REP3_LOW_RANK_VALIDATION_V1", "status": "PASS", "hostile_tests": tests}
    temporary = HERE / "results_validation.json.tmp"
    temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    temporary.replace(HERE / "results_validation.json")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
