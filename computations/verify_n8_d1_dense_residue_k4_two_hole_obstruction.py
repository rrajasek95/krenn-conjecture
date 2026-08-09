#!/usr/bin/env python3
"""Symbolic audit of the dense D1 residue-K4 two-hole obstruction."""

from __future__ import annotations

import hashlib
import importlib
import itertools
import os
import sys
from collections import Counter
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

HOLES = ((6, 7, 2, 0), (6, 7, 2, 1))
EXPECTED_LEDGER_SHA256 = (
    "655afde6d006dca9f4831a48cb849b4cc19ca8c17bf63001a4fb02a53f3a6dbf"
)


def variable(name):
    return D.p_var(name)


def scalar_vector(scalar, vector):
    return tuple(D.p_mul(scalar, entry) for entry in vector)


def vector_add(left, right):
    return tuple(D.p_add(a, b) for a, b in zip(left, right))


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


def zero_matrix():
    return tuple(tuple(D.p_const(0) for _j in range(3)) for _i in range(3))


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
    u = tuple(variable("u%d" % i) for i in range(3))
    v = tuple(variable("v%d" % i) for i in range(3))
    b = tuple(variable("b%d" % i) for i in range(3))
    d = tuple(variable("d%d" % i) for i in range(3))
    w = tuple(variable("w%d" % i) for i in range(3))
    z = tuple(variable("z%d" % i) for i in range(3))
    c0, c1 = variable("c0"), variable("c1")
    r0, r1 = variable("r0"), variable("r1")
    s = variable("s")
    alpha0, alpha1 = variable("alpha0"), variable("alpha1")
    f, lam = variable("f"), variable("lambda")

    a_matrix = matrix_sub(outer(b, v), outer(u, d))
    blocks_b = (
        scalar_vector(r0, b),
        scalar_vector(r1, vector_add(b, scalar_vector(s, u))),
        u,
    )
    blocks_d = (
        scalar_vector(r0, d),
        scalar_vector(r1, vector_add(d, scalar_vector(s, v))),
        v,
    )
    blocks_c = (scalar_vector(c0, u), scalar_vector(c1, u), w)
    blocks_e = (
        scalar_vector(D.p_neg(c0), v),
        scalar_vector(D.p_neg(c1), v),
        z,
    )
    blocks_f = (
        (D.p_mul(r0, c0), D.p_mul(r0, c1), D.p_mul(r0, alpha0)),
        (D.p_mul(r1, c0), D.p_mul(r1, c1), D.p_mul(r1, alpha1)),
        (D.p_const(0), D.p_const(0), f),
    )

    def slice_matrix(k, ell):
        return matrix_add(
            scalar_matrix(blocks_f[k][ell], a_matrix),
            matrix_add(outer(blocks_b[k], blocks_e[ell]),
                       outer(blocks_c[ell], blocks_d[k])),
        )

    automatically_zero = []
    for k, ell in itertools.product(range(3), repeat=2):
        if (k == 2 and ell in (0, 1)) or (k in (0, 1) and ell in (0, 1)):
            require(matrix_equal(slice_matrix(k, ell), zero_matrix()),
                    "a parametrized zero residue slice failed")
            automatically_zero.append((k, ell))

    y0 = matrix_add(
        scalar_matrix(alpha0, a_matrix),
        matrix_add(outer(b, z), outer(w, d)),
    )
    y1 = matrix_add(
        scalar_matrix(alpha1, a_matrix),
        matrix_add(outer(vector_add(b, scalar_vector(s, u)), z),
                   outer(w, vector_add(d, scalar_vector(s, v)))),
    )
    require(matrix_equal(slice_matrix(0, 2), scalar_matrix(r0, y0))
            and matrix_equal(slice_matrix(1, 2), scalar_matrix(r1, y1)),
            "the two remaining mixed-slice factorizations failed")

    pure = matrix_add(
        scalar_matrix(f, a_matrix),
        matrix_add(outer(u, z), outer(w, v)),
    )
    require(matrix_equal(slice_matrix(2, 2), pure),
            "the pure residue slice changed")
    comparison = matrix_sub(y1, y0)
    expected_comparison = matrix_add(
        scalar_matrix(D.p_sub(alpha1, alpha0), a_matrix),
        scalar_matrix(s, matrix_add(outer(u, z), outer(w, v))),
    )
    require(matrix_equal(comparison, expected_comparison),
            "the two mixed slices no longer give the comparison identity")
    comparison_via_pure = matrix_add(
        scalar_matrix(
            D.p_sub(D.p_sub(alpha1, alpha0), D.p_mul(s, f)),
            a_matrix,
        ),
        scalar_matrix(s, pure),
    )
    require(matrix_equal(comparison, comparison_via_pure),
            "the comparison/pure elimination identity failed")

    # Once the hand rank-one lemma gives s=0, alpha0=alpha1=alpha and
    # w=alpha*u+lambda*b, z=-alpha*v-lambda*d, the mixed slice vanishes and
    # the pure slice becomes (f+lambda)A exactly.
    alpha = variable("alpha")
    collapsed_w = vector_add(scalar_vector(alpha, u), scalar_vector(lam, b))
    collapsed_z = vector_add(
        scalar_vector(D.p_neg(alpha), v),
        scalar_vector(D.p_neg(lam), d),
    )
    collapsed_mixed = matrix_add(
        scalar_matrix(alpha, a_matrix),
        matrix_add(outer(b, collapsed_z), outer(collapsed_w, d)),
    )
    collapsed_pure = matrix_add(
        scalar_matrix(f, a_matrix),
        matrix_add(outer(u, collapsed_z), outer(collapsed_w, v)),
    )
    require(matrix_equal(collapsed_mixed, zero_matrix()),
            "the rank-one collapsed mixed slice did not vanish")
    require(matrix_equal(
        collapsed_pure,
        scalar_matrix(D.p_add(f, lam), a_matrix),
    ), "the final pure-slice scalar collapse failed")
    return {
        "automatic_zero_slices": [list(pair) for pair in automatically_zero],
        "A_matrix_sha256": matrix_hash(a_matrix),
        "comparison_sha256": matrix_hash(comparison_via_pure),
        "collapsed_pure_sha256": matrix_hash(collapsed_pure),
    }


