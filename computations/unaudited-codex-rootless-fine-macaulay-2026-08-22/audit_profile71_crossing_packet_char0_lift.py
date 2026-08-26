#!/usr/bin/env python3
"""Lift the 29-word profile71 crossing-packet terminal dual over Z."""

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import sys


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_closure22_joint_cegar import projected_word
from audit_colour_holonomy_quotients import (
    P as SOURCE_PRIME, PM8, key_add, matching_term, semigroup_key,
)
from audit_physical_graph_quotient import holonomy


PRIMES = (31991, 32003, 32009, 32749)
FILES = {
    31991: HERE / "results_closure22_plus_profile71_joint_cegar_rust_p31991.json",
    32003: HERE / "results_closure22_plus_profile71_joint_cegar_rust.json",
    32009: HERE / "results_closure22_plus_profile71_joint_cegar_rust_p32009.json",
    32749: HERE / "results_closure22_plus_profile71_joint_cegar_rust_p32749.json",
}
RESULT = HERE / "results_profile71_crossing_packet_char0_lift.json"


def balanced(value, prime):
    value %= prime
    return value if value <= prime // 2 else value - prime


def dual(result):
    return {
        tuple(record["column"]): record["coefficient"]
        for record in result["terminal_integer_dual"]
    }


def round_signature(result):
    return [
        (
            row["round"], row["rank_before"], row["dual_support"],
            row["crossing_candidates"], row["independent_rows_added"],
            row["rank_after"],
        )
        for row in result["rounds"]
    ]


def exact_target():
    cone = semigroup_key(matching_term((0,) * 8, PM8[0]))
    target = defaultdict(int)
    for term, coefficient in holonomy().items():
        target[key_add(cone, semigroup_key(term))] += balanced(
            coefficient, SOURCE_PRIME
        )
    return {column: value for column, value in target.items() if value}


def exact_translation_crossings(labels, integer_dual):
    crossings = {}
    for label in labels:
        generator = projected_word(tuple(map(int, label)))
        pairings = defaultdict(int)
        for column, coefficient in integer_dual.items():
            for term in generator:
                quotient = tuple(a - b for a, b in zip(column, term))
                if min(quotient) >= 0:
                    pairings[quotient] += coefficient
        live = [value for value in pairings.values() if value]
        if live:
            crossings[label] = {
                "count": len(live),
                "max_abs": max(map(abs, live)),
            }
    return crossings


def audit():
    results = {prime: json.loads(FILES[prime].read_text()) for prime in PRIMES}
    reference = results[32003]
    for prime, result in results.items():
        assert result["prime"] == prime
        assert result["terminal"] == "no existing-word exchange row crosses separator"
        assert result["initial_independent_rows"] == 177996
        assert result["final_rank"] == 185635
        assert result["final_remainder_terms"] == 13636
        assert result["terminal_modular_dual_support"] == 138
        assert len(result["rounds"]) == 33
        assert result["source_words"] == reference["source_words"]
        assert round_signature(result) == round_signature(reference)

    modular_duals = {prime: dual(result) for prime, result in results.items()}
    reference_support = set(modular_duals[32003])
    assert len(reference_support) == 138
    assert all(set(value) == reference_support for value in modular_duals.values())

    lifted_by_prime = {
        prime: {
            column: balanced(2 * coefficient, prime)
            for column, coefficient in modular_duals[prime].items()
        }
        for prime in PRIMES
    }
    integer_dual = lifted_by_prime[32003]
    assert all(value == integer_dual for value in lifted_by_prime.values())
    assert min(integer_dual.values()) == -8
    assert max(integer_dual.values()) == 8
    assert 1 in map(abs, integer_dual.values())

    crossings = exact_translation_crossings(
        reference["source_words"], integer_dual
    )
    assert not crossings
    target = exact_target()
    assert len(target) == 13974
    target_pairing = sum(
        coefficient * integer_dual.get(column, 0)
        for column, coefficient in target.items()
    )
    assert target_pairing == 2

    profile71 = {
        "".join(map(str, word))
        for word in product(range(3), repeat=8)
        if sorted(word.count(colour) for colour in set(word)) == [1, 7]
    }
    present_profile71 = profile71.intersection(reference["source_words"])
    missing_profile71 = profile71.difference(reference["source_words"])
    assert len(profile71) == 48
    assert len(present_profile71) == 15
    assert len(missing_profile71) == 33
    modular_omitted_crossings = reference["all_word_scan"][
        "modular_profile71_crossings"
    ]
    assert set(modular_omitted_crossings).issubset(missing_profile71)
    assert modular_omitted_crossings == {"00000001": 2, "00100000": 2}

    result = {
        "status": "PASS exact Z lift for the 29-word profile71 crossing packet",
        "primes": list(PRIMES),
        "stable_modular_profile": {
            "initial_independent_rows": 177996,
            "terminal_rounds": 33,
            "final_rank": 185635,
            "final_remainder_terms": 13636,
            "dual_support": 138,
            "identical_round_and_pivot_signature": True,
            "identical_dual_column_support": True,
        },
        "rational_reconstruction": {
            "normalization": (
                "the modular dual normalized one coordinate to 1; its "
                "large +/-floor(p/2) entries are +/-1/2 modulo p"
            ),
            "operation": "multiply the modular dual by 2 and balance",
            "coefficient_histogram": {
                str(key): value
                for key, value in sorted(Counter(integer_dual.values()).items())
            },
            "max_abs": max(map(abs, integer_dual.values())),
            "primitive": True,
            "exact_admitted_translation_crossings": crossings,
            "exact_target_pairing": target_pairing,
            "verdict": (
                "poor balanced modular lift, not prime-dependent rank; "
                "the doubled 138-column vector is an exact Z separator"
            ),
        },
        "scope_guard": {
            "artifact_flag_added_complete_profile71_orbit": reference[
                "added_complete_profile71_orbit"
            ],
            "source_word_count": len(reference["source_words"]),
            "profile71_words_present": len(present_profile71),
            "profile71_words_missing": len(missing_profile71),
            "true_full_orbit_size": len(profile71),
            "true_full_packet_total_words": 62,
            "omitted_profile71_words_crossing_terminal_modular_dual": (
                modular_omitted_crossings
            ),
            "verdict": (
                "the artifact is closure22 plus seven crossing words, not "
                "the literal full profile71 orbit; the Z nonmembership "
                "theorem applies only to this fixed 29-word packet"
            ),
        },
        "source_result_sha256": {
            str(prime): sha256(FILES[prime].read_bytes()).hexdigest()
            for prime in PRIMES
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    return result


def main():
    result = audit()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        RESULT.write_text(text)
    if "--check-results" in sys.argv:
        assert RESULT.read_text() == text
    print(text, end="")


if __name__ == "__main__":
    main()
