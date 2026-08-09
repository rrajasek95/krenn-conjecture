#!/usr/bin/env python3
"""Exact reciprocal-coordinate Schur-descent counterguard over Q.

The literal reciprocal pair is the active edge 13=-e1 tensor e0 in the
committed exact binary Delta_(6,2) source.  For a completely general endpoint
covector K, this checker forms the natural hafnian Schur update on the four
residual sites and verifies its first unavoidable two-insertion error.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import os
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_SOURCE_SHA256 = (
    "6a49ea60582c407ab7da8ed4b56380c31de6d67ae8580fb7352990e4e9deb30b"
)
SOURCE = os.path.join(
    HERE, "verify_general_covector_pair_cap_obstruction.py"
)
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest() == PINNED_SOURCE_SHA256,
            "the pinned exact binary pair-cap source changed")
G = importlib.import_module("verify_general_covector_pair_cap_obstruction")

EXPECTED_LEDGER_SHA256 = (
    "1aa67bccbbb925930fe260408fe359825e38cd27898c6dfdafcde6b46d20499c"
)


def content_hash(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def matrix_add(left, right, scalar=1):
    edges = set(left) | set(right)
    result = {}
    for edge in edges:
        matrix = tuple(tuple(sp.factor(
            left.get(edge, G.ZERO)[i][j]
            + scalar * right.get(edge, G.ZERO)[i][j]
        ) for j in G.COLORS) for i in G.COLORS)
        if matrix != G.ZERO:
            result[edge] = matrix
    return result


def tensor_trace(tensor):
    return [[list(word), str(sp.factor(value))]
            for word, value in sorted(tensor.items())]


def matrix_trace(matrices):
    return [[list(edge), [[str(sp.factor(value)) for value in row]
                          for row in matrix]]
            for edge, matrix in sorted(matrices.items())]


def audit():
    full = G.matching_tensor(G.VERTICES, G.X)
    require(full == {(0,) * 6: sp.S.One, (1,) * 6: sp.S.One},
            "the pinned source stopped realizing binary Delta_6")
    active_cofactors = {}
    for edge in G.X:
        complement = tuple(v for v in G.VERTICES if v not in edge)
        cofactor = G.matching_tensor(complement, G.X)
        require(cofactor, "a displayed source edge lost activity")
        active_cofactors[edge] = cofactor

    p, q = 1, 3
    direct = G.X[p, q]
    require(direct == ((0, 0), (-1, 0)),
            "the selected reciprocal coordinate block changed")
    # In endpoint order (p,q), this is -e_1^(p) tensor e_0^(q).  Its nonzero
    # cofactor supplies both directed witnesses p->q (head 0) and q->p
    # (head 1), so the same physical pair is literally reciprocal.
    complement = (2, 4, 5, 6)
    require(active_cofactors[p, q]
            == G.matching_tensor(complement, G.X),
            "the reciprocal pair cofactor changed")

    scalar = sp.factor(sum(
        G.K[i][j] * G.entry(G.X, p, q, i, j)
        for i in G.COLORS for j in G.COLORS
    ))
    require(scalar == -G.K10,
            "the reciprocal coordinate cap scalar changed")
    remaining, first_jet = G.first_jet(p, q)
    require(remaining == complement,
            "the reciprocal residual site set changed")
    correction = G.matching_tensor(remaining, first_jet)
    require(correction == {(1, 0, 1, 1): G.K10 * G.K11},
            "the first two-insertion permanent changed")
    require(sp.factor(correction[(1, 0, 1, 1)]
                      + scalar * G.K11) == 0,
            "the higher insertion is not -s*kappa_1")

    residual = {edge: matrix for edge, matrix in G.X.items()
                if set(edge) <= set(remaining)}
    schur = matrix_add(residual, first_jet, 1 / scalar)
    schur_top = G.matching_tensor(remaining, schur)
    expected_schur = {
        (0, 0, 0, 0): sp.factor(G.K00 / scalar),
        (1, 1, 1, 1): sp.factor(G.K11 / scalar),
        (1, 0, 1, 1): sp.factor(G.K10 * G.K11 / scalar**2),
    }
    require(schur_top == expected_schur,
            "the exact four-site hafnian Schur expansion changed")
    mixed_error = sp.factor(schur_top[(1, 0, 1, 1)])
    require(sp.factor(mixed_error - G.K11 / G.K10) == 0,
            "the reciprocal Schur error changed")

    # Retaining both binary target axes requires kappa_0*kappa_1 != 0;
    # seeing the reciprocal direct cell requires s=-k10 != 0.  On this open
    # set the displayed mixed coefficient cannot vanish.
    product = sp.factor(scalar * G.K00 * G.K11 * mixed_error)
    require(sp.factor(product + G.K00 * G.K11**2) == 0,
            "the nondegenerate reciprocal error product changed")

    # The sign-reversed update suggested by determinant Schur complements is
    # not a repair: it already gets the linear endpoint contraction wrong.
    reverse_schur = matrix_add(residual, first_jet, -1 / scalar)
    reverse_top = G.matching_tensor(remaining, reverse_schur)
    require(reverse_top != expected_schur,
            "the sign-reversed hafnian update unexpectedly descended")

    ledger = {
        "pinned_source_sha256": PINNED_SOURCE_SHA256,
        "field": "Q (hence C)",
        "source": {
            "sites": list(G.VERTICES),
            "colours": list(G.COLORS),
            "output": tensor_trace(full),
            "displayed_active_edges": len(active_cofactors),
        },
        "literal_reciprocal_pair": {
            "edge": [p, q],
            "block": [[str(value) for value in row] for row in direct],
            "forward_head_colour": 0,
            "reverse_head_colour": 1,
            "cofactor": tensor_trace(active_cofactors[p, q]),
            "cap_scalar": str(scalar),
        },
        "first_jet": matrix_trace(first_jet),
        "two_insertion_permanent": tensor_trace(correction),
        "schur_update_top": tensor_trace(schur_top),
        "mixed_error": str(mixed_error),
        "nondegenerate_open_condition": "s*k00*k11 != 0",
        "nondegenerate_error_product": str(product),
        "uniform_packet_identity": (
            "for N=2h+2, q'=q+s^-1 R_K has top hafnian equal to "
            "s^-1 times the capped target plus the sum of insertion terms "
            "s^-j R_K^[j] q^[h-j], j>=2"
        ),
        "verdict": (
            "literal reciprocity alone does not give hafnian Schur descent: "
            "the first higher insertion is nonzero whenever the cap sees "
            "the reciprocal cell and retains both target colours"
        ),
        "scope_guard": (
            "this exact binary source refutes a reciprocity-only local "
            "descent rule; a ternary proof may still use the third-colour "
            "packet or additional global source provenance"
        ),
    }
    digest = content_hash(ledger)
    return ledger, digest


def main():
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the reciprocal Schur counterguard ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("reciprocal block:", ledger["literal_reciprocal_pair"]["block"])
    print("mixed Schur error:", ledger["mixed_error"])
    print("reciprocal coordinate Schur descent: COUNTERGUARDED")


if __name__ == "__main__":
    main()
