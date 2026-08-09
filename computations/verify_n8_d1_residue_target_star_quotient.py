#!/usr/bin/env python3
"""Division-free target-star quotient obstruction and the residue-31 frontier."""

from __future__ import annotations

from collections import Counter
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

EXPECTED_LEDGER_SHA256 = (
    "3f9188ea1e6e7b9ae5b80ca15c8e3005c13bf371b7be61087a8b8d84d0466f9f"
)
MANDATORY = frozenset({
    (0, 1, 0, 0), (0, 2, 0, 1), (0, 2, 2, 2),
    (1, 3, 0, 1), (1, 3, 2, 2), (2, 3, 1, 1),
})
RESIDUE_ACTIVE = {
    (4, 5): {(0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2)},
    (4, 6): {(0, 2), (1, 2), (2, 2)},
    (4, 7): {(0, 0), (0, 1), (0, 2), (1, 1), (1, 2),
             (2, 0), (2, 1), (2, 2)},
    (5, 6): {(0, 2), (1, 2), (2, 2)},
    (5, 7): set(itertools.product(range(3), repeat=2)),
    (6, 7): {(2, 0), (2, 2)},
}
TARGET_STAR_WITNESSES = frozenset({
    (4, 6, 0, 2), (5, 6, 0, 2), (6, 7, 2, 0),
})


def var(name):
    return D.p_var(name)


def dot(left, right):
    out = D.p_const(0)
    for a, b in zip(left, right):
        out = D.p_add(out, D.p_mul(a, b))
    return out


def matrix_bilinear(left, matrix, right):
    out = D.p_const(0)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out = D.p_add(out, D.p_mul(D.p_mul(a, matrix[i][j]), b))
    return out


def polynomial_hash(polynomial):
    return D.content_hash([
        [list(monomial), str(coefficient)]
        for monomial, coefficient in sorted(polynomial.items())
    ])


def symbolic_quotient_audit():
    b = tuple(var("b%d" % index) for index in range(3))
    d = tuple(var("d%d" % index) for index in range(3))
    f = tuple(var("f%d" % index) for index in range(3))
    A = tuple(tuple(var("A%d%d" % (i, j)) for j in range(3))
              for i in range(3))
    E = tuple(tuple(var("E%d%d" % (i, j)) for j in range(3))
              for i in range(3))
    G = tuple(tuple(var("G%d%d" % (i, j)) for j in range(3))
              for i in range(3))

    # Integral covectors killing each incident target vector while evaluating
    # to its localized colour-0 coordinate on the target vector e2.
    zero = D.p_const(0)
    qb = (D.p_neg(b[2]), zero, b[0])
    qd = (D.p_neg(d[2]), zero, d[0])
    qf = (D.p_neg(f[2]), zero, f[0])
    target = (zero, zero, D.p_const(1))
    require(not dot(qb, b) and not dot(qd, d) and not dot(qf, f),
            "a target-star quotient covector stopped killing its line")

    # Contract A tensor f + b tensor E + G tensor d.  Each matching term has
    # one of the three killed incident factors.
    term_af = D.p_mul(matrix_bilinear(qb, A, qd), dot(qf, f))
    term_be = D.p_mul(dot(qb, b), matrix_bilinear(qd, E, qf))
    term_gd = D.p_mul(matrix_bilinear(qb, G, qf), dot(qd, d))
    contracted_left = D.p_add(D.p_add(term_af, term_be), term_gd)
    contracted_target = D.p_mul(
        D.p_mul(dot(qb, target), dot(qd, target)), dot(qf, target)
    )
    expected_target = D.p_mul(D.p_mul(b[0], d[0]), f[0])
    require(not contracted_left and contracted_target == expected_target,
            "the target-star contracted equation changed")
    return {
        "contracted_left_sha256": polynomial_hash(contracted_left),
        "contracted_target_sha256": polynomial_hash(contracted_target),
        "localized_rhs_monomial": "b0*d0*f0",
        "covectors": ["(-b2,0,b0)", "(-d2,0,d0)", "(-f2,0,f0)"],
    }


