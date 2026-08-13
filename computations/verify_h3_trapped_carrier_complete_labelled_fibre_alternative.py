#!/usr/bin/env python3
"""Reduce a trapped active-fan carrier to a complete labelled fibre basis.

Fix one sequential endpoint fibre and retain every labelled response,
target, protected, fine-grade, and selected-anchor row.  Let J be the
resulting complete map on the effective endpoint-coordinate columns in the
trapped packet, and let b=J*x be the value of the current physical row.

Choose a solution x of minimum support B.  Then J_B is injective.  Exactly
one of the following finite alternatives applies.

* |B|=1: the fibre meets a literal target-coordinate line.
* an effective column outside B is transverse to span(J_B): typed rank exit;
* every outside column lies in span(J_B), and one exists: its fundamental
  circuit is a complete-column dependence killing all retained anchor rows;
* B is the whole effective packet: each occupied coordinate covector is a
  row combination of J and reads its nonzero coefficient on b, a localized
  physical dual/source pivot.

This theorem uses the complete map directly and assumes no Gate-I Phi.  It
does not assert that the currently published scalar U/V pivot has exposed
that map: hidden companion and anchor rows are load-bearing.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "computations/verify_h3_active_fan_coloop_saturation_boundary.py":
        "35658ebed521b93387fc00aa7d2600d703f57b3e5e5deca67a11a1ab155d6c56",
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "computations/verify_frame_circuit_complete_source_kernel_lift_gate.py":
        "81738d71a423635da70caf7f3d46ca334cb0ebee7cd8240a0b7a7410c386f76c",
    "computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py":
        "22e1e7a6a933b1ba71bbd95bb605b1351e823506e495682cccff312cd3df3b15",
    "computations/verify_n8_one_bad_affine_guard_full_packet_unit.py":
        "3ecada544805a3ab25206973f8a29395f8d2df34a1b6066460eb85462c24c2b1",
}
EXPECTED_LEDGER_SHA256 = (
    "ab1d1ee4ae539cb64e5bca97dbcf37601550c84785f2017ae8e53c2fa3a28139"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def rref(matrix, width=None):
    work = [list(map(Q, row)) for row in matrix]
    if width is None:
        width = len(work[0]) if work else 0
    require(all(len(row) == width for row in work), "ragged matrix")
    pivots = []
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def rank(matrix, width=None):
    return len(rref(matrix, width)[1])


def mat_vec(matrix, vector):
    return tuple(sum(Q(a) * Q(b) for a, b in zip(row, vector, strict=True))
                 for row in matrix)


def columns(matrix):
    return tuple(tuple(column) for column in zip(*matrix, strict=True))


def column_matrix(selected_columns):
    return tuple(tuple(column[row] for column in selected_columns)
                 for row in range(len(selected_columns[0])))


def solve(matrix, rhs):
    """Return one exact solution of matrix*x=rhs, or None."""
    rows = len(matrix)
    variables = len(matrix[0]) if rows else 0
    augmented = tuple(tuple(map(Q, row)) + (Q(value),)
                      for row, value in zip(matrix, rhs, strict=True))
    reduced, pivots = rref(augmented, variables + 1)
    if any(not any(row[:variables]) and row[variables] for row in reduced):
        return None
    require(variables not in pivots, "consistent solve pivoted in rhs")
    answer = [Q(0)] * variables
    for row, pivot in enumerate(pivots):
        if pivot < variables:
            answer[pivot] = reduced[row][variables]
    require(mat_vec(matrix, answer) == tuple(map(Q, rhs)),
            "solution reconstruction failed")
    return tuple(answer)


def in_span(selected_columns, candidate):
    if not selected_columns:
        return not any(candidate)
    return solve(column_matrix(selected_columns), candidate) is not None


def minimum_support_solution(matrix, target):
    all_columns = columns(matrix)
    effective = tuple(index for index, column in enumerate(all_columns)
                      if any(column))
    for size in range(1, len(effective) + 1):
        for support in combinations(effective, size):
            restricted = column_matrix(tuple(all_columns[index]
                                             for index in support))
            coefficients = solve(restricted, target)
            if coefficients is None or any(value == 0 for value in coefficients):
                continue
            solution = [Q(0)] * len(all_columns)
            for index, value in zip(support, coefficients, strict=True):
                solution[index] = value
            require(mat_vec(matrix, solution) == tuple(map(Q, target)),
                    "minimum-support lift changed target")
            return tuple(solution), support, effective
    return None


def classify_complete_fibre(matrix, target):
    matrix = tuple(tuple(map(Q, row)) for row in matrix)
    target = tuple(map(Q, target))
    require(matrix and matrix[0] and len(matrix) == len(target),
            "empty or mismatched complete fibre")
    minimum = minimum_support_solution(matrix, target)
    require(minimum is not None and any(target),
            "classification requires a nonzero occupied fibre")
    solution, support, effective = minimum
    all_columns = columns(matrix)
    basis_columns = tuple(all_columns[index] for index in support)
    basis_matrix = column_matrix(basis_columns)
    require(rank(basis_matrix) == len(support),
            "minimum fibre support stopped being independent")

    if len(support) == 1:
        index = support[0]
        return {
            "outcome": "target_coordinate_access",
            "minimum_support": list(support),
            "solution": list(map(str, solution)),
            "coordinate": index,
        }

    outside = tuple(index for index in effective if index not in support)
    transverse = next((index for index in outside
                       if not in_span(basis_columns, all_columns[index])), None)
    if transverse is not None:
        return {
            "outcome": "typed_transverse_rank_exit",
            "minimum_support": list(support),
            "solution": list(map(str, solution)),
            "transverse_coordinate": transverse,
            "rank_before": len(support),
            "rank_after": len(support) + 1,
        }

    if outside:
        new_index = outside[0]
        coefficients = solve(basis_matrix, all_columns[new_index])
        require(coefficients is not None, "dependent column lost coordinates")
        relation = [Q(0)] * len(all_columns)
        relation[new_index] = Q(1)
        for index, coefficient in zip(support, coefficients, strict=True):
            relation[index] = -coefficient
        require(not any(mat_vec(matrix, relation))
                and relation[new_index] == 1,
                "fundamental complete-column circuit changed")
        return {
            "outcome": "anchor_safe_complete_column_dependence",
            "minimum_support": list(support),
            "solution": list(map(str, solution)),
            "new_coordinate": new_index,
            "kernel_relation": list(map(str, relation)),
        }

    # Every effective source coordinate is in the minimum basis.  Since the
    # complete labelled map has full column rank, each literal coordinate
    # selector belongs to its row space.  It detects b by the corresponding
    # nonzero coefficient of the unique fibre point.
    coordinate = support[0]
    selector = tuple(Q(int(index == coordinate))
                     for index in range(len(all_columns)))
    dual = solve(tuple(zip(*matrix, strict=True)), selector)
    require(dual is not None, "full-column-rank packet lost its row dual")
    dual_on_columns = mat_vec(tuple(zip(*matrix, strict=True)), dual)
    dual_on_target = sum(value * entry for value, entry
                         in zip(dual, target, strict=True))
    require(dual_on_columns == selector
            and dual_on_target == solution[coordinate] != 0,
            "localized physical coordinate dual changed")
    return {
        "outcome": "localized_physical_coordinate_dual",
        "minimum_support": list(support),
        "solution": list(map(str, solution)),
        "isolated_coordinate": coordinate,
        "dual": list(map(str, dual)),
        "dual_on_target": str(dual_on_target),
    }


def audit_named_branches():
    # Coordinate access: the third literal column is already the target line.
    access = classify_complete_fibre(
        ((4, -2, 1), (3, -2, 0), (0, 0, 0)),
        (2, 0, 0),
    )
    require(access["outcome"] == "target_coordinate_access"
            and access["coordinate"] == 2,
            "coordinate-access branch changed")

    # Same visible scalar U/V row, but a hidden companion row makes the
    # third column dependent rather than a target coordinate.  The relation
    # kills every row, including the last (model anchor) row.
    dependence = classify_complete_fibre(
        ((4, -2, 1), (3, -2, 1), (0, 0, 0)),
        (2, 0, 0),
    )
    require(dependence["outcome"]
            == "anchor_safe_complete_column_dependence"
            and dependence["kernel_relation"] == ["0", "1/2", "1"],
            "complete dependence branch changed")

    # A hidden labelled row makes the same third carrier transverse.
    transverse = classify_complete_fibre(
        ((4, -2, 1), (3, -2, 1), (0, 0, 1)),
        (2, 0, 0),
    )
    require(transverse["outcome"] == "typed_transverse_rank_exit"
            and transverse["transverse_coordinate"] == 2,
            "transverse branch changed")

    # With no further effective carrier, the two-column obstruction
    # X+Y,-Y is not a fourth branch: complete row-space duals isolate both
    # literal source coordinates.
    dual = classify_complete_fibre(
        ((1, 0), (1, -1), (1, 1)),
        (1, 0, 2),
    )
    require(dual["outcome"] == "localized_physical_coordinate_dual"
            and dual["dual_on_target"] == "1",
            "localized dual branch changed")
    return {
        "coordinate_access": access,
        "anchor_safe_dependence": dependence,
        "typed_transverse_exit": transverse,
        "localized_physical_dual": dual,
    }


def audit_small_exhaustion():
    counts = {
        "target_coordinate_access": 0,
        "anchor_safe_complete_column_dependence": 0,
        "localized_physical_coordinate_dual": 0,
    }
    packets = 0
    # Every 2x3 {-1,0,1} map and nonzero target in its image.  A minimum
    # support of size two spans the two-row codomain, so the transverse arm
    # is absent in this bounded census and is audited explicitly above.
    for entries in product((-1, 0, 1), repeat=6):
        matrix = (entries[:3], entries[3:])
        for target in product((-1, 0, 1), repeat=2):
            if target == (0, 0) or minimum_support_solution(matrix, target) is None:
                continue
            record = classify_complete_fibre(matrix, target)
            require(record["outcome"] in counts,
                    ("unexpected two-row outcome", record))
            counts[record["outcome"]] += 1
            packets += 1
    require(packets > 0 and all(counts.values()),
            ("small complete-fibre census changed", packets, counts))
    return {"solvable_nonzero_packets": packets,
            "outcome_histogram": counts}


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    ledger = {
        "theorem": "trapped-carrier complete labelled fibre alternative",
        "pins": PINS,
        "named_branches": audit_named_branches(),
        "small_exhaustion": audit_small_exhaustion(),
        "smallest_complete_map": {
            "domain": (
                "all effective literal endpoint-coordinate columns in one "
                "saturated trapped packet and exact common-q/fine grade"
            ),
            "rows": (
                "the complete two diagonal and crossed response coefficient "
                "rows, unary/target rows, protected endpoint word/head/"
                "orientation rows, and every selected physical anchor row"
            ),
            "right_hand_side": (
                "the value of the current physical endpoint row on all of "
                "those rows; hence the fibre is nonempty before minimization"
            ),
            "zero_rows_and_zero_columns": (
                "delete only rows zero on both the packet and rhs, and "
                "columns identically zero on the complete retained map"
            ),
        },
        "exact_alternative": (
            "a minimum-support fibre point has independent occupied columns. "
            "Support one is target-coordinate access.  Any further effective "
            "column either raises complete labelled rank (typed transverse "
            "exit) or gives its fundamental kernel circuit (anchor-safe "
            "complete-column dependence).  If there is no further effective "
            "column, full column rank puts every occupied literal coordinate "
            "selector in row(J), with nonzero value on the rhs: a localized "
            "physical source dual.  There is no fifth linear branch"
        ),
        "saturation_composition": (
            "apply the theorem after all source-certified holes in the current "
            "K6 closure have been inserted as effective columns.  An omitted "
            "outside-hole column is the already proved strict closure growth; "
            "inside the trapped packet the four alternatives above are finite"
        ),
        "known_affine_guard_composition": {
            "old_two_response_columns": ["X1+Y", "-Y"],
            "full_packet_unary_row": "q^[3][000000]-1=-1",
            "ordinary_certificate": "-(q^[3][000000]-1)=1",
            "verdict": (
                "the published no-coordinate-line guard is already a typed "
                "unit exit after its actual unary row is imposed; it is not "
                "a surviving full-packet counterguard to this alternative"
            ),
        },
        "Phi_scope": (
            "the theorem uses no protected comparison to the canonical Gate-I "
            "packet.  It is a direct Route-A landing on the fan-grade complete "
            "endpoint map.  It supersedes the Phi route only after that map is "
            "exposed with every stated row; a selected U/V scalar projection "
            "does not suffice"
        ),
        "first_unproved_physical_datum": (
            "publish/verify the actual matrix entries of the complete trapped "
            "endpoint map in the common-q grade, especially the unary, second-"
            "colour crossed, and physical-anchor rows.  The scalar identity "
            "alpha*U_i-d_i*V_i=alpha fixes only one projection, and the named "
            "same-projection completions realize access, dependence, and rank "
            "exit"
        ),
        "scope": (
            "exact finite-dimensional basis/circuit/cocircuit theorem and "
            "sharp row-completion reduction.  It does not claim that the "
            "currently published scalar carrier audit is already the complete "
            "map or that an occurrence-only dual is physical"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("trapped-carrier fibre ledger changed", digest))
    print("h3 trapped carrier: COMPLETE LABELLED FIBRE ALTERNATIVE")
    print("outcomes: coordinate / transverse / dependence / physical dual")
    print("Gate-I Phi assumed: NO")
    print("remaining: expose unary+crossed+anchor entries of the complete map")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
