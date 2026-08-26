#!/usr/bin/env python3
"""Exact source/projected-module audit for the full 7+1 word orbit."""

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import sys


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_closure22_joint_cegar import P, insert, projected_word
from audit_colour_holonomy_quotients import PM8, matching_term


RESULT = HERE / "results_profile71_module_shape.json"


def label(word):
    return "".join(map(str, word))


def projected_row(word):
    row = defaultdict(int)
    for column in projected_word(word):
        row[column] += 1
    return dict(row)


def linear_combination(words, coefficients):
    out = defaultdict(int)
    for word, coefficient in zip(words, coefficients):
        for column, value in projected_row(word).items():
            out[column] += coefficient * value
    return {column: value for column, value in out.items() if value}


def rank(rows):
    basis = {}
    for row in rows:
        insert({column: value % P for column, value in row.items()}, basis)
    return len(basis)


def audit():
    orbit = [
        word for word in product(range(3), repeat=8)
        if sorted(word.count(colour) for colour in set(word)) == [1, 7]
    ]
    closure = set(json.loads(
        (HERE / "results_second_order_lift_support.json").read_text()
    )["combined_closure_words"])
    old = [word for word in orbit if label(word) in closure]
    new = [word for word in orbit if label(word) not in closure]

    # Literal decorated matching monomials determine their endpoint word, so
    # different word rows have disjoint support.  Check this directly.
    literal_multiplicity = Counter(
        term
        for word in orbit
        for term in (matching_term(word, matching) for matching in PM8)
    )
    assert len(literal_multiplicity) == 48 * 105
    assert set(literal_multiplicity.values()) == {1}

    rows = [projected_row(word) for word in orbit]
    old_rows = [projected_row(word) for word in old]
    assert rank(rows) == 42
    assert rank(old_rows) == 8

    kernel_checks = []
    kernel_coefficients = (3, -1, -1, -1, -1, -1, -1, 3)
    for majority in range(3):
        for minority in range(3):
            if majority == minority:
                continue
            words = []
            for site in range(8):
                word = [majority] * 8
                word[site] = minority
                words.append(tuple(word))
            relation = linear_combination(words, kernel_coefficients)
            assert not relation
            kernel_checks.append({
                "majority_colour": majority,
                "minority_colour": minority,
                "coefficients_by_site": list(kernel_coefficients),
            })

    # The quotient kernel is not stable under S8: swapping sites 0 and 1 in
    # the (majority,minority)=(0,1) kernel vector leaves a nonzero image.
    words = []
    for site in range(8):
        word = [0] * 8
        word[site] = 1
        words.append(tuple(word))
    swapped_coefficients = list(kernel_coefficients)
    swapped_coefficients[0], swapped_coefficients[1] = (
        swapped_coefficients[1], swapped_coefficients[0]
    )
    swapped_image = linear_combination(words, swapped_coefficients)
    assert len(swapped_image) == 30
    assert Counter(swapped_image.values()) == {-4: 15, 4: 15}

    plus_one = json.loads(
        (HERE / "results_closure22_plus_00000200_joint_cegar.json").read_text()
    )
    assert plus_one["terminal"] == "no existing-word exchange row crosses separator"
    assert plus_one["final_remainder_terms"] == 13636
    assert plus_one["rounds"][-1]["round"] == 100
    assert plus_one["terminal_integer_is_full_semigroup_separator"]

    second_dual = {
        tuple(record["column"]): record["coefficient"]
        for record in plus_one["terminal_integer_dual"]
    }
    second_crossings = {}
    second_pairing_histogram = Counter()
    for word in orbit:
        pairings = defaultdict(int)
        for column, coefficient in second_dual.items():
            for term in projected_word(word):
                quotient = tuple(a - b for a, b in zip(column, term))
                if min(quotient) >= 0:
                    pairings[quotient] += coefficient
        live = [value for value in pairings.values() if value]
        if live:
            second_crossings[label(word)] = len(live)
            second_pairing_histogram.update(live)
    assert len(second_crossings) == 6
    assert sum(second_crossings.values()) == 133
    assert not set(second_crossings).intersection(plus_one["source_words"])

    out = {
        "status": "PASS exact profile71 source/projected module audit",
        "source_orbit": {
            "size": len(orbit),
            "literal_row_support_each": 105,
            "literal_union_support": len(literal_multiplicity),
            "literal_rank": len(orbit),
            "representation_over_Q": (
                "(1 + S^(7,1)) external_tensor "
                "(1 + sign + 2*standard_S3)"
            ),
        },
        "closure22_intersection": {
            "words": sorted(map(label, old)),
            "size": len(old),
            "projected_rank": rank(old_rows),
        },
        "additional_orbit_words": len(new),
        "joint_projection": {
            "rank": rank(rows),
            "kernel_dimension": len(orbit) - rank(rows),
            "relative_generator_rank_over_closure22_intersection": (
                rank(rows) - rank(old_rows)
            ),
            "kernel_basis": kernel_checks,
            "site_swap_01_of_first_kernel": {
                "image_support": len(swapped_image),
                "coefficient_histogram": {
                    str(key): value
                    for key, value in sorted(Counter(swapped_image.values()).items())
                },
            },
            "equivariance_verdict": (
                "the six constant syzygies are quotient artifacts; their "
                "kernel is not S8-stable, so this projection cannot define "
                "an S8-equivariant matching-exchange boundary complex"
            ),
        },
        "plus_single_generator_control": {
            "word": "00000200",
            "rounds": len(plus_one["rounds"]),
            "terminal": plus_one["terminal"],
            "final_rank": plus_one["final_rank"],
            "final_remainder_terms": plus_one["final_remainder_terms"],
            "integer_dual_is_separator": plus_one[
                "terminal_integer_is_full_semigroup_separator"
            ],
            "replacement_dual_support": len(second_dual),
            "replacement_dual_profile71_crossing_words": second_crossings,
            "replacement_dual_profile71_crossing_rows": sum(
                second_crossings.values()
            ),
            "replacement_dual_profile71_pairing_histogram": {
                str(key): value
                for key, value in sorted(second_pairing_histogram.items())
            },
        },
        "theorem_scope": (
            "The completed source-word orbit kills the frozen terminal "
            "100-column functional because seven orbit words cross it.  "
            "Neither orbit completion nor the rank-42 projected packet is "
            "a cellular exactness theorem.  Exactness still requires a new "
            "target reduction or a new dual after adjoining all 48 words."
        ),
    }
    payload = json.dumps(out, indent=2, sort_keys=True) + "\n"
    out["logical_sha256"] = sha256(payload.encode()).hexdigest()
    return out


def main():
    current = audit()
    payload = json.dumps(current, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        RESULT.write_text(payload)
    if "--check-results" in sys.argv:
        assert RESULT.read_text() == payload
    print(payload, end="")


if __name__ == "__main__":
    main()
