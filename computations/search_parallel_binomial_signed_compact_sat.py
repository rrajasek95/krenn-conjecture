#!/usr/bin/env python3
"""Compact exact signed-binomial SAT search for n=6 (and probes at n=8).

For a mixed fibre, split supported matching terms by the parity of their
cell signs.  Requiring at most one term of each parity and equality of the
two nonempty flags says exactly that the fibre is empty or is an
opposite-sign binomial.  This linear-size encoding replaces explicit
matching triples and pairs.

The three complete constant-fibre sums are constrained to be nonzero by a
selected strict sign imbalance.  Therefore every SAT model is independently
an exact +/-1 Krenn counterexample with arbitrary parallel decorated cells.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

import search_parallel_binomial_nonzero_constants_cegar as core
from search_parallel_binomial_signed_sat import (
    conjunction_with_literal,
    conditional_atleast,
    parity_gate,
)


def at_most_one(clauses, pool, literals):
    encoding = CardEnc.atmost(
        lits=literals,
        bound=1,
        top_id=pool.top,
        encoding=EncType.seqcounter,
    )
    pool.top = encoding.nv
    clauses.extend(encoding.clauses)


def nonempty_flag(clauses, pool, literals):
    flag = pool.new()
    clauses.extend([-literal, flag] for literal in literals)
    clauses.append([-flag] + list(literals))
    return flag


def build_formula(size, targets, unique_constants=False):
    pool = core.Pool()
    cells = tuple(
        (u, v, a, b)
        for u, v in combinations(range(size), 2)
        for a, b in product(range(core.Q), repeat=2)
    )
    support = {cell: pool.new() for cell in cells}
    sign = {cell: pool.new() for cell in cells}
    matchings = tuple(core.perfect_matchings(tuple(range(size))))
    clauses = []

    for color, matching in enumerate(targets):
        for u, v in matching:
            clauses.append([support[u, v, color, color]])
            # Stub-sign gauge makes every selected constant cell positive:
            # the selected occurrences form disjoint edges on the 3n stubs.
            clauses.append([-sign[u, v, color, color]])

    target_sets = [set(matching) for matching in targets]
    term_variables = {}
    term_cells = {}
    term_parity = {}
    term_positive = {}
    term_negative = {}

    for coloring in product(range(core.Q), repeat=size):
        for matching_number, matching in enumerate(matchings):
            key = coloring, matching_number
            decorated = tuple(
                (u, v, coloring[u], coloring[v]) for u, v in matching
            )
            term_cells[key] = decorated
            term = term_variables[key] = pool.new()
            for cell in decorated:
                clauses.append([-term, support[cell]])
            clauses.append([-support[cell] for cell in decorated] + [term])
            parity = term_parity[key] = parity_gate(
                clauses, pool, [sign[cell] for cell in decorated]
            )
            term_positive[key] = conjunction_with_literal(
                clauses, pool, term, parity, negative=False
            )
            term_negative[key] = conjunction_with_literal(
                clauses, pool, term, parity, negative=True
            )

            if (
                unique_constants
                and len(set(coloring)) == 1
                and set(matching) != target_sets[coloring[0]]
            ):
                clauses.append([-term])

    for coloring in product(range(core.Q), repeat=size):
        if len(set(coloring)) == 1:
            continue
        positive = [
            term_positive[coloring, number]
            for number in range(len(matchings))
        ]
        negative = [
            term_negative[coloring, number]
            for number in range(len(matchings))
        ]
        at_most_one(clauses, pool, positive)
        at_most_one(clauses, pool, negative)
        positive_nonempty = nonempty_flag(clauses, pool, positive)
        negative_nonempty = nonempty_flag(clauses, pool, negative)
        clauses.extend((
            [-positive_nonempty, negative_nonempty],
            [positive_nonempty, -negative_nonempty],
        ))

    for color in range(core.Q):
        coloring = (color,) * size
        positive = [
            term_positive[coloring, number]
            for number in range(len(matchings))
        ]
        negative = [
            term_negative[coloring, number]
            for number in range(len(matchings))
        ]
        direction = pool.new()
        number_terms = len(matchings)
        conditional_atleast(
            clauses,
            pool,
            positive + [-literal for literal in negative],
            number_terms + 1,
            direction,
        )
        conditional_atleast(
            clauses,
            pool,
            negative + [-literal for literal in positive],
            number_terms + 1,
            -direction,
        )

    return (
        pool,
        clauses,
        cells,
        support,
        sign,
        matchings,
        term_variables,
        term_cells,
    )


def verify_model(size, positive_model, data):
    (
        _pool,
        _clauses,
        cells,
        support,
        sign,
        matchings,
        _term_variables,
        _term_cells,
    ) = data
    selected = frozenset(
        cell for cell in cells if support[cell] in positive_model
    )
    weights = {
        cell: (-1 if sign[cell] in positive_model else 1)
        for cell in selected
    }
    fibres = core.exact_fibres(size, selected, matchings)
    for coloring, terms in fibres.items():
        values = []
        for _matching_number, decorated in terms:
            value = 1
            for cell in decorated:
                value *= weights[cell]
            values.append(value)
        if len(set(coloring)) > 1:
            assert len(values) == 2 and sum(values) == 0
        else:
            assert sum(values) != 0
    return selected, weights, fibres


def run_orbit(size, orbit, targets, unique_constants=False,
              solver_name="cadical195"):
    data = build_formula(size, targets, unique_constants)
    pool, clauses = data[:2]
    print(
        f"orbit={orbit} built variables={pool.top} clauses={len(clauses)}",
        flush=True,
    )
    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        satisfiable = solver.solve()
        if not satisfiable:
            print(f"orbit={orbit} UNSAT", flush=True)
            return None
        positive = {literal for literal in solver.get_model() if literal > 0}
    selected, weights, fibres = verify_model(size, positive, data)
    print(f"orbit={orbit} SAT cells={len(selected)}", flush=True)
    for cell in sorted(selected):
        print(" ", cell, weights[cell])
    return selected, weights, fibres


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, choices=(6, 8), default=6)
    parser.add_argument("--orbit", type=int)
    parser.add_argument("--unique-constants", action="store_true")
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()
    orbits = core.target_orbits(args.n)
    indices = range(len(orbits)) if args.orbit is None else (args.orbit,)
    print(f"n={args.n} target_orbits={len(orbits)}", flush=True)
    for orbit in indices:
        result = run_orbit(
            args.n, orbit, orbits[orbit], args.unique_constants,
            args.solver,
        )
        if result is not None:
            return
    print("all target orbits UNSAT")


if __name__ == "__main__":
    main()
