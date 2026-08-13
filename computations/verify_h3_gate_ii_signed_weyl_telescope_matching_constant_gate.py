#!/usr/bin/env python3
"""Audit the all-pair signed-Weyl telescope in the Gate-II quotient.

Pair the eight sites and apply a signed simultaneous Weyl transformation on
each pair.  The usual telescoping sum of physical Cartan homotopies is target
safe because the total signed Weyl fixes the ternary diagonal tensor.

The operation acts only on colour decorations.  It fixes every underlying
perfect matching, repeated-edge tag, and H2 chart tag.  Consequently its
marked-pair root character has the tensor form chi_w x 1_match.  Gate II
needs chi_w x (2A-B-C)H, whose matching factor is centered.  The constant
matching factor is annihilated by both the L01 coefficient covector and the
downstream word-0102 private detector.  Multiplying the telescope by the
centered matching projector is exactly the missing t_L/L01 carrier landing,
not a free source-provenant operation.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gate_ii_cartan_full_q_pointed_character_gate.py":
        "6f791c41e743a94279ccf9e4924af11a42c278baa7737a5eed108bf85136f499",
    "computations/verify_h3_gate_ii_chiw_chart_complete_h2_face.py":
        "a80e5ec2a1aaa90814b412d13b1c7981f345bb41ca5a5450d5361ae2bc9f5773",
    "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py":
        "59babf6e706973f2eaa8a8fdd7cdb624ddf88560c08243c5fcd05c3a5425a5d7",
    "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py":
        "8ec18f05034b6483512644c49d0009b4b166b0d6b978f6895195321ca9d8417a",
    "notes/h3-tau-plus-connected-sl3-label-orbit-obstruction.md":
        "7272f6da284e6705ae68fdb533f47bdef3d8181fafefcb63984b56f6a08ce6bf",
    "computations/verify_uniform_hybrid_to_pure_cartan_rectangle_cancellation.py":
        "4edfead0410149e871d396fb0d29f232b5e7c73e91f61691a499b96827633244",
}
EXPECTED_LEDGER_SHA256 = (
    "68ba278b9683c123a69f263e7ef8ce8750bb3354c6e29c893fc8751dede178ea"
)


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


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def signed_weyl_matrix():
    # Basis (c,i,k).  w e_c=-e_i, w e_i=e_c, w e_k=e_k.
    return (
        (Q(0), Q(1), Q(0)),
        (Q(-1), Q(0), Q(0)),
        (Q(0), Q(0), Q(1)),
    )


def matvec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def kronecker_action(matrix, left, right):
    left_image = matvec(matrix, left)
    right_image = matvec(matrix, right)
    return tuple(a * b for a in left_image for b in right_image)


def pair_target_audit() -> dict[str, object]:
    w = signed_weyl_matrix()
    basis = tuple(tuple(Q(row == column) for row in range(3))
                  for column in range(3))
    c, i, k = basis
    cc = tuple(a * b for a in c for b in c)
    ii = tuple(a * b for a in i for b in i)
    kk = tuple(a * b for a in k for b in k)
    require(kronecker_action(w, c, c) == ii
            and kronecker_action(w, i, i) == cc
            and kronecker_action(w, k, k) == kk,
            "the signed pair Weyl stopped fixing the pair diagonal")

    pair_delta = tuple(a + b + c0 for a, b, c0 in
                       zip(cc, ii, kk, strict=True))
    transformed = tuple(a + b + c0 for a, b, c0 in zip(
        kronecker_action(w, c, c), kronecker_action(w, i, i),
        kronecker_action(w, k, k), strict=True
    ))
    require(transformed == pair_delta,
            "the pair signed Weyl stopped fixing Delta")
    return {
        "signed_Weyl": "w e_c=-e_i, w e_i=e_c, w e_k=e_k",
        "pair_action": ["cc -> ii", "ii -> cc", "kk -> kk"],
        "pair_Delta_fixed": True,
        "all_pair_product_fixes_global_Delta": True,
        "Cartan_telescope": (
            "H_W=sum_j P_(j-1) h_j, with dH_W+H_Wd=product_j W_j-1"
        ),
        "target_safe": True,
    }


def matching_constant_gate(curvature, p2) -> dict[str, object]:
    matchings, directions, tails, l01_values, r01_values, ah_values = (
        curvature.polynomial_data()
    )
    order = tuple(matchings)
    complete = (Q(1),) * len(order)
    l01 = tuple(Q(l01_values.get(matching, 0)) for matching in order)
    r01 = tuple(Q(r01_values.get(matching, 0)) for matching in order)
    require(len(order) == 105 and sum(l01, Q(0)) == 0
            and dot(complete, l01) == 0
            and rank((complete, l01, r01)) == 3,
            "the matching-constant/centered quotient changed")

    # On the three local H2 charts, the same obstruction is visible in its
    # minimal factor: the telescope has 1_3 and Gate II needs (2,-1,-1).
    local_constant = tuple(map(Q, (1, 1, 1)))
    local_root_even = tuple(map(Q, (2, -1, -1)))
    local_endpoint_odd = tuple(map(Q, (0, 1, -1)))
    require(dot(local_constant, local_root_even) == 0
            and dot(local_endpoint_odd, local_root_even) == 0
            and rank((local_constant, local_endpoint_odd,
                      local_root_even)) == 3,
            "the local chart character split changed")

    # The word-0102 occurrence-private detector also kills constants.
    p2_ledger, p2_digest = p2.audit()
    require(p2_digest == p2.EXPECTED_LEDGER_SHA256,
            "the P2 placement ledger changed")
    representative = tuple(map(Q, p2_ledger["one_endpoint_Hasse_faces"]
                               ["representative_occurrence_vector"]))
    detector = tuple(Q(index in (0, 3)) - Q(index in (1, 6))
                     for index in range(len(representative)))
    require(sum(detector, Q(0)) == 0
            and dot(detector, (Q(1),) * len(detector)) == 0
            and dot(detector, representative) == Q(-13, 6),
            "the 0102 private detector changed")
    return {
        "complete_matching_occurrences": len(order),
        "telescope_matching_factor": "1_105",
        "Gate_II_required_matching_factor": "L01=(2A-B-C)H",
        "L01_augmentation": str(sum(l01, Q(0))),
        "constant_pairing_with_L01": str(dot(complete, l01)),
        "local_chart_factors": {
            "telescope": [1, 1, 1],
            "endpoint_odd_Cartan": [0, 1, -1],
            "Gate_II_root_even": [2, -1, -1],
            "rank": 3,
        },
        "word_0102": {
            "telescope_occurrence_factor": "1_12",
            "private_detector": "+e0+e3-e1-e6",
            "detector_on_telescope": "0",
            "detector_on_required_private_face": "-13/6",
        },
        "consequence": (
            "the all-pair companions cancel the target defect only in the "
            "matching-constant summand; they do not construct L01, R01, or "
            "the occurrence-private 0102 section"
        ),
    }


def physical_provenance_gate() -> dict[str, object]:
    return {
        "colour_action_preserves": [
            "underlying site matching", "matching index",
            "repeated-edge label", "H2 direction-pair tag",
        ],
        "connected_SL3_or_Weyl_changes_B_label": False,
        "complete_Cartan_rectangles_over_matchings": (
            "cancel pairwise in the complete response row"
        ),
        "project_to_centered_matching_component_requires": (
            "a physical occurrence/block projector or relative carrier"
        ),
        "multiplying_H_W_by_L01_or_Pf_is_source_provenant": False,
        "reason": (
            "such multiplication selects a proper matching-occurrence "
            "component of a cancelling complete prism; the needed splitter "
            "is exactly the Gate-II t_L-L01/t_R-R01 comparison"
        ),
        "relation_to_relative_Tate_gate": (
            "the telescope can decorate a correctly landed carrier by the "
            "missing root character, but cannot land that carrier"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    character = load(
        "computations/verify_h3_gate_ii_cartan_full_q_pointed_character_gate.py",
        "signed_telescope_character",
    )
    chart = load(
        "computations/verify_h3_gate_ii_chiw_chart_complete_h2_face.py",
        "signed_telescope_chart",
    )
    curvature = load(
        "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py",
        "signed_telescope_curvature",
    )
    p2 = load(
        "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py",
        "signed_telescope_p2",
    )
    character_ledger, character_digest = character.audit()
    chart_ledger, chart_digest = chart.audit()
    require(character_digest == character.EXPECTED_LEDGER_SHA256
            and chart_digest == chart.EXPECTED_LEDGER_SHA256
            and character_ledger["V4_pointed_character"]
                ["unique_missing_character_after_endpoint_grant"] == "chi_w"
            and chart_ledger["chart_character"]
                ["chi_w_endpoint_even"] == [2, -1, -1],
            "the Gate-II root-character frontier changed")
    ledger = {
        "theorem": "h3 Gate-II signed-Weyl telescope matching-constant gate",
        "pins": PINS,
        "target_telescope": pair_target_audit(),
        "matching_occurrence_quotient": matching_constant_gate(curvature, p2),
        "physical_provenance": physical_provenance_gate(),
        "verdict": (
            "The all-pair signed-Weyl Cartan telescope is a valid target-safe "
            "source homotopy and supplies the missing pure root character at "
            "the complete matching-aggregate level.  Every term preserves "
            "the matching and repeated labels, so its occurrence factor is "
            "constant.  Gate II requires the independent centered factor "
            "(2A-B-C)H.  The L01 covector and the word-0102 private detector "
            "both annihilate the telescope.  Projecting or multiplying the "
            "telescope into that factor is precisely the unconstructed "
            "pointed/block carrier comparison and is circular"
        ),
        "positive_use": (
            "after the matching-centered carrier is physically landed, the "
            "signed-Weyl telescope supplies its target-safe chi_w colour "
            "decoration; it removes the separate global target-correction "
            "problem, not the carrier landing"
        ),
        "scope": (
            "exact signed pair Weyl action, canonical K8 occurrence quotient, "
            "and literal 0102 private block.  No claim is made that a "
            "complete GHZ source realizes the missing centered carrier"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("signed-Weyl telescope ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("freeze EXPECTED_LEDGER_SHA256=" + digest)
        return
    print("all-pair signed Weyl telescope: TARGET-SAFE")
    print("marked root character: chi_w AT MATCHING-CONSTANT LEVEL")
    print("pairing with L01: ZERO")
    print("word-0102 private detector: ZERO")
    print("pointed/block projector: NOT CONSTRUCTED")
    print("post-landing chi_w decoration: AVAILABLE")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
