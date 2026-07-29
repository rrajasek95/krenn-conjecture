#!/usr/bin/env python3
"""Solver-independent four-fiber Laurent certificates for both F=2 graphs.

Each displayed support chart has two full exceptional matrices.  Three exact
binomial fibers force two terms of one exact trinomial fiber to cancel, so
the remaining supported Laurent monomial would have to be zero.  The script
reconstructs all matching supports from the chart and checks the exponent
identities over the integers; it builds no SAT formula and calls no solver.

These are certificates for two individual charts, not exhaustive proofs for
the two graph isomorphism types.  The dynamic CEGAR audit supplies the latter.
"""

from __future__ import annotations

from dataclasses import dataclass

import search_f5_support_sat as base
import verify_f4_support_obstruction as previous


FULL = (0, 1, 2)


@dataclass(frozen=True)
class Certificate:
    name: str
    exceptional: frozenset[tuple[int, int]]
    factors: dict[tuple[int, int], tuple[tuple[int, ...], tuple[int, ...]]]
    target_coloring: tuple[int, ...]
    target_support: tuple[int, int, int]
    cancel_pair: tuple[int, int]
    source_colorings: tuple[tuple[int, ...], ...]
    source_support: tuple[int, int]
    coefficients: tuple[int, ...]


CERTIFICATES = (
    Certificate(
        "2P2+2P1",
        frozenset({(0, 1), (2, 3)}),
        {
            (0, 2): ((0,), (1,)),
            (0, 3): ((1,), (0,)),
            (0, 4): ((2,), (2,)),
            (0, 5): (FULL, FULL),
            (1, 2): ((1,), (0,)),
            (1, 3): ((2,), (2,)),
            (1, 4): (FULL, FULL),
            (1, 5): ((0,), (1,)),
            (2, 4): (FULL, FULL),
            (2, 5): ((2,), (2,)),
            (3, 4): ((0,), (0,)),
            (3, 5): (FULL, FULL),
            (4, 5): ((1,), (1,)),
        },
        (0, 0, 0, 0, 1, 1),
        (0, 1, 14),
        (1, 14),
        (
            (0, 0, 0, 0, 0, 1),
            (0, 0, 0, 0, 0, 2),
            (0, 0, 0, 0, 1, 2),
        ),
        (1, 14),
        (-1, 1, -1),
    ),
    Certificate(
        "P3+3P1",
        frozenset({(0, 1), (1, 2)}),
        {
            (0, 2): ((1,), (0,)),
            (0, 3): ((0,), (1,)),
            (0, 4): (FULL, FULL),
            (0, 5): ((2,), (2,)),
            (1, 3): ((1,), (0,)),
            (1, 4): ((2,), (2,)),
            (1, 5): ((0,), (1,)),
            (2, 3): ((2,), (2,)),
            (2, 4): ((0,), (0,)),
            (2, 5): (FULL, FULL),
            (3, 4): (FULL, FULL),
            (3, 5): (FULL, FULL),
            (4, 5): ((1,), (1,)),
        },
        (0, 0, 0, 0, 0, 1),
        (1, 2, 9),
        (2, 9),
        (
            (0, 0, 0, 0, 1, 1),
            (0, 0, 1, 0, 0, 0),
            (0, 0, 1, 0, 1, 0),
        ),
        (2, 9),
        (-1, -1, 1),
    ),
)


def factor_at(certificate: Certificate, edge, vertex):
    u, v = edge
    return certificate.factors[edge][0 if vertex == u else 1]


def monomial_supported(certificate: Certificate, coloring, matching):
    for edge in matching:
        if edge in certificate.exceptional:
            # Both exceptional matrices have full 3x3 support.
            continue
        u, v = edge
        if coloring[u] not in factor_at(certificate, edge, u):
            return False
        if coloring[v] not in factor_at(certificate, edge, v):
            return False
    return True


def chart_fibers(certificate: Certificate):
    return {
        coloring: tuple(
            index
            for index, matching in enumerate(base.MATCHINGS)
            if monomial_supported(certificate, coloring, matching)
        )
        for coloring in base.COLORINGS
    }


def audit_chart(certificate: Certificate, fibers) -> None:
    assert set(certificate.factors) == (
        set(base.ALL_EDGES) - certificate.exceptional
    )
    assert all(first and second for first, second in certificate.factors.values())

    # The necessary forced-anchor condition is checked independently of the
    # four fibers used below.
    for tail in base.VERTICES:
        for color in base.COLORS:
            assert any(
                factor_at(certificate, tuple(sorted((tail, head))), head)
                == (color,)
                for head in base.VERTICES
                if head != tail
                and tuple(sorted((tail, head))) not in certificate.exceptional
            )

    for coloring, supported in fibers.items():
        if len(set(coloring)) == 1:
            assert supported
        else:
            assert len(supported) != 1

    assert fibers[certificate.target_coloring] == certificate.target_support
    for coloring in certificate.source_colorings:
        assert fibers[coloring] == certificate.source_support


def audit_certificate(certificate: Certificate) -> None:
    fibers = chart_fibers(certificate)
    audit_chart(certificate, fibers)
    signatures = previous.formal_signatures(set(certificate.exceptional), None)

    first_source, second_source = certificate.source_support
    differences = []
    for coloring in certificate.source_colorings:
        differences.append(
            tuple(
                first - second
                for first, second in zip(
                    signatures[coloring, first_source],
                    signatures[coloring, second_source],
                    strict=True,
                )
            )
        )

    first_target, second_target = certificate.cancel_pair
    target_difference = tuple(
        second - first
        for first, second in zip(
            signatures[certificate.target_coloring, first_target],
            signatures[certificate.target_coloring, second_target],
            strict=True,
        )
    )
    combined = tuple(
        sum(
            coefficient * difference[position]
            for coefficient, difference in zip(
                certificate.coefficients, differences, strict=True
            )
        )
        for position in range(len(target_difference))
    )
    assert combined == target_difference
    assert sum(certificate.coefficients) % 2 == 1

    # Each source says x^difference=-1.  The odd combination therefore says
    # target-term(second)/target-term(first)=-1.  Those two terms cancel in
    # the target trinomial, leaving its third, supported, nonzero monomial.
    leftover = next(
        index
        for index in certificate.target_support
        if index not in certificate.cancel_pair
    )
    assert len(set(certificate.target_support) - set(certificate.cancel_pair)) == 1
    print(
        f"verified {certificate.name}: coefficients={certificate.coefficients}, "
        f"sum={sum(certificate.coefficients)} odd; target matchings "
        f"{first_target},{second_target} cancel, leaving {leftover}"
    )


def main() -> None:
    for certificate in CERTIFICATES:
        audit_certificate(certificate)
    print("verified both solver-independent four-fiber F=2 certificates")


if __name__ == "__main__":
    main()
