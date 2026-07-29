#!/usr/bin/env python3
"""Exact MaxSAT minimum for completing the thirteen-cell plateau support.

All thirteen cells from ``verify_valuation_rainbow_descent_cycle.py`` are
fixed present.  The remaining 122 aggregate cells are optional and carry a
unit soft cost.  Tseitin variables encode every decorated perfect-matching
term.  For each mixed coloring, every supported term is required to have a
distinct supported mate.  RC2 proves that the minimum number of added cells
is eighteen.  The independently audited completion in
``verify_valuation_rainbow_plateau_completion.py`` attains that bound and,
more strongly, makes every nonempty mixed fibre binomial.
"""

from itertools import combinations, product

from pysat.examples.rc2 import RC2
from pysat.formula import IDPool, WCNF

import verify_valuation_rainbow_descent_cycle as base
from verify_valuation_rainbow_plateau_completion import ADDITIONS


def build_formula():
    cells = tuple(
        (u, v, a, b)
        for u, v in combinations(range(base.N), 2)
        for a, b in product(base.COLORS, repeat=2)
    )
    fixed = frozenset(base.ENTRIES)
    pool = IDPool()
    support = {cell: pool.id(("cell", cell)) for cell in cells}
    formula = WCNF()

    for cell in cells:
        if cell in fixed:
            formula.append([support[cell]])
        else:
            formula.append([-support[cell]], weight=1)

    for coloring in product(base.COLORS, repeat=base.N):
        terms = []
        for number, matching in enumerate(base.perfect_matchings()):
            decorated = tuple(
                (u, v, coloring[u], coloring[v]) for u, v in matching
            )
            term = pool.id(("term", coloring, number))
            terms.append(term)
            for cell in decorated:
                formula.append([-term, support[cell]])
            formula.append([-support[cell] for cell in decorated] + [term])

        if len(set(coloring)) == 1:
            continue
        for term in terms:
            formula.append([-term] + [other for other in terms if other != term])

    return formula, cells, fixed, support


def no_mixed_singleton(selected):
    for coloring in product(base.COLORS, repeat=base.N):
        if len(set(coloring)) == 1:
            continue
        count = 0
        for matching in base.perfect_matchings():
            decorated = {
                (u, v, coloring[u], coloring[v]) for u, v in matching
            }
            count += decorated <= selected
        if count == 1:
            return False
    return True


def main():
    formula, cells, fixed, support = build_formula()
    optimizer = RC2(
        formula,
        solver="cadical195",
        adapt=False,
        verbose=0,
    )
    model = optimizer.compute()
    assert model is not None
    assert optimizer.cost == 18
    positive = {literal for literal in model if literal > 0}
    selected = frozenset(cell for cell in cells if support[cell] in positive)
    optimizer.delete()

    assert fixed <= selected
    assert len(selected - fixed) == 18
    assert no_mixed_singleton(selected)

    hardcoded = fixed | ADDITIONS
    assert len(ADDITIONS) == 18
    assert no_mixed_singleton(hardcoded)

    print(
        "verified exact completion optimum: at least 18 cells must be added "
        "to the fixed 13-cell support to remove every mixed singleton"
    )
    print(
        "verified hardcoded 18-cell completion attains the optimum "
        "(its stronger 0/2 fiber audit is separate)"
    )


if __name__ == "__main__":
    main()