def projection_profile(residue_support):
    profile = {}
    for center in V.RESIDUE:
        neighbours = {}
        for neighbour in V.RESIDUE:
            if neighbour == center:
                continue
            rows = []
            for source_colour in (0, 1):
                rows.append([
                    target_colour for target_colour in V.COLORS
                    if V.cell(center, neighbour, source_colour,
                              target_colour) in residue_support
                ])
            if rows[0] and rows[1] and rows[0] != rows[1]:
                support_rank = "forced-rank-2"
            elif rows[0] == rows[1]:
                support_rank = "rank-at-most-1"
            else:
                support_rank = "projection-degenerate"
            neighbours[str(neighbour)] = {
                "row_supports": rows,
                "support_rank": support_rank,
            }
        profile[str(center)] = neighbours
    require(all(not item["row_supports"][0]
                and not item["row_supports"][1]
                for item in profile["6"].values()),
            "the completely blocked non-target star at vertex 6 changed")
    return profile


def support_audit():
    _state, _extras, _base_support, admissible, _stats = C.candidate_input()
    residue_cells = {
        V.cell(*edge, i, j)
        for edge in itertools.combinations(V.RESIDUE, 2)
        for i, j in itertools.product(V.COLORS, repeat=2)
    }
    residue_support = {
        V.cell(*edge, i, j)
        for edge, pairs in RESIDUE_ACTIVE.items()
        for i, j in pairs
    }
    holes = residue_cells - residue_support
    support = frozenset(set(admissible) - holes)
    require(len(residue_support) == 31 and len(holes) == 23
            and len(admissible) == 217 and len(support) == 194
            and MANDATORY <= support and TARGET_STAR_WITNESSES <= support,
            "the maximal residue-31 frontier changed")
    for edge, expected in RESIDUE_ACTIVE.items():
        actual = {(i, j) for i, j in itertools.product(V.COLORS, repeat=2)
                  if V.cell(*edge, i, j) in residue_support}
        require(actual == expected,
                "a block of the residue-31 frontier changed")
    shadow = C.support_shadow_audit(support)
    records = C.coefficient_generators(support)
    term_histogram = Counter(len(record["terms"]) for record in records)
    require(len(records) == 7237 and not term_histogram[1]
            and term_histogram[2] == 289
            and D.content_hash(records)
            == "81ce07753287eb2c13138f9c8ecf8f1131c7623600b357d35327b2f061c1c647",
            "the maximal residue-31 coefficient input changed")
    return {
        "admissible_cells": len(admissible),
        "maximal_localized_cells": len(support),
        "residue_cells": len(residue_support),
        "residue_holes": [list(cell) for cell in sorted(holes)],
        "residue_blocks": {
            "%d%d" % edge: [list(pair) for pair in sorted(pairs)]
            for edge, pairs in sorted(RESIDUE_ACTIVE.items())
        },
        "target_star_witnesses": [list(cell)
                                  for cell in sorted(TARGET_STAR_WITNESSES)],
        "complete_fibres_checked": shadow["fibres_checked"],
        "coefficient_generators": len(records),
        "single_term_generators": term_histogram[1],
        "binomial_generators": term_histogram[2],
        "generator_sha256": D.content_hash(records),
        "non_target_projection_profile": projection_profile(residue_support),
    }


def audit():
    started = monotonic()
    ledger = {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "support": support_audit(),
        "symbolic": symbolic_quotient_audit(),
        "target_star_lemma": (
            "at any residue center, if the three incident target vectors "
            "each have a localized non-target coordinate, contract the pure "
            "target slice by integral covectors annihilating those vectors; "
            "all three matching terms die but the target becomes the product "
            "of the three localized coordinates"
        ),
        "hypothesis_strength": (
            "only three incident target-vector witnesses are required; all "
            "other residue and boundary cells are arbitrary"
        ),
        "base_ring_scope": (
            "division-free polynomial identity over Z, valid in every "
            "commutative integral domain after localizing the three witnesses"
        ),
        "characteristic_scope": "empty over every field",
        "status": "the residue-31 frontier is closed by the target-star quotient",
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the target-star quotient ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 residue target-star quotient: PASS (exact)")
    print("residue cells:", ledger["support"]["residue_cells"])
    print("generators:", ledger["support"]["coefficient_generators"])
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
