#!/usr/bin/env python3
"""CEGAR probe for the parallel-cell binomial incidence conjecture.

Unlike ``search_monomial_binomial_toric_cegar.py``, this search has one
Boolean variable for each of the 135 aggregate endpoint-colour cells at six
vertices.  Thus several differently coloured occurrences may lie on the
same underlying pair.  Three fixed constant perfect matchings are required.
Every mixed fibre must have support size zero or two.  Exact Smith reduction
then either returns an odd integer dependency among the binomial exponent
rows or a phase-consistent support, which refutes the incidence-only claim.

This is a discovery program.  Any survivor or short circuit printed here
must be moved to a small independent verifier before being used as a proof.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import reduce
from itertools import combinations, product
from math import gcd

from pysat.solvers import Solver
from sympy import Matrix, ilcm

from search_monomial_binomial_toric_cegar import (
    exact_phase_solution,
    smith_relation,
)
from verify_valuation_rainbow_descent_cycle import (
    N,
    P0,
    P1,
    P2,
    perfect_matchings,
)


Q = 3


class Pool:
    def __init__(self):
        self.top = 0

    def new(self):
        self.top += 1
        return self.top


def build_formula():
    pool = Pool()
    cells = tuple(
        (u, v, a, b)
        for u, v in combinations(range(N), 2)
        for a, b in product(range(Q), repeat=2)
    )
    cell_index = {cell: index for index, cell in enumerate(cells)}
    support = {cell: pool.new() for cell in cells}
    matchings = tuple(perfect_matchings())
    clauses = []

    for target in (P0, P1, P2):
        for cell in target:
            clauses.append([support[cell]])

    term_variables = {}
    term_cells = {}
    for coloring in product(range(Q), repeat=N):
        fibre = []
        for matching_number, matching in enumerate(matchings):
            decorated = tuple(
                (u, v, coloring[u], coloring[v]) for u, v in matching
            )
            term = pool.new()
            term_variables[coloring, matching_number] = term
            term_cells[coloring, matching_number] = decorated
            fibre.append(term)
            for cell in decorated:
                clauses.append([-term, support[cell]])
            clauses.append([-support[cell] for cell in decorated] + [term])

        if len(set(coloring)) == 1:
            continue
        # No singleton: each supported term has a distinct mate.
        for term in fibre:
            clauses.append([-term] + [other for other in fibre if other != term])
        # At most two terms.
        clauses.extend([-a, -b, -c] for a, b, c in combinations(fibre, 3))

    return (
        pool,
        clauses,
        cells,
        cell_index,
        support,
        matchings,
        term_variables,
        term_cells,
    )


def decode(model, support):
    positive = {literal for literal in model if literal > 0}
    return frozenset(cell for cell, variable in support.items() if variable in positive)


def exact_fibres(selected, matchings):
    answer = {}
    for coloring in product(range(Q), repeat=N):
        terms = []
        for matching_number, matching in enumerate(matchings):
            decorated = tuple(
                (u, v, coloring[u], coloring[v]) for u, v in matching
            )
            if set(decorated) <= selected:
                terms.append((matching_number, decorated))
        if terms:
            answer[coloring] = tuple(terms)
    return answer


def exponent_row(left, right, cell_index, number_cells):
    row = [0] * number_cells
    for cell in left:
        row[cell_index[cell]] += 1
    for cell in right:
        row[cell_index[cell]] -= 1
    return row


def fast_odd_relation(rows):
    """Find a certified odd relation from a rational nullspace basis.

    This is only a fast discovery filter: returning ``None`` is not a
    consistency certificate, because a rational echelon basis need not be a
    saturated integer-kernel basis.  Every returned vector is independently
    checked over the integers.
    """
    if not rows:
        return None
    for vector in Matrix(rows).T.nullspace():
        denominator = ilcm(*[entry.q for entry in vector])
        relation = [int(entry * denominator) for entry in vector]
        divisor = reduce(gcd, (abs(value) for value in relation if value), 0)
        relation = [value // divisor for value in relation]
        if sum(relation) % 2 == 0:
            continue
        assert all(
            sum(relation[row] * rows[row][column] for row in range(len(rows))) == 0
            for column in range(len(rows[0]))
        )
        return relation
    return None


def run(max_rounds, verbose):
    (
        pool,
        clauses,
        cells,
        cell_index,
        support,
        matchings,
        _term_variables,
        _term_cells,
    ) = build_formula()
    print(
        f"formula: variables={pool.top}, clauses={len(clauses)}, "
        f"cells={len(cells)}",
        flush=True,
    )

    solver = Solver(name="cadical195", bootstrap_with=clauses)
    for round_number in range(max_rounds):
        if not solver.solve():
            solver.delete()
            print(f"UNSAT after {round_number} odd-lattice cuts", flush=True)
            return None

        selected = decode(solver.get_model(), support)
        fibres = exact_fibres(selected, matchings)
        mixed = [
            (coloring, terms)
            for coloring, terms in sorted(fibres.items())
            if len(set(coloring)) > 1
        ]
        assert all(len(terms) == 2 for _, terms in mixed)
        rows = [
            exponent_row(terms[0][1], terms[1][1], cell_index, len(cells))
            for _, terms in mixed
        ]
        relation = fast_odd_relation(rows)
        if relation is None:
            # The exact saturated test is needed before declaring a survivor.
            relation = smith_relation(rows, [1] * len(rows))
        if relation is None:
            phases = exact_phase_solution(rows, [1] * len(rows))
            solver.delete()
            print(
                f"SAT phase-consistent support at round={round_number}: "
                f"cells={len(selected)}, fibres="
                f"{dict(sorted(Counter(map(len, fibres.values())).items()))}",
                flush=True,
            )
            for cell in sorted(selected):
                print(f"  {cell} phase={phases[cell_index[cell]]}*pi")
            return selected, fibres, phases

        used = [index for index, coefficient in enumerate(relation) if coefficient]
        literals = {
            support[cell]
            for index in used
            for _, decorated in mixed[index][1]
            for cell in decorated
        }
        solver.add_clause([-literal for literal in literals])
        if verbose or round_number % 100 == 0:
            print(
                f"round={round_number}: cells={len(selected)}, "
                f"mixed_binomials={len(mixed)}, odd_support={len(used)}, "
                f"cut_cells={len(literals)}",
                flush=True,
            )
            if verbose:
                for index in used:
                    print(
                        f"  {relation[index]:+d} "
                        f"{''.join(map(str, mixed[index][0]))}",
                        flush=True,
                    )

    solver.delete()
    raise RuntimeError(f"reached max_rounds={max_rounds}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rounds", type=int, default=10000)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    run(args.max_rounds, args.verbose)


if __name__ == "__main__":
    main()
