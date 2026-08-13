#!/usr/bin/env python3
"""Resolve the formal Gate-II three-cap as a relative, not absolute, Tate cell.

On the nine local response occurrences put

    R01=(A+B+C)H,             L01=(2A-B-C)H.

Adjoining carrier coordinates t_R,t_L and degree-one graph generators

    d Gamma_R=t_R-R01,        d Gamma_L=t_L-L01

is presentation-safe: the new coordinates are monic and eliminate back to
the old occurrence algebra.  Replacing either relative boundary by the
absolute boundary -R01 or -L01 is not presentation-safe.  Modulo the complete
105-term response it imposes a new independent equation.

The corrected Gate-II occurrence dual extends uniquely over these two graph
columns with carrier values (-1,+1).  Its first-PP extension has the same
values and sees only the eighteen endpoint/direction terms of dL01.  At the
downstream P2 graph, a local occurrence detector d extends over every
relative Gamma_i only as the nonzero carrier covector C*d=12*d.  Reinsertion
then forces an occurrence-labelled dq/Q/ores face; the best formal Q
cancellation leaves labelled ores with detector -35/72.

Thus the literal order-two construction exists exactly as a relative graph
totalization.  It does not close Gate II: an absolute three-cap changes H0,
while the relative totalization transfers the obstruction to a physical
landing of its carrier.  The known scalar ordinary-residue row cannot land
the final occurrence-labelled carrier.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py":
        "59babf6e706973f2eaa8a8fdd7cdb624ddf88560c08243c5fcd05c3a5425a5d7",
    "computations/verify_h3_h2_c4_trivial_tag_euler_scalar_face_gate.py":
        "47378f8ce904021bb802e0e4fd59de1591f0cd7333e1fcbc645e62cf40deb499",
    "computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py":
        "d5628f66ffbf94e2de37318ab136adda96af5e114e2bea8dce22542ec9f30cb1",
    "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py":
        "c62ca38edf160f706d7aed237a923737ca46fe7b906fb0bb48bdf400e2ea7854",
    "computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py":
        "4dfb2846c698e5603dadeb1a73add17a7984ccedbad25e3bb09b6aa4170e62ce",
    "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py":
        "20646d25c248a39d27a8be29332d85b7995e9091e106fc1026fe343847df5eed",
    "computations/verify_h3_pointed_occurrence_primitive_cap_p2_propagation_gate.py":
        "a8dfe952ce4fbbaf71ffd4ef748e456d5284dbf6b71655cce6f2f10576db0d06",
    "computations/verify_h3_p2_labelled_ores_cut_even_deven_gauge_gate.py":
        "0a4215db2b91843753cc636b489a81f8e30a8c3de234979c74c9f852d74e3d8a",
}
EXPECTED_LEDGER_SHA256 = (
    "7350f787825d596465b98e018a883446f8557cf738a17d729d217c588ae06511"
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


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
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


def vector(order, values):
    return tuple(Q(values.get(label, 0)) for label in order)


def top_relative_three_cap(curvature, scalar_gate) -> dict[str, object]:
    matchings, directions, tails, l01_values, r01_values, ah_values = (
        curvature.polynomial_data()
    )
    order = tuple(matchings)
    response = (Q(1),) * len(order)
    l01 = vector(order, l01_values)
    r01 = vector(order, r01_values)
    ah = vector(order, ah_values)
    require(len(order) == 105 and len(l01_values) == len(r01_values) == 9
            and l01 == add(scale(3, ah), scale(-1, r01))
            and rank((response, r01, l01)) == 3,
            "the top response/R01/L01 packet changed")

    # The two monic graph columns live in (u_105,t_R,t_L).  They resolve the
    # old occurrence module because t_R=R01(u), t_L=L01(u) eliminate the two
    # new coordinates.  The complete response is retained as a physical row.
    zero_u = (Q(0),) * len(order)
    response_column = response + (Q(0), Q(0))
    gamma_r = scale(-1, r01) + (Q(1), Q(0))
    gamma_l = scale(-1, l01) + (Q(0), Q(1))
    kill_t_r = zero_u + (Q(1), Q(0))
    kill_t_l = zero_u + (Q(0), Q(1))
    require(rank((gamma_r, gamma_l)) == 2
            and rank((gamma_r, gamma_l, response_column)) == 3
            and rank((gamma_r, gamma_l, response_column, kill_t_r)) == 4
            and rank((gamma_r, gamma_l, response_column,
                      kill_t_r, kill_t_l)) == 5,
            "absoluteizing a carrier stopped imposing independent equations")

    # Corrected sparse dual from 4aa11b9, normalized to psi(L01)=1.
    selected_tail = tails[0]
    b_occurrence = tuple(sorted(directions[1] + selected_tail))
    c_occurrence = tuple(sorted(directions[2] + selected_tail))
    outside = next(matching for matching in matchings
                   if matching not in r01_values)
    raw_psi = vector(order, {
        b_occurrence: Q(1), c_occurrence: Q(1), outside: Q(-2),
    })
    psi = scale(Q(-1, 2), raw_psi)
    require(dot(psi, response) == dot(psi, ah) == 0
            and dot(psi, l01) == 1 and dot(psi, r01) == -1,
            "the normalized Gate-II top dual changed")
    relative_psi = psi + (Q(-1), Q(1))
    require(dot(relative_psi, gamma_r) == 0
            and dot(relative_psi, gamma_l) == 0
            and dot(relative_psi, response_column) == 0,
            "the forced relative carrier extension changed")

    scalar_ledger, scalar_digest = scalar_gate.audit()
    countermodel = scalar_ledger["literal_product_rule"][
        "response_row_countermodel"
    ]
    require(scalar_digest == scalar_gate.EXPECTED_LEDGER_SHA256
            and countermodel["response_value"] == "0"
            and countermodel["scalar_face_value"] == "3",
            "the response-row countermodel changed")
    return {
        "occurrence_coordinates": len(order),
        "local_three_cap_occurrences": len(r01_values),
        "top_rows": {
            "complete_response": "R",
            "block": "R01=(A+B+C)H",
            "centered": "L01=(2A-B-C)H",
            "identity": "L01=3AH-R01",
            "rank_R_R01_L01": rank((response, r01, l01)),
        },
        "presentation_safe_relative_graph": {
            "new_coordinates": ["t_R", "t_L"],
            "degree_one_generators": ["Gamma_R", "Gamma_L"],
            "boundaries": ["t_R-R01", "t_L-L01"],
            "graph_rank": rank((gamma_r, gamma_l)),
            "H0": "old occurrence algebra by t_R=R01, t_L=L01",
        },
        "absoluteization_rank_test": {
            "graph_plus_complete_response": 3,
            "after_t_R_zero": 4,
            "after_t_R_and_t_L_zero": 5,
            "consequence": (
                "dGamma_R=-R01 or dGamma_L=-L01 is not a resolution "
                "attachment; it quotients the old response fibre"
            ),
        },
        "response_row_countermodel": countermodel,
        "forced_relative_dual": {
            "normalization": "psi(L01)=1",
            "psi_on_R_AH_R01": [
                str(dot(psi, response)), str(dot(psi, ah)),
                str(dot(psi, r01)),
            ],
            "carrier_values_t_R_t_L": ["-1", "1"],
            "annihilates_both_graph_columns": True,
        },
    }


def first_pp_carrier(curvature) -> dict[str, object]:
    matchings, directions, tails, l01_values, r01_values, ah_values = (
        curvature.polynomial_data()
    )
    response_values = {matching: Q(1) for matching in matchings}
    d_response_values = curvature.differential(response_values)
    d_l01_values = curvature.differential(l01_values)
    d_r01_values = curvature.differential(r01_values)
    d_ah_values = curvature.differential(ah_values)
    order = tuple(d_response_values)
    d_response = vector(order, d_response_values)
    d_l01 = vector(order, d_l01_values)
    d_r01 = vector(order, d_r01_values)
    d_ah = vector(order, d_ah_values)

    selected_tail = tails[0]
    b_occurrence = tuple(sorted(directions[1] + selected_tail))
    c_occurrence = tuple(sorted(directions[2] + selected_tail))
    b_label = (b_occurrence, directions[1][0])
    c_label = (c_occurrence, directions[2][0])
    outside_label = next(label for label in d_response_values
                         if label[0] not in r01_values)
    raw_psi = vector(order, {
        b_label: Q(1), c_label: Q(1), outside_label: Q(-2),
    })
    psi = scale(Q(-1, 2), raw_psi)
    require(dot(psi, d_response) == dot(psi, d_ah) == 0
            and dot(psi, d_l01) == 1 and dot(psi, d_r01) == -1,
            "the normalized first-PP dual changed")

    action_sites = {0, 1, 6, 7}
    tail_half = vector(order, {
        label: value for label, value in d_l01_values.items()
        if set(label[1]).isdisjoint(action_sites)
    })
    direction_half = vector(order, {
        label: value for label, value in d_l01_values.items()
        if set(label[1]).issubset(action_sites)
    })
    require(add(tail_half, direction_half) == d_l01
            and dot(psi, tail_half) == 0
            and dot(psi, direction_half) == 1,
            "the first-PP obstruction stopped living on the direction half")

    gamma_r = scale(-1, d_r01) + (Q(1), Q(0))
    gamma_l = scale(-1, d_l01) + (Q(0), Q(1))
    relative_psi = psi + (Q(-1), Q(1))
    require(dot(relative_psi, gamma_r) == dot(relative_psi, gamma_l) == 0,
            "first-PP naturality changed the carrier signs")
    return {
        "complete_PP_coordinates": len(order),
        "dL01_support": sum(bool(value) for value in d_l01),
        "split": "36=18 residual-tail + 18 endpoint/direction",
        "normalized_dual_values": {
            "dR": str(dot(psi, d_response)),
            "dAH": str(dot(psi, d_ah)),
            "dR01": str(dot(psi, d_r01)),
            "dL01": str(dot(psi, d_l01)),
            "tail_18": str(dot(psi, tail_half)),
            "endpoint_direction_18": str(dot(psi, direction_half)),
        },
        "relative_differentiated_graph": [
            "d(t_R)-dR01", "d(t_L)-dL01",
        ],
        "forced_dual_values_on_dt_R_dt_L": ["-1", "1"],
        "consequence": (
            "Kahler/PP naturality transfers the top carrier to the exact "
            "18-term endpoint-even face; it does not cancel that face"
        ),
    }


def downstream_relative_carrier(relative_graph, private_gate,
                                pointed_gate, ores_gate) -> dict[str, object]:
    graph_ledger, graph_digest = relative_graph.audit()
    private_ledger, private_digest = private_gate.audit()
    pointed_ledger, pointed_digest = pointed_gate.audit()
    ores_ledger, ores_digest = ores_gate.audit()
    require(graph_digest == relative_graph.EXPECTED_LEDGER_SHA256
            and private_digest == private_gate.EXPECTED_LEDGER_SHA256
            and pointed_digest == pointed_gate.EXPECTED_LEDGER_SHA256
            and ores_digest == ores_gate.EXPECTED_LEDGER_SHA256,
            "a downstream pinned ledger changed")
    require(graph_ledger["relative_graph_DGA"]
            ["same_classical_physical_fibre_with_t_retained"]
            and graph_ledger["root_PP_functoriality"]
            ["labelled_cobar_square_generated"],
            "the downstream relative graph stopped being presentation-safe")

    z_private = tuple(map(
        Q, private_ledger["second_even_Bminus4_debt"]["preimage"]
    ))
    size = len(z_private)
    require(size == 12 and sum(z_private, Q(0)) == 0,
            "the P2 private carrier changed")
    one = (Q(1),) * size
    identity = tuple(tuple(Q(row == column) for column in range(size))
                     for row in range(size))
    c_matrix = tuple(tuple(Q(size) * identity[row][column] - 1
                           for column in range(size))
                     for row in range(size))
    detector = tuple(Q(index in (0, 3)) - Q(index in (1, 6))
                     for index in range(size))
    t_dual = tuple(dot(row, detector) for row in c_matrix)
    require(t_dual == scale(size, detector)
            and dot(detector, z_private) == Q(35, 72),
            "the P2 local/carrier dual pair changed")

    # Every Gamma_i has boundary t_i-(Cu)_i.  The extension on t must be C*d.
    for index, row in enumerate(c_matrix):
        gamma_u = scale(-1, row)
        gamma_t = identity[index]
        require(dot(detector, gamma_u) + dot(t_dual, gamma_t) == 0,
                ("a relative Gamma column escaped the carrier dual", index))

    reinsertion = private_ledger["q23_reinsertion"]
    propagation = pointed_ledger["augmented_face_order"]
    require(reinsertion["forced_repair_dq23_private_detector"] == "35/72"
            and propagation["best_case_same_label_p_Q_plus_dq"] == 0
            and propagation["best_case_remaining_labelled_p_ores_detector"]
                == "-35/72"
            and propagation["scalar_ores_on_remaining_labelled_packet"] == 0,
            "the q/Q/ores carrier obstruction changed")
    ores_closure = ores_ledger["conditional_closure"]
    require(not ores_ledger["response_gauge_identity"]
                ["requires_new_labelled_direction"]
            and ores_closure["does_not_construct_hypotheses"],
            "the conditional labelled-ores closure changed")
    return {
        "relative_P2_graph": {
            "boundary": "dGamma_i=t_i-(Cu)_i, C=12I-J",
            "same_old_H0_with_t_retained": True,
            "labelled_root_square": True,
            "q_product_rule": graph_ledger["exact_P2_combination"]
                ["q_reinsertion"],
        },
        "local_detector": "+e0+e3-e1-e6",
        "detector_on_z_private": str(dot(detector, z_private)),
        "forced_carrier_dual": {
            "formula": "C*d=12*d",
            "values": [str(value) for value in t_dual],
            "nonzero": True,
            "annihilates_all_t_i-(Cu)_i_columns": True,
        },
        "dq_Q_ores_ladder": {
            "dq23_detector": reinsertion[
                "forced_repair_dq23_private_detector"
            ],
            "best_formal_labelled_p_Q_cancellation": 0,
            "remaining_labelled_ores_detector": propagation[
                "best_case_remaining_labelled_p_ores_detector"
            ],
            "scalar_ordinary_ores": propagation[
                "scalar_ores_on_remaining_labelled_packet"
            ],
            "consequence": (
                "the existing scalar ordinary-residue row cannot absorb the "
                "forced occurrence-labelled carrier"
            ),
        },
        "conditional_labelled_ores_closure": {
            "hypotheses": ores_closure["hypotheses"],
            "response_gauge_plus_d_even": True,
            "new_labelled_residue_direction_after_hypotheses": False,
            "hypotheses_physically_constructed_here": False,
            "consequence": (
                "ores is a forced proper face of the carrier landing, but "
                "not an additional generator after the occurrence-to-Q/ores "
                "map, mixed-target square, complete gauge and d_even section "
                "have been placed"
            ),
        },
    }


def combined_augmented_signature(augmented_dual) -> dict[str, object]:
    ledger, digest = augmented_dual.audit()
    require(digest == augmented_dual.EXPECTED_LEDGER_SHA256,
            "the Gate-II augmented dual ledger changed")
    signature = ledger["full_known_augmented_dual"]["compact_signature"]
    require(signature["B"] == [1, 1, -1, -1]
            and signature["target"] == [-1, -1, 1, 1]
            and signature["W"] == [-1, -1, 1, 1]
            and signature["ordinary_residue"] == [1, 1, -1, -1]
            and signature["q=M-ainc"] == 0
            and signature["ridge"] == 0,
            "the known augmented Gate-II signature changed")
    return {
        "known_cap_Cartan_rows": signature,
        "new_forced_relative_carrier_rows": {
            "top_t_R_t_L": [-1, 1],
            "first_PP_dt_R_dt_L": [-1, 1],
            "P2_t_dual": "C*d=12*d",
            "q23_reinsertion_labelled_ores_detector": "-35/72",
        },
        "q_and_ridge_before_carrier_landing": [0, 0],
        "interpretation": (
            "target, W and ordinary ores already cancel the old r0/T/rho/K "
            "packet.  The relative Tate graph forces additional carrier "
            "coordinates; the final one is occurrence-labelled and cannot "
            "be represented by the existing scalar ordinary-residue row"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    curvature = load(
        "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py",
        "gate_ii_relative_tate_curvature",
    )
    scalar_gate = load(
        "computations/verify_h3_h2_c4_trivial_tag_euler_scalar_face_gate.py",
        "gate_ii_relative_tate_scalar",
    )
    chain = load(
        "computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py",
        "gate_ii_relative_tate_chain",
    )
    augmented_dual = load(
        "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py",
        "gate_ii_relative_tate_augmented_dual",
    )
    relative_graph = load(
        "computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py",
        "gate_ii_relative_tate_p2_graph",
    )
    private_gate = load(
        "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py",
        "gate_ii_relative_tate_private",
    )
    pointed_gate = load(
        "computations/verify_h3_pointed_occurrence_primitive_cap_p2_propagation_gate.py",
        "gate_ii_relative_tate_pointed",
    )
    ores_gate = load(
        "computations/verify_h3_p2_labelled_ores_cut_even_deven_gauge_gate.py",
        "gate_ii_relative_tate_ores",
    )
    chain_ledger, chain_digest = chain.audit()
    require(chain_digest == chain.EXPECTED_LEDGER_SHA256
            and chain_ledger["downstream_word_0102"]
                ["accepted_terminal_status"].startswith("NO:"),
            "the Gate-II extension-chain frontier changed")

    ledger = {
        "theorem": "h3 Gate-II relative three-cap Tate carrier obstruction",
        "pins": PINS,
        "top_three_cap": top_relative_three_cap(curvature, scalar_gate),
        "first_PP": first_pp_carrier(curvature),
        "augmented_dual_signature":
            combined_augmented_signature(augmented_dual),
        "downstream_P2": downstream_relative_carrier(
            relative_graph, private_gate, pointed_gate, ores_gate
        ),
        "verdict": (
            "The covariant order-two/three-cap construction has an exact "
            "presentation-safe realization, but only as a relative graph "
            "cell with boundaries t_R-R01 and t_L-L01.  Setting the carriers "
            "to zero raises the response-conormal rank and changes H0.  The "
            "Gate-II dual therefore extends over the relative graph only "
            "with nonzero carrier values (-1,+1).  PP naturality transfers "
            "the t_L value to the 18 endpoint/direction terms.  The finite "
            "labelled P2 graph then forces the nonzero carrier covector "
            "C*d=12*d, and q23 reinsertion leaves an occurrence-labelled "
            "ores value -35/72 invisible to scalar ordinary residue.  A "
            "complete-response gauge and d_even cancel it after the physical "
            "occurrence-to-Q/ores map is supplied, but do not construct that "
            "map.  Hence "
            "there is no literal absolute Tate filler in a presentation-"
            "preserving enlargement and no accepted terminal from the "
            "current scalar augmented rows"
        ),
        "sharp_remaining_physical_map": (
            "land the relative carrier orbit (t_R,t_L and the downstream "
            "t_zprivate) in a source-valid same-word/fine/repeated augmented "
            "comparison carrying mixed target, physical q/dq, occurrence-"
            "labelled Q/ores, W and ridge; or extend the forced nonzero "
            "carrier covector over exactly that exhaustive landing"
        ),
        "scope": (
            "exact K8 occurrence and first-PP modules, exact monic relative "
            "graph resolution, and exact h2 P2 labelled reinsertion packet. "
            "The response-row countermodel proves nonconsequence only in "
            "the response quotient, not at a complete hypothetical GHZ "
            "source.  No full physical carrier landing or final terminal is "
            "claimed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Gate-II relative Tate ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("freeze EXPECTED_LEDGER_SHA256=" + digest)
        return
    print("three-cap top: RELATIVE GRAPH t_R-R01, t_L-L01")
    print("absolute Tate attachment: CHANGES H0")
    print("forced top carrier dual (t_R,t_L): (-1,+1)")
    print("first PP carrier: 18 ENDPOINT/DIRECTION TERMS")
    print("P2 carrier dual: C*d=12*d")
    print("q23 best Q cancellation leaves labelled ores: -35/72")
    print("accepted physical terminal: NOT YET; CARRIER LANDING OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
