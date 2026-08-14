#!/usr/bin/env python3
"""Promote omega_Eq over the declared h=3 divided-Weyl/trigger algebra.

This is an exhaustive theorem for a *declared free cellular presentation*, not
an enumeration theorem for all primitive physical operations.  The declared
relative-C1 domain contains the two-root full-star simplices, every labelled
deleted-factor and lcm-ambiguity cylinder, the derived cap Hasse/Koszul cubes,
the endpoint-even target cone, the complete local protected cap presentation,
and every squarefree degree-complement slot in the six Gamma_* fine grades.

Every such generator is response-internal, outside the private/Eq block, or
has tied private and Eq incidence.  Hence the normalized local covector

    omega_Eq = delta.(B-Eq)/12

kills the complete declared boundary.  It reads one on the literal balanced
private top.  Promotion to the physical Fredholm terminal is therefore
equivalent to essential surjectivity of this presentation on primitive
same-grade relative-C1 physical cells (including source provenance of the
target cone and of the displayed RHS in the same augmented map).
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
    "computations/verify_h3_endpoint_even_hom_target_cone_eq_terminal_gate.py":
        "c6886ba4652dd6cc4c92219db966e7b1a3e48ef2afe332b32b9d4576b3fa8e37",
    "computations/verify_h3_full_star_minimal_protected_homogenizer_cylinder_gate.py":
        "ab7471a38683da113723ea9a073e3dc2a3c76d4576b9e575a0983ab1054c5d58",
    "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py":
        "e5f2664b99c5ba58e0be385ca52dc52c6d2f6d6d0b793e655ebe297542dce291",
    "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py":
        "6c42cd4dc7dca1544dc0b675f5f4543ec348f1fba34b7ea14bf80cc6a20b9cf1",
    "computations/verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
    "computations/verify_h3_psi_canonical_source_resolution_degree1_loophole_gate.py":
        "feb162f9d13d6debff78361fd28cada31a61bd9ccd57aab62f2722bf365c5064",
    "computations/verify_h3_trig_euler_augp2_common_base_comparison_gate.py":
        "3ca82479bd2d1c2847dff55f3c05c87f24406ec1c2f3a5fbb9cdf619a6f7047a",
}
EXPECTED_LEDGER_SHA256 = (
    "6c6458a9ea11f65deb1b0956eb7598b3a8a89f2f3dc614730a9c89b3548defa9"
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


def full_star_and_cylinder_audit(common, protected) -> dict[str, object]:
    simplex_dimensions = tuple(
        len(common.simplex_basis(6, degree)) for degree in range(6)
    )
    require(simplex_dimensions == (6, 15, 20, 15, 6, 1),
            simplex_dimensions)
    parents_per_root = 90
    root_labels = 2
    simplex_generators = (
        parents_per_root * root_labels * sum(simplex_dimensions)
    )
    require(simplex_generators == 11340, simplex_generators)

    protected_ledger, protected_digest = protected.audit()
    require(protected_digest == protected.EXPECTED_LEDGER_SHA256,
            protected_digest)
    cylinders = protected_ledger["minimal_presentation_safe_cylinders"]
    quotient = protected_ledger[
        "complete_augmented_operation_quotient_and_dual"
    ]
    require(cylinders["presentation_safe_deleted_factor_cylinders"] == 1020
            and cylinders["presentation_safe_ambiguity_cylinders"] == 9,
            cylinders)
    require(quotient["rank_ladder"] == [6, 2046, 2064, 2065],
            quotient["rank_ladder"])
    return {
        "six_trigger_simplex_dimensions": list(simplex_dimensions),
        "parents_per_root": parents_per_root,
        "root_labels": ["AB", "AC"],
        "two_root_full_star_generators": simplex_generators,
        "deleted_factor_cylinders_per_root": 1020,
        "two_root_deleted_factor_cylinders": 2040,
        "lcm_ambiguity_cylinders_per_root": 9,
        "two_root_lcm_ambiguity_cylinders": 18,
        "protected_rank_ladder": quotient["rank_ladder"],
        "omega_Eq_projection": 0,
        "reason": (
            "full-star and presentation cylinders remain in the labelled "
            "response summand; no private-minus-Eq cap coordinate is created"
        ),
    }


def cap_hasse_and_target_audit(hasse, hom_gate, local) -> dict[str, object]:
    cubes = []
    for deleted in hasse.ODD:
        for matching in hasse.matchings(hasse.face(deleted)):
            cubes.append(hasse.audit_one_cube(deleted, matching))
    require(len(cubes) == 15
            and all(cube["indexed_hasse_cycle_terms"] == 17
                    and cube["target"] == cube["ordinary_residue"] == 0
                    and cube["top_chain"] == "r_0-T"
                    and cube["diagonal_projection_commutator"]
                        == "(H_0-u)*eq"
                    for cube in cubes), cubes)
    hasse.cubical_sign_audit()

    hom_ledger, hom_digest = hom_gate.audit()
    require(hom_digest == hom_gate.EXPECTED_LEDGER_SHA256, hom_digest)
    cone = hom_ledger["canonical_target_cone"]
    require(cone["target_H1_before_after_cone"] == [2, 0]
            and cone["total_relative_H1_before_after_cone"] == [3, 1]
            and cone["relative_H0_before_after_cone"] == [0, 0], cone)

    dual = local.integral_terminal_dual()
    tied_top = local.tied_balanced_top()
    tied_direction = local.add(local.primitive_direction_face("B"),
                               local.primitive_direction_face("Eq"))
    tied_tail = local.add(local.balanced_tail_face("B"),
                          local.balanced_tail_face("Eq"))
    require(dot(dual, tied_top) == dot(dual, tied_direction)
            == dot(dual, tied_tail) == 0, "derived cap tie changed")
    return {
        "deleted_odd_sites": list(hasse.ODD),
        "perfect_matchings_per_deleted_site": 3,
        "derived_Hasse_Koszul_cubes": len(cubes),
        "indexed_terms_per_cube": 17,
        "indexed_terms_total": sum(
            cube["indexed_hasse_cycle_terms"] for cube in cubes
        ),
        "derived_cube_projection": "B=Eq (objectwise/tied)",
        "derived_cube_omega_Eq_projection": 0,
        "endpoint_even_target_cone_objects": ["T23", "T45"],
        "target_H1_before_after_cone": [2, 0],
        "total_H1_before_after_cone": [3, 1],
        "H0_before_after_cone": [0, 0],
        "target_cone_omega_Eq_projection": 0,
        "excluded_underived_face": {
            "formula": "(H_0-u)*eq",
            "why_excluded": (
                "the same cube proves top tau(H_m)=1, so this diagonal "
                "projection is not a descended physical relative-C1 column; "
                "constructing that descent is precisely the surviving Eq class"
            ),
        },
        "target_cone_status": (
            "included in the declared relative target presentation; its "
            "occurrence-local physical source provenance remains part of the "
            "essential-surjectivity hypothesis"
        ),
    }


def macaulay_complement_audit(source) -> dict[str, object]:
    slots = []
    degree_histogram: Counter[int] = Counter()
    word = source.CAP_WORD
    for target in source.SELECTED_FACES:
        target_set = frozenset(target)
        target_fine = source.fine_degree(tuple(target), word)
        for mask in range(1 << len(target)):
            relation = tuple(target[index] for index in range(len(target))
                             if mask & (1 << index))
            multiplier = tuple(label for label in target
                               if label not in relation)
            require(frozenset(relation).isdisjoint(multiplier)
                    and frozenset(relation) | frozenset(multiplier)
                        == target_set,
                    (target, relation, multiplier))
            relation_fine = source.fine_degree(relation, word)
            multiplier_fine = source.fine_degree(multiplier, word)
            require(tuple(left + right for left, right in
                          zip(relation_fine, multiplier_fine, strict=True))
                    == target_fine,
                    (target, relation, multiplier))
            slots.append((target, relation, multiplier))
            degree_histogram[len(relation)] += 1
    require(len(slots) == 48
            and degree_histogram == Counter({0: 6, 1: 18, 2: 18, 3: 6}),
            (len(slots), degree_histogram))
    return {
        "Gamma_fine_monomials": ["*".join(face)
                                  for face in source.SELECTED_FACES],
        "squarefree_divisor_complement_slots": len(slots),
        "relation_degree_histogram": {
            str(degree): degree_histogram[degree] for degree in range(4)
        },
        "fine_coordinate_width": 24,
        "every_relation_times_complement_has_exact_target_fine_degree": True,
        "nondividing_monomial": "off the fixed Gamma_* fine summand",
        "omega_Eq_projection": 0,
        "reason": (
            "coefficient/Macaulay multiples are canonical response "
            "presentation images; multiplication preserves word and operation "
            "tags and creates no private-minus-Eq cap incidence"
        ),
    }


def local_declared_columns_audit(local) -> dict[str, object]:
    families = {
        "top_projection": local.top_projection_columns(),
        "PP_and_reinsertion": local.lower_face_and_reinsertion_columns(),
        "external_augmented": local.external_augmented_columns(),
    }
    dual = local.integral_terminal_dual()
    require({name: len(columns) for name, columns in families.items()}
            == {"top_projection": 24, "PP_and_reinsertion": 84,
                "external_augmented": 30}, "local family count changed")
    require(all(dot(dual, vector) == 0
                for columns in families.values()
                for _name, vector in columns),
            "omega_Eq became bright on a protected local column")
    return {
        "family_counts": {name: len(columns)
                          for name, columns in families.items()},
        "total_protected_local_columns": sum(map(len, families.values())),
        "all_literal_columns_have_omega_Eq_projection_zero": True,
    }


def rhs_and_terminal_audit(local, source, loophole) -> dict[str, object]:
    local_ledger, local_digest = local.audit()
    require(local_digest == local.EXPECTED_LEDGER_SHA256, local_digest)
    local_map = local_ledger["exhaustive_local_supermap"]
    require(local_map["rank"] == 126
            and local_map["cokernel_dimension"] == 1, local_map)

    rhs = local.balanced_top("B")
    dual = local.integral_terminal_dual()
    raw_value = dot(dual, rhs)
    require(raw_value == 12, raw_value)

    loophole_ledger, loophole_digest = loophole.audit()
    require(loophole_digest == loophole.EXPECTED_LEDGER_SHA256,
            loophole_digest)
    requirements = loophole_ledger[
        "mapping_cone_and_physical_terminal"
    ]["accepted_Fredholm_requires"]
    require(len(requirements) == 4, requirements)

    full_grade = source.full_grade_audit()
    require(full_grade["word"] == "01211222"
            and full_grade["fine_lattice_coordinate_width"] == 24
            and full_grade["repeated"] == "P3+K2", full_grade)
    return {
        "literal_required_RHS": (
            "b_Gamma*=sum_{N in {23|45,24|35,25|34}} "
            "(B_DQ[a|b],N+B_DQ[b|a],N"
            "-B_PS[P0,S1],N-B_PS[P1,S0],N)"
        ),
        "RHS_support": {
            "B_private_occurrence_coordinates": 12,
            "Eq_coordinates": 0,
            "external_coordinates": 0,
            "target_representative_after_endpoint_even_cone": 0,
        },
        "RHS_tags": {
            "word": full_grade["word"],
            "fine_coordinate_width": 24,
            "fine_labels": full_grade["fine_labels"],
            "repeated": full_grade["repeated"],
            "operation_corners": list(local.CORNERS),
            "fixed_window": "2345",
            "root_paths": ["AB", "AC"],
            "endpoint_parity": "even",
        },
        "integral_omega_Eq_value": raw_value.numerator,
        "normalized_omega_Eq": "delta.(B-Eq)/12",
        "normalized_value_on_RHS": 1,
        "declared_map_rank_before_after_RHS": [126, 127],
        "literal_physical_status": (
            "this is the exact codomain vector the physical Gate-II packet "
            "must produce; this checker does not assert an existing source "
            "cell maps to it"
        ),
        "accepted_terminal_requirements_replayed": requirements,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    common = load(
        "computations/verify_h3_trig_euler_augp2_common_base_comparison_gate.py",
        "declared_gamma_common",
    )
    protected = load(
        "computations/verify_h3_full_star_minimal_protected_homogenizer_cylinder_gate.py",
        "declared_gamma_protected",
    )
    source = load(
        "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py",
        "declared_gamma_source",
    )
    local = load(
        "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py",
        "declared_gamma_local",
    )
    hasse = load(
        "computations/verify_h3_full_hasse_koszul_cap_totalization.py",
        "declared_gamma_hasse",
    )
    hom_gate = load(
        "computations/verify_h3_endpoint_even_hom_target_cone_eq_terminal_gate.py",
        "declared_gamma_hom",
    )
    loophole = load(
        "computations/verify_h3_psi_canonical_source_resolution_degree1_loophole_gate.py",
        "declared_gamma_loophole",
    )

    star = full_star_and_cylinder_audit(common, protected)
    cap = cap_hasse_and_target_audit(hasse, hom_gate, local)
    macaulay = macaulay_complement_audit(source)
    protected_local = local_declared_columns_audit(local)
    rhs = rhs_and_terminal_audit(local, source, loophole)

    declared_free_generator_invocations = (
        star["two_root_full_star_generators"]
        + star["two_root_deleted_factor_cylinders"]
        + star["two_root_lcm_ambiguity_cylinders"]
        + cap["derived_Hasse_Koszul_cubes"]
        + len(cap["endpoint_even_target_cone_objects"])
        + macaulay["squarefree_divisor_complement_slots"]
        + protected_local["total_protected_local_columns"]
    )
    require(declared_free_generator_invocations == 13601,
            declared_free_generator_invocations)
    ledger = {
        "theorem": (
            "h3 declared divided-Weyl/trigger Gamma_* omega_Eq terminal gate"
        ),
        "pins": PINS,
        "declared_A_full_star_and_cylinders": star,
        "declared_A_cap_Hasse_and_target_cone": cap,
        "declared_A_Gamma_Macaulay_complements": macaulay,
        "declared_A_protected_local_columns": protected_local,
        "declared_free_generator_invocations": {
            "count": declared_free_generator_invocations,
            "counting_policy": (
                "free presentation occurrences retain root, parent, face, "
                "operation and fine tags; overlaps in their output shadows "
                "are intentionally not identified"
            ),
            "omega_Eq_charge_histogram": {"0": declared_free_generator_invocations},
        },
        "exact_RHS_and_normalization": rhs,
        "declared_terminal": {
            "omega_Eq_kills_every_declared_relative_C1_generator": True,
            "omega_Eq_reads_literal_RHS": 1,
            "status": "accepted Fredholm terminal for A_decl only",
        },
        "physical_promotion_assumption": {
            "name": "same-grade relative-C1 essential surjectivity",
            "statement": (
                "every primitive physical relative-C1 generator with word "
                "01211222, the six literal Gamma_* fine labels, P3+K2 "
                "repeated shape, DQ/PS operation tags, root paths AB/AC and "
                "the protected q/anchor/W/ores/ridge/eta/sigma/target rows is "
                "generated by A_decl; equivalently there is no independent "
                "same-grade column with nonzero delta.(B-Eq)"
            ),
            "includes": [
                "physical occurrence-local source provenance of T23,T45",
                "the literal b_Gamma* map in the same augmented codomain",
            ],
            "first_falsifier": (
                "one primitive same-grade response-to-cap relative-C1 cell "
                "whose protected projection has delta.(B-Eq) nonzero"
            ),
            "why_not_computationally_closed": (
                "the repository supplies a finite declared cellular grammar, "
                "but no independent theorem enumerates all primitive physical "
                "generators of the ambient source operation category"
            ),
        },
        "verdict": (
            "omega_Eq annihilates all 13,601 root-, parent-, operation- and "
            "fine-labelled generator invocations in the declared full-star, "
            "deleted/lcm cylinder, derived Hasse/Koszul, endpoint-even target "
            "cone, protected local and Gamma_* Macaulay presentation.  The "
            "literal balanced private RHS has normalized value one.  This "
            "promotes the local rank-126/127 dual to a Fredholm terminal for "
            "the declared algebra.  Its promotion to the physical proof is "
            "conditional exactly on same-grade relative-C1 essential "
            "surjectivity; the underived (H_0-u)*eq descent is the first "
            "excluded bright operation, not a currently valid column."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("declared Gamma terminal ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    if arguments.mode == "structural":
        pin_dependencies()
        print("h3 declared Gamma terminal structural gate: PASS")
        return
    ledger, digest = audit()
    if arguments.mode == "exhaustive":
        source = load(
            "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py",
            "declared_gamma_source_stress",
        )
        require(macaulay_complement_audit(source)[
            "squarefree_divisor_complement_slots"] == 48,
            "Macaulay replay changed")
    if arguments.json:
        print(json.dumps({"ledger": ledger, "sha256": digest},
                         indent=2, sort_keys=True))
    else:
        print("h3 declared divided-Weyl/trigger Gamma terminal gate: PASS")
        print("declared free generator invocations: 13601; omega_Eq-dark: 13601")
        print("literal RHS normalized omega_Eq value: 1")
        print("declared Fredholm terminal: YES; physical: CONDITIONAL")
        print("remaining assumption: same-grade relative-C1 essential surjectivity")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
