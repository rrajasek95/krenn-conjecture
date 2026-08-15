#!/usr/bin/env python3
"""Complete physical derivative rank of the C6 seven-cell escape packet.

The seven-cell cap sector has three live colours on cap 34 and two
colour-one residual matchings.  Give the two residual monomials opposite
weights, as forced by either mixed cap row.  This checker adds each of the
twelve possible colour-one perfect matchings avoiding 34, using the minimum
missing cells, and computes every derivative on all 3^6 output words.

At the forced residual equation H=0 all three cap-cell derivatives vanish.
Every new escape cell has derivative supported only on pure word 111111 and
raises physical rank from zero to one.  Deleting all three cap cells leaves
the augmented tensor unchanged.  Thus the escape is a genuinely independent
state, while the killed cap states—not the escape—are support-redundant.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json


N = 6
VERTICES = tuple(range(N))
COLOURS = tuple(range(3))
WORDS = tuple(product(COLOURS, repeat=N))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


MATCHINGS = tuple(sorted(perfect_matchings(VERTICES)))
CAP = edge(3, 4)
CORE = (edge(0, 5), edge(1, 2))
MATE = (edge(0, 1), edge(2, 5))


def cell(endpoints, colour):
    return endpoints, colour, colour


def matching_name(matching):
    return "|".join(f"{left}{right}" for left, right in matching)


def word_name(word):
    return "".join(map(str, word))


def product_value(values):
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def occurrence_cells(matching, word):
    return tuple((endpoints, word[endpoints[0]], word[endpoints[1]])
                 for endpoints in matching)


def matching_tensor(support):
    answer = []
    for word in WORDS:
        coefficient = Fraction(0)
        for matching in MATCHINGS:
            cells = occurrence_cells(matching, word)
            if all(selected in support for selected in cells):
                coefficient += product_value(support[selected]
                                             for selected in cells)
        answer.append(coefficient)
    return tuple(answer)


def derivative_tensor(support, selected_cell):
    answer = []
    for word in WORDS:
        coefficient = Fraction(0)
        for matching in MATCHINGS:
            cells = occurrence_cells(matching, word)
            if selected_cell not in cells:
                continue
            remaining = tuple(item for item in cells
                              if item != selected_cell)
            if all(item in support for item in remaining):
                coefficient += product_value(support[item]
                                             for item in remaining)
        answer.append(coefficient)
    return tuple(answer)


def matrix_rank(columns):
    if not columns:
        return 0
    basis = {}
    for column in columns:
        vector = {index: Fraction(value)
                  for index, value in enumerate(column) if value}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                scale = vector[pivot]
                basis[pivot] = {index: value / scale
                                for index, value in vector.items()}
                break
            scale = vector[pivot]
            for index, value in basis[pivot].items():
                vector[index] = vector.get(index, Fraction(0)) - scale * value
                if not vector[index]:
                    del vector[index]
    return len(basis)


def nonzero_coordinates(vector):
    return tuple((word_name(WORDS[index]), str(value))
                 for index, value in enumerate(vector) if value)


def seven_cell_base():
    support = {cell(CAP, colour): Fraction(1) for colour in COLOURS}
    support.update({
        cell(CORE[0], 1): Fraction(1),
        cell(CORE[1], 1): Fraction(1),
        cell(MATE[0], 1): Fraction(1),
        cell(MATE[1], 1): Fraction(-1),
    })
    require(len(support) == 7, support)
    residual_core = support[cell(CORE[0], 1)] * support[cell(CORE[1], 1)]
    residual_mate = support[cell(MATE[0], 1)] * support[cell(MATE[1], 1)]
    require((residual_core, residual_mate,
             residual_core + residual_mate) ==
            (Fraction(1), Fraction(-1), Fraction(0)),
            (residual_core, residual_mate))
    require(not any(matching_tensor(support)),
            nonzero_coordinates(matching_tensor(support)))
    return support


def augment_by_escape(base, matching):
    require(CAP not in matching, matching)
    missing = tuple(cell(endpoints, 1) for endpoints in matching
                    if cell(endpoints, 1) not in base)
    require(len(missing) in (2, 3), (matching, missing))
    support = dict(base)
    for selected in missing:
        support[selected] = Fraction(1)

    # Normalize the new occurrence itself to coefficient one.  When it uses
    # the pre-existing negative cell 25;11, the last new cell is negated.
    occurrence = tuple(cell(endpoints, 1) for endpoints in matching)
    current_weight = product_value(support[selected]
                                   for selected in occurrence)
    support[missing[-1]] /= current_weight
    require(product_value(support[selected] for selected in occurrence) == 1,
            (matching, support, occurrence))
    return support, missing


def audit_all_escapes():
    base = seven_cell_base()
    base_cells = tuple(base)
    cap_cells = tuple(cell(CAP, colour) for colour in COLOURS)
    cap_words = ("111001", "111111", "111221")
    base_cap_derivatives = tuple(derivative_tensor(base, selected)
                                 for selected in cap_cells)
    require(all(not any(vector) for vector in base_cap_derivatives),
            tuple(map(nonzero_coordinates, base_cap_derivatives)))

    escape_matchings = tuple(matching for matching in MATCHINGS
                             if CAP not in matching)
    require(len(escape_matchings) == 12, escape_matchings)
    missing_histogram = Counter()
    old_rank_histogram = Counter()
    full_old_span_rank_increase = Counter()
    derivative_instances = 0
    ledgers = []
    pure_index = WORDS.index((1,) * N)
    for matching in escape_matchings:
        support, missing = augment_by_escape(base, matching)
        missing_histogram[len(missing)] += 1
        tensor = matching_tensor(support)
        require(nonzero_coordinates(tensor) == (("111111", "1"),),
                (matching, nonzero_coordinates(tensor)))

        cap_derivatives = tuple(derivative_tensor(support, selected)
                                for selected in cap_cells)
        require(all(not any(vector) for vector in cap_derivatives),
                (matching, tuple(map(nonzero_coordinates, cap_derivatives))))
        require(matrix_rank(cap_derivatives) == 0, matching)

        # Also audit the larger, potentially ambiguous comparison against all
        # seven old cell derivatives.  If the escape shares one old residual
        # cell, differentiating that product already exposes the escape word;
        # if it is disjoint, the old span is only the common three-word vector.
        old_derivatives = tuple(derivative_tensor(support, selected)
                                for selected in base_cells)
        old_rank = matrix_rank(old_derivatives)
        overlaps = tuple(cell(endpoints, 1) for endpoints in matching
                         if cell(endpoints, 1) in base)
        require((len(missing), len(overlaps), old_rank) in (
            (2, 1, 2), (3, 0, 1)
        ), (matching, missing, overlaps, old_rank))
        old_rank_histogram[old_rank] += 1

        new_derivative_ledgers = []
        for selected in missing:
            derivative = derivative_tensor(support, selected)
            coordinates = nonzero_coordinates(derivative)
            require(len(coordinates) == 1
                    and coordinates[0][0] == "111111"
                    and abs(derivative[pure_index]) == 1,
                    (matching, selected, coordinates))
            require(matrix_rank(cap_derivatives + (derivative,)) == 1,
                    (matching, selected))
            old_plus_rank = matrix_rank(old_derivatives + (derivative,))
            old_increase = old_plus_rank - old_rank
            require(old_increase == int(not overlaps),
                    (matching, selected, old_rank, old_plus_rank, overlaps))
            full_old_span_rank_increase[old_increase] += 1
            derivative_instances += 1
            new_derivative_ledgers.append({
                "new_cell": (
                    f"{selected[0][0]}{selected[0][1]};"
                    f"{selected[1]}{selected[2]}"
                ),
                "operation": "cap_avoiding_escape_physical_derivative",
                "fine_matching": matching_name(matching),
                "cap_window_label": "avoid:34",
                "word_witness": coordinates[0][0],
                "witness_value": coordinates[0][1],
                "rank_before_after": (0, 1),
                "rank_increase_over_all_seven_old_cells": old_increase,
                "full_old_span_witness": (
                    "delta_111111-delta_111001"
                    if not overlaps else "dependent_after_shared-cell_product"
                ),
            })

        # The exact support move kills all three cap states.  Since their
        # complete derivatives are zero, this changes none of the 729 rows.
        deleted = dict(support)
        for selected in cap_cells:
            deleted.pop(selected)
        require(matching_tensor(deleted) == tensor,
                (matching, nonzero_coordinates(matching_tensor(deleted)),
                 nonzero_coordinates(tensor)))

        # A stronger exact reduction keeps only the three cells of the escape
        # matching.  It removes the whole killed seven-cell sector except for
        # a possible one-cell overlap and preserves all 729 coordinates.
        escape_cells = frozenset(cell(endpoints, 1) for endpoints in matching)
        reduced = {selected: support[selected] for selected in escape_cells}
        require(len(reduced) == 3 and matching_tensor(reduced) == tensor,
                (matching, reduced, nonzero_coordinates(matching_tensor(reduced))))

        ledgers.append({
            "escape_fine": matching_name(matching),
            "missing_cells": tuple(item["new_cell"]
                                   for item in new_derivative_ledgers),
            "complete_tensor": (("111111", "1"),),
            "cap_derivative_words_before_cancellation": cap_words,
            "cap_derivative_rank_after_H_zero": 0,
            "escape_overlap_with_old_residual": tuple(
                f"{selected[0][0]}{selected[0][1]};11"
                for selected in overlaps
            ),
            "all_seven_old_derivative_rank": old_rank,
            "new_derivatives": tuple(new_derivative_ledgers),
            "rank_increase": 1,
            "delete_move": "q34^00=q34^11=q34^22=0",
            "tensor_unchanged_after_delete": True,
            "exact_three_cell_reduction": tuple(
                f"{selected[0][0]}{selected[0][1]};11"
                for selected in sorted(escape_cells)
            ),
        })

    require(missing_histogram == Counter({2: 8, 3: 4}), missing_histogram)
    require(derivative_instances == 28, derivative_instances)
    require(old_rank_histogram == Counter({2: 8, 1: 4}),
            old_rank_histogram)
    require(full_old_span_rank_increase == Counter({0: 16, 1: 12}),
            full_old_span_rank_increase)
    return {
        "physical_output_coordinates_checked_per_tensor": len(WORDS),
        "base_cells": 7,
        "forced_equation": "H=(q05^11*q12^11)+(q01^11*q25^11)=1-1=0",
        "cap_cells": ("34;00", "34;11", "34;22"),
        "cap_derivative_universal_shape": (
            "H*e_111001", "H*e_111111", "H*e_111221"
        ),
        "cap_derivative_rank_mod_H": 0,
        "cap_avoiding_matchings": len(escape_matchings),
        "minimum_new_cell_histogram": tuple(sorted(missing_histogram.items())),
        "new_cell_derivative_instances": derivative_instances,
        "escape_derivative_rank_increase": (0, 1),
        "all_seven_old_derivative_rank_histogram": tuple(
            sorted(old_rank_histogram.items())
        ),
        "new_derivative_increase_over_all_seven_old_cells": tuple(
            sorted(full_old_span_rank_increase.items())
        ),
        "escape_word_witness": "111111",
        "escape_ledgers": tuple(ledgers),
        "support_deleting_move": "delete all three live cap-34 cells",
        "deleted_cells": 3,
        "strong_reduction": "delete to the three cells of the escape matching",
        "state_classification": "escape independent; killed cap sector redundant",
    }


def algebraic_span_guard():
    # In the universal coefficient ring the pure cap derivative is H*e and
    # the escape is e.  Polynomial membership would require 1 in the proper
    # ideal (H).  After the exact mixed-row specialization H=0, the image
    # drops to zero while the escape class survives.
    return {
        "universal_cap_image_in_pure_word": "(H) * e_111111",
        "escape_state": "1 * e_111111",
        "polynomial_span_membership": False,
        "required_illegal_multiplier": "1/H",
        "mixed_row_specialization": "H=0",
        "specialized_cap_rank": 0,
        "specialized_augmented_rank": 1,
        "nonflat_warning": "localizing at H contradicts the live mixed zero",
        "larger_old_span_nuance": (
            "8 overlap escapes are tangent-dependent on all seven old cell "
            "derivatives; 4 disjoint escapes remain independent.  Only the "
            "three cap cells form the jointly-linear boundary block."
        ),
    }


def build_ledger():
    return {
        "theorem": "C6 seven-cell cap-avoiding escape physical derivative rank",
        "span_guard": algebraic_span_guard(),
        "exhaustive_escape_audit": audit_all_escapes(),
        "scope": (
            "exact seven-cell diagonal cap sector plus one minimal pure-one "
            "escape; full 3^6 physical tensors, not a full ternary GHZ source"
        ),
    }


EXPECTED_LEDGER_SHA256 = "acedfcdbce4e9c44a5a9e8d71954733f95b4229b7e8731baa583d2a249b1f610"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                f"C6 escape derivative ledger changed: {digest}")
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("uniform C6 seven-cell escape derivative rank: PASS")
    print("mode", arguments.mode)
    print("ledger_sha256", digest)
    print("cap derivatives mod H: rank 0")
    print("cap-avoiding escape: independent rank increase 0 -> 1")
    print("exact deletion: remove the three killed cap cells")


if __name__ == "__main__":
    main()
