#!/usr/bin/env python3
"""Exact counterexample to the full 1,680 balanced-contrast radical route."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_full_contrast_radical_counterexample.json"
N = 8
P = (1, 0)
Q = (0, 1)
R = (-1, 1)
DIRECTIONS = (P, Q, R)


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def matchings(vertices=tuple(range(N))):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for i in range(1, len(vertices)):
        v = vertices[i]
        rest = vertices[1:i] + vertices[i + 1:]
        for tail in matchings(rest):
            yield ((u, v),) + tail


PM8 = tuple(matchings())
EDGES = tuple((u, v) for u in range(N) for v in range(u + 1, N))
BASE = ((1, 0), (0, 0))
EXCEPTION = ((1, 1), (0, 0))


def assignments() -> tuple[tuple[int, ...], ...]:
    answer = []
    for counts in ((3, 3, 2), (3, 2, 3), (2, 3, 3)):
        seed = tuple(direction for direction, count in enumerate(counts)
                     for _ in range(count))
        answer.extend(sorted(set(permutations(seed))))
    return tuple(answer)


ASSIGNMENTS = assignments()


def bilinear(left: tuple[int, int], block: tuple[tuple[int, int], ...],
             right: tuple[int, int]) -> int:
    return sum(left[i] * block[i][j] * right[j]
               for i in range(2) for j in range(2))


def amplitude(assignment: tuple[int, ...],
              exceptional_edges=((0, 1),)) -> int:
    exceptional = set(exceptional_edges)
    answer = 0
    for matching in PM8:
        term = 1
        for edge in matching:
            block = EXCEPTION if edge in exceptional else BASE
            term *= bilinear(DIRECTIONS[assignment[edge[0]]], block,
                             DIRECTIONS[assignment[edge[1]]])
        answer += term
    return answer


def all_same(direction: tuple[int, int]) -> int:
    answer = 0
    for matching in PM8:
        term = 1
        for edge in matching:
            block = EXCEPTION if edge == (0, 1) else BASE
            term *= bilinear(direction, block, direction)
        answer += term
    return answer


def main() -> None:
    require(len(PM8) == 105 and len(ASSIGNMENTS) == 1680,
            "matching or balanced-assignment census changed")
    values = tuple(amplitude(assignment) for assignment in ASSIGNMENTS)
    require(Counter(values) == {0: 1680},
            "balanced contractions do not all vanish")
    a, b, c = (all_same(direction) for direction in DIRECTIONS)
    require((a, b, c) == (105, 0, 90),
            "pure contrast Hafnians changed")
    factors = (a + b - c, a + c - b, b + c - a)
    heron = factors[0] * factors[1] * factors[2]
    require(factors == (15, 195, -15) and heron == -43_875,
            "Heron target changed or vanished")

    # Raw 3x3 realization: every edge has only x[1,1]=1, while edge 01
    # additionally has x[1,2]=1.  With p=e0-e1 and q=e0-e2 this restricts
    # to BASE and EXCEPTION respectively on the contrast plane.
    raw_base = [[0] * 3 for _ in range(3)]
    raw_base[1][1] = 1
    raw_exception = [row[:] for row in raw_base]
    raw_exception[1][2] = 1
    raw_directions = ((1, -1, 0), (1, 0, -1))
    restricted = []
    for raw in (raw_base, raw_exception):
        restricted.append(tuple(tuple(
            sum(raw_directions[i][u] * raw[u][v] * raw_directions[j][v]
                for u in range(3) for v in range(3))
            for j in range(2)) for i in range(2)))
    require(tuple(restricted) == (BASE, EXCEPTION),
            "raw 3x3 realization does not restrict to the claimed blocks")

    # A second exceptional edge supplies two q slots and must make the
    # termwise-vanishing argument fail for at least one balanced assignment.
    mutated = tuple(amplitude(assignment, ((0, 1), (2, 3)))
                    for assignment in ASSIGNMENTS)
    require(any(value != 0 for value in mutated),
            "two-slot mutation did not fire")

    result = {
        "status": "UNAUDITED exact full balanced-contrast counterexample",
        "balanced_assignments": len(ASSIGNMENTS),
        "balanced_value_histogram": {"0": len(ASSIGNMENTS)},
        "base_block_pq": BASE,
        "exception_edge": [0, 1],
        "exception_block_pq": EXCEPTION,
        "raw_base_nonzero_cells": [[1, 1, 1]],
        "raw_exception_additional_cells": [[1, 2, 1]],
        "pure_contrast_hafnians": [a, b, c],
        "Heron_factors": list(factors),
        "Heron": heron,
        "two_exception_edge_mutation_nonzero_count":
            sum(value != 0 for value in mutated),
        "conclusion": (
            "The complete S3-stable 1,680-generator balanced-contrast ideal "
            "has a rational common zero with nonzero Heron target.  Hence "
            "the Heron cubic is not in its radical and no target power can "
            "be proved using only these contractions."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("full balanced-contrast radical counterexample: PASS")
    print("A,B,C / Heron:", (a, b, c), heron)
    print("mutation nonzero count:",
          result["two_exception_edge_mutation_nonzero_count"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
