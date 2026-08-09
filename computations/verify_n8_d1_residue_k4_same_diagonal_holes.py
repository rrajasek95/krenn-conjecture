#!/usr/bin/env python3
"""Exact residue obstruction for two same-diagonal non-target holes."""

from __future__ import annotations

import hashlib
import importlib
import itertools
import os
import sys
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
D, V = C.D, C.V

SPECIAL_EDGE = (6, 7)
OPPOSITE_EDGE = (4, 5)
HOLES = frozenset({(6, 7, 0, 0), (6, 7, 1, 1)})
OPPOSITE_HOLES = frozenset({(4, 5, 0, 0), (4, 5, 1, 1)})
OFF_TARGET_WITNESS = (4, 5, 0, 1)
MANDATORY = frozenset({
    (0, 1, 0, 0), (0, 2, 0, 1), (0, 2, 2, 2),
    (1, 3, 0, 1), (1, 3, 2, 2), (2, 3, 1, 1),
})
EXPECTED_LEDGER_SHA256 = (
    "983d9b8c9e8d91d7ef843cc6780c23c8a782959e37849185766ab89d159de58f"
)


def var(name):
    return D.p_var(name)


def scale(scalar, vector):
    return tuple(D.p_mul(scalar, entry) for entry in vector)


def vector_add(*vectors):
    out = tuple(D.p_const(0) for _ in range(3))
    for vector in vectors:
        out = tuple(D.p_add(left, right)
                    for left, right in zip(out, vector))
    return out


def outer(left, right):
    return tuple(tuple(D.p_mul(a, b) for b in right) for a in left)


def matrix_add(*matrices):
    out = tuple(tuple(D.p_const(0) for _ in range(3)) for _ in range(3))
    for matrix in matrices:
        out = tuple(tuple(D.p_add(a, b) for a, b in zip(left, right))
                    for left, right in zip(out, matrix))
    return out


def matrix_scale(scalar, matrix):
    return tuple(tuple(D.p_mul(scalar, entry) for entry in row)
                 for row in matrix)


def matrix_neg(matrix):
    return matrix_scale(D.p_const(-1), matrix)


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


def symbolic_audit():
    c0 = tuple(var("c0_%d" % index) for index in range(3))
    c1 = tuple(var("c1_%d" % index) for index in range(3))
    e0 = tuple(var("e0_%d" % index) for index in range(3))
    e1 = tuple(var("e1_%d" % index) for index in range(3))
    alpha, beta = var("alpha"), var("beta")
    b0, d0 = scale(alpha, c0), scale(D.p_neg(alpha), e0)
    b1, d1 = scale(beta, c1), scale(D.p_neg(beta), e1)
    zero00 = matrix_add(outer(b0, e0), outer(c0, d0))
    zero11 = matrix_add(outer(b1, e1), outer(c1, d1))
    zero = tuple(tuple(D.p_const(0) for _ in range(3)) for _ in range(3))
    require(matrix_equal(zero00, zero) and matrix_equal(zero11, zero),
            "the two diagonal rank-one cancellations changed")

    W01 = matrix_add(outer(c0, e1), matrix_neg(outer(c1, e0)))
    p, q, f, g = (var(name) for name in ("p", "q", "f", "g"))
    c2 = vector_add(scale(p, c0), scale(q, c1))
    e2 = vector_add(scale(p, e0), scale(q, e1))
    W02 = matrix_add(outer(c0, e2), matrix_neg(outer(c2, e0)))
    W12 = matrix_add(outer(c1, e2), matrix_neg(outer(c2, e1)))
    require(matrix_equal(W02, matrix_scale(q, W01))
            and matrix_equal(W12, matrix_scale(D.p_neg(p), W01)),
            "the rank-two same-coefficient wedge parametrization changed")

    b2 = vector_add(scale(D.p_neg(g), c0), scale(f, c1))
    d2 = vector_add(scale(g, e0), scale(D.p_neg(f), e1))
    cross20 = matrix_add(outer(b2, e0), outer(c0, d2))
    cross21 = matrix_add(outer(b2, e1), outer(c1, d2))
    require(matrix_equal(cross20, matrix_scale(D.p_neg(f), W01))
            and matrix_equal(cross21, matrix_scale(D.p_neg(g), W01)),
            "the second rank-two wedge parametrization changed")
    pure_cross = matrix_add(outer(b2, e2), outer(c2, d2))
    scalar = D.p_neg(D.p_add(D.p_mul(f, p), D.p_mul(g, q)))
    require(matrix_equal(pure_cross, matrix_scale(scalar, W01)),
            "the rank-two target slice failed to collapse onto A")

    # Rank-one left-dependent branch: c1=kappa*c0.  The proportional wedge
    # equations force c2=lambda*c0, and H20 forces b2=mu*c0.  Every term in
    # H22 then has the same full-support left factor c0.
    kappa, lam, mu = (var(name) for name in ("kappa", "lambda", "mu"))
    left_c1 = scale(kappa, c0)
    left_c2 = scale(lam, c0)
    left_b2 = scale(mu, c0)
    left_W01 = matrix_add(outer(c0, e1),
                          matrix_neg(outer(left_c1, e0)))
    left_pure = matrix_add(
        matrix_scale(var("F22"), left_W01),
        outer(left_b2, e2), outer(left_c2, d2),
    )
    left_factor = vector_add(
        scale(var("F22"), vector_add(e1, scale(D.p_neg(kappa), e0))),
        scale(mu, e2), scale(lam, d2),
    )
    require(matrix_equal(left_pure, outer(c0, left_factor)),
            "the left-dependent pure slice lost its common factor")

    # The right-dependent branch is the transpose-symmetric statement.
    right_e1 = scale(kappa, e0)
    right_e2 = scale(lam, e0)
    right_d2 = scale(mu, e0)
    right_W01 = matrix_add(outer(c0, right_e1),
                           matrix_neg(outer(c1, e0)))
    right_pure = matrix_add(
        matrix_scale(var("G22"), right_W01),
        outer(b2, right_e2), outer(c2, right_d2),
    )
    right_factor = vector_add(
        scale(var("G22"), vector_add(scale(kappa, c0),
                                     scale(D.p_const(-1), c1))),
        scale(lam, b2), scale(mu, c2),
    )
    require(matrix_equal(right_pure, outer(right_factor, e0)),
            "the right-dependent pure slice lost its common factor")
    return {
        "zero00_sha256": matrix_hash(zero00),
        "zero11_sha256": matrix_hash(zero11),
        "W01_sha256": matrix_hash(W01),
        "rank_two_pure_cross_sha256": matrix_hash(pure_cross),
        "rank_one_left_sha256": matrix_hash(left_pure),
        "rank_one_right_sha256": matrix_hash(right_pure),
    }


