#!/usr/bin/env python3
"""Transfer the residual-q private-pivot debt to the relative P2 carrier.

The normalized cap factorization produces the desired endpoint-odd residue
correction but, on literal complete rows, leaves four independent private
pivots with coefficients p=(1,-1,-1,1).  Their sum is zero.  Hence, once
these four labelled pivots are embedded in one centered occurrence module,
the universal relative graph has the exact boundary

    d Gamma_p = t_p-p.

Adding it to the cap combination cancels every private pivot and leaves only
the retained carrier t_p.  This is an exact reduction, not an absolute
construction: a physical landing of t_p is still required.  It shows that
the private-pivot obstruction to the residual-q KS correction and the
AugP2/E14 centered-carrier landing are the same interface after the labelled
embedding is supplied.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_reduced_eq_cap_factorization.py":
        "b6cea93a8a009fce3e97eac0b6321c1175686aa47bb374e82bed7f7e0f604cb4",
    "notes/h3-residual-q-reduced-eq-cap-factorization.md":
        "d0ec335fa09d3524ce04fd14b470a697bcd87ec9cb1e18820dd817920577ec57",
    "computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py":
        "4dfb2846c698e5603dadeb1a73add17a7984ccedbad25e3bb09b6aa4170e62ce",
    "notes/h2-p2-relative-occurrence-graph-resolution-gate.md":
        "101f1040df04e5f6a3ca7c5034c1a3a713903704936207619c5ec8e00d59df37",
    "computations/verify_h3_residual_q_ks_constructive_landing_boundary.py":
        "bc11c8fe61ec8c21a1850326de037a328ab7f7404bcf3902655f6541e496bc9f",
}
EXPECTED_LEDGER_SHA256 = (
    "403dcbb8745ada1b1763ea9ec4388b25758d1fd02355b2131b99ad1792f92201"
)

ROWS = ("Eq", "ainc", "W", "target", "ores")
CORNERS = ("P+q00", "P-q00", "P+q11", "P-q11")
ALPHA = (Q(-1), Q(1), Q(1), Q(-1))
PRIVATE_DEBT = tuple(-entry for entry in ALPHA)
N = 12

R0 = (Q(1), Q(-1), Q(0), Q(1), Q(0))
T = (Q(0), Q(0), Q(-1), Q(1), Q(0))
RHO = (Q(0), Q(0), Q(1), Q(0), Q(1))
REDUCED_EQ = (Q(-1), Q(0), Q(0), Q(0), Q(0))
K = (Q(0), Q(1), Q(0), Q(0), Q(1))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(*vectors):
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * entry for entry in vector)


def unit(index, width):
    return tuple(Q(index == position) for position in range(width))


def rank(columns):
    if not columns:
        return 0
    rows = [list(row) for row in zip(*columns, strict=True)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(len(rows)):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def block(local, private=None, carrier=None):
    private = private or (Q(0),) * N
    carrier = carrier or (Q(0),) * N
    return tuple(local) + tuple(private) + tuple(carrier)


def local_at(corner, vector):
    width = len(ROWS) * len(CORNERS)
    answer = [Q(0)] * width
    offset = corner * len(ROWS)
    answer[offset:offset + len(ROWS)] = vector
    return tuple(answer)


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    local_width = len(ROWS) * len(CORNERS)
    zero_local = (Q(0),) * local_width
    old_combination_terms = []
    desired_terms = []
    for corner, coefficient in enumerate(ALPHA):
        private = unit(corner, N)
        r0_literal = block(local_at(corner, R0), private=private)
        t_column = block(local_at(corner, T))
        rho_column = block(local_at(corner, RHO))
        c_column = block(local_at(corner, REDUCED_EQ))
        k_column = block(local_at(corner, K))
        old_combination_terms.append(scale(
            coefficient,
            add(scale(-1, r0_literal), t_column, rho_column,
                scale(-1, c_column)),
        ))
        desired_terms.append(scale(coefficient, k_column))

    old_combination = add(*old_combination_terms)
    desired = add(*desired_terms)
    p_full = PRIVATE_DEBT + (Q(0),) * (N - len(PRIVATE_DEBT))
    private_vector = (Q(0),) * local_width + p_full + (Q(0),) * N
    require(old_combination == add(desired, private_vector),
            "the literal cap private debt changed")
    require(sum(PRIVATE_DEBT, Q(0)) == 0,
            "the residual-q private debt stopped being centered")

    # Relative graph formula d Gamma_i=t_i-c_i.  The source-labelled
    # embedding identifies the four private pivots with four c_i entries.
    # Its p-combination therefore has boundary t_p-p.
    carrier_vector = (Q(0),) * local_width + (Q(0),) * N + p_full
    gamma_p = add(carrier_vector, scale(-1, private_vector))
    transferred = add(old_combination, gamma_p)
    require(transferred == add(desired, carrier_vector),
            "the relative graph stopped transferring private debt to t")

    # A landing column with principal boundary -t_p finishes the literal
    # private block.  Its forced target/cap/ridge faces are deliberately not
    # inserted here: they are exactly the remaining augmented theorem.
    landing_principal = scale(-1, carrier_vector)
    require(add(transferred, landing_principal) == desired,
            "the conditional physical carrier landing stopped closing")

    old_rank = rank([old_combination])
    transferred_rank = rank([old_combination, gamma_p])
    landing_rank = rank([old_combination, gamma_p, landing_principal])
    require((old_rank, transferred_rank, landing_rank) == (1, 2, 3),
            ("the transfer/landing ranks changed", old_rank,
             transferred_rank, landing_rank))

    # C=12I-J acts by 12 on this centered vector.  Thus in raw occurrence
    # coordinates the same Gamma is obtained from u=p/12.
    one = (Q(1),) * N
    c_matrix = tuple(tuple(Q(12 * (row == column) - 1)
                           for column in range(N))
                     for row in range(N))
    raw = tuple(entry / 12 for entry in p_full)
    centered = tuple(sum(c_matrix[row][column] * raw[column]
                         for column in range(N))
                     for row in range(N))
    require(centered == p_full
            and sum(raw, Q(0)) == 0
            and all(sum(row, Q(0)) == 0 for row in c_matrix)
            and one == (Q(1),) * N,
            "the centered C=12I-J normalization changed")

    ledger = {
        "theorem": "residual-q private pivot to relative P2 carrier transfer",
        "pins": PINS,
        "cap_block": {
            "row_order_per_corner": list(ROWS),
            "corner_order": list(CORNERS),
            "endpoint_odd_coefficients": [str(value) for value in ALPHA],
            "literal_private_debt": [str(value) for value in PRIVATE_DEBT],
            "private_debt_sum": "0",
            "identity": "old cap combination = desired KS residue + p",
        },
        "relative_graph": {
            "centered_operator": "C=12I-J",
            "raw_occurrence_preimage": [str(value) for value in raw],
            "C_times_raw": [str(value) for value in centered],
            "relative_boundary": "d Gamma_p=t_p-p",
            "transferred_identity": (
                "old cap combination + d Gamma_p = desired KS residue + t_p"
            ),
            "same_classical_fibre_with_t_retained": True,
        },
        "conditional_finish": {
            "new_principal_boundary": "-t_p",
            "result_after_landing": "desired endpoint-odd residue-only KS cell",
            "landing_constructed_here": False,
            "forced_augmented_faces": [
                "E14/unary target-normal", "scalar cap residue",
                "reduced Eq", "anchor conormal", "physical q",
                "shifted Kahler ridge", "W", "eta/sigma",
            ],
        },
        "unification": (
            "after a source-labelled embedding of the four complete-row "
            "private pivots into one occurrence orbit, the residual-q KS "
            "private obstruction is not a separate source theorem: it is "
            "exactly the same retained centered-carrier landing required by "
            "AugP2/E14"
        ),
        "first_missing_typing": (
            "construct the literal embedding for every private full-nine "
            "pivot and land t_p with the complete target/cap/ridge/terminal "
            "faces; the coefficient transfer alone does not supply it"
        ),
        "scope": (
            "exact four-corner linear source block and universal relative "
            "graph.  The source-labelled occurrence embedding and physical "
            "carrier landing are hypotheses, not consequences"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


if __name__ == "__main__":
    ledger, digest = audit()
    require(digest == EXPECTED_LEDGER_SHA256,
            ("ledger changed", digest))
    print("residual-q private debt: CENTERED (1,-1,-1,1)")
    print("relative graph: private debt -> retained carrier t_p")
    print("absolute KS correction: CONDITIONAL ON PHYSICAL t_p LANDING")
    print("separate private-pivot theorem after AugP2 landing: NO")
    print("ledger_sha256=" + digest)
