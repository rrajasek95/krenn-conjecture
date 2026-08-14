#!/usr/bin/env python3
"""Audit the apparent Gate-I / balanced-square reduced-Eq convergence.

The shared-loop near-hit for a normalized six-label vector u has

    (B, Eq, ainc) = (u, u, -1),

and its missing correction is (0,-u,+1).  Four normalized shared-loop
directions can be identified abstractly with the four balanced corners.  A
delta-weighted sum of the *missing corrections* then has Eq=-delta and zero
anchor, exactly the balanced projection filler.

This is not a construction from the strongest audited near-hits.  Their same sum is
tied B=Eq and is killed by chi=delta.(B-Eq).  The shore-sign gauge acts on
both blocks and preserves the tie; the physical q identity has zero B/Eq
projection.  More basically, the Gate-I faces-(3,5), normalized-Y=1 pure
component and the balanced AugP2 cap lie in different literal
word/fine/repeated/operation summands.  The four-corner identification is a
grade-forgetting linear map, not a committed source chain map.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_shared_loop_full_augmented_membership_dual.py":
        "108ffb00c5b742613b464d2d6c46dd967b6db4eac3fe2e1d967b32500e4a6abb",
    "notes/h3-shared-loop-full-augmented-membership-dual.md":
        "a0286cbe24c2185c3bb540166d66e1bd60bea75db5206e4dbab50da10bfc10b4",
    "computations/verify_h3_cut_swap_shared_loop_hasse_cross_term_gate.py":
        "cc551585391a990060f78b49486c05af6c3b4a301058c855a422ae9d54fe5be5",
    "notes/h3-cut-swap-shared-loop-hasse-cross-term-gate.md":
        "927e7251ee925fe43e2db194cbe5bebe861c09e9e75969207e7ce25b6f0eeaa2",
    "computations/verify_h3_balanced_square_private_eq_projection_gate.py":
        "bbfb690a73844169574351ad019171a6d9c5fe332e59cc9694a1f67dcf31cf8e",
    "notes/h3-balanced-square-private-eq-projection-gate.md":
        "6d740e7e30231204dbe1b79c4b7c21fe5f5b5ac45122ac714be3c7626afa7c31",
    "computations/verify_h3_balanced_square_pointed_full_q_cone_gate.py":
        "10c2ca7ca9168d41f25f428b628710c0eaf8bc2aa910e23100da161869fdc72e",
    "notes/h3-balanced-square-pointed-full-q-cone-gate.md":
        "a81873b5e6f9b5c7c2e220b39dabd4fc74a7e1914690516b7727b578b04b9248",
    "computations/verify_h3_psi_source_grade_macaulay_exhaustiveness_terminal_gate.py":
        "2ae3d0fe36ca6ab92ee506b4a4441d6476ecb09567a1441c66f54793e304980d",
    "notes/h3-psi-source-grade-macaulay-exhaustiveness-terminal-gate.md":
        "de47eeafdfcffbd043f3b2472f3be54b7ec94ad546fe2bab7194e8b64bd9c98a",
    "computations/verify_h3_reduced_eq_full_physical_augmentation_matrix.py":
        "f66752bd3a44a9506b4a31467ce52dcb16e52f841b0f29ce66066a38ec7f97c1",
    "notes/h3-reduced-eq-full-physical-augmentation-matrix.md":
        "465010f65fb479998a9436fb4fdcc605fd91f9165c641493b00bb75f561e4355",
}
READ_ONLY_EXTERNAL_REPORT = {
    "computations/unaudited-psiz-dual-audit-2026-08-13/REPORT.md":
        "0a7c6223164b9a07c097df07f3911b892b8d5066e786da068b154b6b74262276",
}
EXPECTED_DIGEST = "91a218f314863d3f38b3de167ccf21a29ed4e423a1024125262d9805a279eb78"

DELTA = tuple(map(Q, (1, 1, -1, -1)))
ZERO4 = (Q(0),) * 4
ZERO6 = (Q(0),) * 6


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(values, Q(0)) for values in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(entry) for entry in vector)


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    columns = tuple(columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(height):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in {**PINS, **READ_ONLY_EXTERNAL_REPORT}.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def six_unit(index: int):
    return tuple(Q(position == index) for position in range(6))


def four_unit(index: int):
    return tuple(Q(position == index) for position in range(4))


def abstract_corner_projection(u):
    """The external probe's grade-forgetting four-orbit identification."""
    require(len(u) == 6, "six-label projection width")
    return (Q(u[1]), Q(u[4]), Q(u[0]) + Q(u[5]), Q(u[2]) + Q(u[3]))


