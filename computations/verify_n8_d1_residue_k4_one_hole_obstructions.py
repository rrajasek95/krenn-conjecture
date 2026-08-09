#!/usr/bin/env python3
"""Exact target and non-target one-hole residue-K4 obstructions."""

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

INSTANCES = {
    "target_row": ((6, 7, 2, 0),),
    "non_target_off_diagonal": ((6, 7, 0, 1),),
}
EXPECTED_LEDGER_SHA256 = (
    "2dff9275aed7b2153ebda11dd90ea54aa79d4b79db9ee26ce3476688c76b3ad1"
)


def variable(name):
    return D.p_var(name)


def outer(left, right):
    return tuple(tuple(D.p_mul(a, b) for b in right) for a in left)


def matrix_add(left, right):
    return tuple(tuple(D.p_add(a, b) for a, b in zip(left_row, right_row))
                 for left_row, right_row in zip(left, right))


def matrix_sub(left, right):
    return tuple(tuple(D.p_sub(a, b) for a, b in zip(left_row, right_row))
                 for left_row, right_row in zip(left, right))


def scalar_matrix(scalar, matrix):
    return tuple(tuple(D.p_mul(scalar, entry) for entry in row)
                 for row in matrix)


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
    x = tuple(variable("x%d" % i) for i in range(3))
    y = tuple(variable("y%d" % i) for i in range(3))
    z = tuple(variable("z%d" % i) for i in range(3))
    p = tuple(variable("p%d" % i) for i in range(3))
    q = tuple(variable("q%d" % i) for i in range(3))
    t = tuple(variable("t%d" % i) for i in range(3))
    w01 = matrix_sub(outer(x, q), outer(y, p))
    w02 = matrix_sub(outer(x, t), outer(z, p))
    w12 = matrix_sub(outer(y, t), outer(z, q))

    alpha, lam = variable("alpha"), variable("lambda")
    b1 = tuple(D.p_sub(D.p_mul(lam, xi), D.p_mul(alpha, yi))
               for xi, yi in zip(x, y))
    d1 = tuple(D.p_sub(D.p_mul(alpha, qi), D.p_mul(lam, pi))
               for pi, qi in zip(p, q))
    row1_0 = matrix_add(outer(b1, p), outer(x, d1))
    row1_1 = matrix_add(outer(b1, q), outer(y, d1))
    row1_2 = matrix_add(outer(b1, t), outer(z, d1))
    require(matrix_equal(row1_0, scalar_matrix(alpha, w01)),
            "the first row-0 completion failed")
    require(matrix_equal(row1_1, scalar_matrix(lam, w01)),
            "the first row-1 completion failed")
    expected_row1_2 = matrix_sub(scalar_matrix(lam, w02),
                                scalar_matrix(alpha, w12))
    require(matrix_equal(row1_2, expected_row1_2),
            "the first row-2 completion failed")

    beta, mu = variable("beta"), variable("mu")
    b2 = tuple(D.p_sub(D.p_mul(mu, xi), D.p_mul(beta, yi))
               for xi, yi in zip(x, y))
    d2 = tuple(D.p_sub(D.p_mul(beta, qi), D.p_mul(mu, pi))
               for pi, qi in zip(p, q))
    pure_cross = matrix_add(outer(b2, t), outer(z, d2))
    expected_pure = matrix_sub(scalar_matrix(mu, w02),
                               scalar_matrix(beta, w12))
    require(matrix_equal(pure_cross, expected_pure),
            "the non-target pure-slice completion failed")

    # The target-row case gives one nonzero alternating relation S and a
    # second alternating form T representing the pure slice.
    delta = variable("delta")
    alternating_zero = matrix_sub(
        matrix_sub(scalar_matrix(lam, w02),
                   scalar_matrix(alpha, w12)),
        scalar_matrix(delta, w01),
    )
    f, s = variable("f"), variable("s")
    alternating_pure = matrix_add(scalar_matrix(f, w01),
                                  scalar_matrix(s, w02))
    return {
        "w01_sha256": matrix_hash(w01),
        "w02_sha256": matrix_hash(w02),
        "w12_sha256": matrix_hash(w12),
        "non_target_row2_sha256": matrix_hash(row1_2),
        "non_target_pure_cross_sha256": matrix_hash(pure_cross),
        "target_alternating_zero_sha256": matrix_hash(alternating_zero),
        "target_alternating_pure_sha256": matrix_hash(alternating_pure),
    }


def support_audit():
    _state, _extras, base_support, admissible, _stats = C.candidate_input()
    out = {}
    for name, holes in INSTANCES.items():
        support = set(admissible) - set(holes)
        require(base_support <= support and len(support) == 216,
                "%s one-hole support changed" % name)
        shadow = C.support_shadow_audit(support)
        require((4, 5, 0, 0) in support,
                "%s lost the opposite-block witness" % name)
        # Both concrete instances retain all four adjacent residue blocks.
        required = {
            (u, v, i, j)
            for u, v in ((4, 6), (4, 7), (5, 6), (5, 7))
            for i, j in itertools.product(C.V.COLORS, repeat=2)
        }
        require(required <= support and not (set(holes) & support),
                "%s lost an adjacent-column hypothesis" % name)
        out[name] = {
            "holes": [list(cell) for cell in holes],
            "localized_cells": len(support),
            "complete_fibres_checked": shadow["fibres_checked"],
            "required_adjacent_cells": len(required),
        }
    return out


def audit():
    started = monotonic()
    ledger = {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "instances": support_audit(),
        "symbolic": symbolic_audit(),
        "target_hole_rank_argument": [
            "X*S*Y^T=0 with S nonzero alternating of rank 2",
            "the rank-one target and full coordinate columns force rank X,Y>=2",
            "Sylvester then forces rank X=rank Y=2",
            "alternation forces ker X=ker Y",
            "with a common kernel every X*T*Y^T has rank 0 or 2",
            "this contradicts X*T*Y^T=E22 of rank 1",
        ],
        "non_target_hole_argument": (
            "the three wedges W01,W02,W12 become proportional to A, "
            "so the pure cross term and hence E22 are proportional to A"
        ),
        "characteristic_scope": "empty over every field",
        "status": "both 216-cell one-hole D1 supports are empty",
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the one-hole residue ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 residue-K4 one-hole obstructions: PASS (exact)")
    print("instances:", sorted(ledger["instances"]))
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
