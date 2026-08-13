#!/usr/bin/env python3
"""Verify the rectangular anchor--Cartan rank/kernel alternative.

The zero-holonomy Schur argument does not intrinsically require a square
corank-one component.  Let M:X->Y be the complete protected component map,
h:X->k the distinguished anchor row, and g in Y the complete Cartan column.
If h is nonzero on ker(M), then exactly one of two things happens:

* g is nonzero in coker(M), and adjoining g and h raises rank by two;
* g lies in im(M), and one can solve My=g and h(y)=alpha, producing the
  unit-coefficient kernel vector (-y,1) of [[M,g],[h,alpha]].

The checker exhausts all 2x2 matrices and all small anchor/Cartan/terminal
data over {-1,0,1}, and freezes representative rectangular examples.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_global_dark_cartan_component_absorption.py":
        "2064044fee36392a6a73448409a8f33c7cec7c60e5b8700a43e1f4e6a8420165",
    "computations/verify_anchored_min_support_frame_circuit_cover.py":
        "14bc527f3ff67dd41772409e9556b0241f8b6f49b7e7ecb2c83d05a8e09806aa",
}
EXPECTED_LEDGER_SHA256 = "fb39d34a7a7a98d11901a867bdd495cc197c5722cf257a6e5efdbfb15c0b1bd5"


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


def append_row(matrix, row):
    return tuple(tuple(map(Q, old)) for old in matrix) + (tuple(map(Q, row)),)


def append_column(matrix, column):
    return tuple(tuple(map(Q, row)) + (Q(value),)
                 for row, value in zip(matrix, column, strict=True))


def augment(matrix, g, h, alpha):
    top = append_column(matrix, g)
    return top + (tuple(map(Q, h)) + (Q(alpha),),)


def mat_vec(matrix, vector):
    return tuple(sum(Q(a) * Q(b) for a, b in zip(row, vector, strict=True))
                 for row in matrix)


def solve(matrix, rhs):
    """Return one solution, or None."""
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
            "RREF solution failed")
    return tuple(answer)


def classify(matrix, g, h, alpha):
    base_rank = rank(matrix)
    anchor_visible = rank(append_row(matrix, h)) == base_rank + 1
    cartan_external = rank(append_column(matrix, g)) == base_rank + 1
    full = augment(matrix, g, h, alpha)
    full_rank = rank(full)
    record = {
        "base_rank": base_rank,
        "anchor_visible": anchor_visible,
        "cartan_external": cartan_external,
        "augmented_rank": full_rank,
    }
    if not anchor_visible:
        record["outcome"] = "outside_hypothesis"
        return record
    if cartan_external:
        require(full_rank == base_rank + 2,
                "two-sided visible augmentation did not gain two ranks")
        record["outcome"] = "two_rank_bright"
        return record

    # First solve My=g.  Anchor visibility means that the homogeneous
    # solution space contains c with h(c)!=0, so adjust y along c until
    # h(y)=alpha.  Equivalently solve the fully augmented right side.
    stacked = append_row(matrix, h)
    y = solve(stacked, tuple(map(Q, g)) + (Q(alpha),))
    require(y is not None, "anchor-visible image branch lost its lift")
    kernel = tuple(-value for value in y) + (Q(1),)
    require(mat_vec(full, kernel) == (Q(0),) * len(full),
            "unit-coefficient kernel failed")
    require(full_rank == base_rank + 1,
            "image branch changed the expected augmented rank")
    record.update({
        "outcome": "unit_kernel",
        "potential": list(map(str, y)),
        "kernel": list(map(str, kernel)),
    })
    return record


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))

    counts = {"outside_hypothesis": 0, "two_rank_bright": 0,
              "unit_kernel": 0}
    checked = 0
    for entries in product((-1, 0, 1), repeat=4):
        matrix = (entries[:2], entries[2:])
        for g in product((-1, 0, 1), repeat=2):
            for h in product((-1, 0, 1), repeat=2):
                for alpha in (-1, 0, 1):
                    record = classify(matrix, g, h, alpha)
                    counts[record["outcome"]] += 1
                    checked += 1

    rectangular_bright = classify(
        ((1, 0, 0), (0, 0, 0)),
        g=(0, 1), h=(0, 1, 0), alpha=2,
    )
    require(rectangular_bright["outcome"] == "two_rank_bright",
            "rectangular two-rank branch stopped being bright")
    rectangular_kernel = classify(
        ((1, -1, 0), (0, 1, -1)),
        g=(2, -1), h=(1, 0, 0), alpha=3,
    )
    require(rectangular_kernel["outcome"] == "unit_kernel",
            "rectangular image branch lost its kernel")

    ledger = {
        "pins": PINS,
        "theorem": (
            "for any complete rectangular M, if the distinguished anchor "
            "row is nonzero on ker M, then a Cartan column outside im M "
            "raises the anchor-Cartan augmentation rank by two, while a "
            "Cartan column in im M admits a potential satisfying the anchor "
            "coordinate and gives a unit-coefficient kernel (-y,1)"
        ),
        "small_packets_checked": checked,
        "outcomes": counts,
        "rectangular_bright_example": rectangular_bright,
        "rectangular_kernel_example": rectangular_kernel,
        "proof_frontier": (
            "the square corank-one Schur block is optional once a complete "
            "protected kernel circuit c with nonzero anchor coordinate is "
            "available.  The remaining source theorem is to place every "
            "marked occurrence in such an anchor-visible complete kernel "
            "circuit, or route the first failure as a typed active/Hall exit"
        ),
        "scope": (
            "this is linear algebra over a field.  It does not identify the "
            "physical source incidence map M, prove the anchor-visible "
            "kernel circuit for an arbitrary source, transport the physical "
            "terminal q, or turn a nonzero augmented minor into four-good "
            "rank without the existing localization/source-unit hypotheses"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("rectangular anchor-Cartan alternative: PASS")
    print("small packets:", ledger["small_packets_checked"])
    print("outcomes:", ledger["outcomes"])
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
