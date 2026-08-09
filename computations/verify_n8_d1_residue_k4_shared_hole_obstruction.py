#!/usr/bin/env python3
"""Exact shared-hole residue-K4 obstruction on a dense D1 support."""

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
D = C.D

INSTANCE_HOLES = (
    (4, 5, 2, 2),
    (6, 7, 0, 1),
    (6, 7, 1, 0),
    (6, 7, 2, 0),
)
EXPECTED_LEDGER_SHA256 = (
    "f88dac24787832ca8c5d561efa5a3206f6b70442d33532e7723ae29df5bccfdb"
)


def variable(name):
    return D.p_var(name)


def scalar_vector(scalar, vector):
    return tuple(D.p_mul(scalar, entry) for entry in vector)


def matrix_add(left, right):
    return tuple(tuple(D.p_add(a, b) for a, b in zip(left_row, right_row))
                 for left_row, right_row in zip(left, right))


def matrix_sub(left, right):
    return tuple(tuple(D.p_sub(a, b) for a, b in zip(left_row, right_row))
                 for left_row, right_row in zip(left, right))


def scalar_matrix(scalar, matrix):
    return tuple(tuple(D.p_mul(scalar, entry) for entry in row)
                 for row in matrix)


def outer(left, right):
    return tuple(tuple(D.p_mul(a, b) for b in right) for a in left)


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
    a_matrix = tuple(tuple(variable("A%d%d" % (i, j)) for j in range(3))
                     for i in range(3))
    u = tuple(variable("u%d" % i) for i in range(3))
    v = tuple(variable("v%d" % i) for i in range(3))
    w = tuple(variable("w%d" % i) for i in range(3))
    z = tuple(variable("z%d" % i) for i in range(3))
    r, alpha, f = variable("r"), variable("alpha"), variable("f")
    cross = matrix_add(outer(u, z), outer(w, v))
    normalized_mixed = matrix_add(scalar_matrix(alpha, a_matrix), cross)
    mixed = scalar_matrix(r, normalized_mixed)
    direct_mixed = matrix_add(
        scalar_matrix(D.p_mul(r, alpha), a_matrix),
        matrix_add(outer(scalar_vector(r, u), z),
                   outer(w, scalar_vector(r, v))),
    )
    require(matrix_equal(mixed, direct_mixed),
            "the proportional mixed-slice factorization failed")
    pure = matrix_add(scalar_matrix(f, a_matrix), cross)
    comparison = matrix_sub(pure, normalized_mixed)
    expected = scalar_matrix(D.p_sub(f, alpha), a_matrix)
    require(matrix_equal(comparison, expected),
            "the shared-hole pure/mixed comparison failed")
    return {
        "cross_sha256": matrix_hash(cross),
        "mixed_sha256": matrix_hash(mixed),
        "pure_minus_normalized_mixed_sha256": matrix_hash(comparison),
    }


def audit():
    started = monotonic()
    _state, _extras, base_support, admissible, _stats = C.candidate_input()
    support = set(admissible) - set(INSTANCE_HOLES)
    require(base_support <= support and len(support) == 213,
            "the shared-hole dense support changed")
    shadow = C.support_shadow_audit(support)

    # Full support of A=A45 is unnecessary.  The final identity only needs
    # one non-target witness, here A00.  The shared non-target column is l=0
    # of F=A67, with k=1 and target row 2.
    required = {(4, 5, 0, 0)}
    required.update((4, 6, i, k) for i in C.V.COLORS for k in (1, 2))
    required.update((5, 6, i, k) for i in C.V.COLORS for k in (1, 2))
    required.update((4, 7, i, ell) for i in C.V.COLORS for ell in (0, 2))
    required.update((5, 7, i, ell) for i in C.V.COLORS for ell in (0, 2))
    required.update({(6, 7, 1, 2), (6, 7, 2, 2)})
    shared_holes = {(6, 7, 1, 0), (6, 7, 2, 0)}
    require(required <= support and not (shared_holes & support),
            "the shared-hole support hypotheses changed")
    symbolic = symbolic_audit()
    ledger = {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "localized_cells": len(support),
        "instance_holes": [list(cell) for cell in INSTANCE_HOLES],
        "shared_holes": [list(cell) for cell in sorted(shared_holes)],
        "required_nonzero_cells": len(required),
        "complete_fibres_checked": shadow["fibres_checked"],
        "symbolic": symbolic,
        "rank_one_lemma": (
            "x*y^T+z*w^T=0 with all four vectors nonzero implies "
            "the two left and two right factors are pairwise proportional"
        ),
        "final_identity": "E22=(F22-F12/r)*A45",
        "opposite_block_hypothesis": (
            "one nonzero entry of A45 outside its (2,2) target coordinate"
        ),
        "symmetry_scope": (
            "any residue edge, endpoint orientation, and pair consisting "
            "of the target row/column and one non-target row/column"
        ),
        "characteristic_scope": "empty over every field",
        "status": (
            "the 214-cell D1 support is empty by the shared-hole "
            "four-site residue obstruction"
        ),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the shared-hole residue ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 residue-K4 shared-hole obstruction: PASS (exact)")
    print("localized support:", ledger["localized_cells"])
    print("final identity:", ledger["final_identity"])
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
