#!/usr/bin/env python3
"""Exact residue obstruction for three holes in a non-target 2x2 corner."""

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
HOLES = frozenset({
    (6, 7, 0, 1), (6, 7, 1, 0), (6, 7, 1, 1),
})
SURVIVING_DIAGONAL = (6, 7, 0, 0)
OFF_TARGET_WITNESS = (4, 5, 0, 0)
MANDATORY = frozenset({
    (0, 1, 0, 0), (0, 2, 0, 1), (0, 2, 2, 2),
    (1, 3, 0, 1), (1, 3, 2, 2), (2, 3, 1, 1),
})
EXPECTED_LEDGER_SHA256 = (
    "aa735214c4c8604715b07fddcdececde36946448130cf5065c9c896898f12dea"
)


def var(name):
    return D.p_var(name)


def scale(scalar, vector):
    return tuple(D.p_mul(scalar, entry) for entry in vector)


def outer(left, right):
    return tuple(tuple(D.p_mul(a, b) for b in right) for a in left)


def matrix_add(*matrices):
    zero = D.p_const(0)
    out = tuple(tuple(zero for _ in range(3)) for _ in range(3))
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
    r, s = var("r"), var("s")

    # The F01=0 and F10=0 rank-one cancellations, with all four factors
    # nonzero, have these proportionality normal forms.
    b0, d0 = scale(r, c1), scale(D.p_neg(r), e1)
    b1, d1 = scale(s, c0), scale(D.p_neg(s), e0)
    zero = tuple(tuple(D.p_const(0) for _ in range(3)) for _ in range(3))
    slice01 = matrix_add(outer(b0, e1), outer(c1, d0))
    slice10 = matrix_add(outer(b1, e0), outer(c0, d1))
    require(matrix_equal(slice01, zero) and matrix_equal(slice10, zero),
            "the two rank-one cancellations changed")

    wedge = matrix_add(outer(c0, e1), matrix_neg(outer(c1, e0)))
    slice11 = matrix_add(outer(b1, e1), outer(c1, d1))
    cross00 = matrix_add(outer(b0, e0), outer(c0, d0))
    require(matrix_equal(slice11, matrix_scale(s, wedge)),
            "the F11 zero slice stopped being s times the wedge")
    require(matrix_equal(cross00, matrix_scale(D.p_neg(r), wedge)),
            "the F00 cross term stopped being -r times the wedge")

    # Division-free consequence after the proportionality normal form:
    # s*(F00*A+cross00)+r*slice11 = s*F00*A.
    f00 = var("F00")
    A = tuple(tuple(var("A%d%d" % (i, j)) for j in range(3))
              for i in range(3))
    generator00 = matrix_add(matrix_scale(f00, A), cross00)
    certificate_left = matrix_add(matrix_scale(s, generator00),
                                  matrix_scale(r, slice11))
    certificate_right = matrix_scale(D.p_mul(s, f00), A)
    require(matrix_equal(certificate_left, certificate_right),
            "the three-corner unit certificate changed")
    return {
        "slice01_sha256": matrix_hash(slice01),
        "slice10_sha256": matrix_hash(slice10),
        "wedge_sha256": matrix_hash(wedge),
        "slice11_sha256": matrix_hash(slice11),
        "cross00_sha256": matrix_hash(cross00),
        "certificate_sha256": matrix_hash(certificate_left),
    }


def support_audit():
    _state, _extras, _base_support, admissible, _stats = C.candidate_input()
    support = frozenset(set(admissible) - set(HOLES))
    require(len(admissible) == 217 and len(support) == 214
            and MANDATORY <= support,
            "the maximal three-corner-hole support changed")
    residue_edges = tuple(itertools.combinations(V.RESIDUE, 2))
    for edge in residue_edges:
        active = {(i, j) for i, j in itertools.product(V.COLORS, repeat=2)
                  if V.cell(*edge, i, j) in support}
        expected = (set(itertools.product(V.COLORS, repeat=2))
                    if edge != SPECIAL_EDGE else
                    set(itertools.product(V.COLORS, repeat=2))
                    - {(0, 1), (1, 0), (1, 1)})
        require(active == expected,
                "a residue block in the three-corner orbit changed")

    adjacent_edges = set(residue_edges) - {SPECIAL_EDGE, OPPOSITE_EDGE}
    adjacent_cells = {
        V.cell(*edge, i, j)
        for edge in adjacent_edges
        for i, j in itertools.product(V.COLORS, repeat=2)
    }
    minimal_required = (adjacent_cells
                        | {SURVIVING_DIAGONAL, OFF_TARGET_WITNESS})
    require(len(adjacent_cells) == 36 and len(minimal_required) == 38
            and minimal_required <= support,
            "the three-corner localized hypotheses changed")
    shadow = C.support_shadow_audit(support)
    return {
        "admissible_cells": len(admissible),
        "maximal_localized_cells": len(support),
        "residue_cells": 51,
        "holes": [list(cell) for cell in sorted(HOLES)],
        "localized_adjacent_cells": len(adjacent_cells),
        "surviving_diagonal": list(SURVIVING_DIAGONAL),
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
        "normal_form": (
            "F01=0 gives b0=r*c1,d0=-r*e1; F10=0 gives "
            "b1=s*c0,d1=-s*e0. F11=0 is s*W=0, where "
            "W=c0 tensor e1-c1 tensor e0. The F00 cross term is -r*W."
        ),
        "unit_identity": (
            "s*H00+r*H11=s*F00*A; since s,F00 and one off-target "
            "entry of A are localized, the residue ideal is the unit ideal"
        ),
        "hypothesis_strength": (
            "four adjacent residue blocks are required full only as a simple "
            "support-level sufficient condition; cells outside the residue "
            "K4 and all unnamed cells of the special/opposite blocks are free"
        ),
        "base_ring_scope": (
            "the final identity is polynomial over Z after the proportionality "
            "normal form; that form is obtained over the fraction field of "
            "any localized integral coefficient domain"
        ),
        "characteristic_scope": "empty over every field",
        "status": "the three-corner-hole residue stratum is empty",
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the three-corner-hole ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 residue three-corner holes: PASS (exact)")
    print("holes:", ledger["support"]["holes"])
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