def beq(B=ZERO4, Eq=ZERO4, *, M=0, ainc=0, q=0):
    return tuple(map(Q, (*B, *Eq, M, ainc, q)))


def chi(column):
    return dot(DELTA, column[:4]) - dot(DELTA, column[4:8])


def provenance_audit():
    shared = load(
        "computations/verify_h3_shared_loop_full_augmented_membership_dual.py",
        "cross_frontier_shared",
    )
    shared_ledger, shared_digest = shared.audit()
    require(shared_digest == shared.EXPECTED_LEDGER_SHA256,
            "shared-loop ledger changed")
    component = shared_ledger["canonical_complete_component"]
    repairs = shared_ledger["repair_membership"]
    require(component["faces"] == [3, 5]
            and component["columns_rank"] == [288, 288]
            and component["pure_boundaries"] == 6
            and all(record["minimal_missing_after_grants"]["ainc"] == 1
                    for record in repairs.values()),
            "shared-loop provenance changed")

    balanced = load(
        "computations/verify_h3_balanced_square_private_eq_projection_gate.py",
        "cross_frontier_balanced",
    )
    balanced_ledger, balanced_digest = balanced.audit()
    require(balanced_digest == balanced.EXPECTED_LEDGER_SHA256
            and balanced_ledger["projection"]["delta"] == [1, 1, -1, -1]
            and balanced_ledger["projection"]["old_projection_rank"] == 7,
            "balanced projection provenance changed")

    terminal = load(
        "computations/verify_h3_psi_source_grade_macaulay_exhaustiveness_terminal_gate.py",
        "cross_frontier_terminal_tags",
    )
    cap_grade = terminal.CAP_GRADE
    require(cap_grade == {
        "word": "01211222",
        "fine": "t*q_(v,N) at the selected six P3+K2 occurrences",
        "repeated": "P3+K2",
        "operation": "AugP2-cap/mixed-orbit",
        "window": "2345 with literal occurrence labels",
    }, "balanced cap grade changed")

    expected_fine = [
        1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0,
        1, 2, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0,
    ]
    require(component["fine_degree"] == expected_fine,
            "Gate-I fine degree changed")
    hasse = load(
        "computations/verify_h3_cut_swap_shared_loop_hasse_cross_term_gate.py",
        "cross_frontier_hasse_words",
    )
    hasse_ledger, hasse_digest = hasse.audit()
    require(hasse_digest == hasse.EXPECTED_LEDGER_SHA256
            and hasse_ledger["formal_totalization"]["source_valid"] is False
            and hasse_ledger["third_Bianchi_carrier"]["common_marked_word"]
                == "222000"
            and hasse_ledger["third_Bianchi_carrier"]
                ["rho_on_M3_occurrence"]["word"] == "202020",
            "the shared-loop word-splitting guard changed")
    return {
        "Gate_I_shared_loop_grade": {
            "h": 3,
            "deleted_faces": component["faces"],
            "normalized_target": "Y=1",
            "selected_output_word": "00000000 pure full-eight row",
            "fine_degree_24_coloured_slots": component["fine_degree"],
            "repeated_shape": "labelled P3+K2 component at faces (3,5)",
            "operation_parent": "rootless-C5/shared-loop Hasse repair",
            "six_multiplier_labels": True,
            "literal_features_per_pure_boundary": 90,
        },
        "Gate_II_balanced_grade": {
            "h": 3,
            "response_source_word": "11:110000",
            "cap_output": cap_grade,
            "operation_corners": [
                "DQ[a|b]", "DQ[b|a]", "PS[P0,S1]", "PS[P1,S0]",
            ],
        },
        "literal_grade_equal": False,
        "first_committed_Hasse_placement_guard": {
            "carrier_word": "222000",
            "rho_mate_word": "202020",
            "physical_same_word_totalization": False,
        },
        "external_report_status": (
            "read-only hypothesis source; its four-corner transport is "
            "recomputed below and not imported as a physical map"
        ),
    }


