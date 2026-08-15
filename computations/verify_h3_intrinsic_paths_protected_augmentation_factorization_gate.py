#!/usr/bin/env python3
"""Test protected augmentation factorization of the intrinsic h=3 paths.

The literal EqSystem operators construct one common coefficient occurrence:
the q23/q45 divided-root/restriction paths followed by lower iota give
delta_plus.  They do not produce two source labels called B and Eq.  This
checker asks whether the protected lift can nevertheless be derived from the
existing physical source maps.

It cannot yet.  At the first central cap comparison, the four objectwise
P_f/K_Eq/D4 edges have primitive H1=Z.  Their coefficient shadows add
correctly, but the mixed operation-incidence coordinate is absent.  Thus the
protected B and Eq values are undefined, rather than unequal, on the literal
selected carrier.

The smallest exact datum is one monic mixed mapping-cylinder/Tate two-cell
kappa_orb,Eq.  Its source-section component has normalized proper-face
signature (R,-E,0,+E) in (top,lower,Eq,ores).  Composing with the already
physical internal cap face (0,+E,+E,-E) gives (R,0,+E,0), hence the desired
same-normalization tied B=Eq landing.  Adding only a formal Eq copy or only
the coefficient equality does not fill the primitive square.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_eqsystem_divided_root_restriction_chain_commutator_intrinsic_gate.py":
        "6db24fc6c3f5bb42c7e30185e4887d4a06758154730de0e7c734f131725504be",
    "computations/verify_h3_divided_root_p2_iota_cap_beq_commutator_gate.py":
        "d04ad992bde820edcc79b2660e64a141db8ff52a39a6a78be6c470105467106a",
    "computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py":
        "2e4b1a1b9bb5b5be8d0997132b49b95576a28dc6ccb9cfd83db808ace8f52f3e",
    "computations/verify_h3_e14_d4_p2_keq_deven_simultaneous_totalization_gate.py":
        "dfa46c3519089bb7b2a04d24ea6e4f9d138887d98fb53af60369184d2d2c91fd",
    "computations/verify_h3_normalized_solutionwise_marked_cap_constructive_factor_gate.py":
        "0b8d244925bd82560881d649f7cf173a4abb1e0c80ec0519c1f02d2c1175fef3",
    "computations/verify_h3_marked_parent_endpoint_coordinate_cap_activity_gate.py":
        "5996feac9d555cee0783e9601311b614396b0f0211bc60ecb380c249565fa6f9",
}
EXPECTED_LEDGER_SHA256 = (
    "b09443bf779cc04f5f72972a5b66d07968913a38707cc6e9b205c4b9b9782f68"
)

DELTA_PLUS = tuple(map(Q, (-Q(1, 4), Q(1, 2), -Q(1, 4),
                          -Q(1, 4), Q(1, 2), -Q(1, 4))))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors):
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return 0
    height = len(columns[0])
    rows = [[columns[column][row] for column in range(len(columns))]
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
            rows[row] = [left - value * right
                         for left, right in zip(rows[row], rows[answer],
                                                strict=True)]
        answer += 1
    return answer


def intrinsic_common_shadow_audit(intrinsic):
    ledger, digest = intrinsic.audit()
    require(digest == intrinsic.EXPECTED_LEDGER_SHA256, digest)
    official = ledger["official_EqSystem"]
    marked = ledger["marked_collision_descendants"]
    descent = ledger["protected_no_descent"]
    common = tuple(map(Q, descent["intrinsic_common_cut_value"]))
    difference = tuple(map(Q, descent["intrinsic_path_difference"]))
    require(official["cut_occurrence_squares_checked"] == 1377810
            and official["commutator_on_every_official_relation"] == 0
            and official["scalar_target_composite"] == 0
            and marked["selected_descendant_commutator"] == 0
            and marked["q23_q45_word_fine_image_rank"] == 2
            and common == DELTA_PLUS
            and difference == (Q(0),) * 6,
            (official, marked, descent))
    return {
        "literal_operator_paths": [
            "I_c D_c Phi d", "d I_c Phi_hat D_r",
        ],
        "official_occurrence_squares":
            official["cut_occurrence_squares_checked"],
        "pure_target_value": official["scalar_target_composite"],
        "marked_q23_q45_commutator":
            marked["selected_descendant_commutator"],
        "common_lower_iota_coefficient":
            [str(value) for value in common],
        "common_name": "delta_plus=(c_1^+ + c_4^+)/8",
        "intrinsic_path_difference": [str(value) for value in difference],
        "literal_output_type": (
            "one occurrence-labelled coefficient module U_common; no B or "
            "Eq operation-copy idempotent"
        ),
    }


def protected_copy_lift_audit() -> dict[str, object]:
    zero = (Q(0),) * 6
    tied = DELTA_PLUS + DELTA_PLUS
    b_only = DELTA_PLUS + zero
    eq_only = zero + DELTA_PLUS
    detector = tuple(map(Q, (-1, 2, -1, -1, 2, -1)))
    omega = detector + tuple(-value for value in detector)
    require(dot(omega, tied) == 0
            and dot(omega, b_only) == 3
            and dot(omega, eq_only) == -3
            and rank((tied, b_only)) == 2,
            (dot(omega, tied), dot(omega, b_only), dot(omega, eq_only)))
    return {
        "common_source_shadow": "delta_plus in U_common",
        "candidate_tied_lift": "(delta_plus,delta_plus)",
        "candidate_B_only_lift": "(delta_plus,0)",
        "candidate_Eq_only_lift": "(0,delta_plus)",
        "anti_diagonal_detector_values_tied_Bonly_Eqonly": [0, 3, -3],
        "source_operator_equations_choose_a_lift": False,
        "protected_B_augmentation_from_literal_source_alone": "UNDEFINED",
        "protected_Eq_augmentation_from_literal_source_alone": "UNDEFINED",
        "what_is_derived": (
            "the common coefficient delta_plus and its B1/B4 occurrence "
            "labels, before protected-copy separation"
        ),
        "not_a_literal_counterexample": (
            "the tied and B-only vectors are two possible lifts in the "
            "enriched codomain; neither is automatically a physical map from "
            "the selected source carrier"
        ),
    }


def first_physical_factorization_obstruction(mapping):
    ledger, digest = mapping.audit()
    require(digest == mapping.EXPECTED_LEDGER_SHA256, digest)
    square = ledger["mapping_cylinder"]
    faces = ledger["coupled_physical_faces"]
    generator = ledger["minimal_generator_and_scope"]
    typed = square["physical_source_typed_quotient"]
    require(square["primitive_boundary_cycle"] == [1, -1, 1, -1]
            and square["H1_without_mixed_face"] == "Z"
            and square["H1_after_one_mixed_face"] == 0
            and typed["available_rank"] == 2
            and typed["rank_with_required_comparison"] == 3
            and typed["primitive_dual"] == [0, 0, 1]
            and faces["D4_top_is_literal_P2_hidden"] is False
            and faces["conditional_D3_transfer"]
                == "D_root tensor (-(B1+B4))=-E",
            (square, faces))
    required = generator["minimal_new_central_generator"]
    require(required["name"] == "kappa_orb,Eq"
            and required["type"]
                == "one mixed mapping-cylinder/Tate 2-cell",
            required)
    return {
        "edge_square": square["edge_order"],
        "edge_boundary_rank": square["d1_rank"],
        "primitive_H1_cycle": square["primitive_boundary_cycle"],
        "H1_before_after_one_mixed_cell": ["Z", 0],
        "typed_rows": typed["rows"],
        "typed_rank_before_after_required": [
            typed["available_rank"],
            typed["rank_with_required_comparison"],
        ],
        "primitive_mixed_incidence_dual": typed["primitive_dual"],
        "first_failure": (
            "the protected lift is not typed: objectwise P_f, K_Eq and D4 "
            "edges do not supply their mixed two-cell"
        ),
        "first_literal_proper_face_if_incidence_is_granted":
            faces["missing_D3_label_map_for_hidden_face"],
        "conditional_hidden_transfer": faces["conditional_D3_transfer"],
        "no_unequal_physical_B_Eq_face_yet": True,
        "reason": (
            "the comparison fails at operation incidence before separate B "
            "and Eq readouts are defined on the selected source carrier"
        ),
    }


def minimal_normalized_cell_audit(mapping):
    # Normalize one nonzero component of
    # E=2*D_root tensor (B1+B4)/2.  The missing source-labelled section and
    # the already physical internal cap face have the exact four-row sum.
    # Rows are (principal/top, root-lower, root-Eq, word-resolved ores).
    source_section = tuple(map(Q, (1, -1, 0, 1)))
    internal_cap_o_minus_e = tuple(map(Q, (0, 1, 1, -1)))
    tied_output = tuple(map(Q, (1, 0, 1, 0)))
    require(add(source_section, internal_cap_o_minus_e) == tied_output,
            (source_section, internal_cap_o_minus_e, tied_output))

    # Coefficient equality without the mixed incidence is exactly the
    # forgetful shadow: orbit top plus central Eq.  Restoring incidence gives
    # a rank-raising primitive coordinate.
    orbit_top = tuple(map(Q, (1, 0, 0)))
    central_eq = tuple(map(Q, (0, 1, 0)))
    required_mixed = tuple(map(Q, (1, 1, 1)))
    mixed_dual = tuple(map(Q, (0, 0, 1)))
    require(rank((orbit_top, central_eq)) == 2
            and rank((orbit_top, central_eq, required_mixed)) == 3
            and dot(mixed_dual, orbit_top) == 0
            and dot(mixed_dual, central_eq) == 0
            and dot(mixed_dual, required_mixed) == 1,
            "mixed incidence rank changed")

    minimal = mapping.minimal_physical_generator_audit()[
        "minimal_new_central_generator"]
    require(minimal["proper_faces"][:3] == [
        "hidden root-lower -E",
        "physical invisible K_Eq cap face n",
        "literal face3/5 occurrence-to-B4/B1 label transport",
    ], minimal)
    return {
        "E_normalization": "E=2*D_root tensor (B1+B4)/2",
        "row_order": ["top R", "root lower", "root Eq", "root ores"],
        "missing_source_section": [1, -1, 0, 1],
        "missing_source_section_formula": "(R,-E,0,+E)",
        "existing_internal_cap_face": [0, 1, 1, -1],
        "existing_internal_cap_face_formula": "(0,+E,+E,-E)",
        "sum": [1, 0, 1, 0],
        "sum_formula": "(R,0,+E,0)",
        "same_normalization_B_equals_Eq_after_cell": True,
        "coefficient_shadow_alone_fills_mixed_incidence": False,
        "mixed_incidence_rank_before_after": [2, 3],
        "smallest_extra_datum": {
            "generator": "one monic kappa_orb,Eq/AugP2 mixed two-cell",
            "boundary": "primitive square cycle (1,-1,1,-1)",
            "source_section_proper_faces": [
                "root-lower -E", "word-resolved ores +E",
            ],
            "additional_typed_faces": minimal["proper_faces"][1:],
            "normalization": (
                "top coefficient one and augmented alternating right side "
                "even, fixing the factor two in E"
            ),
        },
        "why_one_cell_is_minimal": (
            "the primitive square obstruction is rank one and free over Z; "
            "one monic two-cell kills it, while a formal Eq coordinate, a "
            "coefficient equality, or either hidden face alone leaves it"
        ),
    }


def audit():
    pin_dependencies()
    intrinsic = load(
        "computations/verify_h3_eqsystem_divided_root_restriction_chain_commutator_intrinsic_gate.py",
        "protected_factor_intrinsic",
    )
    mapping = load(
        "computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py",
        "protected_factor_mapping",
    )
    ledger = {
        "theorem": (
            "the literal selected h=3 source carrier has one canonical "
            "coefficient augmentation delta_plus but no derived protected "
            "B/Eq split; its first physical factorization obstruction is the "
            "primitive orbit/K_Eq mapping square"
        ),
        "pins": PINS,
        "intrinsic_common_shadow": intrinsic_common_shadow_audit(intrinsic),
        "protected_copy_lift": protected_copy_lift_audit(),
        "first_physical_obstruction":
            first_physical_factorization_obstruction(mapping),
        "minimal_normalized_cell": minimal_normalized_cell_audit(mapping),
        "verdict": (
            "no unequal physical B/Eq source face is found because neither "
            "protected copy is separately defined by the literal operator "
            "paths.  They construct only delta_plus in a common occurrence "
            "module.  The first missing datum is exactly one monic physical "
            "mixed kappa_orb,Eq/AugP2 two-cell with hidden (-E,+E) source "
            "faces.  Its addition makes the existing internal cap identity "
            "produce a same-normalization tied B=Eq landing"
        ),
        "scope": (
            "canonical h=3 selected carrier, official EqSystem operator "
            "paths, q23/q45 marked P2/lower-iota coefficient shadow, the "
            "integral P_f/K_Eq/D4 square, and the first root-lower/Eq/ores "
            "packet.  This is an exact missing-cell criterion, not a "
            "construction of that physical cell or a full Fredholm terminal"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "ledger_sha256": digest}, indent=2, sort_keys=True))
    else:
        print("h3 intrinsic-path protected augmentation factorization: SHARP FORK")
        print("mode", arguments.mode)
        print("common coefficient delta_plus: DERIVED")
        print("separate protected B/Eq on source carrier: UNDEFINED")
        print("first obstruction: primitive mixed-square H1=Z")
        print("minimal datum: one monic kappa_orb,Eq cell with (-E,+E) faces")
        print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
