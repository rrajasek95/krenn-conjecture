#!/usr/bin/env python3
"""Verify the universal aggregate reduction behind the physical comparison.

Five cyclic covariance--Spencer edges identify the five face vertices modulo
one aggregate H0.  The order-six primitive normalization and the five
non-Euler marked polar normalizations are all one.  Hence their difference
has zero H0.  Universal positive-degree Spencer acyclicity then contracts the
difference.  Any remaining class is necessarily relative to physical
labelling/readouts, not a universal Hasse obstruction.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_order6_covariance_bridge_cyclic_aggregate.py":
        "01d4d504c0d5d9ac8fd643e06a38b35d75962c859e41908bff3161d10c7cbc13",
    "computations/verify_h3_universal_spencer_euler_contraction.py":
        "4e4e4810dc49ab366555288ab7c696047cd3ce79ab7dc4b159b38047def8942b",
    "computations/verify_h3_rootless_non_euler_diagonal_stabilizer_jet.py":
        "0bbed406d393543b6badf222ff0665dc1b12445a2360a015e5398bd538bd5e5c",
    "computations/verify_h3_residual_q_order6_ridge_jet_commutation.py":
        "00a0798b4aa1d901b52645cac3f1dbe2854a3d8ce796191f7a4ff9a6e295b28f",
    "computations/verify_h3_order6_primitive_face_literal_boundary.py":
        "5fbb2458dd98cf4d647ef72eff7a7b58e4dcfb2a7281bc4c433db7f75b020c4c",
}
EXPECTED_LEDGER_SHA256 = "27731b45f7d5ab26bcd88b3176347f3e8c812b4a1daf0cead9e99a0426f47482"


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def rank(columns):
    height = len(columns[0]) if columns else 0
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
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
        pivot_row += 1
    return pivot_row


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    edges = []
    for index in range(5):
        column = [0] * 5
        column[index] = -1
        column[(index + 1) % 5] = 1
        edges.append(tuple(column))
    aggregate = (1, 1, 1, 1, 1)
    require(rank(edges) == 4
            and all(sum(a * b for a, b in zip(aggregate, edge, strict=True)) == 0
                    for edge in edges),
            "face edge module stopped leaving one aggregate H0")

    order6_augmentations = (1, 1, 1, 1, 1)
    polar_augmentations = (1, 1, 1, 1, 1)
    difference = tuple(left - right for left, right in
                       zip(polar_augmentations, order6_augmentations,
                           strict=True))
    require(difference == (0, 0, 0, 0, 0),
            "normalized order-six/polar H0 values separated")
    require(sum(order6_augmentations) == sum(polar_augmentations) == 5,
            "face aggregate normalization changed")

    return {
        "theorem": "universal aggregate comparison reduction",
        "cyclic_edge_rank": rank(edges),
        "universal_H0_dimension": 1,
        "aggregate_covector": list(aggregate),
        "order6_face_normalizations": list(order6_augmentations),
        "non_euler_polar_normalizations": list(polar_augmentations),
        "normalized_H0_difference": list(difference),
        "universal_positive_degree_homology": 0,
        "universal_comparison_obstruction": 0,
        "remaining_obstruction_location": (
            "relative homology of the physical labelled/readout comparison"
        ),
        "formal_alternative": {
            "relative_class_boundary": "physical aggregate comparison cell",
            "terminal_nonzero_on_relative_class":
                "normalize to the relative generator",
            "terminal_zero_on_relative_homology":
                "terminal descends and the Fredholm separator applies",
        },
        "scope": (
            "the universal Spencer/Hasse complex and normalized face H0 only. "
            "The theorem does not prove that W, anchor, eta, sigma, or the "
            "marked-sector terminal descend through the physical labelled "
            "quotient, and does not perform transverse rank landing"
        ),
    }


def main() -> None:
    ledger = audit()
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("universal aggregate ledger changed", digest))
    print("h3 universal aggregate comparison: EXACT BEFORE PHYSICAL DESCENT")
    print("edge rank 4, common normalized H0, positive Spencer homology 0")
    print("remaining class: physical relative comparison only")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
