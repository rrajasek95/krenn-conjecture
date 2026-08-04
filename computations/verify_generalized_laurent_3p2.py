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

Two independent contradictions are audited here.

* On the full fiber dictionary the engine reports a ``zero-constant-fiber``
  conflict: the constant coloring ``(1,1,1,1,1,1)`` has exactly two supported
  matchings whose Laurent classes cancel, so this chart forces a target
  coordinate that must equal one to vanish.  That branch returns before any
  power relation is collected, which is why the multiplicative certificate
  recorded in ``proofs/representative-low-rank-laurent-certificates.md`` is
  not what a single full-fiber call returns.
* Restricted to the mixed colorings the engine reports the recorded
  ``multiplicative-power`` conflict on the three four-term fibers.  The
  binomial quotient is unchanged by that restriction, because
  ``binomial_relations_from_fibers`` already skips constant colorings, so the
  two audits share one and the same rank-25 unimodular lattice.

Every check below raises instead of asserting.  A bare ``assert`` is deleted
by ``python3 -O``, which would leave this verifier printing its conclusion
without having checked anything.
"""

from __future__ import annotations

from fractions import Fraction

import generalized_laurent_elimination as laurent
import search_f5_support_sat as base
import verify_f4_support_obstruction as previous


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise RuntimeError(message)


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

# The constant coloring whose two supported matchings cancel outright.
ZERO_CONSTANT_FIBER = ((1, 1, 1, 1, 1, 1), (0, 13))


def factor_support_at(edge: tuple[int, int], vertex: int) -> tuple[int, ...]:
    u, v = edge
    require(
        vertex in edge and edge in RANK_ONE_SUPPORTS,
        f"edge {edge} has no recorded rank-one factor at vertex {vertex}",
    )
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
    require(
        set(RANK_ONE_SUPPORTS) == set(base.ALL_EDGES) - EXCEPTIONAL,
        "the rank-one edge set is not the complement of the exceptional edges",
    )
    require(
        all(first and second for first, second in RANK_ONE_SUPPORTS.values()),
        "a rank-one edge has an empty endpoint factor support",
    )

    # Forced-anchor condition: for every ordered (tail, color), some
    # rank-one edge has exactly that singleton as the factor at its head.
    for tail in base.VERTICES:
        for color in base.COLORS:
            require(
                any(
                    factor_support_at(tuple(sorted((tail, head))), head)
                    == (color,)
                    for head in base.VERTICES
                    if head != tail
                    and tuple(sorted((tail, head))) not in EXCEPTIONAL
                ),
                f"no forced anchor of color {color} at vertex {tail}",
            )

    # Constant fibers are nonempty; a mixed coefficient never has exactly
    # one nonzero matching monomial.
    for coloring, supported in fibers.items():
        if len(set(coloring)) == 1:
            require(
                supported,
                f"constant fiber {coloring} has no supported matching",
            )
        else:
            require(
                len(supported) != 1,
                f"mixed fiber {coloring} is a singleton",
            )


def audit_quotient(signatures, fibers, expected_rank: int):
    relations = laurent.binomial_relations_from_fibers(signatures, fibers)
    quotient = laurent.BinomialQuotient(relations)
    require(
        len(quotient.basis_relations) == expected_rank,
        f"binomial quotient rank {len(quotient.basis_relations)} "
        f"!= {expected_rank}",
    )
    require(
        quotient.audit_binomial_character() is None,
        "a binomial relation fails its own character audit",
    )
    return quotient


def audit_zero_constant_fiber(signatures, fibers):
    """The full-fiber call returns the simpler vanishing-coordinate conflict."""

    conflict = laurent.generalized_laurent_conflict_from_fibers(
        signatures, fibers
    )
    require(conflict is not None, "no conflict on the full fiber dictionary")
    require(
        conflict.kind == "zero-constant-fiber",
        f"unexpected full-fiber conflict kind {conflict.kind!r}",
    )
    coloring, supported = ZERO_CONSTANT_FIBER
    require(
        conflict.coloring == coloring,
        f"the vanishing constant fiber is {conflict.coloring}, not {coloring}",
    )
    require(
        fibers[coloring] == supported,
        f"constant fiber {coloring} has support {fibers[coloring]}, "
        f"not {supported}",
    )
    require(
        conflict.scalar == 0,
        "the vanishing-coordinate conflict does not report scalar zero",
    )
    return conflict


def audit_multiplicative_power(signatures, fibers):
    """Restricted to mixed colorings, the recorded power certificate appears."""

    mixed = {
        coloring: supported
        for coloring, supported in fibers.items()
        if len(set(coloring)) > 1
    }
    # The quotient is built only from mixed two-term fibers, so dropping the
    # constant colorings leaves the very same rank-25 unimodular lattice.
    audit_quotient(signatures, mixed, 25)

    conflict = laurent.generalized_laurent_conflict_from_fibers(
        signatures, mixed
    )
    require(conflict is not None, "no conflict on the mixed fibers")
    require(
        conflict.kind == "multiplicative-power",
        f"unexpected mixed-fiber conflict kind {conflict.kind!r}",
    )
    require(
        conflict.coefficients == (-1, -1, 1),
        f"unexpected dependency coefficients {conflict.coefficients}",
    )
    require(conflict.scalar == -1, f"unexpected scalar {conflict.scalar}")
    require(
        len(conflict.power_relations) == 3,
        f"{len(conflict.power_relations)} power relations, expected 3",
    )

    for power in conflict.power_relations:
        require(
            power.coloring in EXPECTED_POWERS,
            f"unexpected power fiber {power.coloring}",
        )
        supported, class_sums, value = EXPECTED_POWERS[power.coloring]
        require(
            power.supported == supported,
            f"power fiber {power.coloring} has support {power.supported}",
        )
        require(
            power.class_sums == class_sums,
            f"power fiber {power.coloring} has class sums {power.class_sums}",
        )
        require(
            power.value == value,
            f"power fiber {power.coloring} has value {power.value}",
        )

    first, second, third = conflict.power_relations
    require(
        all(
            -a - b + c == 0
            for a, b, c in zip(
                first.exponent, second.exponent, third.exponent, strict=True
            )
        ),
        "the exponent dependency -e1-e2+e3=0 fails coordinatewise",
    )
    require(
        first.value ** -1 * second.value ** -1 * third.value
        == conflict.scalar
        == -1,
        "the matching scalar dependency is not 1^(-1) (-1)^(-1) 1 = -1",
    )
    return conflict


def main() -> None:
    fibers = chart_fibers()
    audit_support_chart(fibers)

    # ``formal_signatures`` does not inspect its legacy pool argument.  No
    # clauses are built and no SAT solver is called in this verifier.
    signatures = previous.formal_signatures(EXCEPTIONAL, None)

    audit_quotient(signatures, fibers, 25)
    zero_conflict = audit_zero_constant_fiber(signatures, fibers)
    power_conflict = audit_multiplicative_power(signatures, fibers)

    print("verified solver-independent 3P2 generalized-Laurent certificate")
    print("binomial quotient rank: 25 (selected minor determinant +/-1)")
    print(
        f"vanishing constant fiber {zero_conflict.coloring}: "
        f"support={fibers[zero_conflict.coloring]}, "
        "all Laurent classes cancel, so this coordinate is forced to zero"
    )
    for power in power_conflict.power_relations:
        print(
            f"power fiber {power.coloring}: support={power.supported}, "
            f"class sums={power.class_sums}, value={power.value}"
        )
    print("exponent dependency: -e1-e2+e3=0")
    print("scalar dependency: 1^(-1) (-1)^(-1) 1 = -1 != 1")


if __name__ == "__main__":
    main()
