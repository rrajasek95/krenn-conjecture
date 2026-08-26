#!/usr/bin/env python3
"""Fail-closed validation/hostiles for remaining full-family carrier closures."""

from __future__ import annotations

import copy
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent


def validate(result):
    assert result["schema"] == "KRENN_X5_SEVEN_BLOCK_REPS1_4_5_LOW_RANK_CARRIER_V1"
    assert result["status"] == "PAIRING_ONLY_INCOMPLETE_REPS1_4_5_NONZERO_RANKS"
    assert result["sequential_order"] == [5, 1, 4]
    assert result["selection_basis"] == {"all_supported_matchings": 12, "all_minimum_carrier_terms": 2, "term_loads": {"1": 38718, "4": 40176, "5": 41634}, "first_direct_frozen_best_record_with_guard_controlled_common_factor": 5}
    assert [r["representative_id"] for r in result["representatives"]] == [5, 1, 4]
    expected_outside = {1: "47", 4: "47", 5: "37"}
    expected_factor = {1: "A06^T*K*[A13^T|A35]", 4: "A06^T*K*[A23^T|A35]", 5: "A06^T*K*[A35|A37]"}
    for record in result["representatives"]:
        representative_id = record["representative_id"]
        assert record["outside_pair"] == expected_outside[representative_id]
        assert record["independent_regeneration"]["supported_perfect_matchings"] == 12
        assert len(record["independent_regeneration"]["carrier_terms"]) == 2
        assert record["independent_regeneration"]["source_labelled_factorization"] == expected_factor[representative_id]
        assert record["independent_regeneration"]["best_record_directly_supports_guard_dichotomy"] == (representative_id == 5)
        assert (record["independent_regeneration"]["best_record_obstruction"] is None) == (representative_id == 5)
        assert record["carrier"]["cap"] == "03" and record["carrier"]["star_center"] == 4
        assert record["proof"]["closed_rank_scope"] == [0]
        assert record["proof"]["pairing_only_rank_scope"] == [1, 2, 3]
        assert record["proof"]["missing_diagonal_lemma"].startswith("For every i=0,1,2")
        assert record["exact_Q_rank1_local_replay"]["cap03_pairing"] == "trace(K)=1"
    assert result["scope"] == {
        "closed_representatives": [],
        "rank_zero_closed_representatives": [1, 4, 5],
        "nonzero_ranks_pairing_only": [1, 4, 5],
        "transport_from_rep0_rep2_rep3_used": False,
        "each_support_and_carrier_regenerated": True,
        "non_full_family_claimed": False,
        "full_x5_equations_used": False,
    }


def hostile(result, mutation):
    candidate = copy.deepcopy(result)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    result = json.loads((HERE / "results_remaining_reps_low_rank_carrier.json").read_text())
    validate(result)
    tests = {
        "missing_rep": hostile(result, lambda x: x["representatives"].pop()),
        "wrong_order": hostile(result, lambda x: x.__setitem__("sequential_order", [1, 4, 5])),
        "wrong_matching_count": hostile(result, lambda x: x["representatives"][0]["independent_regeneration"].__setitem__("supported_perfect_matchings", 13)),
        "wrong_outside_pair": hostile(result, lambda x: x["representatives"][1].__setitem__("outside_pair", "37")),
        "wrong_factor_orientation": hostile(result, lambda x: x["representatives"][2]["independent_regeneration"].__setitem__("source_labelled_factorization", "A06*K*[A35|A37]")),
        "rank_scope_overclaim": hostile(result, lambda x: x["representatives"][0]["proof"].__setitem__("closed_rank_scope", [0, 1])),
        "transport_overclaim": hostile(result, lambda x: x["scope"].__setitem__("transport_from_rep0_rep2_rep3_used", True)),
        "non_family_overclaim": hostile(result, lambda x: x["scope"].__setitem__("non_full_family_claimed", True)),
    }
    assert all(tests.values())
    output = {"schema": "KRENN_X5_REMAINING_FULL_FAMILY_VALIDATION_V1", "status": "PASS", "hostile_tests": tests}
    temporary = HERE / "results_validation.json.tmp"
    temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    temporary.replace(HERE / "results_validation.json")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
