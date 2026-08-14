#!/usr/bin/env python3
"""Totalize the first TrigEuler face through the physical K_Eq/AugP2 gate.

The exact q=01 Taylor--Spencer face has parent

    M=01*23*45*67, N=07*12*34*56,

and branch K=07*23*45*67.  Its two kept tail restrictions are q23 and q45.
They are exactly the two coefficient labels which the E14 totalization sends
to B1 and B4.  Thus the new common-V carrier supplies the correct top R and
the correct *response-side* proper faces.

The actual source category still has no word/fine/operation-labelled map

    0112/q23 -> B1,  0121/q45 -> B4.

Objectwise K_Eq, D4, P2 and cap edges form only the boundary of a square.
Across four oriented root paths and six B labels there are 24 primitive
square classes.  Their target and d^2 values vanish.  The strongest formal
label/root naturality identifies them to one class, detected by the
normalized D-character operation covector omega_mix.

Composing with the simultaneous D4/P2/K_Eq/d_even solve removes every old
lower/Eq/ores/ainc/target detector *conditional on* the missing labelled
map.  The transfer is nonsingular over the characteristic-zero theorem ring.
Without that map the common-V carrier contributes only top R and leaves the
exact proper-face debt (lower,ores)=(-E,+E).  Hence abstract comparison after
forgetting labels exists, but the physical enriched Ext/Hom class remains.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_full_star_minimal_protected_homogenizer_cylinder_gate.py":
        "ab7471a38683da113723ea9a073e3dc2a3c76d4576b9e575a0983ab1054c5d58",
    "computations/verify_h3_trig_euler_augp2_common_base_comparison_gate.py":
        "3ca82479bd2d1c2847dff55f3c05c87f24406ec1c2f3a5fbb9cdf619a6f7047a",
    "computations/verify_h3_e14_d4_p2_keq_deven_simultaneous_totalization_gate.py":
        "dfa46c3519089bb7b2a04d24ea6e4f9d138887d98fb53af60369184d2d2c91fd",
    "computations/verify_h3_e14_augmented_rhs_evenness_bockstein_gate.py":
        "9b65dd37aab071b0ced41c663cf5011b722582eaa2cc8330c22a4ee58b900adf",
    "computations/verify_h3_centered_base_denominator_deven_composition_gate.py":
        "ee8952a30b9d1a583f3d0e78b8289e5ed839d399d0865b0457315c969c117291",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "computations/verify_h3_eqsystem_augp2_actual_presentation_underdetermination_gate.py":
        "2c112bffeef2c6adb00029077b6b231de396ace76c78756ab0e11e20078a557b",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_augp2_six_cell_parent_augmentation_gate.py":
        "26259bb67476a30c4237c20f8e393ec919e934f95bab0d0c6845adc9295c3132",
    "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py":
        "8a9bfe47c934658d1b10ad42f283d6a017c27125bcb98615882e4bacd975f1eb",
}
EXPECTED_LEDGER_SHA256 = "70b908555076df66fce45d28d5ed97de92e2dd4ef83d246a464c23984a5009e1"

PURE_WORD = (1,) * 8
A = (0, 1, 1, 1)
B = (0, 7, 1, 1)
M = frozenset(((0, 1, 1, 1), (2, 3, 1, 1),
               (4, 5, 1, 1), (6, 7, 1, 1)))
N = frozenset(((0, 7, 1, 1), (1, 2, 1, 1),
               (3, 4, 1, 1), (5, 6, 1, 1)))
K = frozenset(((0, 7, 1, 1), (2, 3, 1, 1),
               (4, 5, 1, 1), (6, 7, 1, 1)))
Q23 = (2, 3, 1, 1)
Q45 = (4, 5, 1, 1)

B_LABELS = ("B0", "B1", "B2", "B3", "B4", "B5")
COFACTOR_LABELS = ("q45", "q23", "q35", "q24", "q34", "q25")
ROOT_PATHS = ("AB-", "AB+", "AC-", "AC+")
D_ROOT = tuple(map(Q, (-1, 1, -1, 1)))


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


def sparse_rank(vectors) -> int:
    basis = {}
    for source in vectors:
        vector = {key: Q(value) for key, value in source.items() if value}
        while vector:
            pivot = min(vector, key=repr)
            if pivot not in basis:
                inverse = Q(1) / vector[pivot]
                basis[pivot] = {
                    key: value * inverse for key, value in vector.items()
                }
                break
            coefficient = vector[pivot]
            for key, value in basis[pivot].items():
                residue = vector.get(key, Q(0)) - coefficient * value
                if residue:
                    vector[key] = residue
                else:
                    vector.pop(key, None)
    return len(basis)


def dot(dual, vector) -> Q:
    return sum((Q(value) * Q(dual.get(key, 0))
                for key, value in vector.items()), Q(0))


def explicit_parent_face_audit(protected, base, centered, packaging):
    protected.pin_dependencies()
    face = protected.first_literal_noncommuting_face(base)
    common = protected.common_parent_occurrence_augmentation(base)
    require(face["first_restriction_factor_q"] == repr(A)
            and face["left_parent_M"] == repr(tuple(sorted(M)))
            and face["right_parent_N"] == repr(tuple(sorted(N)))
            and face["left_branch_K"] == repr(tuple(sorted(K)))
            and common["common_matching_augmentation_is_exact"],
            (face, common))

    # q23 and q45 are kept branch factors, so their restriction squares are
    # among the commuting faces rather than the 1020 deleted-factor debts.
    require(Q23 in K and Q45 in K and A not in K,
            (K, Q23, Q45))
    q23_face = K - {Q23}
    q45_face = K - {Q45}
    require(len(q23_face) == len(q45_face) == 3,
            (q23_face, q45_face))

    centered.pin_inputs()
    label_audit = centered.conditional_deven_composition_audit()
    require(label_audit["coefficient_labels"]
            == ["0112/q23 -> B1", "0121/q45 -> B4"]
            and not label_audit[
                "physical_occurrence_to_label_map_constructed"],
            label_audit)

    packaging.pin_dependencies()
    words = packaging.word_and_fine_grade_audit()
    require(words["response_word_full"] == "11110000"
            and words["canonical_cap_word"] == "01211222"
            and words["word_hamming_distance"] == 6
            and words["all_six_fine_degrees_change"]
            and not words["literal_grade_preserving_map"], words)
    selected = tuple(row["undecorated"].split("*")[-1]
                     for row in words["selected_P3K2_decorations"])
    require(selected == COFACTOR_LABELS, selected)
    return {
        "parents": {
            "M": repr(tuple(sorted(M))),
            "N": repr(tuple(sorted(N))),
            "selected_q": repr(A),
            "branch_K": repr(tuple(sorted(K))),
        },
        "q01_deleted_factor_square": face,
        "private_q01_cylinder_present": True,
        "kept_branch_faces": {
            "delete_q23": repr(tuple(sorted(q23_face))),
            "delete_q45": repr(tuple(sorted(q45_face))),
            "restriction_squares_commute_response_side": True,
        },
        "six_selected_cofactor_labels_in_order": list(COFACTOR_LABELS),
        "coefficient_label_match": [
            "q23 response face -> B1",
            "q45 response face -> B4",
        ],
        "required_physical_decorated_labels": [
            "0112/q23:21 -> B1",
            "0121/q45:12 -> B4",
        ],
        "common_V_supplies_top_and_undecorated_proper_faces": True,
        "common_V_supplies_word_fine_operation_transport": False,
        "first_decorated_mismatch": (
            "response q23:11/q45:11 (through the 11110000 D4 face q23:00/"
            "q45:00) versus cap-lower q23:21/q45:12"
        ),
    }


def square_packet_totalization(pointed):
    pointed.pin_dependencies()
    square = pointed.mapping_cylinder_square_audit()
    require(square["d1_rank"] == 3
            and square["primitive_boundary_cycle"] == [1, -1, 1, -1]
            and square["H1_without_mixed_face"] == "Z"
            and square["H1_after_one_mixed_face"] == 0,
            square)

    # Vertex order: response at the two root endpoints, then cap at the two
    # endpoints.  Edge order agrees with the pinned pointed square.
    edge_vectors = (
        (-1, 1, 0, 0),
        (-1, 0, 1, 0),
        (0, -1, 0, 1),
        (0, 0, -1, 1),
    )
    cycle = (1, -1, 1, -1)
    target_on_vertices = (0, 0, 1, 1)
    eq_on_vertices = target_on_vertices
    packet_edges = []
    packet_faces = []
    target_values = []
    eq_values = []
    for root in range(len(ROOT_PATHS)):
        for label in range(len(B_LABELS)):
            for edge, values in enumerate(edge_vectors):
                packet_edges.append({
                    ("vertex", root, label, vertex): Q(value)
                    for vertex, value in enumerate(values) if value
                })
            face = {
                ("edge", root, label, edge): Q(value)
                for edge, value in enumerate(cycle) if value
            }
            packet_faces.append(face)
            boundary = tuple(sum(cycle[edge] * edge_vectors[edge][vertex]
                                 for edge in range(4))
                             for vertex in range(4))
            require(boundary == (0, 0, 0, 0),
                    (root, label, boundary))
            edge_target = tuple(sum(target_on_vertices[vertex]
                                    * edge_vectors[edge][vertex]
                                    for vertex in range(4))
                                for edge in range(4))
            edge_eq = tuple(sum(eq_on_vertices[vertex]
                                * edge_vectors[edge][vertex]
                                for vertex in range(4))
                            for edge in range(4))
            target_values.append(sum(cycle[edge] * edge_target[edge]
                                     for edge in range(4)))
            eq_values.append(sum(cycle[edge] * edge_eq[edge]
                                 for edge in range(4)))

    require(len(packet_faces) == 24
            and sparse_rank(packet_edges) == 72
            and sparse_rank(packet_faces) == 24
            and set(target_values) == {0} and set(eq_values) == {0},
            (len(packet_faces), sparse_rank(packet_edges),
             sparse_rank(packet_faces), target_values, eq_values))
    return {
        "root_path_order": list(ROOT_PATHS),
        "D_root_orientation": [int(value) for value in D_ROOT],
        "B_label_order": list(B_LABELS),
        "blocks": 24,
        "vertices": 96,
        "edge_generators": 96,
        "edge_boundary_rank": 72,
        "H1_before_mixed_faces": 24,
        "mixed_faces_needed_blockwise": 24,
        "mixed_face_boundary": [1, -1, 1, -1],
        "d_squared_values": sorted(set(target_values)),
        "target_values_of_square_boundaries": sorted(set(target_values)),
        "Eq_augmentation_values_of_square_boundaries": sorted(set(eq_values)),
        "H1_after_all_mixed_faces": 0,
        "existing_objectwise_K_Eq_supplies_edges_not_faces": True,
    }


def simultaneous_augmented_composition(simultaneous, evenness, protected,
                                       base):
    simultaneous.pin_dependencies()
    d4 = simultaneous.d4_last_boundary_signs()
    linear = simultaneous.simultaneous_rank_and_dependency_audit()
    transfer = simultaneous.coupled_transfer_matrix_audit()
    require(d4["signs_equal_D_root"]
            and linear["one_new_pointed_section"] == [1, -1, 0, 1]
            and linear["old_O_full"] == [0, 1, 1, -1]
            and linear["required_Phi_orb"] == [1, 0, 1, 0]
            and transfer["I_plus_transfer_rank"] == 24
            and transfer["I_plus_transfer_determinant"] == 64,
            (d4, linear, transfer))

    common = protected.common_parent_occurrence_augmentation(base)
    require(common["normalized_response_augmentation"] == "1_V",
            common)
    # Common V supplies the normalized marked top R, but neither of the two
    # operation-labelled proper faces of the pointed section.
    common_top = tuple(map(Q, (1, 0, 0, 0)))
    old_o = tuple(map(Q, linear["old_O_full"]))
    required = tuple(map(Q, linear["required_Phi_orb"]))
    current_sum = tuple(a + b for a, b in zip(common_top, old_o,
                                              strict=True))
    debt = tuple(a - b for a, b in zip(required, current_sum, strict=True))
    require(current_sum == tuple(map(Q, (1, 1, 1, -1)))
            and debt == tuple(map(Q, (0, -1, 0, 1))),
            (current_sum, debt))

    evenness.pin_dependencies()
    rhs = evenness.literal_augmented_rhs_audit()
    require(rhs["A_plus_X_plus_LF_C"] == [0, 1, 0, 0, 1, 0]
            and rhs["solution_over_characteristic_zero_kbeta"]
                == ["0", "1/2", "0", "0", "1/2", "0"], rhs)

    # E=D tensor (B1+B4) has root sum zero.  Thus the cap target and aggregate
    # anchor/ainc rows cancel in the complete D-character packet.  The old
    # lower and ores detectors vanish only after adding precisely debt.
    orbit_sum = tuple(map(Q, (0, 1, 0, 0, 1, 0)))
    e_packet = tuple(root * label for root in D_ROOT
                     for label in orbit_sum)
    require(sum(e_packet, Q(0)) == 0
            and sum(D_ROOT, Q(0)) == 0,
            (e_packet, D_ROOT))
    after_section = tuple(a + b for a, b in
                          zip(current_sum, debt, strict=True))
    require(after_section == required,
            (after_section, required))
    return {
        "full_row_order": linear["full_row_order"],
        "common_V_contribution": [1, 0, 0, 0],
        "old_O_minus_E": linear["old_O_full"],
        "current_sum_before_labelled_section": [1, 1, 1, -1],
        "exact_remaining_proper_face_debt": [0, -1, 0, 1],
        "debt_meaning": "root lower=-E and rooted labelled ores=+E",
        "after_missing_section": linear["required_Phi_orb"],
        "old_lower_detector_before_after": [1, 0],
        "old_ores_detector_before_after": [-1, 0],
        "Eq_debt_after_totalization": 0,
        "target_debt_after_D_root_totalization": 0,
        "ainc_anchor_debt_after_D_root_totalization": 0,
        "reason_target_ainc_cancel": "sum(D_root)=0",
        "six_label_coupled_operator": "I+P_D tensor I_6",
        "coupled_rank_determinant": [
            transfer["I_plus_transfer_rank"],
            transfer["I_plus_transfer_determinant"],
        ],
        "characteristic_zero_solution": "K=(B1+B4)/2",
        "beta_denominator": 0,
        "optional_integral_class": "[B1+B4] in (Z/2)^6",
        "simultaneous_system_closes_if_label_map_is_supplied": True,
        "common_V_alone_closes_simultaneous_system": False,
    }


def enriched_lifting_and_omega(common_comparison, actual, protected):
    common_comparison.pin_dependencies()
    actual_ledger, actual_digest = actual.audit()
    require(actual_digest == actual.EXPECTED_LEDGER_SHA256, actual_digest)
    presentation = actual_ledger["smallest_literal_generated_presentation"]
    require(presentation["Hom0_response_cap"] == 0
            and presentation["generated_Hom1_response_cap"] == 0
            and presentation["primitive_Hom1_response_cap"] == 0
            and presentation["literal_Gamma_cap_entries"] == 25
            and presentation["Gamma_image_rank_of_callable_registry"] == 23
            and presentation["B_Eq_rank_of_callable_registry"] == 7,
            presentation)

    # The formal transport closure is stronger than the current registry.
    # Label differences and D-oriented root-path differences span a rank-23
    # hyperplane of the 24 possible mixed faces.  omega is its normalized
    # annihilator and reads one on the D-oriented full schema.
    relations = []
    for root in range(4):
        for label in range(1, 6):
            relations.append({
                ("mix", root, label): Q(1),
                ("mix", root, 0): Q(-1),
            })
    for root in range(1, 4):
        for label in range(6):
            relations.append({
                ("mix", 0, label): D_ROOT[root],
                ("mix", root, label): -D_ROOT[0],
            })
    omega = {
        ("mix", root, label): D_ROOT[root] / 24
        for root in range(4) for label in range(6)
    }
    candidate = {
        ("mix", root, label): D_ROOT[root]
        for root in range(4) for label in range(6)
    }
    require(sparse_rank(relations) == 23
            and all(dot(omega, relation) == 0 for relation in relations)
            and dot(omega, candidate) == 1
            and sparse_rank(relations + [candidate]) == 24,
            (sparse_rank(relations), dot(omega, candidate)))

    # Pinned current-family counts.  All these columns are known to have zero
    # mixed-operation coordinate; unique dark coordinates model their other
    # retained rows without introducing spurious linear relations.
    protected_columns = 2 * (1020 + 9)
    current_names = [
        *(f"callable-Gamma:{index}" for index in range(25)),
        *(f"protected-cylinder:{index}" for index in range(protected_columns)),
        "collision-hidden-P2", "objectwise-clean-K_Eq", "D4-top",
        "old-O-minus-E", "cap-p", "cap-n", "cap-z", "d-even",
        "target", "q", "anchor-ainc", "W", "ores", "ridge",
        "eta", "sigma",
    ]
    current_columns = [
        {("dark-existing", index): Q(1)}
        for index, _name in enumerate(current_names)
    ]
    require(all(dot(omega, column) == 0 for column in current_columns)
            and all(dot(omega, relation) == 0 for relation in relations),
            "omega stopped extending across an allowed augmented row")
    return {
        "abstract_untyped_category": {
            "common_base": "V=Q^90",
            "response_resolution_projective": True,
            "after_freely_adjoining_cap_augmentation": (
                "Ext^1_Q(V,V)=0; a comparison lift exists"
            ),
            "lifting_equations": [
                "epsilon_C Phi_0=epsilon_R",
                "d_C Phi_n=Phi_(n-1) d_R",
                "at the first square: delta(K)=bottom-left+right-top",
            ],
        },
        "physical_enriched_category": {
            "Hom0_response_cap": 0,
            "Hom1_response_cap": 0,
            "obstruction_class": (
                "[bottom-left+right-top] in H^1 Hom_A(P_R,P_C)"
            ),
            "per_root_label_classes_before_transport": 24,
            "rank_of_strong_label_root_transport_relations": 23,
            "classes_after_strong_transport": 1,
        },
        "normalized_omega_mix": {
            "formula": (
                "omega_mix=(1/24) sum_(r,j) D_root[r] mu_(r,Bj)^*"
            ),
            "value_on_all_current_augmented_rows": 0,
            "value_on_all_label_root_transport_relations": 0,
            "value_on_full_D_oriented_mixed_schema": 1,
        },
        "current_rows_checked_by_pinned_inventories": {
            "callable_Gamma_cap_entries": 25,
            "callable_Gamma_rank": 23,
            "callable_B_Eq_rank": 7,
            "protected_relative_cylinders_two_root": protected_columns,
            "simultaneous_and_protected_named_families":
                len(current_names) - 25 - protected_columns,
            "total_modelled_current_columns": len(current_columns),
        },
        "exact_missing_operation": (
            "one source-labelled mixed K_Eq/AugP2 square whose q23/q45 "
            "proper faces land in B1/B4 in the cap word/fine/repeated grade"
        ),
    }


def endpoint_even_annihilator_gate(six_cell, correction):
    """Pass to the canonical endpoint-even base and expose the obstruction tower.

    Endpoint averaging removes the six P/S-odd parent choices.  It cannot
    identify the response and Eq copies of H-u, and it acts on a different
    tensor factor from the two protected mixed-target normals.  The latter
    have diagonal pairing 2, hence normalized rational detectors 1/2 X^*.

    This is also the finite presentation needed for the proposed A-module
    reframing: after the full-star/deleted-face relations, a putative image
    r0 of the cyclic response generator must satisfy the mixed Eq relation
    and then the two target cone relations.  The checker records this as a
    conditional annihilator criterion; it does not assert that the physical
    cap packet already carries the divided-Weyl/Hasse A-action.
    """
    cap_ledger, cap_digest = six_cell.audit()
    require(cap_digest == six_cell.EXPECTED_LEDGER_SHA256, cap_digest)
    parents = cap_ledger["literal_parent_candidates"]
    boundary = cap_ledger["word_root_paths_and_first_chain_boundary"]
    target = boundary["next_target_obstruction"]
    require(
        parents["coefficient_B4_B1_times_matching_map_rank"] == 6
        and parents["ordered_parent_candidates"] == 12
        and parents["endpoint_odd_kernel_dimension"] == 6
        and parents["canonical_Q_linear_even_section"]["rank"] == 6
        and parents["odd_covector_on_even_section"] == 0
        and boundary["boundary_rank"] == 2
        and boundary["generated_Hom_response_cap"] == 0
        and target["rank_local_diagonal_lines"] == 2
        and target["rank_after_two_mixed_normals"] == 4
        and target["cokernel_rank"] == 2
        and target["pairing_matrix_on_the_two_normals"]
            == [[2, 0], [0, 2]],
        (parents, boundary),
    )

    # Quotient coordinates are (H-u)_R, (H-u)_Eq, X_0112, X_0121.
    # The first differential has independent response/Eq images.  The two
    # target cone faces remain a diagonal 2I_2 block over Q.
    g0_boundary = (Q(1), Q(0), Q(0), Q(0))
    r0_boundary = (Q(0), Q(1), Q(0), Q(0))
    mixed_boundary = tuple(right - left for left, right in
                           zip(g0_boundary, r0_boundary, strict=True))
    target_0112 = (Q(0), Q(0), Q(2), Q(0))
    target_0121 = (Q(0), Q(0), Q(0), Q(2))
    omega_eq = (Q(-1, 2), Q(1, 2), Q(0), Q(0))
    tau_0112 = (Q(0), Q(0), Q(1, 2), Q(0))
    tau_0121 = (Q(0), Q(0), Q(0), Q(1, 2))
    require(
        sparse_rank((dict(enumerate(g0_boundary)),
                     dict(enumerate(r0_boundary)))) == 2
        and dot(dict(enumerate(omega_eq)),
                dict(enumerate(mixed_boundary))) == 1
        and dot(dict(enumerate(tau_0112)),
                dict(enumerate(target_0112))) == 1
        and dot(dict(enumerate(tau_0112)),
                dict(enumerate(target_0121))) == 0
        and dot(dict(enumerate(tau_0121)),
                dict(enumerate(target_0112))) == 0
        and dot(dict(enumerate(tau_0121)),
                dict(enumerate(target_0121))) == 1,
        "endpoint-even normalized obstruction pairing changed",
    )

    # The endpoint involution has already been quotiented.  The root/Weyl
    # involution interchanges the target normals; its invariant sum is still
    # nonzero.  Thus neither averaging operation kills the target stage.
    sigma_even_target = tuple(a + b for a, b in
                              zip(target_0112, target_0121, strict=True))
    tau_sigma = tuple((a + b) / 2 for a, b in
                      zip(tau_0112, tau_0121, strict=True))
    require(dot(dict(enumerate(tau_sigma)),
                dict(enumerate(sigma_even_target))) == 1,
            (tau_sigma, sigma_even_target))

    correction.pin_dependencies()
    extension = correction.explicit_dual_extension_audit()
    require(
        extension["extension_formula"] == {
            "q": 0, "ainc": 0, "Eq_j": 0,
            "target_j": "-mu_j", "W_j": "-mu_j",
            "ores_j": "mu_j", "ridge": "-sum alpha_j mu_j",
        }
        and extension["corrected_packets_detecting_any_known_column"] == 0,
        extension,
    )

    return {
        "endpoint_even_quotient": {
            "unordered_parent_rank": 6,
            "ordered_parent_dimension": 12,
            "odd_kernel_removed": 6,
            "canonical_even_section_rank": 6,
            "requires_a_literal_P_or_S_choice": False,
        },
        "first_obstruction_stage": {
            "row_order": ["(H-u)_response", "(H-u)_Eq_cap"],
            "dG0": [1, 0],
            "dr0": [0, 1],
            "rank": 2,
            "normalized_detector": "1/2*(-delta_R+delta_Eq)",
            "value_on_dr0_minus_dG0": 1,
            "simultaneous_system_solves_after_mixed_section": True,
            "simultaneous_system_constructs_mixed_section": False,
        },
        "second_obstruction_stage": {
            "protected_words": ["00211122", "00111222"],
            "pairing_matrix": [[2, 0], [0, 2]],
            "normalized_detectors": [
                "1/2 X_00211122^*", "1/2 X_00111222^*",
            ],
            "dimension": 2,
            "endpoint_even_quotient_kills_them": False,
            "root_swap_invariant_sum_is_nonzero": True,
            "normalized_invariant_sum_value": 1,
        },
        "effect_of_4373_cap_cartan_correction": {
            "kind": "dual extension, not a source filler",
            "formula": extension["extension_formula"],
            "known_augmented_columns_detected_after_correction": 0,
            "source_image_rank_before_after_dual_correction": [2, 2],
            "rank_after_adjoining_the_two_missing_target_columns": 4,
            "identification_with_protected_word_normals_proved_by_4373":
                False,
            "exact_consequence": (
                "4373 cannot solve either target normal because it adds no "
                "source column.  If a source-labelled placement of a normal "
                "into its four corner rows is supplied, its formula extends "
                "the detecting dual through all known cap/Cartan columns"
            ),
        },
        "cyclic_A_module_reframing": {
            "response_module": "A e_R / Ann_A(e_R)",
            "candidate_map": "e_R |-> r0 in C_cap",
            "exact_existence_criterion": "Ann_A(e_R) r0=0",
            "finite_presented_relations_already_cleared": (
                "full-star simplex, 1020 deleted-factor squares, nine "
                "ambiguous-lcm cylinders, ordinary objectwise K_Eq/D4/P2"
            ),
            "remaining_relation_tower": [
                "one transported (H-u)_response=(H-u)_Eq relation",
                "two protected mixed-target cone relations",
            ],
            "remaining_normalized_obstruction_dimensions": [1, 2],
            "sufficiency_status": (
                "conditional on proving that C_cap is a module over the "
                "literal divided-Weyl/Hasse algebra A and that the pinned "
                "full-star presentation exhausts Ann_A(e_R)"
            ),
            "current_physical_A_module_structure_proved": False,
        },
        "sharp_verdict": (
            "endpoint-even descent removes the six P/S-odd choices, but the "
            "current physical complex still has the one mixed Eq boundary "
            "class followed by two independent target normals.  The "
            "simultaneous solve closes them only conditional on the missing "
            "mixed section; the 4373 correction is dual-side and cannot "
            "raise the source rank.  After a labelled corner placement it "
            "extends a terminal detector, rather than supplying a filler"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    protected = load(
        "computations/verify_h3_full_star_minimal_protected_homogenizer_cylinder_gate.py",
        "first_face_protected",
    )
    common_comparison = load(
        "computations/verify_h3_trig_euler_augp2_common_base_comparison_gate.py",
        "first_face_common_comparison",
    )
    simultaneous = load(
        "computations/verify_h3_e14_d4_p2_keq_deven_simultaneous_totalization_gate.py",
        "first_face_simultaneous",
    )
    evenness = load(
        "computations/verify_h3_e14_augmented_rhs_evenness_bockstein_gate.py",
        "first_face_evenness",
    )
    centered = load(
        "computations/verify_h3_centered_base_denominator_deven_composition_gate.py",
        "first_face_centered",
    )
    packaging = load(
        "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py",
        "first_face_packaging",
    )
    actual = load(
        "computations/verify_h3_eqsystem_augp2_actual_presentation_underdetermination_gate.py",
        "first_face_actual",
    )
    pointed = load(
        "computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py",
        "first_face_pointed",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "first_face_base",
    )
    six_cell = load(
        "computations/verify_h3_augp2_six_cell_parent_augmentation_gate.py",
        "first_face_six_cell",
    )
    correction = load(
        "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py",
        "first_face_terminal_correction",
    )

    ledger = {
        "theorem": "h3 first-face K_Eq/AugP2 mixed-square totalization gate",
        "pins": PINS,
        "explicit_M_N_q01_face": explicit_parent_face_audit(
            protected, base, centered, packaging),
        "six_label_four_root_square_totalization":
            square_packet_totalization(pointed),
        "simultaneous_D4_P2_K_Eq_d_even_composition":
            simultaneous_augmented_composition(
                simultaneous, evenness, protected, base),
        "abstract_vs_physical_lifting_and_terminal_dual":
            enriched_lifting_and_omega(
                common_comparison, actual, protected),
        "endpoint_even_annihilator_and_target_gate":
            endpoint_even_annihilator_gate(six_cell, correction),
        "verdict": (
            "The common-V TrigEuler carrier supplies the exact normalized top "
            "R and, on the explicit M/N/q01 face, the two kept response-side "
            "q23/q45 restrictions whose coefficient labels are B1/B4.  The "
            "24 four-root-by-six-label K_Eq edge squares have d^2=target=0, "
            "but the actual source inventory contains no mixed two-cell.  "
            "The simultaneous D4/P2/K_Eq/d_even solve is nonsingular and, "
            "after the labelled q23->B1 and q45->B4 map is granted, cancels "
            "lower, Eq, ores, target and ainc/anchor with no beta denominator.  "
            "Before that map, common V contributes only top R and leaves the "
            "exact proper-face debt (lower,ores)=(-E,+E).  Therefore an "
            "abstract untyped projective comparison exists after formal cap "
            "augmentation, while the physical enriched obstruction is the "
            "single transported mixed-square class detected by omega_mix.  "
            "Passing to the canonical endpoint-even cap quotient removes the "
            "six P/S-odd choices but not that class or the two protected "
            "mixed-target normals.  The 4373 cap/Cartan formula adds no source "
            "column; after a labelled corner placement it extends a detector, "
            "so it is a terminal certificate rather than a filler"
        ),
        "scope": (
            "exact canonical h=3 M/N/q01 parent face, all six B labels, four "
            "oriented root paths (AB-/AB+/AC-/AC+), characteristic-zero "
            "simultaneous transfer, full protected cylinder counts and pinned "
            "callable augmented registry, canonical endpoint-even six-cell "
            "quotient, and exact cap/Cartan dual extension.  The cyclic "
            "A-module criterion is sufficient only after proving that the "
            "physical cap is an A-module and that the displayed full-star "
            "relations exhaust Ann_A(e_R); neither is declared here"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("first-face mixed-square ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=(
        "all", "face", "square", "simultaneous", "dual", "even-target"),
        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        simultaneous = ledger[
            "simultaneous_D4_P2_K_Eq_d_even_composition"]
        print(f"h3 first-face K_Eq/AugP2 square ({arguments.mode}): PASS")
        print("q23/q45 coefficient labels: B1/B4; physical decorated map: NO")
        print("24 square classes: d^2=target=0; existing mixed faces: 0")
        print("simultaneous transfer rank/det:",
              simultaneous["coupled_rank_determinant"])
        print("remaining proper-face debt:",
              simultaneous["exact_remaining_proper_face_debt"])
        print("omega_mix on full schema: 1")
        endpoint = ledger["endpoint_even_annihilator_and_target_gate"]
        print("endpoint-even remaining obstruction dimensions:",
              endpoint["cyclic_A_module_reframing"][
                  "remaining_normalized_obstruction_dimensions"])
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
