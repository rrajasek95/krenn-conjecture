#!/usr/bin/env python3
"""Fail-closed validator and hostile tests for rep2 exhaustive carrier closure."""

from __future__ import annotations

import copy
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent


def validate(result):
    assert result["schema"] == "KRENN_X5_SEVEN_BLOCK_REP2_EXHAUSTIVE_CARRIER_V1"
    assert result["status"] == "PAIRING_ONLY_INCOMPLETE_REP2_NONZERO_RANKS"
    assert result["representative_id"] == 2
    census = result["exhaustive_census"]
    assert census["perfect_matchings_total"] == 105 and census["perfect_matchings_supported"] == 13
    assert census["supported_caps"] == 15 and census["centers_per_cap"] == 6 and census["carrier_configurations"] == 90
    assert census["term_count_histogram"] == {"2": 8, "3": 14, "4": 28, "5": 8, "6": 12, "7": 12, "8": 4, "9": 2, "10": 2}
    assert len(census["minimum_carriers"]) == 8
    carrier = result["closing_carrier"]
    assert carrier["cap"] == "03" and carrier["star_center"] == 4 and carrier["common_block"] == "06"
    assert carrier["expanded_ledger_factor"] == "A06^T*K*[A23^T|A35]"
    assert result["literal_source_factorization"]["response_matrices"] == {"R26": "A06^T*K*A23^T", "R56": "A06^T*K*A35"}
    assert len(result["literal_source_factorization"]["coordinate_expansions"]) == 18
    assert result["exact_guard"] == ["A06*A57^T=0", "A57^T+A17*A56^T=0", "A26*A57^T+A56^T=0"]
    assert result["proof"]["closed_rank_scope"] == [0]
    assert result["proof"]["pairing_only_rank_scope"] == [1, 2, 3]
    assert result["proof"]["missing_diagonal_lemma"].startswith("For every i=0,1,2")
    assert result["exact_Q_rank1_local_replay"]["cap03_pairing"] == "trace(K)=1"
    assert result["scope"] == {"rep2_full_family_closed": False, "rank_zero_closed": True, "nonzero_ranks_pairing_only": True, "groebner_used": False, "transport_used": False, "non_full_family_claimed": False}


def hostile(result, mutation):
    candidate = copy.deepcopy(result)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    result = json.loads((HERE / "results_rep2_exhaustive_carrier.json").read_text())
    validate(result)
    tests = {
        "wrong_carrier_count": hostile(result, lambda x: x["exhaustive_census"].__setitem__("carrier_configurations", 89)),
        "missing_minimum_carrier": hostile(result, lambda x: x["exhaustive_census"]["minimum_carriers"].pop()),
        "wrong_histogram": hostile(result, lambda x: x["exhaustive_census"]["term_count_histogram"].__setitem__("2", 7)),
        "wrong_response_orientation": hostile(result, lambda x: x["literal_source_factorization"]["response_matrices"].__setitem__("R26", "A06^T*K*A23")),
        "wrong_guard_orientation": hostile(result, lambda x: x["exact_guard"].__setitem__(0, "A06*A57=0")),
        "rank_overclaim": hostile(result, lambda x: x["proof"].__setitem__("closed_rank_scope", [0, 1])),
        "transport_overclaim": hostile(result, lambda x: x["scope"].__setitem__("transport_used", True)),
        "non_family_overclaim": hostile(result, lambda x: x["scope"].__setitem__("non_full_family_claimed", True)),
    }
    assert all(tests.values())
    output = {"schema": "KRENN_X5_REP2_EXHAUSTIVE_CARRIER_VALIDATION_V1", "status": "PASS", "hostile_tests": tests}
    temporary = HERE / "results_validation.json.tmp"
    temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    temporary.replace(HERE / "results_validation.json")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
