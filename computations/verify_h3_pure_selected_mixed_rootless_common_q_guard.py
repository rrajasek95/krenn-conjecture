#!/usr/bin/env python3
"""A 20-cell physical rootless guard for the first pure/mixed subsystem.

This checker asks whether the following intrinsic h=3 subsystem is already
inconsistent:

* one literal common q and physical p_i,s_j;
* all nine rows at each of the three pure residual words;
* all nine rows at the selected mixed word 010122;
* q^[3] independent from the three pure targets;
* exact labelled GHZ quotient slices;
* the common direct matrix and off-diagonal scalar-zero K_* relation;
* generically active selected line and rank-six clean-error Macaulay map.

It is not inconsistent.  The exact 20-cell packet below satisfies every one
of these conditions.  The full EqSystem has 106 remaining defects; the first
is row 00 at residual word 000011.  Thus any unit certificate must consume at
least one additional mixed/deleted-word row beyond this four-word subsystem.
"""

from __future__ import annotations

import importlib
import os
import sys
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINS = {
    "verify_h3_common_q_hessian_realization_gate.py":
        "ff927d71b37a0988ce0ac96230950f99f983646a640229b8614d1e81494567c2",
    "../notes/2026-08-15-h3-common-q-hessian-realization-gate.md":
        "58ce518336914446902d73cb669f72ccf7d195201297553cd7defb07f890d78a",
}
EXPECTED_LEDGER_SHA256 = (
    "d920aad5e4430ddf2e0be7964e7a9e23a3583bf3c8165ef14891dacb052d9666"
)


def pin_sources():
    result = {}
    for relative, expected in sorted(PINS.items()):
        path = os.path.normpath(os.path.join(HERE, relative))
        with open(path, "rb") as handle:
            result[relative] = sha256(handle.read()).hexdigest()
        require(result[relative] == expected,
                "pinned source changed: %s (%s)" %
                (relative, result[relative]))
    return result


PINNED = pin_sources()
H = importlib.import_module("verify_h3_common_q_hessian_realization_gate")
N = H.N
A = H.A
L = A.L

PURE_WORDS = tuple((colour,) * 6 for colour in A.COLORS)
SELECTED_MIXED = (0, 1, 0, 1, 2, 2)
LOCAL_WORDS = PURE_WORDS + (SELECTED_MIXED,)


def build_packet():
    q = {}
    for colour in A.COLORS:
        q[(2, 3, colour, colour)] = Q(1)
        q[(4, 5, colour, colour)] = Q(1)
    q[(0, 1, 0, 1)] = Q(1)
    q[(2, 3, 0, 1)] = Q(1)

    p = {(label, 0, label): Q(1) for label in A.COLORS}
    s = {(label, 1, label): Q(1) for label in A.COLORS}
    p[(0, 2, 0)] = Q(1)
    s[(0, 3, 1)] = Q(1)
    p[(0, 4, 0)] = Q(-1)
    s[(1, 5, 1)] = Q(-1)

    direct = {(0, 0): Q(-1), (0, 1): Q(-1)}
    packet = L.Packet(q, p, s, direct)
    require(len(q) + len(p) + len(s) + len(direct) == 20,
            "the physical guard is no longer a 20-cell packet")
    return packet


def target(i, j, word):
    return Q(1) if i == j and word == (i,) * 6 else Q(0)


def shifted_column(cubic, shift):
    result = [Q(0)] * 6
    for degree, value in enumerate(cubic):
        result[degree + shift] = value
    return tuple(result)


def determinant(matrix):
    return A.determinant(matrix)


