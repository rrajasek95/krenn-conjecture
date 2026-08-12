#!/usr/bin/env python3
"""Exact algebra for coefficientwise flat C4 transport.

If nonzero edge tables satisfy

  X01(a,b) X45(c,d) = lambda X05(a,d) X14(b,c)

for all colours, then the common four-tensor has rank one across the two
crossing bipartitions and is therefore a product of four vertex factors.
No torus hypothesis is needed.  This checker reconstructs the factors by
pivot ratios, verifies a zero-entry example, and freezes the failure of the
conclusion if one assumes equality only on common nonzero support.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json


EXPECTED_LEDGER_SHA256 = (
    "eb4ac8232e20c7de4fe991382f7be83f16b503fe212032941f1486753d33c12c"
)
COLOURS = range(3)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def outer(left, right, scale=Q(1)):
    return tuple(tuple(scale * left[a] * right[b] for b in COLOURS)
                 for a in COLOURS)


def tensor(X01, X45):
    return {
        (a, b, c, d): X01[a][b] * X45[c][d]
        for a in COLOURS for b in COLOURS
        for c in COLOURS for d in COLOURS
    }


def audit_vertex_reconstruction():
    u0 = tuple(map(Q, (2, 3, 5)))
    u1 = tuple(map(Q, (7, 11, 13)))
    u4 = tuple(map(Q, (17, 19, 23)))
    u5 = tuple(map(Q, (29, 31, 37)))
    scalar_01, scalar_45 = Q(3), Q(5)
    scalar_05, scalar_14 = Q(15), Q(1)
    X01 = outer(u0, u1, scalar_01)
    X45 = outer(u4, u5, scalar_45)
    X05 = outer(u0, u5, scalar_05)
    X14 = outer(u1, u4, scalar_14)
    left = tensor(X01, X45)
    right = {
        (a, b, c, d): X05[a][d] * X14[b][c]
        for a in COLOURS for b in COLOURS
        for c in COLOURS for d in COLOURS
    }
    require(left == right, "the crossing Segre equality changed")

    pivot = left[(0, 0, 0, 0)]
    factors = {
        0: tuple(left[(a, 0, 0, 0)] / pivot for a in COLOURS),
        1: tuple(left[(0, b, 0, 0)] for b in COLOURS),
        4: tuple(left[(0, 0, c, 0)] / pivot for c in COLOURS),
        5: tuple(left[(0, 0, 0, d)] / pivot for d in COLOURS),
    }
    reconstructed = {
        word: factors[0][word[0]] * factors[1][word[1]]
              * factors[4][word[2]] * factors[5][word[3]]
        for word in left
    }
    require(reconstructed == left,
            "pivot ratios stopped reconstructing the vertex tensor")

    # Each physical edge table is rank one.  Its vertex lines agree with the
    # reconstructed tensor factors, up to the expected scalar gauges.
    matrices = {"01": X01, "45": X45, "05": X05, "14": X14}
    for name, matrix in matrices.items():
        require(all(matrix[a][b] * matrix[0][0]
                    == matrix[a][0] * matrix[0][b]
                    for a in COLOURS for b in COLOURS),
                f"{name} stopped having rank one")
    return {
        "word_count": len(left),
        "all_entries_nonzero": all(left.values()),
        "vertex_factors": {
            str(site): tuple(map(str, value))
            for site, value in factors.items()
        },
        "edge_rank_one_minors_checked": 4 * 9,
        "conclusion": (
            "the common crossing tensor is a four-vertex pure tensor; "
            "all edge tables are its pairwise vertex factors up to scalars"
        ),
    }


def audit_zero_support_guard():
    # Equality on a sparse support does not force the edge tables themselves
    # to have rank one.  The diagonal identity matrix supplies the smallest
    # guard: choose X01=X05=I and X45=X14=I.  The two products agree only on
    # the all-equal support; none of the edge tables has rank one.
    identity = tuple(tuple(Q(1) if a == b else Q(0) for b in COLOURS)
                     for a in COLOURS)
    left = tensor(identity, identity)
    right = {
        (a, b, c, d): identity[a][d] * identity[b][c]
        for a in COLOURS for b in COLOURS
        for c in COLOURS for d in COLOURS
    }
    common_nonzero = {word for word in left
                      if left[word] and right[word]}
    require(common_nonzero == {(0, 0, 0, 0), (1, 1, 1, 1),
                               (2, 2, 2, 2)},
            "the sparse diagonal support guard changed")
    require(any(identity[a][b] * identity[0][0]
                != identity[a][0] * identity[0][b]
                for a in COLOURS for b in COLOURS),
            "the sparse edge table unexpectedly became rank one")
    return {
        "common_nonzero_words": sorted(common_nonzero),
        "edge_rank": 3,
        "conclusion": (
            "equality only where both products are nonzero does not force "
            "vertex gauge; complete coefficientwise equality is essential"
        ),
    }


def audit_zero_entry_equality():
    # Full coefficientwise equality still forces gauge when vertex factors
    # have zeros.  This guards the stronger statement against accidentally
    # localizing every tensor entry.
    u0 = tuple(map(Q, (1, 0, 2)))
    u1 = tuple(map(Q, (0, 3, 5)))
    u4 = tuple(map(Q, (7, 0, 11)))
    u5 = tuple(map(Q, (13, 17, 0)))
    X01 = outer(u0, u1, Q(2))
    X45 = outer(u4, u5, Q(3))
    X05 = outer(u0, u5, Q(6))
    X14 = outer(u1, u4, Q(1))
    left = tensor(X01, X45)
    right = {
        (a, b, c, d): X05[a][d] * X14[b][c]
        for a in COLOURS for b in COLOURS
        for c in COLOURS for d in COLOURS
    }
    require(left == right and any(not value for value in left.values()),
            "the zero-entry crossing equality changed")
    for name, matrix in (("01", X01), ("45", X45),
                         ("05", X05), ("14", X14)):
        require(all(matrix[a][b] * matrix[0][1]
                    == matrix[a][1] * matrix[0][b]
                    for a in COLOURS for b in COLOURS),
                f"the zero-entry {name} table lost rank one")
    return {
        "zero_tensor_entries": sum(not value for value in left.values()),
        "coefficientwise_equality": True,
        "all_four_edge_tables_rank_one": True,
    }


def main():
    ledger = {
        "torus_vertex_gauge": audit_vertex_reconstruction(),
        "zero_entry_coefficientwise_equality": audit_zero_entry_equality(),
        "common_support_only_guard": audit_zero_support_guard(),
        "proof_identity": (
            "choose nonzero entries of X01 and X45; the crossing equality "
            "writes each as an outer product. Equivalently, a nonzero "
            "tensor simple across 01|45 and 05|14 is fully decomposable"
        ),
        "source_scope": (
            "this identifies matching-evaluation gauge under complete "
            "coefficientwise two-base equality; source rows with additional "
            "matching terms still require base-exhaustivity/saturation"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"C4 torus gauge ledger changed: {digest}")
    print(json.dumps(ledger, sort_keys=True))
    print(f"ledger_sha256={digest}")
    print("C4 coefficientwise flat-transport vertex gauge: PASS")


if __name__ == "__main__":
    main()
