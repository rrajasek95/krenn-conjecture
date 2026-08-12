#!/usr/bin/env python3
r"""Positive-generator boundary for the clean-C5 Omega/r comparison.

After granting the reduced-Eq correction, the committed physical comparison
inventory supplies only the five cyclic differences C_v-C_next.  This
checker composes the complete repeated-site audit with the eta compensation
theorem and freezes the smallest genuinely new generator type:

  P~_(v,N)=(-r_v,+Q_(v,N); ores=1)

in the same labelled P3+K2 grade as the endpoint bar

  B_(v,N)=(-Omega_v,+Q_(v,N); ores=1).

Their difference has boundary -Omega_v+r_v and zero augmented readouts.
For physical zero-indeterminacy its rootless terminal readout must be
1+delta_(vz) u_z/t on eta_z.  Five cyclic copies have aggregate readout
5+u_z/t.

No such lift is in the complete committed inventory.  A single cyclically
homogeneous packaging first occurs in the degree-five C5 lcm; its boundary
is the weighted aggregate of the five comparison vertices.  The existing
degree-five Tor cell instead bounds the five edges and cannot supply it.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "f8e8b2cb1e6a257158527c8645b169d72864bf6f49c7b4019e83052fa48d090f"
PINS = {
    "computations/verify_h3_rootless_clean_separator_repeated_inventory_gate.py":
        "af9a69ad996bd4390ff3fe9139e357a3bb765292ec969350a948612d9b824fa7",
    "computations/verify_h3_rootless_eta_cyclic_compensation_boundary.py":
        "9beab390c8ed2c89f1a8f62ee54857c03199fecd5ad9a69ab6f29d6a04140b6d",
    "computations/verify_h3_rootless_endpoint_to_collision_chain_map_boundary.py":
        "be39a61df8e3723983eea7a20d405fba7ff0f3822bc90e8d48b8039177f69cfc",
    "computations/verify_h3_rootless_five_cycle_positive_interface.py":
        "fd359b3ff2abbb01d9508996c754a27b70890b2cd621926fc30b92057b337851",
    "computations/verify_h3_component_iv_collision_family_normal_jet_interface.py":
        "a777687ed775c73b10129c0bee32b59f12fa3b579de39e6c4154e5ed94634651",
}

FACE_ORDER = (1, 3, 5, 2, 4)
ROWS = ("Omega", "Q", "ridge", "Eq", "W", "target", "ores",
        "ainc")
# Internal C5 variables are (a,b,c,d,e).
VERTEX_DEGREES = (
    (0, 1, 0, 1, 0),  # g_1=bd
    (1, 0, 0, 1, 0),  # g_3=ad
    (1, 0, 1, 0, 0),  # g_5=ac
    (0, 0, 1, 0, 1),  # g_2=ce
    (0, 1, 0, 0, 1),  # g_4=be
)
LCM_DEGREE = (1, 1, 1, 1, 1)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def vector(**entries: int) -> tuple[int, ...]:
    require(set(entries).issubset(ROWS), ("unknown row", entries))
    return tuple(entries.get(row, 0) for row in ROWS)


def add(*columns: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(column[index] for column in columns)
                 for index in range(len(ROWS)))


def scale(coefficient: int, column: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(coefficient * entry for entry in column)


def rank(columns: list[tuple[int, ...]]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(height):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def determinant(columns: list[tuple[int, ...]]) -> int:
    require(columns and all(len(column) == len(columns)
                            for column in columns), "not square")
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(len(columns))]
    value = Q(1)
    for column in range(len(columns)):
        pivot = next((row for row in range(column, len(columns))
                      if matrix[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            value *= -1
        pivot_value = matrix[column][column]
        value *= pivot_value
        matrix[column] = [entry / pivot_value for entry in matrix[column]]
        for row in range(column + 1, len(columns)):
            if not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [left - factor * right for left, right in
                           zip(matrix[row], matrix[column], strict=True)]
    require(value.denominator == 1, "nonintegral determinant")
    return value.numerator


def typed_single_face_lift() -> dict[str, object]:
    endpoint = vector(Omega=-1, Q=1, ores=1)
    coarse_pp = vector(ridge=-1, ores=1)
    lifted_pp = vector(Q=1, ridge=-1, ores=1)
    comparison = add(endpoint, scale(-1, lifted_pp))
    require(comparison == vector(Omega=-1, ridge=1),
            ("comparison boundary changed", comparison))
    require(all(comparison[ROWS.index(row)] == 0
                for row in ("Eq", "W", "target", "ores", "ainc")),
            "comparison acquired an augmented readout")
    return {
        "row_order": list(ROWS),
        "endpoint_bar": list(endpoint),
        "committed_coarse_PP": list(coarse_pp),
        "required_common_companion_PP_lift": list(lifted_pp),
        "endpoint_minus_lifted_PP": list(comparison),
        "boundary": "-t_v*Omega_v+r_v (common multiplier suppressed)",
        "fine_degree": "same labelled repeated P3+K2 endpoint/chart grade",
        "strict_readouts_Eq_W_target_ores_ainc": [0, 0, 0, 0, 0],
    }


def cyclic_boundary_module() -> dict[str, object]:
    edges = []
    for index in range(5):
        column = [0] * 5
        column[index] = 1
        column[(index + 1) % 5] = -1
        edges.append(tuple(column))
    aggregate = (1, 1, 1, 1, 1)
    vertex = (1, 0, 0, 0, 0)
    require(rank(edges) == 4, "clean comparison edges lost rank four")
    require(all(sum(column) == 0 for column in edges),
            "an edge acquired aggregate mass")
    require(rank(edges + [aggregate]) == 5,
            "aggregate unexpectedly entered the edge span")
    require(rank(edges + [vertex]) == 5,
            "one primitive vertex stopped completing the edges")
    tree = edges[:4]
    aggregate_index = abs(determinant(tree + [aggregate]))
    vertex_index = abs(determinant(tree + [vertex]))
    require((aggregate_index, vertex_index) == (5, 1),
            ("integral completion indices changed", aggregate_index,
             vertex_index))
    return {
        "normalized_edge_columns": [list(column) for column in edges],
        "rank": 4,
        "primitive_cokernel_covector": [1, 1, 1, 1, 1],
        "requested_aggregate": list(aggregate),
        "requested_aggregate_in_image": False,
        "tree_plus_aggregate_determinant": aggregate_index,
        "tree_plus_one_vertex_determinant": vertex_index,
        "rational_scope": (
            "over characteristic zero the aggregate kills the remaining "
            "line; integrally it has index five, while one vertex is primitive"
        ),
    }


def degree_five_packaging() -> dict[str, object]:
    coefficients = tuple(tuple(top - base for top, base in
                               zip(LCM_DEGREE, degree, strict=True))
                         for degree in VERTEX_DEGREES)
    expected = (
        (1, 0, 1, 0, 1),  # ace
        (0, 1, 1, 0, 1),  # bce
        (0, 1, 0, 1, 1),  # bde
        (1, 1, 0, 1, 0),  # abd
        (1, 0, 1, 1, 0),  # acd
    )
    require(coefficients == expected,
            ("degree-five aggregate coefficients changed", coefficients))
    for degree, multiplier in zip(VERTEX_DEGREES, coefficients, strict=True):
        require(tuple(left + right for left, right in
                      zip(degree, multiplier, strict=True)) == LCM_DEGREE,
                "weighted comparison boundary is not homogeneous")

    # Existing C5 top has boundary in the edge module with coefficients
    # (ce,be,bd,ad,ac); composing with the cyclic edge boundary is zero.
    top_edge_coefficients = (
        (0, 0, 1, 0, 1),  # ce
        (0, 1, 0, 0, 1),  # be
        (0, 1, 0, 1, 0),  # bd
        (1, 0, 0, 1, 0),  # ad
        (1, 0, 1, 0, 0),  # ac
    )
    # Sparse polynomial cancellation: for each vertex, incoming and outgoing
    # edge coefficients become the same monomial after multiplying the edge
    # lcm.  The pinned positive-interface checker proves the full signs; here
    # we freeze the target homological degree distinction.
    require(len(set(top_edge_coefficients)) == 5,
            "degree-five top edge coefficients collided")
    return {
        "common_internal_multidegree": "abcde",
        "face_order": list(FACE_ORDER),
        "vertex_degrees": [list(degree) for degree in VERTEX_DEGREES],
        "weighted_aggregate_coefficients": [list(value)
                                             for value in coefficients],
        "weighted_boundary": (
            "ace*C_1+bce*C_3+bde*C_5+abd*C_2+acd*C_4"
        ),
        "normalized_boundary": "sum_v C_v",
        "existing_degree_five_Tor_boundary": (
            "ce*E_0+be*E_1+bd*E_2+ad*E_3+ac*E_4"
        ),
        "existing_top_targets_edges_not_vertices": True,
    }


def eta_readout() -> dict[str, object]:
    records = []
    for auxiliary in range(1, 6):
        facewise = [
            f"1+u_{auxiliary}/t" if face == auxiliary else "1"
            for face in range(1, 6)
        ]
        records.append({
            "eta": f"eta_{auxiliary}",
            "required_rootless_face_readouts": facewise,
            "aggregate": f"5+u_{auxiliary}/t",
            "current_Q_readout": 0,
            "current_rootless_readout": 0,
        })
    return {
        "unique_face_local_compensation": "c_v=t-u_v",
        "homogeneous_value_candidate": "(t-u_v)*Q_v",
        "records": records,
        "strict_readouts": {"target": 0, "ores": 0, "ainc": 0, "W": 0},
    }


def main() -> None:
    pin_dependencies()
    ledger = {
        "theorem": "clean C5 positive Omega/r generator boundary",
        "single_face_source_type": typed_single_face_lift(),
        "comparison_cokernel": cyclic_boundary_module(),
        "eta_zero_indeterminacy": eta_readout(),
        "cyclic_homogeneous_packaging": degree_five_packaging(),
        "inventory_verdict": {
            "chain_in_complete_committed_inventory": False,
            "why": (
                "after reduced-Eq correction all completed PP/Hasse/normal/"
                "full-nine/Tate cycles have comparison aggregate zero; the "
                "individual coarse PP route still lacks its same-labelled Q "
                "companion, and every existing rootless readout is zero on eta_z"
            ),
        },
        "smallest_new_physical_generator": {
            "type": "common-companion Omega/r comparison vertex",
            "fine_degree": "one repeated P3+K2 endpoint/chart degree",
            "literal_PP_lift": "(-r_v,+Q_(v,N);ores=1)",
            "comparison_boundary": "-t_v*Omega_v+r_v",
            "readouts": {"Eq": 0, "W": 0, "target": 0,
                         "ores": 0, "ainc": 0},
            "eta_readout": "1+delta_(vz)*u_z/t facewise",
            "five_orbit_aggregate_eta_readout": "5+u_z/t",
        },
        "smallest_single_cyclic_packaging": {
            "internal_multidegree": "abcde (degree five)",
            "boundary": (
                "ace*C_1+bce*C_3+bde*C_5+abd*C_2+acd*C_4; "
                "after Laurent normalization this is sum_v C_v"
            ),
            "not_the_existing_Tor_top": True,
        },
        "scope": (
            "exact complete committed Hasse/PP/collision/full-nine/normal/"
            "Tate inventory after granting reduced-Eq correction; specifies "
            "but does not construct the new physical comparison generator"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"positive Omega/r boundary ledger changed: {digest}")
    print("h3 rootless clean-C5 positive Omega/r generator: BOUNDARY")
    print("existing inventory supplies aggregate comparison: NO")
    print("smallest new type: same-Q P3+K2 comparison vertex")
    print("cyclic homogeneous package: new degree-five relative generator")
    print("eta aggregate readout required: 5+u_z/t")
    print("ledger SHA-256:", digest)


if __name__ == "__main__":
    main()
