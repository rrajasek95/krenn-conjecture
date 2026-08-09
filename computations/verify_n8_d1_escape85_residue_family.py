#!/usr/bin/env python3
"""Exact residue classification and full-ideal frontier for D1 escape 85."""

from __future__ import annotations

import hashlib
import importlib
import itertools
import os
import sys
from collections import Counter
from fractions import Fraction
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_CANDIDATE_SHA256 = (
    "28b5de217d61dbe41c699657fb7ad3d7f29d0a42521a2e9b99926d135cf8b8ca"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_m10_334_branch63_candidate.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_CANDIDATE_SHA256,
            "the pinned D1 candidate source changed")
C = importlib.import_module("verify_n8_d1_m10_334_branch63_candidate")
D = C.D

MISSING_RESIDUE_CELLS = frozenset({
    (4, 5, 0, 0), (4, 5, 0, 1), (4, 5, 0, 2),
    (4, 5, 1, 0), (4, 5, 1, 1), (4, 5, 2, 0), (4, 5, 2, 1),
    (4, 6, 1, 0),
    (4, 7, 0, 0), (4, 7, 0, 1), (4, 7, 1, 2),
    (5, 6, 0, 0), (5, 6, 0, 1), (5, 6, 0, 2),
    (5, 6, 1, 0), (5, 6, 1, 1), (5, 6, 1, 2),
    (5, 7, 0, 0), (5, 7, 0, 1), (5, 7, 0, 2),
    (5, 7, 1, 0), (5, 7, 1, 1), (5, 7, 1, 2),
    (5, 7, 2, 0), (5, 7, 2, 1),
    (6, 7, 0, 2),
})

EXPECTED_LEDGER_SHA256 = (
    "6ca2649ae88ab8394755fc4ad4f2025c7b4c0a9db8151a5ecd2961ab56bb0c41"
)


def variable(name):
    return D.p_var(name)


def vector_add(left, right):
    return tuple(D.p_add(a, b) for a, b in zip(left, right))


def scalar_vector(scalar, vector):
    return tuple(D.p_mul(scalar, entry) for entry in vector)


def outer(left, right):
    return tuple(tuple(D.p_mul(a, b) for b in right) for a in left)


def matrix_add(left, right):
    return tuple(tuple(D.p_add(a, b) for a, b in zip(left_row, right_row))
                 for left_row, right_row in zip(left, right))


def scalar_matrix(scalar, matrix):
    return tuple(tuple(D.p_mul(scalar, entry) for entry in row)
                 for row in matrix)


def zero_matrix():
    return tuple(tuple(D.p_const(0) for _ in range(3)) for _ in range(3))


def matrix_equal(left, right):
    return all(a == b for left_row, right_row in zip(left, right)
               for a, b in zip(left_row, right_row))


def matrix_hash(matrix):
    return D.content_hash([
        [[[list(monomial), str(coefficient)]
          for monomial, coefficient in sorted(entry.items())]
         for entry in row]
        for row in matrix
    ])


def residue_family_audit():
    """Replay the complete normalized torus family symbolically."""
    zero, one = D.p_const(0), D.p_const(1)
    e = (zero, zero, one)
    ratio, c0 = variable("ratio"), variable("c0")
    d = tuple(variable("d%d" % index) for index in range(3))
    b1, b2 = variable("b1"), variable("b2")
    c10, c11, c22 = (variable(name)
                      for name in ("c10", "c11", "c22"))

    # A12 and E22 are normalized to one by the two independent matching-term
    # edge gauges A->A/A12,F->A12*F and E->E/E22,B->E22*B.
    a = (zero, one, ratio)
    blocks_b = (
        scalar_vector(D.p_neg(c0), d),
        (zero, b1, b2),
        vector_add(
            vector_add((zero, D.p_mul(ratio, b1), D.p_mul(ratio, b2)),
                       scalar_vector(D.p_neg(c22), d)),
            e,
        ),
    )
    blocks_c = (
        scalar_vector(c0, e),
        (c10, c11, zero),
        (D.p_mul(ratio, c10), D.p_mul(ratio, c11), c22),
    )
    residue_d = outer(e, d)
    residue_e = outer(e, e)
    residue_f = scalar_matrix(
        D.p_const(-1),
        matrix_add(outer(blocks_b[1], e), outer(d, blocks_c[1])),
    )

    slices = []
    for colour in range(3):
        value = matrix_add(
            scalar_matrix(a[colour], residue_f),
            matrix_add(outer(blocks_b[colour], e),
                       outer(d, blocks_c[colour])),
        )
        expected = outer(e, e) if colour == 2 else zero_matrix()
        require(matrix_equal(value, expected),
                "the normalized residue family failed at row %d" % colour)
        slices.append(matrix_hash(value))

    return {
        "normalized_parameters": [
            "ratio", "c0", "d0", "d1", "d2",
            "b1", "b2", "c10", "c11", "c22",
        ],
        "normalized_parameter_count": 10,
        "edge_gauges_fixed": ["A45_12=1", "E57_22=1"],
        "A45": "(0,1,ratio) tensor e2",
        "B46_rows": ["-c0*d", "(0,b1,b2)",
                      "ratio*(0,b1,b2)-c22*d+e2"],
        "C47_rows": ["c0*e2", "(c10,c11,0)",
                      "(ratio*c10,ratio*c11,c22)"],
        "D56": "e2 tensor d",
        "E57": "e2 tensor e2",
        "F67": "-((0,b1,b2) tensor e2+d tensor (c10,c11,0))",
        "slice_sha256": slices,
        "D56_sha256": matrix_hash(residue_d),
        "E57_sha256": matrix_hash(residue_e),
        "F67_sha256": matrix_hash(residue_f),
        "open_conditions": [
            "all ten parameters are nonzero",
            "ratio*b1-c22*d1 is nonzero",
            "ratio*b2-c22*d2+1 is nonzero",
        ],
    }


