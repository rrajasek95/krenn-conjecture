#!/usr/bin/env python3
"""Audit the mixed product of the five h_v reset cells with T*H_W.

There is a genuine coefficient-level effect which is invisible in the two
factorwise darkness audits.  The endpoint-even switch has three-chart
profile

    T=(-2,1,1).

After the normalized even split of the direct chart into the two oriented
DQ corners this is -delta=(-1,-1,1,1).  Thus, if the central Eq conormal
could be multiplied into the literal corner-Eq module, its Eq-only shadow
would have nonzero Psi_loc.

That shadow is not yet a physical column.  For an odd reset carrier N_v and
X=T*H_W, the full differential is

    d(N_v X)=(dN_v)T H_W-N_v(dT)H_W-N_vT(W-1).

The last two terms are forced by d^2.  They retain the response/C4/P2,
Weyl, word, fine and repeated labels; the signed Weyl action cannot change
those labels.  No committed product comparison maps the resulting tensor
grades to the corner-resolved P3+K2 B/Eq packet.  Hence the strict physical
projection is zero/off-grade.  If such a comparison is merely granted, the
same source boundary still allows a tied dark completion or an Eq-only
bright completion: its B/Eq augmentation is an independent scalar.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_degree4_hv_psiloc_augmented_landing_gate.py":
        "5032493dce5c96b0ddb28175dd8b8a9a73a3c4f566d48d48d63f673802a85106",
    "computations/verify_h3_gate_ii_switch_weyl_product_rule_idempotent_gate.py":
        "fbd4815eb5c6d46b8dbcd018f6e75237f004e3f52b1ccf47631479b698f9db35",
    "computations/verify_h3_gate_ii_chiw_chart_complete_h2_face.py":
        "a80e5ec2a1aaa90814b412d13b1c7981f345bb41ca5a5450d5361ae2bc9f5773",
    "computations/verify_h3_gate_ii_signed_weyl_telescope_matching_constant_gate.py":
        "092c90da62c9bd900939388a1ec7110de28f50c7b070d5029069ea3c3c9373a1",
    "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py":
        "6c42cd4dc7dca1544dc0b675f5f4543ec348f1fba34b7ea14bf80cc6a20b9cf1",
    "computations/verify_h3_cross_word_mapping_cylinder_d2_augmentation_freedom_gate.py":
        "3704235f1030a07556aaebed3225bec8ea0fb9fa4d6a4d3aa124a7727a3bebec",
    "computations/verify_h3_five_denominator_hafnians_complete_intersection.py":
        "4c87c1db939346e8f1d83a26b5edef19e3143a65cc6d6fd5ea636f99d13b5615",
    "notes/h3-degree4-hv-psiloc-augmented-landing-gate.md":
        "e431d03f23c2549e0987d680e48389775444f72eb2ba17cdb5529ed64036a5f5",
    "notes/h3-gate-ii-switch-weyl-product-rule-idempotent-gate.md":
        "432a612161538958c069de828b1f0f0a3321e5bdaa758be104942140df768b7d",
}
EXPECTED_LEDGER_SHA256 = "cf424a6adbccfc4bf0fffd969c0402a16020d4924e78f9df110029e7f508e472"


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
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def matvec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def source_factor_audit(hv_ledger, switch_ledger, chart_ledger,
                        telescope_ledger):
    reset = hv_ledger["five_degree_four_reset_cells"]
    projection = hv_ledger["literal_and_formal_projection_to_Psi_loc"]
    product = switch_ledger["presentation_safe_product"]
    inventory = switch_ledger["full_dt_face_inventory"]
    signed = telescope_ledger["physical_provenance"]
    require(reset["cells"] == 5
            and reset["terms_per_h_v"] == 3
            and reset["distinct_quadratic_terms"] == 15
            and reset["underived_residual"] == "h_v*(H0-u)*e_Eq"
            and projection["literal_projection_to_corner_B_Eq"] == "zero"
            and product["formal_product_in_extended_DGA"]
            and product["total_differential"]
                == "D(T*H_W)=(d_PP T)*H_W+T*(W-1)"
            and inventory["full_dT_support"] == 36
            and inventory["residual_edge_half"]["support"] == 18
            and inventory["direction_factor_half"]["support"] == 18
            and not signed["connected_SL3_or_Weyl_changes_B_label"],
            "the mixed-product input frontier changed")
    return {
        "reset_cells": 5,
        "terms_per_h_v": 3,
        "distinct_h_v_matching_terms": 15,
        "reset_underived_residual": "h_v*(H0-u)*e_Eq",
        "reset_literal_corner_projection": "zero/off-grade",
        "switch_Weyl_cell": "X=T*H_W",
        "switch_Weyl_total_differential": product["total_differential"],
        "dT_faces": {"tail": 18, "direction": 18},
        "Weyl_preserves": signed["colour_action_preserves"],
        "factorwise_status": (
            "both factors are genuine derived/relative source objects, but "
            "neither factor supplies the tensor-to-corner cap comparison"
        ),
    }


def coefficient_shadow_audit(local, chart_ledger):
    chart_data = chart_ledger["chart_character"]
    complete = tuple(map(Q, chart_data["complete_row"]))
    endpoint_even = tuple(map(Q, chart_data["chi_w_endpoint_even"]))
    switch_t = tuple(map(Q, chart_data["switch_carrier_t1_plus_t2"]))
    delta = tuple(map(Q, (1, 1, -1, -1)))

    # The A-coordinate is the aggregate of the two oriented DQ roots.
    # The normalized even/root split sends A/2 to either orientation and
    # leaves the two PS charts unchanged.
    normalized_chart_to_corner = (
        (Q(1, 2), 0, 0),
        (Q(1, 2), 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    )
    require(complete == (1, 1, 1)
            and endpoint_even == (2, -1, -1)
            and switch_t == (-2, 1, 1)
            and matvec(normalized_chart_to_corner, endpoint_even) == delta
            and matvec(normalized_chart_to_corner, switch_t) == scale(-1, delta),
            "the normalized chart-to-corner shadow changed")

    dual = scale(Q(1, 12), local.integral_terminal_dual())
    eq_minus_delta = scale(-1, local.balanced_top("Eq"))
    b_minus_delta = scale(-1, local.balanced_top("B"))
    tied_minus_delta = add(eq_minus_delta, b_minus_delta)
    require(dot(dual, eq_minus_delta) == 1
            and dot(dual, b_minus_delta) == -1
            and dot(dual, tied_minus_delta) == 0,
            "the top mixed-product shadow changed")

    # dT has the negative of the primitive six-direction profile and the
    # negative balanced tail profile.  The factor two is the two Leibniz
    # slots in each chart (two direction edges or two tail deletions).
    eq_direction = scale(-1, local.primitive_direction_face("Eq"))
    eq_tail = scale(-1, local.balanced_tail_face("Eq"))
    tied_direction = add(eq_direction,
                         scale(-1, local.primitive_direction_face("B")))
    tied_tail = add(eq_tail, scale(-1, local.balanced_tail_face("B")))
    require(dot(dual, eq_direction) == 2
            and dot(dual, eq_tail) == 2
            and dot(dual, tied_direction) == 0
            and dot(dual, tied_tail) == 0,
            "the lower mixed-product shadows changed")
    return {
        "three_chart_order": ["A=DQ aggregate", "B=PS01", "C=PS10"],
        "T_profile": [-2, 1, 1],
        "normalized_direct_root_split": (
            "J(a,b,c)=(a/2,a/2,b,c)"
        ),
        "J_of_T": [-1, -1, 1, 1],
        "J_of_T_equals": "-delta",
        "formal_Eq_only_corner_shadow": "Eq=-delta on each C4 matching",
        "normalized_Psi_on_Eq_only_shadow_per_h_v": "h_v",
        "normalized_Psi_on_private_only_shadow_per_h_v": "-h_v",
        "normalized_Psi_on_tied_shadow_per_h_v": "0",
        "proper_face_shadow": {
            "dT_direction_profile": [-2, -2, 1, 1, 1, 1],
            "normalized_Psi_on_Eq_only_direction_packet_per_h_v": "2*h_v",
            "normalized_Psi_on_Eq_only_tail_packet_per_h_v": "2*h_v",
            "normalized_Psi_on_either_tied_packet": "0",
        },
        "positive_but_forgetful_conclusion": (
            "operation decoration can turn the diagonal central coefficient "
            "into the unique balanced corner character; the coefficient "
            "shadow is bright rather than symmetry-forced dark"
        ),
    }


def full_leibniz_audit() -> dict[str, object]:
    # N is odd, X=T*H is odd, K=W-1 is closed and dH=K.  Expand the three
    # first-boundary terms and their second boundaries explicitly.
    first = Counter({
        "dN*T*H": 1,
        "N*dT*H": -1,
        "N*T*K": -1,
    })
    second_from_reset = Counter({
        "dN*dT*H": 1,
        "dN*T*K": 1,
    })
    second_from_dt = Counter({
        "dN*dT*H": -1,
        "N*dT*K": -1,
    })
    second_from_root = Counter({
        "dN*T*K": -1,
        "N*dT*K": 1,
    })
    total_second = Counter()
    for boundary in (second_from_reset, second_from_dt, second_from_root):
        for name, value in boundary.items():
            total_second[name] += value
    total_second = Counter({name: value for name, value in total_second.items()
                            if value})
    require(not total_second,
            (second_from_reset, second_from_dt, second_from_root))

    reset_only = second_from_reset
    require(reset_only == Counter({"dN*dT*H": 1, "dN*T*K": 1}),
            "omitting the cross terms unexpectedly preserved d squared")
    return {
        "candidate": "Z_v=N_v*(T*H_W), |N_v|=|T*H_W|=1",
        "full_first_boundary": dict(first),
        "formula": (
            "dZ_v=(dN_v)T H_W-N_v(dT)H_W-N_vT(W-1)"
        ),
        "second_boundaries": {
            "from_(dN)TH": dict(second_from_reset),
            "from_-N(dT)H": dict(second_from_dt),
            "from_-NTK": dict(second_from_root),
        },
        "d_squared": 0,
        "if_only_the_formal_bright_reset_term_is_kept": {
            "uncancelled": dict(reset_only),
            "d_squared_zero": False,
        },
        "five_cell_cross_face_census": {
            "carrier_level_tail_families": 5 * 18,
            "carrier_level_direction_families": 5 * 18,
            "carrier_level_total_dT_families": 5 * 36,
            "h_v_monomial_decorated_tail_occurrences": 5 * 3 * 18,
            "h_v_monomial_decorated_direction_occurrences": 5 * 3 * 18,
            "h_v_monomial_decorated_total": 5 * 3 * 36,
            "root_W_families": 5,
        },
        "cross_terms_optional": False,
    }


def typed_product_projection_audit(hv_ledger, switch_ledger,
                                   telescope_ledger) -> dict[str, object]:
    reset = hv_ledger["literal_and_formal_projection_to_Psi_loc"]
    typed = switch_ledger["first_typed_gate"]
    provenance = telescope_ledger["physical_provenance"]
    require(reset["raw_reset_site_grade"] == "squarefree 2K2"
            and reset["required_mixed_landing_grade"] == "repeated P3+K2"
            and typed["projection_of_direction_candidate_to_P2"]
                == [0, 0, 0, 0, 0]
            and not provenance["connected_SL3_or_Weyl_changes_B_label"],
            "the product typing obstruction changed")

    terms = {
        "(dN_v)T H_W": {
            "contains": (
                "h_v*central-Eq (and derived h_v*Yw) tensored with the "
                "switch/Weyl homotopy"
            ),
            "literal_B_Eq_projection": 0,
            "reason": (
                "central 2K2 Eq x Weyl/switch is a tensor grade, not a "
                "corner-resolved t*q_(v,N) P3+K2 cap row"
            ),
        },
        "-N_v(dT)H_W": {
            "contains": "90 tail plus 90 direction carrier families over v",
            "literal_B_Eq_projection": 0,
            "reason": (
                "tail C2plus/P2 and direction C4 response tags remain "
                "tensored with N_v and the Weyl homotopy"
            ),
        },
        "-N_vT(W-1)": {
            "contains": "five root/Weyl boundary families",
            "literal_B_Eq_projection": 0,
            "reason": (
                "W-1 is a root/W row, not a private-B cap incidence; "
                "turning it into B is the missing response-to-cap descent"
            ),
        },
    }
    return {
        "reset_tags": {
            "word": "01211222",
            "fine_repeated": "raw squarefree 2K2",
            "operation": "central Hasse/Koszul; no DQ/PS or AB/AC label",
            "row": "central e_Eq",
        },
        "switch_Weyl_tags": {
            "top": "retained chart switch T x root-colour Weyl homotopy",
            "direction": "Hasse[2](DQ/PS), relative C4",
            "tail": "C2plus/P2 response face",
            "Weyl_scope": "changes colour word; preserves matching, repeated and H2 tags",
        },
        "required_output_tags": {
            "word": "01211222 after the response-to-cap arrow",
            "fine_repeated": "t*q_(v,N), repeated P3+K2",
            "operation": "one DQ/PS corner and AB/AC root label",
            "row": "corner-resolved private B or reduced Eq",
        },
        "termwise_projection": terms,
        "strict_projection_of_full_Leibniz_boundary_to_B_Eq": "zero/off-grade",
        "root_or_Maschke_projector_scope": (
            "it realizes the normalized coefficient split J and may recolour "
            "root words, but cannot change the operation, repeated, word/fine "
            "or central-Eq source idempotents"
        ),
        "physical_tensor_to_corner_chain_map_constructed": False,
    }


def augmentation_and_primitivity_audit(freedom, hv_ledger):
    freedom_data = freedom.augmentation_audit()
    quotient = freedom.quotient_audit()
    counterguard = freedom_data["same_source_boundary_counterguard"]
    reset = hv_ledger["five_degree_four_reset_cells"]
    require(counterguard["dark_filler"]["chi"] == 0
            and counterguard["bright_filler"]["chi"] == 4
            and counterguard["both_satisfy_d_squared_zero"]
            and quotient["set_of_d_squared_compatible_values_over_Q"]
                == "chi=4*lambda, lambda arbitrary in Q"
            and reset["denominator_complete_intersection_height"] == 5
            and not reset["denominator_only_primitive_unit_aggregate"],
            "the product augmentation/primitivity guard changed")
    return {
        "after_granting_a_tensor_to_corner_square": {
            "dark_completion": "B=Eq=-delta, Psi=0",
            "bright_completion": "B=0, Eq=-delta, Psi=+1",
            "same_projected_source_boundary": True,
            "both_d_squared_compatible": True,
            "general_value": "chi=4*lambda, lambda arbitrary",
        },
        "what_the_product_coefficients_suggest": (
            "the Eq-only convention would give Psi=h_v for the v-th reset"
        ),
        "what_the_source_differential_forces": (
            "neither Eq-only nor tied B=Eq; the cap augmentation is an "
            "independent chain-map datum"
        ),
        "five_h_v_coefficients": {
            "height": 5,
            "first_syzygies": "Koszul h_i*e_j-h_j*e_i",
            "denominator_only_primitive_unit_aggregate": False,
        },
        "consequence": (
            "even a future bright product remains h_v-weighted until an "
            "additional source-valid normalization/localization is proved"
        ),
    }


def audit():
    pin_dependencies()
    hv = load(
        "computations/verify_h3_degree4_hv_psiloc_augmented_landing_gate.py",
        "hv_switch_product_hv")
    switch = load(
        "computations/verify_h3_gate_ii_switch_weyl_product_rule_idempotent_gate.py",
        "hv_switch_product_switch")
    chart = load(
        "computations/verify_h3_gate_ii_chiw_chart_complete_h2_face.py",
        "hv_switch_product_chart")
    telescope = load(
        "computations/verify_h3_gate_ii_signed_weyl_telescope_matching_constant_gate.py",
        "hv_switch_product_telescope")
    local = load(
        "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py",
        "hv_switch_product_local")
    freedom = load(
        "computations/verify_h3_cross_word_mapping_cylinder_d2_augmentation_freedom_gate.py",
        "hv_switch_product_freedom")

    hv_ledger, hv_digest = hv.audit()
    switch_ledger, switch_digest = switch.audit()
    chart_ledger, chart_digest = chart.audit()
    telescope_ledger, telescope_digest = telescope.audit()
    local_ledger, local_digest = local.audit()
    require(hv_digest == hv.EXPECTED_LEDGER_SHA256
            and switch_digest == switch.EXPECTED_LEDGER_SHA256
            and chart_digest == chart.EXPECTED_LEDGER_SHA256
            and telescope_digest == telescope.EXPECTED_LEDGER_SHA256
            and local_digest == local.EXPECTED_LEDGER_SHA256
            and local_ledger["exhaustive_local_supermap"]["rank"] == 126,
            "a factor/local ledger changed")
    ledger = {
        "theorem": "h3 h_v reset x switch-Weyl mixed-product B/Eq Leibniz gate",
        "pins": PINS,
        "source_factors": source_factor_audit(
            hv_ledger, switch_ledger, chart_ledger, telescope_ledger),
        "formal_coefficient_corner_shadow":
            coefficient_shadow_audit(local, chart_ledger),
        "full_Leibniz_totalization": full_leibniz_audit(),
        "literal_word_fine_repeated_operation_projection":
            typed_product_projection_audit(
                hv_ledger, switch_ledger, telescope_ledger),
        "B_Eq_augmentation_and_h_v_primitivity":
            augmentation_and_primitivity_audit(freedom, hv_ledger),
        "verdict": (
            "The mixed-product idea has a genuine positive coefficient "
            "shadow: the source-provenant switch profile T=(-2,1,1) becomes "
            "-delta after the normalized split of the direct chart, so an "
            "Eq-only corner lift would have Psi=h_v.  This does not construct "
            "a physical chi-bright column.  The full Leibniz differential "
            "also contains N_v(dT)H_W and N_vT(W-1); omitting either breaks "
            "d^2.  All three terms remain in tensor products of the central "
            "2K2 reset grade with response C2plus/C4/P2 or root/Weyl grades. "
            "Weyl/root projectors preserve the missing word/fine/repeated and "
            "operation idempotents, so the current strict B/Eq projection is "
            "zero/off-grade.  Granting a tensor-to-corner comparison still "
            "leaves the B/Eq scalar arbitrary: tied dark and Eq-only bright "
            "completions share the same source boundary.  Finally the bright "
            "shadow is h_v-weighted and the five h_v have no primitive unit "
            "aggregate."
        ),
        "classification": (
            "FORMAL CHI-BRIGHT COEFFICIENT SHADOW; NO PHYSICAL PRODUCT COLUMN"
        ),
        "shortest_positive_datum": (
            "construct one multiplicative source-labelled comparison from "
            "the reset x switch-Weyl tensor totalization to the corner-resolved "
            "P3+K2 cap complex.  It must route all 90 tail and 90 direction "
            "carrier faces plus the five W/root faces, specify an untied "
            "B/Eq augmentation, and supply a primitive normalization of the "
            "remaining h_v coefficient"
        ),
        "nonclaims": [
            "the formal J(T)=-delta shadow is not called a physical cap projection",
            "the root/W face is not silently renamed as a private-B row",
            "off-grade cross terms are not discarded from the Leibniz boundary",
            "d-squared compatibility is not used to select a B/Eq augmentation",
            "an h_v-weighted bright value is not called a primitive unit landing",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("h_v x switch-Weyl product ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("h_v reset x T*H_W coefficient shadow: J(T)=-delta, FORMALLY BRIGHT")
    print("full Leibniz: reset term + 180 dT carrier faces + 5 W/root faces")
    print("literal B/Eq projection: ZERO/OFF-GRADE")
    print("tied versus Eq-only completion: UNFORCED BY d^2")
    print("primitive value: STILL h_v-WEIGHTED")
    print("physical chi-bright product column: NOT CONSTRUCTED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
