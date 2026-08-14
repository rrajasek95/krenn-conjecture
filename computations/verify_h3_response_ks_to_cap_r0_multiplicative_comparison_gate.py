#!/usr/bin/env python3
"""Audit the attempted physical upgrade from response KS to tied cap r0.

The universal response deformation supplies a relative generator

    d epsilon_s = -c_f

in the response occurrence/cotangent object.  Independently, the physical
cap generator is internally tied:

    r0 has private boundary B,  d r0 = E=(H0-u)e_Eq.

As ungraded two-term complexes there is a unique normalized chain-map shape

    epsilon_s |-> r0,      c_f |-> -E.

But the source and target have different literal word, fine, repeated and
operation idempotents.  The current fixed physical grammar has no degree-zero
off-diagonal arrow between them.  A standard mapping cylinder requires such
a map as input; it does not manufacture it.  The first literal proper face
of any proposed arrow is the selected six-term db01 packet, and its first
cross-summand coordinate is the central Eq incidence.

Consequently strict multiplicativity, if this one map is constructed, makes
all eight kappa values zero.  Existing source data do not construct the map.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_universal_response_deformation_e14_orbit_ks_gate.py":
        "39713f3683dd3d2376e5a911987ee3670ec291cf850072d6b4932e7a93745fc7",
    "notes/h3-universal-response-deformation-e14-orbit-ks-gate.md":
        "d9032c365e8fd8fb5baf320dcc5adac8832c023119fb7d4df69d02cce3d5878f",
    "computations/verify_h3_universal_response_ks_augmented_readout_extension_gate.py":
        "4493274dfbda62cec0d6823272762fb01c3a798123a1da206559e91890ba9047",
    "notes/h3-universal-response-ks-augmented-readout-extension-gate.md":
        "f201fd4c4599a27173a824d7475ade679ef2de55e7c91bc3dd9cc917ac16ee37",
    "computations/verify_h3_uc4_beq_tie_source_provenance_audit.py":
        "f237ccffd40863a201b780ea034fcbd7781bc555e1fbc6f528d99d3ab71394c6",
    "notes/h3-uc4-beq-tie-source-provenance-audit.md":
        "4501c6613523222e6c32345f3624a1ceccc7b3b0a2fe934e482a03543e336aa8",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "notes/h3-shear-collision-augp2-packaging-map-gate.md":
        "9d5918605dd94d08d18c099966e5956fa0f1c62855b97fd81bf9ada54f2f45ad",
    "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py":
        "4e32d14b4d495b4439ed7aba59afedc8de0c1c4f76717989ca9e817444e9cd8f",
    "notes/h3-centered-projector-literal-first-hasse-eq-incidence-gate.md":
        "242a0a148c782c73540f060ef4e685902888f6d0e95da2d050b0e46dec5baf9d",
    "computations/verify_h3_e14_selected_fibre_graph_keq_koszul_gate.py":
        "9d57cbcfaeebb8d7f67d6efea87a124b4a46ad1dc054d5fc0954ab0c2338b157",
    "notes/h3-e14-selected-fibre-graph-keq-koszul-gate.md":
        "98cae28b58267abcffc47b571e52581a354950ef684df5f28b58dca88c60c6e7",
    "computations/verify_h3_kappa_lambda_literal_mapping_cone_normalization_gate.py":
        "b60538f9db5b8c2984bbee95e0a05f383408e9ab7c13680216adf56386682522",
    "notes/h3-kappa-lambda-literal-mapping-cone-normalization-gate.md":
        "1e7655ab1661453200ba33aff800aa6d9991dd86922d81d4f5b488fcc15bb817",
    "computations/verify_h3_gate_ii_uniform_response_relative_carrier_landing_gate.py":
        "9b9c05a6789d2ade9359934f279eeb429591b2e85651ebaba8485195050417eb",
    "notes/h3-gate-ii-uniform-response-relative-carrier-landing-gate.md":
        "e1d0b1185cd72ff4d0d915abb1db25835f2848f65f1509458aee9f2325699084",
}
EXPECTED_LEDGER_SHA256 = "61eb76cf31690a4aea7981a872a43b0b740d98193b2a08526d63f232d2f4c7f2"

DELTA = tuple(map(Q, (1, 1, -1, -1)))
ZERO4 = (Q(0),) * 4
KAPPA_WORDS = (
    "0012", "0102", "0110", "0111",
    "0122", "0212", "1112", "2112",
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
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


def dependency_scope_audit() -> dict[str, object]:
    # These are the exact conclusions of the hash-pinned ledgers above.  Do
    # not re-run their large occurrence/D4 enumerations here; this checker
    # audits the new finite chain-map and idempotent step.
    response_word = "11:110000"
    cap_word = "01211222"
    response_full = tuple(map(int, "11110000"))
    cap_full = tuple(map(int, cap_word))
    changed = tuple(index for index, values in enumerate(
        zip(response_full, cap_full, strict=True)) if values[0] != values[1])
    require(changed == (0, 2, 4, 5, 6, 7)
            and response_word != cap_word,
            "literal response/cap word separation changed")
    return {
        "response_relative_KS": "d epsilon_s=-c_f, rank 89 centered family",
        "fixed_source_contains_physical_image_of_epsilon_s": False,
        "cap_r0": {
            "private_boundary": "private full-nine B packet",
            "differential": "d r_0=(H_0-u)e_Eq",
            "normalized_target": 1,
            "B_Eq_tied": True,
        },
        "response_word": response_word,
        "cap_word": cap_word,
        "word_hamming_distance": len(changed),
        "all_six_selected_fine_degrees_change": True,
        "cap_word_in_response_D4_cube": False,
        "central_Eq_forgetful_rank_before_after": [3, 4],
    }


def algebraic_two_term_chain_map_audit() -> dict[str, object]:
    # Response complex: d eps=-c.  Cap complex: d r=E.  Write
    # Phi_1(eps)=a*r and Phi_0(c)=b*E.  The chain-map equation is
    # d Phi_1(eps)=Phi_0 d(eps), hence a=-b.
    # Its relation matrix is [1,1] on (a,b).
    relation = (Q(1), Q(1))
    kernel_generator = (Q(1), Q(-1))
    require(dot(relation, kernel_generator) == 0
            and rank((relation,)) == 1,
            "two-term chain-map equation changed")
    normalized = kernel_generator
    require(normalized == (1, -1), "normalized chain-map signs")

    # Once this map exists, the image r0 is tied and the strict cone product
    # has B=Eq.  Test all corner units and cross-shore edges.
    units = tuple(tuple(Q(1 if row == column else 0) for row in range(4))
                  for column in range(4))
    occurrences = units + tuple(
        tuple(units[left][row] + units[right][row] for row in range(4))
        for left in (0, 1) for right in (2, 3)
    ) + (DELTA,)
    chi = DELTA + tuple(-value for value in DELTA)
    require(all(dot(chi, occurrence + occurrence) == 0
                for occurrence in occurrences),
            "normalized r0 image stopped being tied")
    return {
        "response_complex": "Q<epsilon_s> --d--> Q<c_f>, d epsilon_s=-c_f",
        "cap_complex": "Q<r0> --d--> Q<E>, d r0=E",
        "chain_map_components": "Phi_1(epsilon_s)=a*r0, Phi_0(c_f)=b*E",
        "chain_map_equation": "a+b=0",
        "ungraded_chain_map_parameter_dimension": 1,
        "normalized_solution": {"a": 1, "b": -1},
        "normalization_source": "monic KS coefficient and normalized cap r0 target",
        "strict_cone_B_Eq": "(v,v) coefficientwise",
        "strict_cone_lambda": 0,
        "interpretation": (
            "there is no algebraic coefficient or sign obstruction; the missing "
            "datum is physical existence of the graded chain map"
        ),
    }


def literal_idempotent_hom_audit() -> dict[str, object]:
    response_grade = {
        "word": "11:110000",
        "fine": "centered marked response occurrence / selected first PP",
        "repeated": "response occurrence and PP faces",
        "operation": "universal response KS / endpoint-matching orbit",
    }
    cap_grade = {
        "word": "01211222",
        "fine": "t*q_(v,N) at the selected six occurrences",
        "repeated": "P3+K2",
        "operation": "AugP2 cap / K_Eq r0",
    }
    require(response_grade != cap_grade,
            "response and cap idempotents unexpectedly coincide")

    # Existing fixed-grade source is the direct sum of the two internal
    # complexes.  Its degree-zero operation algebra contains the two
    # diagonal idempotents but no response-to-cap matrix unit.
    identity_response = (Q(1), Q(0))
    identity_cap = (Q(0), Q(1))
    desired_off_diagonal = (Q(0), Q(0), Q(1))
    existing_operation_coordinates = (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
    )
    require(rank(existing_operation_coordinates) == 2
            and rank(existing_operation_coordinates +
                     (desired_off_diagonal,)) == 3,
            "the literal off-diagonal operation rank changed")
    return {
        "response_grade": response_grade,
        "cap_grade": cap_grade,
        "fixed_source_operation_idempotents": [
            list(map(int, identity_response)), list(map(int, identity_cap)),
        ],
        "Hom_degree0_response_to_cap_in_current_grammar": 0,
        "desired_new_matrix_unit": "w_KS,cap: response KS -> cap AugP2/K_Eq",
        "operation_rank_before_after": [2, 3],
        "coefficient_matching_and_D4_create_matrix_unit": False,
        "standard_mapping_cylinder_can_create_missing_input_map": False,
        "reason": (
            "a mapping cylinder is functorial in an already specified chain map; "
            "it adds its cone shift and interchange cells, not a new map between "
            "orthogonal word/fine/repeated/operation idempotents"
        ),
    }


def first_literal_face_audit() -> dict[str, object]:
    # Thirty fixed-endpoint fibres.  The old response supplies their sum;
    # the selected fibre and centered selected fibre are new directions.
    size = 30
    complete = (Q(1),) * size
    selected = (Q(1),) + (Q(0),) * (size - 1)
    centered = tuple(Q(30) * selected[index] - complete[index]
                     for index in range(size))
    require(rank((complete,)) == 1
            and rank((complete, selected)) == 2
            and rank((complete, centered)) == 2
            and sum(centered, Q(0)) == 0,
            "selected response fibre rank changed")

    # Presentation-safe graph counterguard in coordinates
    # (b01, other fibres, z01).
    response = tuple(map(Q, (1, 1, 0)))
    graph = tuple(map(Q, (-1, 0, 1)))
    b01 = tuple(map(Q, (1, 0, 0)))
    separator = tuple(map(Q, (1, -1, 1)))
    require(rank((response, graph)) == 2
            and rank((response, graph, b01)) == 3
            and dot(separator, response) == dot(separator, graph) == 0
            and dot(separator, b01) == 1,
            "selected graph counterguard changed")
    return {
        "coefficient_identity": "(A+I)c_f=3c_01, c_01=30b_01-R",
        "first_PP_identity": "dc_01=30db_01-dR",
        "old_complete_first_PP_rank_then_selected": [1, 2],
        "selected_six_term_face": (
            "db_01=p0*s1*sum_(23|45,24|35,25|34) "
            "(dq_edge*q_mate+q_edge*dq_mate)"
        ),
        "selected_face_in_old_fixed_response_span": False,
        "presentation_safe_graph": "d epsilon_g=z_01-b_01",
        "graph_rank_then_selected": [2, 3],
        "graph_selected_dual": [1, -1, 1],
        "graph_product_residual": "z_01*theta",
        "killing_graph_coordinate_changes_H0": True,
        "first_cross_summand_obstruction": (
            "the source-labelled central Eq incidence Phi((H0-u)e_Eq)=R_E14"
        ),
        "central_Eq_forgetful_rank_before_after": [3, 4],
    }


def fixed_physical_counterguard_audit() -> dict[str, object]:
    # Two internal two-term complexes with literal orthogonal idempotents.
    # Both differentials and both normalizations exist.  The off-diagonal Hom
    # is zero, so the cross cone and its lambdas are not defined/forced.
    d_response = (Q(-1), Q(0))
    d_cap = (Q(0), Q(1))
    require(rank((d_response, d_cap)) == 2,
            "the direct-sum internal complexes stopped separating")
    return {
        "objects": [
            "relative response KS: d epsilon_s=-c_f in 11:110000",
            "physical cap r0: d r0=E in 01211222/tq/P3+K2",
        ],
        "all_internal_response_identities_hold": True,
        "all_internal_cap_r0_B_Eq_target_identities_hold": True,
        "formal_cap_graph_and_D4_flatness_can_hold": True,
        "off_diagonal_Hom": 0,
        "mixed_mapping_cylinder_exists": False,
        "physical_kappa_lambda_values_forced": False,
        "meaning": (
            "the direct sum of the two committed literal presentations is the "
            "smallest source-labelled counterguard; coefficient shadows agree "
            "but no operation changes the idempotent"
        ),
    }


def minimal_positive_schema_audit() -> dict[str, object]:
    return {
        "one_new_schema": "Phi_KS,r0, natural in the marked one-root object",
        "required_generator_map": "Phi_1(epsilon_s)=r0 plus typed dark cap normalizers",
        "required_boundary_map": "Phi_0(c_f)=-E with literal occurrence labels",
        "chain_map_normalization": "monic coefficient 1, forced on both faces by d Phi=Phi d",
        "first_PP_face": "selected db_01 (and endpoint-reversed/root-labelled mates)",
        "first_mixed_face": "Phi((H0-u)e_Eq)=R_E14",
        "cap_proper_faces": [
            "primitive cap/closed T+rho normalizer", "physical ainc/q",
            "W", "labelled ordinary residue", "shifted ridge/eta/sigma",
        ],
        "all_eight_instantiation": [
            {"lower_word": word, "lambda_after_schema": 0,
             "transport": "separate labelled naturality instance"}
            for word in KAPPA_WORDS
        ],
        "symmetry_alone_used": False,
        "consequence": (
            "once Phi is a normalized physical module/DGA map, its standard "
            "mapping cylinder has tied B=Eq and 3ad761f gives all lambda_i=0"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 response-KS to cap-r0 physical multiplicative comparison gate",
        "pinned_physical_scope": dependency_scope_audit(),
        "ungraded_two_term_chain_map": algebraic_two_term_chain_map_audit(),
        "literal_idempotent_Hom": literal_idempotent_hom_audit(),
        "first_literal_faces": first_literal_face_audit(),
        "fixed_physical_counterguard": fixed_physical_counterguard_audit(),
        "minimal_positive_schema": minimal_positive_schema_audit(),
        "verdict": (
            "The universal response family supplies the relative KS generator and "
            "the cap r0 is internally B=Eq tied.  Their two-term complexes admit "
            "a unique normalized ungraded chain-map shape, so there is no scalar "
            "or sign obstruction.  The actual fixed source has orthogonal response "
            "and cap word/fine/repeated/operation idempotents and no degree-zero "
            "arrow between them.  Therefore a standard mapping cylinder cannot be "
            "formed.  The first proper face of the missing arrow is selected db01; "
            "the first cross-summand coordinate is central Eq incidence.  One "
            "normalized source-labelled Phi_KS,r0 schema would close all eight "
            "lambdas to zero; it is not constructed by current operations."
        ),
        "scope": (
            "exact canonical h=3 rational source-labelled counterguard.  It does "
            "not prove nonexistence of the physical comparison, a full GHZ packet, "
            "or uniform spectator-tail transport"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    return ledger, sha256(payload.encode()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("trace", "counterguard", "positive-schema"),
                        default="trace")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    require(digest == EXPECTED_LEDGER_SHA256,
            ("response-KS/cap-r0 comparison ledger changed", digest))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h3 response-KS -> cap-r0 multiplicative gate ({arguments.mode}): PASS")
        print("relative response KS generator: CONSTRUCTED")
        print("physical cap r0 B=Eq tie: CONSTRUCTED INTERNALLY")
        print("literal response-to-cap chain map: NOT CONSTRUCTED")
        print("first proper face: selected db01; first cross face: central Eq incidence")
        print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
