#!/usr/bin/env python3
"""Project the full-site closed-cycle guard and its first exits to B-Eq.

There are six literally labelled chart squares in the two-switch/all-pure
guard.  In each four-corner block, the four internal switches are the
signless K2,2 incidence columns.  Together with the four cap diagonals they
have rank seven in B+Eq, with primitive cokernel

    Psi = delta.(B-Eq),  delta=(1,1,-1,-1).

The 24 internal switches all have Psi-value zero.  More subtly, an
individual absolute one-hole/collision matching repair is the same
shore-crossing column after the physical shore gauge, so it also has value
zero.  Only the balanced L01 private face delta has forced nonzero value.

The first collision/PP family whose B/Eq value is not fixed by committed
maps is the selected six-term db01 vertical face.  Its all-D endpoint is a
different summand, and no comparison to B/Eq has been constructed.  Thus
B-Eq terminalizes the closed internal guard, but not yet the exhaustive
source: the exact remaining scalar is Psi(Pi_BEq(db01)).
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_balanced_square_private_eq_projection_gate.py":
        "bbfb690a73844169574351ad019171a6d9c5fe332e59cc9694a1f67dcf31cf8e",
    "notes/h3-balanced-square-private-eq-projection-gate.md":
        "6d740e7e30231204dbe1b79c4b7c21fe5f5b5ac45122ac714be3c7626afa7c31",
    "computations/verify_h3_full_site_root_companion_closed_balanced_cycle_counterguard.py":
        "d1f9a89b9ef627d9c214c72b76c150c6134fd330f82fd343f68f12a4fcbccd0c",
    "notes/h3-full-site-root-companion-closed-balanced-cycle-counterguard.md":
        "c44f6f5d93edea92d9e4b004c41544982e53ea94bc82f529b27ff077dd77e38f",
    "computations/verify_h3_first_collision_residual_pp_unary_reinsertion_terminal_gate.py":
        "74ee5a56f2d11f910a1121f7ebe48d051913a939c786cb9bd5ed6a6250a1eda7",
    "computations/verify_h3_one_hole_unary_response_cartan_derham_landing_gate.py":
        "591fd99ca92be53de68e781d9feb8796736ad8a4d5161bc12e6f43e1cad05fa1",
    "computations/verify_h3_selected_db01_normalized_gl3_bar_companion_gate.py":
        "620b3e54e8e6ee09a0b616d0259c8d109b0359645b20d35db5fb876c8e7e0311",
    "notes/h3-selected-db01-normalized-gl3-bar-companion-gate.md":
        "46aa4e74c52160cfaa74089727defb1a0d6c4d0051130374ec12dcc887de09de",
    "computations/verify_h3_chart_odd_gate_ii_augmented_filler_terminal_fork.py":
        "cd445864a1440b89b213229c6795b409a9c49b84bf388dc4a476ed2030077e91",
}
EXPECTED_LEDGER_SHA256 = (
    "2ad755844fbae1022c6a7eaefc603c752376266d37001e47cbc3085c39ad02fb"
)


DELTA = (Q(1), Q(1), Q(-1), Q(-1))
EDGES = ((0, 2), (0, 3), (1, 2), (1, 3))
COMPONENTS = tuple((colour, family)
                   for colour in range(3) for family in ("A-B", "A-C"))


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


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    columns = tuple(columns)
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


def block_vector(component_index: int, *, B=(0, 0, 0, 0),
                 Eq=(0, 0, 0, 0)) -> tuple[Q, ...]:
    output = [Q(0)] * (8 * len(COMPONENTS))
    offset = 8 * component_index
    output[offset:offset + 4] = map(Q, B)
    output[offset + 4:offset + 8] = map(Q, Eq)
    return tuple(output)


def component_dual(component_index: int) -> tuple[Q, ...]:
    return block_vector(component_index, B=DELTA,
                        Eq=tuple(-value for value in DELTA))


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    projection = load(
        "computations/verify_h3_balanced_square_private_eq_projection_gate.py",
        "closed_cycle_private_eq_pin",
    )
    projection_ledger, projection_digest = projection.audit()
    require(projection_digest == projection.EXPECTED_LEDGER_SHA256
            and projection_ledger["projection"]["criterion"]
                == "delta dot (B-Eq) is nonzero",
            "the private/Eq projection theorem changed")

    cycle = load(
        "computations/verify_h3_full_site_root_companion_closed_balanced_cycle_counterguard.py",
        "closed_cycle_guard_pin",
    )
    cycle_ledger, cycle_digest = cycle.audit()
    require(cycle_digest == cycle.EXPECTED_LEDGER_SHA256
            and cycle_ledger["full_two_switch_pure_normalized_guard"]
                ["complete_rows"] == 24,
            "the 24-row closed-cycle guard changed")

    collision = load(
        "computations/verify_h3_first_collision_residual_pp_unary_reinsertion_terminal_gate.py",
        "closed_cycle_collision_pin",
    )
    collision_ledger, collision_digest = collision.audit()
    require(collision_digest == collision.EXPECTED_LEDGER_SHA256
            and collision_ledger["source_direction_packets"]
                ["distinct_packets"] == 30
            and collision_ledger["smaller_obstruction"]["support"]
                == "12 p0->D,dD flags minus 12 q01->-s1,ds1 flags",
            "the first collision/PP reduction changed")

    landing = load(
        "computations/verify_h3_one_hole_unary_response_cartan_derham_landing_gate.py",
        "closed_cycle_one_hole_pin",
    )
    landing_ledger, landing_digest = landing.audit()
    require(landing_digest == landing.EXPECTED_LEDGER_SHA256
            and landing_ledger["exact_rank_gate"]
                ["J_filled_after_either_repair"],
            "the one-hole absolute landing gate changed")

    db01 = load(
        "computations/verify_h3_selected_db01_normalized_gl3_bar_companion_gate.py",
        "closed_cycle_db01_pin",
    )
    db01_ledger, db01_digest = db01.audit()
    require(db01_digest == db01.EXPECTED_LEDGER_SHA256
            and db01_ledger["literal_support"]["selected_db01_term_count"] == 6
            and db01_ledger["graph_and_bicomplex"]
                ["rank_before_then_after_db01"] == [2, 3],
            "the selected db01 face changed")

    # Reorder the cyclic object order of 097d3f1 as (A0,A1,B0,B1).  Its four
    # physical chart edges become exactly all four K2,2 shore crossings.
    cycle_reorder = (0, 2, 1, 3)
    cycle_to_block = {old: new for new, old in enumerate(cycle_reorder)}
    reordered_edges = {
        tuple(sorted((cycle_to_block[left], cycle_to_block[right])))
        for left, right in cycle.SQUARE_EDGES
    }
    require(reordered_edges == set(EDGES)
            and tuple(cycle.LAMBDA[index] for index in cycle_reorder) == DELTA,
            ("the physical cycle/private block identification changed",
             reordered_edges))

    # Six independent B+Eq blocks.  The old projected family is 24 cap
    # diagonals plus the 24 internal chart switches.  Each block has rank 7;
    # the direct sum has six primitive private-minus-Eq cokernels.
    diagonals = []
    switches = []
    duals = []
    for component_index, _component in enumerate(COMPONENTS):
        duals.append(component_dual(component_index))
        for corner in range(4):
            basis = tuple(1 if index == corner else 0 for index in range(4))
            diagonals.append(block_vector(component_index, B=basis, Eq=basis))
        for left, right in EDGES:
            incidence = tuple(1 if index in (left, right) else 0
                              for index in range(4))
            switches.append(block_vector(component_index, B=incidence))
    diagonals = tuple(diagonals)
    switches = tuple(switches)
    duals = tuple(duals)
    old = diagonals + switches
    require(len(diagonals) == len(switches) == 24
            and rank(old) == 42
            and rank(duals) == 6
            and all(dot(dual, column) == 0
                    for dual in duals for column in old),
            "the six-block private/Eq guard changed")

    # Collision matching completion and the absolute one-hole cofactor split
    # both give an oriented A-B or A-C switch before the shore gauge.  The
    # gauge DELTA turns e_A-e_B into e_A+e_B, one of the same signless edge
    # columns.  Thus an individual absolute one-hole landing can close its
    # local 60D residual while leaving every global B-Eq charge unchanged.
    oriented_one_hole = []
    gauged_one_hole = []
    one_hole_values = []
    for component_index, _component in enumerate(COMPONENTS):
        dual = duals[component_index]
        for left, right in EDGES:
            oriented = tuple(Q(1) if index == left else
                             Q(-1) if index == right else Q(0)
                             for index in range(4))
            gauged = tuple(DELTA[index] * oriented[index]
                           for index in range(4))
            expected = tuple(Q(1) if index in (left, right) else Q(0)
                             for index in range(4))
            require(gauged == expected,
                    ("shore gauge changed one-hole switch", left, right,
                     gauged, expected))
            oriented_one_hole.append(oriented)
            column = block_vector(component_index, B=gauged)
            gauged_one_hole.append(column)
            one_hole_values.append(dot(dual, column))
    gauged_one_hole = tuple(gauged_one_hole)
    require(len(gauged_one_hole) == 24
            and gauged_one_hole == switches
            and set(one_hole_values) == {Q(0)}
            and rank(old + gauged_one_hole) == rank(old),
            "an individual one-hole/collision repair broke B-Eq")

    # The balanced L01 private face is not a shore-crossing edge.  One copy
    # per component supplies the missing rank in every block and is detected
    # by four.  If its Eq packet is tied, however, the mismatch vanishes.
    l01_private = tuple(block_vector(index, B=DELTA)
                        for index in range(len(COMPONENTS)))
    l01_tied = tuple(block_vector(index, B=DELTA, Eq=DELTA)
                     for index in range(len(COMPONENTS)))
    require([dot(duals[index], l01_private[index])
             for index in range(len(COMPONENTS))] == [Q(4)] * 6
            and [dot(duals[index], l01_tied[index])
                 for index in range(len(COMPONENTS))] == [Q(0)] * 6
            and rank(old + l01_private) == 48
            and rank(old + l01_tied) == 42,
            "the absolute/tied L01 controls changed")

    # Collision tops and their literal PP flags live in collision/vertical
    # PP summands, not in B/Eq.  The committed reduction supplies no map from
    # the first selected six-term db01 face to B/Eq.  Algebraically both a
    # centered completion and a breaking completion are compatible with its
    # independent 3-coordinate graph/all-D rank test.  Hence its mismatch is
    # the exact first scalar which the full comparison must compute.
    zero_projection = (Q(0),) * (8 * len(COMPONENTS))
    symmetric_collision_value = dot(duals[0], zero_projection)
    distinct_pp_packet_value = dot(duals[0], zero_projection)
    db01_centered_candidate = switches[0]
    db01_breaking_candidate = l01_private[0]
    require(symmetric_collision_value == distinct_pp_packet_value == 0
            and dot(duals[0], db01_centered_candidate) == 0
            and dot(duals[0], db01_breaking_candidate) == 4,
            "the db01 comparison fork changed")

    ledger = {
        "theorem": "closed-cycle private/Eq collision-PP exit gate",
        "pins": PINS,
        "six_block_projection": {
            "component_order": [[colour, family]
                                for colour, family in COMPONENTS],
            "coordinates": 48,
            "cap_diagonal_columns": len(diagonals),
            "internal_relative_switch_B_faces": len(switches),
            "old_rank": rank(old),
            "cokernel_dimension": 48 - rank(old),
            "primitive_duals": "one delta.(B-Eq) per labelled component",
            "all_24_internal_switch_values": "0",
        },
        "collision_and_one_hole_exits": {
            "collision_top_BEq_projection": (
                "zero in the currently typed direct sum; collision degree "
                "has no committed B/Eq comparison"
            ),
            "distinct_C2plus_C4_P2_packets": (
                "old/centered or outside the selected B/Eq block; value zero"
            ),
            "same_cell_residual": (
                "J_E01, twelve A flags minus twelve endpoint flags"
            ),
            "absolute_one_hole_before_shore_gauge": "e_A-e_endpoint",
            "after_shore_gauge": "e_A+e_endpoint, an existing K2,2 edge",
            "all_24_one_hole_values": sorted({str(value)
                                               for value in one_hole_values}),
            "rank_after_all_one_hole_edges": rank(old + gauged_one_hole),
            "consequence": (
                "an absolute one-hole landing fills its local first-PP "
                "residual but does not break the global private/Eq charge"
            ),
        },
        "L01_controls": {
            "absolute_private_projection": "(B,Eq)=(delta,0)",
            "value_per_component": 4,
            "rank_after_six_absolute_L01_faces": rank(old + l01_private),
            "tied_projection": "(B,Eq)=(delta,delta)",
            "tied_value": 0,
            "rank_after_six_tied_faces": rank(old + l01_tied),
        },
        "first_untyped_breaker": {
            "name": "selected db01 vertical PP comparison",
            "terms": db01_ledger["literal_support"]
                ["selected_db01_term_count"],
            "local_rank_before_after": db01_ledger["graph_and_bicomplex"]
                ["rank_before_then_after_db01"],
            "all_D_endpoint_is_db01": False,
            "B_Eq_projection_constructed": False,
            "deciding_scalar": "m_db01=delta.(B-Eq)(Pi_BEq(db01))",
            "compatible_centered_value": "0",
            "compatible_breaking_value": "4",
            "if_zero_next_face": (
                "the eighteen endpoint/direction terms of dL01, primitive "
                "profile (2,2,-1,-1,-1,-1)"
            ),
        },
        "verdict": (
            "The B-Eq test terminalizes the entire 24-switch closed internal "
            "guard.  It does not yet terminalize the exhaustive physical "
            "source.  Contrary to the strongest hoped-for statement, an "
            "individual absolute one-hole or collision matching repair is "
            "centered and has zero mismatch.  The absolute balanced L01 face "
            "has forced mismatch four.  Before L01, the first family which "
            "can break the law is the selected six-term db01 PP comparison; "
            "its B/Eq projection is exactly the missing datum."
        ),
        "terminal_criterion": (
            "If the selected db01 comparison and every later dL01/collision "
            "carrier have delta.(B-Eq)=0 in each literal component, the six "
            "private-minus-Eq duals extend and the closed-cycle guard is "
            "terminal.  Any first nonzero value identifies the exact physical "
            "exit and raises the corresponding projected rank."
        ),
        "scope": (
            "exact six-component B/Eq projection, all 24 chart switches, "
            "the shore-gauged one-hole/collision repair type, and the first "
            "untyped selected db01 face.  It does not construct Pi_BEq on "
            "db01 or claim that the collision/PP direct sum is exhaustive."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("closed-cycle B/Eq: 48 COORDS / OLD RANK 42 / COKERNEL 6")
    print("24 internal switches: MISMATCH ZERO")
    print("24 absolute one-hole/collision repairs: STILL ZERO AFTER GAUGE")
    print("absolute L01: MISMATCH 4 / tied L01: ZERO")
    print("first untyped breaker: SELECTED SIX-TERM db01 COMPARISON")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
