#!/usr/bin/env python3
"""Exact branch solver for factorized Laurent remainders.

After quotienting by all exact mixed binomials, a four-class Laurent
polynomial can sometimes factor as a monomial times two binomials.  Its
vanishing is then the finite disjunction that at least one binomial factor
vanishes.  This module solves all such disjunctions exactly when the factor
constants are signs.  Every Boolean branch is checked by the same signed
integer HNF and group-algebra pure-product test used by the toric searches.

The result is deliberately only a sufficient/exhaustive test for charts in
which *every* nonzero remainder has the supported rectangle factorization.
It makes no claim about an unfactorized residual polynomial.
"""

from __future__ import annotations

from dataclasses import dataclass

from pysat.solvers import Solver

import search_parallel_binomial_nonzero_constants_cegar as toric


@dataclass(frozen=True)
class FactorizedBranchResult:
    status: str
    lattice: object | None
    selected_factors: tuple[int, ...]
    factors: tuple[tuple[tuple[int, ...], int], ...]
    clauses: tuple[tuple[int, ...], ...]
    branches: int
    inconsistent_branches: int
    pure_zero_branches: int


def normalize_factor(exponent, rhs_bit):
    """Normalize ``x**exponent=(-1)**rhs_bit`` up to inversion."""

    exponent = tuple(exponent)
    opposite = tuple(-value for value in exponent)
    return (opposite if opposite < exponent else exponent, int(rhs_bit))


def rectangle_factor_pair(remainder):
    """Return two signed binomial factors of a four-term rectangle.

    ``remainder`` maps exponent vectors to nonzero integer coefficients.
    The returned factor ``(d,b)`` means ``x**d=(-1)**b``.  ``None`` means
    that the polynomial is not a coefficient-compatible exponent rectangle
    with sign-valued factor constants.
    """

    if len(remainder) != 4:
        return None
    items = list(remainder.items())
    for first, opposite in ((0, 1), (0, 2), (0, 3)):
        remaining = [index for index in range(4)
                     if index not in (first, opposite)]
        adjacent_left, adjacent_right = remaining
        e00, c00 = items[first]
        e11, c11 = items[opposite]
        e01, c01 = items[adjacent_left]
        e10, c10 = items[adjacent_right]
        if tuple(a + b for a, b in zip(e00, e11)) != tuple(
            a + b for a, b in zip(e01, e10)
        ):
            continue
        if c00 * c11 != c01 * c10:
            continue
        # Factoring after removing c00*x**e00 gives constants
        # c01/c00 and c10/c00.  They define signed binomials precisely
        # when the corresponding absolute coefficients agree.
        if abs(c00) != abs(c01) or abs(c00) != abs(c10):
            continue
        left = normalize_factor(
            (a - b for a, b in zip(e01, e00)), c00 == c01
        )
        right = normalize_factor(
            (a - b for a, b in zip(e10, e00)), c00 == c10
        )
        return left, right
    return None


def _minimal_cover(selected, clauses):
    """Greedily delete redundant true factor variables."""

    selected = set(selected)
    for factor in sorted(tuple(selected)):
        trial = selected - {factor}
        if all(any(item in trial for item in clause) for clause in clauses):
            selected = trial
    assert all(any(item in selected for item in clause) for clause in clauses)
    return tuple(sorted(selected))


def solve_factorized_branches(
    remainders,
    base_rows,
    fibres,
    size,
    cells,
    cell_index,
    solver_name="cadical300",
    base_rhs=None,
):
    """Exhaust all signed-binomial factor branches exactly.

    Return status ``unfactorized`` if even one residual is outside the
    supported rectangle class, ``survivor`` if a branch has a nonzero pure
    product, and ``exhausted`` if every branch is inconsistent or forces the
    pure product to zero.
    """

    factor_pairs = []
    if base_rhs is None:
        base_rhs = [1] * len(base_rows)
    else:
        base_rhs = list(base_rhs)
        assert len(base_rhs) == len(base_rows)
    all_factors = set()
    for remainder in remainders.values():
        pair = rectangle_factor_pair(remainder)
        if pair is None:
            return FactorizedBranchResult(
                "unfactorized", None, (), (), (), 0, 0, 0
            )
        factor_pairs.append(pair)
        all_factors.update(pair)

    factors = tuple(sorted(all_factors))
    factor_index = {factor: index for index, factor in enumerate(factors)}
    clauses = tuple(sorted(set(
        tuple(sorted(set(factor_index[factor] for factor in pair)))
        for pair in factor_pairs
    )))
    if not clauses:
        raise ValueError("at least one nonzero remainder is required")

    branches = 0
    inconsistent = 0
    pure_zero = 0
    with Solver(
        name=solver_name,
        bootstrap_with=[[index + 1 for index in clause] for clause in clauses],
    ) as solver:
        solver.set_phases([-(index + 1) for index in range(len(factors))])
        while solver.solve():
            positive = {literal for literal in solver.get_model() if literal > 0}
            selected = _minimal_cover(
                (index for index in range(len(factors)) if index + 1 in positive),
                clauses,
            )
            branches += 1
            extra_rows = [factors[index][0] for index in selected]
            rhs = base_rhs + [factors[index][1] for index in selected]
            consistent, lattice = toric.signed_quotient_lattice(
                list(base_rows) + extra_rows, len(cells), rhs
            )
            if not consistent:
                inconsistent += 1
            else:
                pure_product, _classes = toric.reduced_constant_product(
                    size, fibres, lattice, cells, cell_index
                )
                if pure_product:
                    return FactorizedBranchResult(
                        "survivor", lattice, selected, factors, clauses,
                        branches, inconsistent, pure_zero,
                    )
                pure_zero += 1

            # Inconsistency and an identically zero pure product are both
            # monotone under adjoining further binomial relations, so this
            # clause soundly removes every Boolean superset of the branch.
            solver.add_clause([-(index + 1) for index in selected])

    return FactorizedBranchResult(
        "exhausted", None, (), factors, clauses,
        branches, inconsistent, pure_zero,
    )