def support_audit():
    _state, _extras, _base_support, admissible, _stats = C.candidate_input()
    single_support = frozenset(set(admissible) - set(HOLES))
    opposite_support = frozenset(
        set(admissible) - set(HOLES | OPPOSITE_HOLES)
    )
    require(len(admissible) == 217 and len(single_support) == 215
            and len(opposite_support) == 213
            and MANDATORY <= opposite_support,
            "the maximal same-diagonal-hole supports changed")
    residue_edges = tuple(itertools.combinations(V.RESIDUE, 2))
    for edge in residue_edges:
        active = {(i, j) for i, j in itertools.product(V.COLORS, repeat=2)
                  if V.cell(*edge, i, j) in opposite_support}
        expected = (set(itertools.product(V.COLORS, repeat=2))
                    if edge not in (SPECIAL_EDGE, OPPOSITE_EDGE) else
                    set(itertools.product(V.COLORS, repeat=2))
                    - {(0, 0), (1, 1)})
        require(active == expected,
                "a residue block in the opposite-double-hole orbit changed")
    shadow = C.support_shadow_audit(opposite_support)

    adjacent_edges = set(residue_edges) - {SPECIAL_EDGE, OPPOSITE_EDGE}
    localized_adjacent = {
        V.cell(*edge, i, j)
        for edge in adjacent_edges
        for i, j in itertools.product(V.COLORS, repeat=2)
    }
    localized_special = {
        V.cell(*SPECIAL_EDGE, i, j)
        for i, j in ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1))
    }
    minimal_required = (localized_adjacent | localized_special
                        | {OFF_TARGET_WITNESS})
    require(len(localized_adjacent) == 36
            and len(localized_special) == 6
            and len(minimal_required) == 43
            and minimal_required <= opposite_support,
            "the weakened same-diagonal hypotheses changed")
    return {
        "admissible_cells": len(admissible),
        "single_hole_pair_maximal_cells": len(single_support),
        "opposite_double_hole_maximal_cells": len(opposite_support),
        "special_holes": [list(cell) for cell in sorted(HOLES)],
        "opposite_holes_allowed": [list(cell)
                                   for cell in sorted(OPPOSITE_HOLES)],
        "localized_adjacent_cells": len(localized_adjacent),
        "localized_special_mixed_cells": len(localized_special),
        "off_target_opposite_witness": list(OFF_TARGET_WITNESS),
        "minimal_required_cells": len(minimal_required),
        "complete_fibres_checked": shadow["fibres_checked"],
    }


def audit():
    started = monotonic()
    ledger = {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "support": support_audit(),
        "symbolic": symbolic_audit(),
        "rank_two_branch": (
            "F00=F11=0 gives b0=alpha*c0,d0=-alpha*e0 and "
            "b1=beta*c1,d1=-beta*e1. The three Wkl are proportional "
            "to the full block A. If W01 has rank two, write "
            "c2=p*c0+q*c1,e2=p*e0+q*e1 and "
            "b2=-g*c0+f*c1,d2=g*e0-f*e1. Then the target cross term "
            "is -(f*p+g*q)*W01, so H22 is a scalar multiple of full A."
        ),
        "rank_one_branch": (
            "F01,alpha,A nonzero force W01 nonzero. If W01 has rank one, "
            "either c0,c1 or e0,e1 are proportional. Proportionality of "
            "W02,W12 and one remaining slice then gives a common full left "
            "or right factor for H22, impossible for the coordinate target."
        ),
        "rank_one_tensor_lemma": (
            "A nonzero difference x tensor y-u tensor v has rank at most "
            "one only if x,u or y,v are linearly dependent."
        ),
        "hypothesis_strength": (
            "only 43 residue cells are required nonzero: four full adjacent "
            "blocks, the six mixed non-target entries of the special block, "
            "and one off-target entry of the opposite block; all other "
            "cells, including the opposite diagonal pair, are arbitrary"
        ),
        "base_ring_scope": (
            "division-free tensor identities over Z; proportionality and "
            "rank splits are applied only after passage from a localized "
            "integral domain to its fraction field"
        ),
        "characteristic_scope": "empty over every field",
        "status": (
            "the weakened same-diagonal two-hole residue stratum, including "
            "the opposite-double-hole orbit, is empty"
        ),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the same-diagonal two-hole ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 residue same-diagonal holes: PASS (exact)")
    print("special holes:", ledger["support"]["special_holes"])
    print("opposite holes allowed:",
          ledger["support"]["opposite_holes_allowed"])
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
