#!/usr/bin/env python3
"""Exact residue obstruction when one block is supported on the target cross."""

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
    (6, 7, 0, 0), (6, 7, 0, 1),
    (6, 7, 1, 0), (6, 7, 1, 1),
})
TARGET_CROSS = frozenset({
    (6, 7, 0, 2), (6, 7, 1, 2),
    (6, 7, 2, 0), (6, 7, 2, 1), (6, 7, 2, 2),
})
OFF_TARGET_WITNESS = (4, 5, 0, 0)
MANDATORY = frozenset({
    (0, 1, 0, 0), (0, 2, 0, 1), (0, 2, 2, 2),
    (1, 3, 0, 1), (1, 3, 2, 2), (2, 3, 1, 1),
})
EXPECTED_LEDGER_SHA256 = (
    "f571d7ab7f9ddd6c4d9ea8c845c7510a20bd25fb7be84c89f91ec80e4f8465a7"
)


def var(name):
    return D.p_var(name)


def scale(scalar, vector):
    return tuple(D.p_mul(scalar, entry) for entry in vector)


def vector_add(*vectors):
    out = tuple(D.p_const(0) for _ in range(3))
    for vector in vectors:
        out = tuple(D.p_add(a, b) for a, b in zip(out, vector))
    return out


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
    u = tuple(var("u%d" % index) for index in range(3))
    v = tuple(var("v%d" % index) for index in range(3))
    c2 = tuple(var("c2_%d" % index) for index in range(3))
    e2 = tuple(var("e2_%d" % index) for index in range(3))
    theta = var("theta")
    betas = (var("beta0"), var("beta1"))
    gammas = (var("gamma0"), var("gamma1"))

    # Complete normal form of the four non-target zero slices.
    b = tuple(scale(beta, u) for beta in betas)
    d = tuple(scale(D.p_mul(theta, beta), v) for beta in betas)
    c = tuple(scale(gamma, u) for gamma in gammas)
    e = tuple(scale(D.p_neg(D.p_mul(theta, gamma)), v)
              for gamma in gammas)
    zero = tuple(tuple(D.p_const(0) for _ in range(3)) for _ in range(3))
    zero_slices = []
    for k, ell in itertools.product(range(2), repeat=2):
        value = matrix_add(outer(b[k], e[ell]), outer(c[ell], d[k]))
        require(matrix_equal(value, zero),
                "a non-target corner slice stopped vanishing")
        zero_slices.append(matrix_hash(value))

    S = matrix_add(outer(u, e2),
                   matrix_scale(theta, outer(c2, v)))
    x, y = var("x"), var("y")
    b2 = vector_add(scale(x, u), scale(y, c2))
    d2 = vector_add(scale(D.p_mul(theta, x), v),
                    scale(D.p_neg(y), e2))
    T = matrix_add(matrix_scale(theta, outer(b2, v)),
                   matrix_neg(outer(u, d2)))
    require(matrix_equal(T, matrix_scale(y, S)),
            "the independent-pair target pencil changed")
    pure_cross = matrix_add(outer(b2, e2), outer(c2, d2))
    require(matrix_equal(pure_cross, matrix_scale(x, S)),
            "the independent-pair target slice left the pencil")

    # If c2 lies on u, the mixed pencil and target slice have common left
    # factor u; if e2 lies on v, the transpose statement holds.
    kappa, mu, f22 = var("kappa"), var("mu"), var("F22")
    left_c2, left_b2 = scale(kappa, u), scale(mu, u)
    left_S = matrix_add(outer(u, e2),
                        matrix_scale(theta, outer(left_c2, v)))
    left_target = matrix_add(matrix_scale(f22, left_S),
                             outer(left_b2, e2), outer(left_c2, d2))
    left_factor = vector_add(
        scale(f22, vector_add(e2, scale(D.p_mul(theta, kappa), v))),
        scale(mu, e2), scale(kappa, d2),
    )
    require(matrix_equal(left_target, outer(u, left_factor)),
            "the left-dependent target slice lost its common factor")

    right_e2, right_d2 = scale(kappa, v), scale(mu, v)
    right_S = matrix_add(outer(u, right_e2),
                         matrix_scale(theta, outer(c2, v)))
    right_target = matrix_add(matrix_scale(f22, right_S),
                              outer(b2, right_e2), outer(c2, right_d2))
    right_factor = vector_add(
        scale(D.p_mul(f22, kappa), u),
        scale(D.p_mul(f22, theta), c2),
        scale(kappa, b2), scale(mu, c2),
    )
    require(matrix_equal(right_target, outer(right_factor, v)),
            "the right-dependent target slice lost its common factor")
    return {
        "zero_slice_sha256": zero_slices,
        "S_sha256": matrix_hash(S),
        "T_sha256": matrix_hash(T),
        "independent_target_sha256": matrix_hash(pure_cross),
        "dependent_left_sha256": matrix_hash(left_target),
        "dependent_right_sha256": matrix_hash(right_target),
    }


