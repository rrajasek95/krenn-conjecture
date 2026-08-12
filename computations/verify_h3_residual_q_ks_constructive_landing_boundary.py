#!/usr/bin/env python3
"""Conditional constructive landing of the residual-q KS attachment.

Assume the exact residual-q Kodaira--Spencer lift isolated by 43b6038 and
made physically sharp by 0e4d7f8: in the labelled repeated comparison grade
it cancels the pure-11 versus mixed-21|12 residue mismatch, has
W/target/anchor readouts zero, obeys the facewise eta comparison law, and
turns the mixed-curvature-minus-rootless-bar near-hit into

    A = E_plus-E_minus+Omega-q_comp.

This checker proves the strongest consequences which use only that exact
hypothesis.  Modulo the existing bar, A supplies D=E_plus-E_minus.  It kills
the unequal-tail endpoint holonomy of 727de71 and, with the existing
signless E14 response S, writes the private orientation as (S+D)/2.  Thus
the E14 first-hit self-loop is closed in its routed endpoint quotient.

The attachment does not by itself supply transverse physical rank: its
target and anchor readouts are zero, and the independent-tail/local-parallel
rank guard remains (2,2,3,3).  Its sound well-founded effect is instead a
typed-component decrease at fixed endpoint support.  The first downstream
guards are the target-family coloop / same-head local-rank restoration and,
on the opposite Hall-star route, the bridge-dark or three-block triangle.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_bidirectional_five_lock_relative_homotopy_boundary.py":
        "aeed58d596f931602dcb77b44aa3bd11a27b8e2d26435cc328b325ce91b0e1bb",
    "computations/verify_h3_shared_four_term_endpoint_word_change_inventory_boundary.py":
        "00db2478df3162a374434ea7d0ab285f770510d33b72619377560404c96b16e8",
    "computations/verify_h3_reciprocal_response_rootless_attachment_parity_gate.py":
        "13aef43505fa09d3c43cf0098598dc62a690598759637820a29672d195139d71",
    "computations/verify_h3_c6_endpoint_visibility_augmented_map_gate.py":
        "589d88020b87c5892be832758c74c73832747c265f4139b6917069685dcd9375",
    "computations/verify_uniform_axis_circuit_third_component_rank_guard.py":
        "d9e852bad1b94c1918523fa834029abff04f4c288bde2f97c790def1bef2644f",
    "computations/verify_uniform_axis_circuit_target_coloop_full_five_boundary.py":
        "4e84ec46bac4b9b97a69dbfa61899877c5b09f3960bf666af1ddf1ade01c54d6",
    "computations/verify_uniform_multisite_hall_star_triangle_bridge_boundary.py":
        "99c2c0038fefd0da51ff46bbf4d29ab6c8cfb72a79c1acf74e6334e9b4fd239e",
    "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py":
        "893f000e37e4bcfc78973cb042cc0858087cb25605d6cf070a1bf8dfa7a76b7a",
    "computations/verify_h3_residual_q_physical_duality_interface_counterguard.py":
        "6f7fa68eb081a1dd3c3754cff5e1974e54c4df81c8ce6d36ffe8d37efba953ba",
}
EXPECTED_LEDGER_SHA256 = "7acff9f5d9ad080d988ad914430a1087b106733cf710f4b901646b0f55b730bb"

FEATURES = (
    "E_plus", "E_minus", "Omega", "q_comp",
    "ores_pure_plus", "ores_pure_minus",
    "ores_mixed_plus", "ores_mixed_minus",
    "W", "target", "ainc",
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def vector(**entries):
    require(set(entries) <= set(FEATURES), ("unknown features", entries))
    return tuple(Q(entries.get(feature, 0)) for feature in FEATURES)


def add(*vectors):
    return tuple(sum(values, Q(0)) for values in zip(*vectors, strict=True))


def scale(value, source):
    return tuple(Q(value) * entry for entry in source)


def rank(rows):
    matrix = [[Q(entry) for entry in row] for row in rows]
    if not matrix:
        return 0
    columns = len(matrix[0])
    require(all(len(row) == columns for row in matrix), "ragged matrix")
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def in_row_span(rows, target):
    return rank(list(rows)) == rank(list(rows) + [tuple(target)])


def audit_exact_ks_hypothesis(inventory, parity, physical_interface):
    curvature = inventory.curvature_kodaira_spencer_audit()
    mismatch = tuple(curvature["combined_candidate"]["residue_vector"])
    require(mismatch == (1, -1, -1, 1)
            and not curvature["combined_candidate"]["residue_zero"],
            "the residual-tail mismatch changed")
    parity_gate = parity.parity_and_residue_gate()
    require(parity_gate["after_reduced_residue_correction"]
            == ["1", "-1", "1", "-1", "0", "0"],
            "the oriented attachment signature changed")
    stabilizer = physical_interface.physical_stabilizer_promotion_gate()
    completion = physical_interface.completion_counterguard()
    require(stabilizer["needed_terminal_comparison_law"].startswith(
                "d r_v(eta_z)=-d Omega_v(eta_z)")
            and completion["completion_with_one_KS_source"]["branch"]
                == "zero_indeterminate_lift"
            and completion[
                "completion_with_two_KS_sources_and_terminal_difference"
            ]["branch"] == "kernel_relative_generator",
            "the physical residual-q interface changed")

    # The curvature-minus-bar candidate already has the four geometric
    # boundary entries A and carries only the four displayed residue corners.
    near_hit = vector(
        E_plus=1, E_minus=-1, Omega=1, q_comp=-1,
        ores_pure_plus=1, ores_pure_minus=-1,
        ores_mixed_plus=-1, ores_mixed_minus=1,
    )
    # This is the exact residual-q KS hypothesis: it transports the two
    # decorated tails by cancelling the primitive residue mismatch and has
    # every protected readout zero.
    ks_correction = vector(
        ores_pure_plus=-1, ores_pure_minus=1,
        ores_mixed_plus=1, ores_mixed_minus=-1,
    )
    attachment = add(near_hit, ks_correction)
    expected = vector(E_plus=1, E_minus=-1, Omega=1, q_comp=-1)
    require(attachment == expected,
            "the exact residual-q correction stopped constructing A")
    require(all(attachment[FEATURES.index(readout)] == 0
                for readout in ("W", "target", "ainc")),
            "a protected attachment readout became nonzero")
    require(all(attachment[FEATURES.index(readout)] == 0 for readout in (
        "ores_pure_plus", "ores_pure_minus",
        "ores_mixed_plus", "ores_mixed_minus",
    )), "the ordinary-residue mismatch was not cancelled")
    return {
        "status": "HYPOTHESIS, not constructed by this checker",
        "feature_order": list(FEATURES),
        "curvature_minus_bar_near_hit": [str(value) for value in near_hit],
        "required_KS_correction": [str(value) for value in ks_correction],
        "corrected_attachment_A": [str(value) for value in attachment],
        "tail_transport": "a24:11*a35:11 -> a24:21*a35:12",
        "protected_readouts_W_target_ainc": [0, 0, 0],
        "ordinary_residue_after_correction": [0, 0, 0, 0],
        "physical_source_condition": (
            "the correction is a column of the complete source-labelled "
            "augmented map in word 1211222 and the labelled repeated P3+K2 "
            "grade, including all eta_z relations and a physical terminal row"
        ),
        "required_eta_comparison":
            stabilizer["needed_terminal_comparison_law"],
        "terminal_alternative": (
            "zero-indeterminate lift and kernel-relative-generator branches "
            "both supply the endpoint attachment; the latter is already a "
            "stronger terminal exit"
        ),
    }


def audit_unequal_tail_holonomy_closure(relative):
    guard = relative.audit_all_five_row_holonomy_guard()
    require(guard["equal_tail_spans_D"]
            and not guard["unequal_tail_spans_D"]
            and guard["unequal_tail_endpoint_dual"] == ["1", "1/2"],
            "the unequal-tail holonomy guard changed")

    labels = tuple(guard["row_labels"])
    weights = [(Q(1), Q(1)) for _label in labels]
    weights[3] = (Q(1), Q(2))
    rows = relative.path_rows(tuple(weights))
    D = tuple(Q(int(index == 0) - int(index == len(labels)))
              for index in range(len(labels) + 1))
    require(rank(rows) == len(labels)
            and not in_row_span(rows, D)
            and rank(rows + (D,)) == len(labels) + 1,
            "the KS endpoint column stopped killing the holonomy cokernel")
    return {
        "all_five_row_labels": list(labels),
        "before_KS_row_rank": rank(rows),
        "before_KS_ambient_dimension": len(D),
        "before_KS_endpoint_dual": guard["unequal_tail_endpoint_dual"],
        "D_in_old_row_span": False,
        "after_adjoining_A_mod_bar_rank": rank(rows + (D,)),
        "remaining_relative_cokernel_dimension": 0,
        "source_valid_reason": (
            "the hypothesized A and the already physical rootless bar have "
            "the same repeated fine grade and protected readouts, so A+B "
            "is the literal endpoint difference D rather than a formal "
            "rescaling of the unequal path"
        ),
    }


def audit_e14_self_loop_closure(inventory, e14):
    response = inventory.complete_response_and_unary_search()
    require(response["unique_hit_endpoint_coefficients"] == [1, 1]
            and response["correct_private_tail_response_hits"] == 1,
            "the unique E14 signless tail hit changed")
    first_ledger, first_digest = e14.audit()
    require(first_digest == e14.EXPECTED_LEDGER_SHA256,
            "the E14 first-hit replay changed")
    first = first_ledger["canonical_first_reduction"]
    require(first["target_augmented_first_hit_rank_Q"] == 269
            and first["rational_dual_pairing"] == "-1",
            "the E14 first-hit self-loop obstruction changed")

    S = (Q(1), Q(1))
    D = (Q(1), Q(-1))
    E_plus = (Q(1), Q(0))
    E_minus = (Q(0), Q(1))
    require(add(scale(Q(1, 2), S), scale(Q(1, 2), D)) == E_plus
            and add(scale(Q(1, 2), S), scale(Q(-1, 2), D)) == E_minus,
            "S,D stopped splitting the endpoint orientations")
    require(rank((S,)) == 1 and rank((S, D)) == 2,
            "the E14 endpoint quotient rank gain changed")
    return {
        "canonical_private_monomial": first["private_monomial"],
        "unary_local_unit_factor": first["unary_unit_factor"],
        "old_first_hit_columns": first[
            "target_augmented_first_hit_column_count"],
        "old_first_hit_rank_Q": first["target_augmented_first_hit_rank_Q"],
        "old_private_dual_pairing": first["rational_dual_pairing"],
        "correct_tail_old_response": "S=E_plus+E_minus",
        "KS_mod_bar_response": "D=E_plus-E_minus",
        "private_orientation_formula": "E_plus=(S+D)/2",
        "transposed_orientation_formula": "E_minus=(S-D)/2",
        "endpoint_quotient_rank_before_after": [1, 2],
        "verdict": (
            "over the complex source field the private endpoint generator "
            "is in the routed source-row span, so reduction cannot return "
            "a surviving copy of the same E14 orientation"
        ),
        "scope": (
            "closure in the routed endpoint/tail quotient under the exact "
            "KS hypothesis; not a reconstruction of the full Spencer lift"
        ),
    }


def audit_well_founded_effect(endpoint_gate):
    potential = endpoint_gate.audit_conditional_sequential_potential()
    require(potential["potential"]
            == "(endpoint support, unresolved typed components)",
            "the conditional sequential potential changed")
    records = []
    for support in range(1, 9):
        for components in range(1, 9):
            before = (support, components)
            after = (support, components - 1)
            require(after < before,
                    "a KS typed attachment stopped decreasing lex order")
            records.append((before, after))
    return {
        "potential": potential["potential"],
        "KS_move": (
            "adjoin one source-typed endpoint/tail attachment at fixed "
            "physical endpoint support"
        ),
        "state_change": "(s,c)->(s,c-1)",
        "strict_decrease": True,
        "finite_state_checks": len(records),
        "E14_self_loop_change": "(s,1)->(s,0) in its routed orbit",
        "not_claimed": [
            "no physical source coefficient is deleted by the attachment",
            "the KS correction may use repeated-grade chain coordinates",
            "rank-(3,3,3,3) is not a consequence of this potential decrease",
        ],
    }


def audit_rank_and_hall_boundary(rank_guard, coloop, triangle):
    local = rank_guard.audit_order(3)
    require(local["deleted_star_profile"] == [2, 2, 3, 3]
            and local["outer_head_span_rank"] == 1
            and local["response_column_rank"] == 3,
            "the local transverse-rank guard changed")
    coloop_guard = coloop.audit_full_five_boundary()
    require(coloop_guard["column_ranks"] == [3, 3]
            and coloop_guard["joint_kernel_dimensions"] == [0, 0]
            and coloop_guard["pure_target_port_supports"]
            == {"X1": [0], "X2": [0]},
            "the full-five target-coloop guard changed")
    bridge = triangle.audit_bridge_or_dark_statement()
    three_block = triangle.audit_three_block_reduction()
    require("exact bridge-dark guard" in bridge["zero_branch"]
            and three_block["exact_row"] == "B_ab+A_Rc+A_Pc=0",
            "the opposite Hall-star residual changed")

    # A has target=anchor=0.  Therefore the hypothesis alone names no new
    # nonzero pure target matching and no physical deleted-star column.  The
    # two endpoint orientations S,D are independent, but their independence
    # lives in the response/source-word factor and does not alter the local
    # rank matrix frozen by the guard.
    S, D = (Q(1), Q(1)), (Q(1), Q(-1))
    require(rank((S, D)) == 2
            and local["deleted_star_profile"] == [2, 2, 3, 3],
            "formal endpoint splitting unexpectedly changed local rank")
    return {
        "what_KS_supplies": {
            "endpoint_orientation_rank": rank((S, D)),
            "target_readout": 0,
            "anchor_incidence_readout": 0,
            "new_avoiding_pure_matching": False,
            "new_physical_deleted_star_column": False,
        },
        "sharp_local_rank_guard": {
            "complete_response_tail_rank": local["response_column_rank"],
            "outer_head_span_rank": local["outer_head_span_rank"],
            "deleted_star_profile": local["deleted_star_profile"],
            "needed": (
                "a source-labelled occupied tail on a transverse local outer "
                "head, with nonzero cofactor and both missing rank-three minors"
            ),
        },
        "outside_arm_rank_guard": {
            "name": "target-family coloop",
            "full_five_column_ranks": coloop_guard["column_ranks"],
            "joint_kernel_dimensions":
                coloop_guard["joint_kernel_dimensions"],
            "pure_target_port_supports":
                coloop_guard["pure_target_port_supports"],
            "needed": (
                "an avoiding nonzero pure target matching or an additional "
                "physical source column which raises both deficient stars"
            ),
        },
        "anchor_contained_Hall_guard": {
            "name": "opposite Hall-star bridge-dark/triangle lock",
            "dark_branch": bridge["zero_branch"],
            "three_block_row": three_block["exact_row"],
            "needed": (
                "exclude unary-cofactor bridge darkness or straighten one "
                "anchor correction into a free/effective carrier"
            ),
        },
        "logical_scope": (
            "the rank and coloop examples are exact structural modules, not "
            "full GHZ sources.  They prove that the stated KS boundary and "
            "readouts alone do not imply transverse rank; a full-source "
            "incidence theorem may still exclude them"
        ),
    }


def main():
    pin_dependencies()
    relative = load(
        "computations/verify_uniform_bidirectional_five_lock_relative_homotopy_boundary.py",
        "ks_landing_relative",
    )
    inventory = load(
        "computations/verify_h3_shared_four_term_endpoint_word_change_inventory_boundary.py",
        "ks_landing_inventory",
    )
    parity = load(
        "computations/verify_h3_reciprocal_response_rootless_attachment_parity_gate.py",
        "ks_landing_parity",
    )
    endpoint_gate = load(
        "computations/verify_h3_c6_endpoint_visibility_augmented_map_gate.py",
        "ks_landing_endpoint_gate",
    )
    rank_guard = load(
        "computations/verify_uniform_axis_circuit_third_component_rank_guard.py",
        "ks_landing_rank_guard",
    )
    coloop = load(
        "computations/verify_uniform_axis_circuit_target_coloop_full_five_boundary.py",
        "ks_landing_coloop",
    )
    triangle = load(
        "computations/verify_uniform_multisite_hall_star_triangle_bridge_boundary.py",
        "ks_landing_triangle",
    )
    e14 = load(
        "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py",
        "ks_landing_e14",
    )
    physical_interface = load(
        "computations/verify_h3_residual_q_physical_duality_interface_counterguard.py",
        "ks_landing_physical_interface",
    )

    ledger = {
        "pins": PINS,
        "exact_residual_q_KS_hypothesis":
            audit_exact_ks_hypothesis(inventory, parity, physical_interface),
        "unequal_tail_five_lock":
            audit_unequal_tail_holonomy_closure(relative),
        "E14_private_self_loop": audit_e14_self_loop_closure(inventory, e14),
        "well_founded_constructive_effect":
            audit_well_founded_effect(endpoint_gate),
        "first_remaining_rank_and_Hall_guards":
            audit_rank_and_hall_boundary(rank_guard, coloop, triangle),
        "conditional_theorem": (
            "assuming the exact residual-q KS lift in every selected marked "
            "tail orbit, the curvature/bar near-hit becomes the physical "
            "four-term attachment A.  Modulo the existing bar this adjoins "
            "D=E_plus-E_minus, kills the one-dimensional unequal-tail "
            "five-lock holonomy, and with the signless E14 response writes "
            "the private orientation as (S+D)/2.  The attachment preserves "
            "endpoint support and strictly decreases the number of unresolved "
            "typed components.  It does not by itself produce a transverse "
            "physical head, avoiding pure matching, or rank-(3,3,3,3) pair"
        ),
        "fastest_downstream_target": (
            "prove source-labelled local rank restoration after the KS "
            "attachment: an occupied common-tail carrier either meets an "
            "avoiding pure target matching, supplies a transverse outer head "
            "with both deficient rank-three minors, or enters the effective "
            "strict Hall envelope.  The exact residual alternatives are the "
            "target-family coloop / same-head (2,2,3,3) carrier and the "
            "opposite Hall-star bridge-dark/three-block triangle lock"
        ),
        "scope": (
            "conditional source-valid landing theorem, not a construction of "
            "the KS lift and not a full-source rank theorem.  The theorem "
            "closes the endpoint/tail provenance residual and identifies, "
            "without eliding it, the next independent physical incidence gate"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"residual-q KS landing ledger changed: {digest}")
    print("h3 residual-q KS constructive landing: CONDITIONAL PASS")
    print("unequal-tail five-lock holonomy: CLOSED under KS")
    print("E14 first-hit endpoint self-loop: CLOSED under KS")
    print("strict effect: unresolved typed components decrease at fixed support")
    print("transverse physical rank: NOT implied")
    print("next: target-coloop/same-head rank restoration or Hall triangle lock")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
