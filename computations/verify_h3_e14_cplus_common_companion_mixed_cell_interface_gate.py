#!/usr/bin/env python3
"""Audit the minimal E14/C+/cap/Omega mixed-cell proposal.

The calculation deliberately distinguishes three source objects:

* the word-000101 E14 unary/G11 first-hit presentation;
* the order-two lower C+ objects 0112/q23 and 0121/q45; and
* the word-01211222 repeated-P3+K2 cap/common-companion object.

The C+ target normal and the E14 target-unary normal are therefore separate
coordinates until a source-labelled P2/iota map is supplied.  This checker
also records the strongest grant in which that normal map and the pure cap
class are supplied: the exact 22-support E14 covector still separates the
desired mixed column.  In contrast, the Omega/r aggregate has precisely the
eta readout required by the cap-residue terminal equations.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_e14_first_hit_dual_endpoint_q_extension_gate.py":
        "4d25b285b22e8a166a5e005a20e59cec11f463d25840f45a8acc4547d9e649ec",
    "notes/h3-e14-first-hit-dual-endpoint-q-extension-gate.md":
        "e841abbfe5d9da98ff041a448959d56ebb3059121ce080a28c0e8608a76c2605",
    "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py":
        "767aa83dce1daee7e615cbeb5684662714bb0e377822805541172581adc2490f",
    "notes/h2-sigma-even-cartan-spencer-cone-residual.md":
        "5e70446f93f2f7c348c43653cfe05a20033ae292c845e924e02b4afca35b4dcb",
    "computations/verify_h3_augp2_primitive_cap_response_keq_reduction_gate.py":
        "4dabdae7b9060bdb92c0ed32b0016e7e2694750dc176e1857cc9a54cb8176587",
    "notes/h3-augp2-primitive-cap-response-keq-reduction-gate.md":
        "1f8e8a4a5ffc26a8fdcefcb970c3bc35887a1d521ca27ce3173a790b82dfba5d",
    "computations/verify_h3_rootless_clean_c5_omega_r_positive_generator_boundary.py":
        "47183bf5c06c0cf0d7c6c73d82776cddca47375ea02d1f6e8a9942d8540a1320",
    "notes/h3-rootless-clean-c5-omega-r-positive-generator-boundary.md":
        "5e2baad472fc1fdded0d633d07ac0e82b3da62207b197ba818406b5e75965919",
    "computations/verify_h3_e14_companion_cap_residue_eta_mate_separation_gate.py":
        "629b72a0b73cb6f89bc85d823b38e13e6fcae948802614e67b7ed5f6920ff7a2",
    "notes/h3-e14-companion-cap-residue-eta-mate-separation-gate.md":
        "cd518f86bf179323690ca17b926f0bcdc61a9419f757428df33b8d19422396c8",
    "computations/verify_h3_residual_q_private_pivot_relative_carrier_transfer.py":
        "59506dc326cc2aec61e149c81eef27ebfe6b94c94c591e54f88688e8ed543428",
    "notes/h3-residual-q-private-pivot-relative-carrier-transfer.md":
        "94c3ef4ad3ca6ac7c80df59159723aa5dc521d5ab80d489641a4b8e3a069ccf7",
}
EXPECTED_LEDGER_SHA256 = (
    "7a75e6715f270d8a88655e81e4fa3785b663db2c0ddcaa6547927c8c7d1e0c8d"
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


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    width = len(columns[0])
    require(all(len(column) == width for column in columns), "rank width")
    matrix = [list(row) for row in zip(*columns, strict=True)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, width)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(width):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == width:
            break
    return pivot_row


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def audit_inputs() -> dict[str, object]:
    e14 = load(
        "computations/verify_h3_e14_first_hit_dual_endpoint_q_extension_gate.py",
        "mixed_cell_e14",
    )
    e14_ledger, e14_digest = e14.audit()
    require(e14_digest == e14.EXPECTED_LEDGER_SHA256,
            "E14 endpoint/q gate changed")
    first = e14_ledger["exact_first_hit"]
    silent = e14_ledger["tempting_q13_deletion"]
    require(first["word"] == "000101"
            and first["dual_support"] == 22
            and first["dual_on_target"] == "-1"
            and first["dual_on_companion"] == "1"
            and first["dual_on_decorated_core"] == "0",
            ("E14 first-hit data changed", first))
    require(silent["set_all_v13_star_to_zero"][
                "target_unary_readout_support"] == 9
            and silent["set_all_v04_star_and_v13_star_to_zero"][
                "target_unary_readout_support"] == 8,
            "E14 target-normal support changed")

    cplus = load(
        "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py",
        "mixed_cell_cplus",
    )
    cplus_ledger, cplus_digest = cplus.audit()
    require(cplus_digest == cplus.EXPECTED_LEDGER_SHA256,
            "C+ target/Eq cone changed")
    cone = cplus_ledger["minimal_target_Eq_cone"]
    residual = cplus_ledger["actual_augmented_residual"]
    scope = cplus_ledger["Hasse_and_physical_scope"]
    require(cone["target_closed"] and cone["root_reduced_Eq_closed"],
            "formal C+ cone stopped closing target/Eq")
    require(residual["word_residual"]["physical_object_words"] == [
                "0112 with q23:21 reinsertion",
                "0121 with q45:12 reinsertion",
            ], "C+ physical words changed")
    require(scope["literal_value_before_P2"] == "undefined"
            and "P2 map" in scope["reason"],
            ("C+ physical-placement scope changed", scope))

    cap = load(
        "computations/verify_h3_augp2_primitive_cap_response_keq_reduction_gate.py",
        "mixed_cell_cap",
    )
    cap_ledger, cap_digest = cap.audit()
    require(cap_digest == cap.EXPECTED_LEDGER_SHA256,
            "primitive cap reduction changed")
    cap_face = cap_ledger["expanded_face_independence"]
    cap_terminal = cap_ledger["terminal_extension"]
    require(not cap_face["p_in_expanded_available_span"]
            and cap_face["separating_covector"] ==
                "scalar cap-ores coordinate",
            "scalar cap residue stopped being independent")
    require(cap_terminal["first_terminal_promotion_datum"].startswith(
                "a physical rootless/ridge terminal mate"),
            "cap terminal datum changed")

    omega = load(
        "computations/verify_h3_rootless_clean_c5_omega_r_positive_generator_boundary.py",
        "mixed_cell_omega",
    )
    omega.pin_dependencies()
    typed = omega.typed_single_face_lift()
    eta = omega.eta_readout()
    cyclic = omega.cyclic_boundary_module()
    require(typed["strict_readouts_Eq_W_target_ores_ainc"] == [0, 0, 0, 0, 0]
            and typed["fine_degree"] ==
                "same labelled repeated P3+K2 endpoint/chart grade",
            ("Omega/r typing changed", typed))
    require(all(record["aggregate"] ==
                f"5+u_{index}/t"
                for index, record in enumerate(eta["records"], 1)),
            "Omega/r eta aggregate changed")
    require(not cyclic["requested_aggregate_in_image"],
            "Omega/r aggregate unexpectedly became a committed boundary")

    carrier = load(
        "computations/verify_h3_residual_q_private_pivot_relative_carrier_transfer.py",
        "mixed_cell_carrier",
    )
    carrier_ledger, carrier_digest = carrier.audit()
    require(carrier_digest == carrier.EXPECTED_LEDGER_SHA256,
            "residual-q carrier transfer changed")
    graph = carrier_ledger["relative_graph"]
    finish = carrier_ledger["conditional_finish"]
    require(graph["relative_boundary"] == "d Gamma_p=t_p-p"
            and graph["transferred_identity"] ==
                "old cap combination + d Gamma_p = desired KS residue + t_p"
            and finish["new_principal_boundary"] == "-t_p"
            and not finish["landing_constructed_here"],
            ("centered carrier transfer changed", graph, finish))

    return {
        "E14": {
            "word": "000101",
            "old_columns_rank": 269,
            "lambda_support": 22,
            "lambda_on_companion_u05_v13_v24": 1,
            "lambda_on_decorated_core_u05_v24_v34": 0,
            "specialized_target_unary_support": {"q13=0": 9,
                                                  "q04=q13=0": 8},
        },
        "Cplus": {
            "source_objects": residual["word_residual"][
                "physical_object_words"],
            "primitive_normal_support_per_cut": [
                cut["primitive_normal_support"]
                for cut in cone["cut_cones"]],
            "formal_target_Eq_triangle_closed": True,
            "literal_source_value_before_P2": "undefined",
        },
        "cap": {
            "source_object": "01211222 / repeated P3+K2",
            "missing_coordinate": "scalar ordinary residue in cap grade",
            "z_cap_in_current_expanded_image": False,
        },
        "Omega_r": {
            "source_object": "01211222 / repeated P3+K2",
            "strict_Eq_W_target_ores_ainc": [0, 0, 0, 0, 0],
            "five_face_eta_aggregate": "5+u_z/t",
            "common_companion_generator_committed": False,
        },
        "private_carrier_transfer": {
            "private_debt": "p=(1,-1,-1,1), sum(p)=0",
            "universal_graph_boundary": "d Gamma_p=t_p-p",
            "result": "desired KS residue correction + retained t_p",
            "separate_private_pivot_theorem_needed_after_landing": False,
            "physical_t_p_landing_committed": False,
        },
    }


def direct_sum_and_strong_grant_audit() -> dict[str, object]:
    # Before a literal P2/iota, the E14 target-unary normal and the formal C+
    # target normal belong to different source/codomain summands.  We retain
    # both, as well as the exact lambda_E14, cap scalar residue, labelled C+
    # residue, and eta terminal.  Signs on target normals are normalized.
    rows = (
        "lambda_E14 companion",
        "E14 target_unary normal",
        "formal Cplus target normal",
        "scalar cap ores",
        "Cplus labelled ores",
        "eta terminal",
    )
    formal_cplus = (Q(0), Q(0), Q(1), Q(0), Q(1), Q(0))
    z_cap = (Q(0), Q(0), Q(0), Q(1), Q(0), Q(0))
    omega_eta = (Q(0), Q(0), Q(0), Q(0), Q(0), Q(1))
    mixed_required = (Q(1), Q(1), Q(0), Q(1), Q(1), Q(1))
    available = (formal_cplus, z_cap, omega_eta)
    lambda_dual = (Q(1), Q(0), Q(0), Q(0), Q(0), Q(0))
    require(rank(available) == 3
            and rank(available + (mixed_required,)) == 4
            and all(dot(lambda_dual, column) == 0 for column in available)
            and dot(lambda_dual, mixed_required) == 1,
            "direct-sum mixed-cell quotient changed")

    # Make the strongest favorable target-normal grant: identify the formal
    # C+ normal with the exact E14 target-unary normal.  Also grant z_cap and
    # the Omega/r eta column as if both had already been placed in this grade.
    # The exact E14 companion coordinate remains a new rank-one direction.
    identified_rows = (
        "lambda_E14 companion",
        "identified target normal",
        "scalar cap ores",
        "Cplus labelled ores",
        "eta terminal",
    )
    cplus_identified = (Q(0), Q(1), Q(0), Q(1), Q(0))
    zcap_identified = (Q(0), Q(0), Q(1), Q(0), Q(0))
    omega_identified = (Q(0), Q(0), Q(0), Q(0), Q(1))
    mixed_identified = (Q(1), Q(1), Q(1), Q(1), Q(1))
    favorable = (cplus_identified, zcap_identified, omega_identified)
    favorable_dual = (Q(1), Q(0), Q(0), Q(0), Q(0))
    require(rank(favorable) == 3
            and rank(favorable + (mixed_identified,)) == 4
            and all(dot(favorable_dual, column) == 0 for column in favorable)
            and dot(favorable_dual, mixed_identified) == 1,
            "strong-grant E14 companion obstruction changed")

    # Without granting z_cap, C+ plus Omega/r has no scalar cap residue at
    # all.  The cap coordinate is an independent second quotient direction.
    cap_dual = (Q(0), Q(0), Q(1), Q(0), Q(0))
    require(dot(cap_dual, cplus_identified) == 0
            and dot(cap_dual, omega_identified) == 0
            and dot(cap_dual, mixed_identified) == 1,
            "C+/Omega acquired scalar cap residue")

    return {
        "honest_direct_sum": {
            "row_order": list(rows),
            "candidate_rank_after_strong_separate_zcap_grant": 3,
            "rank_after_required_mixed_column": 4,
            "separating_covector": "lambda_E14 extended by zero",
            "reason_target_rows_are_distinct": (
                "no source-labelled P2/iota maps the two order-two lower "
                "objects into the word-000101 E14 first-hit codomain"
            ),
        },
        "after_favorable_target_normal_identification": {
            "row_order": list(identified_rows),
            "candidate_rank": 3,
            "rank_after_required_mixed_column": 4,
            "surviving_primitive_dual": [1, 0, 0, 0, 0],
            "interpretation": (
                "even after granting target-normal placement, pure z_cap, "
                "and the Omega/r eta mate, lambda_E14 still forces a new "
                "literal companion-breaking column"
            ),
        },
        "without_zcap_grant": {
            "Cplus_plus_Omega_scalar_cap_ores": 0,
            "scalar_cap_ores_is_independent_second_dual": True,
        },
    }


def eta_compatibility_audit() -> dict[str, object]:
    # The cap terminal calculation asks for +(5+u_z/t).  The sum of the five
    # facewise common companions has exactly four unit contributions plus the
    # distinguished contribution 1+u_z/t.  Thus eta signs are compatible;
    # source existence and common-grade placement remain separate questions.
    records = []
    for z in range(1, 6):
        facewise = [Q(1) for _ in range(5)]
        # Represent constant and u_z/t coefficients separately.
        constant = sum(facewise, Q(0))
        variable = Q(1)
        require((constant, variable) == (Q(5), Q(1)),
                "eta aggregate coefficient changed")
        records.append({
            "eta": f"eta_{z}",
            "facewise": [f"1+u_{z}/t" if face == z else "1"
                         for face in range(1, 6)],
            "aggregate": f"5+u_{z}/t",
        })
    return {
        "records": records,
        "cap_terminal_required": "+(5+u_z/t)",
        "Omega_r_five_face_aggregate": "+(5+u_z/t)",
        "coefficient_compatibility": True,
        "eta_is_first_incompatibility": False,
        "scope": (
            "conditional on constructing the five same-labelled Omega/r "
            "comparison vertices and placing them in the cap grade"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "E14/Cplus/common-companion mixed-cell interface gate",
        "pins": PINS,
        "exact_inputs": audit_inputs(),
        "quotient_calculation": direct_sum_and_strong_grant_audit(),
        "eta_compatibility": eta_compatibility_audit(),
        "first_failed_square": {
            "map": (
                "iota_target: the 11-support primitive normal on each of "
                "0112/q23 and 0121/q45 -> the exact word-000101 E14 "
                "target_unary residual (support 9, or 8 after q04=q13=0)"
            ),
            "status": "not defined by any committed source-labelled P2 map",
            "consequence": (
                "Cplus cannot presently be evaluated under lambda_E14 or "
                "used as the proper target face of the E14 comparison"
            ),
        },
        "minimal_positive_extension": {
            "one_new_generator": (
                "a source-labelled three-object mapping-cone diagonal joining "
                "word 000101, the two lower Cplus objects, and word 01211222"
            ),
            "normalized_required_readouts": {
                "lambda_E14_on_u05_v13_v24": 1,
                "target_normal": "the exact 9/8-coordinate E14 remainder",
                "scalar_cap_ores": 1,
                "Cplus_labelled_ores": "v=(B1+B4)/2",
                "eta_z": "5+u_z/t",
            },
            "proper_faces": (
                "the Cplus reduced-Eq/hidden lower-residue/Hasse faces and "
                "the cap word/fine/repeated placement must be part of the "
                "same differential"
            ),
            "retained_relative_carrier": (
                "the same cell must land t_p; d Gamma_p=t_p-p then cancels "
                "the centered private debt, so no separate private-pivot "
                "generator is required"
            ),
            "committed": False,
        },
        "verdict": (
            "No source-valid mixed cell is obtained by adding the present "
            "Cplus and Omega/r interfaces.  Eta coefficients agree exactly, "
            "but Cplus is only an output-side target/Eq cone before P2/iota, "
            "the common-companion vertices are themselves unconstructed, "
            "and neither carries scalar cap residue.  Even under the strong "
            "grants identifying target normals and supplying z_cap plus the "
            "eta mate, lambda_E14 remains a primitive rank-one separator.  "
            "The next datum must be one literal companion-breaking, cap-"
            "residue-bearing mapping-cone diagonal, not a coefficient-level "
            "sum of the three separately graded classes.  Its AugP2 face "
            "must land the retained t_p carrier; the universal graph then "
            "removes the residual-q private debt automatically."
        ),
        "scope": (
            "Exact for the pinned canonical E14 first-hit module, the h2 "
            "sigma-even Cplus target/Eq cone, the AugP2 cap quotient, and the "
            "clean-C5 Omega/r interface.  This is a first-interface theorem, "
            "not an all-resolution no-go or a promoted physical terminal."
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("mixed-cell interface ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("Cplus + Omega/r source-valid E14 mixed cell: NOT CONSTRUCTED")
    print("eta aggregate: EXACTLY COMPATIBLE (5+u_z/t)")
    print("first failed square: lower Cplus normal -> E14 target_unary normal")
    print("strong target/zcap/eta grants: lambda_E14 still separates")
    print("next: one companion-breaking cap-bearing mapping-cone diagonal")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
