#!/usr/bin/env python3
"""Exact opposite-hole and staircase residue-K4 completion obstructions."""

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
    "opposite_non_target_holes": ((6, 7, 0, 1), (6, 7, 1, 0)),
    "staircase_four_holes": (
        (4, 6, 1, 1), (4, 6, 1, 2),
        (4, 6, 2, 0), (4, 6, 2, 1),
    ),
}
EXPECTED_LEDGER_SHA256 = (
    "42deab2d3c700f27fe19d5715800b4a9d508da7f06ad1006dc022a3ccf2bfa7f"
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

    beta, mu = variable("beta"), variable("mu")
    b2 = tuple(D.p_sub(D.p_mul(mu, xi), D.p_mul(beta, yi))
               for xi, yi in zip(x, y))
    d2 = tuple(D.p_sub(D.p_mul(beta, qi), D.p_mul(mu, pi))
               for pi, qi in zip(p, q))
    opposite_pure = matrix_add(outer(b2, t), outer(z, d2))
    expected_opposite = matrix_sub(scalar_matrix(mu, w02),
                                   scalar_matrix(beta, w12))
    require(matrix_equal(opposite_pure, expected_opposite),
            "the opposite-hole pure completion failed")

    # Normal form forced by the four staircase zero slices.
    u = tuple(variable("u%d" % i) for i in range(3))
    v = tuple(variable("v%d" % i) for i in range(3))
    c0, c1, c2, r = (variable(name)
                     for name in ("c0", "c1", "c2", "r"))
    b1 = tuple(D.p_mul(r, entry) for entry in u)
    d1 = tuple(D.p_mul(r, entry) for entry in v)
    c_0 = tuple(D.p_mul(c0, entry) for entry in u)
    e_0 = tuple(D.p_mul(D.p_neg(c0), entry) for entry in v)
    c_1 = tuple(D.p_mul(c1, entry) for entry in u)
    e_1 = tuple(D.p_mul(D.p_neg(c1), entry) for entry in v)
    c_2 = tuple(D.p_mul(c2, entry) for entry in u)
    e_2 = tuple(D.p_mul(D.p_neg(c2), entry) for entry in v)
    staircase_zero_11 = matrix_add(outer(b1, e_1), outer(c_1, d1))
    staircase_zero_12 = matrix_add(outer(b1, e_2), outer(c_2, d1))
    staircase_mixed_10 = matrix_add(outer(b1, e_0), outer(c_0, d1))
    zero = tuple(tuple(D.p_const(0) for _j in range(3)) for _i in range(3))
    require(matrix_equal(staircase_zero_11, zero)
            and matrix_equal(staircase_zero_12, zero)
            and matrix_equal(staircase_mixed_10, zero),
            "the staircase cancellation normal form failed")
    return {
        "w01_sha256": matrix_hash(w01),
        "opposite_pure_sha256": matrix_hash(opposite_pure),
        "staircase_11_sha256": matrix_hash(staircase_zero_11),
        "staircase_12_sha256": matrix_hash(staircase_zero_12),
        "staircase_10_sha256": matrix_hash(staircase_mixed_10),
    }


def support_audit():
    _state, _extras, base_support, admissible, _stats = C.candidate_input()
    out = {}
    for name, holes in INSTANCES.items():
        support = set(admissible) - set(holes)
        require(base_support <= support,
                "%s lost a mandatory cell" % name)
        shadow = C.support_shadow_audit(support)
        opposite_witness = ((4, 5, 0, 0)
                            if name == "opposite_non_target_holes"
                            else (5, 7, 0, 0))
        require(opposite_witness in support
                and not (set(holes) & support),
                "%s support hypotheses changed" % name)
        out[name] = {
            "holes": [list(cell) for cell in holes],
            "localized_cells": len(support),
            "complete_fibres_checked": shadow["fibres_checked"],
        }
    return out


def audit():
    started = monotonic()
    ledger = {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "instances": support_audit(),
        "symbolic": symbolic_audit(),
        "opposite_hole_identity": (
            "all three wedges W01,W02,W12 are multiples of A, and the "
            "pure cross term is mu*W02-beta*W12"
        ),
        "staircase_identity": (
            "four zero slices make the nonzero F10 cross term vanish, "
            "forcing F10*A=0"
        ),
        "hypothesis_strength": (
            "every displayed adjacent column need only be a nonzero vector; "
            "coordinatewise full support is unnecessary"
        ),
        "characteristic_scope": "empty over every field",
        "status": "both residue support families are empty",
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the two-hole completion ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 residue-K4 two-hole completion family: PASS (exact)")
    print("instances:", sorted(ledger["instances"]))
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
