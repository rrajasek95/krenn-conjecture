#!/usr/bin/env python3
"""Incremental joint-semigroup exchange closure for the closure22 packet."""

from collections import defaultdict
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_colour_holonomy_quotients import (
    P, PM8, inverse, key_add, matching_term, reduce_row, row_add,
    semigroup_key,
)
from audit_physical_graph_quotient import holonomy


RESULTS = HERE / "results_closure22_joint_cegar.json"
RESULTS_71 = HERE / "results_closure71_joint_cegar.json"


def projected_word(word):
    return tuple(semigroup_key(matching_term(word, matching)) for matching in PM8)


def translated_row(generator, quotient):
    row = {}
    for term in generator:
        row_add(row, key_add(quotient, term), 1)
    return row


def insert(row, basis):
    reduced = reduce_row(row, basis)
    if not reduced:
        return False
    pivot = min(reduced)
    scale = inverse(reduced[pivot])
    basis[pivot] = {
        column: coefficient * scale % P
        for column, coefficient in reduced.items()
    }
    return True


def separating_dual(basis, remainder):
    free = min(remainder)
    dual = {free: 1}
    for pivot in sorted(basis, reverse=True):
        value = sum(
            coefficient * dual.get(column, 0)
            for column, coefficient in basis[pivot].items()
            if column != pivot
        ) % P
        if value:
            dual[pivot] = (-value) % P
    assert sum(
        coefficient * dual.get(column, 0)
        for column, coefficient in remainder.items()
    ) % P != 0
    return dual


