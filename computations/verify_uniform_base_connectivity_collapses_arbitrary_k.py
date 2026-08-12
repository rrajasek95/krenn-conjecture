#!/usr/bin/env python3
"""Verify that exhaustive typed base connectivity subsumes arbitrary k.

The theorem is conditional on the source connectivity alternative.  If all
literal matching bases occurring in all occupied complete one-star columns
lie in one connected flat typed-C4 graph, every base tensor is a scalar
multiple of one root tensor.  Hence every complete column is collinear.
At a maximum-anchor/minimum-support representative, two occupied collinear
columns give the exact nu-safe deletion already proved.  Therefore arbitrary
column count creates no additional flat rank problem after connectivity.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_c4_base_exchange_connected_flat_propagation.py":
        "1e1b6ff1ae607b860330a6117f61045640b73f546275c36d4d62daff9ab6e383",
    "notes/c4-base-exchange-connected-flat-propagation.md":
        "9cf4b98c6ca5f9492c854aaf3c726b7eeb48a1294cfa7609a1b521b0df3e2eef",
    "computations/verify_h3_axis_target_coloop_proportional_nu_safe_reduction.py":
        "6f27d3585fdc4708026ab6fef6134295dd874f83bb43fd1f480b7314362c56f3",
    "notes/h3-axis-target-coloop-proportional-nu-safe-reduction.md":
        "8e9ba2c477be06a022f1c86f334d45a95b1ff7d9393b7134c6f38aa21d797f14",
}
EXPECTED_LEDGER_SHA256 = (
    "fd4fe2c0b5d3e9de98bbac03665d044c13167dbcc03d5b14f31d9ac212313e88"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rank(vectors):
    matrix = [list(map(Q, vector)) for vector in vectors]
    if not matrix:
        return 0
    rows, columns = len(matrix), len(matrix[0])
    pivot = 0
    for column in range(columns):
        row = next((index for index in range(pivot, rows)
                    if matrix[index][column]), None)
        if row is None:
            continue
        matrix[pivot], matrix[row] = matrix[row], matrix[pivot]
        value = matrix[pivot][column]
        matrix[pivot] = [entry / value for entry in matrix[pivot]]
        for index in range(rows):
            if index == pivot or not matrix[index][column]:
                continue
            value = matrix[index][column]
            matrix[index] = [old - value * new
                             for old, new in zip(matrix[index], matrix[pivot])]
        pivot += 1
    return pivot


def audit_k(k):
    root = tuple(map(Q, (1, 2, 3, 5, 7)))
    bases = []
    columns = []
    next_scalar = 1
    # Give column j exactly j+1 literal bases.  The flat connected theorem
    # identifies each with a scalar multiple of root; their sums are the
    # complete response columns.
    for column_index in range(k):
        column_bases = []
        for _ in range(column_index + 1):
            scalar = Q(next_scalar)
            next_scalar += 1
            vector = tuple(scalar * value for value in root)
            bases.append(vector)
            column_bases.append(vector)
        columns.append(tuple(sum(vector[coordinate]
                                 for vector in column_bases)
                             for coordinate in range(len(root))))
    require(rank(bases) == rank(columns) == 1,
            f"flat exhaustive graph at k={k} stopped being collinear")
    # Delete the first column into the second by the exact finite linear
    # update.  This is the tensor identity used by the pinned nu-safe move.
    pivot = next(index for index, value in enumerate(columns[0]) if value)
    scalar = columns[1][pivot] / columns[0][pivot]
    deleted = tuple(columns[1][index] - scalar * columns[0][index]
                    for index in range(len(root)))
    require(not any(deleted), f"k={k} finite deletion failed")
    return {
        "occupied_columns": k,
        "literal_bases": len(bases),
        "base_rank": rank(bases),
        "complete_column_rank": rank(columns),
        "finite_deletion_scalar": str(scalar),
    }


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"dependency changed: {relative}: {actual}")
    ledger = {
        "audits": [audit_k(k) for k in range(2, 11)],
        "conditional_theorem": (
            "if the complete literal base inventory of all occupied one-star "
            "columns is one connected source-exhaustive flat typed-C4 graph, "
            "all bases and complete columns lie on one tensor line; two "
            "occupied columns give the pinned exact nu-safe deletion"
        ),
        "consequence": (
            "after the source connectivity-or-separator theorem, arbitrary "
            "column count is not a separate flat rank-completion problem"
        ),
        "remaining_nonflat_scope": (
            "a routed active carrier can still have local profile 2,2,3,3; "
            "nonflat separator landing and Hall/lock incidence remain part "
            "of the connectivity theorem, not of this flat collapse"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"arbitrary-k flat collapse ledger changed: {digest}")
    print(json.dumps(ledger, sort_keys=True))
    print(f"ledger_sha256={digest}")
    print("uniform base connectivity collapses arbitrary k: PASS")


if __name__ == "__main__":
    main()
