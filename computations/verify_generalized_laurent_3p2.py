#!/usr/bin/env python3
"""Solver-independent audit of one generalized-Laurent 3P2 certificate.

The support chart below was first found by the residual-support SAT search,
but this verifier does not invoke a solver.  It reconstructs every supported
perfect-matching monomial directly from the displayed matrix/factor supports,
checks the elementary support axioms, and then runs the exact Laurent checker.

The certificate proves only that this particular support chart cannot be
realized by nonzero complex entries.  It is a regression test for the reusable
``generalized_laurent_elimination`` engine, not an exhaustion of all 3P2
support charts.
"""

from __future__ import annotations

from fractions import Fraction

import generalized_laurent_elimination as laurent
import search_f5_support_sat as base
import verify_f4_support_obstruction as previous


EXCEPTIONAL = {(0, 1), (2, 3), (4, 5)}

# For an oriented rank-one matrix on edge u<v, the two tuples are the
# supports of its factor at u and at v, respectively.
RANK_ONE_SUPPORTS = {
    (0, 2): ((0,), (0,)),
    (0, 3): ((2,), (2,)),
    (0, 4): ((0,), (1,)),
    (0, 5): ((0, 1, 2), (0, 1, 2)),
    (1, 2): ((1,), (0,)),
    (1, 3): ((0, 1, 2), (0, 1, 2)),
    (1, 4): ((2,), (2,)),
    (1, 5): ((1,), (1,)),
    (2, 4): ((0, 1, 2), (0, 1, 2)),
    (2, 5): ((2,), (2,)),
    (3, 4): ((1,), (1,)),
    (3, 5): ((0,), (0,)),
}

EXPECTED_POWERS = {
    (0, 0, 0, 0, 1, 0): ((0, 1, 3, 13), (-1, 1), Fraction(1)),
    (0, 2, 0, 0, 2, 1): ((0, 3, 13, 14), (1, 1), Fraction(-1)),
    (0, 2, 1, 0, 2, 0): ((0, 1, 13, 14), (-1, 1), Fraction(1)),
}


def factor_support_at(edge: tuple[int, int], vertex: int) -> tuple[int, ...]:
    u, v = edge
    assert vertex in edge and edge in RANK_ONE_SUPPORTS
    return RANK_ONE_SUPPORTS[edge][0 if vertex == u else 1]


def monomial_supported(
    coloring: tuple[int, ...], matching: tuple[tuple[int, int], ...]
) -> bool:
    for edge in matching:
        if edge in EXCEPTIONAL:
            # Every entry of each of the three exceptional matrices is in
            # this chart's support.
            continue
        u, v = edge
        if coloring[u] not in factor_support_at(edge, u):
            return False
        if coloring[v] not in factor_support_at(edge, v):
            return False
    return True


def chart_fibers():
    return {
        coloring: tuple(
            index
            for index, matching in enumerate(base.MATCHINGS)
            if monomial_supported(coloring, matching)
        )
        for coloring in base.COLORINGS
    }


def audit_support_chart(fibers) -> None:
    assert set(RANK_ONE_SUPPORTS) == set(base.ALL_EDGES) - EXCEPTIONAL
    assert all(first and second for first, second in RANK_ONE_SUPPORTS.values())

    # Forced-anchor condition: for every ordered (tail, color), some
    # rank-one edge has exactly that singleton as the factor at its head.
    for tail in base.VERTICES:
        for color in base.COLORS:
            assert any(
                factor_support_at(tuple(sorted((tail, head))), head) == (color,)
                for head in base.VERTICES
                if head != tail
                and tuple(sorted((tail, head))) not in EXCEPTIONAL
            )

    # Constant fibers are nonempty; a mixed coefficient never has exactly
    # one nonzero matching monomial.
    for coloring, supported in fibers.items():
        if len(set(coloring)) == 1:
            assert supported
        else:
            assert len(supported) != 1


def main() -> None:
    fibers = chart_fibers()
    audit_support_chart(fibers)

    # ``formal_signatures`` does not inspect its legacy pool argument.  No
    # clauses are built and no SAT solver is called in this verifier.
    signatures = previous.formal_signatures(EXCEPTIONAL, None)

    relations = laurent.binomial_relations_from_fibers(signatures, fibers)
    quotient = laurent.BinomialQuotient(relations)
    assert len(quotient.basis_relations) == 25
    assert quotient.audit_binomial_character() is None

    conflict = laurent.generalized_laurent_conflict_from_fibers(
        signatures, fibers
    )
    assert conflict is not None
    assert conflict.kind == "multiplicative-power"
    assert conflict.coefficients == (-1, -1, 1)
    assert conflict.scalar == -1
    assert len(conflict.power_relations) == 3

    for power in conflict.power_relations:
        supported, class_sums, value = EXPECTED_POWERS[power.coloring]
        assert power.supported == supported
        assert power.class_sums == class_sums
        assert power.value == value

    first, second, third = conflict.power_relations
    assert all(
        -a - b + c == 0
        for a, b, c in zip(
            first.exponent, second.exponent, third.exponent, strict=True
        )
    )
    assert (
        first.value ** -1 * second.value ** -1 * third.value
        == conflict.scalar
        == -1
    )

    print("verified solver-independent 3P2 generalized-Laurent certificate")
    print("binomial quotient rank: 25 (selected minor determinant +/-1)")
    for power in conflict.power_relations:
        print(
            f"power fiber {power.coloring}: support={power.supported}, "
            f"class sums={power.class_sums}, value={power.value}"
        )
    print("exponent dependency: -e1-e2+e3=0")
    print("scalar dependency: 1^(-1) (-1)^(-1) 1 = -1 != 1")


if __name__ == "__main__":
    main()
