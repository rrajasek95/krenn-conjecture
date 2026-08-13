#!/usr/bin/env python3
"""Reduce the pure trapped h=3 H2 residual by its three lower face types.

The literal census leaves C2+, C4 and P2 packets.  The strongest committed
order-two results do not leave three unrelated source problems:

* the C2+ target and root-Eq cone is constructed; its remaining word/Hasse
  descent is exactly P2;
* the P2 graph/Koszul resolution and labelled root/reinsertion coherence are
  constructed; its one missing physical datum is the selected centered
  carrier t_zprivate;
* a C4 face has three literal matching occurrences.  A singleton support is
  a restricted coloop, a normalized target-coloop C4 is already closed by
  the punctured-cube theorem, and every occurrence-asymmetric residual is a
  three-occurrence pointed carrier.  The sole symmetric generic residual is
  one tail-covariant four-site relative-C4 placement.

Thus every pure trapped second face either routes, exhibits the exact
occurrence-asymmetric pointed row, or reduces to one strictly smaller
four-site placement.  The latter is not silently identified with P2: its
operation and repeated-edge grade remain distinct.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py":
        "b03c096eb5bc4e6307cafa966f3d66d8c087e78bb8793c8448eec33f51e7e76a",
    "computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py":
        "4dfb2846c698e5603dadeb1a73add17a7984ccedbad25e3bb09b6aa4170e62ce",
    "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py":
        "767aa83dce1daee7e615cbeb5684662714bb0e377822805541172581adc2490f",
    "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py":
        "8ec18f05034b6483512644c49d0009b4b166b0d6b978f6895195321ca9d8417a",
    "computations/verify_h2_labelled_two_direction_occurrence_hasse_cobar_square_gate.py":
        "77d13c31df34efa26b575497bdd7bb2cc9173e8d1907030541444551c7417804",
    "computations/verify_h3_c4_zero_support_rectangle_boundary.py":
        "2f6d1c82d0c41cbe39d46bec36db1e8f28435b69ff074624efb810f19c7e83db",
    "computations/verify_h3_c4_punctured_cube_alternate_target_lift.py":
        "15494dbdcf5d019d6fc858d2bad016a48dc966f63c672e739491a3692842c503",
    "computations/verify_h3_trace_cartan_even_repair_relative_c4_scope_gate.py":
        "645df036367a7fe60f3ce625dc37710f7e83129a84a3619005945ca6b4f0a486",
}
EXPECTED_LEDGER_SHA256 = (
    "8a76afc11afbbead8efdd570debd8f691315866658f6297ae7153ce4e3a532fa"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rank(rows) -> int:
    rows = [list(map(Q, row)) for row in rows]
    if not rows:
        return 0
    answer = 0
    for column in range(len(rows[0])):
        pivot = next((row for row in range(answer, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(len(rows)):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def centered_matrix(size: int):
    return tuple(tuple(Q(size if row == column else 0) - Q(1)
                       for column in range(size))
                 for row in range(size))


def matvec(matrix, vector):
    return tuple(sum((left * right for left, right in
                      zip(row, vector, strict=True)), Q(0))
                 for row in matrix)


def matmul(left, right):
    columns = tuple(zip(*right, strict=True))
    return tuple(tuple(sum((a * b for a, b in zip(row, column, strict=True)),
                           Q(0))
                       for column in columns)
                 for row in left)


def scale(value, vector):
    return tuple(Q(value) * entry for entry in vector)


def add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def centered_occurrence_alternative(size: int, vectors):
    c_matrix = centered_matrix(size)
    require(rank(c_matrix) == size - 1,
            ("centered rank changed", size))
    require(matmul(c_matrix, c_matrix)
            == tuple(scale(size, row) for row in c_matrix),
            ("C^2=N*C changed", size))
    records = []
    for name, raw in vectors.items():
        vector = tuple(map(Q, raw))
        total = sum(vector, Q(0))
        centered = matvec(c_matrix, vector)
        reconstruction = add((total / size,) * size,
                             scale(Q(1, size), centered))
        require(reconstruction == vector, (name, vector, reconstruction))
        nonzero_indices = tuple(index for index, value in enumerate(centered)
                                if value)
        for index in nonzero_indices:
            pointed = tuple(Q(1 if place == index else 0) - Q(1, size)
                            for place in range(size))
            require(sum((a * b for a, b in
                         zip(pointed, vector, strict=True)), Q(0))
                    == centered[index] / size,
                    (name, index, pointed, centered))
        records.append({
            "name": name,
            "values": [str(value) for value in vector],
            "support": sum(value != 0 for value in vector),
            "aggregate": str(total),
            "centered_carrier": [str(value) for value in centered],
            "centered_dark": not nonzero_indices,
            "first_bright_pointed_index": (
                nonzero_indices[0] if nonzero_indices else None
            ),
        })
    return {
        "occurrences": size,
        "centered_operator": f"C={size}I-J",
        "rank": size - 1,
        "identity": f"C^2={size}C",
        "decomposition": "u=(sum(u)/N)*1+(1/N)*Cu",
        "pointed_row": "P_i=e_i^*-(1/N)*1^*, with P_i(u)=(Cu)_i/N",
        "records": records,
    }


def audit_input_classification():
    face = load(
        "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py",
        "pure_h2_face_input",
    )
    ledger, digest = face.audit()
    profiles = ledger["exact_census"]["response_nonzero_pair_profiles"]
    require(digest == face.EXPECTED_LEDGER_SHA256
            and profiles == {
                "QQ_disjoint_pairs_with_three_term_C2plus_tail": 45,
                "D_Q_pairs_with_three_matching_C4_tail": 15,
                "P_S_distinct_pairs_with_three_matching_C4_tail": 30,
                "P_Q_disjoint_pairs_with_three_term_P2_tail": 60,
                "S_Q_disjoint_pairs_with_three_term_P2_tail": 60,
            }, (digest, profiles))
    return {
        "pinned_face_ledger": digest,
        "pure_trapped_types": ["C2plus", "C4", "P2"],
        "no_fourth_compatible_pair_type": True,
    }


def audit_p2_and_c2plus_descent():
    p2 = load(
        "computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py",
        "pure_h2_p2_graph",
    )
    p2_ledger, p2_digest = p2.audit()
    require(p2_digest == p2.EXPECTED_LEDGER_SHA256
            and p2_ledger["relative_graph_DGA"]
            ["same_classical_physical_fibre_with_t_retained"]
            and p2_ledger["root_PP_functoriality"]
            ["labelled_cobar_square_generated"]
            and p2_ledger["remaining_carrier_landing"]
            ["endpoint_even_private_carrier_rank"] == 5,
            p2_ledger)

    indices = p2_ledger["exact_P2_combination"]["Gamma_indices"]
    coefficients = tuple(Q(value) for value in
                         p2_ledger["exact_P2_combination"]
                         ["Gamma_coefficients"])
    gamma_coefficients = [Q(0)] * 12
    for index, coefficient in zip(indices, coefficients, strict=True):
        gamma_coefficients[index] = coefficient
    c12 = centered_matrix(12)
    z_private = [
        sum((gamma_coefficients[index] * c12[index][column]
             for index in range(12)), Q(0))
        for column in range(12)
    ]
    require(sum(z_private, Q(0)) == 0, z_private)
    centered = centered_occurrence_alternative(
        12, {"exact_P2_z_private": tuple(z_private)}
    )
    p2_record = centered["records"][0]
    require(not p2_record["centered_dark"], p2_record)

    sigma = load(
        "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py",
        "pure_h2_sigma_cone",
    )
    sigma_ledger, sigma_digest = sigma.audit()
    cone = sigma_ledger["minimal_target_Eq_cone"]
    hasse = sigma_ledger["Hasse_and_physical_scope"]
    require(sigma_digest == sigma.EXPECTED_LEDGER_SHA256
            and cone["target_closed"] and cone["root_reduced_Eq_closed"]
            and hasse["literal_value_before_P2"] == "undefined",
            sigma_ledger)

    return {
        "P2_relative_graph": {
            "ledger": p2_digest,
            "physical_occurrences": 12,
            "relative_boundary": p2_ledger["exact_P2_combination"]["boundary"],
            "labelled_root_square": True,
            "q_reinsertion_face_retained": True,
            "endpoint_even_carrier_rank": 5,
            "selected_line": "t_zprivate",
            "selected_line_is_nonzero": True,
            "physical_landing_status": "OPEN",
        },
        "exact_selected_centered_decomposition": centered,
        "C2plus_composition": {
            "ledger": sigma_digest,
            "mixed_target": "CLOSED",
            "root_reduced_Eq": "CLOSED",
            "remaining_word_Hasse_descent": "the same source-labelled P2 orbit",
            "independent_new_target_generator": False,
            "fixed_extra_augmented_faces": [
                "complete Eq -delta_plus", "labelled residue v",
                "two sigma-related lower words", "root-word lower/ores dressing",
            ],
        },
        "conclusion": (
            "C2plus and P2 reduce to one selected occurrence-asymmetric "
            "carrier line t_zprivate; all source-side graph, root-square and "
            "reinsertion coherence is constructed, while its physical "
            "augmented landing is the missing P_f-type comparison"
        ),
    }


def audit_c4_descent():
    centered = centered_occurrence_alternative(3, {
        "singleton_matching": (1, 0, 0),
        "two_matching_face": (1, 1, 0),
        "full_flat_symmetric": (1, 1, 1),
        "full_occurrence_asymmetric": (1, 2, 1),
    })
    records = {record["name"]: record for record in centered["records"]}
    require(records["singleton_matching"]["support"] == 1
            and not records["singleton_matching"]["centered_dark"]
            and not records["two_matching_face"]["centered_dark"]
            and records["full_flat_symmetric"]["centered_dark"]
            and not records["full_occurrence_asymmetric"]["centered_dark"],
            records)

    punctured = load(
        "computations/verify_h3_c4_punctured_cube_alternate_target_lift.py",
        "pure_h2_punctured_c4",
    )
    word_audit = punctured.audit_words_and_routes()
    cube_audit = punctured.audit_cube_identity()
    unit_audit = punctured.audit_unit_propagation()
    require(word_audit and cube_audit and unit_audit,
            (word_audit, cube_audit, unit_audit))

    c4scope = load(
        "computations/verify_h3_trace_cartan_even_repair_relative_c4_scope_gate.py",
        "pure_h2_relative_c4_scope",
    )
    scope_ledger, scope_digest = c4scope.audit()
    require(scope_digest == c4scope.EXPECTED_LEDGER_SHA256
            and scope_ledger["tau_plus_local_C4_census"]
            ["direct_targets_B1_or_B4"] is False
            and not scope_ledger["tau_plus_local_C4_census"]
            ["same_source_grade"], scope_ledger)

    return {
        "three_matching_centered_alternative": centered,
        "literal_support_split": {
            "one_matching": (
                "both base q edges are coloops of the restricted four-site "
                "matching support; this is the smaller coloop arm"
            ),
            "two_or_three_unequal_values": (
                "Cu is nonzero and some explicit P_i=e_i^*-1/3 detects the "
                "occurrence-asymmetric C4 face"
            ),
            "three_equal_nonzero_values": (
                "Cu=0; only the aggregate flat C4 packet remains"
            ),
        },
        "strongest_physical_closure": {
            "normalized_target_coloop_packet": "CLOSED by punctured C4 cube",
            "landing": "alternate pure target reselection or offanchor active exit",
            "scope": "requires the normalized endpoint/common-tail packet",
        },
        "generic_flat_internal_residual": {
            "ledger": scope_digest,
            "strictly_smaller_domain": "four residual sites and three matchings",
            "missing_cell": (
                "one tail-covariant same-grade protected relative-C4 "
                "restriction/insertion primitive"
            ),
            "why_not_P2_by_relabeling": (
                "operation type and repeated-edge grade differ; coefficient "
                "translation and canonical symmetry do not transport them"
            ),
        },
        "conclusion": (
            "the generic C4 arm either gives a restricted coloop, an explicit "
            "three-occurrence P_f-type row, the already closed normalized "
            "punctured packet, or one strictly smaller literal relative-C4 "
            "placement; there is no further six-site H2 topology"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h3 pure trapped H2 C2plus/C4/P2 finite descent reduction",
        "pins": PINS,
        "input": audit_input_classification(),
        "C2plus_and_P2": audit_p2_and_c2plus_descent(),
        "C4": audit_c4_descent(),
        "finite_alternative": [
            "occurrence-asymmetric pointed row P_i is nonzero",
            "restricted pure matching support has a literal coloop",
            "normalized target-coloop C4 routes by punctured-cube reselection",
            "one four-site tail-covariant relative-C4 placement remains",
        ],
        "verdict": (
            "The pure trapped H2 residual is now a finite physical descent, "
            "not three open lower theories.  C2plus has no remaining target/"
            "root-Eq problem and reduces to the P2 word/Hasse descent.  P2's "
            "graph resolution, labelled square and reinsertion are explicit; "
            "only the selected centered carrier t_zprivate needs a physical "
            "augmented P_f-type landing.  For C4, every nonconstant "
            "coefficient profile exposes an explicit centered "
            "three-occurrence row, singleton support is a restricted coloop, "
            "and the normalized packet is closed.  The sole generic symmetric "
            "remainder is one four-site tail-covariant relative-C4 placement."
        ),
        "scope": (
            "canonical h=3 pure trapped second faces and their committed h2/"
            "four-site placements; the relative-C4 remainder is not declared "
            "equal to P2 across its different operation/repeated grade"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("C2plus target/root-Eq -> P2 descent: REDUCED")
    print("P2 relative graph/root/reinsertion -> t_zprivate: CONSTRUCTED")
    print("physical t_zprivate P_f-type landing: OPEN")
    print("C4 -> pointed row / coloop / normalized closure / ONE 4-SITE CELL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
