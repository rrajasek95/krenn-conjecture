#!/usr/bin/env python3
"""Isolate the one-dimensional balanced-only determinant debt at h=3.

The six colour-unbalanced K3,3 determinant covectors span only four of the
five alternating matching directions.  The four balanced determinants add
exactly one common quotient class.  A small rational physical row has zero
hafnian and zero unbalanced determinants while every balanced determinant is
three, so the last class is a genuine local source-row geometry.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py":
        "ba2c32a41b1d070d2af24546819e838697aba0273e85586a796ee25a27f5a950",
    "computations/verify_h3_evaluated_determinant_transverse_landing_reduction.py":
        "73b7a1249c9856c4ac79e0c82a5bf8c024261d85199eef1781a51d4848732ca5",
}
EXPECTED_LEDGER_SHA256 = "1ba2fd09c0185a7cdfb96d348f33638cff6f0e5fd2c99e5dd988aff7b97bda50"


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None, relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rank(rows: list[tuple[Q, ...]]) -> int:
    if not rows:
        return 0
    work = [list(map(Q, row)) for row in rows]
    columns = len(work[0])
    require(all(len(row) == columns for row in work), "ragged matrix")
    pivot = 0
    for column in range(columns):
        found = next((row for row in range(pivot, len(work))
                      if work[row][column]), None)
        if found is None:
            continue
        work[pivot], work[found] = work[found], work[pivot]
        value = work[pivot][column]
        work[pivot] = [entry / value for entry in work[pivot]]
        for row in range(len(work)):
            if row == pivot or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right
                         for left, right in zip(work[row], work[pivot],
                                                strict=True)]
        pivot += 1
        if pivot == len(work):
            break
    return pivot


def det3(matrix: tuple[tuple[Q, ...], ...]) -> Q:
    a, b, c = matrix
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, (relative, actual))

    tangent = load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "balanced_only_tangent")
    determinants = tuple(tangent.cut_determinant(cut)
                         for cut in tangent.CUTS)
    balanced = tuple(index for index, cut in enumerate(tangent.CUTS)
                     if sorted(tangent.WORD[site] for site in cut)
                     == [0, 1, 2])
    unbalanced = tuple(index for index in range(len(tangent.CUTS))
                       if index not in balanced)
    unbalanced_rows = [determinants[index] for index in unbalanced]
    balanced_rows = [determinants[index] for index in balanced]

    require(len(balanced) == 4 and len(unbalanced) == 6,
            "the colour-cut split changed")
    require(rank(unbalanced_rows) == rank(balanced_rows) == 4
            and rank(list(determinants)) == 5,
            "the determinant span ranks changed")
    base = balanced_rows[0]
    require(rank(unbalanced_rows + [base]) == 5,
            "the balanced quotient class vanished")
    for row in balanced_rows[1:]:
        difference = tuple(left - right
                           for left, right in zip(row, base, strict=True))
        require(rank(unbalanced_rows + [difference]) == 4,
                "balanced determinants stopped sharing one quotient class")

    # Edge order is the lexicographic order used by tangent.EDGES.
    values = (-1, 1, 1, -1, -1, 0, 0, -1, -1,
              -1, -1, -1, -1, -1, 0)
    edges = tuple(combinations(tangent.SITES, 2))
    require(len(values) == len(edges) == 15,
            "the six-site edge inventory changed")
    edge_value = dict(zip(edges, map(Q, values), strict=True))

    def matching_value(matching):
        answer = Q(1)
        for edge in matching:
            answer *= edge_value[edge]
        return answer

    occurrence_values = tuple(matching_value(matching)
                              for matching in tangent.MATCHINGS)
    hafnian = sum(occurrence_values, Q(0))
    determinant_values = tuple(
        sum((coefficient * occurrence
             for coefficient, occurrence in zip(row, occurrence_values,
                                                  strict=True)), Q(0))
        for row in determinants)
    balanced_values = tuple(determinant_values[index] for index in balanced)
    unbalanced_values = tuple(determinant_values[index]
                              for index in unbalanced)
    require(hafnian == 0 and not any(unbalanced_values)
            and balanced_values == (Q(3),) * 4,
            "the balanced-only rational guard changed")

    ledger = {
        "pins": PINS,
        "word": "001122",
        "matching_module": "1 + 9 + 5",
        "balanced_cuts": [list(tangent.CUTS[index]) for index in balanced],
        "unbalanced_cuts": [list(tangent.CUTS[index]) for index in unbalanced],
        "determinant_ranks": {
            "balanced": rank(balanced_rows),
            "unbalanced": rank(unbalanced_rows),
            "joint": rank(list(determinants)),
            "balanced_mod_unbalanced": 1,
        },
        "balanced_quotient_identity": (
            "all four balanced determinant covectors are equal modulo the "
            "span of the six unbalanced determinant covectors"
        ),
        "rational_guard": {
            "edge_order": [f"{a}{b}" for a, b in edges],
            "edge_values": list(values),
            "hafnian": int(hafnian),
            "unbalanced_determinants": list(map(int, unbalanced_values)),
            "balanced_determinants": list(map(int, balanced_values)),
        },
        "proof_frontier": (
            "determinant-dark gives the filtered comparison; nonzero "
            "unbalanced determinant gives the offdiagonal fan; the remaining "
            "one-dimensional balanced class is a diagonal-lock/anchor-web "
            "entry and is not closed by the fan theorem"
        ),
        "scope": (
            "exact physical mixed-row guard, not a complete ternary GHZ "
            "source and not a proof that the balanced class survives all "
            "other source rows"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256, digest)
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("balanced determinant quotient dimension: 1")
    print("rational hafnian-zero balanced-only guard: PASS")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
