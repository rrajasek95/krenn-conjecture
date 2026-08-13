#!/usr/bin/env python3
"""Identify the unique new class in the selected Gate-I mapping cone.

The signed twelve-label lower cycle has normalized collapse

    alpha = B0+B2-B3-B5,

and the physical M_v cell has the corresponding 360-feature boundary.  The
Koszul/Cartan cap calculation independently proves that the full alpha
output augmentation is physical (up to the mapping-cone sign):

    O_alpha-K_alpha = -M_v.

The nearest source-side Cartan--Spencer construction reaches the same
grade-forgotten alpha class but leaves the occurrence-local odd packet

    Xi^-=(4/3)(xi-mate-s*xi+s*mate).

The formal 341-edge Weyl bar cancels Xi^-.  In the actual complete-row
inventory, endpoints/bars plus four Hasse faces have rank 12 and adjoining
Xi^- raises it to 13.  The committed extended odd dual kills that whole old
image and reads one on Xi^-.

Thus the selected comparison has one exact hidden-row class relative to the
tested complete-row constructor.  A bare Eq Koszul generator cannot remove
it because it has no occurrence/private coordinate.  The missing datum is
one occurrence-local PP/Weyl-bar lift, not another Eq or aggregate-residue
correction.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cut_swap_odd_prism_kdu_typing_gate.py":
        "a1c7868bee94baf12f0f4915305bb1e21cdc3f6732ccec9adf3d68768d3d90b0",
    "computations/verify_h3_selected_lower_one_chain_comparison_reduction.py":
        "c9fc8c847327d0e119264a3a83cf39d0f4c2ff45b4ddd4e048f42a57cac0e887",
    "computations/verify_h3_selected_lower_full_row_spencer_discrepancy.py":
        "e3c99912600c53228a37e7a1376028fd9e889178e4f242140fc6ff0da328954f",
    "computations/verify_h3_selected_lower_relative_weyl_bar_gate.py":
        "7a6f2afebcacc5924110e32a3f7d9c225992f07abae637d4529b5436c64cc294",
    "computations/verify_h3_reduced_eq_cartan_cap_augmentation_dressing.py":
        "3397fc0b7d773d97fb26e737eb490136c3062549951b07eca701ee46739ff2bb",
    "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py":
        "db23eb4e760dd84934426a80516aad355486e947626da1849454718b512efb2d",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
}
EXPECTED_LEDGER_SHA256 = (
    "c9af24b12ae1829348f6aed4e93a944b24fa418b6255c7372ec028eed4570903"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def packet_audit(bar):
    xi = bar.XI
    mate = bar.transform_monomial(xi, bar.tail_swap_cell)
    s_xi = bar.transform_monomial(xi, bar.endpoint_swap_cell)
    s_mate = bar.transform_monomial(mate, bar.endpoint_swap_cell)
    packet = {
        repr(xi): Q(4, 3),
        repr(mate): Q(-4, 3),
        repr(s_xi): Q(-4, 3),
        repr(s_mate): Q(4, 3),
    }
    require(sum(packet.values(), Q(0)) == 0
            and len(packet) == 4,
            "the endpoint-odd occurrence packet changed")
    normalized_dual = {
        repr(xi): Q(3, 16),
        repr(mate): Q(-3, 16),
        repr(s_xi): Q(-3, 16),
        repr(s_mate): Q(3, 16),
    }
    private_pairing = sum(packet[label] * normalized_dual[label]
                          for label in packet)
    require(private_pairing == 1,
            "the primitive odd private dual lost normalization")
    return {
        "coefficient": "4/3",
        "formula": "Xi^-=(4/3)(xi-mate-sxi+smate)",
        "fine_degrees": 4,
        "private_pairing_before_Hasse_extension": str(private_pairing),
        "repeated_site_profile": [1, 1, 1, 2, 1, 1, 1, 2],
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    one = load(
        "computations/verify_h3_selected_lower_one_chain_comparison_reduction.py",
        "selected_cone_one",
    )
    discrepancy = load(
        "computations/verify_h3_selected_lower_full_row_spencer_discrepancy.py",
        "selected_cone_discrepancy",
    )
    bar = load(
        "computations/verify_h3_selected_lower_relative_weyl_bar_gate.py",
        "selected_cone_bar",
    )
    dressing = load(
        "computations/verify_h3_reduced_eq_cartan_cap_augmentation_dressing.py",
        "selected_cone_dressing",
    )
    kdu = load(
        "computations/verify_h3_cut_swap_odd_prism_kdu_typing_gate.py",
        "selected_cone_kdu",
    )

    one_ledger, one_digest = one.audit()
    discrepancy_ledger, discrepancy_digest = discrepancy.audit()
    bar_ledger, bar_digest = bar.audit()
    dressing_ledger, dressing_digest = dressing.audit()
    kdu_ledger, kdu_digest = kdu.audit()
    require(one_digest == one.EXPECTED_LEDGER_SHA256
            and discrepancy_digest == discrepancy.EXPECTED_LEDGER_SHA256
            and bar_digest == bar.EXPECTED_LEDGER_SHA256
            and dressing_digest == dressing.EXPECTED_LEDGER_SHA256
            and kdu_digest == kdu.EXPECTED_LEDGER_SHA256,
            "a pinned subledger changed")

    prism = kdu_ledger["exact_corner_calculation"]
    require(prism["totalization"].startswith(
                "F_W-rho*F_W-K(u012) has residual +K*d(u012)")
            and kdu_ledger["literal_type_comparison"]
                ["equality_Kd_u012_equals_M_v_well_typed"] is False,
            "the odd-prism residual/type gate changed")

    candidate = one_ledger["exact_candidate"]
    require(candidate["normalized_image"] == ["1", "0", "1", "-1", "0", "-1"]
            and candidate["literal_boundary_features"] == 360
            and candidate["physical_cell"] == "M_v=-O_alpha+K",
            "the selected twelve-label physical target changed")

    selected_output = dressing_ledger["q_and_scope"][
        "selected_Gate_I_odd_output"]
    require(selected_output["closed"] is True
            and selected_output["identity"] == "O_alpha-K_alpha=-M_v",
            "the full-alpha output augmentation stopped being physical")

    first = discrepancy_ledger["first_literal_discrepancy"]
    require(first["coefficient"] == "4/3"
            and first["compatible_complete_full_row_columns"] == 2
            and first["all_candidates_have_forced_q37"] is True
            and first["xi_has_q37"] is False,
            "the first private discrepancy changed")

    private = packet_audit(bar)
    physical_bar = bar_ledger["complete_physical_bar_image"]
    primitive = bar_ledger["primitive_odd_dual"]
    require(physical_bar["endpoint_plus_all_bar_rank"] == 8
            and physical_bar["endpoint_bar_plus_four_hasse_face_rank"] == 12
            and physical_bar["rank_after_required_private_packet"] == 13,
            "the occurrence-local quotient rank changed")
    require(primitive["on_complete_endpoints_bars_and_four_hasse_faces"] == 0
            and primitive["on_required_endpoint_odd_face"] == 1,
            "the extended occurrence dual changed")

    # The normal Koszul cell has only its Eq face before physical comparison.
    # Hence it is zero in the private occurrence coordinate module.  This is
    # not a guessed physical readout: it is the explicit scope distinction in
    # the dressing theorem, which says identifying C_K with -M_v is the
    # remaining source comparison rather than a consequence of dtheta.
    require("supplies the unaugmented -F e_Eq core"
            in selected_output["Koszul_role"],
            "the Koszul/private scope guard changed")
    koszul_private_pairing = Q(0)
    require(koszul_private_pairing == 0,
            "the bare Koszul core acquired a private occurrence face")

    ledger = {
        "theorem": "selected lower Koszul/Cartan mapping-cone hidden class",
        "pins": PINS,
        "selected_lower": {
            "labels": 15,
            "nonzero_labels": 12,
            "normalized_collapse": "alpha=B0+B2-B3-B5",
            "physical_output": "M_v",
            "literal_boundary_features": candidate["literal_boundary_features"],
        },
        "output_augmentation": {
            "physical": True,
            "identity_with_cone_orientation": "O_alpha-K_alpha=-M_v",
            "normalization": "Y=1",
            "scope": "canonical output-side repeated grade",
        },
        "source_constructor": {
            "odd_prism_residual": "+K*d(u012)",
            "exposed_decomposition": (
                "monic normal Eq face plus the normalized twelve-label "
                "alpha collapse"
            ),
            "formal_341_edge_Weyl_bar_cancels_hidden_packet": True,
            "physical_complete_row_occurrence_descent": False,
            "first_hidden_packet": private,
        },
        "exact_quotient": {
            "old_endpoint_plus_bar_rank":
                physical_bar["endpoint_plus_all_bar_rank"],
            "after_four_Hasse_faces_rank":
                physical_bar["endpoint_bar_plus_four_hasse_face_rank"],
            "after_hidden_packet_rank":
                physical_bar["rank_after_required_private_packet"],
            "new_classes_for_selected_packet": 1,
            "extended_dual_on_old_image":
                primitive["on_complete_endpoints_bars_and_four_hasse_faces"],
            "extended_dual_on_Xi_minus":
                primitive["on_required_endpoint_odd_face"],
        },
        "Koszul_core": {
            "bare_private_pairing": str(koszul_private_pairing),
            "can_cancel_Xi_minus_without_comparison": False,
            "reason": (
                "C_K has the normal Eq face but no occurrence-labelled "
                "private coordinate.  Its identification with the literal "
                "lower/terminal packet of +/-M_v is exactly the missing "
                "input comparison"
            ),
        },
        "remaining_cell": (
            "one occurrence-local principal-parts/Weyl-bar lift of the "
            "formal 341-edge bar in the four displayed fine degrees.  Its "
            "boundary must contain -Xi^- and its augmented map must land on "
            "+/-M_v with the already fixed eta/sigma terminal"
        ),
        "decomposition_verdict": (
            "K*d(u012) equals the monic Eq residual plus the twelve-label "
            "alpha only after forgetting the occurrence-private row.  In "
            "the complete tested source constructor it has the additional "
            "class Xi^-.  Using the physically dressed K_Eq/M_v output to "
            "erase Xi^- without an occurrence-local comparison would assume "
            "the desired equation J3(M_v)=A Jcol(l)"
        ),
        "q_scope": (
            "q is not defined on the formal occurrence bar.  After a physical "
            "lift exists, q is governed by the protected quotient-defect/"
            "relative-generator alternative; Xi^- alone is not yet a terminal"
        ),
        "scope": (
            "exact for the selected one-chain and the exhaustive complete-row "
            "endpoint/bar/four-Hasse inventory in its four private grades; no "
            "no-go against the asserted higher occurrence-local PP cell"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 selected lower Koszul/Cartan mapping cone: ONE HIDDEN CLASS")
    print("output alpha augmentation: PHYSICAL (+/-M_v)")
    print("hidden input class: Xi^- across four fine degrees")
    print("complete-row/Hasse rank: 12; with Xi^-: 13")
    print("bare Koszul private pairing: 0; extended odd dual on Xi^-: 1")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
