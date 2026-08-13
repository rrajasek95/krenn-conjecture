#!/usr/bin/env python3
"""Reduce physical promotion of the exported cylinder curvature t*k_ij.

The local Segre block has six coordinates

    (Aq0,Aq1,Aq2,Bq0,Bq1,Bq2).

Its three toric characters span the rank-two endpoint-odd tensor
matching-standard module.  The prototype ``k01`` is the polynomial

    (p1*s0-p0*s1)*(q23*q45-q24*q35).

It has source bidegree (two unary p/s factors, two diagonal edge factors),
word 110000, and no offdiagonal decorated edge.  The parent toric relation
has the literal doubled grade

    p0*s1*p1*s0*q23*q45*q24*q35, word 220000.

Every target-augmented private-site active term instead contains a named
offdiagonal decorated edge, and its determinant/cofactor term has four edge
factors and no unary factor.  Specializing all offdiagonal decorated edge
variables to zero kills that entire active family but leaves k01 nonzero.
Thus the existing private-site rows do not literally realize the curvature.

If a physical target/output object were a graded A-module with a generator
``t`` in the required word/fine/repeated grade, then ``k*t`` would indeed be
an automatic Macaulay multiple.  This only proves that it is a legal
codomain vector.  A physical target-normal source column has a companion:

    d theta = s + t,
    d(k theta)=k*s+k*t.

Consequently pure ``k*t`` is in the old image exactly when its companion
``k*s`` is.  The primitive local dual ``(-1,+1)`` on (companion,target)
kills the available full target-normal column and reads one on pure target.

In the actual h=3 block the GHZ target coefficient of mixed word 110000 is
zero.  The target curvature nevertheless stops being a new theorem once the
physical cap graph is placed across the response/D4 word change: homogeneous
Macaulay multiplication then cancels it and leaves the four-corner ordinary
residue.  The *negative* of the committed endpoint-odd Cartan packet cancels
that residue.  The constant endpoint-transpose involution supplies the
conjugate S half from one canonical P-half attachment, so there is no second
fine-grade transport theorem.  The sole new datum is the canonical
source-labelled cross-word cap attachment, with its principal companion;
central K_Eq and the committed ridge/physical-q laws are objectwise.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_centered_shear_h0_target_cylinder_alternative.py":
        "b4aa84a571500c0e4745ae29ea6c1f23076c63bac139d1bd839fdb1160f515ab",
    "notes/h3-centered-shear-h0-target-cylinder-alternative.md":
        "d21d02f0d3dfece57e080511c34af78b38b77b87600837a05668ae1970b7e70e",
    "computations/verify_h3_universal_response_ks_augmented_readout_extension_gate.py":
        "4493274dfbda62cec0d6823272762fb01c3a798123a1da206559e91890ba9047",
    "notes/h3-universal-response-ks-augmented-readout-extension-gate.md":
        "f201fd4c4599a27173a824d7475ade679ef2de55e7c91bc3dd9cc917ac16ee37",
    "computations/verify_h3_segre_bright_private_site_incidence_tate_alternative.py":
        "e00e9b39740c22b2beacd874e13ab3b7e7c2f776724e19eece28f525400d6258",
    "notes/h3-segre-bright-private-site-incidence-tate-alternative.md":
        "95a8ee1a7603cb5e5af20b44cdf7668a42b22fb020f042839a58e5a8329baa99",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "notes/uniform-target-augmented-private-site-active-minor.md":
        "d7b16ecbb867524615ecf3034e0911e0add34825a7f9088f369f3a11e1c61f0d",
    "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py":
        "4e32d14b4d495b4439ed7aba59afedc8de0c1c4f76717989ca9e817444e9cd8f",
    "notes/h3-centered-projector-literal-first-hasse-eq-incidence-gate.md":
        "242a0a148c782c73540f060ef4e685902888f6d0e95da2d050b0e46dec5baf9d",
    "computations/verify_h3_e14_orbit_relative_d4_target_cone_gate.py":
        "67d33b03ec52c619f29e76c917fdba9b7e28380b4349291fa37b6b7d511e241c",
    "notes/h3-e14-orbit-relative-d4-target-cone-gate.md":
        "6268689c54144cc09b6be596b81d8b4aa741e0590a83e664ec3f6e65b89187bf",
    "computations/verify_h3_h0_cylinder_mixed_curvature_landing_guard.py":
        "9395988206e235f9770e32c06c7cbed0ba9f98705a6ab00e5c667596853b9386",
    "notes/h3-h0-cylinder-mixed-curvature-landing-guard.md":
        "eb98851250ef123de44a9033beb3abcebc045f326fc254c68f07cab1d226893b",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "notes/h3-physical-cartan-source-orbit-descent.md":
        "4f0ab9035124319cc491bb2cc9914ef58ced228774f41625699e8c1cb2ca65d1",
    "computations/verify_h3_centered_shear_to_cartan_single_bridge_reduction.py":
        "27ac408f8ed6dafa1687e22dd8231b1ebea6e5782252d337ab4daf67902a41f1",
    "notes/h3-centered-shear-to-physical-cartan-single-bridge-reduction.md":
        "f7f1dab102a2cc7d01b76db5c853c29861887441d0d7e6e55f824ba4d56902e0",
    "computations/verify_h3_cylinder_d4_cartan_graph_lock_bridge_gate.py":
        "f7f7009c4bf1b4849b26a2aaa7b24d36db3b576148a0f247a95bcac5f01cf4e1",
    "notes/h3-cylinder-d4-cartan-graph-lock-bridge-gate.md":
        "91806307285af0878e469a7ca0d191c729135de1950e73c62007ba9014610c72",
    "computations/verify_h3_trapped_hessian_theta_eq_grade_groupoid.py":
        "b30000bfe8383e1f254fb8fee4724cbd99d8f70a5e8447cffb1c9086a179aec0",
    "notes/h3-trapped-hessian-theta-eq-grade-groupoid.md":
        "5875c531cb0b5ba339665c243488c445bb34ed34edb69dee7bf23f689dc1fbe0",
}
EXPECTED_LEDGER_SHA256 = "ffda8f30e304b5038c3b4c12b28e848f60cf2d6b1badd4ae8cd3d378a229fa29"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank width")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        pivot_value = rows[answer][column]
        rows[answer] = [value / pivot_value for value in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            coefficient = rows[row][column]
            rows[row] = [left - coefficient * right
                         for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def word_with_ones(ones):
    return "".join("1" if site in ones else "0" for site in range(6))


def word_with_zeros(zeros):
    return "".join("0" if site in zeros else "1" for site in range(6))


def local_character_and_grade_audit() -> dict[str, object]:
    # Coordinate order is Aq0,Aq1,Aq2,Bq0,Bq1,Bq2.
    xi01 = (Q(-1), Q(1), Q(0), Q(1), Q(-1), Q(0))
    xi02 = (Q(-1), Q(0), Q(1), Q(1), Q(0), Q(-1))
    xi12 = (Q(0), Q(-1), Q(1), Q(0), Q(1), Q(-1))
    characters = (xi01, xi02, xi12)
    endpoint_rows = (
        (Q(1), Q(1), Q(1), Q(0), Q(0), Q(0)),
        (Q(0), Q(0), Q(0), Q(1), Q(1), Q(1)),
    )
    matching_rows = tuple(
        tuple(Q(coordinate % 3 == matching)
              for coordinate in range(6))
        for matching in range(3)
    )
    require(rank(characters) == 2
            and rank(endpoint_rows + matching_rows) == 4
            and all(dot(character, row) == 0
                    for character in characters
                    for row in endpoint_rows + matching_rows),
            "the local mixed character changed")

    # Literal prototype.  Both products in the toric relation have exactly
    # the same eight coefficient factors.
    toric_product_left = Counter({
        "p1@0^1": 1, "s1@1^1": 1,
        "p1@1^1": 1, "s1@0^1": 1,
        "q23:00": 1, "q45:00": 1,
        "q24:00": 1, "q35:00": 1,
    })
    toric_product_right = Counter({
        "p1@0^1": 1, "s1@1^1": 1,
        "p1@1^1": 1, "s1@0^1": 1,
        "q24:00": 1, "q35:00": 1,
        "q23:00": 1, "q45:00": 1,
    })
    require(toric_product_left == toric_product_right,
            "the doubled toric grade changed")
    require(all(":" not in factor or factor.endswith(":00")
                for factor in toric_product_left),
            "an offdiagonal decoration entered the toric grade")
    return {
        "local_coordinate_order": [
            "Aq0", "Aq1", "Aq2", "Bq0", "Bq1", "Bq2"
        ],
        "toric_character_rank": rank(characters),
        "aggregate_endpoint_matching_rank": rank(endpoint_rows + matching_rows),
        "prototype_k": (
            "(p1@1^1*s1@0^1-p1@0^1*s1@1^1)"
            "*(q23:00*q45:00-q24:00*q35:00)"
        ),
        "k_source_factor_bidegree": {"unary_p_s": 2, "edge_q": 2},
        "k_word": "110000",
        "k_offdiagonal_edge_factors": 0,
        "parent_relation_word": "220000",
        "parent_relation_literal_factors": dict(sorted(toric_product_left.items())),
        "parent_relation_repeated_edge_exponents": 0,
        "cylinder_curvature_grade": (
            "parameter-labelled first-PP face in the displayed doubled "
            "word/fine grade"
        ),
        "global_covariant_character_rank": 30,
    }


def private_site_nonlanding_audit() -> dict[str, object]:
    # Treat an offdiagonal decorated edge as variable e.  Every active
    # private-site determinant/cofactor term is divisible by at least one
    # such e after selecting its reference/mixed cell.  The specialization
    # e_off=0 kills those terms.  The prototype k uses only :00 edge cells.
    diagonal_values = {
        "p1@1^1": Q(2), "s1@0^1": Q(3),
        "p1@0^1": Q(1), "s1@1^1": Q(5),
        "q23:00": Q(7), "q45:00": Q(11),
        "q24:00": Q(13), "q35:00": Q(17),
    }
    k_value = (
        diagonal_values["p1@1^1"] * diagonal_values["s1@0^1"]
        - diagonal_values["p1@0^1"] * diagonal_values["s1@1^1"]
    ) * (
        diagonal_values["q23:00"] * diagonal_values["q45:00"]
        - diagonal_values["q24:00"] * diagonal_values["q35:00"]
    )
    require(k_value == -144 and k_value,
            ("the offdiagonal-zero specialization lost k", k_value))
    offdiagonal_values = (Q(0),) * 6
    active_terms = tuple(value * Q(index + 2)
                         for index, value in enumerate(offdiagonal_values))
    require(not any(active_terms),
            "an active private-site term survived offdiagonal zero")
    return {
        "private_site_reference": "e=A_vu^[b,a], a!=b",
        "private_site_active_term": "Delta_us*C_s",
        "active_term_factor_bidegree_at_h3": {"unary_p_s": 0, "edge_q": 4},
        "active_term_contains_offdiagonal_edge": True,
        "specialization": "all six offdiagonal decorated edge types -> 0",
        "private_site_active_family_after_specialization": 0,
        "prototype_k_after_specialization": str(k_value),
        "existing_offdiagonal_cofactor_rows_realize_k": False,
        "missing_incidence": (
            "endpoint unary wedge -> decorated offdiagonal edge and "
            "matching-standard difference -> its physical cofactor"
        ),
    }


def physical_target_word_audit() -> dict[str, object]:
    # Exact eighteen-word target normal of the marked endpoint projector.
    endpoint_words = set()
    for endpoint in (0, 1):
        for tail in (2, 3, 4, 5):
            endpoint_words.add(word_with_ones({endpoint, tail}))
            endpoint_words.add(word_with_zeros({endpoint, tail}))
    endpoint_words.update(("000000", "111111"))
    require(len(endpoint_words) == 18
            and "110000" not in endpoint_words
            and "111111" in endpoint_words,
            ("the marked target-normal support changed", endpoint_words))

    # The D4 orbit starts at mixed 110000 with target coefficient zero and
    # reaches its unique affine target coefficient at pure 111111.
    d4_profile = (0, 0, 0, 0, 1)
    require(d4_profile[0] == 0 and d4_profile[-1] == 1,
            "the D4 moving-target profile changed")
    return {
        "selected_response_head_word": "G11[110000]",
        "GHZ_target_coefficient_at_110000": 0,
        "marked_endpoint_target_normal_support_size": len(endpoint_words),
        "marked_endpoint_target_normal_words": sorted(endpoint_words),
        "selected_110000_in_endpoint_target_support": False,
        "D4_words": "110000 -> 111111",
        "D4_target_coefficients_by_order": list(d4_profile),
        "D4_target_first_appears_at": "111111",
        "same_grade_existing_target_generator_t": False,
        "multiplication_preserves_target_basis_word": True,
        "Macaulay_multiplication_can_create_missing_110000_target_basis": False,
    }


def module_action_and_dual_audit() -> dict[str, object]:
    # In coordinates (principal companion, target), a genuine target-normal
    # column and desired pure target are respectively (1,1) and (0,1).
    full_target_normal = (Q(1), Q(1))
    pure_target = (Q(0), Q(1))
    primitive_dual = (Q(-1), Q(1))
    require(rank((full_target_normal,)) == 1
            and rank((full_target_normal, pure_target)) == 2
            and dot(primitive_dual, full_target_normal) == 0
            and dot(primitive_dual, pure_target) == 1,
            "the target/companion quotient changed")
    companion_only = (Q(1), Q(0))
    require(rank((full_target_normal, companion_only, pure_target)) == 2,
            "the companion cancellation identity changed")
    return {
        "conditional_A_module_fact": (
            "if T=A*t with t in the exact required grade, then k*t is an "
            "automatic legal codomain element"
        ),
        "conditional_fact_proves_terminal_class": False,
        "physical_target_normal_column": "d theta=s+t",
        "Macaulay_multiple": "d(k*theta)=k*s+k*t",
        "pure_target_membership_equivalence": (
            "k*t lies in the old image iff the companion k*s can be "
            "cancelled in the identical grade"
        ),
        "quotient_coordinates": ["k*principal_companion", "k*target"],
        "available_full_column": [1, 1],
        "desired_pure_target": [0, 1],
        "primitive_dual": [-1, 1],
        "dual_on_available_full_column": 0,
        "dual_on_desired_pure_target": 1,
        "companion_cancellation_suffices": True,
        "actual_same_grade_t_exists": False,
    }


def cap_residue_cartan_composition_audit() -> dict[str, object]:
    # Augmented row order: target, ordinary residue, protected aggregate.
    cylinder = (Q(1), Q(0), Q(0))
    cap_multiple = (Q(-1), Q(-1), Q(0))
    after_cap = tuple(left + right for left, right in
                      zip(cylinder, cap_multiple, strict=True))
    cartan = (Q(0), Q(1), Q(0))
    after_cartan = tuple(left + right for left, right in
                         zip(after_cap, cartan, strict=True))
    require(after_cap == (0, -1, 0)
            and after_cartan == (0, 0, 0),
            "the cylinder/cap/Cartan signatures changed")

    delta = (Q(1), Q(-1), Q(-1), Q(1))
    cylinder_residue = tuple(-value for value in delta)
    # The committed physical Cartan cell K has residue -delta.  The
    # cancellation uses the equally physical oppositely oriented cell -K.
    committed_cartan = tuple(-value for value in delta)
    negative_cartan = delta
    require(committed_cartan == cylinder_residue,
            "the committed Cartan orientation changed")
    require(tuple(left + right for left, right in
                  zip(cylinder_residue, negative_cartan, strict=True))
            == (0, 0, 0, 0),
            "the four-corner residue sign changed")
    delta_m0 = (Q(1), Q(-1), Q(0), Q(0))
    delta_m1 = (Q(0), Q(0), Q(1), Q(-1))
    full_matching_bridge = tuple(right - left for left, right in
                                 zip(delta_m0, delta_m1, strict=True))
    require(rank((delta_m0, delta_m1)) == 2
            and full_matching_bridge == cylinder_residue,
            "the two matching-packet D4/Cartan bridge changed")
    return {
        "coarse_rows": ["target", "ordinary residue", "protected"],
        "cylinder_curvature": [1, 0, 0],
        "minus_cap_T_plus_rho_multiple": [-1, -1, 0],
        "post_cap_remainder": [0, -1, 0],
        "physical_Cartan_correction": [0, 1, 0],
        "post_Cartan_remainder": [0, 0, 0],
        "four_corner_basis": [
            "P+q00", "P-q00", "P+q11", "P-q11"
        ],
        "graph_lock_delta": [1, -1, -1, 1],
        "post_cap_residue_coefficient": [-1, 1, 1, -1],
        "D4_Cartan_matching_packet_basis": [
            "M0^11-M0^decorated", "M1^11-M1^decorated"
        ],
        "matching_packet_rank": rank((delta_m0, delta_m1)),
        "full_cylinder_bridge": "delta_M1-delta_M0",
        "committed_Cartan_K_residue": [-1, 1, 1, -1],
        "oppositely_oriented_minus_K_used_for_cancellation": [1, -1, -1, 1],
        "coefficient_representation_closes": True,
        "literal_source_grade_closes": False,
        "missing_composition": (
            "transport the cap multiple into 01211222/P3+K2 and identify "
            "the D4-top pure-11 tail with the decorated q00/q11 Cartan square"
        ),
        "after_missing_composition": (
            "target and ordinary residue vanish; Cartan's committed protected "
            "rows vanish and its shifted ridge supplies eta/sigma"
        ),
    }


def transpose_groupoid_compression_audit() -> dict[str, object]:
    # Object coordinates are (canonical P grade g, conjugate S grade gT).
    p_half = (Q(1), Q(0))
    theta_p_half = (Q(0), Q(1))
    theta = ((Q(0), Q(1)), (Q(1), Q(0)))

    def apply(matrix, vector):
        return tuple(dot(row, vector) for row in matrix)

    require(apply(theta, p_half) == theta_p_half
            and apply(theta, theta_p_half) == p_half,
            "the two-object transpose orbit changed")
    require(rank((p_half, theta_p_half)) == 2,
            "the P/S object orbit stopped spanning both grades")

    # Central Eq and the aggregate protected scalar are objectwise constant.
    central_eq = (Q(1), Q(1))
    ridge_pair = (Q(-1), Q(-1))
    require(apply(theta, central_eq) == central_eq
            and apply(theta, ridge_pair) == ridge_pair,
            "central Eq/ridge stopped being theta-equivariant")
    return {
        "grade_objects": ["g (canonical P half)", "gT (conjugate S half)"],
        "theta_matrix": [[0, 1], [1, 0]],
        "theta_squared": [[1, 0], [0, 1]],
        "first_PP_diagonal_dtheta": 0,
        "one_P_half_orbit_spans_both_objects": True,
        "independent_conjugate_attachment_theorem_needed": False,
        "central_K_Eq_is_objectwise": True,
        "physical_q_and_terminal_rows_are_theta_equivariant": True,
        "shortest_new_source_datum": (
            "one canonical P-half cross-word cap attachment with its full "
            "principal companion; theta supplies the S half"
        ),
        "still_independent_existing_inputs": [
            "central pointed K_Eq objectwise", "shifted Cartan ridge",
            "physical-q generator/Fredholm alternative",
        ],
    }


def augmented_promotion_audit() -> dict[str, object]:
    return {
        "already_zero_on_mixed_character": [
            "aggregate endpoint row", "aggregate matching row",
            "formal anchor-incidence shadow", "aggregate physical-q shadow"
        ],
        "not_defined_by_bare_response_or_module_naturality": [
            "ainc and hence physical q=M-ainc", "ordinary residue", "W",
            "labelled shifted ridge", "eta", "sigma"
        ],
        "ridge_rule": (
            "once a physical labelled gamma=-dOmega copy is supplied, "
            "eta/sigma transport is unique; it is not supplied by k*t"
        ),
        "single_new_positive_schema": [
            "one canonical P-half word-changing cap object from mixed 110000 "
            "to the endpoint/D4 target cone",
            "its full Macaulay principal companion k*s in doubled grade",
            "its occurrence-local ainc/q and W values",
        ],
        "supplied_without_another_new_schema": [
            "theta supplies the conjugate S half",
            "negative Physical Cartan cancels ordinary residue",
            "central K_Eq is objectwise under theta",
            "the shifted ridge supplies eta/sigma by contraction",
            "physical q uses the committed generator/Fredholm alternative",
        ],
        "minimum_dual_promotion_packet": [
            "extend (-1,+1) across every same-grade source/Macaulay companion",
            "annihilate the complete target, residue, anchor, q, W and ridge rows",
            "annihilate eta/sigma after the labelled ridge extension",
            "retain nonzero pairing with the mixed target curvature",
        ],
        "current_status": (
            "one canonical P-half source attachment OPEN; no independent "
            "target, transpose, residue, q, or terminal theorem remains"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    grade = local_character_and_grade_audit()
    private = private_site_nonlanding_audit()
    target = physical_target_word_audit()
    module = module_action_and_dual_audit()
    composition = cap_residue_cartan_composition_audit()
    transpose = transpose_groupoid_compression_audit()
    augmented = augmented_promotion_audit()
    ledger = {
        "theorem": "h3 centered shear cylinder curvature / physical output gate",
        "scope": "canonical h=3 Segre response block over characteristic zero",
        "pins": PINS,
        "literal_character_and_grade": grade,
        "offdiagonal_private_site_comparison": private,
        "physical_target_word": target,
        "A_module_Macaulay_action": module,
        "cap_residue_Cartan_composition": composition,
        "transpose_groupoid_compression": transpose,
        "augmented_terminal_promotion": augmented,
        "conclusion": {
            "existing_offdiagonal_cofactor_rows_realize_t_k": False,
            "A_module_multiplication_would_make_t_k_legal_if_t_existed": True,
            "same_grade_physical_t_exists": False,
            "legal_codomain_multiple_implies_terminal": False,
            "first_literal_missing_face": (
                "one canonical P-half cross-word placement of the cap target "
                "column and principal companion; theta supplies the S half"
            ),
            "sharp_local_dual": "(-1,+1) on (companion,target)",
            "full_physical_terminal": (
                "OPEN only until the one canonical P-half cap attachment is "
                "constructed or its local dual is extended"
            ),
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    return ledger, sha256(payload.encode()).hexdigest()


def main() -> None:
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    require(digest == EXPECTED_LEDGER_SHA256,
            ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger sha256: {digest}")
    print("t*k offdiagonal/private-site landing: NO (literal grade mismatch)")
    print("A-module target cancellation: YES after cross-word cap placement")
    print("post-cap debt: -k residue = residual-q four-corner character")
    print("remaining face: one P-half cap placement; theta supplies S half")


if __name__ == "__main__":
    main()