def explicit_residue_point_audit():
    """Check a rational localized point on all 81 residue coefficients."""
    values = {
        (4, 5, 1, 2): 1, (4, 5, 2, 2): 1,
        (4, 6, 0, 0): -1, (4, 6, 0, 1): -1,
        (4, 6, 0, 2): -1, (4, 6, 1, 1): 1,
        (4, 6, 1, 2): 1, (4, 6, 2, 0): -3,
        (4, 6, 2, 1): -2, (4, 6, 2, 2): -1,
        (4, 7, 0, 2): 1, (4, 7, 1, 0): 1,
        (4, 7, 1, 1): 1, (4, 7, 2, 0): 1,
        (4, 7, 2, 1): 1, (4, 7, 2, 2): 3,
        (5, 6, 2, 0): 1, (5, 6, 2, 1): 1,
        (5, 6, 2, 2): 1,
        (5, 7, 2, 2): 1,
        (6, 7, 0, 0): -1, (6, 7, 0, 1): -1,
        (6, 7, 1, 0): -1, (6, 7, 1, 1): -1,
        (6, 7, 1, 2): -1, (6, 7, 2, 0): -1,
        (6, 7, 2, 1): -1, (6, 7, 2, 2): -1,
    }
    residue_support = {
        C.V.cell(u, v, i, j)
        for u, v in itertools.combinations(C.V.RESIDUE, 2)
        for i, j in itertools.product(C.V.COLORS, repeat=2)
        if C.V.cell(u, v, i, j) not in MISSING_RESIDUE_CELLS
    }
    require(set(values) == residue_support and len(values) == 28
            and all(value for value in values.values()),
            "the explicit residue point lost its exact localized support")
    histogram = Counter()
    for colours in itertools.product(C.V.COLORS, repeat=4):
        word = dict(zip(C.V.RESIDUE, colours))
        coefficient = Fraction(0)
        for matching in C.V.MATCHINGS[C.V.RESIDUE]:
            term = Fraction(1)
            for u, v in matching:
                term *= values.get(C.V.cell(u, v, word[u], word[v]), 0)
            coefficient += term
        expected = Fraction(1 if set(colours) == {2} else 0)
        require(coefficient == expected,
                "the rational point failed residue word %s" % (colours,))
        histogram[str(coefficient)] += 1
    require(histogram == {"0": 80, "1": 1},
            "the explicit residue coefficient histogram changed")
    return {
        "localized_coordinates": len(values),
        "point": [[list(cell), value] for cell, value in sorted(values.items())],
        "coefficients_checked": 81,
        "coefficient_histogram": dict(sorted(histogram.items())),
    }


def full_frontier_audit():
    _state, _extras, base_support, admissible, _stats = C.candidate_input()
    support = set(admissible) - set(MISSING_RESIDUE_CELLS)
    require(len(admissible) == 217 and len(support) == 191
            and base_support <= support,
            "the escape-85 maximal support changed")
    shadow = C.support_shadow_audit(support)
    records = C.coefficient_generators(support)
    term_histogram = Counter(len(record["terms"]) for record in records)
    plus_binomials = 0
    all_binomials = 0
    for record in records:
        if len(record["terms"]) != 2:
            continue
        all_binomials += 1
        coefficients = {Fraction(coefficient)
                        for _monomial, coefficient in record["terms"]}
        plus_binomials += coefficients == {Fraction(1)}
    require(len(records) == 7029
            and not any(len(record["terms"]) == 1 for record in records)
            and plus_binomials == 288 and all_binomials == 289,
            "the escape-85 exact generator census changed")
    return {
        "admissible_cells": len(admissible),
        "localized_variables": len(support),
        "missing_residue_cells": [list(cell)
                                  for cell in sorted(MISSING_RESIDUE_CELLS)],
        "complete_fibres_checked": shadow["fibres_checked"],
        "live_matching_histogram": shadow["live_matching_histogram"],
        "coefficient_generators": len(records),
        "single_term_generators": 0,
        "plus_binomials": plus_binomials,
        "all_binomials": all_binomials,
        "term_count_histogram": {
            str(count): multiplicity
            for count, multiplicity in sorted(term_histogram.items())
        },
        "generator_sha256": D.content_hash(records),
    }


def audit():
    started = monotonic()
    ledger = {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "full_frontier": full_frontier_audit(),
        "residue_family": residue_family_audit(),
        "explicit_Q_residue_point": explicit_residue_point_audit(),
        "classification_proof": (
            "All three residue matching terms contain e2 at vertex 5. "
            "After fixing A45_12=E57_22=1, row 0 gives B0=-C02*d; "
            "row 1 gives F=-(B1*e2^T+d*C1^T); the two non-target columns "
            "of row 2 give C2_l=ratio*C1_l, and its target column gives "
            "B2=ratio*B1-C22*d+e2. Conversely these formulas reconstruct "
            "every residue coefficient exactly."
        ),
        "scope": (
            "The residue localized ideal is classified and nonempty over Q. "
            "The 191-variable complete six/eight-site localized ideal is "
            "frozen but remains undecided."
        ),
        "status": (
            "escape 85 survives every residue-only coefficient obstruction; "
            "any closure must use six-site or full-output coupling"
        ),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the escape-85 residue/frontier ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 escape85 residue family: PASS (exact)")
    print("residue point:",
          ledger["explicit_Q_residue_point"]["localized_coordinates"],
          "nonzero coordinates")
    print("full frontier: %d variables, %d generators"
          % (ledger["full_frontier"]["localized_variables"],
             ledger["full_frontier"]["coefficient_generators"]))
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
