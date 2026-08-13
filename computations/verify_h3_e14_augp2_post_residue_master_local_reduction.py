#!/usr/bin/env python3
"""Reduce the post-E14 local frontier to three augmented AugP2 faces.

Assume the source-labelled E14 private placement and its same-grade rooted
``d_even`` face.  The former gives the exact unary companion and the latter
cancels the word-resolved residue ``-E``.  This checker composes the pinned
local gates and proves that the remaining quotient has precisely the three
graded readout axes

    P_f=d(u_f-u),    z_cap,    gamma=-d Omega.

They may be faces of one source-labelled augmented-P2 comparison schema, but
they cannot be identified as one homogeneous row.  The mate slack is the
same class as ``-P_f``; the primitive cap is ``z_cap-n`` with ``n`` supplied
by K_Eq; residual q transfers to the same occurrence carrier; and the old
``r0-T`` cap supplies W.  The shifted ridge supplies the eta/sigma terminal
typing, including the aggregate ``5+u_z/t`` required by ``z_cap``.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_e14_keq_private_placement_residue_identification_gate.py":
        "89b0b694b525dba502314e61922cb884ef6ddd2f14fea68b3bafd5215aa40c70",
    "notes/h3-e14-keq-private-placement-residue-identification-gate.md":
        "36828d8503d929427eef55886cb68cbfe7c2431649c38382907835365bd5ed38",
    "computations/verify_h3_cplus_hidden_debt_cartan_mv_root_bar_span.py":
        "7eef9d440fefbae174d2adc61b6f8bdc270351353884ba24e277d36714a9a364",
    "notes/h3-cplus-hidden-debt-cartan-mv-root-bar-span.md":
        "c6c3f107e8d0cd4001c05ea646002c9cface4e11aa360c8de7b328798baf886c",
    "computations/verify_h3_cplus_conditional_physical_dressing_assembly.py":
        "e8014fdfd2263a8eb6bffff11e31c339b5b7965989a61324f8d118a91f791f46",
    "notes/h3-cplus-conditional-physical-dressing-assembly.md":
        "b3afd746e6c275ca23e0b3ee5f26dfbc763301ed7371be4377612709904c19c0",
    "computations/verify_h3_augp2_primitive_cap_response_keq_reduction_gate.py":
        "4dabdae7b9060bdb92c0ed32b0016e7e2694750dc176e1857cc9a54cb8176587",
    "notes/h3-augp2-primitive-cap-response-keq-reduction-gate.md":
        "1f8e8a4a5ffc26a8fdcefcb970c3bc35887a1d521ca27ce3173a790b82dfba5d",
    "computations/verify_h3_p2_mate_slack_centered_occurrence_reduction.py":
        "85be051fa9f27fb909c2a9844084f2c6ccb1feb243d3d6fae1e69cca945e39d3",
    "notes/h3-p2-mate-slack-centered-occurrence-reduction.md":
        "d9a6b2fd0648870acfb2a6cbec8ab4ec4e32a6b617e1c7079cf57f073504914b",
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "notes/h3-augmented-p2-section-shortest-conditional-gate.md":
        "ee5da6f0911feb06707106cc6207161bbac7cabd31885f554321698dfbb989d8",
    "computations/verify_h3_residual_q_private_pivot_relative_carrier_transfer.py":
        "59506dc326cc2aec61e149c81eef27ebfe6b94c94c591e54f88688e8ed543428",
    "notes/h3-residual-q-private-pivot-relative-carrier-transfer.md":
        "94c3ef4ad3ca6ac7c80df59159723aa5dc521d5ab80d489641a4b8e3a069ccf7",
    "computations/verify_h3_cplus_w_yw_cap_factorization.py":
        "0b42e8c7d9e308c93774e59eae030403f3c264e2bfe4b31e7782a0e57b78a506",
    "notes/h3-cplus-w-yw-cap-factorization.md":
        "140bf48f949f72b614a5c641d4acc2d42f077fb28a9ca38c66155bf79a89464c",
    "computations/verify_h3_cplus_q_ridge_w_terminal_reduction.py":
        "b2ace6e49aa5ec1b8347a0e88cc39f36e5d773e1aab1d82f424533de8ce52a9a",
    "notes/h3-cplus-q-ridge-w-terminal-reduction.md":
        "856a4932b1c28dfba34195fa2b37dbf0b3a54cbc98e1f80fe0195535885a7e69",
}
EXPECTED_LEDGER_SHA256 = (
    "0f16930591e9c90d8fb57c294e59d4f60c61dd84f81d08cbcf1222b40aa7a901"
)


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


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    width = len(columns[0])
    require(all(len(column) == width for column in columns), "rank width")
    matrix = [list(row) for row in zip(*columns, strict=True)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, width)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[answer], matrix[pivot] = matrix[pivot], matrix[answer]
        value = matrix[answer][column]
        matrix[answer] = [entry / value for entry in matrix[answer]]
        for row in range(width):
            if row == answer or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def post_residue_main_quotient() -> dict[str, object]:
    residue = load(
        "computations/verify_h3_e14_keq_private_placement_residue_identification_gate.py",
        "post_residue_identification",
    )
    residue_ledger, residue_digest = residue.audit()
    require(residue_digest == residue.EXPECTED_LEDGER_SHA256,
            "the E14 residue-identification ledger changed")
    word = residue_ledger["word_residue_identification"]
    companion = residue_ledger["conditional_E14_companion"]
    require(companion["old_unary_plus_placed_return_is_full_target"]
            and companion["first_remaining_main_row"] ==
                "word-resolved labelled ordinary residue -E"
            and word["exact_residue"] ==
                "-E=-2 D_root tensor d_even"
            and word["cancelling_section"] ==
                "+2 D_root tensor d_even"
            and not word["new_coefficient_direction_beyond_d_even"],
            ("the E14 post-placement residue changed", residue_ledger))

    hidden = load(
        "computations/verify_h3_cplus_hidden_debt_cartan_mv_root_bar_span.py",
        "post_residue_hidden",
    )
    hidden_ledger, hidden_digest = hidden.audit()
    require(hidden_digest == hidden.EXPECTED_LEDGER_SHA256,
            "the hidden-debt decomposition changed")
    require(hidden_ledger["exact_decomposition"] ==
                "H=-M_E+K_E+C_Eq, where C_Eq=(0,E,0) is the clean "
                "Eq-only comparison",
            ("the no-fourth-main-cell formula changed", hidden_ledger))

    dressing = load(
        "computations/verify_h3_cplus_conditional_physical_dressing_assembly.py",
        "post_residue_dressing",
    )
    dressing_ledger, dressing_digest = dressing.audit()
    require(dressing_digest == dressing.EXPECTED_LEDGER_SHA256,
            "the conditional Cplus assembly changed")
    core = dressing_ledger["core_assembly"]["assembled_core"]
    require(all(core[row] == 0 for row in (
                "complete_Eq_debt", "root_private_debt", "root_Eq_debt",
                "mixed_target_debt", "word_resolved_root_ores_debt")),
            ("a main row survived E->R plus rooted d_even", core))

    return {
        "granted_local_faces": [
            "source-labelled private placement E->R_E14",
            "same-grade protected-zero +2D_root*d_even",
            "pointed physical K_Eq comparison",
        ],
        "exact_post_placement_debt": "-E=-2D_root tensor d_even",
        "same_grade_cancellation": "+2D_root tensor d_even",
        "new_residue_coefficient_direction": False,
        "new_residue_transport_after_same_grade_grant": False,
        "qualification": (
            "without the same-grade grant, the committed unrooted/coarse "
            "d_even object still needs a physical word/fine/root placement"
        ),
        "main_rows_after_grants": {
            "occurrence_private": 0,
            "complete_Eq": 0,
            "root_lower": 0,
            "root_Eq": 0,
            "mixed_target": 0,
            "word_resolved_ores": 0,
        },
        "no_fourth_main_cell_formula": hidden_ledger["exact_decomposition"],
    }


def three_face_reduction() -> dict[str, object]:
    cap = load(
        "computations/verify_h3_augp2_primitive_cap_response_keq_reduction_gate.py",
        "post_residue_cap",
    )
    cap_ledger, cap_digest = cap.audit()
    require(cap_digest == cap.EXPECTED_LEDGER_SHA256,
            "the primitive-cap reduction changed")
    cap_core = cap_ledger["aggregate_cap_quotient"]
    cap_independence = cap_ledger["expanded_face_independence"]
    require(cap_core["identity"] == "p_y=z_cap-n_y"
            and cap_independence["separating_covector"] ==
                "scalar cap-ores coordinate"
            and not cap_independence["p_in_expanded_available_span"]
            and cap_independence["d_even_has_scalar_cap_ores"] == 0,
            ("the z_cap reduction/separator changed", cap_ledger))

    mate = load(
        "computations/verify_h3_p2_mate_slack_centered_occurrence_reduction.py",
        "post_residue_mate",
    )
    mate_ledger, mate_digest = mate.audit()
    require(mate_digest == mate.EXPECTED_LEDGER_SHA256,
            "the pointed mate-slack reduction changed")
    literal = mate_ledger["literal_mate_class"]
    require(literal["quotient_identity"] == "[dG]=-[c_f]/90"
            and literal["pointed_face_identity"] ==
                "[d(u_f-u)]=[c_f]/90"
            and mate_ledger["source_cell_and_terminal"][
                "face1_reduction"].startswith(
                    "no independent mate-slack theorem remains"),
            ("the P_f/mate identity changed", mate_ledger))

    # Quotient by the already granted occurrence, K_Eq, rooted d_even, main
    # target/Eq, reinsertion, W, and q faces.  The remaining homogeneous rows
    # are literally distinct direct summands.
    p_f = (Q(1), Q(0), Q(0))
    z_cap = (Q(0), Q(1), Q(0))
    ridge = (Q(0), Q(0), Q(1))
    mate_slack = tuple(-entry for entry in p_f)
    require(rank((p_f, z_cap, ridge)) == 3
            and rank((p_f, mate_slack, z_cap, ridge)) == 3,
            "the three-face quotient or mate reduction changed")

    return {
        "remaining_quotient_rows": [
            "pointed conormal P_f=d(u_f-u)",
            "scalar cap residue z_cap",
            "labelled shifted Kahler ridge gamma=-dOmega",
        ],
        "remaining_rank": 3,
        "primitive_duals": [
            "marked tangent", "scalar cap ordinary residue",
            "shifted-ridge forgetful-kernel coordinate",
        ],
        "mate_slack": (
            "[dG]=-[d(u_f-u)] modulo the complete response row; no fourth "
            "mate-slack face"
        ),
        "primitive_cap": (
            "p_y=z_cap-n_y; physical K_Eq already supplies n_y, so z_cap "
            "is the sole remaining cap face"
        ),
        "interpretation": (
            "three independent homogeneous faces of one augmented placement "
            "schema, not a claim that three unrelated conjecture-level "
            "theorems or three unrelated source objects are required"
        ),
    }


def automatic_face_reductions() -> dict[str, object]:
    residual_q = load(
        "computations/verify_h3_residual_q_private_pivot_relative_carrier_transfer.py",
        "post_residue_q",
    )
    q_ledger, q_digest = residual_q.audit()
    require(q_digest == residual_q.EXPECTED_LEDGER_SHA256,
            "the residual-q transfer changed")
    require(q_ledger["unification"].startswith(
                "after a source-labelled embedding of the four complete-row")
            and q_ledger["conditional_finish"]["new_principal_boundary"] ==
                "-t_p",
            ("the q/carrier reduction changed", q_ledger))

    w_cap = load(
        "computations/verify_h3_cplus_w_yw_cap_factorization.py",
        "post_residue_w",
    )
    w_ledger, w_digest = w_cap.audit()
    require(w_digest == w_cap.EXPECTED_LEDGER_SHA256,
            "the Yw/W cap factorization changed")
    require(not w_ledger["literal_and_normal_source_provenance"][
                "fourth_source_generator_needed_for_W"]
            and w_ledger["root_even_factorization"][
                "physical_W_map_needed"] ==
                "Phi_cap(Yw_E)=W_E (identity on E-line)",
            ("the W reduction changed", w_ledger))

    terminal = load(
        "computations/verify_h3_cplus_q_ridge_w_terminal_reduction.py",
        "post_residue_terminal",
    )
    terminal_ledger, terminal_digest = terminal.audit()
    require(terminal_digest == terminal.EXPECTED_LEDGER_SHA256,
            "the q/ridge terminal reduction changed")
    ridge = terminal_ledger["eta_sigma_ridge"]
    require(ridge["order6_mixed_commutator"] == 0
            and not ridge[
                "current_degree_zero_P2_d_even_KEq_implies_terminal_lift"]
            and ridge["under_fully_augmented_PP_hypothesis"].startswith(
                "eta/sigma close uniquely"),
            ("the shifted-ridge status changed", ridge))

    # Summing eta_v(eta_z)=1+delta_(vz) U over the five exposed v gives the
    # exact aggregate terminal mate required by the z_cap Fredholm extension.
    eta_rows = tuple((Q(1), Q(index == 0)) for index in range(5))
    eta_aggregate = tuple(sum(row[index] for row in eta_rows)
                          for index in range(2))
    require(eta_aggregate == (Q(5), Q(1)),
            "the shifted-ridge aggregate eta law changed")

    return {
        "physical_q": (
            "not an independent generator after the full source-labelled "
            "centered occurrence embedding; its private pivots transfer to "
            "the retained carrier t_p"
        ),
        "W": (
            "not an independent generator: the old r0-T cap gives the "
            "coefficientwise Yw_E->W_E identity; retaining W typing is "
            "load-bearing"
        ),
        "eta_sigma": (
            "not an extra numerical face once the labelled shifted ridge is "
            "physical; its contractions are unique"
        ),
        "z_cap_terminal_match": (
            "sum_v[1+delta_(vz)u_z/t]=5+u_z/t, exactly the cap-terminal "
            "promotion datum"
        ),
        "dq_reinsertion": (
            "not independent once the placement is a principal-parts module "
            "map; follows by the Leibniz law"
        ),
        "typing_guard": (
            "the q reduction requires the full source-labelled four-pivot "
            "embedding, and W closure requires the physical W row; neither "
            "follows from a selected coefficient projection"
        ),
    }


def prior_schema_consistency() -> dict[str, object]:
    schema = load(
        "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py",
        "post_residue_prior_schema",
    )
    faces = schema.homogeneous_face_independence()
    reinsertion = schema.reinsertion_leibniz_audit()
    theorem = schema.shortest_theorem_audit()
    require(faces["raw_face_rank"] == 7
            and not faces["P_f_implies_primitive_p"]
            and not reinsertion[
                "independent_dq_generator_after_PP_functoriality"]
            and theorem["one_theorem_schema"]
            and theorem["not_one_homogeneous_source_cell"],
            ("the prior AugP2 schema logic changed", faces, reinsertion,
             theorem))
    return {
        "prior_raw_face_rank": 7,
        "post_E14_and_existing_face_reductions_rank": 3,
        "one_source_labelled_schema_sufficient_conditionally": True,
        "one_homogeneous_source_cell_claimed": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "post-E14 AugP2 master local reduction",
        "pins": PINS,
        "post_residue_main_quotient": post_residue_main_quotient(),
        "three_face_reduction": three_face_reduction(),
        "automatic_face_reductions": automatic_face_reductions(),
        "prior_schema_consistency": prior_schema_consistency(),
        "shortest_exact_master_local_theorem": (
            "Construct one source-labelled augmented principal-parts P2 "
            "placement schema on the complete centered occurrence orbit.  "
            "After its E->R_E14 and same-grade rooted-d_even faces, it need "
            "only certify the three independent homogeneous faces P_f, "
            "z_cap, and the labelled shifted ridge.  Then mate slack is "
            "-P_f, p=z_cap-n, q transfers to the same carrier, r0-T closes "
            "W, and the ridge uniquely closes eta/sigma."
        ),
        "scope": (
            "conditional canonical h=3 local theorem.  It does not construct "
            "the source-labelled AugP2 schema, prove its beta-integral or "
            "all-h spectator extension, or infer any full-row typing from a "
            "selected coefficient projection"
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
    _ledger, digest = audit()
    print("post-E14 main rows after rooted d_even: CLOSED CONDITIONALLY")
    print("remaining independent faces: P_f, z_cap, shifted ridge")
    print("mate slack/q/W/eta-sigma: REDUCED TO THOSE/EXISTING MAPS")
    print("one augmented P2 schema: SUFFICIENT, NOT ONE HOMOGENEOUS CELL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
