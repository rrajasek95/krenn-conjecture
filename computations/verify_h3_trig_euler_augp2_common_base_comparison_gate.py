#!/usr/bin/env python3
"""Audit the common-base comparison shortcut for TrigEulerSpencer -> AugP2.

The trigger branches over one matching parent form the augmented simplex on
the six possible replacement partners.  Hence the response-side construction
is a literal free resolution of the parent-labelled occurrence module.

This checker tests two proposed common bases:

* the root-labelled 90-parent occurrence module; and
* the seven-dimensional termwise/private residual.

The current AugP2 complex has no literal augmentation to either.  Mapping a
selected P3+K2 cap cell back to a response parent changes word, fine degree
and operation idempotent.  The residual seven is a kernel, not a specified
quotient/augmentation target.  After forgetting those tags one can freely
adjoin a second simplex resolution and lift the identity, but that adjoined
cap augmentation is exactly the missing Phi operation.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_order6_trigger_replacement_euler_complement_gate.py":
        "deb84776e620dbf800b24a3a317545259ab6b902d9d07be48bd6ce93e0c6adce",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py":
        "9c182f13ba4da4f2dd3ff49fd9ebf60dd1a218f53cbf4416e82a63236f57404f",
    "computations/verify_h3_uc4_beq_tie_source_provenance_audit.py":
        "f237ccffd40863a201b780ea034fcbd7781bc555e1fbc6f528d99d3ab71394c6",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "computations/verify_h3_eqsystem_augp2_actual_presentation_underdetermination_gate.py":
        "2c112bffeef2c6adb00029077b6b231de396ace76c78756ab0e11e20078a557b",
}
EXPECTED_LEDGER_SHA256 = "8dd925576a5f0154c1836976562656f3ea7807faa0cad13add7f98e07c2b4e66"

PURE_WORD = (1,) * 8
MIXED_WORD = tuple(map(int, "11211211"))
CAP_WORD = tuple(map(int, "01211222"))
ROOT_LABELS = ("AB", "AC")
STAR_PARTNERS = tuple(range(1, 8))


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


def simplex_basis(size: int, degree: int):
    return tuple(combinations(range(size), degree + 1))


def simplex_boundary(size: int, degree: int):
    """Columns of d_degree: C_degree -> C_(degree-1)."""
    require(degree >= 1, degree)
    lower = {face: index for index, face in enumerate(
        simplex_basis(size, degree - 1))}
    columns = []
    for cell in simplex_basis(size, degree):
        column = {}
        for position in range(len(cell)):
            face = cell[:position] + cell[position + 1:]
            column[lower[face]] = Q(-1 if position % 2 else 1)
        columns.append(column)
    return tuple(columns)


def compose_boundaries(size: int, degree: int):
    upper = simplex_boundary(size, degree)
    lower_columns = simplex_boundary(size, degree - 1)
    result = []
    for column in upper:
        image = Counter()
        for middle, coefficient in column.items():
            for row, value in lower_columns[middle].items():
                image[row] += coefficient * value
        result.append({row: value for row, value in image.items() if value})
    return tuple(result)


def matching_inventory(base):
    row = tuple(tuple(monomial) for monomial in base.full_row(PURE_WORD))
    require(len(row) == len(set(row)) == 90, "pure parent row changed")
    star_of_parent = []
    for monomial in row:
        partners = tuple(right for left, right, a, b in monomial
                         if left == 0 and a == b == 1)
        require(len(partners) == 1 and partners[0] in STAR_PARTNERS,
                (monomial, partners))
        star_of_parent.append(partners[0])
    require(Counter(star_of_parent) ==
            Counter({1: 12, 2: 12, 3: 15, 4: 12, 5: 12, 6: 15, 7: 12}),
            Counter(star_of_parent))
    return row, tuple(star_of_parent)


def response_parent_resolution_audit(base) -> dict[str, object]:
    parents, star_of_parent = matching_inventory(base)
    branches = []
    augmentation_columns = []
    for parent_index, (parent, trigger_partner) in enumerate(
            zip(parents, star_of_parent, strict=True)):
        trigger = (0, trigger_partner, 1, 1)
        for replacement_partner in STAR_PARTNERS:
            if replacement_partner == trigger_partner:
                continue
            replacement = (0, replacement_partner, 1, 1)
            branch = list(parent)
            branch.remove(trigger)
            branch.append(replacement)
            recovered = list(branch)
            recovered.remove(replacement)
            recovered.append(trigger)
            require(tuple(sorted(recovered)) == tuple(sorted(parent)),
                    (parent_index, trigger_partner, replacement_partner))
            branches.append((parent_index, trigger_partner,
                             replacement_partner, tuple(sorted(branch))))
            augmentation_columns.append({parent_index: Q(1)})

    require(len(branches) == 540
            and sparse_rank(augmentation_columns) == 90
            and Counter(parent for parent, _i, _j, _b in branches)
                == Counter({index: 6 for index in range(90)}),
            "parent augmentation stopped being six-to-one")

    dimensions = tuple(len(simplex_basis(6, degree)) for degree in range(6))
    boundary_ranks = tuple(
        sparse_rank(simplex_boundary(6, degree))
        for degree in range(1, 6)
    )
    require(dimensions == (6, 15, 20, 15, 6, 1)
            and boundary_ranks == (5, 10, 10, 5, 1)
            and all(not any(compose_boundaries(6, degree))
                    for degree in range(2, 6)),
            (dimensions, boundary_ranks))
    outgoing = (1,) + boundary_ranks
    incoming = boundary_ranks + (0,)
    require(all(outgoing[degree] + incoming[degree] == dimensions[degree]
                for degree in range(6)),
            (dimensions, outgoing, incoming))

    return {
        "base": "V_parent=Q{M: M a pure direct-free matching}",
        "base_dimension_per_root": 90,
        "root_path_labels_retained": list(ROOT_LABELS),
        "base_dimension_with_two_root_paths": 180,
        "literal_branch_augmentation":
            "epsilon_R(g_(M;i|j))=M after delete j/reinsert i",
        "branch_generators_per_root": len(branches),
        "preimages_per_parent": 6,
        "augmentation_rank_per_root": sparse_rank(augmentation_columns),
        "one_parent_simplex_chain_dimensions_C0_to_C5": list(dimensions),
        "one_parent_boundary_ranks_d1_to_d5": list(boundary_ranks),
        "one_parent_augmentation_rank": 1,
        "d_squared_zero": True,
        "exact_in_every_degree": True,
        "one_root_free_module_dimensions_C0_to_C5":
            [90 * value for value in dimensions],
        "one_root_map_ranks_epsilon_d1_to_d5":
            [90] + [90 * value for value in boundary_ranks],
        "two_root_map_ranks_epsilon_d1_to_d5":
            [180] + [180 * value for value in boundary_ranks],
        "response_is_free_projective_resolution_of_parent_base": True,
    }


def residual_seven_audit(landing) -> dict[str, object]:
    ledger, digest = landing.audit()
    require(digest == landing.EXPECTED_LEDGER_SHA256, digest)
    residual = ledger["literal_two_word_residual"]
    private = ledger["private_insertion_restriction"]
    linear = ledger["most_general_two_root_linear_augmentation"]
    physical = ledger["physical_obstruction_after_linear_solution"]
    require(residual["literal_full_nine_monomials"] == 180
            and residual["residual_dimension"] == 7
            and private["rank_on_residual"] == 7
            and linear["freedom_after_both"] == 0
            and physical["first_typed_obstruction"]
                ["current_operation_algebra_value"] == "e_C A e_R=0",
            (residual, private, linear, physical))

    ambient_dimension = residual["literal_full_nine_monomials"]
    kernel_dimension = residual["residual_dimension"]
    return {
        "ambient_occurrence_module_dimension_per_root": ambient_dimension,
        "residual_definition":
            "K7=kernel(all pair, parity, corner, aggregate, fine and cell readouts)",
        "residual_dimension_per_root": kernel_dimension,
        "two_roots_before_covariance": 14,
        "diagonal_residual_after_root_covariance": 7,
        "private_termwise_insertion_rank_on_K7": private["rank_on_residual"],
        "private_map_direction": "K7 injects into 180 private features",
        "K7_is_existing_common_augmentation_quotient": False,
        "K7_is_existing_submodule_kernel": True,
        "abstract_Q_linear_retraction_exists": True,
        "affine_dimension_of_retractions_fixing_K7":
            kernel_dimension * (ambient_dimension - kernel_dimension),
        "canonical_source_labelled_retraction_constructed": False,
        "unique_formal_tied_landing_after_granting_termwise_map":
            linear["unique_tied_solution_exists_in_linear_enriched_category"],
        "physical_termwise_cap_readout_constructed": False,
        "reason": physical["first_typed_obstruction"]["meaning"],
    }


def hamming(left, right) -> int:
    require(len(left) == len(right), (left, right))
    return sum(a != b for a, b in zip(left, right, strict=True))


def cap_augmentation_audit(cap_provenance, packaging, actual) \
        -> dict[str, object]:
    cap_provenance.pin_dependencies()
    cap = cap_provenance.cap_r0_provenance_audit()
    require(cap["internal_B_equals_Eq_tie"]
            and cap["normalized_target"] == 1
            and cap["cross_word_response_to_cap_membership"] == "OPEN",
            cap)

    packaging.pin_dependencies()
    word = packaging.word_and_fine_grade_audit()
    require(not word["literal_grade_preserving_map"]
            and word["word_hamming_distance"] == 6
            and word["all_six_fine_degrees_change"],
            word)

    actual_ledger, actual_digest = actual.audit()
    require(actual_digest == actual.EXPECTED_LEDGER_SHA256, actual_digest)
    presentation = actual_ledger["smallest_literal_generated_presentation"]
    require(presentation["Hom0_response_cap"] == 0
            and presentation["primitive_Hom1_response_cap"] == 0
            and presentation["literal_Gamma_cap_entries"] == 25
            and presentation["Gamma_image_rank_of_callable_registry"] == 23
            and presentation["B_Eq_rank_of_callable_registry"] == 7
            and presentation["attempt_to_build_Phi_mapping_cylinder"]
                == "MissingPhysicalArrow",
            presentation)

    pure_distance = hamming(PURE_WORD, CAP_WORD)
    mixed_distance = hamming(MIXED_WORD, CAP_WORD)
    require((pure_distance, mixed_distance) == (5, 3),
            (pure_distance, mixed_distance))

    # Coordinates retain the operation parent and the protected cap rows.
    # The first vector is the response Euler carrier.  The second is physical
    # r0.  They become equal only after quotienting every protected coordinate
    # and identifying the two operation idempotents.
    typed_G0 = (Q(1), Q(0), Q(0), Q(0), Q(0))
    typed_r0 = (Q(0), Q(1), Q(1), Q(1), Q(1))
    retagged_G0 = (Q(1), Q(0), Q(0), Q(0))
    retagged_r0 = (Q(1), Q(1), Q(1), Q(1))
    require(sparse_rank((dict(enumerate(typed_G0)),
                         dict(enumerate(typed_r0)))) == 2
            and sparse_rank((dict(enumerate(retagged_G0)),
                             dict(enumerate(retagged_r0)))) == 2,
            "protected r0/G0 distinction collapsed")

    return {
        "candidate_cap_augmentation":
            "epsilon_C(selected P3+K2 branch labelled by M)=M",
        "literal_in_current_AugP2_complex": False,
        "word_checks": {
            "TrigEuler_pure_to_cap_hamming": pure_distance,
            "TrigEuler_mixed_to_cap_hamming": mixed_distance,
            "selected_collision_response_to_cap_hamming":
                word["word_hamming_distance"],
            "all_six_selected_collision_fine_degrees_change":
                word["all_six_fine_degrees_change"],
        },
        "operation_checks": {
            "Hom0_response_cap": presentation["Hom0_response_cap"],
            "primitive_Hom1_response_cap":
                presentation["primitive_Hom1_response_cap"],
            "implemented_operation_changing_atoms": 0,
            "root_path_label_effect": (
                "records the desired endpoints but does not create a path "
                "between the response and cap idempotents"
            ),
        },
        "current_cap_registry": {
            "literal_Gamma_entries":
                presentation["literal_Gamma_cap_entries"],
            "Gamma_image_rank":
                presentation["Gamma_image_rank_of_callable_registry"],
            "B_Eq_rank":
                presentation["B_Eq_rank_of_callable_registry"],
            "mapping_cylinder":
                presentation["attempt_to_build_Phi_mapping_cylinder"],
        },
        "protected_comparison_coordinates":
            ["B_response", "B_cap", "Eq_cap", "target_cap", "Hom_RC"],
        "typed_G0": [int(value) for value in typed_G0],
        "typed_r0": [int(value) for value in typed_r0],
        "rank_typed_G0_r0": 2,
        "after_formal_B_retag_G0": [int(value) for value in retagged_G0],
        "after_formal_B_retag_r0": [int(value) for value in retagged_r0],
        "rank_after_formal_B_retag": 2,
        "actual_r0_boundary": cap["internal_cap_differential"],
        "actual_r0_B_Eq_tied": cap["internal_B_equals_Eq_tie"],
        "actual_r0_normalized_target": cap["normalized_target"],
        "first_failure": (
            "epsilon_C is not a typed morphism: the labelled reinsertion "
            "changes word/fine/operation, and r0 carries independent Eq, "
            "target and response-to-cap coordinates absent from G0"
        ),
    }


def comparison_lifting_audit(response, residual, cap) -> dict[str, object]:
    require(response["response_is_free_projective_resolution_of_parent_base"]
            and not residual["K7_is_existing_common_augmentation_quotient"]
            and not cap["literal_in_current_AugP2_complex"],
            (response, residual, cap))
    return {
        "response_resolution_status":
            "literal free/projective and acyclic over V_parent",
        "cap_resolution_status": (
            "not testable over V_parent or K7: no literal cap augmentation "
            "to either base is defined"
        ),
        "abstract_vector_space_projectivity": True,
        "why_abstract_projectivity_is_insufficient": (
            "the comparison theorem first requires two augmentations in the "
            "same typed category; forgetting word, fine, operation, B, Eq and "
            "target changes that category"
        ),
        "formal_untyped_completion": {
            "construction": (
                "freely adjoin one cap-labelled copy of every response branch "
                "and its simplex faces, then send both copies to M"
            ),
            "cap_copy_is_free_resolution": True,
            "identity_lift_exists": True,
            "normalized_syzygy": "dK=r0-G0",
            "source_status": (
                "circular: the adjoined epsilon_C and K are precisely the "
                "missing response-to-cap Phi mapping cylinder"
            ),
        },
        "physical_normalized_syzygy_exists": False,
        "first_syzygy_failure": (
            "r0-G0 is zero only in the operation/protected-row-forgetting "
            "quotient; with target/B/Eq retained its readout is nonzero"
        ),
        "shortest_positive_datum": (
            "one literal root-natural augmentation epsilon_C from the selected "
            "P3+K2/AugP2 Spencer packet to the root-labelled parent module, "
            "including word/fine transport, B=Eq, normalized target and all "
            "proper reinsertion faces.  Once that exists, the response simplex "
            "resolution gives the normalized comparison lift formally"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "common_base_matching",
    )
    landing = load(
        "computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py",
        "common_base_landing",
    )
    cap_provenance = load(
        "computations/verify_h3_uc4_beq_tie_source_provenance_audit.py",
        "common_base_cap_provenance",
    )
    packaging = load(
        "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py",
        "common_base_packaging",
    )
    actual = load(
        "computations/verify_h3_eqsystem_augp2_actual_presentation_underdetermination_gate.py",
        "common_base_actual",
    )

    response = response_parent_resolution_audit(base)
    residual = residual_seven_audit(landing)
    cap = cap_augmentation_audit(cap_provenance, packaging, actual)
    comparison = comparison_lifting_audit(response, residual, cap)
    ledger = {
        "theorem": "h3 TrigEulerSpencer/AugP2 common-base comparison gate",
        "pins": PINS,
        "response_parent_simplex_resolution": response,
        "termwise_private_residual_seven": residual,
        "cap_common_augmentation": cap,
        "comparison_theorem_test": comparison,
        "verdict": (
            "The common-base idea succeeds exactly on the response side.  "
            "For every parent M its six trigger branches and all higher "
            "simplex faces form a literal free resolution, so two root paths "
            "resolve the root-labelled 180-dimensional parent module.  The "
            "seven-dimensional termwise/private object is instead a kernel "
            "inside the 180-occurrence carrier, with 1211-dimensional freedom "
            "in an abstract retraction and no canonical physical augmentation.  "
            "On the cap side the proposed reinsertion changes word, fine and "
            "operation idempotent; the current presentation has Hom(response,"
            "cap)=0, while physical r0 also has B=Eq and normalized target.  "
            "Thus C_AugP2 is not presently a resolution of the same base and "
            "the comparison theorem cannot be invoked.  Freely adjoining the "
            "cap augmentation makes the lift and dK=r0-G0 tautological, but "
            "that adjoining is exactly the missing Phi constructor"
        ),
        "scope": (
            "exact rational augmented-simplex resolution on all 90 pure "
            "parents and two root labels; pinned exact residual-seven, cap-r0, "
            "word/fine and literal-operation audits.  This obstructs the "
            "redundant-presentation shortcut in the current typed category, "
            "not the explicitly stated new cap augmentation"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("common-base ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("full", "structural"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    if arguments.mode == "structural":
        pin_dependencies()
        print("h3 common-base comparison structural gate: PASS")
        return
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"ledger": ledger, "sha256": digest},
                         indent=2, sort_keys=True))
    else:
        response = ledger["response_parent_simplex_resolution"]
        cap = ledger["cap_common_augmentation"]
        print("h3 TrigEuler/AugP2 common-base comparison gate: PASS")
        print("response simplex exact:",
              response["response_is_free_projective_resolution_of_parent_base"])
        print("residual seven is common quotient: NO")
        print("literal cap augmentation: NO")
        print("first failure:", cap["first_failure"])
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