def audit_packet():
    packet = build_packet()
    p_vectors = tuple(A.star_vector(packet, "P", colour)
                      for colour in A.COLORS)
    s_vectors = tuple(A.star_vector(packet, "S", colour)
                      for colour in A.COLORS)
    star_ranks = (A.D.C.rank(p_vectors), A.D.C.rank(s_vectors),
                  A.D.C.rank(p_vectors + s_vectors))
    require(star_ranks == (3, 3, 6),
            "the endpoint stars are not a full-rank 3+3 split")

    q3 = A.q_cube(packet)
    targets = tuple(A.target_vector(colour) for colour in A.COLORS)
    q3_support = tuple((word, q3[index]) for index, word in enumerate(A.WORDS)
                       if q3[index])
    require(len(q3_support) == 12,
            "the common q cube support changed: %s" % (q3_support,))
    require(all(q3[A.WORDS.index(word)] == 0 for word in PURE_WORDS),
            "q^[3] acquired a pure target coordinate")
    require(len(A.independent_vectors((q3,) + targets)) == 4,
            "q^[3] is not independent of the three pure targets")

    # Full physical common-q/Hessian realization, not a formal C tensor.
    hessian, cross, common_q = H.audit_common_q(packet, p_vectors, s_vectors)

    # The fixed labelled quotient slices are already exactly GHZ diagonal.
    slices = []
    for colour in A.COLORS:
        functional, _ = N.functional_for_pure_target(q3, colour)
        slices.append([[A.pairing(functional, cross[i][j])
                        for j in A.COLORS] for i in A.COLORS])
    slices = tuple(slices)
    require(slices == N.canonical_slices(),
            "the local guard lost exact labelled GHZ quotient slices")
    quotient = N.criterion(slices)
    require(quotient["passes"],
            "the local guard failed the exact GHZ slice criterion")

    local_checks = []
    for word in LOCAL_WORDS:
        for i, j in product(A.COLORS, repeat=2):
            value = packet.row(i, j, dict(enumerate(word)))
            want = target(i, j, word)
            require(value == want,
                    "a local pure/selected-mixed EqSystem row failed")
            local_checks.append((i, j, word, value))
    require(len(local_checks) == 36,
            "the four-word local row census is not 36")

    direct = [[packet.de(i, j) for j in A.COLORS] for i in A.COLORS]
    require(direct == [[Q(-1), Q(-1), Q(0)],
                       [Q(0), Q(0), Q(0)],
                       [Q(0), Q(0), Q(0)]],
            "the common direct matrix changed")
    alpha = direct[0][1]
    tau = sum(direct[i][i] for i in A.COLORS)
    scalar_k = [[-alpha if i == j else Q(0) for j in A.COLORS]
                for i in A.COLORS]
    scalar_k[0][1] += tau
    require(scalar_k == [[Q(1), Q(-1), Q(0)],
                         [Q(0), Q(1), Q(0)],
                         [Q(0), Q(0), Q(1)]],
            "K_*=tr(a)E_01-a_01 I changed")
    require(sum(scalar_k[i][j] * direct[i][j]
                for i, j in product(A.COLORS, repeat=2)) == 0,
            "K_* is not scalar-zero")
    require(determinant(scalar_k) == 1,
            "the off-diagonal scalar-zero channel is singular")

    line = L.line_verdict(packet, 0, 1)
    require(line["act"] == (Q(0), Q(0), Q(0), Q(-1), Q(-1)),
            "the activity is not z^3(-1-z)")
    require(line["gcd"] == (Q(1),) and line["rank"] == 4,
            "the selected affine clean family is not gcd-one/rank-four")
    all_columns = [shifted_column(cubic, shift)
                   for cubic in line["cubics"].values() for shift in range(3)]
    require(L.rank_of(all_columns, 6) == 6,
            "the projective clean-error Macaulay map is not rank six")

    selected_columns = (
        ((0, 0, 0, 0, 0, 1), 0),
        ((0, 0, 0, 0, 0, 1), 1),
        ((0, 0, 0, 0, 0, 1), 2),
        ((0, 0, 0, 1, 0, 0), 2),
        ((0, 0, 0, 1, 0, 1), 0),
        ((0, 1, 0, 0, 0, 1), 0),
    )
    columns = tuple(shifted_column(line["cubics"][word], shift)
                    for word, shift in selected_columns)
    minor = tuple(tuple(columns[column][row] for column in range(6))
                  for row in range(6))
    require(determinant(minor) == Q(-192),
            "the explicit rootless 6x6 Macaulay minor changed")

    deletion_controls = []
    for shore, key in (("p", (0, 4, 0)), ("s", (1, 5, 1))):
        q_copy, p_copy = dict(packet.q), dict(packet.p)
        s_copy, d_copy = dict(packet.s), dict(packet.d)
        del (p_copy if shore == "p" else s_copy)[key]
        smaller = L.Packet(q_copy, p_copy, s_copy, d_copy)
        smaller_line = L.line_verdict(smaller, 0, 1)
        smaller_columns = [shifted_column(cubic, shift)
                           for cubic in smaller_line["cubics"].values()
                           for shift in range(3)]
        require(smaller_line["gcd"] == (Q(0), Q(1), Q(1))
                and L.rank_of(smaller_columns, 6) == 4,
                "deleting one rootless-repair star did not restore z(z+1)")
        deletion_controls.append(
            (shore, key, smaller_line["gcd"],
             L.rank_of(smaller_columns, 6)))

    defects = []
    for i, j in product(A.COLORS, repeat=2):
        for word in A.WORDS:
            value = packet.row(i, j, dict(enumerate(word)))
            difference = value - target(i, j, word)
            if difference:
                defects.append((i, j, word, difference))
    require(len(defects) == 106,
            "the remaining full-EqSystem defect count changed")
    require(defects[0] == (0, 0, (0, 0, 0, 0, 1, 1), Q(1)),
            "the first missing mixed row changed")
    require(not any((i, j, word, value) in defects
                    for i, j, word, value in local_checks),
            "a certified local row reappeared in the defect ledger")

    return {
        "support_cells": {
            "q": len(packet.q), "p": len(packet.p), "s": len(packet.s),
            "direct": len(packet.d), "total": 20,
        },
        "star_ranks_P_S_total": star_ranks,
        "q3_support": q3_support,
        "rank_q3_X0_X1_X2": 4,
        "common_q_hessian": common_q,
        "quotient_slices": tuple(tuple(tuple(row) for row in matrix)
                                 for matrix in slices),
        "quotient_criterion": quotient,
        "local_words": LOCAL_WORDS,
        "local_eqsystem_scalar_rows": len(local_checks),
        "direct_matrix": tuple(tuple(row) for row in direct),
        "selected_colours": (0, 1),
        "alpha_tau": (alpha, tau),
        "scalar_zero_K": tuple(tuple(row) for row in scalar_k),
        "det_K": determinant(scalar_k),
        "activity": line["act"],
        "clean_coordinate_rank": line["rank"],
        "clean_gcd": line["gcd"],
        "macaulay_shape_rank": (6, len(all_columns),
                                 L.rank_of(all_columns, 6)),
        "selected_macaulay_columns": selected_columns,
        "selected_macaulay_minor": minor,
        "selected_macaulay_determinant": determinant(minor),
        "rootless_repair_deletion_controls": tuple(deletion_controls),
        "full_eqsystem": {
            "satisfied": 3 ** 8 - len(defects),
            "defects": len(defects),
            "first_defect": defects[0],
            "full_defect_ledger": tuple(defects),
        },
    }


