#!/usr/bin/env python3
"""Exact common-q closure counterguard for the multiplicity Segre cube.

The dense rank-one alternate tensor forced by the doubled carrier is
coefficient-feasible.  Starting from its M0 recombination cube, add the
aligned matching F0 to cancel the four frozen debts.  This exports eight
singleton words.  The unique third matching in the residual K4, whose two
edges are the cross pairs 25 and 34, cancels all eight with one rank-one
2x2 sign matrix.  The resulting 14-cell quadratic has twelve live top
fibres, every one an exact cancelling binomial, hence q^[3]=0.

Thus the Segre coefficient coupling alone does not contradict a common q.
The exact missing one-bad data are the unary top q^[3]=X0 and the response
rows on the diagonal/cross hole pairs, not another independent mate choice.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = "computations/verify_recombination_cube_segre_cancellation.py"
DEPENDENCY_SHA256 = (
    "b2e3bcfa8b4a7832b2db128f53cc524cb12c8aa87f0490e680f238757af81023"
)
EXPECTED_DIGEST = "6c6f0293e0478c41023366f282ad9936a3c72233da1bec1d580d67f20f599e85"

SITES = tuple(range(6))
COLOURS = tuple(range(3))
M0 = ((0, 1), (2, 3), (4, 5))
F0 = ((0, 1), (2, 4), (3, 5))
CROSS = ((0, 1), (2, 5), (3, 4))
CUBE_DEBT_WORDS = (
    (1, 0, 2, 0, 0, 1),  # 001
    (1, 0, 0, 1, 2, 0),  # 010
    (2, 0, 2, 0, 0, 1),  # 101
    (2, 0, 0, 1, 2, 0),  # 110
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependency():
    actual = sha256((ROOT / DEPENDENCY).read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            f"dependency changed: {DEPENDENCY}: {actual}")


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted(((first, second),) + tail))


MATCHINGS = tuple(perfect_matchings(SITES))


def decorated_term(matching, word):
    return tuple(sorted(
        (edge, (word[edge[0]], word[edge[1]]))
        for edge in matching
    ))


def term_word(term):
    word = [None] * len(SITES)
    for (left, right), (left_colour, right_colour) in term:
        word[left], word[right] = left_colour, right_colour
    require(all(colour is not None for colour in word),
            "a decorated term stopped covering the residual sites")
    return tuple(word)


def term_value(term, weights):
    value = Fraction(1)
    for cell in term:
        value *= weights[cell]
    return value


def live_fibre(word, support):
    return tuple(
        decorated_term(matching, word)
        for matching in MATCHINGS
        if set(decorated_term(matching, word)) <= support
    )


def full_top_table(support, weights):
    table = []
    for word in itertools.product(COLOURS, repeat=len(SITES)):
        live = live_fibre(word, support)
        if not live:
            continue
        coefficient = sum(
            (term_value(term, weights) for term in live),
            Fraction(0),
        )
        table.append((word, live, coefficient))
    return tuple(table)


def incidence(term):
    return Counter(term)


def audit_plucker_square():
    m_terms = tuple(decorated_term(M0, word) for word in CUBE_DEBT_WORDS)
    f_terms = tuple(decorated_term(F0, word) for word in CUBE_DEBT_WORDS)
    require(incidence(m_terms[0]) + incidence(m_terms[3])
            == incidence(m_terms[1]) + incidence(m_terms[2]),
            "the selected cube Plucker monomial identity changed")
    require(incidence(f_terms[0]) + incidence(f_terms[3])
            == incidence(f_terms[1]) + incidence(f_terms[2]),
            "the F0 mate Plucker monomial identity changed")

    support = frozenset(
        cell for term in m_terms + f_terms for cell in term
    )
    require(len(support) == 10,
            "the aligned Plucker-square support changed")
    weights = {cell: Fraction(1) for cell in support}
    # The two F0 cells on edge 24 are private to the mate matching.  Giving
    # both value -1 cancels all four cube debts without changing M0.
    for cell in support:
        if cell[0] == (2, 4):
            weights[cell] = Fraction(-1)

    selected_rows = []
    for word in CUBE_DEBT_WORDS:
        live = live_fibre(word, support)
        values = tuple(term_value(term, weights) for term in live)
        require(len(live) == 2 and values == (Fraction(1), Fraction(-1)),
                f"an aligned debt fibre stopped cancelling: {word}: {values}")
        selected_rows.append({
            "word": "".join(map(str, word)),
            "physical_matchings": [
                [list(edge) for edge, _colours in term] for term in live
            ],
            "values": [str(value) for value in values],
        })

    table = full_top_table(support, weights)
    histogram = Counter((len(live), str(value))
                        for _word, live, value in table)
    require(histogram == Counter({(2, "0"): 4, (1, "1"): 4,
                                  (1, "-1"): 4}),
            f"the first Plucker closure boundary changed: {histogram}")
    exported = tuple((word, value) for word, live, value in table
                     if len(live) == 1)
    require(len(exported) == 8 and all(len(set(word)) > 1
                                       for word, _value in exported),
            "the F0 closure stopped exporting eight mixed singletons")
    return support, weights, selected_rows, exported


def audit_cross_completion(base_support, base_weights, exported):
    # On the residual four-set {2,3,4,5}, M0 uses 23|45 and F0 uses
    # 24|35.  The unique third perfect matching is 25|34.
    residual_matchings = tuple(perfect_matchings((2, 3, 4, 5)))
    require(residual_matchings == (
        ((2, 3), (4, 5)),
        ((2, 4), (3, 5)),
        ((2, 5), (3, 4)),
    ), "the residual K4 one-factorization changed")

    support = set(base_support)
    weights = dict(base_weights)
    cross_cells = {
        ((2, 5), (0, 1)): Fraction(1),
        ((2, 5), (2, 0)): Fraction(-1),
        ((3, 4), (0, 2)): Fraction(1),
        ((3, 4), (1, 0)): Fraction(-1),
    }
    support.update(cross_cells)
    weights.update(cross_cells)
    support = frozenset(support)
    require(len(support) == 14,
            "the K4-completed common-q support changed")

    # The 2x2 cross-matching value matrix is the rank-one sign outer product
    # (1,-1)^T(1,-1).  It supplies exactly the negative of every singleton
    # exported by the F0 stage.
    cross_value_matrix = (
        (cross_cells[((2, 5), (0, 1))]
         * cross_cells[((3, 4), (0, 2))],
         cross_cells[((2, 5), (0, 1))]
         * cross_cells[((3, 4), (1, 0))]),
        (cross_cells[((2, 5), (2, 0))]
         * cross_cells[((3, 4), (0, 2))],
         cross_cells[((2, 5), (2, 0))]
         * cross_cells[((3, 4), (1, 0))]),
    )
    require(cross_value_matrix == ((Fraction(1), Fraction(-1)),
                                   (Fraction(-1), Fraction(1))),
            "the cross-completion rank-one sign matrix changed")
    require(cross_value_matrix[0][0] * cross_value_matrix[1][1]
            == cross_value_matrix[0][1] * cross_value_matrix[1][0],
            "the cross-completion Segre minor stopped vanishing")

    completion_rows = []
    for word, old_value in exported:
        cross_term = decorated_term(CROSS, word)
        require(set(cross_term) <= support,
                f"an exported word lost its cross completion: {word}")
        new_value = term_value(cross_term, weights)
        require(new_value == -old_value,
                f"the cross carrier has the wrong sign: {word}")
        completion_rows.append({
            "word": "".join(map(str, word)),
            "old_singleton": str(old_value),
            "cross_carrier": str(new_value),
        })

    table = full_top_table(support, weights)
    histogram = Counter((len(live), str(value))
                        for _word, live, value in table)
    require(histogram == Counter({(2, "0"): 12}),
            f"the complete top-null table changed: {histogram}")
    require(all(len(set(word)) > 1 for word, _live, _value in table),
            "the completed guard acquired a pure top word")

    physical_support = frozenset(cell[0] for cell in support)
    physical_matchings = tuple(matching for matching in MATCHINGS
                               if set(matching) <= physical_support)
    require(physical_matchings == (M0, F0, CROSS),
            f"the common-q physical matching set changed: {physical_matchings}")
    return {
        "cross_physical_matching": [list(edge) for edge in CROSS],
        "cross_pairs_beyond_common_edge": ["25", "34"],
        "cross_cell_value_matrix": [[str(value) for value in row]
                                      for row in cross_value_matrix],
        "cross_segre_rank": 1,
        "completed_export_rows": completion_rows,
        "final_decorated_cells": len(support),
        "final_physical_matchings": len(physical_matchings),
        "final_live_top_words": len(table),
        "final_fibre_histogram": {"two_terms_sum_zero": len(table)},
        "full_top_tensor": 0,
        "one_bad_unary_residual": "q^[3]-X0=-X0",
    }


def main():
    pin_dependency()
    base_support, base_weights, selected_rows, exported = (
        audit_plucker_square()
    )
    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "aligned_F0_plucker_closure": {
            "selected_matching": [list(edge) for edge in M0],
            "aligned_mate_matching": [list(edge) for edge in F0],
            "four_debt_rows": selected_rows,
            "decorated_cells": len(base_support),
            "exported_singletons": len(exported),
            "exported_values": [str(value) for _word, value in exported],
        },
        "cross_K4_completion": audit_cross_completion(
            base_support, base_weights, exported
        ),
        "verdict": (
            "the dense Segre mate cube is exactly feasible in one common q: "
            "F0 cancels the four frozen debts and the unique cross matching "
            "25|34 cancels its eight exports; the result is top-null"
        ),
        "minimal_missing_carrier": (
            "the unary pure top q^[3]=X0, together with the genuine response "
            "rows that distinguish diagonal hole pairs 24|35 from cross "
            "pairs 25|34; no independent cube coefficient remains"
        ),
        "scope": (
            "exact common-q top-row counterguard and K4 carrier theorem; it "
            "does not satisfy the unary top or construct the endpoint stars, "
            "so it is not a one-bad packet or Krenn counterexample"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"Segre-K4 closure ledger changed: {digest}")
    print("N=8 one-bad Segre-cube K4 closure counterguard: PASS")
    print("F0 closes 4 debts; cross 25|34 closes 8 exports; q^[3]=0")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
