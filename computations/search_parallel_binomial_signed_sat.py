#!/usr/bin/env python3
"""Exact +/-1 search for parallel-cell binomial Krenn counterexamples.

Every supported aggregate cell has a sign.  Every nonempty mixed fibre has
exactly two terms and their sign products are required to be opposite.
Each complete constant fibre has nonzero signed sum (not merely one selected
term).  Thus any SAT model is an exact integer-weight counterexample.

The current explicit fibre-cardinality encoding is sized for n=6.  Running
all twelve target-matching orbits is exhaustive for +/-1 weights with
arbitrary parallel decorated cells at that order.
"""

from __future__ import annotations

import argparse

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

import search_parallel_binomial_nonzero_constants_cegar as core


def xor_gate(clauses, pool, left, right):
    output = pool.new()
    clauses.extend((
        [-left, -right, -output],
        [left, right, -output],
        [left, -right, output],
        [-left, right, output],
    ))
    return output


def parity_gate(clauses, pool, literals):
    assert literals
    if len(literals) == 1:
        return literals[0]
    current = xor_gate(clauses, pool, literals[0], literals[1])
    for literal in literals[2:]:
        current = xor_gate(clauses, pool, current, literal)
    return current


def conjunction_with_literal(clauses, pool, term, parity, negative):
    """Return term & parity if negative, otherwise term & ~parity."""

    output = pool.new()
    signed_parity = parity if negative else -parity
    clauses.extend((
        [-output, term],
        [-output, signed_parity],
        [-term, -signed_parity, output],
    ))
    return output


def conditional_atleast(clauses, pool, literals, bound, condition):
    encoding = CardEnc.atleast(
        lits=literals,
        bound=bound,
        top_id=pool.top,
        encoding=EncType.seqcounter,
    )
    pool.top = encoding.nv
    clauses.extend([-condition] + clause for clause in encoding.clauses)


def build_signed_formula(size, targets, unique_constants=False):
    (
        pool,
        clauses,
        cells,
        _cell_index,
        support,
        matchings,
        term_variables,
        term_cells,
    ) = core.build_formula(size, targets)
    sign = {cell: pool.new() for cell in cells}
    term_parity = {}
    for key, decorated in term_cells.items():
        term_parity[key] = parity_gate(
            clauses, pool, [sign[cell] for cell in decorated]
        )

    if unique_constants:
        target_sets = [set(matching) for matching in targets]
        for color in range(core.Q):
            coloring = (color,) * size
            for matching_number, matching in enumerate(matchings):
                if set(matching) != target_sets[color]:
                    clauses.append([-term_variables[coloring, matching_number]])

    # Since structural clauses allow at most two mixed terms, every supported
    # pair is the whole fibre and must have opposite product signs.
    for coloring in sorted({key[0] for key in term_variables}):
        if len(set(coloring)) == 1:
            continue
        for first in range(len(matchings)):
            for second in range(first + 1, len(matchings)):
                left_term = term_variables[coloring, first]
                right_term = term_variables[coloring, second]
                left_parity = term_parity[coloring, first]
                right_parity = term_parity[coloring, second]
                clauses.extend((
                    [-left_term, -right_term, left_parity, right_parity],
                    [-left_term, -right_term, -left_parity, -right_parity],
                ))

    # A direction bit selects positive or negative strict imbalance in each
    # complete constant fibre.  For N terms,
    #   positive-negative >= 1
    # is the cardinality constraint
    #   sum(positive_i, not negative_i) >= N+1.
    for color in range(core.Q):
        coloring = (color,) * size
        positive = []
        negative = []
        for matching_number in range(len(matchings)):
            term = term_variables[coloring, matching_number]
            parity = term_parity[coloring, matching_number]
            positive.append(conjunction_with_literal(
                clauses, pool, term, parity, negative=False
            ))
            negative.append(conjunction_with_literal(
                clauses, pool, term, parity, negative=True
            ))
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
        term_parity,
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
        _term_parity,
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


def run_orbit(size, orbit, targets, unique_constants=False):
    data = build_signed_formula(size, targets, unique_constants)
    pool, clauses = data[:2]
    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        satisfiable = solver.solve()
        if not satisfiable:
            print(
                f"orbit={orbit} UNSAT variables={pool.top} "
                f"clauses={len(clauses)}",
                flush=True,
            )
            return None
        positive = {literal for literal in solver.get_model() if literal > 0}
    selected, weights, fibres = verify_model(size, positive, data)
    print(
        f"orbit={orbit} SAT cells={len(selected)} variables={pool.top} "
        f"clauses={len(clauses)}",
        flush=True,
    )
    for cell in sorted(selected):
        print(" ", cell, weights[cell])
    return selected, weights, fibres


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int)
    parser.add_argument("--unique-constants", action="store_true")
    args = parser.parse_args()
    size = 6
    orbits = core.target_orbits(size)
    indices = range(len(orbits)) if args.orbit is None else (args.orbit,)
    print(f"n={size} target_orbits={len(orbits)}", flush=True)
    for orbit in indices:
        result = run_orbit(
            size, orbit, orbits[orbit], args.unique_constants
        )
        if result is not None:
            return
    print("all target orbits UNSAT")


if __name__ == "__main__":
    main()