def build_ledger():
    guard = audit_packet()
    return {
        "theorem": (
            "the three pure word matrices plus the selected mixed word do "
            "not give a unit ideal after common-q, exact GHZ quotient, "
            "direct/scalar-zero, activity, and rootless Macaulay saturation"
        ),
        "pins": PINNED,
        "guard": guard,
        "scope": (
            "literal common-q local solution, not a full EqSystem source; "
            "global coarse containment fails on the 106 displayed remaining "
            "rows.  No global support-minimality is claimed for 20 cells."
        ),
        "next_exact_row": (
            "row (0,0), residual word 000011, target zero, physical value one"
        ),
    }


def main():
    ledger = build_ledger()
    digest = A.D.content_hash(ledger)
    require(digest == EXPECTED_LEDGER_SHA256,
            "ledger digest changed: got %s" % digest)
    guard = ledger["guard"]
    print("PASS: 20-cell physical rootless common-q local guard")
    print("local subsystem: 3 pure words + 010122, all 36 rows exact")
    print("GHZ quotient exact; K*=I-E_01; activity z^3(-1-z)")
    print("clean Macaulay: rank 6, explicit minor -192")
    print("full EqSystem: %d/6561 rows satisfied; first defect 00:000011=1" %
          guard["full_eqsystem"]["satisfied"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
