#!/usr/bin/env python3
"""Solver-independent representative Laurent certificates for F=1 and F=0."""

from __future__ import annotations

import search_f5_support_sat as base
import verify_f4_support_obstruction as previous
from verify_small_laurent_f2_certificates import (
    Certificate,
    FULL,
    audit_certificate,
)


P2_CERTIFICATE = Certificate(
    "P2+4P1",
    frozenset({(0, 1)}),
    {
        (0, 2): (FULL, FULL),
        (0, 3): ((1,), (0,)),
        (0, 4): ((0,), (1,)),
        (0, 5): ((2,), (2,)),
        (1, 2): ((1,), (0,)),
        (1, 3): ((2,), (2,)),
        (1, 4): (FULL, FULL),
        (1, 5): ((0,), (1,)),
        (2, 3): (FULL, FULL),
        (2, 4): ((2,), (2,)),
        (2, 5): ((1,), (0,)),
        (3, 4): ((1,), (0,)),
        (3, 5): (FULL, FULL),
        (4, 5): (FULL, FULL),
    },
    (0, 0, 0, 0, 1, 1),
    (0, 4, 11),
    (0, 4),
    (
        (0, 0, 0, 0, 0, 1),
        (0, 0, 0, 0, 0, 2),
        (0, 0, 0, 0, 1, 2),
    ),
    (0, 4),
    (-1, 1, -1),
)


EMPTY_FACTORS = {
    (0, 1): ((1,), (1,)),
    (0, 2): ((0,), FULL),
    (0, 3): ((0,), FULL),
    (0, 4): ((0,), (0,)),
    (0, 5): ((2,), (2,)),
    (1, 2): ((2,), FULL),
    (1, 3): ((2,), FULL),
    (1, 4): ((2,), (2,)),
    (1, 5): ((0,), (0,)),
    (2, 3): ((1, 2), (0, 2)),
    (2, 4): (FULL, FULL),
    (2, 5): (FULL, (1,)),
    (3, 4): (FULL, FULL),
    (3, 5): (FULL, (1,)),
    (4, 5): ((1,), (1,)),
}

EMPTY_BINOMIALS = (
    ((0, 2, 0, 0, 0, 1), (9, 10)),
    ((0, 2, 0, 0, 1, 1), (3, 6)),
    ((0, 2, 0, 0, 2, 1), (4, 7)),
)
EMPTY_COEFFICIENTS = (-1, -1, 1)


def empty_factor_at(edge, vertex):
    u, _v = edge
    return EMPTY_FACTORS[edge][0 if vertex == u else 1]


def empty_fibers():
    answer = {}
    for coloring in base.COLORINGS:
        supported = []
        for index, matching in enumerate(base.MATCHINGS):
            if all(
                coloring[u] in empty_factor_at(edge, u)
                and coloring[v] in empty_factor_at(edge, v)
                for edge in matching
                for u, v in (edge,)
            ):
                supported.append(index)
        answer[coloring] = tuple(supported)
    return answer


def audit_empty_chart() -> None:
    assert set(EMPTY_FACTORS) == set(base.ALL_EDGES)
    fibers = empty_fibers()

    for tail in base.VERTICES:
        for color in base.COLORS:
            assert any(
                empty_factor_at(tuple(sorted((tail, head))), head) == (color,)
                for head in base.VERTICES
                if head != tail
            )
    for coloring, supported in fibers.items():
        if len(set(coloring)) == 1:
            assert supported
        else:
            assert len(supported) != 1
    for coloring, supported in EMPTY_BINOMIALS:
        assert fibers[coloring] == supported

    signatures = previous.formal_signatures(set(), None)
    differences = []
    for coloring, (first, second) in EMPTY_BINOMIALS:
        differences.append(
            tuple(
                a - b
                for a, b in zip(
                    signatures[coloring, first],
                    signatures[coloring, second],
                    strict=True,
                )
            )
        )
    combined = tuple(
        sum(
            coefficient * difference[position]
            for coefficient, difference in zip(
                EMPTY_COEFFICIENTS, differences, strict=True
            )
        )
        for position in range(len(differences[0]))
    )
    assert not any(combined)
    assert sum(EMPTY_COEFFICIENTS) % 2 == 1
    print(
        "verified 6P1: three binomial differences have coefficients "
        "(-1,-1,1), zero exponent sum, and odd sign"
    )


def main() -> None:
    audit_certificate(P2_CERTIFICATE)
    audit_empty_chart()
    print("verified solver-independent representative F=1 and F=0 certificates")


if __name__ == "__main__":
    main()
