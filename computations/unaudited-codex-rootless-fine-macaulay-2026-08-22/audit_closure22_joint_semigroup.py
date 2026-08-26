#!/usr/bin/env python3
"""First-layer joint edge/colour-semigroup gate for the closure22 packet.

The calculation includes exactly the degree-nine translations having a term
in the original target support.  It does not include translations reached
only after one or more exchange steps.  Its dual is therefore a separator for
the first target-touching layer, not for the full homogeneous ideal.
"""

from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_colour_holonomy_quotients import (
    P, PM8, digest, inverse, key_add, matching_term, reduce_row, row_add,
    semigroup_key,
)
from audit_physical_graph_quotient import holonomy


RESULTS = HERE / "results_closure22_joint_semigroup.json"


def projected_word(word):
    row = {}
    for matching in PM8:
        row_add(row, semigroup_key(matching_term(word, matching)), 1)
    return row


def run_audit():
    words = json.loads(
        (HERE / "results_second_order_lift_support.json").read_text()
    )["combined_closure_words"]
    words = tuple(tuple(map(int, word)) for word in words)

    cone = matching_term((0,) * 8, PM8[0])
    cone_key = semigroup_key(cone)
    target = {}
    for term, coefficient in holonomy().items():
        row_add(target, key_add(cone_key, semigroup_key(term)), coefficient)

    basis = {}
    quotient_counts = {}
    generated_rows = 0
    for word in words:
        label = "".join(map(str, word))
        generator = projected_word(word)
        quotients = set()
        for target_key in target:
            for term_key in generator:
                difference = tuple(a - b for a, b in zip(target_key, term_key))
                if min(difference) >= 0:
                    quotients.add(difference)
        quotient_counts[label] = len(quotients)
        for quotient in sorted(quotients):
            row = {}
            for term_key, coefficient in generator.items():
                row_add(row, key_add(quotient, term_key), coefficient)
            generated_rows += 1
            reduced = reduce_row(row, basis)
            if reduced:
                pivot = min(reduced)
                scale = inverse(reduced[pivot])
                basis[pivot] = {
                    column: coefficient * scale % P
                    for column, coefficient in reduced.items()
                }

    remainder = reduce_row(dict(target), basis)
    dual = {}
    dual_free_column = None
    if remainder:
        # The echelon rows have pivot coefficient one and all other columns
        # larger than the pivot.  Choosing one free remainder column and
        # back-substituting therefore constructs an exact F_p functional
        # annihilating the complete row span but not the target.
        dual_free_column = min(remainder)
        dual[dual_free_column] = 1
        for pivot in sorted(basis, reverse=True):
            value = sum(
                coefficient * dual.get(column, 0)
                for column, coefficient in basis[pivot].items()
                if column != pivot
            ) % P
            if value:
                dual[pivot] = (-value) % P
        assert all(
            sum(coefficient * dual.get(column, 0)
                for column, coefficient in row.items()) % P == 0
            for row in basis.values()
        )
    dual_target_pairing = sum(
        coefficient * dual.get(column, 0)
        for column, coefficient in target.items()
    ) % P
    if remainder:
        assert dual_target_pairing != 0

    def balanced(value):
        return value if value <= P // 2 else value - P

    integer_dual = {column: balanced(value) for column, value in dual.items()}
    integer_nonzero_rows = 0
    integer_max_row_pairing = 0
    if integer_dual:
        # Replay against every literal translated row over Z.  This turns
        # the small modular functional into a characteristic-zero witness
        # when the balanced representatives annihilate all rows literally.
        for word in words:
            generator = projected_word(word)
            quotients = set()
            for target_key in target:
                for term_key in generator:
                    difference = tuple(
                        a - b for a, b in zip(target_key, term_key)
                    )
                    if min(difference) >= 0:
                        quotients.add(difference)
            for quotient in quotients:
                pairing = sum(
                    integer_dual.get(key_add(quotient, term_key), 0)
                    for term_key in generator
                )
                integer_max_row_pairing = max(
                    integer_max_row_pairing, abs(pairing)
                )
                integer_nonzero_rows += pairing != 0
    integer_target_pairing = sum(
        balanced(coefficient) * integer_dual.get(column, 0)
        for column, coefficient in target.items()
    )

    return {
        "status": (
            "PASS closure22 target is in the first joint-semigroup layer"
            if not remainder else
            "PASS exact separator for the first joint-semigroup layer"
        ),
        "prime": P,
        "source_words": ["".join(map(str, word)) for word in words],
        "source_rows": len(words),
        "generated_macaulay_rows": generated_rows,
        "quotient_counts": quotient_counts,
        "projected_rank": len(basis),
        "target_terms": len(target),
        "remainder_terms": len(remainder),
        "target_in_joint_semigroup_span": not remainder,
        "remainder_digest": digest(sorted(remainder.items())),
        "remainder_sha256": hashlib.sha256(
            repr(sorted(remainder.items())).encode()
        ).hexdigest(),
        "modular_dual_support": len(dual),
        "modular_dual_target_pairing": dual_target_pairing,
        "modular_dual_balanced_max_abs": max(
            (abs(balanced(value)) for value in dual.values()), default=0
        ),
        "modular_dual_free_column": dual_free_column,
        "integer_dual": [
            {"column": column, "coefficient": coefficient}
            for column, coefficient in sorted(integer_dual.items())
        ],
        "integer_dual_nonzero_row_pairings": integer_nonzero_rows,
        "integer_dual_max_abs_row_pairing": integer_max_row_pairing,
        "integer_dual_target_pairing": integer_target_pairing,
        "integer_dual_is_characteristic_zero_first_layer_separator": (
            bool(integer_dual) and integer_nonzero_rows == 0
            and integer_target_pairing != 0
        ),
        "scope": (
            "Exact target-touching first-layer test only. Rows reached after "
            "exchange through non-target columns are omitted, so either "
            "verdict is nonterminal for full decorated ideal membership."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = run_audit()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        RESULTS.write_text(output)
    if args.check_results and RESULTS.read_text() != output:
        raise RuntimeError("stored closure22 joint-semigroup result changed")
    print(output, end="")


if __name__ == "__main__":
    main()
