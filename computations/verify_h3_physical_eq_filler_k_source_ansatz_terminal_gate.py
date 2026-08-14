#!/usr/bin/env python3
"""Test the smallest literal fixed-grade ansatz for the physical Eq filler K.

The formal Hasse/HPL calculation uniquely asks for

    dK = (H_0-u)e_Eq

with occurrence-local q23/q45 proper faces.  This checker does not adjoin K
or retag a formal Hasse cell.  It forms the smallest source-provenant ansatz
from the existing Taylor--Spencer triggers, the two endpoint-even root
sections, cap r0/K_Eq, and mapping cylinders whose input maps already exist.

The first obstruction is categorical and exact: every generator lies in a
diagonal response or cap operation corner, while e_C A e_R is zero.  A
standard mapping cylinder cannot create its own input map.  The desired
off-diagonal coordinate raises operation rank 2 to 3.  The checker then
tracks the same missing constructor through its selected db01, mixed-square,
local B/Eq, q/dq, target, W, residue and ridge projections.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cap_top_sdr_hpl_transfer_no_go.py":
        "dbdf05cbd9bd6244f43d237665665f99f41987f8c3d46a4a88782d6f5333e526",
    "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py":
        "02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
    "computations/verify_h3_first_face_keq_augp2_mixed_square_totalization_gate.py":
        "346f3885bae10462c11f8046240ad4bc5970f0950a25b163235445592be0e9ab",
    "computations/verify_h3_gate_ii_endpoint_even_cap_operator_module_gate.py":
        "39cb3f4b4e83940993ef7ffa8633a3e13cf04631625d9a3729fb5ef9f8ca307c",
    "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py":
        "20646d25c248a39d27a8be29332d85b7995e9091e106fc1026fe343847df5eed",
    "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py":
        "6c42cd4dc7dca1544dc0b675f5f4543ec348f1fba34b7ea14bf80cc6a20b9cf1",
    "computations/verify_h3_cplus_w_yw_cap_factorization.py":
        "0b42e8c7d9e308c93774e59eae030403f3c264e2bfe4b31e7782a0e57b78a506",
    "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py":
        "e5f2664b99c5ba58e0be385ca52dc52c6d2f6d6d0b793e655ebe297542dce291",
}
EXPECTED_LEDGER_SHA256 = "4cdd1dc9dd890be0828878743d7ca6ba2f6154c57b3966337c14ea6055ef0d07"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right) -> Q:
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


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


def literal_operation_corner_ansatz(response_gate, even_gate) \
        -> dict[str, object]:
    response_ledger, response_digest = response_gate.audit()
    require(response_digest == response_gate.EXPECTED_LEDGER_SHA256,
            response_digest)
    even_ledger, even_digest = even_gate.audit()
    require(even_digest == even_gate.EXPECTED_LEDGER_SHA256, even_digest)

    hom = response_ledger["literal_idempotent_Hom"]
    face = response_ledger["first_literal_faces"]
    root_stage = even_ledger["operator_module_residual"][
        "root_operation_stage"]
    section = even_ledger["six_parent_reynolds_section"]
    require(hom["Hom_degree0_response_to_cap_in_current_grammar"] == 0
            and hom["operation_rank_before_after"] == [2, 3]
            and not hom["standard_mapping_cylinder_can_create_missing_input_map"]
            and root_stage["generated_Hom_response_cap"] == 0
            and root_stage["surviving_covectors"]
                == ["omega_AB^Hom", "omega_AC^Hom"]
            and section["endpoint_even_parent_quotient_dimension"] == 6
            and section["endpoint_odd_kernel_dimension"] == 6
            and section["unique_equivariant_block_coefficient"] == "1/2",
            (hom, root_stage, section))

    e_response = (Q(1), Q(0), Q(0))
    e_cap = (Q(0), Q(1), Q(0))
    off_diagonal = (Q(0), Q(0), Q(1))
    require(rank((e_response, e_cap)) == 2
            and rank((e_response, e_cap, off_diagonal)) == 3,
            "operation-corner rank changed")
    return {
        "literal_diagonal_corners": ["e_R A e_R", "e_C A e_C"],
        "source_provenant_generators": [
            "divided Taylor-Spencer trigger/deletion/reinsertion cells in e_RAe_R",
            "two endpoint-even root sections AB and AC with Reynolds coefficient 1/2",
            "cap r0, T, rho, K_Eq and AugP2 cells in e_CAe_C",
            "deleted-factor, lcm and naturality cylinders for already-present maps",
        ],
        "endpoint_even_parent_dimensions": [12, 6, 6],
        "root_Hom_covectors": root_stage["surviving_covectors"],
        "generated_Hom_response_cap": 0,
        "operation_rank_before_after_off_diagonal": [2, 3],
        "desired_operation_coordinate":
            "e_C Phi_KS,r0 e_R (response KS -> cap AugP2/K_Eq)",
        "standard_mapping_cylinder_creates_input_map": False,
        "first_typing_obstruction": (
            "the source and cap words/fine/repeated/operation idempotents are "
            "orthogonal; permitted cylinders preserve the diagonal corner"
        ),
        "first_face_if_off_diagonal_is_granted":
            face["selected_six_term_face"],
    }


def formal_normalization_only(hpl_gate, response_gate) -> dict[str, object]:
    # These finite functions contain no source-retagging: they only compute
    # the unique scalar/sign shape which a physical constructor would have.
    repair = hpl_gate.universal_one_cell_repair()
    response_ledger, response_digest = response_gate.audit()
    require(response_digest == response_gate.EXPECTED_LEDGER_SHA256,
            response_digest)
    ungraded = response_ledger["ungraded_two_term_chain_map"]
    require(repair["first_HPL_inclusion_correction"] == "-K"
            and repair["higher_HPL_terms"] == 0
            and repair["retraction_of_K"] == 0
            and ungraded["normalized_solution"] == {"a": 1, "b": -1}
            and ungraded["ungraded_chain_map_parameter_dimension"] == 1,
            (repair, ungraded))
    return {
        "required_boundary": "dK=(H0-u)*e_Eq",
        "ungraded_chain_map_solution": ungraded["normalized_solution"],
        "universal_HPL_correction": repair[
            "first_HPL_inclusion_correction"],
        "higher_HPL_terms": repair["higher_HPL_terms"],
        "physical_retraction_of_formal_K": repair["retraction_of_K"],
        "formal_solution_dimension": 1,
        "physical_solution_dimension_in_current_operation_corner": 0,
        "warning": (
            "uniqueness fixes normalization after existence; it does not "
            "supply the absent off-diagonal source map"
        ),
    }


def mixed_square_and_first_faces(first_face_gate, response_gate) \
        -> dict[str, object]:
    first_ledger, first_digest = first_face_gate.audit()
    require(first_digest == first_face_gate.EXPECTED_LEDGER_SHA256,
            first_digest)
    response_ledger, response_digest = response_gate.audit()
    require(response_digest == response_gate.EXPECTED_LEDGER_SHA256,
            response_digest)

    face = first_ledger["explicit_M_N_q01_face"]
    square = first_ledger["six_label_four_root_square_totalization"]
    lift = first_ledger["abstract_vs_physical_lifting_and_terminal_dual"]
    simultaneous = first_ledger[
        "simultaneous_D4_P2_K_Eq_d_even_composition"]
    endpoint = first_ledger["endpoint_even_annihilator_and_target_gate"]
    first = response_ledger["first_literal_faces"]
    require(face["coefficient_label_match"] == [
                "q23 response face -> B1", "q45 response face -> B4"]
            and not face["common_V_supplies_word_fine_operation_transport"]
            and square["edge_boundary_rank"] == 72
            and square["H1_before_mixed_faces"] == 24
            and square["mixed_faces_needed_blockwise"] == 24
            and square["target_values_of_square_boundaries"] == [0]
            and square["Eq_augmentation_values_of_square_boundaries"] == [0]
            and lift["physical_enriched_category"][
                "rank_of_strong_label_root_transport_relations"] == 23
            and lift["physical_enriched_category"][
                "classes_after_strong_transport"] == 1
            and lift["normalized_omega_mix"][
                "value_on_full_D_oriented_mixed_schema"] == 1
            and simultaneous["exact_remaining_proper_face_debt"]
                == [0, -1, 0, 1]
            and simultaneous["coupled_rank_determinant"] == [24, 64]
            and first["old_complete_first_PP_rank_then_selected"] == [1, 2]
            and first["graph_rank_then_selected"] == [2, 3]
            and first["central_Eq_forgetful_rank_before_after"] == [3, 4]
            and endpoint["first_obstruction_stage"]["rank"] == 2
            and endpoint["second_obstruction_stage"]["dimension"] == 2
            and endpoint["second_obstruction_stage"]["pairing_matrix"]
                == [[2, 0], [0, 2]]
            and not endpoint["cyclic_A_module_reframing"][
                "current_physical_A_module_structure_proved"],
            (face, square, lift, simultaneous, first, endpoint))

    # Replay the strongest label/root covariance quotient explicitly.  It is
    # deliberately stronger than current physical transport and still leaves
    # the D-oriented candidate outside its rank-23 span.
    d_root = tuple(map(Q, (-1, 1, -1, 1)))
    coordinates = 24
    relations = []
    for root in range(4):
        for label in range(1, 6):
            vector = [Q(0)] * coordinates
            vector[6 * root + label] = 1
            vector[6 * root] = -1
            relations.append(tuple(vector))
    for root in range(1, 4):
        for label in range(6):
            vector = [Q(0)] * coordinates
            vector[label] = d_root[root]
            vector[6 * root + label] = -d_root[0]
            relations.append(tuple(vector))
    candidate = tuple(d_root[root] for root in range(4)
                      for _label in range(6))
    omega = tuple(d_root[root] / 24 for root in range(4)
                  for _label in range(6))
    require(rank(relations) == 23
            and all(dot(omega, relation) == 0 for relation in relations)
            and dot(omega, candidate) == 1
            and rank(tuple(relations) + (candidate,)) == 24,
            "mixed-square rank/dual changed")
    return {
        "parent": face["parents"],
        "required_decorated_faces": face[
            "required_physical_decorated_labels"],
        "response_side_coefficients_match_B1_B4": True,
        "physical_decorated_map_constructed": False,
        "selected_db01_rank_ladder": [1, 2],
        "presentation_graph_then_db01_rank_ladder": [2, 3],
        "central_Eq_incidence_rank_ladder": [3, 4],
        "four_root_six_label_square": {
            "edge_rank": square["edge_boundary_rank"],
            "H1_without_mixed_faces": square["H1_before_mixed_faces"],
            "actual_existing_mixed_faces": 0,
            "strong_covariance_rank": rank(relations),
            "residual_dimension": 1,
            "omega_mix_on_candidate": str(dot(omega, candidate)),
        },
        "simultaneous_proper_face_debt_row_order":
            simultaneous["full_row_order"],
        "simultaneous_proper_face_debt":
            simultaneous["exact_remaining_proper_face_debt"],
        "debt_meaning": simultaneous["debt_meaning"],
        "conditional_solve_rank_determinant":
            simultaneous["coupled_rank_determinant"],
        "conditional_cap_coefficient":
            simultaneous["characteristic_zero_solution"],
        "proper_target_faces": {
            "protected_words": endpoint["second_obstruction_stage"][
                "protected_words"],
            "pairing_matrix": endpoint["second_obstruction_stage"][
                "pairing_matrix"],
            "rank": endpoint["second_obstruction_stage"]["dimension"],
            "role": (
                "forced T23/T45 target-cone faces, not vanishing equations"
            ),
            "source_provenant_occurrence_placement_constructed": False,
        },
    }


def protected_output_and_dq_gate(local, private_gate, cplus_gate) \
        -> dict[str, object]:
    top = local.top_projection_columns()
    lower = local.lower_face_and_reinsertion_columns()
    external = local.external_augmented_columns()
    columns = tuple(value for _name, value in top + lower + external)
    dual = local.integral_terminal_dual()
    private_top = local.balanced_top("B")
    eq_top = local.balanced_top("Eq")
    tied_top = local.tied_balanced_top()
    require(len(local.LABELS) == 127
            and len(top) == 24 and len(lower) == 84 and len(external) == 30
            and rank(columns) == 126
            and all(dot(dual, column) == 0 for column in columns)
            and dot(dual, private_top) == 12
            and dot(dual, eq_top) == -12
            and dot(dual, tied_top) == 0
            and rank(columns + (private_top,)) == 127
            and rank(columns + (eq_top,)) == 127,
            "protected local rank/dual changed")

    private_ledger, private_digest = private_gate.audit()
    require(private_digest == private_gate.EXPECTED_LEDGER_SHA256,
            private_digest)
    reinsertion = private_ledger["q23_reinsertion"]
    require(reinsertion["forced_repair_dq23_private_detector"] == "35/72"
            and reinsertion["ordinary_residue_aggregate"] == 0
            and reinsertion["occurrence_labelled_conormal_nonzero"],
            reinsertion)

    cap = cplus_gate.root_even_cap_table()
    require(cap["sum_Eq_Yw_W_target_ainc"] == 0
            and cap["table"]["B_E=(r0-T)_E"] == {
                "Eq": "+E", "Yw": "+E", "W": "+E",
                "target": "0", "ainc": "-sum(E)=0"}, cap)
    return {
        "protected_output_dimension_rank": [127, 126],
        "protected_rows": [
            "B", "Eq", "18 direction flags", "24 tail PP flags",
            "target", "q", "anchor/ainc/P_f", "W", "ores",
            "ridge", "eta", "sigma",
        ],
        "all_current_literal_columns_killed_by_integral_dual": True,
        "integral_dual": "delta.(B-Eq) transported through all flags",
        "normalized_charge_on_private_Eq_tied": [1, -1, 0],
        "rank_after_private_or_Eq_control": 127,
        "HPL_boundary_orientation": (
            "the Eq-only control has normalized charge -1; modulo the tied "
            "B=Eq line it is the negative of the private RHS"
        ),
        "cap_top_protected_table": cap["table"]["B_E=(r0-T)_E"],
        "forced_q23_dq_face": {
            "word": "0102", "cut": "dq23:21",
            "detector": "+e0+e3-e1-e6", "value": "35/72",
            "ordinary_residue_aggregate": 0,
        },
        "sigma_mate": {
            "word": "0121", "cut": "dq45:12", "value": "35/72"
        },
        "interpretation": (
            "external decoration cannot repair the missing B/Eq line; once "
            "a physical occurrence landing exists, its dq faces are forced"
        ),
    }


def full_grade_and_minimal_constructor(source, response_ledger) \
        -> dict[str, object]:
    grade = source.full_grade_audit()
    positive = response_ledger["minimal_positive_schema"]
    require(grade["word"] == "01211222"
            and grade["fine_lattice_coordinate_width"] == 24
            and grade["repeated"] == "P3+K2"
            and grade["operation_parent"]
                == "response-to-AugP2 mixed orbit/K_Eq"
            and len(positive["all_eight_instantiation"]) == 8,
            (grade, positive))
    return {
        "new_primitive_constructor": (
            "one normalized source-labelled mixed Taylor-Spencer-to-AugP2 "
            "mate Phi_KS,r0 in e_C A e_R"
        ),
        "why_this_and_not_a_new_formal_K": (
            "once Phi exists, its ordinary functorial mapping cylinder and "
            "K_Eq product create K with forced coefficient/sign; without Phi "
            "no permitted cylinder has the required operation corner"
        ),
        "generator_map": positive["required_generator_map"],
        "boundary_map": positive["required_boundary_map"],
        "normalization": positive["chain_map_normalization"],
        "full_grade": {
            "response_word": grade["response_word"],
            "cap_word": grade["word"],
            "fine_labels": grade["fine_labels"],
            "fine_coordinate_width": grade[
                "fine_lattice_coordinate_width"],
            "repeated": grade["repeated"],
            "operation": grade["operation_parent"],
            "window": "2345 with parent occurrence retained",
            "endpoint_parity": "even",
            "root_sections": ["AB", "AC"],
        },
        "forced_faces": [
            positive["first_PP_face"],
            "0112/q23:21 and 0121/q45:12 occurrence-local P2 landings",
            "0102/dq23:21 and sigma dq45:12 conormals",
            "root lower=-E and word-resolved ores=+E",
            "canonical T23/T45 target cone faces",
            *positive["cap_proper_faces"],
        ],
        "all_eight_lower_word_instances": [
            record["lower_word"]
            for record in positive["all_eight_instantiation"]
        ],
        "standard_mapping_cylinder_after_constructor": True,
        "constructed_by_current_ansatz": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    hpl_gate = load(
        "computations/verify_h3_cap_top_sdr_hpl_transfer_no_go.py",
        "physical_k_ansatz_hpl",
    )
    response_gate = load(
        "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py",
        "physical_k_ansatz_response",
    )
    first_face_gate = load(
        "computations/verify_h3_first_face_keq_augp2_mixed_square_totalization_gate.py",
        "physical_k_ansatz_first_face",
    )
    even_gate = load(
        "computations/verify_h3_gate_ii_endpoint_even_cap_operator_module_gate.py",
        "physical_k_ansatz_even",
    )
    private_gate = load(
        "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py",
        "physical_k_ansatz_private",
    )
    local = load(
        "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py",
        "physical_k_ansatz_local",
    )
    cplus_gate = load(
        "computations/verify_h3_cplus_w_yw_cap_factorization.py",
        "physical_k_ansatz_cplus",
    )
    source = load(
        "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py",
        "physical_k_ansatz_source",
    )

    response_ledger, response_digest = response_gate.audit()
    require(response_digest == response_gate.EXPECTED_LEDGER_SHA256,
            response_digest)
    ledger = {
        "theorem": "h3 physical Eq-filler K source-ansatz terminal gate",
        "pins": PINS,
        "literal_fixed_grade_operation_ansatz":
            literal_operation_corner_ansatz(response_gate, even_gate),
        "formal_normalization_but_not_existence":
            formal_normalization_only(hpl_gate, response_gate),
        "first_source_faces_and_mixed_square":
            mixed_square_and_first_faces(first_face_gate, response_gate),
        "all_protected_rows_and_forced_dq_faces":
            protected_output_and_dq_gate(local, private_gate, cplus_gate),
        "minimal_additional_constructor":
            full_grade_and_minimal_constructor(source, response_ledger),
        "verdict": (
            "No physical K is generated by the smallest literal ansatz.  "
            "The failure occurs before an augmented rank solve: all divided "
            "Taylor-Spencer triggers and permitted cylinders remain in the "
            "response corner, while r0/K_Eq/AugP2 remain in the cap corner, "
            "and e_C A e_R=0.  The desired off-diagonal operation raises "
            "operation rank 2 to 3.  Its first selected db01 face raises rank "
            "1 to 2, its central Eq incidence raises 3 to 4, its four-root/"
            "six-label square is the unique class beyond a rank-23 covariance "
            "span, and its protected B/Eq image is the unique missing line "
            "in rank 126/127.  The minimal genuinely new primitive is not a "
            "retagged K: it is one normalized source-labelled Phi_KS,r0 "
            "mixed mate.  Only after Phi exists do the standard cylinder and "
            "K_Eq product construct K and force the q23/q45 and 35/72 dq faces"
        ),
        "scope": (
            "exact rational h3 canonical M/N/q01 packet, two endpoint-even "
            "root sections, all four oriented root paths and six B labels in "
            "the mixed-square test, full 127-row local protected codomain, "
            "q23 representative and sigma mate.  This is a terminal for the "
            "literal constructor ansatz, not a proof that an unmodeled "
            "physical mixed mate cannot exist and not an all-h theorem"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("physical K source-ansatz ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=(
        "all", "typing", "faces", "protected", "constructor"),
        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        operation = ledger["literal_fixed_grade_operation_ansatz"]
        faces = ledger["first_source_faces_and_mixed_square"]
        protected = ledger["all_protected_rows_and_forced_dq_faces"]
        print(f"h3 physical Eq-filler K ansatz ({arguments.mode}): PASS")
        print("generated Hom(response,cap):",
              operation["generated_Hom_response_cap"])
        print("operation rank before/after missing mate:",
              operation["operation_rank_before_after_off_diagonal"])
        print("mixed covariance residual:",
              faces["four_root_six_label_square"]["residual_dimension"])
        print("protected rank:",
              protected["protected_output_dimension_rank"])
        print("physical K constructed: NO")
        print("minimal constructor: Phi_KS,r0 mixed mate")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
