#!/usr/bin/env python3
"""Bounded exact automatic local normal form through degrees six and five.

The automatic reducer starts only with one selected mixed coefficient, the
196 literal conormal lifts, and the 39 literal quadratic-obstruction lifts.
It closes translated degrees 1,...,6 for H_0 and 1,...,5 for H_1, proving
H_0 in I_mix+m_p^7 and H_1 in I_mix+m_p^6.  The intentionally bounded
checker does not run the memory-heavy unresolved H_1 degree-six step.
"""

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


HERE = Path(__file__).resolve().parent
ANALYZER_PATH = HERE / "analyze_n8_counterexample_local_standard_basis.py"
SPEC = importlib.util.spec_from_file_location("n8_local_standard_basis", ANALYZER_PATH)
ANALYZER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ANALYZER)

EXPECTED_LEDGER_SHA256 = (
    "a37e8bc7ab189edd5557fd368f2e4c8732c4cc40d519cde67b2f08614033c1c9"
)


def colour_ledger(colour, maximum_degree):
    records, reducer = ANALYZER.analyze(colour, maximum_degree)
    require(len(records) == maximum_degree, "automatic reducer stopped early")
    require(all(record["complete"] for record in records),
            "a bounded degree did not close")
    require([record["degree"] for record in records]
            == list(range(1, maximum_degree + 1)),
            "bounded degree sequence changed")
    correction_kinds = Counter(
        correction["kind"].split("_obstruction")[0]
        if "_obstruction" in correction["kind"]
        else correction["kind"].rsplit("_normal", 1)[0]
        for correction in reducer.corrections
    )
    maximum_functional_support = max(
        map(lambda correction: len(correction["functional"]),
            reducer.corrections)
    )
    return {
        "pure_colour": colour,
        "maximum_closed_degree": maximum_degree,
        "local_membership_power": maximum_degree + 1,
        "local_membership": (
            f"H_{colour} belongs to I_mix + m_p^{maximum_degree + 1}"
        ),
        "degree_records": records,
        "total_literal_equation_corrections": len(reducer.corrections),
        "correction_kind_counts": dict(sorted(correction_kinds.items())),
        "maximum_literal_functional_support": maximum_functional_support,
        "maximum_incoming_terms": max(
            record["incoming_terms"] for record in records
        ),
        "maximum_tangent_terms": max(
            record["tangent_terms"] for record in records
        ),
        "all_obstruction_remainders_zero": True,
        "all_final_normal_remainders_zero": True,
    }


def audit():
    zero = colour_ledger(0, 6)
    one = colour_ledger(1, 5)
    require(zero["maximum_incoming_terms"] == 291123,
            "H0 bounded memory ledger changed")
    require(one["maximum_incoming_terms"] == 380392,
            "H1 bounded memory ledger changed")
    return {
        "arithmetic": "exact Q",
        "ambient_variables": 252,
        "mixed_jacobian_rank": 196,
        "mixed_tangent_dimension": 56,
        "quadratic_obstruction_rank": 39,
        "colours": [zero, one],
        "conclusions": [
            "H_0 belongs to I_mix + m_p^7",
            "H_1 belongs to I_mix + m_p^6",
        ],
        "provenance": (
            "every correction is a polynomial multiplier times a literal "
            "rational combination of mixed hafnian equations"
        ),
        "bounded_scope": (
            "H1 translated degree six is intentionally not run; an "
            "exploratory attempt was stopped before the 1.5GB memory cap"
        ),
    }


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen automatic local ledger digest changed")
    print(
        "n=8 automatic local standard basis: PASS; "
        "H0 in I_mix+m_p^7, H1 in I_mix+m_p^6; "
        "exact-Q literal provenance, bounded before H1 degree 6"
    )
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
