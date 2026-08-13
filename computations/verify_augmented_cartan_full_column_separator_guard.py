#!/usr/bin/env python3
"""Separate a full-column Fredholm separator from two-rank coupling.

For J=[M;h] and b=(g,alpha), either b is in im(J), giving a unit-coordinate
kernel of [J b], or it is external, giving a left separator.  Externality
alone raises rank by one and is not the two-rank anchor--Cartan coupling.
The latter requires h nonzero on ker(M) and g nonzero in coker(M).
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_rectangular_interference_anchor_cartan_alternative.py":
        "b3d4db9e58f374bfd1f99a43931cac87fdab109c5d33c2f1c7d110e51e8f9a0a",
    "computations/verify_oo_curved_zero_fitting_pure_anchor_block.py":
        "d196f88111f39309f8c07adfd686919560bf52ba867b49e047d0c5b7cbe23a12",
}
EXPECTED_LEDGER_SHA256 = "7f708b931af316b3a68b464ae1fcd0abc98530ff6194a608b9b9763fa964ad63"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def transpose(matrix):
    return tuple(tuple(row) for row in zip(*matrix, strict=True))


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


def append_row(matrix, row):
    return tuple(tuple(map(Q, old)) for old in matrix) + (tuple(map(Q, row)),)


def append_column(matrix, column):
    return tuple(tuple(map(Q, row)) + (Q(value),)
                 for row, value in zip(matrix, column, strict=True))


def mat_vec(matrix, vector):
    return tuple(sum(Q(a) * Q(b) for a, b in zip(row, vector, strict=True))
                 for row in matrix)


def solve(matrix, rhs):
    augmented = append_column(matrix, rhs)
    reduced, pivots = rref(augmented)
    variables = len(matrix[0]) if matrix else 0
    if variables in pivots:
        return None
    answer = [Q(0)] * variables
    for row, pivot in enumerate(pivots):
        if pivot < variables:
            answer[pivot] = reduced[row][-1]
    require(mat_vec(matrix, answer) == tuple(map(Q, rhs)),
            "solution reconstruction failed")
    return tuple(answer)


def classify(matrix, h, g, alpha):
    matrix = tuple(tuple(map(Q, row)) for row in matrix)
    h = tuple(map(Q, h))
    g = tuple(map(Q, g))
    j = append_row(matrix, h)
    b = tuple(g) + (Q(alpha),)
    augmented = append_column(j, b)
    potential = solve(j, b)
    if potential is not None:
        kernel = tuple(-value for value in potential) + (Q(1),)
        require(mat_vec(augmented, kernel) == (Q(0),) * len(augmented),
                "full-column image branch lost its unit kernel")
        return {
            "outcome": "unit_kernel",
            "rank_M": rank(matrix),
            "rank_J": rank(j),
            "rank_augmented": rank(augmented),
            "kernel": list(map(str, kernel)),
        }

    separator = solve(transpose(j), (Q(0),) * len(j[0]))
    # The homogeneous solve above may return zero.  Extract a separator by
    # solving lambda^T J=0 and lambda^T b=1 in one system instead.
    separator_system = transpose(augmented)
    separator = solve(
        separator_system,
        (Q(0),) * len(j[0]) + (Q(1),),
    )
    require(separator is not None
            and mat_vec(transpose(j), separator) == (Q(0),) * len(j[0])
            and sum(a * value for a, value in zip(separator, b, strict=True)) == 1,
            "external column lost its normalized left separator")
    return {
        "outcome": "left_separator",
        "rank_M": rank(matrix),
        "rank_J": rank(j),
        "rank_augmented": rank(augmented),
        "rank_gain_over_J": rank(augmented) - rank(j),
        "rank_gain_over_M": rank(augmented) - rank(matrix),
        "separator": list(map(str, separator)),
        "separator_on_b": "1",
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    image = classify(
        ((1, 0), (0, 0)),
        h=(0, 1), g=(1, 0), alpha=3,
    )
    require(image["outcome"] == "unit_kernel"
            and image["rank_augmented"] == image["rank_J"],
            "full-column image example changed")

    # External auxiliary Cartan column, no anchor coupling.  A normalized
    # left separator exists, but the total gain over M is only one.
    auxiliary = classify(
        ((0,),),
        h=(0,), g=(1,), alpha=0,
    )
    require(auxiliary["outcome"] == "left_separator"
            and auxiliary["rank_gain_over_M"] == 1,
            "uncoupled external-column guard changed")

    # Triangular pure/target augmentation: the bottom scalar column is
    # external to J, yet det of the 3x3 augmentation remains zero because M
    # has rank one and h is already in row(M).
    block = ((1, -1), (2, -2))
    triangular = classify(
        block,
        h=(1, -1), g=(0, 0), alpha=1,
    )
    require(triangular["outcome"] == "left_separator"
            and triangular["rank_J"] == 1
            and triangular["rank_augmented"] == 2
            and triangular["rank_gain_over_M"] == 1,
            "triangular pure-column guard changed")

    # Genuine rectangular coupling: h raises row rank and g raises column
    # rank.  The full column is external and the total gain over M is two.
    coupled = classify(
        block,
        h=(1, 0), g=(0, 1), alpha=0,
    )
    require(coupled["outcome"] == "left_separator"
            and coupled["rank_J"] == 2
            and coupled["rank_augmented"] == 3
            and coupled["rank_gain_over_M"] == 2,
            "two-rank coupled example changed")

    ledger = {
        "pins": PINS,
        "image_example": image,
        "uncoupled_external_example": auxiliary,
        "triangular_pure_target_example": triangular,
        "two_rank_coupled_example": coupled,
        "full_column_theorem": (
            "for J=[M;h] and b=(g,alpha), b in im(J) gives a "
            "unit-coordinate kernel (-y,1) of [J b].  If b is external, "
            "there is a normalized left separator lambda with lambda^T J=0 "
            "and lambda^T b=1, and rank rises by exactly one over J"
        ),
        "coupling_guard": (
            "the external branch is not automatically a localized source "
            "unit.  A two-rank gain over M requires h nonzero on ker(M) "
            "and g nonzero in coker(M).  Without both, the separator merely "
            "detects the new auxiliary Cartan/target column"
        ),
        "physical_interpretation": (
            "lambda is an arbitrary covector on complete coefficient/readout "
            "rows.  It closes the proof only after it is typed as a physical "
            "terminal/Fitting readout, or shown to isolate a nonzero old "
            "optical occurrence or the normalized target constant.  An "
            "isolated auxiliary Cartan chain coordinate can instead be a "
            "contractible presentation pivot"
        ),
        "scope": (
            "exact finite-dimensional linear algebra.  The checker does not "
            "supply physical typing for the left separator"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("full-column guard ledger changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("augmented Cartan full-column separator guard: PASS")
    print("image branch: unit-coordinate kernel")
    print("external branch: one rank over J and a left separator")
    print("two-rank over M requires anchor and Cartan visibility")
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
