#!/usr/bin/env python3
"""Reduce physical Gamma_* terminal promotion to a finite primitive registry.

The complete protected Gamma_* output has dimension 127.  The 138 literal
local dark columns have rank 126 and are exactly the kernel of

    omega_Eq = delta.(B-Eq)/12.

Adjoining the Eq-only balanced vector gives rank 127.  Consequently *every*
possible boundary column in this codomain has a unique quotient coefficient:

    y = d - omega_Eq(y) e_Eq,   d in D_dark.

Thus the 13,601 declared generator occurrences plus a single nonzero Eq orbit
are already exhaustive at the boundary-image level.  Physical Fredholm
promotion requires only a finite, complete registry of indecomposable
same-grade physical C1 generators and the check omega_Eq(dg)=0 on each.

The official EqSystem/Macaulay presentation does not provide that registry:
it has no operation, fine, repeated, window, or AugP2 labels.  The current
callable enriched registry has 128 objectwise generators and zero bright
charges, but explicitly is not complete for Hom(response,cap).  The
underived (H0-u)eq commutator is a single candidate orbit whose projection
to e_Eq and physical descent are both unconstructed.  A two-completion model
shows that cell-level essential surjectivity cannot be inferred from the
official source data, even though no second boundary obstruction can occur.
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
    "computations/verify_h3_declared_divided_weyl_trigger_gamma_terminal_gate.py":
        "acb8a4eedc7c708ce63618a82cb45359111daa1f2c8c71a33796fc02238c5a32",
    "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py":
        "6c42cd4dc7dca1544dc0b675f5f4543ec348f1fba34b7ea14bf80cc6a20b9cf1",
    "computations/verify_h3_eqsystem_augp2_actual_presentation_underdetermination_gate.py":
        "2c112bffeef2c6adb00029077b6b231de396ace76c78756ab0e11e20078a557b",
    "computations/verify_h3_gamma_star_source_derived_free_closure_census.py":
        "a479ac8759bf7a18b43ee91d8b1ab7d0b432c48a7787b065cac68403ace3df3a",
    "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py":
        "7d9e49f34da84772f6e0863a9bfe56cb9a90e0cfd3fceb76da59175ffea36c50",
    "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py":
        "e5f2664b99c5ba58e0be385ca52dc52c6d2f6d6d0b793e655ebe297542dce291",
    "computations/verify_chart_model_is_official_eqsystem.py":
        "ef1a997323e0a116787fa3c50368e22ecd33804942a9179eabefa2993e4d9373",
}
EXPECTED_LEDGER_SHA256 = (
    "e320c9f8afff04010da5d913c79859497e1ab8936ced05eef1852cd1a2d8d0f8"
)


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
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def add(left, right):
    return tuple(Q(a) + Q(b)
                 for a, b in zip(left, right, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def protected_boundary_quotient_audit(local, declared) -> dict[str, object]:
    families = (
        local.top_projection_columns()
        + local.lower_face_and_reinsertion_columns()
        + local.external_augmented_columns()
    )
    names = tuple(name for name, _vector in families)
    dark = tuple(vector for _name, vector in families)
    integral = local.integral_terminal_dual()
    omega = scale(Q(1, 12), integral)
    eq_orbit = local.balanced_top("Eq")
    rhs = local.balanced_top("B")
    require(len(names) == len(set(names)) == 138
            and len(eq_orbit) == len(rhs) == len(integral) == 127,
            (len(names), len(eq_orbit)))
    rank_dark = local.rank(dark)
    rank_with_eq = local.rank(dark + (eq_orbit,))
    require(rank_dark == 126 and rank_with_eq == 127
            and all(dot(omega, column) == 0 for column in dark)
            and dot(omega, eq_orbit) == -1
            and dot(omega, rhs) == 1,
            (rank_dark, rank_with_eq, dot(omega, eq_orbit), dot(omega, rhs)))

    # Exact universal decomposition.  Since D is contained in ker(omega)
    # and both have dimension 126, they are equal.  The displayed formula is
    # also replayed on every coordinate basis vector.
    for row in range(127):
        basis = tuple(Q(index == row) for index in range(127))
        coefficient = -dot(omega, basis)
        residual = add(basis, scale(-coefficient, eq_orbit))
        require(dot(omega, residual) == 0,
                ("basis decomposition", row, coefficient))
    require(add(rhs, eq_orbit) == local.tied_balanced_top(),
            "RHS plus Eq orbit stopped being tied/dark")

    declared_ledger, declared_digest = declared.audit()
    require(declared_digest == declared.EXPECTED_LEDGER_SHA256,
            declared_digest)
    invocation = declared_ledger["declared_free_generator_invocations"]
    require(invocation["count"] == 13601
            and invocation["omega_Eq_charge_histogram"] == {"0": 13601},
            invocation)
    return {
        "protected_output_dimension": 127,
        "literal_dark_columns": len(dark),
        "literal_dark_rank": rank_dark,
        "ker_omega_Eq_dimension": 126,
        "dark_image_equals_ker_omega_Eq": True,
        "declared_dark_generator_invocations": invocation["count"],
        "Eq_orbit_representative": "e_Eq=balanced_top(Eq)",
        "omega_Eq_on_Eq_orbit": -1,
        "rank_after_Eq_orbit": rank_with_eq,
        "universal_boundary_decomposition": (
            "for every y in Y_Gamma*, y=d-omega_Eq(y)e_Eq with d in D_dark"
        ),
        "decomposition_checked_on_all_coordinate_basis_vectors": 127,
        "literal_balanced_private_RHS": "b_Gamma*=balanced_top(B)",
        "omega_Eq_on_RHS": 1,
        "RHS_plus_Eq_orbit": "balanced_top(B)+balanced_top(Eq) is dark",
        "consequence": (
            "there is exactly one possible protected boundary obstruction; "
            "no independently primitive physical cell can create a second "
            "boundary-quotient direction"
        ),
    }


def actual_source_and_macaulay_audit(actual, source_derived,
                                     source_census) -> dict[str, object]:
    actual_ledger, actual_digest = actual.audit()
    require(actual_digest == actual.EXPECTED_LEDGER_SHA256, actual_digest)
    official = actual_ledger["official_EqSystem_first_presentation"]
    literal = actual_ledger["smallest_literal_generated_presentation"]
    require(official["canonical_weight_variables"] == 252
            and official["relation_cells"] == 6561
            and official["perfect_matching_monomials_per_relation"] == 105
            and not official["primitive_response_to_cap_operation_defined"],
            official)
    require(literal["callable_non_EqSystem_primitives"] == 128
            and literal["literal_Gamma_cap_entries"] == 25
            and literal["Gamma_image_rank_of_callable_registry"] == 23
            and literal["B_Eq_rank_of_callable_registry"] == 7
            and literal["all_callable_Psi_charges"] == 0
            and literal["primitive_Hom1_response_cap"] == 0,
            literal)

    derived_ledger, derived_digest = source_derived.audit()
    require(derived_digest == source_derived.EXPECTED_LEDGER_SHA256,
            derived_digest)
    executable = derived_ledger["executable_Gen_phys"]
    closure = derived_ledger["typed_free_closure"]
    require(executable["constructor_invocations"] == 128
            and executable["Psi_charge_histogram"] == {"0": 128}
            and executable["implemented_operation_changing_atoms"] == 0
            and closure["Hom0_response_cap_dimension"] == 0
            and closure["free_closure_operation_changing_C1_count"] == 0,
            (executable, closure))

    # The coefficient part really is finite after the external Gamma fine
    # enrichment: each of six squarefree cubic target monomials has eight
    # divisor/complement choices.  EqSystem itself does not contain that fine
    # enrichment, so the count cannot enumerate operation primitives.
    slots = 0
    degree_histogram = {degree: 0 for degree in range(4)}
    for target in source_census.SELECTED_FACES:
        require(len(target) == len(set(target)) == 3, target)
        for mask in range(8):
            relation_degree = sum(bool(mask & (1 << index))
                                  for index in range(3))
            degree_histogram[relation_degree] += 1
            slots += 1
    require(slots == 48
            and degree_histogram == {0: 6, 1: 18, 2: 18, 3: 6},
            (slots, degree_histogram))
    return {
        "official_EqSystem": {
            "weight_variables": official["canonical_weight_variables"],
            "relation_cells": official["relation_cells"],
            "matching_monomials_per_relation":
                official["perfect_matching_monomials_per_relation"],
            "labels_present": official["literal_labels_present"],
            "labels_absent": official["literal_labels_absent"],
            "Hom_response_cap_defined": False,
        },
        "fixed_enriched_Gamma_Macaulay_part": {
            "squarefree_target_fine_monomials": 6,
            "divisor_complement_slots": slots,
            "relation_degree_histogram": {
                str(degree): count
                for degree, count in degree_histogram.items()
            },
            "coefficient_part_finite_and_exhaustive_after_enrichment": True,
        },
        "current_callable_enriched_registry": {
            "primitive_constructor_invocations":
                executable["constructor_invocations"],
            "literal_Gamma_entries": executable["literal_Gamma_entries"],
            "Gamma_image_rank": executable["Gamma_image_rank"],
            "B_Eq_image_rank": executable["B_Eq_image_rank"],
            "omega_Eq_charge_histogram": executable["Psi_charge_histogram"],
            "operation_changing_atoms":
                executable["implemented_operation_changing_atoms"],
            "Hom0_response_cap": closure["Hom0_response_cap_dimension"],
            "Hom1_response_cap":
                closure["free_closure_operation_changing_C1_count"],
            "registry_is_exhaustive_for_actual_physical_source": False,
        },
        "sharp_interface": (
            "Macaulay finiteness exhausts coefficient multiples once the "
            "Gamma fine grade is externally supplied, but EqSystem has no "
            "enriched operation generator sort; it cannot enumerate primitive "
            "response-to-cap cells"
        ),
    }


def underived_eq_orbit_audit(commutator) -> dict[str, object]:
    ledger, digest = commutator.audit()
    require(digest == commutator.EXPECTED_DIGEST, digest)
    initial = ledger["initial_layer"]
    top = ledger["qzero_top"]
    require(initial["isolated_underived_commutator"]
                == "h_v*(H_0-u)*eq"
            and initial["commutator_terms"] == 273
            and top["diagonal_projection_commutator"] == "(H_0-u)*eq"
            and not top["underived_source_descent"],
            (initial, top))
    return {
        "source_orbit": "h_v*(H_0-u)*eq over 5 deleted sites x 3 matchings",
        "orbit_representatives": 15,
        "one_orbit_under_deleted-site/matching_transport": True,
        "universal_direct_free_support_terms_at_initial_face":
            initial["commutator_terms"],
        "qzero_top": top["diagonal_projection_commutator"],
        "target": initial["target"],
        "ordinary_residue": initial["ordinary_residue"],
        "underived_source_descent_constructed": False,
        "required_protected_projection": (
            "pi_Gamma*((H_0-u)*eq)=nonzero scalar times balanced_top(Eq) "
            "modulo D_dark"
        ),
        "protected_projection_constructed": False,
        "interpretation": (
            "this is the unique known source-shaped candidate for the one "
            "boundary quotient line, but neither its underived cell nor its "
            "Gamma_* operation-labelled projection currently exists"
        ),
    }


def direct_official_jet_bypass_audit() -> dict[str, object]:
    """Test whether the official fixed-grade jet matrix alone can see omega.

    There are 48 finite native divisor/complement slots, but no native B/Eq
    or operation row.  The two displayed finite completions have identical
    restriction to that complete native matrix and different augmented rank.
    """
    native_dimension = 48
    official_columns = tuple(
        tuple(Q(row == column) for row in range(native_dimension))
        for column in range(native_dimension)
    )
    require(len(official_columns) == native_dimension
            and all(sum(column) == 1 for column in official_columns),
            "native jet identity model changed")

    # Completion zero embeds the entire official matrix with zero protected
    # charge.  Completion bright adds one primitive in the kernel of the
    # forgetful restriction.  Their official 48-row matrices are identical.
    completion_zero = tuple(column + (Q(0),)
                            for column in official_columns)
    bright_kernel_column = (Q(0),) * native_dimension + (Q(1),)
    completion_bright = completion_zero + (bright_kernel_column,)
    restriction_zero = tuple(column[:-1] for column in completion_zero)
    restriction_bright = tuple(column[:-1]
                               for column in completion_bright[:-1])
    require(restriction_zero == restriction_bright == official_columns
            and bright_kernel_column[:-1] == (Q(0),) * native_dimension,
            "two jet completions stopped having identical native restriction")
    require(len(completion_zero) == 48 and len(completion_bright) == 49,
            "jet completion counts changed")
    return {
        "official_fixed_Gamma_jet_grade_slots": native_dimension,
        "operator_description": (
            "all divisor differential operators and degree-complementing "
            "multipliers for the six squarefree cubic Gamma fine monomials"
        ),
        "finite_native_matrix_enumerable": True,
        "native_rows": [
            "EqSystem colour word",
            "252-variable polynomial exponent/fine degree after an external choice",
        ],
        "missing_native_rows": [
            "B versus reduced-Eq occurrence",
            "response versus cap operation parent",
            "P3+K2 repeated type",
            "fixed-window/root path",
            "target/q/anchor/W/ores/ridge/eta/sigma augmentation",
        ],
        "omega_Eq_is_a_functional_on_official_native_jet_space": False,
        "reason": (
            "omega_Eq reads a derived private-minus-Eq augmentation; neither "
            "coordinate is a row of the official EqSystem jet matrix"
        ),
        "two_finite_completions": {
            "common_official_matrix_columns": len(official_columns),
            "completion_zero_augmented_columns": len(completion_zero),
            "completion_bright_augmented_columns": len(completion_bright),
            "official_restrictions_identical": True,
            "bright_extra_column_official_shadow": 0,
            "bright_extra_column_omega_Eq_charge": 1,
        },
        "direct_official_left_null_certificate_possible": False,
        "minimal_enrichment": {
            "name": "GammaJetEnrichment",
            "data": [
                "an operation/fine/repeated/window-labelled fixed-grade jet domain",
                "a chain and augmentation map J_phys,Gamma* into the pinned 127-row Y_Gamma*",
                "a completeness statement that every physical primitive in the kernel of forgetting to EqSystem is a domain generator",
            ],
            "finite_after_enrichment": True,
            "decision_after_enrichment": (
                "evaluate omega_Eq on every column; the one-dimensional "
                "boundary quotient makes this complete"
            ),
        },
    }


def finite_registry_reduction_and_counterguard() -> dict[str, object]:
    # Abstract source-cell quotients.  E is the single Eq commutator orbit;
    # z is an independently primitive off-diagonal cell with the same zero
    # official-source restriction.  Their source ranks differ, although their
    # protected boundary images both lie on the single quotient line.
    model_e = ((Q(1), Q(0)),)
    model_ez = model_e + ((Q(0), Q(1)),)
    require(len(model_e) == 1 and len(model_ez) == 2,
            "abstract countercompletion rank changed")
    return {
        "finite_reduction_theorem": {
            "input_contract": [
                "a finite registry Gen_phys(Gamma*) of every indecomposable physical relative-C1 generator",
                "each record retains word/fine/repeated/operation/root/window and all 127 protected boundary rows",
                "the physical C1 domain is the semi-free cellular closure of those registered indecomposables",
            ],
            "decision_test": (
                "for every registered g compute lambda_g=omega_Eq(dg); "
                "lambda_g=0 iff dg lies in D_dark"
            ),
            "terminal_branch": (
                "all lambda_g=0 implies omega_Eq annihilates the exhaustive "
                "physical map and the literal RHS value 1 promotes it"
            ),
            "filler_branch": (
                "one lambda_g!=0 spans the unique boundary quotient and is "
                "the physical Eq-orbit/filler candidate"
            ),
            "why_primitive_checks_suffice": (
                "a semi-free degree-one word contains exactly one degree-one "
                "indecomposable; the coefficient complements at Gamma_* are "
                "the finite 48-slot Macaulay list, and d plus multiplication "
                "are linear"
            ),
        },
        "minimal_missing_hypothesis": {
            "name": "GammaPrimitiveCompleteness",
            "statement": (
                "the callable enriched registry is extended to a finite list "
                "containing every indecomposable physical Gamma_* C1 cell, "
                "with a literal differential into the pinned 127-row codomain"
            ),
            "strictly_weaker_than": (
                "a source-cell factorization through all 13,601 declared "
                "presentation generators; Fredholm promotion only needs the "
                "boundary charge of each primitive"
            ),
        },
        "two_completion_counterguard": {
            "common_data": (
                "official EqSystem, all coefficient/Macaulay rows, 128 "
                "callable enriched generators, and the candidate Eq orbit"
            ),
            "completion_A_source_quotient_basis": ["E_underived"],
            "completion_B_source_quotient_basis": ["E_underived", "z_exotic"],
            "source_quotient_ranks": [1, 2],
            "z_official_source_and_callable_shadow": 0,
            "protected_boundary_quotient_ranks": [1, 1],
            "reason_boundary_rank_does_not_grow": (
                "Y_Gamma*/D_dark is already one-dimensional, so z has a "
                "boundary congruent to a scalar multiple of E_underived"
            ),
            "consequence": (
                "the actual source/Macaulay presentation cannot prove "
                "cell-level generation by the Eq orbit; however the Fredholm "
                "question only asks whether any registered primitive has "
                "nonzero charge on that one boundary line"
            ),
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    declared = load(
        "computations/verify_h3_declared_divided_weyl_trigger_gamma_terminal_gate.py",
        "actual_primitive_declared",
    )
    local = load(
        "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py",
        "actual_primitive_local",
    )
    actual = load(
        "computations/verify_h3_eqsystem_augp2_actual_presentation_underdetermination_gate.py",
        "actual_primitive_eqsystem",
    )
    source_derived = load(
        "computations/verify_h3_gamma_star_source_derived_free_closure_census.py",
        "actual_primitive_source_derived",
    )
    source_census = load(
        "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py",
        "actual_primitive_source_census",
    )
    commutator = load(
        "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py",
        "actual_primitive_commutator",
    )
    ledger = {
        "theorem": "h3 actual-source primitive terminal reduction gate",
        "pins": PINS,
        "protected_boundary_quotient":
            protected_boundary_quotient_audit(local, declared),
        "actual_source_and_Macaulay_presentation":
            actual_source_and_macaulay_audit(
                actual, source_derived, source_census),
        "direct_official_Macaulay_jet_bypass":
            direct_official_jet_bypass_audit(),
        "single_underived_Eq_commutator_orbit":
            underived_eq_orbit_audit(commutator),
        "finite_primitive_reduction_and_counterguard":
            finite_registry_reduction_and_counterguard(),
        "verdict": (
            "At the protected boundary level the proposed reduction is true: "
            "the 13,601 declared dark occurrences have image ker(omega_Eq), "
            "and one nonzero Eq orbit completes the 127-dimensional codomain. "
            "Thus every physical boundary is dark plus a unique Eq-orbit "
            "coefficient.  At the source-cell level the proposition is not a "
            "theorem of the actual EqSystem/Macaulay presentation, because "
            "that presentation does not define enriched operation primitives; "
            "two completions with the same source restriction can differ by "
            "one independent cell.  The minimal promotion hypothesis is a "
            "finite complete primitive registry with literal protected "
            "boundaries.  Its decision is then only the finite test "
            "omega_Eq(dg)=0.  The current 128-entry registry passes but is "
            "explicitly incomplete.  Direct enumeration of the 48 native "
            "official Macaulay/jet slots cannot bypass this: omega_Eq is not "
            "a functional on the official row space, and a bright kernel "
            "column leaves its full native matrix unchanged.  The minimal "
            "extra datum is GammaJetEnrichment, equivalently the complete "
            "primitive registry.  The known underived Eq commutator has "
            "neither physical descent nor a constructed Gamma projection."
        ),
        "nonclaim": (
            "the abstract exotic completion is not a GHZ counterexample, and "
            "the Eq-only local vector is not identified with the polynomial "
            "commutator before a source-provenant Gamma projection is built"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("actual-source primitive reduction ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    if arguments.mode == "structural":
        pin_dependencies()
        print("h3 actual-source primitive reduction structural gate: PASS")
        return
    ledger, digest = audit()
    if arguments.mode == "exhaustive":
        quotient = ledger["protected_boundary_quotient"]
        require(quotient["decomposition_checked_on_all_coordinate_basis_vectors"]
                == 127, quotient)
    if arguments.json:
        print(json.dumps({"ledger": ledger, "sha256": digest},
                         indent=2, sort_keys=True))
    else:
        print("h3 actual-source primitive terminal reduction gate: PASS")
        print("boundary quotient: one-dimensional; dark + Eq spans 127/127")
        print("current callable registry: 128 entries, all dark, incomplete")
        print("physical terminal: finite primitive charge test, registry missing")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
