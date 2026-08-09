#!/usr/bin/env python3
"""Exact permutation-transversal residue-K4 completion obstruction."""

from __future__ import annotations

import hashlib
import importlib
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_CANDIDATE_SHA256 = (
    "28b5de217d61dbe41c699657fb7ad3d7f29d0a42521a2e9b99926d135cf8b8ca"
)
EXPECTED_LEDGER_SHA256 = (
    "e5ab2f91ddf7f18a2d957d5133d66f3c82f52eb1b357413f44f5736162843c3b"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_m10_334_branch63_candidate.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_CANDIDATE_SHA256,
            "the pinned D1 candidate source changed")
C = importlib.import_module("verify_n8_d1_m10_334_branch63_candidate")
D = C.D

SPECIAL_EDGE = (5, 6)
PERMUTATION = (2, 0, 1)
HOLES = tuple(C.V.cell(*SPECIAL_EDGE, k, PERMUTATION[k])
              for k in C.V.COLORS)


def variable(name):
    return D.p_var(name)


def outer(left, right):
    return tuple(tuple(D.p_mul(a, b) for b in right) for a in left)


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
    c = [tuple(variable("c%d%d" % (i, j)) for j in range(3))
         for i in range(3)]
    e = [tuple(variable("e%d%d" % (i, j)) for j in range(3))
         for i in range(3)]
    scalars = [variable("s%d" % i) for i in range(3)]
    wedges = {
        (i, j): matrix_sub(outer(c[i], e[j]), outer(c[j], e[i]))
        for i, j in itertools.combinations(range(3), 2)
    }

    slice_hashes = {}
    pairs_seen = set()
    for k in range(3):
        pivot = PERMUTATION[k]
        b_k = tuple(D.p_mul(scalars[k], entry) for entry in c[pivot])
        d_k = tuple(D.p_neg(D.p_mul(scalars[k], entry))
                    for entry in e[pivot])
        for ell in range(3):
            cross = tuple(tuple(D.p_add(left, right)
                                for left, right in zip(left_row, right_row))
                          for left_row, right_row in
                          zip(outer(b_k, e[ell]), outer(c[ell], d_k)))
            if ell == pivot:
                zero = tuple(tuple(D.p_const(0) for _j in range(3))
                             for _i in range(3))
                require(matrix_equal(cross, zero),
                        "a transversal zero slice failed")
                continue
            pair = tuple(sorted((pivot, ell)))
            sign = 1 if pivot < ell else -1
            expected = scalar_matrix(
                scalars[k] if sign == 1 else D.p_neg(scalars[k]),
                wedges[pair],
            )
            require(matrix_equal(cross, expected),
                    "a permutation-transversal wedge slice failed")
            pairs_seen.add(pair)
            slice_hashes["%d%d" % (k, ell)] = matrix_hash(cross)
    require(pairs_seen == {(0, 1), (0, 2), (1, 2)},
            "the transversal did not expose all three wedges")
    require("22" in slice_hashes,
            "the pure cross wedge was not audited")
    return {
        "permutation": list(PERMUTATION),
        "wedge_pairs_seen": [list(pair) for pair in sorted(pairs_seen)],
        "slice_hashes": slice_hashes,
    }


def support_audit():
    _state, _extras, base_support, admissible, _stats = C.candidate_input()
    support = set(admissible) - set(HOLES)
    require(base_support <= support and len(support) == 214,
            "the permutation-transversal representative changed")
    shadow = C.support_shadow_audit(support)
    require((4, 7, 0, 0) in support and not (set(HOLES) & support),
            "the opposite witness or transversal holes changed")
    return {
        "holes": [list(cell) for cell in HOLES],
        "localized_cells": len(support),
        "complete_fibres_checked": shadow["fibres_checked"],
    }


def audit():
    ledger = {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "support": support_audit(),
        "symbolic": symbolic_audit(),
        "theorem": (
            "If one residue edge has holes F_k,pi(k) for a color "
            "permutation pi with pi(2)!=2, and the adjacent vectors are "
            "nonzero, all three wedges lie on the opposite-block A-line; "
            "the pure cross wedge does too, contradicting any non-target "
            "entry of A."
        ),
        "hypothesis_strength": (
            "Adjacent columns need only be nonzero vectors; cells outside "
            "the residue K4 are irrelevant."
        ),
        "characteristic_scope": "every field",
        "status": "the permutation-transversal residue family is empty",
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the permutation-transversal ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("n8 D1 residue-K4 permutation transversal: PASS (exact)")
    print("holes:", ledger["support"]["holes"])
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
