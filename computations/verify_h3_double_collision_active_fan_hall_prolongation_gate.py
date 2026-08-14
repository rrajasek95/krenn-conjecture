#!/usr/bin/env python3
"""Test the P4+K2/4K2 db01 debts against active-fan/Hall recurrence.

The ordinary complete-row recurrence is strong on coefficient support, but
it does not prolong automatically to the endpoint-oriented first-jet block
created by p0*s1*q01*H2345.  A literal trapped tangent satisfies the active
coloop target row, the complete B+C response row, and both differentials.
Its pure q support is the single matching 01|23|45, so the relevant tail
shore {23,45} is closed and every supported q edge is a coloop.

The final finite guard grants, for each of the nine faces and both endpoint
orientations, its own Hall/coloop exit graph and even an absolute complete
pair at both ends.  The endpoint-odd class still survives.  Killing it
requires an orientation-asymmetric double-collision jet/prolongation row,
not the current support recurrence.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py":
        "a08598e088c100e4b5116fb2b39717ec639116ea1fa7575062ba9a8f8cf9c683",
    "notes/h3-selected-db01-active-coloop-reinsertion-gate.md":
        "2df84ea4a86f135f99476ed8b7ab9e9e5e5a78cf492ef3c495ef2a438c2e5418",
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "notes/h3-active-fan-coloop-complete-row-pivot.md":
        "2a68b7a9da9c61c67c4f63e666a6cbb1023344722943b9042f2ff15b2863e92e",
    "computations/verify_h3_active_coloop_forced_mate_recurrence_potential_boundary.py":
        "f08e9bc7e7a2a6d561426890c60120b96b37334fb54337d06845fe78d3ffe984",
    "notes/h3-active-coloop-forced-mate-recurrence-potential-boundary.md":
        "3a6823f8b5e8d555883ecbb188137a8d6ec54351d54292ccd06ede3035c4f3aa",
    "computations/verify_h3_active_coloop_closed_shore_complete_row_response_gate.py":
        "fe60edcc44c33e660b50f7e8d627b506c5bd81c1d97f15e66b9e8a35e9f3c4ad",
    "notes/h3-active-coloop-closed-shore-complete-row-response-gate.md":
        "1470ffc55dff20f0919b4be884ca8d54efe7a15e90117d1610aef067c82b44b2",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "notes/h3-active-fan-coloop-or-four-good.md":
        "9be8996264fa2070a8f5d7f725f3fcb154b6ee2df2b3e5d3ccd4a6412ec5b03a",
}
EXPECTED_LEDGER_SHA256 = "cd768a1041dec8bbe13d58e53cc56269bdba0f32ac3a8b2e85fd2f26128afc32"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def edge(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def transversal(family: frozenset[tuple[int, int]]) -> frozenset[tuple[int, int]]:
    all_edges = tuple(combinations(range(6), 2))
    return frozenset(candidate for candidate in all_edges
                     if all(set(candidate) & set(member) for member in family))


def trapped_complete_row_tangent_audit() -> dict[str, object]:
    # The only nonzero residual q cells in this local chart are the matching
    # 01|23|45.  The endpoint orientations have opposite coefficients.
    q = {edge(left, right): Q(0)
         for left, right in combinations(range(6), 2)}
    q[(0, 1)] = q[(2, 3)] = q[(4, 5)] = Q(1)
    dq = {physical: Q(0) for physical in q}
    dq[(0, 1)] = Q(-1)
    dq[(2, 3)] = Q(1)

    h = (q[(2, 3)] * q[(4, 5)]
         + q[(2, 4)] * q[(3, 5)]
         + q[(2, 5)] * q[(3, 4)])
    dh = (dq[(2, 3)] * q[(4, 5)] + q[(2, 3)] * dq[(4, 5)]
          + dq[(2, 4)] * q[(3, 5)] + q[(2, 4)] * dq[(3, 5)]
          + dq[(2, 5)] * q[(3, 4)] + q[(2, 5)] * dq[(3, 4)])
    q01, dq01 = q[(0, 1)], dq[(0, 1)]

    p0, s1, p1, s0 = Q(1), Q(1), Q(1), Q(-1)
    b01 = p0 * s1 * h
    b10 = p1 * s0 * h
    db01 = p0 * s1 * dh
    db10 = p1 * s0 * dh
    unary = q01 * h
    d_unary = dq01 * h + q01 * dh
    response = b01 + b10
    d_response = db01 + db10
    inserted_b01 = q01 * db01 + b01 * dq01
    inserted_b10 = q01 * db10 + b10 * dq01
    require((h, dh, unary, d_unary) == (1, 1, 1, 0)
            and (b01, b10, response) == (1, -1, 0)
            and (db01, db10, d_response) == (1, -1, 0)
            and inserted_b01 == inserted_b10 == 0,
            ("trapped complete-row tangent changed", h, dh, unary,
             d_unary, response, d_response, inserted_b01, inserted_b10))

    shore = frozenset(((2, 3), (4, 5)))
    mate = transversal(shore)
    closure = transversal(mate)
    require(mate == frozenset(((2, 4), (2, 5), (3, 4), (3, 5)))
            and closure == shore,
            ("matching/rectangle Hall concept changed", mate, closure))
    support = (frozenset(((0, 1), (2, 3), (4, 5))),)
    require(all(all(physical in matching for matching in support)
                for physical in support[0]),
            "a singleton-support edge stopped being a coloop")
    return {
        "nonzero_pure_q_support": ["q01", "q23", "q45"],
        "pure_support_matching": "01|23|45",
        "active_normalization": "q01*H2345=1",
        "endpoint_values": {"p0*s1": 1, "p1*s0": -1},
        "complete_response_value": "b01+b10=0",
        "tangent": {"dq01": -1, "dq23": 1, "all_other_dq": 0},
        "target_first_PP": "d(q01*H2345)=0",
        "complete_response_first_PP": "db01+db10=0",
        "each_inserted_double_collision_relation": [
            "q01*db01+b01*dq01=0", "q01*db10+b10*dq01=0",
        ],
        "selected_db01_tangent_value": str(db01),
        "tail_Hall_shore": [list(value) for value in sorted(shore)],
        "transversal_rectangle": [list(value) for value in sorted(mate)],
        "Hall_shore_closed": True,
        "supported_pure_q_edges_are_literal_coloops": True,
        "forced_support_exit": False,
        "scope": (
            "exact local fixed-window coefficient/tangent point, not asserted "
            "to be a complete GHZ tensor"
        ),
    }


def recurrence_scope_audit() -> dict[str, object]:
    previous = load(
        "computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py",
        "double_collision_previous",
    )
    previous_ledger, previous_digest = previous.audit()
    require(previous_digest == previous.EXPECTED_LEDGER_SHA256,
            "the previous double-collision ledger changed")
    literal = previous_ledger["literal_PP_and_reinsertion_faces"]
    require(literal["physical_endpoint_insertion"]["top_type"] == "P4+2K2"
            and literal["physical_endpoint_insertion"]["face_types"]
                == {"endpoint_dp_ds": ["P3+2K2"],
                    "tail_q_db01": ["P4+K2"],
                    "dq01_companion": ["4K2"]},
            "the nine double-collision face types changed")

    pivot = load(
        "computations/verify_h3_active_fan_coloop_complete_row_pivot.py",
        "double_collision_pivot",
    )
    transport = pivot.audit_termwise_common_q_transport()
    require("orientation" in transport["transport"],
            "the complete-row pivot stopped retaining endpoint orientation")

    # The expensive 14^3/4736 support censuses are hash-pinned above.  Audit
    # their two exact scope statements without replaying them in every mode.
    recurrence_note = (ROOT / (
        "notes/h3-active-coloop-forced-mate-recurrence-potential-boundary.md"
    )).read_text()
    closed_note = (ROOT / (
        "notes/h3-active-coloop-closed-shore-complete-row-response-gate.md"
    )).read_text()
    require("closed triangle" in recurrence_note
            and "closed nine-edge shore" in recurrence_note
            and "Hall shadows, not complete GHZ source" in recurrence_note,
            "the trapped-shore recurrence scope changed")
    require("4736 completed response seeds tested" in closed_note
            and "strict Hall growth in every case" in closed_note
            and "not identified with the still separate pointed covector"
                in closed_note,
            "the complete closed-shore scope changed")

    active = load(
        "computations/verify_h3_active_fan_coloop_or_four_good.py",
        "double_collision_active_fan",
    )
    alternative = active.audit_ternary_rank_alternative()
    require(alternative["literal_coloop_assignments"] == 26,
            "the active-fan coloop branch changed")
    return {
        "ordinary_support_recurrence": {
            "domain": "complete unary/response coefficient supports on K6",
            "positive_conclusion": (
                "after all pinned ordinary coefficient rows, a certified "
                "Hall-growth/active-fan entry is forced in that support packet"
            ),
            "does_not_construct": (
                "the pointed occurrence comparison or a first-jet row in "
                "the P4+2K2 double-collision operation block"
            ),
        },
        "termwise_transport_preserves": [
            "physical matching", "P/S partners", "endpoint orientation",
            "remote q tail",
        ],
        "double_collision_face_block": {
            "top": "P4+2K2",
            "live_families": {"P4+K2": 6, "4K2": 3},
            "removed_edge_and_operation_tags_retained": True,
        },
        "active_fan_projected_alternative": "four-good or literal coloop",
        "literal_coloop_status_assignments":
            alternative["literal_coloop_assignments"],
        "projection_of_trapped_tangent": "literal coloop branch",
        "physical_jet_prolongation_present": False,
        "reason": (
            "support recurrence can select or move a coefficient occurrence; "
            "it does not provide the operation-changing boundary which makes "
            "an endpoint-oriented PP carrier absolute"
        ),
    }


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
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


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def endpoint_odd_finite_counterguard_audit() -> dict[str, object]:
    # Coordinate order is (source B, source C, exit B, exit C), nine faces
    # in each block.  Each face receives two monic recurrence graphs.  We
    # also grant a complete B+C row separately in every fine label, both at
    # the source and at the retained exit.  This is stronger than one
    # aggregate complete response row.
    faces = 9
    width = 4 * faces

    def position(block: int, face: int) -> int:
        return block * faces + face

    def vector(values: dict[int, int]) -> tuple[Q, ...]:
        return tuple(Q(values.get(index, 0)) for index in range(width))

    rows = []
    for face in range(faces):
        rows.extend((
            vector({position(0, face): -1, position(2, face): 1}),
            vector({position(1, face): -1, position(3, face): 1}),
            vector({position(0, face): 1, position(1, face): 1}),
            vector({position(2, face): 1, position(3, face): 1}),
        ))
    rows = tuple(rows)
    selected_b = vector({position(0, face): 1 for face in range(faces)})
    odd_dual = vector({
        **{position(0, face): 1 for face in range(faces)},
        **{position(1, face): -1 for face in range(faces)},
        **{position(2, face): 1 for face in range(faces)},
        **{position(3, face): -1 for face in range(faces)},
    })
    old_rank = rank(rows)
    new_rank = rank(rows + (selected_b,))
    require(old_rank == 3 * faces and new_rank == 3 * faces + 1
            and all(dot(odd_dual, row) == 0 for row in rows)
            and dot(odd_dual, selected_b) == faces,
            ("endpoint-odd double-collision guard changed", old_rank, new_rank))
    return {
        "face_order": [
            "six P4+K2 q01*db tail flags", "three 4K2 psH*dq01 flags",
        ],
        "endpoint_orientations": ["B=p0*s1", "C=p1*s0"],
        "coordinates": width,
        "granted_rows_per_face": [
            "B recurrence/coloop exit graph", "C recurrence/coloop exit graph",
            "absolute complete B+C source pair", "absolute complete B+C exit pair",
        ],
        "rank_before_after_selected_B_packet": [old_rank, new_rank],
        "endpoint_odd_dual": {
            "B_source_and_exit": 1,
            "C_source_and_exit": -1,
            "on_all_granted_rows": 0,
            "on_selected_nine_face_B_packet": faces,
        },
        "finite_centered_survivor_dimension": faces,
        "meaning": (
            "complete rows and orientation-preserving recurrence graphs can "
            "move the odd class to coloop carriers but cannot kill it"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 double-collision active-fan/Hall prolongation gate",
        "pins": PINS,
        "trapped_complete_row_tangent": trapped_complete_row_tangent_audit(),
        "committed_recurrence_scope": recurrence_scope_audit(),
        "finite_endpoint_odd_counterguard":
            endpoint_odd_finite_counterguard_audit(),
        "verdict": (
            "The active-fan/Hall recurrence does not close the six P4+K2 "
            "and three 4K2 faces.  On ordinary coefficient support its full "
            "complete-row theorem forces Hall growth/active-fan entry, but "
            "the theorem explicitly stops before the pointed occurrence "
            "comparison and its transport preserves endpoint orientation.  "
            "The double-collision debts live one jet and one operation block "
            "higher.  A literal normalized tangent satisfies the complete "
            "target and B+C response rows while retaining db01 and landing "
            "in the closed matching/rectangle coloop branch.  Even granting "
            "every termwise recurrence graph and a complete B+C row in each "
            "fine label leaves a nine-dimensional endpoint-odd survivor."
        ),
        "first_missing_typed_row": (
            "an endpoint-orientation-asymmetric P4+2K2 first-jet Hall "
            "prolongation (or an absolute coloop-exit row) whose boundary "
            "contains one of the P4+K2/4K2 faces; ordinary support recurrence "
            "and relative carrier graphs do not supply it"
        ),
        "scope": (
            "exact local h=3 fixed-window/tangent and finite labelled rank "
            "counterguard before cap/K_Eq.  The tangent is not asserted to "
            "extend to a complete GHZ tensor, and the theorem does not deny "
            "a new physical jet prolongation"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    return ledger, sha256(payload.encode()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("tangent", "recurrence", "survivor"),
                        default="survivor")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("double-collision Hall ledger changed", digest))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
        return
    print(f"h3 double-collision active-fan/Hall gate ({arguments.mode}): PASS")
    print("complete target/response trapped tangent: EXISTS")
    print("support projection: CLOSED MATCHING/RECTANGLE -> LITERAL COLOOP")
    print("full-labelled endpoint-odd survivor: DIMENSION 9")
    print("P4+2K2 jet/Hall prolongation: NOT CONSTRUCTED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