def audit():
    started = monotonic()
    _state, _extras, base_support, admissible, _stats = C.candidate_input()
    support = set(admissible) - set(HOLES)
    require(base_support <= support and len(admissible) == 217
            and len(support) == 215,
            "the dense two-hole D1 support changed")
    residue_edges = tuple(itertools.combinations(C.V.RESIDUE, 2))
    expected_complete = set(residue_edges) - {(6, 7)}
    for u, v in residue_edges:
        live_cells = {(i, j) for i, j in itertools.product(C.V.COLORS, repeat=2)
                      if C.V.cell(u, v, i, j) in support}
        if (u, v) in expected_complete:
            require(len(live_cells) == 9,
                    "a supposedly complete residue block changed")
        else:
            require(live_cells == {
                (0, 0), (0, 1), (0, 2),
                (1, 0), (1, 1), (1, 2), (2, 2),
            }, "the two-hole residue block changed")
    shadow = C.support_shadow_audit(support)
    residue_histogram = Counter()
    for values in itertools.product(C.V.COLORS, repeat=4):
        word = dict(zip(C.V.RESIDUE, values))
        live = 0
        for matching in C.V.MATCHINGS[C.V.RESIDUE]:
            live += all(C.V.cell(u, v, word[u], word[v]) in support
                        for u, v in matching)
        residue_histogram[live] += 1
    require(residue_histogram == {2: 18, 3: 63},
            "the dense residue matching-term census changed")
    symbolic = symbolic_audit()
    ledger = {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "admissible_cells": len(admissible),
        "localized_cells": len(support),
        "holes": [list(cell) for cell in HOLES],
        "complete_fibres_checked": shadow["fibres_checked"],
        "residue_term_histogram": {
            str(term_count): count
            for term_count, count in sorted(residue_histogram.items())
        },
        "symbolic": symbolic,
        "rank_one_lemma": (
            "b*q^T+p*d^T=0 with b,d nonzero implies "
            "p=lambda*b and q=-lambda*d"
        ),
        "final_identity": "H_residue=(f+lambda)*A",
        "characteristic_scope": "empty over every field",
        "status": (
            "the 215-cell D1 support is empty already on its four-site "
            "residue subsystem"
        ),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the dense residue obstruction ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 dense residue-K4 two-hole obstruction: PASS (exact)")
    print("localized support:", ledger["localized_cells"], "of",
          ledger["admissible_cells"], "admissible cells")
    print("final identity:", ledger["final_identity"])
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
