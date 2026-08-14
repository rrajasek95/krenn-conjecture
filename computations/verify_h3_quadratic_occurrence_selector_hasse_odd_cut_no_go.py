#!/usr/bin/env python3
"""Refute a lift of Q_(0,1) X_23=e_f by the current Hasse inventory.

The quadratic feature identity is exact on the 90 direct-free response
occurrences.  A physical squarefree lift must nevertheless retain all four
edge faces of f=P0|S1|23|45.  Restriction along either marked tail edge has
an order-two endpoint-role-odd component

    45 * (e_f - e_(tau f)).

Every currently available lower complete/q/Cartan row is endpoint-role
even, and the constant theta transport has zero odd boundary.  This checker
grants the entire endpoint-even subspace, as well as arbitrary protected
external rows, and constructs an integral odd dual.
It also grants two new odd fillers and verifies that the independent
360-flag selected-db01 rank jump remains 181 -> 182 (183 -> 184 after the
two direct-sum grants).  Thus the coefficient identity does not define a
single source-valid Hasse column in the current complex.
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
    "computations/verify_h3_direct_free_feature_selector_index_gate.py":
        "46102bc139de2754e5d1b6775a2731ae26d70f250f533b34f3bbc4f69241df08",
    "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py":
        "cb328adc1f23b38f6f9f9305635ddbaef888178633f8db91c205fdfbdca1ff34",
    "computations/verify_h3_order2_promoted_occurrence_orientation_gate.py":
        "c0a34736979eb8a5d059dce30224b3d22f3930e9afaf07916dbbf51b3539c15d",
    "computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py":
        "a08598e088c100e4b5116fb2b39717ec639116ea1fa7575062ba9a8f8cf9c683",
    "computations/verify_h3_pointed_occurrence_edge_euler_boolean_cube_gate.py":
        "2b720f2a81d047454e224ec6af7ad62680c6ffeae33b6d7275cf995789bc8b8c",
}
EXPECTED_LEDGER_SHA256 = "99a3365c86b8e421a80503209a664ef1857af86c6ded183d399a93e2ada535ed"

CUTS = ((2, 3), (4, 5))
PROTECTED = (
    "target", "private B", "reduced Eq", "M", "ainc", "q=M-ainc",
    "W", "pointed P_f", "labelled ordinary residue", "ridge",
    "eta", "sigma",
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


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((vector[index] for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(value: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(value) * entry for entry in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[tuple[Q, ...], ...] | list[tuple[Q, ...]]) -> int:
    if not columns:
        return 0
    require(len({len(column) for column in columns}) == 1, "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(len(columns[0]))]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        pivot_value = rows[answer][column]
        rows[answer] = [value / pivot_value for value in rows[answer]]
        for row in range(len(rows)):
            if row == answer or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [left - multiple * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def unit(width: int, position: int) -> tuple[Q, ...]:
    return tuple(Q(index == position) for index in range(width))


def selector_and_face_audit(selector, euler) -> dict[str, object]:
    selector_ledger, selector_digest = selector.audit()
    require(selector_digest == selector.EXPECTED_DIGEST,
            "quadratic selector ledger changed")
    euler_ledger, euler_digest = euler.audit()
    require(euler_digest == euler.EXPECTED_LEDGER_SHA256,
            "Euler face ledger changed")
    face_data = euler_ledger["word_fine_q_anchor_faces"]["q_and_PP"]
    faces = face_data["four_first_labelled_faces"]
    require(selector_ledger["pointed_feature_identity"] ==
                "Q_(0,1)*X_23=Q_(0,1)*X_45=e_f"
            and selector_ledger["support_counts"] ==
                {"Q_01": 3, "X_23": 12, "X_45": 12, "pointed": 1}
            and faces == [
                "d(P0): S1|23|45", "d(S1): P0|23|45",
                "d(q23): P0|S1|45", "d(q45): P0|S1|23",
            ],
            (selector_ledger, faces))
    return {
        "coefficient_identity": selector_ledger["pointed_feature_identity"],
        "supports_Q_X23_X45_pointed": [3, 12, 12, 1],
        "physical_top": "P0^11|S1^11|q23^00|q45^00",
        "response_word": "11110000 = 11:110000",
        "mandatory_first_faces": faces,
        "label_loss": (
            "using X23 instead of X45 shortens only the coefficient formula; "
            "the selected squarefree top contains both edges, so both tail "
            "restriction/reinsertion faces remain in its physical boundary"
        ),
        "selected_db01_terms": face_data["selected_db01_terms"],
    }


def endpoint_transpose(occurrence):
    p_site, s_site, matching = occurrence
    return s_site, p_site, matching


def marked_cut_record(restriction, cut: tuple[int, int]) -> dict[str, object]:
    vertices = tuple(range(6))
    source = restriction.occurrences(vertices)
    marked = (0, 1, ((2, 3), (4, 5)))
    require(marked in source and len(source) == 90, "marked h3 occurrence")
    lower_vertices = tuple(site for site in vertices if site not in cut)
    lower = restriction.occurrences(lower_vertices)
    require(len(lower) == 12, (cut, len(lower)))
    marked_lower = restriction.restrict_occurrence(marked, cut)
    require(marked_lower in lower, (cut, marked_lower))
    transposed = endpoint_transpose(marked_lower)
    require(transposed in lower and transposed != marked_lower,
            (cut, marked_lower, transposed))

    marked_index = lower.index(marked_lower)
    transposed_index = lower.index(transposed)
    one = tuple(Q(1) for _ in lower)
    e_marked = unit(len(lower), marked_index)
    e_transposed = unit(len(lower), transposed_index)
    pair = add(e_marked, e_transposed)
    primitive_odd = add(e_marked, scale(Q(-1), e_transposed))
    lower_centered = add(scale(Q(12), e_marked), scale(Q(-1), one))
    even = add(scale(Q(6), pair), scale(Q(-1), one))
    odd = scale(Q(6), primitive_odd)
    raw_restriction = add(scale(Q(90), e_marked), scale(Q(-1), one))
    require(lower_centered == add(even, odd)
            and raw_restriction == add(
                scale(Q(15, 2), lower_centered), scale(Q(13, 2), one))
            and raw_restriction == add(
                scale(Q(15, 2), even),
                scale(Q(45), primitive_odd),
                scale(Q(13, 2), one)),
            (cut, raw_restriction))

    # Grant the entire endpoint-role-even subspace, not only the presently
    # named complete/q/Cartan rows.  Tau acts freely on the twelve lower
    # occurrences, so its even subspace has dimension six.
    index = {item: position for position, item in enumerate(lower)}
    representatives = []
    seen = set()
    for occurrence in lower:
        if occurrence in seen:
            continue
        mate = endpoint_transpose(occurrence)
        seen.update((occurrence, mate))
        representatives.append(add(
            unit(len(lower), index[occurrence]),
            unit(len(lower), index[mate]),
        ))
    require(len(representatives) == 6
            and rank(representatives) == 6
            and rank(representatives + [raw_restriction]) == 7
            and all(dot(primitive_odd, vector) == 0
                    for vector in representatives)
            and dot(primitive_odd, raw_restriction) == 90,
            (cut, rank(representatives),
             rank(representatives + [raw_restriction])))

    remaining_edge = next(edge for edge in ((2, 3), (4, 5)) if edge != cut)
    return {
        "deleted_tail_edge": "q" + "".join(map(str, cut)) + ":00",
        "marked_lower_occurrence": repr(marked_lower),
        "endpoint_transposed_occurrence": repr(transposed),
        "remaining_tail_edge":
            "q" + "".join(map(str, remaining_edge)) + ":00",
        "lower_occurrences": len(lower),
        "endpoint_role_pairs": len(representatives),
        "restriction_formula":
            "D_e c_f=(15/2)c_lower+(13/2)1",
        "lower_parity_formula":
            "c_lower=[6(e_f+e_tau)-1]+6(e_f-e_tau)",
        "forced_odd_component": "45*(e_f-e_tau)",
        "maximally_granted_even_rank": rank(representatives),
        "rank_after_required_restriction":
            rank(representatives + [raw_restriction]),
        "primitive_odd_dual": "e_f^*-e_tau^*",
        "dual_on_every_endpoint_even_row": 0,
        "dual_on_required_restriction": 90,
        "even_basis": representatives,
        "required_vector": raw_restriction,
        "odd_dual_vector": primitive_odd,
    }


def two_cut_and_protected_countermodel(restriction, orientation) \
        -> dict[str, object]:
    restriction_ledger = restriction.component_audit(3)
    parity = orientation.parity_decomposition_audit()
    commuting = orientation.commuting_operator_audit()
    source_scope = orientation.source_and_terminal_scope_audit()
    require(restriction_ledger["marked_residual_cuts"] == [
                {"edge": [2, 3], "lower_centered_coefficient": "15/2",
                 "constant_coefficient": "13/2",
                 "primitive_difference_dual_value": "90"},
                {"edge": [4, 5], "lower_centered_coefficient": "15/2",
                 "constant_coefficient": "13/2",
                 "primitive_difference_dual_value": "90"},
            ]
            and parity["primitive_orientation"] == "o_f=e_f-e_tau_f"
            and commuting["Cartan_KS_parity_law"] == "[H_root,tau]=0"
            and not source_scope["theta_boundary_of_orientation"]
            and not source_scope["physical_even_projector_lift_constructed"],
            (restriction_ledger, parity, commuting, source_scope))

    records = [marked_cut_record(restriction, cut) for cut in CUTS]
    block = 12
    even_columns = []
    for cut_index, record in enumerate(records):
        for vector in record.pop("even_basis"):
            even_columns.append(
                (tuple(Q(0) for _ in range(cut_index * block)) + vector
                 + tuple(Q(0) for _ in range((1 - cut_index) * block)))
            )
    required = []
    duals = []
    for cut_index, record in enumerate(records):
        vector = record.pop("required_vector")
        dual = record.pop("odd_dual_vector")
        required.append(
            tuple(Q(0) for _ in range(cut_index * block)) + vector
            + tuple(Q(0) for _ in range((1 - cut_index) * block))
        )
        duals.append(
            tuple(Q(0) for _ in range(cut_index * block)) + dual
            + tuple(Q(0) for _ in range((1 - cut_index) * block))
        )
    require(rank(even_columns) == 12
            and rank(even_columns + [required[0]]) == 13
            and rank(even_columns + required) == 14,
            "two-cut even rank changed")
    signed_ranks = {}
    for sign in (-1, 1):
        combined = add(required[0], scale(Q(sign), required[1]))
        require(rank(even_columns + [combined]) == 13
                and dot(duals[0], combined) == 90
                and dot(duals[1], combined) == 90 * sign,
                (sign, rank(even_columns + [combined])))
        signed_ranks[str(sign)] = rank(even_columns + [combined])

    # Grant arbitrary unit columns on every protected external row.  These
    # can cancel any desired target/q/residue/ridge value, but their lower
    # odd projection is zero, so the obstruction remains.
    extended_width = 24 + len(PROTECTED)
    even_extended = [column + tuple(Q(0) for _ in PROTECTED)
                     for column in even_columns]
    protected_units = [unit(extended_width, 24 + index)
                       for index in range(len(PROTECTED))]
    required_extended = required[0] + tuple(Q(0) for _ in PROTECTED)
    dual_extended = duals[0] + tuple(Q(0) for _ in PROTECTED)
    old_extended = even_extended + protected_units
    require(rank(old_extended) == 12 + len(PROTECTED)
            and rank(old_extended + [required_extended]) ==
                13 + len(PROTECTED)
            and all(dot(dual_extended, column) == 0
                    for column in old_extended)
            and dot(dual_extended, required_extended) == 90,
            "protected-row grant killed the odd obstruction")
    return {
        "cut_records": records,
        "maximal_two_cut_even_rank": 12,
        "rank_after_one_labelled_cut": 13,
        "rank_after_both_labelled_cuts": 14,
        "rank_after_combined_top_boundary_for_either_sign": signed_ranks,
        "protected_rows_granted_arbitrarily": list(PROTECTED),
        "protected_grant_rank_before_after_one_cut":
            [12 + len(PROTECTED), 13 + len(PROTECTED)],
        "first_algebraic_obstruction": (
            "one endpoint-role-odd order-two occurrence class on either "
            "marked tail restriction; the two cuts are separate labelled "
            "instances of one type"
        ),
        "why_current_operations_are_killed": (
            "complete lower rows and residual-q selectors are tau-even, "
            "site/root Cartan commutes with endpoint-role transposition, "
            "and the available constant theta transport has zero boundary "
            "on the odd orientation class"
        ),
    }


def db01_guard_after_odd_grant(active) -> dict[str, object]:
    active_ledger, active_digest = active.audit()
    require(active_digest == active.EXPECTED_LEDGER_SHA256,
            "selected-db01 guard changed")
    guard = active_ledger["maximal_termwise_full_label_counterguard"]
    require(guard["rank_before_after_selected_db01"] == [181, 182]
            and guard["response_flags"] == 180
            and guard["granted_monic_termwise_reinsertion_graphs"] == 180,
            guard)

    # Rebuild the exact 360-flag module and add two completely free lower
    # odd fillers in separate coordinates.  Projection to the flag block
    # still has the old centered obstruction.
    block = 180
    flag_width = 2 * block
    width = flag_width + 2
    response_complete = tuple(Q(index < block) for index in range(flag_width))
    target_complete = tuple(Q(index >= block) for index in range(flag_width))
    graphs = []
    for index in range(block):
        vector = [Q(0) for _ in range(flag_width)]
        vector[index] = Q(-1)
        vector[block + index] = Q(1)
        graphs.append(tuple(vector))
    selected = tuple(Q(index < 6) for index in range(flag_width))
    centered = tuple(Q(29 if index % block < 6 else -1)
                     for index in range(flag_width))
    old = [column + (Q(0), Q(0)) for column in graphs]
    old += [response_complete + (Q(0), Q(0)),
            target_complete + (Q(0), Q(0)),
            unit(width, flag_width), unit(width, flag_width + 1)]
    selected_extended = selected + (Q(0), Q(0))
    centered_extended = centered + (Q(0), Q(0))
    require(rank(old) == 183
            and rank(old + [selected_extended]) == 184
            and all(dot(centered_extended, column) == 0 for column in old)
            and dot(centered_extended, selected_extended) == 174,
            "odd grants changed the 360-flag guard")
    return {
        "original_flag_rank_before_after_db01": [181, 182],
        "granted_lower_odd_fillers": 2,
        "direct_sum_rank_before_after_db01": [183, 184],
        "centered_flag_dual_on_old_plus_odd_fillers": 0,
        "centered_flag_dual_on_selected_db01": 174,
        "conclusion": (
            "even after the first odd-cut obstruction is granted twice, "
            "the selected six-term endpoint-fibre PP carrier remains a "
            "second independent required projection of the top Hasse cell"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    selector = load(
        "computations/verify_h3_direct_free_feature_selector_index_gate.py",
        "quadratic_lift_selector",
    )
    restriction = load(
        "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py",
        "quadratic_lift_restriction",
    )
    orientation = load(
        "computations/verify_h3_order2_promoted_occurrence_orientation_gate.py",
        "quadratic_lift_orientation",
    )
    active = load(
        "computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py",
        "quadratic_lift_db01_guard",
    )
    euler = load(
        "computations/verify_h3_pointed_occurrence_edge_euler_boolean_cube_gate.py",
        "quadratic_lift_euler",
    )
    ledger = {
        "theorem": "h3 quadratic occurrence-selector Hasse odd-cut no-go",
        "pins": PINS,
        "quadratic_coefficient_top_and_physical_faces":
            selector_and_face_audit(selector, euler),
        "first_restriction_obstruction":
            two_cut_and_protected_countermodel(restriction, orientation),
        "second_selected_db01_projection":
            db01_guard_after_odd_grant(active),
        "minimal_new_source_packet": {
            "lower_generator_type": (
                "one p/s-odd order-two occurrence cell W_odd, instantiated "
                "on cuts q23 and q45 and related by (2 5)(3 4)"
            ),
            "top_generator_type": (
                "one pointed quadratic Hasse cell with coefficient top "
                "Q_(0,1)X_23=e_f"
            ),
            "top_mandatory_boundary": [
                "scalar/target correction -90*f(x)",
                "endpoint faces d(P0), d(S1)",
                "both labelled tail faces d(q23), d(q45)",
                "selected six-term db01 projection after matching spread",
                "word 11110000 and all occurrence/fine/reinsertion labels",
                "target, B/Eq, M, ainc/q, W, P_f, labelled residue, ridge, eta, sigma",
            ],
            "status": "not present in the current source inventory",
        },
        "verdict": (
            "The identity Q_(0,1)X_23=Q_(0,1)X_45=e_f is an exact "
            "coefficient selector, but it has no lift through the currently "
            "implemented restriction/reinsertion/Hasse operations.  Either "
            "marked tail restriction of c_f contains the forced class "
            "45(e_f-e_tau_f).  Granting the entire endpoint-even lower "
            "source and arbitrary protected external rows leaves an exact "
            "odd dual of value 90.  The two cut labels require two "
            "instances of one new lower odd generator type.  Even after "
            "granting them, the independent 360-flag selected-db01 guard "
            "retains its rank jump.  Therefore a source-valid construction "
            "requires a new two-stage nonlinear Hasse packet, not a "
            "composition of the existing coefficient correspondences."
        ),
        "scope": (
            "exact canonical h=3 rational countermodel for the named actual "
            "restriction/reinsertion, endpoint-even lower Hasse/Cartan, and "
            "complete 360-flag rows.  It does not prove that the displayed "
            "new odd-plus-top Hasse packet cannot exist in a larger physical "
            "source resolution, nor promote the odd dual to a global terminal"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "selector", "odd", "flags"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    require(digest == EXPECTED_LEDGER_SHA256,
            ("quadratic occurrence-selector ledger changed", digest))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h3 quadratic occurrence-selector Hasse ({arguments.mode}): PASS")
        print("coefficient Q_01*X_23=e_f: EXACT")
        print("marked-cut odd face: 45*(e_f-e_tau); dual value 90")
        print("maximal lower even rank: 12 -> 14 after two labelled cuts")
        print("after granting both odd fillers, db01 flag rank: 183 -> 184")
        print("physical quadratic Hasse lift from current operations: NO")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
