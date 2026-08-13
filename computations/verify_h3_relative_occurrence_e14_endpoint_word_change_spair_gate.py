#!/usr/bin/env python3
"""Audit the first physical face of the relative-carrier/E14 word change.

The retained P2 carrier is endpoint-even.  The canonical E14 coefficient
identification hits one term of the unary S-pair remainder, but the exact
first-hit dual is zero on that term.  Its full pairing is carried by a
different companion tail.  Killing the companion chord does not close the
landing: the obstruction moves to literal target-unary readout coordinates.

The target-safe physical Cartan prism is endpoint-odd.  The even prism needed
for the carrier has a target defect and becomes target-safe only conditionally
on the still-missing P2/iota placement.  This identifies the first missing
face beyond the rank-one W landing without promoting the truncated dual to a
physical terminal.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_relative_occurrence_e14_w_carrier_landing_gate.py":
        "37f571234346c8a90465a5e021bb5ed97b0caec68e31a8b80346d25f94c9f337",
    "notes/h3-relative-occurrence-e14-w-carrier-landing-gate.md":
        "a4a0e1be3cff6779f3641f6c3f1faa6431eac01b85a4cdf1bfbfc9d595d56888",
    "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py":
        "893f000e37e4bcfc78973cb042cc0858087cb25605d6cf070a1bf8dfa7a76b7a",
    "notes/h3-c6-e14-unary-spair-first-reduction-boundary.md":
        "9d3af91f0e97079c8e2bd2dd76db110fdde45e71eed0d21805bdd4575a683c4f",
    "computations/verify_h3_order2_promoted_occurrence_orientation_gate.py":
        "c0a34736979eb8a5d059dce30224b3d22f3930e9afaf07916dbbf51b3539c15d",
    "computations/verify_h2_lower_even_cartan_jstar_target_cone_gate.py":
        "09ba792f229bb3a1e930b2c59b0de2356b08a7434c648aad9573d8382c652a52",
    "computations/verify_h3_cplus_q_ridge_w_terminal_reduction.py":
        "b2ace6e49aa5ec1b8347a0e88cc39f36e5d773e1aab1d82f424533de8ce52a9a",
    "computations/verify_h3_anchor_conormal_functoriality_bridge.py":
        "83879756547765878c36944c1ab14827ab77a1f217931bc05db0c72cb0af32a8",
    "computations/verify_uniform_cartan_augmented_grade_naturality_gate.py":
        "d71b2ae71cdfc910e374b498a70edbb5e897867cf624dec49203c34e74647925",
}
EXPECTED_LEDGER_SHA256 = (
    "fffc345f161fe4331f4a7c34e152a3c705f03273d069164a336ec66f384f9638"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def sparse(vector, coordinates):
    return {coordinate: coefficient for coordinate, coefficient in
            zip(coordinates, vector, strict=True) if coefficient}


def e14_dual_localization(landing) -> tuple[dict[str, object], dict[str, object]]:
    e14 = landing.canonical_first_hit_module()
    coordinates = e14["coordinates"]
    target = sparse(e14["target"], coordinates)
    dual = sparse(e14["dual"], coordinates)
    endpoint = ("p1_0_1", "s1_1_1")
    core = (endpoint, tuple(sorted(("u05_01", "v2411", "v3410"))))
    companion = (endpoint, tuple(sorted(("u05_01", "v1301", "v2411"))))

    require(core == e14["promoted_coordinate"]
            and target[core] == 1 and dual.get(core, Q(0)) == 0,
            "the decorated-core coordinate or its dual value changed")
    require(target[companion] == -1 and dual[companion] == 1,
            "the companion-tail target/dual pairing changed")
    contributions = {
        coordinate: target_value * dual.get(coordinate, Q(0))
        for coordinate, target_value in target.items()
        if target_value * dual.get(coordinate, Q(0))
    }
    require(contributions == {companion: Q(-1)},
            ("the first-hit target pairing stopped localizing on the companion",
             contributions))
    return {
        "E14_word": "000101",
        "target_tail_count": len(target),
        "decorated_core": list(core[1]),
        "decorated_core_target_coefficient": 1,
        "decorated_core_dual_value": 0,
        "dual_visible_companion": list(companion[1]),
        "companion_target_coefficient": -1,
        "companion_dual_value": 1,
        "entire_target_dual_pairing": -1,
        "only_nonzero_target_dual_contribution": "-1 from companion",
        "consequence": (
            "the relabelled 2K2 core is a literal coefficient hit, but it "
            "does not kill the E14 first-hit class; a source comparison must "
            "carry the whole unary S-pair remainder, including its companion"
        ),
    }, e14


def chord_specialization_audit(e14, first) -> dict[str, object]:
    coordinates = e14["coordinates"]

    def project(vector, prefixes):
        return {
            coordinate: coefficient
            for coordinate, coefficient in zip(coordinates, vector, strict=True)
            if coefficient and not any(
                factor.startswith(prefixes) for factor in coordinate[1]
            )
        }

    records = {}
    for name, prefixes, expected_rank, expected_support in (
        ("q13_zero", ("v13",), 211, 9),
        ("q04_q13_zero", ("v04", "v13"), 185, 8),
    ):
        pivots = {}
        for column in e14["columns"]:
            first.add_exact_column(project(column, prefixes), pivots)
        target = project(e14["target"], prefixes)
        reduced = first.exact_reduce(target, pivots)
        require(len(pivots) == expected_rank
                and len(reduced) == expected_support
                and all(coordinate[0][:1] == ("target_unary",)
                        for coordinate in reduced),
                ("the chord specialization changed", name, len(pivots),
                 reduced))
        records[name] = {
            "first_hit_rank_Q": len(pivots),
            "reduced_target_support": len(reduced),
            "reduced_coordinate_type": "target_unary readout only",
            "reduced_coordinates": [
                {"monomial": list(coordinate[1]),
                 "coefficient": str(coefficient)}
                for coordinate, coefficient in sorted(reduced.items())
            ],
        }
    return {
        "specializations": records,
        "consequence": (
            "removing the dual-visible v13 companion does not retire the "
            "landing class.  It migrates to a target-normal unary readout; "
            "also removing v04 leaves the same kind of obstruction"
        ),
    }


def cartan_target_gate(orientation, even_gate) -> dict[str, object]:
    orientation_ledger, orientation_digest = orientation.audit()
    require(orientation_digest == orientation.EXPECTED_LEDGER_SHA256,
            "the order-two occurrence orientation ledger changed")
    parity = orientation_ledger["parity_decomposition"]
    require(parity["even_component"] == "c_f^+=6*(e_f+e_tau_f)-1"
            and parity["residual_q_selector"]
            == "e_f+e_tau_f (endpoint-even)",
            "the retained occurrence carrier stopped being endpoint-even")

    even_ledger, even_digest = even_gate.audit()
    require(even_digest == even_gate.EXPECTED_LEDGER_SHA256,
            "the even Cartan target-cone ledger changed")
    internal = even_ledger["internal_even_Cartan_no_go"]
    principal = even_ledger["first_principal_parts_residual"]
    scope = even_ledger["physical_scope"]
    require(internal["target_kernel"] == "Q*(1,-1), the odd line"
            and not internal["nonzero_even_target_safe_internal_combination"]
            and even_ledger["per_root_target_cancellation"]
            ["target_cancellation"]
            == "exact on alpha*beta != 0 after P2/iota",
            "the odd/even Cartan target alternative changed")
    require(principal["canonical_two_row_projection"]["required_correction"]
            == "+2D*(H0-u)*Eq"
            and scope["first_unavoidable_obstruction"].startswith(
                "the physical placement of P2(I)"),
            "the first even-prism proper face changed")
    return {
        "relative_carrier_parity": "endpoint-even",
        "target_safe_internal_Cartan_line": "endpoint-odd (1-S)H_w",
        "even_internal_target_safe_line": "zero",
        "even_prism_target_defect": "2*(w-1)Delta",
        "conditional_target_repair": (
            "J*=-2 alpha beta I gives C2+=-1/2(1+S)H_w P2(I), "
            "but only after the missing source-labelled P2/iota placement"
        ),
        "first_PP_residual": "R2+=-1/2(1+S)H_w d(P2(I))",
        "first_known_cone_face": "+2D*(H0-u)*Eq",
        "verdict": (
            "the target-safe physical Cartan prism cannot land the even "
            "carrier.  Its even companion requires precisely the still-open "
            "target-bearing endpoint-word-change/operation-type comparison"
        ),
    }


def downstream_augmented_rows(cplus, anchor, naturality) -> dict[str, object]:
    cplus_ledger, cplus_digest = cplus.audit()
    require(cplus_digest == cplus.EXPECTED_LEDGER_SHA256,
            "the C-plus augmented-remainder ledger changed")
    anchor_ledger, anchor_digest = anchor.audit()
    require(anchor_digest == anchor.EXPECTED_LEDGER_SHA256,
            "the anchor-conormal ledger changed")
    naturality_ledger, naturality_digest = naturality.audit()
    require(naturality_digest == naturality.EXPECTED_LEDGER_SHA256,
            "the Cartan augmented naturality ledger changed")

    require(not cplus_ledger["physical_q"]
            ["independent_q_construction_after_hypotheses"]
            and cplus_ledger["eta_sigma_ridge"]
            ["order6_mixed_commutator"] == 0,
            "the conditional q/ridge closure changed")
    require(anchor_ledger["shortest_new_clause"].startswith(
                "add the anchored-section condition")
            and not anchor_ledger["universal_graph_derived_base_change"]
            ["projection_back_to_original_source_is_quasi_isomorphism"],
            "the anchor-pointedness gate changed")
    ridge = naturality_ledger["ridge_eta_sigma"]
    require(not ridge["arbitrary_common_tail_repairs_degree"]
            and not ridge["site_relabeling_repairs_degree"],
            "the ridge grade obstruction changed")
    return {
        "target": (
            "FIRST: the even Cartan word-change needs the independent "
            "target-bearing P2/iota cone; the first known next face is "
            "+2D(H0-u)Eq"
        ),
        "anchor": (
            "DOWNSTREAM: output anchor zero is insufficient; a pointed "
            "source-algebra map must supply d(u_f-u)"
        ),
        "physical_q": (
            "DOWNSTREAM, NOT INDEPENDENT: after a fully augmented physical "
            "P2/KEq comparison, the committed q-defect alternative closes it"
        ),
        "ridge": (
            "DOWNSTREAM: Hasse/ridge commutation is zero, but the labelled "
            "shifted Kähler lift remains; a common multiplier cannot merge "
            "its two site degrees"
        ),
        "W": (
            "the old Yw=W cap is output typing only; endpoint-evenness does "
            "not force W=0"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    landing = load(
        "computations/verify_h3_relative_occurrence_e14_w_carrier_landing_gate.py",
        "e14_word_change_landing",
    )
    first = load(
        "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py",
        "e14_word_change_first",
    )
    orientation = load(
        "computations/verify_h3_order2_promoted_occurrence_orientation_gate.py",
        "e14_word_change_orientation",
    )
    even_gate = load(
        "computations/verify_h2_lower_even_cartan_jstar_target_cone_gate.py",
        "e14_word_change_even",
    )
    cplus = load(
        "computations/verify_h3_cplus_q_ridge_w_terminal_reduction.py",
        "e14_word_change_cplus",
    )
    anchor = load(
        "computations/verify_h3_anchor_conormal_functoriality_bridge.py",
        "e14_word_change_anchor",
    )
    naturality = load(
        "computations/verify_uniform_cartan_augmented_grade_naturality_gate.py",
        "e14_word_change_naturality",
    )

    localization, e14 = e14_dual_localization(landing)
    ledger = {
        "theorem": "relative occurrence to E14 endpoint-word-change S-pair gate",
        "pins": PINS,
        "E14_first_hit_localization": localization,
        "chord_specialization": chord_specialization_audit(e14, first),
        "Cartan_PP_gate": cartan_target_gate(orientation, even_gate),
        "augmented_row_audit": downstream_augmented_rows(
            cplus, anchor, naturality),
        "smallest_missing_cell": {
            "name": "endpoint-even target-bearing unary-S-pair comparison",
            "principal_boundary": (
                "the full word-000101 unary S-pair remainder minus the "
                "endpoint-even t-carrier in word 01211222"
            ),
            "not_sufficient": (
                "a column landing only on the decorated core "
                "u05_01*v24_11*v34_10"
            ),
            "first_forced_proper_face": (
                "mixed target-normal cone 2*(w-1)Delta; in the strongest "
                "current cone its next face is +2D(H0-u)Eq"
            ),
            "later_faces": [
                "pointed conormal d(u_f-u)",
                "physical q by the committed defect alternative",
                "labelled shifted Kähler ridge and eta/sigma",
                "physical W cap compatibility",
            ],
        },
        "scope": (
            "exact for the canonical h=3 relative-carrier/E14 first-hit "
            "packet and the generic h=2 even Cartan target normal.  It does "
            "not construct P2/iota, prove the remaining target-normal class "
            "is a global physical terminal, or cover beta=0/all h"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("E14 decorated core: HIT, BUT FIRST-HIT DUAL VALUE 0")
    print("dual-visible companion: unary S-pair tail")
    print("q13=0: obstruction migrates to 9 target-unary coordinates")
    print("q04=q13=0: obstruction migrates to 8 target-unary coordinates")
    print("first missing physical face: endpoint-even target-bearing P2/iota cone")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