def coefficient_audit():
    candidates = (
        six_unit(1),
        six_unit(4),
        scale(Q(1, 2), add(six_unit(0), six_unit(5))),
        scale(Q(1, 2), add(six_unit(2), six_unit(3))),
    )
    require(tuple(abstract_corner_projection(u) for u in candidates)
            == tuple(four_unit(index) for index in range(4))
            and all(sum(u, Q(0)) == 1 for u in candidates),
            "the four normalized shared-loop directions changed")
    u_delta = add(*(scale(value, u)
                    for value, u in zip(DELTA, candidates, strict=True)))
    expected_u_delta = tuple(map(Q, (
        Q(-1, 2), 1, Q(-1, 2), Q(-1, 2), 1, Q(-1, 2),
    )))
    require(u_delta == expected_u_delta
            and sum(u_delta, Q(0)) == 0
            and abstract_corner_projection(u_delta) == DELTA,
            "the abstract delta transport changed")

    # Linear extension of x_u=(B=u,Eq=u,ainc=-1) from normalized sum(u)=1.
    # At u_delta the anchor cancels, but the B/Eq tie remains exact.
    near_hit = beq(B=DELTA, Eq=DELTA, ainc=-sum(u_delta, Q(0)))
    missing = beq(Eq=tuple(-value for value in DELTA),
                  ainc=sum(u_delta, Q(0)))
    completed = add(near_hit, missing)
    balanced_face = beq(B=DELTA)
    require(near_hit == beq(B=DELTA, Eq=DELTA)
            and missing == beq(Eq=tuple(-value for value in DELTA))
            and completed == balanced_face
            and chi(near_hit) == 0
            and chi(missing) == chi(completed) == Q(4),
            "the cross-frontier coefficient identity changed")
    return {
        "six_label_normalized_directions": [
            [str(value) for value in vector] for vector in candidates
        ],
        "grade_forgetting_projection": (
            "P(u)=(u1,u4,u0+u5,u2+u3)"
        ),
        "delta_weighted_six_label_vector": [str(value) for value in u_delta],
        "sum_u_delta": "0",
        "P_u_delta": [1, 1, -1, -1],
        "strongest_overgranted_near_hit_after_P": {
            "B": [1, 1, -1, -1],
            "Eq": [1, 1, -1, -1],
            "ainc": 0,
            "chi": 0,
        },
        "sum_of_missing_corrections_after_P": {
            "B": [0, 0, 0, 0],
            "Eq": [-1, -1, 1, 1],
            "ainc": 0,
            "chi": 4,
        },
        "formal_identity": (
            "P(x_u_delta)+P(c_u_delta)=(B,Eq)=(delta,0)"
        ),
        "source_reading": (
            "the desired term is exactly the sum of the unconstructed "
            "corrections, not a consequence of the near-hits; the displayed "
            "near-hit already grants unproved labelwise residue cancellation"
        ),
    }


def gauge_q_audit():
    diagonal = []
    for index in range(4):
        e = four_unit(index)
        diagonal.append(beq(B=e, Eq=e))
    companions = []
    for direct in (0, 1):
        for endpoint in (2, 3):
            edge = tuple(Q(index in (direct, endpoint)) for index in range(4))
            companions.append(beq(B=edge))
    q_identity = beq(M=1, ainc=-1, q=-1)
    near_hit = beq(B=DELTA, Eq=DELTA)
    old = tuple(diagonal + companions + [q_identity, near_hit])
    balanced = beq(B=DELTA)
    missing = beq(Eq=tuple(-value for value in DELTA))
    require(all(chi(column) == 0 for column in old)
            and rank(old) == 8
            and rank(old + (balanced,)) == 9
            and rank(old + (missing,)) == 9,
            "near-hit/q span changed the balanced quotient")

    # The shore gauge is a coordinate change, applied equally to B and Eq.
    gauge = DELTA
    gauged_near = beq(
        B=tuple(gauge[index] * near_hit[index] for index in range(4)),
        Eq=tuple(gauge[index] * near_hit[4 + index]
                 for index in range(4)),
    )
    require(gauged_near == beq(B=(1, 1, 1, 1), Eq=(1, 1, 1, 1))
            and gauged_near[:4] == gauged_near[4:8],
            "shore gauge broke a B/Eq tie")
    return {
        "old_plus_near_hit_rank": rank(old),
        "rank_after_balanced_or_missing_Eq": rank(old + (balanced,)),
        "chi_on_every_old_near_hit_q_column": 0,
        "shore_sign_gauge": [1, 1, -1, -1],
        "gauged_near_hit": {
            "B": [1, 1, 1, 1],
            "Eq": [1, 1, 1, 1],
            "still_tied": True,
        },
        "physical_q_identity": {
            "signature_M_ainc_q": [1, -1, -1],
            "B_Eq_projection": 0,
            "chi": 0,
            "effect": (
                "repairs scalar q/anchor bookkeeping inside one grade; "
                "cannot create an Eq incidence or change word/fine/operation"
            ),
        },
        "conclusion": (
            "near-hits, shore gauge, K2,2 companions, diagonal cap rows and "
            "physical q identity remain in ker(delta.(B-Eq))"
        ),
    }


