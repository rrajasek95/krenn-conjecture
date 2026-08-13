#!/usr/bin/env python3
"""Audit the target-augmented affine-circuit/Cartan alternative.

If Cx=t has a support-minimal solution, (x,1) is a circuit of
A=[C|-t].  Appending a complete Cartan column g gives either a unit-g
kernel (g in im A) or a target-annihilating left separator (g external).

The target-coordinate selector e_tau^* is nonzero on the circuit and hence
formally supplies the row side of the rectangular rank-two alternative.
It is not, however, automatically a physical source row.  The checker
freezes a no-coordinate-line circuit for which the e_tau border gains two
ranks while a target-bearing row already in row(A) gains only one.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "computations/verify_rectangular_interference_anchor_cartan_alternative.py":
        "b3d4db9e58f374bfd1f99a43931cac87fdab109c5d33c2f1c7d110e51e8f9a0a",
    "computations/verify_augmented_cartan_full_column_separator_guard.py":
        "0710f16230a1c656bb3ec24843a60c18b668fd499e81652970c41706d6d9f41e",
    "computations/verify_uniform_physical_cartan_source_prism.py":
        "4f23c4645574d619fac4667eba50567435b2f85ff2583b5b3708a565de400cca",
}
EXPECTED_LEDGER_SHA256 = (
    "4a9b28e031310e40adbd8dc09e58f83975575375e873406b3182095aaec8457d"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rref(matrix):
    work = [list(map(Q, row)) for row in matrix]
    if not work:
        return (), ()
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    pivots = []
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def rank(matrix):
    return len(rref(matrix)[1])


def columns_to_matrix(columns):
    return tuple(tuple(column[row] for column in columns)
                 for row in range(len(columns[0])))


def mat_vec(matrix, vector):
    return tuple(sum(Q(a) * Q(b) for a, b in
                     zip(row, vector, strict=True)) for row in matrix)


def append_column(matrix, column):
    return tuple(tuple(map(Q, row)) + (Q(value),) for row, value in
                 zip(matrix, column, strict=True))


def border(matrix, column, row, corner):
    return append_column(matrix, column) + (
        tuple(map(Q, row)) + (Q(corner),),
    )


def circuit_packet(k):
    """The no-coordinate-line normal form C_i=e_i, t=sum_i e_i."""
    require(k >= 2, "the affine circuit must use at least two old columns")
    target = tuple(Q(1) if row < k else Q(0) for row in range(k + 1))
    columns = tuple(
        tuple(Q(int(row == column)) for row in range(k + 1))
        for column in range(k)
    )
    augmented_columns = columns + (tuple(-value for value in target),)
    matrix = columns_to_matrix(augmented_columns)
    circuit = (Q(1),) * (k + 1)
    require(mat_vec(matrix, circuit) == (Q(0),) * (k + 1),
            "the target-augmented circuit changed")
    require(rank(matrix) == k, "the augmented circuit lost corank one")
    for omitted in range(k + 1):
        minor = columns_to_matrix(tuple(
            column for index, column in enumerate(augmented_columns)
            if index != omitted
        ))
        require(rank(minor) == k,
                "a proper subset of the circuit became dependent")
    for column in columns:
        require(rank(columns_to_matrix((column, target))) == 2,
                "the affine fibre acquired a coordinate-line point")
    require(mat_vec(columns_to_matrix(columns), (Q(1),) * k) == target,
            "the normalized affine solution changed")
    return columns, target, matrix, circuit


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")

    circuit_orders = []
    for k in range(2, 9):
        _columns, _target, matrix, circuit = circuit_packet(k)
        circuit_orders.append({
            "old_columns": k,
            "augmented_columns": k + 1,
            "rank": rank(matrix),
            "kernel_circuit": [str(value) for value in circuit],
            "coordinate_line_hit": False,
        })

    columns, target, matrix, circuit = circuit_packet(3)
    cartan_external = (Q(0), Q(0), Q(0), Q(1))
    target_selector = (Q(0), Q(0), Q(0), Q(1))
    # This is a target-bearing row with tau coefficient -1, but it is
    # already a response row and therefore kills the circuit.
    dependent_target_row = tuple(matrix[0])
    transported_candidate_row = tuple(
        left + right for left, right in
        zip(target_selector, dependent_target_row, strict=True)
    )
    require(sum(a * b for a, b in
                zip(target_selector, circuit, strict=True)) == 1,
            "the normalized target selector stopped seeing the circuit")
    require(sum(a * b for a, b in
                zip(dependent_target_row, circuit, strict=True)) == 0,
            "the dependent target-bearing row stopped killing the circuit")
    require(sum(a * b for a, b in
                zip(transported_candidate_row, circuit, strict=True)) == 1,
            "the row-space transported candidate row lost visibility")

    base_rank = rank(matrix)
    formal_rank = rank(border(
        matrix, cartan_external, target_selector, 0
    ))
    dependent_rank = rank(border(
        matrix, cartan_external, dependent_target_row, 0
    ))
    transported_rank = rank(border(
        matrix, cartan_external, transported_candidate_row, 0
    ))
    require((base_rank, formal_rank, dependent_rank, transported_rank)
            == (3, 5, 4, 5),
            "the target-selector/physical-row rank guard changed")

    separator = (Q(0), Q(0), Q(0), Q(1))
    require(mat_vec(tuple(zip(*matrix, strict=True)), separator)
            == (Q(0),) * len(matrix[0]),
            "the external separator stopped annihilating A")
    require(sum(a * b for a, b in zip(separator, target, strict=True)) == 0,
            "the external separator stopped annihilating the target")
    require(sum(a * b for a, b in
                zip(separator, cartan_external, strict=True)) == 1,
            "the external separator stopped detecting Cartan")

    # Internal Cartan column: every old circuit coordinate can be eliminated
    # while the new Cartan coefficient stays a unit.  A nonzero tau value is
    # a new normalized affine solution; tau=0 is a homogeneous connector.
    cartan_internal = tuple(columns[0][row] + columns[1][row]
                            for row in range(4))
    potential = (Q(1), Q(1), Q(0), Q(0))
    require(mat_vec(matrix, potential) == cartan_internal,
            "the internal Cartan potential changed")
    exchange_records = []
    response_matrix = columns_to_matrix(columns)
    for old_coordinate in range(3):
        scalar = -potential[old_coordinate] / circuit[old_coordinate]
        adjusted = tuple(left + scalar * right for left, right in
                         zip(potential, circuit, strict=True))
        require(adjusted[old_coordinate] == 0
                and mat_vec(matrix, adjusted) == cartan_internal,
                "circuit elimination failed to remove an old coordinate")
        relation = tuple(-value for value in adjusted) + (Q(1),)
        require(mat_vec(append_column(matrix, cartan_internal), relation)
                == (Q(0),) * 4,
                "the unit-Cartan exchange relation changed")
        tau = adjusted[-1]
        if tau:
            old_coefficients = tuple(value / tau for value in adjusted[:-1])
            cartan_coefficient = -Q(1) / tau
            response = tuple(
                left + cartan_coefficient * right for left, right in zip(
                    mat_vec(response_matrix, old_coefficients),
                    cartan_internal, strict=True
                )
            )
            require(response == target,
                    "the target-normalized exchange stopped landing on t")
            outcome = "normalized_affine_exchange"
        else:
            require(mat_vec(response_matrix, adjusted[:-1])
                    == cartan_internal,
                    "the homogeneous connector relation changed")
            outcome = "homogeneous_unit_cartan_connector"
        exchange_records.append({
            "deleted_old_coordinate": old_coordinate,
            "adjusted_potential": [str(value) for value in adjusted],
            "tau": str(tau),
            "outcome": outcome,
        })

    alpha = Q(3)
    anchor_adjusted = tuple(left + alpha * right for left, right in
                            zip(potential, circuit, strict=True))
    internal_kernel = tuple(-value for value in anchor_adjusted) + (Q(1),)
    require(mat_vec(border(matrix, cartan_internal, target_selector, alpha),
                    internal_kernel) == (Q(0),) * 5,
            "the internally lifted Cartan kernel lost target normalization")

    ledger = {
        "pins": PINS,
        "circuit_normal_forms": circuit_orders,
        "support_minimal_circuit_theorem": (
            "if Cx=t has inclusion-minimal support, then (x,1) is a "
            "circuit of [C|-t]; a proper dependence containing tau is a "
            "smaller affine solution, while one avoiding tau is a kernel "
            "translation that deletes an occupied coordinate"
        ),
        "no_coordinate_line_consequence": (
            "if the affine fibre misses every old coordinate line, its "
            "target-augmented circuit has at least three columns"
        ),
        "cartan_column_alternative": {
            "internal": (
                "g in im(A) gives a unit-g kernel; circuit elimination "
                "deletes any chosen old circuit coordinate and yields "
                "either a new target-normalized affine exchange or a "
                "homogeneous unit-Cartan connector"
            ),
            "external": (
                "g outside im(A) gives lambda*A=0 and lambda*g=1; since "
                "-t is a column of A, necessarily lambda*t=0, so this is "
                "a target-annihilating Fitting separator, not a target unit"
            ),
            "exchange_records": exchange_records,
        },
        "normalization_row_guard": {
            "rank_A": base_rank,
            "rank_with_external_g_and_e_tau": formal_rank,
            "rank_with_external_g_and_dependent_target_row": dependent_rank,
            "rank_with_external_g_and_transported_candidate_row":
                transported_rank,
            "criterion_on_circuit_block": (
                "a literal physical row h promotes the normalized circuit "
                "exactly when h(c) is nonzero; because ker(A_D)=<c>, this "
                "is equivalent after scaling to h-e_tau in row(A_D)"
            ),
            "guard": (
                "the coefficient e_tau(c)=1 is a domain chart selector, "
                "not a physical source row.  An abstract target-bearing row "
                "can lie in row(A_D), kill c, and leave only one rank gain; "
                "a separate source theorem must identify a literal row "
                "whose restriction to the circuit is nonzero"
            ),
        },
        "typed_outputs": (
            "the internal unit-Cartan relation becomes support deletion "
            "only when its old/new columns are literal anchor-safe endpoint "
            "coordinates; otherwise it is a relative kernel subject to the "
            "physical terminal.  The external covector becomes a source "
            "unit or Hall exit only after literal old-row/Fitting/Hall "
            "typing; target normalization alone cannot provide that typing"
        ),
        "scope": (
            "exact finite-dimensional affine/matroid and rectangular rank "
            "interface.  It does not prove complete-row source exhaustivity "
            "or identify the external separator with a physical Hall row"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"target-augmented affine ledger changed: {digest}")
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("target-augmented affine circuit/Cartan guard: PASS")
    print("minimum affine support: one target-containing circuit")
    print("internal Cartan: unit connector / affine exchange")
    print("external Cartan: target-annihilating separator")
    print("normalized target selector is not automatically physical")
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
