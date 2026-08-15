#!/usr/bin/env python3
"""Support minimality on a tight cut: derivative independence and guard.

The mathematical theorem is elementary but useful.  If every compatible
perfect matching uses exactly one live cut cell, the matching tensor is
jointly linear in all of those cells.  In a support-minimal exact source the
corresponding *physical* derivative tensors are therefore linearly
independent: a kernel vector would permit an affine coefficient move setting
one live cell to zero without changing the tensor.

The checker realizes the sharp obstruction to a stronger deletion claim on
the exact ternary K4 one-factor source.  Its three cut derivatives are the
three pure target tensors.  They are independent and every pure escape is
essential, so pure normalization alone cannot select a deletable cut state.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json


COLOURS = tuple(range(3))
VERTICES = tuple(range(4))
WORDS = tuple(product(COLOURS, repeat=len(VERTICES)))


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
ONE_FACTORS = (
    tuple(sorted((edge(0, 1), edge(2, 3)))),
    tuple(sorted((edge(0, 2), edge(1, 3)))),
    tuple(sorted((edge(0, 3), edge(1, 2)))),
)


def product_value(values):
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def matching_tensor(support):
    answer = []
    for word in WORDS:
        coefficient = Fraction(0)
        for matching in MATCHINGS:
            cells = tuple((endpoints,
                           word[endpoints[0]], word[endpoints[1]])
                          for endpoints in matching)
            if all(cell in support for cell in cells):
                coefficient += product_value(support[cell] for cell in cells)
        answer.append(coefficient)
    return tuple(answer)


def target_tensor():
    return tuple(Fraction(int(len(set(word)) == 1)) for word in WORDS)


def derivative_tensor(support, selected_cell):
    answer = []
    for word in WORDS:
        coefficient = Fraction(0)
        for matching in MATCHINGS:
            cells = tuple((endpoints,
                           word[endpoints[0]], word[endpoints[1]])
                          for endpoints in matching)
            if selected_cell not in cells:
                continue
            other_cells = tuple(cell for cell in cells
                                if cell != selected_cell)
            if all(cell in support for cell in other_cells):
                coefficient += product_value(support[cell]
                                             for cell in other_cells)
        answer.append(coefficient)
    return tuple(answer)


def matrix_rank(columns):
    rows = [[Fraction(column[row]) for column in columns]
            for row in range(len(columns[0]))]
    rank = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(rank, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [left - scale * right
                         for left, right in zip(rows[row], rows[rank],
                                                strict=True)]
        rank += 1
    return rank


def add_vectors(*vectors):
    return tuple(sum(values, Fraction(0))
                 for values in zip(*vectors, strict=True))


def scale_vector(scale, vector):
    return tuple(scale * value for value in vector)


def exact_k4_guard():
    support = {}
    for colour, matching in enumerate(ONE_FACTORS):
        for endpoints in matching:
            support[(endpoints, colour, colour)] = Fraction(1)
    require(MATCHINGS == ONE_FACTORS, (MATCHINGS, ONE_FACTORS))
    tensor = matching_tensor(support)
    target = target_tensor()
    require(tensor == target, "the K4 one-factor source ceased to be exact")

    # The one-vertex shore {0}|{1,2,3} is tight: every matching has exactly
    # one crossing edge.  Keep source-derived labels on its three live cells.
    cut_cells = tuple((edge(0, colour + 1), colour, colour)
                      for colour in COLOURS)
    derivatives = tuple(derivative_tensor(support, cell)
                        for cell in cut_cells)
    require(matrix_rank(derivatives) == 3, derivatives)
    pure_indices = tuple(WORDS.index((colour,) * 4) for colour in COLOURS)
    pure_projection = tuple(
        tuple(derivative[index] for derivative in derivatives)
        for index in pure_indices
    )
    require(pure_projection == (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    ), pure_projection)

    labels = []
    for colour, (cell, matching) in enumerate(zip(cut_cells, ONE_FACTORS,
                                                  strict=True)):
        cofactor = next(endpoints for endpoints in matching
                        if endpoints != cell[0])
        labels.append({
            "word": str(colour) * 4,
            "fine_matching": "|".join(
                f"{left}{right}" for left, right in matching
            ),
            "operation": "tight_cut_physical_derivative",
            "cap_window_L_to_R": f"0>{colour + 1}",
            "endpoint_colour": f"{colour}{colour}",
            "cofactor_state": f"{cofactor[0]}{cofactor[1]};{colour}",
        })

    # Joint linearity is checked on a nontrivial rational perturbation.  The
    # theorem in the note proves the identity for arbitrary perturbations.
    perturbation = (Fraction(2), Fraction(-3), Fraction(5, 2))
    changed = dict(support)
    for cell, delta in zip(cut_cells, perturbation, strict=True):
        changed[cell] += delta
    actual_difference = add_vectors(
        matching_tensor(changed), scale_vector(-1, tensor)
    )
    predicted_difference = add_vectors(*(
        scale_vector(delta, derivative)
        for delta, derivative in zip(perturbation, derivatives, strict=True)
    ))
    require(actual_difference == predicted_difference,
            (actual_difference, predicted_difference))

    deletion_failures = []
    for colour, cell in enumerate(cut_cells):
        deleted = dict(support)
        deleted.pop(cell)
        deleted_tensor = matching_tensor(deleted)
        failed_word = (colour,) * 4
        failed_index = WORDS.index(failed_word)
        require(deleted_tensor[failed_index] == 0
                and target[failed_index] == 1,
                (cell, deleted_tensor[failed_index]))
        deletion_failures.append({
            "deleted_cap_window": labels[colour]["cap_window_L_to_R"],
            "lost_pure_word": "".join(map(str, failed_word)),
            "coefficient_after_deletion": "0",
        })

    # Every one of the six live decorated cells is indispensable.  This is
    # stronger than the cut-cell statement and pins support-minimality of the
    # literal K4 source at its fixed coefficients.
    indispensable = []
    for cell in sorted(support):
        deleted = dict(support)
        deleted.pop(cell)
        require(matching_tensor(deleted) != target, cell)
        indispensable.append(
            f"{cell[0][0]}{cell[0][1]};{cell[1]}{cell[2]}"
        )

    return {
        "vertices": 4,
        "source_exact_for_all_words": len(WORDS),
        "live_decorated_cells": len(support),
        "all_live_cells_indispensable": tuple(indispensable),
        "cut_is_tight": True,
        "live_cut_cells": len(cut_cells),
        "derivative_rank": matrix_rank(derivatives),
        "pure_projection": tuple(tuple(map(str, row))
                                 for row in pure_projection),
        "labels": tuple(labels),
        "joint_linearity_perturbation": tuple(map(str, perturbation)),
        "deletion_failures": tuple(deletion_failures),
        "verdict": "pure escape is essential, not deletable",
    }


def kernel_deletion_formula():
    # Formal coordinates for the source-natural affine move.  If sum h_j D_j
    # is zero and h_p != 0, take t=-q_p/h_p.  This sets q'_p=0 and preserves
    # every output coefficient by joint linearity.
    q = (Fraction(2), Fraction(-3), Fraction(5))
    h = (Fraction(1), Fraction(2), Fraction(-1))
    pivot = 1
    parameter = -q[pivot] / h[pivot]
    moved = tuple(left + parameter * right
                  for left, right in zip(q, h, strict=True))
    require(moved[pivot] == 0, (parameter, moved))
    return {
        "sample_live_coefficients": tuple(map(str, q)),
        "sample_kernel_relation": tuple(map(str, h)),
        "pivot": pivot,
        "affine_parameter": str(parameter),
        "moved_coefficients": tuple(map(str, moved)),
        "pivot_deleted": True,
        "logical_hypothesis": "sum_j h_j D_j = 0",
    }


def build_ledger():
    return {
        "theorem": "support-minimal tight-cut physical derivative independence",
        "minimality_formula": kernel_deletion_formula(),
        "smallest_nontrivial_exact_guard": exact_k4_guard(),
        "scope": (
            "minimality among occupied aggregate decorated cells at fixed "
            "order; derivative tensors are compared after physical "
            "augmentation, not in a freely labelled occurrence module"
        ),
        "not_proved": (
            "site contraction, N-to-N-2 descent, or deletability from a "
            "nonzero pure coordinate alone"
        ),
    }


EXPECTED_LEDGER_SHA256 = "b8f641baa5a66822f2215f5243f453f460d2fa1aad0d4eb2f12e09ac6544c78f"


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
                f"tight-cut minimality ledger changed: {digest}")
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("uniform tight-cut minimal derivative theorem: PASS")
    print("mode", arguments.mode)
    print("ledger_sha256", digest)
    print("minimal exact source => physical cut derivatives independent")
    print("pure escape deletion: FALSE (exact K4 guard)")


if __name__ == "__main__":
    main()
