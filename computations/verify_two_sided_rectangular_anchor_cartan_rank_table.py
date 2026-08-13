#!/usr/bin/env python3
"""Verify the full two-sided rectangular anchor--Cartan rank table.

For M:X->Y, a bottom row h, a right column g, and scalar alpha, the rank of
A=[[M,g],[h,alpha]] is controlled by two visibility bits and, only when both
are dark, one scalar beta.  This freezes why a bare external Cartan column is
only a separator, while simultaneous anchor and Cartan visibility gives the
load-bearing rank-two coupling.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_rectangular_interference_anchor_cartan_alternative.py":
        "b3d4db9e58f374bfd1f99a43931cac87fdab109c5d33c2f1c7d110e51e8f9a0a",
    "computations/verify_oo_curved_zero_fitting_pure_anchor_block.py":
        "d196f88111f39309f8c07adfd686919560bf52ba867b49e047d0c5b7cbe23a12",
}
EXPECTED_LEDGER_SHA256 = "27545ee1fac34b93d3e43b2c8d20828515254aaa7b43c4b71b382f19560735a2"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rref(matrix):
    work = [list(map(Q, row)) for row in matrix]
    if not work:
        return (), ()
    height = len(work)
    width = len(work[0])
    pivot_row = 0
    pivots = []
    for column in range(width):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == height:
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def rank(matrix):
    return len(rref(matrix)[1])


def append_row(matrix, h):
    return tuple(tuple(map(Q, row)) for row in matrix) + (tuple(map(Q, h)),)


def append_column(matrix, g):
    return tuple(tuple(map(Q, row)) + (Q(value),)
                 for row, value in zip(matrix, g, strict=True))


def bordered(matrix, g, h, alpha):
    return append_column(matrix, g) + (tuple(map(Q, h)) + (Q(alpha),),)


def solve(matrix, rhs):
    augmented = append_column(matrix, rhs)
    reduced, pivots = rref(augmented)
    variables = len(matrix[0]) if matrix else 0
    if variables in pivots:
        return None
    solution = [Q(0)] * variables
    for row, pivot in enumerate(pivots):
        if pivot < variables:
            solution[pivot] = reduced[row][-1]
    return tuple(solution)


def transpose(matrix):
    return tuple(tuple(row) for row in zip(*matrix, strict=True))


def dot(left, right):
    return sum(Q(a) * Q(b) for a, b in zip(left, right, strict=True))


def classify(matrix, g, h, alpha):
    r = rank(matrix)
    anchor_visible = rank(append_row(matrix, h)) == r + 1
    cartan_visible = rank(append_column(matrix, g)) == r + 1
    actual = rank(bordered(matrix, g, h, alpha))
    beta = None
    if anchor_visible and cartan_visible:
        expected = r + 2
        branch = "double_visible_rank_two"
    elif anchor_visible or cartan_visible:
        expected = r + 1
        branch = "split_visible_rank_one"
    else:
        y = solve(matrix, g)
        lam = solve(transpose(matrix), h)
        require(y is not None and lam is not None,
                "dark row/column failed to lie in image/row space")
        beta_y = Q(alpha) - dot(h, y)
        beta_lam = Q(alpha) - dot(lam, g)
        require(beta_y == beta_lam,
                "dark scalar depends on the chosen side")
        beta = beta_y
        expected = r + int(bool(beta))
        branch = "double_dark_scalar_pivot" if beta else "double_dark_absorbed"
    require(actual == expected,
            ("two-sided rank formula changed", matrix, g, h, alpha,
             actual, expected))
    return {
        "base_rank": r,
        "anchor_visible": anchor_visible,
        "cartan_visible": cartan_visible,
        "beta": None if beta is None else str(beta),
        "bordered_rank": actual,
        "rank_jump": actual - r,
        "branch": branch,
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))

    counts = {}
    checked = 0
    for entries in product((-1, 0, 1), repeat=4):
        matrix = (entries[:2], entries[2:])
        for g in product((-1, 0, 1), repeat=2):
            for h in product((-1, 0, 1), repeat=2):
                for alpha in (-1, 0, 1):
                    record = classify(matrix, g, h, alpha)
                    counts[record["branch"]] = counts.get(
                        record["branch"], 0) + 1
                    checked += 1

    bare_external_guard = classify(((0,),), g=(1,), h=(0,), alpha=0)
    require(bare_external_guard["branch"] == "split_visible_rank_one",
            "bare external Cartan guard changed")
    triangular_guard = classify(
        ((1, -1), (2, -2)), g=(0, 0), h=(1, 0), alpha=-1)
    require(triangular_guard["rank_jump"] == 1,
            "pure triangular guard stopped being one-sided")
    coupled = classify(
        ((1, -1), (2, -2)), g=(1, 0), h=(1, 0), alpha=0)
    require(coupled["branch"] == "double_visible_rank_two",
            "coupled anchor-Cartan block stopped gaining two ranks")

    ledger = {
        "pins": PINS,
        "small_packets_checked": checked,
        "branches": counts,
        "bare_external_guard": bare_external_guard,
        "pure_triangular_guard": triangular_guard,
        "coupled_example": coupled,
        "theorem": (
            "for A=[[M,g],[h,alpha]], let a record h nonzero on ker M and "
            "b record g nonzero in coker M.  If a=b=1 then rank A=rank M+2. "
            "If exactly one is one, rank rises by one.  If both vanish, "
            "write g=My and h=lambda M; the sole remaining scalar is "
            "beta=alpha-h(y)=alpha-lambda(g), and rank rises exactly when "
            "beta is nonzero"
        ),
        "proof_consequence": (
            "the rank-two double-visible branch is the coupled minor which "
            "can feed the localized interference unit.  A bare external "
            "Cartan column has only a one-rank left separator and is not a "
            "source unit without additional physical terminal/Fitting or "
            "normalized-target typing.  Thus anchor visibility cannot be "
            "removed by invoking the abstract column-membership alternative"
        ),
        "scope": (
            "this is exact field linear algebra.  Physical use still needs "
            "M,g,h,alpha in one complete augmented grade and a theorem "
            "landing the nonzero coupled minor or the one-sided separator"
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
    print("two-sided rectangular anchor-Cartan rank table: PASS")
    print("small packets:", ledger["small_packets_checked"])
    print("branches:", ledger["branches"])
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
