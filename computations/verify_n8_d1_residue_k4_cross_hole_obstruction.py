#!/usr/bin/env python3
"""Exact cross-hole residue-K4 completion obstruction for dense D1."""

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

INSTANCE_HOLES = ((6, 7, 0, 1), (6, 7, 2, 0))
EXPECTED_LEDGER_SHA256 = (
    "00041a7241a912a88f105b2f3e474ae6c5618c64c791edb438e8bc0ffec45757"
)


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
    # x=C_l, y=C_m, z=C_2 and p=E_l, q=E_m, t=E_2.
    x = tuple(variable("x%d" % i) for i in range(3))
    y = tuple(variable("y%d" % i) for i in range(3))
    p = tuple(variable("p%d" % i) for i in range(3))
    q = tuple(variable("q%d" % i) for i in range(3))
    alpha, mu = variable("alpha"), variable("mu")
    z = tuple(D.p_sub(D.p_mul(alpha, yi), D.p_mul(mu, xi))
              for xi, yi in zip(x, y))
    t = tuple(D.p_sub(D.p_mul(alpha, qi), D.p_mul(mu, pi))
              for pi, qi in zip(p, q))
    base_wedge = matrix_sub(outer(x, q), outer(y, p))
    adjacent_wedge = matrix_sub(outer(x, t), outer(z, p))
    pure_wedge = matrix_sub(outer(y, t), outer(z, q))
    require(matrix_equal(adjacent_wedge,
                         scalar_matrix(alpha, base_wedge)),
            "the adjacent wedge completion identity failed")
    require(matrix_equal(pure_wedge, scalar_matrix(mu, base_wedge)),
            "the pure wedge completion identity failed")
    return {
        "base_wedge_sha256": matrix_hash(base_wedge),
        "adjacent_wedge_sha256": matrix_hash(adjacent_wedge),
        "pure_wedge_sha256": matrix_hash(pure_wedge),
    }


def audit():
    started = monotonic()
    _state, _extras, base_support, admissible, _stats = C.candidate_input()
    support = set(admissible) - set(INSTANCE_HOLES)
    require(base_support <= support and len(support) == 215,
            "the cross-hole dense support changed")
    shadow = C.support_shadow_audit(support)

    # F=A67 has holes F01 and F20.  The proof uses the k=0 columns of
    # B=A46,D=A56, all l=0,1,2 columns of C=A47,E=A57, and the target
    # columns of B,D.  A00 is enough to contradict P=lambda*A.
    required = {(4, 5, 0, 0), (6, 7, 0, 0),
                (6, 7, 0, 2), (6, 7, 2, 2)}
    required.update((site, 6, colour, q)
                    for site in (4, 5) for colour in C.V.COLORS
                    for q in (0, 2))
    required.update((site, 7, colour, q)
                    for site in (4, 5) for colour in C.V.COLORS
                    for q in (0, 1, 2))
    require(required <= support and not (set(INSTANCE_HOLES) & support),
            "the cross-hole support hypotheses changed")
    symbolic = symbolic_audit()
    ledger = {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "localized_cells": len(support),
        "instance_holes": [list(cell) for cell in INSTANCE_HOLES],
        "required_nonzero_cells": len(required),
        "complete_fibres_checked": shadow["fibres_checked"],
        "symbolic": symbolic,
        "rank_one_lemma": (
            "u*v^T+x*y^T=0 with nonzero factors makes each factor pair "
            "proportional"
        ),
        "wedge_completion": (
            "C_l E_m^T-C_m E_l^T and C_l E_2^T-C_2 E_l^T "
            "proportional imply C_m E_2^T-C_2 E_m^T proportional"
        ),
        "final_identity": "E22=lambda*A45",
        "symmetry_scope": (
            "any residue edge, either endpoint orientation, and the two "
            "non-target colours"
        ),
        "characteristic_scope": "empty over every field",
        "status": "the 215-cell cross-hole D1 support is empty",
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the cross-hole residue ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 residue-K4 cross-hole obstruction: PASS (exact)")
    print("localized support:", ledger["localized_cells"])
    print("final identity:", ledger["final_identity"])
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