def support_audit():
    _state, _extras, _base_support, admissible, _stats = C.candidate_input()
    support = frozenset(set(admissible) - set(HOLES))
    require(len(admissible) == 217 and len(support) == 213
            and MANDATORY <= support,
            "the maximal target-cross support changed")
    residue_edges = tuple(itertools.combinations(V.RESIDUE, 2))
    for edge in residue_edges:
        active = {V.cell(*edge, i, j)
                  for i, j in itertools.product(V.COLORS, repeat=2)
                  if V.cell(*edge, i, j) in support}
        expected = ({V.cell(*edge, i, j)
                     for i, j in itertools.product(V.COLORS, repeat=2)}
                    if edge != SPECIAL_EDGE else set(TARGET_CROSS))
        require(active == expected,
                "a residue block in the target-cross orbit changed")

    adjacent_edges = set(residue_edges) - {SPECIAL_EDGE, OPPOSITE_EDGE}
    adjacent_cells = {
        V.cell(*edge, i, j)
        for edge in adjacent_edges
        for i, j in itertools.product(V.COLORS, repeat=2)
    }
    mixed_cross = set(TARGET_CROSS) - {V.cell(*SPECIAL_EDGE, 2, 2)}
    minimal_required = (adjacent_cells | mixed_cross
                        | {OFF_TARGET_WITNESS})
    require(len(adjacent_cells) == 36 and len(mixed_cross) == 4
            and len(minimal_required) == 41
            and minimal_required <= support,
            "the target-cross localized hypotheses changed")
    shadow = C.support_shadow_audit(support)
    return {
        "admissible_cells": len(admissible),
        "maximal_localized_cells": len(support),
        "residue_cells": 50,
        "holes": [list(cell) for cell in sorted(HOLES)],
        "target_cross": [list(cell) for cell in sorted(TARGET_CROSS)],
        "localized_adjacent_cells": len(adjacent_cells),
        "localized_mixed_cross_cells": len(mixed_cross),
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
        "corner_normal_form": (
            "the four zero non-target slices synchronize common full lines "
            "u,v and nonzero row/column scalars; the four mixed target slices "
            "make S=u tensor e2+theta*c2 tensor v and "
            "T=theta*b2 tensor v-u tensor d2 proportional to A"
        ),
        "rank_split": (
            "if (u,c2) and (v,e2) are independent, T proportional to S "
            "gives b2=x*u+y*c2,d2=theta*x*v-y*e2, so the target cross is "
            "x*S; if either pair is dependent, the target slice has a "
            "common full left or right factor"
        ),
        "hypothesis_strength": (
            "four adjacent residue blocks, four mixed target-cross cells, "
            "and one off-target opposite-block witness are localized; all "
            "other cells, including F22 and every boundary cell, are free"
        ),
        "base_ring_scope": (
            "all tensor identities are polynomial over Z; the common-line "
            "normal form and rank split are taken over the fraction field of "
            "a localized integral coefficient domain"
        ),
        "characteristic_scope": "empty over every field",
        "status": "the target-cross residue stratum is empty",
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the target-cross residue ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 residue target-cross holes: PASS (exact)")
    print("holes:", ledger["support"]["holes"])
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
