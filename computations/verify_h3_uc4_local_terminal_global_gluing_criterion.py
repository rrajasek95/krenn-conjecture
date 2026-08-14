#!/usr/bin/env python3
"""Glue the exhaustive four-site U_C4 terminal to the h=3 window.

The four-site checker has a 127-row local map of rank 126 and normalized
terminal

    Psi_loc = (1/12) sum_{corner,matching} delta_corner (B-Eq).

This checker embeds the canonical 27-row AugP2 cap packet into that raw
three-matching model and verifies that its normalized cap character is
literally the pullback of Psi_loc.  It then compares Psi_loc with the
normalized fixed-window L=(2,-1,-1) detector.  The top and mandatory
direction normalizations agree (1 and 2 respectively) only for a
private-only placement; the physical h2 response gives a tied B=Eq
placement and has value zero.

Finally, it freezes the exact global extension criterion.  Extending
Psi_loc by zero over all off-grade response/collision blocks is a terminal
iff every missing cross-grade column has zero local mismatch.  All typed
collision/PP companions satisfy this, but the selected db01 comparison,
the dL01 placement, and the response-to-AugP2 mixed incidence have not been
constructed.  Thus the criterion is one explicit gluing hypothesis, not a
claim that the full physical map is already exhaustive.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py":
        "6c42cd4dc7dca1544dc0b675f5f4543ec348f1fba34b7ea14bf80cc6a20b9cf1",
    "computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py":
        "262e1dd08dd1842d60515d45aea53ea406d7e1e5ea55ab506bb6e81d64b07741",
    "computations/verify_h3_balanced_square_private_eq_projection_gate.py":
        "bbfb690a73844169574351ad019171a6d9c5fe332e59cc9694a1f67dcf31cf8e",
    "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py":
        "2ac01c9ba571338b4c7b779dbc70d5d0eaacb2fe01a4035833970fa6b9826fe0",
    "computations/verify_h3_closed_cycle_private_eq_collision_pp_exit_gate.py":
        "fe786e2ca7455b0a145857679037ec79a5cd0669ed3755e1d490aedc5bd8965e",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py":
        "d5628f66ffbf94e2de37318ab136adda96af5e114e2bea8dce22542ec9f30cb1",
    "computations/verify_h3_db01_dl01_literal_private_eq_conservation_gate.py":
        "1a27b00d28be6334a27e0603a0ef776367d3c71b6f8fa45d3005963f8dff4c6c",
}
EXPECTED_LEDGER_SHA256 = (
    "23704e9c056227f171bca411d82f3e0f841f6b86f4ff9ae6fc3da23c6c1552c9"
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


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def rank(columns) -> int:
    columns = tuple(columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
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


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def local_columns(local):
    named = (local.top_projection_columns()
             + local.lower_face_and_reinsertion_columns()
             + local.external_augmented_columns())
    return tuple(value for _name, value in named)


def lift_aggregated_cap_to_local(local, cap_vector):
    """Lift 4-corner cap coordinates to all three matching occurrences."""
    require(len(cap_vector) == 27, "cap width")
    output = [Q(0)] * len(local.LABELS)
    # Cap order: B[4], Eq[4], target[4], W[4], ores[4], seven scalars.
    for block, start in (("B", 0), ("Eq", 4)):
        for corner in range(4):
            for matching in range(3):
                output[local.INDEX[local.top_label(block, corner, matching)]] \
                    += Q(cap_vector[start + corner])
    for family, start in (("target", 8), ("W", 12), ("ores", 16)):
        for corner in range(4):
            output[local.INDEX[f"{family}:{corner}"]] += Q(
                cap_vector[start + corner])
    for label, index in (("M", 20), ("ainc", 21), ("q", 22),
                         ("P_f", 23), ("ridge", 24), ("eta", 25),
                         ("sigma", 26)):
        output[local.INDEX[label]] += Q(cap_vector[index])
    return tuple(output)


def cap_embedding_audit(local, maximal, private_eq):
    values = local_columns(local)
    local_dual = scale(Q(1, 12), local.integral_terminal_dual())
    cap_columns, cap_dual, cap_data = maximal.augmented_private_eq_block(
        private_eq)
    lifted = tuple(lift_aggregated_cap_to_local(local, column)
                   for column in cap_columns)

    # The equality holds on every basis vector, not just named columns.
    basis = tuple(tuple(Q(1) if row == column else Q(0)
                        for row in range(27)) for column in range(27))
    require(rank(values) == 126
            and all(dot(local_dual, lift_aggregated_cap_to_local(local, e))
                    == dot(cap_dual, e) for e in basis)
            and all(dot(local_dual, column) == 0 for column in lifted)
            and rank(values + lifted) == 126,
            "the canonical cap embedding changed the local terminal")
    return local_dual, values, {
        "raw_local_coordinates": len(local.LABELS),
        "raw_local_rank": rank(values),
        "aggregated_cap_coordinates": 27,
        "canonical_lift": (
            "each B_c and Eq_c is repeated on all three C4 matching "
            "occurrences; target/W/ores and scalar augmentations map identically"
        ),
        "character_identity_on_all_27_basis_vectors": (
            "Psi_loc after lift = delta.(B-Eq)/4"
        ),
        "named_cap_columns": len(cap_columns),
        "rank_after_lifting_all_named_cap_columns": rank(values + lifted),
        "named_cap_projection_rank": cap_data["B_Eq_projection_rank"],
    }


def fixed_window_comparison_audit(local, local_dual, k22):
    columns, detector, candidate_h, candidate_r, packet = (
        k22.audit_cartesian_physical_packet())
    window_dual = scale(Q(1, 6), detector)
    k22.audit_direction_routing(detector, candidate_h, candidate_r)

    top_private = local.balanced_top("B")
    top_tied = local.tied_balanced_top()
    direction_private = local.primitive_direction_face("B")
    direction_tied = local.add(
        direction_private, local.primitive_direction_face("Eq"))
    window_direction = scale(2, candidate_h)

    values = {
        "window_LH": dot(window_dual, candidate_h),
        "window_18_direction": dot(window_dual, window_direction),
        "local_private_top": dot(local_dual, top_private),
        "local_tied_top": dot(local_dual, top_tied),
        "local_private_direction": dot(local_dual, direction_private),
        "local_tied_direction": dot(local_dual, direction_tied),
    }
    require(values == {
        "window_LH": Q(1), "window_18_direction": Q(2),
        "local_private_top": Q(1), "local_tied_top": Q(0),
        "local_private_direction": Q(2), "local_tied_direction": Q(0),
    }, values)

    # For a comparison boundary x_window-y_local, the direct-sum detector
    # extends exactly when the two normalized values agree.
    private_top_bridge = values["window_LH"] - values["local_private_top"]
    tied_top_bridge = values["window_LH"] - values["local_tied_top"]
    private_direction_bridge = (
        values["window_18_direction"] - values["local_private_direction"])
    tied_direction_bridge = (
        values["window_18_direction"] - values["local_tied_direction"])
    require((private_top_bridge, tied_top_bridge,
             private_direction_bridge, tied_direction_bridge)
            == (Q(0), Q(1), Q(0), Q(2)),
            "the window/cap comparison normalization changed")
    return {
        "window_coordinates": packet["physical_output_coordinates"],
        "window_internal_columns": packet["internal_boundary_columns"],
        "window_internal_rank": packet["internal_rank"],
        "normalizations": {key: str(value) for key, value in values.items()},
        "comparison_boundary_values": {
            "LH_minus_private_top": str(private_top_bridge),
            "LH_minus_tied_top": str(tied_top_bridge),
            "18_direction_minus_private_direction":
                str(private_direction_bridge),
            "18_direction_minus_tied_direction": str(tied_direction_bridge),
        },
        "consequence": (
            "a normalized pointed comparison needs the unequal private-only "
            "placement; the physical h2 B=Eq lift cannot compare the nonzero "
            "fixed-window L and direction classes"
        ),
    }


def collision_and_uncovered_audit(collision, packaging, same_grade, maximal,
                                  conservation):
    collision_ledger, collision_digest = collision.audit()
    packaging_ledger, packaging_digest = packaging.audit()
    same_grade_ledger, same_grade_digest = same_grade.audit()
    maximal_ledger, maximal_digest = maximal.audit()
    conservation_inputs = conservation.input_ledgers()
    literal = conservation.projection_audit(*conservation_inputs)
    require(collision_digest == collision.EXPECTED_LEDGER_SHA256
            and packaging_digest == packaging.EXPECTED_LEDGER_SHA256
            and same_grade_digest == same_grade.EXPECTED_LEDGER_SHA256
            and maximal_digest == maximal.EXPECTED_LEDGER_SHA256,
            "a global frontier ledger changed")

    exits = collision_ledger["collision_and_one_hole_exits"]
    breaker = collision_ledger["first_untyped_breaker"]
    word = packaging_ledger["literal_word_and_fine_map"]
    augmented = packaging_ledger["augmented_packaging"]
    downstream = same_grade_ledger["downstream_word_0102"]
    maximal_projection = maximal_ledger[
        "typed_projection_and_first_unmodeled_family"]
    require(exits["all_24_one_hole_values"] == ["0"]
            and breaker["B_Eq_projection_constructed"] is False
            and word["word_hamming_distance"] == 6
            and not word["cap_word_in_existing_D4_cube"]
            and not augmented["existing_AugP2_status"]
                ["constructed_literal_source_object"]
            and downstream["accepted_terminal_status"].startswith("NO")
            and maximal_projection[
                "off_grade_named_columns_with_zero_B_Eq_projection"] == 121
            and literal["chi_on_dL01_packet"] == 0
            and literal["rank_after_db01_and_dL01"] == 7,
            "the typed/dark and untyped/unknown split changed")

    return {
        "verified_dark_or_tied_families": [
            "all 121 named response/intermediate columns while grades remain disjoint",
            "all 24 internal chart/root switches",
            "all 24 shore-gauged absolute one-hole/collision matching repairs",
            "the symmetric collision top and its typed direct-sum first-PP flags",
            "the 30 old/centered/outside distinct C2+/C4/P2 packets",
            "the selected six-term db01 packet in strict typed projection",
            "all eighteen dL01 terms in strict typed projection",
            "all 18 local h2 direction and all 24 tail PP flags when lifted B=Eq",
            "all named AugP2 target/q/anchor/W/ores/ridge/eta/sigma rows",
        ],
        "not_covered_by_any_constructed_cross_grade_map": [
            "both DQ-to-PS chart-switch families A+B and A+C with H-r companions",
            "the word/fine diagonal 11:110000 -> 01211222",
            "the response-to-AugP2 mixed private/reduced-Eq mapping-square incidence",
            "the six P3+K2 plus six sibling 3K2 collision boundary placements",
            "the reduced-Eq/cap descent and gamma=-dOmega, -d(q_xv^01) ridge connection",
            "the downstream word-0102 private section and dq23/q/W/labelled-ridge readout",
        ],
        "strict_db01_and_dL01_status": (
            "literal cap projection zero and chi zero; comparison placement "
            "remains part of the unbuilt mapping cylinder"
        ),
        "first_deciding_unknown": (
            "chi(mixed)=delta.(B(mixed)-Eq(mixed)) for the response-to-AugP2 "
            "mapping-square incidence"
        ),
        "first_post_word_independent_row": augmented[
            "first_post_word_obstruction"],
        "word_fine_obstruction": word["first_required_arrow"],
        "downstream_first_missing_column": downstream["first_missing_column"],
        "all_bare_typed_collision_PP_companions_preserve_chi": True,
        "completed_cross_grade_collision_PP_orbit_proved_to_preserve_chi": False,
        "reason": (
            "the named internal, one-hole, db01, and dL01 packets have zero "
            "strict typed projection, but the mixed response-to-cap "
            "comparison incidence has not been constructed"
        ),
    }


def audit():
    pin_dependencies()
    local = load(
        "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py",
        "uc4_global_local")
    maximal = load(
        "computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py",
        "uc4_global_maximal")
    private_eq = load(
        "computations/verify_h3_balanced_square_private_eq_projection_gate.py",
        "uc4_global_private_eq")
    k22 = load(
        "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py",
        "uc4_global_k22")
    collision = load(
        "computations/verify_h3_closed_cycle_private_eq_collision_pp_exit_gate.py",
        "uc4_global_collision")
    packaging = load(
        "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py",
        "uc4_global_packaging")
    same_grade = load(
        "computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py",
        "uc4_global_same_grade")
    conservation = load(
        "computations/verify_h3_db01_dl01_literal_private_eq_conservation_gate.py",
        "uc4_global_conservation")

    local_dual, _local_values, embedding = cap_embedding_audit(
        local, maximal, private_eq)
    comparison = fixed_window_comparison_audit(local, local_dual, k22)
    frontier = collision_and_uncovered_audit(
        collision, packaging, same_grade, maximal, conservation)
    ledger = {
        "theorem": "h3 U_C4 local terminal global gluing criterion",
        "pins": PINS,
        "canonical_cap_embedding": embedding,
        "fixed_window_to_local_normalized_comparison": comparison,
        "collision_PP_and_global_cross_grade_frontier": frontier,
        "smallest_terminal_promotion_hypothesis": {
            "statement": (
                "For every physical cross-grade column g omitted from the "
                "named direct sum, chi(g)=Psi_loc(pi_local g)=0."
            ),
            "raw_formula": (
                "chi(g)=(1/12) sum_{corner,matching} "
                "delta_corner*(B_corner,matching(g)-Eq_corner,matching(g))"
            ),
            "equivalent_factorization": (
                "because the local map has image ker(Psi_loc), every local "
                "projection pi_local(g) factors through the exhaustive "
                "four-site local boundary map"
            ),
            "why_one_hypothesis_suffices": (
                "all named cap, fixed-window, collision, PP, db01, dL01 and "
                "augmentation families have already been checked in strict "
                "typed projection; only the mixed incidence of the missing "
                "response-to-AugP2 mapping-cylinder orbit remains"
            ),
            "conclusion_if_true": (
                "extend Psi_loc by zero on all off-grade blocks; it is then "
                "an accepted terminal on the exhaustive global map"
            ),
            "conclusion_if_false": (
                "the first g with chi(g)!=0 is the projected rank-raising "
                "physical exit; its remaining word/fine/q/ridge faces must "
                "be totalized"
            ),
        },
        "pointed_comparison_variant": (
            "If one instead glues the nonzero fixed-window detector, each "
            "bridge x-y must satisfy lambda_window(x)=Psi_loc(y).  The "
            "private top/direction placements satisfy 1=1 and 2=2; the tied "
            "h2 placements fail by 1 and 2."
        ),
        "verdict": (
            "Psi_loc embeds literally into the canonical h3 cap map and "
            "kills every currently typed collision/PP companion.  This does "
            "not prove a global B=Eq law: bare db01 and dL01 have now been "
            "proved strictly dark, but the mixed response-to-AugP2 incidence "
            "is unconstructed.  The smallest terminal-promotion hypothesis "
            "is the single factorization condition chi=0 on that missing "
            "mapping-cylinder boundary orbit."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("global gluing ledger changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("Psi_loc -> canonical h3 cap embedding: PASS")
    print("fixed-window/private normalization: top 1=1, direction 2=2")
    print("physical h2 tied lift: top 0, direction 0; NOT A COMPARISON")
    print("typed collision/PP companions: B-Eq DARK")
    print("bare typed db01/dL01: STRICT chi=0")
    print("completed cross-grade orbit: NOT PROVED (mixed incidence absent)")
    print("smallest global hypothesis: chi=0 ON MISSING CROSS-GRADE ORBIT")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