def run_audit(max_rounds=64, add_profile71=False, extra_words=()):
    labels = json.loads(
        (HERE / "results_second_order_lift_support.json").read_text()
    )["combined_closure_words"]
    if add_profile71:
        profile71 = [
            "".join(map(str, word))
            for word in product(range(3), repeat=8)
            if sorted(word.count(colour) for colour in set(word)) == [1, 7]
        ]
        labels = list(dict.fromkeys(labels + profile71))
    labels = list(dict.fromkeys(labels + list(extra_words)))
    generators = {
        label: projected_word(tuple(map(int, label))) for label in labels
    }
    cone = semigroup_key(matching_term((0,) * 8, PM8[0]))
    target = {}
    for term, coefficient in holonomy().items():
        row_add(target, key_add(cone, semigroup_key(term)), coefficient)

    basis = {}
    initial_rows = 0
    initial_independent = 0
    for label, generator in generators.items():
        quotients = set()
        for target_column in target:
            for term in generator:
                quotient = tuple(
                    a - b for a, b in zip(target_column, term)
                )
                if min(quotient) >= 0:
                    quotients.add(quotient)
        initial_rows += len(quotients)
        for quotient in sorted(quotients):
            initial_independent += insert(
                translated_row(generator, quotient), basis
            )

    rounds = []
    terminal = "round cap"
    for round_index in range(max_rounds + 1):
        remainder = reduce_row(dict(target), basis)
        if not remainder:
            terminal = "target reduced to zero"
            break
        dual = separating_dual(basis, remainder)
        if round_index == max_rounds:
            break

        candidates = []
        by_word = {}
        for label, generator in generators.items():
            pairings = defaultdict(int)
            for column, coefficient in dual.items():
                for term in generator:
                    quotient = tuple(a - b for a, b in zip(column, term))
                    if min(quotient) >= 0:
                        pairings[quotient] = (
                            pairings[quotient] + coefficient
                        ) % P
            live = sorted(
                quotient for quotient, coefficient in pairings.items()
                if coefficient
            )
            if live:
                by_word[label] = len(live)
                candidates.extend((label, quotient) for quotient in live)

        rank_before = len(basis)
        added = 0
        for label, quotient in candidates:
            added += insert(translated_row(generators[label], quotient), basis)
        rounds.append({
            "round": round_index + 1,
            "rank_before": rank_before,
            "remainder_terms_before": len(remainder),
            "dual_support": len(dual),
            "crossing_candidates": len(candidates),
            "crossing_words": by_word,
            "independent_rows_added": added,
            "rank_after": len(basis),
        })
        if not added:
            terminal = "no existing-word exchange row crosses separator"
            break

    final_remainder = reduce_row(dict(target), basis)
    final_dual = separating_dual(basis, final_remainder) if final_remainder else {}

    def balanced(value):
        return value if value <= P // 2 else value - P

    integer_dual = {
        column: balanced(coefficient)
        for column, coefficient in final_dual.items()
    }
    integer_crossing_translations = 0
    integer_max_abs_translation_pairing = 0
    integer_crossing_words = {}
    if integer_dual:
        for label, generator in generators.items():
            pairings = defaultdict(int)
            for column, coefficient in integer_dual.items():
                for term in generator:
                    quotient = tuple(a - b for a, b in zip(column, term))
                    if min(quotient) >= 0:
                        pairings[quotient] += coefficient
            live = [value for value in pairings.values() if value]
            if live:
                integer_crossing_words[label] = len(live)
                integer_crossing_translations += len(live)
                integer_max_abs_translation_pairing = max(
                    integer_max_abs_translation_pairing,
                    max(map(abs, live)),
                )
    integer_target_pairing = sum(
        balanced(coefficient) * integer_dual.get(column, 0)
        for column, coefficient in target.items()
    )
    return {
        "status": (
            "PASS closure22 joint-semigroup exchange reached target"
            if not final_remainder else
            "INCOMPLETE closure22 joint-semigroup exchange"
        ),
        "prime": P,
        "source_words": labels,
        "added_complete_profile71_orbit": add_profile71,
        "extra_words": list(extra_words),
        "initial_target_touching_rows": initial_rows,
        "initial_independent_rows": initial_independent,
        "rounds": rounds,
        "terminal": terminal,
        "final_rank": len(basis),
        "final_remainder_terms": len(final_remainder),
        "target_reduced_to_zero": not final_remainder,
        "terminal_modular_dual_support": len(final_dual),
        "terminal_integer_dual_balanced_max_abs": max(
            (abs(value) for value in integer_dual.values()), default=0
        ),
        "terminal_integer_crossing_translations": integer_crossing_translations,
        "terminal_integer_crossing_words": integer_crossing_words,
        "terminal_integer_max_abs_translation_pairing": (
            integer_max_abs_translation_pairing
        ),
        "terminal_integer_target_pairing": integer_target_pairing,
        "terminal_integer_is_full_semigroup_separator": (
            bool(integer_dual)
            and integer_crossing_translations == 0
            and integer_target_pairing != 0
        ),
        "terminal_integer_dual": [
            {"column": column, "coefficient": coefficient}
            for column, coefficient in sorted(integer_dual.items())
        ] if len(integer_dual) <= 256 else [],
        "final_remainder_sha256": hashlib.sha256(
            repr(sorted(final_remainder.items())).encode()
        ).hexdigest(),
        "scope": (
            "Exact F_32003 closure in the abstract joint edge/colour "
            "semigroup. Abstract multiplier histograms are not yet literal "
            "decorated monomial lifts, and zero remainder would still require "
            "characteristic-zero reconstruction."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rounds", type=int, default=64)
    parser.add_argument("--add-profile71", action="store_true")
    parser.add_argument("--extra-word", action="append", default=[])
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = run_audit(args.max_rounds, args.add_profile71, args.extra_word)
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.extra_word:
        suffix = "_".join(args.extra_word)
        result_path = HERE / f"results_closure22_plus_{suffix}_joint_cegar.json"
    else:
        result_path = RESULTS_71 if args.add_profile71 else RESULTS
    if args.write_results:
        result_path.write_text(output)
    if args.check_results and result_path.read_text() != output:
        raise RuntimeError("stored joint CEGAR result changed")
    print(output, end="")


if __name__ == "__main__":
    main()