def typed_terminal_audit():
    # A direct-sum presentation is the smallest exact logical counterguard:
    # all committed constructions occupy their own idempotent summands.  The
    # grade-forgetting P is deliberately not a differential in this model.
    grades = {
        "Gate_I": (
            "faces(3,5)|Y=1|word=00000000|fine=24-slot-vector|"
            "labelled-P3+K2|rootless-C5/shared-loop"
        ),
        "Gate_II": (
            "source=11:110000|word=01211222|fine=tq(v,N)|P3+K2|"
            "AugP2-mixed|window=2345|DQPS-four-corner"
        ),
    }
    require(grades["Gate_I"] != grades["Gate_II"], grades)
    return {
        "source_idempotents": grades,
        "committed_differential_is_block_diagonal": True,
        "shore_gauge_preserves_idempotent": True,
        "physical_q_identity_preserves_idempotent": True,
        "abstract_P_preserves_idempotent": False,
        "common_missing_column_constructed": False,
        "common_column_if_added": {
            "name": "source-labelled response-to-AugP2 mixed incidence kappa_mix",
            "Gate_II_projection": "(B,Eq)=(0,-delta) or equivalently (delta,0)",
            "Gate_I_restrictions": (
                "c_u=(literal=0,Eq=-u,ainc=sum(u)) on the four normalized "
                "shared-loop directions"
            ),
            "required_extra_structure": (
                "a word/fine/repeated/operation preserving placement chain map "
                "whose four restrictions realize P and commute with q/anchor"
            ),
        },
        "sharp_verdict": (
            "the frontiers share one coefficient normal form after forgetting "
            "source idempotents, but no committed source morphism identifies "
            "them.  The convergence is a projection coincidence; constructing "
            "the required placement/mixed-incidence column is exactly the "
            "remaining kappa_mix problem"
        ),
    }


def run(mode: str) -> str:
    pin_dependencies()
    ledger = {}
    if mode in ("all", "provenance"):
        ledger["literal_provenance_and_grades"] = provenance_audit()
    if mode in ("all", "coefficient"):
        ledger["abstract_coefficient_convergence"] = coefficient_audit()
    if mode in ("all", "gauge-q"):
        ledger["shore_gauge_and_physical_q_no_go"] = gauge_q_audit()
    if mode in ("all", "typed"):
        ledger["typed_direct_sum_counterguard"] = typed_terminal_audit()
    if mode == "all":
        ledger["theorem"] = (
            "h3 shared-loop / balanced-Eq cross-frontier typed convergence gate"
        )
        ledger["verdict"] = (
            "The delta combination is exact only for four copies of the "
            "unconstructed shared-loop correction: after an abstract "
            "six-label-to-four-corner projection their sum is Eq=-delta.  The "
            "strongest audited near-hits instead give B=Eq=delta, even after "
            "granting unproved labelwise residue sections. Shore gauge and the "
            "physical q identity preserve that tie and have zero chi.  Gate I "
            "and the balanced cap have different literal word/fine/repeated/"
            "operation idempotents, so the abstract projection is not a source "
            "map.  The apparent convergence is a projection coincidence; its "
            "promotion is precisely the missing source-labelled kappa_mix "
            "placement column."
        )
        ledger["scope"] = (
            "exact rational coefficient identity, full committed Gate-I "
            "near-hit provenance, balanced B/Eq quotient, shore gauge, q row, "
            "and literal multigrade tags.  The read-only external report is "
            "used only as the hypothesis being audited and is not edited."
        )
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if mode == "all" and EXPECTED_DIGEST != "TO_BE_FROZEN":
        require(digest == EXPECTED_DIGEST,
                ("cross-frontier convergence ledger changed", digest))
    print(f"h3 cross-frontier Eq convergence gate ({mode}): PASS")
    if mode in ("all", "provenance"):
        print("literal Gate-I and Gate-II source grades: DISTINCT")
    if mode in ("all", "coefficient"):
        print("delta Eq identity uses missing corrections, not strongest near-hits")
    if mode in ("all", "gauge-q"):
        print("near-hit + shore gauge + physical q: chi=0")
    if mode in ("all", "typed"):
        print("common physical column: NOT CONSTRUCTED (kappa_mix placement)")
    print("ledger_sha256=" + digest)
    return digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "provenance", "coefficient", "gauge-q", "typed"),
        default="all",
    )
    arguments = parser.parse_args()
    run(arguments.mode)


if __name__ == "__main__":
    main()
